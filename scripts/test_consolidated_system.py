#!/usr/bin/env python3
"""
Test Consolidated Storage System

Quick validation that the new consolidated file structure works correctly.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "utils"))
from historical_data_manager import DataType, HistoricalDataManager, Timeframe


def test_consolidated_storage():
    """Test the new consolidated storage system"""
    print("🧪 Testing Consolidated Storage System")
    print("=" * 50)

    hdm = HistoricalDataManager()

    # Test data - multiple records for time series
    test_data = {
        "symbol": "TEST_CONSOLIDATED",
        "data": [
            {
                "Date": "2025-07-28",
                "Open": 100.0,
                "High": 105.0,
                "Low": 98.0,
                "Close": 103.0,
                "Volume": 1000000,
                "Adj Close": 103.0,
            },
            {
                "Date": "2025-07-27",
                "Open": 98.0,
                "High": 102.0,
                "Low": 96.0,
                "Close": 100.0,
                "Volume": 800000,
                "Adj Close": 100.0,
            },
            {
                "Date": "2025-07-26",
                "Open": 95.0,
                "High": 99.0,
                "Low": 94.0,
                "Close": 98.0,
                "Volume": 900000,
                "Adj Close": 98.0,
            },
        ],
    }

    # Test 1: Store data
    print("📥 Test 1: Storing consolidated data...")
    success = hdm.store_data(
        symbol="TEST_CONSOLIDATED",
        data=test_data,
        data_type=DataType.STOCK_DAILY_PRICES,
        timeframe=Timeframe.DAILY,
        source="test",
    )
    print("   Storage result: {'✅ SUCCESS' if success else '❌ FAILED'}")

    if not success:
        return False

    # Test 2: Check file structure
    print("\n📁 Test 2: Checking file structure...")
    expected_csv = Path("data/raw/stocks/TEST_CONSOLIDATED/daily.csv")
    expected_meta = Path("data/raw/stocks/TEST_CONSOLIDATED/daily.meta.json")

    csv_exists = expected_csv.exists()
    meta_exists = expected_meta.exists()

    print("   CSV file: {'✅ EXISTS' if csv_exists else '❌ MISSING'} ({expected_csv})")
    print(
        f"   Metadata file: {'✅ EXISTS' if meta_exists else '❌ MISSING'} ({expected_meta})"
    )

    if csv_exists:
        csv_size = expected_csv.stat().st_size
        print("   CSV file size: {csv_size} bytes")

    # Test 3: Retrieve data
    print("\n📤 Test 3: Retrieving consolidated data...")
    retrieved = hdm.retrieve_data(
        symbol="TEST_CONSOLIDATED",
        data_type=DataType.STOCK_DAILY_PRICES,
        date_start="2025-07-26",
        date_end="2025-07-28",
        timeframe=Timeframe.DAILY,
    )

    print("   Retrieved: {len(retrieved)} records")

    if retrieved:
        print("   Record details:")
        for record in retrieved:
            print(
                f"     {record['date']}: Close=${record['close']}, Volume={record['volume']:,}"
            )

    # Test 4: Append additional data (deduplication test)
    print("\n➕ Test 4: Testing append with deduplication...")
    additional_data = {
        "symbol": "TEST_CONSOLIDATED",
        "data": [
            {
                "Date": "2025-07-28",  # Duplicate - should be ignored
                "Open": 100.0,
                "High": 105.0,
                "Low": 98.0,
                "Close": 103.0,
                "Volume": 1000000,
                "Adj Close": 103.0,
            },
            {
                "Date": "2025-07-29",  # New record - should be added
                "Open": 103.0,
                "High": 107.0,
                "Low": 102.0,
                "Close": 106.0,
                "Volume": 1200000,
                "Adj Close": 106.0,
            },
        ],
    }

    success_append = hdm.store_data(
        symbol="TEST_CONSOLIDATED",
        data=additional_data,
        data_type=DataType.STOCK_DAILY_PRICES,
        timeframe=Timeframe.DAILY,
        source="test_append",
    )

    print("   Append result: {'✅ SUCCESS' if success_append else '❌ FAILED'}")

    # Retrieve again to verify deduplication
    final_retrieved = hdm.retrieve_data(
        symbol="TEST_CONSOLIDATED",
        data_type=DataType.STOCK_DAILY_PRICES,
        date_start="2025-07-26",
        date_end="2025-07-29",
        timeframe=Timeframe.DAILY,
    )

    print("   Final count: {len(final_retrieved)} records (should be 4, not 5)")

    # Test 5: Performance comparison
    print("\n⚡ Test 5: File system efficiency...")

    old_structure_files = 4 * 2  # 4 periods × 2 files each (CSV + meta)
    new_structure_files = 2  # 1 CSV + 1 meta

    reduction = (old_structure_files - new_structure_files) / old_structure_files * 100
    print("   Old fragmented approach: {old_structure_files} files")
    print("   New consolidated approach: {new_structure_files} files")
    print("   File reduction: {reduction:.1f}%")

    # Summary
    print("\n📊 SUMMARY")
    print("=" * 50)
    success_rate = (
        sum(
            [
                success,
                csv_exists and meta_exists,
                len(retrieved) == 3,
                success_append,
                len(final_retrieved) == 4,
            ]
        )
        / 5
        * 100
    )

    print("✅ Test Success Rate: {success_rate:.0f}%")
    print("🎯 System Status: {'OPERATIONAL' if success_rate >= 80 else 'NEEDS FIXES'}")

    return success_rate >= 80


if __name__ == "__main__":
    success = test_consolidated_storage()
    exit(0 if success else 1)
