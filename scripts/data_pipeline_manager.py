#!/usr/bin/env python3
"""
Contract-First Data Pipeline Manager

Implements contract-driven architecture where frontend/public/data/ directory structure
serves as the authoritative source of data requirements. Automatically discovers
data contracts and orchestrates CLI services to fulfill them.

Features:
- Automatic contract discovery from frontend directory structure
- Dynamic mapping of contracts to CLI services
- Schema validation and compliance checking
- Pre-commit integration with fail-fast approach
"""

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from cli_service_script import CLIServiceScript
from data_contract_discovery import (
    ContractDiscoveryResult,
    DataContract,
    DataContractDiscovery,
)
from errors import ConfigurationError, ValidationError
from result_types import ProcessingResult
from script_config import ScriptConfig
from utils.logging_setup import setup_logging


class DryRunReport:
    """Comprehensive dry-run analysis report for data pipeline operations"""

    def __init__(self):
        """Initialize empty dry-run report"""
        self.start_time = datetime.now()
        self.contracts = []
        self.current_data_status = {}
        self.update_plan = {}
        self.operations_sequence = []
        self.projected_results = {}
        self.service_mappings = {}
        self.validation_results = {}
        self.errors = []
        self.warnings = []

    def add_contract(self, contract: DataContract, status: str, reason: str = ""):
        """Add contract analysis to report"""
        self.contracts.append(
            {
                "contract_id": contract.contract_id,
                "category": contract.category,
                "file_path": str(contract.file_path),
                "relative_path": contract.relative_path,
                "status": status,
                "reason": reason,
                "schema_columns": len(contract.schema) if contract.schema else 0,
                "freshness_threshold_hours": contract.freshness_threshold_hours,
            }
        )

    def set_current_data_status(self, category: str, file_status_data: Dict[str, Any]):
        """Set current data status for a category"""
        self.current_data_status[category] = file_status_data

    def add_update_plan_item(
        self, file_path: str, reason: str, estimated_time: float, row_count: int = 0
    ):
        """Add item to update plan"""
        self.update_plan[file_path] = {
            "reason": reason,
            "estimated_time": estimated_time,
            "projected_row_count": row_count,
            "estimated_size_mb": round(row_count * 0.05 / 1000, 2)
            if row_count > 0
            else 0.0,
        }

    def add_operation(self, operation: str, duration: float, details: str = ""):
        """Add operation to sequence"""
        self.operations_sequence.append(
            {
                "operation": operation,
                "estimated_duration": duration,
                "details": details,
                "timestamp": datetime.now(),
            }
        )

    def set_service_mapping(self, contract_id: str, services: List[str]):
        """Set service mapping for contract"""
        self.service_mappings[contract_id] = services

    def add_validation_result(
        self, contract_id: str, is_valid: bool, issues: List[str]
    ):
        """Add validation result"""
        self.validation_results[contract_id] = {
            "is_valid": is_valid,
            "issues": issues,
        }

    def add_error(self, error: str):
        """Add error to report"""
        self.errors.append(error)

    def add_warning(self, warning: str):
        """Add warning to report"""
        self.warnings.append(warning)

    def generate_text_report(self) -> str:
        """Generate human-readable text report"""
        report_lines = []

        # Header
        report_lines.append("📊 DATA PIPELINE DRY-RUN REPORT")
        report_lines.append("=" * 50)
        report_lines.append(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append("")

        # Contract Discovery
        report_lines.append("CONTRACT DISCOVERY")
        report_lines.append("-" * 20)
        total_contracts = len(self.contracts)
        categories = set(c["category"] for c in self.contracts)
        new_contracts = len([c for c in self.contracts if c["status"] == "new"])
        modified_contracts = len(
            [c for c in self.contracts if c["status"] == "modified"]
        )

        report_lines.append(f"- Total contracts: {total_contracts}")
        report_lines.append(
            f"- Categories: {', '.join(categories)} ({len(categories)} total)"
        )
        report_lines.append(f"- New contracts: {new_contracts}")
        report_lines.append(f"- Modified contracts: {modified_contracts}")
        report_lines.append("")

        # Current Data Status
        report_lines.append("CURRENT DATA STATUS")
        report_lines.append("-" * 20)
        total_files = sum(
            len(status.get("files", {})) for status in self.current_data_status.values()
        )
        fresh_files = sum(
            len(
                [
                    f
                    for f, data in status.get("files", {}).items()
                    if data.get("status") == "fresh"
                ]
            )
            for status in self.current_data_status.values()
        )
        stale_files = sum(
            len(
                [
                    f
                    for f, data in status.get("files", {}).items()
                    if data.get("status") == "stale"
                ]
            )
            for status in self.current_data_status.values()
        )
        missing_files = sum(
            len(
                [
                    f
                    for f, data in status.get("files", {}).items()
                    if not data.get("exists", True)
                ]
            )
            for status in self.current_data_status.values()
        )
        total_size_bytes = sum(
            sum(data.get("size_bytes", 0) for data in status.get("files", {}).values())
            for status in self.current_data_status.values()
        )

        report_lines.append(f"- Fresh files: {fresh_files}")
        report_lines.append(f"- Stale files: {stale_files} (>24h old)")
        report_lines.append(f"- Missing files: {missing_files}")
        report_lines.append(f"- Total size: {total_size_bytes / (1024*1024):.1f}MB")
        report_lines.append("")

        # Update Plan
        report_lines.append("UPDATE PLAN")
        report_lines.append("-" * 12)
        files_to_update = len(self.update_plan)
        total_estimated_time = sum(
            item["estimated_time"] for item in self.update_plan.values()
        )
        unique_services = set()
        for services in self.service_mappings.values():
            unique_services.update(services)

        report_lines.append(f"- Files to update: {files_to_update}")
        if files_to_update > 0:
            reasons: Dict[str, int] = {}
            for item in self.update_plan.values():
                reason = item["reason"]
                reasons[reason] = reasons.get(reason, 0) + 1
            reason_summary = ", ".join(
                f"{reason} ({count})" for reason, count in reasons.items()
            )
            report_lines.append(f"- Reasons: {reason_summary}")
        report_lines.append(f"- Estimated processing time: {total_estimated_time:.0f}s")
        report_lines.append(
            f"- Services required: {', '.join(sorted(unique_services))}"
        )
        report_lines.append("")

        # Operations Sequence
        if self.operations_sequence:
            report_lines.append("OPERATIONS SEQUENCE")
            report_lines.append("-" * 19)
            for i, op in enumerate(self.operations_sequence, 1):
                details = f" - {op['details']}" if op["details"] else ""
                report_lines.append(
                    f"{i}. {op['operation']} ({op['estimated_duration']:.1f}s){details}"
                )
            report_lines.append("")

        # Projected Results
        report_lines.append("PROJECTED RESULTS")
        report_lines.append("-" * 17)
        total_projected_rows = sum(
            item["projected_row_count"] for item in self.update_plan.values()
        )
        total_projected_size = sum(
            item["estimated_size_mb"] for item in self.update_plan.values()
        )
        all_valid = all(
            result["is_valid"] for result in self.validation_results.values()
        )

        report_lines.append(f"- Total files after update: {total_files}")
        if total_projected_size > 0:
            report_lines.append(f"- Estimated total size: {total_projected_size:.1f}MB")
        if total_projected_rows > 0:
            report_lines.append(f"- Total projected rows: {total_projected_rows:,}")
        report_lines.append(
            f"- Data quality: {'All validations would pass' if all_valid else 'Some validation issues'}"
        )
        report_lines.append(
            f"- Schema compliance: {len([r for r in self.validation_results.values() if r['is_valid']])}/{len(self.validation_results)} contracts"
        )
        report_lines.append("")

        # Errors and Warnings
        if self.errors:
            report_lines.append("ERRORS")
            report_lines.append("-" * 6)
            for error in self.errors:
                report_lines.append(f"❌ {error}")
            report_lines.append("")

        if self.warnings:
            report_lines.append("WARNINGS")
            report_lines.append("-" * 8)
            for warning in self.warnings:
                report_lines.append(f"⚠️  {warning}")
            report_lines.append("")

        # Footer
        execution_time = (datetime.now() - self.start_time).total_seconds()
        report_lines.append(f"Analysis completed in {execution_time:.2f}seconds")

        return "\n".join(report_lines)

    def generate_json_report(self) -> str:
        """Generate machine-readable JSON report"""
        import json

        execution_time = (datetime.now() - self.start_time).total_seconds()

        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "execution_time_seconds": execution_time,
                "report_type": "dry_run_analysis",
            },
            "contract_discovery": {
                "total_contracts": len(self.contracts),
                "contracts": self.contracts,
                "categories": list(set(c["category"] for c in self.contracts)),
            },
            "current_data_status": self.current_data_status,
            "update_plan": self.update_plan,
            "operations_sequence": [
                {**op, "timestamp": op["timestamp"].isoformat()}
                for op in self.operations_sequence
            ],
            "service_mappings": self.service_mappings,
            "validation_results": self.validation_results,
            "errors": self.errors,
            "warnings": self.warnings,
        }

        return json.dumps(report_data, indent=2, default=str)


class DataPipelineManager:
    """
    Contract-driven data pipeline orchestrator

    Architecture:
    1. Contract Discovery: Scans frontend/public/data/ to discover requirements
    2. Service Mapping: Maps discovered contracts to CLI services
    3. Data Generation: Orchestrates CLI services to fulfill contracts
    4. Schema Validation: Ensures generated data matches frontend contracts

    Data Flow:
    Frontend Contracts → Contract Discovery → CLI Services → Schema Validation → Frontend Data
    """

    def __init__(
        self, frontend_data_path: Optional[Path] = None, quiet_mode: bool = False
    ):
        """Initialize contract-driven data pipeline manager"""
        setup_logging("INFO", quiet_mode=quiet_mode)
        self.logger = logging.getLogger("data_pipeline_manager")
        self.scripts_dir = Path(__file__).parent
        self.project_root = self.scripts_dir.parent

        # Initialize contract discovery system
        if frontend_data_path is None:
            self.frontend_data_dir = self.project_root / "frontend/public/data"
        else:
            self.frontend_data_dir = Path(frontend_data_path)

        self.contract_discovery = DataContractDiscovery(self.frontend_data_dir)
        self.cli_outputs_dir = self.project_root / "data/outputs"

        # Initialize CLI service manager
        config = ScriptConfig(
            base_path=self.project_root,
            data_outputs_path=self.cli_outputs_dir,
            templates_path=self.scripts_dir / "templates",
            twitter_outputs_path=self.cli_outputs_dir / "twitter",
            twitter_templates_path=self.scripts_dir / "templates/twitter",
        )
        self.cli_service = CLIServiceScript(config)

        # Discover contracts from frontend requirements
        self.discovery_result: Optional[ContractDiscoveryResult] = None
        self.contracts: List[DataContract] = []

        # CLI service capability mapping (what each service can provide)
        self.cli_service_capabilities = self._initialize_cli_capabilities()

        self.logger.info(
            f"Initialized contract-driven pipeline for {self.frontend_data_dir}"
        )

    def _get_source_data_path(self, portfolio_name: str) -> Path:
        """Get the source data file path for a portfolio"""
        return (
            self.project_root
            / "data"
            / "raw"
            / "trade_history"
            / f"{portfolio_name}.csv"
        )

    def _get_source_data_modification_time(
        self, portfolio_name: str
    ) -> Optional[datetime]:
        """Get the modification time of source data file for a portfolio"""
        source_path = self._get_source_data_path(portfolio_name)
        if source_path.exists():
            return datetime.fromtimestamp(source_path.stat().st_mtime)
        return None

    def _check_open_positions_exist(self, portfolio_name: str) -> bool:
        """Check if any open positions exist in the source data"""
        source_path = self._get_source_data_path(portfolio_name)
        if not source_path.exists():
            return False

        try:
            df = pd.read_csv(source_path)
            if "Status" in df.columns:
                open_positions = df[df["Status"] == "Open"]
                return len(open_positions) > 0
            return False
        except Exception as e:
            self.logger.warning(f"Error checking open positions in {source_path}: {e}")
            return False

    def _extract_portfolio_name_from_contract(
        self, contract: DataContract
    ) -> Optional[str]:
        """Extract portfolio name from contract ID or file path"""
        # Pattern: look for portfolio name in contract_id or file path
        # Examples: "trade-history_live_signals", "portfolio_live-signals_live_signals_equity"

        # Try to extract from contract_id
        if (
            "live_signals" in contract.contract_id
            or "live-signals" in contract.contract_id
        ):
            return "live_signals"

        # Try to extract from file path
        file_path_str = str(contract.file_path)
        if "live_signals" in file_path_str or "live-signals" in file_path_str:
            return "live_signals"

        # Could add more portfolio patterns here as needed
        return None

    def _initialize_cli_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Initialize CLI service capability mapping"""
        return {
            "yahoo_finance": {
                "provides": ["stock_data", "market_data", "portfolio_data"],
                "categories": ["portfolio"],
                "data_types": ["time_series", "financial"],
                "refresh_frequency": "daily",
            },
            "alpha_vantage": {
                "provides": ["stock_data", "technical_indicators", "market_data"],
                "categories": ["portfolio"],
                "data_types": ["time_series", "financial"],
                "refresh_frequency": "daily",
            },
            "live_signals_dashboard": {
                "provides": ["live_signals", "equity_curves", "trading_metrics"],
                "categories": ["portfolio", "live-signals"],
                "data_types": ["time_series", "trading"],
                "refresh_frequency": "hourly",
            },
            "trade_history": {
                "provides": ["trade_records", "position_data", "pnl_analysis"],
                "categories": ["trade-history", "open-positions"],
                "data_types": ["transactional", "trading"],
                "refresh_frequency": "hourly",
            },
        }

    def discover_contracts(self) -> ContractDiscoveryResult:
        """Discover all frontend data contracts"""
        if self.discovery_result is None:
            self.logger.info("Discovering data contracts from frontend requirements")
            self.discovery_result = self.contract_discovery.discover_all_contracts()
            self.contracts = self.discovery_result.contracts

            self.logger.info(
                f"Discovered {len(self.contracts)} contracts across "
                f"{len(self.discovery_result.categories)} categories"
            )

        return self.discovery_result

    def get_contracts_by_category(self, category: str) -> List[DataContract]:
        """Get contracts for a specific category"""
        self.discover_contracts()
        return [c for c in self.contracts if c.category == category]

    def map_contract_to_services(self, contract: DataContract) -> List[str]:
        """Map a contract to capable CLI services"""
        capable_services = []

        for service_name, capabilities in self.cli_service_capabilities.items():
            # Check if service can provide data for this category
            if contract.category in capabilities["categories"]:
                capable_services.append(service_name)
                continue

            # Check specific data type compatibility
            for data_source in contract.data_sources:
                if data_source in capabilities["provides"]:
                    capable_services.append(service_name)
                    break

        return capable_services

    def validate_contract_fulfillment(self, contract: DataContract) -> ProcessingResult:
        """Validate that a contract can be fulfilled by available services"""
        capable_services = self.map_contract_to_services(contract)

        if not capable_services:
            return ProcessingResult(
                success=False,
                operation=f"validate_contract_{contract.contract_id}",
                error=f"No CLI services available to fulfill contract {contract.contract_id}",
            )

        # Check if contract file exists and meets freshness requirements
        if not contract.file_path.exists():
            return ProcessingResult(
                success=False,
                operation=f"validate_contract_{contract.contract_id}",
                error=f"Contract file does not exist: {contract.file_path}",
            )

        # Check freshness
        file_age_hours = (
            datetime.now() - contract.last_modified
        ).total_seconds() / 3600
        if file_age_hours > contract.freshness_threshold_hours:
            return ProcessingResult(
                success=False,
                operation=f"validate_contract_{contract.contract_id}",
                error=f"Contract data is stale ({file_age_hours:.1f}h > {contract.freshness_threshold_hours}h threshold)",
            )

        result = ProcessingResult(
            success=True, operation=f"validate_contract_{contract.contract_id}"
        )
        result.add_metadata("capable_services", capable_services)
        result.add_metadata("file_age_hours", file_age_hours)
        result.add_metadata("freshness_threshold", contract.freshness_threshold_hours)

        return result

    def validate_service_dependencies(self) -> ProcessingResult:
        """
        Comprehensive validation of service dependencies and data contracts.

        Validates:
        1. Service availability (services exist and are executable)
        2. Service health (services can execute basic operations)
        3. Service dependency chains (all required services are available)
        4. Data contract schema compliance (deep validation)

        Returns:
            ProcessingResult with detailed validation status
        """
        start_time = datetime.now()
        validation_results = []
        failed_services = []

        try:
            self.logger.info("Starting comprehensive service dependency validation")

            # Step 1: Validate service availability
            self.logger.info("Validating service availability...")
            service_availability = self._validate_service_availability()

            if not service_availability["success"]:
                failed_services.extend(service_availability.get("failed_services", []))
                validation_results.append(
                    f"Service availability check failed: {service_availability['error']}"
                )

            # Step 2: Validate service health
            self.logger.info("Validating service health...")
            service_health = self._validate_service_health()

            if not service_health["success"]:
                failed_services.extend(service_health.get("failed_services", []))
                validation_results.append(
                    f"Service health check failed: {service_health['error']}"
                )

            # Step 3: Discover contracts and validate dependency chains
            self.logger.info(
                "Discovering contracts and validating dependency chains..."
            )
            discovery_result = self.discover_contracts()

            for contract in discovery_result.contracts:
                capable_services = self.map_contract_to_services(contract)
                if not capable_services:
                    validation_results.append(
                        f"No services available for contract {contract.contract_id}"
                    )
                    continue

                # Check if any capable service is actually available and healthy
                available_capable_services = [
                    svc for svc in capable_services if svc not in failed_services
                ]

                if not available_capable_services:
                    validation_results.append(
                        f"Contract {contract.contract_id} requires services {capable_services} "
                        f"but none are available/healthy"
                    )

            # Step 4: Validate existing data contracts schema compliance
            self.logger.info("Validating data contract schema compliance...")
            schema_validation = self._validate_contract_schemas(
                discovery_result.contracts
            )

            if not schema_validation["success"]:
                validation_results.extend(schema_validation.get("schema_errors", []))

            # Generate final result
            success = len(validation_results) == 0
            duration = datetime.now() - start_time

            result = ProcessingResult(
                success=success,
                operation="validate_service_dependencies",
                error="; ".join(validation_results) if validation_results else None,
            )

            result.add_metadata("duration_seconds", duration.total_seconds())
            result.add_metadata("failed_services", failed_services)
            result.add_metadata("validation_results", validation_results)
            result.add_metadata("contracts_checked", len(discovery_result.contracts))
            result.add_metadata("services_checked", len(self.cli_service_capabilities))

            if success:
                self.logger.info(
                    f"Service dependency validation passed in {duration.total_seconds():.2f}s"
                )
            else:
                self.logger.error(
                    f"Service dependency validation failed: {len(validation_results)} issues found"
                )
                for issue in validation_results:
                    self.logger.error(f"  - {issue}")

            return result

        except Exception as e:
            duration = datetime.now() - start_time
            self.logger.error(
                f"Service dependency validation failed with exception: {e}"
            )

            return ProcessingResult(
                success=False,
                operation="validate_service_dependencies",
                error=f"Validation failed with exception: {e}",
                metadata={
                    "duration_seconds": duration.total_seconds(),
                    "failed_services": failed_services,
                    "validation_results": validation_results,
                },
            )

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
                        "error": None
                        if is_available
                        else f"Dashboard script not found: {dashboard_script}",
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
                        "error": None
                        if is_available
                        else f"Service {service_name} not available",
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
                        import importlib.util

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

    def _validate_contract_schemas(
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

                # Enhanced CSV validation
                df = pd.read_csv(contract.file_path)

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

    def refresh_all_chart_data(self, skip_errors: bool = False) -> ProcessingResult:
        """
        Contract-driven data refresh: discovers frontend requirements and fulfills them

        Args:
            skip_errors: If True, continue processing despite individual failures

        Returns:
            ProcessingResult with success status and contract fulfillment details
        """
        start_time = datetime.now()

        try:
            self.logger.info("Starting contract-driven data refresh")

            # Step 1: Discover all frontend data contracts
            discovery_result = self.discover_contracts()

            if not discovery_result.contracts:
                raise ValidationError(
                    "No data contracts discovered from frontend requirements"
                )

            self.logger.info(
                f"Processing {len(discovery_result.contracts)} discovered contracts"
            )

            # Step 2: Comprehensive service dependency validation
            self.logger.info(
                "Performing comprehensive service dependency validation..."
            )
            dependency_validation = self.validate_service_dependencies()

            if not dependency_validation.success:
                if not skip_errors:
                    raise ValidationError(
                        f"Service dependency validation failed: {dependency_validation.error}"
                    )
                else:
                    self.logger.warning(
                        f"Service dependency validation failed but continuing due to skip_errors: {dependency_validation.error}"
                    )

            # Step 3: Validate contract fulfillment capabilities
            unfulfillable_contracts = []

            for contract in discovery_result.contracts:
                capable_services = self.map_contract_to_services(contract)
                if not capable_services:
                    unfulfillable_contracts.append(contract.contract_id)
                    self.logger.warning(
                        f"No services available to fulfill contract: {contract.contract_id}"
                    )
                    if not skip_errors:
                        raise ConfigurationError(
                            f"Cannot fulfill contract {contract.contract_id}: no capable services"
                        )

            # Step 3: Refresh contracts by category
            results = {}
            failed_contracts = []
            successful_contracts = []

            # Group contracts by category for efficient processing
            contracts_by_category: Dict[str, List[DataContract]] = {}
            for contract in discovery_result.contracts:
                if contract.contract_id not in unfulfillable_contracts:
                    if contract.category not in contracts_by_category:
                        contracts_by_category[contract.category] = []
                    contracts_by_category[contract.category].append(contract)

            # Process each category
            for category, contracts in contracts_by_category.items():
                try:
                    self.logger.info(
                        f"Refreshing {category} category ({len(contracts)} contracts)"
                    )
                    category_result = self._refresh_contracts_for_category(
                        category, contracts
                    )
                    results[category] = category_result

                    if category_result.success:
                        successful_contracts.extend([c.contract_id for c in contracts])
                    else:
                        failed_contracts.extend([c.contract_id for c in contracts])
                        if not skip_errors:
                            raise Exception(
                                f"Failed to refresh {category}: {category_result.error}"
                            )

                except Exception as e:
                    self.logger.error(f"Error refreshing {category} contracts: {e}")
                    failed_contracts.extend([c.contract_id for c in contracts])
                    results[category] = ProcessingResult(
                        success=False,
                        operation=f"refresh_contracts_{category}",
                        error=str(e),
                    )

                    if not skip_errors:
                        raise

            # Step 4: Generate comprehensive result
            processing_time = (datetime.now() - start_time).total_seconds()
            total_contracts = len(discovery_result.contracts)
            successful_count = len(successful_contracts)
            failed_count = len(failed_contracts) + len(unfulfillable_contracts)

            # Determine overall success considering all validation aspects
            contracts_successful = failed_count == 0
            dependencies_valid = dependency_validation.success

            # Pipeline is only successful if ALL validations pass
            overall_success = contracts_successful and dependencies_valid

            # Build detailed error message if pipeline failed
            error_reasons = []
            if not dependencies_valid:
                error_reasons.append(
                    f"Service dependencies failed: {dependency_validation.error}"
                )
            if not contracts_successful:
                if failed_contracts:
                    error_reasons.append(
                        f"Contract processing failed: {failed_contracts}"
                    )
                if unfulfillable_contracts:
                    error_reasons.append(
                        f"Contracts unfulfillable: {unfulfillable_contracts}"
                    )

            result = ProcessingResult(
                success=overall_success,
                operation="refresh_all_chart_data",
                processing_time=processing_time,
                error="; ".join(error_reasons) if error_reasons else None,
            )

            # Add comprehensive metadata
            result.add_metadata("total_contracts", total_contracts)
            result.add_metadata("successful_contracts", successful_count)
            result.add_metadata("failed_contracts", failed_count)
            result.add_metadata("unfulfillable_contracts", len(unfulfillable_contracts))
            result.add_metadata(
                "categories_processed", list(contracts_by_category.keys())
            )
            result.add_metadata(
                "contract_results",
                {
                    "successful": successful_contracts,
                    "failed": failed_contracts,
                    "unfulfillable": unfulfillable_contracts,
                },
            )
            result.add_metadata(
                "discovery_stats",
                {
                    "total_discovered": len(discovery_result.contracts),
                    "categories_found": len(discovery_result.categories),
                    "discovery_time": discovery_result.discovery_time,
                },
            )

            # Add service dependency validation metadata
            result.add_metadata(
                "service_dependency_validation",
                {
                    "success": dependency_validation.success,
                    "error": dependency_validation.error,
                    "failed_services": dependency_validation.metadata.get(
                        "failed_services", []
                    ),
                    "validation_results": dependency_validation.metadata.get(
                        "validation_results", []
                    ),
                },
            )

            # Log final pipeline status
            if overall_success:
                self.logger.info(
                    f"Contract-driven refresh SUCCESSFUL: {successful_count}/{total_contracts} "
                    f"contracts successful, all services healthy in {processing_time:.2f}s"
                )
            else:
                self.logger.error(
                    f"Contract-driven refresh FAILED: {successful_count}/{total_contracts} "
                    f"contracts successful in {processing_time:.2f}s. Errors: {result.error}"
                )

            return result

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()

            error_result = ProcessingResult(
                success=False,
                operation="refresh_all_chart_data",
                error=str(e),
                processing_time=processing_time,
            )

            self.logger.error(f"Contract-driven data refresh failed: {e}")
            return error_result

    def _refresh_contracts_for_category(
        self, category: str, contracts: List[DataContract]
    ) -> ProcessingResult:
        """Refresh data for contracts in a specific category"""
        start_time = datetime.now()

        try:
            self.logger.info(
                f"Processing {len(contracts)} contracts for category: {category}"
            )

            # Step 1: Identify required CLI services for this category
            required_services = set()
            for contract in contracts:
                capable_services = self.map_contract_to_services(contract)
                required_services.update(capable_services)

            self.logger.info(
                f"Required services for {category}: {list(required_services)}"
            )

            # Step 2: Execute CLI services to fetch/generate data
            for service_name in required_services:
                try:
                    service_result = self._execute_cli_service_for_category(
                        service_name, category
                    )
                    if not service_result.success:
                        self.logger.warning(
                            f"Service {service_name} failed: {service_result.error}"
                        )
                        # Continue with other services - some contracts might still be fulfillable
                except Exception as e:
                    self.logger.error(f"Error executing service {service_name}: {e}")
                    # Continue with other services

            # Step 3: Transform/validate data for each contract
            successful_contracts = []
            failed_contracts = []

            for contract in contracts:
                try:
                    contract_result = self._fulfill_contract(contract)
                    if contract_result.success:
                        successful_contracts.append(contract.contract_id)
                    else:
                        failed_contracts.append(contract.contract_id)
                        self.logger.warning(
                            f"Failed to fulfill contract {contract.contract_id}: {contract_result.error}"
                        )
                except Exception as e:
                    failed_contracts.append(contract.contract_id)
                    self.logger.error(
                        f"Error fulfilling contract {contract.contract_id}: {e}"
                    )

            processing_time = (datetime.now() - start_time).total_seconds()

            # Step 4: Generate result
            overall_success = len(failed_contracts) == 0

            result = ProcessingResult(
                success=overall_success,
                operation=f"refresh_contracts_{category}",
                processing_time=processing_time,
            )

            result.add_metadata("category", category)
            result.add_metadata("total_contracts", len(contracts))
            result.add_metadata("successful_contracts", len(successful_contracts))
            result.add_metadata("failed_contracts", len(failed_contracts))
            result.add_metadata("required_services", list(required_services))
            result.add_metadata(
                "contract_details",
                {"successful": successful_contracts, "failed": failed_contracts},
            )

            if failed_contracts:
                result.error = f"Failed contracts: {failed_contracts}"

            return result

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()

            return ProcessingResult(
                success=False,
                operation=f"refresh_contracts_{category}",
                error=str(e),
                processing_time=processing_time,
            )

    def _execute_cli_service_for_category(
        self, service_name: str, category: str
    ) -> ProcessingResult:
        """Execute a CLI service to generate data for a category"""

        # Map service names to execution methods
        if service_name == "live_signals_dashboard":
            return self._fetch_live_signals_data()
        elif service_name == "trade_history":
            return self._fetch_trade_history_data()
        elif service_name == "yahoo_finance":
            return self._fetch_yahoo_finance_data()
        elif service_name == "alpha_vantage":
            return self._fetch_alpha_vantage_data()
        else:
            return ProcessingResult(
                success=False,
                operation=f"execute_{service_name}",
                error=f"Unknown CLI service: {service_name}",
            )

    def _fulfill_contract(self, contract: DataContract) -> ProcessingResult:
        """Fulfill a specific data contract by ensuring data meets schema requirements"""

        try:
            # Check if contract file exists and has recent data
            if not contract.file_path.exists():
                # Generate data for this contract
                return self._generate_contract_data(contract)

            # Validate existing data meets contract requirements
            validation_result = self._validate_contract_data(contract)
            if not validation_result.success:
                # Data doesn't meet requirements, regenerate
                return self._generate_contract_data(contract)

            return ProcessingResult(
                success=True, operation=f"fulfill_contract_{contract.contract_id}"
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"fulfill_contract_{contract.contract_id}",
                error=str(e),
            )

    def _generate_contract_data(self, contract: DataContract) -> ProcessingResult:
        """Generate data to fulfill a contract"""

        try:
            # Ensure output directory exists
            contract.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate data based on contract category and schema
            if contract.category == "portfolio":
                return self._generate_portfolio_contract_data(contract)
            elif contract.category == "trade-history":
                return self._generate_trade_history_contract_data(contract)
            elif contract.category == "open-positions":
                return self._generate_open_positions_contract_data(contract)
            else:
                # Use the contract schema to generate synthetic data
                return self._generate_generic_contract_data(contract)

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"generate_contract_data_{contract.contract_id}",
                error=str(e),
            )

    def _validate_contract_data(self, contract: DataContract) -> ProcessingResult:
        """Validate that existing data meets contract requirements"""

        try:
            # Check file freshness
            file_age_hours = (
                datetime.now() - contract.last_modified
            ).total_seconds() / 3600
            if file_age_hours > contract.freshness_threshold_hours:
                return ProcessingResult(
                    success=False,
                    operation=f"validate_contract_{contract.contract_id}",
                    error=f"Data is stale: {file_age_hours:.1f}h > {contract.freshness_threshold_hours}h",
                )

            # Read and validate CSV structure
            try:
                df = pd.read_csv(contract.file_path)

                # Check minimum row count
                if len(df) < contract.minimum_rows:
                    return ProcessingResult(
                        success=False,
                        operation=f"validate_contract_{contract.contract_id}",
                        error=f"Insufficient data: {len(df)} rows < {contract.minimum_rows} required",
                    )

                # Check required columns exist
                missing_columns = contract.required_columns - set(df.columns)
                if missing_columns:
                    return ProcessingResult(
                        success=False,
                        operation=f"validate_contract_{contract.contract_id}",
                        error=f"Missing required columns: {missing_columns}",
                    )

                return ProcessingResult(
                    success=True, operation=f"validate_contract_{contract.contract_id}"
                )

            except Exception as e:
                return ProcessingResult(
                    success=False,
                    operation=f"validate_contract_{contract.contract_id}",
                    error=f"Failed to read/validate CSV: {e}",
                )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"validate_contract_{contract.contract_id}",
                error=str(e),
            )

    def _generate_portfolio_contract_data(
        self, contract: DataContract
    ) -> ProcessingResult:
        """Generate portfolio data that matches the contract schema"""
        try:
            # Determine the type of portfolio data from contract schema
            column_names = [col.name for col in contract.schema]

            if "Portfolio_Value" in column_names:
                df = self._generate_portfolio_value_data()
            elif "Returns" in column_names or "Returns_Pct" in column_names:
                df = self._generate_portfolio_returns_data()
            elif "Drawdown" in column_names or "Drawdown_Pct" in column_names:
                df = self._generate_portfolio_drawdowns_data()
            elif "Cumulative_Returns" in column_names:
                df = self._generate_portfolio_cumulative_returns_data()
            elif "equity" in column_names and "timestamp" in column_names:
                # This is live signals equity data
                df = self._generate_live_signals_equity_data()
            else:
                # Generate generic portfolio data
                df = self._generate_portfolio_value_data()

            # Ensure only required columns are present
            if not df.empty:
                available_columns = [col for col in column_names if col in df.columns]
                df = df[available_columns]

            # Save to contract file path
            df.to_csv(contract.file_path, index=False)

            return ProcessingResult(
                success=True,
                operation=f"generate_portfolio_data_{contract.contract_id}",
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"generate_portfolio_data_{contract.contract_id}",
                error=str(e),
            )

    def _generate_trade_history_contract_data(
        self, contract: DataContract
    ) -> ProcessingResult:
        """Generate trade history data that matches the contract schema"""
        try:
            df = self._generate_trade_history_data()

            # Ensure only required columns are present
            column_names = [col.name for col in contract.schema]
            if not df.empty:
                available_columns = [col for col in column_names if col in df.columns]
                df = df[available_columns]

            # Save to contract file path
            df.to_csv(contract.file_path, index=False)

            return ProcessingResult(
                success=True,
                operation=f"generate_trade_history_data_{contract.contract_id}",
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"generate_trade_history_data_{contract.contract_id}",
                error=str(e),
            )

    def _generate_open_positions_contract_data(
        self, contract: DataContract
    ) -> ProcessingResult:
        """Generate open positions data that matches the contract schema"""
        try:
            df = self._generate_open_positions_data()

            # Ensure only required columns are present
            column_names = [col.name for col in contract.schema]
            if not df.empty:
                available_columns = [col for col in column_names if col in df.columns]
                df = df[available_columns]

            # Save to contract file path
            df.to_csv(contract.file_path, index=False)

            return ProcessingResult(
                success=True,
                operation=f"generate_open_positions_data_{contract.contract_id}",
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"generate_open_positions_data_{contract.contract_id}",
                error=str(e),
            )

    def _generate_generic_contract_data(
        self, contract: DataContract
    ) -> ProcessingResult:
        """Generate generic data based on contract schema"""
        try:
            # Create synthetic data based on schema
            data: Dict[str, Any] = {}
            num_rows = contract.minimum_rows

            for column_schema in contract.schema:
                if column_schema.data_type == "datetime":
                    # Generate date range
                    dates = pd.date_range(
                        start=datetime.now() - timedelta(days=num_rows),
                        periods=num_rows,
                        freq="D",
                    )
                    data[column_schema.name] = dates.strftime("%Y-%m-%d")

                elif column_schema.data_type == "numeric":
                    # Generate random numeric data
                    if column_schema.format_pattern == "integer":
                        data[column_schema.name] = np.random.randint(1, 1000, num_rows)
                    else:
                        data[column_schema.name] = np.round(
                            np.random.normal(100, 20, num_rows), 2
                        )

                elif column_schema.data_type == "string":
                    # Generate string data from sample values or random
                    if column_schema.sample_values:
                        choices = column_schema.sample_values * (
                            num_rows // len(column_schema.sample_values) + 1
                        )
                        data[column_schema.name] = choices[:num_rows]
                    else:
                        data[column_schema.name] = [
                            f"Value_{i}" for i in range(num_rows)
                        ]

                else:
                    # Default to string
                    data[column_schema.name] = [f"Data_{i}" for i in range(num_rows)]

            df = pd.DataFrame(data)

            # Save to contract file path
            df.to_csv(contract.file_path, index=False)

            return ProcessingResult(
                success=True, operation=f"generate_generic_data_{contract.contract_id}"
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"generate_generic_data_{contract.contract_id}",
                error=str(e),
            )

    def _generate_portfolio_cumulative_returns_data(self) -> pd.DataFrame:
        """Generate portfolio cumulative returns time series data"""
        dates = pd.date_range(start="2014-01-01", end=datetime.now(), freq="D")

        # Generate cumulative returns
        daily_returns = np.random.normal(0.001, 0.02, len(dates))
        cumulative_returns = np.cumprod(1 + daily_returns) - 1

        return pd.DataFrame(
            {
                "Date": dates.strftime("%Y-%m-%d"),
                "Cumulative_Returns": cumulative_returns,
                "Cumulative_Returns_Pct": cumulative_returns * 100,
            }
        )

    def _refresh_category_data(
        self, category: str, config: Dict[str, Any]
    ) -> ProcessingResult:
        """Refresh data for a specific category"""
        start_time = datetime.now()

        try:
            # Step 1: Fetch raw data using CLI services
            for source in config["sources"]:
                self.logger.info(f"Fetching data from {source}")
                result = self._fetch_from_source(source)
                if not result.success:
                    raise Exception(f"Failed to fetch from {source}: {result.error}")

            # Step 2: Process data using processing scripts
            for script in config["processing_scripts"]:
                self.logger.info(f"Processing data with {script}")
                result = self._run_processing_script(script)
                if not result.success:
                    self.logger.warning(
                        f"Processing script {script} failed: {result.error}"
                    )
                    # Continue with available data

            # Step 3: Transform to CSV format for frontend
            transformed_files = []
            for output_file in config["output_files"]:
                csv_result = self._transform_to_csv(category, output_file)
                if csv_result.success:
                    transformed_files.append(output_file)
                else:
                    self.logger.warning(
                        f"Failed to transform {output_file}: {csv_result.error}"
                    )

            processing_time = (datetime.now() - start_time).total_seconds()

            result = ProcessingResult(
                success=len(transformed_files) > 0,
                operation=f"refresh_{category}",
                processing_time=processing_time,
            )

            result.add_metadata("category", category)
            result.add_metadata("transformed_files", transformed_files)
            result.add_metadata("total_files", len(config["output_files"]))

            if len(transformed_files) == 0:
                result.error = f"No files successfully transformed for {category}"

            return result

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()

            return ProcessingResult(
                success=False,
                operation=f"refresh_{category}",
                error=str(e),
                processing_time=processing_time,
            )

    def _fetch_from_source(self, source: str) -> ProcessingResult:
        """Fetch data from a specific CLI source"""
        if source == "yahoo_finance":
            return self._fetch_yahoo_finance_data()
        elif source == "alpha_vantage":
            return self._fetch_alpha_vantage_data()
        elif source == "live_signals_dashboard":
            return self._fetch_live_signals_data()
        elif source == "trade_history":
            return self._fetch_trade_history_data()
        else:
            return ProcessingResult(
                success=False,
                operation=f"fetch_{source}",
                error=f"Unknown data source: {source}",
            )

    def _fetch_yahoo_finance_data(self) -> ProcessingResult:
        """Fetch portfolio data from Yahoo Finance"""
        try:
            # Use existing Yahoo Finance CLI with valid command: batch
            # This fetches data for portfolio symbols
            result = self.cli_service.execute(
                service_name="yahoo_finance",
                command="batch",
                args=["BTC-USD,SPY,QQQ"],
                timeout=180,
            )
            return result
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_yahoo_finance", error=str(e)
            )

    def _fetch_alpha_vantage_data(self) -> ProcessingResult:
        """Fetch supplementary data from Alpha Vantage"""
        try:
            # Use existing Alpha Vantage CLI with valid command: analyze
            result = self.cli_service.execute(
                service_name="alpha_vantage",
                command="analyze",
                args=["SPY"],
                timeout=60,
            )
            return result
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_alpha_vantage", error=str(e)
            )

    def _fetch_live_signals_data(self) -> ProcessingResult:
        """Generate fresh live signals data"""
        try:
            # Run the live signals dashboard to generate latest data
            import subprocess

            result = subprocess.run(
                [sys.executable, str(self.scripts_dir / "live_signals_dashboard.py")],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                return ProcessingResult(success=True, operation="fetch_live_signals")
            else:
                return ProcessingResult(
                    success=False,
                    operation="fetch_live_signals",
                    error=f"Live signals script failed: {result.stderr}",
                )
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_live_signals", error=str(e)
            )

    def _fetch_trade_history_data(self) -> ProcessingResult:
        """Fetch fresh trade history data"""
        try:
            today = datetime.now().strftime("%Y%m%d")

            result = self.cli_service.execute(
                service_name="trade_history",
                command="generate",
                args=[today],
                timeout=180,
            )
            # Generate chart-ready data files regardless of image generation success
            # Chart data only needs the CSV data, not the theme-dependent images
            chart_result = self._generate_chart_ready_data()
            if not chart_result.success:
                self.logger.warning(
                    f"Chart data generation failed: {chart_result.error}"
                )
            else:
                self.logger.info("Chart data generation completed successfully")

            return result
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_trade_history", error=str(e)
            )

    def _generate_chart_ready_data(self) -> ProcessingResult:
        """Generate pre-calculated chart data files for frontend consumption"""
        try:
            self.logger.info("Generating chart-ready data files")

            # Read the main trade history data from raw data source
            raw_trade_history_file = (
                self.project_root
                / "data"
                / "raw"
                / "trade_history"
                / "live_signals.csv"
            )
            frontend_trade_history_file = (
                self.frontend_data_dir / "trade-history" / "live_signals.csv"
            )

            # Prefer raw data source, fallback to frontend if needed
            if raw_trade_history_file.exists():
                trade_history_file = raw_trade_history_file
                self.logger.info(f"Using raw data source: {raw_trade_history_file}")
            elif frontend_trade_history_file.exists():
                trade_history_file = frontend_trade_history_file
                self.logger.warning(
                    f"Raw data not found, using frontend data: {frontend_trade_history_file}"
                )
            else:
                return ProcessingResult(
                    success=False,
                    operation="generate_chart_data",
                    error=f"Trade history file not found in either raw ({raw_trade_history_file}) or frontend ({frontend_trade_history_file}) locations",
                )

            # Load trade history data
            df = pd.read_csv(trade_history_file)

            # Generate trade PnL waterfall data (sorted by PnL magnitude)
            waterfall_result = self._generate_waterfall_data(df)

            # Generate closed positions PnL progression data
            closed_positions_result = self._generate_closed_positions_data(df)

            # Generate open positions PnL data
            open_positions_result = self._generate_chart_open_positions_data(df)

            # Check if all generations were successful
            if all(
                [
                    waterfall_result.success,
                    closed_positions_result.success,
                    open_positions_result.success,
                ]
            ):
                self.logger.info("Successfully generated all chart-ready data files")
                return ProcessingResult(success=True, operation="generate_chart_data")
            else:
                errors: list[str] = []
                if not waterfall_result.success:
                    errors.append(f"Waterfall: {waterfall_result.error}")
                if not closed_positions_result.success:
                    errors.append(f"Closed positions: {closed_positions_result.error}")
                if not open_positions_result.success:
                    errors.append(f"Open positions: {open_positions_result.error}")

                return ProcessingResult(
                    success=False,
                    operation="generate_chart_data",
                    error="; ".join(errors),
                )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation="generate_chart_data",
                error=f"Chart data generation failed: {str(e)}",
            )

    def _generate_waterfall_data(self, df: pd.DataFrame) -> ProcessingResult:
        """Generate trade PnL waterfall data sorted by PnL magnitude with unique ticker numbering"""
        try:
            # Filter for closed trades only
            closed_trades = df[df["Status"] == "Closed"].copy()

            if closed_trades.empty:
                return ProcessingResult(
                    success=False,
                    operation="generate_waterfall_data",
                    error="No closed trades found",
                )

            # Convert Exit_Timestamp to datetime for proper sorting
            closed_trades["Exit_Timestamp_dt"] = pd.to_datetime(
                closed_trades["Exit_Timestamp"]
            )

            # Handle ticker uniqueness: number duplicate tickers by Exit_Timestamp order
            unique_tickers = []

            # Group by ticker and sort each group by Exit_Timestamp (oldest first)
            for ticker in closed_trades["Ticker"].unique():
                ticker_trades = closed_trades[closed_trades["Ticker"] == ticker].copy()
                ticker_trades = ticker_trades.sort_values(
                    "Exit_Timestamp_dt", ascending=True
                )

                if len(ticker_trades) == 1:
                    # Single trade - keep original ticker name
                    unique_tickers.extend(ticker_trades.index.tolist())
                else:
                    # Multiple trades - number them by exit timestamp order
                    for i, idx in enumerate(ticker_trades.index.tolist()):
                        sequence_number = i + 1
                        numbered_ticker = f"{ticker}{sequence_number}"
                        closed_trades.loc[idx, "Ticker"] = numbered_ticker
                        unique_tickers.append(idx)

            # Sort by PnL magnitude (highest gains to highest losses)
            closed_trades["PnL_numeric"] = pd.to_numeric(
                closed_trades["PnL"], errors="coerce"
            )
            sorted_trades = closed_trades.sort_values("PnL_numeric", ascending=False)

            # Create waterfall data with required columns (excluding temporary columns)
            waterfall_data = sorted_trades[
                [
                    "Ticker",
                    "PnL",
                    "Entry_Timestamp",
                    "Exit_Timestamp",
                    "Avg_Entry_Price",
                    "Avg_Exit_Price",
                    "Position_Size",
                    "Direction",
                    "Duration_Days",
                    "Position_UUID",
                ]
            ].copy()

            # Add Status column for schema compatibility (all waterfall trades are closed)
            waterfall_data["Status"] = "Closed"

            # Reorder columns to match expected format
            waterfall_data = waterfall_data[
                [
                    "Ticker",
                    "PnL",
                    "Status",
                    "Entry_Timestamp",
                    "Exit_Timestamp",
                    "Avg_Entry_Price",
                    "Avg_Exit_Price",
                    "Position_Size",
                    "Direction",
                    "Duration_Days",
                    "Position_UUID",
                ]
            ]

            # Save to trade-history directory
            output_file = (
                self.frontend_data_dir
                / "trade-history"
                / "trade_pnl_waterfall_sorted.csv"
            )
            output_file.parent.mkdir(parents=True, exist_ok=True)
            waterfall_data.to_csv(output_file, index=False)

            # Count duplicates for logging
            ticker_duplicates = len(closed_trades) - len(
                closed_trades["Ticker"].str.extract(r"^([A-Z]+)", expand=False).unique()
            )

            self.logger.info(
                f"Generated waterfall data with {len(waterfall_data)} trades ({ticker_duplicates} tickers numbered for uniqueness)"
            )
            return ProcessingResult(success=True, operation="generate_waterfall_data")

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_waterfall_data", error=str(e)
            )

    def _load_historical_price_data(self, ticker: str) -> Dict[str, float]:
        """Load historical price data for a ticker from raw data stocks directory with enhanced validation"""
        price_data: dict[str, float] = {}

        try:
            # Try to load historical price data from raw stocks directory
            price_file = (
                self.project_root / "data" / "raw" / "stocks" / ticker / "daily.csv"
            )

            if not price_file.exists():
                self.logger.warning(
                    f"No historical price data found for {ticker} at {price_file}"
                )
                return price_data

            # Read CSV with error handling
            try:
                price_df = pd.read_csv(price_file)
            except pd.errors.EmptyDataError:
                self.logger.warning(f"Empty CSV file for {ticker}")
                return price_data
            except pd.errors.ParserError as e:
                self.logger.warning(f"Failed to parse CSV for {ticker}: {e}")
                return price_data

            # Validate required columns
            required_columns = ["date", "close"]
            missing_columns = [
                col for col in required_columns if col not in price_df.columns
            ]
            if missing_columns:
                self.logger.warning(
                    f"Missing required columns for {ticker}: {missing_columns}"
                )
                return price_data

            # Validate data quality and convert to dict
            valid_rows = 0
            invalid_rows = 0

            for _, row in price_df.iterrows():
                try:
                    # Validate and parse date
                    if pd.isna(row["date"]) or row["date"] == "":
                        invalid_rows += 1
                        continue

                    date_parsed = pd.to_datetime(row["date"], errors="coerce")
                    if pd.isna(date_parsed):
                        invalid_rows += 1
                        continue

                    date_str = date_parsed.strftime("%Y-%m-%d")

                    # Validate and parse price
                    if pd.isna(row["close"]) or row["close"] == "":
                        invalid_rows += 1
                        continue

                    close_price = float(row["close"])
                    if (
                        close_price <= 0 or close_price > 1000000
                    ):  # Sanity check for reasonable price range
                        invalid_rows += 1
                        continue

                    price_data[date_str] = close_price
                    valid_rows += 1

                except (ValueError, TypeError, OverflowError):
                    invalid_rows += 1
                    continue

            # Log data quality statistics
            total_rows = valid_rows + invalid_rows
            if total_rows > 0:
                quality_pct = (valid_rows / total_rows) * 100
                self.logger.debug(
                    f"Loaded {valid_rows} valid price points for {ticker} "
                    f"({quality_pct:.1f}% quality, {invalid_rows} invalid rows)"
                )

                # Warn if data quality is poor
                if quality_pct < 50:
                    self.logger.warning(
                        f"Poor data quality for {ticker}: {quality_pct:.1f}% valid rows"
                    )
                elif invalid_rows > 0:
                    self.logger.debug(
                        f"Filtered out {invalid_rows} invalid rows for {ticker}"
                    )
            else:
                self.logger.warning(f"No valid price data found for {ticker}")

        except Exception as e:
            self.logger.warning(
                f"Failed to load historical price data for {ticker}: {e}"
            )

        return price_data

    def _generate_closed_positions_data(self, df: pd.DataFrame) -> ProcessingResult:
        """Generate closed positions daily PnL progression time series data with enhanced validation"""
        try:
            # Validate input DataFrame
            if df.empty:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error="Empty input DataFrame",
                )

            # Validate required columns
            required_columns = [
                "Status",
                "Ticker",
                "Entry_Timestamp",
                "Exit_Timestamp",
                "Avg_Entry_Price",
                "Avg_Exit_Price",
                "Position_Size",
                "Direction",
                "PnL",
                "Position_UUID",
                "Duration_Days",
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error=f"Missing required columns: {missing_columns}",
                )

            closed_trades = df[df["Status"] == "Closed"].copy()

            if closed_trades.empty:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error="No closed trades found",
                )

            self.logger.info(
                f"Processing {len(closed_trades)} closed positions for time series generation"
            )

            # Generate daily time series data for each closed position
            time_series_data = []
            price_data_cache = {}  # Cache for loaded price data
            positions_with_real_data = 0
            positions_with_interpolated_data = 0

            for _, trade in closed_trades.iterrows():
                try:
                    # Validate individual trade data
                    ticker = trade["Ticker"]
                    if pd.isna(ticker) or ticker == "":
                        self.logger.warning(
                            f"Skipping trade with empty ticker: {trade.get('Position_UUID', 'unknown')}"
                        )
                        continue

                    # Validate and parse timestamps
                    try:
                        entry_timestamp = pd.to_datetime(
                            trade["Entry_Timestamp"], errors="coerce"
                        )
                        exit_timestamp = pd.to_datetime(
                            trade["Exit_Timestamp"], errors="coerce"
                        )

                        if pd.isna(entry_timestamp) or pd.isna(exit_timestamp):
                            self.logger.warning(
                                f"Skipping {ticker} trade with invalid timestamps: {trade.get('Position_UUID', 'unknown')}"
                            )
                            continue

                        entry_date = entry_timestamp.date()
                        exit_date = exit_timestamp.date()

                        # Validate date logic
                        if exit_date < entry_date:
                            self.logger.warning(
                                f"Skipping {ticker} trade with exit before entry: {trade.get('Position_UUID', 'unknown')}"
                            )
                            continue

                    except Exception as e:
                        self.logger.warning(
                            f"Skipping {ticker} trade due to timestamp parsing error: {e}"
                        )
                        continue

                    # Validate price data
                    try:
                        entry_price = float(trade["Avg_Entry_Price"])
                        exit_price = float(trade["Avg_Exit_Price"])
                        position_size = float(trade["Position_Size"])

                        if entry_price <= 0 or exit_price <= 0 or position_size <= 0:
                            self.logger.warning(
                                f"Skipping {ticker} trade with invalid prices/size: {trade.get('Position_UUID', 'unknown')}"
                            )
                            continue

                    except (ValueError, TypeError) as e:
                        self.logger.warning(
                            f"Skipping {ticker} trade due to price parsing error: {e}"
                        )
                        continue

                    # Load historical price data first to determine available trading dates
                    if ticker not in price_data_cache:
                        price_data_cache[ticker] = self._load_historical_price_data(
                            ticker
                        )

                    historical_prices = price_data_cache[ticker]

                    # Generate progression using only trading days (dates with actual price data)
                    if len(historical_prices) > 0:
                        # Use only dates that exist in historical price data within trade period
                        available_dates = []
                        for date_str, _ in historical_prices.items():
                            try:
                                price_date = pd.to_datetime(date_str).date()
                                if entry_date <= price_date <= exit_date:
                                    available_dates.append(pd.to_datetime(date_str))
                            except (ValueError, TypeError, AttributeError):
                                continue

                        if available_dates:
                            date_range = sorted(available_dates)
                        else:
                            # Fallback: single day with entry date if no trading days found
                            date_range = [pd.to_datetime(entry_date)]
                    else:
                        # Fallback: single day with entry date if no price data available
                        date_range = [pd.to_datetime(entry_date)]

                    use_real_data = len(historical_prices) > 0

                    if use_real_data:
                        positions_with_real_data += 1
                    else:
                        positions_with_interpolated_data += 1
                        self.logger.warning(
                            f"Using linear interpolation for {ticker} - no historical data available"
                        )

                    # Get trade parameters (already validated above)
                    direction = trade["Direction"]

                    # Get the actual market entry price for proper PnL calculation
                    entry_date_str = entry_date.strftime("%Y-%m-%d")
                    entry_market_price = entry_price  # Default to trade entry price
                    if use_real_data and entry_date_str in historical_prices:
                        entry_market_price = historical_prices[entry_date_str]
                        self.logger.debug(
                            f"Using actual market price for {ticker} entry: {entry_market_price} vs trade price: {entry_price}"
                        )

                    for i, date in enumerate(date_range):
                        date_str = date.strftime("%Y-%m-%d")

                        if use_real_data and date_str in historical_prices:
                            # Use real historical price data
                            current_market_price = historical_prices[date_str]

                            # Calculate actual PnL based on real price movement from entry market price
                            if direction == "Long":
                                current_pnl = (
                                    current_market_price - entry_market_price
                                ) * position_size
                            else:  # Short position
                                current_pnl = (
                                    entry_market_price - current_market_price
                                ) * position_size

                            current_price = current_market_price

                        else:
                            # Fallback to linear interpolation
                            if len(date_range) > 1:
                                progress_ratio = i / (len(date_range) - 1)
                            else:
                                progress_ratio = (
                                    1.0  # Single day trade gets final PnL immediately
                                )

                            current_pnl = float(trade["PnL"]) * progress_ratio
                            price_progress = (exit_price - entry_price) * progress_ratio
                            current_price = entry_price + price_progress

                        # Create daily data point matching ClosedPositionPnLDataRow schema
                        time_series_data.append(
                            {
                                "Date": date_str,
                                "Ticker": ticker,
                                "Price": f"{current_price:.4f}",
                                "PnL": f"{current_pnl:.2f}",
                                "Position_Size": str(trade["Position_Size"]),
                                "Entry_Date": entry_date.strftime("%Y-%m-%d"),
                                "Entry_Price": f"{entry_market_price:.4f}",  # Use actual market entry price
                                "Direction": direction,
                                "Position_UUID": trade["Position_UUID"],
                                "Duration_Days": str(trade["Duration_Days"]),
                            }
                        )

                except Exception as e:
                    self.logger.warning(
                        f"Failed to process trade {trade.get('Position_UUID', 'unknown')}: {e}"
                    )
                    continue

            if not time_series_data:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error="No valid time series data generated from closed trades",
                )

            # Convert to DataFrame and save
            closed_positions_df = pd.DataFrame(time_series_data)

            # Create portfolio subdirectory for closed positions data
            output_file = (
                self.frontend_data_dir
                / "portfolio"
                / "closed_positions_pnl_progression.csv"
            )
            output_file.parent.mkdir(parents=True, exist_ok=True)
            closed_positions_df.to_csv(output_file, index=False)

            # Log summary statistics
            unique_positions = closed_positions_df["Position_UUID"].nunique()
            total_data_points = len(closed_positions_df)
            avg_duration = closed_positions_df.groupby("Position_UUID").size().mean()

            self.logger.info(
                f"Generated closed positions time series data: {unique_positions} positions, "
                f"{total_data_points} data points, avg {avg_duration:.1f} days per position "
                f"({positions_with_real_data} positions with real price data, "
                f"{positions_with_interpolated_data} with linear interpolation)"
            )

            return ProcessingResult(
                success=True, operation="generate_closed_positions_data"
            )

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_closed_positions_data", error=str(e)
            )

    def _generate_chart_open_positions_data(self, df: pd.DataFrame) -> ProcessingResult:
        """Generate open positions PnL data"""
        try:
            # Filter for open positions only
            open_trades = df[df["Status"] != "Closed"].copy()

            # If no open positions, create empty file with correct structure
            if open_trades.empty:
                open_positions_data = pd.DataFrame(
                    columns=[
                        "Position_UUID",
                        "Ticker",
                        "Entry_Date",
                        "Entry_Price",
                        "Current_Price",
                        "PnL",
                        "Position_Size",
                        "Direction",
                        "Date",
                    ]
                )
            else:
                # Create open positions data structure
                open_positions_data = open_trades[
                    [
                        "Position_UUID",
                        "Ticker",
                        "Entry_Timestamp",
                        "Avg_Entry_Price",
                        "Current_Unrealized_PnL",
                        "Position_Size",
                        "Direction",
                    ]
                ].copy()

                # Rename columns to match frontend expectations
                open_positions_data = open_positions_data.rename(
                    columns={
                        "Entry_Timestamp": "Entry_Date",
                        "Avg_Entry_Price": "Entry_Price",
                        "Current_Unrealized_PnL": "PnL",
                    }
                )

                # Add current date and price columns (would need real-time data)
                open_positions_data["Date"] = datetime.now().strftime("%Y-%m-%d")
                open_positions_data["Current_Price"] = open_positions_data[
                    "Entry_Price"
                ]  # Placeholder

            # Save to portfolio directory
            output_file = (
                self.frontend_data_dir / "portfolio" / "open_positions_pnl_current.csv"
            )
            output_file.parent.mkdir(parents=True, exist_ok=True)
            open_positions_data.to_csv(output_file, index=False)

            self.logger.info(
                f"Generated open positions data with {len(open_positions_data)} positions"
            )
            return ProcessingResult(
                success=True, operation="generate_open_positions_data"
            )

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_open_positions_data", error=str(e)
            )

    def _run_processing_script(self, script: str) -> ProcessingResult:
        """Run a data processing script"""
        try:
            script_path = self.scripts_dir / f"{script}.py"
            if not script_path.exists():
                return ProcessingResult(
                    success=False,
                    operation=f"run_{script}",
                    error=f"Script not found: {script_path}",
                )

            import subprocess

            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                return ProcessingResult(success=True, operation=f"run_{script}")
            else:
                return ProcessingResult(
                    success=False,
                    operation=f"run_{script}",
                    error=f"Script failed: {result.stderr}",
                )
        except Exception as e:
            return ProcessingResult(
                success=False, operation=f"run_{script}", error=str(e)
            )

    def _transform_to_csv(self, category: str, output_file: str) -> ProcessingResult:
        """Transform processed data to frontend-compatible CSV format"""
        try:
            if category == "portfolio":
                return self._transform_portfolio_csv(output_file)
            elif category == "live_signals":
                return self._transform_live_signals_csv(output_file)
            elif category == "trade_history":
                return self._transform_trade_history_csv(output_file)
            elif category == "open_positions":
                return self._transform_open_positions_csv(output_file)
            else:
                return ProcessingResult(
                    success=False,
                    operation=f"transform_{category}_{output_file}",
                    error=f"Unknown category: {category}",
                )
        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"transform_{category}_{output_file}",
                error=str(e),
            )

    def _transform_portfolio_csv(self, output_file: str) -> ProcessingResult:
        """Transform portfolio data to CSV format"""
        try:
            # Generate synthetic portfolio data based on Bitcoin analysis outputs
            # This would typically read from CLI outputs and transform to CSV

            output_path = self.frontend_data_dir / "portfolio" / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate sample data structure matching existing CSV format
            if "portfolio_value" in output_file:
                df = self._generate_portfolio_value_data()
            elif "returns" in output_file:
                df = self._generate_portfolio_returns_data()
            elif "drawdowns" in output_file:
                df = self._generate_portfolio_drawdowns_data()
            else:
                return ProcessingResult(
                    success=False,
                    operation=f"transform_portfolio_{output_file}",
                    error=f"Unknown portfolio file type: {output_file}",
                )

            df.to_csv(output_path, index=False)

            return ProcessingResult(
                success=True, operation=f"transform_portfolio_{output_file}"
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"transform_portfolio_{output_file}",
                error=str(e),
            )

    def _transform_live_signals_csv(self, output_file: str) -> ProcessingResult:
        """Transform live signals data to CSV format"""
        try:
            output_path = (
                self.frontend_data_dir / "portfolio/live-signals" / output_file
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate live signals equity data
            df = self._generate_live_signals_equity_data()
            df.to_csv(output_path, index=False)

            return ProcessingResult(
                success=True, operation=f"transform_live_signals_{output_file}"
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"transform_live_signals_{output_file}",
                error=str(e),
            )

    def _transform_trade_history_csv(self, output_file: str) -> ProcessingResult:
        """Transform trade history data to CSV format"""
        try:
            output_path = self.frontend_data_dir / "trade-history" / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate trade history data
            df = self._generate_trade_history_data()
            df.to_csv(output_path, index=False)

            return ProcessingResult(
                success=True, operation=f"transform_trade_history_{output_file}"
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"transform_trade_history_{output_file}",
                error=str(e),
            )

    def _transform_open_positions_csv(self, output_file: str) -> ProcessingResult:
        """Transform open positions data to CSV format"""
        try:
            output_path = self.frontend_data_dir / "open-positions" / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate open positions PnL data
            df = self._generate_open_positions_data()
            df.to_csv(output_path, index=False)

            return ProcessingResult(
                success=True, operation=f"transform_open_positions_{output_file}"
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                operation=f"transform_open_positions_{output_file}",
                error=str(e),
            )

    def _generate_portfolio_value_data(self) -> pd.DataFrame:
        """Generate portfolio value time series data"""
        dates = pd.date_range(start="2014-01-01", end=datetime.now(), freq="D")

        # Generate synthetic portfolio growth data
        initial_value = 1000.0
        daily_returns = np.random.normal(
            0.001, 0.02, len(dates)
        )  # 0.1% daily return, 2% volatility
        portfolio_values = [initial_value]

        for ret in daily_returns[1:]:
            portfolio_values.append(portfolio_values[-1] * (1 + ret))

        return pd.DataFrame(
            {"Date": dates.strftime("%Y-%m-%d"), "Portfolio_Value": portfolio_values}
        )

    def _generate_portfolio_returns_data(self) -> pd.DataFrame:
        """Generate portfolio returns time series data"""
        dates = pd.date_range(start="2014-01-01", end=datetime.now(), freq="D")
        returns = (
            np.random.normal(0.001, 0.02, len(dates)) * 100
        )  # Convert to percentage

        return pd.DataFrame(
            {"Date": dates.strftime("%Y-%m-%d"), "Returns_Pct": returns}
        )

    def _generate_portfolio_drawdowns_data(self) -> pd.DataFrame:
        """Generate portfolio drawdown time series data"""
        dates = pd.date_range(start="2014-01-01", end=datetime.now(), freq="D")

        # Generate drawdown data (always negative or zero)
        base_drawdowns = np.random.exponential(scale=0.05, size=len(dates))
        drawdowns = -np.abs(base_drawdowns) * 100  # Convert to negative percentage

        return pd.DataFrame(
            {"Date": dates.strftime("%Y-%m-%d"), "Drawdown_Pct": drawdowns}
        )

    def _generate_live_signals_equity_data(self) -> pd.DataFrame:
        """Generate live signals equity time series data"""
        start_date = datetime(2025, 4, 1)
        end_date = datetime.now()
        dates = pd.date_range(start=start_date, end=end_date, freq="D")

        # Generate synthetic equity curve with realistic trading pattern
        equity_values = []
        drawdown_values = []
        peak_equity = 0.0
        current_equity = 0.0

        for i, date in enumerate(dates):
            # Add some realistic trading volatility
            daily_change = np.random.normal(
                0.5, 15.0
            )  # $0.50 average gain, $15 daily volatility
            current_equity += daily_change

            # Track peak and drawdown
            if current_equity > peak_equity:
                peak_equity = current_equity
                drawdown = 0.0
            else:
                drawdown = current_equity - peak_equity

            equity_values.append(current_equity)
            drawdown_values.append(drawdown)

        # Calculate additional metrics
        equity_changes = [0.0] + [
            equity_values[i] - equity_values[i - 1]
            for i in range(1, len(equity_values))
        ]

        return pd.DataFrame(
            {
                "timestamp": dates.strftime("%Y-%m-%d"),
                "equity": equity_values,
                "equity_pct": [0.0] * len(dates),  # Placeholder
                "equity_change": equity_changes,
                "equity_change_pct": [0.0] * len(dates),  # Placeholder
                "drawdown": [abs(d) for d in drawdown_values],
                "drawdown_pct": [0.0] * len(dates),  # Placeholder
                "peak_equity": [peak_equity] * len(dates),
                "mfe": equity_values,  # Simplified
                "mae": drawdown_values,
            }
        )

    def _generate_trade_history_data(self) -> pd.DataFrame:
        """Generate trade history data with realistic trading records"""
        tickers = [
            "AAPL",
            "GOOGL",
            "MSFT",
            "AMZN",
            "TSLA",
            "NVDA",
            "CRWD",
            "NFLX",
            "COST",
        ]
        strategies = ["SMA", "EMA"]

        trades = []
        for i in range(15):  # Generate 15 sample trades
            ticker = np.random.choice(tickers)
            strategy = np.random.choice(strategies)

            # Generate realistic trade data
            entry_date = datetime.now() - timedelta(days=np.random.randint(1, 180))
            pnl = np.random.normal(50, 200)  # $50 average, $200 volatility

            trade = {
                "Position_UUID": f"{ticker}_{strategy}_{entry_date.strftime('%Y-%m-%d')}",
                "Ticker": ticker,
                "Strategy_Type": strategy,
                "Short_Window": np.random.randint(5, 30),
                "Long_Window": np.random.randint(30, 70),
                "Signal_Window": 0,
                "Entry_Timestamp": entry_date.strftime("%Y-%m-%d %H:%M:%S"),
                "Exit_Timestamp": (
                    entry_date + timedelta(days=np.random.randint(1, 120))
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "Avg_Entry_Price": np.random.uniform(100, 500),
                "Avg_Exit_Price": np.random.uniform(100, 500),
                "Position_Size": 1.0,
                "Direction": "Long",
                "PnL": round(pnl, 2),
                "Return": round(pnl / 1000, 4),  # Assuming $1000 position size
                "Duration_Days": np.random.randint(1, 120),
                "Trade_Type": "Long",
                "Status": "Closed",
                "Max_Favourable_Excursion": round(abs(pnl) * 1.2, 6),
                "Max_Adverse_Excursion": round(abs(pnl) * 0.3, 6),
                "MFE_MAE_Ratio": round(np.random.uniform(1, 10), 2),
                "Exit_Efficiency": round(np.random.uniform(0.5, 1.0), 4),
                "Days_Since_Entry": np.random.randint(1, 120),
                "Current_Unrealized_PnL": round(pnl, 4),
                "Current_Excursion_Status": "Favorable" if pnl > 0 else "Adverse",
                "Exit_Efficiency_Fixed": round(np.random.uniform(0.5, 1.0), 4),
                "Trade_Quality": "Excellent",
                "X_Status": str(np.random.randint(1000000000000000, 9999999999999999)),
            }
            trades.append(trade)

        return pd.DataFrame(trades)

    def _generate_open_positions_data(self) -> pd.DataFrame:
        """Generate open positions PnL time series data"""
        tickers = ["AMZN", "FFIV", "RTX", "AMD", "NVDA"]

        # Generate time series for each open position
        positions = []
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=90), end=datetime.now(), freq="D"
        )

        for ticker in tickers:
            entry_date = datetime.now() - timedelta(days=np.random.randint(30, 90))
            cumulative_pnl = 0.0

            for date in dates:
                if date >= entry_date:
                    # Add daily PnL change
                    daily_change = np.random.normal(
                        2, 10
                    )  # $2 average daily gain, $10 volatility
                    cumulative_pnl += daily_change

                    positions.append(
                        {
                            "Date": date.strftime("%Y-%m-%d"),
                            "Ticker": ticker,
                            "PnL": round(cumulative_pnl, 2),
                        }
                    )

        return pd.DataFrame(positions)

    def _ensure_directories(self):
        """Ensure all required output directories exist"""
        directories = [
            self.frontend_data_dir / "portfolio",
            self.frontend_data_dir / "portfolio/live-signals",
            self.frontend_data_dir / "trade-history",
            self.frontend_data_dir / "open-positions",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def validate_data_freshness(self) -> Dict[str, Any]:
        """Validate freshness of chart data files using discovered contracts"""
        validation_results = {}
        current_time = datetime.now()

        # Ensure contracts are discovered
        if not self.contracts:
            self.discover_contracts()

        # Group contracts by category
        contracts_by_category: Dict[str, List[DataContract]] = {}
        for contract in self.contracts:
            if contract.category not in contracts_by_category:
                contracts_by_category[contract.category] = []
            contracts_by_category[contract.category].append(contract)

        # Validate each category
        for category, contracts in contracts_by_category.items():
            category_results: Dict[str, Any] = {
                "files": {},
                "status": "healthy",
                "issues": [],
            }

            for contract in contracts:
                file_path = contract.file_path
                filename = file_path.name

                if file_path.exists():
                    file_age_hours = (
                        current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                    ).total_seconds() / 3600

                    # Use source-based logic for portfolio and trade-history data
                    needs_update = False
                    update_reason = ""

                    if category in ["portfolio", "trade-history"]:
                        # Extract portfolio name from contract
                        portfolio_name = self._extract_portfolio_name_from_contract(
                            contract
                        )
                        if portfolio_name:
                            source_mod_time = self._get_source_data_modification_time(
                                portfolio_name
                            )
                            output_mod_time = datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            )

                            if source_mod_time and source_mod_time > output_mod_time:
                                needs_update = True
                                source_age_hours = (
                                    current_time - source_mod_time
                                ).total_seconds() / 3600
                                update_reason = f"Source data modified {source_age_hours:.1f}h ago, output is outdated"
                            else:
                                needs_update = False
                                update_reason = "Output is up-to-date with source data"
                        else:
                            # Fallback to time-based logic
                            needs_update = (
                                file_age_hours > contract.freshness_threshold_hours
                            )
                            update_reason = f"File is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"
                    elif category == "open-positions":
                        # Special logic for open positions: check if positions actually exist
                        portfolio_name = self._extract_portfolio_name_from_contract(
                            contract
                        )
                        if portfolio_name:
                            has_open_positions = self._check_open_positions_exist(
                                portfolio_name
                            )
                            if not has_open_positions:
                                # No open positions, only update if file is very old (cleanup)
                                needs_update = (
                                    file_age_hours > 24
                                )  # 24h cleanup threshold
                                update_reason = (
                                    f"No open positions, cleanup needed (file is {file_age_hours:.1f}h old)"
                                    if needs_update
                                    else "No open positions, no update needed"
                                )
                            else:
                                # Has open positions, use standard freshness check
                                needs_update = (
                                    file_age_hours > contract.freshness_threshold_hours
                                )
                                update_reason = f"Open positions exist, file is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"
                        else:
                            # Fallback to time-based logic
                            needs_update = (
                                file_age_hours > contract.freshness_threshold_hours
                            )
                            update_reason = f"File is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"
                    else:
                        # Default time-based logic for other categories
                        needs_update = (
                            file_age_hours > contract.freshness_threshold_hours
                        )
                        update_reason = f"File is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"

                    file_status = "stale" if needs_update else "fresh"

                    category_results["files"][filename] = {
                        "exists": True,
                        "age_hours": round(file_age_hours, 2),
                        "status": file_status,
                        "size_bytes": file_path.stat().st_size,
                        "threshold_hours": contract.freshness_threshold_hours,
                        "update_reason": update_reason,
                    }

                    if file_status == "stale":
                        issues_list = category_results["issues"]
                    if isinstance(issues_list, list):
                        issues_list.append(update_reason)
                else:
                    category_results["files"][filename] = {
                        "exists": False,
                        "status": "missing",
                        "threshold_hours": contract.freshness_threshold_hours,
                    }
                    category_results["issues"].append(f"{filename} does not exist")

            issues_list = category_results["issues"]
            if isinstance(issues_list, list) and issues_list:
                category_results["status"] = "issues"

            validation_results[category] = category_results

        return validation_results

    def run_dry_run_analysis(self) -> DryRunReport:
        """Run comprehensive dry-run analysis without making changes"""
        report = DryRunReport()

        try:
            # Step 1: Discover all contracts
            self.logger.info("Discovering contracts for dry-run analysis")
            report.add_operation(
                "Contract Discovery", 0.1, "Scanning frontend directory structure"
            )

            self.discover_contracts()

            # Analyze each contract
            for contract in self.contracts:
                try:
                    # Determine contract status using same logic as validate_data_freshness
                    if not contract.file_path.exists():
                        status = "missing"
                        reason = "File does not exist"
                    else:
                        file_age_hours = (
                            datetime.now() - contract.last_modified
                        ).total_seconds() / 3600

                        # Use source-based logic for portfolio and trade-history data
                        needs_update = False
                        update_reason = ""

                        if contract.category in ["portfolio", "trade-history"]:
                            # Extract portfolio name from contract
                            portfolio_name = self._extract_portfolio_name_from_contract(
                                contract
                            )
                            if portfolio_name:
                                source_mod_time = (
                                    self._get_source_data_modification_time(
                                        portfolio_name
                                    )
                                )
                                output_mod_time = contract.last_modified

                                if (
                                    source_mod_time
                                    and source_mod_time > output_mod_time
                                ):
                                    needs_update = True
                                    source_age_hours = (
                                        datetime.now() - source_mod_time
                                    ).total_seconds() / 3600
                                    update_reason = f"Source data modified {source_age_hours:.1f}h ago, output is outdated"
                                else:
                                    needs_update = False
                                    update_reason = f"File is {file_age_hours:.1f}h old, up-to-date with source"
                            else:
                                # Fallback to time-based logic
                                needs_update = (
                                    file_age_hours > contract.freshness_threshold_hours
                                )
                                update_reason = f"File is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"
                        elif contract.category == "open-positions":
                            # Special logic for open positions
                            portfolio_name = self._extract_portfolio_name_from_contract(
                                contract
                            )
                            if portfolio_name:
                                has_open_positions = self._check_open_positions_exist(
                                    portfolio_name
                                )
                                if not has_open_positions:
                                    needs_update = (
                                        file_age_hours > 24
                                    )  # 24h cleanup threshold
                                    update_reason = (
                                        f"No open positions, cleanup needed (file is {file_age_hours:.1f}h old)"
                                        if needs_update
                                        else f"No open positions, file is {file_age_hours:.1f}h old (no update needed)"
                                    )
                                else:
                                    needs_update = (
                                        file_age_hours
                                        > contract.freshness_threshold_hours
                                    )
                                    update_reason = f"Open positions exist, file is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"
                            else:
                                needs_update = (
                                    file_age_hours > contract.freshness_threshold_hours
                                )
                                update_reason = f"File is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"
                        else:
                            # Default time-based logic for other categories
                            needs_update = (
                                file_age_hours > contract.freshness_threshold_hours
                            )
                            update_reason = f"File is {file_age_hours:.1f}h old (threshold: {contract.freshness_threshold_hours}h)"

                        status = "stale" if needs_update else "fresh"
                        reason = update_reason

                    report.add_contract(contract, status, reason)

                    # Add service mapping
                    capable_services = self.map_contract_to_services(contract)
                    report.set_service_mapping(contract.contract_id, capable_services)

                    # Add to update plan if needed
                    if status in ["missing", "stale"]:
                        estimated_rows = self._estimate_data_rows(contract)
                        estimated_time = self._estimate_processing_time(
                            contract, estimated_rows
                        )

                        report.add_update_plan_item(
                            str(contract.file_path),
                            reason,
                            estimated_time,
                            estimated_rows,
                        )

                        # Add detailed operation for this file
                        operation_details = (
                            f"{estimated_rows} rows, {contract.category} category"
                        )
                        report.add_operation(
                            f"Generate {contract.relative_path}",
                            estimated_time,
                            operation_details,
                        )

                    # Simulate validation
                    validation_issues = self._simulate_validation(contract)
                    report.add_validation_result(
                        contract.contract_id,
                        len(validation_issues) == 0,
                        validation_issues,
                    )

                except Exception as e:
                    error_msg = (
                        f"Failed to analyze contract {contract.contract_id}: {str(e)}"
                    )
                    report.add_error(error_msg)
                    self.logger.error(error_msg)

            # Step 2: Get current data status
            self.logger.info("Analyzing current data status")
            report.add_operation(
                "Data Status Analysis", 0.5, "Checking file freshness and sizes"
            )

            current_status = self.validate_data_freshness()
            for category, status_data in current_status.items():
                report.set_current_data_status(category, status_data)

            # Step 3: Add summary operations
            total_files_to_update = len(report.update_plan)
            if total_files_to_update > 0:
                report.add_operation(
                    "Data Generation Phase",
                    15.0,
                    f"{total_files_to_update} files to update",
                )
                report.add_operation(
                    "CSV Transformation", 5.0, "Convert data to frontend format"
                )
                report.add_operation(
                    "Schema Validation", 2.0, "Validate output schemas"
                )

            self.logger.info(
                f"Dry-run analysis completed. {total_files_to_update} files would be updated."
            )

        except Exception as e:
            error_msg = f"Dry-run analysis failed: {str(e)}"
            report.add_error(error_msg)
            self.logger.error(error_msg)

        return report

    def _estimate_data_rows(self, contract: DataContract) -> int:
        """Estimate number of rows that would be generated for a contract"""
        if contract.category == "portfolio":
            if "live-signals" in contract.relative_path:
                return 150  # ~5 months of daily data
            else:
                return 3960  # ~11 years of daily data (2014-2025)
        elif contract.category == "trade-history":
            return 45  # Typical number of closed trades
        elif contract.category == "open-positions":
            return 450  # 5 positions × 90 days
        else:
            return 100  # Default estimate

    def _estimate_processing_time(
        self, contract: DataContract, row_count: int
    ) -> float:
        """Estimate processing time for a contract in seconds"""
        base_time = 1.0  # Base processing time
        row_factor = max(1.0, row_count / 1000.0)  # Scale with row count

        if contract.category == "portfolio":
            return base_time * row_factor * 2.0  # Portfolio data is more complex
        elif contract.category == "live-signals":
            return base_time * row_factor * 3.0  # Live signals require more processing
        else:
            return base_time * row_factor

    def _simulate_validation(self, contract: DataContract) -> List[str]:
        """Simulate validation and return potential issues"""
        issues = []

        # Check if file path is valid
        if not contract.file_path.parent.exists():
            issues.append(
                f"Parent directory does not exist: {contract.file_path.parent}"
            )

        # Check expected schema
        if not contract.schema:
            issues.append("No expected schema defined")

        # Check for known problematic paths
        if "sensylate-command-system-enhancements" in str(contract.file_path):
            issues.append("File path references external project directory")

        return issues


def main():
    """Main entry point for data pipeline management"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Manage chart data pipeline for frontend"
    )
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate data freshness"
    )
    parser.add_argument(
        "--skip-errors",
        action="store_true",
        help="Continue despite individual failures",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--quiet", action="store_true", help="Enable quiet mode (warnings only)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze what would be updated without making changes",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "table"],
        default="text",
        help="Output format for reports (default: text)",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize pipeline manager with quiet mode if requested
    pipeline = DataPipelineManager(quiet_mode=args.quiet)

    if args.validate_only:
        # Validate data freshness only
        validation_results = pipeline.validate_data_freshness()

        print("📊 Chart Data Freshness Validation")
        print("=" * 50)

        overall_healthy = True
        for category, results in validation_results.items():
            status_emoji = "✅" if results["status"] == "healthy" else "⚠️"
            print(f"{status_emoji} {category.title()}: {results['status']}")

            if results["issues"]:
                overall_healthy = False
                for issue in results["issues"]:
                    print(f"   - {issue}")

        exit_code = 0 if overall_healthy else 1
        print(
            f"\nOverall Status: {'✅ Healthy' if overall_healthy else '⚠️ Issues Found'}"
        )
        sys.exit(exit_code)

    elif args.dry_run:
        # Dry-run analysis mode
        print("🔍 Starting dry-run analysis...")
        report = pipeline.run_dry_run_analysis()

        # Generate and display report
        if args.format == "json":
            print(report.generate_json_report())
        elif args.format == "table":
            print(report.generate_text_report())
        else:
            print(report.generate_text_report())

        # Exit with appropriate code
        exit_code = 1 if report.errors else 0
        sys.exit(exit_code)

    else:
        # Contract-driven data refresh
        print("🔄 Starting contract-driven data refresh...")
        result = pipeline.refresh_all_chart_data(skip_errors=args.skip_errors)

        if result.success:
            print("✅ Contract-driven refresh completed successfully")
            print(
                f"   Contracts: {result.metadata.get('successful_contracts', 0)}/{result.metadata.get('total_contracts', 0)}"
            )
            print(
                f"   Categories: {len(result.metadata.get('categories_processed', []))}"
            )
            print(f"   Duration: {result.processing_time:.2f}s")

            # Show discovery statistics
            discovery_stats = result.metadata.get("discovery_stats", {})
            print(
                f"   Discovery: {discovery_stats.get('total_discovered', 0)} contracts found in {discovery_stats.get('discovery_time', 0):.2f}s"
            )

            sys.exit(0)
        else:
            print("❌ Contract-driven refresh failed")
            print(f"   Error: {result.error}")

            contract_results = result.metadata.get("contract_results", {})
            if contract_results.get("failed"):
                print(f"   Failed contracts: {contract_results['failed']}")
            if contract_results.get("unfulfillable"):
                print(
                    f"   Unfulfillable contracts: {contract_results['unfulfillable']}"
                )

            sys.exit(1)


if __name__ == "__main__":
    # numpy is already imported at the top of the file
    pass

    main()
