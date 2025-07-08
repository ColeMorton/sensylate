"""
Context-Aware Command Executor

This module provides the base framework for executing Sensylate commands
with injected context. Commands extend the CommandExecutor base class
and use context providers instead of hardcoded configurations.

The executor pattern separates command logic from environmental concerns,
enabling commands to be pure functions that operate on injected context.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

from context import LocalCommandContext, create_local_context
from context.providers import MCPContextProvider, DataContextProvider, ValidationContextProvider


logger = logging.getLogger(__name__)


class CommandExecutionError(Exception):
    """Raised when command execution fails"""
    pass


class CommandExecutor(ABC):
    """
    Base class for context-aware command execution.

    This class provides the foundation for all Sensylate commands,
    handling context injection, provider initialization, and common
    execution patterns. Commands extend this class and implement
    the execute_command method.

    Features:
    - Automatic context injection
    - Provider initialization (MCP, Data, Validation)
    - Error handling and logging
    - Result standardization
    - Performance tracking

    Usage:
        class FundamentalDiscoveryExecutor(CommandExecutor):
            def execute_command(self, ticker: str) -> Dict[str, Any]:
                # Use self.mcp_provider, self.data_provider, etc.
                return {"ticker": ticker, "data": data}

        executor = FundamentalDiscoveryExecutor(context)
        result = executor.execute(ticker="AAPL")
    """

    def __init__(self, context: LocalCommandContext):
        self.context = context
        self.mcp_provider = MCPContextProvider(context.mcp)
        self.data_provider = DataContextProvider(context.data)
        self.validation_provider = ValidationContextProvider(context.validation)

        self._execution_start = None
        self._execution_end = None

    @abstractmethod
    def execute_command(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the command with given arguments.

        This method must be implemented by subclasses to define
        the specific command logic. It should use the injected
        context providers rather than hardcoded configurations.

        Args:
            **kwargs: Command-specific arguments

        Returns:
            Dictionary containing command results
        """
        pass

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Main execution method with error handling and logging.

        This method wraps the command execution with standard
        error handling, performance tracking, and result formatting.

        Args:
            **kwargs: Command-specific arguments

        Returns:
            Standardized result dictionary

        Raises:
            CommandExecutionError: If command execution fails
        """
        self._execution_start = datetime.now()

        try:
            logger.info(f"Starting command execution: {self.context.execution.command_name}")

            # Validate inputs if validation is enabled
            if self.context.validation.format_validation:
                self._validate_inputs(**kwargs)

            # Execute command
            result = self.execute_command(**kwargs)

            # Validate outputs
            validation_result = self._validate_outputs(result)

            # Add execution metadata
            self._execution_end = datetime.now()
            execution_time = (self._execution_end - self._execution_start).total_seconds()

            final_result = {
                "command_result": result,
                "execution_metadata": {
                    "command_name": self.context.execution.command_name,
                    "execution_time_seconds": execution_time,
                    "start_time": self._execution_start.isoformat(),
                    "end_time": self._execution_end.isoformat(),
                    "success": True
                },
                "validation_result": validation_result,
                "context_summary": self._get_context_summary()
            }

            logger.info(f"Command completed successfully in {execution_time:.2f}s")
            return final_result

        except Exception as e:
            self._execution_end = datetime.now()
            execution_time = (self._execution_end - self._execution_start).total_seconds() if self._execution_start else 0

            logger.error(f"Command execution failed after {execution_time:.2f}s: {e}")

            error_result = {
                "command_result": None,
                "execution_metadata": {
                    "command_name": self.context.execution.command_name,
                    "execution_time_seconds": execution_time,
                    "start_time": self._execution_start.isoformat() if self._execution_start else None,
                    "end_time": self._execution_end.isoformat(),
                    "success": False,
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                "validation_result": None,
                "context_summary": self._get_context_summary()
            }

            raise CommandExecutionError(f"Command execution failed: {e}") from e

    def _validate_inputs(self, **kwargs):
        """Validate command inputs"""
        # Basic input validation - can be overridden by subclasses
        for key, value in kwargs.items():
            if value is None:
                raise CommandExecutionError(f"Required parameter '{key}' is None")

    def _validate_outputs(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate command outputs"""
        if not isinstance(result, dict):
            raise CommandExecutionError("Command result must be a dictionary")

        # Use validation provider for format validation
        if self.context.validation.format_validation:
            validation_result = self.validation_provider.validate_json_format(result)

            if not validation_result.is_valid:
                error_issues = [issue for issue in validation_result.issues
                              if issue.severity.value in ["error", "critical"]]
                if error_issues:
                    raise CommandExecutionError(f"Output validation failed: {error_issues[0].message}")

            return {
                "is_valid": validation_result.is_valid,
                "confidence_score": validation_result.confidence_score,
                "issues_count": len(validation_result.issues),
                "validation_timestamp": datetime.now().isoformat()
            }

        return None

    def _get_context_summary(self) -> Dict[str, Any]:
        """Get summary of context configuration"""
        return {
            "environment": self.context.execution.environment,
            "working_directory": str(self.context.execution.working_directory),
            "quality_gates": self.context.validation.quality_gates.value,
            "mcp_servers_available": len(self.context.mcp.available_servers),
            "cache_enabled": self.context.data.cache_enabled,
            "backup_enabled": self.context.data.backup_enabled
        }

    def save_result(self, result: Dict[str, Any], filename: str = None) -> Path:
        """
        Save command result to output file.

        Args:
            result: Result data to save
            filename: Optional filename (auto-generated if not provided)

        Returns:
            Path to saved file
        """
        # Determine output path based on command
        category = self._get_output_category()
        subcategory = self._get_output_subcategory()
        output_path = self.data_provider.get_output_path(category, subcategory)

        # Generate filename if not provided
        if filename is None:
            base_name = self._get_output_base_name(result)
            filename = self.data_provider.generate_filename(
                base_name=base_name,
                extension="json",
                timestamp=self.context.execution.timestamp,
                suffix=subcategory
            )

        # Save result
        saved_path = self.data_provider.save_json_output(result, output_path, filename)
        logger.info(f"Result saved to: {saved_path}")

        return saved_path

    def _get_output_category(self) -> str:
        """Get output category for this command"""
        # Default implementation - can be overridden
        command_name = self.context.execution.command_name

        if "fundamental" in command_name:
            return "fundamental_analysis"
        elif "trade" in command_name:
            return "trading_analysis"
        elif "twitter" in command_name or "social" in command_name:
            return "content_generation"
        else:
            return "general"

    def _get_output_subcategory(self) -> str:
        """Get output subcategory for this command"""
        # Default implementation - can be overridden
        command_name = self.context.execution.command_name

        if "discover" in command_name:
            return "discovery"
        elif "analyze" in command_name:
            return "analyze"
        elif "synthesize" in command_name:
            return "synthesize"
        elif "validate" in command_name:
            return "validate"
        else:
            return "output"

    def _get_output_base_name(self, result: Dict[str, Any]) -> str:
        """Get base name for output file"""
        # Try to extract ticker from result
        if isinstance(result, dict):
            for key in ["ticker", "symbol", "stock_symbol"]:
                if key in result and result[key]:
                    return str(result[key]).upper()

        # Default to command name
        return self.context.execution.command_name

    def get_mcp_client(self, server_name: str):
        """Get MCP client for server"""
        return self.mcp_provider.get_client(server_name)

    def cache_data(self, key: str, data: Any, ttl_seconds: int = 3600) -> Path:
        """Cache data using data provider"""
        return self.data_provider.cache_data(key, data, ttl_seconds)

    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data using data provider"""
        return self.data_provider.get_cached_data(key)


class FundamentalDiscoveryExecutor(CommandExecutor):
    """
    Example implementation of CommandExecutor for fundamental discovery.

    This demonstrates how to implement a context-aware command that uses
    MCP providers instead of hardcoded service access.
    """

    def execute_command(self, ticker: str, depth: str = "comprehensive") -> Dict[str, Any]:
        """
        Execute fundamental discovery for given ticker.

        Args:
            ticker: Stock ticker symbol
            depth: Analysis depth (summary, standard, comprehensive, deep-dive)

        Returns:
            Discovery results dictionary
        """
        # Validate ticker
        ticker_validation = self.validation_provider.validate_ticker_symbol(ticker)
        if not ticker_validation.is_valid:
            raise CommandExecutionError(f"Invalid ticker: {ticker}")

        ticker = ticker.upper().strip()

        # Check cache first
        cache_key = f"fundamental_discovery_{ticker}_{depth}"
        cached_result = self.get_cached_data(cache_key)
        if cached_result:
            logger.info(f"Using cached discovery data for {ticker}")
            return cached_result

        discovery_data = {
            "metadata": {
                "command_name": self.context.execution.command_name,
                "execution_timestamp": self.context.execution.timestamp.isoformat(),
                "framework_phase": "discover",
                "ticker": ticker,
                "depth": depth,
                "data_collection_methodology": "context_aware_mcp_protocol"
            },
            "market_data": {},
            "financial_metrics": {},
            "company_intelligence": {},
            "data_quality_assessment": {}
        }

        # Collect market data via MCP
        try:
            with self.get_mcp_client("yahoo-finance") as client:
                # Get stock fundamentals
                fundamentals = client.call_tool("get_stock_fundamentals", {"ticker": ticker})
                if fundamentals:
                    discovery_data["market_data"] = self._extract_market_data(fundamentals)
                    discovery_data["financial_metrics"] = self._extract_financial_metrics(fundamentals)

                # Get historical data if comprehensive analysis
                if depth in ["comprehensive", "deep-dive"]:
                    market_data = client.call_tool("get_market_data", {"ticker": ticker, "period": "5y"})
                    if market_data:
                        discovery_data["market_data"]["historical_data"] = market_data

                # Get financial statements
                financial_statements = client.call_tool("get_financial_statements", {"ticker": ticker})
                if financial_statements:
                    discovery_data["company_intelligence"]["financial_statements"] = financial_statements

        except Exception as e:
            logger.warning(f"MCP data collection failed: {e}")
            discovery_data["data_quality_assessment"]["mcp_errors"] = str(e)

        # Validate discovery data
        validation_result = self.validation_provider.validate_fundamental_data(discovery_data, ticker)
        discovery_data["data_quality_assessment"]["validation_result"] = {
            "is_valid": validation_result.is_valid,
            "confidence_score": validation_result.confidence_score,
            "issues_count": len(validation_result.issues)
        }

        # Cache result if valid
        if validation_result.is_valid and validation_result.confidence_score >= self.context.validation.confidence_threshold:
            self.cache_data(cache_key, discovery_data, ttl_seconds=1800)  # 30 minute cache

        return discovery_data

    def _extract_market_data(self, fundamentals: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market data from fundamentals response"""
        # Implementation would extract specific fields
        # This is a simplified version
        return {
            "current_price": fundamentals.get("current_price"),
            "market_cap": fundamentals.get("market_cap"),
            "volume": fundamentals.get("volume"),
            "confidence": 0.9
        }

    def _extract_financial_metrics(self, fundamentals: Dict[str, Any]) -> Dict[str, Any]:
        """Extract financial metrics from fundamentals response"""
        return {
            "pe_ratio": fundamentals.get("pe_ratio"),
            "profit_margin": fundamentals.get("profit_margin"),
            "revenue_ttm": fundamentals.get("revenue_ttm"),
            "confidence": 0.9
        }


def create_command_executor(command_name: str, config_path: Path = None) -> CommandExecutor:
    """
    Factory function to create appropriate command executor.

    Args:
        command_name: Name of command to create executor for
        config_path: Optional path to context configuration

    Returns:
        CommandExecutor instance for the command
    """
    # Create context for command
    context = create_local_context(command_name, mcp_config_path=config_path)

    # Return appropriate executor based on command
    if "fundamental" in command_name and "discover" in command_name:
        return FundamentalDiscoveryExecutor(context)

    # Default to base executor (would need command-specific implementations)
    return CommandExecutor(context)
