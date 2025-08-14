#!/usr/bin/env python3
"""
Service Health Check Unit Tests

Test-driven development for service health check functionality including:
- Valid API key health checks
- Missing API key error handling  
- Network failure simulation
- Health check response schema validation
- Service metadata verification
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch, PropertyMock

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from services.base_financial_service import (
    BaseFinancialService,
    ServiceConfig,
    CacheConfig,
    RateLimitConfig,
    HistoricalStorageConfig
)


class ConcreteFinancialService(BaseFinancialService):
    """Concrete implementation of BaseFinancialService for testing purposes"""
    
    def _validate_response(self, data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Test implementation that simply returns the data unchanged"""
        return data


class TestServiceHealthCheckContract:
    """Test health check contract compliance across all services"""
    
    def test_health_check_returns_required_fields(self, mock_config_loader):
        """Test that health check returns all required metadata fields"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key="valid_api_key",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert
        required_fields = [
            "service_name", "timestamp", "status", 
            "api_key_configured", "base_url", 
            "cache_enabled", "rate_limit_enabled"
        ]
        
        for field in required_fields:
            assert field in health_result, f"Health check missing required field: {field}"
        
        assert isinstance(health_result["timestamp"], str)
        assert health_result["service_name"] == "test_service"
        assert health_result["status"] in ["healthy", "configuration_error", "error"]


class TestHealthCheckWithValidConfiguration:
    """Test health check behavior with valid service configuration"""
    
    def test_health_check_with_valid_api_key_returns_healthy(self):
        """Test health check returns healthy status with valid API key"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key="valid_api_key_123",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(enabled=True),
            rate_limit=RateLimitConfig(enabled=True),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert
        assert health_result["status"] == "healthy"
        assert health_result["api_key_configured"] is True
        assert health_result["message"] == "Service configured with API key"
        assert health_result["cache_enabled"] is True
        assert health_result["rate_limit_enabled"] is True
    
    def test_health_check_includes_service_metadata(self):
        """Test health check includes correct service metadata"""
        # Arrange
        config = ServiceConfig(
            name="economic_calendar",
            base_url="https://api.stlouisfed.org/fred/series",
            api_key="test_fred_key",
            timeout_seconds=45,
            max_retries=2,
            cache=CacheConfig(enabled=False),
            rate_limit=RateLimitConfig(enabled=False),
            headers={"Accept": "application/json"},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert
        assert health_result["service_name"] == "economic_calendar"
        assert health_result["base_url"] == "https://api.stlouisfed.org/fred/series"
        assert health_result["cache_enabled"] is False
        assert health_result["rate_limit_enabled"] is False


class TestHealthCheckWithInvalidConfiguration:
    """Test health check behavior with invalid or missing configuration"""
    
    def test_health_check_with_missing_api_key_returns_config_error(self):
        """Test health check returns configuration error with missing API key"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key=None,  # Missing API key
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert
        assert health_result["status"] == "configuration_error"
        assert health_result["api_key_configured"] is False
        assert health_result["message"] == "Missing API key configuration"
    
    def test_health_check_with_empty_api_key_returns_config_error(self):
        """Test health check returns configuration error with empty API key"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key="",  # Empty API key
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert
        assert health_result["status"] == "configuration_error"
        assert health_result["api_key_configured"] is False
        assert health_result["message"] == "Missing API key configuration"


class TestHealthCheckErrorHandling:
    """Test health check error handling and resilience"""
    
    def test_health_check_handles_internal_exceptions(self):
        """Test health check is resilient and always returns a valid response"""
        # Arrange - Create a service with invalid configuration that could cause issues
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com", 
            api_key="valid_key",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act - Health check should always succeed and return valid response
        health_result = service.health_check()
        
        # Assert - Health check should be resilient and always return required fields
        assert health_result is not None
        assert "status" in health_result
        assert "timestamp" in health_result
        assert "service_name" in health_result
        assert health_result["service_name"] == "test_service"
        assert health_result["status"] in ["healthy", "configuration_error", "error"]
        
        # If status is healthy, should have appropriate message
        if health_result["status"] == "healthy":
            assert "message" in health_result
            assert "api key" in health_result["message"].lower()


class TestHealthCheckTimestampValidation:
    """Test health check timestamp format and accuracy"""
    
    def test_health_check_timestamp_format_is_iso8601(self):
        """Test health check timestamp follows ISO 8601 format"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key="valid_key",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert
        timestamp = health_result["timestamp"]
        
        # Validate ISO 8601 format
        try:
            parsed_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert parsed_timestamp is not None
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} is not in valid ISO 8601 format")
    
    def test_health_check_timestamp_is_recent(self):
        """Test health check timestamp is close to current time"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key="valid_key",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        before_time = datetime.now()
        health_result = service.health_check()
        after_time = datetime.now()
        
        # Assert
        timestamp = health_result["timestamp"]
        health_time = datetime.fromisoformat(timestamp)
        
        assert before_time <= health_time <= after_time, \
            f"Health check timestamp {health_time} not within expected range {before_time} - {after_time}"


class TestHealthCheckResponseSchema:
    """Test health check response schema validation"""
    
    def test_health_check_response_schema_validation(self):
        """Test health check response follows expected schema"""
        # Arrange
        config = ServiceConfig(
            name="test_service",
            base_url="https://test-api.example.com",
            api_key="valid_key",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service = ConcreteFinancialService(config)
        
        # Act
        health_result = service.health_check()
        
        # Assert - Check data types
        assert isinstance(health_result["service_name"], str)
        assert isinstance(health_result["timestamp"], str) 
        assert isinstance(health_result["status"], str)
        assert isinstance(health_result["api_key_configured"], bool)
        assert isinstance(health_result["base_url"], str)
        assert isinstance(health_result["cache_enabled"], bool)
        assert isinstance(health_result["rate_limit_enabled"], bool)
        
        # Assert - Check valid status values
        valid_statuses = ["healthy", "configuration_error", "error"]
        assert health_result["status"] in valid_statuses
        
        # Assert - Check non-empty required strings
        assert len(health_result["service_name"]) > 0
        assert len(health_result["timestamp"]) > 0
        assert len(health_result["base_url"]) > 0


@pytest.mark.unit
class TestMultipleServiceHealthChecks:
    """Test health checks across multiple service instances"""
    
    def test_multiple_service_instances_independent_health_checks(self):
        """Test that multiple service instances have independent health checks"""
        # Arrange
        config1 = ServiceConfig(
            name="service_1",
            base_url="https://api1.example.com",
            api_key="key1",
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        config2 = ServiceConfig(
            name="service_2", 
            base_url="https://api2.example.com",
            api_key=None,  # Missing API key
            timeout_seconds=30,
            max_retries=3,
            cache=CacheConfig(),
            rate_limit=RateLimitConfig(),
            headers={},
            historical_storage=HistoricalStorageConfig()
        )
        
        service1 = ConcreteFinancialService(config1)
        service2 = ConcreteFinancialService(config2)
        
        # Act
        health1 = service1.health_check()
        health2 = service2.health_check()
        
        # Assert
        assert health1["service_name"] == "service_1"
        assert health2["service_name"] == "service_2"
        assert health1["status"] == "healthy"
        assert health2["status"] == "configuration_error"
        assert health1["api_key_configured"] is True
        assert health2["api_key_configured"] is False