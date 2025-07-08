"""
Context Factory for Creating Configured Command Contexts

This factory handles the creation of LocalCommandContext objects with
appropriate configuration based on YAML files and command-specific overrides.
It provides the main entry point for commands to get their execution context.
"""

import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from ..base_context import (
    LocalCommandContext,
    ExecutionContext,
    DataContext,
    MCPContext,
    ValidationContext,
    QualityGate,
    RetryPolicy
)


logger = logging.getLogger(__name__)


class ContextConfigurationError(Exception):
    """Raised when context configuration is invalid"""
    pass


class ContextFactory:
    """
    Factory for creating configured command contexts.

    This factory loads configuration from YAML files and creates
    LocalCommandContext objects with appropriate settings for
    each command. It handles configuration merging, validation,
    and environment-specific overrides.

    Usage:
        factory = ContextFactory("config/local_context.yaml")
        context = factory.create_context("fundamental_analyst_discover")
    """

    def __init__(self, config_path: Path = None):
        if config_path is None:
            config_path = Path("config/local_context.yaml")

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load context configuration from YAML file"""
        try:
            with open(self.config_path) as f:
                config = yaml.safe_load(f)

            if not isinstance(config, dict):
                raise ContextConfigurationError("Configuration must be a dictionary")

            return config

        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            return self._get_default_config()
        except yaml.YAMLError as e:
            raise ContextConfigurationError(f"Invalid YAML in config file: {e}")
        except Exception as e:
            raise ContextConfigurationError(f"Failed to load config: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration when file is not available"""
        return {
            "execution": {
                "environment": "local",
                "timeout": 300
            },
            "data": {
                "base_output_path": "./data/outputs",
                "cache_enabled": True,
                "backup_enabled": True
            },
            "mcp": {
                "config_path": "./mcp-servers.json",
                "health_check_enabled": True,
                "retry_policy": "exponential",
                "retry_attempts": 3,
                "timeout": 60
            },
            "validation": {
                "confidence_threshold": 0.8,
                "quality_gates": "standard",
                "format_validation": True,
                "institutional_target": 9.5
            }
        }

    def create_context(
        self,
        command_name: str,
        overrides: Dict[str, Any] = None,
        working_directory: Path = None
    ) -> LocalCommandContext:
        """
        Create configured context for command.

        Args:
            command_name: Name of command to create context for
            overrides: Optional configuration overrides
            working_directory: Optional working directory override

        Returns:
            LocalCommandContext configured for the command
        """
        # Start with base configuration
        merged_config = self.config.copy()

        # Apply command-specific overrides from config
        if "command_overrides" in self.config and command_name in self.config["command_overrides"]:
            command_config = self.config["command_overrides"][command_name]
            merged_config = self._merge_config(merged_config, command_config)

        # Apply runtime overrides
        if overrides:
            merged_config = self._merge_config(merged_config, overrides)

        # Create context components
        execution = self._create_execution_context(command_name, merged_config, working_directory)
        data = self._create_data_context(merged_config)
        mcp = self._create_mcp_context(merged_config, execution.working_directory)
        validation = self._create_validation_context(merged_config)

        return LocalCommandContext(
            execution=execution,
            data=data,
            mcp=mcp,
            validation=validation,
            metadata={
                "config_source": str(self.config_path),
                "command_overrides_applied": command_name in self.config.get("command_overrides", {}),
                "runtime_overrides_applied": bool(overrides)
            }
        )

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge configuration dictionaries"""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def _create_execution_context(
        self,
        command_name: str,
        config: Dict[str, Any],
        working_directory: Path = None
    ) -> ExecutionContext:
        """Create execution context from configuration"""
        exec_config = config.get("execution", {})

        if working_directory is None:
            wd_str = exec_config.get("working_directory", ".")
            working_directory = Path(wd_str).expanduser().resolve()

        return ExecutionContext(
            timestamp=datetime.now(),
            command_name=command_name,
            working_directory=working_directory,
            timeout=exec_config.get("timeout", 300),
            environment=exec_config.get("environment", "local"),
            user_id=exec_config.get("user_id"),
            session_id=exec_config.get("session_id")
        )

    def _create_data_context(self, config: Dict[str, Any]) -> DataContext:
        """Create data context from configuration"""
        data_config = config.get("data", {})

        base_output_path = Path(data_config.get("base_output_path", "./data/outputs"))
        if not base_output_path.is_absolute():
            base_output_path = Path.cwd() / base_output_path

        return DataContext(
            base_output_path=base_output_path,
            cache_enabled=data_config.get("cache_enabled", True),
            backup_enabled=data_config.get("backup_enabled", True),
            temp_cleanup=data_config.get("temp_cleanup", True),
            file_permissions=data_config.get("file_permissions", 0o644)
        )

    def _create_mcp_context(self, config: Dict[str, Any], working_directory: Path) -> MCPContext:
        """Create MCP context from configuration"""
        mcp_config = config.get("mcp", {})

        config_path = Path(mcp_config.get("config_path", "./mcp-servers.json"))
        if not config_path.is_absolute():
            config_path = working_directory / config_path

        # Load available servers from MCP config
        available_servers = []
        if config_path.exists():
            try:
                import json
                with open(config_path) as f:
                    mcp_server_config = json.load(f)
                    available_servers = list(mcp_server_config.get("mcpServers", {}).keys())
            except (json.JSONDecodeError, IOError):
                logger.warning(f"Failed to load MCP server list from {config_path}")

        # Apply server priorities if configured
        server_priorities = mcp_config.get("server_priorities", [])
        if server_priorities:
            # Reorder available_servers based on priorities
            prioritized = [s for s in server_priorities if s in available_servers]
            remaining = [s for s in available_servers if s not in server_priorities]
            available_servers = prioritized + remaining

        retry_policy_str = mcp_config.get("retry_policy", "exponential")
        try:
            retry_policy = RetryPolicy(retry_policy_str)
        except ValueError:
            logger.warning(f"Invalid retry policy: {retry_policy_str}, using exponential")
            retry_policy = RetryPolicy.EXPONENTIAL

        return MCPContext(
            config_path=config_path,
            available_servers=available_servers,
            health_check_enabled=mcp_config.get("health_check_enabled", True),
            health_check_interval=mcp_config.get("health_check_interval", 300),
            retry_policy=retry_policy,
            retry_attempts=mcp_config.get("retry_attempts", 3),
            timeout=mcp_config.get("timeout", 60),
            cache_responses=mcp_config.get("cache_responses", True)
        )

    def _create_validation_context(self, config: Dict[str, Any]) -> ValidationContext:
        """Create validation context from configuration"""
        validation_config = config.get("validation", {})

        quality_gates_str = validation_config.get("quality_gates", "standard")
        try:
            quality_gates = QualityGate(quality_gates_str)
        except ValueError:
            logger.warning(f"Invalid quality gate: {quality_gates_str}, using standard")
            quality_gates = QualityGate.STANDARD

        return ValidationContext(
            confidence_threshold=validation_config.get("confidence_threshold", 0.8),
            quality_gates=quality_gates,
            format_validation=validation_config.get("format_validation", True),
            institutional_target=validation_config.get("institutional_target", 9.5),
            strict_formatting=validation_config.get("strict_formatting", True)
        )

    def get_command_config(self, command_name: str) -> Dict[str, Any]:
        """Get merged configuration for specific command"""
        base_config = self.config.copy()

        if "command_overrides" in self.config and command_name in self.config["command_overrides"]:
            command_config = self.config["command_overrides"][command_name]
            return self._merge_config(base_config, command_config)

        return base_config

    def list_configured_commands(self) -> List[str]:
        """List commands with specific configuration overrides"""
        return list(self.config.get("command_overrides", {}).keys())

    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []

        # Check required sections
        required_sections = ["execution", "data", "mcp", "validation"]
        for section in required_sections:
            if section not in self.config:
                issues.append(f"Missing required section: {section}")

        # Check data paths
        if "data" in self.config:
            data_config = self.config["data"]
            base_path = data_config.get("base_output_path")
            if base_path:
                path_obj = Path(base_path)
                if not path_obj.parent.exists():
                    issues.append(f"Base output path parent does not exist: {base_path}")

        # Check MCP config
        if "mcp" in self.config:
            mcp_config = self.config["mcp"]
            mcp_config_path = mcp_config.get("config_path")
            if mcp_config_path and not Path(mcp_config_path).exists():
                issues.append(f"MCP config file does not exist: {mcp_config_path}")

        # Check validation values
        if "validation" in self.config:
            val_config = self.config["validation"]

            confidence = val_config.get("confidence_threshold")
            if confidence is not None and (confidence < 0 or confidence > 1):
                issues.append("Confidence threshold must be between 0 and 1")

            institutional = val_config.get("institutional_target")
            if institutional is not None and (institutional < 0 or institutional > 10):
                issues.append("Institutional target must be between 0 and 10")

        return issues


# Convenience functions
def create_command_context(
    command_name: str,
    config_path: Path = None,
    overrides: Dict[str, Any] = None
) -> LocalCommandContext:
    """
    Convenience function to create command context.

    Args:
        command_name: Name of command
        config_path: Optional path to config file
        overrides: Optional configuration overrides

    Returns:
        LocalCommandContext configured for command
    """
    factory = ContextFactory(config_path)
    return factory.create_context(command_name, overrides)


def load_context_config(config_path: Path = None) -> Dict[str, Any]:
    """
    Load context configuration from file.

    Args:
        config_path: Optional path to config file

    Returns:
        Configuration dictionary
    """
    factory = ContextFactory(config_path)
    return factory.config
