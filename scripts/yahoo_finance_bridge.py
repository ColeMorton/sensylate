#!/usr/bin/env python3
"""
Yahoo Finance Bridge Script
Provides Yahoo Finance functionality for Claude Code when MCP is not available
"""

import json
import sys
from datetime import datetime
from typing import Any, Dict

import yfinance as yf


class YahooFinanceBridge:
    """Bridge class to provide Yahoo Finance functionality similar to MCP server"""

    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol,
                "name": info.get("longName", "N/A"),
                "current_price": info.get(
                    "currentPrice", info.get("regularMarketPrice")
                ),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "recommendation": info.get("recommendationKey"),
                "target_price": info.get("targetMeanPrice"),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e), "symbol": symbol}

    def get_historical_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """Get historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            return {
                "symbol": symbol,
                "period": period,
                "data": hist.to_dict(orient="records"),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e), "symbol": symbol}

    def get_financials(self, symbol: str) -> Dict[str, Any]:
        """Get financial statements"""
        try:
            ticker = yf.Ticker(symbol)

            return {
                "symbol": symbol,
                "income_statement": ticker.financials.to_dict()
                if not ticker.financials.empty
                else {},
                "balance_sheet": ticker.balance_sheet.to_dict()
                if not ticker.balance_sheet.empty
                else {},
                "cash_flow": ticker.cashflow.to_dict()
                if not ticker.cashflow.empty
                else {},
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e), "symbol": symbol}


def main() -> None:
    """Command line interface for the bridge"""
    if len(sys.argv) < 3:
        print("Usage: python yahoo_finance_bridge.py <command> <symbol> [options]")
        print("Commands: info, history, financials")
        sys.exit(1)

    command = sys.argv[1]
    symbol = sys.argv[2].upper()

    bridge = YahooFinanceBridge()

    if command == "info":
        result = bridge.get_stock_info(symbol)
    elif command == "history":
        period = sys.argv[3] if len(sys.argv) > 3 else "1y"
        result = bridge.get_historical_data(symbol, period)
    elif command == "financials":
        result = bridge.get_financials(symbol)
    else:
        result = {"error": f"Unknown command: {command}"}

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
