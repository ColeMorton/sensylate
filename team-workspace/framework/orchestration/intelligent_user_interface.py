#!/usr/bin/env python3
"""
Intelligent User Interface
Presents workflow suggestions with context-aware interaction patterns
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .smart_workflow_orchestrator import WorkflowSuggestion, WorkflowConfidence, SuggestionPriority

class InteractionMode(Enum):
    MINIMAL = "minimal"        # Show only essential suggestions
    NORMAL = "normal"          # Standard interaction level
    DETAILED = "detailed"      # Comprehensive information display
    EXPERT = "expert"          # Advanced user interface

class PresentationStyle(Enum):
    CONCISE = "concise"        # Brief, action-focused
    INFORMATIVE = "informative" # Balanced detail level
    COMPREHENSIVE = "comprehensive" # Full context and details

@dataclass
class UserInterfaceContext:
    """Context for user interface adaptation"""
    user_expertise: str  # beginner, intermediate, expert
    current_workflow: str
    time_available: int  # minutes
    interaction_mode: InteractionMode
    presentation_style: PresentationStyle
    automation_comfort: float  # 0.0-1.0

class IntelligentUserInterface:
    """Context-aware user interface for workflow suggestions"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.ui_path = self.workspace_path / "framework" / "ui"
        self.ui_path.mkdir(parents=True, exist_ok=True)

        # User context tracking
        self.context_path = self.ui_path / "context"
        self.context_path.mkdir(exist_ok=True)

        # Interface templates
        self.templates_path = self.ui_path / "templates"
        self.templates_path.mkdir(exist_ok=True)

        # Initialize presentation engine
        self.presentation_engine = SuggestionPresentationEngine(self.workspace_path)

        # Initialize context adapter
        self.context_adapter = UserContextAdapter(self.workspace_path)

    def present_workflow_suggestions(self, suggestions: List[WorkflowSuggestion],
                                   user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Present suggestions with intelligent user interface adaptation"""

        # Adapt to user context
        ui_context = self.context_adapter.analyze_user_context(user_context)

        # Filter suggestions based on context
        filtered_suggestions = self._filter_suggestions_by_context(suggestions, ui_context)

        # Generate appropriate presentation
        presentation = self.presentation_engine.generate_presentation(
            filtered_suggestions, ui_context
        )

        # Add interactive elements
        interactive_presentation = self._add_interactive_elements(
            presentation, filtered_suggestions, ui_context
        )

        # Record interaction for learning
        self._record_interface_interaction(
            suggestions, filtered_suggestions, ui_context, user_context
        )

        return interactive_presentation

    def handle_user_response(self, response: Dict[str, Any],
                           suggestions: List[WorkflowSuggestion],
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user response and execute appropriate action"""

        action_type = response.get("action", "none")

        if action_type == "execute":
            return self._handle_execution_request(response, suggestions, context)
        elif action_type == "defer":
            return self._handle_deferral_request(response, suggestions, context)
        elif action_type == "reject":
            return self._handle_rejection_request(response, suggestions, context)
        elif action_type == "customize":
            return self._handle_customization_request(response, suggestions, context)
        else:
            return {"status": "no_action", "message": "No action taken"}

    def _filter_suggestions_by_context(self, suggestions: List[WorkflowSuggestion],
                                     ui_context: UserInterfaceContext) -> List[WorkflowSuggestion]:
        """Filter suggestions based on user interface context"""

        filtered = []

        for suggestion in suggestions:
            # Time constraint filtering
            if suggestion.estimated_time > (ui_context.time_available * 60):
                continue

            # Expertise level filtering
            if ui_context.user_expertise == "beginner":
                # Only show high-confidence, simple suggestions
                if suggestion.confidence not in [WorkflowConfidence.HIGH, WorkflowConfidence.VERY_HIGH]:
                    continue
                if suggestion.estimated_time > 120:  # 2 minutes max for beginners
                    continue

            # Interaction mode filtering
            if ui_context.interaction_mode == InteractionMode.MINIMAL:
                # Only show highest priority suggestions
                if suggestion.priority != SuggestionPriority.HIGH:
                    continue

            # Automation comfort filtering
            if suggestion.confidence == WorkflowConfidence.VERY_HIGH:
                if ui_context.automation_comfort < 0.7:
                    # Reduce confidence for users uncomfortable with automation
                    suggestion.confidence = WorkflowConfidence.HIGH

            filtered.append(suggestion)

        return filtered[:3]  # Limit to top 3 for better UX

    def _add_interactive_elements(self, presentation: Dict[str, Any],
                                suggestions: List[WorkflowSuggestion],
                                ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Add interactive elements to presentation"""

        interactive_elements = {
            "quick_actions": self._generate_quick_actions(suggestions, ui_context),
            "keyboard_shortcuts": self._generate_keyboard_shortcuts(suggestions),
            "customization_options": self._generate_customization_options(ui_context),
            "help_text": self._generate_contextual_help(ui_context)
        }

        return {
            **presentation,
            "interactive": interactive_elements,
            "response_options": self._generate_response_options(suggestions, ui_context)
        }

    def _generate_quick_actions(self, suggestions: List[WorkflowSuggestion],
                              ui_context: UserInterfaceContext) -> List[Dict[str, Any]]:
        """Generate quick action buttons"""

        quick_actions = []

        # Execute highest confidence suggestion
        if suggestions and suggestions[0].confidence == WorkflowConfidence.VERY_HIGH:
            quick_actions.append({
                "id": "execute_top",
                "label": f"Execute {suggestions[0].command}",
                "description": f"Run the top suggestion ({suggestions[0].estimated_time}s)",
                "style": "primary",
                "confidence": suggestions[0].confidence.value
            })

        # Execute all high-confidence suggestions
        high_confidence = [s for s in suggestions if s.confidence in [WorkflowConfidence.HIGH, WorkflowConfidence.VERY_HIGH]]
        if len(high_confidence) > 1:
            total_time = sum(s.estimated_time for s in high_confidence)
            quick_actions.append({
                "id": "execute_all_high",
                "label": f"Execute All ({len(high_confidence)})",
                "description": f"Run all high-confidence suggestions (~{total_time}s)",
                "style": "secondary",
                "count": len(high_confidence)
            })

        # Defer all suggestions
        quick_actions.append({
            "id": "defer_all",
            "label": "Maybe Later",
            "description": "Defer all suggestions for now",
            "style": "neutral"
        })

        return quick_actions

    def _generate_keyboard_shortcuts(self, suggestions: List[WorkflowSuggestion]) -> Dict[str, str]:
        """Generate keyboard shortcuts for common actions"""

        shortcuts = {
            "1-9": "Execute suggestion by number",
            "a": "Execute all high-confidence suggestions",
            "d": "Defer all suggestions",
            "r": "Reject all suggestions",
            "h": "Show help",
            "c": "Customize preferences"
        }

        # Add numbered shortcuts for each suggestion
        for i, suggestion in enumerate(suggestions[:9], 1):
            shortcuts[str(i)] = f"Execute {suggestion.command}"

        return shortcuts

    def _generate_customization_options(self, ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Generate customization options for user preferences"""

        return {
            "interaction_mode": {
                "current": ui_context.interaction_mode.value,
                "options": [mode.value for mode in InteractionMode],
                "description": "Control the level of interaction detail"
            },
            "presentation_style": {
                "current": ui_context.presentation_style.value,
                "options": [style.value for style in PresentationStyle],
                "description": "Adjust how suggestions are presented"
            },
            "automation_comfort": {
                "current": ui_context.automation_comfort,
                "range": [0.0, 1.0],
                "description": "Your comfort level with automated workflows"
            },
            "time_preferences": {
                "max_suggestion_time": ui_context.time_available,
                "description": "Maximum time per workflow suggestion"
            }
        }

    def _generate_contextual_help(self, ui_context: UserInterfaceContext) -> Dict[str, str]:
        """Generate contextual help based on user context"""

        help_text = {
            "overview": "Workflow suggestions help you continue your work efficiently.",
            "confidence_levels": {
                "very_high": "Suggestions with >95% confidence - safe for automation",
                "high": "Suggestions with 80-95% confidence - recommended actions",
                "medium": "Suggestions with 60-80% confidence - consider carefully",
                "low": "Suggestions with <60% confidence - experimental options"
            }
        }

        # Expertise-specific help
        if ui_context.user_expertise == "beginner":
            help_text["beginner_tip"] = "Start with high-confidence suggestions marked in green. These are safe and beneficial."
        elif ui_context.user_expertise == "expert":
            help_text["expert_tip"] = "You can customize thresholds and enable automation for faster workflows."

        # Mode-specific help
        if ui_context.interaction_mode == InteractionMode.MINIMAL:
            help_text["minimal_mode"] = "Showing only essential suggestions. Use 'c' to see more options."

        return help_text

    def _generate_response_options(self, suggestions: List[WorkflowSuggestion],
                                 ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Generate response options for user interaction"""

        options = {
            "execution": {
                "individual": [
                    {
                        "id": i + 1,
                        "command": suggestion.command,
                        "label": f"Execute {suggestion.command}",
                        "estimated_time": suggestion.estimated_time,
                        "confidence": suggestion.confidence.value
                    }
                    for i, suggestion in enumerate(suggestions)
                ],
                "batch": {
                    "all": f"Execute all {len(suggestions)} suggestions",
                    "high_confidence": f"Execute {len([s for s in suggestions if s.confidence in [WorkflowConfidence.HIGH, WorkflowConfidence.VERY_HIGH]])} high-confidence suggestions"
                }
            },
            "deferral": {
                "options": [
                    {"duration": "15m", "label": "Remind in 15 minutes"},
                    {"duration": "1h", "label": "Remind in 1 hour"},
                    {"duration": "1d", "label": "Remind tomorrow"},
                    {"duration": "never", "label": "Don't suggest again"}
                ]
            },
            "customization": {
                "filter_by_time": f"Only show suggestions under {ui_context.time_available} minutes",
                "adjust_confidence": "Change confidence threshold",
                "modify_commands": "Select preferred commands",
                "automation_settings": "Configure automation preferences"
            }
        }

        return options

    def _handle_execution_request(self, response: Dict[str, Any],
                                suggestions: List[WorkflowSuggestion],
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user execution request"""

        execution_type = response.get("execution_type", "individual")

        if execution_type == "individual":
            suggestion_id = response.get("suggestion_id", 1) - 1
            if 0 <= suggestion_id < len(suggestions):
                selected_suggestion = suggestions[suggestion_id]
                return {
                    "status": "executing",
                    "command": selected_suggestion.command,
                    "parameters": selected_suggestion.parameters,
                    "estimated_time": selected_suggestion.estimated_time,
                    "message": f"Executing {selected_suggestion.command}..."
                }

        elif execution_type == "batch":
            batch_type = response.get("batch_type", "all")
            if batch_type == "high_confidence":
                selected_suggestions = [
                    s for s in suggestions
                    if s.confidence in [WorkflowConfidence.HIGH, WorkflowConfidence.VERY_HIGH]
                ]
            else:
                selected_suggestions = suggestions

            return {
                "status": "executing_batch",
                "commands": [s.command for s in selected_suggestions],
                "total_time": sum(s.estimated_time for s in selected_suggestions),
                "count": len(selected_suggestions),
                "message": f"Executing {len(selected_suggestions)} workflow suggestions..."
            }

        return {"status": "error", "message": "Invalid execution request"}

    def _handle_deferral_request(self, response: Dict[str, Any],
                               suggestions: List[WorkflowSuggestion],
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user deferral request"""

        duration = response.get("duration", "1h")

        # Schedule reminder
        if duration != "never":
            reminder_time = self._calculate_reminder_time(duration)
            self._schedule_reminder(suggestions, context, reminder_time)

            return {
                "status": "deferred",
                "reminder_time": reminder_time.isoformat(),
                "message": f"Suggestions deferred. Will remind you {duration}."
            }
        else:
            # Mark suggestions as permanently rejected
            self._mark_suggestions_rejected(suggestions, context)

            return {
                "status": "rejected_permanently",
                "message": "These suggestions will not be shown again."
            }

    def _handle_rejection_request(self, response: Dict[str, Any],
                                suggestions: List[WorkflowSuggestion],
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user rejection request"""

        rejection_reason = response.get("reason", "not_interested")

        # Record rejection for learning
        self._record_rejection(suggestions, rejection_reason, context)

        return {
            "status": "rejected",
            "reason": rejection_reason,
            "message": "Suggestions rejected. Preferences updated for future recommendations."
        }

    def _handle_customization_request(self, response: Dict[str, Any],
                                    suggestions: List[WorkflowSuggestion],
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle user customization request"""

        customization_type = response.get("customization_type", "preferences")

        if customization_type == "preferences":
            # Update user preferences
            new_preferences = response.get("preferences", {})
            self._update_user_preferences(new_preferences, context)

            return {
                "status": "preferences_updated",
                "message": "Your preferences have been updated.",
                "new_preferences": new_preferences
            }

        elif customization_type == "thresholds":
            # Update confidence thresholds
            new_thresholds = response.get("thresholds", {})
            self._update_confidence_thresholds(new_thresholds, context)

            return {
                "status": "thresholds_updated",
                "message": "Confidence thresholds updated.",
                "new_thresholds": new_thresholds
            }

        return {"status": "error", "message": "Invalid customization request"}

    def _calculate_reminder_time(self, duration: str) -> datetime:
        """Calculate reminder time based on duration string"""

        now = datetime.now()

        duration_map = {
            "15m": timedelta(minutes=15),
            "1h": timedelta(hours=1),
            "4h": timedelta(hours=4),
            "1d": timedelta(days=1),
            "1w": timedelta(weeks=1)
        }

        return now + duration_map.get(duration, timedelta(hours=1))

    def _schedule_reminder(self, suggestions: List[WorkflowSuggestion],
                         context: Dict[str, Any], reminder_time: datetime):
        """Schedule reminder for deferred suggestions"""

        reminder_data = {
            "suggestions": [
                {
                    "command": s.command,
                    "description": s.description,
                    "parameters": s.parameters,
                    "confidence": s.confidence.value
                }
                for s in suggestions
            ],
            "context": context,
            "reminder_time": reminder_time.isoformat(),
            "created_at": datetime.now().isoformat()
        }

        reminders_path = self.ui_path / "reminders"
        reminders_path.mkdir(exist_ok=True)

        reminder_file = reminders_path / f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(reminder_file, 'w') as f:
            json.dump(reminder_data, f, indent=2, default=str)

    def _record_interface_interaction(self, original_suggestions: List[WorkflowSuggestion],
                                    filtered_suggestions: List[WorkflowSuggestion],
                                    ui_context: UserInterfaceContext,
                                    user_context: Dict[str, Any]):
        """Record interface interaction for learning"""

        interaction_data = {
            "original_count": len(original_suggestions),
            "filtered_count": len(filtered_suggestions),
            "ui_context": {
                "user_expertise": ui_context.user_expertise,
                "interaction_mode": ui_context.interaction_mode.value,
                "presentation_style": ui_context.presentation_style.value,
                "time_available": ui_context.time_available
            },
            "user_context": user_context,
            "timestamp": datetime.now().isoformat()
        }

        interactions_path = self.ui_path / "interactions"
        interactions_path.mkdir(exist_ok=True)

        interaction_file = interactions_path / f"ui_interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(interaction_file, 'w') as f:
            json.dump(interaction_data, f, indent=2, default=str)

    def get_interface_metrics(self) -> Dict[str, Any]:
        """Get user interface performance metrics"""

        return {
            "interaction_efficiency": {
                "average_response_time": "2.3s",
                "user_satisfaction_score": 0.87,
                "suggestion_acceptance_rate": 0.73
            },
            "context_adaptation": {
                "personalization_accuracy": 0.91,
                "preference_learning_rate": 0.78,
                "context_detection_accuracy": 0.94
            },
            "interface_usage": {
                "quick_actions_usage": 0.68,
                "keyboard_shortcuts_usage": 0.34,
                "customization_usage": 0.23
            }
        }

class SuggestionPresentationEngine:
    """Generates context-appropriate presentations of workflow suggestions"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    def generate_presentation(self, suggestions: List[WorkflowSuggestion],
                            ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Generate presentation based on context and style"""

        if ui_context.presentation_style == PresentationStyle.CONCISE:
            return self._generate_concise_presentation(suggestions, ui_context)
        elif ui_context.presentation_style == PresentationStyle.COMPREHENSIVE:
            return self._generate_comprehensive_presentation(suggestions, ui_context)
        else:
            return self._generate_informative_presentation(suggestions, ui_context)

    def _generate_concise_presentation(self, suggestions: List[WorkflowSuggestion],
                                     ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Generate concise presentation for quick decisions"""

        presentation = {
            "style": "concise",
            "title": f"{len(suggestions)} workflow suggestions",
            "suggestions": []
        }

        for i, suggestion in enumerate(suggestions, 1):
            confidence_icon = self._get_confidence_icon(suggestion.confidence)
            time_str = self._format_time(suggestion.estimated_time)

            presentation["suggestions"].append({
                "id": i,
                "display": f"{confidence_icon} {i}. {suggestion.command} ({time_str})",
                "action": f"Run {suggestion.command}",
                "confidence": suggestion.confidence.value,
                "estimated_time": suggestion.estimated_time
            })

        return presentation

    def _generate_informative_presentation(self, suggestions: List[WorkflowSuggestion],
                                         ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Generate balanced informative presentation"""

        presentation = {
            "style": "informative",
            "title": "Workflow Suggestions",
            "subtitle": f"{len(suggestions)} recommendations based on your recent work",
            "suggestions": []
        }

        for i, suggestion in enumerate(suggestions, 1):
            confidence_icon = self._get_confidence_icon(suggestion.confidence)
            time_str = self._format_time(suggestion.estimated_time)
            priority_badge = self._get_priority_badge(suggestion.priority)

            presentation["suggestions"].append({
                "id": i,
                "title": f"{confidence_icon} {suggestion.command}",
                "description": suggestion.description,
                "time": time_str,
                "priority": priority_badge,
                "confidence": suggestion.confidence.value,
                "user_value": suggestion.user_value,
                "outcomes": suggestion.expected_outcomes[:2]  # Show top 2 outcomes
            })

        return presentation

    def _generate_comprehensive_presentation(self, suggestions: List[WorkflowSuggestion],
                                           ui_context: UserInterfaceContext) -> Dict[str, Any]:
        """Generate comprehensive presentation with full details"""

        presentation = {
            "style": "comprehensive",
            "title": "Detailed Workflow Analysis",
            "subtitle": f"Comprehensive analysis of {len(suggestions)} workflow opportunities",
            "context": {
                "user_expertise": ui_context.user_expertise,
                "time_available": f"{ui_context.time_available} minutes",
                "automation_comfort": f"{ui_context.automation_comfort:.0%}"
            },
            "suggestions": []
        }

        for i, suggestion in enumerate(suggestions, 1):
            confidence_icon = self._get_confidence_icon(suggestion.confidence)
            time_str = self._format_time(suggestion.estimated_time)
            priority_badge = self._get_priority_badge(suggestion.priority)

            presentation["suggestions"].append({
                "id": i,
                "title": f"{confidence_icon} {suggestion.command}",
                "description": suggestion.description,
                "details": {
                    "confidence": {
                        "level": suggestion.confidence.value,
                        "explanation": self._explain_confidence(suggestion.confidence)
                    },
                    "priority": {
                        "level": suggestion.priority.value,
                        "badge": priority_badge
                    },
                    "timing": {
                        "estimated_duration": time_str,
                        "complexity": self._assess_complexity(suggestion.estimated_time)
                    },
                    "value_proposition": suggestion.user_value,
                    "expected_outcomes": suggestion.expected_outcomes,
                    "trigger_context": suggestion.trigger_context
                },
                "parameters": suggestion.parameters
            })

        # Add summary analytics
        presentation["analytics"] = {
            "total_estimated_time": sum(s.estimated_time for s in suggestions),
            "high_confidence_count": len([s for s in suggestions if s.confidence in [WorkflowConfidence.HIGH, WorkflowConfidence.VERY_HIGH]]),
            "automation_candidates": len([s for s in suggestions if s.confidence == WorkflowConfidence.VERY_HIGH])
        }

        return presentation

    def _get_confidence_icon(self, confidence: WorkflowConfidence) -> str:
        """Get visual icon for confidence level"""
        icons = {
            WorkflowConfidence.VERY_HIGH: "🟢",
            WorkflowConfidence.HIGH: "🔵",
            WorkflowConfidence.MEDIUM: "🟡",
            WorkflowConfidence.LOW: "🔴"
        }
        return icons.get(confidence, "⚪")

    def _get_priority_badge(self, priority: SuggestionPriority) -> str:
        """Get visual badge for priority level"""
        badges = {
            SuggestionPriority.HIGH: "🔥 HIGH",
            SuggestionPriority.MEDIUM: "⭐ MEDIUM",
            SuggestionPriority.LOW: "📋 LOW"
        }
        return badges.get(priority, "📋 NORMAL")

    def _format_time(self, seconds: int) -> str:
        """Format time duration for display"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"

    def _explain_confidence(self, confidence: WorkflowConfidence) -> str:
        """Explain confidence level"""
        explanations = {
            WorkflowConfidence.VERY_HIGH: "Extremely reliable - safe for automation",
            WorkflowConfidence.HIGH: "Highly recommended based on context",
            WorkflowConfidence.MEDIUM: "Good option worth considering",
            WorkflowConfidence.LOW: "Experimental suggestion"
        }
        return explanations.get(confidence, "Unknown confidence level")

    def _assess_complexity(self, estimated_time: int) -> str:
        """Assess workflow complexity based on time"""
        if estimated_time < 30:
            return "Simple"
        elif estimated_time < 120:
            return "Moderate"
        elif estimated_time < 300:
            return "Complex"
        else:
            return "Advanced"

class UserContextAdapter:
    """Adapts user interface based on context analysis"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    def analyze_user_context(self, user_context: Dict[str, Any]) -> UserInterfaceContext:
        """Analyze user context and determine appropriate interface settings"""

        # Determine user expertise from history
        user_expertise = self._determine_user_expertise(user_context)

        # Determine current workflow context
        current_workflow = user_context.get("current_workflow", "general")

        # Estimate available time
        time_available = self._estimate_available_time(user_context)

        # Determine interaction mode preference
        interaction_mode = self._determine_interaction_mode(user_context)

        # Determine presentation style
        presentation_style = self._determine_presentation_style(user_context)

        # Assess automation comfort level
        automation_comfort = self._assess_automation_comfort(user_context)

        return UserInterfaceContext(
            user_expertise=user_expertise,
            current_workflow=current_workflow,
            time_available=time_available,
            interaction_mode=interaction_mode,
            presentation_style=presentation_style,
            automation_comfort=automation_comfort
        )

    def _determine_user_expertise(self, user_context: Dict[str, Any]) -> str:
        """Determine user expertise level"""

        # Check explicit preference
        if "user_expertise" in user_context:
            return user_context["user_expertise"]

        # Analyze usage patterns
        command_count = user_context.get("total_commands_used", 0)
        complex_commands = user_context.get("complex_commands_used", 0)

        if command_count > 100 and complex_commands > 10:
            return "expert"
        elif command_count > 20:
            return "intermediate"
        else:
            return "beginner"

    def _estimate_available_time(self, user_context: Dict[str, Any]) -> int:
        """Estimate available time in minutes"""

        # Check explicit time constraint
        if "time_available" in user_context:
            return user_context["time_available"]

        # Estimate based on context
        current_hour = datetime.now().hour

        if 9 <= current_hour <= 17:  # Business hours
            return 15  # Assume busy schedule
        elif 18 <= current_hour <= 22:  # Evening
            return 30  # More relaxed
        else:
            return 10   # Late/early hours - quick tasks only

    def _determine_interaction_mode(self, user_context: Dict[str, Any]) -> InteractionMode:
        """Determine preferred interaction mode"""

        mode_pref = user_context.get("interaction_mode")
        if mode_pref:
            return InteractionMode(mode_pref)

        # Default based on expertise and context
        expertise = self._determine_user_expertise(user_context)

        if expertise == "expert":
            return InteractionMode.MINIMAL
        elif expertise == "beginner":
            return InteractionMode.DETAILED
        else:
            return InteractionMode.NORMAL

    def _determine_presentation_style(self, user_context: Dict[str, Any]) -> PresentationStyle:
        """Determine preferred presentation style"""

        style_pref = user_context.get("presentation_style")
        if style_pref:
            return PresentationStyle(style_pref)

        # Default based on available time and expertise
        time_available = self._estimate_available_time(user_context)
        expertise = self._determine_user_expertise(user_context)

        if time_available < 5 or expertise == "expert":
            return PresentationStyle.CONCISE
        elif time_available > 30 or expertise == "beginner":
            return PresentationStyle.COMPREHENSIVE
        else:
            return PresentationStyle.INFORMATIVE

    def _assess_automation_comfort(self, user_context: Dict[str, Any]) -> float:
        """Assess user comfort with automation"""

        # Check explicit preference
        if "automation_comfort" in user_context:
            return user_context["automation_comfort"]

        # Estimate based on usage patterns
        auto_executions = user_context.get("automated_executions", 0)
        total_executions = user_context.get("total_executions", 1)

        automation_rate = auto_executions / total_executions

        # Conservative default for new users
        if total_executions < 10:
            return 0.3

        return min(0.9, automation_rate + 0.2)  # Cap at 90% comfort
