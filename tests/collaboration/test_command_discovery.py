#!/usr/bin/env python3
"""
Unit tests for command discovery and resolution functionality
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import yaml
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from team_workspace.shared.collaboration_engine import CollaborationEngine
from tests.collaboration.test_helpers import CollaborationTestFramework


class TestCommandDiscovery(unittest.TestCase):
    """Test command discovery and resolution functionality"""

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

    def test_command_discovery_success(self):
        """Test successful command discovery"""
        # Test discovery of existing command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Verify command information
        self.assertIsNotNone(cmd_info)
        self.assertEqual(cmd_info["name"], "Test Analyzer")
        self.assertEqual(cmd_info["description"], "Analyzes test codebase health and metrics")
        self.assertEqual(cmd_info["type"], "analyzer")
        self.assertEqual(cmd_info["scope"], "test")
        self.assertIn("location", cmd_info)

        # Verify performance metrics
        self.assertIn("performance_metrics", cmd_info)
        self.assertEqual(cmd_info["performance_metrics"]["avg_execution_time"], "45s")
        self.assertEqual(cmd_info["performance_metrics"]["cache_hit_rate"], 0.75)

    def test_command_discovery_failure(self):
        """Test command discovery with non-existent command"""
        # Test discovery of non-existent command
        cmd_info = self.engine.discover_command("non-existent-command")

        # Verify None returned
        self.assertIsNone(cmd_info)

    def test_command_discovery_all_registered(self):
        """Test discovery of all registered commands"""
        expected_commands = ["test-analyzer", "test-strategist", "test-implementer"]

        for cmd_name in expected_commands:
            cmd_info = self.engine.discover_command(cmd_name)
            self.assertIsNotNone(cmd_info, f"Command {cmd_name} should be discoverable")
            self.assertEqual(cmd_info["type"], cmd_name.split("-")[1])  # analyzer, strategist, implementer

    def test_project_command_precedence(self):
        """Test that project commands take precedence over user commands"""
        # Create project commands directory
        project_cmd_dir = self.test_workspace / ".claude" / "commands"
        project_cmd_dir.mkdir(parents=True)

        # Create project-specific command
        project_cmd_content = "# Project-Specific Test Analyzer\n\nThis is project-specific."
        project_cmd_file = project_cmd_dir / "test-analyzer.md"
        with open(project_cmd_file, "w") as f:
            f.write(project_cmd_content)

        # Create user commands directory (simulate)
        user_cmd_dir = self.test_workspace / "user_commands"
        user_cmd_dir.mkdir(parents=True)

        # Create user command
        user_cmd_content = "# User Test Analyzer\n\nThis is user-global."
        user_cmd_file = user_cmd_dir / "test-analyzer.md"
        with open(user_cmd_file, "w") as f:
            f.write(user_cmd_content)

        # Override engine's user commands path for testing
        self.engine.user_commands_path = user_cmd_dir
        self.engine.registry["commands"]["test-analyzer"]["location"] = str(user_cmd_file)

        # Discover command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Verify project command is resolved
        self.assertIn("resolved_location", cmd_info)
        resolved_path = Path(cmd_info["resolved_location"])

        if resolved_path.exists():
            with open(resolved_path, "r") as f:
                content = f.read()
            self.assertIn("Project-Specific", content)
            self.assertNotIn("user-global", content)

    def test_user_command_fallback(self):
        """Test fallback to user commands when project commands don't exist"""
        # Create user commands directory (simulate)
        user_cmd_dir = self.test_workspace / "user_commands"
        user_cmd_dir.mkdir(parents=True)

        # Create user command
        user_cmd_content = "# User Test Analyzer\n\nThis is user-global."
        user_cmd_file = user_cmd_dir / "test-analyzer.md"
        with open(user_cmd_file, "w") as f:
            f.write(user_cmd_content)

        # Override engine's user commands path for testing
        self.engine.user_commands_path = user_cmd_dir
        self.engine.registry["commands"]["test-analyzer"]["location"] = str(user_cmd_file)

        # Ensure no project commands exist
        project_cmd_dir = self.test_workspace / ".claude" / "commands"
        if project_cmd_dir.exists():
            shutil.rmtree(project_cmd_dir)

        # Discover command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Verify user command is resolved
        self.assertIn("resolved_location", cmd_info)
        resolved_path = Path(cmd_info["resolved_location"])

        if resolved_path.exists():
            with open(resolved_path, "r") as f:
                content = f.read()
            self.assertIn("user-global", content)

    def test_command_location_fallback_original(self):
        """Test fallback to original location when neither project nor user commands exist"""
        # Create command at original location
        original_location = self.test_workspace / "original_analyzer.md"
        with open(original_location, "w") as f:
            f.write("# Original Test Analyzer\n\nThis is the original location.")

        # Update registry with original location
        self.engine.registry["commands"]["test-analyzer"]["location"] = str(original_location)

        # Override paths to non-existent directories
        self.engine.project_commands_path = self.test_workspace / "non_existent_project"
        self.engine.user_commands_path = self.test_workspace / "non_existent_user"

        # Discover command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Verify original location is resolved
        self.assertIn("resolved_location", cmd_info)
        resolved_path = Path(cmd_info["resolved_location"])

        if resolved_path.exists():
            with open(resolved_path, "r") as f:
                content = f.read()
            self.assertIn("Original Test Analyzer", content)

    def test_command_location_not_found(self):
        """Test handling when command file cannot be found"""
        # Update registry with non-existent location
        self.engine.registry["commands"]["test-analyzer"]["location"] = "/non/existent/path.md"

        # Override paths to non-existent directories
        self.engine.project_commands_path = self.test_workspace / "non_existent_project"
        self.engine.user_commands_path = self.test_workspace / "non_existent_user"

        # Discover command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Should still return command info, but without resolved location
        self.assertIsNotNone(cmd_info)
        self.assertNotIn("resolved_location", cmd_info)

    def test_manifest_loading_success(self):
        """Test successful manifest loading during discovery"""
        # Create manifest file
        manifest_path = self.test_workspace / "test-analyzer-manifest.yaml"
        manifest_data = {
            "command": {
                "name": "test-analyzer",
                "version": "1.0.0",
                "description": "Test analyzer with manifest"
            },
            "dependencies": {
                "required": [],
                "optional": [
                    {
                        "command": "code-owner",
                        "output_type": "health_assessment",
                        "enhancement": "Previous health metrics for trend analysis"
                    }
                ]
            },
            "collaboration": {
                "pre_execution_behavior": ["scan_workspace"],
                "post_execution_behavior": ["store_results"],
                "cache_strategy": "session_based"
            }
        }

        with open(manifest_path, "w") as f:
            yaml.dump(manifest_data, f)

        # Update registry with manifest location
        self.engine.registry["commands"]["test-analyzer"]["manifest"] = str(manifest_path)

        # Discover command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Verify manifest data loaded
        self.assertIn("manifest_data", cmd_info)
        manifest = cmd_info["manifest_data"]

        self.assertEqual(manifest["command"]["name"], "test-analyzer")
        self.assertEqual(manifest["command"]["version"], "1.0.0")
        self.assertIn("dependencies", manifest)
        self.assertIn("collaboration", manifest)

        # Verify collaboration config
        collab = manifest["collaboration"]
        self.assertIn("scan_workspace", collab["pre_execution_behavior"])
        self.assertEqual(collab["cache_strategy"], "session_based")

    def test_manifest_loading_failure(self):
        """Test handling of non-existent or corrupted manifest files"""
        # Update registry with non-existent manifest
        self.engine.registry["commands"]["test-analyzer"]["manifest"] = "/non/existent/manifest.yaml"

        # Discover command
        cmd_info = self.engine.discover_command("test-analyzer")

        # Should still return command info, but without manifest data
        self.assertIsNotNone(cmd_info)
        self.assertNotIn("manifest_data", cmd_info)

    def test_manifest_loading_corrupted(self):
        """Test handling of corrupted manifest files"""
        # Create corrupted manifest file
        manifest_path = self.test_workspace / "corrupted-manifest.yaml"
        with open(manifest_path, "w") as f:
            f.write("invalid: yaml: content: [[[")

        # Update registry with corrupted manifest
        self.engine.registry["commands"]["test-analyzer"]["manifest"] = str(manifest_path)

        # Discover command - should handle gracefully
        try:
            cmd_info = self.engine.discover_command("test-analyzer")

            # Should return command info without manifest data
            self.assertIsNotNone(cmd_info)
            self.assertNotIn("manifest_data", cmd_info)

        except yaml.YAMLError:
            self.fail("Engine should handle corrupted manifest gracefully")

    def test_scope_awareness(self):
        """Test command discovery with scope awareness"""
        # Verify test commands have correct scope
        cmd_info = self.engine.discover_command("test-analyzer")
        self.assertEqual(cmd_info["scope"], "test")

        # Create command with different scope
        self.engine.registry["commands"]["global-command"] = {
            "name": "Global Command",
            "type": "utility",
            "scope": "global",
            "location": "/global/path.md"
        }

        global_cmd = self.engine.discover_command("global-command")
        self.assertEqual(global_cmd["scope"], "global")

    def test_command_discovery_logging(self):
        """Test that command discovery generates appropriate logs"""
        # Clear any existing logs
        log_file = self.engine.session_path / "collaboration-engine.log"
        if log_file.exists():
            log_file.unlink()

        # Perform discovery operations
        self.engine.discover_command("test-analyzer")
        self.engine.discover_command("non-existent-command")

        # Verify log entries
        with open(log_file, "r") as f:
            log_content = f.read()

        self.assertIn("Discovered command: test-analyzer", log_content)
        self.assertIn("Command not found in registry: non-existent-command", log_content)

    def test_command_discovery_registry_update(self):
        """Test command discovery after registry updates"""
        # Initial discovery
        cmd_info = self.engine.discover_command("test-analyzer")
        self.assertIsNotNone(cmd_info)

        # Add new command to registry
        self.engine.registry["commands"]["new-test-command"] = {
            "name": "New Test Command",
            "description": "Newly added test command",
            "type": "test",
            "scope": "test",
            "location": "/test/new-command.md"
        }

        # Discover new command
        new_cmd_info = self.engine.discover_command("new-test-command")
        self.assertIsNotNone(new_cmd_info)
        self.assertEqual(new_cmd_info["name"], "New Test Command")

    def test_discovery_performance_metrics(self):
        """Test that performance metrics are correctly included in discovery"""
        cmd_info = self.engine.discover_command("test-analyzer")

        # Verify performance metrics exist
        self.assertIn("performance_metrics", cmd_info)
        metrics = cmd_info["performance_metrics"]

        # Verify expected metrics
        self.assertIn("avg_execution_time", metrics)
        self.assertIn("cache_hit_rate", metrics)

        # Verify correct values
        self.assertEqual(metrics["avg_execution_time"], "45s")
        self.assertEqual(metrics["cache_hit_rate"], 0.75)

    def test_multi_project_command_discovery(self):
        """Test command discovery across multiple projects"""
        # Create second project workspace
        project2_workspace = self.test_framework.setup_test_workspace("project2")

        # Create different registry for project2
        registry2 = {
            "commands": {
                "project2-analyzer": {
                    "name": "Project 2 Analyzer",
                    "type": "analyzer",
                    "scope": "project",
                    "location": "/project2/analyzer.md"
                }
            }
        }

        registry2_path = project2_workspace / "team-workspace" / "commands" / "registry.yaml"
        with open(registry2_path, "w") as f:
            yaml.dump(registry2, f)

        # Create engine for project2
        engine2 = CollaborationEngine(
            workspace_path=str(project2_workspace / "team-workspace"),
            project_name="project2"
        )

        # Test discovery isolation
        # Project 1 should find test-analyzer, not project2-analyzer
        cmd1 = self.engine.discover_command("test-analyzer")
        cmd1_p2 = self.engine.discover_command("project2-analyzer")

        self.assertIsNotNone(cmd1)
        self.assertIsNone(cmd1_p2)

        # Project 2 should find project2-analyzer, not test-analyzer
        cmd2 = engine2.discover_command("project2-analyzer")
        cmd2_p1 = engine2.discover_command("test-analyzer")

        self.assertIsNotNone(cmd2)
        self.assertIsNone(cmd2_p1)


if __name__ == "__main__":
    unittest.main()
