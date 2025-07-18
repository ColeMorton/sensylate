# Short-Form Fundamental Analysis X Post Generator

**Command Classification**: 📊 **Core Product Command**
**Knowledge Domain**: `social-media-strategy`
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-07-18)*
**Outputs To**: `{DATA_OUTPUTS}/twitter/fundamental_analysis/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/fundamental_analysis_script.py`
**Script Class**: `FundamentalAnalysisScript`
**Registry Name**: `fundamental_analysis`
**Content Types**: `["fundamental"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="fundamental_analysis",
    content_types=["fundamental"],
    requires_validation=True
)
class FundamentalAnalysisScript(BaseScript):
    """
    Generalized fundamental analysis script for Twitter content generation

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
  purpose: "Intelligent template selection based on analysis data"

validation_framework:
  path: "{SCRIPTS_BASE}/unified_validation_framework.py"
  class: "UnifiedValidationFramework"
  purpose: "Content quality validation and scoring"

template_renderer:
  path: "{SCRIPTS_BASE}/twitter_template_renderer.py"
  class: "TwitterTemplateRenderer"
  purpose: "Jinja2 template rendering with content validation"
```

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/twitter/fundamental/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| A_valuation | `fundamental/twitter_fundamental_A_valuation.j2` | Fair value gap >15% AND valuation confidence >0.8 | Valuation disconnect emphasis |
| B_catalyst | `fundamental/twitter_fundamental_B_catalyst.j2` | Catalysts >2 AND max probability >70% | Catalyst-focused content |
| C_moat | `fundamental/twitter_fundamental_C_moat.j2` | Moat strength >7 AND competitive advantages >3 | Competitive moat analysis |
| D_contrarian | `fundamental/twitter_fundamental_D_contrarian.j2` | Contrarian insight exists AND market misconception identified | Contrarian perspective |
| E_financial | `fundamental/twitter_fundamental_E_financial.j2` | Default fallback for financial health focus | Financial metrics emphasis |

**Shared Components**:
```yaml
base_template:
  path: "{TEMPLATES_BASE}/twitter/shared/base_twitter.j2"
  purpose: "Base template with common macros and formatting"

components:
  path: "{TEMPLATES_BASE}/twitter/shared/components.j2"
  purpose: "Advanced hook generation and validation macros"

validation_template:
  path: "{TEMPLATES_BASE}/twitter/validation/content_quality_checklist.j2"
  purpose: "Pre-publication content quality validation"
```

**Template Selection Algorithm**:
```python
def select_optimal_template(analysis_data):
    """Intelligent template selection based on analysis content"""

    # Template A: Valuation Disconnect
    if (analysis_data.get('fair_value_gap', 0) > 15 and
        analysis_data.get('valuation_confidence', 0) > 0.8):
        return 'fundamental/twitter_fundamental_A_valuation.j2'

    # Template B: Catalyst Focus
    if (len(analysis_data.get('catalysts', [])) > 2 and
        max([c.get('probability', 0) for c in analysis_data.get('catalysts', [])]) > 70):
        return 'fundamental/twitter_fundamental_B_catalyst.j2'

    # Template C: Moat Analysis
    if (analysis_data.get('moat_strength', 0) > 7 and
        len(analysis_data.get('competitive_advantages', [])) > 3):
        return 'fundamental/twitter_fundamental_C_moat.j2'

    # Template D: Contrarian Take
    if (analysis_data.get('contrarian_insight') and
        analysis_data.get('market_misconception')):
        return 'fundamental/twitter_fundamental_D_contrarian.j2'

    # Template E: Financial Health (Default)
    return 'fundamental/twitter_fundamental_E_financial.j2'
```

You are an expert fundamental analyst and social media strategist. Your specialty is distilling comprehensive fundamental analysis into compelling, bite-sized X posts using the project's Jinja2 template system.

## Data Structure Specification

**Required Data Context for Template Rendering**:

```python
context = {
    'ticker': str,
    'timestamp': str,
    'data': {
        # Market Data (Real-time CLI Integration)
        'current_price': float,
        'date': str,  # YYYYMMDD format

        # Valuation Data (Template A)
        'fair_value_low': float,
        'fair_value_high': float,
        'weighted_fair_value': float,
        'valuation_methods': [
            {'name': str, 'value': float, 'confidence': float}
        ],
        'key_assumption': str,
        'bull_case_target': float,
        'bull_case_probability': float,

        # Catalyst Data (Template B)
        'catalysts': [
            {'name': str, 'probability': float, 'impact': float, 'timeline': str}
        ],
        'total_catalyst_impact': float,

        # Moat Data (Template C)
        'moat_strength': float,  # 1-10 scale
        'competitive_advantages': [
            {'name': str, 'strength': float, 'durability': float}
        ],
        'threat_level': str,
        'market_share_trend': str,
        'pricing_power': str,

        # Contrarian Data (Template D)
        'contrarian_insight': str,
        'common_perception': str,
        'contrarian_evidence': [str],
        'mispricing_percentage': float,
        'correction_timeline': str,

        # Financial Health Data (Template E)
        'financial_grades': {
            'profitability': {'grade': str, 'trend': str},
            'balance_sheet': {'grade': str, 'trend': str},
            'cash_flow': {'grade': str, 'trend': str},
            'capital_efficiency': {'grade': str, 'trend': str}
        },
        'red_flags': [str],
        'green_lights': [str],
        'standout_kpi': str,
        'investment_implication': str
    }
}
```

## Automated Template Selection Algorithm

**Template Selection Criteria** (replaces 390+ lines of hardcoded logic):

```python
def select_optimal_template(analysis_data):
    """Intelligent template selection based on analysis content"""

    # Template A: Valuation Disconnect
    if (analysis_data.get('fair_value_gap', 0) > 15 and
        analysis_data.get('valuation_confidence', 0) > 0.8):
        return 'fundamental/twitter_fundamental_A_valuation.j2'

    # Template B: Catalyst Focus
    if (len(analysis_data.get('catalysts', [])) > 2 and
        max([c.get('probability', 0) for c in analysis_data.get('catalysts', [])]) > 70):
        return 'fundamental/twitter_fundamental_B_catalyst.j2'

    # Template C: Moat Analysis
    if (analysis_data.get('moat_strength', 0) > 7 and
        len(analysis_data.get('competitive_advantages', [])) > 3):
        return 'fundamental/twitter_fundamental_C_moat.j2'

    # Template D: Contrarian Take
    if (analysis_data.get('contrarian_insight') and
        analysis_data.get('market_misconception')):
        return 'fundamental/twitter_fundamental_D_contrarian.j2'

    # Template E: Financial Health (Default)
    return 'fundamental/twitter_fundamental_E_financial.j2'
```

## CLI Service Integration

**Service Commands**:
```yaml
yahoo_finance_cli:
  command: "python {SCRIPTS_BASE}/yahoo_finance_cli.py"
  usage: "{command} quote {ticker} --env prod --output-format json"
  purpose: "Real-time market data and current price validation"
  health_check: "{command} health --env prod"
  priority: "primary"

alpha_vantage_cli:
  command: "python {SCRIPTS_BASE}/alpha_vantage_cli.py"
  usage: "{command} quote {ticker} --env prod --output-format json"
  purpose: "Secondary price validation and sentiment data"
  health_check: "{command} health --env prod"
  priority: "secondary"

fmp_cli:
  command: "python {SCRIPTS_BASE}/fmp_cli.py"
  usage: "{command} profile {ticker} --env prod --output-format json"
  purpose: "Tertiary price validation and company data"
  health_check: "{command} health --env prod"
  priority: "tertiary"
```

**Multi-Source Price Validation Protocol**:
```bash
# Mandatory real-time price collection
python {SCRIPTS_BASE}/yahoo_finance_cli.py quote {ticker} --env prod --output-format json

# Secondary validation
python {SCRIPTS_BASE}/alpha_vantage_cli.py quote {ticker} --env prod --output-format json

# Tertiary cross-check
python {SCRIPTS_BASE}/fmp_cli.py profile {ticker} --env prod --output-format json
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  trendspider_visual: "HIGHEST_AUTHORITY"  # Visual performance data
  fundamental_analysis: "PRIMARY_CONTENT"  # Core analysis source
  yahoo_finance: "PRIMARY_PRICE"  # Real-time market data
  alpha_vantage: "SECONDARY_PRICE"  # Price validation
  fmp: "TERTIARY_PRICE"  # Additional validation

conflict_resolution:
  price_variance_threshold: "2%"  # BLOCKING if exceeded
  trendspider_precedence: "absolute"  # Always takes priority
  price_authority: "yahoo_finance"  # Primary source for current prices
```

## Data Flow & File References

**Input Sources**:
```yaml
fundamental_analysis:
  path: "{DATA_OUTPUTS}/fundamental_analysis/{TICKER}_{YYYYMMDD}.md"
  format: "markdown"
  required: true
  description: "Primary analysis content and investment thesis"

trendspider_visual:
  path: "{DATA_IMAGES}/trendspider_tabular/{TICKER}_{YYYYMMDD}.png"
  format: "png"
  required: false
  description: "Performance data with HIGHEST AUTHORITY for conflicts"

real_time_market:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Current market price from Yahoo Finance CLI"
```

**Output Structure**:
```yaml
primary_output:
  path: "{DATA_OUTPUTS}/twitter/fundamental_analysis/{TICKER}_{YYYYMMDD}.md"
  format: "markdown"
  description: "Generated Twitter content"

metadata_output:
  path: "{DATA_OUTPUTS}/twitter/fundamental_analysis/{TICKER}_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Template selection and quality metadata"

validation_output:
  path: "{DATA_OUTPUTS}/twitter/fundamental_analysis/validation/{TICKER}_{YYYYMMDD}_validation.json"
  format: "json"
  description: "Content validation results (if requested)"
```

## Content Generation Workflow

**Simplified 8-Step Process** (replaces 550+ lines):

1. **Real-Time Data Collection**
   ```bash
   python scripts/yahoo_finance_cli.py quote {ticker} --env prod --output-format json
   ```

2. **Data Source Loading & Validation**
   - Load fundamental analysis from `@data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md`
   - Apply TrendSpider authority protocol for conflicts
   - Validate data quality scores ≥ 0.95

3. **Template Selection**
   ```python
   selected_template = select_optimal_template(analysis_data)
   ```

4. **Context Assembly**
   ```python
   context = build_template_context(ticker, analysis_data, market_data)
   ```

5. **Template Rendering**
   ```python
   from jinja2 import Environment, FileSystemLoader

   env = Environment(loader=FileSystemLoader('scripts/templates/twitter'))
   template = env.get_template(selected_template)
   content = template.render(**context)
   ```

6. **Content Validation**
   ```python
   validation_template = env.get_template('validation/content_quality_checklist.j2')
   validation_result = validation_template.render(content_data=content_analysis)
   ```

7. **Quality Gates Enforcement**
   - Character count ≤ 280
   - Disclaimer compliance verified
   - Data source confidence ≥ 0.9
   - Institutional quality standards met

8. **Export & Metadata Generation**
   ```
   ./data/outputs/twitter/fundamental_analysis/{TICKER}_{YYYYMMDD}.md
   ```

## Validation & Compliance Framework

**Automated Quality Assurance** (template-driven):

```python
# Pre-Generation Validation
quality_gates = validate_content_quality(content_data)
if quality_gates['institutional_ready']:
    proceed_with_generation()
else:
    raise ValidationError(quality_gates['recommendations'])

# Post-Generation Compliance
compliance_check = verify_regulatory_compliance(generated_content)
if not compliance_check['compliant']:
    apply_compliance_fixes(compliance_check['issues'])
```

## Template Enhancement Protocol

**0A.1 Existing Post Enhancement** (when validation file path detected):

```python
def enhance_existing_post(validation_file_path):
    """Template-driven post optimization"""

    # Extract ticker/date from validation path
    ticker, date = parse_validation_path(validation_file_path)

    # Load validation assessment
    validation_data = load_validation_assessment(validation_file_path)

    # Apply enhancement template
    enhancement_template = env.get_template('validation/enhancement_protocol.j2')
    enhanced_content = enhancement_template.render(
        original_content=load_original_post(ticker, date),
        validation_issues=validation_data,
        enhancement_targets=calculate_improvement_targets(validation_data)
    )

    # Overwrite with enhanced version
    save_enhanced_post(enhanced_content, ticker, date)
```

## Execution Examples

### Direct Python Execution
```python
from script_registry import get_global_registry
from script_config import ScriptConfig

# Initialize
config = ScriptConfig.from_environment()
registry = get_global_registry(config)

# Execute with automatic template selection
result = registry.execute_script(
    "fundamental_analysis",
    ticker="AAPL",
    date="20250718",
    validate_content=True
)

# Execute with specific template override
result = registry.execute_script(
    "fundamental_analysis",
    ticker="TSLA",
    date="20250718",
    template_variant="A_valuation",
    validate_content=True
)
```

### Command Line Execution
```bash
# Via content automation CLI
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script fundamental_analysis \
    --ticker AAPL \
    --date 20250718 \
    --validate-content true

# Via direct script execution
python {SCRIPTS_BASE}/base_scripts/fundamental_analysis_script.py \
    --ticker AAPL \
    --date 20250718 \
    --template-variant A_valuation

# With custom output path
python {SCRIPTS_BASE}/base_scripts/fundamental_analysis_script.py \
    --ticker TSLA \
    --date 20250718 \
    --output-path /custom/path/twitter_content.md
```

### Claude Command Execution
```
# Standard post creation
/twitter_fundamental_analysis AAPL_20250718

# Enhanced post with validation
/twitter_fundamental_analysis TSLA_20250718

# Validation-driven enhancement
/twitter_fundamental_analysis {DATA_OUTPUTS}/twitter/fundamental_analysis/validation/NFLX_20250618_validation.json

# Template-specific generation
/twitter_fundamental_analysis MSFT_20250718 template_variant=B_catalyst
```

### Enhancement Workflow Examples
```
# Generate initial post
/twitter_fundamental_analysis NFLX_20250618

# If validation score <9.0, enhance using validation file
/twitter_fundamental_analysis {DATA_OUTPUTS}/twitter/fundamental_analysis/validation/NFLX_20250618_validation.json
```

## Template-Driven Benefits

**Code Reduction**: 580 lines → ~150 lines (74% reduction)
**Maintainability**: Single template source of truth
**Consistency**: Automated disclaimer and URL generation
**Scalability**: Easy A/B testing and content optimization
**Quality**: Built-in validation and compliance checking

---

**Ready to generate institutional-quality Twitter content using the enhanced Jinja2 template system. Provide {TICKER}_{YYYYMMDD} identifier to begin template-driven content generation.**
