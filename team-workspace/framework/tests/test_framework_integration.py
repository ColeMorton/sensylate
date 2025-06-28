#!/usr/bin/env python3
"""
Integration Tests for Universal Evaluation Framework
Focus on working integration tests with actual API
"""

import os
import sys
import json
import yaml
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent))

from evaluation.command_evaluation_protocol import CommandEvaluationProtocol
from evaluation.universal_dependency_validator import UniversalDependencyValidator
from template_enforcement_engine import TemplateEnforcementEngine


class TestFrameworkIntegration:
    """Integration tests for the Universal Evaluation Framework"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        # Create necessary directories
        (Path(temp_dir) / "framework" / "results").mkdir(parents=True)
        (Path(temp_dir) / "framework" / "cache").mkdir(parents=True)
        (Path(temp_dir) / "framework" / "templates").mkdir(parents=True)
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_eval_manifest(self):
        """Sample evaluation manifest"""
        return {
            "command": "test_command",
            "version": "1.0",
            "evaluation": {
                "phases": {
                    "0A_pre_execution": {
                        "gates": [
                            {
                                "name": "input_validation",
                                "description": "Validate input parameters",
                                "threshold": 1.0,
                                "critical": True,
                                "adaptive": False
                            }
                        ]
                    }
                },
                "quality_targets": {
                    "overall_threshold": 0.75,
                    "critical_gate_threshold": 0.95
                },
                "template_enforcement": {
                    "enabled": True,
                    "strictness": "medium"
                }
            }
        }

    @pytest.fixture
    def sample_deps_manifest(self):
        """Sample dependency manifest"""
        return {
            "command": "test_command",
            "version": "1.0",
            "dependencies": {
                "test_dependency": {
                    "type": "file",
                    "required": False,
                    "validation_method": "file_check",
                    "fallback_strategies": [
                        {
                            "strategy": "create_default",
                            "description": "Create default file if missing"
                        }
                    ]
                }
            }
        }

    def test_framework_components_initialization(self, temp_workspace):
        """Test that all framework components can be initialized"""
        # Test initialization of core components
        evaluation_protocol = CommandEvaluationProtocol(temp_workspace)
        dependency_validator = UniversalDependencyValidator(temp_workspace)
        template_engine = TemplateEnforcementEngine(temp_workspace)

        # Verify components are properly initialized
        assert evaluation_protocol.workspace_path == Path(temp_workspace)
        assert dependency_validator.workspace_path == Path(temp_workspace)
        assert template_engine.workspace_path == Path(temp_workspace)

        # Verify required directories exist
        assert evaluation_protocol.results_path.exists()
        assert dependency_validator.cache_path.exists()
        assert template_engine.templates_path.exists()

    def test_command_evaluation_basic_flow(self, temp_workspace, sample_eval_manifest):
        """Test basic command evaluation flow"""
        evaluation_protocol = CommandEvaluationProtocol(temp_workspace)

        context = {
            "command": "test_command",
            "test_mode": True,
            "timestamp": "2025-06-28T15:00:00Z"
        }

        result = evaluation_protocol.evaluate_command("test_command", sample_eval_manifest, context)

        # Verify evaluation result structure
        assert hasattr(result, 'command')
        assert hasattr(result, 'overall_score')
        assert hasattr(result, 'can_proceed')
        assert hasattr(result, 'phase_results')

        assert result.command == "test_command"
        assert isinstance(result.overall_score, float)
        assert isinstance(result.can_proceed, bool)

    def test_dependency_validation_basic_flow(self, temp_workspace, sample_deps_manifest):
        """Test basic dependency validation flow"""
        dependency_validator = UniversalDependencyValidator(temp_workspace)

        result = dependency_validator.validate_command_dependencies("test_command", sample_deps_manifest)

        # Verify dependency validation result structure
        assert isinstance(result, dict)
        assert "command" in result
        assert "overall_score" in result
        assert "can_proceed" in result
        assert "validation_results" in result

        assert result["command"] == "test_command"
        assert isinstance(result["overall_score"], float)
        assert isinstance(result["can_proceed"], bool)
        assert isinstance(result["validation_results"], list)

    def test_template_enforcement_basic_flow(self, temp_workspace):
        """Test basic template enforcement flow"""
        template_engine = TemplateEnforcementEngine(temp_workspace)

        sample_content = """# Test Document

This is a test document.

## Section 1

Content for section 1.
"""

        compliance = template_engine.enforce_template_compliance(
            "test_command", sample_content, "markdown"
        )

        # Verify template compliance result structure
        assert hasattr(compliance, 'command')
        assert hasattr(compliance, 'overall_score')
        assert hasattr(compliance, 'compliance_percentage')
        assert hasattr(compliance, 'validation_results')

        assert compliance.command == "test_command"
        assert isinstance(compliance.overall_score, float)
        assert isinstance(compliance.compliance_percentage, float)

    def test_integrated_command_execution_flow(self, temp_workspace, sample_eval_manifest, sample_deps_manifest):
        """Test integrated command execution with all components"""
        # Initialize all components
        evaluation_protocol = CommandEvaluationProtocol(temp_workspace)
        dependency_validator = UniversalDependencyValidator(temp_workspace)
        template_engine = TemplateEnforcementEngine(temp_workspace)

        # Step 1: Validate dependencies
        deps_result = dependency_validator.validate_command_dependencies("test_command", sample_deps_manifest)
        assert deps_result["can_proceed"] is not None

        # Step 2: Run evaluation protocol
        context = {"command": "test_command", "test_mode": True}
        eval_result = evaluation_protocol.evaluate_command("test_command", sample_eval_manifest, context)
        assert eval_result.command == "test_command"

        # Step 3: Enforce template compliance
        sample_output = "# Test Command Output\n\nThis is sample output."
        compliance = template_engine.enforce_template_compliance("test_command", sample_output, "markdown")
        assert compliance.command == "test_command"

        # Verify all components worked together
        assert deps_result["command"] == eval_result.command == compliance.command

    def test_framework_error_handling(self, temp_workspace):
        """Test framework error handling"""
        evaluation_protocol = CommandEvaluationProtocol(temp_workspace)

        # Test with invalid manifest
        invalid_manifest = {"invalid": "manifest"}
        context = {"command": "test_command", "test_mode": True}

        # Should not raise an exception
        try:
            result = evaluation_protocol.evaluate_command("test_command", invalid_manifest, context)
            # Result should indicate failure or low score
            assert hasattr(result, 'overall_score')
        except Exception as e:
            # If it does raise, it should be a controlled exception
            assert isinstance(e, (ValueError, KeyError))

    def test_framework_performance(self, temp_workspace, sample_eval_manifest, sample_deps_manifest):
        """Test framework performance characteristics"""
        import time

        evaluation_protocol = CommandEvaluationProtocol(temp_workspace)
        dependency_validator = UniversalDependencyValidator(temp_workspace)

        # Measure evaluation time
        start_time = time.time()
        context = {"command": "test_command", "test_mode": True}
        eval_result = evaluation_protocol.evaluate_command("test_command", sample_eval_manifest, context)
        eval_time = time.time() - start_time

        # Measure dependency validation time
        start_time = time.time()
        deps_result = dependency_validator.validate_command_dependencies("test_command", sample_deps_manifest)
        deps_time = time.time() - start_time

        # Verify reasonable performance (should be under 1 second each)
        assert eval_time < 1.0, f"Evaluation took {eval_time:.2f}s, should be under 1s"
        assert deps_time < 1.0, f"Dependency validation took {deps_time:.2f}s, should be under 1s"

    def test_framework_result_persistence(self, temp_workspace, sample_eval_manifest):
        """Test that framework results are properly persisted"""
        evaluation_protocol = CommandEvaluationProtocol(temp_workspace)

        context = {"command": "test_command", "test_mode": True}
        result = evaluation_protocol.evaluate_command("test_command", sample_eval_manifest, context)

        # Check that result files are created
        results_dir = Path(temp_workspace) / "framework" / "results"
        result_files = list(results_dir.glob("test_command_evaluation_*.json"))

        assert len(result_files) > 0, "No evaluation result files were created"

        # Verify result file content
        with open(result_files[0], 'r') as f:
            saved_result = json.load(f)

        assert "command" in saved_result
        assert "overall_score" in saved_result
        assert saved_result["command"] == "test_command"

    def test_framework_caching_behavior(self, temp_workspace, sample_deps_manifest):
        """Test framework caching mechanisms"""
        dependency_validator = UniversalDependencyValidator(temp_workspace)

        # First validation (should create cache)
        result1 = dependency_validator.validate_command_dependencies("test_command", sample_deps_manifest)

        # Check cache directory
        cache_files = list(dependency_validator.cache_path.glob("*_validation.json"))
        initial_cache_count = len(cache_files)

        # Second validation (should potentially use cache)
        result2 = dependency_validator.validate_command_dependencies("test_command", sample_deps_manifest)

        # Results should be consistent
        assert result1["command"] == result2["command"]
        assert result1["overall_score"] == result2["overall_score"]

    def test_template_generation_and_validation(self, temp_workspace):
        """Test template generation and validation flow"""
        template_engine = TemplateEnforcementEngine(temp_workspace)

        command_info = {
            "command_type": "analysis",
            "complexity": "medium",
            "template_requirements": {
                "output_types": ["markdown"],
                "standardization_needed": True,
                "metadata_requirements": True
            }
        }

        # Generate templates
        templates = template_engine.generate_template_for_command("test_command", command_info)

        assert isinstance(templates, dict)
        assert "markdown" in templates

        # Test template compliance
        sample_content = templates["markdown"]
        compliance = template_engine.enforce_template_compliance("test_command", sample_content, "markdown")

        # Generated template should have good compliance
        assert compliance.overall_score > 0.5


class TestFrameworkComponentAPIs:
    """Test the actual APIs of framework components"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        (Path(temp_dir) / "framework" / "results").mkdir(parents=True)
        (Path(temp_dir) / "framework" / "cache").mkdir(parents=True)
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_evaluation_protocol_api(self, temp_workspace):
        """Test CommandEvaluationProtocol API"""
        protocol = CommandEvaluationProtocol(temp_workspace)

        # Test public methods exist
        assert hasattr(protocol, 'evaluate_command')
        assert callable(protocol.evaluate_command)

        # Test with minimal manifest
        minimal_manifest = {
            "evaluation": {
                "phases": {},
                "quality_targets": {"overall_threshold": 0.75}
            }
        }

        result = protocol.evaluate_command("test", minimal_manifest, {"test_mode": True})
        assert hasattr(result, 'command')
        assert hasattr(result, 'overall_score')

    def test_dependency_validator_api(self, temp_workspace):
        """Test UniversalDependencyValidator API"""
        validator = UniversalDependencyValidator(temp_workspace)

        # Test public methods exist
        assert hasattr(validator, 'validate_command_dependencies')
        assert callable(validator.validate_command_dependencies)

        # Test with minimal manifest
        minimal_manifest = {"dependencies": {}}

        result = validator.validate_command_dependencies("test", minimal_manifest)
        assert isinstance(result, dict)
        assert "command" in result

    def test_template_engine_api(self, temp_workspace):
        """Test TemplateEnforcementEngine API"""
        engine = TemplateEnforcementEngine(temp_workspace)

        # Test public methods exist
        assert hasattr(engine, 'enforce_template_compliance')
        assert hasattr(engine, 'generate_template_for_command')
        assert callable(engine.enforce_template_compliance)
        assert callable(engine.generate_template_for_command)

        # Test basic compliance check
        compliance = engine.enforce_template_compliance("test", "# Test\nContent", "markdown")
        assert hasattr(compliance, 'command')
        assert hasattr(compliance, 'overall_score')


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
