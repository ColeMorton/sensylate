#!/usr/bin/env python3
"""
Team-Workspace Knowledge Dashboard

Provides a unified view of current knowledge state, freshness indicators,
and validation status across all team-workspace content.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib

class KnowledgeDashboard:
    """Unified dashboard for team-workspace knowledge state."""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"
        self.superseding_log_path = self.workspace_path / "coordination" / "superseding-log.yaml"
        self.knowledge_path = self.workspace_path / "knowledge"

    def generate_dashboard(self, format: str = "text") -> str:
        """
        Generate comprehensive knowledge dashboard.

        Args:
            format: Output format ('text', 'json', 'markdown')

        Returns:
            Formatted dashboard content
        """
        dashboard_data = self._gather_dashboard_data()

        if format == "json":
            return json.dumps(dashboard_data, indent=2, default=str)
        elif format == "markdown":
            return self._format_markdown_dashboard(dashboard_data)
        else:
            return self._format_text_dashboard(dashboard_data)

    def get_knowledge_status_summary(self) -> Dict[str, any]:
        """Get high-level summary of knowledge state."""
        registry = self._load_registry()
        if not registry:
            return {"error": "Could not load registry"}

        topics = registry.get("topics", {})

        # Count topics by status
        status_counts = {}
        freshness_issues = []
        conflict_count = 0

        for topic_name, topic_data in topics.items():
            status = topic_data.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

            # Check for conflicts
            if topic_data.get("conflicts_detected"):
                conflict_count += 1

            # Check freshness
            freshness = self._assess_topic_freshness(topic_name, topic_data)
            if freshness["needs_attention"]:
                freshness_issues.append({
                    "topic": topic_name,
                    "issue": freshness["issue"]
                })

        return {
            "total_topics": len(topics),
            "status_distribution": status_counts,
            "conflicts_detected": conflict_count,
            "freshness_issues": len(freshness_issues),
            "freshness_details": freshness_issues,
            "knowledge_health": self._calculate_knowledge_health(status_counts, conflict_count, len(freshness_issues))
        }

    def get_topic_details(self, topic_name: str) -> Dict[str, any]:
        """Get detailed information about a specific topic."""
        registry = self._load_registry()
        if not registry:
            return {"error": "Could not load registry"}

        topics = registry.get("topics", {})
        if topic_name not in topics:
            return {"error": f"Topic '{topic_name}' not found"}

        topic_data = topics[topic_name]

        # Get ownership info
        ownership_info = self._get_topic_ownership_info(topic_name, registry)

        # Get freshness assessment
        freshness = self._assess_topic_freshness(topic_name, topic_data)

        # Get file status
        file_status = self._check_file_status(topic_data)

        # Get related superseding events
        superseding_events = self._get_topic_superseding_events(topic_name)

        return {
            "topic_name": topic_name,
            "topic_data": topic_data,
            "ownership_info": ownership_info,
            "freshness_assessment": freshness,
            "file_status": file_status,
            "superseding_events": superseding_events,
            "validation_status": self._validate_topic_integrity(topic_name, topic_data)
        }

    def check_system_health(self) -> Dict[str, any]:
        """Perform comprehensive system health check."""
        health_checks = {}

        # Check registry integrity
        health_checks["registry_integrity"] = self._check_registry_integrity()

        # Check file system consistency
        health_checks["filesystem_consistency"] = self._check_filesystem_consistency()

        # Check ownership consistency
        health_checks["ownership_consistency"] = self._check_ownership_consistency()

        # Check for orphaned files
        health_checks["orphaned_files"] = self._check_for_orphaned_files()

        # Calculate overall health score
        health_checks["overall_health"] = self._calculate_system_health_score(health_checks)

        return health_checks

    def _gather_dashboard_data(self) -> Dict[str, any]:
        """Gather all data needed for dashboard."""
        registry = self._load_registry()

        dashboard_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": self.get_knowledge_status_summary(),
            "system_health": self.check_system_health(),
            "topics": {},
            "ownership_overview": self._get_ownership_overview(registry),
            "recent_activities": self._get_recent_activities()
        }

        # Add detailed topic information
        if registry and "topics" in registry:
            for topic_name in registry["topics"]:
                dashboard_data["topics"][topic_name] = self.get_topic_details(topic_name)

        return dashboard_data

    def _format_text_dashboard(self, data: Dict[str, any]) -> str:
        """Format dashboard as text."""
        lines = []

        lines.append("TEAM-WORKSPACE KNOWLEDGE DASHBOARD")
        lines.append("=" * 50)
        lines.append(f"Generated: {data['generated_at']}")
        lines.append("")

        # Summary section
        summary = data["summary"]
        lines.append("KNOWLEDGE SUMMARY")
        lines.append("-" * 20)
        lines.append(f"Total Topics: {summary['total_topics']}")
        lines.append(f"Knowledge Health: {summary['knowledge_health']}")
        lines.append(f"Active Conflicts: {summary['conflicts_detected']}")
        lines.append(f"Freshness Issues: {summary['freshness_issues']}")
        lines.append("")

        # Status distribution
        if summary.get("status_distribution"):
            lines.append("Topic Status Distribution:")
            for status, count in summary["status_distribution"].items():
                lines.append(f"  {status}: {count}")
            lines.append("")

        # System health
        health = data["system_health"]
        lines.append("SYSTEM HEALTH")
        lines.append("-" * 15)
        lines.append(f"Overall Health: {health['overall_health']['score']}/100")

        for check_name, check_result in health.items():
            if check_name != "overall_health":
                status = "✅ PASS" if check_result.get("status") == "healthy" else "❌ FAIL"
                lines.append(f"  {check_name}: {status}")
                if check_result.get("issues"):
                    for issue in check_result["issues"][:3]:  # Show first 3 issues
                        lines.append(f"    • {issue}")
        lines.append("")

        # Topic details
        lines.append("TOPIC DETAILS")
        lines.append("-" * 15)
        for topic_name, topic_details in data["topics"].items():
            freshness = topic_details["freshness_assessment"]
            ownership = topic_details["ownership_info"]

            status_icon = "🟢" if not freshness["needs_attention"] else "🟡"
            lines.append(f"{status_icon} {topic_name}")
            lines.append(f"    Owner: {ownership['primary_owner']}")
            lines.append(f"    Status: {topic_details['topic_data'].get('status', 'unknown')}")
            lines.append(f"    Last Updated: {topic_details['topic_data'].get('last_updated', 'unknown')}")

            if freshness["needs_attention"]:
                lines.append(f"    ⚠️  {freshness['issue']}")
            lines.append("")

        return "\n".join(lines)

    def _format_markdown_dashboard(self, data: Dict[str, any]) -> str:
        """Format dashboard as markdown."""
        lines = []

        lines.append("# Team-Workspace Knowledge Dashboard")
        lines.append("")
        lines.append(f"**Generated:** {data['generated_at']}")
        lines.append("")

        # Summary
        summary = data["summary"]
        lines.append("## Knowledge Summary")
        lines.append("")
        lines.append(f"- **Total Topics:** {summary['total_topics']}")
        lines.append(f"- **Knowledge Health:** {summary['knowledge_health']}")
        lines.append(f"- **Active Conflicts:** {summary['conflicts_detected']}")
        lines.append(f"- **Freshness Issues:** {summary['freshness_issues']}")
        lines.append("")

        # Topics table
        lines.append("## Topics Overview")
        lines.append("")
        lines.append("| Topic | Status | Owner | Last Updated | Health |")
        lines.append("|-------|--------|-------|--------------|--------|")

        for topic_name, topic_details in data["topics"].items():
            topic_data = topic_details["topic_data"]
            ownership = topic_details["ownership_info"]
            freshness = topic_details["freshness_assessment"]

            health_icon = "🟢" if not freshness["needs_attention"] else "🟡"

            lines.append(f"| {topic_name} | {topic_data.get('status', 'unknown')} | "
                        f"{ownership['primary_owner']} | {topic_data.get('last_updated', 'unknown')} | "
                        f"{health_icon} |")

        lines.append("")

        # System health
        health = data["system_health"]
        lines.append("## System Health")
        lines.append("")
        lines.append(f"**Overall Score:** {health['overall_health']['score']}/100")
        lines.append("")

        for check_name, check_result in health.items():
            if check_name != "overall_health":
                status_icon = "✅" if check_result.get("status") == "healthy" else "❌"
                lines.append(f"- **{check_name}:** {status_icon} {check_result.get('status', 'unknown')}")

        return "\n".join(lines)

    def _assess_topic_freshness(self, topic_name: str, topic_data: Dict) -> Dict[str, any]:
        """Assess freshness of a topic."""
        last_updated = topic_data.get("last_updated")
        freshness_threshold = topic_data.get("freshness_threshold_days", 30)

        if not last_updated:
            return {
                "needs_attention": True,
                "issue": "No last_updated timestamp",
                "recommendation": "Update topic with proper timestamp"
            }

        try:
            last_update_date = datetime.strptime(last_updated, "%Y-%m-%d")
            days_since_update = (datetime.now() - last_update_date).days

            if days_since_update > freshness_threshold:
                return {
                    "needs_attention": True,
                    "issue": f"Content is {days_since_update} days old (threshold: {freshness_threshold})",
                    "recommendation": "Consider updating or reviewing content"
                }
            else:
                return {
                    "needs_attention": False,
                    "issue": None,
                    "days_since_update": days_since_update,
                    "freshness_threshold": freshness_threshold
                }
        except ValueError:
            return {
                "needs_attention": True,
                "issue": "Invalid date format in last_updated",
                "recommendation": "Fix date format in topic registry"
            }

    def _get_topic_ownership_info(self, topic_name: str, registry: Dict) -> Dict[str, any]:
        """Get ownership information for a topic."""
        ownership_map = registry.get("command_ownership", {})

        primary_owner = None
        secondary_owners = []

        for command, command_topics in ownership_map.items():
            if topic_name in command_topics.get("primary_topics", []):
                primary_owner = command
            if topic_name in command_topics.get("secondary_topics", []):
                secondary_owners.append(command)

        return {
            "primary_owner": primary_owner,
            "secondary_owners": secondary_owners,
            "has_owner": primary_owner is not None
        }

    def _check_file_status(self, topic_data: Dict) -> Dict[str, any]:
        """Check status of files referenced in topic data."""
        authority_path = topic_data.get("current_authority")
        related_files = topic_data.get("related_files", [])

        file_status = {
            "authority_exists": False,
            "related_files_status": [],
            "missing_files": []
        }

        # Check authority file
        if authority_path:
            authority_file = Path(authority_path)
            file_status["authority_exists"] = authority_file.exists()
            if not authority_file.exists():
                file_status["missing_files"].append(authority_path)

        # Check related files
        for file_path in related_files:
            file_obj = Path(file_path)
            status = {
                "path": file_path,
                "exists": file_obj.exists(),
                "size": file_obj.stat().st_size if file_obj.exists() else 0
            }
            file_status["related_files_status"].append(status)

            if not file_obj.exists():
                file_status["missing_files"].append(file_path)

        return file_status

    def _get_topic_superseding_events(self, topic_name: str) -> List[Dict]:
        """Get superseding events related to a topic."""
        superseding_log = self._load_superseding_log()
        if not superseding_log:
            return []

        events = []
        for event in superseding_log.get("superseding_events", []):
            if event.get("topic") == topic_name:
                events.append({
                    "event_id": event.get("event_id"),
                    "timestamp": event.get("timestamp"),
                    "event_type": event.get("event_type"),
                    "initiated_by": event.get("initiated_by"),
                    "reason": event.get("reason")
                })

        return events

    def _validate_topic_integrity(self, topic_name: str, topic_data: Dict) -> Dict[str, any]:
        """Validate integrity of a topic's data and files."""
        validation_results = {
            "valid": True,
            "issues": []
        }

        # Check required fields
        required_fields = ["current_authority", "owner_command", "last_updated"]
        for field in required_fields:
            if not topic_data.get(field):
                validation_results["valid"] = False
                validation_results["issues"].append(f"Missing required field: {field}")

        # Check file existence
        file_status = self._check_file_status(topic_data)
        if not file_status["authority_exists"]:
            validation_results["valid"] = False
            validation_results["issues"].append("Authority file does not exist")

        if file_status["missing_files"]:
            validation_results["valid"] = False
            validation_results["issues"].append(f"Missing files: {file_status['missing_files']}")

        return validation_results

    def _check_registry_integrity(self) -> Dict[str, any]:
        """Check integrity of the topic registry."""
        try:
            registry = self._load_registry()
            if not registry:
                return {"status": "unhealthy", "issues": ["Registry file not found or unreadable"]}

            issues = []

            # Check required sections
            required_sections = ["topics", "command_ownership"]
            for section in required_sections:
                if section not in registry:
                    issues.append(f"Missing section: {section}")

            # Validate topics structure
            topics = registry.get("topics", {})
            for topic_name, topic_data in topics.items():
                if not isinstance(topic_data, dict):
                    issues.append(f"Invalid topic data for {topic_name}")
                    continue

                # Check for required topic fields
                if not topic_data.get("current_authority"):
                    issues.append(f"Topic {topic_name} missing current_authority")

            return {
                "status": "healthy" if not issues else "unhealthy",
                "issues": issues,
                "total_topics": len(topics)
            }

        except Exception as e:
            return {"status": "unhealthy", "issues": [f"Registry validation error: {str(e)}"]}

    def _check_filesystem_consistency(self) -> Dict[str, any]:
        """Check consistency between registry and filesystem."""
        registry = self._load_registry()
        if not registry:
            return {"status": "unhealthy", "issues": ["Cannot load registry"]}

        issues = []

        # Check if knowledge directory exists
        if not self.knowledge_path.exists():
            issues.append("Knowledge directory does not exist")

        # Check topic authority files
        topics = registry.get("topics", {})
        for topic_name, topic_data in topics.items():
            authority_path = topic_data.get("current_authority")
            if authority_path and not Path(authority_path).exists():
                issues.append(f"Authority file missing for {topic_name}: {authority_path}")

        return {
            "status": "healthy" if not issues else "unhealthy",
            "issues": issues
        }

    def _check_ownership_consistency(self) -> Dict[str, any]:
        """Check consistency of ownership assignments."""
        registry = self._load_registry()
        if not registry:
            return {"status": "unhealthy", "issues": ["Cannot load registry"]}

        issues = []
        topics = registry.get("topics", {})
        ownership_map = registry.get("command_ownership", {})

        # Check that all topics have owners
        for topic_name, topic_data in topics.items():
            registry_owner = topic_data.get("owner_command")

            # Find actual owner in ownership map
            actual_owner = None
            for command, command_topics in ownership_map.items():
                if topic_name in command_topics.get("primary_topics", []):
                    actual_owner = command
                    break

            if not registry_owner:
                issues.append(f"Topic {topic_name} has no owner_command")
            elif registry_owner != actual_owner:
                issues.append(f"Topic {topic_name} ownership mismatch: registry={registry_owner}, map={actual_owner}")

        return {
            "status": "healthy" if not issues else "unhealthy",
            "issues": issues
        }

    def _check_for_orphaned_files(self) -> Dict[str, any]:
        """Check for orphaned files in the workspace."""
        # This would scan for files not referenced in the registry
        # For now, return a placeholder
        return {
            "status": "healthy",
            "issues": [],
            "orphaned_count": 0
        }

    def _calculate_system_health_score(self, health_checks: Dict) -> Dict[str, any]:
        """Calculate overall system health score."""
        total_checks = len([k for k in health_checks.keys() if k != "overall_health"])
        healthy_checks = len([v for v in health_checks.values()
                            if isinstance(v, dict) and v.get("status") == "healthy"])

        score = int((healthy_checks / total_checks) * 100) if total_checks > 0 else 0

        if score >= 90:
            health_level = "excellent"
        elif score >= 75:
            health_level = "good"
        elif score >= 50:
            health_level = "fair"
        else:
            health_level = "poor"

        return {
            "score": score,
            "level": health_level,
            "healthy_checks": healthy_checks,
            "total_checks": total_checks
        }

    def _get_ownership_overview(self, registry: Optional[Dict]) -> Dict[str, any]:
        """Get overview of ownership distribution."""
        if not registry:
            return {}

        ownership_map = registry.get("command_ownership", {})
        overview = {}

        for command, command_topics in ownership_map.items():
            primary_count = len(command_topics.get("primary_topics", []))
            secondary_count = len(command_topics.get("secondary_topics", []))

            overview[command] = {
                "primary_topics": primary_count,
                "secondary_topics": secondary_count,
                "total_involvement": primary_count + secondary_count
            }

        return overview

    def _get_recent_activities(self) -> List[Dict]:
        """Get recent superseding and ownership activities."""
        superseding_log = self._load_superseding_log()
        if not superseding_log:
            return []

        recent_events = []
        events = superseding_log.get("superseding_events", [])

        # Get last 5 events
        for event in sorted(events, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]:
            recent_events.append({
                "timestamp": event.get("timestamp"),
                "event_type": event.get("event_type"),
                "topic": event.get("topic"),
                "initiated_by": event.get("initiated_by"),
                "description": event.get("description", "")
            })

        return recent_events

    def _calculate_knowledge_health(self, status_counts: Dict, conflict_count: int,
                                  freshness_issues: int) -> str:
        """Calculate overall knowledge health rating."""
        total_topics = sum(status_counts.values())

        if total_topics == 0:
            return "unknown"

        # Calculate health score
        active_topics = status_counts.get("active", 0)
        completed_topics = status_counts.get("completed", 0)

        healthy_ratio = (active_topics + completed_topics) / total_topics
        conflict_penalty = min(conflict_count * 0.1, 0.3)  # Max 30% penalty
        freshness_penalty = min(freshness_issues * 0.05, 0.2)  # Max 20% penalty

        health_score = healthy_ratio - conflict_penalty - freshness_penalty

        if health_score >= 0.8:
            return "excellent"
        elif health_score >= 0.6:
            return "good"
        elif health_score >= 0.4:
            return "fair"
        else:
            return "needs_attention"

    def _load_registry(self) -> Optional[Dict]:
        """Load topic registry."""
        try:
            if self.registry_path.exists():
                return yaml.safe_load(self.registry_path.read_text())
        except Exception:
            pass
        return None

    def _load_superseding_log(self) -> Optional[Dict]:
        """Load superseding log."""
        try:
            if self.superseding_log_path.exists():
                return yaml.safe_load(self.superseding_log_path.read_text())
        except Exception:
            pass
        return None

def main():
    """CLI interface for knowledge dashboard."""
    import sys

    format_type = "text"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["text", "json", "markdown"]:
            format_type = sys.argv[1]

    dashboard = KnowledgeDashboard()

    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        summary = dashboard.get_knowledge_status_summary()
        print(json.dumps(summary, indent=2, default=str))
    elif len(sys.argv) > 2 and sys.argv[1] == "topic":
        topic_name = sys.argv[2]
        details = dashboard.get_topic_details(topic_name)
        print(json.dumps(details, indent=2, default=str))
    elif len(sys.argv) > 1 and sys.argv[1] == "health":
        health = dashboard.check_system_health()
        print(json.dumps(health, indent=2, default=str))
    else:
        output = dashboard.generate_dashboard(format_type)
        print(output)

if __name__ == "__main__":
    main()
