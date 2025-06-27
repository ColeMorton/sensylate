# Plotly Migration Guide and Best Practices

**Version**: 1.0.0  
**Date**: 2025-06-27  
**Author**: Claude Code Architecture Team  

## Table of Contents

1. [Migration Overview](#migration-overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Migration](#step-by-step-migration)
4. [Configuration Changes](#configuration-changes)
5. [Chart Type Migration](#chart-type-migration)
6. [Performance Optimization](#performance-optimization)
7. [Frontend Integration](#frontend-integration)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Rollback Procedures](#rollback-procedures)

## Migration Overview

This guide provides comprehensive instructions for migrating from the matplotlib-based chart generation system to the new Plotly-based system. The migration is designed to be incremental, maintaining backward compatibility while enabling new capabilities.

### Migration Benefits

- **Unified Chart Definitions**: Single JSON schema shared between Python backend and JavaScript frontend
- **Enhanced Interactivity**: Support for interactive dashboards and real-time data updates
- **Improved Performance**: Optimized rendering with WebGL support for large datasets
- **Better Export Quality**: High-DPI exports (300+ DPI) with multiple format support
- **Reduced Maintenance**: Template-based styling eliminates repetitive code

### Migration Strategy

- **Incremental Rollout**: Gradual migration by chart type with feature flags
- **Backward Compatibility**: Existing matplotlib code continues to work
- **Quality Assurance**: Extensive testing and visual validation
- **Risk Mitigation**: Easy rollback procedures at each step

## Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **Dependencies**: All requirements in `requirements.txt`
- **Memory**: Minimum 4GB RAM for chart generation
- **Storage**: 500MB for templates and cache

### Required Dependencies

```bash
# Core Plotly dependencies
pip install plotly==5.24.1
pip install kaleido==0.2.1

# Optional performance dependencies
pip install psutil  # For memory monitoring
pip install sklearn  # For clustering features
```

### Environment Setup

1. **Update Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```bash
   python -c "import plotly; print(f'Plotly {plotly.__version__} installed')"
   python -c "import kaleido; print('Kaleido available')"
   ```

3. **Test Configuration**:
   ```bash
   python scripts/test_phase1_implementation.py
   ```

## Step-by-Step Migration

### Phase 1: Enable Plotly Support

1. **Update Configuration**:
   ```yaml
   # configs/dashboard_generation.yaml
   chart_engine: "matplotlib"  # Keep matplotlib as default
   plotly_enabled: true        # Enable Plotly support
   ```

2. **Test Basic Functionality**:
   ```bash
   python scripts/dashboard_generator.py --config configs/dashboard_generation.yaml
   ```

3. **Verify Output**:
   - Confirm existing dashboards generate correctly
   - Check file sizes and quality match previous output

### Phase 2: Migrate Core Charts

1. **Enable Monthly Bars Migration**:
   ```yaml
   # configs/dashboard_generation.yaml
   chart_migrations:
     monthly_bars: "plotly"
     donut_chart: "matplotlib"  # Keep others on matplotlib
   ```

2. **Test Monthly Charts**:
   ```bash
   python scripts/test_phase2_implementation.py
   ```

3. **Visual Validation**:
   - Compare matplotlib vs Plotly outputs side-by-side
   - Verify 99%+ visual similarity
   - Check color accuracy and brand compliance

### Phase 3: Migrate Complex Charts

1. **Enable Advanced Charts**:
   ```yaml
   chart_migrations:
     monthly_bars: "plotly"
     donut_chart: "plotly"
     waterfall_chart: "plotly"
     scatter_plot: "plotly"
   ```

2. **Test Complex Features**:
   ```bash
   python scripts/test_phase3_implementation.py
   ```

3. **Validate Scalability**:
   - Test with datasets of varying sizes (10, 100, 1000+ trades)
   - Verify clustering and performance bands work correctly
   - Check memory usage remains within acceptable limits

### Phase 4: Complete Migration

1. **Full Plotly Migration**:
   ```yaml
   chart_engine: "plotly"
   chart_migrations: {}  # Use Plotly for all charts
   ```

2. **Test Complete System**:
   ```bash
   python scripts/test_phase4_implementation.py
   ```

3. **Production Validation**:
   - Generate full dashboard suite
   - Test all export formats (PNG, PDF, SVG, HTML)
   - Verify font rendering and theme consistency

## Configuration Changes

### Dashboard Generation Configuration

```yaml
# configs/dashboard_generation.yaml

# Chart Engine Selection
chart_engine: "plotly"  # "matplotlib" or "plotly"

# Theme Configuration
theme:
  mode: "light"  # "light" or "dark"
  template: "sensylate_light"  # Plotly template name
  high_dpi: true  # Enable high-DPI templates

# Layout Configuration
layout:
  figure_size: [16, 12]  # Figure dimensions in inches
  grid:
    rows: 3
    cols: 2
    height_ratios: [0.2, 0.4, 0.4]
  spacing:
    horizontal: 0.15
    vertical: 0.1

# Performance Configuration
performance:
  enable_caching: true
  sample_large_datasets: true
  use_webgl: true  # For large scatter plots
  max_workers: 4   # Parallel processing threads

# Export Configuration
export:
  formats: ["png", "pdf", "svg"]
  quality:
    scale: 3  # 3x scale = ~300 DPI
    width: 1600
    height: 1200
```

### Feature Flags Configuration

```yaml
# Feature flags for gradual rollout
feature_flags:
  plotly_monthly_bars: true
  plotly_donut_charts: true
  plotly_waterfall: true
  plotly_scatter: true
  plotly_layout_manager: true
  plotly_themes: true
  frontend_export: true
```

## Chart Type Migration

### Monthly Bars Chart

**Before (matplotlib)**:
```python
from scripts.utils.matplotlib_chart_generator import MatplotlibChartGenerator

generator = MatplotlibChartGenerator(theme_manager)
generator.create_enhanced_monthly_bars(ax, monthly_data, mode="light")
```

**After (Plotly)**:
```python
from scripts.utils.plotly_chart_generator import PlotlyChartGenerator

generator = PlotlyChartGenerator(theme_manager)
fig = generator.create_enhanced_monthly_bars(fig, monthly_data, mode="light")
```

**Key Differences**:
- Plotly uses Figure objects instead of Axes
- Enhanced hover information available
- Better color gradient support
- JSON schema export capability

### Donut Chart

**Before (matplotlib)**:
```python
generator.create_enhanced_donut_chart(ax, quality_data, mode="light")
```

**After (Plotly)**:
```python
fig = generator.create_enhanced_donut_chart(fig, quality_data, mode="light")
```

**Key Differences**:
- Interactive hover effects
- Better text positioning
- Pull effects for emphasis
- Improved legend placement

### Waterfall Chart

**New Plotly Features**:
- Automatic cumulative line overlay
- Performance zone annotations
- Smart trade labeling
- Clustering for large datasets
- Performance bands view for scalability

### Scatter Plot

**New Plotly Features**:
- Bubble sizing based on trade magnitude
- DBSCAN clustering for high-density data
- Intelligent outlier labeling
- Trend line overlay
- Quality-based color coding

## Performance Optimization

### Production Configuration

```python
from scripts.utils.production_optimizer import create_production_optimizer

# Initialize optimizer
optimizer = create_production_optimizer(theme_manager)

# Configure for production
optimizer.config.update({
    "enable_webgl": True,
    "cache_templates": True,
    "sample_large_datasets": True,
    "batch_processing": True,
    "parallel_processing": True
})

# Optimize chart generation
chart, metrics = optimizer.optimize_chart_generation(
    chart_generator_func=generator.create_enhanced_scatter,
    chart_type="scatter",
    data=trade_data
)
```

### Memory Management

```python
# Monitor memory usage
report = optimizer.get_performance_report()
print(f"Memory usage: {report['summary']['total_memory_used']} bytes")

# Clean up resources
optimizer.cleanup_resources()
```

### Batch Processing

```python
# Process multiple charts efficiently
chart_requests = [
    {"chart_generator_func": generator.create_enhanced_monthly_bars, 
     "chart_type": "monthly_bars", "data": monthly_data},
    {"chart_generator_func": generator.create_enhanced_donut_chart,
     "chart_type": "donut", "data": quality_data}
]

results = optimizer.batch_optimize_charts(chart_requests)
```

## Frontend Integration

### Exporting Chart Configurations

```python
from scripts.utils.frontend_config_exporter import create_frontend_config_exporter

# Create exporter
exporter = create_frontend_config_exporter(theme_manager)

# Export chart configuration
config = exporter.export_chart_config(
    chart_type="enhanced_monthly_bars",
    data=monthly_data,
    theme_mode="light"
)

# Save for frontend consumption
filepath = exporter.save_config_to_file(config, "monthly_bars_config.json")
```

### React Component Integration

```javascript
// Example React component usage
import { PlotlyChart } from './components/PlotlyChart';
import monthlyBarsConfig from './configs/monthly_bars_config.json';

function Dashboard() {
  return (
    <PlotlyChart
      chartType={monthlyBarsConfig.chart_type}
      data={monthlyBarsConfig.data}
      theme={monthlyBarsConfig.theme}
      layout={monthlyBarsConfig.layout}
      styling={monthlyBarsConfig.styling}
    />
  );
}
```

### JSON Schema Validation

```python
from scripts.utils.json_schema_generator import create_json_schema_generator

# Generate schemas
schema_generator = create_json_schema_generator()
schemas = schema_generator.export_schemas("data/outputs/schemas")

# Validate configuration
is_valid, errors = schema_generator.validate_chart_config(config, "EnhancedMonthlyBars")
if not is_valid:
    print(f"Configuration errors: {errors}")
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Kaleido Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'kaleido'`

**Solution**:
```bash
pip uninstall kaleido
pip install kaleido==0.2.1
```

#### 2. Font Rendering Issues

**Problem**: Fonts not displaying correctly in exports

**Solution**:
```python
# Check font availability
from scripts.utils.plotly_theme_mapper import PlotlyThemeMapper
theme_mapper = PlotlyThemeMapper(theme_manager)
font_config = theme_mapper.get_font_configuration()
print(f"Font family: {font_config['family']}")
```

#### 3. Memory Usage Issues

**Problem**: High memory consumption with large datasets

**Solution**:
```python
# Enable data sampling
optimizer.config["sample_large_datasets"] = True
optimizer.config["memory_optimization"] = True
```

#### 4. Export Quality Issues

**Problem**: Exported images have poor quality

**Solution**:
```python
# Use high-DPI export settings
export_config = {
    "width": 1600,
    "height": 1200,
    "scale": 3,  # 300+ DPI
    "format": "png"
}
```

### Debugging Tools

#### Performance Monitoring

```python
from scripts.utils.production_optimizer import performance_monitor

@performance_monitor
def generate_dashboard():
    # Your chart generation code
    pass
```

#### Visual Comparison

```python
from scripts.utils.chart_comparison_framework import create_comparison_framework

comparison = create_comparison_framework()
similarity = comparison.compare_charts(matplotlib_chart, plotly_chart)
print(f"Visual similarity: {similarity:.2f}%")
```

### Log Analysis

```bash
# Check for common error patterns
grep -i "plotly\|kaleido\|template" logs/dashboard_generation.log

# Monitor memory usage
grep -i "memory\|oom" logs/dashboard_generation.log
```

## Best Practices

### Chart Generation

1. **Use Factory Pattern**:
   ```python
   from scripts.utils.chart_generator_factory import ChartGeneratorFactory
   
   generator = ChartGeneratorFactory.create_chart_generator(
       "plotly", theme_manager, scalability_manager
   )
   ```

2. **Enable Caching**:
   ```python
   # Cache templates and configurations
   generator.theme_mapper.template_cache_enabled = True
   ```

3. **Optimize Data**:
   ```python
   # Sample large datasets
   if len(data) > 1000:
       data = sample_data(data, target_size=500)
   ```

### Theme Management

1. **Use Consistent Templates**:
   ```python
   # Always specify template mode
   fig = theme_mapper.apply_template(fig, mode="light", high_dpi=True)
   ```

2. **Brand Compliance**:
   ```python
   # Validate colors match brand guidelines
   colors = theme_manager.get_theme_colors("light")
   assert colors.primary_data == "#3179f5"  # Sensylate blue
   ```

### Export Quality

1. **High-DPI Settings**:
   ```python
   export_config = {
       "scale": 3,      # ~300 DPI
       "width": 1600,   # High resolution
       "height": 1200
   }
   ```

2. **Format Selection**:
   - **PNG**: High-quality raster for web and print
   - **PDF**: Vector format for professional documents
   - **SVG**: Scalable vector for web applications
   - **HTML**: Interactive dashboards

### Performance

1. **Monitor Metrics**:
   ```python
   metrics = optimizer.get_performance_report()
   if metrics["summary"]["avg_generation_time"] > 2.0:
       print("Performance degradation detected")
   ```

2. **Resource Management**:
   ```python
   # Clean up after batch processing
   optimizer.cleanup_resources()
   ```

### Error Handling

1. **Graceful Degradation**:
   ```python
   try:
       fig = plotly_generator.create_chart(data)
   except Exception:
       # Fallback to matplotlib
       fig = matplotlib_generator.create_chart(data)
   ```

2. **Validation**:
   ```python
   # Validate configuration before generation
   is_valid, errors = validate_chart_config(config)
   if not is_valid:
       raise ValueError(f"Invalid configuration: {errors}")
   ```

## Rollback Procedures

### Emergency Rollback

If critical issues arise, immediate rollback to matplotlib:

1. **Update Configuration**:
   ```yaml
   # configs/dashboard_generation.yaml
   chart_engine: "matplotlib"
   plotly_enabled: false
   ```

2. **Restart Services**:
   ```bash
   # Restart dashboard generation services
   systemctl restart dashboard-generator
   ```

3. **Verify Operation**:
   ```bash
   python scripts/dashboard_generator.py --verify
   ```

### Partial Rollback

Rollback specific chart types while keeping others on Plotly:

```yaml
chart_migrations:
  monthly_bars: "matplotlib"    # Rollback this chart type
  donut_chart: "plotly"        # Keep this on Plotly
  waterfall_chart: "plotly"
  scatter_plot: "plotly"
```

### Rollback Validation

```python
# Test rollback configuration
from scripts.utils.chart_generator_factory import ChartGeneratorFactory

generator = ChartGeneratorFactory.create_chart_generator("matplotlib", theme_manager)
assert isinstance(generator, MatplotlibChartGenerator)
print("✅ Rollback to matplotlib successful")
```

### Data Recovery

If chart outputs are corrupted:

1. **Restore from Backup**:
   ```bash
   cp backup/data/outputs/charts/* data/outputs/charts/
   ```

2. **Regenerate Charts**:
   ```bash
   python scripts/dashboard_generator.py --regenerate-all
   ```

3. **Verify Integrity**:
   ```bash
   python scripts/validate_chart_outputs.py
   ```

## Monitoring and Maintenance

### Health Checks

```python
def check_plotly_health():
    """Perform health check on Plotly system."""
    try:
        import plotly
        import kaleido
        
        # Test chart generation
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]))
        
        # Test export
        fig.write_image("test_export.png", width=800, height=600)
        
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
```

### Performance Monitoring

```python
# Monitor generation times
def monitor_performance():
    report = optimizer.get_performance_report()
    
    if report["summary"]["avg_generation_time"] > 5.0:
        print("⚠️ Performance degradation detected")
    
    if report["summary"]["cache_hit_rate"] < 0.3:
        print("⚠️ Cache efficiency low")
```

### Maintenance Schedule

- **Daily**: Check error logs and performance metrics
- **Weekly**: Clear cache and update templates
- **Monthly**: Review performance trends and optimize
- **Quarterly**: Update dependencies and validate compatibility

---

## Support and Resources

- **Documentation**: [Plotly Documentation](https://plotly.com/python/)
- **Issues**: Report migration issues in project repository
- **Performance**: Use built-in monitoring tools for optimization
- **Updates**: Follow semantic versioning for chart system updates

For additional support, consult the development team or create an issue in the project repository.