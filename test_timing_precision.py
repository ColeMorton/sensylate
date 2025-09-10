#!/usr/bin/env python3
"""
Timing Precision Test

Replicates the exact timing sequence of the real pipeline with actual Yahoo Finance
API calls to isolate timing-based corruption triggers.
"""

import sys
import os
import time
import pandas as pd
import subprocess
import json
import threading
from pathlib import Path
from datetime import datetime

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent / 'scripts'))

from file_protection_manager import FileProtectionManager


class PipelineTimingReplicator:
    """Replicates exact pipeline timing and API call patterns"""
    
    def __init__(self):
        self.file_manager = FileProtectionManager()
        self.target_path = Path("frontend/public/data/raw/stocks/BTC-USD/timing_test.csv")
        self.target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Track timing events exactly like pipeline
        self.events = []
        self.corruption_detected = False
        self.corruption_details = None
    
    def log_event(self, event: str, data: dict = None):
        """Log timing events with microsecond precision"""
        timestamp = time.time()
        event_data = {
            'timestamp': timestamp,
            'event': event,
            'data': data or {}
        }
        self.events.append(event_data)
        
        # Format like pipeline logs
        readable_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')[:-3]
        print(f"⏱️  [{readable_time}] {event}" + (f": {data}" if data else ""))
    
    def fetch_real_yahoo_data(self) -> pd.DataFrame:
        """Fetch real Yahoo Finance data with exact pipeline timing"""
        
        self.log_event("API_CALL_START", {'symbol': 'BTC-USD'})
        
        try:
            # Use identical API call to pipeline
            script_path = Path(__file__).parent / 'scripts' / 'yahoo_finance_cli.py'
            
            api_start = time.time()
            
            result = subprocess.run([
                'python3', str(script_path), 
                'history', 'BTC-USD', 
                '--period', 'max'
            ], capture_output=True, text=True, timeout=30)
            
            api_end = time.time()
            api_duration = api_end - api_start
            
            self.log_event("API_CALL_COMPLETE", {
                'duration': f"{api_duration:.3f}s",
                'return_code': result.returncode,
                'stdout_size': len(result.stdout)
            })
            
            if result.returncode != 0:
                self.log_event("API_CALL_FAILED", {'stderr': result.stderr})
                return None
            
            # Parse response with exact pipeline timing
            parse_start = time.time()
            
            try:
                data = json.loads(result.stdout)
                df = pd.DataFrame(data)
                
                # Add date column processing (same as pipeline)
                if 'date' not in df.columns and 'Date' in df.columns:
                    df['date'] = df['Date']
                elif 'date' not in df.columns:
                    start_date = pd.Timestamp('2014-09-17')
                    df['date'] = [start_date + pd.Timedelta(days=i) for i in range(len(df))]
                    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
                
                parse_end = time.time()
                parse_duration = parse_end - parse_start
                
                self.log_event("DATA_PARSING_COMPLETE", {
                    'duration': f"{parse_duration:.3f}s",
                    'rows': len(df),
                    'columns': list(df.columns),
                    'data_size': len(df.to_csv(index=False).encode('utf-8'))
                })
                
                return df
                
            except json.JSONDecodeError as e:
                self.log_event("JSON_PARSING_FAILED", {'error': str(e)})
                return None
                
        except subprocess.TimeoutExpired:
            self.log_event("API_TIMEOUT")
            return None
        except Exception as e:
            self.log_event("API_ERROR", {'error': str(e)})
            return None
    
    def monitor_corruption_continuously(self, duration: float = 5.0):
        """Monitor file for corruption continuously (like pipeline does)"""
        
        def corruption_monitor():
            monitor_start = time.time()
            check_count = 0
            
            while time.time() - monitor_start < duration:
                if self.target_path.exists():
                    current_size = self.target_path.stat().st_size
                    check_count += 1
                    
                    if current_size < 100:  # Corruption threshold
                        corruption_time = time.time()
                        self.corruption_detected = True
                        self.corruption_details = {
                            'detected_at': corruption_time,
                            'size': current_size,
                            'check_number': check_count,
                            'time_since_write': corruption_time - monitor_start
                        }
                        
                        self.log_event("CORRUPTION_DETECTED", {
                            'size': current_size,
                            'check': check_count,
                            'elapsed': f"{corruption_time - monitor_start:.3f}s"
                        })
                        return
                    
                    # Log periodic status (every 50 checks)
                    if check_count % 50 == 0:
                        self.log_event("CORRUPTION_CHECK", {
                            'check': check_count,
                            'size': current_size,
                            'status': 'ok'
                        })
                
                time.sleep(0.01)  # 10ms intervals (more frequent than pipeline)
            
            self.log_event("CORRUPTION_MONITOR_COMPLETE", {
                'checks': check_count,
                'duration': f"{duration:.1f}s",
                'result': 'no_corruption'
            })
        
        # Start background monitoring
        monitor_thread = threading.Thread(target=corruption_monitor, daemon=True)
        monitor_thread.start()
        
        return monitor_thread
    
    def write_with_pipeline_timing(self, data: pd.DataFrame) -> dict:
        """Write data with exact pipeline timing patterns"""
        
        expected_size = len(data.to_csv(index=False).encode('utf-8'))
        
        self.log_event("FILE_WRITE_START", {
            'path': str(self.target_path),
            'expected_size': expected_size,
            'rows': len(data)
        })
        
        # Start corruption monitoring before write (like pipeline)
        monitor_thread = self.monitor_corruption_continuously(5.0)
        
        # Exact write timing like pipeline
        write_start = time.time()
        
        write_success = self.file_manager.protected_write_csv(
            df=data,
            file_path=self.target_path,
            timeout=30
        )
        
        write_end = time.time()
        write_duration = write_end - write_start
        
        self.log_event("FILE_WRITE_COMPLETE", {
            'success': write_success,
            'duration': f"{write_duration:.3f}s"
        })
        
        if not write_success:
            return {
                'success': False,
                'error': 'Protected write failed',
                'write_duration': write_duration
            }
        
        # Immediate verification (like pipeline)
        if self.target_path.exists():
            immediate_size = self.target_path.stat().st_size
            immediate_corrupted = immediate_size < 100
            
            self.log_event("IMMEDIATE_VERIFICATION", {
                'size': immediate_size,
                'corrupted': immediate_corrupted
            })
            
            if immediate_corrupted:
                return {
                    'success': True,
                    'immediate_corruption': True,
                    'size': immediate_size,
                    'expected_size': expected_size,
                    'write_duration': write_duration
                }
        
        # Wait for monitoring to complete
        monitor_thread.join(timeout=6.0)
        
        # Final verification
        final_size = self.target_path.stat().st_size if self.target_path.exists() else 0
        final_corrupted = final_size < 100
        
        self.log_event("FINAL_VERIFICATION", {
            'size': final_size,
            'corrupted': final_corrupted
        })
        
        return {
            'success': True,
            'immediate_corruption': False,
            'delayed_corruption': self.corruption_detected,
            'final_size': final_size,
            'expected_size': expected_size,
            'write_duration': write_duration,
            'corruption_details': self.corruption_details
        }
    
    def simulate_pipeline_memory_pressure(self):
        """Simulate memory pressure patterns from API + data processing"""
        
        self.log_event("MEMORY_PRESSURE_SIMULATION_START")
        
        # Create memory pressure similar to large API responses
        large_data = []
        for i in range(50000):  # Simulate large dataset processing
            large_data.append({
                'index': i,
                'data': f"market_data_{i}" * 20,
                'timestamp': time.time(),
                'values': [j * i for j in range(10)]
            })
        
        # Process data (like API response processing)
        processed = pd.DataFrame(large_data)
        processed_size = len(processed.to_csv(index=False).encode('utf-8'))
        
        self.log_event("MEMORY_PRESSURE_PEAK", {
            'simulated_rows': len(processed),
            'simulated_size': processed_size
        })
        
        # Clear memory (like pipeline cleanup)
        del large_data, processed
        
        self.log_event("MEMORY_PRESSURE_CLEARED")
    
    def run_timing_precision_test(self) -> dict:
        """Run complete timing precision test"""
        
        self.log_event("TIMING_TEST_START", {'theory': 'API timing + file I/O race conditions'})
        
        # Step 1: Simulate memory pressure (like large API responses)
        self.simulate_pipeline_memory_pressure()
        
        # Step 2: Fetch real Yahoo Finance data (exact API timing)
        btc_data = self.fetch_real_yahoo_data()
        
        if btc_data is None or len(btc_data) == 0:
            self.log_event("TEST_FAILED", {'reason': 'API data unavailable'})
            return {'success': False, 'error': 'API data fetch failed'}
        
        # Step 3: Write with exact pipeline timing
        write_result = self.write_with_pipeline_timing(btc_data)
        
        self.log_event("TIMING_TEST_COMPLETE", write_result)
        
        return write_result


def run_timing_precision_test():
    """Main test runner for timing precision theory"""
    
    print("🔬 TIMING PRECISION CORRUPTION TEST")
    print("=" * 50)
    print("Theory: API timing + file I/O creates race conditions that trigger corruption")
    print()
    
    replicator = PipelineTimingReplicator()
    
    # Run the test
    result = replicator.run_timing_precision_test()
    
    # Analyze results
    print(f"\n📋 TIMING PRECISION TEST RESULTS")
    print("=" * 40)
    
    if not result.get('success'):
        print(f"❌ TEST FAILED: {result.get('error', 'Unknown error')}")
        return False
    
    if result.get('immediate_corruption'):
        print("🚨 IMMEDIATE CORRUPTION DETECTED")
        print("   → Timing-based race condition CONFIRMED")
        print("   → API + file I/O timing IS the root cause")
        print(f"   → File size: {result['size']:,} bytes (expected: {result['expected_size']:,})")
        return True
        
    elif result.get('delayed_corruption'):
        print("🚨 DELAYED CORRUPTION DETECTED") 
        print("   → Timing-based scanning CONFIRMED")
        print("   → API context triggers delayed corruption")
        corruption_details = result.get('corruption_details', {})
        print(f"   → Detected after: {corruption_details.get('time_since_write', 'N/A'):.3f}s")
        print(f"   → Final size: {result['final_size']:,} bytes")
        return True
        
    else:
        print("✅ NO CORRUPTION DETECTED")
        print("   → Timing precision theory DISPROVEN")
        print(f"   → Final size: {result['final_size']:,} bytes (expected: {result['expected_size']:,})")
        print("   → Root cause remains unknown")
        
        # Show timing events for analysis
        print(f"\n📊 TIMING EVENTS SUMMARY")
        print("-" * 25)
        for i, event in enumerate(replicator.events[-10:], 1):  # Last 10 events
            timestamp = datetime.fromtimestamp(event['timestamp']).strftime('%H:%M:%S.%f')[:-3]
            print(f"  {i:2d}. [{timestamp}] {event['event']}")
        
        return False


if __name__ == "__main__":
    try:
        corruption_detected = run_timing_precision_test()
        
        if corruption_detected:
            print(f"\n🎯 CONCLUSION: Timing-based corruption confirmed")
            print("   Root cause: API timing + file I/O race conditions")
            exit(0)
        else:
            print(f"\n🔄 CONCLUSION: All theories disproven")  
            print("   Root cause: Unknown - requires deeper investigation")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(2)