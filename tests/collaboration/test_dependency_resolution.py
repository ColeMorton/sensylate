#!/usr/bin/env python3
"""
Unit tests for dependency resolution and optimization functionality
"""

import unittest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import yaml
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from team_workspace.shared.collaboration_engine import CollaborationEngine
from tests.collaboration.test_helpers import CollaborationTestFramework


class TestDependencyResolution(unittest.TestCase):
    """Test dependency resolution and optimization functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_framework = CollaborationTestFramework()
        self.test_workspace = self.test_framework.setup_test_workspace()
        self.engine = CollaborationEngine(
            workspace_path=str(self.test_workspace / "team-workspace"),
            project_name="test-project"
        )

        # Create test manifests with dependencies
        self._create_test_manifests()

    def tearDown(self):
        """Clean up test environment"""
        self.test_framework.cleanup()

    def _create_test_manifests(self):
        """Create test manifest files with dependency configurations"""
        # Test analyzer manifest (no dependencies)
        analyzer_manifest = {
            "command": {
                "name": "test-analyzer",
                "version": "1.0.0",
                "type": "analyzer"
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
                "pre_execution_behavior": ["scan_workspace_for_relevant_data"],
                "post_execution_behavior": ["store_analysis_results"],
                "cache_strategy": "session_based"
            }
        }

        # Test strategist manifest (depends on analyzer)
        strategist_manifest = {
            "command": {
                "name": "test-strategist",
                "version": "1.0.0",
                "type": "strategist"
            },
            "dependencies": {
                "required": ["test-analyzer"],
                "optional": [
                    {
                        "command": "product-owner",
                        "output_type": "prioritization",
                        "enhancement": "Product roadmap alignment"
                    }
                ]
            },
            "collaboration": {
                "pre_execution_behavior": ["load_analyzer_outputs"],
                "post_execution_behavior": ["store_strategy_outputs"],
                "cache_strategy": "dependency_based"
            }
        }

        # Test implementer manifest (depends on strategist)
        implementer_manifest = {
            "command": {
                "name": "test-implementer",
                "version": "1.0.0",
                "type": "implementer"
            },
            "dependencies": {
                "required": ["test-strategist"],
                "optional": [
                    {
                        "command": "test-analyzer",
                        "output_type": "analysis_report",
                        "enhancement": "Technical context for implementation"
                    }
                ]
            },
            "collaboration": {
                "pre_execution_behavior": ["load_strategy_outputs"],
                "post_execution_behavior": ["store_implementation_plan"],
                "cache_strategy": "quality_based"
            }
        }

        # Write manifest files
        manifests_dir = self.test_workspace / "manifests"
        manifests_dir.mkdir(exist_ok=True)

        manifest_files = {
            "test-analyzer": analyzer_manifest,
            "test-strategist": strategist_manifest,
            "test-implementer": implementer_manifest
        }

        for cmd_name, manifest_data in manifest_files.items():
            manifest_path = manifests_dir / f"{cmd_name}-manifest.yaml"
            with open(manifest_path, "w") as f:
                yaml.dump(manifest_data, f)

            # Update registry with manifest location
            self.engine.registry["commands"][cmd_name]["manifest"] = str(manifest_path)

    def test_resolve_dependencies_no_deps(self):
        """Test dependency resolution for command with no dependencies"""
        context, missing_deps = self.engine.resolve_dependencies("test-analyzer")

        # Verify context structure
        self.assertIn("command", context)
        self.assertIn("session_id", context)
        self.assertIn("project_context", context)
        self.assertIn("available_data", context)
        self.assertIn("missing_dependencies", context)
        self.assertIn("optimization_data", context)
        self.assertIn("execution_plan", context)

        # Verify command info
        self.assertEqual(context["command"], "test-analyzer")
        self.assertEqual(context["session_id"], self.engine.session_id)

        # Should have no required dependencies missing
        self.assertEqual(len(missing_deps), 0)
        self.assertEqual(len(context["missing_dependencies"]), 0)

    def test_resolve_dependencies_with_required(self):
        """Test dependency resolution with required dependencies"""
        # Test strategist which requires analyzer
        context, missing_deps = self.engine.resolve_dependencies("test-strategist")

        # Should have missing required dependency (analyzer output doesn't exist yet)
        self.assertGreater(len(missing_deps), 0)
        self.assertIn("test-analyzer", missing_deps)
        self.assertEqual(context["missing_dependencies"], missing_deps)

    def test_resolve_dependencies_with_available_data(self):
        """Test dependency resolution when dependency data is available"""
        # Create analyzer output first
        self.test_framework.create_test_output(
            "test-analyzer",
            "analysis_report",
            "# Test Analysis Report\n\nThis is test analysis data.",
            0.9
        )

        # Now resolve strategist dependencies
        context, missing_deps = self.engine.resolve_dependencies("test-strategist")

        # Should find available data
        self.assertIn("test-analyzer", context["available_data"])
        self.assertEqual(len(missing_deps), 0)

        # Verify data structure
        analyzer_data = context["available_data"]["test-analyzer"]
        self.assertIn("content", analyzer_data)
        self.assertIn("metadata", analyzer_data)
        self.assertIn("file_path", analyzer_data)

    def test_resolve_dependencies_optimization_data(self):
        """Test dependency resolution with optimization data from optional dependencies"""
        # Create optional dependency output
        self.test_framework.create_test_output(
            "code-owner",
            "health_assessment",
            "# Health Assessment\n\nCodebase health: Good",
            0.85
        )

        # Resolve analyzer dependencies (has optional dependency on code-owner)
        context, missing_deps = self.engine.resolve_dependencies("test-analyzer")

        # Should find optimization data
        self.assertIn("code-owner", context["optimization_data"])

        # Verify optimization data structure
        code_owner_data = context["optimization_data"]["code-owner"]
        self.assertIn("data", code_owner_data)
        self.assertIn("enhancement", code_owner_data)
        self.assertEqual(
            code_owner_data["enhancement"],
            "Previous health metrics for trend analysis"
        )

    def test_dependency_data_discovery(self):
        """Test finding dependency data from command outputs"""
        # Create test output
        output_file, meta_file = self.test_framework.create_test_output(
            "test-analyzer",
            "analysis_report",
            "# Test Analysis\n\nDetailed analysis content.",
            0.88
        )

        # Test data discovery
        data = self.engine._find_dependency_data("test-analyzer", "analysis_report")

        self.assertIsNotNone(data)
        self.assertIn("content", data)
        self.assertIn("metadata", data)
        self.assertIn("file_path", data)

        # Verify content
        self.assertIn("Detailed analysis content", data["content"])

    def test_dependency_data_discovery_type_filtering(self):
        """Test dependency data discovery with output type filtering"""
        # Create outputs of different types
        self.test_framework.create_test_output(
            "test-analyzer",
            "analysis_report",
            "# Analysis Report",
            0.9
        )

        self.test_framework.create_test_output(
            "test-analyzer",
            "metrics_data",
            "# Metrics Data",
            0.85
        )

        # Find specific type
        report_data = self.engine._find_dependency_data("test-analyzer", "analysis_report")
        metrics_data = self.engine._find_dependency_data("test-analyzer", "metrics_data")

        # Both should be found
        self.assertIsNotNone(report_data)
        self.assertIsNotNone(metrics_data)

        # Verify correct content
        self.assertIn("Analysis Report", report_data["content"])
        self.assertIn("Metrics Data", metrics_data["content"])

    def test_dependency_data_discovery_most_recent(self):
        """Test that most recent output is returned when multiple exist"""
        import time

        # Create first output
        self.test_framework.create_test_output(
            "test-analyzer",
            "analysis_report",
            "# First Analysis",
            0.8
        )

        # Wait a moment to ensure different timestamps
        time.sleep(0.1)

        # Create second output
        self.test_framework.create_test_output(
            "test-analyzer",
            "analysis_report",
            "# Second Analysis",
            0.9
        )

        # Find data - should return most recent
        data = self.engine._find_dependency_data("test-analyzer", "analysis_report")

        self.assertIsNotNone(data)
        self.assertIn("Second Analysis", data["content"])

    def test_dependency_data_discovery_no_match(self):
        """Test dependency data discovery when no matching data exists"""
        # Try to find data that doesn't exist
        data = self.engine._find_dependency_data("non-existent-command", "any_type")

        self.assertIsNone(data)

    def test_execution_plan_creation(self):
        """Test execution plan creation based on dependencies and context"""
        # Create context with optimization data
        self.test_framework.create_test_output(
            "code-owner",
            "health_assessment",
            "# Health Data",
            0.9
        )

        context, _ = self.engine.resolve_dependencies("test-analyzer")

        # Verify execution plan
        plan = context["execution_plan"]

        self.assertIn("pre_execution_steps", plan)
        self.assertIn("post_execution_steps", plan)
        self.assertIn("cache_strategy", plan)
        self.assertIn("estimated_duration", plan)
        self.assertIn("optimization_available", plan)
        self.assertIn("data_sources", plan)

        # Verify optimization detected
        self.assertTrue(plan["optimization_available"])
        self.assertIn("code-owner", plan["data_sources"])

    def test_execution_duration_estimation(self):
        """Test execution duration estimation with and without optimization"""
        # Without optimization data
        context1, _ = self.engine.resolve_dependencies("test-analyzer")
        base_duration = context1["execution_plan"]["estimated_duration"]

        # With optimization data
        self.test_framework.create_test_output(
            "code-owner",
            "health_assessment",
            "# Health Data",
            0.9
        )

        context2, _ = self.engine.resolve_dependencies("test-analyzer")
        optimized_duration = context2["execution_plan"]["estimated_duration"]

        # Optimized should be faster (20% reduction)
        self.assertLess(optimized_duration, base_duration)

        # Verify 20% improvement (base is 45s, optimized should be ~36s)
        expected_optimized = int(45 * 0.8)  # 36 seconds
        self.assertEqual(optimized_duration, expected_optimized)

    def test_complex_dependency_chain(self):
        """Test resolution of complex dependency chains"""
        # Create full dependency chain: analyzer -> strategist -> implementer

        # 1. Create analyzer output
        self.test_framework.create_test_output(
            "test-analyzer",
            "analysis_report",
            "# Analysis Report\n\nDetailed analysis",
            0.9
        )

        # 2. Resolve strategist (should find analyzer)
        strategist_context, strategist_missing = self.engine.resolve_dependencies("test-strategist")

        self.assertEqual(len(strategist_missing), 0)
        self.assertIn("test-analyzer", strategist_context["available_data"])

        # 3. Create strategist output
        self.test_framework.create_test_output(
            "test-strategist",
            "strategy_plan",
            "# Strategy Plan\n\nBased on analysis",
            0.85
        )

        # 4. Resolve implementer (should find strategist, optionally analyzer)
        impl_context, impl_missing = self.engine.resolve_dependencies("test-implementer")

        self.assertEqual(len(impl_missing), 0)
        self.assertIn("test-strategist", impl_context["available_data"])
        self.assertIn("test-analyzer", impl_context["optimization_data"])

    def test_missing_dependency_handling(self):
        """Test graceful handling of missing dependencies"""
        # Try to resolve implementer without strategist
        context, missing_deps = self.engine.resolve_dependencies("test-implementer")

        # Should gracefully handle missing required dependency
        self.assertIn("test-strategist", missing_deps)
        self.assertEqual(context["missing_dependencies"], missing_deps)

        # Should still create valid execution context
        self.assertIn("execution_plan", context)
        self.assertIn("available_data", context)

    def test_dependency_resolution_error_handling(self):
        """Test error handling in dependency resolution"""
        # Test with invalid command
        with self.assertRaises(ValueError):
            self.engine.resolve_dependencies("non-existent-command")

    def test_dependency_metadata_validation(self):
        """Test validation of dependency output metadata"""
        # Create output with invalid metadata
        output_dir = (self.test_workspace / "team-workspace" / "commands" /
                     "test-analyzer" / "outputs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create output file
        output_file = output_dir / "invalid-output.md"
        with open(output_file, "w") as f:
            f.write("# Invalid Output")

        # Create metadata with missing required fields
        meta_file = output_dir / ".invalid-output.command-meta.yaml"
        invalid_metadata = {
            "metadata": {
                "command": "test-analyzer"
                # Missing timestamp, version, session_id
            }
        }

        with open(meta_file, "w") as f:
            yaml.dump(invalid_metadata, f)

        # Try to find dependency data - should handle gracefully
        try:
            data = self.engine._find_dependency_data("test-analyzer")
            # Should either return None or valid data, not crash
            if data is not None:
                self.assertIn("content", data)
        except Exception as e:
            self.fail(f"Dependency resolution should handle invalid metadata gracefully: {e}")

    def test_optimization_data_enhancement(self):
        """Test that optimization data includes enhancement descriptions"""
        # Create optional dependency output
        self.test_framework.create_test_output(
            "product-owner",
            "prioritization",
            "# Product Prioritization\n\nFeature priorities",
            0.9
        )

        # Resolve strategist dependencies
        context, _ = self.engine.resolve_dependencies("test-strategist")

        # Verify optimization data includes enhancement
        if "product-owner" in context["optimization_data"]:
            po_data = context["optimization_data"]["product-owner"]
            self.assertIn("enhancement", po_data)
            self.assertEqual(po_data["enhancement"], "Product roadmap alignment")

    def test_cache_strategy_inheritance(self):
        """Test that cache strategy is properly inherited from manifests"""
        context, _ = self.engine.resolve_dependencies("test-analyzer")

        plan = context["execution_plan"]
        self.assertEqual(plan["cache_strategy"], "session_based")

        # Test different cache strategy
        context2, _ = self.engine.resolve_dependencies("test-strategist")
        plan2 = context2["execution_plan"]
        self.assertEqual(plan2["cache_strategy"], "dependency_based")


if __name__ == "__main__":
    unittest.main()
