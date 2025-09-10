#!/usr/bin/env python3
"""
Validation Engine

Comprehensive validation system that:
- Validates service dependencies and health status
- Performs contract schema validation and compliance checking
- Validates data freshness and quality requirements
- Provides simulation capabilities for dry-run analysis
- Enforces CLI contract validation with fail-fast approach

Implements ComponentLifecycle for proper initialization phases:
- init(): Basic initialization, dependency injection
- configure(): Expensive validation and caching operations
- start(): Use cached validation results for fast operations
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import pandas as pd

from cli_contract_validator import CLIContractValidator
from component_lifecycle import ComponentLifecycle
from contract_manager import ContractManager
from data_contract_discovery import DataContract
from errors import ValidationError
from result_types import ProcessingResult
from service_health_manager import ServiceHealthManager


class ValidationEngine(ComponentLifecycle):
    """Comprehensive validation engine for data pipeline operations"""

    def __init__(
        self,
        service_health_manager: ServiceHealthManager,
        contract_manager: ContractManager,
        cli_service_capabilities: Dict[str, Any],
    ):
        # Initialize ComponentLifecycle
        super().__init__("validation_engine")
        
        # Store dependencies (injected during init phase)
        self.service_health_manager = service_health_manager
        self.contract_manager = contract_manager
        self.cli_service_capabilities = cli_service_capabilities

        # Initialize CLI contract validator for pre-execution validation
        self.cli_validator = CLIContractValidator()

        # Cache for validated CLI contracts
        self._validated_contracts: Set[str] = set()
        
        # Cached validation results (populated during configure phase)
        self._service_validation_cache: Optional[Dict[str, Any]] = None
        self._contract_discovery_cache: Optional[List[DataContract]] = None
        self._schema_validation_cache: Optional[Dict[str, Any]] = None

    def _do_init(self) -> None:
        """Phase 1: Basic initialization - dependencies already injected in __init__"""
        self.logger.debug("ValidationEngine initialized with ComponentLifecycle")
        
    def _do_configure(self) -> None:
        """Phase 2: Expensive validation operations and caching"""
        self.logger.info("Configuring ValidationEngine - performing expensive validation operations...")
        
        # Cache service dependency validation results
        self._cache_service_validation()
        
        # Cache contract discovery results
        self._cache_contract_discovery()
        
        # Cache schema validation results
        self._cache_schema_validation()
        
        self.logger.info("ValidationEngine configuration completed - all expensive operations cached")
        
    def _do_start(self) -> None:
        """Phase 3: Ready for fast operations using cached results"""
        self.logger.debug("ValidationEngine started - using cached validation results")
        
    def _cache_service_validation(self) -> None:
        """Cache expensive service dependency validation"""
        start_time = datetime.now()
        self.logger.debug("Caching service dependency validation results...")
        
        # Perform the expensive validation once and cache results
        service_validation = self.service_health_manager.validate_service_dependencies()
        
        # Discover contracts for dependency chain validation
        discovery_result = self.contract_manager.discover_contracts()
        
        # Validate service-contract mappings
        validation_results = []
        failed_services = []
        
        if not service_validation["success"]:
            availability = service_validation.get("availability", {})
            health = service_validation.get("health", {})
            failed_services.extend(availability.get("failed_services", []))
            failed_services.extend(health.get("failed_services", []))
            validation_results.append(
                f"Service {service_validation['stage']} check failed: {service_validation['error']}"
            )
        
        # Check contract-service mappings
        for contract in discovery_result.contracts:
            capable_services = self.contract_manager.map_contract_to_services(contract)
            if not capable_services:
                validation_results.append(
                    f"No services available for contract {contract.contract_id}"
                )
                continue
                
            available_capable_services = [
                svc for svc in capable_services if svc not in failed_services
            ]
            
            if not available_capable_services:
                validation_results.append(
                    f"Contract {contract.contract_id} requires services {capable_services} "
                    f"but none are available/healthy"
                )
        
        # Cache the validation results
        success = len(validation_results) == 0
        duration = datetime.now() - start_time
        
        self._service_validation_cache = {
            "success": success,
            "validation_results": validation_results,
            "failed_services": failed_services,
            "contracts_checked": len(discovery_result.contracts),
            "services_checked": len(self.cli_service_capabilities),
            "duration_seconds": duration.total_seconds(),
            "cached_at": datetime.now()
        }
        
        # Store discovery result in cache
        self._contract_discovery_cache = discovery_result.contracts
        
        self.logger.debug(f"Service validation cached in {duration.total_seconds():.2f}s")
        
    def _cache_contract_discovery(self) -> None:
        """Cache contract discovery results (may already be cached from service validation)"""
        if self._contract_discovery_cache is None:
            self.logger.debug("Caching contract discovery results...")
            discovery_result = self.contract_manager.discover_contracts()
            self._contract_discovery_cache = discovery_result.contracts
        else:
            self.logger.debug("Contract discovery already cached")
            
    def _cache_schema_validation(self) -> None:
        """Cache schema validation results"""
        if self._contract_discovery_cache is None:
            self.logger.warning("Cannot cache schema validation - no contracts discovered")
            return
            
        self.logger.debug("Caching schema validation results...")
        schema_validation = self.service_health_manager.validate_contract_schemas(
            self._contract_discovery_cache
        )
        
        self._schema_validation_cache = {
            **schema_validation,
            "cached_at": datetime.now()
        }
        
        self.logger.debug("Schema validation cached")
        
    def validate_service_dependencies(self) -> ProcessingResult:
        """
        Fast service dependency validation using cached results from configure() phase

        Returns:
            ProcessingResult with detailed validation status
        """
        # Ensure component is configured
        if not self.is_configured():
            raise RuntimeError("ValidationEngine must be configured before validation operations")
            
        if self._service_validation_cache is None:
            raise RuntimeError("Service validation cache not available - configuration may have failed")
            
        try:
            cached_result = self._service_validation_cache
            
            result = ProcessingResult(
                success=cached_result["success"],
                operation="validate_service_dependencies",
                error="; ".join(cached_result["validation_results"]) if cached_result["validation_results"] else None,
            )
            
            result.add_metadata("duration_seconds", cached_result["duration_seconds"])
            result.add_metadata("failed_services", cached_result["failed_services"])
            result.add_metadata("validation_results", cached_result["validation_results"])
            result.add_metadata("contracts_checked", cached_result["contracts_checked"])
            result.add_metadata("services_checked", cached_result["services_checked"])
            result.add_metadata("cached_at", cached_result["cached_at"].isoformat())
            result.add_metadata("using_cache", True)
            
            if cached_result["success"]:
                self.logger.debug(
                    f"Service dependency validation (cached): PASSED in {cached_result['duration_seconds']:.2f}s"
                )
            else:
                self.logger.warning(
                    f"Service dependency validation (cached): FAILED - {len(cached_result['validation_results'])} issues found"
                )
                
            return result
            
        except Exception as e:
            error_msg = f"Failed to retrieve cached service validation results: {str(e)}"
            self.logger.error(error_msg)
            
            result = ProcessingResult(
                success=False,
                operation="validate_service_dependencies",
                error=error_msg,
            )
            result.add_metadata("using_cache", False)
            return result

    def validate_contract_data(self, contract: DataContract) -> ProcessingResult:
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
                error=f"Contract validation failed: {e}",
            )

    def validate_data_freshness(self, contracts: List[DataContract]) -> Dict[str, Any]:
        """Validate freshness of chart data files using discovered contracts"""
        validation_results = {}
        current_time = datetime.now()

        # Group contracts by category
        contracts_by_category: Dict[str, List[DataContract]] = {}
        for contract in contracts:
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
                        current_time - contract.last_modified
                    ).total_seconds() / 3600
                    
                    file_info = {
                        "exists": True,
                        "age_hours": round(file_age_hours, 2),
                        "freshness_threshold": contract.freshness_threshold_hours,
                        "is_fresh": file_age_hours <= contract.freshness_threshold_hours,
                        "last_modified": contract.last_modified.isoformat(),
                    }

                    if not file_info["is_fresh"]:
                        issue = f"{filename} is stale ({file_age_hours:.1f}h > {contract.freshness_threshold_hours}h)"
                        category_results["issues"].append(issue)
                        category_results["status"] = "stale"

                else:
                    file_info = {
                        "exists": False,
                        "age_hours": None,
                        "freshness_threshold": contract.freshness_threshold_hours,
                        "is_fresh": False,
                        "last_modified": None,
                    }
                    issue = f"{filename} does not exist"
                    category_results["issues"].append(issue)
                    category_results["status"] = "missing"

                category_results["files"][filename] = file_info

            validation_results[category] = category_results

        return validation_results

    def simulate_validation(self, contract: DataContract) -> List[str]:
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

    def validate_cli_contract(self, service_name: str, command: str) -> None:
        """
        Validate CLI contract before execution to prevent runtime failures

        Args:
            service_name: Name of the service (e.g., 'yahoo_finance', 'alpha_vantage')
            command: Command to validate (e.g., 'history', 'analyze')

        Raises:
            ValidationError: If the CLI contract is invalid
        """
        contract_key = f"{service_name}:{command}"

        # Skip validation if already validated in this session
        if contract_key in self._validated_contracts:
            return

        self.logger.debug(f"Validating CLI contract: {service_name}.{command}")

        validation_result = self.cli_validator.validate_service_command(
            service_name, command
        )

        if not validation_result.is_valid:
            error_msg = f"CLI contract validation failed for {service_name}.{command}: {validation_result.error_message}"
            self.logger.error(error_msg)
            raise ValidationError(error_msg)

        # Cache successful validation
        self._validated_contracts.add(contract_key)
        self.logger.debug(f"CLI contract validated successfully: {service_name}.{command}")

    def get_validation_cache_info(self) -> Dict[str, Any]:
        """Get information about validation cache state"""
        cache_info = {
            "validated_contracts_count": len(self._validated_contracts),
            "validated_contracts": list(self._validated_contracts),
            "component_state": self.state.value,
            "cache_valid": self._cache_valid,
        }
        
        if self._service_validation_cache:
            cache_info["service_validation_cached_at"] = self._service_validation_cache["cached_at"].isoformat()
            cache_info["service_validation_success"] = self._service_validation_cache["success"]
            
        if self._contract_discovery_cache:
            cache_info["contracts_in_cache"] = len(self._contract_discovery_cache)
            
        if self._schema_validation_cache:
            cache_info["schema_validation_cached_at"] = self._schema_validation_cache["cached_at"].isoformat()
            cache_info["schema_validation_success"] = self._schema_validation_cache["success"]
            
        return cache_info

    def clear_validation_cache(self) -> None:
        """Clear validation cache (useful for testing or cache invalidation)"""
        self.logger.debug(f"Clearing validation cache ({len(self._validated_contracts)} CLI contracts)")
        self._validated_contracts.clear()
        
        # Clear component lifecycle cache
        self.invalidate_cache()
        
        # Clear validation-specific caches
        self._service_validation_cache = None
        self._contract_discovery_cache = None
        self._schema_validation_cache = None
        
        self.logger.debug("All validation caches cleared")