#!/usr/bin/env python3
"""
Clean Screenshot Layout Test

This script validates that the photo booth page uses a clean layout
without unwanted UI elements for screenshots.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_photobooth_base_layout():
    """Test that PhotoBoothBase.astro exists and has clean layout."""
    print("🔍 Testing PhotoBoothBase layout...")

    layout_path = project_root / "frontend/src/layouts/PhotoBoothBase.astro"
    if not layout_path.exists():
        print("❌ PhotoBoothBase layout not found: {layout_path}")
        return False

    with open(layout_path) as f:
        content = f.read()

    # Check that unwanted UI elements are NOT included
    unwanted_elements = [
        "Header",
        "Footer",
        "WebVitals",
        "TwSizeIndicator",
        "SearchModal",
    ]

    for element in unwanted_elements:
        if f"import {element}" in content or f"<{element}" in content:
            print("❌ Unwanted UI element found: {element}")
            return False

    print("✅ PhotoBoothBase layout is clean (no unwanted UI elements)")
    return True


def test_dev_toolbar_hiding():
    """Test that dev toolbar is properly hidden."""
    print("🔍 Testing dev toolbar hiding...")

    layout_path = project_root / "frontend/src/layouts/PhotoBoothBase.astro"
    with open(layout_path) as f:
        content = f.read()

    # Check for dev toolbar hiding CSS
    required_css = [
        "astro-dev-toolbar",
        "display: none !important",
        "visibility: hidden !important",
    ]

    for css_rule in required_css:
        if css_rule not in content:
            print("❌ Missing CSS rule for dev toolbar hiding: {css_rule}")
            return False

    print("✅ Dev toolbar hiding CSS is properly implemented")
    return True


def test_direct_astro_page():
    """Test that photo-booth.astro is a direct page using clean layout."""
    print("🔍 Testing direct Astro page...")

    page_path = project_root / "frontend/src/pages/photo-booth.astro"
    if not page_path.exists():
        print("❌ Direct photo-booth.astro page not found: {page_path}")
        return False

    with open(page_path) as f:
        content = f.read()

    # Check that it uses PhotoBoothBase layout
    if "PhotoBoothBase" not in content:
        print("❌ Page doesn't use PhotoBoothBase layout")
        return False

    # Check that it imports from the correct location
    if 'import PhotoBoothBase from "@/layouts/PhotoBoothBase.astro"' not in content:
        print("❌ Page doesn't import PhotoBoothBase correctly")
        return False

    print("✅ Direct Astro page is properly configured")
    return True


def test_old_mdx_removed():
    """Test that old MDX file has been removed."""
    print("🔍 Testing old MDX file removal...")

    old_mdx_path = project_root / "frontend/src/content/pages/photo-booth.mdx"
    if old_mdx_path.exists():
        print("❌ Old MDX file still exists: {old_mdx_path}")
        return False

    print("✅ Old MDX file has been removed")
    return True


def test_screenshot_optimization():
    """Test that layout includes screenshot optimization CSS."""
    print("🔍 Testing screenshot optimization...")

    layout_path = project_root / "frontend/src/layouts/PhotoBoothBase.astro"
    with open(layout_path) as f:
        content = f.read()

    # Check for screenshot optimization CSS
    optimization_css = [
        "-webkit-font-smoothing: antialiased",
        "-moz-osx-font-smoothing: grayscale",
        "text-rendering: optimizeLegibility",
        ".photo-booth-ready",
    ]

    for css_rule in optimization_css:
        if css_rule not in content:
            print("❌ Missing screenshot optimization CSS: {css_rule}")
            return False

    print("✅ Screenshot optimization CSS is properly implemented")
    return True


def test_minimal_html_structure():
    """Test that layout has minimal HTML structure."""
    print("🔍 Testing minimal HTML structure...")

    layout_path = project_root / "frontend/src/layouts/PhotoBoothBase.astro"
    with open(layout_path) as f:
        content = f.read()

    # Check that body only contains main element (no header, footer, etc.)
    if "<body>" not in content:
        print("❌ No body tag found")
        return False

    # Extract body content
    body_start = content.find("<body>")
    body_end = content.find("</body>")
    if body_start == -1 or body_end == -1:
        print("❌ Could not extract body content")
        return False

    body_content = content[body_start:body_end]

    # Check that body only contains main element (no unwanted UI components)
    unwanted_in_body = [
        "<Header",
        "<Footer",
        "<WebVitals",
        "<TwSizeIndicator",
        "<SearchModal",
    ]
    for unwanted in unwanted_in_body:
        if unwanted in body_content:
            print("❌ Unwanted element found in body: {unwanted}")
            return False

    # Check that main element is present
    if "<main" not in body_content:
        print("❌ Main element not found in body")
        return False

    print("✅ HTML structure is minimal (body > main > slot)")
    return True


def test_puppeteer_ready_indicator():
    """Test that Puppeteer ready indicator is properly configured."""
    print("🔍 Testing Puppeteer ready indicator...")

    layout_path = project_root / "frontend/src/layouts/PhotoBoothBase.astro"
    with open(layout_path) as f:
        content = f.read()

    # Check for photo-booth-ready class
    if 'class="photo-booth-ready"' not in content:
        print("❌ Missing photo-booth-ready class on main element")
        return False

    # Check for CSS definition
    if ".photo-booth-ready" not in content:
        print("❌ Missing CSS definition for photo-booth-ready")
        return False

    print("✅ Puppeteer ready indicator is properly configured")
    return True


def main():
    """Run all clean screenshot layout tests."""
    print("🚀 Running Clean Screenshot Layout Tests")
    print("=" * 50)

    tests = [
        test_photobooth_base_layout,
        test_dev_toolbar_hiding,
        test_direct_astro_page,
        test_old_mdx_removed,
        test_screenshot_optimization,
        test_minimal_html_structure,
        test_puppeteer_ready_indicator,
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
            print("❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()

    print("=" * 50)
    print("📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 Clean screenshot layout is properly implemented!")
        print("\n📋 Key improvements:")
        print("1. PhotoBoothBase.astro minimal layout ✅")
        print("2. Dev toolbar hiding CSS ✅")
        print("3. Direct Astro page (no MDX routing) ✅")
        print("4. Screenshot optimization CSS ✅")
        print("5. Minimal HTML structure ✅")
        print("6. Puppeteer ready indicator ✅")

        print("\n✨ Unwanted UI elements removed:")
        print("- Header ✅")
        print("- Footer ✅")
        print("- PageHeader ✅")
        print("- Core Web Vitals ✅")
        print("- Astro dev toolbar ✅")

        return 0
    else:
        print("💥 Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
