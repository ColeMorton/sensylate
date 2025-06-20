#!/usr/bin/env python3
"""
Pre-Execution Validation Script
MANDATORY: Run this before ANY command execution to prevent collaboration failures
"""

import sys
import argparse
from pathlib import Path

# Add team-workspace to path
workspace_path = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_path / "shared"))

from collaboration_engine import CollaborationEngine

def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description="Validate workspace before command execution")
    parser.add_argument("command", help="Command name to validate")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")

    args = parser.parse_args()

    print(f"🔍 Validating workspace for command: {args.command}")

    # Initialize collaboration engine
    engine = CollaborationEngine()

    # Run validation
    result = engine.validate_before_execution(args.command)

    # Display results
    print(f"\n{'='*60}")
    print(f"VALIDATION RESULT: {'✅ PASSED' if result['validation_passed'] else '❌ FAILED'}")
    print(f"{'='*60}")

    # Show errors
    if result["errors"]:
        print(f"\n🚨 ERRORS ({len(result['errors'])}):")
        for error in result["errors"]:
            print(f"  ❌ {error.get('message', str(error))}")

    # Show warnings
    if result["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(result['warnings'])}):")
        for warning in result["warnings"]:
            print(f"  ⚠️  {warning}")

    # Show recommendations
    if result["recommendations"]:
        print(f"\n💡 RECOMMENDATIONS ({len(result['recommendations'])}):")
        for rec in result["recommendations"]:
            print(f"  💡 {rec}")

    # Show workspace summary if requested
    if args.report:
        print(f"\n📊 WORKSPACE SUMMARY:")
        for cmd, summary in result["workspace_summary"].items():
            completion = f"{summary['completion_rate']:.0%}"
            status_icon = "✅" if summary['completion_rate'] == 1.0 else "⏳"
            print(f"  {status_icon} {cmd}: {completion} complete")
            if summary['active_phase']:
                print(f"    📍 Active: {summary['active_phase']}")
            if summary['last_execution']:
                print(f"    🕒 Last: {summary['last_execution']}")

    # Determine exit code
    exit_code = 0
    if not result["validation_passed"]:
        exit_code = 1
    elif args.strict and result["warnings"]:
        print(f"\n🚫 STRICT MODE: Failing due to {len(result['warnings'])} warnings")
        exit_code = 1

    if exit_code == 0:
        print(f"\n✅ Validation passed - safe to execute {args.command}")
    else:
        print(f"\n❌ Validation failed - resolve issues before executing {args.command}")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())
