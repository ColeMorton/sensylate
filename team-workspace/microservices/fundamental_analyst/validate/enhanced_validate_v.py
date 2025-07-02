#!/usr/bin/env python3
"""
Enhanced Phase 4: Validate - Real-time Market Data Validation for Visa Inc (V)
DASV Framework - Enhanced with Yahoo Finance Real-time Validation
"""

import json
import os
import subprocess
from datetime import datetime

def get_yahoo_finance_data(ticker: str) -> dict:
    """Get real-time Yahoo Finance data for validation"""
    try:
        result = subprocess.run([
            'python', 'scripts/yahoo_finance_service.py', 'info', ticker
        ], capture_output=True, text=True, cwd='/Users/colemorton/Projects/sensylate')

        if result.returncode == 0:
            # Parse JSON output from stdout, handling multi-line JSON
            output = result.stdout.strip()

            # Try to parse the entire output as JSON first
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                # If that fails, look for JSON block in the output
                lines = output.split('\n')
                json_lines = []
                in_json = False

                for line in lines:
                    if line.strip().startswith('{'):
                        in_json = True
                        json_lines = [line]
                    elif in_json:
                        json_lines.append(line)
                        if line.strip().endswith('}'):
                            try:
                                return json.loads('\n'.join(json_lines))
                            except json.JSONDecodeError:
                                continue

                # If still no valid JSON found
                print(f"Debug - Could not parse JSON from output")
                return {}
        else:
            print(f"Error fetching Yahoo Finance data: {result.stderr}")
            return {}
    except Exception as e:
        print(f"Exception in Yahoo Finance API call: {e}")
        return {}

def create_enhanced_validation_report():
    """Create enhanced validation report with real-time data validation"""

    # Load existing validation report
    validation_path = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/validation/V_20250702_validation.json"
    with open(validation_path, 'r') as f:
        validation_report = json.load(f)

    # Load discovery data for comparison
    discovery_path = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/discovery/V_20250702_discovery.json"
    with open(discovery_path, 'r') as f:
        discovery_data = json.load(f)

    # Get real-time Yahoo Finance data
    print("📊 Fetching real-time Yahoo Finance data for enhanced validation...")
    yahoo_data = get_yahoo_finance_data("V")

    if not yahoo_data:
        print("⚠️ Unable to fetch real-time data, using existing validation")
        return validation_report

    # Enhanced validation with real-time data
    enhanced_validations = []

    # Price validation
    reported_price = discovery_data['market_data']['current_price_data']['price']
    yahoo_price = yahoo_data['current_price']
    price_variance = abs(reported_price - yahoo_price) / yahoo_price * 100

    enhanced_validations.append({
        "metric": "Current Price",
        "reported": reported_price,
        "yahoo_finance": yahoo_price,
        "variance_percentage": price_variance,
        "validation_grade": "A+" if price_variance <= 0.5 else "A" if price_variance <= 2.0 else "B",
        "confidence": "9.8/10.0" if price_variance <= 0.5 else "9.5/10.0" if price_variance <= 2.0 else "8.5/10.0"
    })

    # Market Cap validation
    reported_mcap = discovery_data['market_data']['current_price_data']['market_cap']
    yahoo_mcap = yahoo_data['market_cap']
    mcap_variance = abs(reported_mcap - yahoo_mcap) / yahoo_mcap * 100

    enhanced_validations.append({
        "metric": "Market Cap",
        "reported": reported_mcap,
        "yahoo_finance": yahoo_mcap,
        "variance_percentage": mcap_variance,
        "validation_grade": "A+" if mcap_variance <= 0.5 else "A" if mcap_variance <= 2.0 else "B",
        "confidence": "9.8/10.0" if mcap_variance <= 0.5 else "9.5/10.0" if mcap_variance <= 2.0 else "8.5/10.0"
    })

    # P/E Ratio validation
    reported_pe = discovery_data['market_data']['current_price_data']['pe_ratio']
    yahoo_pe = yahoo_data['pe_ratio']
    pe_variance = abs(reported_pe - yahoo_pe) / yahoo_pe * 100

    enhanced_validations.append({
        "metric": "P/E Ratio",
        "reported": reported_pe,
        "yahoo_finance": yahoo_pe,
        "variance_percentage": pe_variance,
        "validation_grade": "A+" if pe_variance <= 1.0 else "A" if pe_variance <= 2.0 else "B",
        "confidence": "9.8/10.0" if pe_variance <= 1.0 else "9.5/10.0" if pe_variance <= 2.0 else "8.5/10.0"
    })

    # Update validation report with enhanced real-time validation
    validation_report["real_time_validation_results"] = {
        "yahoo_finance_verification": {
            "price_validation": {
                "reported_price": reported_price,
                "yahoo_finance_price": yahoo_price,
                "variance_percentage": round(price_variance, 2),
                "validation_grade": enhanced_validations[0]["validation_grade"],
                "confidence": enhanced_validations[0]["confidence"]
            },
            "market_cap_validation": {
                "reported_market_cap": reported_mcap,
                "yahoo_finance_market_cap": yahoo_mcap,
                "variance_percentage": round(mcap_variance, 2),
                "validation_grade": enhanced_validations[1]["validation_grade"],
                "confidence": enhanced_validations[1]["confidence"]
            },
            "pe_ratio_validation": {
                "reported_pe": reported_pe,
                "yahoo_finance_pe": yahoo_pe,
                "variance_percentage": round(pe_variance, 2),
                "validation_grade": enhanced_validations[2]["validation_grade"],
                "confidence": enhanced_validations[2]["confidence"]
            }
        },
        "validation_timestamp": datetime.now().isoformat(),
        "data_freshness": "real_time",
        "yahoo_finance_api_response": yahoo_data
    }

    # Update critical findings with real-time validation results
    high_confidence_claims = []
    for validation in enhanced_validations:
        if validation["confidence"] == "9.8/10.0":
            high_confidence_claims.append(
                f"{validation['metric']}: {validation['reported']} matches Yahoo Finance {validation['yahoo_finance']} with {validation['variance_percentage']:.2f}% variance"
            )

    validation_report["critical_findings_matrix"]["verified_claims_high_confidence"].extend(high_confidence_claims)

    # Calculate enhanced market data accuracy score
    market_scores = []
    for validation in enhanced_validations:
        if validation["confidence"] == "9.8/10.0":
            market_scores.append(9.8)
        elif validation["confidence"] == "9.5/10.0":
            market_scores.append(9.5)
        else:
            market_scores.append(8.5)

    enhanced_market_accuracy = sum(market_scores) / len(market_scores)

    # Update discovery validation scores
    validation_report["dasv_validation_breakdown"]["discovery_validation"]["market_data_accuracy"] = f"{enhanced_market_accuracy:.1f}/10.0"

    # Recalculate overall discovery score
    enhanced_discovery_score = (
        enhanced_market_accuracy * 0.4 +
        float(validation_report["dasv_validation_breakdown"]["discovery_validation"]["financial_statements_integrity"].split("/")[0]) * 0.4 +
        float(validation_report["dasv_validation_breakdown"]["discovery_validation"]["data_quality_assessment"].split("/")[0]) * 0.2
    )

    validation_report["dasv_validation_breakdown"]["discovery_validation"]["overall_discovery_score"] = f"{enhanced_discovery_score:.1f}/10.0"

    # Recalculate overall reliability score
    discovery_score = enhanced_discovery_score
    analysis_score = float(validation_report["dasv_validation_breakdown"]["analysis_validation"]["overall_analysis_score"].split("/")[0])
    synthesis_score = float(validation_report["dasv_validation_breakdown"]["synthesis_validation"]["overall_synthesis_score"].split("/")[0])

    enhanced_overall_score = (discovery_score * 0.35 + analysis_score * 0.35 + synthesis_score * 0.30)

    validation_report["overall_assessment"]["overall_reliability_score"] = f"{enhanced_overall_score:.1f}/10.0"

    # Update execution timestamp
    validation_report["metadata"]["execution_timestamp"] = datetime.now().isoformat()

    # Save enhanced validation report
    enhanced_output_path = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/validation/V_20250702_validation_enhanced.json"
    with open(enhanced_output_path, 'w') as f:
        json.dump(validation_report, f, indent=2)

    # Also update the original validation file
    with open(validation_path, 'w') as f:
        json.dump(validation_report, f, indent=2)

    print(f"✅ Enhanced validation complete with real-time data")
    print(f"📊 Enhanced Market Data Accuracy: {enhanced_market_accuracy:.1f}/10.0")
    print(f"📊 Enhanced Overall Reliability: {enhanced_overall_score:.1f}/10.0")
    print(f"💰 Current Price Validation: {yahoo_price} (variance: {price_variance:.2f}%)")
    print(f"📈 Market Cap Validation: ${yahoo_mcap:,.0f} (variance: {mcap_variance:.2f}%)")
    print(f"📊 P/E Ratio Validation: {yahoo_pe} (variance: {pe_variance:.2f}%)")

    return validation_report

if __name__ == "__main__":
    enhanced_report = create_enhanced_validation_report()
