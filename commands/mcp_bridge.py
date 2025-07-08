"""
MCP-Command Bridge for Tool Discovery and Mapping

This module provides the bridge between Sensylate commands and MCP infrastructure,
handling tool discovery, capability mapping, and automatic tool selection based
on command requirements. It enables commands to declaratively specify their
MCP tool needs rather than hardcoding specific server calls.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Set
from enum import Enum

from context.providers import MCPContextProvider


logger = logging.getLogger(__name__)


class ToolRequirementType(Enum):
    """Types of tool requirements"""
    REQUIRED = "required"
    OPTIONAL = "optional"
    FALLBACK = "fallback"


@dataclass
class MCPToolRequirement:
    """Represents a tool requirement for a command"""
    server: str
    tool: str
    requirement_type: ToolRequirementType
    parameters: Dict[str, Any]
    description: str = ""
    alternatives: List[str] = None

    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []


@dataclass
class ToolMapping:
    """Maps command capabilities to available MCP tools"""
    command_name: str
    requirements: List[MCPToolRequirement]
    server_preferences: List[str]
    fallback_strategy: str = "best_available"


class CapabilityDiscoveryError(Exception):
    """Raised when capability discovery fails"""
    pass


class MCPBridge:
    """
    Bridge between commands and MCP infrastructure.

    This class provides tool discovery, capability mapping, and automatic
    tool selection for commands. It abstracts the complexity of MCP server
    interactions while providing a declarative interface for command requirements.

    Features:
    - Automatic tool discovery across all servers
    - Command-to-tool mapping
    - Server preference handling
    - Fallback strategy implementation
    - Health-aware tool selection

    Usage:
        bridge = MCPBridge(mcp_provider)
        mapping = bridge.get_command_mapping("fundamental_analyst_discover")
        tools = bridge.resolve_tools(mapping.requirements)
    """

    def __init__(self, mcp_provider: MCPContextProvider):
        self.mcp_provider = mcp_provider
        self.tool_mappings = self._load_tool_mappings()
        self._capability_cache = {}

    def _load_tool_mappings(self) -> Dict[str, ToolMapping]:
        """Load predefined tool mappings for commands"""
        return {
            "fundamental_analyst_discover": ToolMapping(
                command_name="fundamental_analyst_discover",
                requirements=[
                    MCPToolRequirement(
                        server="yahoo-finance",
                        tool="get_stock_fundamentals",
                        requirement_type=ToolRequirementType.REQUIRED,
                        parameters={"ticker": "string"},
                        description="Get comprehensive fundamental data"
                    ),
                    MCPToolRequirement(
                        server="yahoo-finance",
                        tool="get_market_data",
                        requirement_type=ToolRequirementType.REQUIRED,
                        parameters={"ticker": "string", "period": "string"},
                        description="Get historical market data"
                    ),
                    MCPToolRequirement(
                        server="yahoo-finance",
                        tool="get_financial_statements",
                        requirement_type=ToolRequirementType.OPTIONAL,
                        parameters={"ticker": "string"},
                        description="Get detailed financial statements"
                    ),
                    MCPToolRequirement(
                        server="sec-edgar",
                        tool="get_company_filings",
                        requirement_type=ToolRequirementType.OPTIONAL,
                        parameters={"ticker": "string", "filing_type": "string"},
                        description="Get SEC regulatory filings"
                    ),
                    MCPToolRequirement(
                        server="sensylate-trading",
                        tool="get_fundamental_analysis",
                        requirement_type=ToolRequirementType.FALLBACK,
                        parameters={"ticker": "string"},
                        description="Get existing fundamental analysis"
                    )
                ],
                server_preferences=["yahoo-finance", "sec-edgar", "sensylate-trading"]
            ),

            "fundamental_analyst_validate": ToolMapping(
                command_name="fundamental_analyst_validate",
                requirements=[
                    MCPToolRequirement(
                        server="sensylate-trading",
                        tool="get_fundamental_analysis",
                        requirement_type=ToolRequirementType.REQUIRED,
                        parameters={"ticker": "string"},
                        description="Get discovery data for validation"
                    ),
                    MCPToolRequirement(
                        server="yahoo-finance",
                        tool="get_stock_fundamentals",
                        requirement_type=ToolRequirementType.REQUIRED,
                        parameters={"ticker": "string"},
                        description="Cross-reference validation data"
                    )
                ],
                server_preferences=["sensylate-trading", "yahoo-finance"]
            ),

            "trade_history_analyze": ToolMapping(
                command_name="trade_history_analyze",
                requirements=[
                    MCPToolRequirement(
                        server="sensylate-trading",
                        tool="get_trading_performance",
                        requirement_type=ToolRequirementType.REQUIRED,
                        parameters={},
                        description="Get trading performance data"
                    ),
                    MCPToolRequirement(
                        server="yahoo-finance",
                        tool="get_market_data",
                        requirement_type=ToolRequirementType.OPTIONAL,
                        parameters={"ticker": "string", "period": "string"},
                        description="Get market context data"
                    )
                ],
                server_preferences=["sensylate-trading", "yahoo-finance"]
            ),

            "twitter_fundamental_analysis": ToolMapping(
                command_name="twitter_fundamental_analysis",
                requirements=[
                    MCPToolRequirement(
                        server="sensylate-trading",
                        tool="generate_blog_content",
                        requirement_type=ToolRequirementType.REQUIRED,
                        parameters={"ticker": "string", "content_type": "string"},
                        description="Generate content from analysis"
                    ),
                    MCPToolRequirement(
                        server="content-automation",
                        tool="create_social_content",
                        requirement_type=ToolRequirementType.OPTIONAL,
                        parameters={"ticker": "string", "analysis_type": "string", "key_points": "string"},
                        description="Create social media content"
                    )
                ],
                server_preferences=["sensylate-trading", "content-automation"]
            )
        }

    def discover_all_capabilities(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Discover all available MCP capabilities across servers.

        Args:
            force_refresh: Force rediscovery even if cached

        Returns:
            Dictionary of server capabilities
        """
        if not force_refresh and self._capability_cache:
            return self._capability_cache

        capabilities = {}

        # Get all available tools
        all_tools = self.mcp_provider.discover_all_tools(force_refresh)

        # Get server health
        health_summary = self.mcp_provider.get_health_summary()

        for server_name in self.mcp_provider.get_available_servers():
            server_tools = all_tools.get(server_name, [])
            server_health = health_summary["servers"].get(server_name, {})

            capabilities[server_name] = {
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                        "required_params": tool.required_params
                    }
                    for tool in server_tools
                ],
                "tool_count": len(server_tools),
                "health_status": server_health.get("status", "unknown"),
                "response_time": server_health.get("response_time", 0),
                "last_check": server_health.get("last_check")
            }

        self._capability_cache = capabilities
        return capabilities

    def get_command_mapping(self, command_name: str) -> Optional[ToolMapping]:
        """
        Get tool mapping for command.

        Args:
            command_name: Name of command

        Returns:
            ToolMapping if available, None otherwise
        """
        return self.tool_mappings.get(command_name)

    def resolve_tools(self, requirements: List[MCPToolRequirement]) -> Dict[str, Any]:
        """
        Resolve tool requirements to available MCP tools.

        Args:
            requirements: List of tool requirements

        Returns:
            Dictionary mapping requirement to resolved tool info
        """
        capabilities = self.discover_all_capabilities()
        resolution = {
            "resolved": [],
            "unresolved": [],
            "warnings": []
        }

        for requirement in requirements:
            resolved_tool = self._resolve_single_requirement(requirement, capabilities)

            if resolved_tool:
                resolution["resolved"].append({
                    "requirement": requirement,
                    "resolved_tool": resolved_tool,
                    "server": requirement.server,
                    "status": "available"
                })
            else:
                # Try alternatives
                alternative_found = False
                for alt_server in requirement.alternatives:
                    if alt_server in capabilities:
                        alt_tool = self._find_tool_in_server(requirement.tool, capabilities[alt_server])
                        if alt_tool:
                            resolution["resolved"].append({
                                "requirement": requirement,
                                "resolved_tool": alt_tool,
                                "server": alt_server,
                                "status": "alternative"
                            })
                            resolution["warnings"].append(
                                f"Using alternative server {alt_server} for {requirement.tool}"
                            )
                            alternative_found = True
                            break

                if not alternative_found:
                    resolution["unresolved"].append({
                        "requirement": requirement,
                        "reason": "tool_not_available",
                        "server": requirement.server
                    })

        return resolution

    def _resolve_single_requirement(
        self,
        requirement: MCPToolRequirement,
        capabilities: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Resolve single tool requirement"""
        server_name = requirement.server

        if server_name not in capabilities:
            return None

        server_info = capabilities[server_name]

        # Check server health
        if server_info["health_status"] not in ["healthy", "degraded"]:
            return None

        # Find tool
        return self._find_tool_in_server(requirement.tool, server_info)

    def _find_tool_in_server(self, tool_name: str, server_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find specific tool in server capabilities"""
        for tool in server_info["tools"]:
            if tool["name"] == tool_name:
                return tool
        return None

    def validate_command_requirements(self, command_name: str) -> Dict[str, Any]:
        """
        Validate that command requirements can be met.

        Args:
            command_name: Name of command to validate

        Returns:
            Validation result with availability status
        """
        mapping = self.get_command_mapping(command_name)
        if not mapping:
            return {
                "command": command_name,
                "has_mapping": False,
                "is_valid": False,
                "reason": "No tool mapping defined for command"
            }

        resolution = self.resolve_tools(mapping.requirements)

        # Check required tools
        required_requirements = [
            req for req in mapping.requirements
            if req.requirement_type == ToolRequirementType.REQUIRED
        ]

        resolved_required = [
            res for res in resolution["resolved"]
            if res["requirement"].requirement_type == ToolRequirementType.REQUIRED
        ]

        unresolved_required = [
            req for req in resolution["unresolved"]
            if req["requirement"].requirement_type == ToolRequirementType.REQUIRED
        ]

        is_valid = len(unresolved_required) == 0

        return {
            "command": command_name,
            "has_mapping": True,
            "is_valid": is_valid,
            "required_tools": len(required_requirements),
            "resolved_required": len(resolved_required),
            "unresolved_required": len(unresolved_required),
            "optional_tools": len([
                req for req in mapping.requirements
                if req.requirement_type == ToolRequirementType.OPTIONAL
            ]),
            "warnings": resolution["warnings"],
            "unresolved_tools": resolution["unresolved"]
        }

    def get_optimal_execution_plan(self, command_name: str) -> Dict[str, Any]:
        """
        Get optimal execution plan for command based on available tools.

        Args:
            command_name: Name of command

        Returns:
            Execution plan with ordered tool calls
        """
        mapping = self.get_command_mapping(command_name)
        if not mapping:
            raise CapabilityDiscoveryError(f"No mapping for command: {command_name}")

        resolution = self.resolve_tools(mapping.requirements)
        validation = self.validate_command_requirements(command_name)

        if not validation["is_valid"]:
            raise CapabilityDiscoveryError(
                f"Command requirements cannot be met: {validation['unresolved_tools']}"
            )

        # Order tools by preference and requirement type
        execution_steps = []

        # Required tools first, in server preference order
        for server in mapping.server_preferences:
            for resolved in resolution["resolved"]:
                if (resolved["server"] == server and
                    resolved["requirement"].requirement_type == ToolRequirementType.REQUIRED):
                    execution_steps.append({
                        "step": len(execution_steps) + 1,
                        "server": server,
                        "tool": resolved["requirement"].tool,
                        "requirement_type": "required",
                        "parameters": resolved["requirement"].parameters,
                        "description": resolved["requirement"].description
                    })

        # Optional tools second
        for server in mapping.server_preferences:
            for resolved in resolution["resolved"]:
                if (resolved["server"] == server and
                    resolved["requirement"].requirement_type == ToolRequirementType.OPTIONAL):
                    execution_steps.append({
                        "step": len(execution_steps) + 1,
                        "server": server,
                        "tool": resolved["requirement"].tool,
                        "requirement_type": "optional",
                        "parameters": resolved["requirement"].parameters,
                        "description": resolved["requirement"].description
                    })

        # Fallback tools last
        for resolved in resolution["resolved"]:
            if resolved["requirement"].requirement_type == ToolRequirementType.FALLBACK:
                execution_steps.append({
                    "step": len(execution_steps) + 1,
                    "server": resolved["server"],
                    "tool": resolved["requirement"].tool,
                    "requirement_type": "fallback",
                    "parameters": resolved["requirement"].parameters,
                    "description": resolved["requirement"].description
                })

        return {
            "command": command_name,
            "execution_steps": execution_steps,
            "total_steps": len(execution_steps),
            "estimated_servers": len(set(step["server"] for step in execution_steps)),
            "execution_strategy": mapping.fallback_strategy,
            "warnings": resolution["warnings"]
        }

    def get_command_coverage_report(self) -> Dict[str, Any]:
        """Get coverage report for all configured commands"""
        coverage_report = {
            "total_commands": len(self.tool_mappings),
            "commands": {},
            "server_usage": {},
            "tool_usage": {},
            "overall_health": True
        }

        for command_name in self.tool_mappings:
            validation = self.validate_command_requirements(command_name)
            coverage_report["commands"][command_name] = validation

            if not validation["is_valid"]:
                coverage_report["overall_health"] = False

        # Calculate server usage
        capabilities = self.discover_all_capabilities()
        for server_name in capabilities:
            usage_count = sum(
                1 for mapping in self.tool_mappings.values()
                for req in mapping.requirements
                if req.server == server_name
            )
            coverage_report["server_usage"][server_name] = {
                "command_count": usage_count,
                "health_status": capabilities[server_name]["health_status"],
                "available_tools": capabilities[server_name]["tool_count"]
            }

        return coverage_report


# Alias for backwards compatibility
CommandMCPBridge = MCPBridge
