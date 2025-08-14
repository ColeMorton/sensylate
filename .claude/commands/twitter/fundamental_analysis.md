# Fundamental Analysis Twitter Synthesis Command

**Command Classification**: 📊 **DASV Synthesis Command**
**DASV Phase**: Synthesis (Twitter Sub-Domain)
**Input Phase**: Synthesis (Fundamental Analysis Domain)
**Quality Requirement**: ≥9.0/10.0 synthesis confidence
**Enhancement Target**: ≥9.5/10.0 with validation enhancement
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-08-11)*
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

You are a **fundamental analysis data processor** specialized in extracting domain-specific insights from comprehensive fundamental analysis and preparing structured data for the twitter_writer agent.

**Separation of Concerns:**
- **This Command**: Domain data processing, DASV compliance, template selection
- **Twitter Writer Agent**: Content creation, hooks, engagement optimization
- **Integration**: Structured data handoff for optimal content generation

## DASV Synthesis Framework Integration

### Input Validation Requirements
```python
def validate_source_synthesis(source_path):
    """Validate fundamental analysis synthesis input"""

    # Check source synthesis exists and is current
    if not source_path.exists() or data_age > timedelta(hours=48):
        raise SynthesisStalenessException("Source synthesis too old or missing")

    # Verify source synthesis quality
    if source_confidence < 0.9:
        raise QualityThresholdException("Source synthesis below institutional grade")

    # Validate schema compliance
    if not validate_fundamental_schema(source_path):
        raise SchemaValidationException("Source synthesis schema invalid")
```

### Synthesis Confidence Calculation
```python
def calculate_twitter_synthesis_confidence(source_conf, data_quality, template_fit):
    """Calculate Twitter-specific synthesis confidence"""

    # Base confidence from source synthesis
    base_confidence = source_conf

    # Apply transformation factors
    data_extraction_quality = assess_data_extraction_completeness()
    template_selection_accuracy = assess_template_fit_score()
    market_context_currency = assess_market_data_freshness()

    # Calculate Twitter synthesis confidence
    twitter_confidence = (base_confidence *
                         data_extraction_quality *
                         template_selection_accuracy *
                         market_context_currency)

    # Enforce institutional threshold
    if twitter_confidence < 0.9:
        raise SynthesisQualityException(f"Twitter synthesis confidence {twitter_confidence} below institutional threshold")

    return twitter_confidence
```

## Fundamental Analysis Data Processing

### Domain-Specific Data Extraction Pipeline

**1. Source Synthesis Loading & Validation**:
```python
def load_fundamental_synthesis(ticker, date):
    """Load and validate source fundamental analysis synthesis"""

    source_path = f"data/outputs/fundamental_analysis/{ticker}_{date}.md"

    # DASV Input Validation
    validate_source_synthesis(source_path)

    # Extract synthesis data
    synthesis_data = parse_fundamental_synthesis(source_path)

    # Validate data completeness
    required_sections = ['investment_thesis', 'valuation_analysis', 'financial_health', 'risk_assessment']
    validate_data_completeness(synthesis_data, required_sections)

    return synthesis_data
```

**2. Template Selection Logic**:
```python
def select_optimal_template(fundamental_data):
    """Domain-specific template selection based on fundamental insights"""

    # Template A: Valuation Disconnect
    if (fundamental_data.get('fair_value_gap', 0) > 15 and
        fundamental_data.get('valuation_confidence', 0) > 0.8):
        return 'A_valuation'

    # Template B: Catalyst Focus
    if (len(fundamental_data.get('catalysts', [])) > 2 and
        max([c.get('probability', 0) for c in fundamental_data.get('catalysts', [])]) > 70):
        return 'B_catalyst'

    # Template C: Moat Analysis
    if (fundamental_data.get('moat_strength', 0) > 7 and
        len(fundamental_data.get('competitive_advantages', [])) > 3):
        return 'C_moat'

    # Template D: Contrarian Take
    if (fundamental_data.get('contrarian_insight') and
        fundamental_data.get('market_misconception')):
        return 'D_contrarian'

    # Template E: Financial Health (Default)
    return 'E_financial'
```

**3. Market Context Integration**:
```python
def integrate_market_context(ticker, fundamental_data):
    """Integrate real-time market data for context validation"""

    # Real-time price collection (mandatory)
    current_market = collect_real_time_data(ticker)

    # Validate price consistency with analysis
    price_variance = calculate_price_variance(fundamental_data['price'], current_market['price'])
    if price_variance > 0.02:  # 2% threshold
        log_price_variance_warning(price_variance)

    # Update market context
    fundamental_data['current_price'] = current_market['price']
    fundamental_data['market_context'] = current_market['context']

    return fundamental_data
```

## Twitter Writer Agent Integration

### Structured Data Handoff Protocol
```json
{
  "command_type": "fundamental_analysis",
  "synthesis_confidence": 0.95,
  "template_recommendation": "A_valuation|B_catalyst|C_moat|D_contrarian|E_financial",
  "ticker": "AAPL",
  "date": "20250811",
  "domain_data": {
    "investment_thesis": "extracted_thesis_summary",
    "key_metrics": {
      "fair_value_range": "$180-$220",
      "current_price": "$198.50",
      "valuation_gap": "15.2%",
      "confidence": 0.92
    },
    "valuation_insights": {
      "dcf_value": "$205",
      "comparables_value": "$195",
      "technical_support": "$185"
    },
    "catalyst_analysis": [
      {"event": "Q1 earnings", "probability": 0.85, "impact": "high", "timeline": "2 weeks"}
    ],
    "competitive_positioning": {
      "moat_strength": 8.5,
      "competitive_advantages": ["ecosystem", "brand", "innovation"],
      "market_position": "dominant"
    },
    "financial_health": {
      "overall_grade": "A-",
      "profitability": "A",
      "balance_sheet": "A-",
      "cash_flow": "A"
    },
    "risk_factors": ["regulatory", "competition", "market_cycles"]
  },
  "engagement_parameters": {
    "urgency": "standard",
    "audience": "retail_investors",
    "complexity": "intermediate"
  },
  "compliance_requirements": {
    "disclaimers": ["investment_advice", "past_performance"],
    "risk_factors": ["market_volatility", "analysis_limitations"],
    "transparency_level": "standard"
  },
  "quality_metadata": {
    "source_confidence": 0.92,
    "data_freshness": "2025-08-11T10:30:00Z",
    "validation_status": "passed",
    "template_rationale": "Selected A_valuation due to 15.2% fair value gap with high confidence"
  }
}
```

### Command Execution Flow
1. **Load and validate** source fundamental analysis synthesis
2. **Extract domain-specific** insights and metrics
3. **Select optimal template** based on fundamental analysis characteristics
4. **Calculate Twitter synthesis confidence** with DASV standards
5. **Prepare structured data** for twitter_writer agent handoff
6. **Use the twitter_writer sub-agent** to create engaging Twitter content from the structured fundamental analysis data
7. **Validate output quality** and apply enhancements if needed
8. **Export final content** with metadata and quality metrics

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

## DASV Synthesis Workflow

**Streamlined 6-Phase Process**:

### Phase 1: Input Validation
```python
def phase_1_input_validation(ticker, date):
    """DASV-compliant input validation"""

    # Load source synthesis
    source_path = f"data/outputs/fundamental_analysis/{ticker}_{date}.md"
    synthesis_data = load_fundamental_synthesis(ticker, date)

    # Validate DASV compliance
    if synthesis_data['confidence'] < 0.9:
        raise QualityThresholdException("Source synthesis below institutional grade")

    # Check data freshness
    if data_age(synthesis_data) > timedelta(hours=48):
        raise DataStalenessException("Source synthesis data too old")

    return synthesis_data
```

### Phase 2: Domain Data Processing
```python
def phase_2_domain_processing(synthesis_data):
    """Extract fundamental analysis insights"""

    # Extract domain-specific insights
    investment_thesis = extract_investment_thesis(synthesis_data)
    valuation_analysis = extract_valuation_insights(synthesis_data)
    financial_health = extract_financial_grades(synthesis_data)
    risk_assessment = extract_risk_factors(synthesis_data)

    # Validate completeness
    validate_extraction_completeness(investment_thesis, valuation_analysis, financial_health, risk_assessment)

    return processed_data
```

### Phase 3: Template Selection & Market Integration
```python
def phase_3_template_selection(processed_data, ticker):
    """Domain-aware template selection with market context"""

    # Integrate real-time market data
    current_market_data = integrate_market_context(ticker, processed_data)

    # Select optimal template
    template_selection = select_optimal_template(current_market_data)

    # Validate template fit
    template_fit_score = assess_template_fit_score(template_selection, current_market_data)

    return template_selection, current_market_data, template_fit_score
```

### Phase 4: Synthesis Confidence Calculation
```python
def phase_4_confidence_calculation(source_conf, data_quality, template_fit):
    """Calculate Twitter synthesis confidence with DASV standards"""

    twitter_confidence = calculate_twitter_synthesis_confidence(source_conf, data_quality, template_fit)

    # Enforce institutional threshold
    if twitter_confidence < 0.9:
        raise SynthesisQualityException(f"Twitter confidence {twitter_confidence:.3f} below institutional threshold")

    return twitter_confidence
```

### Phase 5: Twitter Writer Integration
```python
def phase_5_twitter_writer_handoff(processed_data, template_selection, twitter_confidence):
    """Prepare structured data for twitter_writer sub-agent"""

    # Prepare standardized handoff structure
    writer_input = prepare_twitter_writer_data(processed_data, template_selection, twitter_confidence)

    # Use the twitter_writer sub-agent to create content
    # twitter_writer handles: hooks, engagement, character optimization, platform formatting

    return writer_input
```

### Phase 6: Validation & Enhancement
```python
def phase_6_validation_enhancement(twitter_output, validation_file=None):
    """Apply DASV validation and enhancement protocols"""

    # Check for validation enhancement opportunity
    if validation_file and validation_file.exists():
        # Apply systematic enhancement targeting 9.5+ confidence
        enhanced_output = apply_validation_enhancement(twitter_output, validation_file)
        return enhanced_output

    # Standard validation
    validate_output_quality(twitter_output)
    return twitter_output
```

## DASV Validation & Enhancement Framework

### Pre-Synthesis Quality Gates
```python
def validate_pre_synthesis_requirements(synthesis_data):
    """Enforce DASV quality gates before Twitter synthesis"""

    quality_checks = {
        'source_confidence': synthesis_data['confidence'] >= 0.9,
        'data_completeness': validate_required_sections(synthesis_data),
        'data_freshness': data_age(synthesis_data) <= timedelta(hours=48),
        'schema_compliance': validate_fundamental_schema(synthesis_data)
    }

    # Fail-fast on any quality gate failure
    for check, passed in quality_checks.items():
        if not passed:
            raise QualityGateException(f"Pre-synthesis quality gate failed: {check}")

    return True
```

### Post-Synthesis Validation
```python
def validate_twitter_synthesis_output(twitter_output, expected_confidence):
    """Validate Twitter synthesis meets DASV standards"""

    validation_results = {
        'synthesis_confidence': twitter_output['metadata']['synthesis_confidence'] >= expected_confidence,
        'content_quality': assess_content_institutional_quality(twitter_output['content']),
        'template_compliance': verify_template_adherence(twitter_output),
        'evidence_integration': validate_source_traceability(twitter_output)
    }

    # Calculate aggregate validation score
    validation_score = sum(validation_results.values()) / len(validation_results)

    if validation_score < 0.9:
        raise ValidationException(f"Twitter synthesis validation score {validation_score:.3f} below institutional threshold")

    return validation_score
```

### Validation-Driven Enhancement Protocol
```python
def apply_validation_enhancement(ticker, date, validation_file_path):
    """DASV-compliant systematic enhancement for existing posts"""

    # Parse validation assessment
    validation_data = load_validation_assessment(validation_file_path)

    # Load original synthesis and Twitter output
    original_synthesis = load_fundamental_synthesis(ticker, date)
    original_twitter_output = load_existing_twitter_output(ticker, date)

    # Identify enhancement opportunities
    enhancement_targets = {
        'synthesis_confidence_gap': 0.95 - original_twitter_output['synthesis_confidence'],
        'template_compliance_issues': validation_data.get('template_compliance_issues', []),
        'content_quality_gaps': validation_data.get('content_quality_issues', []),
        'evidence_integration_needs': validation_data.get('evidence_gaps', [])
    }

    # Re-process with enhancement focus
    enhanced_data = enhance_domain_processing(original_synthesis, enhancement_targets)
    enhanced_template_selection = refine_template_selection(enhanced_data, validation_data)
    enhanced_confidence = calculate_enhanced_confidence(enhanced_data)

    # Prepare enhanced data for twitter_writer sub-agent
    enhanced_writer_input = prepare_twitter_writer_data(enhanced_data, enhanced_template_selection, enhanced_confidence)

    # Use twitter_writer sub-agent to generate enhanced content targeting 9.5+ confidence

    return enhanced_writer_input
```

### Enhancement Quality Targets
```python
def validate_enhancement_success(enhanced_output, original_confidence):
    """Ensure enhancement achieves quality improvement"""

    enhancement_requirements = {
        'confidence_improvement': enhanced_output['synthesis_confidence'] > original_confidence,
        'institutional_excellence': enhanced_output['synthesis_confidence'] >= 0.95,
        'template_compliance': verify_enhanced_template_compliance(enhanced_output),
        'content_optimization': assess_content_enhancement_quality(enhanced_output)
    }

    enhancement_success = all(enhancement_requirements.values())

    if not enhancement_success:
        failed_requirements = [req for req, passed in enhancement_requirements.items() if not passed]
        raise EnhancementException(f"Enhancement failed requirements: {failed_requirements}")

    return True
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
# Standard Twitter synthesis from fundamental analysis
/twitter_fundamental_analysis AAPL_20250811

# DASV enhancement with validation file
/twitter_fundamental_analysis {DATA_OUTPUTS}/twitter/fundamental_analysis/validation/TSLA_20250811_validation.json

# Template-specific generation (domain logic override)
/twitter_fundamental_analysis MSFT_20250811 template_variant=B_catalyst
```

### DASV Enhancement Workflow
```
# Phase 1: Generate Twitter synthesis
/twitter_fundamental_analysis NFLX_20250811

# Phase 2: If synthesis confidence <9.5, apply validation enhancement
/twitter_fundamental_analysis {DATA_OUTPUTS}/twitter/fundamental_analysis/validation/NFLX_20250811_validation.json

# Phase 3: Validate institutional excellence achieved (≥9.5/10.0)
```

## DASV Architecture Benefits

**Clean Separation of Concerns**:
- **Domain Focus**: Command handles fundamental analysis data processing only
- **Content Delegation**: Twitter_writer sub-agent handles all content creation
- **Quality Assurance**: DASV framework ensures institutional standards
- **Enhancement Protocol**: Systematic improvement targeting 9.5+ confidence

**Institutional Quality Standards**:
- **Source Validation**: ≥9.0/10.0 synthesis confidence required
- **Data Freshness**: ≤48 hours staleness threshold
- **Template Selection**: Domain-specific logic based on fundamental insights
- **Fail-Fast Quality**: Immediate rejection of substandard inputs

**Integration Excellence**:
- **Twitter Writer**: Structured data handoff for optimal content generation
- **Real-Time Data**: Market context integration for currency
- **Enhancement Loop**: Validation-driven improvement workflow
- **Audit Trail**: Complete quality metrics and decision rationale

---

## Command Usage

**Execute Twitter synthesis from fundamental analysis:**
```
/twitter_fundamental_analysis {TICKER}_{YYYYMMDD}
```

**Processing Flow:**
1. **Load & validate** source fundamental analysis synthesis (≥9.0 confidence)
2. **Extract domain data** (thesis, valuation, health, risks, catalysts)
3. **Select template** based on fundamental analysis characteristics
4. **Calculate Twitter synthesis confidence** with DASV standards
5. **Use twitter_writer sub-agent** to create engaging content from structured data
6. **Apply enhancement** if validation file exists (target: ≥9.5 confidence)
7. **Export results** with complete quality metrics and traceability

**Ready to generate DASV-compliant Twitter synthesis from institutional-grade fundamental analysis. Provide {TICKER}_{YYYYMMDD} identifier to begin domain-focused data processing and twitter_writer integration.**
