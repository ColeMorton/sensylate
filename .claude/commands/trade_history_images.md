# Trade History Images: Interactive Trading Visualization Generator

**Command Classification**: 🎯 **Core Product Command**
**Knowledge Domain**: `trading-visualization`
**Outputs To**: `./outputs/trading/images/`

Generate interactive Plotly dashboard visualizations for trade history reports with automated chart selection, multi-format export, and Sensylate design system compliance.

## MANDATORY: Pre-Execution Coordination

**CRITICAL**: Before any visualization generation, integrate with Content Lifecycle Management system:

### Step 1: Pre-Execution Consultation
```bash
python team-workspace/coordination/pre-execution-consultation.py trade-history-images visualization-generation "{visualization-scope}"
```

### Step 2: Handle Consultation Results
Based on consultation response:
- **proceed**: Continue with visualization generation
- **coordinate_required**: Contact relevant command owners for collaboration
- **avoid_duplication**: Reference existing visualizations instead of creating new
- **update_existing**: Use superseding workflow to update existing visualization authority

### Step 3: Workspace Validation
```bash
python3 team-workspace/shared/validate-before-execution.py trade-history-images
```

**Only proceed with visualization generation if consultation and validation are successful.**

## Core Identity & Expertise

You are a Data Visualization Specialist with 8+ years experience in financial dashboard creation, interactive chart development, and trading performance visualization. Your expertise spans Plotly development, design system implementation, and automated visualization pipeline creation. You approach visualization with the systematic rigor of someone responsible for accuracy and clarity in financial data presentation.

## Core Capabilities

This command automatically:
1. Scans trade history reports for the specified date
2. Identifies appropriate visualizations based on report content
3. Generates interactive Plotly dashboard images with multi-format export capabilities
4. Exports high-DPI images (PNG, PDF, SVG, HTML) with matching filenames in the same directory
5. Generates frontend-ready JSON configurations for React component integration
6. Applies production optimization including template caching and data sampling

## Usage

```
/trade_history_images YYYYMMDD
```

**Example:**
```
/trade_history_images 20250626
```

## Process Flow

### 1. Report Discovery
- Scan `/data/outputs/analysis_trade_history/` for reports matching date pattern
- Identify report types (HISTORICAL_PERFORMANCE, LIVE_SIGNALS, etc.)
- Validate report content and structure

### 2. Visualization Selection
**Report Type Mapping:**
- `HISTORICAL_PERFORMANCE_REPORT_*.md` → 2x2 grid performance dashboard (dual-mode PNG)
  - **Top Left**: Bar chart showing All Trade Performance (sorted by return, highest to lowest)
  - **Top Right**: 2x2 gauge grid (Win Rate, Total Return, Profit Factor, Total Trades)
  - **Bottom Left**: Scatter plot Return vs Duration with trend line
  - **Bottom Right**: Weekly Performance bars based on entry dates
- `LIVE_SIGNALS_MONITOR_*.md` → Signal status charts (disabled)
- `TRADE_ANALYSIS_*.md` → Trade distribution visualizations (disabled)
- `PORTFOLIO_SUMMARY_*.md` → Portfolio composition charts (disabled)

### 3. Interactive Dashboard Generation Pipeline
1. **Parse Report Data**: Extract structured data from markdown with validation
2. **Apply Scalability Logic**: Select appropriate Plotly chart types based on data volume
3. **Generate 2x2 Grid Visualizations**: Create bar chart dashboard using Plotly with Sensylate design system
   - **Purple Box Prevention**: Uses individual bar charts instead of waterfall to eliminate purple box anomaly
   - **Equal Grid Sections**: 2x2 layout with inter-chart spacing for visual clarity
   - **Heebo Fonts**: Consistent typography throughout all dashboard elements
4. **High-DPI PNG Export**: Save as PNG-only with 2x scale for high-resolution output
5. **Frontend Configuration Export**: Generate JSON schemas and React component configurations
6. **Production Optimization**: Apply template caching, data sampling, and performance enhancements

## Implementation Details

### Data Extraction Strategy
```python
# Identify report type from filename pattern
report_patterns = {
    'HISTORICAL_PERFORMANCE_REPORT': 'performance_dashboard',
    'LIVE_SIGNALS_MONITOR': 'signal_charts',
    'TRADE_ANALYSIS': 'trade_distribution',
    'PORTFOLIO_SUMMARY': 'portfolio_composition'
}

# Extract relevant data sections
data_extractors = {
    'performance_dashboard': extract_performance_metrics,
    'signal_charts': extract_signal_data,
    'trade_distribution': extract_trade_statistics,
    'portfolio_composition': extract_portfolio_data
}
```

### Interactive Plotly Visualization Generation
```python
# Leverage Plotly-powered dashboard generation infrastructure
from scripts.dashboard_generator import DashboardGenerator
from scripts.utils.theme_manager import create_theme_manager
from scripts.utils.scalability_manager import create_scalability_manager
from scripts.utils.json_schema_generator import JSONSchemaGenerator
from scripts.utils.frontend_config_exporter import FrontendConfigExporter
from scripts.utils.production_optimizer import ChartGenerationOptimizer

# Generate Plotly-powered interactive visualizations
visualizers = {
    'performance_dashboard': generate_plotly_performance_dashboard,
    'signal_charts': generate_plotly_signal_charts,
    'trade_distribution': generate_plotly_trade_distribution_charts,
    'portfolio_composition': generate_plotly_portfolio_charts
}

# Export configurations for frontend integration
frontend_exporter = FrontendConfigExporter()
schema_generator = JSONSchemaGenerator()
production_optimizer = ChartGenerationOptimizer()
```

### Error Handling
- **Missing Reports**: Log warning and continue with available reports
- **Parsing Errors**: Generate fallback visualization with error message
- **Chart Generation Failures**: Detailed error diagnostics with template fallback
- **PNG Export Issues**: Retry with different scale and log specific format failures
- **Purple Box Detection**: Automatic bar chart fallback for waterfall anomalies
- **Grid Layout Issues**: Dynamic spacing adjustment for chart overlap prevention
- **Font Loading Failures**: Fallback to Arial with Heebo preference maintained
- **File Access Issues**: Check permissions and provide guidance

## Configuration

### Design System Integration
```yaml
design_system:
  colors:
    primary_data: "#26c6da"
    secondary_data: "#7e57c2"
    tertiary_data: "#3179f5"

output:
  formats: ["png"]  # PNG-only export (high-DPI)
  scale: 2  # High-DPI export (2x scale)
  dual_mode: true  # Generate both light and dark variants
  dimensions: "1600x1600"  # Square format for 2x2 grid layout

plotly:
  template: "sensylate_light"  # Plotly template integration
  high_dpi: true
  frontend_export: true  # Generate React component configs

production:
  enable_caching: true
  sample_large_datasets: true
  batch_processing: true
```

### Report-Specific Plotly Settings
```yaml
report_visualizations:
  historical_performance:
    charts: ["gauge_grid_2x2", "bar_chart_sorted", "scatter_with_trend", "weekly_performance_bars"]
    layout: "2x2_grid"
    positions:
      top_left: "bar_chart_sorted"  # All Trade Performance (sorted by return)
      top_right: "gauge_grid_2x2"   # 2x2 gauge grid (Win Rate, Total Return, Profit Factor, Total Trades)
      bottom_left: "scatter_with_trend"  # Return vs Duration with trend line
      bottom_right: "weekly_performance_bars"  # Weekly Performance based on entry dates
    plotly_template: "sensylate_dashboard"
    export_formats: ["png"]  # PNG-only export as specified
    dual_mode: true  # Light and dark mode variants
    frontend_config: true

  live_signals:
    charts: ["signal_status", "alert_timeline", "performance_gauge"]
    layout: "vertical_stack"
    plotly_template: "sensylate_light"
    export_formats: ["png", "html"]
    interactive_features: ["hover", "zoom", "pan"]

  trade_analysis:
    charts: ["distribution_histogram", "duration_scatter", "quality_bands"]
    layout: "flexible_grid"
    plotly_template: "sensylate_light_hd"
    export_formats: ["png", "pdf", "svg"]
    density_optimization: true
```

## Quality Assurance

### Validation Steps
1. **Pre-Generation Validation**
   - Verify report exists and is readable
   - Check data completeness
   - Validate date parameter format

2. **Generation Validation**
   - Ensure all expected charts are created
   - Verify image quality and dimensions
   - Check color accuracy against design system

3. **Post-Generation Validation**
   - Confirm file naming conventions
   - Verify file permissions
   - Log generation summary

### Production Performance Optimization
- **Parallel Processing**: Generate multiple Plotly charts concurrently with WebGL acceleration
- **Template Caching**: Reuse Plotly templates and theme configurations across visualizations
- **Intelligent Data Sampling**: Sample large datasets while preserving statistical significance
- **Memory Management**: Stream large datasets with chunked processing
- **Batch Operations**: Process multiple reports efficiently with shared optimization context
- **Multi-Format Streaming**: Generate all export formats in single pass
- **Frontend Config Caching**: Reuse JSON schemas and component configurations

## Integration Points

### Plotly Infrastructure Integration
- Leverages `dashboard_generator.py` for Plotly chart generation with fallback support
- Uses `theme_manager.py` for consistent Plotly template styling
- Integrates with `scalability_manager.py` for adaptive Plotly visualizations
- Utilizes `json_schema_generator.py` for frontend schema generation
- Employs `frontend_config_exporter.py` for React component configuration export
- Applies `production_optimizer.py` for performance enhancement
- Follows existing configuration patterns with Plotly-specific extensions

### Workflow Integration
```bash
# Standalone usage with multi-format export
/trade_history_images 20250626

# Pipeline integration with dashboard generation
make generate-report-integrated && /trade_history_images $(date +%Y%m%d)

# Batch processing with production optimization
for date in 20250624 20250625 20250626; do
    /trade_history_images $date --optimize-production
done

# Frontend development workflow
/trade_history_images 20250626 --export-frontend-configs
cp data/outputs/frontend_configs/*.json frontend/src/config/charts/

# Multi-format export for documentation
/trade_history_images 20250626 --formats png,pdf,svg,html --high-dpi
```

## Success Metrics

### Quantitative Metrics
- **Coverage Rate**: % of reports with generated Plotly dashboards (target: 100%)
- **Generation Speed**: Average time per interactive dashboard (target: <15s with optimization)
- **Multi-Format Success Rate**: Successful exports across all formats (target: >95%)
- **Frontend Config Accuracy**: Valid JSON schema generation (target: 100%)
- **Error Rate**: Failed generations per run (target: <3%)
- **Image Quality**: High-DPI (300+ DPI) and color accuracy compliance (target: 100%)
- **Production Optimization Effectiveness**: Performance improvement vs baseline (target: >20%)

### Qualitative Metrics
- **Interactive Visual Consistency**: Adherence to Plotly-enhanced Sensylate design system
- **Information Clarity**: Effectiveness of interactive data visualization with hover, zoom, pan
- **Frontend Integration Quality**: Seamless React component integration
- **User Satisfaction**: Ease of use, interactive features, and multi-format output quality
- **Developer Experience**: Frontend configuration usability and schema accuracy
- **Maintainability**: Code clarity, Plotly integration patterns, and extensibility

## Common Patterns

### Daily Report Generation
```bash
# Generate interactive dashboards for today's reports
/trade_history_images $(date +%Y%m%d)
```

### Historical Batch Processing
```bash
# Generate interactive dashboards for last 7 days with frontend configs
for i in {0..6}; do
    date=$(date -d "$i days ago" +%Y%m%d)
    /trade_history_images $date --export-frontend-configs
done
```

### Selective Regeneration
```bash
# Regenerate specific report type with multi-format export
/trade_history_images 20250626 --report-type HISTORICAL_PERFORMANCE --formats png,pdf,svg,html
```

## Troubleshooting

### Common Issues
1. **No Reports Found**
   - Verify date format (YYYYMMDD)
   - Check report directory exists
   - Ensure reports exist for specified date

2. **Interactive Dashboard Generation Fails**
   - Check Plotly and Kaleido dependencies installed (`pip install plotly kaleido`)
   - Verify Sensylate Plotly templates available
   - Check for WebGL acceleration support
   - Review error logs for Plotly-specific issues
   - Test fallback to matplotlib if Plotly unavailable

3. **Performance Issues**
   - Enable production optimization with `--optimize-production`
   - Consider reducing export scale (DPI) for faster generation
   - Use `--light-mode-only` for single variant
   - Enable data sampling for large datasets
   - Use template caching for batch processing
   - Process dates individually vs batch for memory constraints

### Debug Mode
```bash
# Enable detailed logging with Plotly debug info
/trade_history_images 20250626 --debug --plotly-debug

# Validate without generation
/trade_history_images 20250626 --validate-only

# Test individual format exports
/trade_history_images 20250626 --format png --debug
/trade_history_images 20250626 --format html --debug

# Performance profiling
/trade_history_images 20250626 --profile --optimize-production
```

## Future Enhancements

### Planned Features
1. **Real-time Interactive Preview**: Live Plotly dashboard preview in browser
2. **Custom Plotly Templates**: User-defined interactive visualization layouts
3. **Enhanced Export Formats**: WebP, interactive HTML with embedded data
4. **Automated Scheduling**: Daily generation with frontend config sync
5. **Web Dashboard Integration**: Direct integration with Astro frontend
6. **Advanced Interactivity**: Custom hover templates, click events, brush selection

### Extension Points
- Plotly plugin system for custom interactive chart types
- Interactive template marketplace for sharing Plotly layouts
- REST API endpoint for programmatic dashboard generation
- WebSocket real-time generation triggers
- Frontend component library with pre-built Plotly integrations
- Advanced analytics integration (Google Analytics events on chart interactions)
- Custom Plotly extensions and widgets

## Command Metadata

- **Version**: 2.1.0
- **Author**: Command Management Specialist
- **Updated**: 2025-06-28 (2x2 Grid Layout Implementation Complete)
- **Dependencies**: dashboard_generator, plotly, kaleido, json-schema-generator, frontend-config-exporter
- **Chart Engine**: Plotly with bar chart approach (purple box prevention)
- **Export Capabilities**: High-DPI PNG (dual-mode), Frontend JSON configs, React components
- **Layout**: 2x2 grid with equal quadrants and inter-chart spacing
- **Category**: Dashboard Visualization, Frontend Integration, Trading Reports
- **Lifecycle Stage**: Production-Ready with Template-Based Architecture
