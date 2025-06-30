#!/usr/bin/env python3
"""
Command Collaboration Engine - Discovery and dependency resolution system
Enables commands to collaborate as team members with shared workspace
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import logging
from status_synchronizer import StatusSynchronizer

class CollaborationEngine:
    """Core engine for command discovery and dependency resolution"""

    def __init__(self, workspace_path: str = None, project_name: str = None):
        # Auto-detect project from workspace path or use provided project name
        if workspace_path is None:
            if project_name is None:
                # Try to auto-detect from current working directory
                cwd = Path.cwd()
                if "team-workspace" in str(cwd):
                    # Extract project from team-workspace path
                    project_path = cwd
                    while project_path.name != "team-workspace" and project_path.parent != project_path:
                        project_path = project_path.parent
                    if project_path.name == "team-workspace":
                        self.project_root = project_path.parent
                        project_name = self.project_root.name
                        workspace_path = str(project_path)
                else:
                    # Assume we're in project root
                    self.project_root = cwd
                    project_name = cwd.name
                    workspace_path = str(cwd / "team-workspace")
            else:
                self.project_root = Path(f"/Users/colemorton/Projects/{project_name}")
                workspace_path = str(self.project_root / "team-workspace")
        else:
            self.project_root = Path(workspace_path).parent
            if project_name is None:
                project_name = self.project_root.name

        self.workspace_path = Path(workspace_path)
        self.commands_path = self.workspace_path / "commands"
        self.shared_path = self.workspace_path / "shared"
        self.sessions_path = self.workspace_path / "sessions"

        # Command search paths (project takes precedence over user)
        self.project_commands_path = self.project_root / ".claude" / "commands"
        self.user_commands_path = Path("/Users/colemorton/.claude/commands")
        self.project_name = project_name

        # Load registry and schemas
        self.registry = self._load_registry()
        self.metadata_schema = self._load_metadata_schema()
        self.project_context = self._load_project_context()

        # Microservices support
        self.microservices_path = self.workspace_path / "microservices"

        # Initialize session
        self.session_id = self._generate_session_id()
        self.session_path = self.sessions_path / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

        # Initialize status synchronizer
        self.status_sync = StatusSynchronizer(str(self.workspace_path), self.project_name)

    def _load_registry(self) -> Dict[str, Any]:
        """Load command registry"""
        registry_path = self.commands_path / "registry.yaml"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                return yaml.safe_load(f)
        return {"commands": {}, "workflow_patterns": {}}

    def _load_metadata_schema(self) -> Dict[str, Any]:
        """Load metadata validation schema"""
        schema_path = self.shared_path / "metadata-schema.yaml"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _load_project_context(self) -> Dict[str, Any]:
        """Load current project context"""
        context_path = self.shared_path / "project-context.yaml"
        if context_path.exists():
            with open(context_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _generate_session_id(self) -> str:
        """Generate unique session identifier"""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _setup_logging(self):
        """Setup session logging"""
        log_file = self.session_path / "collaboration-engine.log"

        # Create a specific logger for this engine instance
        self.logger = logging.getLogger(f"collaboration_engine_{id(self)}")
        self.logger.setLevel(logging.INFO)

        # Clear any existing handlers
        self.logger.handlers.clear()

        # Add file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def discover_command(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Discover command information and capabilities with scope awareness"""
        # Check for microservice commands first
        microservice_info = self._discover_microservice(command_name)
        if microservice_info:
            return microservice_info

        if command_name in self.registry.get("commands", {}):
            command_info = self.registry["commands"][command_name].copy()

            # Resolve actual command file location based on scope
            command_file = self._resolve_command_location(command_name, command_info)
            if command_file:
                command_info["resolved_location"] = str(command_file)

            # Load manifest if available
            manifest_str = command_info.get("manifest", "")
            if manifest_str:  # Only proceed if manifest path is not empty
                manifest_path = Path(manifest_str)
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = yaml.safe_load(f)
                    command_info["manifest_data"] = manifest

            self.logger.info(f"Discovered command: {command_name} (scope: {command_info.get('scope', 'unknown')})")
            # Ensure log is flushed to file
            for handler in self.logger.handlers:
                handler.flush()
            return command_info

        self.logger.warning(f"Command not found in registry: {command_name}")
        # Ensure log is flushed to file
        for handler in self.logger.handlers:
            handler.flush()
        return None

    def _discover_microservice(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Discover microservice commands with DASV framework support"""
        # Check if this is a microservice command (pattern: role_action)
        if "_" not in command_name:
            return None

        role, action = command_name.rsplit("_", 1)

        # Check for microservice in registry
        microservices = self.registry.get("microservices", {})
        if command_name in microservices:
            microservice_info = microservices[command_name].copy()

            # Resolve microservice file location
            microservice_path = self.microservices_path / role / f"{action}.md"
            if microservice_path.exists():
                microservice_info["resolved_location"] = str(microservice_path)

                # Load microservice manifest
                manifest_path = self.microservices_path / role / action / "manifest.yaml"
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = yaml.safe_load(f)
                    microservice_info["manifest_data"] = manifest
                    microservice_info["type"] = "microservice"
                    microservice_info["role"] = role
                    microservice_info["action"] = action

                    self.logger.info(f"Discovered microservice: {command_name} (role: {role}, action: {action})")
                    return microservice_info

        return None

    def _resolve_command_location(self, command_name: str, command_info: Dict[str, Any]) -> Optional[Path]:
        """Resolve command file location with project/user precedence"""
        scope = command_info.get("scope", "user")

        # Check project-specific commands first
        if self.project_commands_path.exists():
            project_file = self.project_commands_path / f"{command_name}.md"
            if project_file.exists():
                self.logger.info(f"Found project-specific command: {command_name}")
                return project_file

        # Fall back to user commands
        if self.user_commands_path.exists():
            user_file = self.user_commands_path / command_info.get("location", "").split("/")[-1]
            if user_file.exists():
                self.logger.info(f"Found user command: {command_name}")
                return user_file

        # Use original location as fallback
        original_location = Path(command_info.get("location", ""))
        if original_location.exists():
            return original_location

        self.logger.warning(f"Command file not found for: {command_name}")
        return None

    def resolve_dependencies(self, command_name: str) -> Tuple[Dict[str, Any], List[str]]:
        """Resolve command dependencies and return execution context with status validation"""
        # CRITICAL: Synchronize workspace status before dependency resolution
        self.logger.info(f"Synchronizing workspace status before {command_name} execution")
        workspace_status = self.status_sync.sync_global_status()

        # Validate workspace consistency
        validation_errors = workspace_status.get("validation_errors", [])
        if validation_errors:
            self.logger.warning(f"Found {len(validation_errors)} workspace validation errors")
            for error in validation_errors[:3]:  # Log first 3 errors
                self.logger.warning(f"  {error['type']}: {error['message']}")

        command_info = self.discover_command(command_name)
        if not command_info:
            raise ValueError(f"Command {command_name} not found")

        manifest = command_info.get("manifest_data", {})
        dependencies = manifest.get("dependencies", {})

        execution_context = {
            "command": command_name,
            "session_id": self.session_id,
            "project_context": self.project_context,
            "workspace_status": workspace_status,  # Include current workspace status
            "available_data": {},
            "missing_dependencies": [],
            "optimization_data": {},
            "execution_plan": {},
            "status_warnings": validation_errors  # Include validation warnings
        }

        # Check required dependencies
        missing_deps = []
        for dep in dependencies.get("required", []):
            # Handle both string and dict dependency formats
            if isinstance(dep, dict):
                dep_command = dep.get("command")
                dep_output_type = dep.get("output_type")
                dep_name = dep_command
            else:
                dep_command = dep
                dep_output_type = None
                dep_name = dep

            dep_data = self._find_dependency_data(dep_command, dep_output_type)
            if dep_data:
                execution_context["available_data"][dep_name] = dep_data
            else:
                missing_deps.append(dep_name)
                self.logger.warning(f"Missing required dependency: {dep_name}")

        # Gather optional dependencies for optimization
        for dep in dependencies.get("optional", []):
            dep_data = self._find_dependency_data(dep["command"], dep["output_type"])
            if dep_data:
                execution_context["optimization_data"][dep["command"]] = {
                    "data": dep_data,
                    "enhancement": dep["enhancement"]
                }
                self.logger.info(f"Found optimization data from: {dep['command']}")

        execution_context["missing_dependencies"] = missing_deps

        # Generate execution plan
        execution_context["execution_plan"] = self._create_execution_plan(
            command_info, execution_context
        )

        return execution_context, missing_deps

    def _find_dependency_data(self, command: str, output_type: str = None) -> Optional[Dict[str, Any]]:
        """Find available data from dependency command"""
        command_output_path = self.commands_path / command / "outputs"

        if not command_output_path.exists():
            return None

        # Find most recent output of specified type
        output_files = []
        for file_path in command_output_path.glob("*.md"):
            meta_path = file_path.parent / f".{file_path.stem}.command-meta.yaml"
            if meta_path.exists():
                with open(meta_path, 'r') as f:
                    metadata = yaml.safe_load(f)

                # Check if output type matches (if specified)
                if output_type and metadata.get("output_specification", {}).get("type") != output_type:
                    continue

                output_files.append({
                    "file": file_path,
                    "metadata": metadata,
                    "timestamp": datetime.fromisoformat(metadata["metadata"]["timestamp"].replace('Z', '+00:00'))
                })

        if output_files:
            # Return most recent output
            latest = max(output_files, key=lambda x: x["timestamp"])
            with open(latest["file"], 'r') as f:
                content = f.read()

            return {
                "content": content,
                "metadata": latest["metadata"],
                "file_path": str(latest["file"])
            }

        return None

    def _create_execution_plan(self, command_info: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create optimized execution plan"""
        manifest = command_info.get("manifest_data", {})

        plan = {
            "pre_execution_steps": manifest.get("collaboration", {}).get("pre_execution_behavior", []),
            "post_execution_steps": manifest.get("collaboration", {}).get("post_execution_behavior", []),
            "cache_strategy": manifest.get("collaboration", {}).get("cache_strategy", "none"),
            "estimated_duration": self._estimate_duration(command_info, context),
            "optimization_available": len(context["optimization_data"]) > 0,
            "data_sources": list(context["available_data"].keys()) + list(context["optimization_data"].keys())
        }

        return plan

    def _estimate_duration(self, command_info: Dict[str, Any], context: Dict[str, Any]) -> int:
        """Estimate command execution duration"""
        base_time = command_info.get("performance_metrics", {}).get("avg_execution_time", "30s")

        # Parse time string to seconds
        if base_time.endswith('s'):
            base_seconds = int(base_time[:-1])
        elif base_time.endswith('m'):
            base_seconds = int(base_time[:-1]) * 60
        else:
            base_seconds = 30

        # Adjust for optimization data availability
        if context["optimization_data"]:
            base_seconds = int(base_seconds * 0.8)  # 20% faster with optimization data

        return base_seconds

    def register_command_execution(self, command_name: str, context: Dict[str, Any]) -> str:
        """Register command execution start"""
        execution_log = {
            "command": command_name,
            "session_id": self.session_id,
            "started_at": datetime.now().isoformat(),
            "context": context,
            "status": "running"
        }

        log_file = self.session_path / f"{command_name}-execution.yaml"
        with open(log_file, 'w') as f:
            yaml.dump(execution_log, f, default_flow_style=False)

        self.logger.info(f"Registered execution start: {command_name}")
        return str(log_file)

    def store_command_output(self, command_name: str, output_content: str,
                           output_type: str, metadata: Dict[str, Any]) -> Tuple[str, str]:
        """Store command output with metadata"""
        # Create output directory
        output_dir = self.commands_path / command_name / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = output_dir / f"{output_type}-{timestamp}.md"
        meta_file = output_dir / f".{output_type}-{timestamp}.command-meta.yaml"

        # Add output specification to metadata
        metadata.setdefault("output_specification", {})["type"] = output_type

        # Enhance metadata with framework data
        enhanced_metadata = self._enhance_metadata(command_name, metadata, output_content)

        # Write output and metadata
        with open(output_file, 'w') as f:
            f.write(output_content)

        with open(meta_file, 'w') as f:
            yaml.dump(enhanced_metadata, f, default_flow_style=False)

        # Update team workspace
        self._update_team_knowledge(command_name, output_content, enhanced_metadata)

        # Notify dependent commands
        self._notify_dependent_commands(command_name, enhanced_metadata)

        # CRITICAL: Update workspace status after output generation
        self.status_sync.sync_global_status()
        self.logger.info(f"Workspace status synchronized after {command_name} output generation")

        self.logger.info(f"Stored output: {output_file}")
        return str(output_file), str(meta_file)

    def _enhance_metadata(self, command_name: str, base_metadata: Dict[str, Any],
                         content: str) -> Dict[str, Any]:
        """Enhance metadata with framework-generated data"""
        enhanced = base_metadata.copy()

        # Add content hash for integrity
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        enhanced.setdefault("quality_metrics", {})["content_hash"] = content_hash

        # Add session tracking
        enhanced.setdefault("metadata", {})["session_id"] = self.session_id
        enhanced["metadata"]["timestamp"] = datetime.now().isoformat()

        # Add collaboration data
        command_info = self.discover_command(command_name)
        if command_info and "manifest_data" in command_info:
            manifest = command_info["manifest_data"]
            collab_data = manifest.get("collaboration", {})

            enhanced.setdefault("collaboration_data", {}).update({
                "intended_consumers": self._find_potential_consumers(command_name),
                "sharing_policy": collab_data.get("output_sharing", "immediate"),
                "cache_expires": (datetime.now() + timedelta(hours=24)).isoformat()
            })

        return enhanced

    def _find_potential_consumers(self, command_name: str) -> List[str]:
        """Find commands that could consume this command's output"""
        consumers = []

        for cmd_name, cmd_info in self.registry.get("commands", {}).items():
            if cmd_name == command_name:
                continue

            # Check if this command is listed as a dependency
            manifest_path = Path(cmd_info.get("manifest", ""))
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    manifest = yaml.safe_load(f)

                dependencies = manifest.get("dependencies", {})
                for dep in dependencies.get("optional", []):
                    if dep.get("command") == command_name:
                        consumers.append(cmd_name)
                        break

        return consumers

    def _update_team_knowledge(self, command_name: str, content: str, metadata: Dict[str, Any]):
        """Update shared team knowledge base"""
        knowledge_file = self.shared_path / "team-knowledge.yaml"

        if knowledge_file.exists():
            with open(knowledge_file, 'r') as f:
                knowledge = yaml.safe_load(f)
        else:
            knowledge = {"command_outputs": {}, "insights": [], "patterns": {}}

        # Update command outputs tracking
        knowledge["command_outputs"][command_name] = {
            "last_output": metadata["metadata"]["timestamp"],
            "output_type": metadata["output_specification"]["type"],
            "quality_score": metadata.get("quality_metrics", {}).get("quality_score", 0.8)
        }

        # Extract and store insights
        if metadata["output_specification"]["type"] == "implementation_plan":
            knowledge["insights"].append({
                "type": "implementation_strategy",
                "source": command_name,
                "timestamp": metadata["metadata"]["timestamp"],
                "summary": f"Implementation plan generated for {command_name}"
            })

        with open(knowledge_file, 'w') as f:
            yaml.dump(knowledge, f, default_flow_style=False)

    def _notify_dependent_commands(self, command_name: str, metadata: Dict[str, Any]):
        """Notify commands that depend on this output"""
        consumers = metadata.get("collaboration_data", {}).get("intended_consumers", [])

        for consumer in consumers:
            notification = {
                "event": "dependency_available",
                "source_command": command_name,
                "output_type": metadata["output_specification"]["type"],
                "timestamp": datetime.now().isoformat(),
                "data_location": metadata.get("file_path", ""),
                "quality_score": metadata.get("quality_metrics", {}).get("quality_score", 0.8)
            }

            # Store notification
            notification_dir = self.commands_path / consumer / "notifications"
            notification_dir.mkdir(parents=True, exist_ok=True)

            notification_file = notification_dir / f"{command_name}-{datetime.now().strftime('%H-%M-%S')}.yaml"
            with open(notification_file, 'w') as f:
                yaml.dump(notification, f, default_flow_style=False)

            self.logger.info(f"Notified {consumer} of {command_name} output")

    def get_workflow_recommendations(self, requested_commands: List[str]) -> Dict[str, Any]:
        """Recommend optimal workflow for requested commands"""
        workflow_patterns = self.registry.get("workflow_patterns", {})

        recommendations = {
            "suggested_sequence": [],
            "parallel_opportunities": [],
            "missing_dependencies": [],
            "estimated_total_time": 0
        }

        # Check for known workflow patterns
        for pattern_name, pattern_data in workflow_patterns.items():
            if "sequence" in pattern_data:
                pattern_commands = set(pattern_data["sequence"])
                if pattern_commands.issubset(set(requested_commands)):
                    recommendations["suggested_sequence"] = pattern_data["sequence"]
                    recommendations["estimated_total_time"] = pattern_data.get("avg_total_duration", "unknown")
                    break

        # If no pattern found, create dependency-based sequence
        if not recommendations["suggested_sequence"]:
            recommendations["suggested_sequence"] = self._resolve_command_sequence(requested_commands)

        return recommendations

    def _resolve_command_sequence(self, commands: List[str]) -> List[str]:
        """Resolve optimal execution sequence based on dependencies"""
        # Simple topological sort based on dependencies
        sequence = []
        remaining = commands.copy()

        while remaining:
            # Find commands with no unresolved dependencies
            ready = []
            for cmd in remaining:
                cmd_info = self.discover_command(cmd)
                if cmd_info and "manifest_data" in cmd_info:
                    manifest = cmd_info["manifest_data"]
                    required_deps = manifest.get("dependencies", {}).get("required", [])

                    # Check if all required dependencies are satisfied
                    deps_satisfied = all(dep in sequence for dep in required_deps if dep in commands)
                    if deps_satisfied:
                        ready.append(cmd)
                else:
                    ready.append(cmd)  # Commands without manifests can run anytime

            if ready:
                # Add first ready command to sequence
                next_cmd = ready[0]
                sequence.append(next_cmd)
                remaining.remove(next_cmd)
            else:
                # No commands ready, add remaining in original order
                sequence.extend(remaining)
                break

        return sequence

    def validate_before_execution(self, command_name: str) -> Dict[str, Any]:
        """Validate workspace state before command execution - PREVENTS COLLABORATION FAILURES"""
        self.logger.info(f"Running pre-execution validation for {command_name}")

        # Synchronize current status
        workspace_status = self.status_sync.sync_global_status()

        validation_result = {
            "command": command_name,
            "validation_passed": True,
            "errors": [],
            "warnings": [],
            "recommendations": [],
            "workspace_summary": {}
        }

        # Check for completion status conflicts
        validation_errors = workspace_status.get("validation_errors", [])
        if validation_errors:
            validation_result["errors"].extend(validation_errors)
            validation_result["validation_passed"] = False

        # Check dependency completion status
        dependencies = self._get_command_dependencies(command_name)
        for dep in dependencies:
            dep_status = self.status_sync.get_command_status_summary(dep)
            if dep_status:
                if dep_status["status"] == "completed":
                    validation_result["recommendations"].append(
                        f"✅ Dependency {dep} is completed - use latest outputs"
                    )
                else:
                    validation_result["warnings"].append(
                        f"⚠️ Dependency {dep} appears incomplete - verify status before proceeding"
                    )
            else:
                validation_result["warnings"].append(
                    f"❓ No status found for dependency {dep} - check if work has been done"
                )

        # Generate workspace summary
        commands = workspace_status.get("commands", {})
        for cmd, status in commands.items():
            completion_count = sum(1 for s in status["completion_status"].values() if s == "completed")
            total_count = len(status["completion_status"])
            validation_result["workspace_summary"][cmd] = {
                "completion_rate": completion_count / total_count if total_count > 0 else 0,
                "last_execution": status["last_execution"],
                "active_phase": status["active_phase"]
            }

        # Log validation summary
        if validation_result["validation_passed"]:
            self.logger.info(f"✅ Pre-execution validation passed for {command_name}")
        else:
            self.logger.error(f"❌ Pre-execution validation failed for {command_name}")

        return validation_result

    def _get_command_dependencies(self, command_name: str) -> List[str]:
        """Get list of command dependencies"""
        command_info = self.discover_command(command_name)
        if not command_info or "manifest_data" not in command_info:
            return []

        manifest = command_info["manifest_data"]
        dependencies = manifest.get("dependencies", {})

        # Combine required and optional dependencies
        deps = dependencies.get("required", [])
        optional_deps = [dep.get("command", "") for dep in dependencies.get("optional", [])]
        deps.extend([d for d in optional_deps if d])

        return deps

    def execute_dasv_workflow(self, role: str, ticker: str = None, **kwargs) -> Dict[str, Any]:
        """Execute a complete DASV workflow for a given role"""
        dasv_phases = ["discover", "analyze", "synthesize", "validate"]
        results = {
            "role": role,
            "workflow": "DASV",
            "phases": {},
            "status": "starting",
            "ticker": ticker
        }

        self.logger.info(f"Starting DASV workflow for role: {role}")

        try:
            for phase in dasv_phases:
                command_name = f"{role}_{phase}"
                self.logger.info(f"Executing DASV phase: {phase} ({command_name})")

                # Discover microservice
                microservice_info = self._discover_microservice(command_name)
                if not microservice_info:
                    raise ValueError(f"Microservice not found: {command_name}")

                # Resolve dependencies for this phase
                context, missing_deps = self.resolve_dependencies(command_name)

                if missing_deps and phase != "discover":
                    self.logger.warning(f"Missing dependencies for {command_name}: {missing_deps}")

                # Store phase results
                results["phases"][phase] = {
                    "command": command_name,
                    "status": "ready",
                    "context": context,
                    "missing_dependencies": missing_deps,
                    "microservice_info": microservice_info
                }

                self.logger.info(f"DASV phase {phase} prepared successfully")

            results["status"] = "ready_for_execution"
            self.logger.info(f"DASV workflow for {role} prepared successfully")

        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            self.logger.error(f"DASV workflow preparation failed: {e}")

        return results

    def get_workflow_composition(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Get workflow composition definition from registry"""
        workflow_compositions = self.registry.get("workflow_compositions", {})
        return workflow_compositions.get(workflow_name)

    def store_microservice_output(self, role: str, action: str, output_content: str,
                                output_type: str, metadata: Dict[str, Any]) -> Tuple[str, str]:
        """Store microservice output with role/action structure"""
        # Create microservice output directory
        output_dir = self.microservices_path / role / action / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename based on microservice patterns
        timestamp = datetime.now().strftime("%Y%m%d")
        ticker = metadata.get("ticker", "")

        if ticker:
            output_file = output_dir / f"{ticker}_{timestamp}_{action}.json"
            meta_file = output_dir / f".{ticker}_{timestamp}_{action}.meta.yaml"
        else:
            output_file = output_dir / f"{action}_{timestamp}.json"
            meta_file = output_dir / f".{action}_{timestamp}.meta.yaml"

        # Add microservice-specific metadata
        enhanced_metadata = metadata.copy()
        enhanced_metadata.setdefault("microservice", {}).update({
            "role": role,
            "action": action,
            "framework": "DASV",
            "timestamp": datetime.now().isoformat()
        })

        # Write output and metadata
        with open(output_file, 'w') as f:
            f.write(output_content)

        with open(meta_file, 'w') as f:
            yaml.dump(enhanced_metadata, f, default_flow_style=False)

        self.logger.info(f"Stored microservice output: {output_file}")
        return str(output_file), str(meta_file)


def main():
    """Example usage of the Collaboration Engine"""
    # Auto-detect project or specify manually
    engine = CollaborationEngine()

    print(f"=== Collaboration Engine for Project: {engine.project_name} ===")
    print(f"Project root: {engine.project_root}")
    print(f"Team workspace: {engine.workspace_path}")

    # Example: Resolve dependencies for architect command
    print("\n=== Dependency Resolution Example ===")
    context, missing = engine.resolve_dependencies("architect")

    print(f"Command: architect")
    print(f"Missing dependencies: {missing}")
    print(f"Available optimization data: {list(context['optimization_data'].keys())}")
    print(f"Estimated duration: {context['execution_plan']['estimated_duration']}s")

    # Example: Workflow recommendation
    print("\n=== Workflow Recommendation Example ===")
    workflow = engine.get_workflow_recommendations(["code-owner", "product-owner", "architect"])
    print(f"Suggested sequence: {workflow['suggested_sequence']}")
    print(f"Estimated total time: {workflow['estimated_total_time']}")

    # Example: Project-specific vs user commands
    print(f"\n=== Command Resolution Paths ===")
    print(f"User commands: {engine.user_commands_path}")
    print(f"Project commands: {engine.project_commands_path}")
    print(f"Microservices: {engine.microservices_path}")

    # Example: Microservice discovery
    print(f"\n=== Microservice Discovery Example ===")
    fundamental_discover = engine._discover_microservice("fundamental_analyst_discover")
    if fundamental_discover:
        print(f"Found microservice: fundamental_analyst_discover")
        print(f"Role: {fundamental_discover.get('role')}")
        print(f"Action: {fundamental_discover.get('action')}")
        print(f"Type: {fundamental_discover.get('type')}")
    else:
        print("Microservice fundamental_analyst_discover not found")

    # Example: DASV workflow preparation
    print(f"\n=== DASV Workflow Example ===")
    dasv_result = engine.execute_dasv_workflow("fundamental_analyst", ticker="AAPL")
    print(f"DASV Status: {dasv_result['status']}")
    print(f"DASV Phases: {list(dasv_result['phases'].keys())}")

    # Example usage for different projects
    print(f"\n=== Multi-Project Usage ===")
    print(f"# Current project: {engine.project_name}")
    print(f"# For different project: CollaborationEngine(project_name='other-project')")
    print(f"# Auto-detect from path: CollaborationEngine()")



if __name__ == "__main__":
    main()
