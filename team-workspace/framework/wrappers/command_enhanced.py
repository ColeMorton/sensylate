#!/usr/bin/env python3
"""
Enhanced command Command Wrapper
Integrates Universal Evaluation Framework with command command
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

class EnhancedCommandCommand:
    """Enhanced command command with Universal Evaluation integration"""

    def __init__(self, workspace_path: str = None):
        self.command_name = "command"
        self.workspace_path = Path(workspace_path or "team-workspace")

        # Initialize evaluation components
        self.dependency_validator = UniversalDependencyValidator(workspace_path)
        self.evaluation_protocol = CommandEvaluationProtocol(workspace_path)
        self.template_engine = TemplateEnforcementEngine(workspace_path)

        # Load manifests
        self.eval_manifest = self._load_evaluation_manifest()
        self.deps_manifest = self._load_dependency_manifest()

    def execute_with_evaluation(self, **kwargs) -> dict:
        """Execute command with full Universal Evaluation"""

        execution_context = {
            "command": self.command_name,
            "parameters": kwargs,
            "timestamp": datetime.now().isoformat(),
            "enhanced_mode": True
        }

        print(f"🔄 Executing {self.command_name} with Universal Evaluation")

        try:
            # Phase 0A: Pre-execution validation
            if self.deps_manifest:
                deps_validation = self.dependency_validator.validate_command_dependencies(
                    self.command_name, self.deps_manifest
                )
                execution_context["dependency_validation"] = deps_validation

                if not deps_validation["can_proceed"]:
                    return {
                        "status": "failed",
                        "reason": "dependency_validation_failed",
                        "details": deps_validation
                    }

            # Run evaluation protocol
            if self.eval_manifest:
                evaluation_result = self.evaluation_protocol.evaluate_command(
                    self.command_name, self.eval_manifest, execution_context
                )
                execution_context["evaluation_result"] = evaluation_result

                if not evaluation_result.can_proceed:
                    return {
                        "status": "failed",
                        "reason": "evaluation_failed",
                        "details": evaluation_result
                    }

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

            return {
                "status": "success",
                "command": self.command_name,
                "result": command_result,
                "evaluation": evaluation_result if 'evaluation_result' in execution_context else None,
                "enhanced": True
            }

        except Exception as e:
            return {
                "status": "error",
                "command": self.command_name,
                "error": str(e),
                "context": execution_context
            }

    def _execute_original_command(self, **kwargs) -> dict:
        """Execute original command command logic"""
        # Placeholder for actual command implementation
        return {
            "output": f"Sample output from {self.command_name}",
            "execution_time": 1.5,
            "quality_score": 0.85
        }

    def _load_evaluation_manifest(self) -> dict:
        """Load evaluation manifest"""
        manifest_file = Path(".claude/commands/command.eval.yaml")
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _load_dependency_manifest(self) -> dict:
        """Load dependency manifest"""
        manifest_file = Path(".claude/commands/command.deps.yaml")
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _record_execution(self, execution_context: dict):
        """Record execution for learning and optimization"""
        executions_path = self.workspace_path / "framework" / "executions"
        executions_path.mkdir(parents=True, exist_ok=True)

        execution_file = executions_path / f"{self.command_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(execution_file, 'w') as f:
            json.dump(execution_context, f, indent=2, default=str)

def main():
    """Execute enhanced command command"""
    enhanced_command = EnhancedCommandCommand()
    result = enhanced_command.execute_with_evaluation()

    print(json.dumps(result, indent=2, default=str))
    return result

if __name__ == "__main__":
    main()
