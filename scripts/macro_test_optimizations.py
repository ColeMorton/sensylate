#!/usr/bin/env python3
"""
Quick test of macro analysis optimizations
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def test_quality_improvements():
    """Test quality improvements achieved through optimization"""

    # Read the original analysis output
    original_file = "data/outputs/macro_analysis/analysis/asia_20250806_analysis.json"

    if not Path(original_file).exists():
        print(f"❌ Original analysis file not found: {original_file}")
        return

    with open(original_file, "r") as f:
        original_data = json.load(f)

    print("🔍 Analyzing Quality Improvements")
    print("=" * 50)

    # Analyze confidence scores
    print("📊 Confidence Scores Analysis:")
    confidence_sections = {}
    for section_name, section_data in original_data.items():
        if isinstance(section_data, dict) and "confidence" in section_data:
            confidence = section_data["confidence"]
            confidence_sections[section_name] = confidence
            status = "✅ PASS" if confidence >= 0.9 else "❌ BELOW THRESHOLD"
            print(f"  {section_name}: {confidence:.3f} {status}")

    # Analyze template completeness
    print(f"\n📋 Template Completeness Analysis:")
    required_sections = [
        "business_cycle_modeling",
        "liquidity_cycle_positioning",
        "market_regime_classification",
        "economic_scenario_analysis",
        "quantified_risk_assessment",
        "industry_dynamics_scorecard",
        "multi_method_valuation",
        "enhanced_economic_sensitivity",
        "macroeconomic_risk_scoring",
        "investment_recommendation_gap_analysis",
    ]

    present_sections = []
    missing_sections = []

    for section in required_sections:
        if section in original_data:
            present_sections.append(section)
            print(f"  ✅ {section}")
        else:
            missing_sections.append(section)
            print(f"  ❌ {section} (MISSING)")

    completion_rate = len(present_sections) / len(required_sections)
    print(f"\n📈 Template Completion Rate: {completion_rate:.1%}")

    # Analyze quality metrics
    quality_metrics = original_data.get("analysis_quality_metrics", {})
    print(f"\n🎯 Analysis Quality Metrics:")
    for metric, value in quality_metrics.items():
        if isinstance(value, (int, float)):
            status = (
                "✅ GOOD"
                if value >= 0.9
                else "⚠️ NEEDS IMPROVEMENT"
                if value >= 0.8
                else "❌ POOR"
            )
            print(f"  {metric}: {value:.3f} {status}")
        else:
            print(f"  {metric}: {value}")

    # Calculate overall quality score
    avg_confidence = (
        sum(confidence_sections.values()) / len(confidence_sections)
        if confidence_sections
        else 0.0
    )
    overall_quality = (completion_rate + avg_confidence) / 2

    print(f"\n🏆 Overall Quality Assessment:")
    print(f"  Average Confidence: {avg_confidence:.3f}")
    print(f"  Template Completeness: {completion_rate:.3f}")
    print(f"  Overall Quality Score: {overall_quality:.3f}")

    # Recommendations
    print(f"\n💡 Optimization Status:")
    if overall_quality >= 0.9:
        print("  ✅ Quality targets achieved!")
    else:
        print("  ⚠️ Further optimization needed:")
        if avg_confidence < 0.9:
            print("    - Boost confidence scores through improved data utilization")
        if completion_rate < 1.0:
            print(f"    - Implement {len(missing_sections)} missing template sections")
        if len([c for c in confidence_sections.values() if c < 0.9]) > 0:
            print(
                f"    - Fix {len([c for c in confidence_sections.values() if c < 0.9])} sections below confidence threshold"
            )

    return {
        "overall_quality": overall_quality,
        "avg_confidence": avg_confidence,
        "completion_rate": completion_rate,
        "confidence_sections": confidence_sections,
        "missing_sections": missing_sections,
    }


if __name__ == "__main__":
    results = test_quality_improvements()

    print(f"\n📋 Test Summary:")
    print(f"  Overall Quality Score: {results['overall_quality']:.3f}")
    print(
        f"  Confidence Threshold Met: {'✅' if results['avg_confidence'] >= 0.9 else '❌'}"
    )
    print(f"  Template Complete: {'✅' if results['completion_rate'] == 1.0 else '❌'}")
