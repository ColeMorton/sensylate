#!/usr/bin/env python3
"""
Phase 3: Synthesize - Generate Institutional-Quality Investment Analysis for Mastercard (MA)
"""

import json
import os
from datetime import datetime
import numpy as np

def load_phase_data(ticker="MA"):
    """Load data from previous phases"""
    date_str = datetime.now().strftime('%Y%m%d')

    # Load discovery data
    discovery_path = f"/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/discover/outputs/discover_{ticker}_{date_str}.json"
    with open(discovery_path, 'r') as f:
        discovery_data = json.load(f)

    # Load analysis data
    analysis_path = f"/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/analyze/outputs/analyze_{ticker}_{date_str}.json"
    with open(analysis_path, 'r') as f:
        analysis_data = json.load(f)

    return discovery_data, analysis_data

def calculate_fair_value(discovery_data, analysis_data):
    """Multi-method valuation synthesis"""
    inputs = analysis_data['valuation_inputs']
    current_price = inputs['current_price']

    valuations = {}

    # 1. P/E Multiple Valuation
    if inputs['earnings_per_share'] > 0:
        # Use sector average P/E of ~30 for payment processors
        sector_pe = 30
        peer_avg_pe = 35  # Based on V, AXP peers
        target_pe = (sector_pe + peer_avg_pe) / 2
        pe_fair_value = inputs['earnings_per_share'] * target_pe
        valuations['pe_multiple'] = {
            "fair_value": round(pe_fair_value, 2),
            "current_pe": inputs['trailing_pe'],
            "target_pe": target_pe,
            "confidence": 0.8
        }

    # 2. PEG Valuation
    growth_rate = analysis_data['growth_drivers']['revenue_growth_rate']
    if growth_rate > 0 and inputs['trailing_pe'] > 0:
        current_peg = inputs['trailing_pe'] / (growth_rate * 100)
        fair_peg = 1.5  # Fair PEG for quality growth company
        peg_fair_value = current_price * (fair_peg / current_peg)
        valuations['peg_ratio'] = {
            "fair_value": round(peg_fair_value, 2),
            "current_peg": round(current_peg, 2),
            "target_peg": fair_peg,
            "confidence": 0.75
        }

    # 3. DCF Valuation (simplified)
    fcf = inputs['free_cash_flow']
    shares = inputs['shares_outstanding']
    if fcf > 0 and shares > 0:
        # Assumptions
        growth_rate_5y = 0.12  # 12% FCF growth for 5 years
        terminal_growth = 0.03  # 3% perpetual growth
        wacc = 0.08  # 8% WACC for MA

        # Project cash flows
        fcf_projections = []
        current_fcf = fcf
        for i in range(5):
            current_fcf *= (1 + growth_rate_5y)
            fcf_projections.append(current_fcf)

        # Terminal value
        terminal_fcf = fcf_projections[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (wacc - terminal_growth)

        # Present value
        pv_fcf = sum(fcf / (1 + wacc)**(i+1) for i, fcf in enumerate(fcf_projections))
        pv_terminal = terminal_value / (1 + wacc)**5

        enterprise_value = pv_fcf + pv_terminal
        equity_value = enterprise_value - inputs['enterprise_value'] + inputs['market_cap']
        dcf_fair_value = equity_value / shares

        valuations['dcf'] = {
            "fair_value": round(dcf_fair_value, 2),
            "assumptions": {
                "5y_growth": growth_rate_5y,
                "terminal_growth": terminal_growth,
                "wacc": wacc
            },
            "confidence": 0.85
        }

    # 4. Price/Sales Valuation
    if inputs['price_to_sales'] > 0:
        # Premium payment processor P/S range: 15-20x
        target_ps = 17.5
        current_ps = inputs['price_to_sales']
        ps_fair_value = current_price * (target_ps / current_ps)
        valuations['price_to_sales'] = {
            "fair_value": round(ps_fair_value, 2),
            "current_ps": round(current_ps, 2),
            "target_ps": target_ps,
            "confidence": 0.7
        }

    # Calculate weighted fair value
    total_weight = sum(v['confidence'] for v in valuations.values())
    weighted_fair_value = sum(v['fair_value'] * v['confidence'] for v in valuations.values()) / total_weight

    # Calculate upside/downside
    upside = (weighted_fair_value - current_price) / current_price

    return {
        "current_price": current_price,
        "fair_value": round(weighted_fair_value, 2),
        "upside_potential": round(upside, 3),
        "valuation_methods": valuations,
        "recommendation": "BUY" if upside > 0.15 else "HOLD" if upside > -0.10 else "SELL"
    }

def generate_investment_thesis(discovery_data, analysis_data, valuation):
    """Generate comprehensive investment thesis"""

    company_info = discovery_data['company_info']
    financial_health = analysis_data['financial_health']
    competitive = analysis_data['competitive_position']
    growth = analysis_data['growth_drivers']
    risks = analysis_data['risk_assessment']

    # Build thesis components
    thesis_components = []

    # 1. Business Quality
    if competitive['moat_score'] > 0.8:
        thesis_components.append({
            "aspect": "Business Quality",
            "strength": "Strong",
            "rationale": f"Mastercard possesses a wide economic moat (score: {competitive['moat_score']:.1%}) driven by powerful network effects, high switching costs, and global scale advantages.",
            "confidence": 0.9
        })

    # 2. Financial Performance
    if financial_health['overall_health_score'] > 0.5:
        margin = financial_health['details']['net_margin']
        roe = financial_health['details']['roe']
        thesis_components.append({
            "aspect": "Financial Excellence",
            "strength": "Strong",
            "rationale": f"Exceptional financial metrics with {margin:.1%} net margin and {roe:.1%} ROE demonstrate superior capital efficiency and profitability.",
            "confidence": 0.85
        })

    # 3. Growth Prospects
    if growth['weighted_growth_potential'] > 0.6:
        thesis_components.append({
            "aspect": "Growth Trajectory",
            "strength": "Positive",
            "rationale": f"Multiple growth drivers including digital payments adoption and emerging markets expansion support {growth['revenue_growth_rate']:.1%} revenue growth.",
            "confidence": 0.8
        })

    # 4. Valuation
    if valuation['upside_potential'] > 0.1:
        thesis_components.append({
            "aspect": "Valuation",
            "strength": "Attractive",
            "rationale": f"Current price of ${valuation['current_price']:.2f} offers {valuation['upside_potential']:.1%} upside to fair value of ${valuation['fair_value']:.2f}.",
            "confidence": 0.75
        })

    # Overall thesis strength
    thesis_confidence = np.mean([c['confidence'] for c in thesis_components])

    return {
        "thesis_components": thesis_components,
        "overall_confidence": round(thesis_confidence, 3),
        "investment_recommendation": valuation['recommendation'],
        "time_horizon": "12-24 months"
    }

def generate_scenario_analysis(discovery_data, analysis_data, valuation):
    """Generate bull/base/bear scenarios"""

    current_price = valuation['current_price']
    fair_value = valuation['fair_value']

    scenarios = {
        "bull_case": {
            "probability": 0.3,
            "assumptions": [
                "Digital payment adoption accelerates globally",
                "Successful expansion in emerging markets",
                "Value-added services drive margin expansion",
                "Limited regulatory headwinds"
            ],
            "target_price": round(fair_value * 1.25, 2),
            "upside": round((fair_value * 1.25 - current_price) / current_price, 3),
            "key_metrics": {
                "revenue_growth": "16-18%",
                "margin_expansion": "+200 bps",
                "eps_growth": "18-20%"
            }
        },
        "base_case": {
            "probability": 0.5,
            "assumptions": [
                "Steady digital payment growth continues",
                "Market share remains stable",
                "Modest margin improvement",
                "Normal regulatory environment"
            ],
            "target_price": round(fair_value, 2),
            "upside": round((fair_value - current_price) / current_price, 3),
            "key_metrics": {
                "revenue_growth": "12-14%",
                "margin_expansion": "Stable",
                "eps_growth": "13-15%"
            }
        },
        "bear_case": {
            "probability": 0.2,
            "assumptions": [
                "Economic slowdown impacts transaction volumes",
                "Increased competition from fintechs",
                "Regulatory pressure on fees",
                "Technology disruption accelerates"
            ],
            "target_price": round(fair_value * 0.80, 2),
            "upside": round((fair_value * 0.80 - current_price) / current_price, 3),
            "key_metrics": {
                "revenue_growth": "6-8%",
                "margin_expansion": "-100 bps",
                "eps_growth": "5-7%"
            }
        }
    }

    # Calculate probability-weighted target
    weighted_target = sum(s['target_price'] * s['probability'] for s in scenarios.values())

    return {
        "scenarios": scenarios,
        "probability_weighted_target": round(weighted_target, 2),
        "probability_weighted_upside": round((weighted_target - current_price) / current_price, 3)
    }

def synthesize_investment_analysis(ticker="MA"):
    """Generate institutional-quality investment analysis document"""

    print(f"📝 Phase 3: Synthesize - Generating investment analysis for {ticker}")

    # Load data from previous phases
    discovery_data, analysis_data = load_phase_data(ticker)

    # Perform valuation
    valuation = calculate_fair_value(discovery_data, analysis_data)

    # Generate investment thesis
    investment_thesis = generate_investment_thesis(discovery_data, analysis_data, valuation)

    # Generate scenario analysis
    scenario_analysis = generate_scenario_analysis(discovery_data, analysis_data, valuation)

    # Create the institutional-quality markdown document
    company_info = discovery_data['company_info']
    market_data = discovery_data['market_data']
    financial_metrics = discovery_data['financial_metrics']
    analyst_data = discovery_data['analyst_data']
    financial_health = analysis_data['financial_health']
    competitive = analysis_data['competitive_position']
    growth = analysis_data['growth_drivers']
    risks = analysis_data['risk_assessment']

    document = f"""# Mastercard Incorporated (MA) - Institutional Investment Analysis

**Date**: {datetime.now().strftime('%B %d, %Y')}
**Current Price**: ${valuation['current_price']:.2f}
**Fair Value**: ${valuation['fair_value']:.2f}
**Upside Potential**: {valuation['upside_potential']:.1%}
**Investment Recommendation**: **{investment_thesis['investment_recommendation']}**
**Confidence**: {investment_thesis['overall_confidence']:.1f}

---

## Executive Summary

Mastercard Incorporated stands as a dominant force in the global payments ecosystem, leveraging powerful network effects and technological infrastructure to facilitate seamless transactions worldwide. Our comprehensive fundamental analysis reveals a company with exceptional financial metrics, sustainable competitive advantages, and multiple avenues for continued growth.

**Key Investment Highlights:**
- **Wide Economic Moat**: Network effects and scale advantages create formidable barriers to entry (Moat Score: {competitive['moat_score']:.1%})
- **Financial Excellence**: Industry-leading {financial_health['details']['net_margin']:.1%} net margin and {financial_health['details']['roe']:.1%} ROE
- **Growth Momentum**: {growth['revenue_growth_rate']:.1%} revenue growth driven by secular digital payment trends
- **Attractive Valuation**: Current valuation offers {valuation['upside_potential']:.1%} upside to our fair value estimate

## Company Overview

{company_info['description'][:500]}...

**Key Statistics:**
- Market Capitalization: ${market_data['market_cap']:,.0f}
- Enterprise Value: ${market_data['enterprise_value']:,.0f}
- Employees: {company_info['employees']:,}
- Headquarters: {company_info['country']}

## Financial Analysis

### Performance Metrics
Our four-dimensional financial health assessment reveals robust fundamentals:

| Dimension | Score | Assessment |
|-----------|-------|------------|
| Profitability | {financial_health['profitability_score']:.1%} | {"Exceptional" if financial_health['profitability_score'] > 0.8 else "Strong" if financial_health['profitability_score'] > 0.6 else "Moderate"} |
| Growth | {financial_health['growth_score']:.1%} | {"Exceptional" if financial_health['growth_score'] > 0.8 else "Strong" if financial_health['growth_score'] > 0.6 else "Moderate"} |
| Liquidity | {financial_health['liquidity_score']:.1%} | {"Exceptional" if financial_health['liquidity_score'] > 0.8 else "Strong" if financial_health['liquidity_score'] > 0.6 else "Moderate"} |
| Leverage | {financial_health['leverage_score']:.1%} | {"Conservative" if financial_health['leverage_score'] > 0.8 else "Moderate" if financial_health['leverage_score'] > 0.6 else "Elevated"} |
| **Overall Health** | **{financial_health['overall_health_score']:.1%}** | **{"Excellent" if financial_health['overall_health_score'] > 0.7 else "Strong" if financial_health['overall_health_score'] > 0.5 else "Moderate"}** |

### Key Financial Ratios
- **P/E Ratio**: {financial_metrics['pe_ratio']:.1f}x (vs. Forward P/E: {financial_metrics['forward_pe']:.1f}x)
- **Profit Margin**: {financial_metrics['profit_margin']:.1%}
- **ROE**: {financial_metrics['return_on_equity']:.1%}
- **Revenue Growth**: {financial_metrics['revenue_growth']:.1%}
- **Free Cash Flow**: ${financial_metrics['free_cash_flow']:,.0f}

## Competitive Position

Mastercard maintains a **{competitive['market_position']}** position in the global payments industry with significant competitive advantages:

### Moat Analysis
"""

    # Add moat factors
    for factor, score in competitive['moat_factors'].items():
        factor_name = factor.replace('_', ' ').title()
        strength = "Very Strong" if score > 0.8 else "Strong" if score > 0.6 else "Moderate"
        document += f"- **{factor_name}**: {strength} ({score:.1%})\n"

    document += f"""

### Peer Comparison
Mastercard demonstrates superior positioning relative to key competitors:

| Metric | MA | Industry Avg | Advantage |
|--------|-----|--------------|-----------|
| Profit Margin | {financial_metrics['profit_margin']:.1%} | ~35% | +{(financial_metrics['profit_margin'] - 0.35):.1%} |
| Revenue Growth | {financial_metrics['revenue_growth']:.1%} | ~10% | +{(financial_metrics['revenue_growth'] - 0.10):.1%} |
| ROE | {financial_metrics['return_on_equity']:.1%} | ~100% | +{(financial_metrics['return_on_equity'] - 1.0):.1%} |

## Growth Drivers

Our analysis identifies multiple catalysts supporting continued expansion:

"""

    # Add growth drivers
    sorted_drivers = sorted(growth['growth_drivers'].items(), key=lambda x: x[1]['impact'] * x[1]['confidence'], reverse=True)
    for i, (driver_name, driver_data) in enumerate(sorted_drivers[:3]):
        driver_title = driver_name.replace('_', ' ').title()
        document += f"""### {i+1}. {driver_title}
*Impact: {driver_data['impact']:.1%} | Confidence: {driver_data['confidence']:.1%}*

{driver_data['description']}

"""

    document += f"""## Valuation Analysis

### Multi-Method Valuation Summary
Our comprehensive valuation analysis employs multiple methodologies to derive a robust fair value estimate:

| Method | Fair Value | Weight | Rationale |
|--------|------------|--------|-----------|
"""

    # Add valuation methods
    for method_name, method_data in valuation['valuation_methods'].items():
        method_title = method_name.replace('_', ' ').title()
        document += f"| {method_title} | ${method_data['fair_value']:.2f} | {method_data['confidence']:.0%} | "

        if method_name == 'dcf':
            document += f"WACC: {method_data['assumptions']['wacc']:.0%}, Terminal Growth: {method_data['assumptions']['terminal_growth']:.0%}"
        elif method_name == 'pe_multiple':
            document += f"Target P/E: {method_data['target_pe']:.1f}x"
        elif method_name == 'peg_ratio':
            document += f"Target PEG: {method_data['target_peg']:.1f}"
        else:
            document += "Sector comparison"

        document += " |\n"

    document += f"""| **Weighted Average** | **${valuation['fair_value']:.2f}** | **100%** | **{valuation['upside_potential']:.1%} upside** |

## Investment Thesis

"""

    # Add thesis components
    for component in investment_thesis['thesis_components']:
        document += f"""### {component['aspect']}
**Strength**: {component['strength']}
{component['rationale']}

"""

    document += f"""## Scenario Analysis

### Probability-Weighted Outcomes
Target Price: ${scenario_analysis['probability_weighted_target']:.2f} ({scenario_analysis['probability_weighted_upside']:.1%} upside)

"""

    # Add scenarios
    for scenario_name, scenario_data in scenario_analysis['scenarios'].items():
        scenario_title = scenario_name.replace('_', ' ').title()
        document += f"""### {scenario_title} (Probability: {scenario_data['probability']:.0%})
**Target Price**: ${scenario_data['target_price']:.2f} ({scenario_data['upside']:.1%} return)

**Key Assumptions:**
"""
        for assumption in scenario_data['assumptions']:
            document += f"- {assumption}\n"

        document += f"""
**Expected Metrics:**
- Revenue Growth: {scenario_data['key_metrics']['revenue_growth']}
- Margin Impact: {scenario_data['key_metrics']['margin_expansion']}
- EPS Growth: {scenario_data['key_metrics']['eps_growth']}

"""

    document += f"""## Risk Assessment

### Key Risk Factors
Overall Risk Rating: **{risks['risk_rating']}** ({risks['overall_risk_score']:.1%})

"""

    # Add top risks
    sorted_risks = sorted(risks['risk_factors'].items(), key=lambda x: x[1]['risk_score'], reverse=True)
    for risk_name, risk_data in sorted_risks[:3]:
        risk_title = risk_name.replace('_', ' ').title()
        document += f"""**{risk_title}**
*Risk Score: {risk_data['risk_score']:.1%} (Severity: {risk_data['severity']:.0%} × Probability: {risk_data['probability']:.0%})*
{risk_data['description']}

"""

    document += f"""## Analyst Consensus

Current Wall Street consensus reflects {analyst_data['recommendation']} with:
- Average Price Target: ${analyst_data['target_mean']:.2f}
- High Target: ${analyst_data['target_high']:.2f}
- Low Target: ${analyst_data['target_low']:.2f}
- Number of Analysts: {analyst_data['number_of_analysts']}

Our fair value estimate of ${valuation['fair_value']:.2f} {"exceeds" if valuation['fair_value'] > analyst_data['target_mean'] else "aligns with" if abs(valuation['fair_value'] - analyst_data['target_mean']) < 10 else "is below"} consensus estimates.

## Investment Recommendation

Based on our comprehensive fundamental analysis, we issue a **{investment_thesis['investment_recommendation']}** rating for Mastercard Incorporated with a {investment_thesis['time_horizon']} investment horizon.

**Key Takeaways:**
1. **Business Quality**: Exceptional competitive positioning with sustainable moat
2. **Financial Strength**: Industry-leading margins and returns on capital
3. **Growth Trajectory**: Multiple secular tailwinds supporting double-digit growth
4. **Valuation**: Current price offers attractive risk-reward with {valuation['upside_potential']:.1%} upside
5. **Risk Profile**: Well-managed risks with strong operational resilience

**Action**: Investors should consider {"initiating or adding to positions" if investment_thesis['investment_recommendation'] == "BUY" else "maintaining positions" if investment_thesis['investment_recommendation'] == "HOLD" else "reducing exposure"} in Mastercard at current levels.

---

**Author**: Cole Morton
**Confidence**: {investment_thesis['overall_confidence']:.1f}
**Data Quality**: {discovery_data['data_quality']['overall_score']:.1f}
"""

    # Save the document
    output_path = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis"
    output_file = os.path.join(output_path, f"{ticker}_{datetime.now().strftime('%Y%m%d')}.md")

    with open(output_file, 'w') as f:
        f.write(document)

    # Also save synthesis data
    synthesis_data = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "valuation": valuation,
        "investment_thesis": investment_thesis,
        "scenario_analysis": scenario_analysis,
        "document_location": output_file,
        "synthesis_confidence": investment_thesis['overall_confidence']
    }

    synthesis_output_path = "/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/synthesize/outputs"
    synthesis_output_file = os.path.join(synthesis_output_path, f"synthesize_{ticker}_{datetime.now().strftime('%Y%m%d')}.json")

    with open(synthesis_output_file, 'w') as f:
        json.dump(synthesis_data, f, indent=2)

    print(f"✅ Phase 3 Complete: Investment analysis saved to {output_file}")
    print(f"📊 Fair Value: ${valuation['fair_value']:.2f} ({valuation['upside_potential']:+.1%} upside)")
    print(f"🎯 Recommendation: {investment_thesis['investment_recommendation']}")
    print(f"💎 Thesis Confidence: {investment_thesis['overall_confidence']:.1%}")

    return synthesis_data

if __name__ == "__main__":
    # Execute synthesis phase
    synthesis_data = synthesize_investment_analysis("MA")
