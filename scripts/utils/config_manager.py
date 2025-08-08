#!/usr/bin/env python3
"""
Configuration Manager for Macro-Economic Analysis

Centralized configuration loading and validation system that eliminates hardcoded values
throughout the macro-economic analysis pipeline. Provides fail-fast validation,
environment-specific overrides, and runtime configuration management.

Key Features:
- YAML configuration file loading with validation
- Environment-specific configuration overrides (dev/staging/prod)
- Fail-fast validation for required configuration values
- Runtime configuration value access with type checking
- Configuration caching and reload capabilities
- Market data parameter management
- Business logic threshold management

Usage:
    config = ConfigManager()
    fed_rate_fallback = config.get_market_data_fallback('fed_funds_rate', 5.25)
    min_services = config.get_business_logic_threshold('min_services_institutional', 4)
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails"""

    pass


class ConfigManager:
    """
    Centralized configuration management for macro-economic analysis

    Eliminates hardcoded values by providing structured access to configuration
    parameters with validation, environment overrides, and fail-fast behavior.
    """

    def __init__(self, config_path: Optional[str] = None, environment: str = "prod"):
        """
        Initialize configuration manager

        Args:
            config_path: Path to main configuration file (defaults to macro_analysis_config.yaml)
            environment: Environment name for configuration overrides (dev/staging/prod)
        """
        self.environment = environment
        self._config_cache = {}
        self._last_reload = None
        self._cache_ttl = timedelta(minutes=15)  # Configuration cache TTL

        # Determine configuration file path
        if config_path is None:
            # Default to macro_analysis_config.yaml in config directory
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "macro_analysis_config.yaml"

        self.config_path = Path(config_path)

        # Load and validate configuration
        self._load_configuration()
        self._validate_required_configuration()

        logger.info(f"ConfigManager initialized with environment: {environment}")

    def _load_configuration(self) -> None:
        """Load configuration from YAML file with error handling"""
        try:
            if not self.config_path.exists():
                raise ConfigurationError(
                    f"Configuration file not found: {self.config_path}"
                )

            with open(self.config_path, "r") as f:
                self._config_cache = yaml.safe_load(f)

            self._last_reload = datetime.now()
            logger.info(f"Configuration loaded from: {self.config_path}")

        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def _validate_required_configuration(self) -> None:
        """Validate required configuration sections exist with fail-fast behavior"""
        required_sections = [
            "confidence_thresholds",
            "data_validation",
            "business_cycle",
            "regional_analysis",
            "data_sources",
        ]

        missing_sections = []
        for section in required_sections:
            if section not in self._config_cache:
                missing_sections.append(section)

        if missing_sections:
            raise ConfigurationError(
                f"Required configuration sections missing: {missing_sections}"
            )

        # Validate critical subsections
        self._validate_confidence_thresholds()
        self._validate_data_sources()

        logger.info("Configuration validation passed")

    def _validate_confidence_thresholds(self) -> None:
        """Validate confidence threshold configuration"""
        thresholds = self._config_cache.get("confidence_thresholds", {})
        required_thresholds = [
            "discovery_minimum",
            "analysis_minimum",
            "synthesis_minimum",
            "institutional_grade",
        ]

        for threshold in required_thresholds:
            if threshold not in thresholds:
                raise ConfigurationError(f"Missing confidence threshold: {threshold}")

            value = thresholds[threshold]
            if not isinstance(value, (int, float)) or value < 0 or value > 1:
                raise ConfigurationError(
                    f"Invalid confidence threshold {threshold}: {value} (must be 0-1)"
                )

    def _validate_data_sources(self) -> None:
        """Validate data sources configuration"""
        sources = self._config_cache.get("data_sources", {})
        required_sources = ["fred", "imf", "alpha_vantage"]

        for source in required_sources:
            if source not in sources:
                raise ConfigurationError(f"Missing data source configuration: {source}")

            source_config = sources[source]
            if "reliability_score" not in source_config:
                raise ConfigurationError(
                    f"Missing reliability_score for source: {source}"
                )

    def reload_if_stale(self) -> bool:
        """Reload configuration if cache is stale"""
        if self._last_reload and datetime.now() - self._last_reload < self._cache_ttl:
            return False

        try:
            self._load_configuration()
            self._validate_required_configuration()
            return True
        except Exception as e:
            logger.warning(f"Failed to reload configuration: {e}")
            return False

    def get_confidence_threshold(self, threshold_type: str) -> float:
        """
        Get confidence threshold value

        Args:
            threshold_type: Type of threshold (discovery_minimum, institutional_grade, etc.)

        Returns:
            Confidence threshold value (0.0-1.0)

        Raises:
            ConfigurationError: If threshold type not found
        """
        self.reload_if_stale()

        thresholds = self._config_cache.get("confidence_thresholds", {})
        if threshold_type not in thresholds:
            raise ConfigurationError(
                f"Unknown confidence threshold type: {threshold_type}"
            )

        return float(thresholds[threshold_type])

    def get_data_validation_threshold(self, validation_type: str) -> Union[float, int]:
        """
        Get data validation threshold

        Args:
            validation_type: Type of validation threshold (economic_indicator_variance_threshold, etc.)

        Returns:
            Validation threshold value
        """
        self.reload_if_stale()

        validation = self._config_cache.get("data_validation", {})
        if validation_type not in validation:
            raise ConfigurationError(
                f"Unknown validation threshold type: {validation_type}"
            )

        return validation[validation_type]

    def get_business_cycle_parameter(self, parameter_name: str) -> Any:
        """
        Get business cycle modeling parameter

        Args:
            parameter_name: Parameter name (transition_probability_confidence, etc.)

        Returns:
            Parameter value
        """
        self.reload_if_stale()

        business_cycle = self._config_cache.get("business_cycle", {})
        if parameter_name not in business_cycle:
            raise ConfigurationError(
                f"Unknown business cycle parameter: {parameter_name}"
            )

        return business_cycle[parameter_name]

    def get_data_source_config(self, source_name: str) -> Dict[str, Any]:
        """
        Get complete data source configuration

        Args:
            source_name: Data source name (fred, imf, alpha_vantage, etc.)

        Returns:
            Data source configuration dictionary
        """
        self.reload_if_stale()

        sources = self._config_cache.get("data_sources", {})
        if source_name not in sources:
            raise ConfigurationError(f"Unknown data source: {source_name}")

        return sources[source_name].copy()

    def get_data_source_reliability(self, source_name: str) -> float:
        """
        Get data source reliability score

        Args:
            source_name: Data source name

        Returns:
            Reliability score (0.0-1.0)
        """
        source_config = self.get_data_source_config(source_name)
        return float(source_config.get("reliability_score", 0.5))

    def get_regional_indicators(self, region: str, indicator_type: str) -> List[str]:
        """
        Get regional economic indicators list

        Args:
            region: Region name (US, EU, ASIA, etc.)
            indicator_type: Indicator type (gdp_growth, employment, inflation, etc.)

        Returns:
            List of indicator codes
        """
        self.reload_if_stale()

        regional = self._config_cache.get("regional_analysis", {})
        indicators = regional.get("economic_indicators", {})

        if indicator_type not in indicators:
            raise ConfigurationError(f"Unknown indicator type: {indicator_type}")

        return indicators[indicator_type].copy()

    def get_quality_threshold(self, threshold_name: str) -> float:
        """
        Get quality assurance threshold

        Args:
            threshold_name: Threshold name (confidence_minimum, template_gap_coverage, etc.)

        Returns:
            Threshold value
        """
        self.reload_if_stale()

        qa = self._config_cache.get("quality_assurance", {})
        blocking = qa.get("blocking_thresholds", {})

        if threshold_name not in blocking:
            raise ConfigurationError(f"Unknown quality threshold: {threshold_name}")

        return float(blocking[threshold_name])

    def get_service_minimum_count(self) -> int:
        """
        Get minimum required service count for institutional analysis

        Returns:
            Minimum service count
        """
        # This is derived from data_sources configuration
        sources = self._config_cache.get("data_sources", {})
        # Count sources with priority 1-4 (critical sources)
        critical_sources = len(
            [s for s in sources.values() if s.get("priority", 10) <= 4]
        )
        return max(4, critical_sources)  # Minimum 4, or number of critical sources

    def get_market_data_fallback(
        self, data_type: str, default_value: Union[float, int, str] = None
    ) -> Any:
        """
        Get market data fallback values (replacing hardcoded values)

        This method will be extended to provide configurable fallbacks for market data
        when real-time sources are unavailable.

        Args:
            data_type: Type of market data (fed_funds_rate, balance_sheet_size, etc.)
            default_value: Default value if no configuration found

        Returns:
            Configured fallback value or default
        """
        self.reload_if_stale()

        # Check if market_data_fallbacks section exists in config
        market_data = self._config_cache.get("market_data_fallbacks", {})

        if data_type in market_data:
            return market_data[data_type]

        # Return default value with warning
        if default_value is not None:
            logger.warning(f"Using default fallback for {data_type}: {default_value}")
            return default_value

        raise ConfigurationError(
            f"No fallback configured for market data type: {data_type}"
        )

    def get_time_window(self, window_type: str) -> Union[int, str]:
        """
        Get time window configuration (replacing hardcoded time values)

        Args:
            window_type: Type of time window (economic_calendar_days, surprise_index_lookback, etc.)

        Returns:
            Time window value in appropriate units (int for days, str for timeframes like "1y", "2y")
        """
        self.reload_if_stale()

        # Check for time windows configuration
        time_windows = self._config_cache.get("time_windows", {})

        if window_type in time_windows:
            value = time_windows[window_type]
            # Return as-is for string timeframes, convert to int for day counts
            if isinstance(value, str):
                return value
            return int(value)

        # Fallback to sensible defaults with warning
        defaults = {
            "economic_calendar_days": 30,
            "surprise_index_lookback_days": 90,
            "fomc_advance_days": 15,
            "market_regime_duration_days": 45,
            "fed_rates_timeframe": "1y",
            "balance_sheet_timeframe": "2y",
            "m2_money_supply_timeframe": "2y",
        }

        if window_type in defaults:
            logger.warning(
                f"Using default time window for {window_type}: {defaults[window_type]}"
            )
            return defaults[window_type]

        raise ConfigurationError(f"Unknown time window type: {window_type}")

    def get_api_performance_threshold(self, metric_type: str) -> float:
        """
        Get API performance thresholds (replacing hardcoded performance values)

        Args:
            metric_type: Performance metric type (response_time_ms, success_rate, etc.)

        Returns:
            Performance threshold value
        """
        self.reload_if_stale()

        # Check for API performance configuration
        api_perf = self._config_cache.get("api_performance", {})

        if metric_type in api_perf:
            return float(api_perf[metric_type])

        # Return sensible defaults
        defaults = {
            "max_response_time_ms": 30000,
            "min_success_rate": 0.8,
            "min_data_freshness": 0.9,
            "health_score_threshold": 0.85,
        }

        if metric_type in defaults:
            return defaults[metric_type]

        raise ConfigurationError(f"Unknown API performance metric: {metric_type}")

    def validate_runtime_value(
        self, value: Any, value_type: str, valid_range: Optional[tuple] = None
    ) -> bool:
        """
        Validate runtime values against configuration constraints

        Args:
            value: Value to validate
            value_type: Type of value for validation context
            valid_range: Optional (min, max) range for numeric values

        Returns:
            True if value is valid

        Raises:
            ConfigurationError: If value is invalid
        """
        if value_type == "confidence_score":
            if not isinstance(value, (int, float)) or value < 0 or value > 1:
                raise ConfigurationError(
                    f"Invalid confidence score: {value} (must be 0-1)"
                )

        elif value_type == "service_count":
            min_services = self.get_service_minimum_count()
            if not isinstance(value, int) or value < min_services:
                raise ConfigurationError(
                    f"Invalid service count: {value} (minimum {min_services})"
                )

        elif value_type == "percentage":
            if not isinstance(value, (int, float)) or value < 0 or value > 100:
                raise ConfigurationError(f"Invalid percentage: {value} (must be 0-100)")

        elif value_type == "probability":
            if not isinstance(value, (int, float)) or value < 0 or value > 1:
                raise ConfigurationError(f"Invalid probability: {value} (must be 0-1)")

        if valid_range and isinstance(value, (int, float)):
            min_val, max_val = valid_range
            if value < min_val or value > max_val:
                raise ConfigurationError(
                    f"Value {value} out of range [{min_val}, {max_val}]"
                )

        return True

    def get_full_config(self) -> Dict[str, Any]:
        """
        Get complete configuration dictionary (for debugging/inspection)

        Returns:
            Complete configuration dictionary
        """
        self.reload_if_stale()
        return self._config_cache.copy()

    def get_environment_override(
        self, config_key: str, default_value: Any = None
    ) -> Any:
        """
        Get environment-specific configuration override

        Args:
            config_key: Configuration key to override
            default_value: Default value if no override found

        Returns:
            Override value or default
        """
        env_key = f"MACRO_CONFIG_{config_key.upper()}"
        env_value = os.getenv(env_key)

        if env_value is not None:
            logger.info(f"Using environment override for {config_key}: {env_value}")
            # Try to convert to appropriate type
            try:
                # Try float first
                if "." in env_value:
                    return float(env_value)
                # Try int
                return int(env_value)
            except ValueError:
                # Return as string
                return env_value

        return default_value

    def get_api_key(self, key_name: str) -> Optional[str]:
        """
        Get API key from environment variables or configuration

        Args:
            key_name: API key name (e.g., 'FRED_API_KEY', 'ALPHA_VANTAGE_API_KEY')

        Returns:
            API key value or None if not found
        """
        # First check environment variables
        env_value = os.getenv(key_name)
        if env_value and env_value.lower() not in ["none", "null", ""]:
            return env_value

        # Then check financial services configuration
        try:
            financial_services_path = (
                Path(__file__).parent.parent.parent
                / "config"
                / "services"
                / "financial_services.yaml"
            )
            if financial_services_path.exists():
                with open(financial_services_path, "r") as f:
                    financial_config = yaml.safe_load(f)

                # Map key names to service configurations
                service_mapping = {
                    "FRED_API_KEY": "fred",
                    "ALPHA_VANTAGE_API_KEY": "alpha_vantage",
                    "IMF_API_KEY": "imf",
                    "FMP_API_KEY": "fmp",
                    "EIA_API_KEY": "eia",
                    "COINGECKO_API_KEY": "coingecko",
                }

                service_name = service_mapping.get(key_name)
                if service_name and service_name in financial_config.get(
                    "services", {}
                ):
                    api_key = financial_config["services"][service_name].get("api_key")
                    # Handle services that don't require API keys
                    if api_key is None or str(api_key).lower() in ["none", "null"]:
                        # Return 'not_required' for services that don't need API keys
                        return "not_required"
                    elif api_key:
                        return str(api_key)
        except Exception as e:
            logger.warning(
                f"Could not load financial services config for {key_name}: {e}"
            )

        # Return None if not found anywhere
        return None

    def get_regional_volatility_parameters(self, region: str) -> Dict[str, Any]:
        """
        Get region-specific volatility parameters

        Args:
            region: Region name (US, AMERICAS, EUROPE, ASIA, etc.)

        Returns:
            Dictionary containing volatility parameters for the region

        Raises:
            ConfigurationError: If region not found or parameters missing
        """
        self.reload_if_stale()

        volatility_params = self._config_cache.get("regional_volatility_parameters", {})

        if region.upper() not in volatility_params:
            raise ConfigurationError(
                f"No volatility parameters configured for region: {region}"
            )

        params = volatility_params[region.upper()].copy()

        # Validate required parameters
        required_params = ["volatility_index", "long_term_mean", "reversion_speed"]
        missing_params = [p for p in required_params if p not in params]

        if missing_params:
            raise ConfigurationError(
                f"Missing volatility parameters for {region}: {missing_params}"
            )

        # Validate parameter types and ranges
        try:
            params["long_term_mean"] = float(params["long_term_mean"])
            params["reversion_speed"] = float(params["reversion_speed"])

            # Validate reasonable ranges
            if not (10.0 <= params["long_term_mean"] <= 50.0):
                raise ConfigurationError(
                    f"Invalid long_term_mean for {region}: {params['long_term_mean']} (should be 10-50)"
                )

            if not (0.05 <= params["reversion_speed"] <= 0.5):
                raise ConfigurationError(
                    f"Invalid reversion_speed for {region}: {params['reversion_speed']} (should be 0.05-0.5)"
                )

        except ValueError as e:
            raise ConfigurationError(
                f"Invalid volatility parameter types for {region}: {e}"
            )

        logger.debug(f"Retrieved volatility parameters for {region}: {params}")
        return params

    def get_volatility_parameter(
        self, region: str, parameter_name: str
    ) -> Union[float, str]:
        """
        Get specific volatility parameter for a region

        Args:
            region: Region name (US, AMERICAS, EUROPE, ASIA, etc.)
            parameter_name: Parameter name (long_term_mean, reversion_speed, volatility_index, etc.)

        Returns:
            Parameter value (float for numeric, str for names/descriptions)
        """
        params = self.get_regional_volatility_parameters(region)

        if parameter_name not in params:
            raise ConfigurationError(
                f"Unknown volatility parameter {parameter_name} for region {region}"
            )

        return params[parameter_name]

    def validate_cross_regional_volatility_uniqueness(
        self, tolerance: float = 0.02
    ) -> Dict[str, Any]:
        """
        Validate that volatility parameters are sufficiently different across regions
        to prevent template artifacts

        Args:
            tolerance: Minimum relative difference between regions (default 2%)

        Returns:
            Validation results with detected issues
        """
        self.reload_if_stale()

        volatility_params = self._config_cache.get("regional_volatility_parameters", {})
        validation_config = self._config_cache.get("regional_validation", {})
        template_detection = validation_config.get("template_artifact_detection", {})

        # Use configured tolerance or fallback to parameter
        configured_tolerance = template_detection.get(
            "volatility_parameter_variance_threshold", tolerance
        )

        validation_results = {
            "template_artifacts_detected": False,
            "warnings": [],
            "issues": [],
            "parameter_analysis": {},
        }

        # Get all regions with volatility parameters
        regions = list(volatility_params.keys())

        if len(regions) < 2:
            validation_results["warnings"].append(
                "Less than 2 regions configured - cannot validate uniqueness"
            )
            return validation_results

        # Check each numeric parameter for identical values across regions
        numeric_params = ["long_term_mean", "reversion_speed"]

        for param in numeric_params:
            values = []
            region_values = {}

            for region in regions:
                try:
                    value = float(volatility_params[region][param])
                    values.append(value)
                    region_values[region] = value
                except (KeyError, ValueError):
                    validation_results["warnings"].append(
                        f"Missing or invalid {param} for region {region}"
                    )
                    continue

            # Analyze parameter variance
            if len(values) >= 2:
                min_val = min(values)
                max_val = max(values)
                value_range = max_val - min_val
                relative_variance = value_range / max_val if max_val > 0 else 0

                validation_results["parameter_analysis"][param] = {
                    "min_value": min_val,
                    "max_value": max_val,
                    "range": value_range,
                    "relative_variance": relative_variance,
                    "region_values": region_values,
                }

                # Check for template artifacts (identical or nearly identical values)
                if relative_variance < configured_tolerance:
                    validation_results["template_artifacts_detected"] = True
                    validation_results["issues"].append(
                        {
                            "type": "template_artifact",
                            "parameter": param,
                            "issue": f"Parameter {param} has insufficient variance across regions ({relative_variance:.3f} < {configured_tolerance})",
                            "regions_affected": regions,
                            "values": region_values,
                        }
                    )

                # Check for exact duplicates
                duplicate_groups = {}
                for region, value in region_values.items():
                    if value not in duplicate_groups:
                        duplicate_groups[value] = []
                    duplicate_groups[value].append(region)

                for value, dup_regions in duplicate_groups.items():
                    if len(dup_regions) > 1:
                        validation_results["template_artifacts_detected"] = True
                        validation_results["issues"].append(
                            {
                                "type": "exact_duplicate",
                                "parameter": param,
                                "issue": f"Parameter {param} has identical values across multiple regions: {value}",
                                "regions_affected": dup_regions,
                                "duplicate_value": value,
                            }
                        )

        return validation_results

    def suggest_regional_volatility_adjustments(
        self, base_region: str = "US"
    ) -> Dict[str, Dict[str, float]]:
        """
        Suggest volatility parameter adjustments to eliminate template artifacts

        Args:
            base_region: Base region to use as reference (typically US/AMERICAS)

        Returns:
            Dictionary of suggested parameter adjustments by region
        """
        self.reload_if_stale()

        # Get current parameters
        volatility_params = self._config_cache.get("regional_volatility_parameters", {})

        # Historical volatility characteristics by region
        regional_adjustments = {
            "US": {"long_term_mean": 19.5, "reversion_speed": 0.15},
            "AMERICAS": {"long_term_mean": 19.5, "reversion_speed": 0.15},
            "EUROPE": {"long_term_mean": 22.3, "reversion_speed": 0.18},
            "ASIA": {"long_term_mean": 21.8, "reversion_speed": 0.12},
            "EMERGING_MARKETS": {"long_term_mean": 24.2, "reversion_speed": 0.20},
        }

        suggestions = {}

        for region in volatility_params.keys():
            if region in regional_adjustments:
                suggestions[region] = regional_adjustments[region]
            else:
                # For unknown regions, suggest values based on economic development level
                suggestions[region] = {
                    "long_term_mean": 22.0,  # Moderate default
                    "reversion_speed": 0.16,  # Moderate default
                    "note": "Default suggested values - should be calibrated to actual market characteristics",
                }

        return suggestions
