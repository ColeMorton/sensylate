# Macro-Economic Analysis Twitter Synthesis Command

**Command Classification**: 📊 **DASV Synthesis Command**
**DASV Phase**: Synthesis (Twitter Sub-Domain)
**Input Phase**: Synthesis (Macro-Economic Analysis Domain)
**Quality Requirement**: ≥9.0/10.0 synthesis confidence
**Enhancement Target**: ≥9.5/10.0 with validation enhancement
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-08-11)*
**Outputs To**: `{DATA_OUTPUTS}/macro_analysis/twitter/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/macro_twitter_script.py`
**Script Class**: `MacroTwitterScript`
**Registry Name**: `macro_twitter`
**Content Types**: `["macro_twitter"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="macro_twitter",
    content_types=["macro_twitter"],
    requires_validation=True
)
class MacroTwitterScript(BaseScript):
    """
    Macro-economic analysis Twitter content generation script

    Parameters:
        region (str): Region identifier (US, EUROPE, ASIA, AMERICAS, GLOBAL)
        date (str): Analysis date in YYYYMMDD format
        template_variant (Optional[str]): Specific template to use
        validation_file (Optional[str]): Path to validation file for enhancement
        validate_content (bool): Whether to validate generated content
    """
```

**Supporting Components**:
```yaml
macro_data_analyzer:
  path: "{SCRIPTS_BASE}/macro_analysis/macro_data_analyzer.py"
  class: "MacroDataAnalyzer"
  purpose: "Macro-economic analysis data extraction and validation"

economic_indicators_collector:
  path: "{SCRIPTS_BASE}/economic_data/economic_indicators_collector.py"
  class: "EconomicIndicatorsCollector"
  purpose: "Real-time economic indicators collection (GDP, CPI, employment)"

cross_regional_analyzer:
  path: "{SCRIPTS_BASE}/economic_data/cross_regional_analyzer.py"
  class: "CrossRegionalAnalyzer"
  purpose: "Cross-regional economic comparison and correlation analysis"

twitter_template_renderer:
  path: "{SCRIPTS_BASE}/twitter_template_renderer.py"
  class: "TwitterTemplateRenderer"
  purpose: "Jinja2 template rendering with macro-economic optimization"
```

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/twitter/macro/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| business_cycle_analysis | `macro/twitter_business_cycle.j2` | Business cycle transition probability >0.7 AND recession risk assessment | Economic cycle positioning and outlook |
| cross_regional_comparison | `macro/twitter_cross_regional.j2` | Multi-region analysis AND GDP growth differential >100bps | Regional economic comparison and positioning |
| monetary_policy | `macro/twitter_monetary_policy.j2` | Policy change probability >0.6 AND yield curve analysis | Central bank policy and market implications |
| economic_outlook | `macro/twitter_economic_outlook.j2` | GDP/employment/inflation forecasts AND confidence >0.85 | Economic forecast and trajectory analysis |
| economic_indicators | `macro/twitter_economic_indicators.j2` | Default fallback for economic dashboard | Key economic metrics and trends |

**Shared Components**:
```yaml
macro_base_template:
  path: "{TEMPLATES_BASE}/twitter/shared/base_twitter.j2"
  purpose: "Base template with common macros and economic formatting"

macro_components:
  path: "{TEMPLATES_BASE}/twitter/shared/macro_components.j2"
  purpose: "Macro-specific components for economic indicators and policy analysis"

compliance_template:
  path: "{TEMPLATES_BASE}/twitter/validation/macro_compliance.j2"
  purpose: "Economic forecast compliance and disclaimer validation"
```

**Template Selection Algorithm**:
```python
def select_macro_template(macro_analysis_data):
    """Select optimal template for macro Twitter content"""

    # Business cycle template for economic transition analysis
    if (macro_analysis_data.get('business_cycle_transition_probability', 0) > 0.7 and
        macro_analysis_data.get('recession_risk_assessment', False)):
        return 'macro/twitter_business_cycle.j2'

    # Cross-regional comparison for growth differentials
    elif (macro_analysis_data.get('gdp_growth_differential', 0) > 100 and
          macro_analysis_data.get('multi_region_analysis', False)):
        return 'macro/twitter_cross_regional.j2'

    # Monetary policy for central bank focus
    elif (macro_analysis_data.get('policy_change_probability', 0) > 0.6 and
          macro_analysis_data.get('yield_curve_analysis', False)):
        return 'macro/twitter_monetary_policy.j2'

    # Economic outlook for forecast focus
    elif (macro_analysis_data.get('economic_forecast_confidence', 0) > 0.85 and
          macro_analysis_data.get('gdp_employment_inflation_data', False)):
        return 'macro/twitter_economic_outlook.j2'

    # Default economic indicators dashboard
    return 'macro/twitter_economic_indicators.j2'
```

## CLI Service Integration

**Service Commands**:
```yaml
fred_economic_cli:
  command: "python {SCRIPTS_BASE}/fred_economic_cli.py"
  usage: "{command} indicators GDP,GDPC1,PAYEMS,UNRATE,CPIAUCSL,FEDFUNDS,DGS10,DGS2 --env prod --output-format json"
  purpose: "Comprehensive economic indicators for macro analysis"
  health_check: "{command} health --env prod"
  priority: "primary"

imf_cli:
  command: "python {SCRIPTS_BASE}/imf_cli.py"
  usage: "{command} regional-indicators {region} --env prod --output-format json"
  purpose: "International economic data and cross-regional comparisons"
  health_check: "{command} health --env prod"
  priority: "primary"

central_bank_cli:
  command: "python {SCRIPTS_BASE}/central_bank_cli.py"
  usage: "{command} policy-analysis {region} --env prod --output-format json"
  purpose: "Central bank policy data and monetary analysis"
  health_check: "{command} health --env prod"
  priority: "secondary"

alpha_vantage_cli:
  command: "python {SCRIPTS_BASE}/alpha_vantage_cli.py"
  usage: "{command} economic-calendar {region} --env prod --output-format json"
  purpose: "Economic calendar events and market expectations"
  health_check: "{command} health --env prod"
  priority: "secondary"

economic_forecasts_cli:
  command: "python {SCRIPTS_BASE}/economic_forecasts_cli.py"
  usage: "{command} consensus-forecasts {region} --env prod --output-format json"
  purpose: "Economic consensus forecasts and projections"
  health_check: "{command} health --env prod"
  priority: "tertiary"
```

**Macro Twitter Integration Protocol**:
```bash
# Real-time economic indicators collection
python {SCRIPTS_BASE}/fred_economic_cli.py indicators GDP,GDPC1,PAYEMS,UNRATE,CPIAUCSL,FEDFUNDS,DGS10,DGS2 --env prod --output-format json

# Cross-regional economic data
python {SCRIPTS_BASE}/imf_cli.py regional-indicators {region} --env prod --output-format json

# Central bank policy analysis
python {SCRIPTS_BASE}/central_bank_cli.py policy-analysis {region} --env prod --output-format json

# Economic calendar and consensus
python {SCRIPTS_BASE}/economic_forecasts_cli.py consensus-forecasts {region} --env prod --output-format json
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  macro_analysis: "HIGHEST_AUTHORITY"  # Primary macro analysis documents
  fred_data: "ECONOMIC_AUTHORITY"  # Real-time economic indicators
  imf_data: "INTERNATIONAL_AUTHORITY"  # Cross-regional economic context
  central_bank_data: "POLICY_AUTHORITY"  # Monetary policy data

conflict_resolution:
  macro_precedence: "macro_analysis_primary"  # Macro analysis takes priority
  indicator_authority: "fred_primary_imf_secondary"  # FRED for US, IMF for international
  data_staleness: "24_hours"  # Maximum age for economic data
  variance_threshold: "2%"  # BLOCKING if economic data variance exceeds
  action: "fail_fast_on_conflict"  # Resolution strategy
```

## Data Flow & File References

**Input Sources**:
```yaml
macro_analysis_document:
  path: "{DATA_OUTPUTS}/macro_analysis/{REGION}_{YYYYMMDD}.md"
  format: "markdown"
  required: true
  description: "Primary macro analysis with economic thesis and business cycle assessment"

economic_indicators:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Real-time economic indicators (GDP, CPI, employment, Fed Funds)"

cross_regional_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Cross-regional economic comparison data from IMF"

central_bank_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: false
  description: "Central bank policy data and monetary policy analysis"

validation_file:
  path: "{DATA_OUTPUTS}/macro_analysis/twitter/validation/{REGION}_{YYYYMMDD}_validation.json"
  format: "json"
  required: false
  description: "Validation file for post enhancement workflow"
```

**Output Structure**:
```yaml
primary_output:
  path: "{DATA_OUTPUTS}/macro_analysis/twitter/{REGION}_{YYYYMMDD}.md"
  format: "markdown"
  description: "Generated macro Twitter content ready for posting"

metadata_output:
  path: "{DATA_OUTPUTS}/macro_analysis/twitter/{REGION}_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Template selection metadata and quality assurance metrics"

validation_output:
  path: "{DATA_OUTPUTS}/macro_analysis/twitter/validation/{REGION}_{YYYYMMDD}_validation.json"
  format: "json"
  description: "Content validation results and enhancement recommendations"

blog_url_output:
  path: "{DATA_OUTPUTS}/macro_analysis/twitter/{REGION}_{YYYYMMDD}_blog_url.txt"
  format: "text"
  description: "Generated blog URL for full macro analysis access"
```

**Data Dependencies**:
```yaml
content_generation_flow:
  data_validation:
    - "macro analysis confidence ≥ 0.9"
    - "economic indicators currency ≤ 24 hours"
    - "cross-regional data currency ≤ 24 hours"
    - "economic data variance ≤ 2%"

  template_selection:
    - "macro analysis content evaluation"
    - "business cycle positioning assessment"
    - "cross-regional comparison determination"
    - "economic forecast availability check"

  content_optimization:
    - "Twitter character limit compliance"
    - "economic forecast disclaimer inclusion"
    - "blog URL generation and validation"
    - "institutional quality standards verification"
```

## Execution Examples

### Direct Python Execution
```python
from script_registry import get_global_registry
from script_config import ScriptConfig

# Initialize
config = ScriptConfig.from_environment()
registry = get_global_registry(config)

# Execute macro Twitter content generation
result = registry.execute_script(
    "macro_twitter",
    region="US",
    date="20250718",
    validate_content=True
)

# Execute with specific template override
result = registry.execute_script(
    "macro_twitter",
    region="GLOBAL",
    date="20250718",
    template_variant="business_cycle_analysis",
    validate_content=True
)

# Execute post enhancement from validation file
result = registry.execute_script(
    "macro_twitter",
    validation_file="macro_analysis/twitter/validation/US_20250718_validation.json"
)
```

### Command Line Execution
```bash
# Via content automation CLI
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script macro_twitter \
    --region US \
    --date 20250718 \
    --validate-content true

# Via direct script execution
python {SCRIPTS_BASE}/base_scripts/macro_twitter_script.py \
    --region EUROPE \
    --date 20250718 \
    --template-variant cross_regional_comparison

# Post enhancement workflow
python {SCRIPTS_BASE}/base_scripts/macro_twitter_script.py \
    --validation-file "{DATA_OUTPUTS}/macro_analysis/twitter/validation/GLOBAL_20250718_validation.json"

# With custom economic context
python {SCRIPTS_BASE}/base_scripts/macro_twitter_script.py \
    --region ASIA \
    --date 20250718 \
    --economic-context-override true
```

### Claude Command Execution
```
# Standard macro Twitter content generation
/macro_analysis:twitter US_20250718

# European macro analysis
/macro_analysis:twitter EUROPE_20250718

# Global macro with validation
/macro_analysis:twitter GLOBAL_20250718

# Post enhancement using validation file
/macro_analysis:twitter {DATA_OUTPUTS}/macro_analysis/twitter/validation/US_20250718_validation.json

# Template-specific generation
/macro_analysis:twitter ASIA_20250718 template_variant=monetary_policy
```

### Macro Analysis Workflow Examples
```
# US macro analysis workflow
/macro_analysis:twitter US_20250718

# Cross-regional comparison workflow
/macro_analysis:twitter GLOBAL_20250718 template_variant=cross_regional_comparison

# Business cycle analysis
/macro_analysis:twitter US_20250718 template_variant=business_cycle_analysis

# Post validation and enhancement
/macro_analysis:twitter US_20250718
# → If validation score <9.0, enhance using:
/macro_analysis:twitter {DATA_OUTPUTS}/macro_analysis/twitter/validation/US_20250718_validation.json
```

You are a **macro-economic analysis data processor** specialized in extracting domain-specific insights from comprehensive macro-economic analysis and preparing structured data for the twitter_writer agent.

**Separation of Concerns:**
- **This Command**: Domain data processing, DASV compliance, template selection
- **Twitter Writer Agent**: Content creation, hooks, engagement optimization
- **Integration**: Structured data handoff for optimal content generation

## DASV Synthesis Framework Integration

### Macro-Specific Input Validation
```python
def validate_macro_synthesis(source_path):
    """Validate macro analysis synthesis input"""

    # Check source synthesis exists and is current
    if not source_path.exists() or data_age > timedelta(hours=48):
        raise SynthesisStalenessException("Source macro synthesis too old or missing")

    # Verify source synthesis quality
    if source_confidence < 0.9:
        raise QualityThresholdException("Source macro synthesis below institutional grade")

    # Validate macro-specific schema
    if not validate_macro_schema(source_path):
        raise SchemaValidationException("Source macro synthesis schema invalid")
```

### Macro Twitter Synthesis Confidence
```python
def calculate_macro_synthesis_confidence(source_conf, cross_regional_data, economic_integration):
    """Calculate macro-specific Twitter synthesis confidence"""

    # Base confidence from source synthesis
    base_confidence = source_conf

    # Apply macro-specific factors
    cross_regional_consistency = assess_regional_correlation_accuracy()
    economic_data_integration = assess_economic_indicators_quality()
    business_cycle_precision = assess_cycle_positioning_accuracy()
    policy_analysis_clarity = assess_monetary_policy_quality()

    # Calculate macro Twitter synthesis confidence
    macro_confidence = (base_confidence *
                       cross_regional_consistency *
                       economic_data_integration *
                       business_cycle_precision *
                       policy_analysis_clarity)

    # Enforce institutional threshold
    if macro_confidence < 0.9:
        raise SynthesisQualityException(f"Macro synthesis confidence {macro_confidence:.3f} below institutional threshold")

    return macro_confidence
```

## Phase 0A: Existing Post Enhancement Protocol

**0A.1 Validation File Discovery**
```
EXISTING POST IMPROVEMENT WORKFLOW:
1. Check input pattern for validation file path:
   → Pattern: {DATA_OUTPUTS}/macro_analysis/twitter/validation/{REGION}_{YYYYMMDD}_validation.json
   → Alternative: {DATA_OUTPUTS}/macro_analysis/validation/{REGION}_{YYYYMMDD}_validation.json
   → Extract REGION_YYYYMMDD from validation file path

2. If validation file path provided:
   → ROLE CHANGE: From "new post creator" to "Twitter macro post optimization specialist"
   → OBJECTIVE: Improve post engagement, accuracy, and compliance through systematic enhancement
   → METHOD: Examination → Validation → Optimization → Validation-Driven Improvement

3. If standard REGION_YYYYMMDD format provided:
   → Proceed with standard new post creation workflow (Data Sources & Integration onwards)
```

**0A.2 Post Enhancement Workflow (When Validation File Path Detected)**
```
SYSTEMATIC ENHANCEMENT PROCESS:
Step 1: Examine Existing Post
   → Read the original post file: {REGION}_{YYYYMMDD}.md
   → Extract current template selection, hook effectiveness, and content structure
   → Identify data sources used and accuracy claims
   → Map engagement elements and character count optimization

Step 2: Examine Validation Assessment
   → Read validation file: macro_analysis/twitter/validation/{REGION}_{YYYYMMDD}_validation.json
   → Focus on economic data accuracy issues and content improvement areas
   → Extract cross-regional comparison discrepancies and economic indicator conflicts
   → Note business cycle context concerns and disclaimer requirements

Step 3: Data Source Conflict Resolution
   → Apply macro analysis authority protocol for data discrepancies
   → Re-analyze economic indicators as authoritative source for data
   → Update any conflicting economic metrics using macro analysis data
   → Cross-validate with cross-regional indicators for consistency checking

Step 4: Enhancement Implementation
   → Address each validation point systematically
   → Strengthen explicit disclaimers and forecast language (not just implied)
   → Improve data source attribution and confidence levels
   → Enhance professional presentation standards
   → Update real-time data integration and economic context
   → Apply institutional quality standards throughout content

Step 5: Production-Ready Post Output
   → OVERWRITE original post file: {REGION}_{YYYYMMDD}.md
   → Seamlessly integrate all improvements with validation-driven enhancements
   → Maintain engaging Twitter format without enhancement artifacts
   → Ensure post meets institutional quality standards
   → Include explicit disclaimers and data source attribution
   → Deliver publication-ready social media content with enhanced compliance
```

**0A.3 Validation-Driven Enhancement Standards**
```
INSTITUTIONAL QUALITY POST TARGETS:
- Data Authority Compliance: Macro analysis data takes precedence over conflicting sources
- Explicit Disclaimer Integration: Clear economic forecast disclaimers, not just implied
- Content Accuracy Verification: Cross-reference all claims with authoritative sources
- Professional Presentation Standards: Meet institutional formatting requirements
- Economic Context Resolution: Address business cycle discrepancies systematically
- Compliance Enhancement: Strengthen forecast disclaimers and uncertainty language

VALIDATION-DRIVEN SUCCESS CRITERIA:
□ Macro analysis authority protocol applied for data discrepancies
□ Explicit disclaimers integrated (economic forecasts, data limitations, uncertainty)
□ Content improvement areas from validation systematically addressed
□ Business cycle context concerns resolved through data source prioritization
□ Professional presentation standards enhanced throughout content
□ Data source attribution and confidence levels clearly specified
□ All economic claims verified against highest authority sources
□ Institutional quality standards maintained while preserving engagement
```

## Data Sources & Integration

**Primary Data Sources (in priority order):**

1. **Macro Analysis Reports** (PRIMARY): `@{DATA_OUTPUTS}/macro_analysis/`
   - **PRIORITY SOURCE**: Comprehensive macro analysis files (REGION_YYYYMMDD.md)
   - Economic thesis, business cycle assessment, cross-regional positioning
   - Policy analysis, economic indicator integration
   - Economic forecasts, recession probability, investment framework
   - Risk assessments, catalysts, and economic scenario analysis

2. **Real-Time Economic Data - MCP Standardized**: **MANDATORY**
   - Economic indicators via FRED MCP server for macro context
   - GDP growth, employment trends, inflation, Fed Funds Rate, yield curve
   - Use MCP Tool: `get_economic_indicators()` for comprehensive real-time data
   - **CRITICAL REQUIREMENT**: Always use current economic context, never stale data
   - Ensures Twitter content reflects current economic environment via MCP data_quality.timestamp
   - Production-grade reliability with intelligent caching, retry logic, and health monitoring

3. **Cross-Regional Economic Data** (SECONDARY): Real-time international economic analysis
   - Major regions: US, EUROPE, ASIA, AMERICAS, GLOBAL
   - GDP differentials, inflation comparisons, policy divergence
   - Cross-regional correlations and economic positioning
   - **IMF AUTHORITY PROTOCOL**: When conflicts arise, IMF data takes precedence for international

4. **Central Bank Policy Data** (VALIDATION): Policy analysis and monetary frameworks
   - Fed, ECB, BoJ, BoE policy stances and forward guidance
   - Interest rate expectations and policy transmission mechanisms
   - Used for policy analysis validation and consistency checking

## Enhanced Data Integration Protocol

### Phase 1: Multi-Source Macro Validation (MANDATORY)
**Execute all macro data validation sources in parallel:**

1. **Macro Analysis Document** (Primary)
   - Use macro analysis: `{REGION}_{YYYYMMDD}.md`
   - Extract: economic thesis, business cycle assessment, policy analysis
   - Validate: confidence scores and institutional quality metrics

2. **Economic Indicators Validation** (Secondary)
   - Execute: FRED/IMF economic indicators collection for primary region
   - Extract: GDP, CPI, employment, Fed Funds, yield curve
   - Cross-validate with macro analysis economic projections

3. **Cross-Regional Context Validation** (Tertiary)
   - Execute: Multi-regional economic indicators comparison
   - Extract: relative positioning, growth differentials, correlations
   - Final cross-validation check against regional economic analysis

**CRITICAL VALIDATION REQUIREMENTS:**
- Economic data consistency ≤2% variance across all sources
- If variance >2%: FAIL-FAST with explicit error message
- Document economic data source confidence in metadata
- Use most recent timestamp as authoritative

### Phase 2: Macro Analysis Cross-Validation
**Source Analysis Confidence Extraction:**

1. **Load Macro Analysis Confidence**
   - Extract overall confidence from {REGION}_{YYYYMMDD}.md header
   - Validate confidence ≥ 0.9 for institutional baseline
   - Extract data quality scores from analysis metadata

2. **Key Economic Metrics Consistency Validation**
   - Cross-validate economic forecasts vs current indicator trends
   - Verify recession probabilities and business cycle estimates
   - Validate cross-regional relative positioning and correlations

3. **Confidence Propagation Protocol**
   - Apply 0.9+ institutional baseline requirement
   - Adjust confidence based on economic data source agreement
   - Document confidence adjustments in post metadata

### Phase 3: Cross-Regional Context Integration
**Enhanced Cross-Regional Analysis:**

1. **FRED/IMF Economic Indicators**
   - Fed Funds Rate impact on regional economic positioning
   - GDP growth differentials across major regions
   - Employment and inflation trends affecting business cycles

2. **Business Cycle Context**
   - Regional business cycle positioning analysis
   - Cross-regional correlation coefficients
   - Economic transition probability assessment

3. **Cross-Regional Economic Analysis**
   - Multi-regional relative positioning (US, EU, Asia)
   - Economic correlation matrix and policy divergence
   - Regional investment allocation insights

## Macro Analysis Data Processing Pipeline

### Domain-Specific Data Extraction
```python
def load_macro_synthesis(region, date):
    """Load and validate source macro analysis synthesis"""

    source_path = f"{DATA_OUTPUTS}/macro_analysis/{region}_{date}.md"

    # DASV Input Validation
    validate_macro_synthesis(source_path)

    # Extract synthesis data
    synthesis_data = parse_macro_synthesis(source_path)

    # Validate macro-specific completeness
    required_sections = ['economic_thesis', 'business_cycle_assessment', 'cross_regional_positioning', 'policy_analysis']
    validate_macro_completeness(synthesis_data, required_sections)

    return synthesis_data
```

### Macro Template Selection Logic
```python
def select_macro_template(macro_data):
    """Domain-specific template selection for macro analysis"""

    # Template A: Business Cycle Analysis (Economic transition focus)
    if (macro_data.get('business_cycle_transition_probability', 0) > 0.7 and
        macro_data.get('recession_risk_assessment', False)):
        return 'business_cycle_analysis'

    # Template B: Cross-Regional Comparison (Growth differentials)
    elif (macro_data.get('gdp_growth_differential', 0) > 100 and
          macro_data.get('multi_region_analysis', False)):
        return 'cross_regional_comparison'

    # Template C: Monetary Policy (Central bank focus)
    elif (macro_data.get('policy_change_probability', 0) > 0.6 and
          macro_data.get('yield_curve_analysis', False)):
        return 'monetary_policy'

    # Template D: Economic Outlook (Forecast focus)
    elif (macro_data.get('economic_forecast_confidence', 0) > 0.85 and
          macro_data.get('gdp_employment_inflation_data', False)):
        return 'economic_outlook'

    # Template E: Economic Indicators (Default)
    return 'economic_indicators'
```

### Economic Indicators Integration
```python
def integrate_economic_indicators(region, macro_data):
    """Integrate real-time economic indicators for macro context validation"""

    # Economic indicator mapping for major regions
    indicator_mapping = {
        'US': ['GDP', 'GDPC1', 'PAYEMS', 'UNRATE', 'CPIAUCSL', 'FEDFUNDS', 'DGS10', 'DGS2'],
        'EUROPE': ['EU_GDP', 'EU_CPI', 'EU_UNEMPLOYMENT', 'ECB_RATE'],
        'ASIA': ['ASIA_GDP', 'ASIA_CPI', 'BOJ_RATE'],
        'GLOBAL': ['GLOBAL_GDP', 'GLOBAL_CPI', 'GLOBAL_TRADE']
    }

    region_indicators = indicator_mapping.get(region.upper())
    if region_indicators:
        # Real-time economic indicators collection
        current_indicators = collect_economic_indicators(region_indicators)

        # Validate against macro analysis forecasts
        gdp_variance = calculate_indicator_variance(macro_data['gdp_forecast'], current_indicators['gdp'])
        if gdp_variance > 0.02:  # 2% threshold for economic data
            log_economic_variance_warning(gdp_variance)

        # Update macro context
        macro_data['current_gdp'] = current_indicators['gdp']
        macro_data['current_inflation'] = current_indicators['cpi']
        macro_data['current_employment'] = current_indicators['employment']
        macro_data['current_policy_rate'] = current_indicators['policy_rate']

    return macro_data
```

## Twitter Writer Agent Integration

### Structured Data Handoff Protocol
```json
{
  "command_type": "macro_analysis",
  "synthesis_confidence": 0.93,
  "template_recommendation": "business_cycle_analysis|cross_regional_comparison|monetary_policy|economic_outlook|economic_indicators",
  "region": "US",
  "date": "20250811",
  "domain_data": {
    "economic_thesis": "US economy demonstrates late-cycle resilience with controlled expansion trajectory",
    "business_cycle_assessment": {
      "current_phase": "late_expansion",
      "recession_probability": 0.15,
      "transition_probability": 0.25,
      "cycle_duration": "68_months"
    },
    "cross_regional_positioning": {
      "gdp_growth_differential": "+120bps_vs_EU",
      "relative_performance": "outperforming major regions",
      "policy_divergence": "restrictive_vs_accommodative_peers",
      "correlation_benefits": ["low_correlation_emerging", "policy_flexibility"]
    },
    "economic_indicators": {
      "gdp_growth": 2.8,
      "inflation_cpi": 2.73,
      "unemployment": 4.3,
      "fed_funds_rate": 4.33,
      "yield_curve_10y2y": 61
    },
    "policy_analysis": {
      "fed_stance": "restrictive",
      "policy_rate_vs_neutral": "+183bps",
      "dovish_pivot_probability": 0.70,
      "policy_transmission": "effective_disinflation"
    },
    "key_catalysts": [
      {"catalyst": "Fed dovish pivot", "probability": 0.7, "impact": "high", "timeline": "H2_2025"},
      {"catalyst": "GDP momentum sustainability", "probability": 0.85, "impact": "medium", "timeline": "12_months"}
    ],
    "risk_factors": ["policy_transmission_lag", "external_shocks", "credit_tightening"]
  },
  "engagement_parameters": {
    "urgency": "standard",
    "audience": "institutional_investors",
    "complexity": "advanced"
  },
  "compliance_requirements": {
    "disclaimers": ["economic_forecasts", "policy_uncertainty"],
    "risk_factors": ["business_cycles", "forecast_limitations"],
    "transparency_level": "institutional"
  },
  "quality_metadata": {
    "source_confidence": 0.94,
    "economic_integration_quality": 0.96,
    "cross_regional_validation": 0.92,
    "template_rationale": "Selected business_cycle_analysis due to transition probability (0.25) and recession risk focus"
  }
}
```

### Macro Analysis Processing Flow
1. **Load and validate** source macro analysis synthesis (≥9.0 confidence)
2. **Extract macro-specific** insights and cross-regional positioning
3. **Integrate economic indicators** for real-time validation and context
4. **Select optimal template** based on business cycle and economic characteristics
5. **Calculate macro synthesis confidence** with cross-regional validation
6. **Prepare structured data** for twitter_writer agent handoff
7. **Use the twitter_writer sub-agent** to create engaging economic outlook content
8. **Validate output quality** and apply enhancement targeting 9.5+ if needed

## DASV Quality Assurance Framework

### Sector-Specific Validation Gates
```python
def validate_sector_synthesis_quality(sector_data, etf_data, cross_sector_data):
    """Enforce sector-specific DASV quality standards"""

    quality_checks = {
        'source_confidence': sector_data['confidence'] >= 0.9,
        'etf_integration_quality': etf_data['validation_score'] >= 0.9,
        'cross_sector_consistency': cross_sector_data['correlation_score'] >= 0.85,
        'allocation_guidance_clarity': validate_allocation_recommendations(sector_data),
        'economic_sensitivity_accuracy': validate_correlation_coefficients(sector_data)
    }

    # Fail-fast on quality gate failures
    for check, passed in quality_checks.items():
        if not passed:
            raise SectorQualityGateException(f"Sector synthesis quality gate failed: {check}")

    return True
```

### Enhancement Protocol for Sectors
```python
def apply_sector_validation_enhancement(sector, date, validation_file_path):
    """Sector-specific DASV enhancement targeting 9.5+ confidence"""

    # Parse sector validation assessment
    validation_data = load_sector_validation_assessment(validation_file_path)

    # Load original synthesis and identify enhancement opportunities
    original_synthesis = load_sector_synthesis(sector, date)

    enhancement_targets = {
        'cross_sector_positioning_gaps': validation_data.get('positioning_issues', []),
        'etf_integration_needs': validation_data.get('etf_data_conflicts', []),
        'allocation_guidance_clarity': validation_data.get('allocation_issues', []),
        'economic_correlation_precision': validation_data.get('sensitivity_gaps', [])
    }

    # Re-process with enhancement focus
    enhanced_data = enhance_sector_processing(original_synthesis, enhancement_targets)
    enhanced_confidence = calculate_enhanced_sector_confidence(enhanced_data)

    # Prepare enhanced data for twitter_writer sub-agent
    enhanced_writer_input = prepare_sector_writer_data(enhanced_data, enhanced_confidence)

    # Target: 9.5+ synthesis confidence through systematic improvement

    return enhanced_writer_input
```

## MANDATORY COMPLIANCE FRAMEWORK

### Economic Forecast Disclaimer Requirements (NON-NEGOTIABLE)

**CRITICAL: Every Twitter post MUST include economic forecast disclaimers:**

- **Required Disclaimer Text**: One of the following MUST appear before the blog link:
  - `⚠️ Economic forecasts carry uncertainty. Past cycles don't guarantee future patterns.`
  - `⚠️ Economic comparisons reflect current data. Regional dynamics evolve.`
  - `⚠️ Policy predictions carry uncertainty. Market conditions affect transmission.`
  - `⚠️ Economic forecasts are estimates. Multiple scenarios possible.`
  - `⚠️ Economic indicators reflect point-in-time data. Trends may vary.`

**ENFORCEMENT**: Templates automatically include disclaimer text. Content generation WILL FAIL validation if disclaimer is missing or modified.

**REGULATORY COMPLIANCE**:
- No definitive economic predictions without uncertainty disclaimers
- Risk warnings are mandatory for all economic forecast content
- Forecast limitations disclaimers required for business cycle projections
- Analytical framework clearly established in all posts

**VALIDATION CHECKPOINT**: Before export, every post MUST pass forecast disclaimer compliance check.

## Content Optimization Framework (EMBEDDED)

### Template A: Business Cycle Analysis
```
🔄 {REGION} economy positioned in {cycle_phase} with {transition_probability}% transition probability

Business cycle metrics:
• Current phase: {current_phase} ({cycle_duration} months)
• Recession probability: {recession_probability}% (12M)
• Policy stance: {policy_stance} ({rate_vs_neutral})

Economic indicators:
• GDP growth: {gdp_growth}% (vs {region_average}% avg)
• Employment: {employment_trend}
• Policy rate: {policy_rate}% ({policy_trajectory})

📋 Full analysis: https://www.colemorton.com/blog/{region-lowercase}-macro-analysis-{yyyymmdd}/

⚠️ Economic forecasts carry uncertainty. Past cycles don't guarantee future patterns.

#{REGION} #BusinessCycle #MacroAnalysis
```

### Template B: Cross-Regional Comparison
```
📊 {REGION} vs global economic positioning analysis:

Relative economic performance:
• GDP growth vs US: {gdp_differential}% differential
• Inflation vs EU: {inflation_differential}% differential
• Policy rate differential: {policy_rate_differential}bps

Cross-regional metrics:
• Correlation with US: {us_correlation}
• Policy divergence: {policy_divergence}
• Currency strength: {currency_performance} vs DXY

Economic outlook: {economic_outlook_rating} vs peers

📋 Full analysis: https://www.colemorton.com/blog/{region-lowercase}-macro-analysis-{yyyymmdd}/

⚠️ Economic comparisons reflect current data. Regional dynamics evolve.

#{REGION} #CrossRegional #GlobalMacro
```

### Template C: Monetary Policy
```
🎯 {REGION} monetary policy outlook and market implications:

Central bank assessment:
• Current policy rate: {policy_rate}% ({neutral_rate_differential})
• Policy stance: {policy_stance}
• Forward guidance: {forward_guidance}

Policy transmission effects:
• Yield curve: {yield_curve_shape} ({10y2y_spread}bps)
• Credit conditions: {credit_conditions}
• Currency impact: {currency_implications}

Next policy move: {next_move_probability}% probability ({timeline})

📋 Full analysis: https://www.colemorton.com/blog/{region-lowercase}-macro-analysis-{yyyymmdd}/

⚠️ Policy predictions carry uncertainty. Market conditions affect transmission.

#{REGION} #MonetaryPolicy #CentralBank
```

### Template D: Economic Outlook
```
📈 {REGION} economic outlook and forecast trajectory:

Economic forecasts:
• GDP growth: {gdp_forecast}% ({confidence_level} confidence)
• Inflation: {inflation_forecast}% (vs {target}% target)
• Employment: {employment_forecast}

Economic scenario probabilities:
• Base case: {base_case_probability}% - {base_case_outcome}
• Upside: {upside_probability}% - {upside_scenario}
• Downside: {downside_probability}% - {downside_scenario}

Key economic catalysts: {primary_catalyst} ({catalyst_probability}%)

📋 Full analysis: https://www.colemorton.com/blog/{region-lowercase}-macro-analysis-{yyyymmdd}/

⚠️ Economic forecasts are estimates. Multiple scenarios possible.

#{REGION} #EconomicOutlook #Forecasting
```

### Template E: Economic Indicators
```
🏗️ {REGION} key economic indicators dashboard:

Core economic metrics:
• GDP growth: {gdp_growth}% ({trend_direction})
• Inflation (CPI): {cpi_inflation}% ({vs_target})
• Unemployment: {unemployment_rate}% ({labor_market_health})

Financial conditions:
• Policy rate: {policy_rate}% ({recent_change})
• 10Y yield: {ten_year_yield}% ({yield_trend})
• Credit spreads: {credit_spreads}bps ({credit_conditions})

Economic momentum: {economic_momentum_assessment}

📋 Full analysis: https://www.colemorton.com/blog/{region-lowercase}-macro-analysis-{yyyymmdd}/

⚠️ Economic indicators reflect point-in-time data. Trends may vary.

#{REGION} #EconomicIndicators #MacroDashboard
```

### Template Selection Logic
**Automated Template Selection Framework:**
- **IF** (business cycle transition probability > 0.7 AND recession risk assessment) → **Template A: Business Cycle Analysis**
- **IF** (GDP growth differential > 100bps AND multi-region analysis) → **Template B: Cross-Regional Comparison**
- **IF** (policy change probability > 0.6 AND yield curve analysis) → **Template C: Monetary Policy**
- **IF** (economic forecast confidence > 0.85 AND GDP/employment/inflation data) → **Template D: Economic Outlook**
- **ELSE** → **Template E: Economic Indicators**

### Content Optimization Standards (Embedded)

#### Engagement Mechanics
1. **Lead with Economic Data**: Specific percentages, growth rates, probabilities
2. **Strategic Emoji Usage**: 1-2 relevant emojis max for visual appeal
3. **Create Economic Curiosity**: Tease business cycle opportunities before revealing
4. **Include Policy Context**: Central bank policy and economic cycle insights
5. **End with Clear Outlook**: What the economic trajectory suggests

#### Writing Style Requirements
- **Plain Language**: No jargon without explanation
- **Active Voice**: "US economy expands" not "US economy is expanding"
- **Specific Claims**: "2.8% GDP growth" not "strong growth"
- **Present Tense**: Create immediacy and relevance
- **Evidence-Based Tone**: Back analysis with economic data and probability scores

#### Character Count Optimization
- **Target Length**: 280 characters per tweet (can thread if needed)
- **Tweet 1**: Hook + core economic insight
- **Tweet 2** (if needed): Supporting economic indicators
- **Tweet 3** (if needed): Business cycle/policy implications

## Institutional Quality Framework

### Pre-Generation Quality Gates (MANDATORY VALIDATION)
**Execute before any content generation:**

□ **Sector Analysis Confidence Validation**
  - Sector analysis confidence ≥ 0.9 (institutional baseline)
  - Cross-sector data quality scores ≥ 0.95 for multi-source validation
  - Economic context integration confidence ≥ 0.9

□ **Multi-Source Sector Validation**
  - Sector analysis document loaded and validated
  - Sector ETF data obtained and cross-validated
  - Economic indicators current (≤24 hours)
  - Cross-sector variance ≤3% across all sources (BLOCKING if exceeded)

□ **Economic Context Integration Validated**
  - FRED economic indicators current (≤24 hours)
  - Economic cycle assessment completed
  - Sector correlation analysis validated

□ **Template Selection Logic Executed**
  - All template selection criteria evaluated
  - Optimal template selected based on sector analysis content
  - Template placeholder mapping prepared

### Content Quality Standards (INSTITUTIONAL GRADE)
**Apply during content generation:**

□ **Evidence-Backed Claims**
  - All quantitative claims backed by specific confidence scores
  - Sector thesis directly aligned with source analysis
  - Economic assessments include correlation coefficients
  - Allocation impacts include timeline and probability estimates

□ **Professional Presentation Standards**
  - Institutional-grade formatting and structure
  - Confidence scores in 0.0-1.0 format throughout
  - Percentage values with % formatting and precision
  - Economic correlations in decimal format

□ **Data Source Attribution**
  - Multi-source validation results documented
  - Confidence level adjustments clearly noted
  - Economic context integration explicitly referenced
  - Analysis methodology transparency maintained

### Post-Generation Validation (COMPREHENSIVE REVIEW)
**Execute after content generation:**

□ **Character Count Optimization**
  - Twitter character limit (280) strictly enforced
  - Threading strategy implemented if content exceeds limit
  - Optimal hashtag strategy applied (2-3 relevant hashtags)

□ **Regulatory Compliance Verification**
  - Investment disclaimer present and compliant
  - Risk warning language appropriate and clear
  - Data source limitations acknowledged
  - Opinion framework explicitly established

□ **Blog Link Generation Accuracy**
  - URL pattern correctly applied: /blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/
  - Link functionality verified (pattern validation)
  - Analysis attribution metadata included

□ **Final Institutional Standards Review**
  - Content meets publication-ready quality standards
  - Professional tone and presentation maintained
  - All claims verifiable against sector analysis
  - Confidence levels appropriate for institutional usage

### Quality Assurance Metadata Generation
**Include in all outputs:**

```yaml
quality_assurance:
  pre_generation_gates_passed: true
  multi_source_sector_validation: {sector_analysis: confidence_score, etf_data: accuracy_score, economic_context: currency}
  sector_analysis_confidence: X.XX
  economic_context_integration: true
  template_selection: {selected: "Template X", rationale: "reason"}
  content_quality_standards: {evidence_backed: true, professional_presentation: true, attribution_complete: true}
  post_generation_validation: {character_count: XXX, compliance_verified: true, blog_link_accurate: true}
  institutional_standards: {publication_ready: true, confidence_appropriate: true}
```

## Export Protocol (Embedded)

### Blog Post URL Generation
**URL Pattern Specifications:**
- **Input format:** `{REGION}_{YYYYMMDD}` (e.g., `US_20250710`)
- **Output format:** `https://www.colemorton.com/blog/{region-lowercase}-macro-analysis-{yyyymmdd}/`
- **Example conversion:** `US_20250710` → `https://www.colemorton.com/blog/us-macro-analysis-20250710/`

### File Output Requirements
**Primary Output File:**
```
./{DATA_OUTPUTS}/macro_analysis/twitter/{REGION}_{YYYYMMDD}.md
```

**File contains:**
- Clean X post content ready for copy/paste
- Character count for each tweet
- Selected template rationale
- Key economic insights extracted from source analysis
- Generated blog post URL for full macro analysis access

## Command Usage

**Execute Twitter synthesis from macro analysis:**
```
/macro_analysis:twitter {REGION}_{YYYYMMDD}
```

**Examples:**
- `/macro_analysis:twitter US_20250811`
- `/macro_analysis:twitter EUROPE_20250811`
- `/macro_analysis:twitter GLOBAL_20250811`

**DASV Processing Flow:**
1. **Load & validate** source macro analysis synthesis (≥9.0 confidence)
2. **Extract macro data** (economic thesis, business cycle, policy analysis, cross-regional positioning)
3. **Integrate economic indicators** for real-time validation and current economic context
4. **Validate cross-regional** positioning and correlation accuracy
5. **Select optimal template** based on macro analysis characteristics
6. **Calculate macro synthesis confidence** with DASV standards
7. **Use twitter_writer sub-agent** to create engaging economic content from structured data
8. **Apply enhancement** if validation file exists (target: ≥9.5 confidence)
9. **Export results** with complete macro quality metrics and traceability

**Enhancement Workflow:**
```
# Phase 1: Generate macro Twitter synthesis
/macro_analysis:twitter US_20250811

# Phase 2: If synthesis confidence <9.5, apply validation enhancement
/macro_analysis:twitter {DATA_OUTPUTS}/macro_analysis/twitter/validation/US_20250811_validation.json

# Phase 3: Validate institutional excellence achieved (≥9.5/10.0)
```

---

## MANDATORY WORKFLOW REMINDER

⚠️ **CRITICAL FIRST STEP**: Before processing any macro analysis, ALWAYS get current economic context using FRED MCP server and validate cross-regional economic indicators.

**Real-time Data Requirements:**
- Economic indicators current within 24 hours
- Cross-regional data validated against analysis forecasts
- Business cycle correlations updated with current economic conditions

**Never use stale economic data from the macro analysis file - it may be outdated. Always use real-time economic indicators and current cross-regional data for accurate economic positioning.**

## Post-Execution Protocol

### Required Actions
1. **Generate Output Metadata**: Include collaboration metadata for macro content
2. **Store Outputs**: Save to `./{DATA_OUTPUTS}/macro_analysis/twitter/` directories
3. **Quality Validation**: Content accuracy and macro analysis compliance verification
4. **Content Tracking**: Performance metrics and institutional quality standards

### Output Metadata Template
```yaml
metadata:
  generated_by: "twitter-macro-analysis"
  timestamp: "{ISO-8601-timestamp}"
  region: "{REGION}"
  content_type: "macro_analysis_post"

content_metrics:
  character_count: "{post-length}"
  engagement_optimized: true
  accuracy_verified: true
  economic_context_current: true

quality_assurance:
  macro_analysis_source: "{source-file}"
  economic_data_current: true
  twitter_best_practices: true
```

---

## DASV Architecture Benefits

**Clean Separation of Concerns**:
- **Domain Focus**: Command handles macro analysis data processing and economic indicators integration
- **Content Delegation**: Twitter_writer sub-agent handles all content creation and engagement
- **Quality Assurance**: DASV framework ensures institutional economic analysis standards
- **Enhancement Protocol**: Systematic improvement targeting 9.5+ confidence with cross-regional validation

**Macro-Specific Quality Standards**:
- **Source Validation**: ≥9.0/10.0 synthesis confidence required
- **Economic Integration**: Real-time indicators validation with 2% variance threshold
- **Cross-Regional Consistency**: ≥0.85 correlation accuracy requirement
- **Economic Guidance**: Clear business cycle assessments with forecast confidence levels

**Integration Excellence**:
- **Twitter Writer**: Structured macro data handoff for optimal economic content
- **Economic Data**: Real-time integration for economic indicators and policy validation
- **Enhancement Loop**: Validation-driven improvement targeting institutional excellence
- **Audit Trail**: Complete macro quality metrics and decision rationale

**Ready to generate DASV-compliant Twitter synthesis from institutional-grade macro analysis. Provide {REGION}_{YYYYMMDD} identifier to begin macro-focused data processing and twitter_writer integration.**
