#!/usr/bin/env python3
"""
Content Detection Test

Tests whether real Yahoo Finance BTC data triggers corruption in standalone context.
This isolates content-based scanning from process context factors.
"""

import sys
import os
import time
import pandas as pd
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent / 'scripts'))

from file_protection_manager import FileProtectionManager


def fetch_real_yahoo_finance_data() -> pd.DataFrame:
    """Fetch real Yahoo Finance BTC-USD data using the same method as the pipeline"""

    print("📡 Fetching real Yahoo Finance BTC-USD data...")

    try:
        # Use the same Yahoo Finance CLI that the pipeline uses
        script_path = Path(__file__).parent / 'scripts' / 'yahoo_finance_cli.py'

        # Run the same command the pipeline uses for BTC-USD
        result = subprocess.run([
            'python3', str(script_path),
            'history', 'BTC-USD',
            '--period', 'max'
        ], capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"❌ Yahoo Finance fetch failed: {result.stderr}")
            return None

        print(f"✅ Yahoo Finance API success: {len(result.stdout)} chars")

        # Parse JSON response (same as pipeline)
        try:
            data = json.loads(result.stdout)

            # Convert to DataFrame (same format as pipeline)
            df = pd.DataFrame(data)

            # Add date column if not present
            if 'date' not in df.columns and 'Date' in df.columns:
                df['date'] = df['Date']
            elif 'date' not in df.columns:
                # Generate dates if missing (fallback)
                start_date = pd.Timestamp('2014-09-17')
                df['date'] = [start_date + pd.Timedelta(days=i) for i in range(len(df))]
                df['date'] = df['date'].dt.strftime('%Y-%m-%d')

            print(f"📊 Parsed {len(df)} rows of real BTC data")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Date range: {df['date'].iloc[0] if len(df) > 0 else 'N/A'} to {df['date'].iloc[-1] if len(df) > 0 else 'N/A'}")

            return df

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw output: {result.stdout[:200]}...")
            return None

    except subprocess.TimeoutExpired:
        print("❌ Yahoo Finance API timeout")
        return None
    except Exception as e:
        print(f"❌ Yahoo Finance fetch error: {e}")
        return None


def create_fallback_realistic_data() -> pd.DataFrame:
    """Create realistic BTC data as fallback if API fails"""

    print("📊 Creating realistic BTC data (API fallback)...")

    # Create realistic Bitcoin price data based on actual historical patterns
    dates = pd.date_range('2014-09-17', '2025-09-08', freq='D')

    data = []
    base_price = 457.33  # Historical BTC starting price

    for i, date in enumerate(dates):
        # Realistic Bitcoin growth pattern (exponential with volatility)
        days_elapsed = i
        growth_factor = (1 + days_elapsed / 365) ** 2.5  # Exponential growth over years
        daily_volatility = 1 + (hash(str(date)) % 200 - 100) / 1000  # Pseudo-random daily changes

        price = base_price * growth_factor * daily_volatility

        # Generate realistic OHLC data
        daily_range = price * 0.05  # 5% daily range
        open_price = price * (0.98 + (hash(str(date)) % 40) / 2000)
        high_price = price + daily_range * (hash(str(date + pd.Timedelta(hours=1))) % 100) / 100
        low_price = price - daily_range * (hash(str(date + pd.Timedelta(hours=2))) % 100) / 100
        close_price = price

        # Realistic volume (millions of dollars)
        volume = 20000000 + (days_elapsed * 50000) % 80000000

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

    df = pd.DataFrame(data)
    print(f"📊 Generated {len(df)} rows of realistic BTC data")

    return df


def test_content_based_corruption(real_data: pd.DataFrame) -> dict:
    """Test if real BTC content triggers corruption in standalone context"""

    print(f"\n🧪 CONTENT DETECTION TEST")
    print(f"=" * 30)
    print(f"Testing real Yahoo Finance BTC data in standalone context...")

    # Test path (same as pipeline)
    test_path = Path("frontend/public/data/raw/stocks/BTC-USD/daily.csv")
    test_path.parent.mkdir(parents=True, exist_ok=True)

    # Calculate expected file size
    expected_size = len(real_data.to_csv(index=False).encode('utf-8'))
    print(f"📏 Expected file size: {expected_size:,} bytes")
    print(f"📊 Data rows: {len(real_data)}")

    # Initialize FileProtectionManager (same as pipeline)
    file_manager = FileProtectionManager()

    # Record timing
    start_time = time.time()

    # Write real data to BTC-USD filename
    print(f"\n✏️  Writing REAL Yahoo Finance data to BTC-USD file...")
    write_success = file_manager.protected_write_csv(
        df=real_data,
        file_path=test_path,
        timeout=30
    )

    write_time = time.time() - start_time

    if not write_success:
        return {
            'test': 'Content Detection',
            'write_success': False,
            'error': 'Protected write failed',
            'write_time': write_time
        }

    print(f"✅ Write completed successfully in {write_time:.2f}s")

    # CRITICAL: Use same timing as pipeline (immediate verification, no 2s wait)
    print(f"⚡ Immediate verification (pipeline timing)...")

    # Check file immediately (like pipeline does)
    if test_path.exists():
        immediate_size = test_path.stat().st_size
        immediate_corrupted = immediate_size < 100

        print(f"📏 Immediate size: {immediate_size:,} bytes")

        if immediate_corrupted:
            print(f"🚨 IMMEDIATE CORRUPTION DETECTED!")
            result = {
                'test': 'Content Detection',
                'write_success': True,
                'immediate_corruption': True,
                'immediate_size': immediate_size,
                'expected_size': expected_size,
                'corruption_timing': 'immediate',
                'write_time': write_time
            }
        else:
            print(f"✅ No immediate corruption")

            # Wait brief moment and check again (like pipeline verification)
            time.sleep(0.1)

            final_size = test_path.stat().st_size
            final_corrupted = final_size < 100

            print(f"📏 Final size: {final_size:,} bytes")

            if final_corrupted:
                print(f"🚨 DELAYED CORRUPTION DETECTED!")
                result = {
                    'test': 'Content Detection',
                    'write_success': True,
                    'immediate_corruption': False,
                    'delayed_corruption': True,
                    'final_size': final_size,
                    'expected_size': expected_size,
                    'corruption_timing': 'delayed',
                    'write_time': write_time
                }
            else:
                print(f"✅ NO CORRUPTION - Content theory DISPROVEN")
                result = {
                    'test': 'Content Detection',
                    'write_success': True,
                    'no_corruption': True,
                    'final_size': final_size,
                    'expected_size': expected_size,
                    'write_time': write_time
                }
    else:
        result = {
            'test': 'Content Detection',
            'write_success': False,
            'error': 'File disappeared after write',
            'write_time': write_time
        }

    return result


def run_content_detection_test():
    """Main test runner for content detection theory"""

    print("🔬 CONTENT-BASED CORRUPTION DETECTION TEST")
    print("=" * 50)
    print("Theory: Real crypto data content triggers scanning, not just filename")
    print()

    # Step 1: Get real Yahoo Finance data
    real_btc_data = fetch_real_yahoo_finance_data()

    if real_btc_data is None or len(real_btc_data) == 0:
        print("⚠️  Using fallback realistic data (API unavailable)")
        real_btc_data = create_fallback_realistic_data()

    # Step 2: Test real data in standalone context
    test_result = test_content_based_corruption(real_btc_data)

    # Step 3: Analyze results
    print(f"\n📋 CONTENT DETECTION TEST RESULTS")
    print("=" * 35)

    if test_result.get('no_corruption'):
        print("❌ CONTENT THEORY DISPROVEN")
        print("   → Real crypto data does NOT trigger corruption in standalone context")
        print("   → Content scanning is NOT the root cause")
        print("   → Must be process context or timing related")

    elif test_result.get('immediate_corruption') or test_result.get('delayed_corruption'):
        print("✅ CONTENT THEORY CONFIRMED")
        print("   → Real crypto data DOES trigger corruption")
        print("   → Content-based scanning IS the root cause")
        print(f"   → Corruption timing: {test_result.get('corruption_timing', 'unknown')}")

    else:
        print("⚠️  INCONCLUSIVE RESULTS")
        print(f"   → Write success: {test_result.get('write_success')}")
        print(f"   → Error: {test_result.get('error', 'Unknown')}")

    print(f"\nTest Details:")
    print(f"  ✏️  Write Time: {test_result.get('write_time', 0):.2f}s")
    print(f"  📏 Expected Size: {test_result.get('expected_size', 'N/A'):,} bytes")
    print(f"  📏 Final Size: {test_result.get('final_size', test_result.get('immediate_size', 'N/A')):,} bytes" if isinstance(test_result.get('final_size', test_result.get('immediate_size')), int) else f"  📏 Final Size: {test_result.get('final_size', test_result.get('immediate_size', 'N/A'))}")

    return test_result.get('no_corruption') is not True  # Return True if corruption detected


if __name__ == "__main__":
    try:
        corruption_detected = run_content_detection_test()

        if corruption_detected:
            print(f"\n🎯 CONCLUSION: Content-based scanning confirmed")
            print("   Next: Test process context and timing factors")
            exit(0)
        else:
            print(f"\n🔄 CONCLUSION: Content is NOT the trigger")
            print("   Next: Focus on process context and timing")
            exit(1)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(2)
