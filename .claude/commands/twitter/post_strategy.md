# Trading Strategy X Post Generator: Live Trading Signals (Template-Driven)

**Command Classification**: 📊 **Core Product Command**
**Knowledge Domain**: `social-media-strategy`
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-07-18)*
**Outputs To**: `{DATA_OUTPUTS}/twitter/post_strategy/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/strategy_analysis_script.py`
**Script Class**: `StrategyAnalysisScript`
**Registry Name**: `strategy_analysis`
**Content Types**: `["strategy"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="strategy_analysis",
    content_types=["strategy"],
    requires_validation=True
)
class StrategyAnalysisScript(BaseScript):
    """
    Generalized strategy analysis script for live trading signal content generation
    
    Parameters:
        ticker (str): Stock ticker symbol
        date (str): Analysis date in YYYYMMDD format
        template_variant (Optional[str]): Specific template to use
        validate_content (bool): Whether to validate generated content
    """
```

**Supporting Components**:
```yaml
template_selector:
  path: "{SCRIPTS_BASE}/twitter_template_selector_refactored.py"
  class: "TwitterTemplateSelector"
  purpose: "Template selection for strategy signals"
  
validation_framework:
  path: "{SCRIPTS_BASE}/unified_validation_framework.py"
  class: "UnifiedValidationFramework"
  purpose: "Content quality validation and scoring"
  
template_renderer:
  path: "{SCRIPTS_BASE}/twitter_template_renderer.py"
  class: "TwitterTemplateRenderer"
  purpose: "Jinja2 template rendering with live signal optimization"
```

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/twitter/strategy/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| strategy_signal | `strategy/twitter_post_strategy.j2` | Live signal triggered today | Primary trading signal template |
| strategy_default | `strategy/twitter_strategy_default.j2` | General strategy performance | Performance-focused template |

**Shared Components**:
```yaml
base_template:
  path: "{TEMPLATES_BASE}/twitter/shared/base_twitter.j2"
  purpose: "Base template with common macros and formatting"
  
components:
  path: "{TEMPLATES_BASE}/twitter/shared/components.j2"
  purpose: "Advanced hook generation for live signals"
  
validation_template:
  path: "{TEMPLATES_BASE}/twitter/validation/content_quality_checklist.j2"
  purpose: "Quality gates for trading signal compliance"
```

**Template Selection Algorithm**:
```python
def select_strategy_template(signal_data):
    """Select optimal template for trading signal content"""
    
    # Primary: Live signal template for TODAY'S signals
    if (signal_data.get('signal_triggered', False) and
        signal_data.get('live_signal', False)):
        return 'strategy/twitter_post_strategy.j2'
    
    # Default: General strategy performance template
    return 'strategy/twitter_strategy_default.j2'
```

You are an expert financial content analyzer and social media strategist specialized in creating compelling X posts for **LIVE TRADING SIGNALS** using the project's Jinja2 template infrastructure.

## Data Structure Specification

**Required Context for Template Rendering**:

```python
context = {
    'ticker': str,
    'timestamp': str,
    'data': {
        # Strategy Parameters (from CSV)
        'strategy_type': str,  # e.g., "SMA", "EMA"
        'short_window': int,   # e.g., 10
        'long_window': int,    # e.g., 25
        'period': str,         # e.g., "5 years"

        # Performance Metrics (TrendSpider Authority)
        'net_performance': float,
        'win_rate': float,
        'total_trades': int,
        'avg_win': float,
        'avg_loss': float,
        'reward_risk_ratio': float,
        'max_drawdown': float,
        'buy_hold_drawdown': float,
        'sharpe': float,
        'sortino': float,
        'exposure': float,
        'avg_trade_length': float,
        'expectancy': float,

        # Seasonality Data (TrendSpider Visual)
        'current_month': str,
        'current_month_performance': float,
        'current_month_avg': float,
        'best_months': str,
        'best_months_performance': float,
        'worst_months': str,
        'worst_months_performance': float,
        'seasonality_strength': str,

        # Live Signal Context
        'signal_triggered': bool,
        'current_price': float,
        'technical_setup': str,
        'fundamental_catalyst': str,
        'market_context': str,
        'risk_management': str,

        # Fundamental Integration
        'recent_earnings': str,
        'key_financial_metrics': str,
        'sector_performance': str,
        'fundamentals': str,

        # Hook Generation Data
        'hook': str,  # Optional custom hook
        'key_insight': str,
        'conviction_level': str,

        # Compliance
        'disclaimer': str,  # Optional custom disclaimer
        'live_signal': bool
    }
}
```

## Simplified Data Processing Workflow

**Streamlined 6-Step Process** (replaces 769+ lines):

1. **Strategy Parameter Extraction**
   ```python
   def extract_strategy_params(csv_file_path):
       """Extract strategy type, windows from CSV headers"""
       return {
           'strategy_type': parse_strategy_type(csv_file_path),
           'short_window': extract_short_window(csv_file_path),
           'long_window': extract_long_window(csv_file_path)
       }
   ```

## CLI Service Integration

**Service Commands**:
```yaml
yahoo_finance_cli:
  command: "python {SCRIPTS_BASE}/yahoo_finance_cli.py"
  usage: "{command} quote {ticker} --env prod --output-format json"
  purpose: "Real-time market data for current price validation"
  health_check: "{command} health --env prod"
  priority: "primary"
  
alpha_vantage_cli:
  command: "python {SCRIPTS_BASE}/alpha_vantage_cli.py"
  usage: "{command} quote {ticker} --env prod --output-format json"
  purpose: "Secondary price validation for trading signals"
  health_check: "{command} health --env prod"
  priority: "secondary"
```

**Real-Time Data Collection Protocol**:
```bash
# Mandatory real-time price collection for live signals
python {SCRIPTS_BASE}/yahoo_finance_cli.py quote {ticker} --env prod --output-format json

# Secondary validation
python {SCRIPTS_BASE}/alpha_vantage_cli.py quote {ticker} --env prod --output-format json
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  trendspider_performance: "HIGHEST_AUTHORITY"  # TrendSpider tabular data
  csv_strategy_data: "SECONDARY"  # Strategy parameters and historical performance
  yahoo_finance: "REAL_TIME_PRICE"  # Current market price
  
conflict_resolution:
  trendspider_precedence: "absolute"  # TrendSpider always takes priority
  threshold: "10%"  # Variance threshold for conflict detection
  action: "use_trendspider"  # Resolution strategy
```

## Data Flow & File References

**Input Sources**:
```yaml
trendspider_tabular:
  path: "{DATA_IMAGES}/trendspider_tabular/{TICKER}_{YYYYMMDD}.png"
  format: "png"
  required: false
  description: "Performance data with HIGHEST AUTHORITY - pixel-level accuracy required"
  
csv_strategy_data:
  path: "{DATA_RAW}/analysis_strategy/{TICKER}_{YYYYMMDD}.csv"
  format: "csv"
  required: true
  description: "Strategy parameters and historical performance data"
  
real_time_market:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Current market price for TODAY'S ENTRY SIGNAL context"
  
fundamental_context:
  path: "{DATA_OUTPUTS}/fundamental_analysis/{TICKER}_{YYYYMMDD}.md"
  format: "markdown"
  required: false
  description: "Supporting fundamental analysis for signal context"
```

**Output Structure**:
```yaml
primary_output:
  path: "{DATA_OUTPUTS}/twitter/post_strategy/{TICKER}_{YYYYMMDD}.md"
  format: "markdown"
  description: "Generated live trading signal content"
  
metadata_output:
  path: "{DATA_OUTPUTS}/twitter/post_strategy/{TICKER}_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Strategy parameters and template selection metadata"
  
validation_output:
  path: "{DATA_OUTPUTS}/twitter/post_strategy/validation/{TICKER}_{YYYYMMDD}_validation.json"
  format: "json"
  description: "Signal validation and seasonality accuracy results"
```

3. **TrendSpider Data Authority Protocol**
   ```python
   def apply_authority_protocol(trendspider_data, csv_data):
       """Automated conflict resolution using TrendSpider authority"""
       conflicts = detect_conflicts(trendspider_data, csv_data, threshold=0.10)
       return resolve_with_trendspider_authority(conflicts) if conflicts else trendspider_data
   ```

4. **Template Context Assembly**
   ```python
   context = {
       'ticker': ticker,
       'timestamp': datetime.utcnow().isoformat(),
       'data': merge_data_sources(
           strategy_params,
           trendspider_metrics,
           seasonality_data,
           fundamental_context,
           market_data
       )
   }
   ```

5. **Template Rendering with Validation**
   ```python
   from jinja2 import Environment, FileSystemLoader

   env = Environment(loader=FileSystemLoader('scripts/templates/twitter'))

   # Render main content
   template = env.get_template('strategy/twitter_post_strategy.j2')
   content = template.render(**context)

   # Validate quality
   validation_template = env.get_template('validation/content_quality_checklist.j2')
   validation = validation_template.render(content_data=analyze_content(content))

   if not validation['institutional_ready']:
       raise ValidationError(validation['recommendations'])
   ```

6. **Export with Metadata**
   ```
   ./data/outputs/twitter/post_strategy/{TICKER}_{YYYYMMDD}.md
   ```

## Enhanced Data Validation Protocol

**Automated Quality Gates** (template-driven):

```python
# Seasonality Data Validation
def validate_seasonality_extraction(visual_data):
    """Robust validation with confidence assessment"""
    confidence_factors = {
        'no_outliers': all(-50 <= perf <= 100 for perf in visual_data.values()),
        'data_completeness': len(visual_data) == 12,
        'logical_consistency': validate_seasonal_patterns(visual_data),
        'visual_clarity': assess_chart_clarity_score(visual_data)
    }

    confidence = sum(confidence_factors.values()) / len(confidence_factors)

    if confidence >= 0.95:
        return {'status': 'high_confidence', 'data': visual_data}
    elif confidence >= 0.80:
        return {'status': 'medium_confidence', 'data': visual_data, 'flags': get_uncertainty_flags(visual_data)}
    else:
        return {'status': 'fallback_required', 'fallback_data': get_csv_fallback()}

# Data Authority Resolution
authority_resolution = apply_data_authority_protocol(trendspider_data, csv_data)
context['data'].update(authority_resolution['authoritative_data'])
context['metadata'] = authority_resolution['resolution_metadata']
```

## Validation-Driven Enhancement Protocol

**Existing Post Optimization** (when validation file detected):

```python
def enhance_strategy_post(validation_file_path):
    """Systematic post improvement using templates"""

    # Parse validation input
    ticker, date = extract_ticker_date(validation_file_path)
    validation_data = load_validation_assessment(validation_file_path)

    # Load original content and data
    original_post = load_original_post(f"{ticker}_{date}")
    original_data = extract_data_from_post(original_post)

    # Apply enhancement template
    enhancement_context = {
        'original_data': original_data,
        'validation_issues': validation_data,
        'enhancement_targets': {
            'trendspider_authority_required': validation_data.get('data_conflicts', []),
            'seasonality_precision_needed': validation_data.get('seasonality_issues', []),
            'reliability_improvements': validation_data.get('accuracy_concerns', [])
        }
    }

    # Re-render with enhanced data
    enhanced_template = env.get_template('strategy/enhanced_strategy_post.j2')
    enhanced_content = enhanced_template.render(**enhancement_context)

    # Overwrite original with seamless enhancement
    save_enhanced_post(enhanced_content, f"{ticker}_{date}")
```

## Template-Driven Hook Generation

**Dynamic Hook Creation** (replaces 200+ lines of embedded logic):

```python
# Hook generation now handled by template macros
# Templates automatically:
# - Select optimal emoji based on performance metrics
# - Generate 280-character optimized hooks
# - Include ticker and strategy parameters
# - Create urgency for live signals
# - Enforce NO BOLD FORMATTING requirement

# Example template usage:
hook = generate_dynamic_hook(
    ticker=ticker,
    data=strategy_data,
    content_type="strategy",
    style="live_signal" if data.signal_triggered else "performance"
)
```

## Execution Examples

### Direct Python Execution
```python
from script_registry import get_global_registry
from script_config import ScriptConfig

# Initialize
config = ScriptConfig.from_environment()
registry = get_global_registry(config)

# Execute live trading signal generation
result = registry.execute_script(
    "strategy_analysis",
    ticker="AAPL",
    date="20250718",
    validate_content=True
)

# Execute with specific template override
result = registry.execute_script(
    "strategy_analysis",
    ticker="COR",
    date="20250718",
    template_variant="strategy_signal",
    validate_content=True
)
```

### Command Line Execution
```bash
# Via content automation CLI
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script strategy_analysis \
    --ticker AAPL \
    --date 20250718 \
    --validate-content true

# Via direct script execution
python {SCRIPTS_BASE}/base_scripts/strategy_analysis_script.py \
    --ticker COR \
    --date 20250616 \
    --template-variant strategy_signal

# With custom data path
python {SCRIPTS_BASE}/base_scripts/strategy_analysis_script.py \
    --ticker AAPL \
    --date 20250718 \
    --data-path /custom/path/strategy_data.csv
```

### Claude Command Execution
```
# New live trading signal post
/twitter_post_strategy AAPL_20250718

# Strategy performance post
/twitter_post_strategy COR_20250616

# Validation-driven enhancement
/twitter_post_strategy {DATA_OUTPUTS}/twitter/post_strategy/validation/DOV_20250627_validation.json

# Template-specific generation
/twitter_post_strategy MSFT_20250718 template_variant=strategy_signal
```

### Live Signal Workflow Examples
```
# Generate TODAY'S ENTRY SIGNAL post
/twitter_post_strategy AAPL_20250718

# If seasonality validation fails, enhance using validation file
/twitter_post_strategy {DATA_OUTPUTS}/twitter/post_strategy/validation/AAPL_20250718_validation.json

# Generate performance-focused post (no live signal)
/twitter_post_strategy COR_20250616 template_variant=strategy_default
```

## Template-Driven Advantages

**Dramatic Simplification**:
- **Code Reduction**: 769 lines → ~180 lines (77% reduction)
- **Logic Consolidation**: Embedded templates → centralized Jinja2 system
- **Maintenance**: Single source of truth for content structure
- **Testing**: Easy A/B testing of different hook strategies

**Enhanced Quality**:
- **Automated Validation**: Built-in quality gates and compliance
- **Consistent Formatting**: Template-enforced standards
- **Data Authority**: Systematic TrendSpider precedence protocol
- **Error Handling**: Graceful degradation with template fallbacks

**Scalability**:
- **Template Inheritance**: Shared components across content types
- **Dynamic Selection**: Data-driven template routing
- **Conditional Content**: Smart content adaptation based on data
- **Performance**: Template compilation and caching

---

**Ready to generate live trading signal content using the template-driven architecture. Provide {TICKER}_{YYYYMMDD} or validation file path to begin enhanced content generation.**
