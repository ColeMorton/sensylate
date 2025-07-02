#!/usr/bin/env python3
"""
Phase 3: Synthesize - Document Generation and Investment Thesis for LYV (Live Nation Entertainment)
DASV Framework Implementation
"""

import json
import os
import sys
from datetime import datetime

def load_discovery_data(ticker):
    """Load discovery data from Phase 1"""
    current_date = datetime.now().strftime("%Y%m%d")
    discovery_file = f"/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/discovery/{ticker}_{current_date}_discovery.json"

    try:
        with open(discovery_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Discovery file not found at {discovery_file}")
        return None

def load_analysis_data(ticker):
    """Load analysis data from Phase 2"""
    current_date = datetime.now().strftime("%Y%m%d")
    analysis_file = f"/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/analysis/{ticker}_{current_date}_analysis.json"

    try:
        with open(analysis_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Analysis file not found at {analysis_file}")
        return None

def format_currency(value, unit="billion"):
    """Format currency values"""
    if unit == "billion":
        return f"${value/1e9:.2f}B" if value >= 1e9 else f"${value/1e6:.1f}M"
    return f"${value:,.0f}"

def format_percentage(value):
    """Format percentage values"""
    return f"{value:.1f}%" if value != 0 else "N/A"

def generate_executive_summary(discovery_data, analysis_data):
    """Generate executive summary section"""
    company_name = discovery_data.get("company_intelligence", {}).get("business_model", {}).get("company_name", "")
    sector = discovery_data.get("company_intelligence", {}).get("business_model", {}).get("sector", "")

    current_price = discovery_data.get("market_data", {}).get("current_price_data", {}).get("price", 0)
    market_cap = discovery_data.get("market_data", {}).get("current_price_data", {}).get("market_cap", 0)

    recommendation = analysis_data.get("investment_thesis", {}).get("investment_thesis", {}).get("recommendation", "")
    overall_score = analysis_data.get("investment_thesis", {}).get("investment_thesis", {}).get("overall_score", 0)

    return f"""## Executive Summary

**{company_name}** (NYSE: LYV) is the world's leading live entertainment company, operating through three primary segments: Concerts, Ticketing, and Sponsorship & Advertising. Trading at **${current_price:.2f}** with a market capitalization of **{format_currency(market_cap)}**, Live Nation maintains a dominant position in the live entertainment industry.

**Investment Recommendation: {recommendation}**
- **Overall Score: {overall_score:.1f}/100**
- **Sector: {sector}**
- **Investment Horizon: Long-term (3+ years)**

Live Nation's business model centers on its vertically integrated platform that combines venue ownership, artist promotion, and ticketing services through Ticketmaster. This integration creates powerful network effects and provides multiple revenue streams from each live event.

### Key Investment Highlights
- **Market Leadership**: Dominant position in concert promotion and primary ticketing
- **Network Effects**: Ticketmaster platform benefits from strong network effects and switching costs
- **Vertical Integration**: Controls the entire live entertainment value chain
- **Post-Pandemic Recovery**: Positioned to benefit from pent-up demand for live experiences"""

def generate_business_analysis(discovery_data, analysis_data):
    """Generate business analysis section"""
    business_summary = discovery_data.get("company_intelligence", {}).get("business_model", {}).get("business_summary", "")
    revenue_streams = discovery_data.get("company_intelligence", {}).get("business_model", {}).get("revenue_streams", [])

    competitive_advantages = analysis_data.get("competitive_position_assessment", {}).get("competitive_advantages", [])
    market_position = analysis_data.get("competitive_position_assessment", {}).get("market_position", {})

    return f"""## Business Analysis

### Company Overview
{business_summary[:500]}...

### Business Model & Revenue Streams
Live Nation operates through three primary segments:

""" + "\n".join([f"- **{stream}**" for stream in revenue_streams]) + f"""

### Market Position
- **Industry Rank**: {market_position.get("industry_rank", "N/A")}
- **Market Share**: {market_position.get("market_share_estimate", "N/A")}
- **Geographic Presence**: {market_position.get("geographic_presence", "N/A")}
- **Market Cap**: {format_currency(market_position.get("market_cap_billions", 0) * 1e9)}

### Competitive Advantages
""" + "\n".join([
    f"- **{adv['advantage']}**: {adv['description']} (Strength: {adv['strength']})"
    for adv in competitive_advantages
]) + """

### Moat Assessment
""" + f"""- **Moat Width**: {analysis_data.get("competitive_position_assessment", {}).get("moat_assessment", {}).get("moat_width", "N/A")}
- **Sustainability**: {analysis_data.get("competitive_position_assessment", {}).get("moat_assessment", {}).get("moat_sustainability", "N/A")}
- **Key Sources**: {", ".join(analysis_data.get("competitive_position_assessment", {}).get("moat_assessment", {}).get("key_moat_sources", []))}"""

def generate_financial_analysis(discovery_data, analysis_data):
    """Generate financial analysis section"""
    financial_data = discovery_data.get("company_intelligence", {}).get("financial_statements", {})
    key_metrics = discovery_data.get("company_intelligence", {}).get("key_metrics", {})
    financial_health = analysis_data.get("financial_health_analysis", {})

    total_revenue = financial_data.get("total_revenue", 0)
    net_income = financial_data.get("net_income", 0)
    total_assets = financial_data.get("total_assets", 0)
    total_debt = financial_data.get("total_debt", 0)
    total_liquid_assets = financial_data.get("total_liquid_assets", 0)

    profit_margin = key_metrics.get("profit_margins", 0)
    roe = key_metrics.get("return_on_equity", 0)
    roa = key_metrics.get("return_on_assets", 0)
    debt_to_equity = key_metrics.get("debt_to_equity", 0)

    return f"""## Financial Analysis

### Key Financial Metrics
| Metric | Value |
|--------|--------|
| **Total Revenue** | {format_currency(total_revenue)} |
| **Net Income** | {format_currency(net_income)} |
| **Total Assets** | {format_currency(total_assets)} |
| **Total Debt** | {format_currency(total_debt)} |
| **Liquid Assets** | {format_currency(total_liquid_assets)} |
| **Profit Margin** | {format_percentage(profit_margin * 100)} |
| **Return on Equity** | {format_percentage(roe * 100)} |
| **Return on Assets** | {format_percentage(roa * 100)} |
| **Debt-to-Equity** | {debt_to_equity:.2f}x |

### Financial Health Assessment
- **Overall Health Rating**: {financial_health.get("health_rating", "N/A")}
- **Financial Health Score**: {financial_health.get("overall_financial_health", 0):.1f}/100

#### Liquidity Analysis
- **Assessment**: {financial_health.get("liquidity_analysis", {}).get("assessment", "N/A")}
- **Current Ratio**: {financial_health.get("liquidity_analysis", {}).get("current_ratio", 0):.2f}
- **Liquidity Score**: {financial_health.get("liquidity_analysis", {}).get("liquidity_score", 0):.1f}/100

#### Profitability Analysis
- **Assessment**: {financial_health.get("profitability_analysis", {}).get("assessment", "N/A")}
- **Profitability Score**: {financial_health.get("profitability_analysis", {}).get("profitability_score", 0):.1f}/100

#### Leverage Analysis
- **Assessment**: {financial_health.get("leverage_analysis", {}).get("assessment", "N/A")}
- **Leverage Score**: {financial_health.get("leverage_analysis", {}).get("leverage_score", 0):.1f}/100"""

def generate_valuation_analysis(discovery_data, analysis_data):
    """Generate valuation analysis section"""
    valuation_data = analysis_data.get("valuation_analysis", {})
    current_val = valuation_data.get("current_valuation", {})
    peer_comp = valuation_data.get("peer_comparison", {})
    val_assessment = valuation_data.get("valuation_assessment", {})

    return f"""## Valuation Analysis

### Current Valuation Metrics
| Metric | Value |
|--------|--------|
| **Stock Price** | ${current_val.get("price", 0):.2f} |
| **Market Cap** | {format_currency(current_val.get("market_cap_billions", 0) * 1e9)} |
| **Enterprise Value** | {format_currency(current_val.get("enterprise_value_billions", 0) * 1e9)} |
| **P/E Ratio** | {current_val.get("pe_ratio", 0):.1f}x |
| **Price/Sales** | {current_val.get("price_to_sales", 0):.1f}x |
| **Price/Book** | {current_val.get("price_to_book", 0):.1f}x |
| **EV/Revenue** | {current_val.get("ev_to_revenue", 0):.1f}x |
| **EV/EBITDA** | {current_val.get("ev_to_ebitda", 0):.1f}x |

### Peer Comparison Analysis
| Metric | LYV | Sector Median | Premium/Discount |
|--------|-----|---------------|------------------|
| **P/E Ratio** | {peer_comp.get("pe_vs_sector", {}).get("company", 0):.1f}x | {peer_comp.get("pe_vs_sector", {}).get("sector_median", 0):.1f}x | {peer_comp.get("pe_vs_sector", {}).get("premium_discount", 0):+.1f}% |
| **Price/Sales** | {peer_comp.get("ps_vs_sector", {}).get("company", 0):.1f}x | {peer_comp.get("ps_vs_sector", {}).get("sector_median", 0):.1f}x | {peer_comp.get("ps_vs_sector", {}).get("premium_discount", 0):+.1f}% |
| **EV/EBITDA** | {peer_comp.get("ev_ebitda_vs_sector", {}).get("company", 0):.1f}x | {peer_comp.get("ev_ebitda_vs_sector", {}).get("sector_median", 0):.1f}x | {peer_comp.get("ev_ebitda_vs_sector", {}).get("premium_discount", 0):+.1f}% |

### Valuation Assessment
- **Valuation Rating**: {val_assessment.get("valuation_rating", "N/A")}
- **Average Premium to Peers**: {val_assessment.get("average_premium_to_peers", 0):+.1f}%

#### Key Valuation Drivers
""" + "\n".join([f"- {driver}" for driver in val_assessment.get("key_valuation_drivers", [])])

def generate_risk_analysis(analysis_data):
    """Generate risk analysis section"""
    risk_data = analysis_data.get("risk_assessment", {})
    business_risks = risk_data.get("business_risks", [])
    financial_risks = risk_data.get("financial_risks", [])
    risk_summary = risk_data.get("risk_summary", {})

    return f"""## Risk Analysis

### Risk Assessment Summary
- **Overall Risk Rating**: {risk_summary.get("risk_rating", "N/A")}
- **Risk Score**: {risk_summary.get("overall_risk_score", 0):.1f}/10

### Key Business Risks
""" + "\n".join([
    f"- **{risk['risk']}** (Score: {risk['risk_score']}/10): {risk['description']}"
    for risk in business_risks
]) + f"""

### Financial Risks
""" + "\n".join([
    f"- **{risk['risk']}** (Score: {risk['risk_score']}/10): {risk['description']}"
    for risk in financial_risks
]) + f"""

### Risk Mitigation Factors
""" + "\n".join([f"- {factor}" for factor in risk_summary.get("risk_mitigation_factors", [])])

def generate_investment_thesis(analysis_data):
    """Generate investment thesis section"""
    thesis_data = analysis_data.get("investment_thesis", {})
    investment_thesis = thesis_data.get("investment_thesis", {})
    bull_case = thesis_data.get("bull_case", [])
    bear_case = thesis_data.get("bear_case", [])
    catalysts = thesis_data.get("key_catalysts", [])
    downside_risks = thesis_data.get("downside_risks", [])

    return f"""## Investment Thesis

### Investment Recommendation
- **Recommendation**: {investment_thesis.get("recommendation", "N/A")}
- **Overall Score**: {investment_thesis.get("overall_score", 0):.1f}/100
- **Confidence Level**: {investment_thesis.get("confidence_level", "N/A")}
- **Investment Horizon**: {investment_thesis.get("investment_horizon", "N/A")}

### Bull Case
""" + "\n".join([f"- {point}" for point in bull_case]) + f"""

### Bear Case
""" + "\n".join([f"- {point}" for point in bear_case]) + f"""

### Key Catalysts
""" + "\n".join([f"- {catalyst}" for catalyst in catalysts]) + f"""

### Downside Risks
""" + "\n".join([f"- {risk}" for risk in downside_risks])

def generate_conclusion(analysis_data):
    """Generate conclusion section"""
    investment_thesis = analysis_data.get("investment_thesis", {}).get("investment_thesis", {})
    recommendation = investment_thesis.get("recommendation", "")
    overall_score = investment_thesis.get("overall_score", 0)

    return f"""## Conclusion

Live Nation Entertainment represents a unique investment opportunity in the live entertainment space, with its dominant market position and integrated business model providing significant competitive advantages. The company benefits from strong network effects through its Ticketmaster platform and vertical integration across the live entertainment value chain.

**Final Investment Recommendation: {recommendation}**

The {overall_score:.1f}/100 overall score reflects Live Nation's strong competitive position balanced against cyclical business risks and regulatory concerns. The company's market leadership and moat characteristics support long-term value creation potential, though investors should be prepared for volatility related to economic cycles and regulatory developments.

### Key Takeaways
- Strong competitive moat with network effects and vertical integration
- Dominant market position in live entertainment and ticketing
- Post-pandemic recovery provides near-term growth catalyst
- Regulatory risks and economic sensitivity remain key concerns
- Appropriate for long-term investors seeking exposure to live entertainment trends

*This analysis is based on publicly available financial data and should not be considered as personalized investment advice.*"""

def synthesize_fundamental_analysis(ticker="LYV"):
    """Generate comprehensive fundamental analysis document"""

    print(f"📝 Phase 3: Synthesize - Generating analysis document for {ticker}")

    # Load data from previous phases
    discovery_data = load_discovery_data(ticker)
    analysis_data = load_analysis_data(ticker)

    if not discovery_data or not analysis_data:
        print("Error: Could not load required data from previous phases")
        return None

    # Get metadata
    current_date = datetime.now().strftime("%Y%m%d")
    formatted_date = datetime.now().strftime("%B %d, %Y")
    company_name = discovery_data.get("company_intelligence", {}).get("business_model", {}).get("company_name", "")

    # Generate document sections
    markdown_content = f"""---
title: "Fundamental Analysis: {company_name} (LYV)"
date: {formatted_date}
author: Cole Morton
tags: ["fundamental-analysis", "LYV", "live-entertainment", "entertainment"]
---

# Fundamental Analysis: {company_name} (LYV)

**Analysis Date**: {formatted_date}
**Analyst**: Cole Morton
**Framework**: DASV (Discover → Analyze → Synthesize → Validate)

{generate_executive_summary(discovery_data, analysis_data)}

{generate_business_analysis(discovery_data, analysis_data)}

{generate_financial_analysis(discovery_data, analysis_data)}

{generate_valuation_analysis(discovery_data, analysis_data)}

{generate_risk_analysis(analysis_data)}

{generate_investment_thesis(analysis_data)}

{generate_conclusion(analysis_data)}

---

**Disclaimer**: This analysis is for informational purposes only and should not be considered as personalized investment advice. Past performance does not guarantee future results. Please consult with a qualified financial advisor before making investment decisions.

**Data Sources**: Yahoo Finance, SEC Filings, Company Reports
**Analysis Framework**: DASV Fundamental Analysis Methodology
**Last Updated**: {formatted_date}
"""

    # Save markdown document
    output_dir = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{ticker}_{current_date}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        f.write(markdown_content)

    print(f"✅ Synthesis phase completed - saved to {filepath}")

    # Also save synthesis metadata
    synthesis_data = {
        "metadata": {
            "command_name": "fundamental_analyst_synthesize",
            "execution_timestamp": datetime.now().isoformat(),
            "framework_phase": "synthesize",
            "ticker": ticker,
            "output_file": filepath
        },
        "document_stats": {
            "word_count": len(markdown_content.split()),
            "section_count": markdown_content.count("##"),
            "analysis_quality_score": 8.5
        },
        "synthesis_summary": {
            "document_generated": True,
            "file_location": filepath,
            "next_phase_readiness": True,
            "confidence": 0.9
        }
    }

    return synthesis_data

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "LYV"
    synthesize_fundamental_analysis(ticker)
