#!/usr/bin/env python3
"""
Data Fetch Coordinator

High-performance data fetching coordination system that:
- Orchestrates parallel data fetching across multiple services (Yahoo Finance, Alpha Vantage)
- Implements smart caching and incremental data strategies
- Manages service error categorization and resilient data operations
- Generates chart-ready data with portfolio and trading analytics
"""

import concurrent.futures
import logging
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pandas as pd
import yfinance as yf

from data_contract_discovery import DataContract
from file_operation_manager import FileOperationManager
from result_types import ProcessingResult


class DataFetchCoordinator:
    """Coordinates parallel data fetching and chart data generation"""

    def __init__(
        self,
        project_root: Path,
        frontend_data_dir: Path,
        scripts_dir: Path,
        cli_service: Any,
        chart_status_manager: Any,
        file_operation_manager: FileOperationManager,
        discovered_contracts: List[DataContract],
        cli_service_capabilities: Dict[str, Any],
    ):
        self.project_root = project_root
        self.frontend_data_dir = frontend_data_dir
        self.scripts_dir = scripts_dir
        self.cli_service = cli_service
        self.chart_status_manager = chart_status_manager
        self.file_operation_manager = file_operation_manager
        self.discovered_contracts = discovered_contracts
        self.cli_service_capabilities = cli_service_capabilities
        self.logger = logging.getLogger("data_fetch_coordinator")

    def fetch_yahoo_finance_data(self) -> ProcessingResult:
        """Fetch historical price data from Yahoo Finance for all discovered symbols using parallel processing"""
        try:
            # Extract symbols dynamically from discovered contracts
            symbols = self._extract_symbols_from_contracts()

            # Analyze refresh strategy for all symbols
            refresh_analysis = {}
            for symbol in symbols:
                freshness_info = self._get_data_freshness_info(symbol)
                refresh_analysis[symbol] = freshness_info

            # Count refresh strategies
            fresh_count = sum(
                1 for info in refresh_analysis.values() if not info["needs_update"]
            )
            incremental_count = sum(
                1
                for info in refresh_analysis.values()
                if info["needs_update"] and not info["needs_full_refresh"]
            )
            full_refresh_count = sum(
                1 for info in refresh_analysis.values() if info["needs_full_refresh"]
            )

            self.logger.info(
                f"📊 Data refresh strategy analysis: {fresh_count} fresh, {incremental_count} incremental, {full_refresh_count} full refresh"
            )

            self.logger.info(
                f"Initiating intelligent parallel Yahoo Finance data fetch for {len(symbols)} symbols: {', '.join(symbols)}"
            )

            # Determine optimal concurrency level based on pipeline configuration
            # Check if any colocated charts specify maxConcurrency in their pipeline settings
            max_concurrent_from_config = self._get_max_concurrency_from_charts()
            default_max_concurrent = 3  # Conservative default to respect API limits

            max_concurrent_requests = min(
                len(symbols), max_concurrent_from_config or default_max_concurrent
            )

            self.logger.info(
                f"Using parallel processing with {max_concurrent_requests} concurrent requests "
                f"(config: {max_concurrent_from_config}, default: {default_max_concurrent})"
            )

            # Execute parallel data fetching
            successful_symbols = []
            failed_symbols = []

            # Record start time for parallel execution timing
            parallel_start_time = time.time()

            # Use ThreadPoolExecutor for parallel API calls
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_concurrent_requests
            ) as executor:
                # Submit all symbol fetch tasks
                future_to_symbol = {
                    executor.submit(self._fetch_single_symbol, symbol): symbol
                    for symbol in symbols
                }

                self.logger.info(
                    f"📡 Submitted {len(symbols)} parallel data fetch tasks"
                )

                # Process completed futures as they finish
                completed_count = 0
                for future in concurrent.futures.as_completed(future_to_symbol):
                    symbol, success, error = future.result()
                    completed_count += 1

                    if success:
                        successful_symbols.append(symbol)
                        self.logger.info(
                            f"✅ [{completed_count}/{len(symbols)}] {symbol} completed successfully"
                        )
                    else:
                        failed_symbols.append(symbol)
                        self.logger.warning(
                            f"❌ [{completed_count}/{len(symbols)}] {symbol} failed: {error}"
                        )

            parallel_duration = time.time() - parallel_start_time

            # Calculate time savings from incremental strategy
            estimated_full_sequential_time = sum(
                [24.5, 5.2, 6.8]
            )  # Historical baseline
            estimated_incremental_time = (
                fresh_count * 0 + incremental_count * 5 + full_refresh_count * 25
            )  # Rough estimates
            total_time_savings = max(
                0, estimated_full_sequential_time - parallel_duration
            )

            self.logger.info(
                f"🚀 Intelligent parallel execution completed in {parallel_duration:.2f}s"
            )
            self.logger.info(
                f"📈 Performance: {fresh_count} skipped, {incremental_count} incremental ({incremental_count * 5:.0f}s est), "
                f"{full_refresh_count} full refresh ({full_refresh_count * 25:.0f}s est)"
            )

            if total_time_savings > 0:
                self.logger.info(
                    f"⚡ Time saved: {total_time_savings:.1f}s vs baseline full refresh "
                    f"(efficiency: {((estimated_full_sequential_time - parallel_duration) / estimated_full_sequential_time * 100):.1f}%)"
                )

            # Return overall success only if majority of symbols succeeded (60% threshold)
            success_rate = len(successful_symbols) / len(symbols) if symbols else 0
            min_success_rate = 0.6  # Require 60% success rate
            overall_success = success_rate >= min_success_rate

            if overall_success:
                self.logger.info(
                    f"✅ Parallel Yahoo Finance historical data fetch completed successfully: "
                    f"{len(successful_symbols)}/{len(symbols)} symbols ({success_rate:.1%} success rate) "
                    f"in {parallel_duration:.2f}s"
                )

                # Note: Frontend data copy is now handled directly in _save_symbol_data_to_frontend
                # Legacy copy method disabled to prevent overwriting enhanced saves
                # self._copy_symbols_to_frontend(successful_symbols)
            else:
                self.logger.error(
                    f"Yahoo Finance historical data fetch failed: "
                    f"{len(successful_symbols)}/{len(symbols)} symbols ({success_rate:.1%} success rate, "
                    f"below {min_success_rate:.0%} threshold)"
                )

            return ProcessingResult(
                success=overall_success,
                operation="fetch_yahoo_finance_historical",
                error=f"Failed symbols: {failed_symbols}" if failed_symbols else None,
                metadata={
                    "successful_symbols": successful_symbols,
                    "failed_symbols": failed_symbols,
                    "total_symbols": len(symbols),
                },
            )
        except Exception as e:
            # This is an infrastructure/code error, not a service error
            error_msg = f"Infrastructure error in Yahoo Finance execution: {str(e)}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                operation="fetch_yahoo_finance",
                error=error_msg,
                error_category="infrastructure",
            )

    def fetch_alpha_vantage_data(self) -> ProcessingResult:
        """Fetch supplementary data from Alpha Vantage"""
        try:
            self.logger.info(
                "Initiating Alpha Vantage data fetch for technical analysis"
            )

            # Use existing Alpha Vantage CLI with valid command: analyze
            # Validate CLI contract before execution
            self._validate_cli_contract("alpha_vantage", "analyze")

            result = self.cli_service.execute(
                service_name="alpha_vantage",
                command="analyze",
                args=["SPY"],
                timeout=60,
            )

            if result.success:
                self.logger.info("Alpha Vantage data fetch completed successfully")
            else:
                # Categorize the error type for better debugging
                error_category = self._categorize_service_error(result.error)
                self.logger.warning(
                    f"Alpha Vantage data fetch failed: {error_category} - {result.error}"
                )

            return result
        except Exception as e:
            # This is an infrastructure/code error, not a service error
            error_msg = f"Infrastructure error in Alpha Vantage execution: {str(e)}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                operation="fetch_alpha_vantage",
                error=error_msg,
                error_category="infrastructure",
            )

    def fetch_live_signals_data(self) -> ProcessingResult:
        """Generate fresh live signals data"""
        try:
            # Run the live signals dashboard to generate latest data
            result = subprocess.run(
                [sys.executable, str(self.scripts_dir / "live_signals_dashboard.py")],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                return ProcessingResult(success=True, operation="fetch_live_signals")
            else:
                return ProcessingResult(
                    success=False,
                    operation="fetch_live_signals",
                    error=f"Live signals script failed: {result.stderr}",
                )
        except Exception as e:
            return ProcessingResult(
                success=False, operation="fetch_live_signals", error=str(e)
            )

    def fetch_trade_history_data(self) -> ProcessingResult:
        """Fetch fresh trade history data"""
        try:
            today = datetime.now().strftime("%Y%m%d")
            self.logger.info(f"Initiating trade history data fetch for date: {today}")

            # Validate CLI contract before execution
            self._validate_cli_contract("trade_history", "generate")

            result = self.cli_service.execute(
                service_name="trade_history",
                command="generate",
                args=[today],
                timeout=180,
            )

            if result.success:
                self.logger.info("Trade history data fetch completed successfully")
            else:
                # Categorize the error type for better debugging
                error_category = self._categorize_service_error(result.error)
                self.logger.warning(
                    f"Trade history data fetch failed: {error_category} - {result.error}"
                )

            # Generate chart-ready data files regardless of image generation success
            # Chart data only needs the CSV data, not the theme-dependent images
            chart_result = self._generate_chart_ready_data()
            if not chart_result.success:
                self.logger.warning(
                    f"Chart data generation failed: {chart_result.error}"
                )
            else:
                self.logger.info("Chart data generation completed successfully")

            return result
        except Exception as e:
            # This is an infrastructure/code error, not a service error
            error_msg = f"Infrastructure error in trade history execution: {str(e)}"
            self.logger.error(error_msg)
            return ProcessingResult(
                success=False,
                operation="fetch_trade_history",
                error=error_msg,
                error_category="infrastructure",
            )

    def _extract_symbols_from_contracts(self) -> List[str]:
        """Extract unique stock symbols from discovered contracts"""
        symbols = set()

        for contract in self.discovered_contracts:
            # Extract symbol from contract ID or path structure
            if contract.category in ["stocks", "crypto"]:
                # For stock/crypto contracts, symbol should be in path: data/raw/stocks/{SYMBOL}/daily.csv
                try:
                    path_parts = contract.file_path.parts
                    if "stocks" in path_parts or "crypto" in path_parts:
                        symbol_index = (
                            list(path_parts).index("stocks") + 1
                            if "stocks" in path_parts
                            else list(path_parts).index("crypto") + 1
                        )
                        if symbol_index < len(path_parts):
                            symbol = path_parts[symbol_index]
                            symbols.add(symbol)
                            self.logger.debug(
                                f"Extracted symbol '{symbol}' from {contract.file_path}"
                            )
                except Exception as e:
                    self.logger.debug(
                        f"Could not extract symbol from contract path {contract.file_path}: {e}"
                    )

        symbols_list = list(symbols)
        self.logger.info(
            f"Discovered {len(symbols_list)} unique symbols: {symbols_list}"
        )

        return symbols_list

    def _get_data_freshness_info(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive freshness analysis for a symbol to determine refresh strategy"""
        try:
            # Define file paths
            frontend_file = (
                self.frontend_data_dir / "raw" / "stocks" / symbol / "daily.csv"
            )

            # Check if data file exists
            if not frontend_file.exists():
                self.logger.debug(
                    f"No existing data file for {symbol}, needs full refresh"
                )
                return {
                    "needs_update": True,
                    "needs_full_refresh": True,
                    "reason": "no_existing_data",
                    "last_date": None,
                    "days_since_update": float("inf"),
                }

            # Check file size
            file_size = frontend_file.stat().st_size
            if file_size <= 100:  # Very small files likely corrupted or empty
                self.logger.debug(
                    f"Data file for {symbol} is too small ({file_size} bytes), needs full refresh"
                )
                return {
                    "needs_update": True,
                    "needs_full_refresh": True,
                    "reason": "corrupted_file",
                    "last_date": None,
                    "days_since_update": float("inf"),
                }

            # Load and analyze existing data
            try:
                df = pd.read_csv(frontend_file)
                if df.empty:
                    self.logger.debug(
                        f"Data file for {symbol} is empty, needs full refresh"
                    )
                    return {
                        "needs_update": True,
                        "needs_full_refresh": True,
                        "reason": "empty_dataframe",
                        "last_date": None,
                        "days_since_update": float("inf"),
                    }

                # Get the most recent date in the data
                last_date_str = df["date"].iloc[-1] if "date" in df.columns else None
                if not last_date_str:
                    self.logger.debug(
                        f"No date column in {symbol} data, needs full refresh"
                    )
                    return {
                        "needs_update": True,
                        "needs_full_refresh": True,
                        "reason": "no_date_column",
                        "last_date": None,
                        "days_since_update": float("inf"),
                    }

                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                days_since_update = (datetime.now() - last_date).days

                # Get freshness threshold for this symbol
                freshness_threshold = self._get_freshness_threshold_for_symbol(symbol)

                self.logger.debug(
                    f"Symbol {symbol}: last_date={last_date_str}, days_since={days_since_update}, "
                    f"threshold={freshness_threshold}"
                )

                # Determine refresh strategy
                if days_since_update <= freshness_threshold:
                    # Data is fresh enough
                    return {
                        "needs_update": False,
                        "needs_full_refresh": False,
                        "reason": "data_fresh",
                        "last_date": last_date,
                        "days_since_update": days_since_update,
                    }
                elif (
                    days_since_update <= 30
                ):  # Within last 30 days - incremental update
                    return {
                        "needs_update": True,
                        "needs_full_refresh": False,
                        "reason": "incremental_update",
                        "last_date": last_date,
                        "days_since_update": days_since_update,
                    }
                else:  # More than 30 days old - full refresh
                    return {
                        "needs_update": True,
                        "needs_full_refresh": True,
                        "reason": "data_stale",
                        "last_date": last_date,
                        "days_since_update": days_since_update,
                    }

            except Exception as e:
                self.logger.debug(f"Error analyzing {symbol} data file: {e}")
                return {
                    "needs_update": True,
                    "needs_full_refresh": True,
                    "reason": "analysis_error",
                    "last_date": None,
                    "days_since_update": float("inf"),
                }

        except Exception as e:
            self.logger.debug(f"Error getting freshness info for {symbol}: {e}")
            return {
                "needs_update": True,
                "needs_full_refresh": True,
                "reason": "error",
                "last_date": None,
                "days_since_update": float("inf"),
            }

    def _get_freshness_threshold_for_symbol(self, symbol: str) -> float:
        """Get the freshness threshold (in days) for a given symbol based on its characteristics"""
        # Default freshness thresholds
        default_threshold = 1.0  # 1 day for most symbols

        # Crypto symbols (24/7 markets) should have tighter freshness requirements
        crypto_symbols = {"BTC-USD", "ETH-USD", "DOGE-USD"}
        if symbol in crypto_symbols:
            return 0.5  # 12 hours for crypto

        # Major indices and ETFs - daily updates sufficient
        major_indices = {"SPY", "QQQ", "IWM", "VTI", "AAPL", "MSFT", "GOOGL", "AMZN"}
        if symbol in major_indices:
            return 1.0  # 1 day

        # Less liquid assets can tolerate slightly staler data
        return default_threshold

    def _fetch_single_symbol(self, symbol: str) -> Tuple[str, bool, Optional[str]]:
        """Fetch data for a single symbol with intelligent refresh strategy"""
        try:
            self.logger.debug(f"Starting fetch for symbol: {symbol}")

            # Get freshness analysis
            freshness_info = self._get_data_freshness_info(symbol)

            # Skip if data is fresh
            if not freshness_info["needs_update"]:
                self.logger.info(
                    f"📊 {symbol}: Data is fresh (last updated {freshness_info['days_since_update']:.1f} days ago)"
                )
                return symbol, True, None

            # Determine fetch strategy
            if freshness_info["needs_full_refresh"]:
                self.logger.info(
                    f"🔄 {symbol}: Full refresh needed ({freshness_info['reason']})"
                )
                success, error = self._fetch_full_data(symbol)
            else:
                self.logger.info(
                    f"📈 {symbol}: Incremental update (last: {freshness_info['last_date'].strftime('%Y-%m-%d')})"
                )
                success, error = self._fetch_incremental_data(
                    symbol, freshness_info["last_date"]
                )

            if success:
                self.logger.debug(f"✅ Successfully fetched data for {symbol}")
            else:
                self.logger.error(f"❌ Failed to fetch data for {symbol}: {error}")

            return symbol, success, error

        except Exception as e:
            error_msg = f"Exception in fetch_single_symbol: {str(e)}"
            self.logger.error(error_msg)
            return symbol, False, error_msg

    def _fetch_full_data(self, symbol: str) -> Tuple[bool, Optional[str]]:
        """Fetch complete historical data for a symbol"""
        try:
            # Get 5 years of historical data (sufficient for most analysis)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=5 * 365)

            self.logger.debug(
                f"Fetching full data for {symbol} from {start_date.date()} to {end_date.date()}"
            )

            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(
                start=start_date, end=end_date, auto_adjust=True, back_adjust=True
            )

            if hist_data.empty:
                return False, f"No data returned for {symbol}"

            # Convert to our standard format
            hist_data = hist_data.reset_index()
            hist_data["Date"] = hist_data["Date"].dt.strftime("%Y-%m-%d")
            hist_data.columns = [
                col.lower().replace(" ", "_") for col in hist_data.columns
            ]

            # Rename columns to match frontend expectations
            hist_data = hist_data.rename(columns={"date": "date"})

            # Add required columns if missing
            if "dividends" not in hist_data.columns:
                hist_data["dividends"] = 0.0
            if "stock_splits" not in hist_data.columns:
                hist_data["stock_splits"] = 0.0

            # Reorder columns to match expected format
            column_order = [
                "open",
                "high",
                "low",
                "close",
                "volume",
                "dividends",
                "stock_splits",
                "date",
            ]
            hist_data = hist_data[column_order]

            # Save data to frontend location
            self._save_symbol_data_to_frontend(symbol, hist_data)

            self.logger.debug(
                f"Successfully saved {len(hist_data)} rows of full data for {symbol}"
            )
            return True, None

        except Exception as e:
            error_msg = f"Error fetching full data for {symbol}: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def _fetch_incremental_data(
        self, symbol: str, last_date: datetime
    ) -> Tuple[bool, Optional[str]]:
        """Fetch only new data since the last update"""
        try:
            # Fetch data from day after last_date to today
            start_date = last_date + timedelta(days=1)
            end_date = datetime.now()

            self.logger.debug(
                f"Fetching incremental data for {symbol} from {start_date.date()} to {end_date.date()}"
            )

            ticker = yf.Ticker(symbol)
            new_data = ticker.history(
                start=start_date, end=end_date, auto_adjust=True, back_adjust=True
            )

            if new_data.empty:
                self.logger.info(f"No new data available for {symbol}")
                return True, None  # Not an error, just no new data

            # Convert to our standard format
            new_data = new_data.reset_index()
            new_data["Date"] = new_data["Date"].dt.strftime("%Y-%m-%d")
            new_data.columns = [
                col.lower().replace(" ", "_") for col in new_data.columns
            ]
            new_data = new_data.rename(columns={"date": "date"})

            # Add required columns if missing
            if "dividends" not in new_data.columns:
                new_data["dividends"] = 0.0
            if "stock_splits" not in new_data.columns:
                new_data["stock_splits"] = 0.0

            # Reorder columns
            column_order = [
                "open",
                "high",
                "low",
                "close",
                "volume",
                "dividends",
                "stock_splits",
                "date",
            ]
            new_data = new_data[column_order]

            # Merge with existing data
            success = self._merge_incremental_data(symbol, new_data)

            if success:
                self.logger.debug(
                    f"Successfully merged {len(new_data)} rows of incremental data for {symbol}"
                )
                return True, None
            else:
                return False, f"Failed to merge incremental data for {symbol}"

        except Exception as e:
            error_msg = f"Error fetching incremental data for {symbol}: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def _merge_incremental_data(
        self, symbol: str, incremental_df: pd.DataFrame
    ) -> bool:
        """Merge new incremental data with existing data"""
        try:
            existing_data_path = (
                self.frontend_data_dir / "raw" / "stocks" / symbol / "daily.csv"
            )

            if not existing_data_path.exists():
                # No existing data, save the incremental data as new file
                self._save_symbol_data_to_frontend(symbol, incremental_df)
                return True

            # Load existing data
            existing_df = pd.read_csv(existing_data_path)

            # Ensure date columns are comparable
            existing_df["date"] = pd.to_datetime(existing_df["date"]).dt.strftime(
                "%Y-%m-%d"
            )
            incremental_df["date"] = pd.to_datetime(incremental_df["date"]).dt.strftime(
                "%Y-%m-%d"
            )

            # Remove any overlapping dates from incremental data (avoid duplicates)
            existing_dates = set(existing_df["date"])
            incremental_df = incremental_df[
                ~incremental_df["date"].isin(existing_dates)
            ]

            if not incremental_df.empty:
                # Combine the dataframes
                combined_df = pd.concat(
                    [existing_df, incremental_df], ignore_index=True
                )

                # Sort by date
                combined_df["date"] = pd.to_datetime(combined_df["date"])
                combined_df = combined_df.sort_values("date")
                combined_df["date"] = combined_df["date"].dt.strftime("%Y-%m-%d")

                # Write merged data back to file
                combined_df.to_csv(existing_data_path, index=False)

                self.logger.info(
                    f"📈 Successfully merged {len(incremental_df)} new rows of incremental data for {symbol}"
                )
                return True
            else:
                self.logger.info(f"📊 No new incremental data found for {symbol}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to merge incremental data for {symbol}: {e}")
            return False

    def _save_symbol_data_to_frontend(self, symbol: str, data: pd.DataFrame) -> None:
        """Save symbol data to frontend location using atomic file operations"""
        try:
            # Determine output path based on symbol
            output_dir = self.frontend_data_dir / "raw" / "stocks" / symbol
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / "daily.csv"

            self.logger.info(
                f"💾 Saving {len(data)} rows of data for {symbol} to {output_path}"
            )

            # Use atomic file operations to prevent corruption
            operation_result = self.file_operation_manager.atomic_csv_write(
                file_path=output_path,
                dataframe=data,
                backup_original=True,
                verify_content=True,
            )

            if operation_result.success:
                self.logger.info(
                    f"✅ Successfully saved {symbol} data ({operation_result.file_size} bytes)"
                )
            else:
                self.logger.error(
                    f"❌ Failed to save {symbol} data: {operation_result.error}"
                )

        except Exception as e:
            self.logger.error(f"Exception saving data for {symbol}: {e}")

    def _get_max_concurrency_from_charts(self) -> Optional[int]:
        """Extract max concurrency setting from colocated chart configurations"""
        max_concurrency_values = []

        for contract in self.discovered_contracts:
            try:
                # Look for pipeline settings in the chart's data-requirements.ts file
                chart_dir = (
                    contract.file_path.parent.parent
                )  # Go up from data/raw/stocks/BTC-USD/daily.csv
                data_requirements_file = chart_dir / "data-requirements.ts"

                if data_requirements_file.exists():
                    content = data_requirements_file.read_text()

                    # Look for maxConcurrency in pipeline settings
                    if "maxConcurrency:" in content:
                        # Extract the value after maxConcurrency:
                        lines = content.split("\n")
                        for line in lines:
                            if "maxConcurrency:" in line:
                                # Extract number from line like "    maxConcurrency: 5,"
                                try:
                                    value_part = line.split("maxConcurrency:")[
                                        1
                                    ].strip()
                                    value_part = value_part.split(",")[0].strip()
                                    max_concurrency = int(value_part)
                                    max_concurrency_values.append(max_concurrency)
                                    self.logger.debug(
                                        f"Found maxConcurrency: {max_concurrency} in {data_requirements_file}"
                                    )
                                except (ValueError, IndexError) as e:
                                    self.logger.debug(
                                        f"Could not parse maxConcurrency from line: {line} - {e}"
                                    )

            except Exception as e:
                self.logger.debug(
                    f"Error checking chart config {contract.file_path}: {e}"
                )

        if max_concurrency_values:
            # Use the minimum value to respect the most conservative setting
            result = min(max_concurrency_values)
            self.logger.info(
                f"Using maxConcurrency from chart configs: {result} (from values: {max_concurrency_values})"
            )
            return result

        return None

    def _categorize_service_error(self, error_message: str) -> str:
        """Categorize service errors for better debugging and monitoring"""
        if not error_message:
            return "unknown"

        error_lower = error_message.lower()

        # Infrastructure/logging errors
        if "log_error" in error_lower or "logging" in error_lower:
            return "infrastructure_logging"

        # Network/connectivity errors
        if any(
            term in error_lower
            for term in ["connection", "timeout", "network", "dns", "ssl"]
        ):
            return "network"

        # Authentication/API key errors
        if any(
            term in error_lower
            for term in ["auth", "api key", "unauthorized", "forbidden", "401", "403"]
        ):
            return "authentication"

        # Rate limiting errors
        if any(
            term in error_lower for term in ["rate limit", "too many requests", "429"]
        ):
            return "rate_limit"

        # Data/validation errors
        if any(
            term in error_lower
            for term in ["invalid", "validation", "schema", "format"]
        ):
            return "data_validation"

        # Service unavailable errors
        if any(
            term in error_lower
            for term in ["unavailable", "service", "500", "502", "503"]
        ):
            return "service_unavailable"

        # Default category for unclassified errors
        return "service_error"

    def _validate_cli_contract(self, service_name: str, command: str) -> None:
        """Validate that CLI service supports the requested command"""
        if service_name not in self.cli_service_capabilities:
            raise ValueError(f"Service '{service_name}' not found in capabilities")

        service_config = self.cli_service_capabilities[service_name]
        available_commands = service_config.get("commands", [])

        if command not in available_commands:
            raise ValueError(
                f"Command '{command}' not supported by service '{service_name}'. "
                f"Available commands: {available_commands}"
            )

    def _generate_chart_ready_data(self) -> ProcessingResult:
        """Generate pre-calculated chart data files for frontend consumption"""
        try:
            self.logger.info("Generating chart-ready data files")

            # Read the main trade history data from raw data source
            raw_trade_history_file = (
                self.project_root
                / "data"
                / "raw"
                / "trade_history"
                / "live_signals.csv"
            )
            frontend_trade_history_file = (
                self.frontend_data_dir / "trade-history" / "live_signals.csv"
            )

            # Prefer raw data source, fallback to frontend if needed
            if raw_trade_history_file.exists():
                trade_history_file = raw_trade_history_file
                self.logger.info(f"Using raw data source: {raw_trade_history_file}")
            elif frontend_trade_history_file.exists():
                trade_history_file = frontend_trade_history_file
                self.logger.warning(
                    f"Raw data not found, using frontend data: {frontend_trade_history_file}"
                )
            else:
                return ProcessingResult(
                    success=False,
                    operation="generate_chart_data",
                    error=f"Trade history file not found in either raw ({raw_trade_history_file}) or frontend ({frontend_trade_history_file}) locations",
                )

            # Load trade history data
            df = pd.read_csv(trade_history_file)

            # Apply chart status filtering before generating chart data
            results = []

            # Generate trade PnL waterfall data (sorted by PnL magnitude)
            waterfall_output_path = str(
                self.frontend_data_dir
                / "trade-history"
                / "trade_pnl_waterfall_sorted.csv"
            )
            if self.chart_status_manager.should_skip_output_file(waterfall_output_path):
                self.logger.info(
                    "Skipping waterfall data generation - chart is frozen/static"
                )
                waterfall_result = ProcessingResult(
                    success=True, operation="skip_waterfall_data"
                )
            else:
                waterfall_result = self._generate_waterfall_data(df)
            results.append(waterfall_result)

            # Generate closed positions PnL progression data
            closed_positions_output_path = str(
                self.frontend_data_dir
                / "portfolio"
                / "closed_positions_pnl_progression.csv"
            )
            if self.chart_status_manager.should_skip_output_file(
                closed_positions_output_path
            ):
                self.logger.info(
                    "Skipping closed positions data generation - chart is frozen/static"
                )
                closed_positions_result = ProcessingResult(
                    success=True, operation="skip_closed_positions_data"
                )
            else:
                closed_positions_result = self._generate_closed_positions_data(df)
            results.append(closed_positions_result)

            # Generate open positions PnL data
            open_positions_output_path = str(
                self.frontend_data_dir / "portfolio" / "open_positions_pnl_current.csv"
            )
            if self.chart_status_manager.should_skip_output_file(
                open_positions_output_path
            ):
                self.logger.info(
                    "Skipping open positions data generation - chart is frozen/static"
                )
                open_positions_result = ProcessingResult(
                    success=True, operation="skip_open_positions_data"
                )
            else:
                open_positions_result = self._generate_chart_open_positions_data(df)
            results.append(open_positions_result)

            # Check if all operations were successful
            all_success = all(result.success for result in results)
            failed_operations = [
                result.operation for result in results if not result.success
            ]

            if all_success:
                return ProcessingResult(
                    success=True,
                    operation="generate_chart_data",
                    metadata={"results": results},
                )
            else:
                return ProcessingResult(
                    success=False,
                    operation="generate_chart_data",
                    error=f"Failed operations: {failed_operations}",
                    metadata={"results": results},
                )

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_chart_data", error=str(e)
            )

    def _generate_waterfall_data(self, df: pd.DataFrame) -> ProcessingResult:
        """Generate waterfall chart data from trade history"""
        try:
            # Filter for closed positions only
            closed_trades = df[df["Status"] == "Closed"].copy()

            if closed_trades.empty:
                # Create empty waterfall data with correct structure
                waterfall_data = pd.DataFrame(
                    columns=["Ticker", "PnL", "CumulativePnL"]
                )
            else:
                # Sort by PnL magnitude (absolute value) for better visual impact
                closed_trades["PnL_abs"] = closed_trades["PnL"].abs()
                closed_trades = closed_trades.sort_values("PnL_abs", ascending=False)

                # Create waterfall data
                waterfall_data = closed_trades[["Ticker", "PnL"]].copy()
                waterfall_data["CumulativePnL"] = waterfall_data["PnL"].cumsum()

                # Remove the temporary column
                closed_trades.drop("PnL_abs", axis=1, inplace=True)

            # Save to frontend
            output_path = (
                self.frontend_data_dir
                / "trade-history"
                / "trade_pnl_waterfall_sorted.csv"
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            waterfall_data.to_csv(output_path, index=False)

            self.logger.info(
                f"Generated waterfall data with {len(waterfall_data)} trades"
            )

            return ProcessingResult(success=True, operation="generate_waterfall_data")

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_waterfall_data", error=str(e)
            )

    def _load_historical_price_data(self, ticker: str) -> Dict[str, float]:
        """Load historical price data for a specific ticker to calculate unrealized PnL"""
        price_data = {"current_price": 0.0, "previous_close": 0.0}

        try:
            # Check if we have local data first (more reliable)
            local_data_path = (
                self.frontend_data_dir / "raw" / "stocks" / ticker / "daily.csv"
            )

            if local_data_path.exists():
                df = pd.read_csv(local_data_path)
                if not df.empty and "close" in df.columns:
                    # Get the most recent closing price
                    price_data["current_price"] = float(df["close"].iloc[-1])
                    if len(df) > 1:
                        price_data["previous_close"] = float(df["close"].iloc[-2])
                    else:
                        price_data["previous_close"] = price_data["current_price"]

                    self.logger.debug(
                        f"Loaded local price data for {ticker}: current=${price_data['current_price']:.2f}"
                    )
                    return price_data

            # Fallback to live data fetch if no local data
            self.logger.debug(f"No local data found for {ticker}, fetching live data")
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period="5d")

            if not hist.empty:
                price_data["current_price"] = float(hist["Close"].iloc[-1])
                if len(hist) > 1:
                    price_data["previous_close"] = float(hist["Close"].iloc[-2])
                else:
                    price_data["previous_close"] = price_data["current_price"]

                self.logger.debug(
                    f"Fetched live price data for {ticker}: current=${price_data['current_price']:.2f}"
                )

        except Exception as e:
            self.logger.warning(
                f"Failed to load historical price data for {ticker}: {e}"
            )

        return price_data

    def _generate_closed_positions_data(self, df: pd.DataFrame) -> ProcessingResult:
        """Generate closed positions daily PnL progression time series data with enhanced validation"""
        try:
            # Validate input DataFrame
            if df.empty:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error="Empty input DataFrame",
                )

            # Validate required columns
            required_columns = [
                "Status",
                "Ticker",
                "Entry_Timestamp",
                "Exit_Timestamp",
                "Avg_Entry_Price",
                "Avg_Exit_Price",
                "Position_Size",
                "Direction",
                "PnL",
                "Position_UUID",
                "Duration_Days",
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error=f"Missing required columns: {missing_columns}",
                )

            closed_trades = df[df["Status"] == "Closed"].copy()

            if closed_trades.empty:
                return ProcessingResult(
                    success=False,
                    operation="generate_closed_positions_data",
                    error="No closed trades found",
                )

            self.logger.info(
                f"Processing {len(closed_trades)} closed positions for PnL progression analysis"
            )

            # Convert timestamps to datetime for proper sorting and processing
            closed_trades["Exit_Timestamp"] = pd.to_datetime(
                closed_trades["Exit_Timestamp"]
            )
            closed_trades = closed_trades.sort_values("Exit_Timestamp")

            # Create daily progression data
            closed_trades["Exit_Date"] = closed_trades["Exit_Timestamp"].dt.date
            closed_trades["PnL"] = pd.to_numeric(closed_trades["PnL"], errors="coerce")

            # Group by exit date and sum PnL for trades closed on the same day
            daily_pnl = closed_trades.groupby("Exit_Date")["PnL"].sum().reset_index()
            daily_pnl["Exit_Date"] = pd.to_datetime(daily_pnl["Exit_Date"])
            daily_pnl = daily_pnl.sort_values("Exit_Date")

            # Calculate cumulative PnL progression
            daily_pnl["Cumulative_PnL"] = daily_pnl["PnL"].cumsum()

            # Format dates for frontend consumption
            daily_pnl["Date"] = daily_pnl["Exit_Date"].dt.strftime("%Y-%m-%d")

            # Create final output with clean column names
            output_data = daily_pnl[["Date", "PnL", "Cumulative_PnL"]].rename(
                columns={"PnL": "Daily_PnL"}
            )

            # Round financial values for display
            output_data["Daily_PnL"] = output_data["Daily_PnL"].round(2)
            output_data["Cumulative_PnL"] = output_data["Cumulative_PnL"].round(2)

            # Save to frontend location
            output_path = (
                self.frontend_data_dir
                / "portfolio"
                / "closed_positions_pnl_progression.csv"
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_data.to_csv(output_path, index=False)

            self.logger.info(
                f"Generated closed positions PnL progression data: {len(output_data)} daily records, "
                f"total PnL: ${output_data['Cumulative_PnL'].iloc[-1]:.2f}"
            )

            return ProcessingResult(
                success=True, operation="generate_closed_positions_data"
            )

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_closed_positions_data", error=str(e)
            )

    def _generate_chart_open_positions_data(self, df: pd.DataFrame) -> ProcessingResult:
        """Generate open positions PnL data"""
        try:
            # Filter for open positions only
            open_trades = df[df["Status"] != "Closed"].copy()

            # If no open positions, create empty file with correct structure
            if open_trades.empty:
                open_positions_data = pd.DataFrame(
                    columns=[
                        "Position_UUID",
                        "Ticker",
                        "Direction",
                        "Position_Size",
                        "Avg_Entry_Price",
                        "Current_Price",
                        "Unrealized_PnL",
                        "PnL_Percent",
                        "Entry_Date",
                        "Days_Held",
                    ]
                )
            else:
                # Calculate current prices and unrealized PnL for open positions
                self.logger.info(f"Processing {len(open_trades)} open positions")

                open_positions_data = []
                for _, trade in open_trades.iterrows():
                    try:
                        # Get current price data for the ticker
                        price_data = self._load_historical_price_data(trade["Ticker"])
                        current_price = price_data["current_price"]

                        if current_price > 0:
                            # Calculate unrealized PnL based on position direction
                            entry_price = float(trade["Avg_Entry_Price"])
                            position_size = float(trade["Position_Size"])
                            direction = trade["Direction"]

                            if direction == "Long":
                                unrealized_pnl = (
                                    current_price - entry_price
                                ) * position_size
                            else:  # Short
                                unrealized_pnl = (
                                    entry_price - current_price
                                ) * position_size

                            pnl_percent = (
                                (current_price - entry_price) / entry_price * 100
                            )
                            if direction == "Short":
                                pnl_percent = -pnl_percent

                            # Calculate days held
                            entry_date = pd.to_datetime(trade["Entry_Timestamp"]).date()
                            days_held = (datetime.now().date() - entry_date).days

                            open_positions_data.append(
                                {
                                    "Position_UUID": trade["Position_UUID"],
                                    "Ticker": trade["Ticker"],
                                    "Direction": direction,
                                    "Position_Size": position_size,
                                    "Avg_Entry_Price": entry_price,
                                    "Current_Price": current_price,
                                    "Unrealized_PnL": round(unrealized_pnl, 2),
                                    "PnL_Percent": round(pnl_percent, 2),
                                    "Entry_Date": entry_date.strftime("%Y-%m-%d"),
                                    "Days_Held": days_held,
                                }
                            )
                        else:
                            self.logger.warning(
                                f"Could not get current price for {trade['Ticker']}"
                            )

                    except Exception as e:
                        self.logger.warning(
                            f"Error processing open position for {trade.get('Ticker', 'unknown')}: {e}"
                        )

                open_positions_data = pd.DataFrame(open_positions_data)

            # Save to frontend location
            output_path = (
                self.frontend_data_dir / "portfolio" / "open_positions_pnl_current.csv"
            )
            output_path.parent.mkdir(parents=True, exist_ok=True)
            open_positions_data.to_csv(output_path, index=False)

            total_unrealized_pnl = (
                open_positions_data["Unrealized_PnL"].sum()
                if not open_positions_data.empty
                else 0
            )
            self.logger.info(
                f"Generated open positions data: {len(open_positions_data)} positions, "
                f"total unrealized PnL: ${total_unrealized_pnl:.2f}"
            )

            return ProcessingResult(
                success=True, operation="generate_open_positions_data"
            )

        except Exception as e:
            return ProcessingResult(
                success=False, operation="generate_open_positions_data", error=str(e)
            )
