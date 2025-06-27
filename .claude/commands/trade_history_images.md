# Trade History Images Command

Generate visualization images for trade history reports with automated chart selection and Sensylate design system compliance.

## Core Capabilities

This command automatically:
1. Scans trade history reports for the specified date
2. Identifies appropriate visualizations based on report content
3. Generates high-quality images following Sensylate design standards
4. Exports images with matching filenames in the same directory

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
- `HISTORICAL_PERFORMANCE_REPORT_*.md` → Performance dashboard (dual-mode)
- `LIVE_SIGNALS_MONITOR_*.md` → Signal status charts
- `TRADE_ANALYSIS_*.md` → Trade distribution visualizations
- `PORTFOLIO_SUMMARY_*.md` → Portfolio composition charts

### 3. Image Generation Pipeline
1. **Parse Report Data**: Extract structured data from markdown
2. **Apply Scalability Logic**: Select appropriate chart types based on data volume
3. **Generate Visualizations**: Create charts using Sensylate design system
4. **Export Images**: Save as high-quality PNG with matching filenames

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

### Visualization Generation
```python
# Leverage existing dashboard generation infrastructure
from scripts.dashboard_generator import DashboardGenerator
from scripts.utils.theme_manager import create_theme_manager
from scripts.utils.scalability_manager import create_scalability_manager

# Generate appropriate visualizations
visualizers = {
    'performance_dashboard': generate_performance_dashboard,
    'signal_charts': generate_signal_charts,
    'trade_distribution': generate_trade_distribution_charts,
    'portfolio_composition': generate_portfolio_charts
}
```

### Error Handling
- **Missing Reports**: Log warning and continue with available reports
- **Parsing Errors**: Generate fallback visualization with error message
- **Generation Failures**: Provide detailed error diagnostics
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
  format: "png"
  dpi: 300
  dual_mode: true  # Generate both light and dark variants
```

### Report-Specific Settings
```yaml
report_visualizations:
  historical_performance:
    charts: ["metrics_summary", "monthly_bars", "quality_donut", "waterfall"]
    layout: "2x2_grid"
    
  live_signals:
    charts: ["signal_status", "alert_timeline", "performance_gauge"]
    layout: "vertical_stack"
    
  trade_analysis:
    charts: ["distribution_histogram", "duration_scatter", "quality_bands"]
    layout: "flexible_grid"
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

### Performance Optimization
- **Parallel Processing**: Generate multiple charts concurrently
- **Caching**: Reuse parsed data across visualizations
- **Memory Management**: Stream large datasets
- **Batch Operations**: Process multiple reports efficiently

## Integration Points

### Existing Infrastructure
- Leverages `dashboard_generator.py` for chart generation
- Uses `theme_manager.py` for consistent styling
- Integrates with `scalability_manager.py` for adaptive visualizations
- Follows existing configuration patterns

### Workflow Integration
```bash
# Standalone usage
/trade_history_images 20250626

# Pipeline integration
make generate-report && /trade_history_images $(date +%Y%m%d)

# Batch processing
for date in 20250624 20250625 20250626; do
    /trade_history_images $date
done
```

## Success Metrics

### Quantitative Metrics
- **Coverage Rate**: % of reports with generated images (target: 100%)
- **Generation Speed**: Average time per report (target: <10s)
- **Error Rate**: Failed generations per run (target: <5%)
- **Image Quality**: DPI and color accuracy compliance (target: 100%)

### Qualitative Metrics
- **Visual Consistency**: Adherence to Sensylate design system
- **Information Clarity**: Effectiveness of data visualization
- **User Satisfaction**: Ease of use and output quality
- **Maintainability**: Code clarity and extensibility

## Common Patterns

### Daily Report Generation
```bash
# Generate images for today's reports
/trade_history_images $(date +%Y%m%d)
```

### Historical Batch Processing
```bash
# Generate images for last 7 days
for i in {0..6}; do
    date=$(date -d "$i days ago" +%Y%m%d)
    /trade_history_images $date
done
```

### Selective Regeneration
```bash
# Regenerate specific report type
/trade_history_images 20250626 --report-type HISTORICAL_PERFORMANCE
```

## Troubleshooting

### Common Issues
1. **No Reports Found**
   - Verify date format (YYYYMMDD)
   - Check report directory exists
   - Ensure reports exist for specified date

2. **Image Generation Fails**
   - Check Python dependencies installed
   - Verify Sensylate configuration present
   - Review error logs for specific issues

3. **Performance Issues**
   - Consider reducing DPI for faster generation
   - Use --light-mode-only for single variant
   - Process dates individually vs batch

### Debug Mode
```bash
# Enable detailed logging
/trade_history_images 20250626 --debug

# Validate without generation
/trade_history_images 20250626 --validate-only
```

## Future Enhancements

### Planned Features
1. **Interactive Mode**: Preview before saving
2. **Custom Templates**: User-defined visualization layouts
3. **Export Formats**: SVG, PDF support
4. **Scheduling**: Automated daily generation
5. **Web Dashboard**: Browser-based preview interface

### Extension Points
- Plugin system for custom chart types
- Template marketplace for sharing layouts
- API endpoint for programmatic access
- Real-time generation triggers

## Command Metadata

- **Version**: 1.0.0
- **Author**: Command Management Specialist
- **Created**: 2025-06-26
- **Dependencies**: dashboard_generator, matplotlib, sensylate-config
- **Category**: Visualization, Reporting
- **Lifecycle Stage**: Production-Ready