#!/usr/bin/env python3
"""
Team-Workspace Topic Ownership Management System

Manages topic ownership assignment, permissions, and collaboration coordination
between AI commands to prevent duplicate work and establish clear authority.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
import re

class TopicOwnershipManager:
    """Manages topic ownership and command collaboration permissions."""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"

    def assign_topic_ownership(self, topic: str, primary_owner: str,
                             secondary_owners: List[str] = None) -> Dict[str, any]:
        """
        Assign or update topic ownership.

        Args:
            topic: Topic name to assign ownership for
            primary_owner: Command that will be primary owner
            secondary_owners: Commands that can contribute to topic

        Returns:
            Assignment operation result
        """
        secondary_owners = secondary_owners or []

        # Validate command names
        valid_commands = {"architect", "code-owner", "product-owner", "business-analyst",
                         "twitter-post", "twitter-post-strategy", "fundamental-analysis", "command", "create-command", "commit-push", "trade-history"}

        if primary_owner not in valid_commands:
            return {"success": False, "error": f"Invalid primary owner command: {primary_owner}"}

        invalid_secondary = [cmd for cmd in secondary_owners if cmd not in valid_commands]
        if invalid_secondary:
            return {"success": False, "error": f"Invalid secondary owner commands: {invalid_secondary}"}

        # Load current registry
        registry = self._load_registry()
        if not registry:
            return {"success": False, "error": "Could not load topic registry"}

        # Update command ownership mapping
        ownership_map = registry.setdefault("command_ownership", {})

        # Remove topic from all previous ownerships
        self._remove_topic_from_all_ownerships(topic, ownership_map)

        # Assign new ownership
        self._assign_primary_ownership(topic, primary_owner, ownership_map)

        for secondary_owner in secondary_owners:
            self._assign_secondary_ownership(topic, secondary_owner, ownership_map)

        # Update topic data if it exists
        if "topics" in registry and topic in registry["topics"]:
            registry["topics"][topic]["owner_command"] = primary_owner
            registry["topics"][topic]["last_ownership_update"] = datetime.now().strftime("%Y-%m-%d")

        # Save registry
        try:
            self.registry_path.write_text(yaml.dump(registry, default_flow_style=False))
            return {
                "success": True,
                "topic": topic,
                "primary_owner": primary_owner,
                "secondary_owners": secondary_owners,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to save registry: {str(e)}"}

    def claim_unowned_topic(self, topic: str, claiming_command: str,
                          justification: str = "") -> Dict[str, any]:
        """
        Allow a command to claim ownership of an unowned topic.

        Args:
            topic: Topic to claim
            claiming_command: Command claiming ownership
            justification: Reason for claiming ownership

        Returns:
            Claiming operation result
        """
        registry = self._load_registry()
        if not registry:
            return {"success": False, "error": "Could not load topic registry"}

        # Check if topic already has ownership
        current_ownership = self.get_topic_ownership(topic)
        if current_ownership.get("has_primary_owner"):
            return {
                "success": False,
                "error": f"Topic {topic} already owned by {current_ownership['primary_owner']}"
            }

        # Claim ownership
        result = self.assign_topic_ownership(topic, claiming_command)

        if result["success"]:
            # Log claiming event
            self._log_ownership_event("topic_claimed", topic, claiming_command, justification)
            result["claimed"] = True
            result["justification"] = justification

        return result

    def get_topic_ownership(self, topic: str) -> Dict[str, any]:
        """
        Get current ownership information for a topic.

        Args:
            topic: Topic to check ownership for

        Returns:
            Ownership information
        """
        registry = self._load_registry()
        if not registry:
            return {"has_primary_owner": False, "error": "Could not load registry"}

        ownership_map = registry.get("command_ownership", {})

        # Find primary owner
        primary_owner = None
        secondary_owners = []

        for command, command_topics in ownership_map.items():
            if topic in command_topics.get("primary_topics", []):
                primary_owner = command
            if topic in command_topics.get("secondary_topics", []):
                secondary_owners.append(command)

        return {
            "topic": topic,
            "has_primary_owner": primary_owner is not None,
            "primary_owner": primary_owner,
            "secondary_owners": secondary_owners,
            "total_owners": len(secondary_owners) + (1 if primary_owner else 0)
        }

    def get_command_topics(self, command_name: str) -> Dict[str, any]:
        """
        Get all topics owned by a specific command.

        Args:
            command_name: Command to get topics for

        Returns:
            Command's topic ownership
        """
        registry = self._load_registry()
        if not registry:
            return {"primary_topics": [], "secondary_topics": []}

        ownership_map = registry.get("command_ownership", {})
        command_topics = ownership_map.get(command_name, {})

        return {
            "command": command_name,
            "primary_topics": command_topics.get("primary_topics", []),
            "secondary_topics": command_topics.get("secondary_topics", []),
            "total_topics": len(command_topics.get("primary_topics", [])) + len(command_topics.get("secondary_topics", []))
        }

    def suggest_collaboration(self, requesting_command: str, topic: str) -> Dict[str, any]:
        """
        Suggest collaboration approach for a command wanting to work on a topic.

        Args:
            requesting_command: Command requesting to work on topic
            topic: Topic the command wants to work on

        Returns:
            Collaboration suggestion
        """
        ownership_info = self.get_topic_ownership(topic)

        if not ownership_info.get("has_primary_owner"):
            return {
                "collaboration_type": "claim_ownership",
                "suggestion": f"Topic {topic} is unowned - you can claim primary ownership",
                "action": "claim",
                "coordination_required": False
            }

        primary_owner = ownership_info["primary_owner"]
        secondary_owners = ownership_info["secondary_owners"]

        if requesting_command == primary_owner:
            return {
                "collaboration_type": "primary_owner",
                "suggestion": f"You are the primary owner of {topic} - proceed with analysis",
                "action": "proceed",
                "coordination_required": False
            }

        if requesting_command in secondary_owners:
            return {
                "collaboration_type": "secondary_owner",
                "suggestion": f"You are a secondary owner - coordinate with primary owner {primary_owner}",
                "action": "coordinate",
                "coordination_required": True,
                "primary_owner": primary_owner
            }

        # Not an owner - suggest collaboration approaches
        collaboration_approaches = self._generate_collaboration_approaches(
            requesting_command, topic, primary_owner, secondary_owners
        )

        return {
            "collaboration_type": "external_contributor",
            "suggestion": f"Topic owned by {primary_owner} - coordination required",
            "action": "collaborate",
            "coordination_required": True,
            "primary_owner": primary_owner,
            "secondary_owners": secondary_owners,
            "collaboration_approaches": collaboration_approaches
        }

    def detect_ownership_conflicts(self) -> List[Dict[str, any]]:
        """
        Detect ownership conflicts and gaps in the current registry.

        Returns:
            List of ownership issues
        """
        registry = self._load_registry()
        if not registry:
            return [{"type": "registry_error", "message": "Could not load registry"}]

        conflicts = []
        topics = registry.get("topics", {})
        ownership_map = registry.get("command_ownership", {})

        # Check for topics without ownership
        for topic_name, topic_data in topics.items():
            ownership_info = self.get_topic_ownership(topic_name)

            if not ownership_info.get("has_primary_owner"):
                conflicts.append({
                    "type": "unowned_topic",
                    "topic": topic_name,
                    "message": f"Topic {topic_name} has no primary owner",
                    "suggestion": "Assign primary ownership to appropriate command"
                })

        # Check for ownership inconsistencies
        for topic_name, topic_data in topics.items():
            registry_owner = topic_data.get("owner_command")
            actual_ownership = self.get_topic_ownership(topic_name)

            if registry_owner != actual_ownership.get("primary_owner"):
                conflicts.append({
                    "type": "ownership_mismatch",
                    "topic": topic_name,
                    "registry_owner": registry_owner,
                    "actual_owner": actual_ownership.get("primary_owner"),
                    "message": f"Topic {topic_name} ownership mismatch between registry and ownership map"
                })

        # Check for over-ownership (too many primary topics per command)
        for command, command_topics in ownership_map.items():
            primary_count = len(command_topics.get("primary_topics", []))
            if primary_count > 5:  # Threshold for too many primary topics
                conflicts.append({
                    "type": "over_ownership",
                    "command": command,
                    "primary_topic_count": primary_count,
                    "message": f"Command {command} has {primary_count} primary topics (may be overloaded)"
                })

        return conflicts

    def _load_registry(self) -> Optional[Dict]:
        """Load topic registry."""
        try:
            if self.registry_path.exists():
                return yaml.safe_load(self.registry_path.read_text())
        except Exception:
            pass
        return None

    def _remove_topic_from_all_ownerships(self, topic: str, ownership_map: Dict):
        """Remove topic from all command ownerships."""
        for command, command_topics in ownership_map.items():
            if "primary_topics" in command_topics and topic in command_topics["primary_topics"]:
                command_topics["primary_topics"].remove(topic)
            if "secondary_topics" in command_topics and topic in command_topics["secondary_topics"]:
                command_topics["secondary_topics"].remove(topic)

    def _assign_primary_ownership(self, topic: str, owner: str, ownership_map: Dict):
        """Assign primary ownership of topic to command."""
        if owner not in ownership_map:
            ownership_map[owner] = {"primary_topics": [], "secondary_topics": []}

        if "primary_topics" not in ownership_map[owner]:
            ownership_map[owner]["primary_topics"] = []

        if topic not in ownership_map[owner]["primary_topics"]:
            ownership_map[owner]["primary_topics"].append(topic)

    def _assign_secondary_ownership(self, topic: str, owner: str, ownership_map: Dict):
        """Assign secondary ownership of topic to command."""
        if owner not in ownership_map:
            ownership_map[owner] = {"primary_topics": [], "secondary_topics": []}

        if "secondary_topics" not in ownership_map[owner]:
            ownership_map[owner]["secondary_topics"] = []

        if topic not in ownership_map[owner]["secondary_topics"]:
            ownership_map[owner]["secondary_topics"].append(topic)

    def _generate_collaboration_approaches(self, requesting_command: str, topic: str,
                                         primary_owner: str, secondary_owners: List[str]) -> List[Dict[str, str]]:
        """Generate collaboration approach suggestions."""
        approaches = []

        # Suggest becoming secondary owner
        approaches.append({
            "type": "request_secondary_ownership",
            "description": f"Request secondary ownership from {primary_owner}",
            "action": f"Coordinate with {primary_owner} to become secondary owner"
        })

        # Suggest collaborative analysis
        approaches.append({
            "type": "collaborative_analysis",
            "description": "Propose collaborative analysis with existing owners",
            "action": f"Propose joint analysis with {primary_owner}"
        })

        # Suggest complementary analysis
        approaches.append({
            "type": "complementary_analysis",
            "description": "Focus on complementary aspects not covered by existing analysis",
            "action": "Identify gaps or complementary angles for separate analysis"
        })

        return approaches

    def _log_ownership_event(self, event_type: str, topic: str, command: str, details: str):
        """Log ownership events for audit trail."""
        # This would typically log to a separate ownership events log
        # For now, we'll add it to the superseding log as a general audit trail
        try:
            superseding_log_path = self.workspace_path / "coordination" / "superseding-log.yaml"
            if superseding_log_path.exists():
                log_data = yaml.safe_load(superseding_log_path.read_text())
            else:
                log_data = {"superseding_events": []}

            ownership_event = {
                "event_id": f"ownership_{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "topic": topic,
                "command": command,
                "details": details
            }

            log_data["superseding_events"].append(ownership_event)
            superseding_log_path.write_text(yaml.dump(log_data, default_flow_style=False))

        except Exception:
            pass  # Logging failures shouldn't break ownership operations

def main():
    """CLI interface for topic ownership management."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python topic-ownership-manager.py <operation> [args...]")
        print("Operations:")
        print("  assign <topic> <primary_owner> [secondary_owner1,secondary_owner2...]")
        print("  claim <topic> <claiming_command> [justification]")
        print("  ownership <topic>")
        print("  topics <command>")
        print("  collaborate <requesting_command> <topic>")
        print("  conflicts")
        sys.exit(1)

    operation = sys.argv[1]
    manager = TopicOwnershipManager()

    if operation == "assign" and len(sys.argv) >= 4:
        topic = sys.argv[2]
        primary_owner = sys.argv[3]
        secondary_owners = sys.argv[4].split(',') if len(sys.argv) > 4 else []

        result = manager.assign_topic_ownership(topic, primary_owner, secondary_owners)
        print(f"Assignment Result: {result}")

    elif operation == "claim" and len(sys.argv) >= 4:
        topic = sys.argv[2]
        claiming_command = sys.argv[3]
        justification = ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else ""

        result = manager.claim_unowned_topic(topic, claiming_command, justification)
        print(f"Claiming Result: {result}")

    elif operation == "ownership" and len(sys.argv) >= 3:
        topic = sys.argv[2]
        result = manager.get_topic_ownership(topic)
        print(f"Ownership Info: {result}")

    elif operation == "topics" and len(sys.argv) >= 3:
        command = sys.argv[2]
        result = manager.get_command_topics(command)
        print(f"Command Topics: {result}")

    elif operation == "collaborate" and len(sys.argv) >= 4:
        requesting_command = sys.argv[2]
        topic = sys.argv[3]
        result = manager.suggest_collaboration(requesting_command, topic)
        print(f"Collaboration Suggestion: {result}")

    elif operation == "conflicts":
        conflicts = manager.detect_ownership_conflicts()
        print(f"Ownership Conflicts: {conflicts}")

    else:
        print("Invalid operation or arguments")
        sys.exit(1)

if __name__ == "__main__":
    main()
