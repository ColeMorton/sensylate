#!/usr/bin/env python3
"""
Service Health Manager

Comprehensive service health monitoring and validation system that:
- Validates CLI service availability and health status
- Performs contract schema validation with error/warning categorization
- Provides detailed health reporting for diagnostic purposes

Implements ComponentLifecycle for proper initialization phases:
- init(): Basic initialization, dependency injection
- configure(): Expensive CLI health checks and caching operations  
- start(): Use cached health check results for fast operations
"""

import importlib.util
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd

from component_lifecycle import ComponentLifecycle
from data_contract_discovery import DataContract
from utils.logging_setup import setup_logging


class ServiceHealthManager(ComponentLifecycle):
    """Manages service health checks and contract schema validation"""

    def __init__(self, scripts_dir: Path, cli_service_capabilities: Dict[str, Any]):
        # Initialize ComponentLifecycle
        super().__init__("service_health_manager")
        
        # Store dependencies (injected during init phase)
        self.scripts_dir = scripts_dir
        self.cli_service_capabilities = cli_service_capabilities
        
        # Cached health check results (populated during configure phase)
        self._cached_service_dependencies: Optional[Dict[str, Any]] = None
        self._cached_schema_validation: Optional[Dict[str, Any]] = None

    def _do_init(self) -> None:
        """Phase 1: Basic initialization"""
        self.logger.info(f"ServiceHealthManager: Phase 1 - Basic initialization")
        # Basic dependency validation already done in __init__
        
    def _do_configure(self) -> None:
        """Phase 2: Expensive CLI health checks and caching operations"""
        self.logger.info(f"ServiceHealthManager: Phase 2 - Caching expensive health checks")
        
        # Cache service dependencies during configure phase
        self._cache_service_dependencies()
        
    def _do_start(self) -> None:
        """Phase 3: Ready for fast operations"""
        self.logger.info(f"ServiceHealthManager: Phase 3 - Ready for cached operations")
        # Service health manager ready for fast cached operations
        
    def _cache_service_dependencies(self) -> None:
        """Cache expensive service dependency validation (CLI health checks)"""
        self.logger.info("Caching service dependency validation (expensive CLI operations)")
        
        # Perform expensive operations once during configure phase
        availability_result = self._validate_service_availability()
        health_result = None
        
        if availability_result["success"]:
            health_result = self._validate_service_health()
            
        # Cache the complete validation result
        self._cached_service_dependencies = {
            "success": availability_result["success"] and (health_result is None or health_result["success"]),
            "availability": availability_result,
            "health": health_result,
            "stage": "health" if health_result and not health_result["success"] else "availability" if not availability_result["success"] else None,
            "error": (health_result and health_result.get("error")) or availability_result.get("error")
        }
        
        self.logger.info(f"Cached service dependencies validation: {self._cached_service_dependencies['success']}")

    def validate_service_dependencies(self) -> Dict[str, Any]:
        """Fast service dependency validation using cached results"""
        if self._cached_service_dependencies is None:
            self.logger.error("ServiceHealthManager not properly configured - cached dependencies missing")
            raise RuntimeError("ServiceHealthManager must go through configure() phase before validate_service_dependencies()")
            
        self.logger.info("Using cached service dependency validation results")
        return self._cached_service_dependencies.copy()

    def _validate_service_availability(self) -> Dict[str, Any]:
        """Validate that CLI services are available and executable"""
        from cli_wrapper import get_service_manager

        failed_services = []
        availability_details = {}

        try:
            service_manager = get_service_manager()

            for service_name in self.cli_service_capabilities.keys():
                # Special case: live_signals_dashboard is handled directly, not via CLI wrapper
                if service_name == "live_signals_dashboard":
                    # Check if the live_signals_dashboard.py file exists
                    dashboard_script = self.scripts_dir / "live_signals_dashboard.py"
                    is_available = dashboard_script.exists()
                    availability_details[service_name] = {
                        "available": is_available,
                        "error": (
                            None
                            if is_available
                            else f"Dashboard script not found: {dashboard_script}"
                        ),
                    }
                    if not is_available:
                        failed_services.append(service_name)
                    continue

                try:
                    # Check if service is available via service manager
                    service_wrapper = service_manager.get_service(service_name)
                    is_available = service_wrapper.is_available()

                    availability_details[service_name] = {
                        "available": is_available,
                        "error": (
                            None
                            if is_available
                            else f"Service {service_name} not available"
                        ),
                    }

                    if not is_available:
                        failed_services.append(service_name)

                except Exception as e:
                    availability_details[service_name] = {
                        "available": False,
                        "error": str(e),
                    }
                    failed_services.append(service_name)

            success = len(failed_services) == 0
            error_msg = None

            if not success:
                error_msg = f"Services not available: {', '.join(failed_services)}"

            return {
                "success": success,
                "failed_services": failed_services,
                "availability_details": availability_details,
                "error": error_msg,
            }

        except Exception as e:
            return {
                "success": False,
                "failed_services": list(self.cli_service_capabilities.keys()),
                "availability_details": {},
                "error": f"Service manager initialization failed: {e}",
            }

    def _validate_service_health(self) -> Dict[str, Any]:
        """Validate that available services are healthy and can execute basic operations"""
        from cli_wrapper import get_service_manager

        failed_services = []
        health_details: dict[str, dict[str, Union[bool, str, None]]] = {}

        try:
            service_manager = get_service_manager()

            for service_name in self.cli_service_capabilities.keys():
                # Special case: live_signals_dashboard is handled directly, not via CLI wrapper
                if service_name == "live_signals_dashboard":
                    # Check if the dashboard script can be imported (basic health check)
                    try:
                        dashboard_script = (
                            self.scripts_dir / "live_signals_dashboard.py"
                        )
                        if dashboard_script.exists():
                            spec = importlib.util.spec_from_file_location(
                                "live_signals_dashboard", dashboard_script
                            )
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            health_details[service_name] = {
                                "healthy": True,
                                "error": None,
                            }
                        else:
                            health_details[service_name] = {
                                "healthy": False,
                                "error": "Dashboard script not found",
                            }
                            failed_services.append(service_name)
                    except Exception as e:
                        health_details[service_name] = {
                            "healthy": False,
                            "error": f"Dashboard script import failed: {e}",
                        }
                        failed_services.append(service_name)
                    continue

                try:
                    # Get service wrapper and check if available
                    service_wrapper = service_manager.get_service(service_name)

                    if not service_wrapper.is_available():
                        health_details[service_name] = {
                            "healthy": False,
                            "error": "Service not available for health check",
                        }
                        failed_services.append(service_name)
                        continue

                    # Execute health check
                    health_result = service_wrapper.health_check()

                    if health_result.get("status") == "healthy":
                        health_details[service_name] = {
                            "healthy": True,
                            "error": None,
                            "health_data": health_result,
                        }
                    else:
                        health_details[service_name] = {
                            "healthy": False,
                            "error": health_result.get("error", "Health check failed"),
                        }
                        failed_services.append(service_name)

                except Exception as e:
                    health_details[service_name] = {
                        "healthy": False,
                        "error": f"Health check exception: {e}",
                    }
                    failed_services.append(service_name)

            success = len(failed_services) == 0
            error_msg = None

            if not success:
                error_msg = (
                    f"Services failed health check: {', '.join(failed_services)}"
                )

            return {
                "success": success,
                "failed_services": failed_services,
                "health_details": health_details,
                "error": error_msg,
            }

        except Exception as e:
            return {
                "success": False,
                "failed_services": list(self.cli_service_capabilities.keys()),
                "health_details": {},
                "error": f"Service health validation failed: {e}",
            }

    def validate_contract_schemas(
        self, contracts: List[DataContract]
    ) -> Dict[str, Any]:
        """Validate that contract data meets expected schemas with warning vs error categorization"""
        schema_errors = []
        schema_warnings = []
        validated_contracts = 0

        for contract in contracts:
            try:
                if not contract.file_path.exists():
                    continue  # Skip non-existent files, will be handled by other validation

                # Check if file is empty or has only headers
                file_size = contract.file_path.stat().st_size
                if file_size == 0:
                    schema_warnings.append(
                        f"File {contract.contract_id} is empty - will be populated by data pipeline"
                    )
                    continue

                # Enhanced CSV validation with empty file handling
                try:
                    df = pd.read_csv(contract.file_path)

                    # Check if DataFrame is empty after parsing
                    if df.empty:
                        schema_warnings.append(
                            f"File {contract.contract_id} contains only headers - will be populated by data pipeline"
                        )
                        continue

                except pd.errors.EmptyDataError:
                    schema_warnings.append(
                        f"File {contract.contract_id} has no data rows - will be populated by data pipeline"
                    )
                    continue
                except Exception as csv_error:
                    schema_errors.append(
                        f"Failed to parse CSV for {contract.contract_id}: {csv_error}"
                    )
                    continue

                # Validate data types based on contract category - now returns (errors, warnings)
                if contract.category == "trade-history":
                    errors, warnings = self._validate_trade_history_schema(df, contract)
                    schema_errors.extend(errors)
                    schema_warnings.extend(warnings)
                elif contract.category == "portfolio":
                    errors, warnings = self._validate_portfolio_schema(df, contract)
                    schema_errors.extend(errors)
                    schema_warnings.extend(warnings)
                elif contract.category == "open-positions":
                    errors, warnings = self._validate_open_positions_schema(
                        df, contract
                    )
                    schema_errors.extend(errors)
                    schema_warnings.extend(warnings)

                validated_contracts += 1

            except Exception as e:
                schema_errors.append(
                    f"Schema validation failed for {contract.contract_id}: {e}"
                )

        # Only fail on critical errors, not warnings
        success = len(schema_errors) == 0

        # Log warnings separately
        for warning in schema_warnings:
            self.logger.warning(f"Schema validation warning: {warning}")

        return {
            "success": success,
            "schema_errors": schema_errors,
            "schema_warnings": schema_warnings,
            "validated_contracts": validated_contracts,
        }

    def _validate_trade_history_schema(
        self, df: pd.DataFrame, contract: DataContract
    ) -> Tuple[List[str], List[str]]:
        """Validate trade history specific schema requirements - returns (errors, warnings)"""
        errors: list[str] = []
        warnings: list[str] = []

        # Required columns for trade history
        required_columns = {
            "Ticker",
            "PnL",
            "Status",
            "Entry_Timestamp",
            "Exit_Timestamp",
        }
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            errors.append(
                f"Missing trade history columns in {contract.contract_id}: {missing_columns}"
            )

        if len(df) > 0:
            # Validate PnL is numeric
            try:
                pd.to_numeric(df["PnL"], errors="coerce")
            except Exception:
                errors.append(
                    f"PnL column contains non-numeric values in {contract.contract_id}"
                )

            # Validate Status values
            valid_statuses = {"Open", "Closed"}
            invalid_statuses = set(df["Status"].unique()) - valid_statuses
            if invalid_statuses:
                errors.append(
                    f"Invalid Status values in {contract.contract_id}: {invalid_statuses}"
                )

        return errors, warnings

    def _validate_portfolio_schema(
        self, df: pd.DataFrame, contract: DataContract
    ) -> Tuple[List[str], List[str]]:
        """Validate portfolio specific schema requirements - returns (errors, warnings)"""
        errors: list[str] = []
        warnings: list[str] = []

        # Check for Date column - treat as warning since portfolio data might have different structures
        required_columns = {"Date"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            warnings.append(
                f"Missing portfolio columns in {contract.contract_id}: {missing_columns}"
            )

        if len(df) > 0 and "Date" in df.columns:
            # Validate Date format - treat as warning since data might be parseable in different format
            try:
                pd.to_datetime(df["Date"])
            except Exception:
                warnings.append(f"Invalid Date format in {contract.contract_id}")

        return errors, warnings

    def _validate_open_positions_schema(
        self, df: pd.DataFrame, contract: DataContract
    ) -> Tuple[List[str], List[str]]:
        """Validate open positions specific schema requirements - returns (errors, warnings)"""
        errors: list[str] = []
        warnings: list[str] = []

        # Required columns for open positions
        required_columns = {"Ticker", "PnL", "Date"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            errors.append(
                f"Missing open positions columns in {contract.contract_id}: {missing_columns}"
            )

        if len(df) > 0:
            # Validate PnL is numeric
            try:
                pd.to_numeric(df["PnL"], errors="coerce")
            except Exception:
                errors.append(
                    f"PnL column contains non-numeric values in {contract.contract_id}"
                )

            # Validate Date format
            try:
                pd.to_datetime(df["Date"])
            except Exception:
                errors.append(f"Invalid Date format in {contract.contract_id}")

        return errors, warnings