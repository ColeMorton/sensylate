#!/usr/bin/env python3
"""
Generalized Fundamental Analysis Module
Performs systematic financial analysis on discovery data for any ticker
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class FundamentalAnalyzer:
    """Generalized fundamental analysis for any stock discovery data"""

    def __init__(
        self,
        ticker: str,
        discovery_data: Optional[Dict[str, Any]] = None,
        output_dir: str = "./team-workspace/data/outputs/fundamental_analysis/analysis",
    ):
        """
        Initialize analyzer with configurable parameters

        Args:
            ticker: Stock symbol (e.g., 'AAPL', 'MSFT', 'MA', 'BIIB')
            discovery_data: Optional discovery data dict, will load from file if None
            output_dir: Directory to save analysis outputs
        """
        self.ticker = ticker.upper()
        self.discovery_data = discovery_data
        self.output_dir = output_dir
        self.timestamp = datetime.now()

        # Industry-specific benchmarks for scoring
        self.industry_benchmarks = {
            "technology": {"profit_margin": 0.25, "roe": 0.30, "revenue_growth": 0.20},
            "financial_services": {
                "profit_margin": 0.30,
                "roe": 0.50,
                "revenue_growth": 0.15,
            },
            "healthcare": {"profit_margin": 0.20, "roe": 0.25, "revenue_growth": 0.15},
            "consumer": {"profit_margin": 0.15, "roe": 0.20, "revenue_growth": 0.10},
            "default": {"profit_margin": 0.15, "roe": 0.20, "revenue_growth": 0.10},
        }

    def load_discovery_data(self, discovery_file_path: Optional[str] = None) -> bool:
        """Load discovery data from file if not provided"""
        if self.discovery_data is not None:
            return True

        if discovery_file_path is None:
            # Try to find discovery file with today's date
            today = self.timestamp.strftime("%Y%m%d")
            discovery_dir = (
                "./team-workspace/data/outputs/fundamental_analysis/discovery"
            )
            discovery_file_path = os.path.join(
                discovery_dir, f"{self.ticker}_{today}_discovery.json"
            )

        try:
            if os.path.exists(discovery_file_path):
                with open(discovery_file_path, "r") as f:
                    self.discovery_data = json.load(f)
                print(f"📂 Loaded discovery data from: {discovery_file_path}")
                return True
            else:
                print(f"❌ Discovery file not found: {discovery_file_path}")
                return False
        except Exception as e:
            print(f"❌ Error loading discovery data: {str(e)}")
            return False

    def get_industry_benchmarks(self) -> Dict[str, float]:
        """Get industry-specific benchmarks for analysis"""
        if not self.discovery_data:
            return self.industry_benchmarks["default"]

        industry = (
            self.discovery_data.get("company_intelligence", {})
            .get("industry", "")
            .lower()
        )

        for key, benchmarks in self.industry_benchmarks.items():
            if key in industry:
                return benchmarks

        return self.industry_benchmarks["default"]

    def analyze_financial_health(self) -> Dict[str, Any]:
        """Comprehensive 4-dimensional financial health scorecard"""
        if not self.discovery_data:
            raise ValueError("Discovery data not available for analysis")

        metrics = self.discovery_data.get("financial_metrics", {})
        benchmarks = self.get_industry_benchmarks()

        # 1. Profitability Score (0-1)
        profitability_scores = []

        # Net profit margin
        net_margin = metrics.get("profit_margin", 0)
        profitability_scores.append(min(net_margin / benchmarks["profit_margin"], 1.0))

        # ROE
        roe = metrics.get("return_on_equity", 0)
        profitability_scores.append(min(roe / benchmarks["roe"], 1.0))

        # Operating margin (estimated from gross profit if available)
        gross_profit = metrics.get("gross_profit", 0)
        revenue = metrics.get("revenue_ttm", 1)
        operating_margin = (gross_profit / revenue) if revenue > 0 else 0
        profitability_scores.append(
            min(operating_margin / (benchmarks["profit_margin"] * 1.3), 1.0)
        )

        profitability_score = np.mean(profitability_scores)

        # 2. Growth Score (0-1)
        growth_scores = []

        # Revenue growth
        rev_growth = metrics.get("revenue_growth", 0)
        growth_scores.append(min(rev_growth / benchmarks["revenue_growth"], 1.0))

        # Earnings growth (estimated from forward metrics)
        forward_eps = metrics.get("forward_eps", 0)
        trailing_eps = metrics.get("earnings_per_share", 0)
        earnings_growth = (
            ((forward_eps - trailing_eps) / trailing_eps) if trailing_eps > 0 else 0
        )
        growth_scores.append(min(earnings_growth / benchmarks["revenue_growth"], 1.0))

        growth_score = np.mean(growth_scores)

        # 3. Financial Stability Score (0-1)
        stability_scores = []

        # Cash position strength
        cash_ratio = metrics.get("cash_ratio", 0)
        stability_scores.append(min(cash_ratio / 2.0, 1.0))  # 2.0 is excellent

        # Debt management (using P/E as proxy for leverage in absence of debt ratios)
        pe_ratio = metrics.get("pe_ratio", 0)
        if pe_ratio > 0:
            # Lower P/E can indicate better value/less speculative
            stability_scores.append(max(1 - (pe_ratio / 50), 0))  # 50+ P/E is high risk
        else:
            stability_scores.append(0.5)  # Neutral if no P/E available

        stability_score = np.mean(stability_scores)

        # 4. Valuation Score (0-1, lower multiples are better)
        valuation_scores = []

        # P/E ratio assessment
        if pe_ratio > 0:
            valuation_scores.append(
                max(1 - (pe_ratio / 25), 0)
            )  # 25 is reasonable, lower is better

        # P/B ratio assessment
        pb_ratio = metrics.get("price_to_book", 0)
        if pb_ratio > 0:
            valuation_scores.append(
                max(1 - (pb_ratio / 3), 0)
            )  # 3 is reasonable, lower is better

        # P/S ratio assessment
        ps_ratio = metrics.get("price_to_sales", 0)
        if ps_ratio > 0:
            valuation_scores.append(
                max(1 - (ps_ratio / 5), 0)
            )  # 5 is reasonable, lower is better

        valuation_score = np.mean(valuation_scores) if valuation_scores else 0.5

        # Overall health score
        overall_score = np.mean(
            [profitability_score, growth_score, stability_score, valuation_score]
        )

        return {
            "profitability_score": round(profitability_score, 3),
            "growth_score": round(growth_score, 3),
            "stability_score": round(stability_score, 3),
            "valuation_score": round(valuation_score, 3),
            "overall_health_score": round(overall_score, 3),
            "health_grade": self._calculate_health_grade(overall_score),
            "benchmarks_used": benchmarks,
            "detailed_metrics": {
                "profit_margin": round(net_margin, 3),
                "return_on_equity": round(roe, 3),
                "operating_margin": round(operating_margin, 3),
                "revenue_growth": round(rev_growth, 3),
                "earnings_growth": round(earnings_growth, 3),
                "pe_ratio": round(pe_ratio, 3),
                "pb_ratio": round(pb_ratio, 3),
                "ps_ratio": round(ps_ratio, 3),
            },
        }

    def analyze_competitive_position(self) -> Dict[str, Any]:
        """Analyze competitive position and economic moat"""
        if not self.discovery_data:
            raise ValueError("Discovery data not available for analysis")

        company_info = self.discovery_data.get("company_intelligence", {})
        market_data = self.discovery_data.get("market_data", {})
        financial_metrics = self.discovery_data.get("financial_metrics", {})

        # Market position analysis
        market_cap = market_data.get("market_cap", 0)
        market_position = self._classify_market_position(market_cap)

        # Competitive advantages analysis
        competitive_advantages = self._identify_competitive_advantages(
            company_info, financial_metrics
        )

        # Moat strength assessment
        moat_strength = self._assess_moat_strength(financial_metrics, company_info)

        # Industry dynamics
        industry_dynamics = self._analyze_industry_dynamics(company_info)

        return {
            "market_position": market_position,
            "competitive_advantages": competitive_advantages,
            "moat_assessment": moat_strength,
            "industry_dynamics": industry_dynamics,
            "competitive_strength_score": self._calculate_competitive_score(
                market_position, competitive_advantages, moat_strength
            ),
            "key_risks": self._identify_competitive_risks(
                company_info, financial_metrics
            ),
        }

    def analyze_risk_profile(self) -> Dict[str, Any]:
        """Comprehensive risk assessment matrix"""
        if not self.discovery_data:
            raise ValueError("Discovery data not available for analysis")

        market_data = self.discovery_data.get("market_data", {})
        financial_metrics = self.discovery_data.get("financial_metrics", {})
        company_info = self.discovery_data.get("company_intelligence", {})

        # Market risk assessment
        market_risks = self._assess_market_risks(market_data)

        # Financial risk assessment
        financial_risks = self._assess_financial_risks(financial_metrics)

        # Operational risk assessment
        operational_risks = self._assess_operational_risks(
            company_info, financial_metrics
        )

        # Aggregate risk score
        risk_scores = [
            market_risks["risk_score"],
            financial_risks["risk_score"],
            operational_risks["risk_score"],
        ]

        overall_risk_score = np.mean(risk_scores)
        risk_grade = self._calculate_risk_grade(overall_risk_score)

        return {
            "market_risks": market_risks,
            "financial_risks": financial_risks,
            "operational_risks": operational_risks,
            "overall_risk_score": round(overall_risk_score, 3),
            "risk_grade": risk_grade,
            "risk_summary": self._generate_risk_summary(
                market_risks, financial_risks, operational_risks
            ),
            "mitigation_factors": self._identify_risk_mitigations(
                financial_metrics, company_info
            ),
        }

    def generate_investment_metrics(self) -> Dict[str, Any]:
        """Generate comprehensive investment decision metrics"""
        if not self.discovery_data:
            raise ValueError("Discovery data not available for analysis")

        financial_metrics = self.discovery_data.get("financial_metrics", {})
        market_data = self.discovery_data.get("market_data", {})

        # Valuation metrics
        valuation_metrics = {
            "pe_ratio": financial_metrics.get("pe_ratio", 0),
            "forward_pe": financial_metrics.get("forward_pe", 0),
            "peg_ratio": financial_metrics.get("peg_ratio", 0),
            "price_to_book": financial_metrics.get("price_to_book", 0),
            "price_to_sales": financial_metrics.get("price_to_sales", 0),
            "ev_to_revenue": financial_metrics.get("ev_to_revenue", 0),
        }

        # Efficiency metrics
        efficiency_metrics = {
            "return_on_equity": financial_metrics.get("return_on_equity", 0),
            "return_on_assets": self._calculate_roa(financial_metrics),
            "asset_turnover": self._calculate_asset_turnover(financial_metrics),
            "profit_margin": financial_metrics.get("profit_margin", 0),
        }

        # Growth metrics
        growth_metrics = {
            "revenue_growth": financial_metrics.get("revenue_growth", 0),
            "estimated_earnings_growth": self._estimate_earnings_growth(
                financial_metrics
            ),
            "free_cash_flow_growth": self._estimate_fcf_growth(financial_metrics),
        }

        # Quality metrics
        quality_metrics = {
            "earnings_quality": self._assess_earnings_quality(financial_metrics),
            "balance_sheet_strength": self._assess_balance_sheet_strength(
                financial_metrics
            ),
            "cash_generation": self._assess_cash_generation(financial_metrics),
        }

        return {
            "valuation_metrics": valuation_metrics,
            "efficiency_metrics": efficiency_metrics,
            "growth_metrics": growth_metrics,
            "quality_metrics": quality_metrics,
            "investment_attractiveness_score": self._calculate_investment_score(
                valuation_metrics, efficiency_metrics, growth_metrics, quality_metrics
            ),
        }

    def execute_analysis(
        self, discovery_file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute complete fundamental analysis workflow"""
        print(f"📊 Starting fundamental analysis for {self.ticker}")

        # Load discovery data if needed
        if not self.load_discovery_data(discovery_file_path):
            return {"error": f"Failed to load discovery data for {self.ticker}"}

        try:
            # Execute all analysis components
            analysis_result = {
                "metadata": {
                    "command_name": "fundamental_analyst_analyze",
                    "execution_timestamp": self.timestamp.isoformat(),
                    "framework_phase": "analyze",
                    "ticker": self.ticker,
                    "analysis_methodology": "systematic_financial_analysis",
                },
                "financial_health_analysis": self.analyze_financial_health(),
                "competitive_position_analysis": self.analyze_competitive_position(),
                "risk_profile_analysis": self.analyze_risk_profile(),
                "investment_metrics": self.generate_investment_metrics(),
                "analysis_summary": self._generate_analysis_summary(),
            }

            # Calculate overall analysis confidence
            analysis_result[
                "analysis_confidence"
            ] = self._calculate_analysis_confidence(analysis_result)

            # Save analysis results
            self._save_analysis_results(analysis_result)

            print(f"✅ Analysis completed for {self.ticker}")
            return analysis_result

        except Exception as e:
            error_msg = f"Analysis failed for {self.ticker}: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg, "ticker": self.ticker}

    # Helper methods for analysis calculations
    def _calculate_health_grade(self, score: float) -> str:
        """Convert health score to letter grade"""
        if score >= 0.9:
            return "A+"
        elif score >= 0.8:
            return "A"
        elif score >= 0.7:
            return "B+"
        elif score >= 0.6:
            return "B"
        elif score >= 0.5:
            return "C+"
        elif score >= 0.4:
            return "C"
        else:
            return "D"

    def _classify_market_position(self, market_cap: float) -> Dict[str, Any]:
        """Classify market position based on market cap"""
        if market_cap > 200_000_000_000:
            return {
                "category": "Mega-cap",
                "description": "Market leader with dominant position",
                "score": 0.9,
            }
        elif market_cap > 10_000_000_000:
            return {
                "category": "Large-cap",
                "description": "Established player with strong market presence",
                "score": 0.8,
            }
        elif market_cap > 2_000_000_000:
            return {
                "category": "Mid-cap",
                "description": "Growing company with expansion potential",
                "score": 0.7,
            }
        elif market_cap > 300_000_000:
            return {
                "category": "Small-cap",
                "description": "Emerging company with higher growth potential",
                "score": 0.6,
            }
        else:
            return {
                "category": "Micro-cap",
                "description": "Early-stage company with significant risk",
                "score": 0.4,
            }

    def _identify_competitive_advantages(
        self, company_info: Dict[str, Any], financial_metrics: Dict[str, Any]
    ) -> List[str]:
        """Identify potential competitive advantages"""
        advantages = []

        # High margins suggest pricing power
        if financial_metrics.get("profit_margin", 0) > 0.20:
            advantages.append("High profit margins indicating pricing power")

        # Strong ROE suggests efficient capital use
        if financial_metrics.get("return_on_equity", 0) > 0.25:
            advantages.append(
                "Strong return on equity demonstrating capital efficiency"
            )

        # Industry-specific advantages
        industry = company_info.get("industry", "").lower()
        if "technology" in industry:
            advantages.append("Technology moat with potential network effects")
        elif "financial" in industry:
            advantages.append("Financial services with regulatory barriers")
        elif "healthcare" in industry:
            advantages.append("Healthcare with intellectual property protection")

        return advantages

    def _assess_moat_strength(
        self, financial_metrics: Dict[str, Any], company_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess economic moat strength"""
        moat_indicators = []

        # Consistent high returns suggest moat
        roe = financial_metrics.get("return_on_equity", 0)
        if roe > 0.25:
            moat_indicators.append("Consistently high returns on equity")

        # High margins suggest pricing power
        margin = financial_metrics.get("profit_margin", 0)
        if margin > 0.20:
            moat_indicators.append("Strong profit margins")

        # Industry moat factors
        industry = company_info.get("industry", "").lower()
        if "financial" in industry or "utility" in industry:
            moat_indicators.append("Regulatory barriers to entry")
        elif "technology" in industry:
            moat_indicators.append("Network effects and switching costs")

        strength_score = min(len(moat_indicators) / 3, 1.0)  # Normalize to 0-1

        return {
            "strength_score": round(strength_score, 3),
            "moat_sources": moat_indicators,
            "assessment": (
                "Strong"
                if strength_score > 0.7
                else "Moderate"
                if strength_score > 0.4
                else "Weak"
            ),
        }

    def _analyze_industry_dynamics(
        self, company_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze industry dynamics and trends"""
        sector = company_info.get("sector", "").lower()
        industry = company_info.get("industry", "").lower()

        # Industry growth assessment
        growth_outlook = "Moderate"
        if "technology" in sector or "healthcare" in sector:
            growth_outlook = "High"
        elif "utilities" in sector or "consumer staples" in sector:
            growth_outlook = "Low"

        return {
            "sector": company_info.get("sector", "Unknown"),
            "industry": company_info.get("industry", "Unknown"),
            "growth_outlook": growth_outlook,
            "competitive_intensity": "High",  # Default assumption
            "regulatory_environment": "Moderate",  # Default assumption
        }

    def _calculate_competitive_score(
        self,
        market_position: Dict[str, Any],
        advantages: List[str],
        moat_strength: Dict[str, Any],
    ) -> float:
        """Calculate overall competitive strength score"""
        position_score = market_position.get("score", 0.5)
        advantage_score = min(len(advantages) / 4, 1.0)  # Normalize to 0-1
        moat_score = moat_strength.get("strength_score", 0.5)

        return round(np.mean([position_score, advantage_score, moat_score]), 3)

    def _identify_competitive_risks(
        self, company_info: Dict[str, Any], financial_metrics: Dict[str, Any]
    ) -> List[str]:
        """Identify key competitive risks"""
        risks = []

        # High P/E suggests high expectations
        if financial_metrics.get("pe_ratio", 0) > 30:
            risks.append(
                "High valuation creates vulnerability to earnings disappointments"
            )

        # Industry-specific risks
        industry = company_info.get("industry", "").lower()
        if "technology" in industry:
            risks.append("Technology disruption and rapid innovation cycles")
        elif "retail" in industry:
            risks.append("Consumer preference shifts and economic sensitivity")

        return risks

    def _assess_market_risks(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market-related risks"""
        beta = market_data.get("beta", 1.0)

        # Beta-based risk assessment
        if beta > 1.5:
            market_risk = "High"
            risk_score = 0.8
        elif beta > 1.2:
            market_risk = "Moderate-High"
            risk_score = 0.6
        elif beta < 0.8:
            market_risk = "Low"
            risk_score = 0.3
        else:
            market_risk = "Moderate"
            risk_score = 0.5

        return {
            "market_sensitivity": market_risk,
            "beta": beta,
            "risk_score": risk_score,
            "risk_factors": [
                "Market volatility exposure",
                "Systematic risk correlation",
            ],
        }

    def _assess_financial_risks(
        self, financial_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess financial-related risks"""
        risk_factors = []
        risk_score = 0.5  # Default moderate risk

        # Profitability risk
        if financial_metrics.get("profit_margin", 0) < 0.05:
            risk_factors.append("Low profit margins")
            risk_score += 0.2

        # Growth sustainability risk
        if financial_metrics.get("revenue_growth", 0) < 0:
            risk_factors.append("Declining revenue")
            risk_score += 0.3

        # Valuation risk
        if financial_metrics.get("pe_ratio", 0) > 40:
            risk_factors.append("High valuation multiples")
            risk_score += 0.2

        risk_score = min(risk_score, 1.0)

        return {
            "financial_stability": (
                "Low"
                if risk_score > 0.7
                else "Moderate"
                if risk_score > 0.4
                else "High"
            ),
            "risk_score": round(risk_score, 3),
            "risk_factors": risk_factors,
        }

    def _assess_operational_risks(
        self, company_info: Dict[str, Any], financial_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess operational and business model risks"""
        risk_factors = []

        # Industry-specific operational risks
        industry = company_info.get("industry", "").lower()
        if "technology" in industry:
            risk_factors.append("Rapid technological change")
        elif "healthcare" in industry:
            risk_factors.append("Regulatory approval dependencies")
        elif "financial" in industry:
            risk_factors.append("Interest rate sensitivity")

        return {
            "operational_complexity": "Moderate",
            "risk_score": 0.5,  # Default moderate
            "risk_factors": risk_factors,
        }

    def _calculate_risk_grade(self, risk_score: float) -> str:
        """Convert risk score to risk grade"""
        if risk_score < 0.3:
            return "Low Risk"
        elif risk_score < 0.5:
            return "Moderate Risk"
        elif risk_score < 0.7:
            return "High Risk"
        else:
            return "Very High Risk"

    def _generate_risk_summary(
        self,
        market_risks: Dict[str, Any],
        financial_risks: Dict[str, Any],
        operational_risks: Dict[str, Any],
    ) -> str:
        """Generate comprehensive risk summary"""
        risk_levels = [
            f"Market: {market_risks['market_sensitivity']}",
            f"Financial: {financial_risks['financial_stability']}",
            f"Operational: Moderate",
        ]
        return f"Risk Profile - {', '.join(risk_levels)}"

    def _identify_risk_mitigations(
        self, financial_metrics: Dict[str, Any], company_info: Dict[str, Any]
    ) -> List[str]:
        """Identify factors that mitigate risks"""
        mitigations = []

        # Strong cash position
        if financial_metrics.get("free_cash_flow", 0) > 0:
            mitigations.append("Positive free cash flow generation")

        # Market leadership
        if company_info.get("name", "").lower() in [
            "apple",
            "microsoft",
            "google",
            "amazon",
        ]:
            mitigations.append("Market leadership position")

        return mitigations

    # Additional helper methods for investment metrics
    def _calculate_roa(self, financial_metrics: Dict[str, Any]) -> float:
        """Calculate Return on Assets"""
        net_income = financial_metrics.get("net_income", 0)
        # Estimate total assets from enterprise value as proxy
        total_assets = financial_metrics.get("revenue_ttm", 1) * 1.5  # Rough estimate
        return (net_income / total_assets) if total_assets > 0 else 0

    def _calculate_asset_turnover(self, financial_metrics: Dict[str, Any]) -> float:
        """Calculate Asset Turnover ratio"""
        revenue = financial_metrics.get("revenue_ttm", 0)
        # Estimate total assets from enterprise value as proxy
        total_assets = revenue * 1.5 if revenue > 0 else 1
        return (revenue / total_assets) if total_assets > 0 else 0

    def _estimate_earnings_growth(self, financial_metrics: Dict[str, Any]) -> float:
        """Estimate earnings growth rate"""
        forward_eps = financial_metrics.get("forward_eps", 0)
        trailing_eps = financial_metrics.get("earnings_per_share", 0)

        if trailing_eps > 0 and forward_eps > 0:
            return (forward_eps - trailing_eps) / trailing_eps
        else:
            return financial_metrics.get(
                "revenue_growth", 0
            )  # Fallback to revenue growth

    def _estimate_fcf_growth(self, financial_metrics: Dict[str, Any]) -> float:
        """Estimate free cash flow growth"""
        # Without historical data, use revenue growth as proxy
        return financial_metrics.get("revenue_growth", 0)

    def _assess_earnings_quality(self, financial_metrics: Dict[str, Any]) -> float:
        """Assess earnings quality (0-1 scale)"""
        fcf = financial_metrics.get("free_cash_flow", 0)
        net_income = financial_metrics.get("net_income", 1)

        # FCF to net income ratio as quality indicator
        if net_income > 0:
            quality_ratio = min(fcf / net_income, 2.0) / 2.0  # Normalize
            return max(0, quality_ratio)
        return 0.5

    def _assess_balance_sheet_strength(
        self, financial_metrics: Dict[str, Any]
    ) -> float:
        """Assess balance sheet strength (0-1 scale)"""
        # Use cash ratio as proxy for balance sheet strength
        cash_ratio = financial_metrics.get("cash_ratio", 0)
        return min(cash_ratio / 2.0, 1.0)

    def _assess_cash_generation(self, financial_metrics: Dict[str, Any]) -> float:
        """Assess cash generation capability (0-1 scale)"""
        fcf = financial_metrics.get("free_cash_flow", 0)
        revenue = financial_metrics.get("revenue_ttm", 1)

        fcf_margin = fcf / revenue if revenue > 0 else 0
        return min(fcf_margin / 0.15, 1.0)  # 15% FCF margin is excellent

    def _calculate_investment_score(
        self,
        valuation: Dict[str, Any],
        efficiency: Dict[str, Any],
        growth: Dict[str, Any],
        quality: Dict[str, Any],
    ) -> float:
        """Calculate overall investment attractiveness score"""
        # Valuation score (lower is better)
        val_score = 0.5  # Default neutral
        if valuation["pe_ratio"] > 0:
            val_score = max(1 - (valuation["pe_ratio"] / 25), 0)

        # Efficiency score
        eff_score = min(efficiency["return_on_equity"] / 0.20, 1.0)

        # Growth score
        growth_score = min(growth["revenue_growth"] / 0.15, 1.0)

        # Quality score
        quality_score = (
            quality["earnings_quality"]
            + quality["balance_sheet_strength"]
            + quality["cash_generation"]
        ) / 3

        return round(np.mean([val_score, eff_score, growth_score, quality_score]), 3)

    def _generate_analysis_summary(self) -> Dict[str, Any]:
        """Generate executive summary of analysis"""
        return {
            "analysis_date": self.timestamp.strftime("%Y-%m-%d"),
            "ticker_analyzed": self.ticker,
            "key_findings": [
                "Comprehensive financial health assessment completed",
                "Competitive position and moat strength evaluated",
                "Risk profile and mitigation factors identified",
                "Investment metrics calculated for decision support",
            ],
            "next_steps": [
                "Proceed to synthesis phase for investment thesis development",
                "Consider peer comparison for relative valuation",
                "Monitor key risk factors identified in analysis",
            ],
        }

    def _calculate_analysis_confidence(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate confidence in analysis results"""
        # Base confidence on data availability and quality
        base_confidence = 0.8  # Default high confidence for systematic analysis

        # Adjust based on discovery data quality if available
        if self.discovery_data and "data_quality_assessment" in self.discovery_data:
            data_quality = self.discovery_data["data_quality_assessment"].get(
                "overall_data_quality", 0.8
            )
            base_confidence = (base_confidence + data_quality) / 2

        return round(base_confidence, 3)

    def _save_analysis_results(self, analysis_result: Dict[str, Any]) -> str:
        """Save analysis results to output directory"""
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp_str = self.timestamp.strftime("%Y%m%d")
        filename = f"{self.ticker}_{timestamp_str}_analysis.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(analysis_result, f, indent=2, default=str)

        print(f"💾 Analysis results saved: {filepath}")
        return filepath


def main():
    """Command-line interface for fundamental analysis"""
    parser = argparse.ArgumentParser(
        description="Execute fundamental analysis for any stock ticker"
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL, MSFT, MA)")
    parser.add_argument("--discovery-file", help="Path to discovery data file")
    parser.add_argument(
        "--output-dir",
        default="./team-workspace/data/outputs/fundamental_analysis/analysis",
        help="Output directory for analysis results",
    )

    args = parser.parse_args()

    # Execute analysis
    analyzer = FundamentalAnalyzer(ticker=args.ticker, output_dir=args.output_dir)

    result = analyzer.execute_analysis(args.discovery_file)

    if "error" in result:
        print(f"❌ Analysis failed: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ Analysis completed successfully for {args.ticker}")
        sys.exit(0)


if __name__ == "__main__":
    main()
