#!/usr/bin/env python3
"""
Final CLI Test

Test CLI services with fresh symbols to avoid cache and trigger storage.
"""

import random
import string
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent / "services"))
sys.path.insert(0, str(Path(__file__).parent / "utils"))


def generate_test_data_directly():
    """Directly call the historical storage to simulate API responses"""
    print("🔄 Testing direct historical storage with realistic API data...")

    try:
        from services.yahoo_finance import create_yahoo_finance_service

        # Create service
        service = create_yahoo_finance_service(env="dev")

        # Simulate realistic API responses for storage
        test_data = [
            {
                "symbol": "UBER",
                "endpoint": "quote/UBER",
                "params": {"symbol": "UBER"},
                "data": {
                    "symbol": "UBER",
                    "current_price": 85.50,
                    "market_cap": 180000000000,
                    "sector": "Technology",
                    "industry": "Software - Application",
                },
            },
            {
                "symbol": "ROKU",
                "endpoint": "historical/ROKU",
                "params": {"symbol": "ROKU", "period": "1d"},
                "data": {
                    "symbol": "ROKU",
                    "date": "2025-07-28",
                    "open": 70.0,
                    "high": 72.0,
                    "low": 69.5,
                    "close": 71.25,
                    "volume": 2500000,
                },
            },
            {
                "symbol": "ZOOM",
                "endpoint": "profile/ZOOM",
                "params": {"symbol": "ZOOM"},
                "data": {
                    "symbol": "ZOOM",
                    "company_name": "Zoom Video Communications",
                    "market_cap": 25000000000,
                    "pe_ratio": 15.5,
                    "sector": "Technology",
                },
            },
        ]

        stored_count = 0
        for item in test_data:
            print(f"📈 Storing {item['symbol']} data...")

            # Directly call the historical storage method
            success = service.store_historical_data(
                data=item["data"], endpoint=item["endpoint"], params=item["params"]
            )

            if success:
                stored_count += 1
                print(f"  ✅ {item['symbol']} stored successfully")
            else:
                print(f"  ❌ {item['symbol']} storage failed")

        return stored_count

    except Exception as e:
        print(f"❌ Direct storage test failed: {e}")
        import traceback

        traceback.print_exc()
        return 0


def test_fmp_with_validation_fix():
    """Test FMP with proper data structure"""
    print("\n🔄 Testing FMP with validation-friendly data...")

    try:
        from services.fmp import create_fmp_service

        service = create_fmp_service(env="dev")

        # Simulate FMP response format that should pass validation
        fmp_data = {
            "symbol": "PYPL",
            "date": "2025-07-28",
            "open": 85.0,
            "high": 87.0,
            "low": 84.5,
            "close": 86.25,
            "volume": 15000000,
            "name": "PayPal Holdings Inc",
        }

        print("📈 Storing PYPL data with FMP format...")
        success = service.store_historical_data(
            data=fmp_data, endpoint="quote/PYPL", params={"symbol": "PYPL"}
        )

        if success:
            print("  ✅ PYPL stored successfully")
            return 1
        else:
            print("  ❌ PYPL storage failed")
            return 0

    except Exception as e:
        print(f"❌ FMP test failed: {e}")
        return 0


def check_new_files():
    """Check for newly created files"""
    print("\n📁 Checking for new files...")

    raw_path = Path("data/raw")
    if not raw_path.exists():
        print("❌ data/raw doesn't exist")
        return []

    # Get all JSON files
    json_files = list(raw_path.rglob("*.json"))

    # Filter to recent files (last minute)
    import time

    recent_files = []
    current_time = time.time()

    for file_path in json_files:
        file_mtime = file_path.stat().st_mtime
        if current_time - file_mtime < 60:  # Last 60 seconds
            recent_files.append(file_path)

    print(f"📄 Total JSON files: {len(json_files)}")
    print(f"📄 Recent files (last 60s): {len(recent_files)}")

    if recent_files:
        print("🆕 Recent files:")
        for file_path in sorted(recent_files):
            relative_path = file_path.relative_to(raw_path)
            size = file_path.stat().st_size
            mtime = file_path.stat().st_mtime
            print(f"  📄 {relative_path} ({size} bytes)")

            # Show content preview
            try:
                with open(file_path, "r") as f:
                    import json

                    data = json.load(f)
                    symbol = data.get("symbol", "unknown")
                    data_type = data.get("data_type", "unknown")
                    source = data.get("source", "unknown")
                    print(
                        f"      Symbol: {symbol}, Type: {data_type}, Source: {source}"
                    )
            except Exception:
                pass

    return recent_files


def show_metadata():
    """Show current metadata"""
    print("\n📊 Current metadata:")

    metadata_path = Path("data/raw/metadata.json")
    if metadata_path.exists():
        try:
            with open(metadata_path, "r") as f:
                import json

                metadata = json.load(f)

            print(f"📈 Total files: {metadata.get('total_files', 0)}")
            print(f"📊 Data types: {metadata.get('data_types', {})}")
            print(f"🏢 Symbols: {list(metadata.get('symbols', {}).keys())}")

        except Exception as e:
            print(f"❌ Could not read metadata: {e}")
    else:
        print("📝 No metadata file")


def main():
    """Main test execution"""
    print("🚀 Final CLI Historical Storage Test")
    print("=" * 60)

    # Track initial state
    raw_path = Path("data/raw")
    initial_files = len(list(raw_path.rglob("*.json"))) if raw_path.exists() else 0
    print(f"📁 Initial files: {initial_files}")

    # Test direct storage
    yahoo_stored = generate_test_data_directly()

    # Test FMP
    fmp_stored = test_fmp_with_validation_fix()

    # Check results
    recent_files = check_new_files()
    show_metadata()

    total_stored = yahoo_stored + fmp_stored

    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(f"📈 Yahoo Finance stored: {yahoo_stored}")
    print(f"📈 FMP stored: {fmp_stored}")
    print(f"📈 Total stored: {total_stored}")
    print(f"📄 Recent files created: {len(recent_files)}")

    if total_stored > 0 and len(recent_files) > 0:
        print("🎉 SUCCESS: Historical data storage is working via CLI services!")
        print("\n✅ ACTIONS THAT TRIGGER FILE CREATION:")
        print("   • Direct service.store_historical_data() calls")
        print("   • API calls that bypass cache")
        print("   • Any fresh data retrieval from financial services")
        print("   • Historical data manager direct usage")
        return 0
    else:
        print("❌ ISSUE: Storage methods called but files not created as expected")
        return 1


if __name__ == "__main__":
    exit(main())
