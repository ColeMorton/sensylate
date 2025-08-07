#!/usr/bin/env python3
"""
Trade History Discovery - Atomic Data Collection Tool

Atomic utility tool for trade history data discovery. Focuses on:
- Portfolio file resolution and CSV data loading
- Basic data validation and enhancement
- Integration with unified calculation engine for metrics
- Schema-compliant discovery output generation

This tool is designed to be called by the discover command via researcher sub-agent.
All complex calculations are delegated to the unified calculation engine.

Usage:
    python scripts/trade_history_discover.py --portfolio {portfolio_name}
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from trade_history.unified_calculation_engine import TradingCalculationEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AtomicDiscoveryTool:
    """Atomic tool for trade history data discovery"""

    def __init__(self, portfolio_name: str):
        self.portfolio_name = portfolio_name
        self.execution_date = datetime.now()
        self.data_dir = Path(__file__).parent.parent / "data"
        self.raw_dir = self.data_dir / "raw" / "trade_history"
        self.output_dir = self.data_dir / "outputs" / "trade_history" / "discovery"
        self.fundamental_dir = self.data_dir / "outputs" / "fundamental_analysis"

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def resolve_portfolio_file(self) -> Path:
        """
        Resolve portfolio name to CSV file path
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

    def scan_local_fundamental_analysis(self, unique_tickers: set) -> Dict[str, Any]:
        """
        Scan local fundamental analysis coverage
        """
        logger.info("Scanning local fundamental analysis coverage...")

        coverage = {}
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

                    coverage[ticker] = {
                        "file_path": str(latest_file),
                        "file_date": file_date.isoformat() if file_date else None,
                        "age_days": (
                            (self.execution_date - file_date).days
                            if file_date
                            else None
                        ),
                    }

        coverage_stats = {
            "fundamental_analysis_coverage": len(coverage) / len(unique_tickers)
            if unique_tickers
            else 0,
            "tickers_with_analysis": len(coverage),
            "tickers_missing_analysis": len(unique_tickers) - len(coverage),
            "coverage_percentage": (len(coverage) / len(unique_tickers) * 100)
            if unique_tickers
            else 0,
        }

        logger.info(
            f"Fundamental analysis coverage: {coverage_stats['coverage_percentage']:.1f}%"
        )

        return {
            "execution_timestamp": self.execution_date.isoformat(),
            "total_tickers": len(unique_tickers),
            "fundamental_analysis_coverage": coverage,
            "tickers_with_local_data": list(coverage.keys()),
            "coverage_statistics": coverage_stats,
        }

    def execute_discovery(self) -> Dict[str, Any]:
        """
        Execute atomic discovery data collection
        """
        logger.info(f"Starting atomic discovery for portfolio: {self.portfolio_name}")

        try:
            # Step 1: Resolve portfolio file
            csv_file = self.resolve_portfolio_file()

            # Step 2: Use unified calculation engine for data processing
            engine = TradingCalculationEngine(str(csv_file))

            # Step 3: Get discovery data from unified engine
            discovery_data = engine.get_discovery_data()

            # Step 4: Get unique tickers from trades
            unique_tickers = set(trade.ticker for trade in engine.trades)

            # Step 5: Add local data inventory
            local_inventory = self.scan_local_fundamental_analysis(unique_tickers)
            discovery_data["local_data_integration"] = local_inventory

            # Step 6: Update confidence scores based on local data
            fundamental_coverage = local_inventory["coverage_statistics"][
                "fundamental_analysis_coverage"
            ]
            discovery_data["data_quality_assessment"][
                "fundamental_coverage_confidence"
            ] = fundamental_coverage

            # Recalculate overall confidence with local data integration
            original_confidence = discovery_data["discovery_metadata"][
                "confidence_score"
            ]
            discovery_data["discovery_metadata"]["confidence_score"] = (
                original_confidence * 0.8 + fundamental_coverage * 0.2
            )
            discovery_data["data_quality_assessment"][
                "overall_confidence"
            ] = discovery_data["discovery_metadata"]["confidence_score"]

            # Step 7: Save output
            output_filename = (
                f"{self.portfolio_name}_{self.execution_date.strftime('%Y%m%d')}.json"
            )
            output_file = self.output_dir / output_filename

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(discovery_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Discovery output saved to: {output_file}")

            # Log summary
            logger.info(
                f"Discovery complete - Total trades: {discovery_data['portfolio_summary']['total_trades']}, "
                f"Closed: {discovery_data['portfolio_summary']['closed_trades']}, "
                f"Active: {discovery_data['portfolio_summary']['active_trades']}, "
                f"Confidence: {discovery_data['discovery_metadata']['confidence_score']:.3f}"
            )

            return discovery_data

        except Exception as e:
            logger.error(f"Atomic discovery failed: {e}")
            raise


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Atomic trade history discovery tool")
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
    discovery_tool = AtomicDiscoveryTool(portfolio_name=args.portfolio)
    result = discovery_tool.execute_discovery()

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        # Print summary
        print("\n" + "=" * 60)
        print("ATOMIC DISCOVERY COMPLETE")
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

        print("\nDATA QUALITY:")
        quality = result["data_quality_assessment"]
        print(f"  Overall Confidence: {quality['overall_confidence']:.3f}")
        print(
            f"  Fundamental Coverage: {quality['fundamental_coverage_confidence']:.3f}"
        )

        print(f"\nOutput saved to: {discovery_tool.output_dir}")
        print("=" * 60)


if __name__ == "__main__":
    main()
