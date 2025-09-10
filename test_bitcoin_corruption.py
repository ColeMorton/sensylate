#!/usr/bin/env python3
"""
Bitcoin Filename Corruption Test

Tests whether renaming BTC-USD to BITCOIN eliminates macOS system corruption.
Compares corruption behavior between identical files with different names.
"""

import sys
import os
import time
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent / 'scripts'))

from file_protection_manager import FileProtectionManager


def create_sample_bitcoin_data(num_rows: int = 4010) -> pd.DataFrame:
    """Generate sample Bitcoin price data identical in structure to real BTC-USD data"""

    # Generate date range from 2014-09-17 to present (matching real BTC data)
    start_date = datetime(2014, 9, 17)
    dates = [start_date + timedelta(days=i) for i in range(num_rows)]

    # Generate realistic Bitcoin price progression
    base_price = 457.33  # Starting price from real BTC data
    data = []

    for i, date in enumerate(dates):
        # Simulate realistic price movement (exponential growth with volatility)
        price_multiplier = 1 + (i / num_rows) * 200  # Growth factor
        volatility = 0.05 * (1 + i/1000)  # Increasing volatility over time

        daily_change = 1 + ((i * 7 + i * i) % 200 - 100) / 10000 * volatility
        current_price = base_price * price_multiplier * daily_change

        # Generate OHLCV data
        open_price = current_price * (0.98 + (i % 40) / 2000)
        high_price = current_price * (1.02 + (i % 30) / 1500)
        low_price = current_price * (0.96 + (i % 25) / 2000)
        close_price = current_price
        volume = 20000000 + (i * 1000000) % 50000000  # Realistic volume

        data.append({
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume,
            'dividends': 0.0,
            'stock splits': 0.0,
            'date': date.strftime('%Y-%m-%d')
        })

    return pd.DataFrame(data)


def test_file_corruption(file_path: Path, symbol_name: str, test_data: pd.DataFrame) -> dict:
    """Test file corruption for a given path and return results"""

    print(f"\n🧪 Testing {symbol_name} file corruption...")
    print(f"   📂 Path: {file_path}")
    print(f"   📊 Data: {len(test_data)} rows")

    # Initialize FileProtectionManager
    file_manager = FileProtectionManager()

    # Record start time
    start_time = time.time()

    # Perform protected write
    print(f"   ✏️  Writing {symbol_name} data...")
    write_success = file_manager.protected_write_csv(
        df=test_data,
        file_path=file_path,
        timeout=30
    )

    write_time = time.time() - start_time

    if not write_success:
        return {
            'symbol': symbol_name,
            'write_success': False,
            'error': 'Protected write failed',
            'write_time': write_time
        }

    # Wait a moment for any external corruption to occur
    print(f"   ⏱️  Waiting for potential external corruption...")
    time.sleep(2)

    # Check file size and integrity
    if file_path.exists():
        file_size = file_path.stat().st_size
        corruption_detected = file_size < 100  # Same threshold as pipeline

        print(f"   📏 Final size: {file_size:,} bytes")
        if corruption_detected:
            print(f"   🚨 CORRUPTION DETECTED: {file_size} bytes (expected ~371,570)")
        else:
            print(f"   ✅ NO CORRUPTION: File size normal")

        return {
            'symbol': symbol_name,
            'write_success': True,
            'file_size': file_size,
            'corruption_detected': corruption_detected,
            'write_time': write_time,
            'expected_size': len(test_data.to_csv(index=False).encode('utf-8'))
        }
    else:
        return {
            'symbol': symbol_name,
            'write_success': False,
            'error': 'File does not exist after write',
            'write_time': write_time
        }


def run_comparative_test():
    """Run comparative corruption test between BTC-USD and BITCOIN"""

    print("🔬 BITCOIN FILENAME CORRUPTION TEST")
    print("=" * 50)
    print("Testing whether filename change eliminates macOS corruption")
    print()

    # Generate identical test data
    print("📊 Generating test data (4010 rows)...")
    test_data = create_sample_bitcoin_data(4010)
    expected_size = len(test_data.to_csv(index=False).encode('utf-8'))
    print(f"   Expected file size: {expected_size:,} bytes")

    # Define test paths
    btc_path = Path("frontend/public/data/raw/stocks/BTC-USD/daily.csv")
    bitcoin_path = Path("frontend/public/data/raw/stocks/BITCOIN/daily.csv")

    # Ensure directories exist
    btc_path.parent.mkdir(parents=True, exist_ok=True)
    bitcoin_path.parent.mkdir(parents=True, exist_ok=True)

    # Run tests simultaneously (to ensure identical system conditions)
    print("\n🚀 Running parallel corruption tests...")

    # Test 1: BTC-USD (known to corrupt)
    btc_results = test_file_corruption(btc_path, "BTC-USD", test_data)

    # Test 2: BITCOIN (test for corruption)
    bitcoin_results = test_file_corruption(bitcoin_path, "BITCOIN", test_data)

    # Analyze results
    print("\n📋 TEST RESULTS SUMMARY")
    print("=" * 30)

    for result in [btc_results, bitcoin_results]:
        symbol = result['symbol']
        print(f"\n{symbol}:")
        print(f"  ✏️  Write Success: {result.get('write_success', False)}")
        print(f"  📏 File Size: {result.get('file_size', 'N/A'):,} bytes" if 'file_size' in result else f"  ❌ Error: {result.get('error', 'Unknown')}")
        print(f"  🚨 Corrupted: {result.get('corruption_detected', 'N/A')}")
        print(f"  ⏱️  Write Time: {result.get('write_time', 0):.2f}s")

    # Determine test outcome
    btc_corrupted = btc_results.get('corruption_detected', True)
    bitcoin_corrupted = bitcoin_results.get('corruption_detected', True)

    print(f"\n🎯 CONCLUSION")
    print("=" * 15)

    if btc_corrupted and not bitcoin_corrupted:
        print("✅ SUCCESS: BITCOIN filename prevents corruption!")
        print("   BTC-USD corrupted (as expected)")
        print("   BITCOIN remained intact")
        print("   → Filename change solution CONFIRMED")
        return True

    elif btc_corrupted and bitcoin_corrupted:
        print("❌ FAILURE: Both files corrupted")
        print("   → Filename change does NOT resolve issue")
        print("   → Need alternative solution")
        return False

    elif not btc_corrupted and not bitcoin_corrupted:
        print("⚠️  INCONCLUSIVE: Neither file corrupted")
        print("   → Corruption may be intermittent")
        print("   → Rerun test or check system conditions")
        return None

    else:  # not btc_corrupted and bitcoin_corrupted
        print("🤔 UNEXPECTED: Only BITCOIN corrupted")
        print("   → Unusual result, investigate further")
        return None


if __name__ == "__main__":
    try:
        success = run_comparative_test()

        if success:
            print(f"\n🚀 READY FOR FULL IMPLEMENTATION")
            print("   The filename change solution is validated.")
            exit(0)
        elif success is False:
            print(f"\n🔄 NEED ALTERNATIVE SOLUTION")
            print("   Filename change does not resolve corruption.")
            exit(1)
        else:
            print(f"\n🔁 INCONCLUSIVE - RERUN TEST")
            print("   Results need verification.")
            exit(2)

    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {e}")
        exit(3)
