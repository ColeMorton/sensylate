#!/usr/bin/env python3
"""
End-to-end integration tests for Command Collaboration Framework
"""

import unittest
import tempfile
import time
from pathlib import Path
from datetime import datetime
import yaml
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import CollaborationEngine directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "team-workspace" / "shared"))
from collaboration_engine import CollaborationEngine
from tests.collaboration.test_helpers import CollaborationTestFramework, benchmark_collaboration_gains


class TestE2ECollaboration(unittest.TestCase):
    """End-to-end collaboration workflow tests"""

    def setUp(self):
        """Set up test environment"""
        self.test_framework = CollaborationTestFramework()
        self.test_workspace = self.test_framework.setup_test_workspace()
        self.engine = CollaborationEngine(
            workspace_path=str(self.test_workspace / "team-workspace"),
            project_name="test-project"
        )

        # Create comprehensive manifests for E2E testing
        self._create_e2e_manifests()

    def tearDown(self):
        """Clean up test environment"""
        self.test_framework.cleanup()

    def _create_e2e_manifests(self):
        """Create comprehensive manifests for end-to-end testing"""
        manifests = {
            "test-analyzer": {
                "command": {
                    "name": "test-analyzer",
                    "version": "1.0.0",
                    "type": "analyzer",
                    "classification": "collaboration_infrastructure"
                },
                "dependencies": {
                    "required": [],
                    "optional": [
                        {
                            "command": "code-owner",
                            "output_type": "health_assessment",
                            "enhancement": "Historical health trends for comparative analysis"
                        }
                    ]
                },
                "outputs": [
                    {"type": "analysis_report", "format": "markdown"},
                    {"type": "metrics_data", "format": "json"}
                ],
                "collaboration": {
                    "pre_execution_behavior": ["scan_workspace_for_relevant_data"],
                    "post_execution_behavior": ["store_analysis_results", "update_team_knowledge"],
                    "output_sharing": "immediate",
                    "cache_strategy": "session_based"
                }
            },
            "test-strategist": {
                "command": {
                    "name": "test-strategist",
                    "version": "1.0.0",
                    "type": "strategist",
                    "classification": "collaboration_infrastructure"
                },
                "dependencies": {
                    "required": ["test-analyzer"],
                    "optional": [
                        {
                            "command": "product-owner",
                            "output_type": "prioritization",
                            "enhancement": "Business priorities for strategic alignment"
                        }
                    ]
                },
                "outputs": [
                    {"type": "strategy_plan", "format": "markdown"},
                    {"type": "action_items", "format": "yaml"}
                ],
                "collaboration": {
                    "pre_execution_behavior": ["load_analyzer_outputs", "check_optimization_data"],
                    "post_execution_behavior": ["store_strategy_outputs", "trigger_implementation_planning"],
                    "output_sharing": "on_completion",
                    "cache_strategy": "dependency_based"
                }
            },
            "test-implementer": {
                "command": {
                    "name": "test-implementer",
                    "version": "1.0.0",
                    "type": "implementer",
                    "classification": "collaboration_infrastructure"
                },
                "dependencies": {
                    "required": ["test-strategist"],
                    "optional": [
                        {
                            "command": "test-analyzer",
                            "output_type": "analysis_report",
                            "enhancement": "Technical context for implementation decisions"
                        },
                        {
                            "command": "architect",
                            "output_type": "implementation_plan",
                            "enhancement": "Architectural patterns and best practices"
                        }
                    ]
                },
                "outputs": [
                    {"type": "implementation_plan", "format": "markdown"},
                    {"type": "task_breakdown", "format": "yaml"}
                ],
                "collaboration": {
                    "pre_execution_behavior": ["load_strategy_outputs", "gather_technical_context"],
                    "post_execution_behavior": ["store_implementation_plan", "validate_completeness"],
                    "output_sharing": "immediate",
                    "cache_strategy": "quality_based"
                }
            }
        }

        # Write manifest files and update registry
        manifests_dir = self.test_workspace / "manifests"
        manifests_dir.mkdir(exist_ok=True)

        for cmd_name, manifest_data in manifests.items():
            manifest_path = manifests_dir / f"{cmd_name}-manifest.yaml"
            with open(manifest_path, "w") as f:
                yaml.dump(manifest_data, f)

            # Update registry
            if cmd_name in self.engine.registry["commands"]:
                self.engine.registry["commands"][cmd_name]["manifest"] = str(manifest_path)

    def test_full_collaboration_workflow(self):
        """Test complete team collaboration cycle: analyzer → strategist → implementer"""

        # === PHASE 1: Analyzer Execution ===
        print("\n=== Phase 1: Test Analyzer Execution ===")

        # Resolve analyzer dependencies (should have no required deps)
        analyzer_context, analyzer_missing = self.engine.resolve_dependencies("test-analyzer")

        self.assertEqual(len(analyzer_missing), 0, "Analyzer should have no missing required dependencies")

        # Simulate analyzer execution
        analyzer_output = """# Test Codebase Analysis Report

## Executive Summary
Comprehensive analysis of test codebase reveals moderate technical debt with opportunities for optimization.

## Key Findings
- Code quality score: 78/100
- Test coverage: 85%
- Technical debt: Medium priority
- Performance bottlenecks: 3 identified

## Recommendations
1. Refactor authentication module
2. Improve caching strategy
3. Enhance error handling patterns

## Metrics Data
- Lines of code: 15,420
- Cyclomatic complexity: 12.4 average
- Duplication ratio: 8.2%
"""

        # Store analyzer output
        analyzer_output_file, analyzer_meta_file = self.engine.store_command_output(
            "test-analyzer",
            analyzer_output,
            "analysis_report",
            {
                "execution_time": "45s",
                "quality_score": 0.89,
                "confidence_level": "high"
            }
        )

        print(f"Analyzer output stored: {analyzer_output_file}")

        # === PHASE 2: Strategist Execution ===
        print("\n=== Phase 2: Test Strategist Execution ===")

        # Resolve strategist dependencies (should find analyzer output)
        strategist_context, strategist_missing = self.engine.resolve_dependencies("test-strategist")

        self.assertEqual(len(strategist_missing), 0, "Strategist should find analyzer output")
        self.assertIn("test-analyzer", strategist_context["available_data"],
                     "Strategist should have access to analyzer data")

        # Verify analyzer data content
        analyzer_data = strategist_context["available_data"]["test-analyzer"]
        self.assertIn("Code quality score: 78/100", analyzer_data["content"])

        # Simulate strategist execution with enhanced context
        strategist_output = """# Strategic Implementation Plan

## Analysis Integration
Based on the analyzer findings (quality score: 78/100), the following strategic priorities are recommended:

## Strategic Priorities
1. **High Priority**: Authentication module refactoring
   - Impact: Security and maintainability
   - Effort: 2-3 weeks
   - Dependencies: None

2. **Medium Priority**: Caching strategy optimization
   - Impact: Performance improvement
   - Effort: 1 week
   - Dependencies: None

3. **Low Priority**: Error handling enhancement
   - Impact: System reliability
   - Effort: 1 week
   - Dependencies: Authentication refactor

## Resource Allocation
- Senior developers: 2 FTE
- Timeline: 6 weeks total
- Risk level: Medium

## Success Metrics
- Code quality improvement to 85+
- Performance gain of 20%
- Reduced error rates by 40%
"""

        # Store strategist output
        strategist_output_file, strategist_meta_file = self.engine.store_command_output(
            "test-strategist",
            strategist_output,
            "strategy_plan",
            {
                "execution_time": "35s",  # Faster due to collaboration
                "quality_score": 0.92,
                "confidence_level": "high",
                "collaboration_benefits": ["analyzer_context", "performance_optimization"]
            }
        )

        print(f"Strategist output stored: {strategist_output_file}")

        # === PHASE 3: Implementer Execution ===
        print("\n=== Phase 3: Test Implementer Execution ===")

        # Resolve implementer dependencies (should find strategist + analyzer optimization)
        implementer_context, implementer_missing = self.engine.resolve_dependencies("test-implementer")

        self.assertEqual(len(implementer_missing), 0, "Implementer should find strategist output")
        self.assertIn("test-strategist", implementer_context["available_data"],
                     "Implementer should have access to strategist data")
        self.assertIn("test-analyzer", implementer_context["optimization_data"],
                     "Implementer should have analyzer optimization data")

        # Verify cumulative context
        strategist_data = implementer_context["available_data"]["test-strategist"]
        self.assertIn("Authentication module refactoring", strategist_data["content"])

        analyzer_opt_data = implementer_context["optimization_data"]["test-analyzer"]
        self.assertIn("Technical context for implementation decisions",
                     analyzer_opt_data["enhancement"])

        # Simulate implementer execution with full team context
        implementer_output = """# Implementation Plan: Test Codebase Optimization

## Context Integration
This plan incorporates insights from:
- **Analyzer**: Technical debt assessment and performance bottlenecks
- **Strategist**: Priority ranking and resource allocation

## Phase 1: Authentication Module Refactoring (2-3 weeks)

### Technical Approach
Based on analyzer findings (quality score: 78/100, complexity: 12.4), implementing:

1. **JWT Token Management Refactor**
   - Files: `auth/token.py`, `auth/middleware.py`
   - Pattern: Strategy pattern for token validation
   - Tests: Unit + integration coverage

2. **Session Management Optimization**
   - Redis-based session store
   - Cache expiration strategy
   - Performance target: 20% improvement

### Implementation Tasks
```yaml
tasks:
  - name: "Refactor token validation"
    estimate: "3 days"
    assignee: "senior_dev_1"
    dependencies: []

  - name: "Implement session caching"
    estimate: "2 days"
    assignee: "senior_dev_2"
    dependencies: ["token_validation"]

  - name: "Integration testing"
    estimate: "1 day"
    assignee: "qa_engineer"
    dependencies: ["session_caching"]
```

## Phase 2: Performance Optimization (1 week)
[Additional implementation details...]

## Quality Assurance
- Code review checkpoints
- Automated testing pipeline
- Performance monitoring
"""

        # Store implementer output
        implementer_output_file, implementer_meta_file = self.engine.store_command_output(
            "test-implementer",
            implementer_output,
            "implementation_plan",
            {
                "execution_time": "28s",  # Fastest due to full collaboration
                "quality_score": 0.95,
                "confidence_level": "high",
                "collaboration_benefits": ["analyzer_context", "strategist_context", "performance_optimization"]
            }
        )

        print(f"Implementer output stored: {implementer_output_file}")

        # === VERIFICATION: End-to-End Validation ===
        print("\n=== End-to-End Validation ===")

        # Verify complete data lineage
        self._verify_data_lineage()

        # Verify team knowledge accumulation
        self._verify_team_knowledge_accumulation()

        # Verify performance improvements
        self._verify_collaboration_performance()

        print("✅ Full collaboration workflow completed successfully")




    def test_new_command_integration(self):
        """Test dynamic command ecosystem evolution"""

        print("\n=== Testing New Command Integration ===")

        # Create existing command ecosystem
        self.test_framework.create_test_output("test-analyzer", "analysis_report",
                                             "# Existing Analysis", 0.9)

        # Add new command to registry
        new_command_manifest = {
            "command": {
                "name": "test-optimizer",
                "version": "1.0.0",
                "type": "optimizer"
            },
            "dependencies": {
                "required": ["test-analyzer"],
                "optional": []
            },
            "outputs": [
                {"type": "optimization_report", "format": "markdown"}
            ],
            "collaboration": {
                "pre_execution_behavior": ["load_analysis_data"],
                "post_execution_behavior": ["store_optimization_results"],
                "output_sharing": "immediate",
                "cache_strategy": "session_based"
            }
        }

        # Write new manifest
        manifest_path = self.test_workspace / "test-optimizer-manifest.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(new_command_manifest, f)

        # Add to registry
        self.engine.registry["commands"]["test-optimizer"] = {
            "name": "Test Optimizer",
            "description": "Optimizes test implementations",
            "type": "optimizer",
            "scope": "test",
            "location": "/test/optimizer.md",
            "manifest": str(manifest_path)
        }

        # Test integration
        context, missing_deps = self.engine.resolve_dependencies("test-optimizer")

        # Should find analyzer dependency
        self.assertEqual(len(missing_deps), 0, "New command should integrate with existing ecosystem")
        self.assertIn("test-analyzer", context["available_data"])

        # Store optimizer output
        optimizer_output = "# Optimization Report\n\nBased on analysis findings, optimizations applied."
        self.engine.store_command_output("test-optimizer", optimizer_output,
                                        "optimization_report", {"integration": "success"})

        # Update strategist to use optimizer data
        strategist_context, _ = self.engine.resolve_dependencies("test-strategist")

        print("✅ New command successfully integrated into ecosystem")

    def test_product_vs_infrastructure_command_behavior(self):
        """Test different behaviors between product and infrastructure commands"""

        print("\n=== Testing Product vs Infrastructure Command Behavior ===")

        # Create product command manifest
        product_manifest = {
            "command": {
                "name": "test-product-service",
                "version": "1.0.0",
                "type": "product",
                "classification": "core_product"
            },
            "dependencies": {
                "required": [],
                "optional": [
                    {
                        "command": "test-analyzer",
                        "output_type": "analysis_report",
                        "enhancement": "Analysis context for product features"
                    }
                ]
            },
            "outputs": [
                {"type": "user_output", "format": "markdown"},
                {"type": "product_metrics", "format": "json"}
            ],
            "collaboration": {
                "pre_execution_behavior": ["load_user_context", "optimize_user_experience"],
                "post_execution_behavior": ["track_usage_metrics", "improve_product_features"],
                "output_sharing": "user_focused",
                "cache_strategy": "user_based"
            }
        }

        # Write product manifest
        product_manifest_path = self.test_workspace / "test-product-service-manifest.yaml"
        with open(product_manifest_path, "w") as f:
            yaml.dump(product_manifest, f)

        # Add product command to registry
        self.engine.registry["commands"]["test-product-service"] = {
            "name": "Test Product Service",
            "description": "Test user-facing product functionality",
            "type": "product",
            "classification": "core_product",
            "scope": "test",
            "location": "/test/product-service.md",
            "manifest": str(product_manifest_path)
        }

        # Create infrastructure analysis output for product to use
        self.test_framework.create_test_output("test-analyzer", "analysis_report",
                                             "# Infrastructure Analysis\n\nTechnical context for product", 0.88)

        # Test infrastructure command behavior
        print("Testing infrastructure command...")
        infra_context, infra_missing = self.engine.resolve_dependencies("test-analyzer")

        # Infrastructure commands should focus on collaboration
        self.assertEqual(len(infra_missing), 0)
        # Infrastructure commands may have limited data as they create foundation

        # Test product command behavior
        print("Testing product command...")
        product_context, product_missing = self.engine.resolve_dependencies("test-product-service")

        # Product commands should leverage infrastructure outputs
        self.assertEqual(len(product_missing), 0)
        # Check optimization data since test-analyzer is an optional dependency
        self.assertIn("test-analyzer", product_context.get("optimization_data", {}))

        # Verify different collaboration behaviors
        infra_cmd_info = self.engine.discover_command("test-analyzer")
        product_cmd_info = self.engine.discover_command("test-product-service")

        # Infrastructure commands focus on team collaboration
        self.assertEqual(infra_cmd_info["classification"], "collaboration_infrastructure")
        self.assertEqual(infra_cmd_info["type"], "infrastructure")

        # Product commands focus on user value
        self.assertEqual(product_cmd_info["classification"], "core_product")
        self.assertEqual(product_cmd_info["type"], "product")

        print("✅ Product and infrastructure commands show distinct behaviors")

    def _verify_data_lineage(self):
        """Verify complete data lineage tracking"""
        # Check that implementer metadata tracks its data sources
        implementer_outputs = list((self.engine.commands_path / "test-implementer" / "outputs").glob("*.md"))
        self.assertGreater(len(implementer_outputs), 0, "Implementer should have outputs")

        # Find corresponding metadata
        latest_output = max(implementer_outputs, key=lambda f: f.stat().st_mtime)
        meta_file = latest_output.parent / f".{latest_output.stem}.command-meta.yaml"

        with open(meta_file, "r") as f:
            metadata = yaml.safe_load(f)

        # Should have collaboration data tracking sources
        self.assertIn("collaboration_data", metadata)

    def _verify_team_knowledge_accumulation(self):
        """Verify team knowledge base has been updated"""
        knowledge_file = self.engine.shared_path / "team-knowledge.yaml"
        self.assertTrue(knowledge_file.exists(), "Team knowledge file should exist")

        with open(knowledge_file, "r") as f:
            knowledge = yaml.safe_load(f)

        # Should track all command outputs
        self.assertIn("command_outputs", knowledge)
        self.assertIn("test-analyzer", knowledge["command_outputs"])
        self.assertIn("test-strategist", knowledge["command_outputs"])
        self.assertIn("test-implementer", knowledge["command_outputs"])

        # Should have accumulated insights
        self.assertIn("insights", knowledge)
        self.assertGreater(len(knowledge["insights"]), 0)

    def _verify_collaboration_performance(self):
        """Verify performance improvements through collaboration"""
        # Use the benchmark function
        improvements = benchmark_collaboration_gains(self.test_framework)

        # Validate performance targets
        self.assertGreater(improvements["speed_gain"], 0.10,
                          "Should achieve >10% speed improvement")
        self.assertGreater(improvements["cache_hit_rate"], 0.50,
                          "Should achieve >50% cache hit rate")
        self.assertGreater(improvements["data_reuse_count"], 0,
                          "Should demonstrate data reuse")


if __name__ == "__main__":
    unittest.main(verbosity=2)
