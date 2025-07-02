#!/usr/bin/env python3
"""
Phase 1: Discover - Comprehensive Data Collection for Mastercard (MA)
"""

import json
import yfinance as yf
from datetime import datetime, timedelta
import os

def discover_fundamental_data(ticker="MA"):
    """Execute comprehensive data discovery for fundamental analysis"""

    print(f"🔍 Phase 1: Discover - Collecting data for {ticker}")

    # Initialize Yahoo Finance ticker
    stock = yf.Ticker(ticker)

    # Get current market data
    info = stock.info
    current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))

    # Collect comprehensive data
    discovery_data = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "company_info": {
            "name": info.get('longName', 'Mastercard Incorporated'),
            "sector": info.get('sector', 'Financial Services'),
            "industry": info.get('industry', 'Credit Services'),
            "country": info.get('country', 'United States'),
            "website": info.get('website', 'https://www.mastercard.com'),
            "employees": info.get('fullTimeEmployees', 0),
            "description": info.get('longBusinessSummary', '')
        },
        "market_data": {
            "current_price": current_price,
            "market_cap": info.get('marketCap', 0),
            "enterprise_value": info.get('enterpriseValue', 0),
            "shares_outstanding": info.get('sharesOutstanding', 0),
            "float_shares": info.get('floatShares', 0),
            "beta": info.get('beta', 0),
            "52_week_high": info.get('fiftyTwoWeekHigh', 0),
            "52_week_low": info.get('fiftyTwoWeekLow', 0),
            "50_day_avg": info.get('fiftyDayAverage', 0),
            "200_day_avg": info.get('twoHundredDayAverage', 0),
            "volume": info.get('volume', 0),
            "avg_volume": info.get('averageVolume', 0)
        },
        "financial_metrics": {
            "revenue_ttm": info.get('totalRevenue', 0),
            "revenue_per_share": info.get('revenuePerShare', 0),
            "gross_profit": info.get('grossProfits', 0),
            "ebitda": info.get('ebitda', 0),
            "net_income": info.get('netIncomeToCommon', 0),
            "earnings_per_share": info.get('trailingEps', 0),
            "forward_eps": info.get('forwardEps', 0),
            "pe_ratio": info.get('trailingPE', 0),
            "forward_pe": info.get('forwardPE', 0),
            "peg_ratio": info.get('pegRatio', 0),
            "price_to_book": info.get('priceToBook', 0),
            "price_to_sales": info.get('priceToSalesTrailing12Months', 0),
            "ev_to_revenue": info.get('enterpriseToRevenue', 0),
            "ev_to_ebitda": info.get('enterpriseToEbitda', 0),
            "profit_margin": info.get('profitMargins', 0),
            "operating_margin": info.get('operatingMargins', 0),
            "gross_margin": info.get('grossMargins', 0),
            "ebitda_margin": info.get('ebitdaMargins', 0),
            "return_on_assets": info.get('returnOnAssets', 0),
            "return_on_equity": info.get('returnOnEquity', 0),
            "revenue_growth": info.get('revenueGrowth', 0),
            "earnings_growth": info.get('earningsGrowth', 0),
            "free_cash_flow": info.get('freeCashflow', 0),
            "operating_cash_flow": info.get('operatingCashflow', 0),
            "total_cash": info.get('totalCash', 0),
            "total_debt": info.get('totalDebt', 0),
            "current_ratio": info.get('currentRatio', 0),
            "quick_ratio": info.get('quickRatio', 0),
            "debt_to_equity": info.get('debtToEquity', 0)
        },
        "analyst_data": {
            "recommendation": info.get('recommendationKey', ''),
            "recommendation_mean": info.get('recommendationMean', 0),
            "number_of_analysts": info.get('numberOfAnalystOpinions', 0),
            "target_high": info.get('targetHighPrice', 0),
            "target_low": info.get('targetLowPrice', 0),
            "target_mean": info.get('targetMeanPrice', 0),
            "target_median": info.get('targetMedianPrice', 0)
        },
        "dividend_data": {
            "dividend_rate": info.get('dividendRate', 0),
            "dividend_yield": info.get('dividendYield', 0),
            "ex_dividend_date": info.get('exDividendDate', 0),
            "payout_ratio": info.get('payoutRatio', 0),
            "five_year_avg_yield": info.get('fiveYearAvgDividendYield', 0),
            "trailing_annual_dividend": info.get('trailingAnnualDividendRate', 0),
            "trailing_annual_yield": info.get('trailingAnnualDividendYield', 0)
        }
    }

    # Get historical financial data
    try:
        # Income statement
        income_stmt = stock.income_stmt
        quarterly_income = stock.quarterly_income_stmt

        # Balance sheet
        balance_sheet = stock.balance_sheet
        quarterly_balance = stock.quarterly_balance_sheet

        # Cash flow
        cash_flow = stock.cash_flow
        quarterly_cash = stock.quarterly_cash_flow

        # Add to discovery data (convert to JSON-serializable format)
        discovery_data["financial_statements"] = {
            "income_statement": income_stmt.to_dict('list') if not income_stmt.empty else {},
            "balance_sheet": balance_sheet.to_dict('list') if not balance_sheet.empty else {},
            "cash_flow": cash_flow.to_dict('list') if not cash_flow.empty else {},
            "quarterly_income": quarterly_income.to_dict('list') if not quarterly_income.empty else {},
            "quarterly_balance": quarterly_balance.to_dict('list') if not quarterly_balance.empty else {},
            "quarterly_cash": quarterly_cash.to_dict('list') if not quarterly_cash.empty else {}
        }
    except Exception as e:
        print(f"Warning: Could not fetch some financial statements: {e}")
        discovery_data["financial_statements"] = {}

    # Get peer companies
    peers = ["V", "AXP", "PYPL", "SQ", "DFS"]  # Visa, Amex, PayPal, Block, Discover
    peer_data = {}

    for peer in peers:
        try:
            peer_stock = yf.Ticker(peer)
            peer_info = peer_stock.info
            peer_data[peer] = {
                "name": peer_info.get('longName', peer),
                "market_cap": peer_info.get('marketCap', 0),
                "pe_ratio": peer_info.get('trailingPE', 0),
                "profit_margin": peer_info.get('profitMargins', 0),
                "revenue_growth": peer_info.get('revenueGrowth', 0),
                "price": peer_info.get('currentPrice', peer_info.get('regularMarketPrice', 0))
            }
        except:
            print(f"Warning: Could not fetch data for peer {peer}")

    discovery_data["peer_comparison"] = peer_data

    # Calculate data quality score
    data_quality = calculate_data_quality(discovery_data)
    discovery_data["data_quality"] = data_quality

    # Save discovery data
    output_path = "/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/discover/outputs"
    output_file = os.path.join(output_path, f"discover_{ticker}_{datetime.now().strftime('%Y%m%d')}.json")

    with open(output_file, 'w') as f:
        json.dump(discovery_data, f, indent=2, default=str)

    print(f"✅ Phase 1 Complete: Discovery data saved to {output_file}")
    print(f"📊 Data Quality Score: {data_quality['overall_score']:.1%}")

    return discovery_data

def calculate_data_quality(data):
    """Calculate data quality score based on completeness"""
    scores = []

    # Check market data completeness
    market_fields = ['current_price', 'market_cap', 'enterprise_value', 'shares_outstanding']
    market_complete = sum(1 for f in market_fields if data['market_data'].get(f, 0) > 0)
    scores.append(market_complete / len(market_fields))

    # Check financial metrics completeness
    key_metrics = ['revenue_ttm', 'net_income', 'earnings_per_share', 'pe_ratio',
                   'profit_margin', 'return_on_equity', 'free_cash_flow']
    metrics_complete = sum(1 for m in key_metrics if data['financial_metrics'].get(m, 0) != 0)
    scores.append(metrics_complete / len(key_metrics))

    # Check analyst data
    analyst_fields = ['recommendation', 'target_mean', 'number_of_analysts']
    analyst_complete = sum(1 for f in analyst_fields if data['analyst_data'].get(f))
    scores.append(analyst_complete / len(analyst_fields))

    # Check peer data
    peer_count = len(data.get('peer_comparison', {}))
    scores.append(min(peer_count / 5, 1.0))

    overall_score = sum(scores) / len(scores)

    return {
        "overall_score": overall_score,
        "market_data_score": scores[0],
        "financial_metrics_score": scores[1],
        "analyst_data_score": scores[2],
        "peer_data_score": scores[3],
        "threshold_met": overall_score >= 0.9
    }

if __name__ == "__main__":
    # Execute discovery phase
    discovery_data = discover_fundamental_data("MA")
