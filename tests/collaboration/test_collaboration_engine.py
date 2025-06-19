#!/usr/bin/env python3
"""
Unit tests for CollaborationEngine core functionality
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import yaml
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import CollaborationEngine directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "team-workspace" / "shared"))
from collaboration_engine import CollaborationEngine
from tests.collaboration.test_helpers import CollaborationTestFramework


class TestCollaborationEngine(unittest.TestCase):
    """Test core CollaborationEngine functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_framework = CollaborationTestFramework()
        self.test_workspace = self.test_framework.setup_test_workspace()
        self.engine = CollaborationEngine(
            workspace_path=str(self.test_workspace / "team-workspace"),
            project_name="test-project"
        )

    def tearDown(self):
        """Clean up test environment"""
        self.test_framework.cleanup()

    def test_engine_initialization(self):
        """Test CollaborationEngine initialization"""
        # Verify engine properties
        self.assertEqual(self.engine.project_name, "test-project")
        self.assertEqual(str(self.engine.project_root), str(self.test_workspace))
        self.assertTrue(self.engine.workspace_path.exists())
        self.assertTrue(self.engine.commands_path.exists())
        self.assertTrue(self.engine.shared_path.exists())
        self.assertTrue(self.engine.sessions_path.exists())

        # Verify session creation
        self.assertIsNotNone(self.engine.session_id)
        self.assertTrue(self.engine.session_path.exists())


    def test_registry_loading(self):
        """Test command registry loading"""
        registry = self.engine.registry

        # Verify registry structure
        self.assertIn("commands", registry)
        self.assertIn("workflow_patterns", registry)

        # Verify test commands loaded
        self.assertIn("test-analyzer", registry["commands"])
        self.assertIn("test-strategist", registry["commands"])
        self.assertIn("test-implementer", registry["commands"])

        # Verify workflow patterns
        self.assertIn("test-analysis-flow", registry["workflow_patterns"])

    def test_metadata_schema_loading(self):
        """Test metadata schema loading"""
        schema = self.engine.metadata_schema

        # Verify schema sections
        self.assertIn("metadata", schema)
        self.assertIn("input_context", schema)
        self.assertIn("output_specification", schema)
        self.assertIn("quality_metrics", schema)
        self.assertIn("collaboration_data", schema)

        # Verify required fields
        metadata_required = schema["metadata"]["required"]
        self.assertIn("command", metadata_required)
        self.assertIn("timestamp", metadata_required)
        self.assertIn("version", metadata_required)
        self.assertIn("session_id", metadata_required)

    def test_project_context_loading(self):
        """Test project context loading"""
        context = self.engine.project_context

        # Verify context structure
        self.assertIn("project", context)
        self.assertIn("environment", context)

        # Verify project info
        self.assertEqual(context["project"]["name"], "test-project")
        self.assertEqual(context["project"]["type"], "test")
        self.assertTrue(context["project"]["test_mode"])


    def test_command_discovery(self):
        """Test command discovery functionality"""
        # Test existing command
        cmd_info = self.engine.discover_command("test-analyzer")

        self.assertIsNotNone(cmd_info)
        self.assertEqual(cmd_info["name"], "Test Analyzer")
        self.assertEqual(cmd_info["type"], "infrastructure")
        self.assertEqual(cmd_info["scope"], "test")

        # Test non-existent command
        missing_cmd = self.engine.discover_command("non-existent-command")
        self.assertIsNone(missing_cmd)

    def test_command_location_resolution(self):
        """Test command file location resolution with project/user precedence"""
        # Create project-specific command directory
        project_cmd_dir = self.test_workspace / ".claude" / "commands"
        project_cmd_dir.mkdir(parents=True)

        # Create project-specific command
        project_cmd_file = project_cmd_dir / "test-analyzer.md"
        with open(project_cmd_file, "w") as f:
            f.write("# Project-specific test-analyzer")

        # Create user command directory (simulate)
        user_cmd_dir = self.test_workspace / "user_commands"
        user_cmd_dir.mkdir(parents=True)

        # Override user commands path for testing
        self.engine.user_commands_path = user_cmd_dir

        # Create user command
        user_cmd_file = user_cmd_dir / "test-analyzer.md"
        with open(user_cmd_file, "w") as f:
            f.write("# User test-analyzer")

        # Update registry with correct location
        self.engine.registry["commands"]["test-analyzer"]["location"] = str(user_cmd_file)

        # Test resolution - should find project-specific first
        cmd_info = self.engine.discover_command("test-analyzer")
        resolved_location = Path(cmd_info.get("resolved_location", ""))

        # Verify project command takes precedence
        if resolved_location.exists():
            with open(resolved_location, "r") as f:
                content = f.read()
            self.assertIn("Project-specific", content)

    def test_manifest_loading(self):
        """Test command manifest loading"""
        # Create manifest file
        manifest_path = self.test_workspace / "test-analyzer-manifest.yaml"
        manifest_data = {
            "command": {
                "name": "test-analyzer",
                "version": "1.0.0"
            },
            "dependencies": {
                "required": [],
                "optional": [
                    {
                        "command": "code-owner",
                        "output_type": "health_assessment",
                        "enhancement": "Previous health metrics"
                    }
                ]
            }
        }

        with open(manifest_path, "w") as f:
            yaml.dump(manifest_data, f)

        # Update registry with manifest location
        self.engine.registry["commands"]["test-analyzer"]["manifest"] = str(manifest_path)

        # Discover command and verify manifest loaded
        cmd_info = self.engine.discover_command("test-analyzer")

        self.assertIn("manifest_data", cmd_info)
        self.assertEqual(
            cmd_info["manifest_data"]["command"]["name"],
            "test-analyzer"
        )

    def test_registry_integrity(self):
        """Test registry data integrity and consistency"""
        registry = self.engine.registry

        # Verify all commands have required fields
        for cmd_name, cmd_info in registry["commands"].items():
            self.assertIn("name", cmd_info)
            self.assertIn("description", cmd_info)
            self.assertIn("type", cmd_info)
            self.assertIn("scope", cmd_info)
            self.assertIn("location", cmd_info)

        # Verify workflow patterns reference valid commands
        for pattern_name, pattern_info in registry["workflow_patterns"].items():
            if "sequence" in pattern_info:
                for cmd in pattern_info["sequence"]:
                    self.assertIn(cmd, registry["commands"],
                                f"Workflow {pattern_name} references unknown command {cmd}")


    def test_logging_functionality(self):
        """Test logging setup and functionality"""
        # Verify log file exists
        log_file = self.engine.session_path / "collaboration-engine.log"
        self.assertTrue(log_file.exists())

        # Perform logged operation
        self.engine.discover_command("test-analyzer")

        # Verify log content
        with open(log_file, "r") as f:
            log_content = f.read()

        self.assertIn("Discovered command: test-analyzer", log_content)
        self.assertIn("INFO", log_content)

    def test_multi_project_isolation(self):
        """Test that multiple projects maintain isolation"""
        # Create second project
        project2_path = Path(tempfile.mkdtemp(prefix="project2_"))
        workspace2_path = project2_path / "team-workspace"
        (workspace2_path / "commands").mkdir(parents=True)
        (workspace2_path / "shared").mkdir(parents=True)
        (workspace2_path / "sessions").mkdir(parents=True)

        # Create different registry for project2
        registry2 = {
            "commands": {
                "project2-cmd": {
                    "name": "Project2 Command",
                    "type": "test",
                    "scope": "project"
                }
            }
        }

        with open(workspace2_path / "commands" / "registry.yaml", "w") as f:
            yaml.dump(registry2, f)

        try:
            # Create engines for both projects
            engine1 = self.engine
            engine2 = CollaborationEngine(
                workspace_path=str(workspace2_path),
                project_name="project2"
            )

            # Verify isolation
            self.assertIn("test-analyzer", engine1.registry["commands"])
            self.assertNotIn("test-analyzer", engine2.registry["commands"])

            self.assertNotIn("project2-cmd", engine1.registry["commands"])
            self.assertIn("project2-cmd", engine2.registry["commands"])

            # Verify different session paths
            self.assertNotEqual(engine1.session_path.parent, engine2.session_path.parent)

        finally:
            # Cleanup
            shutil.rmtree(project2_path)


if __name__ == "__main__":
    unittest.main()
