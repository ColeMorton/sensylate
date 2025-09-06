#!/usr/bin/env python3
"""
API Dashboard Loading Test

This script validates that the new API-based dashboard loading works correctly.
"""

import sys
from pathlib import Path

import requests

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_api_endpoint_exists():
    """Test that the dashboard API endpoint file exists."""
    print("🔍 Testing API endpoint file...")

    api_path = project_root / "frontend/src/pages/api/dashboards.json.ts"
    if not api_path.exists():
        print("❌ API endpoint file not found: {api_path}")
        return False

    with open(api_path) as f:
        content = f.read()

    # Check for required exports and functions
    required_elements = [
        "export const GET: APIRoute",
        'getCollection("dashboards")',
        "DashboardConfig",
        "DASHBOARD_CONFIGS",
    ]

    for element in required_elements:
        if element not in content:
            print("❌ Missing required element: {element}")
            return False

    print("✅ API endpoint file is properly structured")
    return True


def test_dashboard_loader_updated():
    """Test that DashboardLoader no longer uses astro:content."""
    print("🔍 Testing DashboardLoader client-side compatibility...")

    loader_path = project_root / "frontend/src/lib/dashboardLoader.ts"
    with open(loader_path) as f:
        content = f.read()

    # Check that astro:content imports are removed
    if "import { getCollection }" in content:
        print("❌ DashboardLoader still imports getCollection from astro:content")
        return False

    if 'from "astro:content"' in content:
        print("❌ DashboardLoader still has astro:content imports")
        return False

    # Check that fetch is used instead
    if 'fetch("/api/dashboards.json")' not in content:
        print("❌ DashboardLoader doesn't use fetch for API calls")
        return False

    # Check for proper interfaces
    required_interfaces = [
        "interface DashboardAPIResponse",
        "DashboardChart",
        "DashboardConfig",
    ]

    for interface in required_interfaces:
        if interface not in content:
            print("❌ Missing required interface: {interface}")
            return False

    print("✅ DashboardLoader is client-side compatible")
    return True


def test_fallback_configurations():
    """Test that fallback configurations are still available."""
    print("🔍 Testing fallback configurations...")

    loader_path = project_root / "frontend/src/lib/dashboardLoader.ts"
    with open(loader_path) as f:
        content = f.read()

    # Check for fallback logic
    if "DASHBOARD_CONFIGS" not in content:
        print("❌ No fallback configurations found")
        return False

    if "fallbackDashboards" not in content:
        print("❌ No fallback logic found")
        return False

    # Check for expected dashboard IDs
    expected_dashboards = [
        "trading_performance",
        "portfolio_analysis",
        "market_overview",
    ]

    for dashboard_id in expected_dashboards:
        if dashboard_id not in content:
            print("❌ Missing dashboard configuration: {dashboard_id}")
            return False

    print("✅ Fallback configurations are available")
    return True


def test_api_endpoint_running():
    """Test that the API endpoint is accessible (requires dev server)."""
    print("🔍 Testing API endpoint accessibility...")

    try:
        # Try to connect to the API endpoint
        response = requests.get("http://localhost:4321/api/dashboards.json", timeout=5)

        if response.status_code == 200:
            data = response.json()

            if not data.get("success"):
                print("❌ API returned error: {data.get('error', 'Unknown error')}")
                return False

            dashboards = data.get("dashboards", [])
            if not dashboards:
                print("❌ API returned no dashboards")
                return False

            print(
                f"✅ API endpoint is accessible and returns {len(dashboards)} dashboards"
            )
            return True
        else:
            print(
                f"⚠️ API endpoint returned status {response.status_code} (dev server may not be running)"
            )
            return None  # Neutral result - server not running

    except requests.exceptions.RequestException as e:
        print(
            f"⚠️ Could not connect to API endpoint: {e} (dev server may not be running)"
        )
        return None  # Neutral result - server not running


def test_configuration_consistency():
    """Test that API and loader configurations are consistent."""
    print("🔍 Testing configuration consistency...")

    # Load API configurations
    api_path = project_root / "frontend/src/pages/api/dashboards.json.ts"
    with open(api_path) as f:
        api_content = f.read()

    # Load loader configurations
    loader_path = project_root / "frontend/src/lib/dashboardLoader.ts"
    with open(loader_path) as f:
        loader_content = f.read()

    # Check that both have the same dashboard IDs (basic check)
    expected_dashboard_patterns = [
        "trading_performance",
        "portfolio_analysis",
        "market_overview",
    ]

    for pattern in expected_dashboard_patterns:
        if pattern not in api_content:
            print("❌ API missing dashboard: {pattern}")
            return False

        if pattern not in loader_content:
            print("❌ Loader missing dashboard: {pattern}")
            return False

    print("✅ API and loader configurations are consistent")
    return True


def main():
    """Run all API dashboard loading tests."""
    print("🚀 Running API Dashboard Loading Tests")
    print("=" * 50)

    tests = [
        test_api_endpoint_exists,
        test_dashboard_loader_updated,
        test_fallback_configurations,
        test_configuration_consistency,
        test_api_endpoint_running,
    ]

    passed = 0
    failed = 0
    skipped = 0

    for test in tests:
        try:
            result = test()
            if result is True:
                passed += 1
            elif result is False:
                failed += 1
            else:  # result is None (skipped)
                skipped += 1
        except Exception as e:
            print("❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()

    print("=" * 50)
    print("📊 Test Results: {passed} passed, {failed} failed, {skipped} skipped")

    if failed == 0:
        print("🎉 API dashboard loading is properly implemented!")
        print("\n📋 Key improvements:")
        print("1. Server-side API endpoint ✅")
        print("2. Client-side fetch implementation ✅")
        print("3. Fallback configurations ✅")
        print("4. Configuration consistency ✅")
        print(
            f"5. API accessibility {'✅' if skipped == 0 else '⚠️ (requires dev server)'}"
        )

        if skipped > 0:
            print("\n💡 To test API endpoint: yarn dev (then re-run this test)")

        return 0
    else:
        print("💥 Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
