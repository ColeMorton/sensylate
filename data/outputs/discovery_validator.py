#!/usr/bin/env python3
"""
Discovery Phase Validation Specialist
DASV Phase 4: Comprehensive Quality Assurance for Discovery Output
"""

import json
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
import math

class DiscoveryValidator:
    def __init__(self, discovery_file_path):
        self.discovery_file_path = discovery_file_path
        self.validation_results = {
            "validation_metadata": {
                "validation_timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "validator_version": "1.0",
                "validation_scope": "discovery_phase_only",
                "confidence_threshold": 0.70
            },
            "statistical_validation": {},
            "data_integrity_validation": {},
            "business_logic_validation": {},
            "confidence_scoring": {},
            "overall_assessment": {}
        }

    def load_discovery_data(self):
        """Load and parse discovery phase output"""
        try:
            with open(self.discovery_file_path, 'r') as f:
                self.discovery_data = json.load(f)
            return True
        except Exception as e:
            self.validation_results["overall_assessment"]["file_load_error"] = str(e)
            return False

    def validate_statistical_accuracy(self):
        """Phase 4A: Statistical Validation and Significance Testing"""
        results = {}

        # Sample size adequacy check
        trade_data = self.discovery_data.get("authoritative_trade_data", {})
        total_trades = trade_data.get("total_trades", 0)
        open_positions = trade_data.get("open_positions", 0)
        closed_positions = trade_data.get("closed_positions", 0)

        # Basic trade count validation
        results["sample_adequacy"] = {
            "total_trades": total_trades,
            "minimum_threshold": 10,
            "adequate_sample": total_trades >= 10,
            "closed_positions": closed_positions,
            "open_positions": open_positions,
            "trade_sum_accuracy": (open_positions + closed_positions) == total_trades
        }

        # Date range validation
        date_range = trade_data.get("date_range", {})
        results["temporal_validation"] = {
            "earliest_entry": date_range.get("earliest_entry"),
            "latest_entry": date_range.get("latest_entry"),
            "latest_exit": date_range.get("latest_exit"),
            "date_format_valid": self._validate_date_format(date_range)
        }

        # Strategy distribution validation
        strategy_dist = trade_data.get("strategy_distribution", {})
        sma_count = strategy_dist.get("SMA", 0)
        ema_count = strategy_dist.get("EMA", 0)
        results["strategy_distribution_validation"] = {
            "SMA_count": sma_count,
            "EMA_count": ema_count,
            "total_matches_trades": (sma_count + ema_count) == total_trades,
            "distribution_logical": sma_count > 0 and ema_count >= 0
        }

        self.validation_results["statistical_validation"] = results
        return results

    def validate_data_integrity(self):
        """Phase 4B: Data Integrity and Completeness Verification"""
        results = {}

        # Required sections validation
        required_sections = [
            "portfolio", "discovery_metadata", "authoritative_trade_data",
            "market_context", "fundamental_integration", "research_enhancement",
            "data_quality_assessment", "next_phase_inputs"
        ]

        results["structural_completeness"] = {
            section: section in self.discovery_data
            for section in required_sections
        }
        results["all_sections_present"] = all(results["structural_completeness"].values())

        # Market context validation
        market_context = self.discovery_data.get("market_context", {})
        benchmark_data = market_context.get("benchmark_data", {})

        results["market_data_validation"] = {
            "SPY_present": "SPY" in benchmark_data,
            "QQQ_present": "QQQ" in benchmark_data,
            "VTI_present": "VTI" in benchmark_data,
            "volatility_data": "volatility_environment" in market_context,
            "economic_context": "economic_context" in market_context
        }

        # Fundamental integration validation
        fundamental_data = self.discovery_data.get("fundamental_integration", {})
        coverage = fundamental_data.get("analysis_coverage", {})

        results["fundamental_validation"] = {
            "coverage_percentage": coverage.get("coverage_percentage", 0),
            "adequate_coverage": coverage.get("coverage_percentage", 0) > 20,
            "analysis_files_present": len(fundamental_data.get("analysis_files", {})) > 0,
            "recommendation_distribution": fundamental_data.get("integration_quality", {}).get("recommendation_distribution", {})
        }

        # Ticker universe validation
        ticker_data = self.discovery_data.get("authoritative_trade_data", {}).get("ticker_universe", {})
        results["ticker_validation"] = {
            "total_tickers": ticker_data.get("total_tickers", 0),
            "unique_tickers_count": len(ticker_data.get("unique_tickers", [])),
            "ticker_count_consistent": ticker_data.get("total_tickers", 0) == len(ticker_data.get("unique_tickers", [])),
            "sector_distribution": ticker_data.get("sector_distribution", {})
        }

        self.validation_results["data_integrity_validation"] = results
        return results

    def validate_business_logic(self):
        """Phase 4C: Business Logic Validation and Coherence Checking"""
        results = {}

        # Position sizing methodology validation
        position_data = self.discovery_data.get("authoritative_trade_data", {}).get("position_sizing_methodology", {})
        results["position_sizing_validation"] = {
            "type": position_data.get("type"),
            "value": position_data.get("value"),
            "confidence": position_data.get("confidence"),
            "fixed_sizing_logical": position_data.get("type") == "fixed" and position_data.get("value") == 1.0
        }

        # Market regime validation
        volatility_env = self.discovery_data.get("market_context", {}).get("volatility_environment", {})
        vix_current = volatility_env.get("VIX_current", 0)
        market_regime = volatility_env.get("market_regime", "")

        results["market_regime_validation"] = {
            "VIX_current": vix_current,
            "market_regime": market_regime,
            "regime_logical": self._validate_vix_regime_consistency(vix_current, market_regime),
            "confidence": volatility_env.get("confidence", 0)
        }

        # Fundamental analysis coherence
        fundamental_files = self.discovery_data.get("fundamental_integration", {}).get("analysis_files", {})
        recommendation_dist = self.discovery_data.get("fundamental_integration", {}).get("integration_quality", {}).get("recommendation_distribution", {})

        results["fundamental_coherence"] = {
            "files_vs_recommendations": len(fundamental_files) == sum(recommendation_dist.values()) if recommendation_dist else False,
            "no_sell_recommendations": recommendation_dist.get("SELL", 0) == 0,
            "buy_recommendations": recommendation_dist.get("BUY", 0),
            "hold_recommendations": recommendation_dist.get("HOLD", 0)
        }

        # Next phase readiness validation
        next_phase = self.discovery_data.get("next_phase_inputs", {})
        results["readiness_validation"] = {
            "analysis_ready": next_phase.get("analysis_ready", False),
            "confidence_met": next_phase.get("required_confidence_met", False),
            "threshold": next_phase.get("confidence_threshold", 0),
            "actual_confidence": next_phase.get("actual_confidence", 0),
            "threshold_exceeded": next_phase.get("actual_confidence", 0) >= next_phase.get("confidence_threshold", 0.7)
        }

        self.validation_results["business_logic_validation"] = results
        return results

    def calculate_confidence_scores(self):
        """Phase 4D: Comprehensive Confidence Scoring"""
        results = {}

        # Discovery phase confidence components
        discovery_meta = self.discovery_data.get("discovery_metadata", {})
        data_quality = self.discovery_data.get("data_quality_assessment", {})

        # Component confidence calculation
        components = {
            "data_completeness": {
                "weight": 0.30,
                "score": data_quality.get("completeness_score", 0),
                "source": "CSV completeness and data availability"
            },
            "fundamental_integration": {
                "weight": 0.20,
                "score": self.discovery_data.get("fundamental_integration", {}).get("analysis_coverage", {}).get("confidence", 0) / 100 * self.discovery_data.get("fundamental_integration", {}).get("analysis_coverage", {}).get("coverage_percentage", 0) / 100,
                "source": "Fundamental analysis coverage and quality"
            },
            "market_context_quality": {
                "weight": 0.25,
                "score": data_quality.get("source_reliability", 0),
                "source": "Benchmark and economic data quality"
            },
            "portfolio_metadata": {
                "weight": 0.25,
                "score": 1.0 if self.discovery_data.get("authoritative_trade_data", {}).get("total_trades", 0) >= 10 else 0.7,
                "source": "Trade count adequacy and timeframe coverage"
            }
        }

        # Calculate weighted confidence score
        weighted_sum = sum(comp["weight"] * comp["score"] for comp in components.values())

        results["component_confidence"] = components
        results["calculated_confidence"] = weighted_sum
        results["reported_confidence"] = discovery_meta.get("confidence_score", 0)
        results["confidence_variance"] = abs(weighted_sum - discovery_meta.get("confidence_score", 0))
        results["confidence_calibrated"] = results["confidence_variance"] < 0.05

        # Quality band classification
        if weighted_sum >= 0.90:
            quality_band = "institutional_grade"
        elif weighted_sum >= 0.80:
            quality_band = "operational_grade"
        elif weighted_sum >= 0.70:
            quality_band = "standard_grade"
        elif weighted_sum >= 0.60:
            quality_band = "developmental_grade"
        else:
            quality_band = "inadequate"

        results["quality_band"] = quality_band
        results["threshold_compliance"] = weighted_sum >= 0.70

        self.validation_results["confidence_scoring"] = results
        return results

    def generate_overall_assessment(self):
        """Generate comprehensive validation assessment"""
        # Collect all validation results
        statistical_pass = self.validation_results["statistical_validation"].get("sample_adequacy", {}).get("adequate_sample", False)
        integrity_pass = self.validation_results["data_integrity_validation"].get("all_sections_present", False)
        logic_pass = self.validation_results["business_logic_validation"].get("readiness_validation", {}).get("analysis_ready", False)
        confidence_pass = self.validation_results["confidence_scoring"].get("threshold_compliance", False)

        # Calculate validation scores
        validation_scores = {
            "statistical_validation": 1.0 if statistical_pass else 0.6,
            "data_integrity": 1.0 if integrity_pass else 0.4,
            "business_logic": 1.0 if logic_pass else 0.5,
            "confidence_calibration": 1.0 if confidence_pass else 0.3
        }

        overall_score = sum(validation_scores.values()) / len(validation_scores)

        # Identify issues
        issues_found = []
        if not statistical_pass:
            issues_found.append("Insufficient sample size for robust analysis")
        if not integrity_pass:
            issues_found.append("Missing required data sections")
        if not logic_pass:
            issues_found.append("Business logic inconsistencies detected")
        if not confidence_pass:
            issues_found.append("Confidence score below minimum threshold")

        # Generate recommendations
        recommendations = []
        if self.discovery_data.get("fundamental_integration", {}).get("analysis_coverage", {}).get("coverage_percentage", 0) < 50:
            recommendations.append("Expand fundamental analysis coverage to >50% for enhanced insights")
        if self.discovery_data.get("data_quality_assessment", {}).get("quality_issues", []):
            recommendations.append("Address identified data quality issues")
        if overall_score < 0.80:
            recommendations.append("Improve data collection and validation processes")

        assessment = {
            "validation_passed": overall_score >= 0.70,
            "overall_validation_score": overall_score,
            "component_scores": validation_scores,
            "issues_identified": issues_found,
            "improvement_recommendations": recommendations,
            "discovery_phase_certified": overall_score >= 0.70 and len(issues_found) == 0,
            "next_phase_approved": self.validation_results["business_logic_validation"].get("readiness_validation", {}).get("analysis_ready", False)
        }

        self.validation_results["overall_assessment"] = assessment
        return assessment

    def _validate_date_format(self, date_range):
        """Validate date format consistency"""
        try:
            for date_key, date_val in date_range.items():
                if date_val:
                    datetime.strptime(date_val, '%Y-%m-%d')
            return True
        except:
            return False

    def _validate_vix_regime_consistency(self, vix_current, market_regime):
        """Validate VIX level consistency with market regime classification"""
        if vix_current < 20 and market_regime == "low_volatility":
            return True
        elif 20 <= vix_current < 30 and market_regime == "moderate_volatility":
            return True
        elif vix_current >= 30 and market_regime == "high_volatility":
            return True
        else:
            return False

    def save_validation_report(self, output_path):
        """Save comprehensive validation report"""
        with open(output_path, 'w') as f:
            json.dump(self.validation_results, f, indent=2)

def main():
    # Initialize validator
    discovery_file = "/Users/colemorton/Projects/sensylate/team-workspace/microservices/trade_history/discover/outputs/live_signals_20250703.json"
    validator = DiscoveryValidator(discovery_file)

    # Load discovery data
    if not validator.load_discovery_data():
        print("Failed to load discovery data")
        return

    print("🔍 DASV Phase 4: Discovery Validation Specialist")
    print("=" * 50)

    # Execute validation phases
    print("Phase 4A: Statistical Validation...")
    validator.validate_statistical_accuracy()

    print("Phase 4B: Data Integrity Validation...")
    validator.validate_data_integrity()

    print("Phase 4C: Business Logic Validation...")
    validator.validate_business_logic()

    print("Phase 4D: Confidence Scoring...")
    validator.calculate_confidence_scores()

    print("Generating Overall Assessment...")
    assessment = validator.generate_overall_assessment()

    # Save validation report
    output_file = f"live_signals_ANALYSIS_VALIDATION_{datetime.now().strftime('%Y%m%d')}.json"
    output_path = Path("analysis_trade_history/validation") / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    validator.save_validation_report(output_path)

    # Print summary
    print("\n" + "=" * 50)
    print("🎯 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Overall Validation Score: {assessment['overall_validation_score']:.2f}")
    print(f"Validation Passed: {'✅ YES' if assessment['validation_passed'] else '❌ NO'}")
    print(f"Discovery Phase Certified: {'✅ YES' if assessment['discovery_phase_certified'] else '❌ NO'}")
    print(f"Next Phase Approved: {'✅ YES' if assessment['next_phase_approved'] else '❌ NO'}")

    if assessment['issues_identified']:
        print(f"\n⚠️  Issues Identified ({len(assessment['issues_identified'])}):")
        for issue in assessment['issues_identified']:
            print(f"   • {issue}")

    if assessment['improvement_recommendations']:
        print(f"\n💡 Recommendations ({len(assessment['improvement_recommendations'])}):")
        for rec in assessment['improvement_recommendations']:
            print(f"   • {rec}")

    print(f"\n📊 Component Scores:")
    for component, score in assessment['component_scores'].items():
        status = "✅" if score >= 0.80 else "⚠️" if score >= 0.60 else "❌"
        print(f"   {status} {component}: {score:.2f}")

    print(f"\n📁 Validation report saved: {output_path}")

    return assessment

if __name__ == "__main__":
    main()
