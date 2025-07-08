"""
Base Context Classes for Sensylate Command Context Management

Implements the core context architecture that separates command logic from
environmental state, enabling commands to be pure functions that operate
on injected context rather than hardcoded configurations.

This follows the dependency injection pattern outlined in the MCP documentation,
treating context as a first-class architectural concern.
"""

import dataclasses
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from enum import Enum


class QualityGate(Enum):
    """Quality gate levels for validation"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    STRICT = "strict"
    INSTITUTIONAL = "institutional"


class RetryPolicy(Enum):
    """Retry policies for MCP operations"""
    NONE = "none"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"


@dataclasses.dataclass
class ExecutionContext:
    """Execution environment context for command runs"""
    timestamp: datetime
    command_name: str
    working_directory: Path
    timeout: int = 300
    environment: str = "local"
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    def get_session_prefix(self) -> str:
        """Get session-based prefix for file naming"""
        return f"{self.command_name}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}"

    def is_expired(self, max_age_seconds: int = 3600) -> bool:
        """Check if execution context has expired"""
        return (datetime.now() - self.timestamp).total_seconds() > max_age_seconds


@dataclasses.dataclass
class DataContext:
    """Data management context for file operations"""
    base_output_path: Path
    cache_enabled: bool = True
    backup_enabled: bool = True
    temp_cleanup: bool = True
    file_permissions: int = 0o644

    def get_output_path(self, category: str, subcategory: str = None) -> Path:
        """Get context-aware output path"""
        if subcategory:
            return self.base_output_path / category / subcategory
        return self.base_output_path / category

    def get_cache_path(self, key: str) -> Path:
        """Get cache file path for given key"""
        return self.base_output_path / ".cache" / f"{key}.json"

    def get_backup_path(self, original_path: Path) -> Path:
        """Get backup path for original file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return original_path.parent / ".backups" / f"{original_path.stem}_{timestamp}{original_path.suffix}"


@dataclasses.dataclass
class MCPContext:
    """MCP infrastructure context for server access"""
    config_path: Path
    available_servers: List[str]
    health_check_enabled: bool = True
    health_check_interval: int = 300
    retry_policy: RetryPolicy = RetryPolicy.EXPONENTIAL
    retry_attempts: int = 3
    timeout: int = 60
    cache_responses: bool = True

    def is_server_available(self, server_name: str) -> bool:
        """Check if MCP server is configured and available"""
        return server_name in self.available_servers

    def get_retry_config(self) -> Dict[str, Any]:
        """Get retry configuration for MCP operations"""
        return {
            "policy": self.retry_policy.value,
            "attempts": self.retry_attempts,
            "timeout": self.timeout
        }


@dataclasses.dataclass
class ValidationContext:
    """Validation context for data quality and compliance"""
    confidence_threshold: float = 0.8
    quality_gates: QualityGate = QualityGate.STANDARD
    format_validation: bool = True
    institutional_target: float = 9.5
    strict_formatting: bool = True

    def meets_confidence_threshold(self, confidence: float) -> bool:
        """Check if confidence meets threshold"""
        return confidence >= self.confidence_threshold

    def get_quality_requirements(self) -> Dict[str, Any]:
        """Get quality requirements based on quality gate"""
        requirements = {
            QualityGate.MINIMAL: {"accuracy": 0.6, "completeness": 0.5},
            QualityGate.STANDARD: {"accuracy": 0.8, "completeness": 0.7},
            QualityGate.STRICT: {"accuracy": 0.9, "completeness": 0.8},
            QualityGate.INSTITUTIONAL: {"accuracy": 0.95, "completeness": 0.9}
        }
        return requirements.get(self.quality_gates, requirements[QualityGate.STANDARD])


@dataclasses.dataclass
class LocalCommandContext:
    """
    Primary context container for Sensylate commands in local development.

    This class serves as the main dependency injection container, providing
    all environmental concerns needed by commands while keeping command logic pure.

    Context Flow:
    1. Context created with environment-specific configuration
    2. Injected into command execution
    3. Command uses context providers instead of hardcoded values
    4. Context tracks execution state and provides observability
    """
    execution: ExecutionContext
    data: DataContext
    mcp: MCPContext
    validation: ValidationContext
    metadata: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        """Validate context consistency after initialization"""
        self._validate_context()

    def _validate_context(self):
        """Validate context configuration consistency"""
        # Ensure output paths exist
        self.data.base_output_path.mkdir(parents=True, exist_ok=True)

        # Ensure MCP config exists
        if not self.mcp.config_path.exists():
            raise ValueError(f"MCP config file not found: {self.mcp.config_path}")

    def get_command_output_path(self, category: str, filename: str = None) -> Path:
        """Get full output path for command with optional filename"""
        base_path = self.data.get_output_path(category, None)

        if filename:
            return base_path / filename

        # Generate filename from execution context
        timestamp = self.execution.timestamp.strftime("%Y%m%d")
        default_filename = f"{self.execution.command_name}_{timestamp}.json"
        return base_path / default_filename

    def create_child_context(self, command_name: str, **overrides) -> 'LocalCommandContext':
        """Create child context for sub-command execution"""
        new_execution = dataclasses.replace(
            self.execution,
            command_name=command_name,
            timestamp=datetime.now()
        )

        # Apply any overrides
        context_data = {
            "execution": new_execution,
            "data": self.data,
            "mcp": self.mcp,
            "validation": self.validation,
            "metadata": self.metadata.copy()
        }
        context_data.update(overrides)

        return LocalCommandContext(**context_data)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to dictionary for logging/debugging"""
        return {
            "execution": {
                "timestamp": self.execution.timestamp.isoformat(),
                "command_name": self.execution.command_name,
                "working_directory": str(self.execution.working_directory),
                "timeout": self.execution.timeout,
                "environment": self.execution.environment
            },
            "data": {
                "base_output_path": str(self.data.base_output_path),
                "cache_enabled": self.data.cache_enabled,
                "backup_enabled": self.data.backup_enabled
            },
            "mcp": {
                "config_path": str(self.mcp.config_path),
                "available_servers": self.mcp.available_servers,
                "retry_policy": self.mcp.retry_policy.value
            },
            "validation": {
                "confidence_threshold": self.validation.confidence_threshold,
                "quality_gates": self.validation.quality_gates.value,
                "institutional_target": self.validation.institutional_target
            },
            "metadata": self.metadata
        }


def create_local_context(
    command_name: str,
    working_directory: Path = None,
    base_output_path: Path = None,
    mcp_config_path: Path = None,
    **kwargs
) -> LocalCommandContext:
    """
    Factory function for creating local development context.

    This function provides sensible defaults for Sensylate's local development
    environment while allowing customization for specific use cases.

    Args:
        command_name: Name of the command being executed
        working_directory: Working directory (defaults to current)
        base_output_path: Base path for outputs (defaults to ./data/outputs)
        mcp_config_path: Path to MCP configuration (defaults to ./mcp-servers.json)
        **kwargs: Additional context overrides

    Returns:
        LocalCommandContext configured for local development
    """

    # Set defaults for local development
    if working_directory is None:
        working_directory = Path.cwd()

    if base_output_path is None:
        base_output_path = working_directory / "data" / "outputs"

    if mcp_config_path is None:
        mcp_config_path = working_directory / "mcp-servers.json"

    # Load available MCP servers from config
    available_servers = []
    if mcp_config_path.exists():
        import json
        try:
            with open(mcp_config_path) as f:
                config = json.load(f)
                available_servers = list(config.get("mcpServers", {}).keys())
        except (json.JSONDecodeError, IOError):
            available_servers = []

    # Create context components
    execution = ExecutionContext(
        timestamp=datetime.now(),
        command_name=command_name,
        working_directory=working_directory,
        timeout=kwargs.get("timeout", 300),
        environment="local"
    )

    data = DataContext(
        base_output_path=base_output_path,
        cache_enabled=kwargs.get("cache_enabled", True),
        backup_enabled=kwargs.get("backup_enabled", True),
        temp_cleanup=kwargs.get("temp_cleanup", True)
    )

    mcp = MCPContext(
        config_path=mcp_config_path,
        available_servers=available_servers,
        health_check_enabled=kwargs.get("health_check_enabled", True),
        retry_policy=RetryPolicy(kwargs.get("retry_policy", "exponential")),
        retry_attempts=kwargs.get("retry_attempts", 3),
        timeout=kwargs.get("mcp_timeout", 60)
    )

    validation = ValidationContext(
        confidence_threshold=kwargs.get("confidence_threshold", 0.8),
        quality_gates=QualityGate(kwargs.get("quality_gates", "standard")),
        format_validation=kwargs.get("format_validation", True),
        institutional_target=kwargs.get("institutional_target", 9.5)
    )

    return LocalCommandContext(
        execution=execution,
        data=data,
        mcp=mcp,
        validation=validation,
        metadata=kwargs.get("metadata", {})
    )
