#!/usr/bin/env python3
"""
Contract Manager

Centralized contract discovery and service mapping system that:
- Discovers data requirements from active charts (demand-driven approach)
- Maps contracts to capable CLI services using active chart requirements
- Validates contract fulfillment capabilities
- Provides contract filtering and categorization

Implements ComponentLifecycle for proper initialization phases:
- init(): Basic initialization, dependency injection
- configure(): Expensive chart discovery and caching operations
- start(): Use cached discovery results for fast operations
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from component_lifecycle import ComponentLifecycle
from data_contract_discovery import ContractDiscoveryResult, DataContract
from result_types import ProcessingResult
from utils.logging_setup import setup_logging


class ContractManager(ComponentLifecycle):
    """Manages contract discovery, service mapping, and validation"""

    def __init__(
        self,
        frontend_src_path: Path,
        frontend_data_path: Path,
        cli_service_capabilities: Dict[str, dict],
    ):
        # Initialize ComponentLifecycle
        super().__init__("contract_manager")

        # Store dependencies (injected during init phase)
        self.frontend_src_path = frontend_src_path
        self.frontend_data_path = frontend_data_path
        self.cli_service_capabilities = cli_service_capabilities

        # Cache for discovered contracts (populated during configure phase)
        self.discovery_result: Optional[ContractDiscoveryResult] = None
        self.contracts: List[DataContract] = []

        # Cached active requirements (expensive operation moved to configure phase)
        self._cached_active_requirements = None
        self._cached_detector = None

    def _do_init(self) -> None:
        """Phase 1: Basic initialization - dependencies already injected in __init__"""
        self.logger.debug("ContractManager initialized with ComponentLifecycle")

    def _do_configure(self) -> None:
        """Phase 2: Expensive chart discovery operations and caching"""
        self.logger.info(
            "Configuring ContractManager - performing expensive chart discovery operations..."
        )

        # Cache the expensive ActiveChartRequirementsDetector operations
        self._cache_active_requirements()

        # Cache the contract discovery results
        self._cache_contract_discovery()

        self.logger.info(
            "ContractManager configuration completed - all expensive discovery operations cached"
        )

    def _do_start(self) -> None:
        """Phase 3: Ready for fast operations using cached results"""
        self.logger.debug("ContractManager started - using cached discovery results")

    def _cache_active_requirements(self) -> None:
        """Cache expensive active chart requirements discovery"""
        self.logger.debug("Caching active chart requirements discovery...")

        # Import and create detector once
        from active_chart_requirements import ActiveChartRequirementsDetector

        self._cached_detector = ActiveChartRequirementsDetector(
            frontend_src_path=self.frontend_src_path,
            frontend_data_path=self.frontend_data_path,
        )

        # Perform expensive discovery once and cache results
        self._cached_active_requirements = (
            self._cached_detector.discover_active_requirements()
        )

        self.logger.debug(
            f"Active requirements cached: {len(self._cached_active_requirements.requirements)} requirements"
        )

    def _cache_contract_discovery(self) -> None:
        """Cache contract discovery results using cached active requirements"""
        if self._cached_active_requirements is None:
            raise RuntimeError(
                "Active requirements must be cached before contract discovery"
            )

        self.logger.debug("Caching contract discovery results...")

        active_requirements = self._cached_active_requirements

        # Convert active requirements to contracts format for compatibility
        active_contracts = []

        for req in active_requirements.requirements:
            # Create virtual contract from active chart requirement
            contract = DataContract(
                contract_id=f"{req.category}_{req.chart_type}_{Path(req.data_source).stem}",
                category=req.category,
                file_path=Path(req.file_path),
                relative_path=req.data_source,
                schema=[],  # Schema will be determined during generation
                minimum_rows=0,
                freshness_threshold_hours=24,
            )
            active_contracts.append(contract)

        # Create discovery result with only active chart requirements
        self.discovery_result = ContractDiscoveryResult(
            contracts=active_contracts,
            categories=active_requirements.categories_needed,
            total_files=active_requirements.total_active_charts,
            successful_discoveries=len(active_contracts),
            failed_discoveries=[],
            discovery_time=active_requirements.discovery_time_seconds,
        )

        self.contracts = active_contracts

        self.logger.info(
            f"Contract discovery cached: {len(active_contracts)} data files needed for "
            f"{active_requirements.total_active_charts} active charts "
            f"(skipped {active_requirements.total_frozen_charts} frozen charts)"
        )

        if active_requirements.total_frozen_charts > 0:
            self.logger.debug(
                f"Runtime filtering: excluded {active_requirements.total_frozen_charts} frozen charts "
                f"from data requirements (demand-driven approach)"
            )

    def discover_contracts(self) -> ContractDiscoveryResult:
        """Fast contract discovery using cached results from configure() phase"""
        # Ensure component is configured
        if not self.is_configured():
            raise RuntimeError(
                "ContractManager must be configured before discovery operations"
            )

        if self.discovery_result is None:
            raise RuntimeError(
                "Contract discovery cache not available - configuration may have failed"
            )

        self.logger.debug(
            f"Returning cached contract discovery: {len(self.contracts)} contracts"
        )
        return self.discovery_result

    def get_contracts_by_category(self, category: str) -> List[DataContract]:
        """Get contracts for a specific category using cached results"""
        # Ensure discovery has been performed (uses cached results)
        self.discover_contracts()

        contracts = [c for c in self.contracts if c.category == category]
        self.logger.debug(f"Found {len(contracts)} contracts for category '{category}'")
        return contracts

    def map_contract_to_services(self, contract: DataContract) -> List[str]:
        """Fast contract-to-service mapping using cached active requirements"""
        # Ensure component is configured
        if not self.is_configured():
            raise RuntimeError(
                "ContractManager must be configured before service mapping operations"
            )

        if self._cached_active_requirements is None:
            raise RuntimeError(
                "Active requirements cache not available - configuration may have failed"
            )

        try:
            # Find matching requirement for this contract using cached results
            active_requirements = self._cached_active_requirements
            for req in active_requirements.requirements:
                if str(contract.relative_path) == req.data_source:
                    self.logger.debug(
                        f"Found cached service mapping for {contract.contract_id}: {req.required_services}"
                    )
                    return req.required_services

            # Fallback to category-based service mapping if no specific requirement found
            category_service_map = {
                "portfolio": ["yahoo_finance", "alpha_vantage"],
                "trade-history": ["trade_history"],
                "open-positions": ["trade_history"],
                "raw": ["yahoo_finance"],
            }

            services = category_service_map.get(contract.category, [])
            self.logger.debug(
                f"Used category-based mapping for {contract.contract_id}: {services}"
            )
            return services

        except Exception as e:
            self.logger.warning(f"Error mapping contract to services: {e}")

            # Final fallback to old logic
            capable_services = []
            for service_name, capabilities in self.cli_service_capabilities.items():
                if contract.category in capabilities["categories"]:
                    capable_services.append(service_name)
            self.logger.debug(
                f"Used fallback mapping for {contract.contract_id}: {capable_services}"
            )
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

        # Check freshness if file has last_modified time
        if hasattr(contract, "last_modified") and contract.last_modified is not None:
            file_age_hours = (
                datetime.now() - contract.last_modified
            ).total_seconds() / 3600
            if file_age_hours > contract.freshness_threshold_hours:
                return ProcessingResult(
                    success=False,
                    operation=f"validate_contract_{contract.contract_id}",
                    error=f"Contract data is stale ({file_age_hours:.1f}h > {contract.freshness_threshold_hours}h threshold)",
                )
        else:
            # If no last_modified time, use file modification time
            try:
                file_stat = contract.file_path.stat()
                file_mtime = datetime.fromtimestamp(file_stat.st_mtime)
                file_age_hours = (datetime.now() - file_mtime).total_seconds() / 3600
                if file_age_hours > contract.freshness_threshold_hours:
                    return ProcessingResult(
                        success=False,
                        operation=f"validate_contract_{contract.contract_id}",
                        error=f"Contract data is stale ({file_age_hours:.1f}h > {contract.freshness_threshold_hours}h threshold)",
                    )
            except Exception:
                # If we can't get file modification time, assume it's fresh
                file_age_hours = 0

        result = ProcessingResult(
            success=True, operation=f"validate_contract_{contract.contract_id}"
        )
        result.add_metadata("capable_services", capable_services)
        result.add_metadata("file_age_hours", file_age_hours)
        result.add_metadata("freshness_threshold", contract.freshness_threshold_hours)

        return result

    def get_unfulfillable_contracts(self, contracts: List[DataContract]) -> List[str]:
        """Get list of contracts that cannot be fulfilled by available services"""
        unfulfillable = []

        for contract in contracts:
            capable_services = self.map_contract_to_services(contract)
            if not capable_services:
                unfulfillable.append(contract.contract_id)

        return unfulfillable

    def group_contracts_by_category(
        self, contracts: List[DataContract]
    ) -> Dict[str, List[DataContract]]:
        """Group contracts by category for efficient processing"""
        contracts_by_category = {}

        for contract in contracts:
            if contract.category not in contracts_by_category:
                contracts_by_category[contract.category] = []
            contracts_by_category[contract.category].append(contract)

        return contracts_by_category
