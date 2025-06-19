#!/usr/bin/env python3
"""
Unit tests for YahooFinanceService

Tests cover validation, error handling, caching, and rate limiting functionality.
"""

import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import sys
import os

# Add scripts directory to path for importing the service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from yahoo_finance_service import (
    YahooFinanceService,
    YahooFinanceError,
    ValidationError,
    RateLimitError,
    DataNotFoundError,
    APITimeoutError,
    FileBasedCache,
    RateLimiter
)


class TestFileBasedCache(unittest.TestCase):
    """Test file-based cache functionality"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cache = FileBasedCache(cache_dir=self.temp_dir, ttl=1)

    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_cache_set_and_get(self):
        """Test basic cache set and get operations"""
        test_data = {"test": "data", "number": 123}
        self.cache.set("test_key", test_data)

        retrieved = self.cache.get("test_key")
        self.assertEqual(retrieved, test_data)

    def test_cache_expiry(self):
        """Test cache TTL expiration"""
        test_data = {"test": "data"}
        self.cache.set("test_key", test_data)

        # Data should be available immediately
        self.assertIsNotNone(self.cache.get("test_key"))

        # Wait for TTL to expire
        time.sleep(1.5)

        # Data should be expired
        self.assertIsNone(self.cache.get("test_key"))

    def test_cache_miss(self):
        """Test cache miss for non-existent key"""
        self.assertIsNone(self.cache.get("non_existent_key"))


class TestRateLimiter(unittest.TestCase):
    """Test rate limiting functionality"""

    def setUp(self):
        self.rate_limiter = RateLimiter(requests_per_minute=2)

    def test_rate_limiting(self):
        """Test rate limiting behavior"""
        # Should allow first two requests
        self.assertTrue(self.rate_limiter.can_make_request())
        self.rate_limiter.record_request()

        self.assertTrue(self.rate_limiter.can_make_request())
        self.rate_limiter.record_request()

        # Third request should be blocked
        self.assertFalse(self.rate_limiter.can_make_request())


class TestYahooFinanceService(unittest.TestCase):
    """Test YahooFinanceService functionality"""

    def setUp(self):
        # Create service with temp cache directory
        self.temp_dir = tempfile.mkdtemp()
        self.service = YahooFinanceService(cache_ttl=60, rate_limit=100)  # High rate limit for testing
        self.service.cache.cache_dir = Path(self.temp_dir)

    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_symbol_validation_success(self):
        """Test valid symbol normalization"""
        # Test uppercase conversion
        self.assertEqual(self.service._validate_symbol("aapl"), "AAPL")
        self.assertEqual(self.service._validate_symbol(" MSFT "), "MSFT")
        self.assertEqual(self.service._validate_symbol("BRK.B"), "BRK.B")

    def test_symbol_validation_failure(self):
        """Test invalid symbol rejection"""
        with self.assertRaises(ValidationError):
            self.service._validate_symbol("")

        with self.assertRaises(ValidationError):
            self.service._validate_symbol("INVALID@SYMBOL")

        with self.assertRaises(ValidationError):
            self.service._validate_symbol("TOOLONGSYMBOL")

    def test_period_validation_success(self):
        """Test valid period validation"""
        for period in ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']:
            self.assertEqual(self.service._validate_period(period), period)

    def test_period_validation_failure(self):
        """Test invalid period rejection"""
        with self.assertRaises(ValidationError):
            self.service._validate_period("invalid_period")

        with self.assertRaises(ValidationError):
            self.service._validate_period("3y")  # Not in valid list

    @patch('yahoo_finance_service.yf.Ticker')
    def test_get_stock_info_success(self, mock_ticker):
        """Test successful stock info retrieval"""
        # Mock yfinance response
        mock_instance = Mock()
        mock_instance.info = {
            'symbol': 'AAPL',
            'longName': 'Apple Inc.',
            'currentPrice': 150.0,
            'marketCap': 2500000000000,
            'trailingPE': 25.0
        }
        mock_ticker.return_value = mock_instance

        result = self.service.get_stock_info("AAPL")

        self.assertEqual(result['symbol'], 'AAPL')
        self.assertEqual(result['name'], 'Apple Inc.')
        self.assertEqual(result['current_price'], 150.0)
        self.assertIn('timestamp', result)

    @patch('yahoo_finance_service.yf.Ticker')
    def test_get_stock_info_not_found(self, mock_ticker):
        """Test stock info for invalid symbol"""
        # Mock empty response
        mock_instance = Mock()
        mock_instance.info = {}
        mock_ticker.return_value = mock_instance

        with self.assertRaises(DataNotFoundError):
            self.service.get_stock_info("INVALID")

    @patch('yahoo_finance_service.yf.Ticker')
    def test_get_historical_data_success(self, mock_ticker):
        """Test successful historical data retrieval"""
        # Mock yfinance response
        mock_instance = Mock()
        mock_df = Mock()
        mock_df.empty = False
        mock_df.to_dict.return_value = {'Date': ['2023-01-01'], 'Close': [150.0]}
        mock_instance.history.return_value = mock_df
        mock_ticker.return_value = mock_instance

        result = self.service.get_historical_data("AAPL", "1y")

        self.assertEqual(result['symbol'], 'AAPL')
        self.assertEqual(result['period'], '1y')
        self.assertIn('data', result)
        self.assertIn('timestamp', result)

    @patch('yahoo_finance_service.yf.Ticker')
    def test_get_historical_data_empty(self, mock_ticker):
        """Test historical data for invalid symbol/period"""
        # Mock empty response
        mock_instance = Mock()
        mock_df = Mock()
        mock_df.empty = True
        mock_instance.history.return_value = mock_df
        mock_ticker.return_value = mock_instance

        with self.assertRaises(DataNotFoundError):
            self.service.get_historical_data("INVALID", "1y")

    @patch('yahoo_finance_service.yf.Ticker')
    def test_get_financials_success(self, mock_ticker):
        """Test successful financials retrieval"""
        # Mock yfinance response
        mock_instance = Mock()
        mock_instance.info = {'symbol': 'AAPL'}
        mock_df = Mock()
        mock_df.empty = False
        mock_df.to_dict.return_value = {'Revenue': [100000000]}
        mock_instance.financials = mock_df
        mock_instance.balance_sheet = mock_df
        mock_instance.cashflow = mock_df
        mock_ticker.return_value = mock_instance

        result = self.service.get_financials("AAPL")

        self.assertEqual(result['symbol'], 'AAPL')
        self.assertIn('income_statement', result)
        self.assertIn('balance_sheet', result)
        self.assertIn('cash_flow', result)
        self.assertIn('timestamp', result)

    @patch('yahoo_finance_service.yf.Ticker')
    def test_caching_behavior(self, mock_ticker):
        """Test that results are properly cached"""
        # Mock yfinance response
        mock_instance = Mock()
        mock_instance.info = {
            'symbol': 'AAPL',
            'longName': 'Apple Inc.',
            'currentPrice': 150.0
        }
        mock_ticker.return_value = mock_instance

        # First call should hit the API
        result1 = self.service.get_stock_info("AAPL")
        self.assertEqual(mock_ticker.call_count, 1)

        # Second call should use cache
        result2 = self.service.get_stock_info("AAPL")
        self.assertEqual(mock_ticker.call_count, 1)  # Should not increase

        # Results should be identical
        self.assertEqual(result1, result2)

    @patch('yahoo_finance_service.yf.Ticker')
    def test_health_check(self, mock_ticker):
        """Test service health check"""
        # Mock successful response
        mock_instance = Mock()
        mock_instance.info = {
            'symbol': 'AAPL',
            'longName': 'Apple Inc.',
            'currentPrice': 150.0
        }
        mock_ticker.return_value = mock_instance

        health = self.service.health_check()

        self.assertEqual(health['status'], 'healthy')
        self.assertEqual(health['test_result'], 'success')
        self.assertIn('timestamp', health)

    @patch('yahoo_finance_service.yf.Ticker')
    def test_health_check_failure(self, mock_ticker):
        """Test service health check with API failure"""
        # Mock API failure
        mock_ticker.side_effect = Exception("API Error")

        health = self.service.health_check()

        self.assertEqual(health['status'], 'unhealthy')
        self.assertIn('error', health)
        self.assertIn('timestamp', health)


class TestCommandLineInterface(unittest.TestCase):
    """Test command line interface"""

    @patch('yahoo_finance_service.YahooFinanceService')
    def test_cli_info_command(self, mock_service_class):
        """Test CLI info command"""
        # Mock service instance
        mock_service = Mock()
        mock_service.get_stock_info.return_value = {'symbol': 'AAPL', 'name': 'Apple Inc.'}
        mock_service_class.return_value = mock_service

        # Test would require sys.argv mocking for full CLI test
        # This is a basic structure for CLI testing
        self.assertTrue(True)  # Placeholder


if __name__ == '__main__':
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromModule(sys.modules[__name__])

    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)
