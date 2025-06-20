#!/usr/bin/env python3
"""
Team-Workspace Decision Tree System

Provides structured decision guidance for commands determining whether to
create new analysis, update existing content, or coordinate with other commands.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

class DecisionType(Enum):
    """Types of decisions the system can make."""
    PROCEED_NEW = "proceed_new"
    UPDATE_EXISTING = "update_existing"
    COORDINATE_REQUIRED = "coordinate_required"
    AVOID_DUPLICATION = "avoid_duplication"
    CLAIM_OWNERSHIP = "claim_ownership"
    REFERENCE_EXISTING = "reference_existing"

class DecisionTree:
    """Decision tree for content creation and update decisions."""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"

    def make_decision(self, command_name: str, proposed_topic: str,
                     proposed_scope: str = "", force_new: bool = False) -> Dict[str, any]:
        """
        Make a structured decision about whether and how to proceed with analysis.

        Args:
            command_name: Command requesting decision
            proposed_topic: Topic for analysis
            proposed_scope: Scope or description of intended analysis
            force_new: Whether to force creation of new analysis

        Returns:
            Decision with rationale and action steps
        """
        # Load necessary data
        registry = self._load_registry()
        if not registry:
            return self._create_decision(
                DecisionType.PROCEED_NEW,
                "No registry found - safe to proceed with new analysis",
                ["Create new analysis", "Establish topic ownership"]
            )

        # Execute decision tree logic
        decision_context = self._gather_decision_context(
            command_name, proposed_topic, proposed_scope, registry
        )

        if force_new:
            return self._handle_forced_new_analysis(decision_context)

        return self._execute_decision_tree(decision_context)

    def _gather_decision_context(self, command_name: str, proposed_topic: str,
                               proposed_scope: str, registry: Dict) -> Dict[str, any]:
        """Gather all information needed for decision making."""

        # Check for existing knowledge
        existing_knowledge = self._find_existing_knowledge(proposed_topic, registry)

        # Check ownership status
        ownership_status = self._check_ownership_status(command_name, proposed_topic, registry)

        # Analyze content freshness
        freshness_analysis = self._analyze_content_freshness(existing_knowledge)

        # Check for related/competing work
        related_work = self._find_related_work(proposed_topic, proposed_scope, registry)

        # Assess scope overlap
        scope_analysis = self._analyze_scope_overlap(proposed_scope, existing_knowledge, related_work)

        return {
            "command_name": command_name,
            "proposed_topic": proposed_topic,
            "proposed_scope": proposed_scope,
            "existing_knowledge": existing_knowledge,
            "ownership_status": ownership_status,
            "freshness_analysis": freshness_analysis,
            "related_work": related_work,
            "scope_analysis": scope_analysis,
            "registry": registry
        }

    def _execute_decision_tree(self, context: Dict[str, any]) -> Dict[str, any]:
        """Execute the main decision tree logic."""

        # Decision Node 1: Does exact topic knowledge exist?
        if not context["existing_knowledge"]:
            return self._handle_no_existing_knowledge(context)

        # Decision Node 2: Is existing knowledge stale?
        if context["freshness_analysis"]["is_stale"]:
            return self._handle_stale_knowledge(context)

        # Decision Node 3: Are you the owner?
        if context["ownership_status"]["is_primary_owner"]:
            return self._handle_primary_owner_scenario(context)
        elif context["ownership_status"]["is_secondary_owner"]:
            return self._handle_secondary_owner_scenario(context)
        else:
            return self._handle_non_owner_scenario(context)

    def _handle_no_existing_knowledge(self, context: Dict[str, any]) -> Dict[str, any]:
        """Handle case where no existing knowledge exists on the topic."""

        # Check if there's related work that might overlap
        if context["related_work"]:
            high_overlap_work = [work for work in context["related_work"]
                               if work.get("overlap_score", 0) > 0.7]

            if high_overlap_work:
                return self._create_decision(
                    DecisionType.COORDINATE_REQUIRED,
                    f"No exact match but found {len(high_overlap_work)} highly related topics",
                    [
                        "Review related work for potential overlap",
                        "Consider extending existing analysis instead",
                        "Coordinate with related topic owners"
                    ],
                    related_topics=[work["topic"] for work in high_overlap_work]
                )

        # No existing knowledge and no high overlap - safe to proceed
        if context["ownership_status"]["topic_has_no_owner"]:
            return self._create_decision(
                DecisionType.CLAIM_OWNERSHIP,
                "No existing knowledge and topic is unowned",
                [
                    "Claim primary ownership of topic",
                    "Create new authoritative analysis",
                    "Establish topic in registry"
                ]
            )
        else:
            return self._create_decision(
                DecisionType.PROCEED_NEW,
                "No existing knowledge found - safe to create new analysis",
                [
                    "Create new analysis",
                    "Coordinate with any related topic owners",
                    "Establish clear scope boundaries"
                ]
            )

    def _handle_stale_knowledge(self, context: Dict[str, any]) -> Dict[str, any]:
        """Handle case where existing knowledge is stale."""

        if context["ownership_status"]["is_primary_owner"]:
            return self._create_decision(
                DecisionType.UPDATE_EXISTING,
                f"You own stale content ({context['freshness_analysis']['staleness_reason']})",
                [
                    "Update existing authoritative content",
                    "Archive previous version",
                    "Update topic registry with new timestamp"
                ],
                existing_authority=context["existing_knowledge"]["authority_path"]
            )

        elif context["ownership_status"]["is_secondary_owner"]:
            primary_owner = context["ownership_status"]["primary_owner"]
            return self._create_decision(
                DecisionType.COORDINATE_REQUIRED,
                f"Stale content exists but primary owner is {primary_owner}",
                [
                    f"Coordinate with primary owner ({primary_owner})",
                    "Propose collaborative update",
                    "Consider secondary analysis if scope differs"
                ],
                coordination_required_with=primary_owner
            )

        else:
            primary_owner = context["ownership_status"]["primary_owner"]
            return self._create_decision(
                DecisionType.COORDINATE_REQUIRED,
                f"Stale content exists but you're not an owner (owner: {primary_owner})",
                [
                    f"Contact primary owner ({primary_owner}) about update needs",
                    "Propose collaboration or assistance",
                    "Consider whether new analysis adds distinct value"
                ],
                coordination_required_with=primary_owner
            )

    def _handle_primary_owner_scenario(self, context: Dict[str, any]) -> Dict[str, any]:
        """Handle case where command is primary owner of fresh content."""

        # Check if new scope adds value
        scope_adds_value = context["scope_analysis"]["adds_new_value"]

        if scope_adds_value:
            return self._create_decision(
                DecisionType.UPDATE_EXISTING,
                "You own fresh content but new scope adds value",
                [
                    "Extend existing authoritative analysis",
                    "Update with new scope/findings",
                    "Maintain single authoritative source"
                ],
                existing_authority=context["existing_knowledge"]["authority_path"]
            )
        else:
            return self._create_decision(
                DecisionType.REFERENCE_EXISTING,
                "You own fresh, comprehensive content",
                [
                    "Reference existing authoritative analysis",
                    "Consider if any updates are truly needed",
                    "Avoid unnecessary duplication"
                ],
                existing_authority=context["existing_knowledge"]["authority_path"]
            )

    def _handle_secondary_owner_scenario(self, context: Dict[str, any]) -> Dict[str, any]:
        """Handle case where command is secondary owner."""

        primary_owner = context["ownership_status"]["primary_owner"]
        scope_differs = context["scope_analysis"]["scope_differs_significantly"]

        if scope_differs:
            return self._create_decision(
                DecisionType.COORDINATE_REQUIRED,
                f"Fresh content exists but your scope differs (primary: {primary_owner})",
                [
                    f"Coordinate with primary owner ({primary_owner})",
                    "Clarify scope differentiation",
                    "Consider complementary analysis approach"
                ],
                coordination_required_with=primary_owner
            )
        else:
            return self._create_decision(
                DecisionType.REFERENCE_EXISTING,
                f"Fresh content covers your scope (primary: {primary_owner})",
                [
                    "Reference existing authoritative analysis",
                    f"Coordinate with {primary_owner} if updates needed",
                    "Avoid duplicating existing work"
                ],
                existing_authority=context["existing_knowledge"]["authority_path"]
            )

    def _handle_non_owner_scenario(self, context: Dict[str, any]) -> Dict[str, any]:
        """Handle case where command is not an owner of existing fresh content."""

        primary_owner = context["ownership_status"]["primary_owner"]
        scope_differs = context["scope_analysis"]["scope_differs_significantly"]

        if scope_differs:
            return self._create_decision(
                DecisionType.COORDINATE_REQUIRED,
                f"Fresh content exists but scope differs (owner: {primary_owner})",
                [
                    f"Coordinate with owner ({primary_owner})",
                    "Clarify scope boundaries",
                    "Request secondary ownership if appropriate"
                ],
                coordination_required_with=primary_owner
            )
        else:
            return self._create_decision(
                DecisionType.AVOID_DUPLICATION,
                f"Fresh content covers your scope (owner: {primary_owner})",
                [
                    "Reference existing authoritative analysis",
                    f"Coordinate with {primary_owner} if additional perspective needed",
                    "Avoid creating duplicate analysis"
                ],
                existing_authority=context["existing_knowledge"]["authority_path"]
            )

    def _handle_forced_new_analysis(self, context: Dict[str, any]) -> Dict[str, any]:
        """Handle case where new analysis is forced despite existing content."""

        warnings = []
        if context["existing_knowledge"]:
            warnings.append("Forcing new analysis despite existing content")

        if not context["ownership_status"]["has_any_ownership"]:
            warnings.append("Creating analysis without topic ownership")

        return self._create_decision(
            DecisionType.PROCEED_NEW,
            "Forced creation of new analysis (override mode)",
            [
                "Create new analysis as requested",
                "Declare superseding intent if appropriate",
                "Ensure clear differentiation from existing work"
            ],
            warnings=warnings
        )

    def _find_existing_knowledge(self, topic: str, registry: Dict) -> Optional[Dict]:
        """Find existing knowledge for the exact topic."""
        topics = registry.get("topics", {})

        if topic in topics:
            topic_data = topics[topic]
            return {
                "exists": True,
                "topic_name": topic,
                "authority_path": topic_data.get("current_authority"),
                "owner": topic_data.get("owner_command"),
                "last_updated": topic_data.get("last_updated"),
                "status": topic_data.get("status"),
                "topic_data": topic_data
            }

        return None

    def _check_ownership_status(self, command_name: str, topic: str, registry: Dict) -> Dict[str, any]:
        """Check ownership status for command and topic."""
        ownership_map = registry.get("command_ownership", {})
        command_topics = ownership_map.get(command_name, {})

        is_primary = topic in command_topics.get("primary_topics", [])
        is_secondary = topic in command_topics.get("secondary_topics", [])

        # Find primary owner
        primary_owner = None
        for cmd, cmd_topics in ownership_map.items():
            if topic in cmd_topics.get("primary_topics", []):
                primary_owner = cmd
                break

        return {
            "is_primary_owner": is_primary,
            "is_secondary_owner": is_secondary,
            "has_any_ownership": is_primary or is_secondary,
            "primary_owner": primary_owner,
            "topic_has_no_owner": primary_owner is None
        }

    def _analyze_content_freshness(self, existing_knowledge: Optional[Dict]) -> Dict[str, any]:
        """Analyze freshness of existing content."""
        if not existing_knowledge:
            return {"is_stale": False, "reason": "No existing content"}

        last_updated = existing_knowledge.get("last_updated")
        if not last_updated:
            return {"is_stale": True, "staleness_reason": "No last_updated timestamp"}

        try:
            last_update_date = datetime.strptime(last_updated, "%Y-%m-%d")
            days_since_update = (datetime.now() - last_update_date).days

            # Get freshness threshold from topic data
            topic_data = existing_knowledge.get("topic_data", {})
            threshold = topic_data.get("freshness_threshold_days", 30)

            is_stale = days_since_update > threshold

            return {
                "is_stale": is_stale,
                "days_since_update": days_since_update,
                "freshness_threshold": threshold,
                "staleness_reason": f"Content is {days_since_update} days old (threshold: {threshold} days)"
            }
        except ValueError:
            return {"is_stale": True, "staleness_reason": "Invalid date format"}

    def _find_related_work(self, topic: str, scope: str, registry: Dict) -> List[Dict[str, any]]:
        """Find related work that might overlap with proposed analysis."""
        related_work = []
        topics = registry.get("topics", {})

        topic_keywords = set(topic.lower().split('-'))
        scope_keywords = set(scope.lower().split()) if scope else set()

        for topic_name, topic_data in topics.items():
            if topic_name == topic:
                continue  # Skip exact match

            existing_keywords = set(topic_name.lower().split('-'))
            keyword_overlap = len(topic_keywords & existing_keywords)

            # Calculate overlap score
            total_keywords = len(topic_keywords | existing_keywords)
            overlap_score = keyword_overlap / total_keywords if total_keywords > 0 else 0

            if overlap_score > 0.3:  # 30% keyword overlap threshold
                related_work.append({
                    "topic": topic_name,
                    "overlap_score": overlap_score,
                    "keyword_overlap": keyword_overlap,
                    "owner": topic_data.get("owner_command"),
                    "authority_path": topic_data.get("current_authority")
                })

        # Sort by overlap score
        related_work.sort(key=lambda x: x["overlap_score"], reverse=True)
        return related_work

    def _analyze_scope_overlap(self, proposed_scope: str, existing_knowledge: Optional[Dict],
                             related_work: List[Dict]) -> Dict[str, any]:
        """Analyze whether proposed scope overlaps with existing work."""

        if not proposed_scope:
            return {
                "adds_new_value": False,
                "scope_differs_significantly": False,
                "overlap_assessment": "Cannot assess without proposed scope"
            }

        # Simple keyword-based analysis (could be enhanced with NLP)
        proposed_keywords = set(proposed_scope.lower().split())

        scope_analysis = {
            "adds_new_value": True,  # Default assumption
            "scope_differs_significantly": True,  # Default assumption
            "overlap_assessment": "Scope appears distinct"
        }

        # Check against existing knowledge
        if existing_knowledge and existing_knowledge.get("authority_path"):
            # This would ideally analyze the actual content
            # For now, we'll use simple heuristics
            if len(proposed_keywords) < 3:
                scope_analysis["adds_new_value"] = False
                scope_analysis["overlap_assessment"] = "Scope too general, likely covered"

        # Check against related work
        high_overlap_related = [work for work in related_work if work["overlap_score"] > 0.7]
        if high_overlap_related:
            scope_analysis["scope_differs_significantly"] = False
            scope_analysis["overlap_assessment"] = f"High overlap with {len(high_overlap_related)} related topics"

        return scope_analysis

    def _create_decision(self, decision_type: DecisionType, rationale: str,
                        action_steps: List[str], **kwargs) -> Dict[str, any]:
        """Create a structured decision result."""

        decision = {
            "decision": decision_type.value,
            "rationale": rationale,
            "action_steps": action_steps,
            "timestamp": datetime.now().isoformat(),
            "confidence": self._calculate_confidence(decision_type, kwargs)
        }

        # Add optional fields
        if "existing_authority" in kwargs:
            decision["existing_authority"] = kwargs["existing_authority"]
        if "coordination_required_with" in kwargs:
            decision["coordination_required_with"] = kwargs["coordination_required_with"]
        if "related_topics" in kwargs:
            decision["related_topics"] = kwargs["related_topics"]
        if "warnings" in kwargs:
            decision["warnings"] = kwargs["warnings"]

        return decision

    def _calculate_confidence(self, decision_type: DecisionType, context: Dict) -> str:
        """Calculate confidence level for the decision."""

        if decision_type in [DecisionType.PROCEED_NEW, DecisionType.CLAIM_OWNERSHIP]:
            return "high" if not context.get("related_topics") else "medium"

        elif decision_type == DecisionType.UPDATE_EXISTING:
            return "high"

        elif decision_type == DecisionType.COORDINATE_REQUIRED:
            return "medium"

        elif decision_type in [DecisionType.AVOID_DUPLICATION, DecisionType.REFERENCE_EXISTING]:
            return "high"

        return "medium"

    def _load_registry(self) -> Optional[Dict]:
        """Load topic registry."""
        try:
            if self.registry_path.exists():
                return yaml.safe_load(self.registry_path.read_text())
        except Exception:
            pass
        return None

def main():
    """CLI interface for decision tree."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python decision-tree.py <command_name> <topic> [scope] [--force-new]")
        print("Example: python decision-tree.py architect technical-health 'comprehensive security analysis'")
        sys.exit(1)

    command_name = sys.argv[1]
    topic = sys.argv[2]
    scope = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else ""
    force_new = "--force-new" in sys.argv

    decision_tree = DecisionTree()
    decision = decision_tree.make_decision(command_name, topic, scope, force_new)

    print(f"Decision Tree Analysis for {command_name} → {topic}")
    print("=" * 60)
    print(f"Decision: {decision['decision'].upper()}")
    print(f"Confidence: {decision['confidence'].upper()}")
    print(f"Rationale: {decision['rationale']}")

    if decision.get('warnings'):
        print(f"\nWarnings:")
        for warning in decision['warnings']:
            print(f"  ⚠️  {warning}")

    print(f"\nRecommended Actions:")
    for i, action in enumerate(decision['action_steps'], 1):
        print(f"  {i}. {action}")

    if decision.get('coordination_required_with'):
        print(f"\nCoordination Required With: {decision['coordination_required_with']}")

    if decision.get('existing_authority'):
        print(f"Existing Authority: {decision['existing_authority']}")

if __name__ == "__main__":
    main()
