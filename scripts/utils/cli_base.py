"""
CLI Base Framework

Provides standardized CLI infrastructure for all financial services with:
- Typer-based command line interface
- YAML configuration integration
- Consistent argument parsing and validation
- Output formatting (JSON, YAML, table, CSV)
- Error handling and logging
- Environment management
"""

import json
import logging
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import typer
import yaml
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config_loader import ConfigLoader, FinancialServiceConfig


class OutputFormat:
    """Output format constants"""

    JSON = "json"
    YAML = "yaml"
    TABLE = "table"
    CSV = "csv"


class CLIError(Exception):
    """Base exception for CLI errors"""

    pass


class ValidationError(CLIError):
    """Raised when input validation fails"""

    pass


class ServiceError(CLIError):
    """Raised when service operation fails"""

    pass


class BaseFinancialCLI(ABC):
    """
    Base class for financial service CLIs

    Provides:
    - Standardized command structure
    - Configuration management
    - Output formatting
    - Error handling
    - Logging
    """

    def __init__(
        self, service_name: str, description: str = "Financial data service CLI"
    ):
        self.service_name = service_name
        self.description = description
        self.app = typer.Typer(
            name=service_name, help=description, add_completion=False
        )
        self.console = Console()
        self.config_loader = ConfigLoader()
        self.logger = self._setup_logger()

        # Add common commands
        self._add_common_commands()

    def _setup_logger(self) -> logging.Logger:
        """Setup structured logging for CLI"""
        logger = logging.getLogger(f"financial_cli.{self.service_name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _add_common_commands(self) -> None:
        """Add common commands to all service CLIs"""

        @self.app.command("health")
        def health_check(
            env: str = typer.Option("dev", help="Environment (dev/test/prod)"),
            verbose: bool = typer.Option(
                False, "--verbose", "-v", help="Verbose output"
            ),
        ):
            """Check service health and configuration"""
            try:
                result = self.perform_health_check(env)
                self._output_result(
                    result, OutputFormat.JSON if verbose else OutputFormat.TABLE
                )
            except Exception as e:
                self._handle_error(e, "Health check failed")

        @self.app.command("config")
        def show_config(
            env: str = typer.Option("dev", help="Environment (dev/test/prod)"),
            validate: bool = typer.Option(
                False, "--validate", help="Validate configuration"
            ),
        ):
            """Show service configuration"""
            try:
                if validate:
                    result = self.config_loader.validate_configuration(env)
                    self._output_result(result, OutputFormat.JSON)
                else:
                    config = self.get_service_config(env)
                    self._output_result(config.dict(), OutputFormat.YAML)
            except Exception as e:
                self._handle_error(e, "Failed to load configuration")

        @self.app.command("cache")
        def cache_management(
            action: str = typer.Argument(
                ..., help="Cache action (clear/cleanup/stats)"
            ),
            env: str = typer.Option("dev", help="Environment"),
        ):
            """Manage service cache"""
            try:
                result = self.perform_cache_action(action, env)
                self._output_result(result, OutputFormat.JSON)
            except Exception as e:
                self._handle_error(e, f"Cache {action} failed")

    def get_service_config(self, env: str = "dev") -> FinancialServiceConfig:
        """Get validated service configuration"""
        return self.config_loader.get_service_config(self.service_name, env)

    def validate_ticker(self, ticker: str) -> str:
        """Validate and normalize ticker symbol"""
        if not ticker:
            raise ValidationError("Ticker symbol is required")

        ticker = ticker.strip().upper()

        # Basic validation
        if not ticker.isalnum() and not all(c.isalnum() or c in ".-" for c in ticker):
            raise ValidationError(f"Invalid ticker format: {ticker}")

        if len(ticker) > 10:
            raise ValidationError(f"Ticker too long: {ticker}")

        return ticker

    def _output_result(
        self,
        data: Any,
        format_type: str = OutputFormat.JSON,
        title: Optional[str] = None,
    ) -> None:
        """Output result in specified format"""

        if format_type == OutputFormat.JSON:
            output = json.dumps(data, indent=2, default=str)
            if title:
                rprint(Panel(output, title=title, expand=False))
            else:
                rprint(output)

        elif format_type == OutputFormat.YAML:
            output = yaml.dump(data, default_flow_style=False, sort_keys=False)
            if title:
                rprint(Panel(output, title=title, expand=False))
            else:
                rprint(output)

        elif format_type == OutputFormat.TABLE:
            self._output_table(data, title)

        elif format_type == OutputFormat.CSV:
            self._output_csv(data)

        else:
            raise CLIError(f"Unsupported output format: {format_type}")

    def _output_table(self, data: Any, title: Optional[str] = None) -> None:
        """Output data as a formatted table"""

        if isinstance(data, dict):
            table = Table(title=title or "Service Data")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="green")

            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, default=str)
                table.add_row(str(key), str(value))

            self.console.print(table)

        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # Table from list of dicts
            if not data:
                rprint("No data to display")
                return

            table = Table(title=title or "Service Data")

            # Add columns from first item
            for key in data[0].keys():
                table.add_column(str(key), style="cyan")

            # Add rows
            for item in data:
                row = []
                for key in data[0].keys():
                    value = item.get(key, "")
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, default=str)
                    row.append(str(value))
                table.add_row(*row)

            self.console.print(table)

        else:
            # Fallback to JSON for complex data
            self._output_result(data, OutputFormat.JSON, title)

    def _output_csv(self, data: Any) -> None:
        """Output data as CSV"""
        import csv
        import io

        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            rprint(output.getvalue())
        else:
            # Convert single dict to CSV
            if isinstance(data, dict):
                output = io.StringIO()
                writer = csv.writer(output)
                for key, value in data.items():
                    writer.writerow([key, value])
                rprint(output.getvalue())
            else:
                raise CLIError("CSV format not supported for this data type")

    def _handle_error(
        self, error: Exception, context: str = "Operation failed"
    ) -> None:
        """Handle and display errors consistently"""

        error_info = {
            "error": str(error),
            "error_type": type(error).__name__,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "service": self.service_name,
        }

        # Log error details
        self.logger.error(f"{context}: {error}")

        # Display user-friendly error
        self.console.print(
            Panel(
                f"[red]Error:[/red] {context}\n[yellow]Details:[/yellow] {str(error)}",
                title="❌ Operation Failed",
                border_style="red",
            )
        )

        # Exit with error code
        raise typer.Exit(1)

    def add_standard_options(self) -> Dict[str, Any]:
        """Get standard CLI options for financial service commands"""
        return {
            "env": typer.Option("dev", help="Environment (dev/test/prod)"),
            "output_format": typer.Option(
                OutputFormat.JSON, help="Output format (json/yaml/table/csv)"
            ),
            "verbose": typer.Option(False, "--verbose", "-v", help="Verbose output"),
            "no_cache": typer.Option(False, "--no-cache", help="Disable caching"),
            "timeout": typer.Option(30, help="Request timeout in seconds"),
        }

    @abstractmethod
    def perform_health_check(self, env: str) -> Dict[str, Any]:
        """Perform service-specific health check"""
        pass

    @abstractmethod
    def perform_cache_action(self, action: str, env: str) -> Dict[str, Any]:
        """Perform cache management action"""
        pass

    def run(self) -> None:
        """Run the CLI application"""
        try:
            self.app()
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled by user[/yellow]")
            raise typer.Exit(1)
        except Exception as e:
            self._handle_error(e, "Unexpected error")


class FinancialDataCLI:
    """
    Unified CLI for financial data services

    Provides a single entry point to access all financial services
    """

    def __init__(self):
        self.app = typer.Typer(
            name="financial-data",
            help="Unified financial data CLI",
            add_completion=False,
        )
        self.console = Console()
        self.config_loader = ConfigLoader()

        self._add_unified_commands()

    def _add_unified_commands(self) -> None:
        """Add unified commands for all services"""

        @self.app.command("list-services")
        def list_services(env: str = typer.Option("dev", help="Environment")):
            """List all available financial services"""
            try:
                services = self.config_loader.list_available_services(env)

                table = Table(title="Available Financial Services")
                table.add_column("Service", style="cyan")
                table.add_column("Description", style="green")

                service_descriptions = {
                    "yahoo_finance": "Yahoo Finance - Stock quotes, historical data, fundamentals",
                    "alpha_vantage": "Alpha Vantage - Technical indicators, news sentiment",
                    "fred": "FRED - Federal Reserve economic data",
                    "sec_edgar": "SEC EDGAR - Regulatory filings",
                    "fmp": "Financial Modeling Prep - Advanced financial data",
                    "coingecko": "CoinGecko - Cryptocurrency data",
                    "imf": "IMF - International economic data",
                }

                for service in services:
                    description = service_descriptions.get(
                        service, "Financial data service"
                    )
                    table.add_row(service, description)

                self.console.print(table)

            except Exception as e:
                self.console.print(f"[red]Error:[/red] {str(e)}")
                raise typer.Exit(1)

        @self.app.command("validate-config")
        def validate_config(env: str = typer.Option("dev", help="Environment")):
            """Validate configuration for all services"""
            try:
                result = self.config_loader.validate_configuration(env)

                if result["valid"]:
                    self.console.print(
                        Panel(
                            f"✅ Configuration valid for {result['services_validated']} services",
                            title="Configuration Validation",
                            border_style="green",
                        )
                    )
                else:
                    error_panel = f"❌ Configuration validation failed\n\n"
                    error_panel += "\n".join(f"• {error}" for error in result["errors"])

                    if result["warnings"]:
                        error_panel += "\n\n⚠️  Warnings:\n"
                        error_panel += "\n".join(
                            f"• {warning}" for warning in result["warnings"]
                        )

                    self.console.print(
                        Panel(
                            error_panel,
                            title="Configuration Validation",
                            border_style="red",
                        )
                    )

            except Exception as e:
                self.console.print(f"[red]Error:[/red] {str(e)}")
                raise typer.Exit(1)

    def run(self) -> None:
        """Run the unified CLI"""
        try:
            self.app()
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled by user[/yellow]")
            raise typer.Exit(1)
