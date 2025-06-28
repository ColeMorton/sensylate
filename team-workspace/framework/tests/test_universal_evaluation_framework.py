#!/usr/bin/env python3
"""
Comprehensive Test Suite for Universal Evaluation Framework
Tests all components of the framework with full coverage
"""

import os
import sys
import json
import yaml
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent))

from evaluation.command_evaluation_protocol import CommandEvaluationProtocol, EvaluationResult, PhaseResult
from evaluation.universal_dependency_validator import UniversalDependencyValidator, ValidationResult, DependencyRequirement
from template_enforcement_engine import TemplateEnforcementEngine, TemplateCompliance, ValidationSeverity
from universal_integration_deployer import UniversalIntegrationDeployer
from phase4_command_catalog import Phase4CommandCatalog
from manifest_generator import ManifestGenerator


class TestCommandEvaluationProtocol:
    """Test suite for Command Evaluation Protocol"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def evaluation_protocol(self, temp_workspace):
        """Create evaluation protocol instance"""
        return CommandEvaluationProtocol(temp_workspace)

    @pytest.fixture
    def sample_manifest(self):
        """Sample evaluation manifest for testing"""
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
                    },
                    "0B_execution_monitoring": {
                        "gates": [
                            {
                                "name": "progress_monitoring",
                                "threshold": 0.8,
                                "critical": False,
                                "adaptive": True
                            }
                        ]
                    },
                    "0C_post_execution": {
                        "gates": [
                            {
                                "name": "output_validation",
                                "threshold": 0.9,
                                "critical": True
                            }
                        ]
                    },
                    "0D_feedback_integration": {
                        "gates": [
                            {
                                "name": "learning_integration",
                                "threshold": 0.8,
                                "critical": False
                            }
                        ]
                    }
                },
                "quality_targets": {
                    "overall_threshold": 0.75,
                    "critical_gate_threshold": 0.95,
                    "performance_target": 0.85
                }
            }
        }

    def test_initialization(self, temp_workspace):
        """Test protocol initialization"""
        protocol = CommandEvaluationProtocol(temp_workspace)
        assert protocol.workspace_path == Path(temp_workspace)
        assert protocol.results_path.exists()

    def test_evaluate_command_success(self, evaluation_protocol, sample_manifest):
        """Test successful command evaluation"""
        context = {"command": "test_command", "test_mode": True}

        result = evaluation_protocol.evaluate_command("test_command", sample_manifest, context)

        assert isinstance(result, EvaluationResult)
        assert result.command == "test_command"
        assert result.overall_score > 0
        assert len(result.phase_results) == 4
        assert all(phase in result.phase_results for phase in ["0A", "0B", "0C", "0D"])

    def test_evaluate_command_critical_failure(self, evaluation_protocol, sample_manifest):
        """Test command evaluation with critical gate failure"""
        # Modify manifest to have impossible threshold
        sample_manifest["evaluation"]["phases"]["0A_pre_execution"]["gates"][0]["threshold"] = 2.0

        context = {"command": "test_command", "test_mode": True}
        result = evaluation_protocol.evaluate_command("test_command", sample_manifest, context)

        assert not result.can_proceed

    def test_enhancement_mode_detection(self, evaluation_protocol, sample_manifest, temp_workspace):
        """Test enhancement mode detection"""
        # Create evaluation file
        eval_file = Path(temp_workspace) / "test_command_evaluation.md"
        eval_file.write_text("# Test Evaluation\nSample evaluation content")

        context = {"command": "test_command", "test_mode": True}
        result = evaluation_protocol.evaluate_command("test_command", sample_manifest, context)

        # Enhancement mode should be detected
        assert "enhancement_mode" in result.metadata

    def test_phase_validation(self, evaluation_protocol):
        """Test individual phase validation"""
        gates = [
            {"name": "test_gate", "threshold": 0.8, "critical": False, "adaptive": True}
        ]
        context = {"test_mode": True}

        phase_result = evaluation_protocol._validate_phase("0A", gates, context)

        assert isinstance(phase_result, PhaseResult)
        assert phase_result.phase == "0A"
        assert phase_result.score >= 0

    def test_adaptive_threshold_adjustment(self, evaluation_protocol):
        """Test adaptive threshold adjustment"""
        initial_threshold = 0.8
        performance_score = 0.95

        adjusted = evaluation_protocol._adjust_adaptive_threshold(initial_threshold, performance_score)

        # Should adjust based on performance
        assert adjusted != initial_threshold

    def test_result_saving(self, evaluation_protocol, sample_manifest, temp_workspace):
        """Test evaluation result saving"""
        context = {"command": "test_command", "test_mode": True}
        result = evaluation_protocol.evaluate_command("test_command", sample_manifest, context)

        # Check if result file was created
        result_files = list(Path(temp_workspace).glob("**/test_command_evaluation_*.json"))
        assert len(result_files) > 0


class TestUniversalDependencyValidator:
    """Test suite for Universal Dependency Validator"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def dependency_validator(self, temp_workspace):
        """Create dependency validator instance"""
        return UniversalDependencyValidator(temp_workspace)

    @pytest.fixture
    def sample_dependencies_manifest(self):
        """Sample dependency manifest for testing"""
        return {
            "command": "test_command",
            "version": "1.0",
            "dependencies": {
                "yahoo_finance_api": {
                    "type": "api",
                    "required": True,
                    "validation_method": "api_test",
                    "fallback_strategies": [
                        {
                            "strategy": "cached_data",
                            "description": "Use cached data if API unavailable",
                            "max_age_hours": 4
                        }
                    ]
                },
                "local_file": {
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

    def test_initialization(self, temp_workspace):
        """Test validator initialization"""
        validator = UniversalDependencyValidator(temp_workspace)
        assert validator.workspace_path == Path(temp_workspace)
        assert validator.cache_path.exists()

    def test_validate_command_dependencies(self, dependency_validator, sample_dependencies_manifest):
        """Test command dependency validation"""
        result = dependency_validator.validate_command_dependencies("test_command", sample_dependencies_manifest)

        assert "command" in result
        assert "overall_score" in result
        assert "can_proceed" in result
        assert "validation_results" in result
        assert isinstance(result["validation_results"], list)

    def test_dependency_requirement_creation(self, dependency_validator):
        """Test dependency requirement creation"""
        dep_config = {
            "type": "api",
            "required": True,
            "validation_method": "api_test",
            "fallback_strategies": [{"strategy": "cached_data"}]
        }

        requirement = dependency_validator._create_dependency_requirement("test_dep", dep_config)

        assert isinstance(requirement, DependencyRequirement)
        assert requirement.name == "test_dep"
        assert requirement.type == "api"
        assert requirement.required == True

    def test_api_dependency_validation(self, dependency_validator):
        """Test API dependency validation"""
        requirement = DependencyRequirement(
            name="test_api",
            type="api",
            required=True,
            fallback_strategies=["cached_data"],
            validation_method="api_test"
        )

        result = dependency_validator._validate_api_dependency(requirement)

        assert isinstance(result, ValidationResult)
        assert result.dependency_name == "test_api"

    def test_file_dependency_validation(self, dependency_validator, temp_workspace):
        """Test file dependency validation"""
        # Create test file
        test_file = Path(temp_workspace) / "test_file.txt"
        test_file.write_text("test content")

        requirement = DependencyRequirement(
            name=str(test_file),
            type="file",
            required=True,
            fallback_strategies=[],
            validation_method="file_check"
        )

        result = dependency_validator._validate_file_dependency(requirement)

        assert isinstance(result, ValidationResult)
        assert result.available == True

    def test_fallback_strategy_generation(self, dependency_validator, sample_dependencies_manifest):
        """Test fallback strategy generation"""
        dependencies = [
            DependencyRequirement(
                name="test_dep",
                type="api",
                required=True,
                fallback_strategies=["cached_data", "alternative_source"],
                validation_method="api_test"
            )
        ]

        validation_results = [
            ValidationResult(
                dependency_name="test_dep",
                available=False,
                validation_score=0.0
            )
        ]

        strategy = dependency_validator._generate_fallback_strategy(dependencies, validation_results)

        assert "strategy_type" in strategy
        assert "recommended_actions" in strategy

    def test_caching_mechanism(self, dependency_validator):
        """Test dependency validation caching"""
        dependency_name = "test_cache_dep"

        # First validation (should cache)
        result1 = dependency_validator._validate_yahoo_finance_api()

        # Second validation (should use cache if within time limit)
        result2 = dependency_validator._validate_yahoo_finance_api()

        # Results should be consistent
        assert result1.dependency_name == result2.dependency_name


class TestTemplateEnforcementEngine:
    """Test suite for Template Enforcement Engine"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def template_engine(self, temp_workspace):
        """Create template enforcement engine instance"""
        return TemplateEnforcementEngine(temp_workspace)

    @pytest.fixture
    def sample_markdown_content(self):
        """Sample markdown content for testing"""
        return """# Test Document

This is a test document with some content.

## Section 1

Content for section 1.

TODO: Add more content here.

## Section 2

Content for section 2.
"""

    @pytest.fixture
    def sample_command_info(self):
        """Sample command info for template generation"""
        return {
            "command_type": "analysis",
            "complexity": "medium",
            "template_requirements": {
                "output_types": ["markdown", "json"],
                "standardization_needed": True,
                "metadata_requirements": True
            }
        }

    def test_initialization(self, temp_workspace):
        """Test engine initialization"""
        engine = TemplateEnforcementEngine(temp_workspace)
        assert engine.workspace_path == Path(temp_workspace)
        assert engine.templates_path.exists()

    def test_enforce_template_compliance(self, template_engine, sample_markdown_content):
        """Test template compliance enforcement"""
        compliance = template_engine.enforce_template_compliance(
            "test_command", sample_markdown_content, "markdown"
        )

        assert isinstance(compliance, TemplateCompliance)
        assert compliance.command == "test_command"
        assert 0 <= compliance.overall_score <= 1
        assert 0 <= compliance.compliance_percentage <= 100

    def test_markdown_structure_validation(self, template_engine, sample_markdown_content):
        """Test markdown structure validation"""
        rule = {"type": "markdown_structure"}
        results = template_engine._validate_markdown_structure(sample_markdown_content, rule)

        assert isinstance(results, list)
        for result in results:
            assert hasattr(result, 'valid')
            assert hasattr(result, 'severity')
            assert hasattr(result, 'message')

    def test_json_schema_validation(self, template_engine):
        """Test JSON schema validation"""
        json_content = json.dumps({
            "timestamp": datetime.now().isoformat(),
            "command": "test_command",
            "status": "success"
        })

        rule = {"type": "json_schema"}
        results = template_engine._validate_json_schema(json_content, rule)

        assert isinstance(results, list)

    def test_automatic_fixes(self, template_engine):
        """Test automatic content fixes"""
        content_with_issues = "This has mixed *bold* and **bold** formatting.\r\nAnd inconsistent line endings.\n"

        validation_results = [
            Mock(severity=ValidationSeverity.INFO, rule_name="line_endings"),
            Mock(severity=ValidationSeverity.INFO, rule_name="consistent_formatting")
        ]

        fixed_content, fixes_applied = template_engine._apply_automatic_fixes(
            content_with_issues, validation_results, "markdown"
        )

        assert fixes_applied > 0
        assert "\r\n" not in fixed_content

    def test_template_generation(self, template_engine, sample_command_info):
        """Test template generation for commands"""
        templates = template_engine.generate_template_for_command("test_command", sample_command_info)

        assert isinstance(templates, dict)
        assert "markdown" in templates
        assert "json" in templates

    def test_compliance_scoring(self, template_engine):
        """Test compliance score calculation"""
        validation_results = [
            Mock(valid=True, severity=ValidationSeverity.INFO),
            Mock(valid=False, severity=ValidationSeverity.WARNING),
            Mock(valid=False, severity=ValidationSeverity.ERROR)
        ]

        score = template_engine._calculate_compliance_score(validation_results)

        assert 0 <= score <= 1

    def test_metadata_header_validation(self, template_engine):
        """Test metadata header validation"""
        content_with_metadata = """---
Created: 2025-06-28
Author: Test
---

# Test Document
Content here.
"""

        content_without_metadata = """# Test Document
Content here.
"""

        rule = {"type": "metadata_headers"}

        results_with = template_engine._validate_metadata_headers(content_with_metadata, rule)
        results_without = template_engine._validate_metadata_headers(content_without_metadata, rule)

        assert len(results_without) > len(results_with)


class TestUniversalIntegrationDeployer:
    """Test suite for Universal Integration Deployer"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        # Create necessary directory structure
        (Path(temp_dir) / "framework" / "results").mkdir(parents=True)
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def temp_commands_dir(self):
        """Create temporary commands directory"""
        temp_dir = tempfile.mkdtemp()

        # Create sample manifest files
        commands = ["test_command", "another_command"]
        for command in commands:
            eval_file = Path(temp_dir) / f"{command}.eval.yaml"
            deps_file = Path(temp_dir) / f"{command}.deps.yaml"

            eval_content = {
                "command": command,
                "evaluation": {
                    "phases": {
                        "0A_pre_execution": {
                            "gates": [{"name": "input_validation", "threshold": 1.0, "critical": True}]
                        }
                    },
                    "quality_targets": {"overall_threshold": 0.75}
                }
            }

            deps_content = {
                "command": command,
                "dependencies": {
                    "test_dep": {
                        "type": "api",
                        "required": True,
                        "fallback_strategies": [{"strategy": "cached_data"}]
                    }
                }
            }

            with open(eval_file, 'w') as f:
                yaml.dump(eval_content, f)
            with open(deps_file, 'w') as f:
                yaml.dump(deps_content, f)

        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def integration_deployer(self, temp_workspace):
        """Create integration deployer instance"""
        return UniversalIntegrationDeployer(temp_workspace)

    def test_initialization(self, temp_workspace):
        """Test deployer initialization"""
        deployer = UniversalIntegrationDeployer(temp_workspace)
        assert deployer.workspace_path == Path(temp_workspace)

    @patch('universal_integration_deployer.Path.glob')
    def test_commands_discovery(self, mock_glob, integration_deployer, temp_commands_dir):
        """Test command discovery with manifests"""
        # Mock glob to return test files
        eval_files = [Path(temp_commands_dir) / "test_command.eval.yaml"]
        mock_glob.return_value = eval_files

        # Mock the commands path
        integration_deployer.commands_path = Path(temp_commands_dir)

        commands = integration_deployer._get_commands_with_manifests()

        assert isinstance(commands, list)

    def test_integration_quality_calculation(self, integration_deployer):
        """Test integration quality score calculation"""
        deps_validation = {"overall_score": 0.8}
        eval_test = {"success": True, "overall_score": 0.9}
        template_compliance = {"compliance_score": 0.85}
        wrapper_created = True

        quality_score = integration_deployer._calculate_integration_quality(
            deps_validation, eval_test, template_compliance, wrapper_created
        )

        assert 0 <= quality_score <= 1

    def test_enhanced_wrapper_creation(self, integration_deployer, temp_workspace):
        """Test enhanced wrapper creation"""
        eval_manifest = {
            "evaluation": {
                "template_enforcement": {"enabled": True}
            }
        }
        deps_manifest = {"dependencies": {}}

        success = integration_deployer._create_enhanced_wrapper(
            "test_command", eval_manifest, deps_manifest
        )

        assert isinstance(success, bool)

    def test_ecosystem_health_calculation(self, integration_deployer):
        """Test ecosystem health calculation"""
        integrated_commands = ["command1", "command2"]
        compatibility_tests = {
            "framework_compatibility": True,
            "manifest_compatibility": True,
            "template_compatibility": True
        }
        performance_tests = {"performance_acceptable": True}

        # Set up integration results
        integration_deployer.integration_results = {"total_commands": 2}

        health = integration_deployer._calculate_ecosystem_health(
            integrated_commands, compatibility_tests, performance_tests
        )

        assert health in ["excellent", "good", "fair", "needs_improvement"]


class TestPhase4CommandCatalog:
    """Test suite for Phase 4 Command Catalog"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def temp_commands_dir(self):
        """Create temporary commands directory with sample commands"""
        temp_dir = tempfile.mkdtemp()

        # Create sample command files
        commands = {
            "trading_analyzer.md": "# Trading Analyzer\nAnalyzes trading strategies and market data.",
            "content_creator.md": "# Content Creator\nCreates social media content and blog posts.",
            "simple_utility.md": "# Simple Utility\nBasic utility command for simple tasks."
        }

        for filename, content in commands.items():
            (Path(temp_dir) / filename).write_text(content)

        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_initialization(self, temp_workspace):
        """Test catalog initialization"""
        catalog = Phase4CommandCatalog(temp_workspace)
        assert catalog.workspace_path == Path(temp_workspace)

    @patch('phase4_command_catalog.Path.glob')
    def test_command_discovery(self, mock_glob, temp_workspace, temp_commands_dir):
        """Test command discovery and cataloging"""
        # Mock glob to return test command files
        command_files = list(Path(temp_commands_dir).glob("*.md"))
        mock_glob.return_value = command_files

        catalog = Phase4CommandCatalog(temp_workspace)
        catalog.commands_path = Path(temp_commands_dir)

        result = catalog.catalog_commands()

        assert "phase4_scope" in result
        assert "commands" in result["phase4_scope"]

    def test_complexity_assessment(self, temp_workspace):
        """Test command complexity assessment"""
        catalog = Phase4CommandCatalog(temp_workspace)

        high_complexity_content = "fundamental analysis market data trading strategy backtesting"
        medium_complexity_content = "content creation social media publishing optimization"
        low_complexity_content = "simple basic utility helper function"

        assert catalog._assess_complexity(high_complexity_content) == "high"
        assert catalog._assess_complexity(medium_complexity_content) == "medium"
        assert catalog._assess_complexity(low_complexity_content) == "low"

    def test_command_type_classification(self, temp_workspace):
        """Test command type classification"""
        catalog = Phase4CommandCatalog(temp_workspace)

        analysis_content = "fundamental analysis market research data analysis"
        content_content = "content creation social media blog publishing"
        trading_content = "trading strategy backtesting market signals"
        development_content = "technical implementation architecture planning"

        assert catalog._classify_command_type(analysis_content) == "analysis"
        assert catalog._classify_command_type(content_content) == "content"
        assert catalog._classify_command_type(trading_content) == "trading"
        assert catalog._classify_command_type(development_content) == "development"


class TestManifestGenerator:
    """Test suite for Manifest Generator"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_command_catalog(self):
        """Sample command catalog for testing"""
        return {
            "phase4_scope": {
                "commands": {
                    "test_command": {
                        "complexity": "medium",
                        "command_type": "analysis",
                        "estimated_time": 60,
                        "dependencies": ["yahoo_finance_api", "local_storage"]
                    }
                }
            }
        }

    def test_initialization(self, temp_workspace):
        """Test generator initialization"""
        generator = ManifestGenerator(temp_workspace)
        assert generator.workspace_path == Path(temp_workspace)

    def test_evaluation_manifest_generation(self, temp_workspace, sample_command_catalog):
        """Test evaluation manifest generation"""
        generator = ManifestGenerator(temp_workspace)

        manifest = generator._generate_evaluation_manifest(
            "test_command",
            sample_command_catalog["phase4_scope"]["commands"]["test_command"]
        )

        assert "command" in manifest
        assert "evaluation" in manifest
        assert "phases" in manifest["evaluation"]
        assert "quality_targets" in manifest["evaluation"]

    def test_dependency_manifest_generation(self, temp_workspace, sample_command_catalog):
        """Test dependency manifest generation"""
        generator = ManifestGenerator(temp_workspace)

        manifest = generator._generate_dependency_manifest(
            "test_command",
            sample_command_catalog["phase4_scope"]["commands"]["test_command"]
        )

        assert "command" in manifest
        assert "dependencies" in manifest

    def test_quality_gates_generation(self, temp_workspace):
        """Test quality gates generation"""
        generator = ManifestGenerator(temp_workspace)

        command_info = {
            "complexity": "high",
            "command_type": "analysis",
            "estimated_time": 120
        }

        gates = generator._generate_quality_gates("test_command", command_info)

        assert isinstance(gates, list)
        assert len(gates) > 0
        for gate in gates:
            assert "name" in gate
            assert "threshold" in gate
            assert "critical" in gate

    def test_dependency_requirements_generation(self, temp_workspace):
        """Test dependency requirements generation"""
        generator = ManifestGenerator(temp_workspace)

        command_info = {
            "dependencies": ["yahoo_finance_api", "local_storage", "external_service"]
        }

        dependencies = generator._generate_dependency_requirements("test_command", command_info)

        assert isinstance(dependencies, dict)
        assert len(dependencies) > 0

    def test_fallback_strategies_generation(self, temp_workspace):
        """Test fallback strategies generation"""
        generator = ManifestGenerator(temp_workspace)

        strategies = generator._generate_fallback_strategies("api", True)

        assert isinstance(strategies, list)
        assert len(strategies) > 0
        for strategy in strategies:
            assert "strategy" in strategy
            assert "description" in strategy


# Integration Tests
class TestFrameworkIntegration:
    """Integration tests for the complete framework"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        (Path(temp_dir) / "framework" / "results").mkdir(parents=True)
        (Path(temp_dir) / "framework" / "wrappers").mkdir(parents=True)
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_end_to_end_command_evaluation(self, temp_workspace):
        """Test complete command evaluation flow"""
        # Create sample manifests
        eval_manifest = {
            "command": "integration_test",
            "evaluation": {
                "phases": {
                    "0A_pre_execution": {
                        "gates": [{"name": "input_validation", "threshold": 1.0, "critical": True}]
                    }
                },
                "quality_targets": {"overall_threshold": 0.75}
            }
        }

        deps_manifest = {
            "command": "integration_test",
            "dependencies": {
                "test_dependency": {
                    "type": "file",
                    "required": False,
                    "fallback_strategies": [{"strategy": "create_default"}]
                }
            }
        }

        # Initialize components
        protocol = CommandEvaluationProtocol(temp_workspace)
        validator = UniversalDependencyValidator(temp_workspace)

        # Run evaluation
        context = {"command": "integration_test", "test_mode": True}
        eval_result = protocol.evaluate_command("integration_test", eval_manifest, context)

        # Run dependency validation
        deps_result = validator.validate_command_dependencies("integration_test", deps_manifest)

        # Verify results
        assert eval_result.command == "integration_test"
        assert eval_result.overall_score > 0
        assert deps_result["command"] == "integration_test"

    def test_framework_component_compatibility(self, temp_workspace):
        """Test compatibility between framework components"""
        # Test that all components can be initialized together
        protocol = CommandEvaluationProtocol(temp_workspace)
        validator = UniversalDependencyValidator(temp_workspace)
        template_engine = TemplateEnforcementEngine(temp_workspace)

        # Verify they share compatible workspace structure
        assert protocol.workspace_path == Path(temp_workspace)
        assert validator.workspace_path == Path(temp_workspace)
        assert template_engine.workspace_path == Path(temp_workspace)

    def test_manifest_schema_validation(self, temp_workspace):
        """Test that generated manifests are valid"""
        generator = ManifestGenerator(temp_workspace)

        command_info = {
            "complexity": "medium",
            "command_type": "analysis",
            "estimated_time": 60,
            "dependencies": ["yahoo_finance_api"]
        }

        eval_manifest = generator._generate_evaluation_manifest("test_command", command_info)
        deps_manifest = generator._generate_dependency_manifest("test_command", command_info)

        # Verify manifests have required structure
        assert "command" in eval_manifest
        assert "evaluation" in eval_manifest
        assert "command" in deps_manifest
        assert "dependencies" in deps_manifest


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
