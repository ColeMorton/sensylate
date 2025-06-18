#!/usr/bin/env python3
"""
Test runner for Command Collaboration Framework tests

This script provides a convenient way to run different test suites
for the team-collaboration feature.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False)
        print(f"✅ {description} - PASSED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Command Collaboration Framework tests")
    parser.add_argument("--suite", choices=["unit", "e2e", "all", "coverage"],
                       default="all", help="Test suite to run")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Run with verbose output")

    args = parser.parse_args()

    # Change to project root directory
    project_root = Path(__file__).parent.parent

    print(f"🚀 Command Collaboration Framework Test Runner")
    print(f"📁 Project root: {project_root}")
    print(f"🎯 Test suite: {args.suite}")

    results = []

    if args.suite in ["unit", "all"]:
        # Run unit tests
        verbose_flag = "-v -s" if args.verbose else "-v"

        tests = [
            ("tests/collaboration/test_collaboration_engine.py", "Core CollaborationEngine Tests"),
            ("tests/collaboration/test_command_discovery.py", "Command Discovery Tests"),
            ("tests/collaboration/test_dependency_resolution.py", "Dependency Resolution Tests"),
            ("tests/collaboration/test_team_workspace.py", "Team Workspace Management Tests"),
        ]

        for test_file, description in tests:
            cmd = f"python -m pytest {test_file} {verbose_flag} --tb=short"
            results.append(run_command(cmd, description))

    if args.suite in ["e2e", "all"]:
        # Run E2E tests
        verbose_flag = "-v -s" if args.verbose else "-v"
        cmd = f"python -m pytest tests/collaboration/test_e2e_collaboration.py {verbose_flag} --tb=long"
        results.append(run_command(cmd, "End-to-End Collaboration Tests"))

    if args.suite == "coverage":
        # Run coverage tests
        cmd = "python -m pytest tests/collaboration/ --cov=team_workspace --cov-report=html --cov-report=term"
        results.append(run_command(cmd, "Collaboration Tests with Coverage"))

        print(f"\n📊 Coverage report generated in htmlcov/index.html")

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\n{'='*60}")
    print(f"📋 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {total - passed}")
    print(f"📊 Total:  {total}")

    if passed == total:
        print(f"\n🎉 All tests passed! Team collaboration framework is working correctly.")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
