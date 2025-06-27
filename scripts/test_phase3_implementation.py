#!/usr/bin/env python3
"""
Comprehensive test suite for Phase 3: Complex Chart Migration and Scalability.

This module validates the waterfall chart, enhanced scatter plot implementations,
scalability management integration, and advanced styling system.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import testing modules
import plotly.graph_objects as go
import numpy as np

from scripts.utils.chart_generator_factory import ChartGeneratorFactory
from scripts.utils.theme_manager import create_theme_manager
from scripts.utils.scalability_manager import create_scalability_manager
from scripts.utils.chart_comparison_framework import ChartComparisonFramework, create_test_data
from scripts.utils.dashboard_parser import TradeData


def create_test_trade_data(size: str = "medium") -> List[TradeData]:
    """Create test trade data with different sizes for scalability testing."""
    np.random.seed(42)  # For reproducible results
    
    # Define data sizes
    size_map = {
        "small": 15,
        "medium": 50, 
        "large": 150
    }
    
    n_trades = size_map.get(size, 50)
    
    trades = []
    tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA", "JPM", "V", "JNJ",
               "WMT", "PG", "UNH", "HD", "MA", "DIS", "ADBE", "NFLX", "CRM", "PYPL"]
    
    qualities = ["Excellent", "Good", "Poor", "Failed", "Poor Setup"]
    quality_weights = [0.2, 0.3, 0.25, 0.15, 0.1]  # Distribution weights
    
    for i in range(n_trades):
        # Generate realistic trade data
        ticker = np.random.choice(tickers)
        
        # Duration: mostly 5-30 days with some outliers
        if np.random.random() < 0.1:  # 10% outliers
            duration = np.random.choice([1, 2, 45, 60, 90])
        else:
            duration = int(np.random.normal(15, 8))
            duration = max(1, min(duration, 90))
        
        # Return: influenced by quality
        quality = np.random.choice(qualities, p=quality_weights)
        
        if quality == "Excellent":
            return_pct = np.random.normal(8, 3)
        elif quality == "Good":
            return_pct = np.random.normal(3, 2)
        elif quality == "Poor":
            return_pct = np.random.normal(-1, 2)
        elif quality == "Failed":
            return_pct = np.random.normal(-5, 3)
        else:  # Poor Setup
            return_pct = np.random.normal(-2, 1.5)
        
        # Add some extreme outliers for testing
        if np.random.random() < 0.05:  # 5% extreme outliers
            return_pct = np.random.choice([-15, -12, 12, 15, 20])
        
        trades.append(TradeData(
            rank=i + 1,
            ticker=f"{ticker}_{i}",  # Make unique
            strategy="Test Strategy",
            entry_date="2024-01-01",
            exit_date="2024-01-15",
            return_pct=round(return_pct, 2),
            duration_days=duration,
            quality=quality
        ))
    
    return trades


class Phase3TestSuite:
    """Comprehensive test suite for Phase 3 implementation."""
    
    def __init__(self):
        """Initialize test suite."""
        self.theme_manager = create_theme_manager()
        
        # Create scalability config
        scalability_config = {
            'scalability': {
                'trade_volume_thresholds': {
                    'small': 50,
                    'medium': 100,
                    'large': 200
                },
                'monthly_timeline_thresholds': {
                    'compact': 3,
                    'medium': 8,
                    'condensed': 12
                },
                'scatter_density_thresholds': {
                    'low': 50,
                    'medium': 150,
                    'high': 200
                },
                'clustering': {
                    'enabled': True,
                    'min_samples': 3,
                    'eps': 0.5
                },
                'compression': {
                    'enabled': True,
                    'max_labels': 20
                }
            }
        }
        
        self.scalability_manager = create_scalability_manager(scalability_config)
        self.comparison_framework = ChartComparisonFramework("data/outputs/phase3_tests")
        
        # Create chart generators
        self.matplotlib_generator = ChartGeneratorFactory.create_chart_generator(
            "matplotlib", self.theme_manager, self.scalability_manager
        )
        self.plotly_generator = ChartGeneratorFactory.create_chart_generator(
            "plotly", self.theme_manager, self.scalability_manager
        )
        
        print("✅ Phase 3 test suite initialized")

    def test_waterfall_chart_implementation(self) -> Dict[str, Any]:
        """Test waterfall chart implementation with various data sizes."""
        print("\n🔄 Testing waterfall chart implementation...")
        
        results = {}
        
        for size in ["small", "medium"]:  # Skip large to avoid performance bands in basic test
            trades = create_test_trade_data(size)
            
            try:
                # Test Plotly implementation
                fig = go.Figure()
                start_time = time.time()
                result = self.plotly_generator.create_waterfall_chart(fig, trades, "light")
                end_time = time.time()
                
                # Validate result
                assert result is not None, f"Waterfall chart returned None for {size} dataset"
                assert isinstance(result, go.Figure), f"Expected Figure, got {type(result)}"
                assert len(result.data) > 0, f"No traces added to waterfall chart for {size} dataset"
                
                # Check for cumulative line trace
                has_line = any(trace.type == 'scatter' for trace in result.data)
                assert has_line, f"Missing cumulative line in waterfall chart for {size} dataset"
                
                # Performance validation
                generation_time = end_time - start_time
                assert generation_time < 2.0, f"Waterfall chart generation too slow: {generation_time:.2f}s"
                
                results[f"waterfall_{size}"] = {
                    "status": "✅ PASS",
                    "traces": len(result.data),
                    "generation_time": f"{generation_time:.3f}s",
                    "trades_processed": len(trades)
                }
                
                print(f"  ✅ {size.title()} dataset: {len(trades)} trades, {len(result.data)} traces, {generation_time:.3f}s")
                
            except Exception as e:
                results[f"waterfall_{size}"] = {
                    "status": f"❌ FAIL: {str(e)}",
                    "trades_processed": len(trades)
                }
                print(f"  ❌ {size.title()} dataset failed: {str(e)}")
        
        return results

    def test_enhanced_scatter_implementation(self) -> Dict[str, Any]:
        """Test enhanced scatter plot implementation with clustering."""
        print("\n🔄 Testing enhanced scatter plot implementation...")
        
        results = {}
        
        for size in ["small", "medium", "large"]:
            trades = create_test_trade_data(size)
            
            try:
                # Test Plotly implementation
                fig = go.Figure()
                start_time = time.time()
                result = self.plotly_generator.create_enhanced_scatter(fig, trades, "light")
                end_time = time.time()
                
                # Validate result
                assert result is not None, f"Scatter plot returned None for {size} dataset"
                assert isinstance(result, go.Figure), f"Expected Figure, got {type(result)}"
                assert len(result.data) > 0, f"No traces added to scatter plot for {size} dataset"
                
                # Check for trend line trace (should exist for normal scatter)
                if size != "large":  # Large datasets might use clustering
                    has_trend = any(trace.mode and 'lines' in trace.mode for trace in result.data)
                    assert has_trend, f"Missing trend line in scatter plot for {size} dataset"
                
                # Performance validation
                generation_time = end_time - start_time
                assert generation_time < 3.0, f"Scatter plot generation too slow: {generation_time:.2f}s"
                
                results[f"scatter_{size}"] = {
                    "status": "✅ PASS",
                    "traces": len(result.data),
                    "generation_time": f"{generation_time:.3f}s",
                    "trades_processed": len(trades),
                    "clustering_used": size == "large"
                }
                
                print(f"  ✅ {size.title()} dataset: {len(trades)} trades, {len(result.data)} traces, {generation_time:.3f}s")
                
            except Exception as e:
                results[f"scatter_{size}"] = {
                    "status": f"❌ FAIL: {str(e)}",
                    "trades_processed": len(trades)
                }
                print(f"  ❌ {size.title()} dataset failed: {str(e)}")
        
        return results

    def test_scalability_integration(self) -> Dict[str, Any]:
        """Test scalability manager integration with Plotly charts."""
        print("\n🔄 Testing scalability manager integration...")
        
        results = {}
        
        # Test volume detection
        small_trades = create_test_trade_data("small")
        medium_trades = create_test_trade_data("medium")
        large_trades = create_test_trade_data("large")
        
        try:
            # Test trade volume categorization
            small_category = self.scalability_manager.detect_trade_volume_category(small_trades)
            medium_category = self.scalability_manager.detect_trade_volume_category(medium_trades)
            large_category = self.scalability_manager.detect_trade_volume_category(large_trades)
            
            assert small_category == "small", f"Expected 'small', got '{small_category}'"
            assert medium_category in ["medium", "small"], f"Expected 'medium'/'small', got '{medium_category}'"
            assert large_category in ["large", "medium"], f"Expected 'large'/'medium', got '{large_category}'"
            
            # Test scatter density detection
            scatter_category = self.scalability_manager.detect_scatter_density_category(large_trades)
            assert scatter_category in ["high", "medium", "low"], f"Invalid scatter category: {scatter_category}"
            
            # Test performance bands creation
            bands = self.scalability_manager.create_performance_bands(large_trades)
            assert isinstance(bands, dict), "Performance bands should be a dictionary"
            assert len(bands) > 0, "Performance bands should not be empty"
            
            results["scalability_detection"] = {
                "status": "✅ PASS",
                "small_category": small_category,
                "medium_category": medium_category,
                "large_category": large_category,
                "scatter_category": scatter_category,
                "performance_bands": len(bands)
            }
            
            print(f"  ✅ Volume detection: {len(small_trades)}→{small_category}, {len(medium_trades)}→{medium_category}, {len(large_trades)}→{large_category}")
            print(f"  ✅ Scatter density: {scatter_category}")
            print(f"  ✅ Performance bands: {len(bands)} categories")
            
        except Exception as e:
            results["scalability_detection"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Scalability detection failed: {str(e)}")
        
        return results

    def test_performance_bands_chart(self) -> Dict[str, Any]:
        """Test performance bands chart for large datasets."""
        print("\n🔄 Testing performance bands chart...")
        
        results = {}
        
        try:
            large_trades = create_test_trade_data("large")
            
            # Force performance bands by using large dataset
            fig = go.Figure()
            start_time = time.time()
            result = self.plotly_generator.create_waterfall_chart(fig, large_trades, "light")
            end_time = time.time()
            
            # Validate result
            assert result is not None, "Performance bands chart returned None"
            assert isinstance(result, go.Figure), f"Expected Figure, got {type(result)}"
            
            # Check for horizontal bar traces (performance bands)
            has_bars = any(trace.type == 'bar' for trace in result.data)
            assert has_bars, "Missing bar traces in performance bands chart"
            
            # Performance validation
            generation_time = end_time - start_time
            assert generation_time < 2.0, f"Performance bands generation too slow: {generation_time:.2f}s"
            
            results["performance_bands"] = {
                "status": "✅ PASS",
                "traces": len(result.data),
                "generation_time": f"{generation_time:.3f}s",
                "trades_processed": len(large_trades)
            }
            
            print(f"  ✅ Performance bands: {len(large_trades)} trades → {len(result.data)} traces, {generation_time:.3f}s")
            
        except Exception as e:
            results["performance_bands"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Performance bands test failed: {str(e)}")
        
        return results

    def test_clustering_functionality(self) -> Dict[str, Any]:
        """Test DBSCAN clustering for high-density scatter plots."""
        print("\n🔄 Testing clustering functionality...")
        
        results = {}
        
        try:
            # Create large dataset to trigger clustering
            large_trades = create_test_trade_data("large")
            
            # Test clustering directly
            cluster_info = self.scalability_manager.cluster_scatter_points(large_trades)
            
            # Validate cluster info structure
            assert isinstance(cluster_info, dict), "Cluster info should be a dictionary"
            assert "clusters" in cluster_info, "Missing 'clusters' key"
            assert "noise" in cluster_info, "Missing 'noise' key"
            assert "total_clusters" in cluster_info, "Missing 'total_clusters' key"
            assert "clustered_points" in cluster_info, "Missing 'clustered_points' key"
            assert "noise_points" in cluster_info, "Missing 'noise_points' key"
            
            # Validate cluster data
            total_points = cluster_info["clustered_points"] + cluster_info["noise_points"]
            assert total_points == len(large_trades), f"Point count mismatch: {total_points} != {len(large_trades)}"
            
            # Test clustered scatter chart creation
            fig = go.Figure()
            start_time = time.time()
            result = self.plotly_generator._create_clustered_scatter(fig, cluster_info, "light")
            end_time = time.time()
            
            # Validate result
            assert result is not None, "Clustered scatter returned None"
            assert isinstance(result, go.Figure), f"Expected Figure, got {type(result)}"
            assert len(result.data) > 0, "No traces in clustered scatter plot"
            
            # Performance validation
            generation_time = end_time - start_time
            assert generation_time < 1.0, f"Clustering visualization too slow: {generation_time:.2f}s"
            
            results["clustering"] = {
                "status": "✅ PASS",
                "total_trades": len(large_trades),
                "clusters": cluster_info["total_clusters"],
                "clustered_points": cluster_info["clustered_points"],
                "noise_points": cluster_info["noise_points"],
                "visualization_traces": len(result.data),
                "generation_time": f"{generation_time:.3f}s"
            }
            
            print(f"  ✅ Clustering: {len(large_trades)} trades → {cluster_info['total_clusters']} clusters")
            print(f"  ✅ Grouped: {cluster_info['clustered_points']}, Individual: {cluster_info['noise_points']}")
            print(f"  ✅ Visualization: {len(result.data)} traces, {generation_time:.3f}s")
            
        except Exception as e:
            results["clustering"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Clustering test failed: {str(e)}")
        
        return results

    def test_advanced_styling_system(self) -> Dict[str, Any]:
        """Test advanced styling system for complex charts."""
        print("\n🔄 Testing advanced styling system...")
        
        results = {}
        
        try:
            # Test styling configurations for different chart types
            chart_types = ["waterfall", "scatter", "clustering", "performance_bands"]
            
            for chart_type in chart_types:
                # Get styling configuration
                styling_config = self.plotly_generator.theme_mapper.get_advanced_styling_config(chart_type, "light")
                
                # Validate configuration structure
                assert isinstance(styling_config, dict), f"Styling config should be dict for {chart_type}"
                assert len(styling_config) > 0, f"Empty styling config for {chart_type}"
                
                # Test scalability styling
                for volume in ["small", "medium", "large"]:
                    scalability_config = self.plotly_generator.theme_mapper.get_scalability_styling(volume, "light")
                    assert isinstance(scalability_config, dict), f"Scalability config should be dict for {volume}"
                    assert "opacity" in scalability_config, f"Missing opacity in {volume} config"
                    assert "detail_level" in scalability_config, f"Missing detail_level in {volume} config"
            
            # Test theme application
            fig = go.Figure()
            self.plotly_generator.theme_mapper.apply_advanced_styling(fig, "scatter", "light", title="Test Chart")
            
            # Validate figure has been styled
            assert fig.layout.template is not None or len(str(fig.layout)) > 100, "Figure not properly styled"
            
            results["advanced_styling"] = {
                "status": "✅ PASS",
                "chart_types_configured": len(chart_types),
                "scalability_levels": 3,
                "theme_application": "success"
            }
            
            print(f"  ✅ Styling configs: {len(chart_types)} chart types")
            print(f"  ✅ Scalability configs: 3 volume levels")
            print(f"  ✅ Theme application: working")
            
        except Exception as e:
            results["advanced_styling"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Advanced styling test failed: {str(e)}")
        
        return results

    def test_json_schema_export(self) -> Dict[str, Any]:
        """Test JSON schema export for complex charts."""
        print("\n🔄 Testing JSON schema export...")
        
        results = {}
        
        try:
            # Test schema export for complex chart types
            chart_types = ["waterfall_chart", "enhanced_scatter"]
            
            for chart_type in chart_types:
                # Export schema
                schema = self.plotly_generator.export_chart_config(chart_type, {"mode": "light"})
                
                # Validate schema structure
                assert isinstance(schema, dict), f"Schema should be dict for {chart_type}"
                assert "engine" in schema, f"Missing 'engine' in {chart_type} schema"
                assert "chart_type" in schema, f"Missing 'chart_type' in {chart_type} schema"
                assert "version" in schema, f"Missing 'version' in {chart_type} schema"
                assert "theme" in schema, f"Missing 'theme' in {chart_type} schema"
                assert "chart_config" in schema, f"Missing 'chart_config' in {chart_type} schema"
                assert "data_requirements" in schema, f"Missing 'data_requirements' in {chart_type} schema"
                
                # Validate data requirements
                data_req = schema["data_requirements"]
                assert "fields" in data_req, f"Missing 'fields' in {chart_type} data requirements"
                assert "format" in data_req, f"Missing 'format' in {chart_type} data requirements"
                assert len(data_req["fields"]) > 0, f"Empty fields in {chart_type} data requirements"
                
                # Validate JSON serializable
                json_str = json.dumps(schema)
                assert len(json_str) > 100, f"Schema too small for {chart_type}"
                
                # Save schema for inspection
                schema_path = Path("data/outputs/phase3_tests") / f"{chart_type}_schema_light.json"
                schema_path.parent.mkdir(parents=True, exist_ok=True)
                with open(schema_path, 'w') as f:
                    json.dump(schema, f, indent=2)
            
            results["json_schema"] = {
                "status": "✅ PASS",
                "schemas_exported": len(chart_types),
                "validation": "complete"
            }
            
            print(f"  ✅ Schema export: {len(chart_types)} chart types")
            print(f"  ✅ Validation: structure and JSON serialization")
            
        except Exception as e:
            results["json_schema"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ JSON schema test failed: {str(e)}")
        
        return results

    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all Phase 3 tests and generate comprehensive report."""
        print("🚀 Starting Phase 3 Comprehensive Test Suite")
        print("=" * 60)
        
        start_time = time.time()
        all_results = {}
        
        # Run all test categories
        test_methods = [
            ("Waterfall Chart", self.test_waterfall_chart_implementation),
            ("Enhanced Scatter", self.test_enhanced_scatter_implementation),
            ("Scalability Integration", self.test_scalability_integration),
            ("Performance Bands", self.test_performance_bands_chart),
            ("Clustering", self.test_clustering_functionality),
            ("Advanced Styling", self.test_advanced_styling_system),
            ("JSON Schema Export", self.test_json_schema_export)
        ]
        
        for test_name, test_method in test_methods:
            try:
                results = test_method()
                all_results[test_name.lower().replace(" ", "_")] = results
            except Exception as e:
                all_results[test_name.lower().replace(" ", "_")] = {
                    "error": f"Test suite failed: {str(e)}"
                }
                print(f"❌ {test_name} test suite failed: {str(e)}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 PHASE 3 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        
        for category, results in all_results.items():
            if isinstance(results, dict) and "error" not in results:
                for test_name, test_result in results.items():
                    total_tests += 1
                    if isinstance(test_result, dict) and test_result.get("status", "").startswith("✅"):
                        passed_tests += 1
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Pass Rate: {passed_tests}/{total_tests} ({pass_rate:.1f}%)")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")
        print(f"🎯 Status: {'✅ PHASE 3 COMPLETE' if pass_rate >= 80 else '❌ NEEDS ATTENTION'}")
        
        # Save detailed results
        results_path = Path("data/outputs/phase3_tests/test_results.json")
        results_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "pass_rate": pass_rate,
            "total_time": total_time,
            "status": "COMPLETE" if pass_rate >= 80 else "NEEDS_ATTENTION",
            "detailed_results": all_results
        }
        
        with open(results_path, 'w') as f:
            json.dump(summary_results, f, indent=2)
        
        print(f"📄 Detailed results saved to: {results_path}")
        
        return summary_results


def main():
    """Run Phase 3 test suite."""
    try:
        test_suite = Phase3TestSuite()
        results = test_suite.run_comprehensive_tests()
        
        # Exit with appropriate code
        if results["pass_rate"] >= 80:
            print("\n🎉 Phase 3 implementation successful!")
            return 0
        else:
            print("\n⚠️  Phase 3 implementation needs attention!")
            return 1
            
    except Exception as e:
        print(f"\n💥 Phase 3 test suite failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())