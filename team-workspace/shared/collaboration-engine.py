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
        
        # Initialize session
        self.session_id = self._generate_session_id()
        self.session_path = self.sessions_path / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
    
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
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def discover_command(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Discover command information and capabilities with scope awareness"""
        if command_name in self.registry.get("commands", {}):
            command_info = self.registry["commands"][command_name].copy()
            
            # Resolve actual command file location based on scope
            command_file = self._resolve_command_location(command_name, command_info)
            if command_file:
                command_info["resolved_location"] = str(command_file)
            
            # Load manifest if available
            manifest_path = Path(command_info.get("manifest", ""))
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    manifest = yaml.safe_load(f)
                command_info["manifest_data"] = manifest
            
            self.logger.info(f"Discovered command: {command_name} (scope: {command_info.get('scope', 'unknown')})")
            return command_info
        
        self.logger.warning(f"Command not found in registry: {command_name}")
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
        """Resolve command dependencies and return execution context"""
        command_info = self.discover_command(command_name)
        if not command_info:
            raise ValueError(f"Command {command_name} not found")
        
        manifest = command_info.get("manifest_data", {})
        dependencies = manifest.get("dependencies", {})
        
        execution_context = {
            "command": command_name,
            "session_id": self.session_id,
            "project_context": self.project_context,
            "available_data": {},
            "missing_dependencies": [],
            "optimization_data": {},
            "execution_plan": {}
        }
        
        # Check required dependencies
        missing_deps = []
        for dep in dependencies.get("required", []):
            dep_data = self._find_dependency_data(dep)
            if dep_data:
                execution_context["available_data"][dep] = dep_data
            else:
                missing_deps.append(dep)
                self.logger.warning(f"Missing required dependency: {dep}")
        
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


def main():
    """Example usage of the Collaboration Engine"""
    engine = CollaborationEngine()
    
    # Example: Resolve dependencies for architect command
    print("=== Dependency Resolution Example ===")
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


if __name__ == "__main__":
    main()