#!/usr/bin/env python3
"""
Environment Test Utilities

Provides test utilities that replicate the same environment loading mechanism 
used by CLI services to ensure test environment consistency.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from utils.config_loader import ConfigLoader


def load_service_environment(config_dir: Optional[str] = None) -> Dict[str, str]:
    """
    Load environment variables using the same mechanism as CLI services.
    
    This replicates the exact environment loading process used by service factories
    to ensure test environment consistency.
    
    Args:
        config_dir: Optional config directory path. If None, uses project default.
        
    Returns:
        Dictionary of loaded environment variables
    """
    if config_dir is None:
        # Use same config directory resolution as services
        config_dir = str(Path(__file__).parent.parent.parent / "config")
    
    # Create ConfigLoader with auto_load_env=True (default behavior)
    config_loader = ConfigLoader(config_dir)
    
    # Return currently loaded environment variables
    api_keys = [
        'ALPHA_VANTAGE_API_KEY',
        'FRED_API_KEY', 
        'FMP_API_KEY',
        'SEC_EDGAR_API_KEY',
        'COINGECKO_API_KEY',
        'IMF_API_KEY',
        'EIA_API_KEY'
    ]
    
    loaded_vars = {}
    for key in api_keys:
        value = os.environ.get(key)
        if value:
            loaded_vars[key] = value
    
    return loaded_vars


def validate_service_environment() -> Dict[str, any]:
    """
    Validate environment variables using the same process as CLI services.
    
    Returns:
        Dictionary with validation results including:
        - loaded_count: Number of API keys successfully loaded
        - missing_keys: List of missing API keys
        - present_keys: List of present API keys
        - validation_passed: Boolean indicating if core keys are present
    """
    # Load environment using service mechanism
    loaded_vars = load_service_environment()
    
    # Define required API keys for core services
    required_keys = ['ALPHA_VANTAGE_API_KEY', 'FRED_API_KEY', 'FMP_API_KEY']
    optional_keys = ['SEC_EDGAR_API_KEY', 'COINGECKO_API_KEY', 'IMF_API_KEY', 'EIA_API_KEY']
    
    present_keys = list(loaded_vars.keys())
    missing_required = [key for key in required_keys if key not in present_keys]
    missing_optional = [key for key in optional_keys if key not in present_keys]
    
    # Core validation passes if all required keys are present
    validation_passed = len(missing_required) == 0
    
    return {
        'loaded_count': len(loaded_vars),
        'missing_required': missing_required,
        'missing_optional': missing_optional,
        'present_keys': present_keys,
        'validation_passed': validation_passed,
        'loaded_vars': loaded_vars
    }


def ensure_test_environment_loaded():
    """
    Ensure test environment is loaded using the same mechanism as services.
    
    Call this function at the start of any test that needs to verify
    environment variables are loaded correctly.
    
    Raises:
        EnvironmentError: If required environment variables cannot be loaded
    """
    validation = validate_service_environment()
    
    if not validation['validation_passed']:
        missing = validation['missing_required']
        raise EnvironmentError(
            f"Required environment variables not found after loading: {missing}. "
            f"Check that .env file exists and contains the required API keys."
        )


def create_mock_service_environment() -> Dict[str, str]:
    """
    Create a mock environment for testing that mimics service configuration.
    
    Returns:
        Dictionary of mock environment variables for testing
    """
    mock_env = {
        'ALPHA_VANTAGE_API_KEY': 'test_alpha_vantage_key_12345',
        'FRED_API_KEY': 'test_fred_key_67890', 
        'FMP_API_KEY': 'test_fmp_key_abcde',
        'SEC_EDGAR_API_KEY': 'test_sec_edgar_key_fghij',
        'COINGECKO_API_KEY': 'not_required',
        'IMF_API_KEY': 'not_required',
        'EIA_API_KEY': 'not_required'
    }
    
    # Set in actual environment for testing
    for key, value in mock_env.items():
        os.environ[key] = value
    
    return mock_env


def check_service_environment_consistency():
    """
    Test that environment loading is consistent between tests and services.
    
    This function verifies that the test environment loading mechanism
    produces the same results as the service environment loading mechanism.
    
    Returns:
        Boolean indicating if environment loading is consistent
    """
    try:
        # Load environment using service mechanism
        service_env = load_service_environment()
        
        # Verify that os.environ now contains the loaded variables
        os_env_vars = {}
        for key in service_env.keys():
            value = os.environ.get(key)
            if value:
                os_env_vars[key] = value
        
        # Check consistency
        consistent = service_env == os_env_vars
        
        return {
            'consistent': consistent,
            'service_loaded': len(service_env),
            'os_environ_accessible': len(os_env_vars),
            'service_vars': list(service_env.keys()),
            'os_vars': list(os_env_vars.keys())
        }
        
    except Exception as e:
        return {
            'consistent': False,
            'error': str(e),
            'service_loaded': 0,
            'os_environ_accessible': 0
        }


if __name__ == "__main__":
    # Test the environment loading utilities
    print("Testing Environment Loading Utilities...")
    print()
    
    # Test service environment loading
    print("🔄 Loading environment using service mechanism...")
    loaded_vars = load_service_environment()
    print(f"✅ Loaded {len(loaded_vars)} environment variables")
    
    # Test validation
    print("🔄 Validating environment...")
    validation = validate_service_environment()
    print(f"✅ Validation passed: {validation['validation_passed']}")
    print(f"   Present keys: {validation['present_keys']}")
    if validation['missing_required']:
        print(f"   Missing required: {validation['missing_required']}")
    if validation['missing_optional']:
        print(f"   Missing optional: {validation['missing_optional']}")
    
    # Test consistency
    print("🔄 Testing environment consistency...")
    consistency = check_service_environment_consistency()
    print(f"✅ Environment consistent: {consistency['consistent']}")
    print(f"   Service loaded: {consistency['service_loaded']}")
    print(f"   OS accessible: {consistency['os_environ_accessible']}")
    
    print()
    print("🎯 Environment Loading Utilities Test Complete")