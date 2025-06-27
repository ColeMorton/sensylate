#!/usr/bin/env python3
"""
Test script for Phase 1 implementation validation.

This script tests:
1. Abstract interface creation and compliance
2. Matplotlib wrapper functionality
3. Factory pattern implementation
4. Configuration-based engine selection
5. Backward compatibility
"""

import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.utils.abstract_chart_generator import AbstractChartGenerator
from scripts.utils.chart_generator_factory import ChartGeneratorFactory
from scripts.utils.config_loader import ConfigLoader
from scripts.utils.matplotlib_chart_generator import MatplotlibChartGenerator
from scripts.utils.plotly_chart_generator import PlotlyChartGenerator
from scripts.utils.scalability_manager import create_scalability_manager
from scripts.utils.theme_manager import create_theme_manager


def test_abstract_interface():
    """Test that abstract interface is properly defined."""
    print("✓ Testing abstract interface...")

    # Check that AbstractChartGenerator is abstract
    try:
        AbstractChartGenerator(None, None)
        print("  ✗ Abstract class should not be instantiable")
        return False
    except TypeError:
        print("  ✓ Abstract class correctly prevents instantiation")

    # Check required methods
    required_methods = [
        "create_enhanced_gauge",
        "create_enhanced_monthly_bars",
        "create_enhanced_donut_chart",
        "create_waterfall_chart",
        "create_enhanced_scatter",
        "create_performance_summary_panel",
    ]

    for method in required_methods:
        if hasattr(AbstractChartGenerator, method):
            print(f"  ✓ Method '{method}' defined in abstract interface")
        else:
            print(f"  ✗ Method '{method}' missing from abstract interface")
            return False

    return True


def test_matplotlib_wrapper():
    """Test that matplotlib wrapper implements interface correctly."""
    print("\n✓ Testing matplotlib wrapper...")

    # Create theme manager
    theme_manager = create_theme_manager()

    # Create matplotlib generator
    generator = MatplotlibChartGenerator(theme_manager)

    # Check inheritance
    if isinstance(generator, AbstractChartGenerator):
        print("  ✓ MatplotlibChartGenerator inherits from AbstractChartGenerator")
    else:
        print(
            "  ✗ MatplotlibChartGenerator does not inherit from AbstractChartGenerator"
        )
        return False

    # Check that legacy generator is created
    if hasattr(generator, "_legacy_generator"):
        print("  ✓ Legacy generator wrapped successfully")
    else:
        print("  ✗ Legacy generator not wrapped")
        return False

    return True


def test_plotly_stub():
    """Test that Plotly stub implements interface correctly."""
    print("\n✓ Testing Plotly stub...")

    # Create theme manager
    theme_manager = create_theme_manager()

    # Create Plotly generator
    generator = PlotlyChartGenerator(theme_manager)

    # Check inheritance
    if isinstance(generator, AbstractChartGenerator):
        print("  ✓ PlotlyChartGenerator inherits from AbstractChartGenerator")
    else:
        print("  ✗ PlotlyChartGenerator does not inherit from AbstractChartGenerator")
        return False

    # Check that methods raise NotImplementedError
    try:
        generator.create_enhanced_gauge(None, 50, "Test", 100, "light")
        print("  ✗ Stub methods should raise NotImplementedError")
        return False
    except NotImplementedError:
        print("  ✓ Stub methods correctly raise NotImplementedError")

    return True


def test_factory_pattern():
    """Test factory pattern implementation."""
    print("\n✓ Testing factory pattern...")

    theme_manager = create_theme_manager()

    # Test matplotlib creation
    matplotlib_gen = ChartGeneratorFactory.create_chart_generator(
        "matplotlib", theme_manager
    )
    if isinstance(matplotlib_gen, MatplotlibChartGenerator):
        print("  ✓ Factory creates matplotlib generator correctly")
    else:
        print("  ✗ Factory failed to create matplotlib generator")
        return False

    # Test plotly creation
    plotly_gen = ChartGeneratorFactory.create_chart_generator("plotly", theme_manager)
    if isinstance(plotly_gen, PlotlyChartGenerator):
        print("  ✓ Factory creates plotly generator correctly")
    else:
        print("  ✗ Factory failed to create plotly generator")
        return False

    # Test invalid engine
    try:
        ChartGeneratorFactory.create_chart_generator("invalid", theme_manager)
        print("  ✗ Factory should raise error for invalid engine")
        return False
    except ValueError:
        print("  ✓ Factory correctly raises error for invalid engine")

    return True


def test_configuration_integration():
    """Test configuration-based engine selection."""
    print("\n✓ Testing configuration integration...")

    # Load default config
    config_loader = ConfigLoader()
    config = config_loader.load_with_environment(
        "configs/dashboard_generation.yaml", "dev"
    )

    # Check chart engine config
    if "chart_engine" in config:
        print(f"  ✓ Chart engine configured: {config['chart_engine']}")
    else:
        print("  ✗ Chart engine not in configuration")
        return False

    # Test default engine
    default_engine = ChartGeneratorFactory.get_default_engine(config)
    if default_engine == "matplotlib":
        print("  ✓ Default engine is matplotlib (backward compatible)")
    else:
        print("  ✗ Default engine is not matplotlib")
        return False

    # Test with plotly config
    config["chart_engine"] = "plotly"
    plotly_engine = ChartGeneratorFactory.get_default_engine(config)
    if plotly_engine == "plotly":
        print("  ✓ Configuration override works correctly")
    else:
        print("  ✗ Configuration override failed")
        return False

    return True


def test_dashboard_generator_integration():
    """Test that DashboardGenerator uses the new factory."""
    print("\n✓ Testing DashboardGenerator integration...")

    # This would require actually running the dashboard generator
    # For now, we'll just check imports work
    try:
        from scripts.dashboard_generator import DashboardGenerator

        print("  ✓ DashboardGenerator imports successfully")

        # Check that it imports the factory
        import scripts.dashboard_generator

        if "ChartGeneratorFactory" in scripts.dashboard_generator.__dict__:
            print("  ✓ DashboardGenerator imports ChartGeneratorFactory")
        else:
            print("  ✗ DashboardGenerator does not import ChartGeneratorFactory")
            return False

    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False

    return True


def main():
    """Run all Phase 1 validation tests."""
    print("=" * 60)
    print("Phase 1 Implementation Validation")
    print("=" * 60)

    tests = [
        test_abstract_interface,
        test_matplotlib_wrapper,
        test_plotly_stub,
        test_factory_pattern,
        test_configuration_integration,
        test_dashboard_generator_integration,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✅ All Phase 1 implementation tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
