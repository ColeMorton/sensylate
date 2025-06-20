#!/usr/bin/env python3
"""
Validate workspace before command execution.

This script validates that the team-workspace is in a healthy state before
allowing commands to execute, ensuring content integrity and preventing
conflicts.
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any

class WorkspaceValidator:
    """Validates workspace health before command execution."""

    def __init__(self, workspace_path: str = "team-workspace"):
        self.workspace_path = Path(workspace_path)
        self.coordination_path = self.workspace_path / "coordination"

    def validate_workspace(self, command_name: str) -> Dict[str, Any]:
        """
        Validate workspace health for command execution.

        Args:
            command_name: Name of command requesting validation

        Returns:
            Dict with validation results and recommendations
        """
        validation_results = {
            "validation_passed": True,
            "errors": [],
            "warnings": [],
            "recommendations": [],
            "command_name": command_name
        }

        # Check required infrastructure
        self._validate_infrastructure(validation_results)

        # Check topic registry health
        self._validate_topic_registry(validation_results)

        # Check for critical conflicts
        self._validate_conflict_status(validation_results)

        # Check workspace permissions
        self._validate_permissions(validation_results, command_name)

        # Determine overall validation status
        validation_results["validation_passed"] = len(validation_results["errors"]) == 0

        return validation_results

    def _validate_infrastructure(self, results: Dict[str, Any]):
        """Validate required infrastructure exists."""
        required_components = [
            self.coordination_path / "topic-registry.yaml",
            self.coordination_path / "superseding-log.yaml",
            self.coordination_path / "pre-execution-consultation.py",
            self.coordination_path / "topic-ownership-manager.py",
            self.coordination_path / "superseding-workflow.py",
            self.workspace_path / "knowledge",
            self.workspace_path / "archive"
        ]

        for component in required_components:
            if not component.exists():
                results["errors"].append(f"Missing required component: {component}")

    def _validate_topic_registry(self, results: Dict[str, Any]):
        """Validate topic registry is accessible and valid."""
        registry_path = self.coordination_path / "topic-registry.yaml"

        if not registry_path.exists():
            results["errors"].append("Topic registry not found")
            return

        try:
            with open(registry_path, 'r') as f:
                registry = yaml.safe_load(f)

            if not isinstance(registry, dict) or "topics" not in registry:
                results["errors"].append("Topic registry format is invalid")
                return

            # Check for registry health indicators
            topics = registry.get("topics", {})
            conflicts_detected = sum(1 for topic in topics.values()
                                   if topic.get("conflicts_detected", False))

            if conflicts_detected > 0:
                results["warnings"].append(f"{conflicts_detected} topics have detected conflicts")

        except Exception as e:
            results["errors"].append(f"Error reading topic registry: {e}")

    def _validate_conflict_status(self, results: Dict[str, Any]):
        """Check for critical workspace conflicts."""
        try:
            # Import conflict detection if available
            sys.path.append(str(self.coordination_path))
            from conflict_detection import ConflictDetector

            detector = ConflictDetector(str(self.workspace_path))
            conflicts = detector.detect_all_conflicts()

            total_conflicts = sum(len(conflict_list) for conflict_list in conflicts.values())

            if total_conflicts > 100:
                results["warnings"].append(f"High conflict count detected: {total_conflicts}")
                results["recommendations"].append("Consider running conflict resolution before proceeding")
            elif total_conflicts > 20:
                results["warnings"].append(f"Moderate conflict count: {total_conflicts}")

        except ImportError:
            results["warnings"].append("Conflict detection not available")
        except Exception as e:
            results["warnings"].append(f"Error during conflict detection: {e}")

    def _validate_permissions(self, results: Dict[str, Any], command_name: str):
        """Validate command has necessary permissions."""
        # Check write permissions to workspace
        if not self.workspace_path.exists():
            results["errors"].append("Workspace directory not accessible")
            return

        # Check write permissions to coordination directory
        if not self.coordination_path.exists():
            results["errors"].append("Coordination directory not accessible")
            return

        # Validate command-specific requirements
        if command_name in ["architect", "code-owner", "product-owner", "business-analyst"]:
            knowledge_path = self.workspace_path / "knowledge"
            if not knowledge_path.exists():
                results["errors"].append("Knowledge directory not accessible for content creation")

        if command_name == "commit-push":
            # For git operations, ensure we're in a git repository
            try:
                import subprocess
                result = subprocess.run(["git", "rev-parse", "--git-dir"],
                                      capture_output=True, text=True, cwd=self.workspace_path.parent)
                if result.returncode != 0:
                    results["warnings"].append("Not in a git repository - git operations may fail")
            except Exception:
                results["warnings"].append("Cannot validate git repository status")

def main():
    """Main validation entry point."""
    parser = argparse.ArgumentParser(description="Validate workspace before command execution")
    parser.add_argument("command_name", help="Name of command requesting validation")
    parser.add_argument("--workspace", default="team-workspace",
                       help="Path to team workspace (default: team-workspace)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed validation output")

    args = parser.parse_args()

    validator = WorkspaceValidator(args.workspace)
    results = validator.validate_workspace(args.command_name)

    # Output results
    if args.verbose or not results["validation_passed"]:
        print(f"Workspace Validation for {args.command_name}")
        print("=" * 50)

        if results["errors"]:
            print("ERRORS:")
            for error in results["errors"]:
                print(f"  ❌ {error}")
            print()

        if results["warnings"]:
            print("WARNINGS:")
            for warning in results["warnings"]:
                print(f"  ⚠️  {warning}")
            print()

        if results["recommendations"]:
            print("RECOMMENDATIONS:")
            for rec in results["recommendations"]:
                print(f"  💡 {rec}")
            print()

    if results["validation_passed"]:
        print(f"✅ Workspace validation passed for {args.command_name}")
        sys.exit(0)
    else:
        print(f"❌ Workspace validation failed for {args.command_name}")
        print("Please resolve errors before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
