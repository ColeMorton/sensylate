#!/usr/bin/env python3
"""
Shared Test Fixtures and Configuration

Provides reusable test fixtures for CLI services testing including:
- Mock service configurations
- Sample API responses
- Test environment setup
- Shared test utilities
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Add test utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

# Import after adding to path
from services.base_financial_service import (
    BaseFinancialService,
    ServiceConfig,
    CacheConfig,
    RateLimitConfig,
    HistoricalStorageConfig
)

# Import environment test utilities
from environment_test_helpers import (
    load_service_environment,
    ensure_test_environment_loaded
)


class ConcreteFinancialService(BaseFinancialService):
    """Concrete implementation of BaseFinancialService for testing purposes"""

    def _validate_response(self, data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Test implementation that simply returns the data unchanged"""
        return data


@pytest.fixture
def test_financial_service():
    """Fixture that provides a configured ConcreteFinancialService instance"""
    config = ServiceConfig(
        name="test_service",
        base_url="https://test-api.example.com",
        api_key="test_api_key",
        timeout_seconds=30,
        max_retries=3,
        cache=CacheConfig(),
        rate_limit=RateLimitConfig(),
        headers={},
        historical_storage=HistoricalStorageConfig()
    )
    return ConcreteFinancialService(config)


@pytest.fixture
def mock_config_loader():
    """Mock ConfigLoader with predefined service configurations"""
    mock_loader = Mock()

    # Mock service configuration
    mock_service_config = Mock()
    mock_service_config.name = "test_service"
    mock_service_config.base_url = "https://test-api.example.com"
    mock_service_config.api_key = "test_api_key_123"
    mock_service_config.timeout_seconds = 30
    mock_service_config.max_retries = 3
    mock_service_config.cache = {
        "enabled": True,
        "ttl_seconds": 900,
        "cache_dir": "/tmp/test_cache",
        "max_size_mb": 100
    }
    mock_service_config.rate_limit = {
        "enabled": True,
        "requests_per_minute": 60,
        "burst_limit": 10
    }
    mock_service_config.headers = {"Accept": "application/json"}

    mock_loader.get_service_config.return_value = mock_service_config
    mock_loader.load_financial_services_config.return_value = {
        "services": {
            "test_service": {
                "name": "test_service",
                "base_url": "https://test-api.example.com",
                "api_key": "${TEST_API_KEY}",
                "cache": {"ttl_seconds": 900}
            }
        }
    }

    return mock_loader


@pytest.fixture
def mock_config_loader_missing_api_key():
    """Mock ConfigLoader with missing API key"""
    mock_loader = Mock()

    mock_service_config = Mock()
    mock_service_config.name = "test_service"
    mock_service_config.base_url = "https://test-api.example.com"
    mock_service_config.api_key = None  # Missing API key
    mock_service_config.timeout_seconds = 30
    mock_service_config.max_retries = 3
    mock_service_config.cache = {"enabled": True, "ttl_seconds": 900}
    mock_service_config.rate_limit = {"enabled": True, "requests_per_minute": 60}
    mock_service_config.headers = {}

    mock_loader.get_service_config.return_value = mock_service_config
    return mock_loader


@pytest.fixture
def sample_economic_calendar_response():
    """Sample economic calendar API response data"""
    return {
        "upcoming_events": [
            {
                "event_name": "Non-Farm Payrolls",
                "event_date": "2025-08-15T12:30:00Z",
                "event_type": "employment",
                "importance": "high",
                "actual": None,
                "forecast": 180.0,
                "previous": 175.0
            },
            {
                "event_name": "CPI Month-over-Month",
                "event_date": "2025-08-14T12:30:00Z",
                "event_type": "inflation",
                "importance": "high",
                "actual": 0.2,
                "forecast": 0.3,
                "previous": 0.4
            }
        ],
        "fomc_probabilities": {
            "next_meeting_date": "2025-09-18",
            "rate_cut_probability": 0.65,
            "rate_hold_probability": 0.30,
            "rate_hike_probability": 0.05
        },
        "economic_surprises": {
            "index_value": 15.2,
            "trend": "improving",
            "confidence": 0.85
        }
    }


@pytest.fixture
def sample_service_health_response():
    """Sample service health check response"""
    return {
        "service_name": "test_service",
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "api_key_configured": True,
        "base_url": "https://test-api.example.com",
        "cache_enabled": True,
        "rate_limit_enabled": True,
        "message": "Service configured with API key"
    }


@pytest.fixture
def sample_unhealthy_service_response():
    """Sample unhealthy service response"""
    return {
        "service_name": "test_service",
        "timestamp": datetime.now().isoformat(),
        "status": "configuration_error",
        "api_key_configured": False,
        "base_url": "https://test-api.example.com",
        "cache_enabled": True,
        "rate_limit_enabled": True,
        "message": "Missing API key configuration"
    }


@pytest.fixture
def temporary_config_file():
    """Create temporary configuration file for testing"""
    config_data = {
        "services": {
            "test_service": {
                "name": "test_service",
                "base_url": "https://test-api.example.com",
                "api_key": "${TEST_API_KEY}",
                "timeout_seconds": 30,
                "cache": {"enabled": True, "ttl_seconds": 900},
                "rate_limit": {"enabled": True, "requests_per_minute": 60}
            }
        },
        "global": {
            "cache": {"enabled": True, "ttl_seconds": 900},
            "rate_limiting": {"enabled": True, "default_requests_per_minute": 60}
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        import yaml
        yaml.dump(config_data, f)
        temp_file_path = f.name

    yield temp_file_path

    # Cleanup
    os.unlink(temp_file_path)


@pytest.fixture
def test_environment_variables():
    """Set up test environment variables"""
    test_env = {
        "TEST_API_KEY": "test_key_12345",
        "ALPHA_VANTAGE_API_KEY": "test_alpha_vantage_key",
        "FRED_API_KEY": "test_fred_key",
        "FMP_API_KEY": "test_fmp_key"
    }

    original_env = {}
    for key, value in test_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value

    yield test_env

    # Restore original environment
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def mock_service_factory():
    """Mock service factory that returns a properly configured service"""
    def _create_mock_service(env="test"):
        mock_service = Mock()
        mock_service.health_check.return_value = {
            "status": "healthy",
            "service_name": "test_service",
            "api_key_configured": True,
            "message": "Service configured with API key"
        }
        return mock_service

    return _create_mock_service


@pytest.fixture
def mock_failing_service_factory():
    """Mock service factory that returns None (simulating creation failure)"""
    def _create_failing_service(env="test"):
        return None

    return _create_failing_service


@pytest.fixture
def sample_volatility_parameters():
    """Sample region-specific volatility parameters"""
    return {
        "US": {"long_term_mean": 19.39, "reversion_speed": 0.150},
        "EUROPE": {"long_term_mean": 20.50, "reversion_speed": 0.150},
        "EU": {"long_term_mean": 22.30, "reversion_speed": 0.180},
        "ASIA": {"long_term_mean": 21.80, "reversion_speed": 0.120},
        "EMERGING_MARKETS": {"long_term_mean": 24.20, "reversion_speed": 0.200}
    }


@pytest.fixture
def mock_macro_synthesis():
    """Mock MacroEconomicSynthesis instance for testing"""
    mock_synthesis = Mock()
    mock_synthesis.region = "US"
    mock_synthesis.economic_calendar_data = {}
    mock_synthesis.global_liquidity_data = {}
    mock_synthesis.sector_correlation_data = {}
    mock_synthesis.service_health = {
        "economic_calendar": {"status": "pending", "error": None},
        "global_liquidity": {"status": "pending", "error": None},
        "sector_correlations": {"status": "pending", "error": None}
    }

    return mock_synthesis


@pytest.fixture(autouse=True)
def ensure_environment_loaded():
    """Automatically ensure environment is loaded before each test"""
    try:
        # Load environment using the same mechanism as services
        load_service_environment()
    except Exception:
        # If loading fails, continue with test (might be intentional for some tests)
        pass
    yield


@pytest.fixture
def loaded_environment():
    """Fixture that provides properly loaded environment variables"""
    return load_service_environment()


@pytest.fixture
def validated_environment():
    """Fixture that ensures environment is validated and provides validation results"""
    from environment_test_helpers import validate_service_environment
    validation = validate_service_environment()
    if not validation['validation_passed']:
        pytest.skip(f"Environment validation failed: missing {validation['missing_required']}")
    return validation


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically cleanup test files after each test"""
    yield

    # Cleanup any test files in common locations
    test_dirs = ["/tmp/test_cache", "/tmp/test_config"]
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)


# Custom pytest markers for better test organization
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers",
        "requires_api_key: mark test as requiring real API key"
    )
    config.addinivalue_line(
        "markers",
        "network_dependent: mark test as requiring network access"
    )
