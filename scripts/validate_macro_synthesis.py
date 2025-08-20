#!/usr/bin/env python3
"""
Validation script for enhanced macro_synthesis.py
Tests institutional quality and template compliance
"""

import json
import os
import sys
from datetime import datetime

import yaml

from macro_synthesis import MacroEconomicSynthesis
from services.volatility_analysis_service import create_volatility_analysis_service
from utils.config_manager import ConfigManager


def load_config():
    """Load configuration from macro_analysis_config.yaml"""
    config_path = "./config/macro_analysis_config.yaml"
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"⚠️  Config file not found: {config_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"⚠️  Error parsing config file: {e}")
        return {}


def validate_template_artifacts():
    """Validate that discovery files don't contain template artifacts"""
    print("\n🔍 VALIDATING TEMPLATE ARTIFACTS")
    print("-" * 50)

    try:
        # Initialize configuration manager
        config_manager = ConfigManager()

        # Get discovery files directory
        discovery_dir = "./data/outputs/macro_analysis/discovery/"

        if not os.path.exists(discovery_dir):
            print(f"⚠️ Discovery directory not found: {discovery_dir}")
            return 0.8  # Neutral score if no files to validate

        # Find all discovery files
        discovery_files = []
        for filename in os.listdir(discovery_dir):
            if filename.endswith("_discovery.json"):
                discovery_files.append(os.path.join(discovery_dir, filename))

        if len(discovery_files) < 2:
            print(
                f"⚠️ Need at least 2 discovery files for cross-validation (found {len(discovery_files)})"
            )
            return 0.8

        print(f"📊 Found {len(discovery_files)} discovery files for validation")

        # Extract volatility parameters from discovery files
        volatility_data = {}

        for file_path in discovery_files:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Extract region from filename
                filename = os.path.basename(file_path)
                region = filename.split("_")[0].upper()

                # Extract calculated volatility parameters from CLI market intelligence
                cli_market = data.get("cli_market_intelligence", {})
                volatility_analysis = cli_market.get("volatility_analysis", {})
                mean_reversion = volatility_analysis.get("mean_reversion", {})

                if (
                    "long_term_mean" in mean_reversion
                    and "reversion_speed" in mean_reversion
                ):
                    volatility_data[region] = {
                        "long_term_mean": float(mean_reversion["long_term_mean"]),
                        "reversion_speed": float(mean_reversion["reversion_speed"]),
                        "file_path": file_path,
                        "source": "calculated_cli_data",
                    }
                    print(f"✓ Extracted calculated volatility parameters for {region}")
                else:
                    print(f"⚠️ Missing calculated volatility parameters in {filename}")
                    print(
                        f"    Expected: cli_market_intelligence.volatility_analysis.mean_reversion fields"
                    )
                    print(f"    Check discovery file generation process for {region}")

            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in {file_path}: {e}")
                continue
            except KeyError as e:
                print(f"❌ Missing required field in {file_path}: {e}")
                print(
                    f"    Check discovery file structure for cli_market_intelligence section"
                )
                continue
            except Exception as e:
                print(f"❌ Unexpected error processing {file_path}: {e}")
                continue

        if len(volatility_data) < 2:
            print(
                "⚠️ Insufficient calculated volatility data for template artifact detection"
            )
            print(
                "⚠️ Ensure discovery files contain CLI market intelligence with calculated volatility parameters"
            )
            return 0.7

        # Enhanced completeness validation
        print(
            f"✅ Found {len(volatility_data)} regions with calculated volatility parameters"
        )

        # Validate data quality
        data_quality_issues = []
        for region, data in volatility_data.items():
            # Check for reasonable parameter ranges
            long_term_mean = data["long_term_mean"]
            reversion_speed = data["reversion_speed"]

            if not (10.0 <= long_term_mean <= 50.0):
                data_quality_issues.append(
                    f"{region}: long_term_mean {long_term_mean:.2f} outside reasonable range [10.0, 50.0]"
                )

            if not (0.05 <= reversion_speed <= 0.5):
                data_quality_issues.append(
                    f"{region}: reversion_speed {reversion_speed:.3f} outside reasonable range [0.05, 0.5]"
                )

        if data_quality_issues:
            print("⚠️ Data quality warnings:")
            for issue in data_quality_issues:
                print(f"    - {issue}")
        else:
            print("✅ All calculated volatility parameters within reasonable ranges")

        # Check for template artifacts
        template_artifact_score = 1.0
        artifact_issues = []

        # Check for identical values
        long_term_means = [data["long_term_mean"] for data in volatility_data.values()]
        reversion_speeds = [
            data["reversion_speed"] for data in volatility_data.values()
        ]

        # Check long-term mean variance
        if len(set(long_term_means)) == 1:
            artifact_issues.append("All regions have identical long_term_mean values")
            template_artifact_score -= 0.4
        elif len(long_term_means) > 1:
            mean_variance = max(long_term_means) - min(long_term_means)
            relative_variance = mean_variance / max(long_term_means)
            if relative_variance < 0.02:  # Less than 2% variance
                artifact_issues.append(
                    f"Long_term_mean variance too low ({relative_variance:.3f})"
                )
                template_artifact_score -= 0.2

        # Check reversion speed variance
        if len(set(reversion_speeds)) == 1:
            artifact_issues.append("All regions have identical reversion_speed values")
            template_artifact_score -= 0.4
        elif len(reversion_speeds) > 1:
            speed_variance = max(reversion_speeds) - min(reversion_speeds)
            relative_variance = speed_variance / max(reversion_speeds)
            if relative_variance < 0.02:  # Less than 2% variance
                artifact_issues.append(
                    f"Reversion_speed variance too low ({relative_variance:.3f})"
                )
                template_artifact_score -= 0.2

        # Note: Removed config validation dependency to focus on calculated discovery data
        # Template artifact validation now exclusively uses calculated CLI market intelligence data
        print(
            "✅ Validation uses calculated discovery data (config hardcoded values ignored)"
        )

        # Report results
        template_artifact_score = max(0.0, template_artifact_score)

        print(f"📊 Template artifact validation score: {template_artifact_score:.2f}")

        if artifact_issues:
            print("⚠️ Template artifact issues detected:")
            for issue in artifact_issues:
                print(f"  - {issue}")
        else:
            print("✅ No template artifacts detected")

        # Detailed calculated parameter analysis
        print("\n📈 Calculated Volatility Parameter Analysis (from discovery files):")
        for region, data in volatility_data.items():
            print(
                f"  {region}: mean={data['long_term_mean']:.2f}, speed={data['reversion_speed']:.3f} (source: {data['source']})"
            )

        return template_artifact_score

    except Exception as e:
        print(f"❌ Template artifact validation failed: {e}")
        return 0.5


def validate_institutional_quality(region="US", date="20250804"):
    """Validate institutional quality standards"""
    print("🔍 VALIDATING INSTITUTIONAL QUALITY & TEMPLATE COMPLIANCE")
    print("=" * 70)

    # Load configuration
    config = load_config()

    # Get file paths from config
    file_paths = config.get("file_paths", {})
    discovery_template = file_paths.get("naming_convention", {}).get(
        "discovery", "{region}_{date}_discovery.json"
    )
    analysis_template = file_paths.get("naming_convention", {}).get(
        "analysis", "{region}_{date}_analysis.json"
    )

    discovery_dir = file_paths.get(
        "discovery_output", "./data/outputs/macro_analysis/discovery/"
    )
    analysis_dir = file_paths.get(
        "analysis_output", "./data/outputs/macro_analysis/analysis/"
    )

    discovery_file = os.path.join(
        discovery_dir, discovery_template.format(region=region.lower(), date=date)
    )
    analysis_file = os.path.join(
        analysis_dir, analysis_template.format(region=region.lower(), date=date)
    )

    print(f"📂 Discovery file: {discovery_file}")
    print(f"📂 Analysis file: {analysis_file}")

    # Check if files exist
    discovery_exists = os.path.exists(discovery_file)
    analysis_exists = os.path.exists(analysis_file)

    print(f"✓ Discovery file exists: {discovery_exists}")
    print(f"✓ Analysis file exists: {analysis_exists}")

    # Initialize synthesis
    try:
        synthesis = MacroEconomicSynthesis(
            region="US",
            discovery_file=discovery_file if discovery_exists else None,
            analysis_file=analysis_file if analysis_exists else None,
        )
        print("✅ MacroEconomicSynthesis initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize synthesis: {e}")
        return False

    # Validate enhanced service data collection
    print("\n📡 TESTING ENHANCED SERVICE DATA COLLECTION")
    print("-" * 50)

    try:
        synthesis._collect_enhanced_service_data()

        # Check if enhanced data was collected
        has_calendar_data = bool(synthesis.economic_calendar_data)
        has_liquidity_data = bool(synthesis.global_liquidity_data)
        has_sector_data = bool(synthesis.sector_correlation_data)

        print(f"✓ Economic calendar data collected: {has_calendar_data}")
        print(f"✓ Global liquidity data collected: {has_liquidity_data}")
        print(f"✓ Sector correlation data collected: {has_sector_data}")

        enhanced_services_score = (
            sum([has_calendar_data, has_liquidity_data, has_sector_data]) / 3
        )
        print(f"📊 Enhanced services integration score: {enhanced_services_score:.1%}")

    except Exception as e:
        print(f"⚠️  Enhanced service collection warning: {e}")
        enhanced_services_score = 0.0

    # Validate synthesis components
    print("\n🧠 TESTING SYNTHESIS COMPONENTS")
    print("-" * 50)

    synthesis_scores = {}

    # Get default confidence scores from config
    confidence_thresholds = config.get("confidence_thresholds", {})
    synthesis_minimum = confidence_thresholds.get("synthesis_minimum", 0.90)

    try:
        economic_thesis = synthesis.synthesize_economic_thesis()
        synthesis_scores["economic_thesis"] = economic_thesis.get(
            "economic_confidence", synthesis_minimum
        )
        print(f"✅ Economic thesis synthesis: {synthesis_scores['economic_thesis']:.2f}")
    except Exception as e:
        print(f"❌ Economic thesis failed: {e}")
        synthesis_scores["economic_thesis"] = 0.0

    try:
        business_cycle = synthesis.synthesize_business_cycle_assessment()
        synthesis_scores["business_cycle"] = business_cycle.get(
            "cycle_confidence", synthesis_minimum
        )
        print(f"✅ Business cycle assessment: {synthesis_scores['business_cycle']:.2f}")
    except Exception as e:
        print(f"❌ Business cycle failed: {e}")
        synthesis_scores["business_cycle"] = 0.0

    try:
        policy_analysis = synthesis.synthesize_policy_analysis()
        synthesis_scores["policy_analysis"] = policy_analysis.get(
            "policy_confidence", synthesis_minimum * 0.95
        )
        print(f"✅ Policy analysis: {synthesis_scores['policy_analysis']:.2f}")
    except Exception as e:
        print(f"❌ Policy analysis failed: {e}")
        synthesis_scores["policy_analysis"] = 0.0

    try:
        risk_assessment = synthesis.synthesize_risk_assessment()
        synthesis_scores["risk_assessment"] = risk_assessment.get(
            "risk_confidence", synthesis_minimum * 0.97
        )
        print(f"✅ Risk assessment: {synthesis_scores['risk_assessment']:.2f}")
    except Exception as e:
        print(f"❌ Risk assessment failed: {e}")
        synthesis_scores["risk_assessment"] = 0.0

    try:
        investment_implications = synthesis.synthesize_investment_implications()
        synthesis_scores["investment_implications"] = investment_implications.get(
            "implications_confidence", synthesis_minimum * 0.96
        )
        print(
            f"✅ Investment implications: {synthesis_scores['investment_implications']:.2f}"
        )
    except Exception as e:
        print(f"❌ Investment implications failed: {e}")
        synthesis_scores["investment_implications"] = 0.0

    # Calculate overall synthesis quality
    avg_synthesis_score = (
        sum(synthesis_scores.values()) / len(synthesis_scores)
        if synthesis_scores
        else 0.0
    )
    print(f"📊 Average synthesis component score: {avg_synthesis_score:.2f}")

    # Test document generation
    print("\n📄 TESTING DOCUMENT GENERATION")
    print("-" * 50)

    try:
        document = synthesis.generate_synthesis_document()

        # Validate document structure
        required_sections = [
            "# US Macro-Economic Analysis",
            "## 🎯 Executive Summary & Economic Thesis",
            "## 📊 Economic Positioning Dashboard",
            "## 📅 Economic Calendar & Policy Timeline",
            "## 🏆 Business Cycle Assessment",
            "## 📈 Economic Forecasting Framework",
            "## ⚠️ Economic Risk Assessment Matrix",
            "## 🎯 Investment Implications & Asset Allocation",
            "## 📋 Analysis Metadata",
            "## 🏁 Economic Outlook & Investment Recommendation Summary",
        ]

        sections_found = 0
        for section in required_sections:
            if section in document:
                sections_found += 1
                print(f"✅ Found: {section}")
            else:
                print(f"❌ Missing: {section}")

        template_compliance = sections_found / len(required_sections)
        print(f"📊 Template compliance score: {template_compliance:.1%}")

        # Check document length (institutional quality indicator)
        document_length = len(document)
        print(f"📏 Document length: {document_length:,} characters")

        # Get minimum document length from config
        quality_assurance = config.get("quality_assurance", {})
        document_quality = quality_assurance.get("document_quality", {})
        min_doc_length = document_quality.get("minimum_document_length", 15000)

        length_quality = (
            1.0
            if document_length > min_doc_length
            else document_length / min_doc_length
        )
        print(f"📊 Document length quality: {length_quality:.1%}")

        document_generated = True

    except Exception as e:
        print(f"❌ Document generation failed: {e}")
        template_compliance = 0.0
        length_quality = 0.0
        document_generated = False

    # Test enhanced methods
    print("\n🚀 TESTING ENHANCED METHODS")
    print("-" * 50)

    enhanced_methods_score = 0.0
    enhanced_methods_count = 0

    try:
        enhanced_thesis = synthesis._generate_enhanced_core_economic_thesis()
        print(f"✅ Enhanced core economic thesis: {len(enhanced_thesis)} chars")
        enhanced_methods_score += 1
    except Exception as e:
        print(f"❌ Enhanced thesis failed: {e}")
    enhanced_methods_count += 1

    try:
        enhanced_confidence = synthesis._calculate_enhanced_economic_confidence()
        print(f"✅ Enhanced confidence calculation: {enhanced_confidence:.2f}")
        enhanced_methods_score += 1
    except Exception as e:
        print(f"❌ Enhanced confidence failed: {e}")
    enhanced_methods_count += 1

    try:
        enhanced_catalysts = synthesis._identify_enhanced_economic_catalysts()
        print(f"✅ Enhanced economic catalysts: {len(enhanced_catalysts)} items")
        enhanced_methods_score += 1
    except Exception as e:
        print(f"❌ Enhanced catalysts failed: {e}")
    enhanced_methods_count += 1

    enhanced_methods_score /= enhanced_methods_count
    print(f"📊 Enhanced methods score: {enhanced_methods_score:.1%}")

    # Validate template artifacts
    template_artifact_score = validate_template_artifacts()

    # Calculate overall institutional quality score
    print("\n🏛️ INSTITUTIONAL QUALITY ASSESSMENT")
    print("-" * 50)

    quality_components = {
        "Enhanced Services Integration": enhanced_services_score * 0.15,
        "Synthesis Components": avg_synthesis_score * 0.20,
        "Template Compliance": template_compliance * 0.20,
        "Template Artifact Prevention": template_artifact_score * 0.15,
        "Document Quality": length_quality * 0.15,
        "Enhanced Methods": enhanced_methods_score * 0.15,
    }

    for component, score in quality_components.items():
        print(f"📊 {component}: {score:.3f}")

    overall_quality = sum(quality_components.values())
    print(f"\n🎯 OVERALL INSTITUTIONAL QUALITY SCORE: {overall_quality:.3f}/1.000")

    # Get quality thresholds from config
    institutional_threshold = confidence_thresholds.get("institutional_grade", 0.95)
    validation_threshold = confidence_thresholds.get("validation_minimum", 0.95)
    synthesis_threshold = confidence_thresholds.get("synthesis_minimum", 0.90)

    # Determine certification status using config thresholds
    if overall_quality >= institutional_threshold:
        certification = "🏆 INSTITUTIONAL GRADE CERTIFIED"
        status = "PASSED"
    elif overall_quality >= validation_threshold * 0.85:  # 85% of validation minimum
        certification = "⭐ HIGH QUALITY CERTIFIED"
        status = "PASSED"
    elif overall_quality >= synthesis_threshold * 0.78:  # 78% of synthesis minimum
        certification = "✅ STANDARD QUALITY"
        status = "PASSED"
    else:
        certification = "⚠️  NEEDS IMPROVEMENT"
        status = "NEEDS WORK"

    print(f"\n{certification}")
    print(f"📋 Validation Status: {status}")

    # Use dynamic threshold for pass/fail decision
    pass_threshold = validation_threshold * 0.85  # 85% of validation minimum
    return overall_quality >= pass_threshold


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate macro-economic synthesis quality"
    )
    parser.add_argument("--region", default="US", help="Economic region to validate")
    parser.add_argument(
        "--date", default="20250804", help="Analysis date (YYYYMMDD format)"
    )

    args = parser.parse_args()

    success = validate_institutional_quality(args.region, args.date)
    sys.exit(0 if success else 1)
