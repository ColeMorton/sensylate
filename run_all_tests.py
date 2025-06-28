#!/usr/bin/env python3
"""
Comprehensive Test Runner for Sensylate Platform
Runs all tests including framework, collaboration, and core functionality
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Run comprehensive test suite"""
    print("🚀 SENSYLATE COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    # Change to project root
    project_root = Path(__file__).parent
    print(f"📁 Working directory: {project_root}")

    test_results = []

    # 1. Run main project tests
    print("\n🔍 Running main project tests...")
    success = run_command(
        "python -m pytest tests/ -v --tb=short --disable-warnings",
        "Main Project Tests (Collaboration & Core)"
    )
    test_results.append(("Main Project Tests", success))

    # 2. Run framework integration tests
    print("\n🔍 Running framework integration tests...")
    success = run_command(
        "cd team-workspace/framework && python -m pytest tests/test_framework_integration.py -v --tb=short --disable-warnings",
        "Framework Integration Tests"
    )
    test_results.append(("Framework Integration Tests", success))

    # 3. Run framework phase tests
    print("\n🔍 Running framework phase tests...")
    phase_tests = [
        ("Phase 1 Implementation", "cd team-workspace/framework && python test_phase1_implementation.py"),
        ("Phase 2 Implementation", "cd team-workspace/framework && python test_phase2_implementation.py"),
        ("Phase 3 Implementation", "cd team-workspace/framework && python test_phase3_implementation.py"),
    ]

    for test_name, cmd in phase_tests:
        success = run_command(cmd, test_name)
        test_results.append((test_name, success))

    # 4. Run template enforcement tests
    print("\n🔍 Running template enforcement tests...")
    success = run_command(
        "cd team-workspace/framework && python template_enforcement_engine.py",
        "Template Enforcement Engine Tests"
    )
    test_results.append(("Template Enforcement Tests", success))

    # 5. Run dependency validation tests
    print("\n🔍 Running dependency validation tests...")
    success = run_command(
        "cd team-workspace/framework && python -c \"from evaluation.universal_dependency_validator import UniversalDependencyValidator; v = UniversalDependencyValidator(); print('✅ Dependency validator working')\"",
        "Dependency Validation Tests"
    )
    test_results.append(("Dependency Validation Tests", success))

    # 6. Run frontend tests if available
    print("\n🔍 Running frontend tests...")
    success = run_command(
        "cd frontend && yarn test --passWithNoTests --silent",
        "Frontend Tests"
    )
    test_results.append(("Frontend Tests", success))

    # 7. Test Universal Evaluation Framework deployment
    print("\n🔍 Testing Universal Evaluation Framework...")
    success = run_command(
        "cd team-workspace/framework && python -c \"from universal_integration_deployer import UniversalIntegrationDeployer; d = UniversalIntegrationDeployer(); print('✅ Framework deployment ready')\"",
        "Universal Evaluation Framework Validation"
    )
    test_results.append(("Universal Evaluation Framework", success))

    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)

    total_tests = len(test_results)
    passed_tests = sum(1 for _, success in test_results if success)
    failed_tests = total_tests - passed_tests

    for test_name, success in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:<12} {test_name}")

    print(f"\n📈 OVERALL RESULTS:")
    print(f"   Total Test Suites: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {failed_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {failed_tests} test suite(s) failed. Review output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
