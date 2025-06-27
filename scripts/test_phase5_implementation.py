#!/usr/bin/env python3
"""
Comprehensive test suite for Phase 5: Integration and Production Readiness.

This module validates the complete Plotly migration system including JSON schemas,
frontend configuration export, production optimization, feature flags, and
comprehensive regression testing.
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

from scripts.utils.json_schema_generator import create_json_schema_generator
from scripts.utils.frontend_config_exporter import create_frontend_config_exporter
from scripts.utils.production_optimizer import create_production_optimizer
from scripts.utils.feature_flags import FeatureFlagManager, FeatureState
from scripts.utils.chart_generator_factory import ChartGeneratorFactory
from scripts.utils.theme_manager import create_theme_manager
from scripts.utils.scalability_manager import create_scalability_manager
from scripts.test_phase4_implementation import create_test_monthly_data, create_test_quality_data
from scripts.test_phase3_implementation import create_test_trade_data
from scripts.utils.dashboard_parser import MonthlyPerformance, QualityDistribution


class Phase5TestSuite:
    """Comprehensive test suite for Phase 5 implementation."""
    
    def __init__(self):
        """Initialize test suite."""
        self.theme_manager = create_theme_manager()
        
        # Create scalability config
        scalability_config = {
            'scalability': {
                'trade_volume_thresholds': {'small': 50, 'medium': 100, 'large': 200}
            }
        }
        self.scalability_manager = create_scalability_manager(scalability_config)
        
        # Create components
        self.schema_generator = create_json_schema_generator(self.theme_manager)
        self.config_exporter = create_frontend_config_exporter(self.theme_manager)
        self.production_optimizer = create_production_optimizer(self.theme_manager)
        self.feature_flag_manager = FeatureFlagManager()
        
        # Create chart generators
        self.plotly_generator = ChartGeneratorFactory.create_chart_generator(
            "plotly", self.theme_manager, self.scalability_manager
        )
        self.matplotlib_generator = ChartGeneratorFactory.create_chart_generator(
            "matplotlib", self.theme_manager, self.scalability_manager
        )
        
        print("✅ Phase 5 test suite initialized")

    def test_json_schema_system(self) -> Dict[str, Any]:
        """Test comprehensive JSON schema system."""
        print("\n🔄 Testing JSON schema system...")
        
        results = {}
        
        try:
            # Test schema generation
            all_schemas = self.schema_generator.get_all_schemas()
            
            # Validate required schemas exist
            required_schemas = [
                'MonthlyPerformance', 'QualityDistribution', 'TradeData',
                'EnhancedMonthlyBars', 'EnhancedDonutChart', 
                'WaterfallChart', 'EnhancedScatter',
                'DashboardLayout', 'ThemeConfiguration', 'ExportConfiguration'
            ]
            
            missing_schemas = [name for name in required_schemas if name not in all_schemas]
            assert len(missing_schemas) == 0, f"Missing schemas: {missing_schemas}"
            
            # Test schema export
            exported_files = self.schema_generator.export_schemas("data/outputs/test_schemas")
            assert len(exported_files) == len(all_schemas), "Schema export count mismatch"
            
            # Validate exported files exist
            for schema_name, filepath in exported_files.items():
                assert Path(filepath).exists(), f"Schema file not found: {filepath}"
                
                # Validate JSON format
                with open(filepath, 'r') as f:
                    schema_content = json.load(f)
                    assert "$schema" in schema_content, f"Invalid JSON schema: {schema_name}"
            
            # Test example configuration generation
            examples = self.schema_generator.generate_example_configs()
            assert len(examples) >= 4, "Insufficient example configurations"
            
            # Test configuration validation
            for chart_type, example_config in examples.items():
                is_valid, errors = self.schema_generator.validate_chart_config(example_config, chart_type)
                if not is_valid:
                    print(f"Warning: Example config validation failed for {chart_type}: {errors}")
            
            results["json_schema_system"] = {
                "status": "✅ PASS",
                "schemas_generated": len(all_schemas),
                "files_exported": len(exported_files),
                "examples_created": len(examples),
                "all_schemas": list(all_schemas.keys())
            }
            
            print(f"  ✅ JSON Schema System: {len(all_schemas)} schemas, {len(exported_files)} files exported")
            
        except Exception as e:
            results["json_schema_system"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ JSON schema system test failed: {str(e)}")
        
        return results

    def test_frontend_config_export(self) -> Dict[str, Any]:
        """Test frontend configuration export system."""
        print("\n🔄 Testing frontend configuration export...")
        
        results = {}
        
        try:
            # Test chart configuration export
            monthly_data = create_test_monthly_data()
            quality_data = create_test_quality_data()
            trade_data = create_test_trade_data("medium")
            
            chart_configs = {}
            
            # Test monthly bars export
            monthly_config = self.config_exporter.export_chart_config(
                chart_type="enhanced_monthly_bars",
                data=monthly_data,
                theme_mode="light"
            )
            chart_configs["monthly_bars"] = monthly_config
            
            # Test donut chart export
            donut_config = self.config_exporter.export_chart_config(
                chart_type="enhanced_donut_chart",
                data=quality_data,
                theme_mode="light"
            )
            chart_configs["donut_chart"] = donut_config
            
            # Test waterfall chart export
            waterfall_config = self.config_exporter.export_chart_config(
                chart_type="waterfall_chart",
                data=trade_data[:20],
                theme_mode="light"
            )
            chart_configs["waterfall"] = waterfall_config
            
            # Test scatter chart export
            scatter_config = self.config_exporter.export_chart_config(
                chart_type="enhanced_scatter",
                data=trade_data,
                theme_mode="light"
            )
            chart_configs["scatter"] = scatter_config
            
            # Validate configurations
            config_validations = {}
            for name, config in chart_configs.items():
                # Check required fields
                required_fields = ["chart_type", "data", "theme", "layout", "styling", "export", "metadata"]
                missing_fields = [field for field in required_fields if field not in config]
                
                # Validate with schema
                is_valid, errors = self.config_exporter.validate_config(config)
                
                config_validations[name] = {
                    "required_fields_present": len(missing_fields) == 0,
                    "schema_valid": is_valid,
                    "errors": errors if not is_valid else []
                }
            
            # Test batch export
            exported_files = self.config_exporter.batch_export_configs(
                chart_configs, "data/outputs/test_frontend_configs"
            )
            
            # Validate exported files
            for name, filepath in exported_files.items():
                assert Path(filepath).exists(), f"Config file not found: {filepath}"
                
                # Validate JSON format
                with open(filepath, 'r') as f:
                    config_content = json.load(f)
                    assert "chart_type" in config_content, f"Invalid config file: {name}"
            
            # Test React component props generation
            react_props = {}
            for name, config in chart_configs.items():
                props = self.config_exporter.generate_react_component_props(config)
                react_props[name] = props
                
                # Validate props structure
                required_props = ["chartType", "data", "theme", "layout", "styling"]
                missing_props = [prop for prop in required_props if prop not in props]
                assert len(missing_props) == 0, f"Missing React props for {name}: {missing_props}"
            
            # Test dashboard configuration export
            dashboard_config = self.config_exporter.export_dashboard_config(
                charts=list(chart_configs.values()),
                theme_mode="light"
            )
            
            assert "dashboard_type" in dashboard_config, "Invalid dashboard configuration"
            assert "charts" in dashboard_config, "Missing charts in dashboard config"
            assert len(dashboard_config["charts"]) == len(chart_configs), "Chart count mismatch"
            
            results["frontend_config_export"] = {
                "status": "✅ PASS",
                "chart_configs_exported": len(chart_configs),
                "files_exported": len(exported_files),
                "react_props_generated": len(react_props),
                "dashboard_config_created": True,
                "config_validations": config_validations
            }
            
            print(f"  ✅ Frontend Config Export: {len(chart_configs)} configs, {len(exported_files)} files")
            
        except Exception as e:
            results["frontend_config_export"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Frontend config export test failed: {str(e)}")
        
        return results

    def test_production_optimization(self) -> Dict[str, Any]:
        """Test production optimization system."""
        print("\n🔄 Testing production optimization...")
        
        results = {}
        
        try:
            # Test performance optimizer initialization
            assert self.production_optimizer is not None, "Production optimizer not initialized"
            
            # Test template caching
            self.production_optimizer.template_cache.set_template("test", "light", "template_obj")
            cached_template = self.production_optimizer.template_cache.get_template("test", "light")
            assert cached_template is not None, "Template caching failed"
            
            # Test data sampling
            large_dataset = list(range(1000))
            sampled_data = self.production_optimizer.data_sampler.sample_data(
                large_dataset, target_size=100, strategy="intelligent"
            )
            assert len(sampled_data) == 100, "Data sampling failed"
            assert len(set(sampled_data)) == 100, "Data sampling not unique"
            
            # Test chart generation optimization (mock)
            def mock_chart_generator(data, **kwargs):
                # Simulate chart generation
                time.sleep(0.01)  # Small delay
                return f"chart_with_{len(data)}_points"
            
            # Test optimization with small dataset
            small_data = create_test_monthly_data()
            result, metrics = self.production_optimizer.optimize_chart_generation(
                chart_generator_func=mock_chart_generator,
                chart_type="monthly_bars",
                data=small_data
            )
            
            assert result is not None, "Chart generation optimization failed"
            assert metrics.chart_type == "monthly_bars", "Metrics chart type incorrect"
            assert metrics.data_size == len(small_data), "Metrics data size incorrect"
            
            # Test batch processing
            chart_requests = [
                {
                    "chart_generator_func": mock_chart_generator,
                    "chart_type": "monthly_bars",
                    "data": small_data
                },
                {
                    "chart_generator_func": mock_chart_generator,
                    "chart_type": "donut",
                    "data": create_test_quality_data()
                }
            ]
            
            batch_results = self.production_optimizer.batch_optimize_charts(chart_requests)
            assert len(batch_results) == 2, "Batch processing failed"
            
            # Test performance reporting
            performance_report = self.production_optimizer.get_performance_report()
            assert "summary" in performance_report, "Performance report missing summary"
            assert "total_charts_generated" in performance_report["summary"], "Performance metrics incomplete"
            
            # Test export optimization
            export_config = self.production_optimizer.optimize_export_settings(
                format="png", quality_level="balanced"
            )
            assert "width" in export_config, "Export optimization failed"
            assert export_config["scale"] == 2, "Export scale incorrect"
            
            results["production_optimization"] = {
                "status": "✅ PASS",
                "template_caching": True,
                "data_sampling": True,
                "chart_optimization": True,
                "batch_processing": True,
                "performance_reporting": True,
                "export_optimization": True,
                "charts_processed": len(self.production_optimizer.metrics_history)
            }
            
            print(f"  ✅ Production Optimization: All systems functional")
            
        except Exception as e:
            results["production_optimization"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Production optimization test failed: {str(e)}")
        
        return results

    def test_feature_flag_system(self) -> Dict[str, Any]:
        """Test feature flag system."""
        print("\n🔄 Testing feature flag system...")
        
        results = {}
        
        try:
            # Test basic flag functionality
            enabled_features = self.feature_flag_manager.get_enabled_features()
            assert len(enabled_features) > 0, "No features enabled"
            
            # Test specific flags
            critical_flags = [
                "plotly_enabled",
                "plotly_monthly_bars",
                "plotly_themes",
                "production_optimization"
            ]
            
            flag_statuses = {}
            for flag in critical_flags:
                enabled = self.feature_flag_manager.is_enabled(flag)
                flag_statuses[flag] = enabled
                
                # These should be enabled for production readiness
                if flag != "experimental_features":
                    assert enabled, f"Critical flag {flag} not enabled"
            
            # Test flag configuration
            test_flag = "test_phase5_flag"
            self.feature_flag_manager.set_flag(
                test_flag,
                FeatureState.ENABLED,
                rollout_percentage=75.0,
                description="Test flag for Phase 5"
            )
            
            # Test rollout percentage
            enabled_count = 0
            total_tests = 100
            for i in range(total_tests):
                context = {"user_id": f"test_user_{i}"}
                if self.feature_flag_manager.is_enabled(test_flag, context):
                    enabled_count += 1
            
            rollout_percentage = (enabled_count / total_tests) * 100
            assert 65 <= rollout_percentage <= 85, f"Rollout percentage off: {rollout_percentage}%"
            
            # Test conditional flags
            self.feature_flag_manager.set_flag(
                "conditional_test",
                FeatureState.ENABLED,
                conditions={"environment": "production"}
            )
            
            prod_context = {"environment": "production"}
            dev_context = {"environment": "development"}
            
            assert self.feature_flag_manager.is_enabled("conditional_test", prod_context), "Conditional flag failed"
            assert not self.feature_flag_manager.is_enabled("conditional_test", dev_context), "Conditional flag leaked"
            
            # Test flag listing
            all_flags = self.feature_flag_manager.list_flags()
            enabled_flags = self.feature_flag_manager.list_flags(FeatureState.ENABLED)
            
            assert len(all_flags) >= len(enabled_flags), "Flag listing inconsistent"
            
            # Test cache functionality
            self.feature_flag_manager.clear_cache()
            cache_size_before = len(self.feature_flag_manager.evaluation_cache)
            
            # Trigger some evaluations
            for flag in critical_flags[:3]:
                self.feature_flag_manager.is_enabled(flag)
            
            cache_size_after = len(self.feature_flag_manager.evaluation_cache)
            assert cache_size_after > cache_size_before, "Cache not working"
            
            results["feature_flag_system"] = {
                "status": "✅ PASS",
                "enabled_features": len(enabled_features),
                "critical_flags_enabled": all(flag_statuses.values()),
                "rollout_percentage_test": f"{rollout_percentage:.1f}%",
                "conditional_flags": True,
                "cache_functionality": True,
                "total_flags": len(all_flags)
            }
            
            print(f"  ✅ Feature Flag System: {len(enabled_features)} enabled, rollout {rollout_percentage:.1f}%")
            
        except Exception as e:
            results["feature_flag_system"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Feature flag system test failed: {str(e)}")
        
        return results

    def test_comprehensive_regression(self) -> Dict[str, Any]:
        """Test comprehensive regression across all phases."""
        print("\n🔄 Testing comprehensive regression...")
        
        results = {}
        
        try:
            # Test all chart types end-to-end
            chart_tests = {}
            
            # Test data
            monthly_data = create_test_monthly_data()
            quality_data = create_test_quality_data()
            trade_data = create_test_trade_data("medium")
            
            # Test monthly bars (Phase 2)
            try:
                fig = go.Figure()
                monthly_result = self.plotly_generator.create_enhanced_monthly_bars(fig, monthly_data, "light")
                chart_tests["monthly_bars"] = {
                    "generation_successful": monthly_result is not None,
                    "trace_count": len(monthly_result.data) if monthly_result else 0
                }
            except Exception as e:
                chart_tests["monthly_bars"] = {"generation_successful": False, "error": str(e)}
            
            # Test donut chart (Phase 2)
            try:
                fig = go.Figure()
                donut_result = self.plotly_generator.create_enhanced_donut_chart(fig, quality_data, "light")
                chart_tests["donut_chart"] = {
                    "generation_successful": donut_result is not None,
                    "trace_count": len(donut_result.data) if donut_result else 0
                }
            except Exception as e:
                chart_tests["donut_chart"] = {"generation_successful": False, "error": str(e)}
            
            # Test waterfall chart (Phase 3)
            try:
                fig = go.Figure()
                waterfall_result = self.plotly_generator.create_waterfall_chart(fig, trade_data[:20], "light")
                chart_tests["waterfall_chart"] = {
                    "generation_successful": waterfall_result is not None,
                    "trace_count": len(waterfall_result.data) if waterfall_result else 0
                }
            except Exception as e:
                chart_tests["waterfall_chart"] = {"generation_successful": False, "error": str(e)}
            
            # Test scatter plot (Phase 3)
            try:
                fig = go.Figure()
                scatter_result = self.plotly_generator.create_enhanced_scatter(fig, trade_data, "light")
                chart_tests["scatter_plot"] = {
                    "generation_successful": scatter_result is not None,
                    "trace_count": len(scatter_result.data) if scatter_result else 0
                }
            except Exception as e:
                chart_tests["scatter_plot"] = {"generation_successful": False, "error": str(e)}
            
            # Test theme system (Phase 4)
            theme_tests = {}
            for mode in ["light", "dark"]:
                try:
                    colors = self.theme_manager.get_theme_colors(mode)
                    theme_tests[f"{mode}_mode"] = {
                        "colors_available": hasattr(colors, 'primary_data'),
                        "background_set": hasattr(colors, 'background')
                    }
                except Exception as e:
                    theme_tests[f"{mode}_mode"] = {"error": str(e)}
            
            # Test export system (Phase 4)
            export_tests = {}
            try:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 4, 2]))
                
                # Test PNG export configuration
                export_config = self.plotly_generator.configure_export_settings(
                    format="png", scale=2.0
                )
                export_tests["export_config"] = {
                    "config_generated": bool(export_config),
                    "scale_correct": export_config.get("scale") == 2.0
                }
            except Exception as e:
                export_tests["export_config"] = {"error": str(e)}
            
            # Test integration with feature flags
            integration_tests = {}
            for chart_type in ["monthly_bars", "donut_charts", "waterfall", "scatter"]:
                flag_name = f"plotly_{chart_type}"
                integration_tests[chart_type] = {
                    "flag_enabled": self.feature_flag_manager.is_enabled(flag_name),
                    "flag_exists": self.feature_flag_manager.get_flag(flag_name) is not None
                }
            
            # Calculate success rates
            chart_success_rate = sum(1 for test in chart_tests.values() 
                                   if test.get("generation_successful", False)) / len(chart_tests)
            
            theme_success_rate = sum(1 for test in theme_tests.values() 
                                   if "error" not in test) / len(theme_tests)
            
            export_success_rate = sum(1 for test in export_tests.values() 
                                    if "error" not in test) / len(export_tests)
            
            integration_success_rate = sum(1 for test in integration_tests.values() 
                                         if test.get("flag_enabled", False)) / len(integration_tests)
            
            overall_success_rate = (chart_success_rate + theme_success_rate + 
                                  export_success_rate + integration_success_rate) / 4
            
            results["comprehensive_regression"] = {
                "status": "✅ PASS" if overall_success_rate >= 0.9 else "⚠️ PARTIAL",
                "chart_tests": chart_tests,
                "theme_tests": theme_tests,
                "export_tests": export_tests,
                "integration_tests": integration_tests,
                "success_rates": {
                    "chart_generation": f"{chart_success_rate * 100:.1f}%",
                    "theme_system": f"{theme_success_rate * 100:.1f}%",
                    "export_system": f"{export_success_rate * 100:.1f}%",
                    "integration": f"{integration_success_rate * 100:.1f}%",
                    "overall": f"{overall_success_rate * 100:.1f}%"
                }
            }
            
            print(f"  ✅ Comprehensive Regression: {overall_success_rate * 100:.1f}% success rate")
            
        except Exception as e:
            results["comprehensive_regression"] = {
                "status": f"❌ FAIL: {str(e)}"
            }
            print(f"  ❌ Comprehensive regression test failed: {str(e)}")
        
        return results

    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all Phase 5 tests and generate comprehensive report."""
        print("🚀 Starting Phase 5 Comprehensive Test Suite")
        print("=" * 60)
        
        start_time = time.time()
        all_results = {}
        
        # Run all test categories
        test_methods = [
            ("JSON Schema System", self.test_json_schema_system),
            ("Frontend Config Export", self.test_frontend_config_export),
            ("Production Optimization", self.test_production_optimization),
            ("Feature Flag System", self.test_feature_flag_system),
            ("Comprehensive Regression", self.test_comprehensive_regression)
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
        print("📊 PHASE 5 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        
        for category, results in all_results.items():
            if isinstance(results, dict) and "error" not in results:
                for test_name, test_result in results.items():
                    if isinstance(test_result, dict):
                        total_tests += 1
                        if test_result.get("status", "").startswith("✅"):
                            passed_tests += 1
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📈 Pass Rate: {passed_tests}/{total_tests} ({pass_rate:.1f}%)")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")
        print(f"🎯 Status: {'✅ PHASE 5 COMPLETE' if pass_rate >= 90 else '❌ NEEDS ATTENTION'}")
        
        # Save detailed results
        results_path = Path("data/outputs/phase5_tests/test_results.json")
        results_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "pass_rate": pass_rate,
            "total_time": total_time,
            "status": "COMPLETE" if pass_rate >= 90 else "NEEDS_ATTENTION",
            "detailed_results": all_results
        }
        
        with open(results_path, 'w') as f:
            json.dump(summary_results, f, indent=2, default=str)
        
        print(f"📄 Detailed results saved to: {results_path}")
        
        # Cleanup test resources
        self.production_optimizer.cleanup_resources()
        
        return summary_results


def main():
    """Run Phase 5 test suite."""
    try:
        test_suite = Phase5TestSuite()
        results = test_suite.run_comprehensive_tests()
        
        # Exit with appropriate code
        if results["pass_rate"] >= 90:
            print("\n🎉 Phase 5 implementation successful!")
            print("🚀 Plotly migration is production ready!")
            return 0
        else:
            print("\n⚠️  Phase 5 implementation needs attention!")
            return 1
            
    except Exception as e:
        print(f"\n💥 Phase 5 test suite failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())