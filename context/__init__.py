"""
Context Management Framework for Sensylate

This module provides a comprehensive context management system that decouples
command logic from environmental concerns, enabling commands to be pure functions
that operate on injected context rather than hardcoded configurations.

Core Components:
- LocalCommandContext: Primary context container for local development
- Context Providers: Specialized providers for different aspects (MCP, data, validation)
- Context Factories: Factory patterns for context creation and injection

Usage:
    from context import LocalCommandContext, create_local_context

    # Create context for command execution
    context = create_local_context(command_name="fundamental_analyst_discover")

    # Use context in command
    output_path = context.data.get_output_path("fundamental_analysis", "discovery")
    mcp_client = context.mcp.get_client("yahoo-finance")
"""

from .base_context import (
    LocalCommandContext,
    ExecutionContext,
    DataContext,
    MCPContext,
    ValidationContext,
    create_local_context
)

from .providers import (
    MCPContextProvider,
    DataContextProvider,
    ValidationContextProvider
)

__all__ = [
    "LocalCommandContext",
    "ExecutionContext",
    "DataContext",
    "MCPContext",
    "ValidationContext",
    "create_local_context",
    "MCPContextProvider",
    "DataContextProvider",
    "ValidationContextProvider"
]
