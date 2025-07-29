#!/usr/bin/env python3
"""
Debug Auto-Collection Test

Debug test to understand why auto-collection might not be creating files.
"""

import logging
import sys
import time
from pathlib import Path

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils"))


def test_with_debug():
    """Test with debug logging to see what's happening"""
    print("🔍 Debug Auto-Collection Test")
    print("=" * 50)

    try:
        from services.yahoo_finance import create_yahoo_finance_service

        # Create service
        service = create_yahoo_finance_service()

        # Check configuration
        print("⚙️  Configuration Check:")
        config = service.config.historical_storage
        print(f"   Auto-collection enabled: {config.auto_collection_enabled}")
        print(f"   Trigger on price calls: {config.trigger_on_price_calls}")
        print(f"   Background collection: {config.background_collection}")
        print(f"   Daily days: {config.daily_days}")
        print(f"   Weekly years: {config.weekly_years}")

        # Check if historical manager is initialized
        print(f"   Historical manager: {service.historical_manager is not None}")

        print("\n📈 Making API call with debug logging...")

        # Enable debug logging for the service
        service.logger.setLevel(logging.DEBUG)

        result = service.get_stock_info("AMD")

        if result:
            print(f"   ✅ API call successful for: {result.get('symbol', 'N/A')}")

            # Check if data type detection worked
            from services.base_financial_service import DataType

            detected_type = service._detect_data_type("stock_info_AMD", result)
            print(f"   🔍 Detected data type: {detected_type}")

            # Check if symbol extraction worked
            symbol = service._extract_symbol_from_data(result, {"symbol": "AMD"})
            print(f"   🔍 Extracted symbol: {symbol}")

            # Check if collection should be triggered
            if detected_type:
                should_trigger = service._should_trigger_comprehensive_collection(
                    symbol or "AMD", detected_type
                )
                print(f"   🔍 Should trigger collection: {should_trigger}")

            # Wait and check for collection activity
            print("   ⏳ Waiting 10 seconds for background activity...")
            time.sleep(10)

            # Check collection cache
            print(f"   🔍 Collection cache: {list(service._collection_cache.keys())}")

        else:
            print("❌ API call failed")

        return True

    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_synchronous_collection():
    """Test with synchronous collection (no background threads)"""
    print("\n🔄 Testing Synchronous Collection")
    print("=" * 50)

    try:
        # Create a custom service config with synchronous collection
        from services.base_financial_service import (
            CacheConfig,
            HistoricalStorageConfig,
            RateLimitConfig,
            ServiceConfig,
        )
        from utils.config_loader import ConfigLoader

        # Load base config
        config_dir = Path(__file__).parent.parent / "config"
        config_loader = ConfigLoader(str(config_dir))
        service_config = config_loader.get_service_config("yahoo_finance", "dev")

        # Create config with synchronous collection
        config = ServiceConfig(
            name=service_config.name,
            base_url=service_config.base_url,
            api_key=service_config.api_key,
            timeout_seconds=service_config.timeout_seconds,
            max_retries=service_config.max_retries,
            cache=CacheConfig(**service_config.cache),
            rate_limit=RateLimitConfig(**service_config.rate_limit),
            historical_storage=HistoricalStorageConfig(
                enabled=True,
                store_stock_prices=True,
                store_financials=True,
                store_fundamentals=True,
                auto_collection_enabled=True,
                daily_days=30,  # Reduced for testing
                weekly_years=1,  # Reduced for testing
                trigger_on_price_calls=True,
                collection_interval_hours=0,  # No throttling for test
                background_collection=False,  # Synchronous!
            ),
            headers=service_config.headers,
        )

        from services.yahoo_finance import YahooFinanceAPIService

        service = YahooFinanceAPIService(config)

        print("⚙️  Using SYNCHRONOUS collection (no background threads)")
        print("📈 Making API call...")

        # Count files before
        data_path = Path("data/raw")
        files_before = len(list(data_path.rglob("*.json"))) if data_path.exists() else 0
        print(f"   📁 Files before: {files_before}")

        result = service.get_stock_info("INTC")

        if result:
            print(f"   ✅ API call completed: {result.get('symbol', 'N/A')}")

            # Count files after (should be immediate with sync collection)
            files_after = (
                len(list(data_path.rglob("*.json"))) if data_path.exists() else 0
            )
            print(f"   📁 Files after: {files_after}")

            new_files = files_after - files_before
            print(f"   📈 New files: {new_files}")

            if new_files > 0:
                print("   🎉 SYNCHRONOUS COLLECTION SUCCESS!")

                # Show what was created
                if data_path.exists():
                    for file_path in data_path.rglob("*.json"):
                        if (
                            file_path.stat().st_mtime > time.time() - 5
                        ):  # Modified in last 5 seconds
                            rel_path = file_path.relative_to(data_path)
                            size = file_path.stat().st_size
                            print(f"      📄 {rel_path} ({size} bytes)")

                return True
            else:
                print("   ⚠️  No files created with synchronous collection")
                return False
        else:
            print("   ❌ API call failed")
            return False

    except Exception as e:
        print(f"❌ Synchronous test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Debug Auto-Collection Analysis")
    print("=" * 70)

    # Test 1: Debug with logging
    success1 = test_with_debug()

    # Test 2: Synchronous collection
    success2 = test_synchronous_collection()

    print("\n" + "=" * 70)
    print("🏁 DEBUG RESULTS")
    print("=" * 70)

    if success1:
        print("✅ Debug test completed (check logs above)")
    else:
        print("❌ Debug test failed")

    if success2:
        print("✅ Synchronous collection test passed")
        print("🎉 Auto-collection mechanism is working!")
    else:
        print("❌ Synchronous collection test failed")
        print("⚠️  Auto-collection mechanism needs investigation")

    if success1 and success2:
        print("\n🎯 CONCLUSION: Auto-collection is working correctly!")
        print("Files are being created when API calls are made.")
    else:
        print("\n🔍 INVESTIGATION NEEDED: Check the debug output above")

    sys.exit(0 if (success1 and success2) else 1)
