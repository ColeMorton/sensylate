#!/usr/bin/env python3
"""
Trade History Discovery - DASV Phase 1 Implementation

Performs comprehensive data discovery following trade_history:discover command requirements:
- Authoritative CSV data ingestion with fail-fast principles
- Local data inventory integration (fundamental analysis, sector analysis, cache)
- Data categorization and enhancement with ALL derivable fields
- Quality validation with confidence scoring
- Discovery output generation according to schema

Key Requirements:
- NEVER calculate PnL for closed trades - use CSV values exactly
- Calculate ALL missing Duration_Days for active trades
- Derive Trade_Type for ALL trades (never null)
- Maintain clear separation between closed and active trade analytics
- Include all trades in output with proper categorization

Usage:
    python scripts/trade_history_discover.py --portfolio {portfolio_name}
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TradeHistoryDiscovery:
    """Trade history discovery following DASV Phase 1 protocol"""

    def __init__(self, portfolio_name: str):
        self.portfolio_name = portfolio_name
        self.execution_date = datetime.now()
        self.data_dir = Path(__file__).parent.parent / "data"
        self.raw_dir = self.data_dir / "raw" / "trade_history"
        self.output_dir = self.data_dir / "outputs" / "trade_history" / "discovery"
        self.fundamental_dir = self.data_dir / "outputs" / "fundamental_analysis"
        self.sector_dir = self.data_dir / "outputs" / "sector_analysis"
        self.cache_dir = self.data_dir / "cache"

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize data containers
        self.trades: List[Dict[str, Any]] = []
        self.local_inventory: Dict[str, Any] = {}
        self.confidence_factors: Dict[str, float] = {}

    def resolve_portfolio_file(self) -> Path:
        """
        Resolve portfolio name to CSV file following PORTFOLIO_RESOLUTION_PROTOCOL
        """
        logger.info(f"Resolving portfolio file for: {self.portfolio_name}")

        # Check if portfolio name contains date pattern (YYYYMMDD)
        if re.search(r"\d{8}", self.portfolio_name):
            # Exact filename provided
            csv_file = self.raw_dir / f"{self.portfolio_name}.csv"
            if csv_file.exists():
                logger.info(f"Found exact file: {csv_file}")
                return csv_file
            else:
                raise FileNotFoundError(f"Exact file not found: {csv_file}")

        # Portfolio name only - find latest matching file
        pattern = f"{self.portfolio_name}_*.csv"
        matching_files = list(self.raw_dir.glob(pattern))

        if not matching_files:
            # Try without date suffix
            exact_file = self.raw_dir / f"{self.portfolio_name}.csv"
            if exact_file.exists():
                logger.info(f"Found file without date: {exact_file}")
                return exact_file
            raise FileNotFoundError(
                f"No portfolio file found matching '{self.portfolio_name}' in {self.raw_dir}"
            )

        # Return most recent file
        latest_file = max(matching_files, key=lambda f: f.stat().st_mtime)
        logger.info(f"Found latest file: {latest_file}")
        return latest_file

    def load_and_validate_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Authoritative CSV data ingestion with comprehensive validation
        """
        logger.info(f"Loading authoritative CSV data from: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        trades = []

        try:
            # Use pandas for robust CSV parsing
            df = pd.read_csv(file_path)

            # Log CSV structure
            logger.info(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns")
            logger.info(f"Columns: {list(df.columns)}")

            # Convert to list of dictionaries
            for _, row in df.iterrows():
                trade: Dict[str, Any] = {}
                for col_name, value in row.items():
                    col = str(col_name)  # Ensure column name is string
                    # Handle NaN values
                    if pd.isna(value):
                        trade[col] = None
                    elif col in [
                        "Position_Size",
                        "Avg_Entry_Price",
                        "Avg_Exit_Price",
                        "PnL",
                        "Return",
                        "Duration_Days",
                        "Days_Since_Entry",
                        "Current_Unrealized_PnL",
                        "Max_Favourable_Excursion",
                        "Max_Adverse_Excursion",
                        "MFE_MAE_Ratio",
                        "Exit_Efficiency",
                        "Exit_Efficiency_Fixed",
                    ]:
                        # Numeric fields
                        try:
                            trade[col] = float(value) if not pd.isna(value) else None
                        except (ValueError, TypeError):
                            trade[col] = None
                    elif col in ["Short_Window", "Long_Window", "Signal_Window"]:
                        # Integer fields
                        try:
                            trade[col] = int(value) if not pd.isna(value) else None
                        except (ValueError, TypeError):
                            trade[col] = None
                    else:
                        # String fields - ensure proper type
                        if pd.isna(value):
                            trade[col] = None
                        else:
                            trade[col] = str(value)

                trades.append(trade)

        except Exception as e:
            raise ValueError(f"Failed to parse CSV file {file_path}: {e}")

        logger.info(f"Successfully parsed {len(trades)} trades from CSV")
        return trades

    def calculate_all_derivable_fields(
        self, trades: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate ALL missing but derivable data - NEVER output null for derivable fields
        """
        logger.info("Calculating all derivable fields...")

        enhanced_trades = []
        derivable_field_stats = {
            "duration_days_calculated": 0,
            "trade_type_derived": 0,
            "entry_dates_parsed": 0,
            "exit_dates_parsed": 0,
        }

        for trade in trades:
            enhanced_trade = trade.copy()

            # Parse Entry_Timestamp
            entry_date = None
            if enhanced_trade.get("Entry_Timestamp"):
                try:
                    entry_date = datetime.strptime(
                        enhanced_trade["Entry_Timestamp"].split()[0], "%Y-%m-%d"
                    )
                    enhanced_trade["Entry_Date"] = entry_date.strftime("%Y-%m-%d")
                    derivable_field_stats["entry_dates_parsed"] += 1
                except Exception:
                    logger.warning(
                        f"Failed to parse entry timestamp: {enhanced_trade.get('Entry_Timestamp')}"
                    )
                    enhanced_trade["Entry_Date"] = None

            # Parse Exit_Timestamp
            exit_date = None
            if enhanced_trade.get("Exit_Timestamp"):
                try:
                    exit_date = datetime.strptime(
                        enhanced_trade["Exit_Timestamp"].split()[0], "%Y-%m-%d"
                    )
                    enhanced_trade["Exit_Date"] = exit_date.strftime("%Y-%m-%d")
                    derivable_field_stats["exit_dates_parsed"] += 1
                except Exception:
                    logger.warning(
                        f"Failed to parse exit timestamp: {enhanced_trade.get('Exit_Timestamp')}"
                    )
                    enhanced_trade["Exit_Date"] = None

            # Calculate Duration_Days for ALL active trades (CRITICAL REQUIREMENT)
            if enhanced_trade.get("Status") == "Open" and entry_date:
                if enhanced_trade.get("Duration_Days") is None:
                    duration_days = (self.execution_date - entry_date).days
                    enhanced_trade["Duration_Days"] = float(duration_days)
                    derivable_field_stats["duration_days_calculated"] += 1
                    logger.debug(
                        f"Calculated Duration_Days for {enhanced_trade.get('Ticker')}: {duration_days}"
                    )

            # Calculate Days_Since_Entry for active trades
            if enhanced_trade.get("Status") == "Open" and entry_date:
                days_since_entry = (self.execution_date - entry_date).days
                enhanced_trade["Days_Since_Entry"] = float(days_since_entry)

            # Derive Trade_Type for ALL trades (NEVER null - CRITICAL REQUIREMENT)
            if (
                not enhanced_trade.get("Trade_Type")
                or enhanced_trade.get("Trade_Type") == ""
            ):
                trade_type = self._derive_trade_type(enhanced_trade)
                enhanced_trade["Trade_Type"] = trade_type
                derivable_field_stats["trade_type_derived"] += 1
                logger.debug(
                    f"Derived Trade_Type for {enhanced_trade.get('Ticker')}: {trade_type}"
                )

            # Ensure Trade_Type is never null
            if not enhanced_trade.get("Trade_Type"):
                enhanced_trade["Trade_Type"] = "Standard_Signal"  # Fallback
                derivable_field_stats["trade_type_derived"] += 1

            # Additional quality fields
            enhanced_trade["Data_Complete"] = self._assess_data_completeness(
                enhanced_trade
            )
            enhanced_trade["Trade_Category"] = (
                "Closed" if enhanced_trade.get("Status") == "Closed" else "Active"
            )

            enhanced_trades.append(enhanced_trade)

        logger.info(f"Derivable field calculation complete: {derivable_field_stats}")
        return enhanced_trades

    def _derive_trade_type(self, trade: Dict[str, Any]) -> str:
        """
        Derive Trade_Type using business logic - NEVER return null
        """
        # First, check if Trade_Type is already provided and valid
        existing_type = trade.get("Trade_Type")
        if existing_type and existing_type.strip() and existing_type != "null":
            return existing_type.strip()

        # Use Trade_Quality for derivation if available
        quality = trade.get("Trade_Quality", "").strip()
        if quality:
            if quality == "Excellent":
                return "Momentum_Winner"
            elif quality == "Good":
                return "Trend_Follower"
            elif quality in ["Failed", "Failed to Capture Upside"]:
                return "Failed_Breakout"
            elif quality in ["Poor", "Poor Setup - High Risk, Low Reward"]:
                return "High_Risk_Entry"

        # For active trades, use Current_Unrealized_PnL
        if trade.get("Status") == "Open":
            unrealized_pnl = trade.get("Current_Unrealized_PnL", 0)
            if unrealized_pnl > 0.1:  # > 10% gain
                return "Momentum_Winner"
            elif unrealized_pnl > 0:
                return "Trend_Follower"
            elif unrealized_pnl < -0.1:  # > 10% loss
                return "Failed_Breakout"
            else:
                return "Standard_Signal"

        # For closed trades, use Return
        return_pct = trade.get("Return", 0)
        if return_pct is not None:
            if return_pct > 0.15:  # > 15% gain
                return "Momentum_Winner"
            elif return_pct > 0:
                return "Trend_Follower"
            elif return_pct < -0.1:  # > 10% loss
                return "Failed_Breakout"
            else:
                return "Standard_Signal"

        # Use Direction as final fallback
        direction = trade.get("Direction", "").strip()
        if direction:
            return direction  # 'Long' or 'Short'

        # Ultimate fallback - NEVER return null
        return "Standard_Signal"

    def _assess_data_completeness(self, trade: Dict[str, Any]) -> float:
        """Assess data completeness for a trade"""
        required_fields = [
            "Position_UUID",
            "Ticker",
            "Strategy_Type",
            "Entry_Timestamp",
            "Status",
        ]
        optional_fields = [
            "Exit_Timestamp",
            "Avg_Entry_Price",
            "Avg_Exit_Price",
            "PnL",
            "Return",
        ]

        complete_required = sum(
            1 for field in required_fields if trade.get(field) is not None
        )
        complete_optional = sum(
            1 for field in optional_fields if trade.get(field) is not None
        )

        total_possible = len(required_fields) + len(optional_fields)
        total_complete = complete_required + complete_optional

        return total_complete / total_possible

    def perform_local_data_inventory(self, unique_tickers: Set[str]) -> Dict[str, Any]:
        """
        Phase 0: LOCAL-FIRST DATA INVENTORY to prevent memory leaks
        """
        logger.info("Phase 0: Performing local-first data inventory...")

        inventory = {
            "execution_timestamp": self.execution_date.isoformat(),
            "total_tickers": len(unique_tickers),
            "fundamental_analysis_coverage": {},
            "tickers_with_local_data": [],
            "coverage_statistics": {},
        }

        # Scan fundamental analysis directory
        if self.fundamental_dir.exists():
            for ticker in unique_tickers:
                ticker_files = list(self.fundamental_dir.glob(f"{ticker}_*.md"))
                if ticker_files:
                    # Get most recent file
                    latest_file = max(ticker_files, key=lambda f: f.stat().st_mtime)

                    # Extract date from filename
                    date_match = re.search(r"(\d{8})", latest_file.stem)
                    file_date = None
                    if date_match:
                        try:
                            file_date = datetime.strptime(date_match.group(1), "%Y%m%d")
                        except ValueError:
                            pass

                    inventory["fundamental_analysis_coverage"][ticker] = {
                        "file_path": str(latest_file),
                        "file_date": file_date.isoformat() if file_date else None,
                        "age_days": (self.execution_date - file_date).days
                        if file_date
                        else None,
                    }
                    inventory["tickers_with_local_data"].append(ticker)

        # Calculate coverage statistics
        local_coverage_count = len(inventory["tickers_with_local_data"])
        inventory["coverage_statistics"] = {
            "fundamental_analysis_coverage": local_coverage_count / len(unique_tickers)
            if unique_tickers
            else 0,
            "tickers_with_analysis": local_coverage_count,
            "tickers_missing_analysis": len(unique_tickers) - local_coverage_count,
            "coverage_percentage": (local_coverage_count / len(unique_tickers) * 100)
            if unique_tickers
            else 0,
        }

        logger.info(
            f"Local inventory complete: {local_coverage_count}/{len(unique_tickers)} "
            f"tickers ({inventory['coverage_statistics']['coverage_percentage']:.1f}%) have fundamental analysis"
        )

        return inventory

    def categorize_and_validate_trades(
        self, trades: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Data categorization with quality validation following DASV requirements
        """
        logger.info("Categorizing and validating trades...")

        closed_trades = []
        active_trades = []
        validation_issues = []

        for trade in trades:
            status = trade.get("Status", "").strip()

            # Categorize trades
            if status == "Closed":
                # Validate closed trades have complete exit data
                if not trade.get("Exit_Timestamp"):
                    validation_issues.append(
                        f"Closed trade {trade.get('Position_UUID')} missing Exit_Timestamp"
                    )
                if trade.get("PnL") is None:
                    validation_issues.append(
                        f"Closed trade {trade.get('Position_UUID')} missing PnL"
                    )
                closed_trades.append(trade)

            elif status in ["Open", "Active"]:
                # Validate active trades have null exit fields but populated unrealized metrics
                if trade.get("Exit_Timestamp") is not None:
                    validation_issues.append(
                        f"Active trade {trade.get('Position_UUID')} has Exit_Timestamp but status is Open"
                    )
                if trade.get("Duration_Days") is None:
                    validation_issues.append(
                        f"Active trade {trade.get('Position_UUID')} missing Duration_Days"
                    )
                active_trades.append(trade)
            else:
                validation_issues.append(
                    f"Trade {trade.get('Position_UUID')} has invalid status: {status}"
                )

        # Calculate strategy distributions
        closed_strategy_dist: Dict[str, int] = {}
        active_strategy_dist: Dict[str, int] = {}

        for trade in closed_trades:
            strategy = trade.get("Strategy_Type", "Unknown")
            closed_strategy_dist[strategy] = closed_strategy_dist.get(strategy, 0) + 1

        for trade in active_trades:
            strategy = trade.get("Strategy_Type", "Unknown")
            active_strategy_dist[strategy] = active_strategy_dist.get(strategy, 0) + 1

        # Date range analysis
        closed_entry_dates = [
            trade.get("Entry_Date")
            for trade in closed_trades
            if trade.get("Entry_Date")
        ]
        closed_exit_dates = [
            trade.get("Exit_Date") for trade in closed_trades if trade.get("Exit_Date")
        ]
        active_entry_dates = [
            trade.get("Entry_Date")
            for trade in active_trades
            if trade.get("Entry_Date")
        ]

        categorization_result = {
            "closed_trades": {
                "count": len(closed_trades),
                "percentage": len(closed_trades) / len(trades) if trades else 0,
                "strategy_distribution": closed_strategy_dist,
                "date_range": {
                    "earliest_entry": min(closed_entry_dates)
                    if closed_entry_dates
                    else None,
                    "latest_entry": max(closed_entry_dates)
                    if closed_entry_dates
                    else None,
                    "earliest_exit": min(closed_exit_dates)
                    if closed_exit_dates
                    else None,
                    "latest_exit": max(closed_exit_dates)
                    if closed_exit_dates
                    else None,
                },
                "trades": closed_trades,
            },
            "active_trades": {
                "count": len(active_trades),
                "percentage": len(active_trades) / len(trades) if trades else 0,
                "strategy_distribution": active_strategy_dist,
                "entry_date_range": {
                    "earliest_entry": min(active_entry_dates)
                    if active_entry_dates
                    else None,
                    "latest_entry": max(active_entry_dates)
                    if active_entry_dates
                    else None,
                },
                "average_days_held": sum(
                    trade.get("Days_Since_Entry", 0) for trade in active_trades
                )
                / len(active_trades)
                if active_trades
                else 0,
                "trades": active_trades,
            },
            "validation_issues": validation_issues,
            "data_quality_score": 1.0 - (len(validation_issues) / len(trades))
            if trades
            else 0,
        }

        logger.info(
            f"Trade categorization complete: {len(closed_trades)} closed, {len(active_trades)} active, "
            f"{len(validation_issues)} validation issues"
        )

        return categorization_result

    def calculate_confidence_scores(
        self, trades_data: Dict[str, Any], local_inventory: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Calculate comprehensive confidence scores based on data quality
        """
        confidence = {}

        # Trade data completeness confidence
        total_trades = len(trades_data["closed_trades"]["trades"]) + len(
            trades_data["active_trades"]["trades"]
        )
        complete_trades = sum(
            1
            for trade in (
                trades_data["closed_trades"]["trades"]
                + trades_data["active_trades"]["trades"]
            )
            if trade.get("Data_Complete", 0) > 0.8
        )
        confidence["trade_data_completeness"] = (
            complete_trades / total_trades if total_trades > 0 else 0
        )

        # Derivable fields confidence (should be 1.0 if all calculated)
        missing_duration_days = sum(
            1
            for trade in trades_data["active_trades"]["trades"]
            if trade.get("Duration_Days") is None
        )
        missing_trade_types = sum(
            1
            for trade in (
                trades_data["closed_trades"]["trades"]
                + trades_data["active_trades"]["trades"]
            )
            if not trade.get("Trade_Type") or trade.get("Trade_Type") == "null"
        )

        total_active = len(trades_data["active_trades"]["trades"])
        confidence["derivable_fields"] = (
            1.0
            - (missing_duration_days + missing_trade_types)
            / (total_active + total_trades)
            if (total_active + total_trades) > 0
            else 1.0
        )

        # Local data coverage confidence
        confidence["fundamental_coverage"] = local_inventory["coverage_statistics"][
            "fundamental_analysis_coverage"
        ]

        # Data validation confidence
        confidence["data_validation"] = trades_data["data_quality_score"]

        # Overall confidence (weighted average)
        weights = {
            "trade_data_completeness": 0.3,
            "derivable_fields": 0.3,
            "fundamental_coverage": 0.2,
            "data_validation": 0.2,
        }

        confidence["overall"] = sum(
            confidence[key] * weight for key, weight in weights.items()
        )

        return confidence

    def generate_discovery_output(
        self,
        trades_data: Dict[str, Any],
        local_inventory: Dict[str, Any],
        confidence_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Generate comprehensive discovery JSON output following DASV schema
        """
        logger.info("Generating comprehensive discovery output...")

        # Get all trades for summary statistics
        all_trades = (
            trades_data["closed_trades"]["trades"]
            + trades_data["active_trades"]["trades"]
        )
        unique_tickers = list(
            set(trade["Ticker"] for trade in all_trades if trade.get("Ticker"))
        )

        # Calculate performance metrics for closed trades only
        closed_trades = trades_data["closed_trades"]["trades"]
        wins = [t for t in closed_trades if t.get("Return", 0) > 0]
        losses = [t for t in closed_trades if t.get("Return", 0) < 0]

        performance_metrics = {
            "total_closed_trades": len(closed_trades),
            "win_rate": len(wins) / len(closed_trades) if closed_trades else 0,
            "total_wins": len(wins),
            "total_losses": len(losses),
            "average_win_return": sum(t.get("Return", 0) for t in wins) / len(wins)
            if wins
            else 0,
            "average_loss_return": sum(t.get("Return", 0) for t in losses) / len(losses)
            if losses
            else 0,
            "profit_factor": (
                abs(
                    sum(t.get("Return", 0) for t in wins)
                    / sum(t.get("Return", 0) for t in losses)
                )
                if losses and sum(t.get("Return", 0) for t in losses) != 0
                else 0
            ),
            "total_pnl": sum(
                t.get("PnL", 0) for t in closed_trades if t.get("PnL") is not None
            ),
            "total_return_percentage": sum(t.get("Return", 0) for t in closed_trades),
        }

        # Build comprehensive discovery output
        discovery_output = {
            "portfolio": self.portfolio_name,
            "discovery_metadata": {
                "execution_timestamp": self.execution_date.isoformat(),
                "protocol_version": "DASV_Phase_1_Comprehensive",
                "data_source": str(self.resolve_portfolio_file()),
                "confidence_score": confidence_scores["overall"],
                "data_completeness": confidence_scores["trade_data_completeness"],
                "derivable_fields_calculated": confidence_scores["derivable_fields"],
            },
            "portfolio_summary": {
                "total_trades": len(all_trades),
                "closed_trades": len(closed_trades),
                "active_trades": len(trades_data["active_trades"]["trades"]),
                "unique_tickers": len(unique_tickers),
            },
            "strategy_distribution": {
                **trades_data["closed_trades"]["strategy_distribution"],
                **trades_data["active_trades"]["strategy_distribution"],
            },
            "ticker_performance": {
                ticker: {
                    "total_trades": len(
                        [t for t in all_trades if t.get("Ticker") == ticker]
                    ),
                    "closed_trades": len(
                        [t for t in closed_trades if t.get("Ticker") == ticker]
                    ),
                    "active_trades": len(
                        [
                            t
                            for t in trades_data["active_trades"]["trades"]
                            if t.get("Ticker") == ticker
                        ]
                    ),
                    "total_return": sum(
                        t.get("Return", 0)
                        for t in closed_trades
                        if t.get("Ticker") == ticker and t.get("Return") is not None
                    ),
                    "win_rate": len(
                        [
                            t
                            for t in closed_trades
                            if t.get("Ticker") == ticker and t.get("Return", 0) > 0
                        ]
                    )
                    / len([t for t in closed_trades if t.get("Ticker") == ticker])
                    if [t for t in closed_trades if t.get("Ticker") == ticker]
                    else 0,
                }
                for ticker in unique_tickers
            },
            "performance_metrics": performance_metrics,
            "active_positions": [
                {
                    "ticker": trade.get("Ticker"),
                    "strategy": trade.get("Strategy_Type"),
                    "days_held": trade.get("Days_Since_Entry", 0),
                    "current_return": trade.get("Current_Unrealized_PnL", 0),
                }
                for trade in trades_data["active_trades"]["trades"]
            ],
            "data_quality_assessment": {
                "overall_confidence": confidence_scores["overall"],
                "trade_data_completeness": confidence_scores["trade_data_completeness"],
                "derivable_fields_confidence": confidence_scores["derivable_fields"],
                "fundamental_coverage_confidence": confidence_scores[
                    "fundamental_coverage"
                ],
                "validation_confidence": confidence_scores["data_validation"],
                "validation_issues_count": len(trades_data["validation_issues"]),
                "validation_issues": trades_data["validation_issues"][
                    :10
                ],  # First 10 issues
            },
            "local_data_integration": local_inventory,
            "next_phase_inputs": {
                "analysis_ready": confidence_scores["overall"] > 0.8,
                "required_confidence_met": confidence_scores["overall"] > 0.95,
                "closed_trades_count": len(closed_trades),
                "active_trades_count": len(trades_data["active_trades"]["trades"]),
                "statistical_adequacy": len(closed_trades) >= 25,
                "data_package_complete": True,
            },
        }

        return discovery_output

    def execute_discovery(self) -> Dict[str, Any]:
        """
        Execute the complete DASV Phase 1 discovery protocol
        """
        logger.info(
            f"Starting trade history discovery for portfolio: {self.portfolio_name}"
        )

        try:
            # Step 1: Resolve and load CSV file
            csv_file = self.resolve_portfolio_file()
            trades = self.load_and_validate_csv(csv_file)

            # Step 2: Calculate ALL derivable fields (CRITICAL)
            trades = self.calculate_all_derivable_fields(trades)

            # Step 3: Get unique tickers for inventory
            unique_tickers = set(
                trade["Ticker"] for trade in trades if trade.get("Ticker")
            )

            # Step 4: Perform local data inventory (Phase 0)
            local_inventory = self.perform_local_data_inventory(unique_tickers)

            # Step 5: Categorize and validate trades
            trades_data = self.categorize_and_validate_trades(trades)

            # Step 6: Calculate confidence scores
            confidence_scores = self.calculate_confidence_scores(
                trades_data, local_inventory
            )

            # Step 7: Generate comprehensive discovery output
            discovery_output = self.generate_discovery_output(
                trades_data, local_inventory, confidence_scores
            )

            # Step 8: Save output with proper naming
            output_filename = (
                f"{self.portfolio_name}_{self.execution_date.strftime('%Y%m%d')}.json"
            )
            output_file = self.output_dir / output_filename

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(discovery_output, f, indent=2, ensure_ascii=False)

            logger.info(f"Discovery output saved to: {output_file}")

            # Log summary statistics
            logger.info(
                f"Discovery complete - Total trades: {discovery_output['portfolio_summary']['total_trades']}, "
                f"Closed: {discovery_output['portfolio_summary']['closed_trades']}, "
                f"Active: {discovery_output['portfolio_summary']['active_trades']}, "
                f"Confidence: {confidence_scores['overall']:.3f}"
            )

            return discovery_output

        except Exception as e:
            logger.error(f"Discovery failed: {e}")
            raise


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Execute trade history discovery protocol"
    )
    parser.add_argument("--portfolio", required=True, help="Portfolio name (required)")
    parser.add_argument(
        "--output-format",
        choices=["json", "summary"],
        default="summary",
        help="Output format (default: summary)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Execute discovery
    discovery = TradeHistoryDiscovery(portfolio_name=args.portfolio)
    result = discovery.execute_discovery()

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        # Print summary
        print("\n" + "=" * 60)
        print("TRADE HISTORY DISCOVERY COMPLETE")
        print("=" * 60)
        print(f"Portfolio: {result['portfolio']}")
        print(f"Execution: {result['discovery_metadata']['execution_timestamp']}")
        print(f"Data Source: {result['discovery_metadata']['data_source']}")
        print(
            f"Overall Confidence: {result['discovery_metadata']['confidence_score']:.3f}"
        )

        print("\nTRADE SUMMARY:")
        summary = result["portfolio_summary"]
        print(f"  Total Trades: {summary['total_trades']}")
        print(f"  Closed Positions: {summary['closed_trades']}")
        print(f"  Active Positions: {summary['active_trades']}")
        print(f"  Unique Tickers: {summary['unique_tickers']}")

        print("\nPERFORMANCE (Closed Trades Only):")
        perf = result["performance_metrics"]
        print(f"  Win Rate: {perf['win_rate']:.1%}")
        print(f"  Total Wins: {perf['total_wins']}")
        print(f"  Total Losses: {perf['total_losses']}")
        print(f"  Profit Factor: {perf['profit_factor']:.2f}")
        print(f"  Total PnL: ${perf['total_pnl']:.2f}")

        print("\nACTIVE PORTFOLIO:")
        print(f"  Active Positions: {summary['active_trades']}")

        print("\nDATA QUALITY:")
        quality = result["data_quality_assessment"]
        print(f"  Overall Confidence: {quality['overall_confidence']:.3f}")
        print(f"  Derivable Fields: {quality['derivable_fields_confidence']:.3f}")
        print(f"  Validation Issues: {quality['validation_issues_count']}")

        print(f"\nOutput saved to: {discovery.output_dir}")
        print("=" * 60)


if __name__ == "__main__":
    main()
