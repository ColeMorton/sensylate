#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

# Load the tickers list
with open('tickers_list.json', 'r') as f:
    all_tickers = json.load(f)

# Find fundamental analysis files
fundamental_dir = Path('./fundamental_analysis')
fundamental_files = {}
analysis_coverage = {}

if fundamental_dir.exists():
    for file in fundamental_dir.glob('*.md'):
        filename = file.name
        if '_' in filename:
            ticker = filename.split('_')[0]
            date_str = filename.split('_')[1].split('.')[0]

            if ticker in all_tickers:
                if ticker not in fundamental_files:
                    fundamental_files[ticker] = []
                fundamental_files[ticker].append({
                    'file': filename,
                    'date': date_str,
                    'path': str(file)
                })

# Get most recent analysis for each ticker
for ticker in all_tickers:
    if ticker in fundamental_files:
        # Sort by date and get most recent
        sorted_files = sorted(fundamental_files[ticker], key=lambda x: x['date'], reverse=True)
        most_recent = sorted_files[0]

        analysis_coverage[ticker] = {
            'file': most_recent['file'],
            'date': most_recent['date'],
            'path': most_recent['path']
        }

# Calculate coverage statistics
total_tickers = len(all_tickers)
covered_tickers = len(analysis_coverage)
coverage_percentage = (covered_tickers / total_tickers) * 100

coverage_data = {
    'total_tickers': total_tickers,
    'covered_tickers': covered_tickers,
    'coverage_percentage': coverage_percentage,
    'analysis_files': analysis_coverage
}

# Save fundamental integration data
with open('fundamental_integration.json', 'w') as f:
    json.dump(coverage_data, f, indent=2)

print('Fundamental Analysis Coverage:')
print('Total tickers: {}'.format(total_tickers))
print('Covered tickers: {}'.format(covered_tickers))
print('Coverage percentage: {:.1f}%'.format(coverage_percentage))
print('\nCovered tickers:')
for ticker in sorted(analysis_coverage.keys()):
    print('  {}: {}'.format(ticker, analysis_coverage[ticker]['file']))
