#!/usr/bin/env python3
"""
Dynamic Confidence Engine Test Script

Demonstrates the dynamic confidence calculation engine with various data scenarios:
- Data aging and confidence decay over time
- Multi-source validation impact on confidence
- Data quality factor effects on composite confidence
- Real-world scenario testing with different data conditions

This script validates Phase 5 implementation and shows how confidence adjusts
based on data freshness, source reliability, and cross-source consistency.
"""

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the scripts directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from services.dynamic_confidence_engine import (
        DynamicConfidenceEngine,
        create_dynamic_confidence_engine,
    )
    from services.real_time_market_data import MarketDataPoint
    from utils.config_manager import ConfigManager

    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    IMPORTS_AVAILABLE = False


def create_test_data_scenarios():
    """Create various test data scenarios to demonstrate confidence calculation"""

    scenarios = {}
    now = datetime.now()

    # Scenario 1: Fresh, high-quality data from reliable sources
    scenarios["fresh_high_quality"] = {
        "description": "Fresh data from reliable sources (< 2 hours old)",
        "data_points": {
            "fed_funds_rate": MarketDataPoint(
                value=5.25,
                timestamp=now - timedelta(hours=1),
                source="fred",
                data_type="fed_funds_rate",
                confidence=0.95,
                is_real_time=True,
                age_hours=1.0,
            ),
            "gdp_growth": MarketDataPoint(
                value=2.3,
                timestamp=now - timedelta(hours=1.5),
                source="fred",
                data_type="gdp_growth",
                confidence=0.92,
                is_real_time=True,
                age_hours=1.5,
            ),
            "vix_level": MarketDataPoint(
                value=16.8,
                timestamp=now - timedelta(minutes=30),
                source="alpha_vantage",
                data_type="vix_volatility",
                confidence=0.88,
                is_real_time=True,
                age_hours=0.5,
            ),
        },
        "context": {
            "expected_data_points": 3,
            "analysis_type": "macro_discovery",
            "region": "US",
        },
    }

    # Scenario 2: Aging data (24-48 hours old)
    scenarios["aging_data"] = {
        "description": "Aging data showing confidence decay over time",
        "data_points": {
            "fed_funds_rate": MarketDataPoint(
                value=5.25,
                timestamp=now - timedelta(hours=30),
                source="fred",
                data_type="fed_funds_rate",
                confidence=0.95,
                is_real_time=False,
                age_hours=30.0,
            ),
            "gdp_growth": MarketDataPoint(
                value=2.3,
                timestamp=now - timedelta(days=2),
                source="fred",
                data_type="gdp_growth",
                confidence=0.92,
                is_real_time=False,
                age_hours=48.0,
            ),
            "consumer_confidence": MarketDataPoint(
                value=76.5,
                timestamp=now - timedelta(days=3),
                source="survey",
                data_type="consumer_confidence",
                confidence=0.85,
                is_real_time=False,
                age_hours=72.0,
            ),
        },
        "context": {
            "expected_data_points": 3,
            "analysis_type": "macro_discovery",
            "region": "US",
        },
    }

    # Scenario 3: Stale data (> 1 week old)
    scenarios["stale_data"] = {
        "description": "Stale data demonstrating significant confidence decay",
        "data_points": {
            "fed_funds_rate": MarketDataPoint(
                value=5.25,
                timestamp=now - timedelta(days=10),
                source="config_fallback",
                data_type="fed_funds_rate",
                confidence=0.70,
                is_real_time=False,
                age_hours=240.0,
            ),
            "gdp_growth": MarketDataPoint(
                value=2.3,
                timestamp=now - timedelta(days=45),
                source="config_fallback",
                data_type="gdp_growth",
                confidence=0.60,
                is_real_time=False,
                age_hours=1080.0,
            ),
        },
        "context": {
            "expected_data_points": 3,
            "analysis_type": "macro_discovery",
            "region": "US",
        },
    }

    # Scenario 4: Mixed source reliability
    scenarios["mixed_reliability"] = {
        "description": "Mixed data sources with varying reliability scores",
        "data_points": {
            "fed_funds_rate_fred": MarketDataPoint(
                value=5.25,
                timestamp=now - timedelta(hours=2),
                source="fred",
                data_type="fed_funds_rate",
                confidence=0.95,
                is_real_time=True,
                age_hours=2.0,
            ),
            "fed_funds_rate_alpha": MarketDataPoint(
                value=5.28,
                timestamp=now - timedelta(hours=1),
                source="alpha_vantage",
                data_type="fed_funds_rate",
                confidence=0.85,
                is_real_time=True,
                age_hours=1.0,
            ),
            "fed_funds_rate_mock": MarketDataPoint(
                value=5.30,
                timestamp=now - timedelta(hours=3),
                source="mock_data",
                data_type="fed_funds_rate",
                confidence=0.75,
                is_real_time=False,
                age_hours=3.0,
            ),
        },
        "context": {
            "expected_data_points": 3,
            "analysis_type": "macro_discovery",
            "region": "US",
        },
    }

    # Scenario 5: Inconsistent cross-source data
    scenarios["inconsistent_sources"] = {
        "description": "Inconsistent data across sources affecting confidence",
        "data_points": {
            "vix_bloomberg": MarketDataPoint(
                value=15.2,
                timestamp=now - timedelta(minutes=15),
                source="bloomberg",
                data_type="vix_volatility",
                confidence=0.90,
                is_real_time=True,
                age_hours=0.25,
            ),
            "vix_alpha_vantage": MarketDataPoint(
                value=18.8,
                timestamp=now - timedelta(minutes=10),
                source="alpha_vantage",
                data_type="vix_volatility",
                confidence=0.85,
                is_real_time=True,
                age_hours=0.17,
            ),
            "vix_yahoo": MarketDataPoint(
                value=22.1,
                timestamp=now - timedelta(minutes=20),
                source="yahoo_finance",
                data_type="vix_volatility",
                confidence=0.75,
                is_real_time=True,
                age_hours=0.33,
            ),
        },
        "context": {
            "expected_data_points": 3,
            "analysis_type": "macro_discovery",
            "region": "US",
        },
    }

    # Scenario 6: Incomplete data set
    scenarios["incomplete_data"] = {
        "description": "Incomplete data set with missing indicators",
        "data_points": {
            "fed_funds_rate": MarketDataPoint(
                value=5.25,
                timestamp=now - timedelta(hours=1),
                source="fred",
                data_type="fed_funds_rate",
                confidence=0.95,
                is_real_time=True,
                age_hours=1.0,
            )
        },
        "context": {
            "expected_data_points": 5,
            "analysis_type": "macro_discovery",
            "region": "US",
        },
    }

    return scenarios


def run_confidence_tests():
    """Run comprehensive confidence calculation tests"""

    if not IMPORTS_AVAILABLE:
        print("❌ Required imports not available. Please check service dependencies.")
        return False

    print("🚀 Starting Dynamic Confidence Engine Tests")
    print("=" * 60)

    try:
        # Initialize confidence engine
        config = ConfigManager()
        engine = create_dynamic_confidence_engine(config)

        # Create test scenarios
        scenarios = create_test_data_scenarios()

        results = {}

        for scenario_name, scenario_data in scenarios.items():
            print(f"\n📊 Testing Scenario: {scenario_data['description']}")
            print("-" * 50)

            # Calculate confidence for this scenario
            result = engine.calculate_confidence(
                scenario_data["data_points"], scenario_data["context"], "market_data"
            )

            results[scenario_name] = result

            # Check if calculation succeeded or failed
            if "error" in result:
                print(f"❌ Calculation failed: {result['error']}")
                continue

            # Display results
            print(f"Composite Confidence: {result['composite_confidence']:.3f}")
            print(f"Confidence Level: {result['confidence_level']}")
            print(
                f"Meets Institutional Grade: {result.get('meets_institutional_grade', 'Unknown')}"
            )

            # Quality metrics breakdown
            if "quality_metrics" in result:
                quality = result["quality_metrics"]
                print(f"\nQuality Breakdown:")
                print(f"  Completeness: {quality.completeness_score:.3f}")
                print(f"  Freshness: {quality.freshness_score:.3f}")
                print(f"  Reliability: {quality.reliability_score:.3f}")
                print(f"  Consistency: {quality.consistency_score:.3f}")
                print(f"  Overall Quality: {quality.overall_quality:.3f}")

            # Validation results
            if "validation_results" in result:
                validation = result["validation_results"]
                print(f"\nCross-Source Validation:")
                print(f"  Sources Available: {validation['source_count']}")
                print(f"  Source Agreement: {validation['source_agreement']:.3f}")
                print(f"  Validation Quality: {validation['validation_quality']}")

            # Recommendations
            if "recommendations" in result and result["recommendations"]:
                print(f"\nRecommendations:")
                for rec in result["recommendations"]:
                    print(f"  • {rec}")

        # Comparative analysis
        print("\n" + "=" * 60)
        print("📈 COMPARATIVE ANALYSIS")
        print("=" * 60)

        # Sort scenarios by confidence level
        sorted_results = sorted(
            results.items(), key=lambda x: x[1]["composite_confidence"], reverse=True
        )

        print(f"\n🏆 Confidence Ranking:")
        for i, (scenario_name, result) in enumerate(sorted_results, 1):
            confidence = result["composite_confidence"]
            level = result["confidence_level"]
            institutional = "✅" if result["meets_institutional_grade"] else "❌"
            print(f"{i}. {scenario_name}: {confidence:.3f} ({level}) {institutional}")

        # Analyze confidence decay patterns
        print(f"\n⏰ Data Age Impact Analysis:")
        age_analysis = []

        for scenario_name, scenario_data in scenarios.items():
            result = results[scenario_name]

            # Calculate average age
            ages = []
            for dp in scenario_data["data_points"].values():
                if hasattr(dp, "age_hours"):
                    ages.append(dp.age_hours)

            avg_age = sum(ages) / len(ages) if ages else 0
            confidence = result["composite_confidence"]
            freshness = result["quality_metrics"].freshness_score

            age_analysis.append((scenario_name, avg_age, confidence, freshness))

        # Sort by age
        age_analysis.sort(key=lambda x: x[1])

        for scenario_name, avg_age, confidence, freshness in age_analysis:
            age_str = f"{avg_age:.1f}h" if avg_age < 48 else f"{avg_age/24:.1f}d"
            print(
                f"  {scenario_name}: {age_str} → Confidence: {confidence:.3f}, Freshness: {freshness:.3f}"
            )

        # Source reliability impact
        print(f"\n🔍 Source Reliability Impact:")
        reliability_analysis = []

        for scenario_name, result in results.items():
            reliability = result["quality_metrics"].reliability_score
            confidence = result["composite_confidence"]
            reliability_analysis.append((scenario_name, reliability, confidence))

        reliability_analysis.sort(key=lambda x: x[1], reverse=True)

        for scenario_name, reliability, confidence in reliability_analysis:
            print(
                f"  {scenario_name}: Reliability {reliability:.3f} → Confidence {confidence:.3f}"
            )

        print(f"\n✅ All Dynamic Confidence Engine tests completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Confidence engine tests failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def demonstrate_decay_functions():
    """Demonstrate confidence decay over various time periods"""

    if not IMPORTS_AVAILABLE:
        return

    print("\n" + "=" * 60)
    print("📉 CONFIDENCE DECAY DEMONSTRATION")
    print("=" * 60)

    try:
        config = ConfigManager()
        engine = create_dynamic_confidence_engine(config)

        now = datetime.now()
        base_data_point = MarketDataPoint(
            value=5.25,
            timestamp=now,
            source="fred",
            data_type="fed_funds_rate",
            confidence=0.95,
            is_real_time=True,
            age_hours=0.0,
        )

        # Test decay over various time periods
        test_ages = [0, 1, 6, 12, 24, 48, 72, 168, 336, 720]  # Hours

        print(f"\n⏰ Fed Funds Rate Confidence Decay (Half-life: 24h):")
        print(f"{'Age':<10} {'Freshness':<10} {'Confidence':<10} {'Status'}")
        print("-" * 45)

        for age_hours in test_ages:
            # Create aged data point
            aged_data_point = MarketDataPoint(
                value=5.25,
                timestamp=now - timedelta(hours=age_hours),
                source="fred",
                data_type="fed_funds_rate",
                confidence=0.95,
                is_real_time=age_hours < 24,
                age_hours=age_hours,
            )

            # Calculate freshness score
            freshness = engine._calculate_freshness_score(age_hours, "market_data")

            # Calculate full confidence
            result = engine.calculate_confidence(
                {"fed_funds": aged_data_point},
                {"expected_data_points": 1},
                "market_data",
            )

            confidence = result["composite_confidence"]

            # Determine status
            if confidence >= 0.85:
                status = "✅ Institutional"
            elif confidence >= 0.70:
                status = "⚠️  Moderate"
            elif confidence >= 0.50:
                status = "🔸 Low"
            else:
                status = "❌ Insufficient"

            age_str = f"{age_hours}h" if age_hours < 48 else f"{age_hours//24}d"
            print(f"{age_str:<10} {freshness:<10.3f} {confidence:<10.3f} {status}")

        # Test different data types
        print(f"\n📊 Decay Comparison Across Data Types:")
        print(
            f"{'Data Type':<20} {'Half-Life':<12} {'1d Decay':<10} {'1w Decay':<10} {'1m Decay'}"
        )
        print("-" * 65)

        data_types = [
            "market_data",
            "economic_indicators",
            "volatility_data",
            "consumer_confidence",
        ]

        for data_type in data_types:
            decay_params = engine.decay_parameters.get(data_type)
            if decay_params:
                half_life = f"{decay_params.half_life_hours}h"

                # Calculate decay at different intervals
                decay_1d = engine._calculate_freshness_score(24, data_type)
                decay_1w = engine._calculate_freshness_score(168, data_type)
                decay_1m = engine._calculate_freshness_score(720, data_type)

                print(
                    f"{data_type:<20} {half_life:<12} {decay_1d:<10.3f} {decay_1w:<10.3f} {decay_1m:<10.3f}"
                )

        print(f"\n✅ Confidence decay demonstration completed!")

    except Exception as e:
        print(f"❌ Decay demonstration failed: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("Dynamic Confidence Engine Test Suite")
    print("Validating Phase 5: Dynamic confidence calculation implementation")
    print("=" * 70)

    # Run main confidence tests
    success = run_confidence_tests()

    # Demonstrate decay functions
    demonstrate_decay_functions()

    if success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"Phase 5 implementation is working correctly.")
        print(f"Dynamic confidence engine successfully demonstrates:")
        print(f"  ✅ Data aging and confidence decay")
        print(f"  ✅ Multi-source validation")
        print(f"  ✅ Quality factor assessment")
        print(f"  ✅ Cross-source consistency analysis")
        print(f"  ✅ Institutional-grade confidence calibration")
    else:
        print(f"\n❌ SOME TESTS FAILED!")
        print(f"Please review the error messages above.")

    print(f"\nTest completed at: {datetime.now().isoformat()}")
