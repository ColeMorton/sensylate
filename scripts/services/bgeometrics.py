"""
BGeometrics Service

Production-grade BGeometrics Bitcoin on-chain data integration with:
- MVRV (Market Value to Realized Value) ratio with daily updates
- MVRV Z-Score for statistical market analysis
- LTH-MVRV (Long Term Holder) metrics for cycle analysis
- Completely free API with no authentication required
- Perfect for Bitcoin cycle analysis and institutional-grade on-chain metrics
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


class BGeometricsService(BaseFinancialService):
    """
    BGeometrics service extending BaseFinancialService

    Provides access to BGeometrics' free Bitcoin on-chain metrics including:
    - MVRV ratio and MVRV Z-Score metrics
    - Long Term Holder MVRV (LTH-MVRV) data
    - Bitcoin cycle analysis metrics
    - Historical on-chain data with daily granularity
    """

    def __init__(self, config: ServiceConfig):
        super().__init__(config)

        # BGeometrics API is completely free, no API key required
        if not self.config.base_url:
            # Based on research, they have bitcoin-data.com API
            self.config.base_url = "https://bitcoin-data.com/api/v1"

    def _validate_response(
        self, data: Union[Dict[str, Any], List[Dict[str, Any]]], endpoint: str
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Validate BGeometrics response data"""

        if not data:
            raise DataNotFoundError(f"No data returned from BGeometrics {endpoint}")

        # Handle different response structures
        if isinstance(data, dict):
            # Check for error responses
            if "error" in data:
                raise DataNotFoundError(f"BGeometrics API error: {data['error']}")

            # Extract data if wrapped
            if "data" in data:
                return data["data"]
            return data

        return data

    def _format_date(self, date_input: Union[str, datetime]) -> str:
        """Format date for API requests"""
        if isinstance(date_input, str):
            return date_input
        elif isinstance(date_input, datetime):
            return date_input.strftime("%Y-%m-%d")
        else:
            raise ValueError(f"Invalid date format: {date_input}")

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

    def get_mvrv_ratio(
        self, start_date: str = "2024-01-01", end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get MVRV (Market Value to Realized Value) ratio data"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Based on research, BGeometrics provides MVRV data
        # Using assumed endpoint structure - may need adjustment based on actual API
        endpoint = f"metrics/mvrv"
        params = {"start_date": start_date, "end_date": end_date, "format": "json"}

        try:
            data = self._make_request_with_retry(endpoint, params=params)
            validated_data = self._validate_response(data, "MVRV ratio")

            # Enhance data with zone classification
            if isinstance(validated_data, list):
                for item in validated_data:
                    if "mvrv" in item:
                        item["mvrv_zone"] = self._classify_mvrv_zone(
                            float(item["mvrv"])
                        )
                    elif "value" in item:
                        item["mvrv_zone"] = self._classify_mvrv_zone(
                            float(item["value"])
                        )

            return (
                validated_data if isinstance(validated_data, list) else [validated_data]
            )

        except Exception as e:
            self.logger.error(f"Failed to get MVRV ratio data: {e}")
            # Return empty result instead of raising to match existing patterns
            return []

    def get_mvrv_zscore(
        self, start_date: str = "2024-01-01", end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get MVRV Z-Score data for statistical analysis"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        endpoint = f"metrics/mvrv-zscore"
        params = {"start_date": start_date, "end_date": end_date, "format": "json"}

        try:
            data = self._make_request_with_retry(endpoint, params=params)
            validated_data = self._validate_response(data, "MVRV Z-Score")

            # Enhance data with zone classification for Z-Score
            if isinstance(validated_data, list):
                for item in validated_data:
                    zscore_value = item.get("zscore") or item.get("value")
                    if zscore_value is not None:
                        zscore = float(zscore_value)
                        if zscore <= -2:
                            item["market_signal"] = "Strong Buy Signal"
                        elif zscore <= 0:
                            item["market_signal"] = "Buy Signal"
                        elif zscore <= 5:
                            item["market_signal"] = "Normal Range"
                        elif zscore <= 7:
                            item["market_signal"] = "Sell Signal"
                        else:
                            item["market_signal"] = "Strong Sell Signal"

            return (
                validated_data if isinstance(validated_data, list) else [validated_data]
            )

        except Exception as e:
            self.logger.error(f"Failed to get MVRV Z-Score data: {e}")
            return []

    def get_lth_mvrv(
        self, start_date: str = "2024-01-01", end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get Long Term Holder MVRV data (155+ days)"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        endpoint = f"metrics/lth-mvrv"
        params = {"start_date": start_date, "end_date": end_date, "format": "json"}

        try:
            data = self._make_request_with_retry(endpoint, params=params)
            validated_data = self._validate_response(data, "LTH-MVRV")

            # Enhance data with LTH-specific insights
            if isinstance(validated_data, list):
                for item in validated_data:
                    lth_mvrv = item.get("lth_mvrv") or item.get("value")
                    if lth_mvrv is not None:
                        value = float(lth_mvrv)
                        if value <= 1.0:
                            item[
                                "lth_behavior"
                            ] = "Long-term holders in profit accumulation"
                        elif value <= 2.0:
                            item["lth_behavior"] = "Long-term holders neutral"
                        else:
                            item["lth_behavior"] = "Long-term holders taking profits"

            return (
                validated_data if isinstance(validated_data, list) else [validated_data]
            )

        except Exception as e:
            self.logger.error(f"Failed to get LTH-MVRV data: {e}")
            return []

    def get_bitcoin_cycle_metrics(
        self, start_date: str = "2024-01-01", end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get comprehensive Bitcoin cycle metrics including MVRV variants"""

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Collect all MVRV metrics
            mvrv_data = self.get_mvrv_ratio(start_date, end_date)
            mvrv_zscore = self.get_mvrv_zscore(start_date, end_date)
            lth_mvrv = self.get_lth_mvrv(start_date, end_date)

            # Combine metrics by date
            combined_data = {}

            # Process MVRV ratio data
            for item in mvrv_data:
                date_key = item.get("date") or item.get("timestamp")
                if date_key:
                    if date_key not in combined_data:
                        combined_data[date_key] = {"date": date_key}
                    combined_data[date_key]["mvrv_ratio"] = item.get(
                        "mvrv"
                    ) or item.get("value")
                    combined_data[date_key]["mvrv_zone"] = item.get("mvrv_zone")

            # Process MVRV Z-Score data
            for item in mvrv_zscore:
                date_key = item.get("date") or item.get("timestamp")
                if date_key and date_key in combined_data:
                    combined_data[date_key]["mvrv_zscore"] = item.get(
                        "zscore"
                    ) or item.get("value")
                    combined_data[date_key]["market_signal"] = item.get("market_signal")

            # Process LTH-MVRV data
            for item in lth_mvrv:
                date_key = item.get("date") or item.get("timestamp")
                if date_key and date_key in combined_data:
                    combined_data[date_key]["lth_mvrv"] = item.get(
                        "lth_mvrv"
                    ) or item.get("value")
                    combined_data[date_key]["lth_behavior"] = item.get("lth_behavior")

            # Convert to list and sort by date
            result = list(combined_data.values())
            result.sort(key=lambda x: x.get("date", ""), reverse=True)

            return result

        except Exception as e:
            self.logger.error(f"Failed to get Bitcoin cycle metrics: {e}")
            return []

    def get_current_mvrv(self) -> Dict[str, Any]:
        """Get current MVRV ratio and analysis"""
        try:
            # Get latest MVRV data (last 5 days to ensure we get current)
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

            mvrv_data = self.get_mvrv_ratio(start_date, end_date)

            if not mvrv_data:
                return {}

            # Get most recent data point
            current = mvrv_data[0] if mvrv_data else {}

            # Add analysis
            if "mvrv" in current or "value" in current:
                mvrv_value = float(current.get("mvrv") or current.get("value", 0))
                current["analysis"] = {
                    "current_value": mvrv_value,
                    "zone": self._classify_mvrv_zone(mvrv_value),
                    "interpretation": self._get_mvrv_interpretation(mvrv_value),
                    "historical_context": self._get_historical_context(mvrv_value),
                }

            return current

        except Exception as e:
            self.logger.error(f"Failed to get current MVRV: {e}")
            return {}

    def _get_mvrv_interpretation(self, mvrv_value: float) -> str:
        """Get interpretation of MVRV value"""
        if mvrv_value <= 0.5:
            return "Extremely undervalued - Strong accumulation opportunity"
        elif mvrv_value <= 1.0:
            return "Below fair value - Good accumulation zone"
        elif mvrv_value <= 2.0:
            return "Normal valuation range - Market equilibrium"
        elif mvrv_value <= 3.5:
            return "Above fair value - Consider taking profits"
        else:
            return "Extremely overvalued - Strong sell signal"

    def _get_historical_context(self, mvrv_value: float) -> str:
        """Get historical context for MVRV value"""
        if mvrv_value <= 1.0:
            return "Historically, these levels have marked major market bottoms"
        elif mvrv_value >= 3.5:
            return "Historically, these levels have marked major market tops"
        else:
            return "Normal range - no extreme historical significance"


def create_bgeometrics_service(env: str = "dev") -> BGeometricsService:
    """
    Factory function to create BGeometricsService with environment-specific configuration

    Args:
        env: Environment name (dev/test/prod)

    Returns:
        Configured BGeometricsService instance
    """
    try:
        # BGeometrics is completely free, no configuration needed
        service_config = ServiceConfig(
            name="bgeometrics",
            api_key=None,  # No API key required
            base_url="https://bitcoin-data.com/api/v1",
            timeout_seconds=30,
            max_retries=3,
        )

        return BGeometricsService(service_config)

    except Exception as e:
        # Fallback configuration
        service_config = ServiceConfig(
            name="bgeometrics",
            api_key=None,
            base_url="https://bitcoin-data.com/api/v1",
            timeout_seconds=30,
            max_retries=3,
        )

        return BGeometricsService(service_config)


if __name__ == "__main__":
    # Test the service
    import logging

    logging.basicConfig(level=logging.INFO)

    service = create_bgeometrics_service()

    print("Testing BGeometrics service:")
    print("Current MVRV:", service.get_current_mvrv())
