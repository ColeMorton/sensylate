#!/usr/bin/env python3
"""
Visual comparison test for Phase 3 complex charts.

This module generates side-by-side comparisons of matplotlib vs Plotly
implementations for waterfall and scatter charts.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.test_phase3_implementation import create_test_trade_data
from scripts.utils.chart_comparison_framework import ChartComparisonFramework
from scripts.utils.chart_generator_factory import ChartGeneratorFactory
from scripts.utils.scalability_manager import create_scalability_manager
from scripts.utils.theme_manager import create_theme_manager


def main():
    """Run visual comparison for Phase 3 charts."""
    print("🎨 Starting Phase 3 Visual Comparison")
    print("=" * 50)

    # Initialize components
    theme_manager = create_theme_manager()

    scalability_config = {
        "scalability": {
            "trade_volume_thresholds": {"small": 50, "medium": 100, "large": 200}
        }
    }
    scalability_manager = create_scalability_manager(scalability_config)

    # Create chart generators
    matplotlib_generator = ChartGeneratorFactory.create_chart_generator(
        "matplotlib", theme_manager, scalability_manager
    )
    plotly_generator = ChartGeneratorFactory.create_chart_generator(
        "plotly", theme_manager, scalability_manager
    )

    # Create comparison framework
    comparison_framework = ChartComparisonFramework(
        "data/outputs/phase3_visual_comparisons"
    )

    # Test data
    small_trades = create_test_trade_data("small")  # Will show waterfall
    medium_trades = create_test_trade_data("medium")  # Will show scatter

    print(
        f"📊 Testing with {len(small_trades)} small trades and {len(medium_trades)} medium trades"
    )

    results = []

    # Test waterfall chart comparison
    print("\n🔄 Comparing waterfall charts...")
    try:
        waterfall_result = comparison_framework.compare_charts(
            matplotlib_generator, plotly_generator, "waterfall", small_trades, "light"
        )
        results.append(waterfall_result)

        similarity = waterfall_result["similarity_metrics"]["similarity_percent"]
        print(f"  ✅ Waterfall similarity: {similarity:.1f}%")

    except Exception as e:
        print(f"  ❌ Waterfall comparison failed: {str(e)}")

    # Test scatter chart comparison
    print("\n🔄 Comparing scatter charts...")
    try:
        scatter_result = comparison_framework.compare_charts(
            matplotlib_generator, plotly_generator, "scatter", medium_trades, "light"
        )
        results.append(scatter_result)

        similarity = scatter_result["similarity_metrics"]["similarity_percent"]
        print(f"  ✅ Scatter similarity: {similarity:.1f}%")

    except Exception as e:
        print(f"  ❌ Scatter comparison failed: {str(e)}")

    # Generate comparison report
    if results:
        print("\n📝 Generating comparison report...")
        report_path = comparison_framework.generate_test_report(results)
        print(f"  📄 Report saved to: {report_path}")

        # Calculate average similarity
        avg_similarity = sum(
            r["similarity_metrics"]["similarity_percent"] for r in results
        ) / len(results)
        print(f"\n📈 Average Visual Similarity: {avg_similarity:.1f}%")

        if avg_similarity >= 95:
            print("🎉 Phase 3 visual validation: EXCELLENT")
        elif avg_similarity >= 85:
            print("✅ Phase 3 visual validation: GOOD")
        else:
            print("⚠️  Phase 3 visual validation: NEEDS IMPROVEMENT")

    print("\n✨ Phase 3 visual comparison complete!")


if __name__ == "__main__":
    main()
