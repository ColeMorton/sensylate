#!/usr/bin/env python3
"""
Comprehensive test suite for data service adapters

Tests the adapter pattern implementation including:
- YahooFinanceAdapter functionality and JSON parsing
- AlphaVantageAdapter functionality
- FileBasedAdapter functionality
- DataServiceAdapterFactory
- Error handling and edge cases
- Caching behavior
- Incremental data fetching
"""

import io
import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pandas as pd

# Test data and fixtures
from data_service_adapter import (
    AlphaVantageAdapter,
    BaseDataServiceAdapter,
    DataFetchRequest,
    DataFetchResponse,
    DataServiceAdapterFactory,
    FileBasedAdapter,
    YahooFinanceAdapter,
)
from errors import ProcessingError, ValidationError
from result_types import ProcessingResult


class TestDataFetchRequest(unittest.TestCase):
    """Test DataFetchRequest dataclass"""

    def test_basic_request(self):
        """Test basic request creation"""
        request = DataFetchRequest(symbol="AAPL", period="1y")
        self.assertEqual(request.symbol, "AAPL")
        self.assertEqual(request.period, "1y")
        self.assertEqual(request.interval, "1d")
        self.assertIsInstance(request.metadata, dict)

    def test_request_with_dates(self):
        """Test request with start/end dates"""
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)

        request = DataFetchRequest(
            symbol="MSFT", start_date=start_date, end_date=end_date
        )

        self.assertEqual(request.start_date, start_date)
        self.assertEqual(request.end_date, end_date)


class TestDataFetchResponse(unittest.TestCase):
    """Test DataFetchResponse dataclass"""

    def test_successful_response(self):
        """Test successful response creation"""
        df = pd.DataFrame({"A": [1, 2, 3]})
        response = DataFetchResponse(success=True, data=df, row_count=3)

        self.assertTrue(response.success)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.row_count, 3)
        self.assertIsInstance(response.fetch_time, datetime)

    def test_error_response(self):
        """Test error response creation"""
        response = DataFetchResponse(success=False, error="API rate limit exceeded")

        self.assertFalse(response.success)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, "API rate limit exceeded")


class TestYahooFinanceAdapter(unittest.TestCase):
    """Test YahooFinanceAdapter functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_cli = Mock()
        self.adapter = YahooFinanceAdapter(cli_wrapper=self.mock_cli)
        self.sample_json_output = """
2025-09-09 11:34:14,127 - financial_service.yahoo_finance - INFO - Historical data storage enabled
╭──────── Historical Data: AAPL (5d) ─────────╮
│ {                                           │
│   "symbol": "AAPL",                         │
│   "period": "5d",                           │
│   "interval": "1d",                         │
│   "data": [                                 │
│     {                                       │
│       "Date": "2025-09-02 00:00:00-04:00",  │
│       "Open": 229.25,                       │
│       "High": 230.85000610351562,           │
│       "Low": 226.97000122070312,            │
│       "Close": 229.72000122070312,          │
│       "Volume": 44075600,                   │
│       "Dividends": 0.0,                     │
│       "Stock Splits": 0.0                   │
│     },                                      │
│     {                                       │
│       "Date": "2025-09-03 00:00:00-04:00",  │
│       "Open": 237.2100067138672,            │
│       "High": 238.85000610351562,           │
│       "Low": 234.36000061035156,            │
│       "Close": 238.47000122070312,          │
│       "Volume": 66427800,                   │
│       "Dividends": 0.0,                     │
│       "Stock Splits": 0.0                   │
│     }                                       │
│   ],                                        │
│   "timestamp": "2025-09-09T10:00:28.536652" │
│ }                                           │
╰─────────────────────────────────────────────╯
"""

    def test_json_parsing_success(self):
        """Test successful JSON parsing from Yahoo Finance CLI output"""
        df = self.adapter._parse_yahoo_data(self.sample_json_output)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("Open", df.columns)
        self.assertIn("Close", df.columns)
        self.assertIn("Volume", df.columns)

        # Check data types
        self.assertTrue(pd.api.types.is_numeric_dtype(df["Open"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(df["Volume"]))

    def test_json_parsing_empty_data(self):
        """Test JSON parsing with empty data"""
        df = self.adapter._parse_yahoo_data("")
        self.assertTrue(df.empty)

    def test_json_parsing_malformed_json(self):
        """Test JSON parsing with malformed JSON falls back to CSV"""
        malformed_output = "Date,Open,Close\\n2023-01-01,100,105\\n"
        df = self.adapter._parse_yahoo_data(malformed_output)
        # Should fall back to CSV parsing or return empty DataFrame
        self.assertIsInstance(df, pd.DataFrame)

    def test_request_validation_success(self):
        """Test successful request validation"""
        request = DataFetchRequest(symbol="AAPL", period="1y")
        # Should not raise exception
        self.adapter._validate_request(request)

    def test_request_validation_no_symbol(self):
        """Test request validation fails without symbol"""
        request = DataFetchRequest(symbol="", period="1y")
        with self.assertRaises(ValidationError):
            self.adapter._validate_request(request)

    def test_request_validation_invalid_period(self):
        """Test request validation fails with invalid period"""
        request = DataFetchRequest(symbol="AAPL", period="invalid_period")
        with self.assertRaises(ValidationError):
            self.adapter._validate_request(request)

    def test_fetch_raw_data_success(self):
        """Test successful raw data fetching"""
        # Mock CLI response
        mock_result = ProcessingResult(
            success=True,
            operation="test_fetch",
            content=self.sample_json_output,
            metadata={},
        )
        self.mock_cli.execute_command.return_value = mock_result

        request = DataFetchRequest(symbol="AAPL", period="5d")
        df = self.adapter._fetch_raw_data(request)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.mock_cli.execute_command.assert_called_once()

    def test_fetch_raw_data_cli_failure(self):
        """Test handling of CLI failure"""
        # Mock CLI failure
        mock_result = ProcessingResult(
            success=False,
            operation="test_fetch_fail",
            error="API rate limit exceeded",
            content="",
            metadata={},
        )
        self.mock_cli.execute_command.return_value = mock_result

        request = DataFetchRequest(symbol="AAPL", period="5d")
        with self.assertRaises(ProcessingError):
            self.adapter._fetch_raw_data(request)

    def test_health_check(self):
        """Test health check functionality"""
        self.mock_cli.is_available.return_value = True
        self.assertTrue(self.adapter.health_check())

        self.mock_cli.is_available.return_value = False
        self.assertFalse(self.adapter.health_check())

    def test_get_capabilities(self):
        """Test capabilities reporting"""
        capabilities = self.adapter.get_capabilities()

        self.assertIn("service_name", capabilities)
        self.assertIn("data_types", capabilities)
        self.assertIn("intervals", capabilities)
        self.assertEqual(capabilities["service_name"], "yahoo_finance")
        self.assertIn("stocks", capabilities["data_types"])


class TestAlphaVantageAdapter(unittest.TestCase):
    """Test AlphaVantageAdapter functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_cli = Mock()
        self.adapter = AlphaVantageAdapter(cli_wrapper=self.mock_cli)
        self.sample_json_response = {
            "Meta Data": {"1. Information": "Daily Prices", "2. Symbol": "AAPL"},
            "Time Series (Daily)": {
                "2023-01-01": {
                    "1. open": "150.00",
                    "2. high": "155.00",
                    "3. low": "149.00",
                    "4. close": "154.00",
                    "5. volume": "1000000",
                },
                "2023-01-02": {
                    "1. open": "154.00",
                    "2. high": "156.00",
                    "3. low": "153.00",
                    "4. close": "155.50",
                    "5. volume": "1100000",
                },
            },
        }

    def test_request_validation_success(self):
        """Test successful request validation"""
        request = DataFetchRequest(symbol="AAPL", interval="1d")
        # Should not raise exception
        self.adapter._validate_request(request)

    def test_request_validation_invalid_interval(self):
        """Test request validation fails with invalid interval"""
        request = DataFetchRequest(symbol="AAPL", interval="invalid")
        with self.assertRaises(ValidationError):
            self.adapter._validate_request(request)

    def test_fetch_raw_data_success(self):
        """Test successful raw data fetching"""
        # Mock CLI response
        mock_result = ProcessingResult(
            success=True,
            operation="test_alpha_vantage_fetch",
            content=json.dumps(self.sample_json_response),
            metadata={},
        )
        self.mock_cli.execute_command.return_value = mock_result

        request = DataFetchRequest(symbol="AAPL", interval="1d")
        df = self.adapter._fetch_raw_data(request)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("Open", df.columns)
        self.assertIn("High", df.columns)
        self.assertIn("Low", df.columns)
        self.assertIn("Close", df.columns)
        self.assertIn("Volume", df.columns)

    def test_get_capabilities(self):
        """Test capabilities reporting"""
        capabilities = self.adapter.get_capabilities()

        self.assertEqual(capabilities["service_name"], "alpha_vantage")
        self.assertIn("stocks", capabilities["data_types"])
        self.assertIn("forex", capabilities["data_types"])


class TestFileBasedAdapter(unittest.TestCase):
    """Test FileBasedAdapter functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path("/tmp/test_data")
        self.temp_dir.mkdir(exist_ok=True)
        self.adapter = FileBasedAdapter(data_dir=self.temp_dir)

        # Create sample CSV file
        self.sample_csv_path = self.temp_dir / "AAPL.csv"
        sample_data = pd.DataFrame(
            {
                "Date": ["2023-01-01", "2023-01-02"],
                "Open": [150.0, 154.0],
                "Close": [154.0, 155.5],
                "Volume": [1000000, 1100000],
            }
        )
        sample_data.to_csv(self.sample_csv_path, index=False)

    def test_fetch_raw_data_csv_success(self):
        """Test successful CSV file loading"""
        request = DataFetchRequest(symbol="AAPL")
        df = self.adapter._fetch_raw_data(request)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("Open", df.columns)

    def test_fetch_raw_data_file_not_found(self):
        """Test handling of missing file"""
        request = DataFetchRequest(symbol="NONEXISTENT")
        with self.assertRaises(ProcessingError):
            self.adapter._fetch_raw_data(request)

    def test_health_check(self):
        """Test health check functionality"""
        self.assertTrue(self.adapter.health_check())

        # Test with non-existent directory
        bad_adapter = FileBasedAdapter(data_dir=Path("/nonexistent"))
        self.assertFalse(bad_adapter.health_check())

    def tearDown(self):
        """Clean up test files"""
        if self.sample_csv_path.exists():
            self.sample_csv_path.unlink()


class TestDataServiceAdapterFactory(unittest.TestCase):
    """Test DataServiceAdapterFactory functionality"""

    def test_create_yahoo_finance_adapter(self):
        """Test Yahoo Finance adapter creation"""
        adapter = DataServiceAdapterFactory.create_adapter("yahoo_finance")
        self.assertIsInstance(adapter, YahooFinanceAdapter)

    def test_create_alpha_vantage_adapter(self):
        """Test Alpha Vantage adapter creation"""
        adapter = DataServiceAdapterFactory.create_adapter("alpha_vantage")
        self.assertIsInstance(adapter, AlphaVantageAdapter)

    def test_create_file_based_adapter(self):
        """Test file-based adapter creation"""
        adapter = DataServiceAdapterFactory.create_adapter(
            "file_based", data_dir=Path("/tmp")
        )
        self.assertIsInstance(adapter, FileBasedAdapter)

    def test_create_unknown_adapter(self):
        """Test handling of unknown adapter type"""
        with self.assertRaises(ValidationError):
            DataServiceAdapterFactory.create_adapter("unknown_service")

    def test_register_new_adapter(self):
        """Test registering new adapter type"""

        class CustomAdapter(BaseDataServiceAdapter):
            def __init__(self, **kwargs):
                super().__init__("custom_service")

            def _fetch_raw_data(self, request):
                return pd.DataFrame()

            def _validate_request(self, request):
                pass

            def health_check(self):
                return True

            def get_capabilities(self):
                return {}

        DataServiceAdapterFactory.register_adapter("custom", CustomAdapter)
        adapter = DataServiceAdapterFactory.create_adapter("custom")
        self.assertIsInstance(adapter, CustomAdapter)

    def test_get_available_services(self):
        """Test getting list of available services"""
        services = DataServiceAdapterFactory.get_available_services()
        self.assertIn("yahoo_finance", services)
        self.assertIn("alpha_vantage", services)
        self.assertIn("file_based", services)


class TestBaseDataServiceAdapterIntegration(unittest.TestCase):
    """Integration tests for base adapter functionality"""

    def setUp(self):
        """Set up test fixtures"""

        # Create a minimal concrete adapter for testing
        class TestAdapter(BaseDataServiceAdapter):
            def __init__(self):
                import tempfile

                # Use temporary directory for clean cache testing
                temp_cache_dir = Path(tempfile.mkdtemp()) / "test_cache"
                super().__init__("test_service", cache_dir=temp_cache_dir)
                self.test_data = pd.DataFrame(
                    {
                        "Date": pd.date_range("2023-01-01", periods=5),
                        "Value": [1, 2, 3, 4, 5],
                    }
                )
                self.test_data.set_index("Date", inplace=True)

            def _fetch_raw_data(self, request):
                return self.test_data.copy()

            def _validate_request(self, request):
                if not request.symbol:
                    raise ValidationError("Symbol required")

            def health_check(self):
                return True

            def get_capabilities(self):
                return {"service_name": "test_service"}

        self.adapter = TestAdapter()

    def test_caching_behavior(self):
        """Test caching functionality"""
        request = DataFetchRequest(symbol="TEST")

        # First fetch - should fetch raw data
        response1 = self.adapter.fetch(request)
        self.assertTrue(response1.success)
        self.assertFalse(response1.cache_hit)

        # Second fetch - should hit cache
        response2 = self.adapter.fetch(request)
        self.assertTrue(response2.success)
        self.assertTrue(response2.cache_hit)

    def test_force_refresh(self):
        """Test force refresh bypasses cache"""
        request1 = DataFetchRequest(symbol="TEST")
        request2 = DataFetchRequest(symbol="TEST", force_refresh=True)

        # First fetch
        self.adapter.fetch(request1)

        # Force refresh should bypass cache
        response = self.adapter.fetch(request2)
        self.assertTrue(response.success)
        self.assertFalse(response.cache_hit)

    def test_error_handling(self):
        """Test error handling in fetch method"""
        # Test validation error
        request = DataFetchRequest(symbol="")  # Empty symbol
        response = self.adapter.fetch(request)
        self.assertFalse(response.success)
        self.assertIsNotNone(response.error)


if __name__ == "__main__":
    # Configure logging for tests
    import logging

    logging.basicConfig(level=logging.WARNING)

    # Run tests
    unittest.main(verbosity=2)
