#!/usr/bin/env python3
"""
Generalized Fundamental Data Discovery Module
Supports any stock ticker with configurable depth and output options
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd

# Add scripts directory to path for MCP integration
sys.path.insert(0, str(Path(__file__).parent.parent))
from mcp_integration import DataAccessError, MCPDataAccess, MCPIntegrationError


class FundamentalDiscovery:
    """Generalized fundamental data discovery for any stock ticker"""

    def __init__(
        self,
        ticker: str,
        depth: str = "comprehensive",
        output_dir: str = "./data/outputs/fundamental_analysis/discovery",
    ):
        """
        Initialize discovery with configurable parameters

        Args:
            ticker: Stock symbol (e.g., 'AAPL', 'MSFT', 'MA', 'BIIB')
            depth: Analysis depth ('summary', 'standard', 'comprehensive', 'deep-dive')
            output_dir: Directory to save discovery outputs
        """
        self.ticker = ticker.upper()
        self.depth = depth
        self.output_dir = output_dir
        self.timestamp = datetime.now()

        # Initialize MCP data access instead of direct yfinance
        try:
            self.mcp = MCPDataAccess()
            self.fundamentals_data = None
            self.market_data = None
            self.financial_statements = None
        except Exception as e:
            raise MCPIntegrationError(f"Failed to initialize MCP data access: {e}")

    def safe_get(
        self, data: Dict[str, Any], key: str, default: Union[int, float, str] = 0
    ) -> Any:
        """Safely extract value from dictionary with type conversion"""
        value = data.get(key, default)
        if isinstance(value, (np.int64, np.float64)):
            return float(value)
        return value if value is not None else default

    def convert_to_serializable(self, obj: Any) -> Any:
        """Convert various data types to JSON-serializable format"""
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            return (
                obj.to_dict("records")
                if isinstance(obj, pd.DataFrame)
                else obj.to_dict()
            )
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, (list, tuple)):
            return [self.convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {str(k): self.convert_to_serializable(v) for k, v in obj.items()}
        else:
            return obj

    def initialize_data_source(self) -> bool:
        """Initialize MCP data sources and validate ticker"""
        try:
            # Get fundamental data via MCP to validate ticker
            self.fundamentals_data = self.mcp.get_stock_fundamentals(self.ticker)

            # Validate ticker exists by checking for required fields
            if not self.fundamentals_data or not self.fundamentals_data.get("symbol"):
                raise DataAccessError(f"Invalid ticker symbol: {self.ticker}")

            # Load additional data sets
            self.market_data = self.mcp.get_market_data(self.ticker, "1y")
            self.financial_statements = self.mcp.get_financial_statements(self.ticker)

            return True
        except DataAccessError as e:
            print(f"❌ Data access error for {self.ticker}: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error initializing MCP data source for {self.ticker}: {str(e)}")
            return False

    def collect_company_intelligence(self) -> Dict[str, Any]:
        """Collect comprehensive company information"""
        return {
            "name": self.safe_get(
                self.fundamentals_data, "longName", f"{self.ticker} Corporation"
            ),
            "sector": self.safe_get(self.fundamentals_data, "sector", "Unknown"),
            "industry": self.safe_get(self.fundamentals_data, "industry", "Unknown"),
            "country": self.safe_get(self.fundamentals_data, "country", "Unknown"),
            "website": self.safe_get(self.fundamentals_data, "website", ""),
            "employees": self.safe_get(self.fundamentals_data, "fullTimeEmployees", 0),
            "description": self.safe_get(
                self.fundamentals_data, "longBusinessSummary", ""
            ),
            "business_model": {
                "revenue_streams": self._identify_revenue_streams(),
                "operational_model": self._classify_business_model(),
                "confidence": 0.8,  # Confidence in business model identification
            },
        }

    def collect_market_data(self) -> Dict[str, Any]:
        """Collect current market data and trading metrics"""
        return {
            "current_price": self.safe_get(
                self.fundamentals_data,
                "currentPrice",
                self.safe_get(self.fundamentals_data, "regularMarketPrice", 0),
            ),
            "market_cap": self.safe_get(self.fundamentals_data, "marketCap", 0),
            "enterprise_value": self.safe_get(
                self.fundamentals_data, "enterpriseValue", 0
            ),
            "shares_outstanding": self.safe_get(
                self.fundamentals_data, "sharesOutstanding", 0
            ),
            "float_shares": self.safe_get(self.fundamentals_data, "floatShares", 0),
            "beta": self.safe_get(self.fundamentals_data, "beta", 0),
            "52_week_high": self.safe_get(
                self.fundamentals_data, "fiftyTwoWeekHigh", 0
            ),
            "52_week_low": self.safe_get(self.fundamentals_data, "fiftyTwoWeekLow", 0),
            "50_day_avg": self.safe_get(self.fundamentals_data, "fiftyDayAverage", 0),
            "200_day_avg": self.safe_get(
                self.fundamentals_data, "twoHundredDayAverage", 0
            ),
            "volume": self.safe_get(self.fundamentals_data, "volume", 0),
            "avg_volume": self.safe_get(self.fundamentals_data, "averageVolume", 0),
            "confidence": self._calculate_market_data_confidence(),
        }

    def collect_financial_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive financial metrics"""
        metrics = {
            "revenue_ttm": self.safe_get(self.fundamentals_data, "totalRevenue", 0),
            "net_income": self.safe_get(self.fundamentals_data, "netIncomeToCommon", 0),
            "earnings_per_share": self.safe_get(
                self.fundamentals_data, "trailingEps", 0
            ),
            "pe_ratio": self.safe_get(self.fundamentals_data, "trailingPE", 0),
            "profit_margin": self.safe_get(self.fundamentals_data, "profitMargins", 0),
            "return_on_equity": self.safe_get(
                self.fundamentals_data, "returnOnEquity", 0
            ),
            "free_cash_flow": self.safe_get(self.fundamentals_data, "freeCashflow", 0),
            "revenue_growth": self.safe_get(self.fundamentals_data, "revenueGrowth", 0),
            "revenue_per_share": self.safe_get(
                self.fundamentals_data, "revenuePerShare", 0
            ),
            "gross_profit": self.safe_get(self.fundamentals_data, "grossProfits", 0),
            "ebitda": self.safe_get(self.fundamentals_data, "ebitda", 0),
            "forward_eps": self.safe_get(self.fundamentals_data, "forwardEps", 0),
            "forward_pe": self.safe_get(self.fundamentals_data, "forwardPE", 0),
            "peg_ratio": self.safe_get(self.fundamentals_data, "pegRatio", 0),
            "price_to_book": self.safe_get(self.fundamentals_data, "priceToBook", 0),
            "price_to_sales": self.safe_get(
                self.fundamentals_data, "priceToSalesTrailing12Months", 0
            ),
            "ev_to_revenue": self.safe_get(
                self.fundamentals_data, "enterpriseToRevenue", 0
            ),
            "confidence": self._calculate_financial_metrics_confidence(),
        }

        # Add cash position analysis
        cash_breakdown = self._analyze_cash_position()
        metrics.update(cash_breakdown)

        return metrics

    def collect_financial_statements(self) -> Dict[str, Any]:
        """Collect and structure financial statements data"""
        try:
            # Get financial statements via MCP
            if self.financial_statements:
                statements = self.financial_statements
                return {
                    "income_statement": statements.get("income_statement", {}),
                    "balance_sheet": statements.get("balance_sheet", {}),
                    "cash_flow": statements.get("cash_flow", {}),
                    "cash_position_breakdown": self._get_detailed_cash_analysis(),
                    "confidence": self._calculate_statements_confidence(),
                }
            else:
                raise DataAccessError("Financial statements not available")

        except Exception as e:
            print(f"⚠️ Limited financial statements data for {self.ticker}: {str(e)}")
            return {
                "income_statement": {},
                "balance_sheet": {},
                "cash_flow": {},
                "cash_position_breakdown": {},
                "confidence": 0.3,
            }

    def establish_peer_group(self) -> Dict[str, Any]:
        """Establish peer group based on sector and industry"""
        try:
            # This would ideally use a more sophisticated peer identification system
            # For now, provide a framework for peer analysis
            sector = self.safe_get(self.fundamentals_data, "sector", "Unknown")
            industry = self.safe_get(self.fundamentals_data, "industry", "Unknown")

            return {
                "peer_selection_rationale": f"Selected based on {sector} sector and {industry} industry classification",
                "peer_companies": self._get_industry_peers(),
                "comparative_metrics": {},
                "confidence": 0.7,
            }
        except Exception as e:
            print(f"⚠️ Limited peer data available for {self.ticker}: {str(e)}")
            return {
                "peer_selection_rationale": "Limited peer data available",
                "peer_companies": [],
                "comparative_metrics": {},
                "confidence": 0.3,
            }

    def assess_data_quality(self, discovery_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall data quality and completeness"""
        quality_scores = []

        # Market data quality
        market_completeness = len(
            [v for v in discovery_data["market_data"].values() if v != 0]
        ) / len(discovery_data["market_data"])
        quality_scores.append(market_completeness)

        # Financial metrics quality
        financial_completeness = len(
            [v for v in discovery_data["financial_metrics"].values() if v != 0]
        ) / len(discovery_data["financial_metrics"])
        quality_scores.append(financial_completeness)

        # Overall quality assessment
        overall_quality = np.mean(quality_scores)

        return {
            "overall_data_quality": round(overall_quality, 3),
            "source_reliability_scores": {
                "yahoo_finance": 0.85,  # Generally reliable for market data
                "financial_statements": 0.90,  # High reliability for official filings
                "peer_analysis": 0.70,  # Moderate reliability for comparative data
            },
            "data_completeness": round(overall_quality * 100, 1),
            "data_freshness": {
                "market_data": "real-time",
                "financial_statements": "quarterly",
                "peer_data": "periodic",
            },
            "quality_flags": self._identify_quality_issues(discovery_data),
        }

    def execute_discovery(self) -> Dict[str, Any]:
        """Execute complete discovery workflow"""
        print(f"🔍 Starting {self.depth} fundamental discovery for {self.ticker}")

        if not self.initialize_data_source():
            return {"error": f"Failed to initialize data source for {self.ticker}"}

        try:
            # Collect all discovery data
            discovery_data = {
                "metadata": {
                    "command_name": "fundamental_analyst_discover",
                    "execution_timestamp": self.timestamp.isoformat(),
                    "framework_phase": "discover",
                    "ticker": self.ticker,
                    "depth": self.depth,
                    "data_collection_methodology": "systematic_discovery_protocol",
                },
                "company_intelligence": self.collect_company_intelligence(),
                "market_data": self.collect_market_data(),
                "financial_metrics": self.collect_financial_metrics(),
                "financial_statements": self.collect_financial_statements(),
                "peer_group_data": self.establish_peer_group(),
            }

            # Assess data quality
            discovery_data["data_quality_assessment"] = self.assess_data_quality(
                discovery_data
            )

            # Generate discovery insights
            discovery_data["discovery_insights"] = self._generate_insights(
                discovery_data
            )

            # Save discovery data
            self._save_discovery_data(discovery_data)

            print(f"✅ Discovery completed for {self.ticker}")
            return discovery_data

        except Exception as e:
            error_msg = f"Discovery failed for {self.ticker}: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg, "ticker": self.ticker}

    def _identify_revenue_streams(self) -> list:
        """Identify primary revenue streams based on business description"""
        description = self.safe_get(
            self.fundamentals_data, "longBusinessSummary", ""
        ).lower()
        revenue_streams = []

        # Basic revenue stream identification
        if "payment" in description or "transaction" in description:
            revenue_streams.append("Transaction Processing")
        if "subscription" in description or "software" in description:
            revenue_streams.append("Software/Subscription")
        if "product" in description or "manufacturing" in description:
            revenue_streams.append("Product Sales")
        if "service" in description:
            revenue_streams.append("Services")

        return revenue_streams if revenue_streams else ["Business Operations"]

    def _classify_business_model(self) -> str:
        """Classify business model based on industry and description"""
        industry = self.safe_get(self.fundamentals_data, "industry", "").lower()

        if "technology" in industry or "software" in industry:
            return "Technology/Software"
        elif "financial" in industry or "bank" in industry:
            return "Financial Services"
        elif "healthcare" in industry or "pharmaceutical" in industry:
            return "Healthcare/Pharmaceutical"
        elif "retail" in industry:
            return "Retail/Consumer"
        else:
            return "Traditional Business"

    def _calculate_market_data_confidence(self) -> float:
        """Calculate confidence in market data completeness"""
        required_fields = ["currentPrice", "marketCap", "volume"]
        available = sum(
            1
            for field in required_fields
            if self.safe_get(self.fundamentals_data, field, 0) != 0
        )
        return round(available / len(required_fields), 3)

    def _calculate_financial_metrics_confidence(self) -> float:
        """Calculate confidence in financial metrics completeness"""
        key_metrics = [
            "totalRevenue",
            "netIncomeToCommon",
            "trailingEps",
            "profitMargins",
        ]
        available = sum(
            1
            for metric in key_metrics
            if self.safe_get(self.fundamentals_data, metric, 0) != 0
        )
        return round(available / len(key_metrics), 3)

    def _calculate_statements_confidence(self) -> float:
        """Calculate confidence in financial statements availability"""
        try:
            stmt_availability = 0
            if self.financial_statements:
                if self.financial_statements.get("income_statement"):
                    stmt_availability += 1
                if self.financial_statements.get("balance_sheet"):
                    stmt_availability += 1
                if self.financial_statements.get("cash_flow"):
                    stmt_availability += 1
            return round(stmt_availability / 3, 3)
        except:
            return 0.3

    def _analyze_cash_position(self) -> Dict[str, Any]:
        """Analyze cash position and liquid assets"""
        cash_and_equivalents = self.safe_get(self.fundamentals_data, "totalCash", 0)
        short_term_investments = self.safe_get(
            self.fundamentals_data, "shortTermInvestments", 0
        )

        return {
            "cash_and_equivalents": cash_and_equivalents,
            "short_term_investments": short_term_investments,
            "total_liquid_assets": cash_and_equivalents + short_term_investments,
            "cash_ratio": self.safe_get(self.fundamentals_data, "currentRatio", 0),
        }

    def _get_detailed_cash_analysis(self) -> Dict[str, Any]:
        """Get detailed cash position breakdown"""
        return {
            "cash_and_equivalents": self.safe_get(
                self.fundamentals_data, "totalCash", 0
            ),
            "short_term_investments": self.safe_get(
                self.fundamentals_data, "shortTermInvestments", 0
            ),
            "total_liquid_assets": self.safe_get(self.fundamentals_data, "totalCash", 0)
            + self.safe_get(self.fundamentals_data, "shortTermInvestments", 0),
            "investment_portfolio_breakdown": {
                "investments_and_advances": self.safe_get(
                    self.fundamentals_data, "longTermInvestments", 0
                ),
                "definition_note": "investments_and_advances_includes_illiquid_long_term_assets",
            },
        }

    def _get_industry_peers(self) -> list:
        """Get industry peer companies (placeholder for more sophisticated peer identification)"""
        # This would ideally connect to a peer identification service
        industry = self.safe_get(self.fundamentals_data, "industry", "")
        sector = self.safe_get(self.fundamentals_data, "sector", "")

        # Return framework for peer identification
        return [
            {
                "symbol": "PEER1",
                "name": f"Industry Peer in {industry}",
                "rationale": f"Same industry ({industry}) and sector ({sector})",
            }
        ]

    def _identify_quality_issues(self, data: Dict[str, Any]) -> list:
        """Identify potential data quality issues"""
        issues = []

        if data["market_data"]["market_cap"] == 0:
            issues.append("Missing market capitalization data")
        if data["financial_metrics"]["revenue_ttm"] == 0:
            issues.append("Missing revenue data")
        if data["financial_metrics"]["pe_ratio"] == 0:
            issues.append("Missing P/E ratio")

        return issues

    def _generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate initial insights from discovery data"""
        insights = []

        # Market cap insight
        market_cap = data["market_data"]["market_cap"]
        if market_cap > 200_000_000_000:
            insights.append("Mega-cap company with substantial market presence")
        elif market_cap > 10_000_000_000:
            insights.append("Large-cap company with established market position")
        elif market_cap > 2_000_000_000:
            insights.append("Mid-cap company with growth potential")

        # Profitability insight
        profit_margin = data["financial_metrics"]["profit_margin"]
        if profit_margin > 0.20:
            insights.append(
                "High profitability margins indicate strong competitive position"
            )
        elif profit_margin > 0.10:
            insights.append("Moderate profitability with room for improvement")

        return {
            "initial_observations": insights,
            "data_gaps_identified": data["data_quality_assessment"]["quality_flags"],
            "research_priorities": self._identify_research_priorities(data),
            "next_phase_readiness": len(
                data["data_quality_assessment"]["quality_flags"]
            )
            < 3,
        }

    def _identify_research_priorities(self, data: Dict[str, Any]) -> list:
        """Identify priority areas for deeper research"""
        priorities = []

        if data["financial_metrics"]["revenue_growth"] > 0.15:
            priorities.append("Investigate sustainability of high growth rates")
        if data["financial_metrics"]["pe_ratio"] > 30:
            priorities.append("Analyze valuation premium justification")
        if data["peer_group_data"]["confidence"] < 0.5:
            priorities.append("Establish comprehensive peer comparison")

        return priorities

    def _save_discovery_data(self, data: Dict[str, Any]) -> str:
        """Save discovery data to output directory"""
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp_str = self.timestamp.strftime("%Y%m%d")
        filename = f"{self.ticker}_{timestamp_str}_discovery.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

        print(f"💾 Discovery data saved: {filepath}")
        return filepath


def main():
    """Command-line interface for fundamental discovery"""
    parser = argparse.ArgumentParser(
        description="Execute fundamental data discovery for any stock ticker"
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL, MSFT, MA)")
    parser.add_argument(
        "--depth",
        choices=["summary", "standard", "comprehensive", "deep-dive"],
        default="comprehensive",
        help="Analysis depth",
    )
    parser.add_argument(
        "--output-dir",
        default="./data/outputs/fundamental_analysis/discovery",
        help="Output directory for discovery results",
    )

    args = parser.parse_args()

    # Execute discovery
    discovery = FundamentalDiscovery(
        ticker=args.ticker, depth=args.depth, output_dir=args.output_dir
    )

    result = discovery.execute_discovery()

    if "error" in result:
        print(f"❌ Discovery failed: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ Discovery completed successfully for {args.ticker}")
        sys.exit(0)


if __name__ == "__main__":
    main()
