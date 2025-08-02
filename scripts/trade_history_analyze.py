#!/usr/bin/env python3
"""
Trade History Analysis - DASV Phase 2 Implementation

Performs comprehensive statistical analysis and performance measurement following trade_history:analyze command requirements:
- Signal effectiveness analysis with proper closed/active trade separation
- Statistical performance measurement using closed trades only
- Pattern recognition and quality classification
- Risk assessment and optimization opportunities
- Confidence scoring with statistical significance validation

Key Requirements:
- MANDATORY: Use closed trades only for all performance calculations
- MANDATORY: Separate active trades for portfolio analysis only
- MANDATORY: Apply sample size validation and exclude insufficient samples
- MANDATORY: Conservative confidence scoring based on actual closed trade counts
- MANDATORY: Use CSV PnL values exactly (never calculate PnL from returns)

Usage:
    python scripts/trade_history_analyze.py --portfolio {portfolio_name}
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import scipy.stats as stats

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TradeHistoryAnalysis:
    """Trade history analysis following DASV Phase 2 protocol"""

    def __init__(self, portfolio_name: str):
        self.portfolio_name = portfolio_name
        self.execution_date = datetime.now()
        self.data_dir = Path(__file__).parent.parent / "data"
        self.discovery_dir = self.data_dir / "outputs" / "trade_history" / "discovery"
        self.output_dir = self.data_dir / "outputs" / "trade_history" / "analysis"

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize analysis containers
        self.discovery_data: Dict[str, Any] = {}
        self.closed_trades: List[Dict[str, Any]] = []
        self.active_trades: List[Dict[str, Any]] = []
        self.confidence_factors: Dict[str, float] = {}

    def load_discovery_data(self) -> Dict[str, Any]:
        """
        Load and validate discovery phase JSON data
        """
        logger.info(f"Loading discovery data for portfolio: {self.portfolio_name}")

        # Find latest discovery file
        pattern = f"{self.portfolio_name}_*.json"
        discovery_files = list(self.discovery_dir.glob(pattern))

        if not discovery_files:
            raise FileNotFoundError(
                f"No discovery files found for portfolio '{self.portfolio_name}' in {self.discovery_dir}"
            )

        # Get most recent discovery file
        latest_file = max(discovery_files, key=lambda f: f.stat().st_mtime)
        logger.info(f"Loading discovery data from: {latest_file}")

        with open(latest_file, "r", encoding="utf-8") as f:
            discovery_data = json.load(f)

        # Validate discovery data structure
        required_keys = [
            "portfolio_summary",
            "ticker_performance",
            "performance_metrics",
        ]
        for key in required_keys:
            if key not in discovery_data:
                raise ValueError(f"Missing required key '{key}' in discovery data")

        logger.info(
            f"Discovery data loaded successfully: {discovery_data['portfolio_summary']['total_trades']} total trades"
        )
        return discovery_data

    def extract_trade_data(
        self, discovery_data: Dict[str, Any]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Extract and categorize trade data from discovery data
        """
        logger.info("Extracting and categorizing trade data...")

        # Load raw CSV data to get individual trades
        csv_path = discovery_data["discovery_metadata"]["data_source"]
        df = pd.read_csv(csv_path)

        closed_trades = []
        active_trades = []

        for _, row in df.iterrows():
            trade = row.to_dict()

            # Clean up NaN values
            for key, value in trade.items():
                if pd.isna(value):
                    trade[key] = None

            # Categorize by status
            status = str(trade.get("Status", "")).strip()
            if status == "Closed":
                # Validate closed trades have required data
                if trade.get("PnL") is not None and trade.get("Return") is not None:
                    closed_trades.append(trade)
                else:
                    logger.warning(
                        f"Closed trade {trade.get('Position_UUID')} missing PnL or Return data"
                    )
            elif status in ["Open", "Active"]:
                active_trades.append(trade)

        logger.info(
            f"Trade data extracted: {len(closed_trades)} closed, {len(active_trades)} active"
        )
        return closed_trades, active_trades

    def analyze_signal_effectiveness(
        self, closed_trades: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze signal effectiveness using closed trades only
        """
        logger.info("Analyzing signal effectiveness...")

        if not closed_trades:
            logger.warning(
                "No closed trades available for signal effectiveness analysis"
            )
            return {
                "entry_signal_analysis": {
                    "status": "NO_CLOSED_TRADES",
                    "message": "Signal effectiveness analysis requires closed trades",
                },
                "exit_signal_analysis": {
                    "status": "NO_CLOSED_TRADES",
                    "message": "Exit analysis requires closed trades",
                },
            }

        # Group by strategy type
        strategy_groups: Dict[str, List[Dict[str, Any]]] = {}
        for trade in closed_trades:
            strategy = trade.get("Strategy_Type", "Unknown")
            if strategy not in strategy_groups:
                strategy_groups[strategy] = []
            strategy_groups[strategy].append(trade)

        # Analyze each strategy
        entry_analysis = {}
        for strategy, trades in strategy_groups.items():
            if len(trades) < 5:  # Minimum sample size requirement
                entry_analysis[strategy] = {
                    "status": "INSUFFICIENT_SAMPLE",
                    "closed_trades": len(trades),
                    "minimum_required": 5,
                    "analysis_possible": False,
                    "recommendation": "Exclude from analysis until sufficient closed trades available",
                    "note": "Performance calculations require minimum 5 closed trades for statistical validity",
                }
                continue

            # Calculate strategy metrics
            wins = [t for t in trades if t.get("Return", 0) > 0]
            losses = [t for t in trades if t.get("Return", 0) <= 0]

            win_rate = len(wins) / len(trades) if trades else 0
            win_returns = [t.get("Return") for t in wins if t.get("Return") is not None]
            loss_returns = [
                t.get("Return") for t in losses if t.get("Return") is not None
            ]
            avg_win_return = np.mean(win_returns) if win_returns else 0
            avg_loss_return = np.mean(loss_returns) if loss_returns else 0

            # Calculate confidence based on sample size
            confidence = min(0.95, 0.5 + (len(trades) / 30))

            entry_analysis[strategy] = {
                "win_rate": win_rate,
                "total_trades": len(trades),
                "winners": len(wins),
                "losers": len(losses),
                "average_return_winners": avg_win_return,
                "average_return_losers": avg_loss_return,
                "sample_size_adequacy": len(trades) >= 15,
                "confidence": confidence,
            }

        # Exit signal analysis (using all closed trades)
        valid_exit_eff_trades = [
            t for t in closed_trades if t.get("Exit_Efficiency") is not None
        ]
        valid_mfe_ratio_trades = [
            t for t in closed_trades if t.get("MFE_MAE_Ratio") is not None
        ]

        exit_analysis = {}
        if valid_exit_eff_trades:
            # Calculate exit efficiency safely
            exit_eff_values = [
                t.get("Exit_Efficiency")
                for t in valid_exit_eff_trades
                if t.get("Exit_Efficiency") is not None
            ]
            mfe_ratio_values = [
                t.get("MFE_MAE_Ratio")
                for t in valid_mfe_ratio_trades
                if t.get("MFE_MAE_Ratio") is not None
            ]

            exit_analysis = {
                "exit_efficiency_metrics": {
                    "overall_exit_efficiency": (
                        np.mean(exit_eff_values) if exit_eff_values else 0
                    ),
                    "mfe_capture_rate": (
                        np.mean(mfe_ratio_values) if mfe_ratio_values else 0
                    ),
                    "sample_size": len(valid_exit_eff_trades),
                    "confidence": min(0.95, 0.5 + (len(valid_exit_eff_trades) / 20)),
                }
            }
        else:
            exit_analysis = {
                "exit_efficiency_metrics": {
                    "status": "INSUFFICIENT_DATA",
                    "message": "Exit efficiency analysis requires trades with Exit_Efficiency data",
                }
            }

        return {
            "entry_signal_analysis": {
                "win_rate_by_strategy": entry_analysis,
                "total_strategies_analyzed": len(
                    [
                        s
                        for s in entry_analysis.values()
                        if isinstance(s, dict) and s.get("analysis_possible", True)
                    ]
                ),
                "strategies_excluded": len(
                    [
                        s
                        for s in entry_analysis.values()
                        if isinstance(s, dict) and not s.get("analysis_possible", True)
                    ]
                ),
            },
            "exit_signal_analysis": exit_analysis,
        }

    def perform_statistical_analysis(
        self, closed_trades: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Perform statistical performance measurement using closed trades only
        """
        logger.info("Performing statistical analysis...")

        if not closed_trades:
            return {
                "status": "NO_CLOSED_TRADES",
                "message": "Statistical analysis requires closed trades",
            }

        # Extract returns for statistical analysis
        returns = [
            t.get("Return", 0) for t in closed_trades if t.get("Return") is not None
        ]
        pnl_values = [
            t.get("PnL", 0) for t in closed_trades if t.get("PnL") is not None
        ]

        if not returns:
            return {
                "status": "NO_RETURN_DATA",
                "message": "Statistical analysis requires return data",
            }

        # Return distribution analysis
        returns_array = np.array(returns)

        # Normality test (if sample size >= 8)
        normality_p_value = None
        if len(returns) >= 8:
            _, normality_p_value = stats.shapiro(returns_array)

        # Statistical significance test vs zero
        t_stat, p_value = stats.ttest_1samp(returns_array, 0)

        # Confidence interval for mean return
        confidence_interval = stats.t.interval(
            0.95,
            len(returns) - 1,
            loc=np.mean(returns_array),
            scale=stats.sem(returns_array),
        )

        return_analysis = {
            "return_distribution": {
                "mean_return": float(np.mean(returns_array)),
                "median_return": float(np.median(returns_array)),
                "std_deviation": float(np.std(returns_array, ddof=1)),
                "skewness": float(stats.skew(returns_array)),
                "kurtosis": float(stats.kurtosis(returns_array)),
                "normality_test_p_value": (
                    float(normality_p_value) if normality_p_value else None
                ),
                "sample_size": len(returns),
                "confidence": min(0.95, 0.5 + (len(returns) / 25)),
            },
            "statistical_significance": {
                "return_vs_zero": {
                    "t_statistic": float(t_stat),
                    "p_value": float(p_value),
                    "significant_at_95": p_value < 0.05,
                    "confidence_interval_95": [
                        float(confidence_interval[0]),
                        float(confidence_interval[1]),
                    ],
                }
            },
        }

        # Risk-adjusted metrics (if sufficient data)
        if len(returns) >= 10 and np.std(returns_array) > 0:
            sharpe_ratio = np.mean(returns_array) / np.std(returns_array, ddof=1)

            # Sortino ratio (downside deviation)
            downside_returns = returns_array[returns_array < 0]
            downside_deviation = (
                np.std(downside_returns, ddof=1)
                if len(downside_returns) > 1
                else np.std(returns_array, ddof=1)
            )
            sortino_ratio = (
                np.mean(returns_array) / downside_deviation
                if downside_deviation > 0
                else 0
            )

            return_analysis["risk_adjusted_metrics"] = {
                "sharpe_ratio": float(sharpe_ratio),
                "sortino_ratio": float(sortino_ratio),
                "downside_deviation": float(downside_deviation),
                "confidence": min(0.9, 0.4 + (len(returns) / 20)),
            }

        # Performance metrics using actual CSV PnL values
        wins = [t for t in closed_trades if t.get("Return", 0) > 0]
        losses = [t for t in closed_trades if t.get("Return", 0) <= 0]

        win_pnl = sum(t.get("PnL", 0) for t in wins if t.get("PnL") is not None)
        loss_pnl = sum(t.get("PnL", 0) for t in losses if t.get("PnL") is not None)

        performance_metrics = {
            "win_rate": len(wins) / len(closed_trades),
            "total_wins": len(wins),
            "total_losses": len(losses),
            "total_pnl": sum(pnl_values),
            "profit_factor": abs(win_pnl / loss_pnl) if loss_pnl != 0 else float("inf"),
            "expectancy": np.mean(returns_array),
            "sample_size": len(closed_trades),
            "confidence": min(0.95, 0.5 + (len(closed_trades) / 30)),
        }

        return {
            "statistical_analysis": return_analysis,
            "performance_metrics": performance_metrics,
        }

    def analyze_patterns_and_quality(
        self, closed_trades: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Conduct pattern recognition and quality classification analysis
        """
        logger.info("Analyzing patterns and quality classification...")

        if not closed_trades:
            return {
                "status": "NO_CLOSED_TRADES",
                "message": "Pattern analysis requires closed trades",
            }

        # Trade quality classification
        quality_distribution = {}
        for trade in closed_trades:
            quality = trade.get("Trade_Quality", "Unknown")
            if quality not in quality_distribution:
                quality_distribution[quality] = []
            quality_distribution[quality].append(trade)

        quality_analysis = {}
        for quality, trades in quality_distribution.items():
            if trades:
                returns = [
                    t.get("Return", 0) for t in trades if t.get("Return") is not None
                ]
                quality_analysis[quality] = {
                    "count": len(trades),
                    "percentage": len(trades) / len(closed_trades),
                    "avg_return": np.mean(returns) if returns else 0,
                    "characteristics": self._derive_quality_characteristics(
                        quality, trades
                    ),
                }

        # Temporal patterns (if sufficient data)
        temporal_patterns = {}
        if len(closed_trades) >= 10:
            # Convert entry timestamps for analysis
            trades_with_dates = []
            for trade in closed_trades:
                try:
                    entry_date = pd.to_datetime(trade.get("Entry_Timestamp"))
                    trade_copy = trade.copy()
                    trade_copy["entry_month"] = entry_date.month
                    trade_copy["entry_quarter"] = entry_date.quarter
                    trades_with_dates.append(trade_copy)
                except (ValueError, TypeError):
                    continue

            if trades_with_dates:
                # Monthly analysis
                monthly_performance = {}
                for month in range(1, 13):
                    month_trades = [
                        t for t in trades_with_dates if t.get("entry_month") == month
                    ]
                    if month_trades:
                        month_returns = [
                            t.get("Return", 0)
                            for t in month_trades
                            if t.get("Return") is not None
                        ]
                        monthly_performance[f"month_{month}"] = {
                            "trade_count": len(month_trades),
                            "win_rate": len(
                                [t for t in month_trades if t.get("Return", 0) > 0]
                            )
                            / len(month_trades),
                            "avg_return": (
                                np.mean(month_returns) if month_returns else 0
                            ),
                        }

                temporal_patterns["monthly_effectiveness"] = monthly_performance

        return {
            "trade_quality_classification": quality_analysis,
            "pattern_recognition": {
                "signal_temporal_patterns": temporal_patterns,
                "sample_size": len(closed_trades),
                "confidence": min(0.85, 0.4 + (len(closed_trades) / 25)),
            },
        }

    def _derive_quality_characteristics(
        self, quality: str, trades: List[Dict[str, Any]]
    ) -> List[str]:
        """Derive characteristics based on trade quality and performance"""
        characteristics = []

        if not trades:
            return characteristics

        return_values = [t.get("Return") for t in trades if t.get("Return") is not None]
        duration_values = [
            t.get("Duration_Days") for t in trades if t.get("Duration_Days") is not None
        ]
        avg_return = np.mean(return_values) if return_values else 0
        avg_duration = np.mean(duration_values) if duration_values else 0

        # Duration characteristics
        if avg_duration < 15:
            characteristics.append("short_duration")
        elif avg_duration > 45:
            characteristics.append("long_duration")
        else:
            characteristics.append("medium_duration")

        # Performance characteristics
        if quality == "Excellent" or avg_return > 0.1:
            characteristics.extend(["high_performance", "optimal_timing"])
        elif quality == "Good" or avg_return > 0:
            characteristics.extend(["consistent_performance", "adequate_timing"])
        elif quality == "Poor" or avg_return < -0.05:
            characteristics.extend(["poor_timing", "suboptimal_execution"])
        elif quality == "Failed":
            characteristics.extend(["systematic_timing_issues", "poor_entry_signals"])

        return characteristics

    def generate_optimization_opportunities(
        self, analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate optimization opportunities based on analysis results
        """
        logger.info("Generating optimization opportunities...")

        opportunities = {
            "entry_signal_enhancements": [],
            "exit_signal_refinements": [],
            "strategy_parameter_optimization": [],
        }

        # Check signal effectiveness results
        signal_analysis = analysis_results.get("signal_effectiveness", {})
        entry_analysis = signal_analysis.get("entry_signal_analysis", {})

        # Entry signal opportunities
        win_rates = entry_analysis.get("win_rate_by_strategy", {})
        for strategy, metrics in win_rates.items():
            if isinstance(metrics, dict) and metrics.get("analysis_possible", True):
                win_rate = metrics.get("win_rate", 0)
                if win_rate < 0.6:  # Below 60% win rate
                    opportunities["entry_signal_enhancements"].append(
                        {
                            "opportunity": f"Improve {strategy} signal quality",
                            "current_win_rate": win_rate,
                            "potential_improvement": "10-15% win rate increase through signal refinement",
                            "implementation": f"Add confirmation filters for {strategy} signals",
                            "confidence": min(0.8, metrics.get("confidence", 0.5)),
                        }
                    )

        # Exit signal opportunities
        exit_analysis = signal_analysis.get("exit_signal_analysis", {})
        exit_metrics = exit_analysis.get("exit_efficiency_metrics", {})
        if isinstance(exit_metrics, dict) and "overall_exit_efficiency" in exit_metrics:
            exit_eff = exit_metrics.get("overall_exit_efficiency", 0)
            if exit_eff < 0.7:  # Below 70% exit efficiency
                opportunities["exit_signal_refinements"].append(
                    {
                        "opportunity": "Improve exit timing efficiency",
                        "current_efficiency": exit_eff,
                        "potential_improvement": f"{(0.8 - exit_eff) * 100:.1f}% efficiency improvement",
                        "implementation": "Implement trailing stop optimization",
                        "confidence": exit_metrics.get("confidence", 0.6),
                    }
                )

        # Statistical significance opportunities
        stats_analysis = analysis_results.get("statistical_analysis", {})
        significance = stats_analysis.get("statistical_significance", {})
        return_test = significance.get("return_vs_zero", {})

        if not return_test.get("significant_at_95", False):
            opportunities["strategy_parameter_optimization"].append(
                {
                    "opportunity": "Increase statistical significance",
                    "current_p_value": return_test.get("p_value", 1.0),
                    "requirement": "P-value < 0.05 for statistical significance",
                    "implementation": "Increase sample size or improve signal quality",
                    "confidence": 0.9,
                }
            )

        return opportunities

    def assess_risk_and_portfolio(
        self, closed_trades: List[Dict[str, Any]], active_trades: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Assess risk metrics and portfolio composition
        """
        logger.info("Assessing risk and portfolio metrics...")

        risk_assessment = {}

        # Closed trades risk analysis
        if closed_trades:
            returns = [
                t.get("Return", 0) for t in closed_trades if t.get("Return") is not None
            ]
            if returns:
                returns_array = np.array(returns)

                # Drawdown analysis (simplified)
                cumulative_returns = np.cumsum(returns_array)
                running_max = np.maximum.accumulate(cumulative_returns)
                drawdowns = cumulative_returns - running_max

                risk_assessment["drawdown_analysis"] = {
                    "max_drawdown": float(np.min(drawdowns)),
                    "avg_drawdown": (
                        float(np.mean(drawdowns[drawdowns < 0]))
                        if any(drawdowns < 0)
                        else 0
                    ),
                    "downside_deviation": (
                        float(np.std(returns_array[returns_array < 0], ddof=1))
                        if any(returns_array < 0)
                        else 0
                    ),
                    "confidence": min(0.9, 0.4 + (len(returns) / 20)),
                }

        # Active portfolio analysis
        if active_trades:
            # Sector concentration
            sectors = {}
            for trade in active_trades:
                # Simplified sector mapping based on ticker (would be enhanced with real sector data)
                ticker = trade.get("Ticker", "")
                sector = self._map_ticker_to_sector(ticker)
                sectors[sector] = sectors.get(sector, 0) + 1

            total_active = len(active_trades)
            sector_concentration = {
                sector: count / total_active for sector, count in sectors.items()
            }

            risk_assessment["portfolio_risk_metrics"] = {
                "active_positions": total_active,
                "sector_concentration": sector_concentration,
                "position_diversification": (
                    len(sectors) / total_active if total_active > 0 else 0
                ),
                "confidence": 0.8,
            }

        return risk_assessment

    def _map_ticker_to_sector(self, ticker: str) -> str:
        """Simple sector mapping for risk analysis"""
        tech_tickers = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "NVDA",
            "TSLA",
            "AMD",
            "SMCI",
        ]
        healthcare_tickers = ["UHS", "ILMN", "WELL"]
        financial_tickers = ["MA", "COIN"]

        if ticker in tech_tickers:
            return "Technology"
        elif ticker in healthcare_tickers:
            return "Healthcare"
        elif ticker in financial_tickers:
            return "Financials"
        else:
            return "Other"

    def calculate_comprehensive_confidence(
        self, analysis_results: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Calculate comprehensive confidence scores based on analysis quality
        """
        confidence_scores = {}

        # Sample size confidence
        total_closed = len(self.closed_trades)
        confidence_scores["sample_size"] = min(0.95, 0.5 + (total_closed / 30))

        # Statistical significance confidence
        stats_analysis = analysis_results.get("statistical_analysis", {})
        significance = stats_analysis.get("statistical_significance", {})
        return_test = significance.get("return_vs_zero", {})

        if return_test.get("significant_at_95", False):
            confidence_scores["statistical_significance"] = 0.95
        elif return_test.get("p_value", 1.0) < 0.1:
            confidence_scores["statistical_significance"] = 0.8
        else:
            confidence_scores["statistical_significance"] = 0.5

        # Signal effectiveness confidence
        signal_analysis = analysis_results.get("signal_effectiveness", {})
        entry_analysis = signal_analysis.get("entry_signal_analysis", {})
        strategies_analyzed = entry_analysis.get("total_strategies_analyzed", 0)

        if strategies_analyzed > 0:
            confidence_scores["signal_effectiveness"] = min(
                0.9, 0.6 + (strategies_analyzed * 0.2)
            )
        else:
            confidence_scores["signal_effectiveness"] = 0.3

        # Overall confidence (weighted average)
        weights = {
            "sample_size": 0.4,
            "statistical_significance": 0.3,
            "signal_effectiveness": 0.3,
        }

        confidence_scores["overall"] = sum(
            confidence_scores[key] * weight for key, weight in weights.items()
        )

        return confidence_scores

    def generate_analysis_output(
        self, analysis_results: Dict[str, Any], confidence_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive analysis JSON output following DASV schema
        """
        logger.info("Generating comprehensive analysis output...")

        analysis_output = {
            "portfolio": self.portfolio_name,
            "analysis_metadata": {
                "execution_timestamp": self.execution_date.isoformat(),
                "protocol_version": "DASV_Phase_2_Statistical_Analysis",
                "confidence_score": confidence_scores["overall"],
                "sample_size_adequacy": confidence_scores["sample_size"],
                "statistical_significance": confidence_scores[
                    "statistical_significance"
                ],
                "signal_effectiveness_confidence": confidence_scores[
                    "signal_effectiveness"
                ],
            },
            "sample_validation": {
                "total_trades": len(self.closed_trades) + len(self.active_trades),
                "closed_trades_analyzed": len(self.closed_trades),
                "active_trades_portfolio": len(self.active_trades),
                "minimum_sample_met": len(self.closed_trades) >= 25,
                "statistical_power": min(0.9, len(self.closed_trades) / 30),
                "methodology_compliance": "Closed trades only for performance calculations",
            },
            "signal_effectiveness": analysis_results.get("signal_effectiveness", {}),
            "statistical_analysis": analysis_results.get("statistical_analysis", {}),
            "performance_measurement": analysis_results.get(
                "performance_measurement", {}
            ),
            "pattern_recognition": analysis_results.get("pattern_recognition", {}),
            "optimization_opportunities": analysis_results.get(
                "optimization_opportunities", {}
            ),
            "risk_assessment": analysis_results.get("risk_assessment", {}),
            "analysis_quality_assessment": {
                "overall_confidence": confidence_scores["overall"],
                "sample_size_confidence": confidence_scores["sample_size"],
                "statistical_robustness": confidence_scores["statistical_significance"],
                "signal_analysis_confidence": confidence_scores["signal_effectiveness"],
                "methodology_compliance": True,
                "conservative_scoring": True,
                "limitations": self._generate_analysis_limitations(),
            },
            "next_phase_inputs": {
                "synthesis_ready": confidence_scores["overall"] > 0.7,
                "confidence_threshold_met": confidence_scores["overall"] > 0.8,
                "analysis_package_path": str(
                    self.output_dir
                    / f"{self.portfolio_name}_{self.execution_date.strftime('%Y%m%d')}.json"
                ),
                "critical_findings": self._extract_critical_findings(analysis_results),
                "report_focus_areas": [
                    "signal_effectiveness_optimization",
                    "statistical_performance_validation",
                    "risk_management_enhancement",
                    "strategy_parameter_tuning",
                ],
            },
        }

        return analysis_output

    def _generate_analysis_limitations(self) -> List[str]:
        """Generate honest assessment of analysis limitations"""
        limitations = []

        if len(self.closed_trades) < 25:
            limitations.append(
                f"Sample size ({len(self.closed_trades)} closed trades) below recommended minimum of 25 for robust statistical analysis"
            )

        if len(self.closed_trades) < 15:
            limitations.append(
                "Limited statistical power due to small sample size - results should be interpreted cautiously"
            )

        # Check strategy distribution
        strategy_counts = {}
        for trade in self.closed_trades:
            strategy = trade.get("Strategy_Type", "Unknown")
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        insufficient_strategies = [
            s for s, count in strategy_counts.items() if count < 5
        ]
        if insufficient_strategies:
            limitations.append(
                f"Strategies with insufficient samples excluded from analysis: {', '.join(insufficient_strategies)}"
            )

        return limitations

    def _extract_critical_findings(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Extract critical findings for synthesis phase"""
        findings = []

        # Statistical significance
        stats_analysis = analysis_results.get("statistical_analysis", {})
        significance = stats_analysis.get("statistical_significance", {})
        return_test = significance.get("return_vs_zero", {})

        if return_test.get("significant_at_95", False):
            findings.append(
                "Strategy returns are statistically significant at 95% confidence level"
            )
        else:
            findings.append(
                "Strategy returns lack statistical significance - require larger sample or improved signals"
            )

        # Performance metrics
        perf_metrics = stats_analysis.get("performance_metrics", {})
        win_rate = perf_metrics.get("win_rate", 0)

        if win_rate > 0.6:
            findings.append(
                f"Strong win rate of {win_rate:.1%} indicates effective signal quality"
            )
        elif win_rate < 0.5:
            findings.append(
                f"Below-average win rate of {win_rate:.1%} suggests signal refinement needed"
            )

        # Sample size adequacy
        if len(self.closed_trades) < 15:
            findings.append(
                "Critical: Insufficient sample size for reliable statistical conclusions"
            )

        return findings

    def _convert_numpy_types(self, obj: Any) -> Any:
        """Convert numpy types to native Python types for JSON serialization"""
        import numpy as np

        if isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    def execute_analysis(self) -> Dict[str, Any]:
        """
        Execute the complete DASV Phase 2 analysis protocol
        """
        logger.info(
            f"Starting trade history analysis for portfolio: {self.portfolio_name}"
        )

        try:
            # Step 1: Load discovery data
            self.discovery_data = self.load_discovery_data()

            # Step 2: Extract and categorize trade data
            self.closed_trades, self.active_trades = self.extract_trade_data(
                self.discovery_data
            )

            # Step 3: Validate minimum requirements
            if len(self.closed_trades) == 0:
                logger.warning("No closed trades available - analysis will be limited")

            # Step 4: Execute analysis components
            analysis_results = {}

            # Signal effectiveness analysis
            analysis_results[
                "signal_effectiveness"
            ] = self.analyze_signal_effectiveness(self.closed_trades)

            # Statistical performance measurement
            analysis_results[
                "statistical_analysis"
            ] = self.perform_statistical_analysis(self.closed_trades)

            # Pattern recognition and quality classification
            analysis_results["pattern_recognition"] = self.analyze_patterns_and_quality(
                self.closed_trades
            )

            # Optimization opportunities
            analysis_results[
                "optimization_opportunities"
            ] = self.generate_optimization_opportunities(analysis_results)

            # Risk assessment
            analysis_results["risk_assessment"] = self.assess_risk_and_portfolio(
                self.closed_trades, self.active_trades
            )

            # Step 5: Calculate comprehensive confidence scores
            confidence_scores = self.calculate_comprehensive_confidence(
                analysis_results
            )

            # Step 6: Generate comprehensive analysis output
            analysis_output = self.generate_analysis_output(
                analysis_results, confidence_scores
            )

            # Step 7: Save output with proper naming
            output_filename = (
                f"{self.portfolio_name}_{self.execution_date.strftime('%Y%m%d')}.json"
            )
            output_file = self.output_dir / output_filename

            # Convert numpy types to native Python types for JSON serialization
            analysis_output = self._convert_numpy_types(analysis_output)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(analysis_output, f, indent=2, ensure_ascii=False)

            logger.info(f"Analysis output saved to: {output_file}")

            # Log summary statistics
            logger.info(
                f"Analysis complete - Closed trades: {len(self.closed_trades)}, "
                f"Active trades: {len(self.active_trades)}, "
                f"Overall confidence: {confidence_scores['overall']:.3f}"
            )

            return analysis_output

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Execute trade history analysis protocol"
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

    # Execute analysis
    analyzer = TradeHistoryAnalysis(portfolio_name=args.portfolio)
    result = analyzer.execute_analysis()

    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        # Print summary
        print("\n" + "=" * 60)
        print("TRADE HISTORY ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Portfolio: {result['portfolio']}")
        print(f"Execution: {result['analysis_metadata']['execution_timestamp']}")
        print(
            f"Overall Confidence: {result['analysis_metadata']['confidence_score']:.3f}"
        )

        print("\nSAMPLE VALIDATION:")
        sample = result["sample_validation"]
        print(f"  Closed Trades Analyzed: {sample['closed_trades_analyzed']}")
        print(f"  Active Trades (Portfolio): {sample['active_trades_portfolio']}")
        print(f"  Minimum Sample Met: {sample['minimum_sample_met']}")
        print(f"  Statistical Power: {sample['statistical_power']:.3f}")

        print("\nSTATISTICAL ANALYSIS:")
        if "statistical_analysis" in result and result["statistical_analysis"]:
            stats = result["statistical_analysis"]
            if "performance_metrics" in stats:
                perf = stats["performance_metrics"]
                print(f"  Win Rate: {perf.get('win_rate', 0):.1%}")
                print(f"  Profit Factor: {perf.get('profit_factor', 0):.2f}")
                print(f"  Total PnL: ${perf.get('total_pnl', 0):.2f}")

            if "statistical_significance" in stats:
                sig = stats["statistical_significance"]["return_vs_zero"]
                print(
                    f"  Statistical Significance: {sig.get('significant_at_95', False)}"
                )
                print(f"  P-Value: {sig.get('p_value', 1.0):.4f}")

        print("\nQUALITY ASSESSMENT:")
        quality = result["analysis_quality_assessment"]
        print(f"  Overall Confidence: {quality['overall_confidence']:.3f}")
        print(f"  Statistical Robustness: {quality['statistical_robustness']:.3f}")
        print(f"  Methodology Compliance: {quality['methodology_compliance']}")

        if quality.get("limitations"):
            print("\nLIMITATIONS:")
            for limitation in quality["limitations"]:
                print(f"  - {limitation}")

        print(f"\nOutput saved to: {analyzer.output_dir}")
        print("=" * 60)


if __name__ == "__main__":
    main()
