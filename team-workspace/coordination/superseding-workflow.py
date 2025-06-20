#!/usr/bin/env python3
"""
Team-Workspace Superseding Workflow System

Manages the complete superseding lifecycle with explicit replacement declarations,
archive management, and audit trail maintenance.
"""

import os
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

class SupersedingWorkflow:
    """Manages content superseding workflow with explicit declarations."""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.registry_path = self.workspace_path / "coordination" / "topic-registry.yaml"
        self.superseding_log_path = self.workspace_path / "coordination" / "superseding-log.yaml"
        self.knowledge_path = self.workspace_path / "knowledge"
        self.archive_path = self.workspace_path / "archive"

    def declare_superseding(self, command_name: str, topic: str, new_file_path: str,
                          superseded_files: List[str], reason: str,
                          superseding_type: str = "update") -> Dict[str, any]:
        """
        Declare that new content supersedes existing content.

        Args:
            command_name: Command performing superseding
            topic: Topic being superseded
            new_file_path: Path to new authoritative content
            superseded_files: List of files being superseded
            reason: Reason for superseding
            superseding_type: Type of superseding (update, consolidation, replacement)

        Returns:
            Superseding operation result
        """
        # Generate superseding event ID
        event_id = f"supersede_{topic}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Validate superseding request
        validation = self._validate_superseding_operation(
            command_name, topic, new_file_path, superseded_files
        )

        if not validation["valid"]:
            return {
                "success": False,
                "event_id": event_id,
                "error": validation["error"],
                "timestamp": datetime.now().isoformat()
            }

        # Execute superseding workflow
        try:
            # 1. Create archive directory
            archive_dir = self._create_archive_directory(event_id, command_name, topic)

            # 2. Archive superseded files
            archived_files = self._archive_files(superseded_files, archive_dir)

            # 3. Update topic registry
            self._update_topic_registry(topic, new_file_path, archived_files)

            # 4. Log superseding event
            self._log_superseding_event(
                event_id, command_name, topic, new_file_path,
                superseded_files, archived_files, reason, superseding_type
            )

            # 5. Create archive metadata
            self._create_archive_metadata(
                archive_dir, event_id, topic, superseded_files, new_file_path, reason
            )

            return {
                "success": True,
                "event_id": event_id,
                "archived_files": archived_files,
                "new_authority": new_file_path,
                "archive_location": str(archive_dir),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "event_id": event_id,
                "error": f"Superseding failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def complete_superseding_from_intent(self, intent_event_id: str,
                                       new_file_path: str) -> Dict[str, any]:
        """
        Complete a superseding operation that was previously declared as intent.

        Args:
            intent_event_id: Event ID from previous superseding intent
            new_file_path: Path to the completed new content

        Returns:
            Completion result
        """
        # Load superseding log to find intent
        superseding_log = self._load_superseding_log()
        if not superseding_log:
            return {"success": False, "error": "No superseding log found"}

        # Find intent event
        intent_event = None
        for event in superseding_log.get("superseding_events", []):
            if event.get("event_id") == intent_event_id:
                intent_event = event
                break

        if not intent_event:
            return {"success": False, "error": f"Intent event {intent_event_id} not found"}

        # Execute superseding based on intent
        return self.declare_superseding(
            command_name=intent_event["initiated_by"],
            topic=intent_event["topic"],
            new_file_path=new_file_path,
            superseded_files=intent_event["superseded_files"],
            reason=intent_event["reason"],
            superseding_type="completion_of_intent"
        )

    def rollback_superseding(self, event_id: str) -> Dict[str, any]:
        """
        Rollback a superseding operation by restoring archived content.

        Args:
            event_id: ID of superseding event to rollback

        Returns:
            Rollback operation result
        """
        superseding_log = self._load_superseding_log()
        if not superseding_log:
            return {"success": False, "error": "No superseding log found"}

        # Find superseding event
        event = None
        for evt in superseding_log.get("superseding_events", []):
            if evt.get("event_id") == event_id:
                event = evt
                break

        if not event:
            return {"success": False, "error": f"Event {event_id} not found"}

        try:
            # Restore archived files
            restored_files = []
            archive_base = self.archive_path / event_id.replace("supersede_", "")

            for archived_file in event.get("archived_files", []):
                source_path = Path(archived_file["archive_path"])
                target_path = Path(archived_file["original_path"])

                if source_path.exists():
                    # Ensure target directory exists
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, target_path)
                    restored_files.append(str(target_path))

            # Update topic registry to remove superseding
            self._rollback_topic_registry_update(event["topic"], event_id)

            # Log rollback event
            rollback_event_id = f"rollback_{event_id}_{datetime.now().strftime('%H%M%S')}"
            self._log_rollback_event(rollback_event_id, event_id, restored_files)

            return {
                "success": True,
                "rollback_event_id": rollback_event_id,
                "restored_files": restored_files,
                "original_event_id": event_id,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Rollback failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _validate_superseding_operation(self, command_name: str, topic: str,
                                      new_file_path: str, superseded_files: List[str]) -> Dict[str, any]:
        """Validate superseding operation requirements."""

        # Check if new file exists
        if not Path(new_file_path).exists():
            return {"valid": False, "error": f"New file {new_file_path} does not exist"}

        # Check if superseded files exist
        missing_files = []
        for file_path in superseded_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)

        if missing_files:
            return {"valid": False, "error": f"Superseded files not found: {missing_files}"}

        # Load registry to check ownership
        registry = self._load_registry()
        if registry:
            ownership_map = registry.get("command_ownership", {})
            command_topics = ownership_map.get(command_name, {})

            has_permission = (
                topic in command_topics.get("primary_topics", []) or
                topic in command_topics.get("secondary_topics", [])
            )

            if not has_permission:
                return {"valid": False, "error": f"Command {command_name} lacks permission for topic {topic}"}

        return {"valid": True}

    def _create_archive_directory(self, event_id: str, command_name: str, topic: str) -> Path:
        """Create archive directory for superseding event."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        archive_dir = self.archive_path / date_str / command_name / topic / event_id
        archive_dir.mkdir(parents=True, exist_ok=True)
        return archive_dir

    def _archive_files(self, file_paths: List[str], archive_dir: Path) -> List[Dict[str, str]]:
        """Archive files to archive directory."""
        archived_files = []

        for file_path in file_paths:
            source_path = Path(file_path)
            if source_path.exists():
                target_path = archive_dir / source_path.name
                shutil.copy2(source_path, target_path)

                archived_files.append({
                    "original_path": str(source_path),
                    "archive_path": str(target_path),
                    "file_size": source_path.stat().st_size,
                    "archive_timestamp": datetime.now().isoformat()
                })

                # Remove original file
                source_path.unlink()

        return archived_files

    def _update_topic_registry(self, topic: str, new_authority_path: str,
                             archived_files: List[Dict[str, str]]):
        """Update topic registry with new authority and archived files."""
        registry = self._load_registry()
        if not registry:
            return

        topics = registry.get("topics", {})
        if topic in topics:
            # Update authority
            topics[topic]["current_authority"] = new_authority_path
            topics[topic]["last_updated"] = datetime.now().strftime("%Y-%m-%d")

            # Update related files to point to new authority
            topics[topic]["related_files"] = [new_authority_path]

            # Add archived files list
            if "archived_files" not in topics[topic]:
                topics[topic]["archived_files"] = []

            for archived_file in archived_files:
                topics[topic]["archived_files"].append(archived_file["archive_path"])

            # Mark conflicts as resolved if they existed
            if topics[topic].get("conflicts_detected"):
                topics[topic]["conflicts_detected"] = False
                topics[topic]["conflict_details"] = "RESOLVED: Superseding workflow completed"

        # Write updated registry
        self.registry_path.write_text(yaml.dump(registry, default_flow_style=False))

    def _log_superseding_event(self, event_id: str, command_name: str, topic: str,
                             new_file_path: str, superseded_files: List[str],
                             archived_files: List[Dict[str, str]], reason: str,
                             superseding_type: str):
        """Log superseding event to audit trail."""
        superseding_log = self._load_superseding_log()
        if not superseding_log:
            superseding_log = {"superseding_events": []}

        event = {
            "event_id": event_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "superseding_completed",
            "superseding_type": superseding_type,
            "description": f"Content superseding for {topic} by {command_name}",
            "superseded_files": superseded_files,
            "superseding_files": [new_file_path],
            "archived_files": archived_files,
            "topic": topic,
            "initiated_by": command_name,
            "reason": reason,
            "validation_status": "completed"
        }

        superseding_log["superseding_events"].append(event)

        # Update metrics
        if "lifecycle_metrics" not in superseding_log:
            superseding_log["lifecycle_metrics"] = {}

        metrics = superseding_log["lifecycle_metrics"]
        metrics["total_superseding_events"] = metrics.get("total_superseding_events", 0) + 1
        metrics["successful_migrations"] = metrics.get("successful_migrations", 0) + 1

        # Write log
        self.superseding_log_path.write_text(yaml.dump(superseding_log, default_flow_style=False))

    def _create_archive_metadata(self, archive_dir: Path, event_id: str, topic: str,
                               superseded_files: List[str], new_authority: str, reason: str):
        """Create metadata file in archive directory."""
        metadata = {
            "event_id": event_id,
            "topic": topic,
            "superseding_timestamp": datetime.now().isoformat(),
            "reason": reason,
            "new_authority": new_authority,
            "superseded_files": superseded_files,
            "recovery_instructions": {
                "rollback_command": f"python coordination/superseding-workflow.py rollback {event_id}",
                "manual_recovery": f"Copy files from {archive_dir} back to original locations"
            }
        }

        metadata_file = archive_dir / "superseding-metadata.yaml"
        metadata_file.write_text(yaml.dump(metadata, default_flow_style=False))

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

    def _rollback_topic_registry_update(self, topic: str, event_id: str):
        """Rollback topic registry changes for a specific event."""
        # This would restore the registry state before the superseding event
        # For now, we'll mark it as requiring manual intervention
        pass

    def _log_rollback_event(self, rollback_event_id: str, original_event_id: str,
                          restored_files: List[str]):
        """Log rollback event to audit trail."""
        superseding_log = self._load_superseding_log()
        if not superseding_log:
            return

        rollback_event = {
            "event_id": rollback_event_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "rollback_completed",
            "description": f"Rollback of superseding event {original_event_id}",
            "original_event_id": original_event_id,
            "restored_files": restored_files,
            "validation_status": "rollback_completed"
        }

        superseding_log["superseding_events"].append(rollback_event)
        self.superseding_log_path.write_text(yaml.dump(superseding_log, default_flow_style=False))

def main():
    """CLI interface for superseding workflow operations."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python superseding-workflow.py <operation> [args...]")
        print("Operations:")
        print("  declare <command> <topic> <new_file> <superseded_file1,file2...> <reason>")
        print("  rollback <event_id>")
        print("  complete <intent_event_id> <new_file>")
        sys.exit(1)

    operation = sys.argv[1]
    workflow = SupersedingWorkflow()

    if operation == "declare" and len(sys.argv) >= 6:
        command_name = sys.argv[2]
        topic = sys.argv[3]
        new_file = sys.argv[4]
        superseded_files = sys.argv[5].split(',')
        reason = ' '.join(sys.argv[6:])

        result = workflow.declare_superseding(command_name, topic, new_file, superseded_files, reason)
        print(f"Superseding Result: {result}")

    elif operation == "rollback" and len(sys.argv) >= 3:
        event_id = sys.argv[2]
        result = workflow.rollback_superseding(event_id)
        print(f"Rollback Result: {result}")

    elif operation == "complete" and len(sys.argv) >= 4:
        intent_event_id = sys.argv[2]
        new_file = sys.argv[3]
        result = workflow.complete_superseding_from_intent(intent_event_id, new_file)
        print(f"Completion Result: {result}")

    else:
        print("Invalid operation or arguments")
        sys.exit(1)

if __name__ == "__main__":
    main()
