#!/usr/bin/env python3
"""Debug dashboard generation to isolate the profit factor issue."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from scripts.utils.dashboard_parser import parse_dashboard_data
from scripts.utils.theme_manager import create_theme_manager

# Parse data
print("Parsing data...")
data = parse_dashboard_data('data/outputs/analysis_trade_history/HISTORICAL_PERFORMANCE_REPORT_20250626.md')
metrics = data['performance_metrics']

print(f"Metrics object: {metrics}")
print(f"Profit factor: {metrics.profit_factor}")

# Test theme manager
print("\nTesting theme manager...")
theme_manager = create_theme_manager()
theme = theme_manager.get_theme_colors("light")
print(f"Theme background: {theme.background}")

# Test the exact formatting used in dashboard
print("\nTesting dashboard formatting...")
metric_positions = [
    {"x": 0.125, "title": "Win Rate", "value": f"{getattr(metrics, 'win_rate', 0):.1f}%", "color": "#26c6da"},
    {"x": 0.375, "title": "Total Return", "value": f"{getattr(metrics, 'total_return', 0):+.1f}%", "color": "#26c6da" if getattr(metrics, 'total_return', 0) >= 0 else "#ff7043"},
    {"x": 0.625, "title": "Profit Factor", "value": f"{getattr(metrics, 'profit_factor', 0):.2f}", "color": "#7e57c2"},
    {"x": 0.875, "title": "Total Trades", "value": f"{getattr(metrics, 'total_trades', 0)}", "color": "#3179f5"}
]

for metric in metric_positions:
    print(f"{metric['title']}: {metric['value']}")

print("\nData summary:")
print(f"  Trades: {len(data['trades'])}")
print(f"  Monthly data: {len(data['monthly_performance'])}")
print(f"  Quality data: {len(data['quality_distribution'])}")

if len(data['trades']) > 0:
    print(f"  First trade: {data['trades'][0]}")
else:
    print("  No trades found!")

print("\nDone!")
