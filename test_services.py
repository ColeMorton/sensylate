#!/usr/bin/env python3

import sys
import os
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_service_availability():
    """Test which CLI services are available"""
    service_status = {}

    services_to_test = {
        "fred_economic_cli": ("services.fred_economic", "create_fred_economic_service"),
        "imf_cli": ("services.imf", "create_imf_service"),
        "alpha_vantage_cli": ("services.alpha_vantage", "create_alpha_vantage_service"),
        "eia_energy_cli": ("services.eia_energy", "create_eia_energy_service"),
        "coingecko_cli": ("services.coingecko", "create_coingecko_service"),
        "fmp_cli": ("services.fmp", "create_fmp_service"),
        "economic_calendar_cli": ("services.economic_calendar", "create_economic_calendar_service")
    }

    for service_name, (module_name, factory_name) in services_to_test.items():
        try:
            # Try to import the module
            module = __import__(module_name, fromlist=[factory_name])
            factory = getattr(module, factory_name)

            # Try to create the service
            service = factory("prod")
            service_status[service_name] = {"status": "available", "error": None}
            logger.info(f"✓ {service_name} - Available")

        except ImportError as e:
            service_status[service_name] = {"status": "import_error", "error": str(e)}
            logger.error(f"✗ {service_name} - Import Error: {e}")

        except Exception as e:
            service_status[service_name] = {"status": "creation_error", "error": str(e)}
            logger.error(f"✗ {service_name} - Creation Error: {e}")

    # Summary
    available_count = sum(1 for status in service_status.values() if status["status"] == "available")
    total_count = len(service_status)

    print(f"\n=== SERVICE AVAILABILITY SUMMARY ===")
    print(f"Available: {available_count}/{total_count}")
    print(f"Success Rate: {available_count/total_count*100:.1f}%")

    for service_name, status in service_status.items():
        if status["status"] != "available":
            print(f"\nFAILED: {service_name}")
            print(f"  Status: {status['status']}")
            print(f"  Error: {status['error']}")

    return service_status

if __name__ == "__main__":
    test_service_availability()
