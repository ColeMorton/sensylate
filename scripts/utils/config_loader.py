"""
Configuration loading utilities with environment support.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigLoader:
    """Loads and merges YAML configurations with environment support."""

    def __init__(self) -> None:
        self.env_pattern = re.compile(r"\$\{([^}]+)\}")

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load a single YAML configuration file."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(path, "r") as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            raise ValueError(
                f"Configuration file must contain a YAML dictionary: {config_path}"
            )

        return self._substitute_variables(config)

    def load_with_environment(
        self, config_path: str, env: str = "dev"
    ) -> Dict[str, Any]:
        """Load base config and overlay environment-specific settings."""
        base_config = self.load_config(config_path)

        # Try to load environment-specific config
        config_dir = Path(config_path).parent
        env_config_path = config_dir / "environments" / f"{env}.yaml"

        if env_config_path.exists():
            env_config = self.load_config(str(env_config_path))
            base_config = self._merge_configs(base_config, env_config)

        # Load shared configs
        shared_dir = config_dir / "shared"
        if shared_dir.exists():
            for shared_file in shared_dir.glob("*.yaml"):
                shared_config = self.load_config(str(shared_file))
                base_config = self._merge_configs(shared_config, base_config)

        return base_config

    def _substitute_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively substitute environment variables in config."""
        return self._substitute_variables_recursive(config)  # type: ignore

    def _substitute_variables_recursive(self, config: Any) -> Any:
        """Internal recursive substitution method."""
        if isinstance(config, dict):
            return {
                key: self._substitute_variables_recursive(value)
                for key, value in config.items()
            }
        elif isinstance(config, list):
            return [self._substitute_variables_recursive(item) for item in config]
        elif isinstance(config, str):
            return self._substitute_string_variables(config)
        else:
            return config

    def _substitute_string_variables(self, value: str) -> str:
        """Substitute environment variables in a string."""

        def replacer(match: Any) -> str:
            var_name = match.group(1)
            # Handle nested variable references like ${base_paths.data_root}
            if "." in var_name:
                # Return original for complex references (handle in post-processing)
                return value
            return os.getenv(var_name, match.group(0))

        return self.env_pattern.sub(replacer, value)

    def _merge_configs(
        self, base: Dict[str, Any], overlay: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep merge two configuration dictionaries."""
        result = base.copy()

        for key, value in overlay.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result
