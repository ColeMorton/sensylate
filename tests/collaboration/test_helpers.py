#!/usr/bin/env python3
"""
Test utilities and helpers for Command Collaboration Framework testing
"""

import tempfile
import shutil
import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import hashlib


class CollaborationTestFramework:
    """Test utilities for Command Collaboration Framework"""

    def __init__(self):
        self.test_workspace = None
        self.test_commands = {}
        self.test_outputs = {}

    def setup_test_workspace(self, project_name: str = "test-project") -> Path:
        """Create clean test workspace with sample data"""
        # Create temporary directory
        self.test_workspace = Path(tempfile.mkdtemp(prefix=f"{project_name}_"))

        # Create directory structure
        workspace_path = self.test_workspace / "team-workspace"
        (workspace_path / "commands").mkdir(parents=True)
        (workspace_path / "shared").mkdir(parents=True)
        (workspace_path / "sessions").mkdir(parents=True)

        # Copy test fixtures
        fixtures_path = Path(__file__).parent.parent / "fixtures" / "collaboration"

        # Copy registry
        shutil.copy(
            fixtures_path / "test_registry.yaml",
            workspace_path / "commands" / "registry.yaml"
        )

        # Copy metadata schema
        shutil.copy(
            fixtures_path / "test_metadata_schema.yaml",
            workspace_path / "shared" / "metadata-schema.yaml"
        )

        # Create project context
        project_context = {
            "project": {
                "name": project_name,
                "type": "test",
                "created_at": datetime.now().isoformat(),
                "test_mode": True
            },
            "environment": {
                "type": "test",
                "data_sources": ["mock_data"],
                "constraints": []
            }
        }

        with open(workspace_path / "shared" / "project-context.yaml", "w") as f:
            yaml.dump(project_context, f)

        # Create command directories
        for cmd in ["test-analyzer", "test-strategist", "test-implementer"]:
            cmd_dir = workspace_path / "commands" / cmd
            (cmd_dir / "outputs").mkdir(parents=True)
            (cmd_dir / "cache").mkdir(parents=True)

        return self.test_workspace

    def create_test_command(self, name: str, dependencies: List[str] = None,
                          outputs: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate test command with specified dependencies"""
        if dependencies is None:
            dependencies = []
        if outputs is None:
            outputs = [{"type": "test_output", "format": "markdown"}]

        command_data = {
            "name": name,
            "type": "test",
            "scope": "test",
            "manifest": {
                "command": {
                    "name": name,
                    "version": "1.0.0",
                    "type": "test",
                    "description": f"Test command {name}"
                },
                "dependencies": {
                    "required": dependencies,
                    "optional": []
                },
                "outputs": outputs,
                "collaboration": {
                    "pre_execution_behavior": ["scan_workspace_for_relevant_data"],
                    "post_execution_behavior": ["store_analysis_results"],
                    "output_sharing": "immediate",
                    "cache_strategy": "session_based"
                }
            }
        }

        self.test_commands[name] = command_data
        return command_data

    def create_test_output(self, command_name: str, output_type: str = "test_output",
                         content: str = None, quality_score: float = 0.85) -> Tuple[Path, Path]:
        """Create test command output with metadata"""
        if content is None:
            content = f"# Test Output from {command_name}\n\nThis is test content."

        workspace_path = self.test_workspace / "team-workspace"
        output_dir = workspace_path / "commands" / command_name / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = output_dir / f"{output_type}-{timestamp}.md"
        meta_file = output_dir / f".{output_type}-{timestamp}.command-meta.yaml"

        # Write content
        with open(output_file, "w") as f:
            f.write(content)

        # Create metadata
        metadata = {
            "metadata": {
                "command": command_name,
                "timestamp": datetime.now().isoformat() + "Z",
                "version": "1.0.0",
                "session_id": f"test-session-{timestamp}"
            },
            "input_context": {
                "dependencies_used": [],
                "optimization_data": []
            },
            "output_specification": {
                "type": output_type,
                "format": "markdown",
                "size_bytes": len(content.encode()),
                "line_count": len(content.splitlines())
            },
            "quality_metrics": {
                "quality_score": quality_score,
                "confidence_level": "high" if quality_score > 0.8 else "medium",
                "validation_passed": True,
                "execution_time": "1.5s",
                "content_hash": hashlib.sha256(content.encode()).hexdigest()
            },
            "collaboration_data": {
                "intended_consumers": [],
                "sharing_policy": "immediate",
                "cache_expires": (datetime.now() + timedelta(hours=24)).isoformat()
            }
        }

        with open(meta_file, "w") as f:
            yaml.dump(metadata, f)

        self.test_outputs[command_name] = {
            "output_file": output_file,
            "meta_file": meta_file,
            "metadata": metadata
        }

        return output_file, meta_file

    def measure_performance(self, command_sequence: List[str],
                          with_collaboration: bool = True) -> Dict[str, Any]:
        """Execute and measure command chain performance"""
        import time

        results = {
            "commands": command_sequence,
            "collaboration_enabled": with_collaboration,
            "execution_times": {},
            "total_time": 0,
            "cache_hits": 0,
            "data_reuse": []
        }

        start_time = time.time()

        for cmd in command_sequence:
            cmd_start = time.time()

            # Simulate command execution
            time.sleep(0.1)  # Base execution time

            if with_collaboration and cmd in self.test_outputs:
                # Simulate faster execution due to collaboration
                results["cache_hits"] += 1
                results["data_reuse"].append(cmd)
            else:
                # Simulate normal execution
                time.sleep(0.2)

            cmd_time = time.time() - cmd_start
            results["execution_times"][cmd] = cmd_time

        results["total_time"] = time.time() - start_time

        return results

    def validate_metadata_compliance(self, metadata_path: Path) -> Dict[str, Any]:
        """Verify metadata schema compliance"""
        with open(metadata_path, "r") as f:
            metadata = yaml.safe_load(f)

        # Load schema
        schema_path = self.test_workspace / "team-workspace" / "shared" / "metadata-schema.yaml"
        with open(schema_path, "r") as f:
            schema = yaml.safe_load(f)

        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # Check required fields
        for section, section_schema in schema.items():
            if section not in metadata:
                validation_results["valid"] = False
                validation_results["errors"].append(f"Missing required section: {section}")
                continue

            if "required" in section_schema:
                for field in section_schema["required"]:
                    if field not in metadata[section]:
                        validation_results["valid"] = False
                        validation_results["errors"].append(
                            f"Missing required field: {section}.{field}"
                        )

        return validation_results

    def simulate_failure_scenario(self, failure_type: str) -> None:
        """Create specific failure conditions for testing"""
        workspace_path = self.test_workspace / "team-workspace"

        if failure_type == "corrupted_registry":
            # Corrupt the registry file
            registry_path = workspace_path / "commands" / "registry.yaml"
            with open(registry_path, "w") as f:
                f.write("invalid: yaml: content: [[[")

        elif failure_type == "missing_dependencies":
            # Remove command outputs
            for cmd_dir in (workspace_path / "commands").iterdir():
                if cmd_dir.is_dir():
                    outputs_dir = cmd_dir / "outputs"
                    if outputs_dir.exists():
                        shutil.rmtree(outputs_dir)

        elif failure_type == "invalid_metadata":
            # Create outputs with invalid metadata
            for cmd_dir in (workspace_path / "commands").iterdir():
                if cmd_dir.is_dir():
                    outputs_dir = cmd_dir / "outputs"
                    for meta_file in outputs_dir.glob("*.command-meta.yaml"):
                        with open(meta_file, "w") as f:
                            f.write("invalid_metadata: true")

        elif failure_type == "workspace_permissions":
            # Make workspace read-only
            import os
            import stat
            for root, dirs, files in os.walk(workspace_path):
                for d in dirs:
                    os.chmod(os.path.join(root, d), stat.S_IRUSR | stat.S_IRGRP)
                for f in files:
                    os.chmod(os.path.join(root, f), stat.S_IRUSR | stat.S_IRGRP)

    def cleanup(self):
        """Clean up test workspace"""
        if self.test_workspace and self.test_workspace.exists():
            # Fix permissions if needed
            import os
            import stat
            for root, dirs, files in os.walk(self.test_workspace):
                for d in dirs:
                    os.chmod(os.path.join(root, d), stat.S_IRWXU)
                for f in files:
                    os.chmod(os.path.join(root, f), stat.S_IRWXU)

            shutil.rmtree(self.test_workspace)
            self.test_workspace = None

    def create_multi_project_setup(self, projects: List[str]) -> Dict[str, Path]:
        """Create multiple project workspaces for isolation testing"""
        project_paths = {}

        for project in projects:
            project_path = self.setup_test_workspace(project)

            # Create project-specific commands directory
            project_commands = project_path / ".claude" / "commands"
            project_commands.mkdir(parents=True)

            # Add project-specific command
            project_cmd = f"{project}-specific-cmd.md"
            with open(project_commands / project_cmd, "w") as f:
                f.write(f"# {project} Specific Command\n\nProject-specific implementation.")

            project_paths[project] = project_path

        return project_paths

    def generate_test_data_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Generate various test data scenarios"""
        scenarios = {
            "small_project": {
                "files": 10,
                "commands": ["analyzer", "optimizer"],
                "dependencies": "simple",
                "expected_performance": {"execution_time": "<5s", "cache_hit_rate": 0.8}
            },
            "medium_project": {
                "files": 100,
                "commands": ["analyzer", "strategist", "implementer"],
                "dependencies": "complex",
                "expected_performance": {"execution_time": "<30s", "cache_hit_rate": 0.7}
            },
            "large_project": {
                "files": 1000,
                "commands": ["analyzer", "strategist", "implementer", "optimizer", "validator"],
                "dependencies": "extensive",
                "expected_performance": {"execution_time": "<2m", "cache_hit_rate": 0.75}
            },
            "first_run": {
                "description": "Clean workspace, no team data",
                "cache_state": "empty",
                "expected_behavior": "Full execution, no optimizations"
            },
            "optimized_run": {
                "description": "Full team context available",
                "cache_state": "warm",
                "expected_behavior": "20%+ performance improvement"
            },
            "degraded_run": {
                "description": "Partial data corruption",
                "cache_state": "partial",
                "expected_behavior": "Graceful degradation, warnings generated"
            }
        }

        return scenarios


def benchmark_collaboration_gains(test_framework: CollaborationTestFramework) -> Dict[str, Any]:
    """Measure performance improvements from collaboration"""

    # Baseline: isolated execution
    baseline_results = test_framework.measure_performance(
        ["test-analyzer", "test-strategist", "test-implementer"],
        with_collaboration=False
    )

    # Create some test outputs to simulate collaboration
    test_framework.create_test_output("test-analyzer", "analysis_report")
    test_framework.create_test_output("test-strategist", "strategy_plan")

    # Collaboration: team-enhanced execution
    collaboration_results = test_framework.measure_performance(
        ["test-analyzer", "test-strategist", "test-implementer"],
        with_collaboration=True
    )

    # Calculate improvements
    improvements = {
        "speed_gain": (baseline_results["total_time"] - collaboration_results["total_time"]) / baseline_results["total_time"],
        "cache_hit_rate": collaboration_results["cache_hits"] / len(collaboration_results["commands"]),
        "data_reuse_count": len(collaboration_results["data_reuse"]),
        "baseline_time": baseline_results["total_time"],
        "optimized_time": collaboration_results["total_time"]
    }

    return improvements
