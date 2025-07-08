"""
Context-Aware Command Execution Framework

This module provides the infrastructure for executing Sensylate commands
with proper context injection. Commands use injected context rather than
hardcoded configurations, enabling environment flexibility and testability.

Key Components:
- CommandExecutor: Base class for context-aware command execution
- MCPBridge: Bridge between commands and MCP infrastructure
- CommandFactory: Factory for creating context-injected commands

Usage:
    from commands import create_command_executor

    executor = create_command_executor("fundamental_analyst_discover")
    result = executor.execute(ticker="AAPL")
"""

from .command_executor import CommandExecutor, create_command_executor
from .mcp_bridge import MCPBridge, CommandMCPBridge

__all__ = [
    "CommandExecutor",
    "create_command_executor",
    "MCPBridge",
    "CommandMCPBridge"
]
