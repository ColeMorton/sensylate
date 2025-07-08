"""
Yahoo Finance Service

Production-grade Yahoo Finance data integration with:
- Stock quotes and historical data
- Company fundamentals and financial statements
- Comprehensive error handling and validation
- Caching and rate limiting
- Integration with existing yahoo_finance_service.py
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add scripts directory to path for importing existing service
sys.path.insert(0, str(Path(__file__).parent.parent))

from yahoo_finance_service import DataNotFoundError as YFDataNotFoundError
from yahoo_finance_service import ValidationError as YFValidationError
from yahoo_finance_service import YahooFinanceError, YahooFinanceService

from .base_financial_service import (
    BaseFinancialService,
    DataNotFoundError,
    FinancialServiceError,
    ServiceConfig,
    ValidationError,
)

sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
from config_loader import ConfigLoader


class YahooFinanceAPIService(BaseFinancialService):
    """
    Yahoo Finance service extending BaseFinancialService

    Integrates with existing YahooFinanceService implementation
    while providing standardized interface and enhanced functionality.
    """

    def __init__(self, config: ServiceConfig):
        super().__init__(config)

        # Initialize the underlying Yahoo Finance service
        self.yf_service = YahooFinanceService(
            cache_ttl=config.cache.ttl_seconds,
            rate_limit=config.rate_limit.requests_per_minute,
        )

    def _validate_response(self, data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """Validate Yahoo Finance response data"""

        if not isinstance(data, dict):
            raise ValidationError(f"Invalid response format for {endpoint}")

        # Check for error indicators
        if "error" in data:
            raise ValidationError(f"API error: {data['error']}")

        # Endpoint-specific validation
        if endpoint.startswith("stock_info"):
            if "symbol" not in data:
                raise ValidationError("Missing symbol in stock info response")

        elif endpoint.startswith("historical"):
            if "data" not in data or not isinstance(data["data"], list):
                raise ValidationError("Missing or invalid historical data")

        elif endpoint.startswith("financials"):
            if "symbol" not in data:
                raise ValidationError("Missing symbol in financials response")

        # Add timestamp if not present
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()

        return data

    def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get comprehensive stock information

        Args:
            ticker: Stock symbol (e.g., 'AAPL', 'MSFT')

        Returns:
            Dictionary containing comprehensive stock data
        """
        try:
            # Use the existing service for the actual API call
            result = self.yf_service.get_stock_info(ticker)
            return self._validate_response(result, f"stock_info_{ticker}")

        except YFValidationError as e:
            raise ValidationError(str(e))
        except YFDataNotFoundError as e:
            raise DataNotFoundError(str(e))
        except YahooFinanceError as e:
            raise FinancialServiceError(str(e))

    def get_historical_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Get historical price data

        Args:
            ticker: Stock symbol
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')

        Returns:
            Dictionary containing historical price data
        """
        try:
            result = self.yf_service.get_historical_data(ticker, period)
            return self._validate_response(result, f"historical_{ticker}_{period}")

        except YFValidationError as e:
            raise ValidationError(str(e))
        except YFDataNotFoundError as e:
            raise DataNotFoundError(str(e))
        except YahooFinanceError as e:
            raise FinancialServiceError(str(e))

    def get_financial_statements(self, ticker: str) -> Dict[str, Any]:
        """
        Get financial statements

        Args:
            ticker: Stock symbol

        Returns:
            Dictionary containing financial statements
        """
        try:
            result = self.yf_service.get_financials(ticker)
            return self._validate_response(result, f"financials_{ticker}")

        except YFValidationError as e:
            raise ValidationError(str(e))
        except YFDataNotFoundError as e:
            raise DataNotFoundError(str(e))
        except YahooFinanceError as e:
            raise FinancialServiceError(str(e))

    def get_market_data_summary(
        self, ticker: str, period: str = "1y"
    ) -> Dict[str, Any]:
        """
        Get summarized market data optimized for analysis workflows

        Args:
            ticker: Stock symbol
            period: Time period

        Returns:
            Dictionary containing market performance summary
        """
        try:
            # Get historical data
            historical_result = self.yf_service.get_historical_data(ticker, period)

            if not historical_result.get("data"):
                raise DataNotFoundError(f"No historical data available for {ticker}")

            data = historical_result["data"]

            # Calculate summary statistics
            prices = [float(d["Close"]) for d in data if d.get("Close")]
            volumes = [int(d["Volume"]) for d in data if d.get("Volume")]

            if not prices:
                raise DataNotFoundError(f"No price data available for {ticker}")

            start_price = prices[0]
            end_price = prices[-1]
            high_price = max(prices)
            low_price = min(prices)
            avg_price = sum(prices) / len(prices)

            # Performance calculations
            total_return = (
                (end_price - start_price) / start_price if start_price != 0 else 0
            )
            price_volatility = (
                (max(prices) - min(prices)) / avg_price if avg_price != 0 else 0
            )

            # Volume statistics
            avg_volume = sum(volumes) / len(volumes) if volumes else 0
            total_volume = sum(volumes) if volumes else 0

            summary_result = {
                "ticker": ticker.upper(),
                "period": period,
                "data_points": len(data),
                "date_range": {
                    "start": data[0]["Date"] if data else None,
                    "end": data[-1]["Date"] if data else None,
                },
                "performance_summary": {
                    "start_price": round(start_price, 2),
                    "end_price": round(end_price, 2),
                    "high_price": round(high_price, 2),
                    "low_price": round(low_price, 2),
                    "average_price": round(avg_price, 2),
                    "total_return": round(total_return, 4),
                    "total_return_percent": round(total_return * 100, 2),
                    "price_volatility": round(price_volatility, 4),
                    "price_range": {
                        "absolute": round(high_price - low_price, 2),
                        "percent_of_avg": round(price_volatility * 100, 2),
                    },
                },
                "volume_summary": {
                    "average_volume": int(avg_volume),
                    "total_volume": int(total_volume),
                    "highest_volume": max(volumes) if volumes else 0,
                    "lowest_volume": min(volumes) if volumes else 0,
                },
                "analysis_ready": True,
                "data_quality": {
                    "source": "yahoo_finance",
                    "timestamp": datetime.now().isoformat(),
                    "period_requested": period,
                    "completeness": len([d for d in data if d.get("Close")]) / len(data)
                    if data
                    else 0,
                },
            }

            return self._validate_response(summary_result, f"summary_{ticker}_{period}")

        except YFValidationError as e:
            raise ValidationError(str(e))
        except YFDataNotFoundError as e:
            raise DataNotFoundError(str(e))
        except YahooFinanceError as e:
            raise FinancialServiceError(str(e))

    def health_check(self) -> Dict[str, Any]:
        """Service health check"""
        try:
            # Use the underlying service health check
            base_health = self.yf_service.health_check()

            # Enhance with service-specific information
            enhanced_health = {
                "service_name": self.config.name,
                "status": base_health.get("status", "unknown"),
                "underlying_service": base_health,
                "configuration": {
                    "cache_enabled": self.config.cache.enabled,
                    "rate_limit_enabled": self.config.rate_limit.enabled,
                    "requests_per_minute": self.config.rate_limit.requests_per_minute,
                    "cache_ttl_seconds": self.config.cache.ttl_seconds,
                },
                "capabilities": [
                    "Stock quotes and fundamentals",
                    "Historical price data",
                    "Financial statements",
                    "Market data summaries",
                    "Production-grade caching",
                    "Rate limiting",
                ],
                "timestamp": datetime.now().isoformat(),
            }

            return enhanced_health

        except Exception as e:
            return {
                "service_name": self.config.name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def cleanup_cache(self) -> None:
        """Clean up expired cache entries"""
        super().cleanup_cache()
        # Also cleanup the underlying service cache
        if hasattr(self.yf_service, "cache"):
            self.yf_service.cache.cleanup_expired()

    def clear_cache(self) -> None:
        """Clear all cached data"""
        super().clear_cache()
        # Also clear the underlying service cache
        if hasattr(self.yf_service, "cache"):
            self.yf_service.cache.clear()


def create_yahoo_finance_service(env: str = "dev") -> YahooFinanceAPIService:
    """
    Factory function to create Yahoo Finance service with configuration

    Args:
        env: Environment name (dev/test/prod)

    Returns:
        Configured Yahoo Finance service instance
    """
    # Use absolute path to config directory
    config_dir = Path(__file__).parent.parent.parent / "config"
    config_loader = ConfigLoader(str(config_dir))
    service_config = config_loader.get_service_config("yahoo_finance", env)

    # Convert to ServiceConfig format
    from .base_financial_service import CacheConfig, RateLimitConfig, ServiceConfig

    config = ServiceConfig(
        name=service_config.name,
        base_url=service_config.base_url,
        api_key=service_config.api_key,
        timeout_seconds=service_config.timeout_seconds,
        max_retries=service_config.max_retries,
        cache=CacheConfig(**service_config.cache),
        rate_limit=RateLimitConfig(**service_config.rate_limit),
        headers=service_config.headers,
    )

    return YahooFinanceAPIService(config)
