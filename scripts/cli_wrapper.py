#!/usr/bin/env python3
"""
CLI Wrapper System

Provides unified interface for CLI service execution with:
- Global command detection and fallback to local execution
- Service discovery and health checking
- Memory-efficient command execution
- Local-first data strategy integration
"""

import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class CLIServiceError(Exception):
    """Base exception for CLI service errors"""

    pass


class CLIServiceNotFoundError(CLIServiceError):
    """Raised when CLI service is not available"""

    pass


class CLIExecutionError(CLIServiceError):
    """Raised when CLI command execution fails"""

    pass


class CLIServiceWrapper:
    """
    Wrapper for CLI services that handles both global and local execution modes
    """

    def __init__(self, service_name: str, scripts_dir: Optional[Path] = None):
        self.service_name = service_name
        self.scripts_dir = scripts_dir or Path(__file__).parent
        self.logger = self._setup_logger()

        # CLI service configuration
        self.cli_script_name = f"{service_name}_cli.py"
        self.cli_script_path = self.scripts_dir / self.cli_script_name
        self.global_command_name = f"{service_name}_cli"

        # Execution modes
        self.global_available = self._check_global_availability()
        self.local_available = self._check_local_availability()

        self.logger.info(
            f"CLI wrapper initialized for {service_name} - Global: {self.global_available}, Local: {self.local_available}"
        )

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for CLI wrapper"""
        logger = logging.getLogger(f"cli_wrapper.{self.service_name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _check_global_availability(self) -> bool:
        """Check if CLI service is available as global command"""
        try:
            # Check if command exists in PATH
            return shutil.which(self.global_command_name) is not None
        except Exception:
            return False

    def _check_local_availability(self) -> bool:
        """Check if CLI service is available as local Python script"""
        return self.cli_script_path.exists() and self.cli_script_path.is_file()

    def is_available(self) -> bool:
        """Check if CLI service is available in any form"""
        return self.global_available or self.local_available

    def execute_command(self, command: str, *args, **kwargs) -> Tuple[bool, str, str]:
        """
        Execute CLI command with fallback mechanisms

        Args:
            command: Command to execute (e.g., 'analyze', 'quote')
            *args: Command arguments
            **kwargs: Command options

        Returns:
            Tuple of (success, stdout, stderr)
        """
        if not self.is_available():
            raise CLIServiceNotFoundError(
                f"CLI service '{self.service_name}' is not available"
            )

        # Build command arguments
        cmd_args = [command] + list(args)

        # Add options from kwargs
        for key, value in kwargs.items():
            if key.startswith("_"):
                continue
            option_name = f"--{key.replace('_', '-')}"
            if isinstance(value, bool):
                if value:
                    cmd_args.append(option_name)
            else:
                cmd_args.extend([option_name, str(value)])

        # Try global command first
        if self.global_available:
            try:
                return self._execute_global_command(cmd_args)
            except Exception as e:
                self.logger.warning(
                    f"Global command failed: {e}, falling back to local execution"
                )

        # Fall back to local execution
        if self.local_available:
            try:
                return self._execute_local_command(cmd_args)
            except Exception as e:
                self.logger.error(f"Local command failed: {e}")
                raise CLIExecutionError(f"Command execution failed: {e}")

        raise CLIServiceNotFoundError(
            f"No execution method available for {self.service_name}"
        )

    def _execute_global_command(self, args: List[str]) -> Tuple[bool, str, str]:
        """Execute command as global CLI"""
        cmd = [self.global_command_name] + args
        self.logger.debug(f"Executing global command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.scripts_dir.parent,
            )

            success = result.returncode == 0
            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            raise CLIExecutionError(f"Command timed out: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            raise CLIExecutionError(
                f"Command failed with return code {e.returncode}: {e.stderr}"
            )

    def _execute_local_command(self, args: List[str]) -> Tuple[bool, str, str]:
        """Execute command as local Python script"""
        cmd = [sys.executable, str(self.cli_script_path)] + args
        self.logger.debug(f"Executing local command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.scripts_dir.parent,
            )

            success = result.returncode == 0
            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            raise CLIExecutionError(f"Local command timed out: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            raise CLIExecutionError(
                f"Local command failed with return code {e.returncode}: {e.stderr}"
            )

    def get_service_info(self) -> Dict[str, Any]:
        """Get service information and availability"""
        return {
            "service_name": self.service_name,
            "cli_script_path": str(self.cli_script_path),
            "global_command_name": self.global_command_name,
            "global_available": self.global_available,
            "local_available": self.local_available,
            "is_available": self.is_available(),
            "execution_mode": (
                "global"
                if self.global_available
                else "local"
                if self.local_available
                else "unavailable"
            ),
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on CLI service"""
        health_info = {
            "service_name": self.service_name,
            "status": "unknown",
            "details": {},
            "timestamp": subprocess.run(
                ["date", "-Iseconds"], capture_output=True, text=True
            ).stdout.strip(),
        }

        try:
            if not self.is_available():
                health_info["status"] = "unavailable"
                health_info["details"]["error"] = "CLI service not found"
                return health_info

            # Try to get version or help info
            try:
                success, stdout, stderr = self.execute_command("--help")
                if success:
                    health_info["status"] = "healthy"
                    health_info["details"]["help_available"] = True
                else:
                    health_info["status"] = "unhealthy"
                    health_info["details"]["error"] = stderr
            except Exception as e:
                health_info["status"] = "unhealthy"
                health_info["details"]["error"] = str(e)

            health_info["details"]["service_info"] = self.get_service_info()

        except Exception as e:
            health_info["status"] = "error"
            health_info["details"]["error"] = str(e)

        return health_info


class CLIServiceManager:
    """
    Manager for all CLI services with discovery and health checking
    """

    def __init__(self, scripts_dir: Optional[Path] = None):
        self.scripts_dir = scripts_dir or Path(__file__).parent
        self.logger = self._setup_logger()
        self.services = {}
        self._discover_services()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for CLI service manager"""
        logger = logging.getLogger("cli_service_manager")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _discover_services(self) -> None:
        """Discover available CLI services"""
        self.logger.info("Discovering CLI services...")

        # Expected financial CLI services
        expected_services = [
            "yahoo_finance",
            "alpha_vantage",
            "fred_economic",
            "coingecko",
            "fmp",
            "sec_edgar",
            "imf",
        ]

        for service_name in expected_services:
            try:
                wrapper = CLIServiceWrapper(service_name, self.scripts_dir)
                self.services[service_name] = wrapper

                if wrapper.is_available():
                    self.logger.info(f"✓ {service_name} service available")
                else:
                    self.logger.warning(f"✗ {service_name} service not available")

            except Exception as e:
                self.logger.error(f"Failed to initialize {service_name} service: {e}")

    def get_service(self, service_name: str) -> CLIServiceWrapper:
        """Get CLI service wrapper"""
        if service_name not in self.services:
            raise CLIServiceNotFoundError(f"Service '{service_name}' not found")

        wrapper = self.services[service_name]
        if not wrapper.is_available():
            raise CLIServiceNotFoundError(f"Service '{service_name}' is not available")

        return wrapper

    def get_available_services(self) -> List[str]:
        """Get list of available service names"""
        return [
            name for name, wrapper in self.services.items() if wrapper.is_available()
        ]

    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services"""
        status = {
            "total_services": len(self.services),
            "available_services": len(self.get_available_services()),
            "services": {},
        }

        for name, wrapper in self.services.items():
            status["services"][name] = wrapper.get_service_info()

        return status

    def health_check_all(self) -> Dict[str, Any]:
        """Perform health check on all services"""
        health_results = {
            "timestamp": subprocess.run(
                ["date", "-Iseconds"], capture_output=True, text=True
            ).stdout.strip(),
            "summary": {
                "total": len(self.services),
                "healthy": 0,
                "unhealthy": 0,
                "unavailable": 0,
            },
            "services": {},
        }

        for name, wrapper in self.services.items():
            health_info = wrapper.health_check()
            health_results["services"][name] = health_info

            status = health_info["status"]
            if status == "healthy":
                health_results["summary"]["healthy"] += 1
            elif status == "unavailable":
                health_results["summary"]["unavailable"] += 1
            else:
                health_results["summary"]["unhealthy"] += 1

        return health_results


# Global service manager instance
_service_manager = None


def get_service_manager() -> CLIServiceManager:
    """Get global service manager instance"""
    global _service_manager
    if _service_manager is None:
        _service_manager = CLIServiceManager()
    return _service_manager


def get_cli_service(service_name: str) -> CLIServiceWrapper:
    """Get CLI service wrapper by name"""
    return get_service_manager().get_service(service_name)


def execute_cli_command(
    service_name: str, command: str, *args, **kwargs
) -> Tuple[bool, str, str]:
    """
    Execute CLI command with automatic service discovery and fallback

    Args:
        service_name: Name of the service (e.g., 'yahoo_finance')
        command: Command to execute (e.g., 'analyze')
        *args: Command arguments
        **kwargs: Command options

    Returns:
        Tuple of (success, stdout, stderr)
    """
    service = get_cli_service(service_name)
    return service.execute_command(command, *args, **kwargs)


if __name__ == "__main__":
    # Example usage and testing
    import pprint

    # Test service discovery
    manager = get_service_manager()

    print("=== CLI Service Status ===")
    pprint.pprint(manager.get_service_status())

    print("\n=== Health Check ===")
    pprint.pprint(manager.health_check_all())

    # Test individual service
    available_services = manager.get_available_services()
    if available_services:
        test_service = available_services[0]
        print(f"\n=== Testing {test_service} service ===")
        try:
            service = get_cli_service(test_service)
            success, stdout, stderr = service.execute_command("--help")
            print(f"Success: {success}")
            print(f"Output: {stdout[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
