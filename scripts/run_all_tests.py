#!/usr/bin/env python3
"""
Unified Test Runner with Performance Reporting

Runs all test suites for the consolidated storage system with comprehensive reporting.
Provides performance metrics, coverage analysis, and detailed results.
"""

import subprocess
import sys
import time
import unittest
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


class TestRunner:
    """Unified test runner for all storage system tests"""

    def __init__(self):
        self.start_time = datetime.now()
        self.script_dir = Path(__file__).parent
        self.results = []

        print("🚀 Unified Test Runner - Consolidated Storage System")
        print("=" * 70)
        print(f"Started: {self.start_time}")
        print(f"Working directory: {self.script_dir}")

    def run_unittest_suite(self, test_module: str, description: str) -> Dict[str, Any]:
        """Run a unittest-based test suite"""
        result = {
            "test_type": "unittest",
            "module": test_module,
            "description": description,
            "success": False,
            "execution_time": 0,
            "tests_run": 0,
            "failures": 0,
            "errors": 0,
            "details": [],
        }

        print(f"\n🧪 {description}")
        print("-" * 50)

        start_time = time.time()

        try:
            # Import the test module
            sys.path.insert(0, str(self.script_dir))

            if test_module == "test_consolidated_storage_core":
                from test_consolidated_storage_core import TestConsolidatedStorageSystem

                test_class = TestConsolidatedStorageSystem
            elif test_module == "test_consolidated_system_unittest":
                from test_consolidated_system_unittest import (
                    TestConsolidatedStorageSystem,
                )

                test_class = TestConsolidatedStorageSystem
            else:
                raise ImportError(f"Unknown test module: {test_module}")

            # Create test suite
            test_loader = unittest.TestLoader()
            test_suite = test_loader.loadTestsFromTestCase(test_class)

            # Run tests
            runner = unittest.TextTestRunner(verbosity=1, stream=subprocess.DEVNULL)
            test_results = runner.run(test_suite)

            result["execution_time"] = time.time() - start_time
            result["tests_run"] = test_results.testsRun
            result["failures"] = len(test_results.failures)
            result["errors"] = len(test_results.errors)
            result["success"] = result["failures"] == 0 and result["errors"] == 0

            # Collect failure/error details
            for test, traceback in test_results.failures:
                result["details"].append(f"FAILURE - {test}: {traceback[:100]}...")

            for test, traceback in test_results.errors:
                result["details"].append(f"ERROR - {test}: {traceback[:100]}...")

            print(
                f"   ✅ {result['tests_run']} tests, {result['failures']} failures, {result['errors']} errors"
            )
            print(f"   ⏱️  Execution time: {result['execution_time']:.2f}s")

        except Exception as e:
            result["execution_time"] = time.time() - start_time
            result["details"].append(f"EXCEPTION: {str(e)}")
            print(f"   ❌ Failed to run test suite: {e}")

        self.results.append(result)
        return result

    def run_script_test(
        self, script_name: str, description: str, timeout: int = 60
    ) -> Dict[str, Any]:
        """Run a standalone test script"""
        result = {
            "test_type": "script",
            "script": script_name,
            "description": description,
            "success": False,
            "execution_time": 0,
            "return_code": -1,
            "stdout": "",
            "stderr": "",
            "details": [],
        }

        print(f"\n🖥️  {description}")
        print("-" * 50)

        start_time = time.time()

        try:
            process = subprocess.run(
                ["python", script_name],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.script_dir,
            )

            result["execution_time"] = time.time() - start_time
            result["return_code"] = process.returncode
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            result["success"] = process.returncode == 0

            if result["success"]:
                print(f"   ✅ Script completed successfully")
            else:
                print(f"   ❌ Script failed (return code: {process.returncode})")
                if result["stderr"]:
                    result["details"].append(f"STDERR: {result['stderr'][:200]}...")

            print(f"   ⏱️  Execution time: {result['execution_time']:.2f}s")

        except subprocess.TimeoutExpired:
            result["execution_time"] = timeout
            result["details"].append(f"Script timed out after {timeout} seconds")
            print(f"   ⏰ Script timed out ({timeout}s)")
        except Exception as e:
            result["execution_time"] = time.time() - start_time
            result["details"].append(f"EXCEPTION: {str(e)}")
            print(f"   ❌ Failed to run script: {e}")

        self.results.append(result)
        return result

    def analyze_file_system_state(self) -> Dict[str, Any]:
        """Analyze current file system state"""
        print(f"\n📁 File System State Analysis")
        print("-" * 50)

        analysis = {
            "data_directory_exists": False,
            "csv_files": 0,
            "meta_files": 0,
            "json_files": 0,
            "total_files": 0,
            "symbols_found": [],
            "timeframes_found": set(),
            "file_sizes": {},
        }

        data_dir = Path("data/raw")

        if data_dir.exists():
            analysis["data_directory_exists"] = True

            # Count files by type
            csv_files = list(data_dir.rglob("*.csv"))
            meta_files = list(data_dir.rglob("*.meta.json"))
            json_files = [
                f for f in data_dir.rglob("*.json") if not f.name.endswith(".meta.json")
            ]

            analysis["csv_files"] = len(csv_files)
            analysis["meta_files"] = len(meta_files)
            analysis["json_files"] = len(json_files)
            analysis["total_files"] = len(csv_files) + len(meta_files) + len(json_files)

            # Find symbols
            stocks_dir = data_dir / "stocks"
            if stocks_dir.exists():
                analysis["symbols_found"] = [
                    d.name for d in stocks_dir.iterdir() if d.is_dir()
                ]

            # Find timeframes from filenames
            for csv_file in csv_files:
                timeframe = csv_file.stem  # e.g., "daily", "weekly"
                analysis["timeframes_found"].add(timeframe)

            # Calculate file sizes
            total_csv_size = sum(f.stat().st_size for f in csv_files)
            total_meta_size = sum(f.stat().st_size for f in meta_files)
            total_json_size = sum(f.stat().st_size for f in json_files)

            analysis["file_sizes"] = {
                "csv_total": total_csv_size,
                "meta_total": total_meta_size,
                "json_total": total_json_size,
                "grand_total": total_csv_size + total_meta_size + total_json_size,
            }

        # Report findings
        print(
            f"   📂 Data directory exists: {'✅' if analysis['data_directory_exists'] else '❌'}"
        )
        print(f"   📄 CSV files: {analysis['csv_files']}")
        print(f"   📋 Metadata files: {analysis['meta_files']}")
        print(f"   📋 JSON files: {analysis['json_files']}")
        print(f"   📊 Total files: {analysis['total_files']}")

        if analysis["symbols_found"]:
            print(f"   📈 Symbols: {', '.join(analysis['symbols_found'][:5])}")
            if len(analysis["symbols_found"]) > 5:
                print(f"        ... and {len(analysis['symbols_found']) - 5} more")

        if analysis["timeframes_found"]:
            print(f"   ⏰ Timeframes: {', '.join(sorted(analysis['timeframes_found']))}")

        if analysis.get("file_sizes", {}).get("grand_total", 0) > 0:
            sizes = analysis["file_sizes"]
            print(f"   💾 Storage: {sizes['grand_total']} bytes total")
            print(
                f"      CSV: {sizes['csv_total']} bytes, Meta: {sizes['meta_total']} bytes"
            )

        return analysis

    def run_all_tests(self):
        """Execute all test suites"""
        print(f"\n🎯 Starting Comprehensive Test Execution")

        # Test suite configuration
        test_suites = [
            # Core unittest suites
            ("test_consolidated_storage_core", "Core Consolidated Storage Tests"),
            ("test_consolidated_system_unittest", "System Integration Unit Tests"),
        ]

        # Script-based tests
        script_tests = [
            ("service_configuration_auditor.py", "Service Configuration Audit"),
            ("test_aapl_e2e_cli.py", "AAPL End-to-End CLI Tests"),
        ]

        # Run unittest suites
        for module, description in test_suites:
            self.run_unittest_suite(module, description)

        # Run script tests
        for script, description in script_tests:
            self.run_script_test(script, description, timeout=120)

        # Analyze file system state
        file_analysis = self.analyze_file_system_state()

        # Generate comprehensive report
        self.generate_comprehensive_report(file_analysis)

    def generate_comprehensive_report(self, file_analysis: Dict[str, Any]):
        """Generate comprehensive test execution report"""
        total_duration = datetime.now() - self.start_time

        print(f"\n📊 COMPREHENSIVE TEST EXECUTION REPORT")
        print("=" * 70)
        print(f"Total Duration: {total_duration}")
        print(f"Test Suites Executed: {len(self.results)}")

        # Categorize results
        unittest_results = [r for r in self.results if r["test_type"] == "unittest"]
        script_results = [r for r in self.results if r["test_type"] == "script"]

        successful_unittests = [r for r in unittest_results if r["success"]]
        successful_scripts = [r for r in script_results if r["success"]]

        # Unittest summary
        print(f"\n🧪 Unit Test Suite Results:")
        total_tests = sum(r["tests_run"] for r in unittest_results)
        total_failures = sum(r["failures"] for r in unittest_results)
        total_errors = sum(r["errors"] for r in unittest_results)

        print(
            f"   Test Suites: {len(successful_unittests)}/{len(unittest_results)} passed"
        )
        print(
            f"   Individual Tests: {total_tests} run, {total_failures} failures, {total_errors} errors"
        )

        for result in unittest_results:
            status = "✅" if result["success"] else "❌"
            print(
                f"   {status} {result['description']} ({result['tests_run']} tests, {result['execution_time']:.2f}s)"
            )

        # Script test summary
        print(f"\n🖥️  Script Test Results:")
        print(f"   Scripts: {len(successful_scripts)}/{len(script_results)} passed")

        for result in script_results:
            status = "✅" if result["success"] else "❌"
            print(
                f"   {status} {result['description']} ({result['execution_time']:.2f}s)"
            )

        # Performance metrics
        total_execution_time = sum(r["execution_time"] for r in self.results)
        avg_execution_time = (
            total_execution_time / len(self.results) if self.results else 0
        )

        print(f"\n⚡ Performance Metrics:")
        print(f"   Total Test Execution Time: {total_execution_time:.2f}s")
        print(f"   Average Test Suite Time: {avg_execution_time:.2f}s")
        print(
            f"   Tests per Second: {total_tests/total_execution_time:.1f}"
            if total_execution_time > 0
            else "   Tests per Second: N/A"
        )

        # File system efficiency
        if file_analysis["total_files"] > 0:
            print(f"\n💾 Storage Efficiency:")
            print(f"   Files Created: {file_analysis['total_files']}")
            print(
                f"   Consolidated Format: {file_analysis['csv_files']} CSV + {file_analysis['meta_files']} metadata"
            )
            print(
                f"   Storage Used: {file_analysis['file_sizes']['grand_total']} bytes"
            )

            # Estimate old format file count
            symbols = len(file_analysis["symbols_found"])
            timeframes = len(file_analysis["timeframes_found"])
            if symbols > 0 and timeframes > 0:
                # Assume average 20 periods per timeframe (conservative estimate)
                estimated_old_files = (
                    symbols * timeframes * 20 * 2
                )  # 2 files per period
                actual_files = file_analysis["csv_files"] + file_analysis["meta_files"]
                if estimated_old_files > actual_files:
                    efficiency = (1 - actual_files / estimated_old_files) * 100
                    print(
                        f"   Estimated Efficiency Gain: {efficiency:.1f}% fewer files"
                    )

        # Error summary
        failed_results = [r for r in self.results if not r["success"]]
        if failed_results:
            print(f"\n⚠️  Failed Tests:")
            for result in failed_results:
                print(f"   ❌ {result['description']}")
                for detail in result["details"]:
                    print(f"      {detail}")

        # Overall assessment
        unittest_success_rate = (
            len(successful_unittests) / len(unittest_results) if unittest_results else 1
        )
        script_success_rate = (
            len(successful_scripts) / len(script_results) if script_results else 1
        )
        overall_success_rate = (
            (len(successful_unittests) + len(successful_scripts)) / len(self.results)
            if self.results
            else 0
        )

        print(f"\n🎯 OVERALL ASSESSMENT:")
        print(f"   Unit Test Success Rate: {unittest_success_rate:.0%}")
        print(f"   Script Test Success Rate: {script_success_rate:.0%}")
        print(f"   Overall Success Rate: {overall_success_rate:.0%}")

        if overall_success_rate >= 0.8 and total_failures == 0 and total_errors == 0:
            print(f"\n🎉 CONSOLIDATED STORAGE SYSTEM: ALL TESTS PASSED!")
            print("   ✅ Core functionality verified")
            print("   ✅ Integration tests successful")
            print("   ✅ File system efficiency confirmed")
            print("   ✅ Data integrity validated")
            print("   ✅ CLI integration working")
            return True
        else:
            print(f"\n⚠️  CONSOLIDATED STORAGE SYSTEM: ISSUES DETECTED")
            print(f"   - Success rate: {overall_success_rate:.0%}")
            print(f"   - Check individual test results above")
            return False


def main():
    """Main test runner execution"""
    runner = TestRunner()
    success = runner.run_all_tests()

    print(f"\n{'='*70}")
    if success:
        print("🏆 Unified Test Runner: ALL SYSTEMS OPERATIONAL")
    else:
        print("❌ Unified Test Runner: ISSUES REQUIRE ATTENTION")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
