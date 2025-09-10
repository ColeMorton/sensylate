#!/usr/bin/env python3
"""
Size Threshold Corruption Test

Tests specific file sizes with BTC-USD filename to find corruption threshold.
"""

import sys
import os
import time
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent / 'scripts'))

from file_protection_manager import FileProtectionManager


def create_sized_btc_data(target_size_kb: int) -> pd.DataFrame:
    """Create BTC data targeting specific file size in KB"""
    
    print(f"📊 Creating BTC data targeting ~{target_size_kb}KB...")
    
    # Calculate rows needed for target size
    # Average row size is ~100 bytes including header
    target_rows = (target_size_kb * 1024) // 100
    
    # Generate dates for the calculated rows
    base_date = pd.Timestamp('2014-09-17')
    dates = [base_date + pd.Timedelta(days=i) for i in range(target_rows)]
    
    data = []
    base_price = 457.33
    
    for i, date in enumerate(dates):
        # Realistic Bitcoin patterns
        days_elapsed = i
        growth_factor = (1 + days_elapsed / 365) ** 2.5
        daily_volatility = 1 + (hash(str(date)) % 200 - 100) / 1000
        
        price = base_price * growth_factor * daily_volatility
        
        # Generate realistic OHLC data
        daily_range = price * 0.05
        open_price = price * (0.98 + (hash(str(date)) % 40) / 2000)
        high_price = price + daily_range * (hash(str(date + pd.Timedelta(hours=1))) % 100) / 100
        low_price = price - daily_range * (hash(str(date + pd.Timedelta(hours=2))) % 100) / 100
        close_price = price
        
        # Realistic volume
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
    actual_size = len(df.to_csv(index=False).encode('utf-8'))
    actual_size_kb = actual_size // 1024
    
    print(f"📏 Generated {len(df)} rows = {actual_size:,} bytes (~{actual_size_kb}KB)")
    
    return df


def test_size_corruption(size_kb: int, test_name: str) -> dict:
    """Test corruption for specific file size"""
    
    print(f"\n🧪 TEST: {test_name} (~{size_kb}KB)")
    print("=" * 50)
    
    # Create test data
    test_data = create_sized_btc_data(size_kb)
    actual_size = len(test_data.to_csv(index=False).encode('utf-8'))
    
    # Use BTC-USD path (critical for trigger)
    test_path = Path(f"frontend/public/data/raw/stocks/BTC-USD/size_test_{size_kb}kb.csv")
    test_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_manager = FileProtectionManager()
    
    print(f"✏️  Writing {len(test_data)} rows to BTC-USD path...")
    
    # Write with protection
    start_time = time.time()
    write_success = file_manager.protected_write_csv(
        df=test_data,
        file_path=test_path
    )
    write_time = time.time() - start_time
    
    if not write_success:
        return {
            'test': test_name,
            'size_kb': size_kb,
            'success': False,
            'error': 'Protected write failed'
        }
    
    print(f"✅ Write completed in {write_time:.2f}s")
    
    # Immediate check
    if test_path.exists():
        immediate_size = test_path.stat().st_size
        immediate_corrupted = immediate_size < 100
        
        print(f"📏 Immediate size: {immediate_size:,} bytes")
        
        if immediate_corrupted:
            print(f"🚨 IMMEDIATE CORRUPTION!")
            return {
                'test': test_name,
                'size_kb': size_kb,
                'success': True,
                'immediate_corruption': True,
                'size': immediate_size,
                'expected_size': actual_size
            }
    
    # Wait brief moment for external processes
    time.sleep(0.5)
    
    # Final check
    if test_path.exists():
        final_size = test_path.stat().st_size
        final_corrupted = final_size < 100
        
        print(f"📏 Final size: {final_size:,} bytes")
        
        if final_corrupted:
            print(f"🚨 DELAYED CORRUPTION!")
            return {
                'test': test_name,
                'size_kb': size_kb,
                'success': True,
                'delayed_corruption': True,
                'size': final_size,
                'expected_size': actual_size
            }
        else:
            print(f"✅ NO CORRUPTION")
            return {
                'test': test_name,
                'size_kb': size_kb,
                'success': True,
                'no_corruption': True,
                'size': final_size,
                'expected_size': actual_size
            }
    
    return {
        'test': test_name,
        'size_kb': size_kb,
        'success': False,
        'error': 'File disappeared'
    }


def run_size_threshold_tests():
    """Run comprehensive size threshold testing"""
    
    print("🔬 SIZE THRESHOLD CORRUPTION ANALYSIS")
    print("=" * 50)
    print("Testing different file sizes with BTC-USD filename to find corruption threshold")
    print()
    
    # Test various sizes around the known corruption point
    test_cases = [
        (100, "Small File (100KB)"),
        (200, "Medium Small (200KB)"),
        (300, "Pre-Corruption (300KB)"),
        (370, "Corruption Size (370KB)"),   # Known corruption size
        (400, "Post-Corruption (400KB)"),
        (500, "Large File (500KB)"),
        (640, "MSTR Size (640KB)"),         # MSTR works at this size
        (800, "Very Large (800KB)")
    ]
    
    results = []
    corruption_threshold = None
    
    for size_kb, test_name in test_cases:
        result = test_size_corruption(size_kb, test_name)
        results.append(result)
        
        # Track first corruption occurrence
        if (result.get('immediate_corruption') or result.get('delayed_corruption')) and corruption_threshold is None:
            corruption_threshold = size_kb
    
    # Analyze results
    print(f"\n📋 SIZE THRESHOLD TEST RESULTS")
    print("=" * 40)
    
    corruption_sizes = []
    safe_sizes = []
    
    for result in results:
        test_name = result['test']
        size_kb = result['size_kb']
        
        if result.get('success'):
            if result.get('immediate_corruption') or result.get('delayed_corruption'):
                print(f"🚨 {test_name}: CORRUPTION at {size_kb}KB")
                corruption_sizes.append(size_kb)
            elif result.get('no_corruption'):
                print(f"✅ {test_name}: Safe at {size_kb}KB")
                safe_sizes.append(size_kb)
        else:
            print(f"❌ {test_name}: Test failed - {result.get('error')}")
    
    # Analysis
    print(f"\n🎯 SIZE THRESHOLD ANALYSIS")
    print("=" * 30)
    
    if corruption_sizes and safe_sizes:
        max_safe = max(safe_sizes)
        min_corruption = min(corruption_sizes)
        
        print(f"✅ Safe sizes: {safe_sizes}")
        print(f"🚨 Corruption sizes: {corruption_sizes}")
        print(f"📊 Threshold: Between {max_safe}KB and {min_corruption}KB")
        
        if min_corruption - max_safe <= 100:
            print(f"🎯 PRECISE THRESHOLD IDENTIFIED: ~{max_safe}-{min_corruption}KB")
        
    elif corruption_sizes:
        print(f"🚨 ALL tested sizes corrupt: {corruption_sizes}")
        print(f"   → Threshold below {min(corruption_sizes)}KB")
        
    elif safe_sizes:
        print(f"✅ ALL tested sizes safe: {safe_sizes}")
        print(f"   → Threshold above {max(safe_sizes)}KB")
        
    else:
        print(f"❌ No conclusive results")
    
    return len(corruption_sizes) > 0


if __name__ == "__main__":
    try:
        corruption_found = run_size_threshold_tests()
        
        if corruption_found:
            print(f"\n🎯 CONCLUSION: Size threshold corruption confirmed")
            print("   → Specific file size ranges trigger BTC-USD corruption")
        else:
            print(f"\n🔄 CONCLUSION: No size threshold corruption detected")
            print("   → BTC-USD corruption may be timing/context dependent")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()