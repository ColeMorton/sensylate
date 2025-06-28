#!/usr/bin/env python3
"""
User Preference Tracking System
Tracks evaluation patterns and threshold optimizations for intelligent learning
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

@dataclass
class PreferenceRecord:
    """Individual preference record"""
    timestamp: str
    command: str
    evaluation_type: str
    user_choice: str
    context: Dict[str, Any]
    outcome_score: float
    confidence_level: float

@dataclass
class ThresholdAdjustment:
    """Threshold adjustment record"""
    gate_name: str
    original_threshold: float
    adjusted_threshold: float
    adjustment_reason: str
    success_rate: float
    timestamp: str

@dataclass
class PreferenceSummary:
    """User preference summary for a command"""
    command: str
    total_interactions: int
    success_rate: float
    preferred_thresholds: Dict[str, float]
    common_patterns: List[str]
    optimization_suggestions: List[str]
    last_updated: str

class UserPreferenceTracker:
    """Tracks user preferences and evaluation patterns for learning optimization"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.preferences_path = self.workspace_path / "framework" / "preferences"
        self.preferences_path.mkdir(parents=True, exist_ok=True)

        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Preference storage files
        self.records_file = self.preferences_path / "preference_records.json"
        self.thresholds_file = self.preferences_path / "threshold_adjustments.json"
        self.summaries_file = self.preferences_path / "preference_summaries.json"

        # Load existing data
        self.preference_records = self._load_preference_records()
        self.threshold_adjustments = self._load_threshold_adjustments()
        self.preference_summaries = self._load_preference_summaries()

    def record_user_interaction(self, command: str, evaluation_result: Dict[str, Any],
                               user_feedback: Dict[str, Any] = None) -> str:
        """Record user interaction with evaluation system"""

        interaction_id = f"{command}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Extract evaluation context
        context = {
            "overall_score": evaluation_result.get("overall_score", 0.0),
            "can_proceed": evaluation_result.get("can_proceed", False),
            "phase_count": len(evaluation_result.get("phase_results", [])),
            "failed_gates": self._extract_failed_gates(evaluation_result),
            "execution_time": evaluation_result.get("total_execution_time", 0.0)
        }

        # Determine user choice and outcome
        user_choice = user_feedback.get("action", "proceeded") if user_feedback else "proceeded"
        outcome_score = user_feedback.get("satisfaction", 0.8) if user_feedback else 0.8
        confidence_level = evaluation_result.get("overall_score", 0.0)

        # Create preference record
        record = PreferenceRecord(
            timestamp=datetime.now().isoformat(),
            command=command,
            evaluation_type="universal_evaluation",
            user_choice=user_choice,
            context=context,
            outcome_score=outcome_score,
            confidence_level=confidence_level
        )

        # Store record
        self.preference_records.append(asdict(record))
        self._save_preference_records()

        # Update preference summary
        self._update_preference_summary(command)

        self.logger.info(f"Recorded user interaction: {interaction_id}")
        return interaction_id

    def record_threshold_adjustment(self, command: str, gate_name: str,
                                  original_threshold: float, new_threshold: float,
                                  reason: str, success_rate: float = 0.0) -> str:
        """Record threshold adjustment for learning"""

        adjustment_id = f"{command}_{gate_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        adjustment = ThresholdAdjustment(
            gate_name=gate_name,
            original_threshold=original_threshold,
            adjusted_threshold=new_threshold,
            adjustment_reason=reason,
            success_rate=success_rate,
            timestamp=datetime.now().isoformat()
        )

        # Store adjustment
        if command not in self.threshold_adjustments:
            self.threshold_adjustments[command] = []

        self.threshold_adjustments[command].append(asdict(adjustment))
        self._save_threshold_adjustments()

        self.logger.info(f"Recorded threshold adjustment: {adjustment_id}")
        return adjustment_id

    def get_preferred_thresholds(self, command: str) -> Dict[str, float]:
        """Get user's preferred thresholds for a command based on learning"""

        if command not in self.preference_summaries:
            return {}

        return self.preference_summaries[command].get("preferred_thresholds", {})

    def get_optimization_suggestions(self, command: str,
                                   current_evaluation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get optimization suggestions based on user preferences and patterns"""

        suggestions = []

        # Get command preference summary
        if command not in self.preference_summaries:
            return suggestions

        summary = self.preference_summaries[command]
        current_score = current_evaluation.get("overall_score", 0.0)

        # Suggest threshold adjustments based on patterns
        preferred_thresholds = summary.get("preferred_thresholds", {})
        for gate_name, preferred_threshold in preferred_thresholds.items():
            suggestions.append({
                "type": "threshold_adjustment",
                "gate": gate_name,
                "current_threshold": "unknown",
                "suggested_threshold": preferred_threshold,
                "confidence": self._calculate_suggestion_confidence(command, gate_name),
                "reason": f"Based on {summary.get('total_interactions', 0)} interactions"
            })

        # Suggest workflow optimizations
        common_patterns = summary.get("common_patterns", [])
        for pattern in common_patterns:
            if "low_score_success" in pattern and current_score < 0.7:
                suggestions.append({
                    "type": "workflow_optimization",
                    "suggestion": "Consider proceeding despite low score",
                    "confidence": 0.7,
                    "reason": "User historically successful with similar scores"
                })

        # Suggest enhancement opportunities
        if summary.get("success_rate", 0.0) < 0.8:
            suggestions.append({
                "type": "enhancement_opportunity",
                "suggestion": "Enable adaptive thresholds for this command",
                "confidence": 0.8,
                "reason": f"Command success rate below target: {summary.get('success_rate', 0.0):.2f}"
            })

        return suggestions

    def analyze_preference_patterns(self, command: str = None) -> Dict[str, Any]:
        """Analyze preference patterns for insights and optimization"""

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "commands_analyzed": [],
            "global_patterns": [],
            "optimization_opportunities": []
        }

        commands_to_analyze = [command] if command else list(self.preference_summaries.keys())

        for cmd in commands_to_analyze:
            if cmd not in self.preference_summaries:
                continue

            cmd_analysis = self._analyze_command_patterns(cmd)
            analysis["commands_analyzed"].append(cmd_analysis)

            # Extract global patterns
            analysis["global_patterns"].extend(cmd_analysis.get("patterns", []))

        # Identify optimization opportunities
        analysis["optimization_opportunities"] = self._identify_optimization_opportunities(
            analysis["commands_analyzed"]
        )

        return analysis

    def _analyze_command_patterns(self, command: str) -> Dict[str, Any]:
        """Analyze patterns for a specific command"""

        # Get command records
        cmd_records = [r for r in self.preference_records if r["command"] == command]

        if not cmd_records:
            return {"command": command, "patterns": [], "insights": []}

        analysis = {
            "command": command,
            "total_interactions": len(cmd_records),
            "patterns": [],
            "insights": [],
            "recommendations": []
        }

        # Analyze success patterns
        success_records = [r for r in cmd_records if r["outcome_score"] > 0.7]
        analysis["success_rate"] = len(success_records) / len(cmd_records)

        # Pattern: Low score but high satisfaction
        low_score_success = [r for r in success_records if r["confidence_level"] < 0.7]
        if len(low_score_success) > len(cmd_records) * 0.3:
            analysis["patterns"].append("low_score_success_pattern")
            analysis["insights"].append("User often satisfied despite low evaluation scores")
            analysis["recommendations"].append("Consider lowering quality gate thresholds")

        # Pattern: High execution time tolerance
        long_execution = [r for r in cmd_records if r["context"].get("execution_time", 0) > 60]
        if len(long_execution) > len(cmd_records) * 0.5:
            analysis["patterns"].append("high_execution_time_tolerance")
            analysis["insights"].append("User tolerates longer execution times")

        # Pattern: Specific gate failure tolerance
        failed_gates_analysis = self._analyze_failed_gates_tolerance(cmd_records)
        analysis["patterns"].extend(failed_gates_analysis["patterns"])
        analysis["insights"].extend(failed_gates_analysis["insights"])

        return analysis

    def _analyze_failed_gates_tolerance(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze tolerance for specific gate failures"""

        analysis = {"patterns": [], "insights": []}

        # Count gate failure frequencies and user responses
        gate_failures = {}
        for record in records:
            failed_gates = record["context"].get("failed_gates", [])
            user_proceeded = record["user_choice"] in ["proceeded", "accepted"]

            for gate in failed_gates:
                if gate not in gate_failures:
                    gate_failures[gate] = {"total": 0, "proceeded": 0}
                gate_failures[gate]["total"] += 1
                if user_proceeded:
                    gate_failures[gate]["proceeded"] += 1

        # Identify high-tolerance gates
        for gate, stats in gate_failures.items():
            if stats["total"] > 2:  # At least 3 occurrences
                tolerance_rate = stats["proceeded"] / stats["total"]
                if tolerance_rate > 0.7:
                    analysis["patterns"].append(f"high_tolerance_{gate}")
                    analysis["insights"].append(f"User tolerates {gate} failures {tolerance_rate:.1%} of the time")

        return analysis

    def _identify_optimization_opportunities(self, command_analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify system-wide optimization opportunities"""

        opportunities = []

        # Global threshold optimization
        low_success_commands = [a for a in command_analyses if a.get("success_rate", 1.0) < 0.8]
        if len(low_success_commands) > len(command_analyses) * 0.3:
            opportunities.append({
                "type": "global_threshold_reduction",
                "description": "Multiple commands have low success rates",
                "affected_commands": [a["command"] for a in low_success_commands],
                "priority": "high"
            })

        # Pattern-based optimization
        all_patterns = []
        for analysis in command_analyses:
            all_patterns.extend(analysis.get("patterns", []))

        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        # Common patterns across commands
        common_patterns = [p for p, count in pattern_counts.items() if count > 1]
        if common_patterns:
            opportunities.append({
                "type": "pattern_based_optimization",
                "description": "Common user patterns identified across commands",
                "patterns": common_patterns,
                "priority": "medium"
            })

        return opportunities

    def _extract_failed_gates(self, evaluation_result: Dict[str, Any]) -> List[str]:
        """Extract failed gate names from evaluation result"""
        failed_gates = []

        phase_results = evaluation_result.get("phase_results", [])
        for phase_result in phase_results:
            if isinstance(phase_result, dict):
                gates = phase_result.get("gates", [])
                for gate in gates:
                    if isinstance(gate, dict) and not gate.get("passed", True):
                        failed_gates.append(gate.get("name", "unknown_gate"))

        return failed_gates

    def _update_preference_summary(self, command: str):
        """Update preference summary for command"""

        # Get recent records for command
        cmd_records = [r for r in self.preference_records if r["command"] == command]

        if not cmd_records:
            return

        # Calculate summary statistics
        total_interactions = len(cmd_records)
        success_records = [r for r in cmd_records if r["outcome_score"] > 0.7]
        success_rate = len(success_records) / total_interactions

        # Calculate preferred thresholds (simplified - would use more sophisticated analysis)
        preferred_thresholds = {}
        if success_records:
            avg_confidence = sum(r["confidence_level"] for r in success_records) / len(success_records)
            preferred_thresholds["overall_threshold"] = max(0.6, avg_confidence - 0.1)

        # Identify common patterns
        common_patterns = []
        low_score_success = [r for r in success_records if r["confidence_level"] < 0.7]
        if len(low_score_success) > total_interactions * 0.3:
            common_patterns.append("low_score_success")

        # Generate optimization suggestions
        optimization_suggestions = []
        if success_rate < 0.8:
            optimization_suggestions.append("Consider adaptive thresholds")
        if common_patterns:
            optimization_suggestions.append("Apply pattern-based optimizations")

        # Create/update summary
        summary = PreferenceSummary(
            command=command,
            total_interactions=total_interactions,
            success_rate=success_rate,
            preferred_thresholds=preferred_thresholds,
            common_patterns=common_patterns,
            optimization_suggestions=optimization_suggestions,
            last_updated=datetime.now().isoformat()
        )

        self.preference_summaries[command] = asdict(summary)
        self._save_preference_summaries()

    def _calculate_suggestion_confidence(self, command: str, gate_name: str) -> float:
        """Calculate confidence level for threshold suggestions"""

        if command not in self.threshold_adjustments:
            return 0.5

        # Find adjustments for this gate
        adjustments = [a for a in self.threshold_adjustments[command]
                      if a["gate_name"] == gate_name]

        if not adjustments:
            return 0.5

        # Calculate confidence based on success rate and frequency
        avg_success_rate = sum(a["success_rate"] for a in adjustments) / len(adjustments)
        frequency_factor = min(1.0, len(adjustments) / 5.0)  # Max confidence with 5+ adjustments

        return avg_success_rate * frequency_factor

    # Data persistence methods

    def _load_preference_records(self) -> List[Dict[str, Any]]:
        """Load preference records from file"""
        if self.records_file.exists():
            try:
                with open(self.records_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load preference records: {str(e)}")
        return []

    def _save_preference_records(self):
        """Save preference records to file"""
        try:
            with open(self.records_file, 'w') as f:
                json.dump(self.preference_records, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save preference records: {str(e)}")

    def _load_threshold_adjustments(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load threshold adjustments from file"""
        if self.thresholds_file.exists():
            try:
                with open(self.thresholds_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load threshold adjustments: {str(e)}")
        return {}

    def _save_threshold_adjustments(self):
        """Save threshold adjustments to file"""
        try:
            with open(self.thresholds_file, 'w') as f:
                json.dump(self.threshold_adjustments, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save threshold adjustments: {str(e)}")

    def _load_preference_summaries(self) -> Dict[str, Dict[str, Any]]:
        """Load preference summaries from file"""
        if self.summaries_file.exists():
            try:
                with open(self.summaries_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load preference summaries: {str(e)}")
        return {}

    def _save_preference_summaries(self):
        """Save preference summaries to file"""
        try:
            with open(self.summaries_file, 'w') as f:
                json.dump(self.preference_summaries, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save preference summaries: {str(e)}")

    def export_preferences_report(self) -> str:
        """Export comprehensive preferences report"""

        report_path = self.preferences_path / f"preferences_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report = {
            "export_timestamp": datetime.now().isoformat(),
            "total_records": len(self.preference_records),
            "commands_tracked": list(self.preference_summaries.keys()),
            "preference_summaries": self.preference_summaries,
            "threshold_adjustments": self.threshold_adjustments,
            "pattern_analysis": self.analyze_preference_patterns()
        }

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        return str(report_path)

if __name__ == "__main__":
    # Example usage and testing
    tracker = UserPreferenceTracker()

    # Simulate user interaction
    eval_result = {
        "overall_score": 0.75,
        "can_proceed": True,
        "total_execution_time": 45.0,
        "phase_results": []
    }

    interaction_id = tracker.record_user_interaction("fundamental_analysis", eval_result)
    print(f"Recorded interaction: {interaction_id}")

    # Get optimization suggestions
    suggestions = tracker.get_optimization_suggestions("fundamental_analysis", eval_result)
    print(f"Optimization suggestions: {len(suggestions)}")

    # Export report
    report_path = tracker.export_preferences_report()
    print(f"Preferences report exported: {report_path}")
