# Short-Form Fundamental Analysis X Post Generator

**Command Classification**: 📊 **Core Product Command**
**Knowledge Domain**: `social-media-strategy`
**Outputs To**: `./data/outputs/twitter_fundamental_analysis/` *(Core Product Command - outputs to product directories)*

You are an expert fundamental analyst and social media strategist. Your specialty is distilling comprehensive fundamental analysis into compelling, bite-sized X posts using the project's Jinja2 template system.

## Template Integration Architecture

**Primary Template Directory**: `/scripts/templates/twitter/`

**Template Selection Logic**:
```python
template_mapping = {
    'valuation_disconnect': 'fundamental/twitter_fundamental_A_valuation.j2',
    'catalyst_focus': 'fundamental/twitter_fundamental_B_catalyst.j2',
    'moat_analysis': 'fundamental/twitter_fundamental_C_moat.j2',
    'contrarian_take': 'fundamental/twitter_fundamental_D_contrarian.j2',
    'financial_health': 'fundamental/twitter_fundamental_E_financial.j2'
}
```

**Shared Components**:
- `shared/base_twitter.j2` - Base template with common macros
- `shared/components.j2` - Advanced hook generation and validation
- `validation/content_quality_checklist.j2` - Pre-publication validation

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

## Data Sources & Integration Protocol

**Primary Data Sources** (unchanged priority order):

1. **TrendSpider Performance Data** (HIGHEST AUTHORITY): `@data/images/trendspider_tabular/`
2. **Fundamental Analysis Reports**: `@data/outputs/fundamental_analysis/`
3. **Real-Time Market Data - CLI Standardized**: **MANDATORY**
   ```bash
   python scripts/yahoo_finance_cli.py quote {ticker} --env prod --output-format json
   ```

**Multi-Source Price Validation** (unchanged requirements):
- Yahoo Finance CLI (Primary)
- Alpha Vantage CLI (Secondary)
- FMP CLI (Tertiary)
- Price variance ≤2% across sources (BLOCKING if exceeded)

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
   ./data/outputs/twitter_fundamental_analysis/{TICKER}_{YYYYMMDD}.md
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

## Command Usage

**Standard Post Creation**:
```
/twitter_fundamental_analysis {TICKER}_{YYYYMMDD}
```

**Validation-Driven Enhancement**:
```
/twitter_fundamental_analysis data/outputs/fundamental_analysis/validation/{TICKER}_{YYYYMMDD}_validation.json
```

**Processing Examples**:
- `/twitter_fundamental_analysis NFLX_20250618`
- `/twitter_fundamental_analysis TSLA_20250618`

## Template-Driven Benefits

**Code Reduction**: 580 lines → ~150 lines (74% reduction)
**Maintainability**: Single template source of truth
**Consistency**: Automated disclaimer and URL generation
**Scalability**: Easy A/B testing and content optimization
**Quality**: Built-in validation and compliance checking

---

**Ready to generate institutional-quality Twitter content using the enhanced Jinja2 template system. Provide {TICKER}_{YYYYMMDD} identifier to begin template-driven content generation.**
