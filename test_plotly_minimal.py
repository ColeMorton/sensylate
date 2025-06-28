#!/usr/bin/env python3
"""Minimal Plotly test to isolate dashboard generation issues."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scripts.utils.dashboard_parser import parse_dashboard_data
from scripts.utils.theme_manager import create_theme_manager

def test_minimal_dashboard():
    """Create a minimal dashboard to test basic functionality."""
    print("Starting minimal dashboard test...")

    # Parse data
    data = parse_dashboard_data('data/outputs/analysis_trade_history/HISTORICAL_PERFORMANCE_REPORT_20250626.md')
    metrics = data['performance_metrics']

    print(f"Parsed metrics: win_rate={metrics.win_rate}, profit_factor={metrics.profit_factor}")

    # Create simple figure
    fig = go.Figure()

    # Add a simple annotation to test
    fig.add_annotation(
        x=0.5, y=0.5,
        text=f"Profit Factor: {metrics.profit_factor:.2f}",
        showarrow=False,
        font=dict(size=20),
        xref="paper", yref="paper"
    )

    # Set layout
    fig.update_layout(
        title="Test Dashboard",
        width=800, height=600,
        paper_bgcolor="white"
    )

    # Try to save
    output_path = "data/outputs/dashboards/test_minimal.png"
    try:
        print(f"Attempting to save to {output_path}...")
        fig.write_image(output_path, format="png", width=800, height=600, scale=2)
        print(f"✅ Successfully saved minimal dashboard to {output_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to save dashboard: {e}")
        return False

if __name__ == "__main__":
    success = test_minimal_dashboard()
    if success:
        print("\n✅ Minimal test passed - Plotly is working")
    else:
        print("\n❌ Minimal test failed - Issue with Plotly setup")
