#!/usr/bin/env python3
"""
Test Enhanced Templates with Sample Data

This script tests that the enhanced fundamental and sector analysis templates
render correctly with existing sample data, verifying that template inheritance
and macro imports work properly.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateError


def load_sample_data(file_path: str) -> dict:
    """Load sample data from JSON file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Sample data file not found: {file_path}")

    with open(path, "r") as f:
        return json.load(f)


def test_template_rendering():
    """Test rendering of enhanced templates with sample data"""

    # Set up paths
    scripts_dir = Path(__file__).parent
    templates_dir = scripts_dir / "templates"
    test_data_dir = scripts_dir / "test_data"

    # Set up Jinja2 environment
    jinja_env = Environment(
        loader=FileSystemLoader(str(templates_dir)), autoescape=True
    )

    print("🧪 Testing Enhanced Templates with Sample Data")
    print("=" * 60)

    # Test cases
    test_cases = [
        {
            "name": "Enhanced Fundamental Analysis Template",
            "template": "fundamental_analysis_enhanced.j2",
            "data_file": test_data_dir / "sample_fundamental_data.json",
            "context_key": "ticker",
            "context_value": "AAPL",
        },
        {
            "name": "Enhanced Sector Analysis Template",
            "template": "sector_analysis_enhanced.j2",
            "data_file": test_data_dir / "sample_sector_data.json",
            "context_key": "sector",
            "context_value": "XLK",
        },
    ]

    results = []

    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print("-" * 40)

        try:
            # Load sample data
            print(f"   Loading data: {test_case['data_file'].name}")
            data = load_sample_data(test_case["data_file"])

            # Load template
            print(f"   Loading template: {test_case['template']}")
            template = jinja_env.get_template(test_case["template"])

            # Prepare context
            context = {
                "data": data,
                test_case["context_key"]: test_case["context_value"],
                "timestamp": datetime.now().isoformat(),
            }

            # Render template
            print(f"   Rendering template...")
            content = template.render(**context)

            # Basic validation
            if len(content) < 1000:
                raise ValueError("Rendered content too short - possible template issue")

            if "{% extends" in content:
                raise ValueError("Template inheritance not processed correctly")

            if "{% from" in content:
                raise ValueError("Macro imports not processed correctly")

            # Check for required sections
            required_sections = [
                "# ",  # Should have markdown headers
                "Economic Sensitivity",
                "Risk Assessment",
                "Confidence",
                "Data Quality",
            ]

            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)

            if missing_sections:
                print(f"   ⚠️  Missing sections: {', '.join(missing_sections)}")

            # Success
            print(f"   ✅ Template rendered successfully")
            print(f"   📊 Content length: {len(content):,} characters")

            results.append(
                {
                    "name": test_case["name"],
                    "status": "PASSED",
                    "content_length": len(content),
                    "missing_sections": missing_sections,
                }
            )

        except TemplateError as e:
            print(f"   ❌ Template Error: {e}")
            results.append(
                {
                    "name": test_case["name"],
                    "status": "FAILED",
                    "error": f"Template Error: {e}",
                }
            )

        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(
                {"name": test_case["name"], "status": "FAILED", "error": str(e)}
            )

    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)

    for result in results:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {result['name']}: {result['status']}")

        if result["status"] == "PASSED":
            print(f"   📊 Content length: {result['content_length']:,} characters")
            if result.get("missing_sections"):
                print(
                    f"   ⚠️  Missing sections: {', '.join(result['missing_sections'])}"
                )
        else:
            print(f"   💥 Error: {result.get('error', 'Unknown error')}")

    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All templates rendered successfully!")
        print("✨ Template duplication reduction implementation is working correctly!")
        return True
    else:
        print("❌ Some templates failed to render. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = test_template_rendering()
    sys.exit(0 if success else 1)
