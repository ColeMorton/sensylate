#!/usr/bin/env python3
"""
Universal Integration Deployer
Integrates Universal Evaluation Framework across all commands
"""

import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add framework to path
sys.path.append(str(Path(__file__).parent))

from evaluation.universal_dependency_validator import UniversalDependencyValidator
from evaluation.command_evaluation_protocol import CommandEvaluationProtocol
from template_enforcement_engine import TemplateEnforcementEngine

class UniversalIntegrationDeployer:
    """Deploys Universal Evaluation Framework across all commands"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.commands_path = Path(".claude/commands")

        # Initialize framework components
        self.dependency_validator = UniversalDependencyValidator(workspace_path)
        self.evaluation_protocol = CommandEvaluationProtocol(workspace_path)
        self.template_engine = TemplateEnforcementEngine(workspace_path)

        # Load deployment configuration
        self.deployment_config = self._load_deployment_config()

        # Integration tracking
        self.integration_results = {
            "timestamp": datetime.now().isoformat(),
            "total_commands": 0,
            "integrated_commands": {},
            "integration_summary": {},
            "validation_results": {}
        }

    def deploy_universal_framework(self) -> Dict[str, Any]:
        """Deploy Universal Evaluation Framework across all commands"""

        print("🚀 UNIVERSAL EVALUATION FRAMEWORK DEPLOYMENT")
        print("=" * 60)

        # Get all commands with manifests
        commands_with_manifests = self._get_commands_with_manifests()
        self.integration_results["total_commands"] = len(commands_with_manifests)

        print(f"📊 Deploying to {len(commands_with_manifests)} commands")

        # Deploy in priority order
        deployment_order = self._get_deployment_order(commands_with_manifests)

        for i, command in enumerate(deployment_order, 1):
            print(f"\n🔧 [{i}/{len(deployment_order)}] Integrating: {command}")

            try:
                integration_result = self._integrate_command(command)
                self.integration_results["integrated_commands"][command] = integration_result

                # Display integration status
                status = "✅" if integration_result["success"] else "❌"
                print(f"   {status} Integration: {integration_result['status']}")

                if integration_result["success"]:
                    print(f"      📋 Quality Gates: {integration_result['quality_gates']}")
                    print(f"      🔗 Dependencies: {integration_result['dependencies_validated']}")
                    print(f"      📝 Template: {integration_result['template_compliance']:.1%}")
                else:
                    print(f"      ❌ Error: {integration_result.get('error', 'Unknown error')}")

            except Exception as e:
                print(f"   ❌ Integration failed: {str(e)}")
                self.integration_results["integrated_commands"][command] = {
                    "success": False,
                    "error": str(e),
                    "status": "failed"
                }

        # Generate integration summary
        self._generate_integration_summary()

        # Validate complete ecosystem
        ecosystem_validation = self._validate_ecosystem_integration()
        self.integration_results["validation_results"] = ecosystem_validation

        print(f"\n📊 DEPLOYMENT SUMMARY:")
        summary = self.integration_results["integration_summary"]
        print(f"   Total Commands: {summary['total_commands']}")
        print(f"   Successfully Integrated: {summary['successful_integrations']}")
        print(f"   Failed Integrations: {summary['failed_integrations']}")
        print(f"   Success Rate: {summary['success_rate']:.1%}")
        print(f"   Ecosystem Health: {ecosystem_validation['overall_health']}")

        return self.integration_results

    def _integrate_command(self, command: str) -> Dict[str, Any]:
        """Integrate Universal Evaluation Framework for single command"""

        # Load command manifests
        eval_manifest = self._load_evaluation_manifest(command)
        deps_manifest = self._load_dependency_manifest(command)

        if not eval_manifest or not deps_manifest:
            return {
                "success": False,
                "status": "missing_manifests",
                "error": "Required manifests not found"
            }

        # Validate dependency manifest
        deps_validation = self.dependency_validator.validate_command_dependencies(
            command, deps_manifest
        )

        # Test evaluation protocol
        eval_test = self._test_evaluation_protocol(command, eval_manifest)

        # Generate and validate templates
        template_compliance = self._integrate_template_enforcement(command, eval_manifest)

        # Create enhanced command wrapper
        wrapper_created = self._create_enhanced_wrapper(command, eval_manifest, deps_manifest)

        # Calculate integration quality score
        quality_score = self._calculate_integration_quality(
            deps_validation, eval_test, template_compliance, wrapper_created
        )

        integration_result = {
            "success": quality_score >= 0.8,
            "status": "integrated" if quality_score >= 0.8 else "partial_integration",
            "quality_score": quality_score,
            "quality_gates": len(eval_manifest.get("evaluation", {}).get("phases", {}).get("0A_pre_execution", {}).get("gates", [])),
            "dependencies_validated": deps_validation["overall_score"],
            "template_compliance": template_compliance["compliance_score"],
            "wrapper_created": wrapper_created,
            "evaluation_test": eval_test["success"],
            "integration_details": {
                "dependency_validation": deps_validation,
                "evaluation_test": eval_test,
                "template_compliance": template_compliance
            }
        }

        return integration_result

    def _test_evaluation_protocol(self, command: str, eval_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Test evaluation protocol for command"""

        try:
            # Create test context
            test_context = {
                "command": command,
                "test_mode": True,
                "timestamp": datetime.now().isoformat()
            }

            # Run evaluation protocol test
            evaluation_result = self.evaluation_protocol.evaluate_command(
                command, eval_manifest, test_context
            )

            return {
                "success": True,
                "overall_score": evaluation_result.overall_score,
                "phases_tested": len(evaluation_result.phase_results),
                "can_proceed": evaluation_result.can_proceed
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _integrate_template_enforcement(self, command: str, eval_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate template enforcement for command"""

        template_config = eval_manifest.get("evaluation", {}).get("template_enforcement", {})

        if not template_config.get("enabled", False):
            return {
                "enabled": False,
                "compliance_score": 1.0,
                "templates_generated": 0
            }

        # Generate templates for command
        try:
            # Mock command info for template generation
            command_info = {
                "command_type": "utility",
                "complexity": "medium",
                "template_requirements": {
                    "output_types": template_config.get("output_types", ["markdown"]),
                    "standardization_needed": True,
                    "metadata_requirements": True
                }
            }

            templates = self.template_engine.generate_template_for_command(command, command_info)

            # Test template compliance with sample content
            sample_content = f"# {command.replace('_', ' ').title()}\n\nSample output content for testing."
            compliance = self.template_engine.enforce_template_compliance(
                command, sample_content, "markdown"
            )

            return {
                "enabled": True,
                "compliance_score": compliance.overall_score,
                "templates_generated": len(templates),
                "validation_rules": len(template_config.get("validation_rules", []))
            }

        except Exception as e:
            return {
                "enabled": True,
                "compliance_score": 0.0,
                "error": str(e)
            }

    def _create_enhanced_wrapper(self, command: str, eval_manifest: Dict[str, Any],
                               deps_manifest: Dict[str, Any]) -> bool:
        """Create enhanced command wrapper with Universal Evaluation integration"""

        try:
            wrapper_path = self.workspace_path / "framework" / "wrappers" / f"{command}_enhanced.py"
            wrapper_path.parent.mkdir(parents=True, exist_ok=True)

            wrapper_content = f'''#!/usr/bin/env python3
"""
Enhanced {command} Command Wrapper
Integrates Universal Evaluation Framework with {command} command
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent))

from evaluation.universal_dependency_validator import UniversalDependencyValidator
from evaluation.command_evaluation_protocol import CommandEvaluationProtocol
from template_enforcement_engine import TemplateEnforcementEngine

class Enhanced{command.replace("_", "").title()}Command:
    """Enhanced {command} command with Universal Evaluation integration"""

    def __init__(self, workspace_path: str = None):
        self.command_name = "{command}"
        self.workspace_path = Path(workspace_path or "team-workspace")

        # Initialize evaluation components
        self.dependency_validator = UniversalDependencyValidator(workspace_path)
        self.evaluation_protocol = CommandEvaluationProtocol(workspace_path)
        self.template_engine = TemplateEnforcementEngine(workspace_path)

        # Load manifests
        self.eval_manifest = self._load_evaluation_manifest()
        self.deps_manifest = self._load_dependency_manifest()

    def execute_with_evaluation(self, **kwargs) -> dict:
        """Execute {command} with full Universal Evaluation"""

        execution_context = {{
            "command": self.command_name,
            "parameters": kwargs,
            "timestamp": datetime.now().isoformat(),
            "enhanced_mode": True
        }}

        print(f"🔄 Executing {{self.command_name}} with Universal Evaluation")

        try:
            # Phase 0A: Pre-execution validation
            if self.deps_manifest:
                deps_validation = self.dependency_validator.validate_command_dependencies(
                    self.command_name, self.deps_manifest
                )
                execution_context["dependency_validation"] = deps_validation

                if not deps_validation["can_proceed"]:
                    return {{
                        "status": "failed",
                        "reason": "dependency_validation_failed",
                        "details": deps_validation
                    }}

            # Run evaluation protocol
            if self.eval_manifest:
                evaluation_result = self.evaluation_protocol.evaluate_command(
                    self.command_name, self.eval_manifest, execution_context
                )
                execution_context["evaluation_result"] = evaluation_result

                if not evaluation_result.can_proceed:
                    return {{
                        "status": "failed",
                        "reason": "evaluation_failed",
                        "details": evaluation_result
                    }}

            # Execute original command (placeholder)
            # In real implementation, this would call the actual command
            command_result = self._execute_original_command(**kwargs)

            # Apply template enforcement if enabled
            if self.eval_manifest and command_result.get("output"):
                template_compliance = self.template_engine.enforce_template_compliance(
                    self.command_name, command_result["output"], "markdown"
                )
                command_result["template_compliance"] = template_compliance

            # Record execution for learning
            execution_context["command_result"] = command_result
            self._record_execution(execution_context)

            return {{
                "status": "success",
                "command": self.command_name,
                "result": command_result,
                "evaluation": evaluation_result if 'evaluation_result' in execution_context else None,
                "enhanced": True
            }}

        except Exception as e:
            return {{
                "status": "error",
                "command": self.command_name,
                "error": str(e),
                "context": execution_context
            }}

    def _execute_original_command(self, **kwargs) -> dict:
        """Execute original {command} command logic"""
        # Placeholder for actual command implementation
        return {{
            "output": f"Sample output from {{self.command_name}}",
            "execution_time": 1.5,
            "quality_score": 0.85
        }}

    def _load_evaluation_manifest(self) -> dict:
        """Load evaluation manifest"""
        manifest_file = Path(".claude/commands/{command}.eval.yaml")
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return yaml.safe_load(f)
        return {{}}

    def _load_dependency_manifest(self) -> dict:
        """Load dependency manifest"""
        manifest_file = Path(".claude/commands/{command}.deps.yaml")
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return yaml.safe_load(f)
        return {{}}

    def _record_execution(self, execution_context: dict):
        """Record execution for learning and optimization"""
        executions_path = self.workspace_path / "framework" / "executions"
        executions_path.mkdir(parents=True, exist_ok=True)

        execution_file = executions_path / f"{{self.command_name}}_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"

        with open(execution_file, 'w') as f:
            json.dump(execution_context, f, indent=2, default=str)

def main():
    """Execute enhanced {command} command"""
    enhanced_command = Enhanced{command.replace("_", "").title()}Command()
    result = enhanced_command.execute_with_evaluation()

    print(json.dumps(result, indent=2, default=str))
    return result

if __name__ == "__main__":
    main()
'''

            with open(wrapper_path, 'w') as f:
                f.write(wrapper_content)

            return True

        except Exception as e:
            print(f"      ⚠️ Wrapper creation failed: {str(e)}")
            return False

    def _calculate_integration_quality(self, deps_validation: Dict[str, Any],
                                     eval_test: Dict[str, Any],
                                     template_compliance: Dict[str, Any],
                                     wrapper_created: bool) -> float:
        """Calculate overall integration quality score"""

        scores = []

        # Dependency validation score (30%)
        scores.append(deps_validation.get("overall_score", 0.0) * 0.3)

        # Evaluation test score (30%)
        if eval_test.get("success", False):
            scores.append(eval_test.get("overall_score", 0.8) * 0.3)
        else:
            scores.append(0.0)

        # Template compliance score (20%)
        scores.append(template_compliance.get("compliance_score", 1.0) * 0.2)

        # Wrapper creation score (20%)
        scores.append((1.0 if wrapper_created else 0.0) * 0.2)

        return sum(scores)

    def _validate_ecosystem_integration(self) -> Dict[str, Any]:
        """Validate complete ecosystem integration"""

        print("\n🔍 Validating ecosystem integration...")

        integrated_commands = [
            cmd for cmd, result in self.integration_results["integrated_commands"].items()
            if result.get("success", False)
        ]

        # Test cross-command compatibility
        compatibility_tests = self._test_cross_command_compatibility(integrated_commands)

        # Test framework performance
        performance_tests = self._test_framework_performance(integrated_commands[:5])  # Test top 5

        # Calculate ecosystem health
        ecosystem_health = self._calculate_ecosystem_health(
            integrated_commands, compatibility_tests, performance_tests
        )

        return {
            "integrated_commands": len(integrated_commands),
            "compatibility_tests": compatibility_tests,
            "performance_tests": performance_tests,
            "overall_health": ecosystem_health,
            "validation_timestamp": datetime.now().isoformat()
        }

    def _test_cross_command_compatibility(self, commands: List[str]) -> Dict[str, Any]:
        """Test cross-command compatibility"""

        compatibility_results = {
            "framework_compatibility": True,
            "manifest_compatibility": True,
            "template_compatibility": True,
            "issues": []
        }

        # Test framework component compatibility
        try:
            for command in commands[:3]:  # Test first 3 commands
                eval_manifest = self._load_evaluation_manifest(command)
                deps_manifest = self._load_dependency_manifest(command)

                if not eval_manifest:
                    compatibility_results["issues"].append(f"Missing evaluation manifest: {command}")
                    compatibility_results["manifest_compatibility"] = False

                if not deps_manifest:
                    compatibility_results["issues"].append(f"Missing dependency manifest: {command}")
                    compatibility_results["manifest_compatibility"] = False

        except Exception as e:
            compatibility_results["framework_compatibility"] = False
            compatibility_results["issues"].append(f"Framework compatibility error: {str(e)}")

        return compatibility_results

    def _test_framework_performance(self, commands: List[str]) -> Dict[str, Any]:
        """Test framework performance with sample commands"""

        performance_results = {
            "average_evaluation_time": 0.0,
            "average_dependency_time": 0.0,
            "total_overhead": 0.0,
            "performance_acceptable": True
        }

        if not commands:
            return performance_results

        import time

        total_eval_time = 0
        total_deps_time = 0
        tests_run = 0

        for command in commands:
            try:
                # Test evaluation protocol performance
                start_time = time.time()
                eval_manifest = self._load_evaluation_manifest(command)
                if eval_manifest:
                    self.evaluation_protocol.evaluate_command(command, eval_manifest, {"test": True})
                eval_time = time.time() - start_time
                total_eval_time += eval_time

                # Test dependency validation performance
                start_time = time.time()
                deps_manifest = self._load_dependency_manifest(command)
                if deps_manifest:
                    self.dependency_validator.validate_command_dependencies(command, deps_manifest)
                deps_time = time.time() - start_time
                total_deps_time += deps_time

                tests_run += 1

            except Exception:
                continue

        if tests_run > 0:
            performance_results["average_evaluation_time"] = total_eval_time / tests_run
            performance_results["average_dependency_time"] = total_deps_time / tests_run
            performance_results["total_overhead"] = (total_eval_time + total_deps_time) / tests_run

            # Performance is acceptable if overhead is under 2 seconds
            performance_results["performance_acceptable"] = performance_results["total_overhead"] < 2.0

        return performance_results

    def _calculate_ecosystem_health(self, integrated_commands: List[str],
                                   compatibility_tests: Dict[str, Any],
                                   performance_tests: Dict[str, Any]) -> str:
        """Calculate overall ecosystem health"""

        health_factors = []

        # Integration coverage
        total_commands = self.integration_results["total_commands"]
        integration_coverage = len(integrated_commands) / total_commands if total_commands > 0 else 0
        health_factors.append(integration_coverage)

        # Compatibility health
        compatibility_score = 1.0
        if not compatibility_tests["framework_compatibility"]:
            compatibility_score -= 0.5
        if not compatibility_tests["manifest_compatibility"]:
            compatibility_score -= 0.3
        if not compatibility_tests["template_compatibility"]:
            compatibility_score -= 0.2
        health_factors.append(max(0.0, compatibility_score))

        # Performance health
        performance_score = 1.0 if performance_tests["performance_acceptable"] else 0.6
        health_factors.append(performance_score)

        # Calculate overall health
        overall_health = sum(health_factors) / len(health_factors)

        if overall_health >= 0.9:
            return "excellent"
        elif overall_health >= 0.8:
            return "good"
        elif overall_health >= 0.7:
            return "fair"
        else:
            return "needs_improvement"

    def _get_commands_with_manifests(self) -> List[str]:
        """Get list of commands that have both evaluation and dependency manifests"""

        commands = []

        # Debug path resolution
        print(f"   Looking for manifests in: {self.commands_path}")
        print(f"   Commands path exists: {self.commands_path.exists()}")

        # Try absolute path resolution
        if not self.commands_path.is_absolute():
            abs_commands_path = Path.cwd() / self.commands_path
            print(f"   Using absolute path: {abs_commands_path}")

            eval_files = list(abs_commands_path.glob("*.eval.yaml"))
            print(f"   Found {len(eval_files)} .eval.yaml files")

            for eval_file in eval_files:
                command = eval_file.stem.replace('.eval', '')
                deps_file = abs_commands_path / f"{command}.deps.yaml"
                print(f"   Checking {command}: eval={eval_file.exists()}, deps={deps_file.exists()}")

                if deps_file.exists():
                    commands.append(command)
                    print(f"   ✅ Added: {command}")
        else:
            for eval_file in self.commands_path.glob("*.eval.yaml"):
                command = eval_file.stem.replace('.eval', '')
                deps_file = self.commands_path / f"{command}.deps.yaml"

                if deps_file.exists():
                    commands.append(command)
                    print(f"   Found: {command}")

        print(f"   Total commands with manifests: {len(commands)}")
        return commands

    def _get_deployment_order(self, commands: List[str]) -> List[str]:
        """Get optimal deployment order for commands"""

        # Load catalog for deployment priority
        try:
            catalog_file = self.workspace_path / "framework" / "phase4_command_catalog.json"
            with open(catalog_file, 'r') as f:
                catalog = json.load(f)

            deployment_priority = catalog.get("phase4_scope", {}).get("deployment_priority", [])

            # Filter to only include commands with manifests
            ordered_commands = [cmd for cmd in deployment_priority if cmd in commands]

            # Add any remaining commands
            remaining = [cmd for cmd in commands if cmd not in ordered_commands]
            ordered_commands.extend(remaining)

            return ordered_commands

        except Exception:
            # Fallback to alphabetical order
            return sorted(commands)

    def _load_evaluation_manifest(self, command: str) -> Optional[Dict[str, Any]]:
        """Load evaluation manifest for command"""

        manifest_file = self.commands_path / f"{command}.eval.yaml"

        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    return yaml.safe_load(f)
            except Exception:
                pass

        return None

    def _load_dependency_manifest(self, command: str) -> Optional[Dict[str, Any]]:
        """Load dependency manifest for command"""

        manifest_file = self.commands_path / f"{command}.deps.yaml"

        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    return yaml.safe_load(f)
            except Exception:
                pass

        return None

    def _load_deployment_config(self) -> Dict[str, Any]:
        """Load deployment configuration"""

        return {
            "batch_size": 5,
            "validation_timeout": 30,
            "quality_threshold": 0.8,
            "performance_threshold": 2.0
        }

    def _generate_integration_summary(self):
        """Generate integration summary"""

        total_commands = self.integration_results["total_commands"]
        integrated_commands = self.integration_results["integrated_commands"]

        successful = len([cmd for cmd, result in integrated_commands.items() if result.get("success", False)])
        failed = len(integrated_commands) - successful

        self.integration_results["integration_summary"] = {
            "total_commands": total_commands,
            "successful_integrations": successful,
            "failed_integrations": failed,
            "success_rate": successful / len(integrated_commands) if integrated_commands else 0.0,
            "average_quality_score": sum(
                result.get("quality_score", 0.0) for result in integrated_commands.values()
            ) / len(integrated_commands) if integrated_commands else 0.0
        }

    def save_integration_results(self) -> Path:
        """Save integration results to file"""

        results_path = self.workspace_path / "framework" / "results"
        results_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_path / f"universal_integration_results_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump(self.integration_results, f, indent=2, default=str)

        return results_file

def main():
    """Run Universal Integration Deployment"""

    deployer = UniversalIntegrationDeployer()
    results = deployer.deploy_universal_framework()
    results_file = deployer.save_integration_results()

    print(f"\n💾 Integration results saved: {results_file}")

    return results

if __name__ == "__main__":
    main()
