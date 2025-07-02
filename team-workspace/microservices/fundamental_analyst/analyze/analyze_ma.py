#!/usr/bin/env python3
"""
Phase 2: Analyze - Systematic Financial Analysis for Mastercard (MA)
"""

import json
import os
from datetime import datetime
import numpy as np

def load_discovery_data(ticker="MA"):
    """Load discovery data from Phase 1"""
    discovery_path = f"/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/discover/outputs/discover_{ticker}_{datetime.now().strftime('%Y%m%d')}.json"

    with open(discovery_path, 'r') as f:
        return json.load(f)

def analyze_financial_health(discovery_data):
    """4-dimensional financial health scorecard"""
    metrics = discovery_data['financial_metrics']

    # Profitability Score (0-1)
    profitability_scores = []

    # Net profit margin
    net_margin = metrics.get('profit_margin', 0)
    profitability_scores.append(min(net_margin / 0.30, 1.0))  # 30% is excellent

    # ROE
    roe = metrics.get('return_on_equity', 0)
    profitability_scores.append(min(roe / 0.50, 1.0))  # 50% is excellent

    # Operating margin
    op_margin = metrics.get('operating_margin', 0)
    profitability_scores.append(min(op_margin / 0.40, 1.0))  # 40% is excellent

    profitability_score = np.mean(profitability_scores)

    # Growth Score (0-1)
    growth_scores = []

    # Revenue growth
    rev_growth = metrics.get('revenue_growth', 0)
    growth_scores.append(min(rev_growth / 0.15, 1.0))  # 15% is excellent

    # Earnings growth
    earn_growth = metrics.get('earnings_growth', 0)
    growth_scores.append(min(earn_growth / 0.15, 1.0))  # 15% is excellent

    growth_score = np.mean(growth_scores)

    # Liquidity Score (0-1)
    liquidity_scores = []

    # Current ratio
    current_ratio = metrics.get('current_ratio', 0)
    liquidity_scores.append(min(current_ratio / 2.0, 1.0))  # 2.0 is excellent

    # Quick ratio
    quick_ratio = metrics.get('quick_ratio', 0)
    liquidity_scores.append(min(quick_ratio / 1.5, 1.0))  # 1.5 is excellent

    liquidity_score = np.mean(liquidity_scores)

    # Leverage Score (0-1, lower debt is better)
    leverage_scores = []

    # Debt to equity (inverted scale - lower is better)
    debt_equity = metrics.get('debt_to_equity', 0)
    if debt_equity > 0:
        leverage_scores.append(max(1 - (debt_equity / 200), 0))  # 0% is best, 200% is worst
    else:
        leverage_scores.append(1.0)

    leverage_score = np.mean(leverage_scores)

    return {
        "profitability_score": round(profitability_score, 3),
        "growth_score": round(growth_score, 3),
        "liquidity_score": round(liquidity_score, 3),
        "leverage_score": round(leverage_score, 3),
        "overall_health_score": round(np.mean([profitability_score, growth_score, liquidity_score, leverage_score]), 3),
        "details": {
            "net_margin": round(net_margin, 3),
            "roe": round(roe, 3),
            "operating_margin": round(op_margin, 3),
            "revenue_growth": round(rev_growth, 3),
            "earnings_growth": round(earn_growth, 3),
            "current_ratio": round(current_ratio, 3),
            "debt_to_equity": round(debt_equity, 3)
        }
    }

def analyze_competitive_position(discovery_data):
    """Analyze competitive position and moat"""
    company_metrics = discovery_data['financial_metrics']
    peers = discovery_data['peer_comparison']

    # Calculate relative metrics
    ma_market_cap = discovery_data['market_data']['market_cap']
    ma_pe = company_metrics.get('pe_ratio', 0)
    ma_margin = company_metrics.get('profit_margin', 0)
    ma_growth = company_metrics.get('revenue_growth', 0)

    # Peer comparison
    peer_analysis = {}
    for peer_ticker, peer_data in peers.items():
        peer_analysis[peer_ticker] = {
            "name": peer_data['name'],
            "market_cap_ratio": round(ma_market_cap / peer_data['market_cap'], 2) if peer_data['market_cap'] > 0 else 0,
            "pe_comparison": round(ma_pe - peer_data['pe_ratio'], 2) if peer_data['pe_ratio'] > 0 else 0,
            "margin_delta": round(ma_margin - peer_data['profit_margin'], 3),
            "growth_delta": round(ma_growth - peer_data['revenue_growth'], 3)
        }

    # Calculate competitive strength
    competitive_scores = []

    # Market position (size relative to peers)
    avg_market_cap_ratio = np.mean([p['market_cap_ratio'] for p in peer_analysis.values() if p['market_cap_ratio'] > 0])
    competitive_scores.append(min(avg_market_cap_ratio / 2.0, 1.0))  # 2x peers is strong

    # Profitability advantage
    margin_advantages = [p['margin_delta'] for p in peer_analysis.values()]
    avg_margin_advantage = np.mean(margin_advantages)
    competitive_scores.append(min((avg_margin_advantage + 0.1) / 0.2, 1.0))  # 10% better is strong

    # Growth advantage
    growth_advantages = [p['growth_delta'] for p in peer_analysis.values()]
    avg_growth_advantage = np.mean(growth_advantages)
    competitive_scores.append(min((avg_growth_advantage + 0.05) / 0.1, 1.0))  # 5% better is strong

    competitive_strength = np.mean(competitive_scores)

    # Moat analysis
    moat_factors = {
        "network_effects": 0.9,  # Very strong for payment networks
        "switching_costs": 0.8,  # High for financial infrastructure
        "scale_advantages": 0.85,  # Strong economies of scale
        "brand_strength": 0.9,  # Global brand recognition
        "regulatory_barriers": 0.7  # Moderate regulatory requirements
    }

    moat_score = np.mean(list(moat_factors.values()))

    return {
        "competitive_strength": round(competitive_strength, 3),
        "moat_score": round(moat_score, 3),
        "peer_analysis": peer_analysis,
        "moat_factors": moat_factors,
        "market_position": "Leader" if avg_market_cap_ratio > 1.5 else "Major Player" if avg_market_cap_ratio > 0.7 else "Challenger"
    }

def identify_growth_drivers(discovery_data):
    """Identify and quantify growth drivers"""
    metrics = discovery_data['financial_metrics']

    growth_drivers = {
        "digital_payments_adoption": {
            "impact": 0.8,
            "confidence": 0.9,
            "description": "Continued shift from cash to digital payments globally"
        },
        "cross_border_expansion": {
            "impact": 0.7,
            "confidence": 0.85,
            "description": "Growth in international commerce and travel"
        },
        "value_added_services": {
            "impact": 0.6,
            "confidence": 0.8,
            "description": "Expansion beyond core payments (analytics, security, consulting)"
        },
        "emerging_markets": {
            "impact": 0.75,
            "confidence": 0.85,
            "description": "Financial inclusion in developing economies"
        },
        "b2b_payments": {
            "impact": 0.65,
            "confidence": 0.8,
            "description": "Commercial and B2B payment solutions growth"
        }
    }

    # Calculate weighted growth potential
    total_impact = sum(d['impact'] * d['confidence'] for d in growth_drivers.values())
    total_confidence = sum(d['confidence'] for d in growth_drivers.values())

    weighted_growth_potential = total_impact / total_confidence if total_confidence > 0 else 0

    return {
        "growth_drivers": growth_drivers,
        "weighted_growth_potential": round(weighted_growth_potential, 3),
        "revenue_growth_rate": metrics.get('revenue_growth', 0),
        "earnings_growth_rate": metrics.get('earnings_growth', 0),
        "growth_sustainability": round(min(weighted_growth_potential / 0.6, 1.0), 3)  # 0.6 is sustainable threshold
    }

def assess_risks(discovery_data):
    """Comprehensive risk assessment"""
    metrics = discovery_data['financial_metrics']
    market_data = discovery_data['market_data']

    risk_factors = {
        "regulatory_risk": {
            "severity": 0.6,
            "probability": 0.7,
            "description": "Increased payment regulation and interchange fee pressure"
        },
        "competition_risk": {
            "severity": 0.5,
            "probability": 0.8,
            "description": "Competition from fintech and alternative payment methods"
        },
        "economic_sensitivity": {
            "severity": 0.7,
            "probability": 0.5,
            "description": "Exposure to consumer spending and economic cycles"
        },
        "technology_disruption": {
            "severity": 0.6,
            "probability": 0.6,
            "description": "Blockchain and cryptocurrency payment alternatives"
        },
        "cybersecurity_risk": {
            "severity": 0.8,
            "probability": 0.4,
            "description": "Data breaches and security incidents"
        }
    }

    # Calculate risk scores
    risk_scores = []
    for risk_name, risk_data in risk_factors.items():
        risk_score = risk_data['severity'] * risk_data['probability']
        risk_data['risk_score'] = round(risk_score, 3)
        risk_scores.append(risk_score)

    overall_risk = np.mean(risk_scores)

    # Beta-based market risk
    beta = market_data.get('beta', 1.0)
    market_risk = min(beta / 1.5, 1.0)  # Beta > 1.5 is high risk

    return {
        "risk_factors": risk_factors,
        "overall_risk_score": round(overall_risk, 3),
        "market_risk_score": round(market_risk, 3),
        "beta": beta,
        "risk_rating": "Low" if overall_risk < 0.3 else "Moderate" if overall_risk < 0.6 else "High"
    }

def prepare_valuation_inputs(discovery_data):
    """Prepare inputs for valuation models"""
    metrics = discovery_data['financial_metrics']
    market_data = discovery_data['market_data']

    # Extract key valuation inputs
    valuation_inputs = {
        "current_price": market_data['current_price'],
        "shares_outstanding": market_data['shares_outstanding'],
        "market_cap": market_data['market_cap'],
        "enterprise_value": market_data['enterprise_value'],
        "trailing_pe": metrics.get('pe_ratio', 0),
        "forward_pe": metrics.get('forward_pe', 0),
        "peg_ratio": metrics.get('peg_ratio', 0),
        "price_to_book": metrics.get('price_to_book', 0),
        "price_to_sales": metrics.get('price_to_sales', 0),
        "ev_to_revenue": metrics.get('ev_to_revenue', 0),
        "ev_to_ebitda": metrics.get('ev_to_ebitda', 0),
        "free_cash_flow": metrics.get('free_cash_flow', 0),
        "fcf_per_share": metrics.get('free_cash_flow', 0) / market_data['shares_outstanding'] if market_data['shares_outstanding'] > 0 else 0,
        "earnings_per_share": metrics.get('earnings_per_share', 0),
        "revenue_ttm": metrics.get('revenue_ttm', 0),
        "ebitda": metrics.get('ebitda', 0),
        "net_income": metrics.get('net_income', 0),
        "growth_rate": metrics.get('revenue_growth', 0),
        "margin": metrics.get('profit_margin', 0),
        "roe": metrics.get('return_on_equity', 0)
    }

    # Calculate additional metrics
    if valuation_inputs['fcf_per_share'] > 0:
        valuation_inputs['fcf_yield'] = valuation_inputs['fcf_per_share'] / valuation_inputs['current_price']
    else:
        valuation_inputs['fcf_yield'] = 0

    if valuation_inputs['earnings_per_share'] > 0:
        valuation_inputs['earnings_yield'] = valuation_inputs['earnings_per_share'] / valuation_inputs['current_price']
    else:
        valuation_inputs['earnings_yield'] = 0

    return valuation_inputs

def analyze_fundamental_data(ticker="MA"):
    """Execute comprehensive fundamental analysis"""

    print(f"📊 Phase 2: Analyze - Performing systematic analysis for {ticker}")

    # Load discovery data
    discovery_data = load_discovery_data(ticker)

    # Perform analyses
    financial_health = analyze_financial_health(discovery_data)
    competitive_position = analyze_competitive_position(discovery_data)
    growth_drivers = identify_growth_drivers(discovery_data)
    risk_assessment = assess_risks(discovery_data)
    valuation_inputs = prepare_valuation_inputs(discovery_data)

    # Calculate overall analysis confidence
    confidence_factors = [
        discovery_data['data_quality']['overall_score'],
        financial_health['overall_health_score'],
        competitive_position['competitive_strength'],
        growth_drivers['growth_sustainability'],
        1 - risk_assessment['overall_risk_score']
    ]

    overall_confidence = np.mean(confidence_factors)

    # Compile analysis results
    analysis_data = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "financial_health": financial_health,
        "competitive_position": competitive_position,
        "growth_drivers": growth_drivers,
        "risk_assessment": risk_assessment,
        "valuation_inputs": valuation_inputs,
        "analysis_confidence": round(overall_confidence, 3),
        "investment_grade": "Strong Buy" if overall_confidence > 0.8 else "Buy" if overall_confidence > 0.65 else "Hold" if overall_confidence > 0.5 else "Sell"
    }

    # Save analysis data
    output_path = "/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/analyze/outputs"
    output_file = os.path.join(output_path, f"analyze_{ticker}_{datetime.now().strftime('%Y%m%d')}.json")

    with open(output_file, 'w') as f:
        json.dump(analysis_data, f, indent=2)

    print(f"✅ Phase 2 Complete: Analysis data saved to {output_file}")
    print(f"💎 Financial Health Score: {financial_health['overall_health_score']:.1%}")
    print(f"🏆 Competitive Strength: {competitive_position['competitive_strength']:.1%}")
    print(f"📈 Growth Potential: {growth_drivers['weighted_growth_potential']:.1%}")
    print(f"⚠️  Risk Score: {risk_assessment['overall_risk_score']:.1%}")
    print(f"🎯 Analysis Confidence: {overall_confidence:.1%}")

    return analysis_data

if __name__ == "__main__":
    # Execute analysis phase
    analysis_data = analyze_fundamental_data("MA")
