#!/usr/bin/env python3
"""
Universal Dependency Validator
Extends existing pre-execution coordination with intelligent fallback management
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

# Import existing coordination system
import sys
coordination_path = str(Path(__file__).parent.parent / "coordination")
if coordination_path not in sys.path:
    sys.path.append(coordination_path)

try:
    from pre_execution_consultation import PreExecutionConsultant
except ImportError:
    # Fallback for testing
    class PreExecutionConsultant:
        def __init__(self, workspace_path=None):
            pass

@dataclass
class DependencyRequirement:
    """Represents a single dependency requirement"""
    name: str
    type: str  # "data_source", "api", "file", "service"
    required: bool
    fallback_strategies: List[str]
    validation_method: str
    timeout: int = 30

@dataclass
class ValidationResult:
    """Result of dependency validation"""
    dependency_name: str
    available: bool
    validation_score: float  # 0.0-1.0
    fallback_used: Optional[str] = None
    error_message: Optional[str] = None
    response_time: float = 0.0

class UniversalDependencyValidator:
    """
    Universal validation system for all command dependencies
    Extends existing pre-execution coordination with intelligent fallbacks
    """

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.consultation_system = PreExecutionConsultant(workspace_path)
        self.cache_path = self.workspace_path / "framework" / "cache"
        self.cache_path.mkdir(parents=True, exist_ok=True)

        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_command_dependencies(self, command_name: str,
                                    dependency_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for command dependency validation

        Args:
            command_name: Name of the command requesting validation
            dependency_manifest: Loaded .deps.yaml content

        Returns:
            Comprehensive validation result with fallback recommendations
        """
        start_time = datetime.now()

        # Extract dependencies from manifest
        dependencies = self._parse_dependency_manifest(dependency_manifest)

        # Validate each dependency
        validation_results = []
        overall_score = 0.0
        critical_failures = []

        for dep in dependencies:
            result = self._validate_single_dependency(dep)
            validation_results.append(result)

            if dep.required and not result.available:
                critical_failures.append(dep.name)

            # Weight scoring by dependency importance
            weight = 1.0 if dep.required else 0.5
            overall_score += result.validation_score * weight

        # Calculate overall dependency health
        total_weight = sum(1.0 if dep.required else 0.5 for dep in dependencies)
        overall_score = overall_score / total_weight if total_weight > 0 else 0.0

        # Generate fallback strategy if needed
        fallback_strategy = None
        if overall_score < 0.8 or critical_failures:
            fallback_strategy = self._generate_fallback_strategy(
                dependencies, validation_results, critical_failures
            )

        execution_time = (datetime.now() - start_time).total_seconds()

        return {
            "command": command_name,
            "overall_score": overall_score,
            "can_proceed": overall_score >= 0.6 and not critical_failures,
            "validation_results": [self._serialize_validation_result(r) for r in validation_results],
            "critical_failures": critical_failures,
            "fallback_strategy": fallback_strategy,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_recommendations(overall_score, validation_results)
        }

    def _parse_dependency_manifest(self, manifest: Dict[str, Any]) -> List[DependencyRequirement]:
        """Parse dependency manifest into structured requirements"""
        dependencies = []

        deps_config = manifest.get("dependencies", {})

        for dep_name, dep_config in deps_config.items():
            dependencies.append(DependencyRequirement(
                name=dep_name,
                type=dep_config.get("type", "unknown"),
                required=dep_config.get("required", True),
                fallback_strategies=dep_config.get("fallback_strategies", []),
                validation_method=dep_config.get("validation_method", "basic"),
                timeout=dep_config.get("timeout", 30)
            ))

        return dependencies

    def _validate_single_dependency(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate a single dependency with fallback handling"""
        start_time = datetime.now()

        try:
            # Check cache first
            cached_result = self._check_dependency_cache(dependency.name)
            if cached_result and self._is_cache_fresh(cached_result, dependency):
                cached_result["response_time"] = (datetime.now() - start_time).total_seconds()
                return ValidationResult(**cached_result)

            # Validate based on dependency type
            if dependency.type == "api":
                result = self._validate_api_dependency(dependency)
            elif dependency.type == "data_source":
                result = self._validate_data_source(dependency)
            elif dependency.type == "file":
                result = self._validate_file_dependency(dependency)
            elif dependency.type == "service":
                result = self._validate_service_dependency(dependency)
            else:
                result = ValidationResult(
                    dependency_name=dependency.name,
                    available=False,
                    validation_score=0.0,
                    error_message=f"Unknown dependency type: {dependency.type}"
                )

            result.response_time = (datetime.now() - start_time).total_seconds()

            # Cache successful validation
            if result.validation_score > 0.5:
                self._cache_validation_result(dependency.name, result)

            return result

        except Exception as e:
            self.logger.error(f"Dependency validation failed for {dependency.name}: {str(e)}")
            return ValidationResult(
                dependency_name=dependency.name,
                available=False,
                validation_score=0.0,
                error_message=str(e),
                response_time=(datetime.now() - start_time).total_seconds()
            )

    def _validate_api_dependency(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate API-based dependencies"""
        try:
            # Special handling for known APIs
            if "yahoo" in dependency.name.lower() or "finance" in dependency.name.lower():
                return self._validate_yahoo_finance_api()
            elif "github" in dependency.name.lower():
                return self._validate_github_api()
            else:
                # Generic API validation
                return self._validate_generic_api(dependency)

        except Exception as e:
            return ValidationResult(
                dependency_name=dependency.name,
                available=False,
                validation_score=0.0,
                error_message=f"API validation failed: {str(e)}"
            )

    def _validate_yahoo_finance_api(self) -> ValidationResult:
        """Validate Yahoo Finance API availability"""
        try:
            # Check if yfinance is available
            try:
                import yfinance as yf
                # Simple validation - just check if we can import and create ticker
                test_ticker = yf.Ticker("AAPL")
                return ValidationResult(
                    dependency_name="yahoo_finance_api",
                    available=True,
                    validation_score=0.9  # Lower score since we didn't test actual API call
                )
            except ImportError:
                return ValidationResult(
                    dependency_name="yahoo_finance_api",
                    available=False,
                    validation_score=0.0,
                    error_message="yfinance library not installed"
                )

        except Exception as e:
            return ValidationResult(
                dependency_name="yahoo_finance_api",
                available=False,
                validation_score=0.0,
                error_message=f"Yahoo Finance API error: {str(e)}"
            )

    def _validate_data_source(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate data source availability"""
        # Check team workspace data availability
        if "team_workspace" in dependency.name:
            return self._validate_team_workspace_data(dependency)
        elif "market_data" in dependency.name:
            return self._validate_market_data_source(dependency)
        else:
            return ValidationResult(
                dependency_name=dependency.name,
                available=True,
                validation_score=0.8,
                error_message="Generic data source - assumed available"
            )

    def _validate_file_dependency(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate file-based dependencies"""
        try:
            # Check if this is a script or configuration file
            if dependency.name.endswith('.py'):
                file_path = Path(dependency.name)
                if not file_path.is_absolute():
                    # Check common script locations
                    for base_path in ["scripts", "team-workspace", "."]:
                        full_path = Path(base_path) / dependency.name
                        if full_path.exists():
                            file_path = full_path
                            break

                if file_path.exists():
                    return ValidationResult(
                        dependency_name=dependency.name,
                        available=True,
                        validation_score=1.0
                    )
                else:
                    return ValidationResult(
                        dependency_name=dependency.name,
                        available=False,
                        validation_score=0.0,
                        error_message=f"File not found: {dependency.name}"
                    )
            else:
                # Generic file validation
                return ValidationResult(
                    dependency_name=dependency.name,
                    available=True,
                    validation_score=0.9
                )

        except Exception as e:
            return ValidationResult(
                dependency_name=dependency.name,
                available=False,
                validation_score=0.0,
                error_message=f"File validation failed: {str(e)}"
            )

    def _validate_team_workspace_data(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate team workspace data availability"""
        try:
            # Check workspace health
            knowledge_path = self.workspace_path / "knowledge"
            commands_path = self.workspace_path / "commands"

            if not knowledge_path.exists() or not commands_path.exists():
                return ValidationResult(
                    dependency_name=dependency.name,
                    available=False,
                    validation_score=0.0,
                    error_message="Team workspace structure incomplete"
                )

            # Count available knowledge topics
            knowledge_topics = len(list(knowledge_path.iterdir()))
            commands_available = len(list(commands_path.iterdir()))

            # Calculate health score based on available resources
            health_score = min(1.0, (knowledge_topics * 0.05) + (commands_available * 0.03))

            return ValidationResult(
                dependency_name=dependency.name,
                available=health_score > 0.5,
                validation_score=health_score
            )

        except Exception as e:
            return ValidationResult(
                dependency_name=dependency.name,
                available=False,
                validation_score=0.0,
                error_message=f"Team workspace validation failed: {str(e)}"
            )

    def _generate_fallback_strategy(self, dependencies: List[DependencyRequirement],
                                   results: List[ValidationResult],
                                   critical_failures: List[str]) -> Dict[str, Any]:
        """Generate intelligent fallback strategy for failed dependencies"""
        strategy = {
            "type": "intelligent_fallback",
            "critical_failures": critical_failures,
            "recommended_actions": [],
            "alternative_approaches": [],
            "estimated_success_probability": 0.0
        }

        # Generate specific fallback recommendations
        for dep, result in zip(dependencies, results):
            if not result.available and dep.fallback_strategies:
                for fallback in dep.fallback_strategies:
                    strategy["recommended_actions"].append({
                        "dependency": dep.name,
                        "action": fallback,
                        "estimated_effectiveness": 0.7  # Default estimate
                    })

        # Calculate overall success probability with fallbacks
        success_factors = []
        for dep, result in zip(dependencies, results):
            if result.available:
                success_factors.append(1.0)
            elif dep.fallback_strategies:
                success_factors.append(0.6)  # Fallback success rate
            elif not dep.required:
                success_factors.append(0.8)  # Non-critical can be skipped
            else:
                success_factors.append(0.1)  # Critical failure

        strategy["estimated_success_probability"] = sum(success_factors) / len(success_factors) if success_factors else 0.0

        return strategy

    def _generate_recommendations(self, overall_score: float,
                                results: List[ValidationResult]) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []

        if overall_score < 0.6:
            recommendations.append("CRITICAL: Dependency health below acceptable threshold")
            recommendations.append("Consider postponing command execution until dependencies are resolved")

        elif overall_score < 0.8:
            recommendations.append("WARNING: Some dependencies have issues")
            recommendations.append("Proceed with caution and monitor for degraded performance")

        # Specific recommendations for slow dependencies
        slow_deps = [r for r in results if r.response_time > 10.0]
        if slow_deps:
            recommendations.append(f"Performance concern: {len(slow_deps)} dependencies are slow")
            recommendations.append("Consider implementing caching or alternative data sources")

        return recommendations

    def _check_dependency_cache(self, dependency_name: str) -> Optional[Dict[str, Any]]:
        """Check if dependency validation is cached"""
        cache_file = self.cache_path / f"{dependency_name}_validation.json"

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _is_cache_fresh(self, cached_result: Dict[str, Any],
                       dependency: DependencyRequirement) -> bool:
        """Check if cached validation result is still fresh"""
        try:
            cache_time = datetime.fromisoformat(cached_result.get("timestamp", ""))
            age = datetime.now() - cache_time

            # Different freshness requirements for different dependency types
            if dependency.type == "api":
                max_age = timedelta(minutes=15)
            elif dependency.type == "data_source":
                max_age = timedelta(hours=1)
            else:
                max_age = timedelta(hours=6)

            return age < max_age
        except Exception:
            return False

    def _cache_validation_result(self, dependency_name: str, result: ValidationResult):
        """Cache validation result for future use"""
        try:
            cache_file = self.cache_path / f"{dependency_name}_validation.json"

            cache_data = {
                "dependency_name": result.dependency_name,
                "available": result.available,
                "validation_score": result.validation_score,
                "fallback_used": result.fallback_used,
                "error_message": result.error_message,
                "timestamp": datetime.now().isoformat()
            }

            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)

        except Exception as e:
            self.logger.warning(f"Failed to cache validation result: {str(e)}")

    def _serialize_validation_result(self, result: ValidationResult) -> Dict[str, Any]:
        """Convert ValidationResult to serializable dictionary"""
        return {
            "dependency_name": result.dependency_name,
            "available": result.available,
            "validation_score": result.validation_score,
            "fallback_used": result.fallback_used,
            "error_message": result.error_message,
            "response_time": result.response_time
        }

    # Additional validation methods for specific services
    def _validate_github_api(self) -> ValidationResult:
        """Validate GitHub API availability"""
        try:
            # Basic validation without external requests for testing
            return ValidationResult(
                dependency_name="github_api",
                available=True,
                validation_score=0.8,
                error_message="Simulated validation - external requests disabled for testing"
            )
        except Exception as e:
            return ValidationResult(
                dependency_name="github_api",
                available=False,
                validation_score=0.0,
                error_message=f"GitHub API error: {str(e)}"
            )

    def _validate_generic_api(self, dependency: DependencyRequirement) -> ValidationResult:
        """Generic API validation method"""
        return ValidationResult(
            dependency_name=dependency.name,
            available=True,
            validation_score=0.7,
            error_message="Generic API validation - assumed available"
        )

    def _validate_service_dependency(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate service-based dependencies"""
        return ValidationResult(
            dependency_name=dependency.name,
            available=True,
            validation_score=0.8,
            error_message="Service validation not implemented - assumed available"
        )

    def _validate_market_data_source(self, dependency: DependencyRequirement) -> ValidationResult:
        """Validate market data source availability"""
        # This would integrate with existing Yahoo Finance service
        return self._validate_yahoo_finance_api()

if __name__ == "__main__":
    # CLI interface for testing
    import argparse

    parser = argparse.ArgumentParser(description="Universal Dependency Validator")
    parser.add_argument("command", help="Command name to validate dependencies for")
    parser.add_argument("--manifest", help="Path to dependency manifest file")

    args = parser.parse_args()

    validator = UniversalDependencyValidator()

    if args.manifest:
        with open(args.manifest, 'r') as f:
            manifest = yaml.safe_load(f)
    else:
        # Default test manifest
        manifest = {
            "dependencies": {
                "yahoo_finance_api": {
                    "type": "api",
                    "required": True,
                    "fallback_strategies": ["cached_data", "alternative_source"],
                    "validation_method": "api_test"
                }
            }
        }

    result = validator.validate_command_dependencies(args.command, manifest)
    print(json.dumps(result, indent=2))
