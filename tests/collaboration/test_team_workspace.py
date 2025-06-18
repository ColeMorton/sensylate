#!/usr/bin/env python3
"""
Unit tests for team workspace management functionality
"""

import unittest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import yaml
import json
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from team_workspace.shared.collaboration_engine import CollaborationEngine
from tests.collaboration.test_helpers import CollaborationTestFramework


class TestTeamWorkspace(unittest.TestCase):
    """Test team workspace management functionality"""

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

    def test_command_execution_registration(self):
        """Test registering command execution start"""
        # Create test context
        context = {
            "command": "test-analyzer",
            "available_data": {"test": "data"},
            "optimization_data": {},
            "execution_plan": {"duration": 30}
        }

        # Register execution
        log_file_path = self.engine.register_command_execution("test-analyzer", context)

        # Verify log file created
        log_file = Path(log_file_path)
        self.assertTrue(log_file.exists())

        # Verify log content
        with open(log_file, "r") as f:
            log_data = yaml.safe_load(f)

        self.assertEqual(log_data["command"], "test-analyzer")
        self.assertEqual(log_data["session_id"], self.engine.session_id)
        self.assertEqual(log_data["status"], "running")
        self.assertIn("started_at", log_data)
        self.assertEqual(log_data["context"], context)

    def test_command_output_storage(self):
        """Test storing command output with metadata"""
        # Test content and metadata
        output_content = "# Test Analysis Report\n\nThis is a test analysis."
        output_type = "analysis_report"
        base_metadata = {
            "command": "test-analyzer",
            "version": "1.0.0",
            "execution_time": "2.5s"
        }

        # Store output
        output_file, meta_file = self.engine.store_command_output(
            "test-analyzer",
            output_content,
            output_type,
            base_metadata
        )

        # Verify files created
        self.assertTrue(Path(output_file).exists())
        self.assertTrue(Path(meta_file).exists())

        # Verify output content
        with open(output_file, "r") as f:
            stored_content = f.read()
        self.assertEqual(stored_content, output_content)

        # Verify metadata enhancement
        with open(meta_file, "r") as f:
            metadata = yaml.safe_load(f)

        # Check base metadata preserved
        self.assertEqual(metadata.get("command"), "test-analyzer")
        self.assertEqual(metadata.get("version"), "1.0.0")

        # Check framework enhancements
        self.assertIn("quality_metrics", metadata)
        self.assertIn("content_hash", metadata["quality_metrics"])
        self.assertIn("metadata", metadata)
        self.assertEqual(metadata["metadata"]["session_id"], self.engine.session_id)

    def test_metadata_enhancement(self):
        """Test metadata enhancement with framework-generated data"""
        output_content = "# Test Output\n\nTest content for metadata enhancement."
        base_metadata = {
            "command": "test-analyzer",
            "version": "1.0.0"
        }

        # Test metadata enhancement
        enhanced = self.engine._enhance_metadata("test-analyzer", base_metadata, output_content)

        # Verify content hash added
        self.assertIn("quality_metrics", enhanced)
        self.assertIn("content_hash", enhanced["quality_metrics"])

        # Verify session tracking added
        self.assertIn("metadata", enhanced)
        self.assertEqual(enhanced["metadata"]["session_id"], self.engine.session_id)

        # Verify collaboration data added
        self.assertIn("collaboration_data", enhanced)
        collab_data = enhanced["collaboration_data"]
        self.assertIn("intended_consumers", collab_data)
        self.assertIn("sharing_policy", collab_data)
        self.assertIn("cache_expires", collab_data)

    def test_team_knowledge_update(self):
        """Test updating shared team knowledge base"""
        # Create test metadata
        metadata = {
            "metadata": {
                "timestamp": datetime.now().isoformat() + "Z",
                "session_id": self.engine.session_id
            },
            "output_specification": {
                "type": "implementation_plan"
            },
            "quality_metrics": {
                "quality_score": 0.95
            }
        }

        # Update team knowledge
        self.engine._update_team_knowledge("test-implementer", "# Implementation Plan", metadata)

        # Verify knowledge file created/updated
        knowledge_file = self.engine.shared_path / "team-knowledge.yaml"
        self.assertTrue(knowledge_file.exists())

        # Verify knowledge content
        with open(knowledge_file, "r") as f:
            knowledge = yaml.safe_load(f)

        # Check structure
        self.assertIn("command_outputs", knowledge)
        self.assertIn("insights", knowledge)
        self.assertIn("patterns", knowledge)

        # Check command output tracking
        self.assertIn("test-implementer", knowledge["command_outputs"])
        cmd_info = knowledge["command_outputs"]["test-implementer"]
        self.assertEqual(cmd_info["output_type"], "implementation_plan")
        self.assertEqual(cmd_info["quality_score"], 0.95)

        # Check insights extraction
        self.assertGreater(len(knowledge["insights"]), 0)
        insight = knowledge["insights"][0]
        self.assertEqual(insight["type"], "implementation_strategy")
        self.assertEqual(insight["source"], "test-implementer")

    def test_dependent_command_notification(self):
        """Test notification system for dependent commands"""
        # Create metadata with consumer information
        metadata = {
            "output_specification": {
                "type": "analysis_report"
            },
            "quality_metrics": {
                "quality_score": 0.88
            },
            "collaboration_data": {
                "intended_consumers": ["test-strategist", "test-implementer"]
            }
        }

        # Notify dependent commands
        self.engine._notify_dependent_commands("test-analyzer", metadata)

        # Verify notifications created
        for consumer in ["test-strategist", "test-implementer"]:
            notification_dir = self.engine.commands_path / consumer / "notifications"
            self.assertTrue(notification_dir.exists())

            # Find notification files
            notification_files = list(notification_dir.glob("test-analyzer-*.yaml"))
            self.assertGreater(len(notification_files), 0)

            # Verify notification content
            with open(notification_files[0], "r") as f:
                notification = yaml.safe_load(f)

            self.assertEqual(notification["event"], "dependency_available")
            self.assertEqual(notification["source_command"], "test-analyzer")
            self.assertEqual(notification["output_type"], "analysis_report")
            self.assertEqual(notification["quality_score"], 0.88)

    def test_potential_consumers_discovery(self):
        """Test discovery of potential consumers for command outputs"""
        # Create test manifests with dependencies
        consumer_manifest = {
            "dependencies": {
                "optional": [
                    {
                        "command": "test-analyzer",
                        "output_type": "analysis_report",
                        "enhancement": "Analysis insights"
                    }
                ]
            }
        }

        # Create manifest file
        manifest_path = self.test_workspace / "consumer-manifest.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(consumer_manifest, f)

        # Add consumer to registry
        self.engine.registry["commands"]["test-consumer"] = {
            "name": "Test Consumer",
            "manifest": str(manifest_path)
        }

        # Find potential consumers
        consumers = self.engine._find_potential_consumers("test-analyzer")

        # Verify consumer found
        self.assertIn("test-consumer", consumers)

    def test_workflow_recommendations(self):
        """Test workflow pattern recommendations"""
        # Test with commands matching a known workflow pattern
        requested_commands = ["test-analyzer", "test-strategist", "test-implementer"]

        recommendations = self.engine.get_workflow_recommendations(requested_commands)

        # Verify recommendation structure
        self.assertIn("suggested_sequence", recommendations)
        self.assertIn("parallel_opportunities", recommendations)
        self.assertIn("missing_dependencies", recommendations)
        self.assertIn("estimated_total_time", recommendations)

        # Should find matching workflow pattern
        expected_sequence = ["test-analyzer", "test-strategist", "test-implementer"]
        self.assertEqual(recommendations["suggested_sequence"], expected_sequence)
        self.assertEqual(recommendations["estimated_total_time"], "3m")

    def test_workflow_dependency_resolution(self):
        """Test dependency-based workflow sequence resolution"""
        # Test with commands not matching a workflow pattern
        requested_commands = ["test-implementer", "test-analyzer", "test-strategist"]

        recommendations = self.engine.get_workflow_recommendations(requested_commands)

        # Should resolve based on dependencies
        suggested_sequence = recommendations["suggested_sequence"]

        # Verify dependency order: analyzer before strategist before implementer
        analyzer_idx = suggested_sequence.index("test-analyzer")
        strategist_idx = suggested_sequence.index("test-strategist")
        implementer_idx = suggested_sequence.index("test-implementer")

        self.assertLess(analyzer_idx, strategist_idx)
        self.assertLess(strategist_idx, implementer_idx)

    def test_session_isolation(self):
        """Test that different sessions maintain isolation"""
        # Create another engine instance (different session)
        engine2 = CollaborationEngine(
            workspace_path=str(self.test_workspace / "team-workspace"),
            project_name="test-project"
        )

        # Verify different sessions
        self.assertNotEqual(self.engine.session_id, engine2.session_id)
        self.assertNotEqual(self.engine.session_path, engine2.session_path)

        # Store outputs in both sessions
        self.engine.store_command_output(
            "test-analyzer",
            "# Session 1 Output",
            "analysis_report",
            {"session": "1"}
        )

        engine2.store_command_output(
            "test-analyzer",
            "# Session 2 Output",
            "analysis_report",
            {"session": "2"}
        )

        # Verify session isolation in logs
        log1 = self.engine.session_path / "collaboration-engine.log"
        log2 = engine2.session_path / "collaboration-engine.log"

        self.assertTrue(log1.exists())
        self.assertTrue(log2.exists())
        self.assertNotEqual(log1, log2)

    def test_workspace_structure_integrity(self):
        """Test workspace directory structure integrity"""
        # Verify core directories exist
        workspace_path = self.engine.workspace_path
        self.assertTrue((workspace_path / "commands").exists())
        self.assertTrue((workspace_path / "shared").exists())
        self.assertTrue((workspace_path / "sessions").exists())

        # Verify session directory structure
        session_path = self.engine.session_path
        self.assertTrue(session_path.exists())
        self.assertTrue(session_path.is_dir())

        # Verify command directories
        for cmd in ["test-analyzer", "test-strategist", "test-implementer"]:
            cmd_dir = workspace_path / "commands" / cmd
            self.assertTrue(cmd_dir.exists())
            self.assertTrue((cmd_dir / "outputs").exists())
            self.assertTrue((cmd_dir / "cache").exists())

    def test_output_file_naming_convention(self):
        """Test consistent output file naming conventions"""
        # Store multiple outputs
        output1_file, meta1_file = self.engine.store_command_output(
            "test-analyzer",
            "# First Output",
            "analysis_report",
            {"test": "1"}
        )

        output2_file, meta2_file = self.engine.store_command_output(
            "test-analyzer",
            "# Second Output",
            "metrics_data",
            {"test": "2"}
        )

        # Verify naming convention
        output1_path = Path(output1_file)
        output2_path = Path(output2_file)
        meta1_path = Path(meta1_file)
        meta2_path = Path(meta2_file)

        # Output files should end with .md
        self.assertTrue(output1_path.name.endswith(".md"))
        self.assertTrue(output2_path.name.endswith(".md"))

        # Metadata files should start with dot and end with .command-meta.yaml
        self.assertTrue(meta1_path.name.startswith("."))
        self.assertTrue(meta1_path.name.endswith(".command-meta.yaml"))
        self.assertTrue(meta2_path.name.startswith("."))
        self.assertTrue(meta2_path.name.endswith(".command-meta.yaml"))

        # Should contain timestamp
        import re
        timestamp_pattern = r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"
        self.assertRegex(output1_path.name, timestamp_pattern)
        self.assertRegex(output2_path.name, timestamp_pattern)

    def test_cache_expiration_handling(self):
        """Test cache expiration in collaboration data"""
        metadata = {
            "quality_metrics": {"quality_score": 0.9}
        }

        enhanced = self.engine._enhance_metadata("test-analyzer", metadata, "test content")

        # Verify cache expiration set
        self.assertIn("collaboration_data", enhanced)
        self.assertIn("cache_expires", enhanced["collaboration_data"])

        # Parse expiration time
        cache_expires = datetime.fromisoformat(
            enhanced["collaboration_data"]["cache_expires"]
        )

        # Should be approximately 24 hours from now
        now = datetime.now()
        expected_expiry = now + timedelta(hours=24)

        # Allow 1 minute tolerance
        time_diff = abs((cache_expires - expected_expiry).total_seconds())
        self.assertLess(time_diff, 60)

    def test_command_output_versioning(self):
        """Test that multiple outputs from same command are properly versioned"""
        import time

        # Create multiple outputs with slight delays
        outputs = []
        for i in range(3):
            output_file, meta_file = self.engine.store_command_output(
                "test-analyzer",
                f"# Output {i+1}",
                "analysis_report",
                {"version": i+1}
            )
            outputs.append((output_file, meta_file))
            time.sleep(0.1)  # Ensure different timestamps

        # Verify all outputs exist and are unique
        output_files = [Path(output[0]) for output in outputs]
        meta_files = [Path(output[1]) for output in outputs]

        # All files should exist
        for f in output_files + meta_files:
            self.assertTrue(f.exists())

        # All filenames should be unique
        output_names = [f.name for f in output_files]
        meta_names = [f.name for f in meta_files]

        self.assertEqual(len(set(output_names)), len(output_names))
        self.assertEqual(len(set(meta_names)), len(meta_names))


if __name__ == "__main__":
    unittest.main()
