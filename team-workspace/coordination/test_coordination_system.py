#!/usr/bin/env python3
"""
Comprehensive Test Suite for Team-Workspace Content Lifecycle Management System

Tests all coordination components including pre-execution consultation,
superseding workflow, topic ownership, decision tree, and knowledge dashboard.
"""

import unittest
import tempfile
import shutil
import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta

# Import coordination system components
from pre_execution_consultation import PreExecutionConsultant
from superseding_workflow import SupersedingWorkflow
from topic_ownership_manager import TopicOwnershipManager
from decision_tree import DecisionTree
from knowledge_dashboard import KnowledgeDashboard
from conflict_detection import ConflictDetector

class TestCoordinationSystem(unittest.TestCase):
    """Test suite for the complete coordination system."""

    def setUp(self):
        """Set up test environment with temporary workspace."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.workspace_path = self.test_dir / "team-workspace"

        # Create workspace structure
        self._create_test_workspace()

        # Initialize components
        self.consultant = PreExecutionConsultant(str(self.workspace_path))
        self.workflow = SupersedingWorkflow(str(self.workspace_path))
        self.ownership_manager = TopicOwnershipManager(str(self.workspace_path))
        self.decision_tree = DecisionTree(str(self.workspace_path))
        self.dashboard = KnowledgeDashboard(str(self.workspace_path))
        self.conflict_detector = ConflictDetector(str(self.workspace_path))

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def _create_test_workspace(self):
        """Create test workspace with sample data."""
        # Create directory structure
        directories = [
            "coordination",
            "knowledge/technical-health",
            "knowledge/implementation-plans",
            "knowledge/product-strategy",
            "knowledge/requirements",
            "archive",
            "commands/architect/outputs",
            "commands/code-owner/outputs",
            "commands/product-owner/outputs",
            "commands/business-analyst/outputs"
        ]

        for dir_path in directories:
            (self.workspace_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Create sample registry
        sample_registry = {
            "version": "1.0",
            "updated": "2025-06-20T00:00:00Z",
            "topics": {
                "technical-health": {
                    "description": "Technical health assessments",
                    "current_authority": "team-workspace/knowledge/technical-health/current-assessment.md",
                    "owner_command": "code-owner",
                    "last_updated": "2025-06-19",
                    "freshness_threshold_days": 30,
                    "status": "active",
                    "related_files": ["team-workspace/knowledge/technical-health/current-assessment.md"],
                    "conflicts_detected": False
                },
                "test-topic": {
                    "description": "Test topic for validation",
                    "current_authority": "team-workspace/knowledge/requirements/test-topic.md",
                    "owner_command": "business-analyst",
                    "last_updated": "2025-06-20",
                    "freshness_threshold_days": 14,
                    "status": "active",
                    "related_files": ["team-workspace/knowledge/requirements/test-topic.md"],
                    "conflicts_detected": False
                }
            },
            "command_ownership": {
                "architect": {
                    "primary_topics": ["implementation-plans"],
                    "secondary_topics": []
                },
                "code-owner": {
                    "primary_topics": ["technical-health"],
                    "secondary_topics": []
                },
                "business-analyst": {
                    "primary_topics": ["test-topic"],
                    "secondary_topics": ["technical-health"]
                },
                "product-owner": {
                    "primary_topics": ["product-strategy"],
                    "secondary_topics": ["technical-health"]
                }
            }
        }

        registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"
        registry_path.write_text(yaml.dump(sample_registry, default_flow_style=False))

        # Create sample superseding log
        superseding_log = {
            "version": "1.0",
            "created": "2025-06-20T00:00:00Z",
            "superseding_events": []
        }

        log_path = self.workspace_path / "coordination" / "superseding-log.yaml"
        log_path.write_text(yaml.dump(superseding_log, default_flow_style=False))

        # Create sample authority files
        authority_files = [
            "knowledge/technical-health/current-assessment.md",
            "knowledge/requirements/test-topic.md"
        ]

        for file_path in authority_files:
            full_path = self.workspace_path / file_path
            full_path.write_text(f"# Test Authority File\n\nContent for {file_path}")

class TestPreExecutionConsultation(TestCoordinationSystem):
    """Test pre-execution consultation system."""

    def test_consult_existing_topic_non_owner(self):
        """Test consultation for existing topic when not owner."""
        result = self.consultant.consult_before_execution(
            "architect", "technical-health", "security analysis"
        )

        self.assertEqual(result["recommendation"], "avoid_duplication")
        self.assertIn("not the primary owner", result["rationale"])
        self.assertIsNotNone(result["existing_knowledge"])

    def test_consult_existing_topic_owner(self):
        """Test consultation for existing topic when owner."""
        result = self.consultant.consult_before_execution(
            "code-owner", "technical-health", "security analysis"
        )

        self.assertEqual(result["recommendation"], "consider_necessity")
        self.assertIn("Fresh analysis already exists", result["rationale"])

    def test_consult_new_topic(self):
        """Test consultation for new topic."""
        result = self.consultant.consult_before_execution(
            "architect", "new-implementation", "new system design"
        )

        self.assertEqual(result["recommendation"], "proceed")
        self.assertIn("No existing knowledge", result["rationale"])

    def test_declare_superseding_intent(self):
        """Test superseding intent declaration."""
        result = self.consultant.declare_superseding_intent(
            "code-owner", "technical-health",
            ["old-file.md"], "Updated analysis"
        )

        self.assertTrue(result["superseding_approved"])
        self.assertIsNotNone(result["superseding_id"])

class TestSupersedingWorkflow(TestCoordinationSystem):
    """Test superseding workflow system."""

    def test_declare_superseding_valid(self):
        """Test valid superseding declaration."""
        # Create test files
        old_file = self.workspace_path / "commands" / "code-owner" / "outputs" / "old-analysis.md"
        old_file.write_text("Old analysis content")

        new_file = self.workspace_path / "knowledge" / "technical-health" / "new-analysis.md"
        new_file.write_text("New analysis content")

        result = self.workflow.declare_superseding(
            "code-owner", "technical-health", str(new_file),
            [str(old_file)], "Updated with new findings"
        )

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["event_id"])
        self.assertEqual(len(result["archived_files"]), 1)

    def test_declare_superseding_missing_file(self):
        """Test superseding with missing file."""
        result = self.workflow.declare_superseding(
            "code-owner", "technical-health",
            "nonexistent-new.md", ["nonexistent-old.md"], "Test"
        )

        self.assertFalse(result["success"])
        self.assertIn("does not exist", result["error"])

    def test_declare_superseding_no_permission(self):
        """Test superseding without permission."""
        # Create test files
        old_file = self.workspace_path / "commands" / "architect" / "outputs" / "old-analysis.md"
        old_file.write_text("Old analysis content")

        new_file = self.workspace_path / "knowledge" / "technical-health" / "new-analysis.md"
        new_file.write_text("New analysis content")

        result = self.workflow.declare_superseding(
            "architect", "technical-health", str(new_file),
            [str(old_file)], "Unauthorized update"
        )

        self.assertFalse(result["success"])
        self.assertIn("lacks permission", result["error"])

class TestTopicOwnershipManager(TestCoordinationSystem):
    """Test topic ownership management."""

    def test_assign_topic_ownership_valid(self):
        """Test valid topic ownership assignment."""
        result = self.ownership_manager.assign_topic_ownership(
            "new-topic", "architect", ["business-analyst"]
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["primary_owner"], "architect")
        self.assertEqual(result["secondary_owners"], ["business-analyst"])

    def test_assign_topic_ownership_invalid_command(self):
        """Test ownership assignment with invalid command."""
        result = self.ownership_manager.assign_topic_ownership(
            "new-topic", "invalid-command", []
        )

        self.assertFalse(result["success"])
        self.assertIn("Invalid primary owner", result["error"])

    def test_get_topic_ownership(self):
        """Test getting topic ownership information."""
        result = self.ownership_manager.get_topic_ownership("technical-health")

        self.assertTrue(result["has_primary_owner"])
        self.assertEqual(result["primary_owner"], "code-owner")
        self.assertIn("business-analyst", result["secondary_owners"])

    def test_claim_unowned_topic(self):
        """Test claiming unowned topic."""
        result = self.ownership_manager.claim_unowned_topic(
            "unowned-topic", "architect", "New area of responsibility"
        )

        self.assertTrue(result["success"])
        self.assertTrue(result["claimed"])

    def test_claim_owned_topic(self):
        """Test claiming already owned topic."""
        result = self.ownership_manager.claim_unowned_topic(
            "technical-health", "architect", "Trying to claim owned topic"
        )

        self.assertFalse(result["success"])
        self.assertIn("already owned", result["error"])

    def test_suggest_collaboration(self):
        """Test collaboration suggestions."""
        # Test primary owner
        result = self.ownership_manager.suggest_collaboration("code-owner", "technical-health")
        self.assertEqual(result["collaboration_type"], "primary_owner")

        # Test secondary owner
        result = self.ownership_manager.suggest_collaboration("business-analyst", "technical-health")
        self.assertEqual(result["collaboration_type"], "secondary_owner")

        # Test external contributor
        result = self.ownership_manager.suggest_collaboration("architect", "technical-health")
        self.assertEqual(result["collaboration_type"], "external_contributor")

    def test_detect_ownership_conflicts(self):
        """Test ownership conflict detection."""
        conflicts = self.ownership_manager.detect_ownership_conflicts()

        # Should be a list of conflict dictionaries
        self.assertIsInstance(conflicts, list)

class TestDecisionTree(TestCoordinationSystem):
    """Test decision tree system."""

    def test_decision_no_existing_knowledge(self):
        """Test decision for topic with no existing knowledge."""
        decision = self.decision_tree.make_decision(
            "architect", "new-topic", "comprehensive analysis"
        )

        self.assertEqual(decision["decision"], "claim_ownership")
        self.assertIn("No existing knowledge", decision["rationale"])

    def test_decision_existing_fresh_content_owner(self):
        """Test decision for existing fresh content when owner."""
        decision = self.decision_tree.make_decision(
            "code-owner", "technical-health", "additional security analysis"
        )

        self.assertIn(decision["decision"], ["update_existing", "reference_existing"])
        self.assertEqual(decision["confidence"], "high")

    def test_decision_existing_fresh_content_non_owner(self):
        """Test decision for existing fresh content when not owner."""
        decision = self.decision_tree.make_decision(
            "architect", "technical-health", "security analysis"
        )

        self.assertIn(decision["decision"], ["coordinate_required", "avoid_duplication"])
        self.assertIsNotNone(decision.get("coordination_required_with"))

    def test_decision_forced_new(self):
        """Test forced new analysis decision."""
        decision = self.decision_tree.make_decision(
            "architect", "technical-health", "forced analysis", force_new=True
        )

        self.assertEqual(decision["decision"], "proceed_new")
        self.assertIn("warnings", decision)

class TestKnowledgeDashboard(TestCoordinationSystem):
    """Test knowledge dashboard system."""

    def test_generate_dashboard_text(self):
        """Test text dashboard generation."""
        dashboard = self.dashboard.generate_dashboard("text")

        self.assertIn("TEAM-WORKSPACE KNOWLEDGE DASHBOARD", dashboard)
        self.assertIn("KNOWLEDGE SUMMARY", dashboard)
        self.assertIn("SYSTEM HEALTH", dashboard)

    def test_generate_dashboard_json(self):
        """Test JSON dashboard generation."""
        dashboard_json = self.dashboard.generate_dashboard("json")
        dashboard_data = json.loads(dashboard_json)

        self.assertIn("summary", dashboard_data)
        self.assertIn("system_health", dashboard_data)
        self.assertIn("topics", dashboard_data)

    def test_generate_dashboard_markdown(self):
        """Test markdown dashboard generation."""
        dashboard = self.dashboard.generate_dashboard("markdown")

        self.assertIn("# Team-Workspace Knowledge Dashboard", dashboard)
        self.assertIn("## Knowledge Summary", dashboard)
        self.assertIn("| Topic | Status |", dashboard)

    def test_get_knowledge_status_summary(self):
        """Test knowledge status summary."""
        summary = self.dashboard.get_knowledge_status_summary()

        self.assertIn("total_topics", summary)
        self.assertIn("status_distribution", summary)
        self.assertIn("knowledge_health", summary)
        self.assertGreater(summary["total_topics"], 0)

    def test_get_topic_details(self):
        """Test detailed topic information."""
        details = self.dashboard.get_topic_details("technical-health")

        self.assertEqual(details["topic_name"], "technical-health")
        self.assertIn("ownership_info", details)
        self.assertIn("freshness_assessment", details)
        self.assertIn("file_status", details)

    def test_get_topic_details_not_found(self):
        """Test topic details for non-existent topic."""
        details = self.dashboard.get_topic_details("nonexistent-topic")

        self.assertIn("error", details)
        self.assertIn("not found", details["error"])

    def test_check_system_health(self):
        """Test system health check."""
        health = self.dashboard.check_system_health()

        self.assertIn("registry_integrity", health)
        self.assertIn("filesystem_consistency", health)
        self.assertIn("ownership_consistency", health)
        self.assertIn("overall_health", health)

        overall = health["overall_health"]
        self.assertIn("score", overall)
        self.assertIn("level", overall)
        self.assertIsInstance(overall["score"], int)

class TestConflictDetection(TestCoordinationSystem):
    """Test conflict detection system."""

    def test_detect_all_conflicts(self):
        """Test comprehensive conflict detection."""
        conflicts = self.conflict_detector.detect_all_conflicts()

        self.assertIn("duplications", conflicts)
        self.assertIn("contradictions", conflicts)
        self.assertIn("temporal_issues", conflicts)
        self.assertIn("orphaned_content", conflicts)

        # Each should be a list
        for conflict_type, conflict_list in conflicts.items():
            self.assertIsInstance(conflict_list, list)

    def test_detect_duplicate_content(self):
        """Test duplicate content detection."""
        # Create duplicate files
        file1 = self.workspace_path / "commands" / "architect" / "outputs" / "test1.md"
        file2 = self.workspace_path / "commands" / "architect" / "outputs" / "test2.md"

        content = "# Test Analysis\n\nThis is a test analysis with similar content keywords."
        file1.write_text(content)
        file2.write_text(content)

        duplicates = self.conflict_detector.detect_duplicate_content()

        self.assertIsInstance(duplicates, list)

    def test_detect_temporal_inconsistencies(self):
        """Test temporal inconsistency detection."""
        # Create file with future date
        future_file = self.workspace_path / "commands" / "architect" / "outputs" / "future-analysis.md"
        future_date = (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")
        content = f"# Future Analysis\n\n_Generated: {future_date}_\n\nThis has a future date."
        future_file.write_text(content)

        temporal_issues = self.conflict_detector.detect_temporal_inconsistencies()

        self.assertIsInstance(temporal_issues, list)

class TestIntegrationScenarios(TestCoordinationSystem):
    """Test realistic integration scenarios."""

    def test_complete_analysis_workflow(self):
        """Test complete workflow from consultation to superseding."""
        # 1. Consult before execution
        consultation = self.consultant.consult_before_execution(
            "code-owner", "technical-health", "updated security analysis"
        )

        # Should recommend update since owner has fresh content
        self.assertIn(consultation["recommendation"], ["consider_necessity", "update_existing"])

        # 2. Make decision
        decision = self.decision_tree.make_decision(
            "code-owner", "technical-health", "updated security analysis"
        )

        # Should allow update since owner
        self.assertIn(decision["decision"], ["update_existing", "reference_existing"])

        # 3. If updating, declare superseding
        if decision["decision"] == "update_existing":
            # Create files for superseding
            old_file = self.workspace_path / "knowledge" / "technical-health" / "current-assessment.md"
            new_file = self.workspace_path / "knowledge" / "technical-health" / "updated-assessment.md"
            new_file.write_text("Updated technical health assessment")

            superseding = self.workflow.declare_superseding(
                "code-owner", "technical-health", str(new_file),
                [str(old_file)], "Added security analysis"
            )

            self.assertTrue(superseding["success"])

    def test_collaboration_scenario(self):
        """Test collaboration between commands."""
        # 1. Non-owner wants to work on owned topic
        consultation = self.consultant.consult_before_execution(
            "architect", "technical-health", "performance analysis"
        )

        self.assertEqual(consultation["recommendation"], "avoid_duplication")

        # 2. Get collaboration suggestion
        collaboration = self.ownership_manager.suggest_collaboration(
            "architect", "technical-health"
        )

        self.assertEqual(collaboration["collaboration_type"], "external_contributor")
        self.assertTrue(collaboration["coordination_required"])

        # 3. Request secondary ownership
        ownership_result = self.ownership_manager.assign_topic_ownership(
            "technical-health", "code-owner", ["business-analyst", "architect"]
        )

        self.assertTrue(ownership_result["success"])

        # 4. Now consultation should allow coordination
        new_consultation = self.consultant.consult_before_execution(
            "architect", "technical-health", "performance analysis"
        )

        # Should now suggest coordination rather than avoidance
        self.assertNotEqual(new_consultation["recommendation"], "avoid_duplication")

    def test_conflict_resolution_workflow(self):
        """Test workflow for resolving detected conflicts."""
        # 1. Detect conflicts
        conflicts = self.conflict_detector.detect_all_conflicts()

        # 2. Check dashboard for system health
        health = self.dashboard.check_system_health()

        # 3. If conflicts exist, they should be reflected in health
        total_conflicts = sum(len(conflict_list) for conflict_list in conflicts.values())
        if total_conflicts > 0:
            # System health should reflect conflicts
            self.assertIsInstance(health["overall_health"]["score"], int)

def run_all_tests():
    """Run all tests and return results."""
    # Create test suite
    test_classes = [
        TestPreExecutionConsultation,
        TestSupersedingWorkflow,
        TestTopicOwnershipManager,
        TestDecisionTree,
        TestKnowledgeDashboard,
        TestConflictDetection,
        TestIntegrationScenarios
    ]

    suite = unittest.TestSuite()

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result

if __name__ == "__main__":
    print("Running Team-Workspace Content Lifecycle Management System Tests")
    print("=" * 70)

    result = run_all_tests()

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - System is working correctly!")
    else:
        print(f"\n❌ {len(result.failures + result.errors)} tests failed - Review issues above")
