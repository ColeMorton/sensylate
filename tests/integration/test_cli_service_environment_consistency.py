#!/usr/bin/env python3
"""
CLI Service Environment Consistency Tests

TDD tests that verify environment loading consistency between tests and services.
These tests demonstrate the correct way to test environment-dependent services.
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

# Import test utilities
test_utils_path = Path(__file__).parent.parent / "utils"
sys.path.insert(0, str(test_utils_path))
from environment_test_helpers import (
    load_service_environment,
    validate_service_environment,
    ensure_test_environment_loaded,
    check_service_environment_consistency
)

# Import services
from services.economic_calendar import create_economic_calendar_service
from services.global_liquidity_monitor import create_global_liquidity_monitor
from services.sector_economic_correlations import create_sector_economic_correlations
from services.alpha_vantage import create_alpha_vantage_service


class TestEnvironmentLoadingConsistency:
    """Test environment loading consistency between tests and services"""
    
    def test_environment_loading_mechanism_consistency(self):
        """Test that environment loading is consistent between tests and services"""
        # Test the consistency mechanism itself
        consistency_result = check_service_environment_consistency()
        
        assert consistency_result['consistent'], \
            f"Environment loading inconsistent: {consistency_result}"
        assert consistency_result['service_loaded'] > 0, \
            "No environment variables loaded by service mechanism"
        assert consistency_result['os_environ_accessible'] > 0, \
            "Environment variables not accessible via os.environ after loading"
    
    def test_service_environment_validation(self):
        """Test that service environment validation works correctly"""
        # Load environment using service mechanism
        validation = validate_service_environment()
        
        # Should pass validation with required keys
        assert validation['validation_passed'], \
            f"Environment validation failed: missing {validation['missing_required']}"
        
        # Should have loaded multiple variables
        assert validation['loaded_count'] >= 3, \
            f"Expected at least 3 API keys, got {validation['loaded_count']}"
        
        # Should have all required keys
        required_keys = ['ALPHA_VANTAGE_API_KEY', 'FRED_API_KEY', 'FMP_API_KEY']
        for key in required_keys:
            assert key in validation['present_keys'], \
                f"Required key {key} not found in loaded environment"
    
    def test_ensure_test_environment_loaded_success(self):
        """Test that ensure_test_environment_loaded works correctly for valid environment"""
        # This should not raise an exception if environment is properly loaded
        try:
            ensure_test_environment_loaded()
        except EnvironmentError as e:
            pytest.fail(f"Environment loading failed unexpectedly: {e}")
    
    def test_ensure_test_environment_loaded_failure(self):
        """Test that ensure_test_environment_loaded fails correctly for invalid environment"""
        # Patch both os.environ and the ConfigLoader to simulate complete failure
        with patch.dict('os.environ', {}, clear=True):
            with patch('environment_test_helpers.ConfigLoader') as mock_loader:
                # Make ConfigLoader fail to load environment
                mock_loader.side_effect = Exception("Config loading failed")
                
                with pytest.raises(EnvironmentError) as exc_info:
                    ensure_test_environment_loaded()
                
                assert "Required environment variables not found" in str(exc_info.value)


class TestCLIServiceEnvironmentIntegration:
    """Test CLI services using correct environment loading mechanism"""
    
    def setup_method(self):
        """Ensure environment is loaded before each test"""
        ensure_test_environment_loaded()
    
    def test_economic_calendar_service_with_proper_environment(self):
        """Test economic calendar service with properly loaded environment"""
        # Load environment using service mechanism
        loaded_vars = load_service_environment()
        assert 'FRED_API_KEY' in loaded_vars, "FRED_API_KEY not loaded"
        
        # Create service (should work with loaded environment)
        service = create_economic_calendar_service('dev')
        assert service is not None, "Economic calendar service creation failed"
        
        # Test health check
        health = service.health_check()
        assert health['status'] == 'healthy', f"Service unhealthy: {health}"
        assert health.get('api_key_configured', False), "API key not configured in service"
    
    def test_global_liquidity_monitor_with_proper_environment(self):
        """Test global liquidity monitor with properly loaded environment"""
        # Load environment using service mechanism  
        loaded_vars = load_service_environment()
        assert 'FRED_API_KEY' in loaded_vars, "FRED_API_KEY not loaded"
        
        # Create service
        service = create_global_liquidity_monitor('dev')
        assert service is not None, "Global liquidity monitor creation failed"
        
        # Test health check
        health = service.health_check()
        assert health['status'] == 'healthy', f"Service unhealthy: {health}"
        assert health.get('api_key_configured', False), "API key not configured in service"
    
    def test_sector_correlations_service_with_proper_environment(self):
        """Test sector correlations service with properly loaded environment"""
        # Load environment using service mechanism
        loaded_vars = load_service_environment()
        assert 'FRED_API_KEY' in loaded_vars, "FRED_API_KEY not loaded"
        
        # Create service
        service = create_sector_economic_correlations('dev')
        assert service is not None, "Sector correlations service creation failed"
        
        # Test health check
        health = service.health_check()
        assert health['status'] == 'healthy', f"Service unhealthy: {health}"
        assert health.get('api_key_configured', False), "API key not configured in service"
    
    def test_alpha_vantage_service_with_proper_environment(self):
        """Test Alpha Vantage service with properly loaded environment"""
        # Load environment using service mechanism
        loaded_vars = load_service_environment()
        assert 'ALPHA_VANTAGE_API_KEY' in loaded_vars, "ALPHA_VANTAGE_API_KEY not loaded"
        
        # Create service
        service = create_alpha_vantage_service('dev')
        assert service is not None, "Alpha Vantage service creation failed"
        
        # Test health check
        health = service.health_check()
        assert health['status'] == 'healthy', f"Service unhealthy: {health}"
        # Note: Alpha Vantage has different health check format
        assert 'test_result' in health, "Alpha Vantage health check missing test result"
    
    def test_all_cli_services_environment_summary(self):
        """Test all CLI services and provide environment summary"""
        # Load environment using proper mechanism
        validation = validate_service_environment()
        
        services = [
            ('Economic Calendar', create_economic_calendar_service),
            ('Global Liquidity Monitor', create_global_liquidity_monitor),
            ('Sector Correlations', create_sector_economic_correlations),
            ('Alpha Vantage', create_alpha_vantage_service)
        ]
        
        operational_count = 0
        total_count = len(services)
        service_results = {}
        
        for name, factory in services:
            try:
                service = factory('dev')
                if service:
                    health = service.health_check()
                    status = health.get('status', 'unknown')
                    if status == 'healthy':
                        operational_count += 1
                        service_results[name] = 'healthy'
                    else:
                        service_results[name] = f'unhealthy: {status}'
                else:
                    service_results[name] = 'creation failed'
            except Exception as e:
                service_results[name] = f'error: {str(e)[:50]}...'
        
        # Assert that all services are operational
        success_rate = operational_count / total_count
        assert success_rate >= 0.8, \
            f"CLI service success rate {success_rate:.1%} below 80%. Results: {service_results}"
        
        # Verify environment was properly loaded
        assert validation['validation_passed'], \
            f"Environment validation failed: missing {validation['missing_required']}"
        
        # Log success for visibility
        print(f"\n✅ CLI Services Status: {operational_count}/{total_count} operational ({success_rate:.1%})")
        print(f"   Environment Variables: {validation['loaded_count']} loaded")
        print(f"   Service Results: {service_results}")


class TestEnvironmentLoadingErrorCases:
    """Test error cases and edge conditions in environment loading"""
    
    def test_missing_config_directory_handling(self):
        """Test handling of missing config directory"""
        # Try to load with non-existent config directory
        try:
            loaded_vars = load_service_environment("/nonexistent/config/dir")
            # Should still work by falling back to auto-detection
            assert isinstance(loaded_vars, dict)
        except Exception as e:
            # If it fails, should fail gracefully
            assert "not found" in str(e).lower() or "no such file" in str(e).lower()
    
    def test_partial_environment_loading(self):
        """Test behavior with partially loaded environment"""
        # Temporarily remove one key to test partial loading
        original_value = None
        if 'FMP_API_KEY' in os.environ:
            original_value = os.environ['FMP_API_KEY']
            del os.environ['FMP_API_KEY']
        
        try:
            # Reload environment
            loaded_vars = load_service_environment()
            
            # Should still have other keys
            assert 'ALPHA_VANTAGE_API_KEY' in loaded_vars or 'FRED_API_KEY' in loaded_vars, \
                "No API keys loaded even with partial environment"
            
        finally:
            # Restore original value
            if original_value:
                os.environ['FMP_API_KEY'] = original_value


@pytest.mark.integration
class TestEnvironmentLoadingIntegration:
    """Integration tests for environment loading with real services"""
    
    def test_environment_loading_before_service_creation(self):
        """Test that environment loading happens before service creation"""
        # Clear relevant environment variables
        api_keys = ['ALPHA_VANTAGE_API_KEY', 'FRED_API_KEY', 'FMP_API_KEY']
        original_values = {}
        
        for key in api_keys:
            if key in os.environ:
                original_values[key] = os.environ[key]
                del os.environ[key]
        
        try:
            # Verify keys are not in environment
            for key in api_keys:
                assert os.environ.get(key) is None, f"{key} still in environment"
            
            # Load environment using service mechanism
            loaded_vars = load_service_environment()
            
            # Verify keys are now in environment
            for key in api_keys:
                if key in loaded_vars:
                    assert os.environ.get(key) is not None, \
                        f"{key} not in os.environ after loading"
            
            # Verify services can be created successfully
            service = create_economic_calendar_service('dev')
            assert service is not None, "Service creation failed after environment loading"
            
        finally:
            # Restore original environment
            for key, value in original_values.items():
                os.environ[key] = value


if __name__ == "__main__":
    # Run basic environment consistency tests
    print("Running CLI Service Environment Consistency Tests...")
    
    # Test environment loading utilities
    consistency = check_service_environment_consistency()
    print(f"Environment Consistency: {consistency['consistent']}")
    
    # Test validation
    validation = validate_service_environment()
    print(f"Environment Validation: {validation['validation_passed']}")
    print(f"Loaded Variables: {validation['loaded_count']}")
    
    print("✅ Environment consistency tests complete")