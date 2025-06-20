#!/usr/bin/env python3
"""
Team-Workspace Pre-Execution Consultation System

Prevents duplicate analysis by checking existing knowledge before command execution.
Provides decision guidance for update-vs-new analysis scenarios.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import re

class PreExecutionConsultant:
    """Provides consultation before command execution to prevent duplication."""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"
        self.superseding_log_path = self.workspace_path / "coordination" / "superseding-log.yaml"

    def consult_before_execution(self, command_name: str, proposed_topic: str,
                               proposed_scope: str = "") -> Dict[str, any]:
        """
        Main consultation entry point for commands before execution.

        Args:
            command_name: Name of the executing command (e.g., 'architect', 'code-owner')
            proposed_topic: Topic the command intends to analyze
            proposed_scope: Brief description of intended analysis scope

        Returns:
            Consultation result with recommendation and existing knowledge
        """
        # Load current registry state
        registry = self._load_registry()
        if not registry:
            return self._create_consultation_result("proceed", "No registry found - safe to proceed")

        # Check for existing knowledge on this topic
        existing_knowledge = self._find_existing_knowledge(proposed_topic, registry)

        # Determine ownership and authority
        ownership_status = self._check_ownership(command_name, proposed_topic, registry)

        # Analyze freshness and need for update
        freshness_analysis = self._analyze_freshness(existing_knowledge)

        # Generate recommendation
        recommendation = self._generate_recommendation(
            existing_knowledge, ownership_status, freshness_analysis, proposed_scope
        )

        return {
            "recommendation": recommendation["action"],
            "rationale": recommendation["rationale"],
            "existing_knowledge": existing_knowledge,
            "ownership_status": ownership_status,
            "freshness_analysis": freshness_analysis,
            "suggested_actions": recommendation["suggested_actions"],
            "consultation_timestamp": datetime.now().isoformat()
        }

    def declare_superseding_intent(self, command_name: str, topic: str,
                                 superseding_files: List[str], reason: str) -> Dict[str, any]:
        """
        Declare intent to supersede existing content with new analysis.

        Args:
            command_name: Command declaring superseding intent
            topic: Topic being superseded
            superseding_files: List of files that will be superseded
            reason: Reason for superseding

        Returns:
            Superseding approval and guidance
        """
        registry = self._load_registry()

        # Validate superseding request
        validation = self._validate_superseding_request(
            command_name, topic, superseding_files, reason, registry
        )

        if validation["approved"]:
            # Log superseding intent
            self._log_superseding_intent(command_name, topic, superseding_files, reason)

        return {
            "superseding_approved": validation["approved"],
            "superseding_id": validation.get("superseding_id"),
            "validation_notes": validation["notes"],
            "next_steps": validation["next_steps"],
            "timestamp": datetime.now().isoformat()
        }

    def get_topic_ownership_guidance(self, command_name: str, topic: str) -> Dict[str, any]:
        """Get guidance on topic ownership and collaboration requirements."""
        registry = self._load_registry()
        if not registry:
            return {"guidance": "No registry - proceed with caution"}

        # Check command ownership mapping
        ownership_map = registry.get("command_ownership", {})
        command_topics = ownership_map.get(command_name, {})

        is_primary_owner = topic in command_topics.get("primary_topics", [])
        is_secondary_owner = topic in command_topics.get("secondary_topics", [])

        # Find primary owner if not this command
        primary_owner = None
        for cmd, cmd_topics in ownership_map.items():
            if topic in cmd_topics.get("primary_topics", []):
                primary_owner = cmd
                break

        guidance = {
            "ownership_status": "primary" if is_primary_owner else "secondary" if is_secondary_owner else "none",
            "primary_owner": primary_owner,
            "collaboration_required": not is_primary_owner and primary_owner is not None,
            "recommended_action": self._get_ownership_recommendation(
                is_primary_owner, is_secondary_owner, primary_owner, command_name
            )
        }

        return guidance

    def _load_registry(self) -> Optional[Dict]:
        """Load topic registry."""
        try:
            if self.registry_path.exists():
                return yaml.safe_load(self.registry_path.read_text())
        except Exception:
            pass
        return None

    def _find_existing_knowledge(self, proposed_topic: str, registry: Dict) -> Optional[Dict]:
        """Find existing knowledge related to the proposed topic."""
        topics = registry.get("topics", {})

        # Direct topic match
        if proposed_topic in topics:
            return {
                "exact_match": True,
                "topic_name": proposed_topic,
                "topic_data": topics[proposed_topic]
            }

        # Fuzzy matching for related topics
        related_topics = []
        topic_keywords = set(proposed_topic.lower().split('-'))

        for topic_name, topic_data in topics.items():
            existing_keywords = set(topic_name.lower().split('-'))
            keyword_overlap = len(topic_keywords & existing_keywords)

            if keyword_overlap >= 2:  # At least 2 keyword overlap
                related_topics.append({
                    "topic_name": topic_name,
                    "topic_data": topic_data,
                    "keyword_overlap": keyword_overlap
                })

        if related_topics:
            # Sort by keyword overlap
            related_topics.sort(key=lambda x: x["keyword_overlap"], reverse=True)
            return {
                "exact_match": False,
                "related_topics": related_topics
            }

        return None

    def _check_ownership(self, command_name: str, topic: str, registry: Dict) -> Dict[str, any]:
        """Check ownership status for command and topic."""
        ownership_map = registry.get("command_ownership", {})
        command_topics = ownership_map.get(command_name, {})

        is_primary = topic in command_topics.get("primary_topics", [])
        is_secondary = topic in command_topics.get("secondary_topics", [])

        # Find actual primary owner
        primary_owner = None
        for cmd, cmd_topics in ownership_map.items():
            if topic in cmd_topics.get("primary_topics", []):
                primary_owner = cmd
                break

        return {
            "is_primary_owner": is_primary,
            "is_secondary_owner": is_secondary,
            "primary_owner": primary_owner,
            "has_ownership": is_primary or is_secondary
        }

    def _analyze_freshness(self, existing_knowledge: Optional[Dict]) -> Dict[str, any]:
        """Analyze freshness of existing knowledge."""
        if not existing_knowledge or not existing_knowledge.get("exact_match"):
            return {"needs_update": False, "reason": "No existing knowledge"}

        topic_data = existing_knowledge["topic_data"]
        last_updated = topic_data.get("last_updated")
        freshness_threshold = topic_data.get("freshness_threshold_days", 30)

        if not last_updated:
            return {"needs_update": True, "reason": "No last_updated timestamp"}

        try:
            last_update_date = datetime.strptime(last_updated, "%Y-%m-%d")
            days_since_update = (datetime.now() - last_update_date).days

            is_stale = days_since_update > freshness_threshold

            return {
                "needs_update": is_stale,
                "days_since_update": days_since_update,
                "freshness_threshold": freshness_threshold,
                "reason": f"Content is {days_since_update} days old, threshold is {freshness_threshold} days"
            }
        except ValueError:
            return {"needs_update": True, "reason": "Invalid last_updated format"}

    def _generate_recommendation(self, existing_knowledge: Optional[Dict],
                               ownership_status: Dict, freshness_analysis: Dict,
                               proposed_scope: str) -> Dict[str, any]:
        """Generate execution recommendation based on consultation analysis."""

        # No existing knowledge - proceed
        if not existing_knowledge:
            return {
                "action": "proceed",
                "rationale": "No existing knowledge found on this topic",
                "suggested_actions": ["Create new analysis", "Establish topic ownership"]
            }

        # Existing knowledge with exact match
        if existing_knowledge.get("exact_match"):
            topic_data = existing_knowledge["topic_data"]

            # Check if needs update due to staleness
            if freshness_analysis.get("needs_update"):
                if ownership_status["is_primary_owner"]:
                    return {
                        "action": "update_existing",
                        "rationale": f"Content is stale: {freshness_analysis['reason']}",
                        "suggested_actions": [
                            "Update existing authority file",
                            "Archive previous version",
                            "Update topic registry"
                        ]
                    }
                else:
                    return {
                        "action": "coordinate",
                        "rationale": f"Content needs update but you're not primary owner (owner: {ownership_status['primary_owner']})",
                        "suggested_actions": [
                            "Coordinate with primary owner",
                            "Propose collaborative update",
                            "Consider secondary analysis approach"
                        ]
                    }

            # Fresh content exists
            else:
                if ownership_status["is_primary_owner"]:
                    return {
                        "action": "consider_necessity",
                        "rationale": "Fresh analysis already exists and you're the owner",
                        "suggested_actions": [
                            "Review existing analysis for completeness",
                            "Consider if new scope adds value",
                            "Update existing analysis if needed"
                        ]
                    }
                else:
                    return {
                        "action": "avoid_duplication",
                        "rationale": "Fresh analysis exists and you're not the primary owner",
                        "suggested_actions": [
                            "Review existing analysis",
                            "Reference existing work",
                            "Coordinate with primary owner if additional analysis needed"
                        ]
                    }

        # Related topics found
        else:
            related_topics = existing_knowledge["related_topics"]
            return {
                "action": "review_related",
                "rationale": f"Found {len(related_topics)} related topic(s) that may overlap",
                "suggested_actions": [
                    "Review related topics for overlap",
                    "Consider extending existing analysis",
                    "Ensure clear scope differentiation"
                ]
            }

    def _validate_superseding_request(self, command_name: str, topic: str,
                                    superseding_files: List[str], reason: str,
                                    registry: Dict) -> Dict[str, any]:
        """Validate superseding request against policies."""

        # Check if topic is protected
        policies = registry.get("superseding_policies", {})
        protected_topics = policies.get("protection_rules", {}).get("protected_topics", [])

        if topic in protected_topics:
            return {
                "approved": False,
                "notes": f"Topic '{topic}' is protected and requires manual approval",
                "next_steps": ["Request manual approval from architect or product-owner"]
            }

        # Check ownership permissions
        ownership_map = registry.get("command_ownership", {})
        command_topics = ownership_map.get(command_name, {})

        has_permission = (
            topic in command_topics.get("primary_topics", []) or
            topic in command_topics.get("secondary_topics", [])
        )

        if not has_permission:
            return {
                "approved": False,
                "notes": f"Command '{command_name}' lacks ownership permission for topic '{topic}'",
                "next_steps": ["Coordinate with topic owner", "Request permission"]
            }

        # Generate superseding ID
        superseding_id = f"supersede_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        return {
            "approved": True,
            "superseding_id": superseding_id,
            "notes": "Superseding request approved",
            "next_steps": ["Proceed with analysis", "Log superseding when complete"]
        }

    def _log_superseding_intent(self, command_name: str, topic: str,
                              superseding_files: List[str], reason: str):
        """Log superseding intent to audit trail."""
        try:
            superseding_log = yaml.safe_load(self.superseding_log_path.read_text()) if self.superseding_log_path.exists() else {}

            event_id = f"supersede_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            new_event = {
                "event_id": event_id,
                "timestamp": datetime.now().isoformat(),
                "event_type": "superseding_intent",
                "description": f"Intent to supersede {topic} declared by {command_name}",
                "superseded_files": superseding_files,
                "superseding_files": [],  # Will be filled when actual superseding occurs
                "topic": topic,
                "initiated_by": command_name,
                "reason": reason,
                "validation_status": "intent_logged"
            }

            if "superseding_events" not in superseding_log:
                superseding_log["superseding_events"] = []

            superseding_log["superseding_events"].append(new_event)

            # Write back to file
            self.superseding_log_path.write_text(yaml.dump(superseding_log, default_flow_style=False))

        except Exception as e:
            print(f"Warning: Could not log superseding intent: {e}")

    def _get_ownership_recommendation(self, is_primary: bool, is_secondary: bool,
                                    primary_owner: Optional[str], command_name: str) -> str:
        """Get ownership-based recommendation."""
        if is_primary:
            return "You are the primary owner - proceed with analysis"
        elif is_secondary:
            return f"You are a secondary owner - coordinate with primary owner ({primary_owner})"
        elif primary_owner:
            return f"Topic owned by {primary_owner} - coordination required"
        else:
            return "No established ownership - you can claim ownership"

    def _create_consultation_result(self, action: str, rationale: str) -> Dict[str, any]:
        """Create a basic consultation result."""
        return {
            "recommendation": action,
            "rationale": rationale,
            "existing_knowledge": None,
            "ownership_status": {"has_ownership": False},
            "freshness_analysis": {"needs_update": False},
            "suggested_actions": [],
            "consultation_timestamp": datetime.now().isoformat()
        }

def main():
    """CLI interface for pre-execution consultation."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python pre-execution-consultation.py <command_name> <topic> [scope]")
        print("Example: python pre-execution-consultation.py architect technical-health 'comprehensive analysis'")
        sys.exit(1)

    command_name = sys.argv[1]
    topic = sys.argv[2]
    scope = sys.argv[3] if len(sys.argv) > 3 else ""

    consultant = PreExecutionConsultant()
    result = consultant.consult_before_execution(command_name, topic, scope)

    print(f"Pre-Execution Consultation Results for {command_name} → {topic}")
    print("=" * 60)
    print(f"Recommendation: {result['recommendation'].upper()}")
    print(f"Rationale: {result['rationale']}")

    if result['existing_knowledge']:
        print(f"\nExisting Knowledge: Found")
        if result['existing_knowledge'].get('exact_match'):
            topic_data = result['existing_knowledge']['topic_data']
            print(f"  Authority: {topic_data.get('current_authority', 'N/A')}")
            print(f"  Owner: {topic_data.get('owner_command', 'N/A')}")
            print(f"  Last Updated: {topic_data.get('last_updated', 'N/A')}")

    if result['suggested_actions']:
        print(f"\nSuggested Actions:")
        for action in result['suggested_actions']:
            print(f"  • {action}")

if __name__ == "__main__":
    main()
