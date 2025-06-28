#!/usr/bin/env python3
"""
Universal Evaluation Manifest Generator
Creates evaluation and dependency manifests for all Phase 4 commands
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class ManifestGenerator:
    """Generates evaluation and dependency manifests for commands"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.commands_path = Path(".claude/commands")

        # Load command catalog
        catalog_file = self.workspace_path / "framework" / "phase4_command_catalog.json"
        with open(catalog_file, 'r') as f:
            self.catalog = json.load(f)

    def generate_all_manifests(self) -> Dict[str, Any]:
        """Generate evaluation and dependency manifests for all remaining commands"""

        remaining_commands = self.catalog["remaining_commands"]
        deployment_order = self.catalog["phase4_scope"]["deployment_priority"]

        generation_results = {
            "timestamp": datetime.now().isoformat(),
            "commands_processed": 0,
            "evaluation_manifests": {},
            "dependency_manifests": {},
            "generation_summary": {}
        }

        print("🏭 GENERATING UNIVERSAL EVALUATION MANIFESTS")
        print("=" * 60)

        for cmd_name in deployment_order:
            if cmd_name not in remaining_commands:
                continue

            print(f"\n📝 Processing: {cmd_name}")
            cmd_info = remaining_commands[cmd_name]

            # Generate evaluation manifest
            eval_manifest = self._generate_evaluation_manifest(cmd_name, cmd_info)
            eval_file = self.commands_path / f"{cmd_name}.eval.yaml"

            with open(eval_file, 'w') as f:
                yaml.dump(eval_manifest, f, indent=2, default_flow_style=False)

            generation_results["evaluation_manifests"][cmd_name] = str(eval_file)
            print(f"   ✅ Evaluation manifest: {eval_file.name}")

            # Generate dependency manifest
            deps_manifest = self._generate_dependency_manifest(cmd_name, cmd_info)
            deps_file = self.commands_path / f"{cmd_name}.deps.yaml"

            with open(deps_file, 'w') as f:
                yaml.dump(deps_manifest, f, indent=2, default_flow_style=False)

            generation_results["dependency_manifests"][cmd_name] = str(deps_file)
            print(f"   ✅ Dependency manifest: {deps_file.name}")

            # Summary
            generation_results["generation_summary"][cmd_name] = {
                "complexity": cmd_info["complexity"],
                "command_type": cmd_info["command_type"],
                "quality_gates": len(eval_manifest["evaluation"]["phases"]["0A_pre_execution"]["gates"]),
                "dependencies": len(deps_manifest["dependencies"]),
                "template_enforcement": eval_manifest["evaluation"]["template_enforcement"]["enabled"]
            }

            generation_results["commands_processed"] += 1

        return generation_results

    def _generate_evaluation_manifest(self, cmd_name: str, cmd_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate evaluation manifest for command"""

        complexity = cmd_info["complexity"]
        cmd_type = cmd_info["command_type"]
        eval_requirements = cmd_info["evaluation_requirements"]

        # Base manifest structure
        manifest = {
            "version": "1.0",
            "command": cmd_name,
            "description": f"Universal Evaluation manifest for {cmd_name} command",
            "created_at": datetime.now().isoformat(),
            "evaluation": {
                "phases": {
                    "0A_pre_execution": {
                        "gates": self._generate_quality_gates(cmd_name, cmd_info),
                        "enhancement_detection": {
                            "enabled": True,
                            "file_patterns": [f"*_evaluation.md", f"{cmd_name}_*_evaluation.md"],
                            "role_transformation": f"{cmd_type} specialist → optimization specialist"
                        }
                    },
                    "0B_execution_monitoring": {
                        "gates": self._generate_monitoring_gates(cmd_name, cmd_info)
                    },
                    "0C_post_execution": {
                        "gates": self._generate_validation_gates(cmd_name, cmd_info)
                    },
                    "0D_feedback_integration": {
                        "gates": self._generate_feedback_gates(cmd_name, cmd_info)
                    }
                },
                "quality_targets": self._generate_quality_targets(cmd_name, cmd_info),
                "template_enforcement": self._generate_template_enforcement(cmd_name, cmd_info),
                "orchestration_integration": {
                    "smart_suggestions": True,
                    "automation_eligible": complexity in ["low", "medium"],
                    "preference_learning": True
                }
            }
        }

        return manifest

    def _generate_quality_gates(self, cmd_name: str, cmd_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Phase 0A quality gates"""

        gates = []

        # Always include input validation
        gates.append({
            "name": "input_validation",
            "description": "Validate command input parameters and context",
            "threshold": 1.0,
            "critical": True,
            "adaptive": False
        })

        # Dependency validation if needed
        if cmd_info["dependencies"]:
            gates.append({
                "name": "dependency_validation",
                "description": "Validate external dependencies and data sources",
                "threshold": 0.95,
                "critical": True,
                "adaptive": False
            })

        # Enhancement detection (Phase 0A compatibility)
        gates.append({
            "name": "enhancement_detection",
            "description": "Detect evaluation files for Phase 0A enhancement mode",
            "threshold": 0.6,
            "critical": False,
            "adaptive": False
        })

        # Historical performance check
        gates.append({
            "name": "historical_performance",
            "description": "Check historical command performance metrics",
            "threshold": 0.7,
            "critical": False,
            "adaptive": True
        })

        # Command-specific gates based on type
        if cmd_info["command_type"] == "analysis":
            gates.append({
                "name": "data_quality_check",
                "description": "Validate input data quality and completeness",
                "threshold": 0.85,
                "critical": True,
                "adaptive": False
            })

        if cmd_info["command_type"] == "content":
            gates.append({
                "name": "content_validation",
                "description": "Validate content structure and formatting requirements",
                "threshold": 0.9,
                "critical": False,
                "adaptive": True
            })

        if cmd_info["command_type"] == "trading":
            gates.append({
                "name": "market_data_validation",
                "description": "Validate market data currency and accuracy",
                "threshold": 0.95,
                "critical": True,
                "adaptive": False
            })

        return gates

    def _generate_monitoring_gates(self, cmd_name: str, cmd_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Phase 0B monitoring gates"""

        gates = [
            {
                "name": "execution_progress",
                "description": "Monitor command execution progress and milestones",
                "threshold": 0.8,
                "critical": False,
                "adaptive": True
            },
            {
                "name": "resource_monitoring",
                "description": "Monitor system resource usage during execution",
                "threshold": 0.9,
                "critical": False,
                "adaptive": True
            }
        ]

        # Add performance monitoring for complex commands
        if cmd_info["complexity"] in ["medium", "high"]:
            gates.append({
                "name": "performance_monitoring",
                "description": "Monitor execution time and efficiency metrics",
                "threshold": 0.8,
                "critical": False,
                "adaptive": True
            })

        return gates

    def _generate_validation_gates(self, cmd_name: str, cmd_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Phase 0C validation gates"""

        gates = [
            {
                "name": "output_validation",
                "description": "Validate command output format and completeness",
                "threshold": 0.9,
                "critical": True,
                "adaptive": False
            },
            {
                "name": "quality_scoring",
                "description": "Score output quality against command standards",
                "threshold": 0.8,
                "critical": False,
                "adaptive": True
            }
        ]

        # Add confidence scoring for analysis commands
        if cmd_info["command_type"] == "analysis":
            gates.append({
                "name": "confidence_scoring",
                "description": "Calculate confidence score for analysis results",
                "threshold": 0.7,
                "critical": False,
                "adaptive": True
            })

        # Add compliance checking for content commands
        if cmd_info["command_type"] == "content":
            gates.append({
                "name": "compliance_checking",
                "description": "Verify content compliance with platform requirements",
                "threshold": 1.0,
                "critical": True,
                "adaptive": False
            })

        return gates

    def _generate_feedback_gates(self, cmd_name: str, cmd_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Phase 0D feedback gates"""

        gates = [
            {
                "name": "learning_integration",
                "description": "Integrate execution results into learning systems",
                "threshold": 0.8,
                "critical": False,
                "adaptive": True
            },
            {
                "name": "performance_metrics",
                "description": "Record performance metrics for optimization",
                "threshold": 0.9,
                "critical": False,
                "adaptive": False
            }
        ]

        # Add optimization recommendations for complex commands
        if cmd_info["complexity"] == "high":
            gates.append({
                "name": "optimization_recommendations",
                "description": "Generate optimization recommendations for future executions",
                "threshold": 0.7,
                "critical": False,
                "adaptive": True
            })

        return gates

    def _generate_quality_targets(self, cmd_name: str, cmd_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quality targets based on command characteristics"""

        base_targets = {
            "overall_threshold": 0.8,
            "critical_gate_threshold": 0.95,
            "performance_target": 0.85
        }

        # Adjust targets based on complexity
        if cmd_info["complexity"] == "high":
            base_targets.update({
                "overall_threshold": 0.85,
                "confidence_target": 0.9,
                "institutional_quality": True
            })
        elif cmd_info["complexity"] == "low":
            base_targets.update({
                "overall_threshold": 0.75,
                "fast_execution": True
            })

        # Command type specific targets
        if cmd_info["command_type"] == "analysis":
            base_targets["confidence_target"] = 0.9
            base_targets["data_quality_target"] = 0.95
        elif cmd_info["command_type"] == "content":
            base_targets["engagement_target"] = 0.8
            base_targets["compliance_target"] = 1.0
        elif cmd_info["command_type"] == "trading":
            base_targets["accuracy_target"] = 0.98
            base_targets["real_time_performance"] = True

        return base_targets

    def _generate_template_enforcement(self, cmd_name: str, cmd_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate template enforcement configuration"""

        template_requirements = cmd_info["template_requirements"]

        enforcement = {
            "enabled": template_requirements["standardization_needed"],
            "strictness": "medium",
            "output_types": template_requirements["output_types"],
            "validation_rules": []
        }

        # Add validation rules based on output types
        for output_type in template_requirements["output_types"]:
            if output_type == "markdown":
                enforcement["validation_rules"].append({
                    "type": "markdown_structure",
                    "description": "Enforce markdown heading structure and formatting",
                    "required": True
                })
            elif output_type == "json":
                enforcement["validation_rules"].append({
                    "type": "json_schema",
                    "description": "Validate JSON output against schema",
                    "required": True
                })
            elif output_type == "report":
                enforcement["validation_rules"].append({
                    "type": "report_template",
                    "description": "Enforce report template structure",
                    "required": True
                })

        # Metadata requirements
        if template_requirements["metadata_requirements"]:
            enforcement["validation_rules"].append({
                "type": "metadata_headers",
                "description": "Require standard metadata headers",
                "required": True
            })

        return enforcement

    def _generate_dependency_manifest(self, cmd_name: str, cmd_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate dependency manifest for command"""

        manifest = {
            "version": "1.0",
            "command": cmd_name,
            "description": f"Dependency manifest for {cmd_name} command",
            "created_at": datetime.now().isoformat(),
            "dependencies": {}
        }

        # Add dependencies based on command analysis
        dependencies = cmd_info["dependencies"]

        if "data_sources" in dependencies:
            manifest["dependencies"]["market_data_api"] = {
                "type": "api",
                "required": True,
                "description": "Market data API access",
                "validation": {
                    "endpoint_check": True,
                    "rate_limit_check": True,
                    "data_freshness": True
                },
                "fallback_strategies": [
                    {
                        "strategy": "cached_data",
                        "description": "Use cached data if API unavailable",
                        "max_age_hours": 4
                    },
                    {
                        "strategy": "alternative_source",
                        "description": "Use alternative data source",
                        "source": "backup_api"
                    }
                ]
            }

        if "file_systems" in dependencies:
            manifest["dependencies"]["file_system"] = {
                "type": "file_system",
                "required": True,
                "description": "File system access for input/output operations",
                "validation": {
                    "directory_access": True,
                    "write_permissions": True,
                    "disk_space": True
                },
                "fallback_strategies": [
                    {
                        "strategy": "temporary_storage",
                        "description": "Use temporary storage if primary unavailable",
                        "cleanup_policy": "auto"
                    }
                ]
            }

        if "services" in dependencies:
            manifest["dependencies"]["external_services"] = {
                "type": "service",
                "required": False,
                "description": "External service integrations",
                "validation": {
                    "service_health": True,
                    "authentication": True
                },
                "fallback_strategies": [
                    {
                        "strategy": "degraded_mode",
                        "description": "Continue with reduced functionality",
                        "impact": "minor"
                    }
                ]
            }

        if "other_commands" in dependencies:
            manifest["dependencies"]["command_ecosystem"] = {
                "type": "internal",
                "required": False,
                "description": "Other commands in the ecosystem",
                "validation": {
                    "command_availability": True,
                    "version_compatibility": True
                },
                "fallback_strategies": [
                    {
                        "strategy": "manual_mode",
                        "description": "Request manual input if commands unavailable",
                        "user_prompt": True
                    }
                ]
            }

        # Add universal dependencies
        manifest["dependencies"]["team_workspace"] = {
            "type": "internal",
            "required": True,
            "description": "Team workspace infrastructure",
            "validation": {
                "workspace_access": True,
                "knowledge_authority": True
            },
            "fallback_strategies": [
                {
                    "strategy": "local_mode",
                    "description": "Use local storage if workspace unavailable",
                    "sync_when_available": True
                }
            ]
        }

        return manifest

def main():
    """Generate all manifests for Phase 4 commands"""

    generator = ManifestGenerator()
    results = generator.generate_all_manifests()

    print(f"\n📊 MANIFEST GENERATION SUMMARY:")
    print(f"Commands Processed: {results['commands_processed']}")
    print(f"Evaluation Manifests: {len(results['evaluation_manifests'])}")
    print(f"Dependency Manifests: {len(results['dependency_manifests'])}")

    print(f"\n🎯 QUALITY GATE SUMMARY:")
    for cmd_name, summary in results['generation_summary'].items():
        print(f"   {cmd_name}: {summary['quality_gates']} gates, {summary['dependencies']} dependencies")

    # Save results
    results_file = Path("team-workspace/framework/manifest_generation_results.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Results saved: {results_file}")

    return results

if __name__ == "__main__":
    main()
