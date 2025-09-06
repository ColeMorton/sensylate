"""
CoinMetrics Service

Production-grade CoinMetrics institutional-grade cryptocurrency data integration with:
- Network data and on-chain metrics for Bitcoin and other cryptocurrencies
- Market data with institutional-grade quality standards
- Historical data with comprehensive coverage since genesis blocks
- Academic-rigor data validation and methodology transparency
- Free tier available with generous limits for Bitcoin analysis
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_financial_service import (
    BaseFinancialService,
    DataNotFoundError,
    ServiceConfig,
)

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from config_loader import ConfigLoader


class CoinMetricsService(BaseFinancialService):
    """
    CoinMetrics service extending BaseFinancialService

    Provides access to CoinMetrics' institutional-grade cryptocurrency data including:
    - Network data and on-chain metrics with academic rigor
    - Market data with institutional-grade quality standards
    - Historical data with comprehensive coverage
    - Bitcoin cycle analysis metrics (MVRV, NUPL, etc.)
    """

    def __init__(self, config: ServiceConfig):
        super().__init__(config)

        # CoinMetrics free tier available, API key optional but recommended
        if not self.config.base_url:
            self.config.base_url = "https://community-api.coinmetrics.io/v4"

        # Add API key to headers if provided
        if config.api_key:
            self.config.headers["api_key"] = config.api_key

    def _validate_response(
        self, data: Union[Dict[str, Any], List[Dict[str, Any]]], endpoint: str
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Validate CoinMetrics response data"""

        if not data:
            raise DataNotFoundError(f"No data returned from CoinMetrics {endpoint}")

        # CoinMetrics returns structured data with 'data' field
        if isinstance(data, dict) and "data" in data:
            return data["data"]

        return data

    def get_supported_assets(self) -> List[Dict[str, Any]]:
        """Get list of supported assets"""
        endpoint = "/catalog/assets"
        data = self._make_request_with_retry(endpoint)
        return self._validate_response(data, "supported assets")

    def get_available_metrics(self, asset: str = "btc") -> List[Dict[str, Any]]:
        """Get available metrics for an asset"""
        endpoint = f"/catalog/asset-metrics"
        params = {"assets": asset.lower()}
        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"metrics for {asset}")

    def get_network_data(
        self,
        asset: str = "btc",
        metrics: str = "AdrActCnt,BlkCnt,TxCnt,TxTfrValUSD",
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get network data for specified asset and metrics"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": asset.lower(),
            "metrics": metrics,
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"network data for {asset}")

    def get_market_data(
        self,
        asset: str = "btc",
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get market data for specified asset"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        endpoint = f"/timeseries/market-data"
        params = {
            "assets": asset.lower(),
            "metrics": "PriceUSD,VolTrusted24hUSD,CapMrktCurUSD",
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"market data for {asset}")

    def get_bitcoin_cycle_metrics(
        self, start_date: str = "2024-01-01", end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get Bitcoin cycle-specific metrics using Community API available metrics"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Bitcoin cycle analysis metrics (Community API compatible)
        cycle_metrics = [
            "PriceUSD",  # Bitcoin Price in USD
            "CapMrktCurUSD",  # Market Capitalization
            "TxCnt",  # Transaction Count
            "AdrActCnt",  # Active Addresses
            "TxTfrValUSD",  # Transfer Value in USD
            "BlkCnt",  # Block Count
        ]

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": "btc",
            "metrics": ",".join(cycle_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        try:
            data = self._make_request_with_retry(endpoint, params=params)
            return self._validate_response(data, "Bitcoin cycle metrics")
        except Exception as e:
            # If the full request fails, try with basic metrics only
            basic_metrics = ["PriceUSD", "CapMrktCurUSD", "TxCnt"]
            params["metrics"] = ",".join(basic_metrics)

            self.logger.warning(
                f"Full metrics request failed, trying with basic metrics: {basic_metrics}"
            )
            data = self._make_request_with_retry(endpoint, params=params)
            return self._validate_response(data, "Bitcoin basic cycle metrics")

    def get_supply_data(
        self,
        asset: str = "btc",
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get supply-related data for specified asset"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        supply_metrics = [
            "SplyCur",  # Current Supply
            "SplyAct1d",  # Active Supply 1d
            "SplyAct7d",  # Active Supply 7d
            "SplyAct30d",  # Active Supply 30d
            "SplyAct90d",  # Active Supply 90d
            "SplyAct1yr",  # Active Supply 1yr
        ]

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": asset.lower(),
            "metrics": ",".join(supply_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"supply data for {asset}")

    def get_mining_data(
        self,
        asset: str = "btc",
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get mining-related data (hash rate, difficulty, etc.)"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Bitcoin-specific mining metrics
        if asset.lower() == "btc":
            mining_metrics = [
                "HashRate",  # Hash Rate
                "DiffMean",  # Mining Difficulty
                "BlkCnt",  # Block Count
                "BlkSizeByte",  # Block Size
                "RevUSD",  # Revenue USD
                "FeeMeanUSD",  # Mean Fee USD
            ]
        else:
            mining_metrics = ["HashRate", "DiffMean", "BlkCnt"]

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": asset.lower(),
            "metrics": ",".join(mining_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"mining data for {asset}")

    def get_exchange_data(self, asset: str = "btc") -> List[Dict[str, Any]]:
        """Get exchange-related data and metrics"""
        endpoint = f"/catalog/exchanges"
        params = {"assets": asset.lower()}
        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"exchange data for {asset}")

    def get_institutional_data(self, asset: str = "btc") -> Dict[str, Any]:
        """Get institutional holdings and flow data"""
        # Note: Institutional data might be limited in free tier
        # This is a placeholder for institutional metrics

        institutional_metrics = [
            "SplyAct1yr",  # Long-term holdings proxy
            "TxTfrValUSD",  # Transfer value (institutional flows)
            "TxCnt",  # Transaction count
        ]

        # Get last 30 days of data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": asset.lower(),
            "metrics": ",".join(institutional_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"institutional data for {asset}")

    def get_realized_cap_data(
        self,
        asset: str = "btc",
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get realized capitalization data for Bitcoin cycle analysis"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Realized cap and related metrics for cycle analysis
        realized_cap_metrics = [
            "CapRealUSD",  # Realized Cap
            "CapMrktCurUSD",  # Market Cap
            "CapMVRVCur",  # MVRV Ratio
            "PriceUSD",  # Price USD
        ]

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": asset.lower(),
            "metrics": ",".join(realized_cap_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        data = self._make_request_with_retry(endpoint, params=params)
        return self._validate_response(data, f"realized cap data for {asset}")

    def get_mvrv_data(
        self,
        asset: str = "btc",
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get MVRV (Market Value to Realized Value) data for Bitcoin cycle analysis"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Get both market cap and realized cap for MVRV calculation
        mvrv_metrics = [
            "PriceUSD",  # Bitcoin Price in USD
            "CapMrktCurUSD",  # Market Cap (Market Value)
            "CapRealUSD",  # Realized Cap (Realized Value)
            "TxCnt",  # Transaction Count for context
        ]

        endpoint = f"/timeseries/asset-metrics"
        params = {
            "assets": asset.lower(),
            "metrics": ",".join(mvrv_metrics),
            "start_time": start_date,
            "end_time": end_date,
            "frequency": "1d",
        }

        try:
            data = self._make_request_with_retry(endpoint, params=params)
            validated_data = self._validate_response(data, f"MVRV data for {asset}")

            # Calculate MVRV and add analysis
            enhanced_data = []
            for item in validated_data:
                enhanced_item = item.copy()

                # Calculate MVRV ratio
                market_cap = float(item.get("CapMrktCurUSD", 0))
                realized_cap = float(item.get("CapRealUSD", 0))

                if realized_cap > 0:
                    mvrv_ratio = market_cap / realized_cap
                    enhanced_item["MVRV"] = round(mvrv_ratio, 4)
                    enhanced_item["mvrv_zone"] = self._classify_mvrv_zone(mvrv_ratio)
                    enhanced_item["market_signal"] = self._get_mvrv_signal(mvrv_ratio)

                enhanced_data.append(enhanced_item)

            return enhanced_data

        except Exception as e:
            self.logger.error(f"Failed to get MVRV data: {e}")
            return []

    def _classify_mvrv_zone(self, mvrv_value: float) -> str:
        """Classify MVRV value into market zones"""
        if mvrv_value <= 0.5:
            return "Deep Value Zone"
        elif mvrv_value <= 1.0:
            return "Accumulation Zone"
        elif mvrv_value <= 2.0:
            return "Normal Zone"
        elif mvrv_value <= 3.5:
            return "Euphoria Zone"
        else:
            return "Extreme Bubble Zone"

    def _get_mvrv_signal(self, mvrv_value: float) -> str:
        """Get trading signal based on MVRV value"""
        if mvrv_value <= 0.5:
            return "Strong Buy"
        elif mvrv_value <= 1.0:
            return "Buy"
        elif mvrv_value <= 2.0:
            return "Hold"
        elif mvrv_value <= 3.5:
            return "Consider Selling"
        else:
            return "Strong Sell"

    def get_mvrv_z_score_data(
        self,
        asset: str = "btc",
        start_date: str = "2020-01-01",
        end_date: Optional[str] = None,
        lookback_days: int = 1460,  # 4 years for statistical baseline
    ) -> Dict[str, Any]:
        """Get MVRV Z-Score analysis for Bitcoin cycle intelligence framework

        Returns comprehensive MVRV analysis including:
        - Current MVRV Z-Score
        - Historical percentile ranking
        - Schema-compliant zone classification
        - Statistical confidence metrics
        """
        from statistics import mean, stdev

        import numpy as np

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Calculate historical baseline start date
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        baseline_start = (end_dt - timedelta(days=lookback_days)).strftime("%Y-%m-%d")

        # Get historical MVRV data for statistical baseline
        self.logger.info(
            f"Collecting {lookback_days} days of historical MVRV data for Z-Score calculation"
        )
        historical_data = self.get_mvrv_data(asset, baseline_start, end_date)

        if len(historical_data) < 90:  # Need at least 90 days for basic statistics
            raise DataNotFoundError(
                f"Insufficient historical data for MVRV Z-Score calculation. Got {len(historical_data)} data points, need minimum 90"
            )

        # Extract MVRV ratios and calculate statistics
        mvrv_values = [item["MVRV"] for item in historical_data if "MVRV" in item]

        if not mvrv_values:
            raise DataNotFoundError("No valid MVRV data found for Z-Score calculation")

        # Calculate statistical metrics
        mvrv_mean = mean(mvrv_values)
        mvrv_std = stdev(mvrv_values) if len(mvrv_values) > 1 else 0
        current_mvrv = mvrv_values[-1]  # Most recent MVRV value

        # Calculate Z-Score
        if mvrv_std > 0:
            z_score = (current_mvrv - mvrv_mean) / mvrv_std
        else:
            z_score = 0.0

        # Calculate historical percentile
        mvrv_sorted = sorted(mvrv_values)
        percentile_rank = (
            sum(1 for x in mvrv_sorted if x <= current_mvrv) / len(mvrv_sorted)
        ) * 100

        # Get schema-compliant zone classification
        zone_classification = self._classify_mvrv_zone_schema_compliant(
            current_mvrv, z_score
        )

        # Calculate confidence based on data quality and statistical significance
        confidence = self._calculate_mvrv_confidence(
            len(mvrv_values), mvrv_std, abs(z_score)
        )

        return {
            "current_score": round(z_score, 4),
            "current_mvrv_ratio": round(current_mvrv, 4),
            "historical_percentile": round(percentile_rank, 2),
            "zone_classification": zone_classification,
            "statistical_metrics": {
                "mean": round(mvrv_mean, 4),
                "std_dev": round(mvrv_std, 4),
                "data_points": len(mvrv_values),
                "lookback_days": lookback_days,
            },
            "confidence": confidence,
            "analysis_date": end_date,
            "trend_analysis": self._analyze_mvrv_trend(
                mvrv_values[-30:] if len(mvrv_values) >= 30 else mvrv_values
            ),
        }

    def _classify_mvrv_zone_schema_compliant(
        self, mvrv_value: float, z_score: float
    ) -> str:
        """Classify MVRV into schema-compliant zone classifications for Bitcoin cycle intelligence

        Maps MVRV ratios and Z-Scores to schema zones:
        - deep_capitulation, capitulation, accumulation, neutral, euphoria, extreme_euphoria
        """
        # Use both MVRV ratio and Z-Score for more accurate classification
        if z_score <= -2.0 or mvrv_value <= 0.5:
            return "deep_capitulation"
        elif z_score <= -1.0 or mvrv_value <= 0.8:
            return "capitulation"
        elif z_score <= 0.0 or mvrv_value <= 1.2:
            return "accumulation"
        elif z_score <= 1.0 or mvrv_value <= 2.0:
            return "neutral"
        elif z_score <= 2.0 or mvrv_value <= 3.5:
            return "euphoria"
        else:
            return "extreme_euphoria"

    def _calculate_mvrv_confidence(
        self, data_points: int, std_dev: float, z_score_abs: float
    ) -> float:
        """Calculate confidence score for MVRV analysis based on data quality and statistical significance"""
        # Base confidence on data quantity
        data_confidence = min(
            data_points / 1460, 1.0
        )  # 4 years = max confidence from data quantity

        # Statistical reliability based on standard deviation and Z-score
        stat_confidence = min(std_dev * 0.5, 1.0) if std_dev > 0.1 else 0.5
        significance_confidence = (
            min(z_score_abs * 0.3, 1.0) if z_score_abs > 0.5 else 0.7
        )

        # Combined confidence (weighted average)
        confidence = (
            data_confidence * 0.4
            + stat_confidence * 0.3
            + significance_confidence * 0.3
        )
        return round(min(confidence, 1.0), 3)

    def _analyze_mvrv_trend(self, recent_mvrv_values: List[float]) -> Dict[str, Any]:
        """Analyze recent MVRV trend for cycle intelligence"""
        if len(recent_mvrv_values) < 2:
            return {"trend": "insufficient_data", "momentum": "neutral"}

        # Calculate trend direction
        first_half = recent_mvrv_values[: len(recent_mvrv_values) // 2]
        second_half = recent_mvrv_values[len(recent_mvrv_values) // 2 :]

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        trend_direction = "rising" if avg_second > avg_first else "falling"
        trend_strength = abs(avg_second - avg_first) / avg_first * 100

        # Determine momentum
        if trend_strength > 10:
            momentum = "strong"
        elif trend_strength > 5:
            momentum = "moderate"
        else:
            momentum = "weak"

        return {
            "trend": trend_direction,
            "momentum": momentum,
            "strength_percent": round(trend_strength, 2),
            "30_day_trend": f"{trend_direction} ({momentum})",
        }

    def get_enhanced_bitcoin_cycle_metrics(
        self, start_date: str = "2024-01-01", end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get enhanced Bitcoin cycle metrics including MVRV calculations"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Get MVRV data which includes comprehensive cycle metrics
        mvrv_data = self.get_mvrv_data("btc", start_date, end_date)

        if not mvrv_data:
            # Fallback to basic cycle metrics
            self.logger.warning(
                "MVRV data not available, falling back to basic cycle metrics"
            )
            return self.get_bitcoin_cycle_metrics(start_date, end_date)

        return mvrv_data


def create_coinmetrics_service(env: str = "dev") -> CoinMetricsService:
    """
    Factory function to create CoinMetricsService with environment-specific configuration

    Args:
        env: Environment name (dev/test/prod)

    Returns:
        Configured CoinMetricsService instance
    """
    try:
        # Load configuration
        config_loader = ConfigLoader()

        # Try to get API key from config (optional for free tier)
        api_key = None
        try:
            api_key = config_loader.get_api_key("coinmetrics", env)
        except:
            pass  # API key is optional for free tier

        # Create service config
        service_config = ServiceConfig(
            name="coinmetrics",
            api_key=api_key,
            base_url="https://community-api.coinmetrics.io/v4",
            timeout_seconds=30,
            max_retries=3,
        )

        return CoinMetricsService(service_config)

    except Exception as e:
        # Fallback configuration for free tier
        service_config = ServiceConfig(
            name="coinmetrics",
            api_key=None,  # Free tier
            base_url="https://community-api.coinmetrics.io/v4",
            timeout_seconds=30,
            max_retries=3,
        )

        return CoinMetricsService(service_config)
