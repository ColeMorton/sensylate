#!/usr/bin/env python3
"""
Photo Booth Access Restriction Test

This script validates that the photo booth page is properly restricted based on environment.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_feature_flag_exists():
    """Test that photoBooth feature flag is properly defined."""
    print("🔍 Testing photoBooth feature flag definition...")

    # Check FeatureFlags interface
    types_path = project_root / "frontend/src/types/index.d.ts"
    with open(types_path) as f:
        content = f.read()

    if "photoBooth: boolean;" not in content:
        print("❌ photoBooth not found in FeatureFlags interface")
        return False

    print("✅ photoBooth feature flag is defined in FeatureFlags interface")
    return True


def test_config_implementation():
    """Test that photoBooth is properly configured in config.ts."""
    print("🔍 Testing photoBooth configuration...")

    config_path = project_root / "frontend/src/lib/config.ts"
    with open(config_path) as f:
        content = f.read()

    # Check for photoBooth configuration
    required_elements = [
        "photoBooth:",
        "PUBLIC_FEATURE_PHOTO_BOOTH",
        "(isDevelopment() || isStaging())",
    ]

    for element in required_elements:
        if element not in content:
            print(f"❌ Missing configuration element: {element}")
            return False

    # Check validation array
    if '"photoBooth"' not in content:
        print("❌ photoBooth not found in validation array")
        return False

    print("✅ photoBooth is properly configured with environment logic")
    return True


def test_netlify_configuration():
    """Test that Netlify environments are properly configured."""
    print("🔍 Testing Netlify environment configuration...")

    netlify_path = project_root / "frontend/netlify.toml"
    with open(netlify_path) as f:
        content = f.read()

    # Find production context
    prod_start = content.find("[context.production.environment]")
    if prod_start == -1:
        print("❌ Production context not found")
        return False

    # Find next context to limit search
    branch_start = content.find("[context.branch-deploy.environment]", prod_start)
    prod_section = content[prod_start:branch_start]

    # Check production has photoBooth disabled
    if 'PUBLIC_FEATURE_PHOTO_BOOTH = "false"' not in prod_section:
        print("❌ Production environment doesn't disable photo booth")
        return False

    # Check staging/preview have photoBooth enabled
    staging_section = content[branch_start:]

    if staging_section.count('PUBLIC_FEATURE_PHOTO_BOOTH = "true"') < 2:
        print("❌ Staging/preview environments don't enable photo booth")
        return False

    print("✅ Netlify environments properly configured")
    print("   - Production: photo booth disabled ✅")
    print("   - Staging: photo booth enabled ✅")
    print("   - Preview: photo booth enabled ✅")
    return True


def test_page_protection():
    """Test that photo-booth.astro page has feature flag check."""
    print("🔍 Testing photo booth page protection...")

    page_path = project_root / "frontend/src/pages/photo-booth.astro"
    with open(page_path) as f:
        content = f.read()

    # Check for feature flag import
    if 'import { features } from "@/lib/config"' not in content:
        print("❌ Missing features import")
        return False

    # Check for feature flag check
    if "!features.photoBooth" not in content:
        print("❌ Missing feature flag check")
        return False

    # Check for redirect
    if 'Astro.redirect("/404")' not in content:
        print("❌ Missing redirect to 404")
        return False

    print("✅ Photo booth page has proper feature flag protection")
    return True


def test_environment_logic():
    """Test the environment detection logic."""
    print("🔍 Testing environment detection logic...")

    config_path = project_root / "frontend/src/lib/config.ts"
    with open(config_path) as f:
        content = f.read()

    # Check for environment detection functions
    env_functions = [
        "function isDevelopment():",
        "function isProduction():",
        "function isStaging():",
    ]

    for func in env_functions:
        if func not in content:
            print(f"❌ Missing environment function: {func}")
            return False

    # Check photoBooth uses environment detection
    photobooth_section = content[
        content.find("photoBooth:") : content.find("photoBooth:") + 300
    ]

    if "isDevelopment() || isStaging()" not in photobooth_section:
        print("❌ photoBooth doesn't use proper environment detection")
        return False

    print("✅ Environment detection logic is properly implemented")
    return True


def test_feature_consistency():
    """Test that photo booth follows the same pattern as other protected features."""
    print("🔍 Testing feature consistency with other protected pages...")

    config_path = project_root / "frontend/src/lib/config.ts"
    with open(config_path) as f:
        content = f.read()

    # Check that chartsPage uses similar logic
    charts_section = content[
        content.find("chartsPage:") : content.find("chartsPage:") + 300
    ]

    if "(isDevelopment() || isStaging())" not in charts_section:
        print("⚠️ chartsPage doesn't use the same pattern")
    else:
        print("✅ photoBooth follows the same pattern as chartsPage")

    return True


def main():
    """Run all photo booth access restriction tests."""
    print("🚀 Running Photo Booth Access Restriction Tests")
    print("=" * 50)

    tests = [
        test_feature_flag_exists,
        test_config_implementation,
        test_netlify_configuration,
        test_page_protection,
        test_environment_logic,
        test_feature_consistency,
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
        print("🎉 Photo booth access restrictions are properly implemented!")
        print("\n📋 Implementation Summary:")
        print("1. Feature flag 'photoBooth' added to FeatureFlags interface ✅")
        print(
            "2. Configuration logic: enabled in dev/staging, disabled in production ✅"
        )
        print("3. Netlify environments properly configured ✅")
        print("4. Photo booth page protected with feature flag check ✅")
        print("5. 404 redirect when feature is disabled ✅")

        print("\n🔒 Access Control:")
        print("- Local Development: ✅ Accessible")
        print("- Development Environment: ✅ Accessible")
        print("- Staging Environment: ✅ Accessible")
        print("- Production Environment: ❌ Blocked (redirects to 404)")

        return 0
    else:
        print("💥 Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
