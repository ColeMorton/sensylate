#!/usr/bin/env python3
"""
Environment Loading Demonstration

This script demonstrates the difference between incorrect and correct ways
to test environment variables for CLI services, highlighting the TDD issue
that was causing false negatives.
"""

import os
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Add test utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))

from environment_test_helpers import (
    load_service_environment,
    validate_service_environment
)

# Import services to test
from services.economic_calendar import create_economic_calendar_service
from services.global_liquidity_monitor import create_global_liquidity_monitor


def demonstrate_broken_environment_testing():
    """
    Demonstrate the BROKEN way to test environment variables.

    This approach directly checks os.environ without loading environment
    the same way services do, leading to false negatives.
    """
    print("🔴 BROKEN APPROACH: Direct os.environ Check")
    print("=" * 50)

    # Check environment variables directly (the wrong way)
    api_keys = ['ALPHA_VANTAGE_API_KEY', 'FRED_API_KEY', 'FMP_API_KEY']
    missing_count = 0

    print("Checking environment variables directly...")
    for key in api_keys:
        value = os.environ.get(key)
        if value:
            print(f"  ✅ {key}: configured")
        else:
            print(f"  ❌ {key}: missing")
            missing_count += 1

    print(f"\nResult: {missing_count}/{len(api_keys)} API keys appear MISSING")

    # But let's try to create a service anyway...
    print("\nTrying to create Economic Calendar service...")
    try:
        service = create_economic_calendar_service('dev')
        if service:
            health = service.health_check()
            print(f"  Service Status: {health.get('status', 'unknown')}")
            print(f"  API Key Configured: {health.get('api_key_configured', False)}")
            print("  🤔 SERVICE WORKS despite 'missing' environment variables!")
        else:
            print("  ❌ Service creation failed")
    except Exception as e:
        print(f"  ❌ Service creation error: {e}")

    print("\n💡 This is the TDD INCONSISTENCY PROBLEM:")
    print("   - Environment check shows missing keys")
    print("   - But services work correctly")
    print("   - Test gives FALSE NEGATIVE result")


def demonstrate_correct_environment_testing():
    """
    Demonstrate the CORRECT way to test environment variables.

    This approach uses the same environment loading mechanism that
    services use, ensuring test consistency.
    """
    print("\n\n🟢 CORRECT APPROACH: Service-Consistent Environment Loading")
    print("=" * 60)

    # Load environment using the same mechanism as services
    print("Loading environment using service mechanism...")
    loaded_vars = load_service_environment()

    print(f"Environment Variables Loaded: {len(loaded_vars)}")
    for key, value in loaded_vars.items():
        if 'API_KEY' in key:
            print(f"  ✅ {key}: ****")
        else:
            print(f"  ✅ {key}: {value}")

    # Validate environment
    validation = validate_service_environment()
    print(f"\nEnvironment Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")
    print(f"Required Keys Present: {len(validation['present_keys']) - len(validation['missing_required'])}/{len(validation['present_keys'])}")

    if validation['missing_required']:
        print(f"Missing Required: {validation['missing_required']}")
    if validation['missing_optional']:
        print(f"Missing Optional: {validation['missing_optional']}")

    # Now test services
    print("\nTesting CLI Services with proper environment loading...")

    services = [
        ('Economic Calendar', create_economic_calendar_service),
        ('Global Liquidity Monitor', create_global_liquidity_monitor)
    ]

    operational_count = 0
    for name, factory in services:
        try:
            service = factory('dev')
            if service:
                health = service.health_check()
                status = health.get('status', 'unknown')
                api_configured = health.get('api_key_configured', False)

                if status == 'healthy':
                    print(f"  ✅ {name}: {status} (API: {api_configured})")
                    operational_count += 1
                else:
                    print(f"  ⚠️  {name}: {status}")
            else:
                print(f"  ❌ {name}: creation failed")
        except Exception as e:
            print(f"  ❌ {name}: error - {str(e)[:50]}...")

    success_rate = operational_count / len(services)
    print(f"\n🎯 CLI Services Result: {operational_count}/{len(services)} operational ({success_rate:.1%})")

    print("\n💡 This approach provides ACCURATE results:")
    print("   - Environment loading matches service behavior")
    print("   - Test results reflect actual service capability")
    print("   - No false negatives or misleading test failures")


def demonstrate_environment_loading_timing():
    """
    Demonstrate how environment loading timing affects test results.
    """
    print("\n\n⏰ TIMING ISSUE DEMONSTRATION")
    print("=" * 40)

    # Clear some environment variables temporarily
    api_keys = ['FRED_API_KEY', 'ALPHA_VANTAGE_API_KEY']
    original_values = {}

    print("1. Clearing environment variables...")
    for key in api_keys:
        if key in os.environ:
            original_values[key] = os.environ[key]
            del os.environ[key]
            print(f"   Cleared: {key}")

    print("\n2. Checking os.environ directly (before loading)...")
    for key in api_keys:
        value = os.environ.get(key)
        print(f"   {key}: {'present' if value else 'MISSING'}")

    print("\n3. Loading environment using service mechanism...")
    loaded_vars = load_service_environment()
    loaded_keys = [key for key in api_keys if key in loaded_vars]
    print(f"   Loaded {len(loaded_keys)} API keys: {loaded_keys}")

    print("\n4. Checking os.environ after loading...")
    for key in api_keys:
        value = os.environ.get(key)
        print(f"   {key}: {'present' if value else 'MISSING'}")

    print("\n💡 Key insight: Environment loading TIMING matters!")
    print("   - Services trigger loading during initialization")
    print("   - Tests must replicate the same loading sequence")
    print("   - Checking too early gives incorrect results")

    # Restore original values (cleanup)
    for key, value in original_values.items():
        os.environ[key] = value


def main():
    """Run the complete environment loading demonstration."""
    print("🔬 CLI Service Environment Loading Analysis")
    print("=" * 50)
    print("Demonstrating TDD environment consistency issues and solutions")
    print()

    # Show the broken approach first
    demonstrate_broken_environment_testing()

    # Show the correct approach
    demonstrate_correct_environment_testing()

    # Show timing issues
    demonstrate_environment_loading_timing()

    print("\n\n🎯 SUMMARY:")
    print("=" * 20)
    print("✅ SOLUTION: Use environment loading utilities that replicate service behavior")
    print("✅ BENEFIT: Tests accurately reflect actual service capabilities")
    print("✅ RESULT: No more false negative environment variable tests")
    print()
    print("📚 For testing CLI services, always use:")
    print("   from tests.utils.environment_test_helpers import load_service_environment")
    print("   loaded_vars = load_service_environment()")
    print()


if __name__ == "__main__":
    main()
