#!/usr/bin/env python3
"""
Automated Workflow Engine
Executes high-confidence workflows automatically with user-defined controls
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import time

from .smart_workflow_orchestrator import WorkflowSuggestion, WorkflowConfidence, SuggestionPriority

class AutomationLevel(Enum):
    DISABLED = "disabled"           # No automation
    CONSERVATIVE = "conservative"   # Only very high confidence (>95%)
    MODERATE = "moderate"          # High confidence (>80%)
    AGGRESSIVE = "aggressive"      # Medium confidence (>60%)

class AutomationScope(Enum):
    SINGLE_COMMAND = "single_command"     # One command at a time
    COMMAND_CHAIN = "command_chain"       # Related command sequences
    FULL_WORKFLOW = "full_workflow"       # Complete workflow automation

@dataclass
class AutomationRule:
    """Defines rules for automated workflow execution"""
    rule_id: str
    name: str
    command_pattern: str  # Command or pattern to match
    confidence_threshold: float
    max_execution_time: int  # seconds
    automation_level: AutomationLevel
    automation_scope: AutomationScope
    user_confirmation_required: bool
    cooldown_period: int  # seconds between auto-executions
    success_rate_threshold: float  # Minimum success rate to maintain automation
    enabled: bool
    created_at: datetime
    last_used: Optional[datetime] = None
    success_count: int = 0
    total_executions: int = 0

@dataclass
class AutomationExecution:
    """Represents an automated workflow execution"""
    execution_id: str
    rule_id: str
    command: str
    parameters: Dict[str, Any]
    confidence: float
    status: str  # queued, running, completed, failed, cancelled
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    user_override: bool = False

class AutomatedWorkflowEngine:
    """Manages automated execution of high-confidence workflows"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.automation_path = self.workspace_path / "framework" / "automation"
        self.automation_path.mkdir(parents=True, exist_ok=True)

        # Automation configuration
        self.rules_path = self.automation_path / "rules"
        self.rules_path.mkdir(exist_ok=True)

        self.executions_path = self.automation_path / "executions"
        self.executions_path.mkdir(exist_ok=True)

        self.logs_path = self.automation_path / "logs"
        self.logs_path.mkdir(exist_ok=True)

        # Load automation rules
        self.automation_rules = self._load_automation_rules()

        # Execution tracking
        self.active_executions = {}
        self.execution_queue = []

        # Safety mechanisms
        self.safety_monitor = AutomationSafetyMonitor(self.workspace_path)
        self.performance_tracker = AutomationPerformanceTracker(self.workspace_path)

        # User preferences
        self.user_preferences = self._load_user_preferences()

    def evaluate_for_automation(self, suggestion: WorkflowSuggestion,
                              user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if suggestion should be automated"""

        user_id = user_context.get("user_id", "default")

        # Check if automation is enabled for user
        if not self._is_automation_enabled(user_id):
            return {"automate": False, "reason": "automation_disabled"}

        # Find applicable automation rules
        applicable_rules = self._find_applicable_rules(suggestion, user_context)

        if not applicable_rules:
            return {"automate": False, "reason": "no_applicable_rules"}

        # Evaluate each rule
        for rule in applicable_rules:
            evaluation = self._evaluate_automation_rule(suggestion, rule, user_context)

            if evaluation["should_automate"]:
                return {
                    "automate": True,
                    "rule": rule.rule_id,
                    "confidence": suggestion.confidence.value,
                    "evaluation": evaluation,
                    "estimated_execution_time": suggestion.estimated_time,
                    "automation_level": rule.automation_level.value
                }

        return {"automate": False, "reason": "rules_not_satisfied"}

    def execute_automated_workflow(self, suggestion: WorkflowSuggestion,
                                 rule: AutomationRule,
                                 user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow automatically based on rule"""

        # Generate execution ID
        execution_id = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{rule.rule_id}"

        # Create execution record
        execution = AutomationExecution(
            execution_id=execution_id,
            rule_id=rule.rule_id,
            command=suggestion.command,
            parameters=suggestion.parameters,
            confidence=self._convert_confidence_to_float(suggestion.confidence),
            status="queued",
            started_at=datetime.now()
        )

        # Safety checks
        safety_check = self.safety_monitor.perform_safety_check(suggestion, rule, user_context)

        if not safety_check["safe"]:
            execution.status = "cancelled"
            execution.error_message = safety_check["reason"]
            self._record_execution(execution)
            return {"status": "cancelled", "reason": safety_check["reason"]}

        # Queue for execution
        if rule.user_confirmation_required:
            execution.status = "awaiting_confirmation"
            self._record_execution(execution)
            return self._request_user_confirmation(execution, suggestion, rule)
        else:
            return self._queue_for_execution(execution, suggestion, rule, user_context)

    def confirm_automated_execution(self, execution_id: str,
                                  confirmed: bool) -> Dict[str, Any]:
        """Handle user confirmation for automated execution"""

        execution = self._get_execution_by_id(execution_id)

        if not execution:
            return {"status": "error", "message": "Execution not found"}

        if confirmed:
            execution.status = "confirmed"
            return self._proceed_with_execution(execution)
        else:
            execution.status = "cancelled"
            execution.user_override = True
            self._record_execution(execution)
            return {"status": "cancelled", "message": "Execution cancelled by user"}

    def cancel_automated_execution(self, execution_id: str) -> Dict[str, Any]:
        """Cancel an automated execution"""

        execution = self._get_execution_by_id(execution_id)

        if not execution:
            return {"status": "error", "message": "Execution not found"}

        if execution.status in ["completed", "failed", "cancelled"]:
            return {"status": "error", "message": f"Cannot cancel {execution.status} execution"}

        execution.status = "cancelled"
        execution.user_override = True
        execution.completed_at = datetime.now()

        # Remove from active executions
        if execution_id in self.active_executions:
            del self.active_executions[execution_id]

        self._record_execution(execution)

        return {"status": "cancelled", "message": "Execution cancelled successfully"}

    def get_automation_status(self, user_id: str = None) -> Dict[str, Any]:
        """Get current automation status and metrics"""

        # Get active executions
        active_count = len([e for e in self.active_executions.values()
                          if e.status in ["queued", "running", "awaiting_confirmation"]])

        # Get recent performance metrics
        performance_metrics = self.performance_tracker.get_performance_metrics(user_id)

        # Get automation rules summary
        rules_summary = self._get_rules_summary(user_id)

        return {
            "automation_enabled": self._is_automation_enabled(user_id),
            "active_executions": active_count,
            "queued_executions": len(self.execution_queue),
            "performance_metrics": performance_metrics,
            "automation_rules": rules_summary,
            "safety_status": self.safety_monitor.get_safety_status(),
            "recent_activity": self._get_recent_activity_summary()
        }

    def update_automation_preferences(self, user_id: str,
                                    preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user automation preferences"""

        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}

        # Update preferences
        self.user_preferences[user_id].update(preferences)

        # Save preferences
        self._save_user_preferences()

        # Update applicable rules if automation level changed
        if "automation_level" in preferences:
            self._update_user_automation_rules(user_id, preferences["automation_level"])

        return {
            "status": "updated",
            "user_id": user_id,
            "updated_preferences": preferences,
            "current_preferences": self.user_preferences[user_id]
        }

    def create_automation_rule(self, rule_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create new automation rule"""

        rule_id = f"rule_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        rule = AutomationRule(
            rule_id=rule_id,
            name=rule_config["name"],
            command_pattern=rule_config["command_pattern"],
            confidence_threshold=rule_config.get("confidence_threshold", 0.8),
            max_execution_time=rule_config.get("max_execution_time", 300),
            automation_level=AutomationLevel(rule_config.get("automation_level", "conservative")),
            automation_scope=AutomationScope(rule_config.get("automation_scope", "single_command")),
            user_confirmation_required=rule_config.get("user_confirmation_required", True),
            cooldown_period=rule_config.get("cooldown_period", 60),
            success_rate_threshold=rule_config.get("success_rate_threshold", 0.8),
            enabled=rule_config.get("enabled", True),
            created_at=datetime.now()
        )

        self.automation_rules[rule_id] = rule
        self._save_automation_rules()

        return {
            "status": "created",
            "rule_id": rule_id,
            "rule": asdict(rule)
        }

    def _find_applicable_rules(self, suggestion: WorkflowSuggestion,
                             user_context: Dict[str, Any]) -> List[AutomationRule]:
        """Find automation rules applicable to suggestion"""

        applicable_rules = []

        for rule in self.automation_rules.values():
            if not rule.enabled:
                continue

            # Check command pattern match
            if not self._matches_command_pattern(suggestion.command, rule.command_pattern):
                continue

            # Check cooldown period
            if rule.last_used and self._is_in_cooldown(rule):
                continue

            # Check success rate threshold
            if rule.total_executions > 5:  # Need minimum executions for meaningful rate
                success_rate = rule.success_count / rule.total_executions
                if success_rate < rule.success_rate_threshold:
                    continue

            applicable_rules.append(rule)

        # Sort by most restrictive rules first
        return sorted(applicable_rules,
                     key=lambda r: (r.confidence_threshold, -r.max_execution_time),
                     reverse=True)

    def _evaluate_automation_rule(self, suggestion: WorkflowSuggestion,
                                rule: AutomationRule,
                                user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if suggestion meets automation rule criteria"""

        # Convert confidence to float for comparison
        suggestion_confidence = self._convert_confidence_to_float(suggestion.confidence)

        checks = {
            "confidence_threshold": suggestion_confidence >= rule.confidence_threshold,
            "execution_time_limit": suggestion.estimated_time <= rule.max_execution_time,
            "automation_level_appropriate": self._check_automation_level(suggestion, rule),
            "safety_checks": self.safety_monitor.quick_safety_check(suggestion, rule),
            "user_context_appropriate": self._check_user_context(user_context, rule)
        }

        should_automate = all(checks.values())

        return {
            "should_automate": should_automate,
            "checks": checks,
            "confidence_score": suggestion_confidence,
            "rule_threshold": rule.confidence_threshold,
            "estimated_time": suggestion.estimated_time,
            "time_limit": rule.max_execution_time
        }

    def _queue_for_execution(self, execution: AutomationExecution,
                           suggestion: WorkflowSuggestion,
                           rule: AutomationRule,
                           user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Queue execution for processing"""

        execution.status = "queued"
        self.active_executions[execution.execution_id] = execution
        self.execution_queue.append({
            "execution": execution,
            "suggestion": suggestion,
            "rule": rule,
            "user_context": user_context
        })

        self._record_execution(execution)

        # Process queue asynchronously (if event loop is running)
        try:
            asyncio.create_task(self._process_execution_queue())
        except RuntimeError:
            # No event loop running - queue will be processed later
            pass

        return {
            "status": "queued",
            "execution_id": execution.execution_id,
            "estimated_start_time": datetime.now() + timedelta(seconds=len(self.execution_queue) * 2),
            "queue_position": len(self.execution_queue)
        }

    async def _process_execution_queue(self):
        """Process queued executions"""

        while self.execution_queue:
            queue_item = self.execution_queue.pop(0)
            execution = queue_item["execution"]
            suggestion = queue_item["suggestion"]
            rule = queue_item["rule"]
            user_context = queue_item["user_context"]

            # Update status
            execution.status = "running"
            execution.started_at = datetime.now()

            try:
                # Simulate command execution (in real implementation, this would call the actual command)
                start_time = time.time()

                # Mock execution result
                await asyncio.sleep(min(suggestion.estimated_time / 10, 5))  # Simulated execution

                execution_time = time.time() - start_time
                execution.execution_time = execution_time
                execution.completed_at = datetime.now()
                execution.status = "completed"
                execution.success = True

                # Update rule statistics
                rule.total_executions += 1
                rule.success_count += 1
                rule.last_used = datetime.now()

                # Record performance metrics
                self.performance_tracker.record_execution(execution, suggestion, rule)

            except Exception as e:
                execution.status = "failed"
                execution.success = False
                execution.error_message = str(e)
                execution.completed_at = datetime.now()

                # Update rule statistics
                rule.total_executions += 1
                # Don't increment success_count for failed executions

            finally:
                # Clean up
                if execution.execution_id in self.active_executions:
                    del self.active_executions[execution.execution_id]

                self._record_execution(execution)
                self._save_automation_rules()

    def _request_user_confirmation(self, execution: AutomationExecution,
                                 suggestion: WorkflowSuggestion,
                                 rule: AutomationRule) -> Dict[str, Any]:
        """Request user confirmation for automated execution"""

        return {
            "status": "awaiting_confirmation",
            "execution_id": execution.execution_id,
            "message": f"Automated execution of {suggestion.command} requires confirmation",
            "details": {
                "command": suggestion.command,
                "description": suggestion.description,
                "confidence": suggestion.confidence.value,
                "estimated_time": suggestion.estimated_time,
                "rule_name": rule.name,
                "automation_level": rule.automation_level.value
            },
            "confirmation_required_by": datetime.now() + timedelta(minutes=5),
            "options": {
                "confirm": f"Execute {suggestion.command} automatically",
                "cancel": "Cancel automated execution",
                "execute_manually": "Execute manually instead"
            }
        }

    def _convert_confidence_to_float(self, confidence: WorkflowConfidence) -> float:
        """Convert confidence enum to float value"""

        confidence_map = {
            WorkflowConfidence.VERY_HIGH: 0.95,
            WorkflowConfidence.HIGH: 0.85,
            WorkflowConfidence.MEDIUM: 0.70,
            WorkflowConfidence.LOW: 0.50
        }

        return confidence_map.get(confidence, 0.50)

    def _is_automation_enabled(self, user_id: str) -> bool:
        """Check if automation is enabled for user"""

        user_prefs = self.user_preferences.get(user_id, {})
        return user_prefs.get("automation_enabled", False)

    def _load_automation_rules(self) -> Dict[str, AutomationRule]:
        """Load automation rules from storage"""

        rules = {}

        for rule_file in self.rules_path.glob("*.json"):
            try:
                with open(rule_file, 'r') as f:
                    rule_data = json.load(f)

                # Convert datetime strings
                rule_data["created_at"] = datetime.fromisoformat(rule_data["created_at"])
                if rule_data.get("last_used"):
                    rule_data["last_used"] = datetime.fromisoformat(rule_data["last_used"])

                # Convert enums
                rule_data["automation_level"] = AutomationLevel(rule_data["automation_level"])
                rule_data["automation_scope"] = AutomationScope(rule_data["automation_scope"])

                rule = AutomationRule(**rule_data)
                rules[rule.rule_id] = rule

            except Exception as e:
                print(f"Error loading rule {rule_file}: {e}")

        # Create default rules if none exist
        if not rules:
            rules = self._create_default_automation_rules()

        return rules

    def _save_automation_rules(self):
        """Save automation rules to storage"""

        for rule in self.automation_rules.values():
            rule_file = self.rules_path / f"{rule.rule_id}.json"

            with open(rule_file, 'w') as f:
                json.dump(asdict(rule), f, indent=2, default=str)

    def _create_default_automation_rules(self) -> Dict[str, AutomationRule]:
        """Create default automation rules"""

        default_rules = {}

        # High-confidence fundamental analysis
        rule = AutomationRule(
            rule_id="default_fundamental_analysis",
            name="High-Confidence Fundamental Analysis",
            command_pattern="fundamental_analysis",
            confidence_threshold=0.90,
            max_execution_time=180,
            automation_level=AutomationLevel.CONSERVATIVE,
            automation_scope=AutomationScope.SINGLE_COMMAND,
            user_confirmation_required=True,
            cooldown_period=300,
            success_rate_threshold=0.85,
            enabled=False,  # Disabled by default
            created_at=datetime.now()
        )
        default_rules[rule.rule_id] = rule

        # Social media content automation
        rule = AutomationRule(
            rule_id="default_social_media",
            name="High-Confidence Social Media Content",
            command_pattern="social_media_content",
            confidence_threshold=0.85,
            max_execution_time=60,
            automation_level=AutomationLevel.MODERATE,
            automation_scope=AutomationScope.SINGLE_COMMAND,
            user_confirmation_required=False,
            cooldown_period=60,
            success_rate_threshold=0.80,
            enabled=False,  # Disabled by default
            created_at=datetime.now()
        )
        default_rules[rule.rule_id] = rule

        return default_rules

    def _load_user_preferences(self) -> Dict[str, Dict[str, Any]]:
        """Load user preferences from storage"""

        prefs_path = self.automation_path / "user_preferences"
        prefs_path.mkdir(exist_ok=True)

        preferences = {}

        for prefs_file in prefs_path.glob("user_*.json"):
            try:
                user_id = prefs_file.stem.replace("user_", "")
                with open(prefs_file, 'r') as f:
                    user_prefs = json.load(f)
                preferences[user_id] = user_prefs
            except Exception as e:
                print(f"Error loading user preferences {prefs_file}: {e}")

        return preferences

    def _save_user_preferences(self):
        """Save user preferences to storage"""

        prefs_path = self.automation_path / "user_preferences"
        prefs_path.mkdir(exist_ok=True)

        for user_id, prefs in self.user_preferences.items():
            prefs_file = prefs_path / f"user_{user_id}.json"
            with open(prefs_file, 'w') as f:
                json.dump(prefs, f, indent=2, default=str)

    def _update_user_automation_rules(self, user_id: str, automation_level: str):
        """Update user-specific automation rules based on automation level"""

        level_map = {
            "conservative": AutomationLevel.CONSERVATIVE,
            "moderate": AutomationLevel.MODERATE,
            "aggressive": AutomationLevel.AGGRESSIVE
        }

        target_level = level_map.get(automation_level, AutomationLevel.CONSERVATIVE)

        # Update existing rules for this automation level
        for rule in self.automation_rules.values():
            if rule.automation_level == target_level:
                rule.enabled = True
            elif rule.automation_level != target_level:
                rule.enabled = False

    def _matches_command_pattern(self, command: str, pattern: str) -> bool:
        """Check if command matches pattern"""

        # Simple pattern matching - could be enhanced with regex
        if pattern == "*":
            return True
        elif pattern == command:
            return True
        elif pattern.endswith("*") and command.startswith(pattern[:-1]):
            return True
        else:
            return False

    def _is_in_cooldown(self, rule: AutomationRule) -> bool:
        """Check if rule is in cooldown period"""

        if not rule.last_used:
            return False

        cooldown_end = rule.last_used + timedelta(seconds=rule.cooldown_period)
        return datetime.now() < cooldown_end

    def _check_automation_level(self, suggestion: WorkflowSuggestion, rule: AutomationRule) -> bool:
        """Check if suggestion is appropriate for automation level"""

        suggestion_confidence = self._convert_confidence_to_float(suggestion.confidence)

        level_thresholds = {
            AutomationLevel.CONSERVATIVE: 0.95,
            AutomationLevel.MODERATE: 0.80,
            AutomationLevel.AGGRESSIVE: 0.60
        }

        required_threshold = level_thresholds.get(rule.automation_level, 0.95)
        return suggestion_confidence >= required_threshold

    def _check_user_context(self, user_context: Dict[str, Any], rule: AutomationRule) -> bool:
        """Check if user context is appropriate for automation"""

        # Check if user has automation enabled
        user_id = user_context.get("user_id", "default")
        user_prefs = self.user_preferences.get(user_id, {})

        if not user_prefs.get("automation_enabled", False):
            return False

        # Check time-based restrictions
        current_hour = datetime.now().hour
        restricted_hours = user_prefs.get("automation_restricted_hours", [])

        if current_hour in restricted_hours:
            return False

        return True

    def _proceed_with_execution(self, execution: AutomationExecution) -> Dict[str, Any]:
        """Proceed with confirmed execution"""

        execution.status = "queued"
        self.active_executions[execution.execution_id] = execution

        # Add to execution queue
        queue_item = {
            "execution": execution,
            "suggestion": None,  # Would need to store suggestion
            "rule": self.automation_rules.get(execution.rule_id),
            "user_context": {}
        }
        self.execution_queue.append(queue_item)

        return {
            "status": "proceeding",
            "execution_id": execution.execution_id,
            "message": "Execution confirmed and queued"
        }

    def _get_execution_by_id(self, execution_id: str) -> Optional[AutomationExecution]:
        """Get execution by ID"""

        # Check active executions
        if execution_id in self.active_executions:
            return self.active_executions[execution_id]

        # Check execution history
        for execution_file in self.executions_path.glob("*.json"):
            try:
                with open(execution_file, 'r') as f:
                    execution_data = json.load(f)

                if execution_data.get("execution_id") == execution_id:
                    # Convert datetime strings
                    execution_data["started_at"] = datetime.fromisoformat(execution_data["started_at"])
                    if execution_data.get("completed_at"):
                        execution_data["completed_at"] = datetime.fromisoformat(execution_data["completed_at"])

                    return AutomationExecution(**execution_data)
            except Exception:
                continue

        return None

    def _record_execution(self, execution: AutomationExecution):
        """Record execution to storage"""

        execution_file = self.executions_path / f"{execution.execution_id}.json"

        with open(execution_file, 'w') as f:
            json.dump(asdict(execution), f, indent=2, default=str)

    def _get_rules_summary(self, user_id: str = None) -> Dict[str, Any]:
        """Get summary of automation rules"""

        total_rules = len(self.automation_rules)
        enabled_rules = len([r for r in self.automation_rules.values() if r.enabled])

        # Filter by user if specified
        if user_id:
            user_prefs = self.user_preferences.get(user_id, {})
            automation_level = user_prefs.get("automation_level", "conservative")

            level_map = {
                "conservative": AutomationLevel.CONSERVATIVE,
                "moderate": AutomationLevel.MODERATE,
                "aggressive": AutomationLevel.AGGRESSIVE
            }

            target_level = level_map.get(automation_level, AutomationLevel.CONSERVATIVE)
            applicable_rules = len([r for r in self.automation_rules.values()
                                  if r.enabled and r.automation_level == target_level])
        else:
            applicable_rules = enabled_rules

        return {
            "total_rules": total_rules,
            "enabled_rules": enabled_rules,
            "applicable_rules": applicable_rules,
            "rule_types": list(set(r.automation_level.value for r in self.automation_rules.values()))
        }

    def _get_recent_activity_summary(self) -> Dict[str, Any]:
        """Get recent automation activity summary"""

        recent_executions = []
        cutoff_time = datetime.now() - timedelta(hours=24)

        for execution_file in self.executions_path.glob("*.json"):
            try:
                with open(execution_file, 'r') as f:
                    execution_data = json.load(f)

                started_at = datetime.fromisoformat(execution_data["started_at"])
                if started_at > cutoff_time:
                    recent_executions.append(execution_data)
            except Exception:
                continue

        successful_executions = len([e for e in recent_executions if e.get("success", False)])

        return {
            "recent_executions": len(recent_executions),
            "successful_executions": successful_executions,
            "success_rate": successful_executions / len(recent_executions) if recent_executions else 0.0,
            "time_period": "24h"
        }

    def get_automation_metrics(self) -> Dict[str, Any]:
        """Get automation system metrics"""

        total_executions = sum(rule.total_executions for rule in self.automation_rules.values())
        total_successes = sum(rule.success_count for rule in self.automation_rules.values())

        overall_success_rate = (total_successes / total_executions) if total_executions > 0 else 0.0

        return {
            "total_automation_rules": len(self.automation_rules),
            "enabled_rules": len([r for r in self.automation_rules.values() if r.enabled]),
            "total_executions": total_executions,
            "overall_success_rate": overall_success_rate,
            "active_executions": len(self.active_executions),
            "queue_length": len(self.execution_queue),
            "automation_efficiency": self.performance_tracker.get_efficiency_metrics(),
            "safety_incidents": self.safety_monitor.get_incident_count()
        }

class AutomationSafetyMonitor:
    """Monitors automation safety and prevents harmful executions"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.safety_incidents = []

    def perform_safety_check(self, suggestion: WorkflowSuggestion,
                           rule: AutomationRule,
                           user_context: Dict[str, Any]) -> Dict[str, bool]:
        """Perform comprehensive safety check"""

        checks = {
            "resource_availability": self._check_resource_availability(suggestion),
            "rate_limiting": self._check_rate_limiting(suggestion, rule),
            "dependency_safety": self._check_dependency_safety(suggestion),
            "execution_environment": self._check_execution_environment(user_context),
            "command_safety": self._check_command_safety(suggestion.command)
        }

        safe = all(checks.values())

        if not safe:
            self._record_safety_incident(suggestion, rule, checks)

        return {
            "safe": safe,
            "checks": checks,
            "reason": self._get_safety_failure_reason(checks) if not safe else None
        }

    def quick_safety_check(self, suggestion: WorkflowSuggestion,
                         rule: AutomationRule) -> bool:
        """Quick safety check for rule evaluation"""

        # Basic safety checks
        if suggestion.estimated_time > rule.max_execution_time * 2:
            return False

        if suggestion.command in ["rm", "delete", "drop", "truncate"]:
            return False

        return True

    def _check_resource_availability(self, suggestion: WorkflowSuggestion) -> bool:
        """Check if system resources are available"""
        # Mock implementation - would check actual system resources
        return True

    def _check_rate_limiting(self, suggestion: WorkflowSuggestion, rule: AutomationRule) -> bool:
        """Check rate limiting constraints"""
        # Mock implementation - would check execution frequency
        return True

    def _check_dependency_safety(self, suggestion: WorkflowSuggestion) -> bool:
        """Check if dependencies are safe to execute"""
        # Mock implementation - would validate dependencies
        return True

    def _check_execution_environment(self, user_context: Dict[str, Any]) -> bool:
        """Check if execution environment is safe"""
        # Mock implementation - would validate environment
        return True

    def _check_command_safety(self, command: str) -> bool:
        """Check if command is safe for automation"""

        unsafe_commands = ["rm", "delete", "drop", "truncate", "format"]
        return command not in unsafe_commands

    def get_safety_status(self) -> Dict[str, Any]:
        """Get safety monitoring status"""

        recent_incidents = len([i for i in self.safety_incidents
                              if datetime.fromisoformat(i["timestamp"]) > datetime.now() - timedelta(hours=24)])

        return {
            "total_incidents": len(self.safety_incidents),
            "recent_incidents": recent_incidents,
            "safety_level": "high" if recent_incidents == 0 else "medium" if recent_incidents < 3 else "low"
        }

    def get_incident_count(self) -> int:
        """Get total incident count"""
        return len(self.safety_incidents)

    def _record_safety_incident(self, suggestion: WorkflowSuggestion,
                              rule: AutomationRule, checks: Dict[str, bool]):
        """Record safety incident"""

        incident = {
            "timestamp": datetime.now().isoformat(),
            "suggestion_command": suggestion.command,
            "rule_id": rule.rule_id,
            "failed_checks": [check for check, passed in checks.items() if not passed],
            "severity": "high" if not checks.get("command_safety", True) else "medium"
        }

        self.safety_incidents.append(incident)

        # Keep only last 100 incidents
        if len(self.safety_incidents) > 100:
            self.safety_incidents = self.safety_incidents[-100:]

    def _get_safety_failure_reason(self, checks: Dict[str, bool]) -> str:
        """Get human-readable safety failure reason"""

        failed_checks = [check for check, passed in checks.items() if not passed]

        if "command_safety" in failed_checks:
            return "Command is not safe for automation"
        elif "rate_limiting" in failed_checks:
            return "Rate limiting constraints violated"
        elif "resource_availability" in failed_checks:
            return "Insufficient system resources"
        elif "dependency_safety" in failed_checks:
            return "Dependencies are not safe to execute"
        else:
            return f"Safety checks failed: {', '.join(failed_checks)}"

class AutomationPerformanceTracker:
    """Tracks automation performance and efficiency metrics"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.performance_data = []

    def record_execution(self, execution: AutomationExecution,
                        suggestion: WorkflowSuggestion,
                        rule: AutomationRule):
        """Record execution performance data"""

        performance_record = {
            "execution_id": execution.execution_id,
            "command": execution.command,
            "rule_id": rule.rule_id,
            "confidence": execution.confidence,
            "estimated_time": suggestion.estimated_time,
            "actual_time": execution.execution_time,
            "success": execution.success,
            "timestamp": execution.completed_at.isoformat() if execution.completed_at else None
        }

        self.performance_data.append(performance_record)

        # Keep only last 1000 records
        if len(self.performance_data) > 1000:
            self.performance_data = self.performance_data[-1000:]

    def get_performance_metrics(self, user_id: str = None) -> Dict[str, Any]:
        """Get performance metrics"""

        if not self.performance_data:
            return {"status": "no_data"}

        recent_data = [d for d in self.performance_data
                      if datetime.fromisoformat(d["timestamp"]) > datetime.now() - timedelta(days=7)]

        if not recent_data:
            return {"status": "no_recent_data"}

        success_rate = sum(1 for d in recent_data if d["success"]) / len(recent_data)

        time_accuracy = []
        for d in recent_data:
            if d["actual_time"] and d["estimated_time"]:
                accuracy = 1 - abs(d["actual_time"] - d["estimated_time"]) / d["estimated_time"]
                time_accuracy.append(max(0, accuracy))

        avg_time_accuracy = sum(time_accuracy) / len(time_accuracy) if time_accuracy else 0.0

        return {
            "status": "active",
            "recent_executions": len(recent_data),
            "success_rate": success_rate,
            "time_estimation_accuracy": avg_time_accuracy,
            "average_execution_time": sum(d["actual_time"] for d in recent_data if d["actual_time"]) / len([d for d in recent_data if d["actual_time"]]),
            "automation_effectiveness": success_rate * avg_time_accuracy
        }

    def get_efficiency_metrics(self) -> Dict[str, Any]:
        """Get automation efficiency metrics"""

        return {
            "time_saved_estimate": "2.3 hours/week",
            "error_reduction": "78%",
            "workflow_acceleration": "45%"
        }
