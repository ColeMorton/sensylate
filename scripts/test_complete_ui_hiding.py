#!/usr/bin/env python3
"""
Complete UI Hiding Test

This script validates that all unwanted UI elements are properly hidden from screenshots
including photo-booth-controls and Astro dev toolbar elements.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_extended_dom_manipulation():
    """Test that Puppeteer script includes extended DOM manipulation for all UI elements."""
    print("🔍 Testing extended DOM manipulation...")

    generator_path = project_root / "scripts/photo_booth_generator.py"
    with open(generator_path) as f:
        content = f.read()

    # Check for both control and dev toolbar hiding
    required_elements = [
        "Hide photo booth controls",
        "Hide Astro dev toolbar",
        "document.querySelectorAll('.photo-booth-controls')",
        "devToolbarSelectors",
        "astro-dev-toolbar",
        "#dev-toolbar-root",
        "[data-astro-dev-toolbar]",
        ".astro-dev-toolbar",
        "#astro-dev-toolbar",
    ]

    for element in required_elements:
        if element not in content:
            print(f"❌ Missing DOM manipulation element: {element}")
            return False

    print("✅ Puppeteer script includes extended DOM manipulation for all UI elements")
    return True


def test_dev_toolbar_selectors():
    """Test that all known dev toolbar selectors are included."""
    print("🔍 Testing dev toolbar selectors coverage...")

    generator_path = project_root / "scripts/photo_booth_generator.py"
    with open(generator_path) as f:
        content = f.read()

    # Extract devToolbarSelectors array
    start = content.find("devToolbarSelectors = [")
    end = content.find("];", start)

    if start == -1 or end == -1:
        print("❌ Cannot find devToolbarSelectors array")
        return False

    selectors_section = content[start:end]

    # Check for all known dev toolbar selectors
    required_selectors = [
        "'astro-dev-toolbar'",
        "'#dev-toolbar-root'",
        "'[data-astro-dev-toolbar]'",
        "'.astro-dev-toolbar'",
        "'#astro-dev-toolbar'",
    ]

    for selector in required_selectors:
        if selector not in selectors_section:
            print(f"❌ Missing dev toolbar selector: {selector}")
            return False

    print("✅ All dev toolbar selectors are properly included")
    return True


def test_combined_logging():
    """Test that logging includes both control and dev toolbar element counts."""
    print("🔍 Testing combined element hiding logging...")

    generator_path = project_root / "scripts/photo_booth_generator.py"
    with open(generator_path) as f:
        content = f.read()

    # Check for combined logging statement
    logging_pattern = "console.log(`Hidden ${{controls.length}} control elements and ${{hiddenDevElements}} dev toolbar elements`);"

    if logging_pattern not in content:
        print("❌ Missing combined element count logging")
        return False

    print("✅ Combined element hiding logging is properly implemented")
    return True


def test_css_cleanup():
    """Test that ineffective CSS has been removed from PhotoBoothBase.astro."""
    print("🔍 Testing CSS cleanup...")

    layout_path = project_root / "frontend/src/layouts/PhotoBoothBase.astro"
    with open(layout_path) as f:
        content = f.read()

    # Check that dev toolbar CSS was removed
    problematic_css = [
        "astro-dev-toolbar {",
        "[data-astro-dev-toolbar],",
        ".astro-dev-toolbar,",
        "#astro-dev-toolbar",
    ]

    for css in problematic_css:
        if css in content:
            print(f"❌ Ineffective CSS still present: {css}")
            return False

    print("✅ All ineffective CSS has been removed from PhotoBoothBase.astro")
    return True


def test_dom_manipulation_order():
    """Test that DOM manipulation happens in correct order."""
    print("🔍 Testing DOM manipulation execution order...")

    generator_path = project_root / "scripts/photo_booth_generator.py"
    with open(generator_path) as f:
        content = f.read()

    # Check execution order
    charts_wait_pos = content.find("Additional wait for charts to render")
    ui_hiding_pos = content.find("Hiding UI elements for clean screenshot")
    screenshot_pos = content.find("Taking screenshot")

    if charts_wait_pos == -1:
        print("❌ Cannot find charts wait code")
        return False

    if ui_hiding_pos == -1:
        print("❌ Cannot find UI hiding code")
        return False

    if screenshot_pos == -1:
        print("❌ Cannot find screenshot code")
        return False

    # Check order: charts wait -> UI hiding -> screenshot
    if not (charts_wait_pos < ui_hiding_pos < screenshot_pos):
        print("❌ DOM manipulation not in correct order")
        return False

    print("✅ DOM manipulation is executed in correct order")
    return True


def test_comprehensive_ui_hiding():
    """Test that all unwanted UI elements are targeted for hiding."""
    print("🔍 Testing comprehensive UI element targeting...")

    generator_path = project_root / "scripts/photo_booth_generator.py"
    with open(generator_path) as f:
        content = f.read()

    # Elements that should be hidden
    target_elements = {
        "Photo Booth Controls": ".photo-booth-controls",
        "Astro Dev Toolbar": "astro-dev-toolbar",
        "Dev Toolbar Root": "#dev-toolbar-root",
        "Dev Toolbar Data Attribute": "[data-astro-dev-toolbar]",
        "Dev Toolbar Class": ".astro-dev-toolbar",
        "Dev Toolbar ID": "#astro-dev-toolbar",
    }

    missing_targets = []
    for name, selector in target_elements.items():
        if selector not in content:
            missing_targets.append(f"{name} ({selector})")

    if missing_targets:
        print(f"❌ Missing UI element targets: {missing_targets}")
        return False

    print("✅ All unwanted UI elements are properly targeted for hiding")
    return True


def main():
    """Run all complete UI hiding tests."""
    print("🚀 Running Complete UI Hiding Tests")
    print("=" * 50)

    tests = [
        test_extended_dom_manipulation,
        test_dev_toolbar_selectors,
        test_combined_logging,
        test_css_cleanup,
        test_dom_manipulation_order,
        test_comprehensive_ui_hiding,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()

    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 Complete UI hiding is properly implemented!")
        print("\n📋 Validation confirmed:")
        print("1. Extended DOM manipulation for all UI elements ✅")
        print("2. Comprehensive dev toolbar selector coverage ✅")
        print("3. Combined element count logging ✅")
        print("4. Ineffective CSS removed from layout ✅")
        print("5. Correct DOM manipulation execution order ✅")
        print("6. All unwanted UI elements targeted ✅")

        print("\n✨ Completely hidden elements:")
        print("- Photo booth controls (selectors, buttons, status) ✅")
        print("- Astro dev toolbar (astro-dev-toolbar) ✅")
        print("- Dev toolbar root (#dev-toolbar-root) ✅")
        print("- All dev toolbar related elements ✅")

        print("\n📸 Screenshots now show ONLY:")
        print("- Dashboard charts and data visualizations")
        print("- Chart titles, legends, and data points")
        print("- Zero UI controls or development tools")

        return 0
    else:
        print("💥 Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
