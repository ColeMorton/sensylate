"""
Data Service Adapter Pattern

Provides a unified interface for different data services (CLI, API, file-based)
with standardized data fetching, caching, and incremental update capabilities.
Follows the adapter pattern to abstract service-specific implementations.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union

import pandas as pd

from errors import ProcessingError, ValidationError
from result_types import ProcessingResult


@dataclass
class DataFetchRequest:
    """Standardized data fetch request across all adapters"""

    symbol: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    period: Optional[str] = None  # e.g., "1y", "5d", "max"
    interval: str = "1d"  # e.g., "1d", "1h", "5m"
    incremental: bool = False
    force_refresh: bool = False
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class DataFetchResponse:
    """Standardized data fetch response across all adapters"""

    success: bool
    data: Optional[pd.DataFrame] = None
    error: Optional[str] = None
    fetch_time: Optional[datetime] = None
    row_count: int = 0
    cache_hit: bool = False
    incremental_rows: int = 0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        self.fetch_time = self.fetch_time or datetime.now()


class DataServiceProtocol(Protocol):
    """Protocol defining the interface all data service adapters must implement"""

    def fetch(self, request: DataFetchRequest) -> DataFetchResponse:
        """Fetch data based on standardized request"""
        ...

    def health_check(self) -> bool:
        """Check if service is available and healthy"""
        ...

    def get_capabilities(self) -> Dict[str, Any]:
        """Get service capabilities and metadata"""
        ...


class BaseDataServiceAdapter(ABC):
    """
    Base adapter class for all data services
    Provides common functionality for caching, incremental updates, and error handling
    """

    def __init__(self, service_name: str, cache_dir: Optional[Path] = None):
        self.service_name = service_name
        self.logger = logging.getLogger(f"data_adapter.{service_name}")
        self.cache_dir = cache_dir or Path("data/cache") / service_name
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def _fetch_raw_data(self, request: DataFetchRequest) -> pd.DataFrame:
        """Service-specific implementation to fetch raw data"""
        pass

    @abstractmethod
    def _validate_request(self, request: DataFetchRequest) -> None:
        """Validate request parameters for specific service"""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if service is available and healthy"""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get service capabilities and metadata"""
        pass

    def fetch(self, request: DataFetchRequest) -> DataFetchResponse:
        """
        Unified fetch method with caching and incremental support
        """
        try:
            # Validate request
            self._validate_request(request)

            # Check cache if not forcing refresh
            if not request.force_refresh:
                cached_data = self._load_from_cache(request)
                if cached_data is not None:
                    self.logger.info(f"Cache hit for {request.symbol}")
                    return DataFetchResponse(
                        success=True,
                        data=cached_data,
                        row_count=len(cached_data),
                        cache_hit=True,
                    )

            # Handle incremental fetch
            if request.incremental:
                response = self._fetch_incremental(request)
            else:
                # Fetch full data
                self.logger.info(f"Fetching full data for {request.symbol}")
                data = self._fetch_raw_data(request)
                response = DataFetchResponse(
                    success=True,
                    data=data,
                    row_count=len(data) if data is not None else 0,
                )

            # Cache successful response
            if response.success and response.data is not None:
                self._save_to_cache(request, response.data)

            return response

        except Exception as e:
            self.logger.error(f"Error fetching data for {request.symbol}: {e}")
            return DataFetchResponse(success=False, error=str(e))

    def _fetch_incremental(self, request: DataFetchRequest) -> DataFetchResponse:
        """Handle incremental data fetching"""
        # Load existing data
        existing_data = self._load_from_cache(request)

        if existing_data is None or existing_data.empty:
            # No existing data, fetch full
            self.logger.info(
                f"No existing data for {request.symbol}, fetching full dataset"
            )
            data = self._fetch_raw_data(request)
            return DataFetchResponse(
                success=True,
                data=data,
                row_count=len(data) if data is not None else 0,
                incremental_rows=len(data) if data is not None else 0,
            )

        # Determine incremental period
        last_date = pd.to_datetime(existing_data.index).max()
        days_old = (datetime.now() - last_date).days

        # Create incremental request
        incremental_request = DataFetchRequest(
            symbol=request.symbol,
            start_date=last_date - timedelta(days=1),  # Overlap by 1 day
            end_date=request.end_date,
            interval=request.interval,
            metadata=request.metadata,
        )

        self.logger.info(
            f"Fetching incremental data for {request.symbol} from {incremental_request.start_date}"
        )
        new_data = self._fetch_raw_data(incremental_request)

        if new_data is not None and not new_data.empty:
            # Merge with existing data
            merged_data = self._merge_data(existing_data, new_data)
            incremental_rows = len(merged_data) - len(existing_data)

            return DataFetchResponse(
                success=True,
                data=merged_data,
                row_count=len(merged_data),
                incremental_rows=incremental_rows,
            )
        else:
            # No new data
            return DataFetchResponse(
                success=True,
                data=existing_data,
                row_count=len(existing_data),
                incremental_rows=0,
            )

    def _merge_data(self, existing: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
        """Merge existing and new data, removing duplicates"""
        # Ensure both have datetime index
        if not isinstance(existing.index, pd.DatetimeIndex):
            existing.index = pd.to_datetime(existing.index)
        if not isinstance(new.index, pd.DatetimeIndex):
            new.index = pd.to_datetime(new.index)

        # Combine and remove duplicates, keeping newer data
        combined = pd.concat([existing, new])
        combined = combined[~combined.index.duplicated(keep="last")]
        combined = combined.sort_index()

        return combined

    def _get_cache_path(self, request: DataFetchRequest) -> Path:
        """Get cache file path for request"""
        return self.cache_dir / f"{request.symbol}_{request.interval}.parquet"

    def _load_from_cache(self, request: DataFetchRequest) -> Optional[pd.DataFrame]:
        """Load data from cache if available and fresh"""
        cache_path = self._get_cache_path(request)

        if not cache_path.exists():
            return None

        try:
            # Check cache age
            cache_age = datetime.now() - datetime.fromtimestamp(
                cache_path.stat().st_mtime
            )
            max_cache_age = timedelta(hours=24)  # Default 24 hour cache

            if cache_age > max_cache_age and not request.incremental:
                self.logger.info(f"Cache expired for {request.symbol}")
                return None

            # Load cached data
            data = pd.read_parquet(cache_path)
            return data

        except Exception as e:
            self.logger.warning(f"Error loading cache for {request.symbol}: {e}")
            return None

    def _save_to_cache(self, request: DataFetchRequest, data: pd.DataFrame) -> None:
        """Save data to cache"""
        try:
            cache_path = self._get_cache_path(request)
            data.to_parquet(cache_path)
            self.logger.debug(f"Saved {len(data)} rows to cache for {request.symbol}")
        except Exception as e:
            self.logger.warning(f"Error saving cache for {request.symbol}: {e}")


class YahooFinanceAdapter(BaseDataServiceAdapter):
    """Adapter for Yahoo Finance CLI service"""

    def __init__(self, cli_wrapper=None, cache_dir: Optional[Path] = None):
        super().__init__("yahoo_finance", cache_dir)

        # Initialize CLI wrapper if not provided
        if cli_wrapper is None:
            from cli_wrapper import CLIServiceWrapper

            self.cli = CLIServiceWrapper("yahoo_finance")
        else:
            self.cli = cli_wrapper

    def _validate_request(self, request: DataFetchRequest) -> None:
        """Validate Yahoo Finance specific request parameters"""
        if not request.symbol:
            raise ValidationError("Symbol is required for Yahoo Finance")

        # Validate period format if provided
        valid_periods = [
            "1d",
            "5d",
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
            "10y",
            "ytd",
            "max",
        ]
        if request.period and request.period not in valid_periods:
            raise ValidationError(
                f"Invalid period: {request.period}. Valid periods: {valid_periods}"
            )

    def _fetch_raw_data(self, request: DataFetchRequest) -> pd.DataFrame:
        """Fetch data from Yahoo Finance CLI"""
        # Build CLI arguments
        args = [request.symbol]

        if request.period:
            args.extend(["--period", request.period])
        elif request.start_date and request.end_date:
            args.extend(
                [
                    "--start",
                    request.start_date.strftime("%Y-%m-%d"),
                    "--end",
                    request.end_date.strftime("%Y-%m-%d"),
                ]
            )

        if request.interval != "1d":
            args.extend(["--interval", request.interval])

        # Execute CLI command using proper wrapper interface
        result = self.cli.execute_command("history", *args)

        if not result.success:
            raise ProcessingError(f"Yahoo Finance CLI failed: {result.error}")

        # Parse Yahoo Finance CLI output
        data_content = result.content or ""
        if not data_content:
            error_details = f"CLI success: {result.success}, content length: {len(result.content) if result.content else 0}"
            if result.metadata:
                error_details += f", metadata keys: {list(result.metadata.keys())}"
            raise ProcessingError(
                f"No data returned from Yahoo Finance. {error_details}"
            )

        df = self._parse_yahoo_data(data_content)

        if df is None or df.empty:
            raise ProcessingError("Failed to parse Yahoo Finance data")

        # Set date column as index if not already
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)
        elif not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
            df.index.name = "Date"

        return df

    def _parse_yahoo_data(self, data: str) -> pd.DataFrame:
        """Parse Yahoo Finance CLI output into DataFrame."""
        if not data.strip():
            return pd.DataFrame()

        # First try to extract JSON from formatted box output
        try:
            import json

            lines = data.split("\n")
            json_lines = []
            in_json_box = False

            for line in lines:
                # Look for the start of the JSON box (line with opening brace)
                if "│ {" in line:
                    in_json_box = True
                    # Extract the JSON content after the box character, removing trailing box chars
                    json_content = line.split("│ ", 1)[1].strip()
                    json_content = json_content.rstrip("│").strip()
                    json_lines.append(json_content)
                elif in_json_box and "│ }" in line:
                    # End of JSON box
                    json_content = line.split("│ ", 1)[1].strip()
                    json_content = json_content.rstrip("│").strip()
                    json_lines.append(json_content)
                    break
                elif in_json_box and line.startswith("│ "):
                    # Middle of JSON box - extract content after box character
                    json_content = line.split("│ ", 1)[1].strip()
                    json_content = json_content.rstrip("│").strip()
                    if json_content:  # Skip empty lines
                        json_lines.append(json_content)

            if json_lines:
                # Join the extracted JSON lines
                json_str = "\n".join(json_lines)
                self.logger.debug(f"Extracted JSON string: {json_str[:200]}...")

                try:
                    data_dict = json.loads(json_str)

                    # Convert JSON data to DataFrame
                    if "data" in data_dict and isinstance(data_dict["data"], list):
                        df = pd.DataFrame(data_dict["data"])
                        self.logger.info(
                            f"Successfully parsed JSON format with {len(df)} rows"
                        )
                        return df
                    else:
                        self.logger.warning("JSON parsed but no 'data' array found")

                except json.JSONDecodeError as json_err:
                    self.logger.warning(f"JSON decode failed: {json_err}")

        except (KeyError, ValueError, AttributeError, IndexError) as e:
            self.logger.warning(f"Failed to parse JSON format, trying CSV: {e}")

        # Fallback to CSV parsing
        try:
            import io

            df = pd.read_csv(io.StringIO(data))
            self.logger.info(f"Successfully parsed CSV format with {len(df)} rows")
        except pd.errors.ParserError as e:
            self.logger.error(f"Failed to parse Yahoo Finance data: {e}")
            # Try to extract CSV content if it's embedded in formatted output
            csv_lines = []
            for line in data.split("\n"):
                if (
                    "," in line
                    and not line.startswith("#")
                    and not "INFO" in line
                    and not "WARNING" in line
                ):
                    csv_lines.append(line.strip())

            if csv_lines:
                try:
                    df = pd.read_csv(io.StringIO("\n".join(csv_lines)))
                    self.logger.info(
                        f"Successfully parsed extracted CSV with {len(df)} rows"
                    )
                except Exception as inner_e:
                    self.logger.error(f"Failed to parse extracted CSV: {inner_e}")
                    return pd.DataFrame()
            else:
                return pd.DataFrame()

        return df

    def health_check(self) -> bool:
        """Check if Yahoo Finance service is available"""
        try:
            return self.cli.is_available()
        except Exception:
            return False

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Yahoo Finance capabilities"""
        return {
            "service_name": "yahoo_finance",
            "data_types": ["stocks", "etfs", "crypto", "forex"],
            "intervals": ["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"],
            "max_period": "max",
            "supports_incremental": True,
            "rate_limits": {"requests_per_minute": 60, "requests_per_hour": 2000},
        }


class AlphaVantageAdapter(BaseDataServiceAdapter):
    """Adapter for Alpha Vantage CLI service"""

    def __init__(self, cli_wrapper=None, cache_dir: Optional[Path] = None):
        super().__init__("alpha_vantage", cache_dir)

        # Initialize CLI wrapper if not provided
        if cli_wrapper is None:
            from cli_wrapper import CLIServiceWrapper

            self.cli = CLIServiceWrapper("alpha_vantage")
        else:
            self.cli = cli_wrapper

    def _validate_request(self, request: DataFetchRequest) -> None:
        """Validate Alpha Vantage specific request parameters"""
        if not request.symbol:
            raise ValidationError("Symbol is required for Alpha Vantage")

        # Alpha Vantage has different interval constraints
        valid_intervals = [
            "1min",
            "5min",
            "15min",
            "30min",
            "60min",
            "daily",
            "weekly",
            "monthly",
        ]
        interval_map = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
            "1h": "60min",
            "1d": "daily",
        }

        if request.interval not in interval_map:
            raise ValidationError(f"Invalid interval: {request.interval}")

    def _fetch_raw_data(self, request: DataFetchRequest) -> pd.DataFrame:
        """Fetch data from Alpha Vantage CLI"""
        # Map intervals
        interval_map = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
            "1h": "60min",
            "1d": "daily",
        }
        av_interval = interval_map.get(request.interval, "daily")

        # Build CLI arguments
        args = [request.symbol, "--function", f"TIME_SERIES_{av_interval.upper()}"]

        if av_interval == "daily" and request.period == "max":
            args[2] = "TIME_SERIES_DAILY_ADJUSTED"
            args.extend(["--outputsize", "full"])

        # Execute CLI command using proper wrapper interface
        result = self.cli.execute_command("timeseries", *args)

        if not result.success:
            raise ProcessingError(f"Alpha Vantage CLI failed: {result.error}")

        # Parse JSON response from result.content (not metadata)
        import json

        json_str = result.content or "{}"
        if not json_str or json_str.strip() == "":
            # Enhanced error message for debugging
            error_details = f"CLI success: {result.success}, content length: {len(result.content) if result.content else 0}"
            if result.metadata:
                error_details += f", metadata keys: {list(result.metadata.keys())}"
            raise ProcessingError(
                f"No JSON data returned from Alpha Vantage. {error_details}"
            )

        json_data = json.loads(json_str)

        # Extract time series data
        series_key = [k for k in json_data.keys() if "Time Series" in k][0]
        series_data = json_data[series_key]

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(series_data, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # Rename columns to match Yahoo Finance format
        column_map = {
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume",
        }
        df = df.rename(columns=column_map)

        return df

    def health_check(self) -> bool:
        """Check if Alpha Vantage service is available"""
        try:
            return self.cli.is_available()
        except Exception:
            return False

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Alpha Vantage capabilities"""
        return {
            "service_name": "alpha_vantage",
            "data_types": ["stocks", "forex", "crypto", "technical_indicators"],
            "intervals": [
                "1min",
                "5min",
                "15min",
                "30min",
                "60min",
                "daily",
                "weekly",
                "monthly",
            ],
            "max_period": "20+ years",
            "supports_incremental": True,
            "rate_limits": {"requests_per_minute": 5, "requests_per_day": 500},
        }


class FileBasedAdapter(BaseDataServiceAdapter):
    """Adapter for file-based data sources (CSV, Parquet, etc)"""

    def __init__(self, data_dir: Path, cache_dir: Optional[Path] = None):
        super().__init__("file_based", cache_dir)
        self.data_dir = Path(data_dir)

    def _validate_request(self, request: DataFetchRequest) -> None:
        """Validate file-based request parameters"""
        if not request.symbol:
            raise ValidationError("Symbol is required for file-based adapter")

    def _fetch_raw_data(self, request: DataFetchRequest) -> pd.DataFrame:
        """Load data from file system"""
        # Look for data file
        possible_files = [
            self.data_dir / f"{request.symbol}.csv",
            self.data_dir / f"{request.symbol}.parquet",
            self.data_dir / request.symbol / "daily.csv",
            self.data_dir / "stocks" / request.symbol / "daily.csv",
        ]

        for file_path in possible_files:
            if file_path.exists():
                self.logger.info(f"Loading data from {file_path}")

                if file_path.suffix == ".csv":
                    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
                elif file_path.suffix == ".parquet":
                    df = pd.read_parquet(file_path)
                else:
                    raise ProcessingError(
                        f"Unsupported file format: {file_path.suffix}"
                    )

                # Apply date filtering if requested
                if request.start_date:
                    df = df[df.index >= request.start_date]
                if request.end_date:
                    df = df[df.index <= request.end_date]

                return df

        raise ProcessingError(f"No data file found for symbol: {request.symbol}")

    def health_check(self) -> bool:
        """Check if data directory exists and is accessible"""
        return self.data_dir.exists() and self.data_dir.is_dir()

    def get_capabilities(self) -> Dict[str, Any]:
        """Get file-based adapter capabilities"""
        return {
            "service_name": "file_based",
            "data_types": ["any"],
            "intervals": ["depends on file"],
            "max_period": "depends on file",
            "supports_incremental": False,
            "rate_limits": None,
        }


class DataServiceAdapterFactory:
    """Factory for creating appropriate data service adapters"""

    _adapters: Dict[str, type] = {
        "yahoo_finance": YahooFinanceAdapter,
        "alpha_vantage": AlphaVantageAdapter,
        "file_based": FileBasedAdapter,
    }

    @classmethod
    def create_adapter(cls, service_name: str, **kwargs) -> BaseDataServiceAdapter:
        """Create appropriate adapter for service"""
        adapter_class = cls._adapters.get(service_name)

        if not adapter_class:
            raise ValidationError(f"Unknown data service: {service_name}")

        return adapter_class(**kwargs)

    @classmethod
    def register_adapter(cls, service_name: str, adapter_class: type) -> None:
        """Register new adapter type"""
        cls._adapters[service_name] = adapter_class

    @classmethod
    def get_available_services(cls) -> List[str]:
        """Get list of available services"""
        return list(cls._adapters.keys())
