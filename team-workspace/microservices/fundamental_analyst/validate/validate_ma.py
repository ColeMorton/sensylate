#!/usr/bin/env python3
"""
Phase 4: Validate - Quality Assurance and Confidence Verification for Mastercard (MA)
"""

import json
import os
from datetime import datetime
import re

def load_all_phase_data(ticker="MA"):
    """Load data from all previous phases"""
    date_str = datetime.now().strftime('%Y%m%d')

    # Load discovery data
    discovery_path = f"/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/discover/outputs/discover_{ticker}_{date_str}.json"
    with open(discovery_path, 'r') as f:
        discovery_data = json.load(f)

    # Load analysis data
    analysis_path = f"/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/analyze/outputs/analyze_{ticker}_{date_str}.json"
    with open(analysis_path, 'r') as f:
        analysis_data = json.load(f)

    # Load synthesis data
    synthesis_path = f"/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/synthesize/outputs/synthesize_{ticker}_{date_str}.json"
    with open(synthesis_path, 'r') as f:
        synthesis_data = json.load(f)

    # Load generated document
    document_path = f"/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/{ticker}_{date_str}.md"
    with open(document_path, 'r') as f:
        document_content = f.read()

    return discovery_data, analysis_data, synthesis_data, document_content

def validate_financial_metrics(discovery_data, document_content):
    """Cross-validate financial metrics with primary sources"""
    validation_results = []

    # Extract metrics from discovery data
    metrics = discovery_data['financial_metrics']
    market_data = discovery_data['market_data']

    # Define key metrics to validate
    key_metrics = {
        'current_price': market_data['current_price'],
        'market_cap': market_data['market_cap'],
        'pe_ratio': metrics['pe_ratio'],
        'profit_margin': metrics['profit_margin'],
        'roe': metrics['return_on_equity'],
        'revenue_growth': metrics['revenue_growth'],
        'free_cash_flow': metrics['free_cash_flow']
    }

    # Validate each metric appears correctly in document
    for metric_name, metric_value in key_metrics.items():
        if metric_value == 0:
            continue

        # Format value for search
        if metric_name in ['profit_margin', 'roe', 'revenue_growth']:
            formatted_value = f"{metric_value:.1%}"
        elif metric_name in ['current_price', 'pe_ratio']:
            formatted_value = f"{metric_value:.1f}"
        elif metric_name in ['market_cap', 'free_cash_flow']:
            formatted_value = f"{metric_value:,.0f}"
        else:
            formatted_value = str(metric_value)

        # Check if value appears in document
        if formatted_value in document_content or str(metric_value) in document_content:
            validation_results.append({
                "metric": metric_name,
                "source_value": metric_value,
                "status": "PASS",
                "message": "Metric correctly reflected in document"
            })
        else:
            validation_results.append({
                "metric": metric_name,
                "source_value": metric_value,
                "status": "WARNING",
                "message": f"Metric value {formatted_value} not found in exact format"
            })

    # Calculate validation score
    passed = sum(1 for r in validation_results if r['status'] == 'PASS')
    total = len(validation_results)
    validation_score = passed / total if total > 0 else 0

    return {
        "validation_results": validation_results,
        "validation_score": validation_score,
        "passed": passed,
        "total": total
    }

def validate_investment_thesis(synthesis_data, document_content):
    """Verify investment thesis coherence and logic"""
    thesis_checks = []

    # Check recommendation consistency
    recommendation = synthesis_data['investment_thesis']['investment_recommendation']
    upside = synthesis_data['valuation']['upside_potential']

    # Validate recommendation logic
    if recommendation == "BUY" and upside > 0.15:
        thesis_checks.append({
            "check": "Recommendation Logic",
            "status": "PASS",
            "message": "BUY recommendation consistent with >15% upside"
        })
    elif recommendation == "HOLD" and -0.10 <= upside <= 0.15:
        thesis_checks.append({
            "check": "Recommendation Logic",
            "status": "PASS",
            "message": "HOLD recommendation consistent with -10% to +15% range"
        })
    elif recommendation == "SELL" and upside < -0.10:
        thesis_checks.append({
            "check": "Recommendation Logic",
            "status": "PASS",
            "message": "SELL recommendation consistent with >10% downside"
        })
    else:
        thesis_checks.append({
            "check": "Recommendation Logic",
            "status": "FAIL",
            "message": f"Recommendation {recommendation} inconsistent with {upside:.1%} upside"
        })

    # Check thesis components
    thesis_components = synthesis_data['investment_thesis']['thesis_components']
    if len(thesis_components) >= 3:
        thesis_checks.append({
            "check": "Thesis Completeness",
            "status": "PASS",
            "message": f"Comprehensive thesis with {len(thesis_components)} components"
        })
    else:
        thesis_checks.append({
            "check": "Thesis Completeness",
            "status": "WARNING",
            "message": f"Limited thesis with only {len(thesis_components)} components"
        })

    # Check scenario analysis
    scenarios = synthesis_data['scenario_analysis']['scenarios']
    if all(s in scenarios for s in ['bull_case', 'base_case', 'bear_case']):
        thesis_checks.append({
            "check": "Scenario Analysis",
            "status": "PASS",
            "message": "Complete bull/base/bear scenario analysis"
        })
    else:
        thesis_checks.append({
            "check": "Scenario Analysis",
            "status": "FAIL",
            "message": "Incomplete scenario analysis"
        })

    # Calculate thesis score
    passed = sum(1 for c in thesis_checks if c['status'] == 'PASS')
    total = len(thesis_checks)
    thesis_score = passed / total if total > 0 else 0

    return {
        "thesis_checks": thesis_checks,
        "thesis_score": thesis_score,
        "passed": passed,
        "total": total
    }

def validate_confidence_methodology(analysis_data, synthesis_data):
    """Assess confidence score format compliance and methodology"""
    confidence_checks = []

    # Check confidence scores are in 0.0-1.0 range
    confidence_values = [
        ("Analysis Confidence", analysis_data['analysis_confidence']),
        ("Synthesis Confidence", synthesis_data['synthesis_confidence']),
        ("Thesis Confidence", synthesis_data['investment_thesis']['overall_confidence'])
    ]

    for name, value in confidence_values:
        if 0.0 <= value <= 1.0:
            confidence_checks.append({
                "check": f"{name} Range",
                "status": "PASS",
                "value": value,
                "message": "Confidence score within valid range"
            })
        else:
            confidence_checks.append({
                "check": f"{name} Range",
                "status": "FAIL",
                "value": value,
                "message": "Confidence score outside 0.0-1.0 range"
            })

    # Check confidence methodology
    if all(0.0 <= v[1] <= 1.0 for v in confidence_values):
        avg_confidence = sum(v[1] for v in confidence_values) / len(confidence_values)
        if avg_confidence >= 0.7:
            confidence_checks.append({
                "check": "Overall Confidence Level",
                "status": "PASS",
                "value": avg_confidence,
                "message": "High confidence analysis"
            })
        elif avg_confidence >= 0.5:
            confidence_checks.append({
                "check": "Overall Confidence Level",
                "status": "WARNING",
                "value": avg_confidence,
                "message": "Moderate confidence analysis"
            })
        else:
            confidence_checks.append({
                "check": "Overall Confidence Level",
                "status": "FAIL",
                "value": avg_confidence,
                "message": "Low confidence analysis"
            })

    # Calculate methodology score
    passed = sum(1 for c in confidence_checks if c['status'] == 'PASS')
    total = len(confidence_checks)
    methodology_score = passed / total if total > 0 else 0

    return {
        "confidence_checks": confidence_checks,
        "methodology_score": methodology_score,
        "passed": passed,
        "total": total,
        "average_confidence": avg_confidence if 'avg_confidence' in locals() else 0
    }

def validate_quality_standards(document_content):
    """Verify institutional quality standards"""
    quality_checks = []

    # Check document structure
    required_sections = [
        "Executive Summary",
        "Company Overview",
        "Financial Analysis",
        "Competitive Position",
        "Growth Drivers",
        "Valuation Analysis",
        "Investment Thesis",
        "Scenario Analysis",
        "Risk Assessment",
        "Investment Recommendation"
    ]

    for section in required_sections:
        if f"## {section}" in document_content or f"# {section}" in document_content:
            quality_checks.append({
                "check": f"{section} Section",
                "status": "PASS",
                "message": "Required section present"
            })
        else:
            quality_checks.append({
                "check": f"{section} Section",
                "status": "FAIL",
                "message": "Required section missing"
            })

    # Check formatting standards
    if "**Author**: Cole Morton" in document_content:
        quality_checks.append({
            "check": "Author Attribution",
            "status": "PASS",
            "message": "Correct author attribution"
        })
    else:
        quality_checks.append({
            "check": "Author Attribution",
            "status": "FAIL",
            "message": "Missing or incorrect author attribution"
        })

    # Check data presentation
    if "|" in document_content and "---" in document_content:
        quality_checks.append({
            "check": "Table Formatting",
            "status": "PASS",
            "message": "Professional table formatting present"
        })
    else:
        quality_checks.append({
            "check": "Table Formatting",
            "status": "WARNING",
            "message": "Limited table formatting"
        })

    # Check professional language
    if len(document_content) > 5000:
        quality_checks.append({
            "check": "Document Completeness",
            "status": "PASS",
            "message": f"Comprehensive analysis ({len(document_content):,} characters)"
        })
    else:
        quality_checks.append({
            "check": "Document Completeness",
            "status": "WARNING",
            "message": f"Brief analysis ({len(document_content):,} characters)"
        })

    # Calculate quality score
    passed = sum(1 for c in quality_checks if c['status'] == 'PASS')
    total = len(quality_checks)
    quality_score = passed / total if total > 0 else 0

    return {
        "quality_checks": quality_checks,
        "quality_score": quality_score,
        "passed": passed,
        "total": total,
        "document_length": len(document_content)
    }

def calculate_content_evaluator_score(validation_results):
    """Calculate overall content evaluator score (target 8.5+)"""

    # Weight components
    weights = {
        "financial_validation": 0.30,
        "thesis_coherence": 0.25,
        "confidence_methodology": 0.20,
        "quality_standards": 0.25
    }

    # Calculate weighted score
    weighted_score = (
        validation_results['financial_validation']['validation_score'] * weights['financial_validation'] +
        validation_results['thesis_coherence']['thesis_score'] * weights['thesis_coherence'] +
        validation_results['confidence_methodology']['methodology_score'] * weights['confidence_methodology'] +
        validation_results['quality_standards']['quality_score'] * weights['quality_standards']
    )

    # Convert to 10-point scale
    content_score = weighted_score * 10

    return {
        "content_evaluator_score": round(content_score, 1),
        "target_score": 8.5,
        "meets_target": content_score >= 8.5,
        "component_scores": {
            "financial_accuracy": round(validation_results['financial_validation']['validation_score'] * 10, 1),
            "thesis_quality": round(validation_results['thesis_coherence']['thesis_score'] * 10, 1),
            "confidence_compliance": round(validation_results['confidence_methodology']['methodology_score'] * 10, 1),
            "institutional_quality": round(validation_results['quality_standards']['quality_score'] * 10, 1)
        }
    }

def validate_fundamental_analysis(ticker="MA"):
    """Execute comprehensive validation and quality assurance"""

    print(f"✅ Phase 4: Validate - Quality assurance for {ticker}")

    # Load all phase data
    discovery_data, analysis_data, synthesis_data, document_content = load_all_phase_data(ticker)

    # Perform validations
    financial_validation = validate_financial_metrics(discovery_data, document_content)
    thesis_coherence = validate_investment_thesis(synthesis_data, document_content)
    confidence_methodology = validate_confidence_methodology(analysis_data, synthesis_data)
    quality_standards = validate_quality_standards(document_content)

    # Compile validation results
    validation_results = {
        "financial_validation": financial_validation,
        "thesis_coherence": thesis_coherence,
        "confidence_methodology": confidence_methodology,
        "quality_standards": quality_standards
    }

    # Calculate content evaluator score
    content_evaluation = calculate_content_evaluator_score(validation_results)

    # Create validation report
    validation_report = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "validation_results": validation_results,
        "content_evaluation": content_evaluation,
        "overall_status": "PASS" if content_evaluation['meets_target'] else "NEEDS_IMPROVEMENT",
        "key_findings": []
    }

    # Add key findings
    if financial_validation['validation_score'] < 0.8:
        validation_report['key_findings'].append("Some financial metrics need verification")

    if not thesis_coherence['thesis_checks'][0]['status'] == 'PASS':
        validation_report['key_findings'].append("Investment recommendation logic needs review")

    if confidence_methodology['average_confidence'] < 0.7:
        validation_report['key_findings'].append("Overall confidence below optimal threshold")

    if quality_standards['quality_score'] < 0.8:
        validation_report['key_findings'].append("Document structure or formatting needs improvement")

    if content_evaluation['meets_target']:
        validation_report['key_findings'].append("Analysis meets institutional quality standards")

    # Save validation report
    output_path = "/Users/colemorton/Projects/sensylate/team-workspace/microservices/fundamental_analyst/validate/outputs"
    output_file = os.path.join(output_path, f"validate_{ticker}_{datetime.now().strftime('%Y%m%d')}.json")

    with open(output_file, 'w') as f:
        json.dump(validation_report, f, indent=2)

    print(f"✅ Phase 4 Complete: Validation report saved to {output_file}")
    print(f"📊 Content Evaluator Score: {content_evaluation['content_evaluator_score']}/10 (Target: 8.5+)")
    print(f"✓ Financial Accuracy: {content_evaluation['component_scores']['financial_accuracy']}/10")
    print(f"✓ Thesis Quality: {content_evaluation['component_scores']['thesis_quality']}/10")
    print(f"✓ Confidence Compliance: {content_evaluation['component_scores']['confidence_compliance']}/10")
    print(f"✓ Institutional Quality: {content_evaluation['component_scores']['institutional_quality']}/10")
    print(f"🎯 Overall Status: {validation_report['overall_status']}")

    return validation_report

if __name__ == "__main__":
    # Execute validation phase
    validation_report = validate_fundamental_analysis("MA")
