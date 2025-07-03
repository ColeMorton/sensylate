#!/usr/bin/env python3
import yfinance as yf
import json
from datetime import datetime

# Collect benchmark data
benchmarks = ['SPY', 'QQQ', 'VTI', '^VIX']
market_data = {}

for benchmark in benchmarks:
    try:
        ticker = yf.Ticker(benchmark)
        info = ticker.info
        ytd_data = ticker.history(period='ytd')

        if len(ytd_data) > 0:
            current_price = ytd_data['Close'].iloc[-1]
            first_price = ytd_data['Close'].iloc[0]
            ytd_return = (current_price - first_price) / first_price

            # Calculate volatility (annualized)
            returns = ytd_data['Close'].pct_change().dropna()
            volatility = returns.std() * (252 ** 0.5)  # Annualized

            market_data[benchmark] = {
                'current_price': float(current_price),
                'ytd_return': float(ytd_return),
                'volatility': float(volatility),
                'confidence': 0.95
            }
            print('{}: ${:.2f}, YTD: {:.2%}, Vol: {:.2%}'.format(benchmark, current_price, ytd_return, volatility))
        else:
            print('No data for {}'.format(benchmark))

    except Exception as e:
        print('Error getting {}: {}'.format(benchmark, e))

# Add economic context
market_data['economic_context'] = {
    'fed_funds_rate': 0.0525,  # Current approximate fed funds rate
    'rate_environment': 'restrictive',
    'confidence': 0.80
}

# Save market context
with open('market_context.json', 'w') as f:
    json.dump(market_data, f, indent=2)

print('Market context collected for {} instruments'.format(len(market_data)))
