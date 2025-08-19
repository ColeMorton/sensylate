#!/usr/bin/env python3
"""
Template Compliance Validation Script
Validates that synthesis outputs follow the correct template structure
"""

import os
import re
from pathlib import Path


def validate_fundamental_analysis_structure(file_path):
    """
    Validate that a fundamental analysis document follows the template structure
    """
    if not os.path.exists(file_path):
        return {"valid": False, "error": f"File not found: {file_path}"}

    with open(file_path, "r") as f:
        content = f.read()

    issues = []
    required_elements = []

    # Check for required emojis and sections
    required_emojis = ["🎯", "📊", "🏆"]
    for emoji in required_emojis:
        if emoji not in content:
            issues.append(f"Missing required emoji: {emoji}")
        else:
            required_elements.append(f"✅ Found emoji: {emoji}")

    # Check for required dashboard sections
    required_sections = [
        "Investment Thesis & Recommendation",
        "Business Intelligence Dashboard",
        "Business-Specific KPIs",
        "Financial Health Scorecard",
        "Economic Sensitivity Matrix",
        "Competitive Position Analysis",
        "Valuation Analysis",
        "Risk Assessment Framework",
    ]

    for section in required_sections:
        if section in content:
            required_elements.append(f"✅ Found section: {section}")
        else:
            issues.append(f"Missing section: {section}")

    # Check for table structures
    table_patterns = [
        r"\|\s*Metric\s*\|.*\|",  # KPI table header pattern
        r"\|\s*Category\s*\|.*\|",  # Scorecard table pattern
        r"\|\s*Indicator\s*\|.*\|",  # Economic sensitivity pattern
    ]

    for i, pattern in enumerate(table_patterns):
        if re.search(pattern, content):
            required_elements.append(f"✅ Found table structure {i+1}")
        else:
            issues.append(f"Missing expected table structure {i+1}")

    # Check for narrative vs dashboard format
    if "## Executive Summary" in content and len(re.findall(r"\|.*\|", content)) < 10:
        issues.append(
            "Document appears to use narrative format instead of dashboard tables"
        )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "elements_found": required_elements,
        "template_compliance_score": len(required_elements)
        / (len(required_elements) + len(issues))
        if (len(required_elements) + len(issues)) > 0
        else 0,
    }


def main():
    """
    Main validation function
    """
    # Check recent fundamental analysis outputs
    output_dir = Path("./data/outputs/fundamental_analysis/")

    if not output_dir.exists():
        print("❌ Fundamental analysis output directory not found")
        return

    # Get recent .md files
    md_files = list(output_dir.glob("*.md"))
    recent_files = sorted(md_files, key=os.path.getmtime, reverse=True)[:5]

    print("🔍 Template Compliance Validation Report\n")
    print("=" * 60)

    for file_path in recent_files:
        print(f"\n📄 Validating: {file_path.name}")
        print("-" * 40)

        result = validate_fundamental_analysis_structure(file_path)

        if result["valid"]:
            print("✅ PASSED - Template compliance validated")
        else:
            print("❌ FAILED - Template compliance issues found")

        print(f"📊 Compliance Score: {result['template_compliance_score']:.2%}")

        if result["elements_found"]:
            print("\n✅ Elements Found:")
            for element in result["elements_found"][:3]:  # Show first 3
                print(f"   {element}")
            if len(result["elements_found"]) > 3:
                print(f"   ... and {len(result['elements_found']) - 3} more")

        if result["issues"]:
            print("\n❌ Issues Found:")
            for issue in result["issues"]:
                print(f"   • {issue}")

    print("\n" + "=" * 60)
    print("✅ Validation complete")


if __name__ == "__main__":
    main()
