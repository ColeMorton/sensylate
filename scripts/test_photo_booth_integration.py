#!/usr/bin/env python3
"""
Photo Booth Integration Test

This script validates the photo booth setup and configuration.
"""

import json
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_configuration():
    """Test that the photo booth configuration exists and is valid."""
    print("🔍 Testing configuration...")

    config_path = project_root / "frontend/src/config/photo-booth.json"

    if not config_path.exists():
        print("❌ Configuration file not found: {config_path}")
        return False

    try:
        with open(config_path) as f:
            config = json.load(f)

        # Validate required keys
        required_keys = [
            "default_dashboard",
            "active_dashboards",
            "screenshot_settings",
            "output",
        ]
        for key in required_keys:
            if key not in config:
                print("❌ Missing required configuration key: {key}")
                return False

        # Validate active dashboards
        if not config["active_dashboards"]:
            print("❌ No active dashboards configured")
            return False

        enabled_dashboards = [
            d for d in config["active_dashboards"] if d.get("enabled", False)
        ]
        if not enabled_dashboards:
            print("❌ No enabled dashboards found")
            return False

        print("✅ Configuration valid - {len(enabled_dashboards)} enabled dashboards")
        return True

    except json.JSONDecodeError as e:
        print("❌ Invalid JSON in configuration: {e}")
        return False


def test_page_files():
    """Test that the photo booth page and components exist."""
    print("🔍 Testing page files...")

    # Check photo booth page (now direct Astro page)
    page_path = project_root / "frontend/src/pages/photo-booth.astro"
    if not page_path.exists():
        print("❌ Photo booth page not found: {page_path}")
        return False

    # Check component
    component_path = (
        project_root / "frontend/src/layouts/shortcodes/PhotoBoothDisplay.tsx"
    )
    if not component_path.exists():
        print("❌ PhotoBoothDisplay component not found: {component_path}")
        return False

    print("✅ Page files exist")
    return True


def test_dashboard_templates():
    """Test that dashboard templates exist."""
    print("🔍 Testing dashboard templates...")

    dashboards_dir = project_root / "frontend/src/content/dashboards"
    if not dashboards_dir.exists():
        print("❌ Dashboards directory not found: {dashboards_dir}")
        return False

    dashboard_files = list(dashboards_dir.glob("*.mdx"))
    if not dashboard_files:
        print("❌ No dashboard template files found")
        return False

    print("✅ Found {len(dashboard_files)} dashboard templates")
    return True


def test_screenshot_generator():
    """Test that the screenshot generator script exists."""
    print("🔍 Testing screenshot generator...")

    generator_path = project_root / "scripts/photo_booth_generator.py"
    if not generator_path.exists():
        print("❌ Screenshot generator not found: {generator_path}")
        return False

    print("✅ Screenshot generator exists")
    return True


def test_yarn_scripts():
    """Test that yarn scripts are configured."""
    print("🔍 Testing yarn scripts...")

    package_json_path = project_root / "frontend/package.json"
    if not package_json_path.exists():
        print("❌ package.json not found: {package_json_path}")
        return False

    try:
        with open(package_json_path) as f:
            package = json.load(f)

        scripts = package.get("scripts", {})
        photo_booth_scripts = [
            key for key in scripts.keys() if key.startswith("photo-booth:")
        ]

        if not photo_booth_scripts:
            print("❌ No photo-booth yarn scripts found")
            return False

        print("✅ Found {len(photo_booth_scripts)} photo-booth yarn scripts")
        return True

    except json.JSONDecodeError as e:
        print("❌ Invalid JSON in package.json: {e}")
        return False


def test_output_directory():
    """Test that output directory can be created."""
    print("🔍 Testing output directory...")

    output_dir = project_root / "data/outputs/photo-booth"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not output_dir.exists():
        print("❌ Could not create output directory: {output_dir}")
        return False

    print("✅ Output directory created successfully")
    return True


def test_dependencies():
    """Test that required dependencies are available."""
    print("🔍 Testing dependencies...")

    # Check if Puppeteer is in package.json
    package_json_path = project_root / "frontend/package.json"
    try:
        with open(package_json_path) as f:
            package = json.load(f)

        dependencies = {
            **package.get("dependencies", {}),
            **package.get("devDependencies", {}),
        }

        if "puppeteer" not in dependencies:
            print("❌ Puppeteer not found in package.json dependencies")
            return False

        print("✅ Dependencies check passed")
        return True

    except Exception as e:
        print("❌ Error checking dependencies: {e}")
        return False


def test_api_endpoint():
    """Test that the API endpoint is properly configured."""
    print("🔍 Testing API endpoint...")

    api_path = project_root / "frontend/src/pages/api/dashboards.json.ts"
    if not api_path.exists():
        print("❌ API endpoint file not found: {api_path}")
        return False

    with open(api_path) as f:
        content = f.read()

    # Check for required API elements
    required_elements = [
        "export const GET: APIRoute",
        "DashboardConfig",
        "DASHBOARD_CONFIGS",
    ]

    for element in required_elements:
        if element not in content:
            print("❌ Missing required API element: {element}")
            return False

    print("✅ API endpoint is properly configured")
    return True


def test_client_side_compatibility():
    """Test that DashboardLoader is client-side compatible."""
    print("🔍 Testing client-side compatibility...")

    loader_path = project_root / "frontend/src/lib/dashboardLoader.ts"
    with open(loader_path) as f:
        content = f.read()

    # Check that astro:content is not used
    if 'from "astro:content"' in content:
        print("❌ DashboardLoader still uses astro:content (client-side incompatible)")
        return False

    # Check for fetch usage
    if 'fetch("/api/dashboards.json")' not in content:
        print("❌ DashboardLoader doesn't use API endpoint")
        return False

    print("✅ Client-side compatibility verified")
    return True


def main():
    """Run all integration tests."""
    print("🚀 Running Photo Booth Integration Tests")
    print("=" * 50)

    tests = [
        test_configuration,
        test_page_files,
        test_dashboard_templates,
        test_screenshot_generator,
        test_yarn_scripts,
        test_output_directory,
        test_dependencies,
        test_api_endpoint,
        test_client_side_compatibility,
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
        print("🎉 All tests passed! Photo booth setup is ready.")
        print("\n📋 Next steps:")
        print("1. Start the Astro dev server: yarn dev")
        print("2. Visit http://localhost:4321/photo-booth")
        print("3. Generate screenshots: yarn photo-booth:generate")
        return 0
    else:
        print("💥 Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
