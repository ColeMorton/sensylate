#!/usr/bin/env python3
"""
Phase 4: Validate - Quality Assurance and Confidence Verification for LYV (Live Nation Entertainment)
DASV Framework Implementation
"""

import json
import os
import sys
from datetime import datetime
import re

def load_discovery_data(ticker):
    """Load discovery data from Phase 1"""
    current_date = datetime.now().strftime("%Y%m%d")
    discovery_file = f"/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/discovery/{ticker}_{current_date}_discovery.json"

    try:
        with open(discovery_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Discovery file not found at {discovery_file}")
        return None

def load_analysis_data(ticker):
    """Load analysis data from Phase 2"""
    current_date = datetime.now().strftime("%Y%m%d")
    analysis_file = f"/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/analysis/{ticker}_{current_date}_analysis.json"

    try:
        with open(analysis_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Analysis file not found at {analysis_file}")
        return None

def load_synthesis_document(ticker):
    """Load synthesis document from Phase 3"""
    current_date = datetime.now().strftime("%Y%m%d")
    synthesis_file = f"/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/{ticker}_{current_date}.md"

    try:
        with open(synthesis_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Synthesis file not found at {synthesis_file}")
        return None

def validate_discovery_phase(discovery_data):
    """Validate discovery phase data quality"""
    validation_results = {
        "phase": "discovery",
        "overall_score": 0,
        "detailed_scores": {},
        "quality_issues": [],
        "strengths": []
    }

    if not discovery_data:
        validation_results["overall_score"] = 0
        validation_results["quality_issues"].append("Discovery data not available")
        return validation_results

    # Validate market data completeness and accuracy
    market_data = discovery_data.get("market_data", {})
    current_price_data = market_data.get("current_price_data", {})

    market_data_score = 0
    if current_price_data.get("price", 0) > 0:
        market_data_score += 25
        validation_results["strengths"].append("Current price data available")
    if current_price_data.get("market_cap", 0) > 0:
        market_data_score += 25
        validation_results["strengths"].append("Market cap data available")
    if current_price_data.get("volume", 0) > 0:
        market_data_score += 25
        validation_results["strengths"].append("Volume data available")
    if current_price_data.get("confidence", 0) >= 0.8:
        market_data_score += 25
        validation_results["strengths"].append("High confidence in market data")

    validation_results["detailed_scores"]["market_data_accuracy"] = market_data_score

    # Validate financial statements integrity
    financial_statements = discovery_data.get("company_intelligence", {}).get("financial_statements", {})

    financial_score = 0
    required_fields = ["total_revenue", "net_income", "total_assets", "cash_and_equivalents", "total_debt"]
    available_fields = sum(1 for field in required_fields if financial_statements.get(field, 0) != 0)
    financial_score = (available_fields / len(required_fields)) * 100

    validation_results["detailed_scores"]["financial_statements_integrity"] = financial_score

    if financial_score < 60:
        validation_results["quality_issues"].append("Incomplete financial statement data")
    else:
        validation_results["strengths"].append("Comprehensive financial statements")

    # Validate business intelligence quality
    business_model = discovery_data.get("company_intelligence", {}).get("business_model", {})

    business_score = 0
    if business_model.get("company_name"):
        business_score += 20
    if business_model.get("sector"):
        business_score += 20
    if business_model.get("business_summary"):
        business_score += 30
    if business_model.get("revenue_streams"):
        business_score += 30

    validation_results["detailed_scores"]["business_intelligence_quality"] = business_score

    # Overall data quality assessment
    data_quality = discovery_data.get("data_quality_assessment", {})
    overall_data_quality = data_quality.get("overall_data_quality", 0) * 100

    validation_results["detailed_scores"]["data_quality_assessment"] = overall_data_quality

    # Calculate overall discovery score
    scores = [
        validation_results["detailed_scores"]["market_data_accuracy"],
        validation_results["detailed_scores"]["financial_statements_integrity"],
        validation_results["detailed_scores"]["business_intelligence_quality"],
        validation_results["detailed_scores"]["data_quality_assessment"]
    ]

    validation_results["overall_score"] = sum(scores) / len(scores)

    return validation_results

def validate_analysis_phase(analysis_data):
    """Validate analysis phase quality"""
    validation_results = {
        "phase": "analysis",
        "overall_score": 0,
        "detailed_scores": {},
        "quality_issues": [],
        "strengths": []
    }

    if not analysis_data:
        validation_results["overall_score"] = 0
        validation_results["quality_issues"].append("Analysis data not available")
        return validation_results

    # Validate financial health analysis
    financial_health = analysis_data.get("financial_health_analysis", {})
    financial_health_score = financial_health.get("overall_financial_health", 0)

    validation_results["detailed_scores"]["financial_health_analysis"] = financial_health_score

    if financial_health_score < 50:
        validation_results["quality_issues"].append("Financial health analysis shows concerning results")
    else:
        validation_results["strengths"].append("Comprehensive financial health analysis")

    # Validate competitive position assessment
    competitive_position = analysis_data.get("competitive_position_assessment", {})
    competitive_score = competitive_position.get("competitive_strength_score", 0)

    validation_results["detailed_scores"]["competitive_analysis_depth"] = competitive_score

    if len(competitive_position.get("competitive_advantages", [])) >= 3:
        validation_results["strengths"].append("Thorough competitive advantage analysis")
    else:
        validation_results["quality_issues"].append("Limited competitive advantage analysis")

    # Validate valuation analysis
    valuation_analysis = analysis_data.get("valuation_analysis", {})
    current_valuation = valuation_analysis.get("current_valuation", {})

    valuation_score = 0
    valuation_metrics = ["pe_ratio", "price_to_sales", "price_to_book", "ev_to_revenue"]
    available_metrics = sum(1 for metric in valuation_metrics if current_valuation.get(metric, 0) > 0)
    valuation_score = (available_metrics / len(valuation_metrics)) * 100

    validation_results["detailed_scores"]["valuation_methodology"] = valuation_score

    # Validate risk assessment
    risk_assessment = analysis_data.get("risk_assessment", {})
    business_risks = risk_assessment.get("business_risks", [])
    financial_risks = risk_assessment.get("financial_risks", [])

    risk_score = 0
    if len(business_risks) >= 3:
        risk_score += 50
        validation_results["strengths"].append("Comprehensive business risk analysis")
    if len(financial_risks) >= 2:
        risk_score += 50
        validation_results["strengths"].append("Thorough financial risk assessment")

    validation_results["detailed_scores"]["risk_assessment_completeness"] = risk_score

    # Investment thesis validation
    investment_thesis = analysis_data.get("investment_thesis", {})
    thesis_score = 0

    if investment_thesis.get("bull_case") and len(investment_thesis["bull_case"]) >= 3:
        thesis_score += 25
    if investment_thesis.get("bear_case") and len(investment_thesis["bear_case"]) >= 3:
        thesis_score += 25
    if investment_thesis.get("key_catalysts") and len(investment_thesis["key_catalysts"]) >= 3:
        thesis_score += 25
    if investment_thesis.get("investment_thesis", {}).get("recommendation"):
        thesis_score += 25

    validation_results["detailed_scores"]["investment_thesis_quality"] = thesis_score

    # Calculate overall analysis score
    scores = [
        validation_results["detailed_scores"]["financial_health_analysis"],
        validation_results["detailed_scores"]["competitive_analysis_depth"],
        validation_results["detailed_scores"]["valuation_methodology"],
        validation_results["detailed_scores"]["risk_assessment_completeness"],
        validation_results["detailed_scores"]["investment_thesis_quality"]
    ]

    validation_results["overall_score"] = sum(scores) / len(scores)

    return validation_results

def validate_synthesis_phase(synthesis_document, discovery_data, analysis_data):
    """Validate synthesis document quality"""
    validation_results = {
        "phase": "synthesis",
        "overall_score": 0,
        "detailed_scores": {},
        "quality_issues": [],
        "strengths": []
    }

    if not synthesis_document:
        validation_results["overall_score"] = 0
        validation_results["quality_issues"].append("Synthesis document not available")
        return validation_results

    # Document structure validation
    required_sections = [
        "Executive Summary",
        "Business Analysis",
        "Financial Analysis",
        "Valuation Analysis",
        "Risk Analysis",
        "Investment Thesis",
        "Conclusion"
    ]

    structure_score = 0
    missing_sections = []

    for section in required_sections:
        if f"## {section}" in synthesis_document:
            structure_score += (100 / len(required_sections))
        else:
            missing_sections.append(section)

    validation_results["detailed_scores"]["document_structure"] = structure_score

    if missing_sections:
        validation_results["quality_issues"].append(f"Missing sections: {', '.join(missing_sections)}")
    else:
        validation_results["strengths"].append("Complete document structure")

    # Content quality validation
    word_count = len(synthesis_document.split())

    content_quality_score = 0
    if word_count >= 2000:
        content_quality_score += 50
        validation_results["strengths"].append("Comprehensive content length")
    elif word_count >= 1000:
        content_quality_score += 30
    else:
        validation_results["quality_issues"].append("Document may be too brief")

    # Data integration validation
    company_name = discovery_data.get("company_intelligence", {}).get("business_model", {}).get("company_name", "")
    if company_name in synthesis_document:
        content_quality_score += 25
        validation_results["strengths"].append("Proper company identification")

    # Recommendation presence
    recommendation = analysis_data.get("investment_thesis", {}).get("investment_thesis", {}).get("recommendation", "")
    if recommendation and recommendation in synthesis_document:
        content_quality_score += 25
        validation_results["strengths"].append("Clear investment recommendation")

    validation_results["detailed_scores"]["content_quality"] = content_quality_score

    # Professional presentation validation
    presentation_score = 0

    # Check for tables
    if "|" in synthesis_document and "---" in synthesis_document:
        presentation_score += 25
        validation_results["strengths"].append("Professional table formatting")

    # Check for proper markdown formatting
    if synthesis_document.count("**") >= 10:  # Bold formatting
        presentation_score += 25

    # Check for bullet points
    if synthesis_document.count("- ") >= 20:
        presentation_score += 25

    # Check for proper structure indicators
    if "###" in synthesis_document:
        presentation_score += 25

    validation_results["detailed_scores"]["professional_presentation"] = presentation_score

    # Calculate overall synthesis score
    scores = [
        validation_results["detailed_scores"]["document_structure"],
        validation_results["detailed_scores"]["content_quality"],
        validation_results["detailed_scores"]["professional_presentation"]
    ]

    validation_results["overall_score"] = sum(scores) / len(scores)

    return validation_results

def validate_fundamental_analysis(ticker="LYV"):
    """Execute comprehensive validation of all DASV phases"""

    print(f"✅ Phase 4: Validate - Quality assurance for {ticker}")

    # Load all phase data
    discovery_data = load_discovery_data(ticker)
    analysis_data = load_analysis_data(ticker)
    synthesis_document = load_synthesis_document(ticker)

    # Validate each phase
    discovery_validation = validate_discovery_phase(discovery_data)
    analysis_validation = validate_analysis_phase(analysis_data)
    synthesis_validation = validate_synthesis_phase(synthesis_document, discovery_data, analysis_data)

    # Overall validation summary
    phase_scores = [
        discovery_validation["overall_score"],
        analysis_validation["overall_score"],
        synthesis_validation["overall_score"]
    ]

    overall_quality_score = sum(phase_scores) / len(phase_scores)

    # Quality rating
    if overall_quality_score >= 90:
        quality_rating = "Excellent"
    elif overall_quality_score >= 80:
        quality_rating = "Good"
    elif overall_quality_score >= 70:
        quality_rating = "Satisfactory"
    elif overall_quality_score >= 60:
        quality_rating = "Needs Improvement"
    else:
        quality_rating = "Poor"

    # Comprehensive validation results
    current_date = datetime.now().strftime("%Y%m%d")
    validation_data = {
        "metadata": {
            "command_name": "fundamental_analyst_validate",
            "execution_timestamp": datetime.now().isoformat(),
            "framework_phase": "validate",
            "ticker": ticker,
            "validation_methodology": "comprehensive_quality_assurance"
        },
        "validation_summary": {
            "overall_quality_score": overall_quality_score,
            "quality_rating": quality_rating,
            "phases_validated": 3,
            "validation_confidence": 0.9
        },
        "phase_validations": {
            "discovery_validation": discovery_validation,
            "analysis_validation": analysis_validation,
            "synthesis_validation": synthesis_validation
        },
        "quality_assurance": {
            "institutional_quality_standard": overall_quality_score >= 80,
            "professional_presentation": synthesis_validation["detailed_scores"]["professional_presentation"] >= 75,
            "comprehensive_analysis": analysis_validation["overall_score"] >= 75,
            "data_integrity": discovery_validation["overall_score"] >= 75
        },
        "improvement_recommendations": [],
        "validation_conclusion": {
            "analysis_approved": overall_quality_score >= 70,
            "confidence_level": "High" if overall_quality_score >= 85 else "Moderate" if overall_quality_score >= 70 else "Low",
            "ready_for_publication": overall_quality_score >= 75
        }
    }

    # Add improvement recommendations based on identified issues
    all_issues = (discovery_validation["quality_issues"] +
                 analysis_validation["quality_issues"] +
                 synthesis_validation["quality_issues"])

    if all_issues:
        validation_data["improvement_recommendations"] = list(set(all_issues))

    # Save validation results
    output_dir = "/Users/colemorton/Projects/sensylate/data/outputs/fundamental_analysis/validation"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{ticker}_{current_date}_validation.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        json.dump(validation_data, f, indent=2, default=str)

    print(f"✅ Validation phase completed - saved to {filepath}")
    print(f"📊 Overall Quality Score: {overall_quality_score:.1f}/100 ({quality_rating})")

    return validation_data

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "LYV"
    validate_fundamental_analysis(ticker)
