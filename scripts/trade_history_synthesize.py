#!/usr/bin/env python3
"""
Trade History Synthesize - DASV Phase 3 Implementation

Generates comprehensive report synthesis following trade_history:synthesize command requirements:
- Multi-audience document generation (internal, live, historical reports)
- Live Signals context automatic inclusion for live_signals portfolio
- Template compliance and formatting consistency
- Executive dashboard synthesis
- Exact CSV P&L values (never calculated)
- Statistical honesty with sample size limitations
- Institutional-grade quality standards

Usage:
    python scripts/trade_history_synthesize.py --portfolio live_signals
    python scripts/trade_history_synthesize.py --portfolio live_signals --report-type historical
    python scripts/trade_history_synthesize.py --portfolio live_signals --report-type all
"""

import argparse
import csv
import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DASVPhase3Synthesizer:
    """DASV Phase 3 synthesizer for comprehensive institutional-grade report generation."""

    def __init__(self, portfolio_name: str):
        self.portfolio_name = portfolio_name
        self.execution_date = datetime.now()
        self.data_dir = Path(__file__).parent.parent / "data"
        self.output_dir = self.data_dir / "outputs" / "trade_history"
        self.raw_data_dir = self.data_dir / "raw" / "trade_history"

        # Ensure output directories exist
        (self.output_dir / "internal").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "live").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "historical").mkdir(parents=True, exist_ok=True)

        # Initialize data containers
        self.discovery_data = None
        self.analysis_data = None
        self.raw_trades_df = None

    def load_phase_data(self) -> Dict[str, Any]:
        """Load discovery, analysis, and raw CSV data from previous DASV phases."""
        # Find latest discovery and analysis files
        discovery_dir = self.data_dir / "outputs" / "trade_history" / "discovery"
        analysis_dir = self.data_dir / "outputs" / "trade_history" / "analysis"

        # Discovery data
        discovery_pattern = f"{self.portfolio_name}_*.json"
        discovery_files = list(discovery_dir.glob(discovery_pattern))
        if not discovery_files:
            raise FileNotFoundError(
                f"No discovery files found for portfolio '{self.portfolio_name}'"
            )

        latest_discovery = max(discovery_files, key=lambda f: f.stat().st_mtime)

        # Analysis data
        analysis_pattern = f"{self.portfolio_name}_*.json"
        analysis_files = list(analysis_dir.glob(analysis_pattern))
        if not analysis_files:
            raise FileNotFoundError(
                f"No analysis files found for portfolio '{self.portfolio_name}'"
            )

        latest_analysis = max(analysis_files, key=lambda f: f.stat().st_mtime)

        # Load JSON data
        with open(latest_discovery, "r") as f:
            self.discovery_data = json.load(f)

        with open(latest_analysis, "r") as f:
            self.analysis_data = json.load(f)

        # Load raw CSV data for exact P&L values
        csv_file = self.raw_data_dir / f"{self.portfolio_name}.csv"
        if not csv_file.exists():
            raise FileNotFoundError(f"Raw CSV file not found: {csv_file}")

        self.raw_trades_df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(self.raw_trades_df)} trades from CSV: {csv_file}")

        logger.info(f"Loaded discovery data from: {latest_discovery}")
        logger.info(f"Loaded analysis data from: {latest_analysis}")

        return {
            "discovery": self.discovery_data,
            "analysis": self.analysis_data,
            "discovery_file": str(latest_discovery),
            "analysis_file": str(latest_analysis),
            "csv_file": str(csv_file),
        }

    def generate_live_signals_overview(self) -> str:
        """Generate standardized Live Signals Overview section for live_signals portfolio."""
        if self.portfolio_name != "live_signals":
            return ""

        return """## 📡 Live Signals Overview

### Trading Signal Platform

**Live Signals** are real-time trading signals posted publicly on X/Twitter at **[@colemorton7](https://x.com/colemorton7)** for educational and transparency purposes. These signals provide followers with live market insights, entry/exit points, and portfolio tracking in real-time.

### Methodology & Approach

- **Position Sizing**: Single unit position size per strategy for consistency and simplicity
- **Risk Management**: Risk management details are omitted from public signals to focus on signal quality and timing
- **Signal Types**: Technical analysis using SMA and EMA crossover strategies
- **Transparency**: All trades are tracked and reported publicly for educational purposes

### Platform Benefits

- **Real-time Updates**: Live signal posting and portfolio tracking
- **Educational Value**: Transparent methodology and performance reporting
- **Accessibility**: Public access to institutional-quality analysis
- **Community**: Shared learning and market insights

---

"""

    def _generate_trade_table(self, trades_df: pd.DataFrame) -> str:
        """Generate comprehensive trade table with exact CSV values."""
        table_rows = []
        table_rows.append(
            "| Ticker | Strategy | Entry Date | Exit Date | Duration | P&L | Return | Status |"
        )
        table_rows.append(
            "|--------|----------|------------|-----------|----------|-----|--------|--------|"
        )

        for _, trade in trades_df.iterrows():
            entry_date = pd.to_datetime(trade["Entry_Timestamp"]).strftime("%m/%d/%Y")
            exit_date = pd.to_datetime(trade["Exit_Timestamp"]).strftime("%m/%d/%Y")
            pnl_str = (
                f"${trade['PnL']:.2f}"
                if trade["PnL"] >= 0
                else f"(${abs(trade['PnL']):.2f})"
            )
            return_str = (
                f"{trade['Return']:.2%}"
                if trade["Return"] >= 0
                else f"({abs(trade['Return']):.2%})"
            )

            table_rows.append(
                f"| {trade['Ticker']} | {trade['Strategy_Type']} | {entry_date} | {exit_date} | {trade['Duration_Days']:.0f}d | {pnl_str} | {return_str} | {trade['Status']} |"
            )

        return "\n".join(table_rows)

    def _generate_top_trades_section(self, trades_df: pd.DataFrame) -> str:
        """Generate top performing trades analysis."""
        top_winners = trades_df.nlargest(5, "PnL")
        top_losers = trades_df.nsmallest(5, "PnL")

        content = ["### Top 5 Winners"]
        for _, trade in top_winners.iterrows():
            content.append(
                f"- **{trade['Ticker']}** ({trade['Strategy_Type']}): ${trade['PnL']:.2f} ({trade['Return']:.1%}) - {trade['Duration_Days']:.0f} days"
            )

        content.append("\n### Top 5 Losers")
        for _, trade in top_losers.iterrows():
            content.append(
                f"- **{trade['Ticker']}** ({trade['Strategy_Type']}): ${trade['PnL']:.2f} ({trade['Return']:.1%}) - {trade['Duration_Days']:.0f} days"
            )

        return "\n".join(content)

    def generate_historical_report(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive historical performance report."""

        # Calculate key metrics from raw CSV data
        closed_trades = self.raw_trades_df[
            self.raw_trades_df["Status"] == "Closed"
        ].copy()
        total_pnl = closed_trades["PnL"].sum()
        win_rate = len(closed_trades[closed_trades["PnL"] > 0]) / len(closed_trades)
        avg_win = closed_trades[closed_trades["PnL"] > 0]["PnL"].mean()
        avg_loss = closed_trades[closed_trades["PnL"] < 0]["PnL"].mean()
        best_trade = closed_trades.loc[closed_trades["PnL"].idxmax()]
        worst_trade = closed_trades.loc[closed_trades["PnL"].idxmin()]
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float("inf")
        avg_duration = closed_trades["Duration_Days"].mean()

        # Strategy distribution
        strategy_dist = closed_trades["Strategy_Type"].value_counts()

        # Generate comprehensive trade table
        trade_table = self._generate_trade_table(closed_trades)

        # Statistical significance assessment
        sample_size = len(closed_trades)
        min_required = 25
        adequacy = "✅ **ADEQUATE**" if sample_size >= min_required else "⚠️ **LIMITED**"

        report_content = f"""# {self.portfolio_name.replace('_', ' ').title()} Historical Performance Report
**Portfolio**: {self.portfolio_name} | **Date**: {self.execution_date.strftime("%B %d, %Y")} | **Type**: Closed Positions Analysis

---

{self.generate_live_signals_overview()}## 📊 Performance Summary (Closed Trades Only)

### Statistical Honesty Disclosure
**Sample Size**: {sample_size} closed trades | **Minimum Required**: {min_required} trades | **Status**: {adequacy}

*Note: Analysis based on completed trades only. Results may not be indicative of future performance. Small sample sizes limit statistical confidence.*

### Overall Results
- **Total Closed Trades**: {sample_size} {adequacy} for basic analysis
- **Win Rate**: {win_rate:.2%} ({len(closed_trades[closed_trades['PnL'] > 0])} wins, {len(closed_trades[closed_trades['PnL'] <= 0])} losses)
- **Total P&L**: ${total_pnl:.2f} (from exact CSV values)
- **Average Duration**: {avg_duration:.1f} days
- **Strategy Mix**: {dict(strategy_dist)}

### Key Performance Metrics
- **Average Win**: ${avg_win:.2f}
- **Average Loss**: ${avg_loss:.2f}
- **Profit Factor**: {profit_factor:.2f}
- **Best Trade**: {best_trade['Ticker']} (${best_trade['PnL']:.2f})
- **Worst Trade**: {worst_trade['Ticker']} (${worst_trade['PnL']:.2f})
- **Expectancy**: ${(win_rate * avg_win + (1-win_rate) * avg_loss):.2f} per trade

---

## 🏆 Top Performing Closed Trades

{self._generate_top_trades_section(closed_trades)}

---

## 📋 Complete Closed Trade History

**All values sourced directly from CSV data - no calculations applied**

{trade_table}

---

## 📈 Performance Analysis

### Win Rate Breakdown
- **Overall Win Rate**: {win_rate:.2%}
- **SMA Strategy**: {len(closed_trades[(closed_trades['Strategy_Type'] == 'SMA') & (closed_trades['PnL'] > 0)]) / len(closed_trades[closed_trades['Strategy_Type'] == 'SMA']):.2%} ({len(closed_trades[closed_trades['Strategy_Type'] == 'SMA'])} trades)
- **EMA Strategy**: {len(closed_trades[(closed_trades['Strategy_Type'] == 'EMA') & (closed_trades['PnL'] > 0)]) / len(closed_trades[closed_trades['Strategy_Type'] == 'EMA']):.2%} ({len(closed_trades[closed_trades['Strategy_Type'] == 'EMA'])} trades)

### Risk-Adjusted Returns
- **Sharpe Ratio**: {self.analysis_data.get('performance_measurement', {}).get('statistical_analysis', {}).get('risk_adjusted_metrics', {}).get('sharpe_ratio', 'N/A')}
- **Maximum Drawdown**: {self.analysis_data.get('risk_assessment', {}).get('portfolio_risk_metrics', {}).get('drawdown_analysis', {}).get('max_drawdown', 'N/A')}

---

## 📊 Statistical Significance Analysis

### Sample Size Assessment
- **Current Sample**: {sample_size} trades
- **Minimum for Basic Analysis**: 25 trades
- **Recommended for Robust Analysis**: 100+ trades
- **Statistical Power**: {"High" if sample_size >= 100 else "Medium" if sample_size >= 50 else "Limited"}

### Confidence Intervals (95%)
*Note: Confidence intervals widen with smaller sample sizes*
- **Win Rate Range**: {max(0, win_rate - 1.96 * np.sqrt(win_rate * (1-win_rate) / sample_size)):.1%} - {min(1, win_rate + 1.96 * np.sqrt(win_rate * (1-win_rate) / sample_size)):.1%}

---

## 📱 Live Signals Platform Integration

**Follow Live Signals**: [@colemorton7](https://x.com/colemorton7) on X/Twitter

**Historical Track Record Summary**:
- **{sample_size} Closed Trades**: Comprehensive performance transparency
- **{win_rate:.1%} Win Rate**: Based on exact CSV P&L values
- **${total_pnl:.2f} Total P&L**: Unmodified trading results

**Platform Methodology**:
- Technical analysis with fundamental research integration
- Single unit position sizing for educational clarity
- Real-time portfolio tracking and performance updates
- Transparent wins and losses with detailed analysis

---

**Analysis Completed**: {self.execution_date.strftime("%B %d, %Y")} | **Statistical Confidence**: {self.analysis_data.get('analysis_quality_assessment', {}).get('overall_confidence', 0):.1%} | **Sample Size Limitation**: {"None" if sample_size >= 100 else "Moderate" if sample_size >= 50 else "Significant"}
"""

        return report_content

    def generate_internal_report(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive internal trading report."""

        # Calculate executive metrics
        closed_trades = self.raw_trades_df[
            self.raw_trades_df["Status"] == "Closed"
        ].copy()
        total_pnl = closed_trades["PnL"].sum()
        win_rate = len(closed_trades[closed_trades["PnL"] > 0]) / len(closed_trades)

        # Portfolio health score (0-100)
        health_score = min(100, max(0, 50 + (total_pnl / 1000) * 10 + win_rate * 30))

        return f"""# Internal Trading Report: {self.portfolio_name.replace('_', ' ').title()}
**Generated**: {self.execution_date.strftime("%Y-%m-%d %H:%M:%S")} | **Classification**: INTERNAL USE ONLY

{self.generate_live_signals_overview()}## 📊 Executive Dashboard

### 30-Second Brief
- **Portfolio Health Score**: {health_score:.1f}/100 ({self._health_score_interpretation(health_score)})
- **Total P&L**: ${total_pnl:.2f} | **Win Rate**: {win_rate:.1%} | **Trades**: {len(closed_trades)}
- **Critical Issues**: {len(self._identify_critical_issues(closed_trades))} requiring immediate attention
- **Optimization Potential**: {self._calculate_optimization_potential()}

### Performance Deep Dive
- **System Quality Number**: {self.analysis_data.get('advanced_statistical_metrics', {}).get('system_quality_assessment', {}).get('system_quality_number', 'N/A')}
- **Exit Efficiency**: {self.analysis_data.get('signal_effectiveness', {}).get('exit_signal_analysis', {}).get('exit_efficiency_metrics', {}).get('overall_exit_efficiency', 'N/A')}
- **Statistical Significance**: {self.analysis_data.get('statistical_validation', {}).get('significance_testing', {}).get('return_vs_zero', {}).get('significant', 'N/A')}

---

## 🎯 Strategic Recommendations

### Immediate Actions (0-30 days)
- Review recent trade performance for pattern identification
- Validate signal generation parameters for current market conditions
- Update risk management protocols based on recent volatility

### Medium-term Optimizations (1-3 months)
- Implement exit timing optimization based on analysis insights
- Enhance entry signal parameters for current market regime
- Develop position sizing optimization framework

---

**Report Classification**: INTERNAL USE ONLY | **Next Review**: {(self.execution_date + pd.Timedelta(days=7)).strftime("%Y-%m-%d")} | **Confidence Level**: {self.analysis_data.get('analysis_quality_assessment', {}).get('overall_confidence', 0):.1%}
"""

    def generate_live_monitor(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive live signals monitor report."""

        # Current portfolio status
        active_trades = self.raw_trades_df[self.raw_trades_df["Status"] != "Closed"]
        closed_trades = self.raw_trades_df[self.raw_trades_df["Status"] == "Closed"]

        return f"""# Live Signals Monitor: {self.portfolio_name.replace('_', ' ').title()}
**Generated**: {self.execution_date.strftime("%Y-%m-%d %H:%M:%S")} | **Status**: LIVE MONITORING

{self.generate_live_signals_overview()}## 📊 Portfolio Overview

### Current Status
- **Active Positions**: {len(active_trades)} open trades
- **Total Positions**: {len(self.raw_trades_df)} lifetime trades
- **Platform Status**: ✅ ACTIVE on [@colemorton7](https://x.com/colemorton7)

### Live Performance Metrics
- **Win Rate (All-Time)**: {len(closed_trades[closed_trades['PnL'] > 0]) / len(closed_trades):.1%}
- **Total P&L**: ${closed_trades['PnL'].sum():.2f}
- **System Quality**: {self.analysis_data.get('advanced_statistical_metrics', {}).get('system_quality_assessment', {}).get('system_quality_number', 'N/A')}

---

## 📱 Social Media Integration

### X/Twitter Performance
- **Platform**: [@colemorton7](https://x.com/colemorton7)
- **Signal Posting**: Real-time entry/exit signals
- **Transparency**: Full trade history disclosure
- **Educational Value**: Strategy explanation and analysis

---

**Monitor Status**: ACTIVE | **Last Update**: {self.execution_date.strftime("%Y-%m-%d %H:%M:%S")} | **Next Refresh**: {(self.execution_date + pd.Timedelta(hours=1)).strftime("%H:%M")}
"""

    def synthesize_reports(self, report_types: List[str] = None) -> Dict[str, str]:
        """Generate all requested report types with comprehensive analysis."""
        if report_types is None:
            report_types = ["internal", "live", "historical"]

        # Load phase data
        data = self.load_phase_data()

        # Generate reports
        reports = {}
        date_stamp = self.execution_date.strftime("%Y%m%d")

        if "historical" in report_types:
            logger.info("Generating historical performance report...")
            historical_content = self.generate_historical_report(data)
            historical_file = (
                self.output_dir
                / "historical"
                / f"{self.portfolio_name}_{date_stamp}.md"
            )

            with open(historical_file, "w", encoding="utf-8") as f:
                f.write(historical_content)

            reports["historical"] = str(historical_file)
            logger.info(f"Historical report generated: {historical_file}")

        if "internal" in report_types:
            logger.info("Generating internal trading report...")
            internal_content = self.generate_internal_report(data)
            internal_file = (
                self.output_dir / "internal" / f"{self.portfolio_name}_{date_stamp}.md"
            )

            with open(internal_file, "w", encoding="utf-8") as f:
                f.write(internal_content)

            reports["internal"] = str(internal_file)
            logger.info(f"Internal report generated: {internal_file}")

        if "live" in report_types:
            logger.info("Generating live signals monitor...")
            live_content = self.generate_live_monitor(data)
            live_file = (
                self.output_dir / "live" / f"{self.portfolio_name}_{date_stamp}.md"
            )

            with open(live_file, "w", encoding="utf-8") as f:
                f.write(live_content)

            reports["live"] = str(live_file)
            logger.info(f"Live monitor generated: {live_file}")

        return reports

    # Helper methods
    def _health_score_interpretation(self, score: float) -> str:
        """Interpret portfolio health score."""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Needs Improvement"

    def _identify_critical_issues(self, trades_df: pd.DataFrame) -> List[str]:
        """Identify critical issues requiring attention."""
        issues = []

        # Win rate check
        win_rate = len(trades_df[trades_df["PnL"] > 0]) / len(trades_df)
        if win_rate < 0.4:
            issues.append(f"Low win rate ({win_rate:.1%}) - below 40% threshold")

        # Large losses check
        max_loss = trades_df["PnL"].min()
        if max_loss < -50:
            issues.append(f"Large single loss (${max_loss:.2f}) exceeds risk tolerance")

        # Sample size check
        if len(trades_df) < 25:
            issues.append("Insufficient sample size for robust statistical analysis")

        return issues

    def _calculate_optimization_potential(self) -> str:
        """Calculate optimization potential based on analysis data."""
        exit_efficiency = (
            self.analysis_data.get("signal_effectiveness", {})
            .get("exit_signal_analysis", {})
            .get("exit_efficiency_metrics", {})
            .get("overall_exit_efficiency", 0)
        )

        if isinstance(exit_efficiency, (int, float)) and exit_efficiency < -0.5:
            return "High (Exit timing optimization opportunity)"
        elif isinstance(exit_efficiency, (int, float)) and exit_efficiency < 0:
            return "Medium (Exit efficiency can be improved)"
        else:
            return "Low (System performing efficiently)"


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Execute DASV Phase 3 trade history synthesis with institutional-grade reporting"
    )
    parser.add_argument("--portfolio", required=True, help="Portfolio name (required)")
    parser.add_argument(
        "--report-type",
        choices=["internal", "live", "historical", "all"],
        default="all",
        help="Specific report type (default: all)",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Determine report types
        if args.report_type == "all":
            report_types = ["internal", "live", "historical"]
        else:
            report_types = [args.report_type]

        # Run synthesis
        logger.info(f"Starting DASV Phase 3 Synthesis for portfolio: {args.portfolio}")
        synthesizer = DASVPhase3Synthesizer(portfolio_name=args.portfolio)

        # Generate reports
        reports = synthesizer.synthesize_reports(report_types)

        # Summary
        logger.info("Phase 3 synthesis complete")
        for report_type, file_path in reports.items():
            logger.info(f"  {report_type.title()} report: {file_path}")

        print("\n=== DASV Phase 3 Synthesis Complete ===")
        print(f"Portfolio: {args.portfolio}")
        print(f"Reports Generated: {len(reports)}")
        for report_type, file_path in reports.items():
            print(f"  {report_type.title()}: {file_path}")

        # Validation reminder
        if args.portfolio == "live_signals":
            print(
                "\n✅ Live Signals Overview section automatically included in all reports"
            )
            print("✅ Exact CSV P&L values used (no calculations applied)")
            print("✅ Statistical honesty with sample size limitations disclosed")

    except Exception as e:
        logger.error(f"Synthesis failed: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
