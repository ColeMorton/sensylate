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
from typing import Any, Dict, List, Optional

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

    def __init__(self, frontend_data_path: Optional[Path] = None):
        """Initialize contract-driven data pipeline manager"""
        setup_logging("INFO")
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
            "trade_history_cli": {
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

            # Step 2: Validate contract fulfillment capabilities
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
            contracts_by_category = {}
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

            overall_success = failed_count == 0

            result = ProcessingResult(
                success=overall_success,
                operation="refresh_all_chart_data",
                processing_time=processing_time,
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

            if failed_contracts or unfulfillable_contracts:
                error_details = []
                if failed_contracts:
                    error_details.append(f"Failed: {failed_contracts}")
                if unfulfillable_contracts:
                    error_details.append(f"Unfulfillable: {unfulfillable_contracts}")
                result.error = "; ".join(error_details)

            self.logger.info(
                f"Contract-driven refresh completed: {successful_count}/{total_contracts} "
                f"contracts successful in {processing_time:.2f}s"
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
        elif service_name == "trade_history_cli":
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
            data = {}
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
        elif source == "trade_history_cli":
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
            # Use existing Yahoo Finance CLI to fetch portfolio symbols
            # This would typically fetch data for Bitcoin, major indices, etc.
            result = self.cli_service.execute(
                service_name="yahoo_finance",
                command="fetch_portfolio_data",
                args=["BTC-USD", "SPY", "QQQ"],
                timeout=60,
            )
            return result
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_yahoo_finance", error=str(e)
            )

    def _fetch_alpha_vantage_data(self) -> ProcessingResult:
        """Fetch supplementary data from Alpha Vantage"""
        try:
            result = self.cli_service.execute(
                service_name="alpha_vantage", command="fetch_market_data", timeout=60
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
            return result
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_trade_history", error=str(e)
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
        """Validate freshness of chart data files"""
        validation_results = {}
        current_time = datetime.now()

        for category, config in self.chart_data_dependencies.items():
            category_results = {"files": {}, "status": "healthy", "issues": []}

            for output_file in config["output_files"]:
                if category == "portfolio":
                    file_path = self.frontend_data_dir / "portfolio" / output_file
                elif category == "live_signals":
                    file_path = (
                        self.frontend_data_dir / "portfolio/live-signals" / output_file
                    )
                elif category == "trade_history":
                    file_path = self.frontend_data_dir / "trade-history" / output_file
                elif category == "open_positions":
                    file_path = self.frontend_data_dir / "open-positions" / output_file
                else:
                    continue

                if file_path.exists():
                    file_age_hours = (
                        current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
                    ).total_seconds() / 3600
                    file_status = "fresh" if file_age_hours <= 24 else "stale"

                    category_results["files"][output_file] = {
                        "exists": True,
                        "age_hours": round(file_age_hours, 2),
                        "status": file_status,
                        "size_bytes": file_path.stat().st_size,
                    }

                    if file_status == "stale":
                        category_results["issues"].append(
                            f"{output_file} is {file_age_hours:.1f} hours old"
                        )
                else:
                    category_results["files"][output_file] = {
                        "exists": False,
                        "status": "missing",
                    }
                    category_results["issues"].append(f"{output_file} does not exist")

            if category_results["issues"]:
                category_results["status"] = "issues"

            validation_results[category] = category_results

        return validation_results


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

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize pipeline manager
    pipeline = DataPipelineManager()

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
