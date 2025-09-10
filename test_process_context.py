#!/usr/bin/env python3
"""
Process Context Isolation Test

Tests whether the yarn->node->python execution chain triggers corruption
without involving actual API calls. This isolates process context factors.
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


def create_realistic_btc_data() -> pd.DataFrame:
    """Create realistic BTC data matching the size and format of real pipeline data"""
    
    print("📊 Creating realistic BTC data for process context test...")
    
    # Create data matching typical BTC-USD daily.csv size (~370KB)
    dates = pd.date_range('2014-09-17', '2025-09-08', freq='D')
    
    data = []
    base_price = 457.33  # Historical BTC starting price
    
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
    print(f"📊 Generated {len(df)} rows of realistic BTC data ({len(df.to_csv(index=False).encode('utf-8')):,} bytes)")
    
    return df


def test_python_direct_write(btc_data: pd.DataFrame) -> dict:
    """Test direct Python write (control case)"""
    
    print(f"\n🧪 TEST: Direct Python Write (Control)")
    print("=" * 40)
    
    test_path = Path("frontend/public/data/raw/stocks/BTC-USD/direct_test.csv")
    test_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_manager = FileProtectionManager()
    expected_size = len(btc_data.to_csv(index=False).encode('utf-8'))
    
    start_time = time.time()
    write_success = file_manager.protected_write_csv(df=btc_data, file_path=test_path)
    write_time = time.time() - start_time
    
    if not write_success:
        return {'test': 'Direct Python', 'success': False, 'error': 'Write failed'}
    
    if test_path.exists():
        final_size = test_path.stat().st_size
        corrupted = final_size < 100
        
        print(f"📏 Size: {final_size:,} bytes (expected: {expected_size:,})")
        print(f"✅ Result: {'CORRUPTED' if corrupted else 'SUCCESS'}")
        
        return {
            'test': 'Direct Python',
            'success': True,
            'corrupted': corrupted,
            'size': final_size,
            'expected_size': expected_size,
            'write_time': write_time
        }
    
    return {'test': 'Direct Python', 'success': False, 'error': 'File disappeared'}


def test_node_spawned_python(btc_data: pd.DataFrame) -> dict:
    """Test Python spawned by Node.js (simulating pipeline context)"""
    
    print(f"\n🧪 TEST: Node.js → Python Chain")
    print("=" * 40)
    
    # Create temporary data file for the child process
    temp_data_path = Path("/tmp/test_btc_data.csv")
    btc_data.to_csv(temp_data_path, index=False)
    
    # Create temporary Python script that mimics the pipeline's file write
    temp_script = Path("/tmp/pipeline_write_test.py")
    script_content = f'''
import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "scripts"))
sys.path.append("{Path(__file__).parent / 'scripts'}")

try:
    from file_protection_manager import FileProtectionManager
    
    # Read the test data
    df = pd.read_csv("{temp_data_path}")
    
    # Write to BTC-USD path (same as pipeline)
    test_path = Path("frontend/public/data/raw/stocks/BTC-USD/node_spawned_test.csv")
    test_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_manager = FileProtectionManager()
    success = file_manager.protected_write_csv(df=df, file_path=test_path)
    
    if success and test_path.exists():
        file_size = test_path.stat().st_size
        print(f"CHILD_RESULT:{{success:true,size:{{file_size}}}}")
    else:
        print("CHILD_RESULT:{{success:false,error:'write_failed'}}")
        
except Exception as e:
    print(f"CHILD_RESULT:{{success:false,error:'{{str(e)}}'}}")
'''
    
    temp_script.write_text(script_content)
    
    # Create Node.js script that spawns Python (mimicking the pipeline)
    node_script = Path("/tmp/test_node_spawn.js")
    node_content = f'''
const {{ spawn }} = require('child_process');
const path = require('path');

console.log("📡 Node.js spawning Python process...");

const python = spawn('python3', ['{temp_script}'], {{
    cwd: '{Path.cwd()}',
    stdio: ['inherit', 'pipe', 'pipe'],
    env: process.env
}});

let output = '';
let error = '';

python.stdout.on('data', (data) => {{
    output += data.toString();
}});

python.stderr.on('data', (data) => {{
    error += data.toString();
}});

python.on('close', (code) => {{
    console.log(`✅ Python process completed (exit code: ${{code}})`);
    if (output) {{
        console.log(output.trim());
    }}
    if (error) {{
        console.error(error.trim());
    }}
}});
'''
    
    node_script.write_text(node_content)
    
    # Execute Node.js script (mimicking yarn data:pipeline)
    expected_size = len(btc_data.to_csv(index=False).encode('utf-8'))
    
    print("🚀 Executing Node.js → Python chain...")
    start_time = time.time()
    
    result = subprocess.run(
        ['node', str(node_script)], 
        cwd=Path.cwd(),
        capture_output=True, 
        text=True,
        timeout=30
    )
    
    exec_time = time.time() - start_time
    
    print(f"📋 Node.js output: {result.stdout}")
    if result.stderr:
        print(f"❌ Node.js error: {result.stderr}")
    
    # Check the result file
    result_path = Path("frontend/public/data/raw/stocks/BTC-USD/node_spawned_test.csv")
    
    if result_path.exists():
        final_size = result_path.stat().st_size
        corrupted = final_size < 100
        
        print(f"📏 Size: {final_size:,} bytes (expected: {expected_size:,})")
        print(f"✅ Result: {'CORRUPTED' if corrupted else 'SUCCESS'}")
        
        # Cleanup
        temp_data_path.unlink(missing_ok=True)
        temp_script.unlink(missing_ok=True)  
        node_script.unlink(missing_ok=True)
        
        return {
            'test': 'Node → Python',
            'success': True,
            'corrupted': corrupted,
            'size': final_size,
            'expected_size': expected_size,
            'exec_time': exec_time,
            'node_exit_code': result.returncode
        }
    else:
        print("❌ Result file not found")
        return {
            'test': 'Node → Python', 
            'success': False, 
            'error': 'Result file missing',
            'node_exit_code': result.returncode
        }


def test_yarn_node_python_chain(btc_data: pd.DataFrame) -> dict:
    """Test full yarn → node → python chain (closest to actual pipeline)"""
    
    print(f"\n🧪 TEST: Yarn → Node.js → Python Chain")
    print("=" * 45)
    
    # Create temporary package.json for yarn test
    temp_package = Path("/tmp/test_package.json")
    package_content = {
        "name": "process-context-test",
        "version": "1.0.0",
        "scripts": {
            "test:write": f"node {Path('/tmp/test_yarn_node.js')}"
        }
    }
    
    temp_package.write_text(json.dumps(package_content, indent=2))
    
    # Create data file
    temp_data_path = Path("/tmp/test_btc_data_yarn.csv")
    btc_data.to_csv(temp_data_path, index=False)
    
    # Create Python script
    temp_script = Path("/tmp/pipeline_yarn_test.py")
    script_content = f'''
import sys
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "scripts"))
sys.path.append("{Path(__file__).parent / 'scripts'}")

try:
    from file_protection_manager import FileProtectionManager
    
    df = pd.read_csv("{temp_data_path}")
    
    test_path = Path("frontend/public/data/raw/stocks/BTC-USD/yarn_spawned_test.csv")
    test_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_manager = FileProtectionManager()
    success = file_manager.protected_write_csv(df=df, file_path=test_path)
    
    if success and test_path.exists():
        file_size = test_path.stat().st_size
        print(f"YARN_RESULT:{{success:true,size:{{file_size}}}}")
    else:
        print("YARN_RESULT:{{success:false,error:'write_failed'}}")
        
except Exception as e:
    print(f"YARN_RESULT:{{success:false,error:'{{str(e)}}'}}")
'''
    
    temp_script.write_text(script_content)
    
    # Create Node.js script
    node_script = Path("/tmp/test_yarn_node.js")
    node_content = f'''
const {{ spawn }} = require('child_process');

console.log("🧶 Yarn spawned Node.js spawning Python...");

const python = spawn('python3', ['{temp_script}'], {{
    cwd: '{Path.cwd()}',
    stdio: ['inherit', 'pipe', 'pipe'],
    env: process.env
}});

let output = '';
let error = '';

python.stdout.on('data', (data) => {{
    output += data.toString();
}});

python.stderr.on('data', (data) => {{
    error += data.toString();
}});

python.on('close', (code) => {{
    console.log(`✅ Python process completed (exit code: ${{code}})`);
    if (output) {{
        console.log(output.trim());
    }}
    if (error && error.trim() !== '') {{
        console.error(error.trim());
    }}
}});
'''
    
    node_script.write_text(node_content)
    
    # Execute yarn command (mimicking actual pipeline invocation)
    expected_size = len(btc_data.to_csv(index=False).encode('utf-8'))
    
    print("🧶 Executing Yarn → Node.js → Python chain...")
    start_time = time.time()
    
    result = subprocess.run(
        ['yarn', 'test:write'], 
        cwd=Path('/tmp'),
        capture_output=True, 
        text=True,
        timeout=45
    )
    
    exec_time = time.time() - start_time
    
    print(f"📋 Yarn output: {result.stdout}")
    if result.stderr:
        print(f"⚠️  Yarn stderr: {result.stderr}")
    
    # Check the result file
    result_path = Path("frontend/public/data/raw/stocks/BTC-USD/yarn_spawned_test.csv")
    
    cleanup_files = [temp_package, temp_data_path, temp_script, node_script]
    
    if result_path.exists():
        final_size = result_path.stat().st_size
        corrupted = final_size < 100
        
        print(f"📏 Size: {final_size:,} bytes (expected: {expected_size:,})")
        print(f"✅ Result: {'CORRUPTED' if corrupted else 'SUCCESS'}")
        
        # Cleanup temp files
        for f in cleanup_files:
            f.unlink(missing_ok=True)
        
        return {
            'test': 'Yarn → Node → Python',
            'success': True,
            'corrupted': corrupted,
            'size': final_size,
            'expected_size': expected_size,
            'exec_time': exec_time,
            'yarn_exit_code': result.returncode
        }
    else:
        print("❌ Result file not found")
        
        # Cleanup temp files  
        for f in cleanup_files:
            f.unlink(missing_ok=True)
            
        return {
            'test': 'Yarn → Node → Python', 
            'success': False, 
            'error': 'Result file missing',
            'yarn_exit_code': result.returncode
        }


def run_process_context_tests():
    """Main test runner for process context isolation"""
    
    print("🔬 PROCESS CONTEXT ISOLATION TEST")
    print("=" * 50)
    print("Theory: Multi-process execution chain triggers corruption")
    print()
    
    # Generate test data
    btc_data = create_realistic_btc_data()
    
    # Run tests in order of complexity
    results = []
    
    # Test 1: Direct Python (control)
    results.append(test_python_direct_write(btc_data))
    
    # Test 2: Node → Python
    results.append(test_node_spawned_python(btc_data))
    
    # Test 3: Yarn → Node → Python (full chain)
    results.append(test_yarn_node_python_chain(btc_data))
    
    # Analyze results
    print(f"\n📋 PROCESS CONTEXT TEST RESULTS")
    print("=" * 40)
    
    corruption_found = False
    corruption_level = None
    
    for result in results:
        test_name = result['test']
        if result.get('success'):
            if result.get('corrupted'):
                print(f"🚨 {test_name}: CORRUPTION DETECTED")
                print(f"   Size: {result['size']:,} → {result['expected_size']:,} bytes")
                corruption_found = True
                if corruption_level is None:
                    corruption_level = test_name
            else:
                print(f"✅ {test_name}: No corruption")
                print(f"   Size: {result['size']:,} bytes")
        else:
            print(f"❌ {test_name}: Test failed - {result.get('error', 'unknown error')}")
    
    # Conclusion
    print(f"\n🎯 PROCESS CONTEXT ANALYSIS")
    print("=" * 30)
    
    if corruption_found:
        print(f"✅ PROCESS THEORY CONFIRMED")
        print(f"   → Corruption triggered at: {corruption_level}")
        print(f"   → Process execution chain IS the root cause")
        
        if corruption_level == "Node → Python":
            print(f"   → Node.js process spawning triggers corruption")
        elif corruption_level == "Yarn → Node → Python":
            print(f"   → Full yarn pipeline chain triggers corruption")
        
        return True
    else:
        print(f"❌ PROCESS THEORY DISPROVEN")
        print(f"   → Process execution chain does NOT trigger corruption")
        print(f"   → Must investigate timing precision factors")
        return False


if __name__ == "__main__":
    try:
        corruption_detected = run_process_context_tests()
        
        if corruption_detected:
            print(f"\n🎯 CONCLUSION: Process context confirmed")
            print("   Next: Identify specific process trigger")
            exit(0)
        else:
            print(f"\n🔄 CONCLUSION: Process context is NOT the trigger")  
            print("   Next: Focus on timing precision factors")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(2)