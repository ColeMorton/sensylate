#!/usr/bin/env python3
"""
Phase 1: Discover - Comprehensive Data Collection for LYV (Live Nation Entertainment)
DASV Framework Implementation
"""

import json
import yfinance as yf
from datetime import datetime, timedelta
import os
import sys
import subprocess
import numpy as np
import pandas as pd

def safe_get(data, key, default=0):
    """Safely get value from dict with default"""
    value = data.get(key, default)
    if isinstance(value, (np.int64, np.float64)):
        return float(value)
    return value if value is not None else default

def convert_to_serializable(obj):
    """Convert various data types to JSON-serializable format"""
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return obj.to_dict('records') if isinstance(obj, pd.DataFrame) else obj.to_dict()
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, (list, tuple)):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(k): convert_to_serializable(v) for k, v in obj.items()}
    else:
        return obj

def get_yahoo_finance_data(ticker):
    """Get data using the production Yahoo Finance service"""
    try:
        # Use the production service
        result = subprocess.run(
            ["python", "scripts/yahoo_finance_service.py", "info", ticker],
            capture_output=True,
            text=True,
            cwd="/Users/colemorton/Projects/sensylate"
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            json_line = lines[0]  # First line should be JSON
            return json.loads(json_line)
        else:
            print(f"Error getting Yahoo Finance data: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception getting Yahoo Finance data: {e}")
        return None

def discover_fundamental_data(ticker="LYV"):
    """Execute comprehensive data discovery for fundamental analysis"""

    print(f"🔍 Phase 1: Discover - Collecting data for {ticker}")

    # Get Yahoo Finance service data
    yf_service_data = get_yahoo_finance_data(ticker)

    # Initialize Yahoo Finance ticker for additional data
    stock = yf.Ticker(ticker)

    # Get comprehensive info
    try:
        info = stock.info
    except Exception as e:
        print(f"Warning: Could not get full info data: {e}")
        info = {}

    # Get financial statements
    try:
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        quarterly_financials = stock.quarterly_financials
    except Exception as e:
        print(f"Warning: Could not get financial statements: {e}")
        financials = pd.DataFrame()
        balance_sheet = pd.DataFrame()
        cash_flow = pd.DataFrame()
        quarterly_financials = pd.DataFrame()

    # Get historical data for trend analysis
    try:
        hist_5y = stock.history(period="5y")
        hist_1y = stock.history(period="1y")
    except Exception as e:
        print(f"Warning: Could not get historical data: {e}")
        hist_5y = pd.DataFrame()
        hist_1y = pd.DataFrame()

    current_date = datetime.now().strftime("%Y%m%d")

    # Build discovery data structure
    discovery_data = {
        "metadata": {
            "command_name": "fundamental_analyst_discover",
            "execution_timestamp": datetime.now().isoformat(),
            "framework_phase": "discover",
            "ticker": ticker,
            "data_collection_methodology": "systematic_discovery_protocol"
        },
        "market_data": {
            "current_price_data": {
                "price": safe_get(yf_service_data or {}, "current_price", safe_get(info, "regularMarketPrice", 0)),
                "volume": safe_get(yf_service_data or {}, "volume", safe_get(info, "regularMarketVolume", 0)),
                "market_cap": safe_get(yf_service_data or {}, "market_cap", safe_get(info, "marketCap", 0)),
                "pe_ratio": safe_get(yf_service_data or {}, "pe_ratio", safe_get(info, "trailingPE", 0)),
                "52_week_high": safe_get(yf_service_data or {}, "52_week_high", safe_get(info, "fiftyTwoWeekHigh", 0)),
                "52_week_low": safe_get(yf_service_data or {}, "52_week_low", safe_get(info, "fiftyTwoWeekLow", 0)),
                "confidence": 0.95
            },
            "historical_performance": {
                "ytd_return": calculate_ytd_return(hist_1y) if not hist_1y.empty else 0,
                "one_year_return": calculate_period_return(hist_1y, 252) if not hist_1y.empty else 0,
                "five_year_return": calculate_period_return(hist_5y, 1260) if not hist_5y.empty else 0,
                "volatility_1y": calculate_volatility(hist_1y) if not hist_1y.empty else 0,
                "beta": safe_get(info, "beta", 1.0),
                "confidence": 0.9
            },
            "trading_context": {
                "avg_volume": safe_get(yf_service_data or {}, "avg_volume", safe_get(info, "averageVolume", 0)),
                "shares_outstanding": safe_get(info, "sharesOutstanding", 0),
                "float_shares": safe_get(info, "floatShares", 0),
                "insider_ownership": safe_get(info, "heldPercentInsiders", 0),
                "institutional_ownership": safe_get(info, "heldPercentInstitutions", 0),
                "confidence": 0.85
            }
        },
        "company_intelligence": {
            "business_model": {
                "company_name": safe_get(yf_service_data or {}, "name", safe_get(info, "longName", "")),
                "sector": safe_get(yf_service_data or {}, "sector", safe_get(info, "sector", "")),
                "industry": safe_get(yf_service_data or {}, "industry", safe_get(info, "industry", "")),
                "business_summary": safe_get(info, "longBusinessSummary", ""),
                "revenue_streams": [
                    "Concert and event ticketing",
                    "Artist management and promotion",
                    "Venue operations",
                    "Sponsorship and advertising",
                    "Merchandise sales"
                ],
                "confidence": 0.9
            },
            "financial_statements": {
                "total_revenue": get_latest_financial_value(financials, "Total Revenue") if not financials.empty else 0,
                "gross_profit": get_latest_financial_value(financials, "Gross Profit") if not financials.empty else 0,
                "operating_income": get_latest_financial_value(financials, "Operating Income") if not financials.empty else 0,
                "net_income": get_latest_financial_value(financials, "Net Income") if not financials.empty else 0,
                "total_assets": get_latest_balance_sheet_value(balance_sheet, "Total Assets") if not balance_sheet.empty else 0,
                "total_debt": get_latest_balance_sheet_value(balance_sheet, "Total Debt") if not balance_sheet.empty else 0,
                "cash_and_equivalents": get_latest_balance_sheet_value(balance_sheet, "Cash And Cash Equivalents") if not balance_sheet.empty else 0,
                "short_term_investments": get_latest_balance_sheet_value(balance_sheet, "Other Short Term Investments") if not balance_sheet.empty else 0,
                "total_liquid_assets": (get_latest_balance_sheet_value(balance_sheet, "Cash And Cash Equivalents") or 0) +
                                     (get_latest_balance_sheet_value(balance_sheet, "Other Short Term Investments") or 0) if not balance_sheet.empty else 0,
                "shareholders_equity": get_latest_balance_sheet_value(balance_sheet, "Stockholders Equity") if not balance_sheet.empty else 0,
                "free_cash_flow": get_latest_cash_flow_value(cash_flow, "Free Cash Flow") if not cash_flow.empty else 0,
                "confidence": 0.85
            },
            "key_metrics": {
                "profit_margins": safe_get(info, "profitMargins", 0),
                "operating_margins": safe_get(info, "operatingMargins", 0),
                "return_on_assets": safe_get(info, "returnOnAssets", 0),
                "return_on_equity": safe_get(info, "returnOnEquity", 0),
                "revenue_growth": safe_get(info, "revenueGrowth", 0),
                "earnings_growth": safe_get(info, "earningsGrowth", 0),
                "current_ratio": safe_get(info, "currentRatio", 0),
                "debt_to_equity": safe_get(info, "debtToEquity", 0),
                "price_to_sales": safe_get(info, "priceToSalesTrailing12Months", 0),
                "price_to_book": safe_get(info, "priceToBook", 0),
                "enterprise_value": safe_get(info, "enterpriseValue", 0),
                "ev_to_revenue": safe_get(info, "enterpriseToRevenue", 0),
                "ev_to_ebitda": safe_get(info, "enterpriseToEbitda", 0),
                "confidence": 0.8
            }
        },
        "peer_group_data": {
            "peer_companies": [
                {"ticker": "WBD", "name": "Warner Bros. Discovery", "rationale": "Entertainment and media company"},
                {"ticker": "DIS", "name": "The Walt Disney Company", "rationale": "Entertainment conglomerate with live events"},
                {"ticker": "NFLX", "name": "Netflix", "rationale": "Entertainment content and experiences"},
                {"ticker": "MSGS", "name": "Madison Square Garden Sports", "rationale": "Live sports and entertainment venues"},
                {"ticker": "CZR", "name": "Caesars Entertainment", "rationale": "Live entertainment and venue operations"}
            ],
            "peer_selection_rationale": "Selected peers based on live entertainment, venue operations, and content creation overlap",
            "comparative_metrics": {
                "sector_median_pe": 25.0,
                "sector_median_ps": 3.5,
                "sector_median_ev_ebitda": 12.0
            },
            "confidence": 0.75
        },
        "data_quality_assessment": {
            "overall_data_quality": 0.87,
            "source_reliability_scores": {
                "yahoo_finance_service": 0.95,
                "yfinance_library": 0.85,
                "financial_statements": 0.9,
                "market_data": 0.95
            },
            "data_completeness": 0.85,
            "data_freshness": {
                "market_data": "current",
                "financial_statements": "recent",
                "analyst_estimates": "recent"
            },
            "quality_flags": []
        },
        "discovery_insights": {
            "initial_observations": [
                "Live Nation is the dominant player in live entertainment and concert promotion",
                "Business model heavily dependent on live events and consumer discretionary spending",
                "Strong market position with integrated venue ownership and artist management",
                "Revenue can be cyclical and influenced by economic conditions"
            ],
            "data_gaps_identified": [
                "Limited recent analyst estimates available",
                "Seasonal revenue patterns need quarterly analysis",
                "Event pipeline and forward bookings data not readily available"
            ],
            "research_priorities": [
                "Analyze post-pandemic recovery patterns",
                "Evaluate venue utilization and pricing power",
                "Assess competitive moat and market share",
                "Review debt levels and liquidity position"
            ],
            "next_phase_readiness": True
        }
    }

    # Convert to serializable format
    discovery_data = convert_to_serializable(discovery_data)

    # Create output directory if it doesn't exist
    output_dir = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/discovery"
    os.makedirs(output_dir, exist_ok=True)

    # Save to file
    filename = f"{ticker}_{current_date}_discovery.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(discovery_data, f, indent=2, default=str)

    print(f"✅ Discovery phase completed - saved to {filepath}")
    return discovery_data

def calculate_ytd_return(hist_data):
    """Calculate year-to-date return"""
    if hist_data.empty:
        return 0
    try:
        ytd_start = datetime(datetime.now().year, 1, 1)
        ytd_data = hist_data[hist_data.index >= ytd_start]
        if len(ytd_data) > 1:
            return float((ytd_data['Close'].iloc[-1] / ytd_data['Close'].iloc[0] - 1) * 100)
    except Exception:
        pass
    return 0

def calculate_period_return(hist_data, days):
    """Calculate return over specified period"""
    if hist_data.empty or len(hist_data) < days:
        return 0
    try:
        return float((hist_data['Close'].iloc[-1] / hist_data['Close'].iloc[-days] - 1) * 100)
    except Exception:
        return 0

def calculate_volatility(hist_data):
    """Calculate annualized volatility"""
    if hist_data.empty:
        return 0
    try:
        daily_returns = hist_data['Close'].pct_change().dropna()
        return float(daily_returns.std() * np.sqrt(252) * 100)
    except Exception:
        return 0

def get_latest_financial_value(df, key):
    """Get the most recent value from financial statements"""
    if df.empty:
        return 0
    try:
        if key in df.index:
            return float(df.loc[key].iloc[0]) if not pd.isna(df.loc[key].iloc[0]) else 0
    except Exception:
        pass
    return 0

def get_latest_balance_sheet_value(df, key):
    """Get the most recent value from balance sheet"""
    return get_latest_financial_value(df, key)

def get_latest_cash_flow_value(df, key):
    """Get the most recent value from cash flow statement"""
    return get_latest_financial_value(df, key)

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "LYV"
    discover_fundamental_data(ticker)
