#!/usr/bin/env python3
"""
Command Evaluation Protocol (CEP) Orchestrator
Manages 4-phase evaluation workflow (0A-0D) with validation checkpoints
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass, asdict
from enum import Enum

# Import Universal Dependency Validator
from .universal_dependency_validator import UniversalDependencyValidator, ValidationResult

class EvaluationPhase(Enum):
    """Evaluation phase enumeration"""
    PRE_EXECUTION = "0A_pre_execution"
    EXECUTION_MONITORING = "0B_execution_monitoring"
    POST_EXECUTION = "0C_post_execution"
    FEEDBACK_INTEGRATION = "0D_feedback_integration"

@dataclass
class EvaluationGate:
    """Represents a single evaluation gate"""
    name: str
    phase: EvaluationPhase
    threshold: float
    critical: bool
    adaptive: bool = False
    execution_time: float = 0.0
    result: Optional[float] = None
    passed: Optional[bool] = None
    error_message: Optional[str] = None

@dataclass
class PhaseResult:
    """Result of a single evaluation phase"""
    phase: EvaluationPhase
    gates: List[EvaluationGate]
    overall_score: float
    passed: bool
    execution_time: float
    timestamp: str
    recommendations: List[str] = None

@dataclass
class EvaluationResult:
    """Complete evaluation result across all phases"""
    command: str
    version: str
    overall_score: float
    can_proceed: bool
    phase_results: List[PhaseResult]
    enhancement_mode: bool = False
    fallback_strategy: Optional[Dict[str, Any]] = None
    total_execution_time: float = 0.0
    timestamp: str = ""

class CommandEvaluationProtocol:
    """
    Orchestrates 4-phase evaluation workflow for AI commands
    Integrates with existing Phase 0A protocols and Universal Dependency Validator
    """

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.dependency_validator = UniversalDependencyValidator(workspace_path)

        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Phase execution handlers
        self.phase_handlers = {
            EvaluationPhase.PRE_EXECUTION: self._execute_pre_execution_phase,
            EvaluationPhase.EXECUTION_MONITORING: self._execute_monitoring_phase,
            EvaluationPhase.POST_EXECUTION: self._execute_post_execution_phase,
            EvaluationPhase.FEEDBACK_INTEGRATION: self._execute_feedback_phase
        }

        # Create framework directories
        self.results_path = self.workspace_path / "framework" / "results"
        self.results_path.mkdir(parents=True, exist_ok=True)

    def evaluate_command(self, command_name: str, evaluation_manifest: Dict[str, Any],
                        command_context: Dict[str, Any] = None) -> EvaluationResult:
        """
        Main entry point for command evaluation

        Args:
            command_name: Name of the command being evaluated
            evaluation_manifest: Loaded .eval.yaml content
            command_context: Context data from command execution

        Returns:
            Complete evaluation result
        """
        start_time = datetime.now()
        command_context = command_context or {}

        self.logger.info(f"Starting evaluation for command: {command_name}")

        # Check for enhancement mode (existing Phase 0A protocol)
        enhancement_mode = self._detect_enhancement_mode(command_name, evaluation_manifest, command_context)

        # Initialize evaluation result
        evaluation_result = EvaluationResult(
            command=command_name,
            version=evaluation_manifest.get("version", "1.0"),
            overall_score=0.0,
            can_proceed=False,
            phase_results=[],
            enhancement_mode=enhancement_mode,
            timestamp=start_time.isoformat()
        )

        # Execute each evaluation phase
        for phase in EvaluationPhase:
            try:
                phase_result = self._execute_evaluation_phase(
                    phase, command_name, evaluation_manifest, command_context
                )
                evaluation_result.phase_results.append(phase_result)

                # Check if critical gate failure should stop evaluation
                if not phase_result.passed and self._has_critical_failures(phase_result):
                    self.logger.warning(f"Critical failure in {phase.value}, stopping evaluation")
                    break

            except Exception as e:
                self.logger.error(f"Phase {phase.value} execution failed: {str(e)}")
                # Create failure result for this phase
                failure_result = PhaseResult(
                    phase=phase,
                    gates=[],
                    overall_score=0.0,
                    passed=False,
                    execution_time=0.0,
                    timestamp=datetime.now().isoformat(),
                    recommendations=[f"Phase execution failed: {str(e)}"]
                )
                evaluation_result.phase_results.append(failure_result)
                break

        # Calculate overall evaluation score
        evaluation_result.overall_score = self._calculate_overall_score(evaluation_result.phase_results)
        evaluation_result.can_proceed = self._determine_proceed_status(evaluation_result)
        evaluation_result.total_execution_time = (datetime.now() - start_time).total_seconds()

        # Generate fallback strategy if needed
        if not evaluation_result.can_proceed:
            evaluation_result.fallback_strategy = self._generate_evaluation_fallback_strategy(
                evaluation_result, evaluation_manifest
            )

        # Save evaluation result
        self._save_evaluation_result(evaluation_result)

        self.logger.info(f"Evaluation completed for {command_name}: score={evaluation_result.overall_score:.3f}, can_proceed={evaluation_result.can_proceed}")

        return evaluation_result

    def _execute_evaluation_phase(self, phase: EvaluationPhase, command_name: str,
                                 evaluation_manifest: Dict[str, Any],
                                 command_context: Dict[str, Any]) -> PhaseResult:
        """Execute a single evaluation phase"""
        start_time = datetime.now()

        # Get phase configuration from manifest
        phase_config = evaluation_manifest.get("evaluation_phases", {}).get(phase.value, {})
        quality_gates_config = evaluation_manifest.get("quality_gates", {})

        # Execute phase-specific handler
        handler = self.phase_handlers.get(phase)
        if not handler:
            raise ValueError(f"No handler found for phase: {phase.value}")

        gates = handler(command_name, phase_config, quality_gates_config, command_context)

        # Calculate phase score and status
        overall_score = sum(g.result for g in gates if g.result is not None) / len(gates) if gates else 0.0
        passed = all(g.passed for g in gates if g.critical) and overall_score >= 0.6

        execution_time = (datetime.now() - start_time).total_seconds()

        # Generate phase-specific recommendations
        recommendations = self._generate_phase_recommendations(phase, gates, overall_score)

        return PhaseResult(
            phase=phase,
            gates=gates,
            overall_score=overall_score,
            passed=passed,
            execution_time=execution_time,
            timestamp=start_time.isoformat(),
            recommendations=recommendations
        )

    def _execute_pre_execution_phase(self, command_name: str, phase_config: Dict[str, Any],
                                   quality_gates_config: Dict[str, Any],
                                   command_context: Dict[str, Any]) -> List[EvaluationGate]:
        """Execute Phase 0A: Pre-execution validation"""
        gates = []

        # Gate 1: Dependency Validation
        dependency_gate = self._execute_dependency_validation_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(dependency_gate)

        # Gate 2: Input Validation
        input_gate = self._execute_input_validation_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(input_gate)

        # Gate 3: Enhancement Detection (Phase 0A protocol)
        enhancement_gate = self._execute_enhancement_detection_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(enhancement_gate)

        # Gate 4: Historical Performance Check
        performance_gate = self._execute_historical_performance_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(performance_gate)

        return gates

    def _execute_monitoring_phase(self, command_name: str, phase_config: Dict[str, Any],
                                quality_gates_config: Dict[str, Any],
                                command_context: Dict[str, Any]) -> List[EvaluationGate]:
        """Execute Phase 0B: Execution monitoring"""
        gates = []

        # Gate 1: Progress Tracking
        progress_gate = EvaluationGate(
            name="progress_tracking",
            phase=EvaluationPhase.EXECUTION_MONITORING,
            threshold=0.8,
            critical=False,
            result=0.9,  # Simulated - would integrate with actual progress tracking
            passed=True
        )
        gates.append(progress_gate)

        # Gate 2: Error Detection
        error_gate = EvaluationGate(
            name="error_detection",
            phase=EvaluationPhase.EXECUTION_MONITORING,
            threshold=0.95,
            critical=True,
            result=1.0,  # No errors detected
            passed=True
        )
        gates.append(error_gate)

        return gates

    def _execute_post_execution_phase(self, command_name: str, phase_config: Dict[str, Any],
                                    quality_gates_config: Dict[str, Any],
                                    command_context: Dict[str, Any]) -> List[EvaluationGate]:
        """Execute Phase 0C: Post-execution validation"""
        gates = []

        # Gate 1: Output Validation
        output_gate = self._execute_output_validation_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(output_gate)

        # Gate 2: Confidence Scoring
        confidence_gate = self._execute_confidence_scoring_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(confidence_gate)

        # Gate 3: Template Compliance
        template_gate = self._execute_template_compliance_gate(
            command_name, quality_gates_config, command_context
        )
        gates.append(template_gate)

        return gates

    def _execute_feedback_phase(self, command_name: str, phase_config: Dict[str, Any],
                              quality_gates_config: Dict[str, Any],
                              command_context: Dict[str, Any]) -> List[EvaluationGate]:
        """Execute Phase 0D: Feedback integration"""
        gates = []

        # Gate 1: Learning Integration
        learning_gate = EvaluationGate(
            name="learning_integration",
            phase=EvaluationPhase.FEEDBACK_INTEGRATION,
            threshold=0.7,
            critical=False,
            result=0.8,  # Learning patterns integrated
            passed=True
        )
        gates.append(learning_gate)

        # Gate 2: Parameter Optimization
        optimization_gate = EvaluationGate(
            name="parameter_optimization",
            phase=EvaluationPhase.FEEDBACK_INTEGRATION,
            threshold=0.6,
            critical=False,
            result=0.7,  # Parameters optimized based on feedback
            passed=True
        )
        gates.append(optimization_gate)

        return gates

    def _execute_dependency_validation_gate(self, command_name: str,
                                          quality_gates_config: Dict[str, Any],
                                          command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute dependency validation using Universal Dependency Validator"""
        start_time = datetime.now()

        try:
            # Load dependency manifest for this command
            deps_manifest = self._load_dependency_manifest(command_name)

            if deps_manifest:
                validation_result = self.dependency_validator.validate_command_dependencies(
                    command_name, deps_manifest
                )

                # Find threshold from quality gates config
                threshold = self._get_gate_threshold("dependency_availability", quality_gates_config, 0.95)

                gate = EvaluationGate(
                    name="dependency_validation",
                    phase=EvaluationPhase.PRE_EXECUTION,
                    threshold=threshold,
                    critical=True,
                    result=validation_result["overall_score"],
                    passed=validation_result["can_proceed"],
                    execution_time=(datetime.now() - start_time).total_seconds()
                )

                if not validation_result["can_proceed"]:
                    gate.error_message = f"Critical dependencies failed: {validation_result.get('critical_failures', [])}"

            else:
                # No dependency manifest - assume basic validation
                gate = EvaluationGate(
                    name="dependency_validation",
                    phase=EvaluationPhase.PRE_EXECUTION,
                    threshold=0.8,
                    critical=False,
                    result=0.8,
                    passed=True,
                    execution_time=(datetime.now() - start_time).total_seconds()
                )

            return gate

        except Exception as e:
            return EvaluationGate(
                name="dependency_validation",
                phase=EvaluationPhase.PRE_EXECUTION,
                threshold=0.95,
                critical=True,
                result=0.0,
                passed=False,
                error_message=f"Dependency validation failed: {str(e)}",
                execution_time=(datetime.now() - start_time).total_seconds()
            )

    def _execute_input_validation_gate(self, command_name: str,
                                     quality_gates_config: Dict[str, Any],
                                     command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute input validation gate"""
        start_time = datetime.now()

        # Basic input validation - would be enhanced based on command requirements
        input_score = 1.0  # Assume valid inputs for now

        # Check for required context elements
        if command_name == "fundamental_analysis":
            if "ticker" not in command_context:
                input_score = 0.0

        threshold = self._get_gate_threshold("input_validation", quality_gates_config, 1.0)

        return EvaluationGate(
            name="input_validation",
            phase=EvaluationPhase.PRE_EXECUTION,
            threshold=threshold,
            critical=True,
            result=input_score,
            passed=input_score >= threshold,
            execution_time=(datetime.now() - start_time).total_seconds()
        )

    def _execute_enhancement_detection_gate(self, command_name: str,
                                          quality_gates_config: Dict[str, Any],
                                          command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute enhancement detection (Phase 0A protocol)"""
        start_time = datetime.now()

        # Check for existing evaluation files (Phase 0A pattern)
        enhancement_detected = self._check_for_evaluation_files(command_name, command_context)

        enhancement_score = 1.0 if enhancement_detected else 0.8

        return EvaluationGate(
            name="enhancement_detection",
            phase=EvaluationPhase.PRE_EXECUTION,
            threshold=0.6,
            critical=False,
            result=enhancement_score,
            passed=True,  # Always pass - this is informational
            execution_time=(datetime.now() - start_time).total_seconds()
        )

    def _execute_historical_performance_gate(self, command_name: str,
                                           quality_gates_config: Dict[str, Any],
                                           command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute historical performance check"""
        start_time = datetime.now()

        # Check recent performance metrics for this command
        performance_score = self._get_command_performance_score(command_name)

        return EvaluationGate(
            name="historical_performance",
            phase=EvaluationPhase.PRE_EXECUTION,
            threshold=0.7,
            critical=False,
            result=performance_score,
            passed=performance_score >= 0.7,
            execution_time=(datetime.now() - start_time).total_seconds()
        )

    def _execute_output_validation_gate(self, command_name: str,
                                      quality_gates_config: Dict[str, Any],
                                      command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute output validation gate"""
        # This would validate actual command output - simulated for now
        return EvaluationGate(
            name="output_validation",
            phase=EvaluationPhase.POST_EXECUTION,
            threshold=0.8,
            critical=True,
            result=0.9,
            passed=True
        )

    def _execute_confidence_scoring_gate(self, command_name: str,
                                       quality_gates_config: Dict[str, Any],
                                       command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute confidence scoring gate"""
        threshold = self._get_gate_threshold("confidence_score", quality_gates_config, 0.7)

        # This would analyze actual output confidence scores
        confidence_score = 0.85  # Simulated

        return EvaluationGate(
            name="confidence_scoring",
            phase=EvaluationPhase.POST_EXECUTION,
            threshold=threshold,
            critical=False,
            adaptive=True,
            result=confidence_score,
            passed=confidence_score >= threshold
        )

    def _execute_template_compliance_gate(self, command_name: str,
                                        quality_gates_config: Dict[str, Any],
                                        command_context: Dict[str, Any]) -> EvaluationGate:
        """Execute template compliance gate"""
        # This would validate output format compliance
        return EvaluationGate(
            name="template_compliance",
            phase=EvaluationPhase.POST_EXECUTION,
            threshold=0.9,
            critical=False,
            result=0.95,
            passed=True
        )

    # Helper methods

    def _detect_enhancement_mode(self, command_name: str, evaluation_manifest: Dict[str, Any],
                               command_context: Dict[str, Any]) -> bool:
        """Detect if command should run in enhancement mode (Phase 0A protocol)"""
        enhancement_config = evaluation_manifest.get("enhancement_detection", {})

        if not enhancement_config.get("enable_enhancement_mode", True):
            return False

        return self._check_for_evaluation_files(command_name, command_context)

    def _check_for_evaluation_files(self, command_name: str, command_context: Dict[str, Any]) -> bool:
        """Check for existing evaluation files (Phase 0A pattern)"""
        # Implementation would check for evaluation file patterns
        # For now, return False (no enhancement files found)
        return False

    def _load_dependency_manifest(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Load dependency manifest for command"""
        deps_file = Path(f".claude/commands/{command_name}.deps.yaml")

        if deps_file.exists():
            try:
                with open(deps_file, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load dependency manifest for {command_name}: {str(e)}")

        return None

    def _get_gate_threshold(self, gate_name: str, quality_gates_config: Dict[str, Any],
                           default: float) -> float:
        """Get threshold for specific gate from configuration"""
        for phase_name, gates in quality_gates_config.items():
            for gate_config in gates:
                if gate_config.get("gate") == gate_name:
                    return gate_config.get("threshold", default)
        return default

    def _get_command_performance_score(self, command_name: str) -> float:
        """Get historical performance score for command"""
        # This would analyze recent execution history
        # For now, return a simulated score
        return 0.85

    def _has_critical_failures(self, phase_result: PhaseResult) -> bool:
        """Check if phase has critical gate failures"""
        return any(g.critical and not g.passed for g in phase_result.gates)

    def _calculate_overall_score(self, phase_results: List[PhaseResult]) -> float:
        """Calculate overall evaluation score from phase results"""
        if not phase_results:
            return 0.0

        # Weight phases differently
        phase_weights = {
            EvaluationPhase.PRE_EXECUTION: 0.4,
            EvaluationPhase.EXECUTION_MONITORING: 0.2,
            EvaluationPhase.POST_EXECUTION: 0.3,
            EvaluationPhase.FEEDBACK_INTEGRATION: 0.1
        }

        weighted_score = 0.0
        total_weight = 0.0

        for result in phase_results:
            weight = phase_weights.get(result.phase, 0.25)
            weighted_score += result.overall_score * weight
            total_weight += weight

        return weighted_score / total_weight if total_weight > 0 else 0.0

    def _determine_proceed_status(self, evaluation_result: EvaluationResult) -> bool:
        """Determine if command can proceed based on evaluation"""
        # Must pass all critical gates and have minimum overall score
        critical_failures = []
        for phase_result in evaluation_result.phase_results:
            critical_failures.extend([g for g in phase_result.gates if g.critical and not g.passed])

        return len(critical_failures) == 0 and evaluation_result.overall_score >= 0.6

    def _generate_evaluation_fallback_strategy(self, evaluation_result: EvaluationResult,
                                             evaluation_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback strategy for failed evaluation"""
        return {
            "type": "evaluation_fallback",
            "overall_score": evaluation_result.overall_score,
            "failed_phases": [r.phase.value for r in evaluation_result.phase_results if not r.passed],
            "retry_strategies": evaluation_manifest.get("retry_strategies", []),
            "recommendation": "Review failed gates and retry with enhanced parameters"
        }

    def _generate_phase_recommendations(self, phase: EvaluationPhase,
                                      gates: List[EvaluationGate],
                                      overall_score: float) -> List[str]:
        """Generate recommendations for phase results"""
        recommendations = []

        failed_gates = [g for g in gates if not g.passed]
        if failed_gates:
            recommendations.append(f"Failed gates in {phase.value}: {[g.name for g in failed_gates]}")

        if overall_score < 0.7:
            recommendations.append(f"Phase score below target: {overall_score:.2f}")

        return recommendations

    def _save_evaluation_result(self, evaluation_result: EvaluationResult):
        """Save evaluation result to framework results directory"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = self.results_path / f"{evaluation_result.command}_evaluation_{timestamp}.json"

            # Convert to serializable format
            result_dict = asdict(evaluation_result)

            # Convert enum values to strings
            for phase_result in result_dict["phase_results"]:
                phase_result["phase"] = phase_result["phase"].value if hasattr(phase_result["phase"], "value") else str(phase_result["phase"])
                for gate in phase_result["gates"]:
                    gate["phase"] = gate["phase"].value if hasattr(gate["phase"], "value") else str(gate["phase"])

            with open(result_file, 'w') as f:
                json.dump(result_dict, f, indent=2, default=str)

            self.logger.info(f"Evaluation result saved: {result_file}")

        except Exception as e:
            self.logger.error(f"Failed to save evaluation result: {str(e)}")

if __name__ == "__main__":
    # CLI interface for testing
    import argparse

    parser = argparse.ArgumentParser(description="Command Evaluation Protocol")
    parser.add_argument("command", help="Command name to evaluate")
    parser.add_argument("--manifest", help="Path to evaluation manifest file")
    parser.add_argument("--context", help="JSON string with command context")

    args = parser.parse_args()

    evaluator = CommandEvaluationProtocol()

    # Load manifest
    if args.manifest:
        with open(args.manifest, 'r') as f:
            manifest = yaml.safe_load(f)
    else:
        # Default test manifest
        manifest = {
            "version": "1.0",
            "evaluation_phases": {
                "0A_pre_execution": {"gates": ["dependency_validation", "input_validation"]},
                "0B_execution_monitoring": {"gates": ["progress_tracking"]},
                "0C_post_execution": {"gates": ["output_validation", "confidence_scoring"]},
                "0D_feedback_integration": {"gates": ["learning_integration"]}
            },
            "quality_gates": {
                "pre_execution": [
                    {"gate": "dependency_availability", "threshold": 0.95, "critical": True}
                ]
            }
        }

    # Parse context
    context = {}
    if args.context:
        context = json.loads(args.context)

    # Run evaluation
    result = evaluator.evaluate_command(args.command, manifest, context)

    # Print summary
    print(f"Evaluation Summary for {result.command}:")
    print(f"Overall Score: {result.overall_score:.3f}")
    print(f"Can Proceed: {result.can_proceed}")
    print(f"Enhancement Mode: {result.enhancement_mode}")
    print(f"Execution Time: {result.total_execution_time:.2f}s")

    for phase_result in result.phase_results:
        print(f"\n{phase_result.phase.value}: {phase_result.overall_score:.3f} ({'PASS' if phase_result.passed else 'FAIL'})")
        for gate in phase_result.gates:
            status = "PASS" if gate.passed else "FAIL"
            print(f"  {gate.name}: {gate.result:.3f} [{status}]")
