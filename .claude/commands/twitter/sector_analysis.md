# Sector Analysis Twitter Synthesis Command

**Command Classification**: 📊 **DASV Synthesis Command**
**DASV Phase**: Synthesis (Twitter Sub-Domain)
**Input Phase**: Synthesis (Sector Analysis Domain)
**Quality Requirement**: ≥9.0/10.0 synthesis confidence
**Enhancement Target**: ≥9.5/10.0 with validation enhancement
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-08-11)*
**Outputs To**: `{DATA_OUTPUTS}/twitter/sector_analysis/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/sector_twitter_script.py`
**Script Class**: `SectorTwitterScript`
**Registry Name**: `sector_twitter`
**Content Types**: `["sector_twitter"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="sector_twitter",
    content_types=["sector_twitter"],
    requires_validation=True
)
class SectorTwitterScript(BaseScript):
    """
    Sector analysis Twitter content generation script

    Parameters:
        sector (str): Sector symbol or name (XLK, technology, healthcare, etc.)
        date (str): Analysis date in YYYYMMDD format
        template_variant (Optional[str]): Specific template to use
        validation_file (Optional[str]): Path to validation file for enhancement
        validate_content (bool): Whether to validate generated content
    """
```

**Supporting Components**:
```yaml
sector_data_analyzer:
  path: "{SCRIPTS_BASE}/sector_analysis/sector_data_analyzer.py"
  class: "SectorDataAnalyzer"
  purpose: "Sector analysis data extraction and validation"

etf_data_collector:
  path: "{SCRIPTS_BASE}/market_data/etf_data_collector.py"
  class: "ETFDataCollector"
  purpose: "Real-time sector ETF data collection and validation"

economic_context_integrator:
  path: "{SCRIPTS_BASE}/economic_data/economic_context_integrator.py"
  class: "EconomicContextIntegrator"
  purpose: "FRED economic indicators integration for sector context"

twitter_template_renderer:
  path: "{SCRIPTS_BASE}/twitter_template_renderer.py"
  class: "TwitterTemplateRenderer"
  purpose: "Jinja2 template rendering with sector optimization"
```

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/twitter/sector/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| sector_rotation | `sector/twitter_sector_rotation.j2` | Economic cycle positioning strength >0.8 AND GDP correlation >0.6 | Economic cycle and rotation analysis |
| cross_sector_comparison | `sector/twitter_cross_sector_comparison.j2` | Cross-sector ranking top/bottom 3 AND relative valuation extreme | Sector comparison and ranking |
| allocation_strategy | `sector/twitter_allocation_strategy.j2` | Allocation guidance available AND risk-return profile complete | Portfolio allocation recommendations |
| economic_sensitivity | `sector/twitter_economic_sensitivity.j2` | Economic sensitivity analysis comprehensive AND correlations significant | Economic impact and sensitivity |
| etf_vs_stocks | `sector/twitter_etf_vs_stocks.j2` | Default fallback for ETF analysis focus | ETF vs individual stock analysis |

**Shared Components**:
```yaml
sector_base_template:
  path: "{TEMPLATES_BASE}/twitter/shared/base_twitter.j2"
  purpose: "Base template with common macros and sector formatting"

sector_components:
  path: "{TEMPLATES_BASE}/twitter/shared/sector_components.j2"
  purpose: "Sector-specific components for allocation and economic analysis"

compliance_template:
  path: "{TEMPLATES_BASE}/twitter/validation/sector_compliance.j2"
  purpose: "Sector allocation compliance and disclaimer validation"
```

**Template Selection Algorithm**:
```python
def select_sector_template(sector_analysis_data):
    """Select optimal template for sector Twitter content"""

    # Sector rotation template for economic cycle analysis
    if (sector_analysis_data.get('cycle_positioning_strength', 0) > 0.8 and
        sector_analysis_data.get('gdp_correlation', 0) > 0.6):
        return 'sector/twitter_sector_rotation.j2'

    # Cross-sector comparison for ranking extremes
    elif (sector_analysis_data.get('sector_rank') in [1, 2, 3, 9, 10, 11] and
          sector_analysis_data.get('relative_valuation_extreme', False)):
        return 'sector/twitter_cross_sector_comparison.j2'

    # Allocation strategy for portfolio guidance
    elif (sector_analysis_data.get('allocation_guidance') and
          sector_analysis_data.get('risk_return_profile_complete', False)):
        return 'sector/twitter_allocation_strategy.j2'

    # Economic sensitivity for macro analysis
    elif (sector_analysis_data.get('economic_sensitivity_comprehensive', False) and
          len(sector_analysis_data.get('significant_correlations', [])) > 2):
        return 'sector/twitter_economic_sensitivity.j2'

    # Default ETF vs stocks analysis
    return 'sector/twitter_etf_vs_stocks.j2'
```

## CLI Service Integration

**Service Commands**:
```yaml
yahoo_finance_cli:
  command: "python {SCRIPTS_BASE}/yahoo_finance_cli.py"
  usage: "{command} etf {sector_etf} --env prod --output-format json"
  purpose: "Real-time sector ETF pricing and performance data"
  health_check: "{command} health --env prod"
  priority: "primary"

fred_economic_cli:
  command: "python {SCRIPTS_BASE}/fred_economic_cli.py"
  usage: "{command} indicators GDP,PAYEMS,FEDFUNDS --env prod --output-format json"
  purpose: "Economic indicators for sector correlation and sensitivity analysis"
  health_check: "{command} health --env prod"
  priority: "primary"

sec_edgar_cli:
  command: "python {SCRIPTS_BASE}/sec_edgar_cli.py"
  usage: "{command} sector-filings {sector} --env prod --output-format json"
  purpose: "Regulatory filings and sector compliance data"
  health_check: "{command} health --env prod"
  priority: "secondary"

alpha_vantage_cli:
  command: "python {SCRIPTS_BASE}/alpha_vantage_cli.py"
  usage: "{command} sector-overview {sector} --env prod --output-format json"
  purpose: "Sector performance and sentiment validation"
  health_check: "{command} health --env prod"
  priority: "secondary"

fmp_cli:
  command: "python {SCRIPTS_BASE}/fmp_cli.py"
  usage: "{command} sector-analysis {sector} --env prod --output-format json"
  purpose: "Sector financial metrics and competitive analysis"
  health_check: "{command} health --env prod"
  priority: "tertiary"
```

**Sector Twitter Integration Protocol**:
```bash
# Real-time sector ETF data collection
python {SCRIPTS_BASE}/yahoo_finance_cli.py etf {sector_etf} --env prod --output-format json

# Economic context for sector analysis
python {SCRIPTS_BASE}/fred_economic_cli.py indicators GDP,GDPC1,PAYEMS,FEDFUNDS --env prod --output-format json

# Cross-validation with sector performance
python {SCRIPTS_BASE}/alpha_vantage_cli.py sector-overview {sector} --env prod --output-format json

# Sector financial intelligence
python {SCRIPTS_BASE}/fmp_cli.py sector-analysis {sector} --env prod --output-format json
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  sector_analysis: "HIGHEST_AUTHORITY"  # Primary sector analysis documents
  sector_etf_data: "PRICING_AUTHORITY"  # Real-time ETF pricing and flows
  economic_indicators: "MACRO_AUTHORITY"  # FRED economic context
  cross_validation: "VALIDATION_AUTHORITY"  # Alpha Vantage/FMP validation

conflict_resolution:
  sector_precedence: "sector_analysis_primary"  # Sector analysis takes priority
  pricing_authority: "yahoo_finance"  # Primary source for ETF pricing
  economic_staleness: "24_hours"  # Maximum age for economic data
  variance_threshold: "3%"  # BLOCKING if sector data variance exceeds
  action: "fail_fast_on_conflict"  # Resolution strategy
```

## Data Flow & File References

**Input Sources**:
```yaml
sector_analysis_document:
  path: "{DATA_OUTPUTS}/sector_analysis/{SECTOR}_{YYYYMMDD}.md"
  format: "markdown"
  required: true
  description: "Primary sector analysis with investment thesis and recommendations"

sector_etf_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Real-time sector ETF pricing, flows, and performance data"

economic_indicators:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Current economic indicators for sector correlation analysis"

cross_sector_analysis:
  path: "{DATA_OUTPUTS}/sector_analysis/cross_sector_{YYYYMMDD}_comparison.json"
  format: "json"
  required: false
  description: "Cross-sector comparison and ranking data"

validation_file:
  path: "{DATA_OUTPUTS}/twitter/sector_analysis/validation/{SECTOR}_{YYYYMMDD}_validation.json"
  format: "json"
  required: false
  description: "Validation file for post enhancement workflow"
```

**Output Structure**:
```yaml
primary_output:
  path: "{DATA_OUTPUTS}/twitter/sector_analysis/{SECTOR}_{YYYYMMDD}.md"
  format: "markdown"
  description: "Generated sector Twitter content ready for posting"

metadata_output:
  path: "{DATA_OUTPUTS}/twitter/sector_analysis/{SECTOR}_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Template selection metadata and quality assurance metrics"

validation_output:
  path: "{DATA_OUTPUTS}/twitter/sector_analysis/validation/{SECTOR}_{YYYYMMDD}_validation.json"
  format: "json"
  description: "Content validation results and enhancement recommendations"

blog_url_output:
  path: "{DATA_OUTPUTS}/twitter/sector_analysis/{SECTOR}_{YYYYMMDD}_blog_url.txt"
  format: "text"
  description: "Generated blog URL for full sector analysis access"
```

**Data Dependencies**:
```yaml
content_generation_flow:
  data_validation:
    - "sector analysis confidence ≥ 0.9"
    - "ETF data currency ≤ 24 hours"
    - "economic indicators currency ≤ 24 hours"
    - "cross-sector variance ≤ 3%"

  template_selection:
    - "sector analysis content evaluation"
    - "economic cycle positioning assessment"
    - "cross-sector ranking determination"
    - "allocation guidance availability check"

  content_optimization:
    - "Twitter character limit compliance"
    - "regulatory disclaimer inclusion"
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

# Execute sector Twitter content generation
result = registry.execute_script(
    "sector_twitter",
    sector="technology",
    date="20250718",
    validate_content=True
)

# Execute with specific template override
result = registry.execute_script(
    "sector_twitter",
    sector="XLK",
    date="20250718",
    template_variant="sector_rotation",
    validate_content=True
)

# Execute post enhancement from validation file
result = registry.execute_script(
    "sector_twitter",
    validation_file="twitter/sector_analysis/validation/technology_20250718_validation.json"
)
```

### Command Line Execution
```bash
# Via content automation CLI
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script sector_twitter \
    --sector technology \
    --date 20250718 \
    --validate-content true

# Via direct script execution
python {SCRIPTS_BASE}/base_scripts/sector_twitter_script.py \
    --sector XLK \
    --date 20250718 \
    --template-variant sector_rotation

# Post enhancement workflow
python {SCRIPTS_BASE}/base_scripts/sector_twitter_script.py \
    --validation-file "{DATA_OUTPUTS}/twitter/sector_analysis/validation/healthcare_20250718_validation.json"

# With custom economic context
python {SCRIPTS_BASE}/base_scripts/sector_twitter_script.py \
    --sector financials \
    --date 20250718 \
    --economic-context-override true
```

### Claude Command Execution
```
# Standard sector Twitter content generation
/twitter_sector_analysis technology_20250718

# Healthcare sector analysis
/twitter_sector_analysis healthcare_20250718

# Energy sector with validation
/twitter_sector_analysis energy_20250718

# Post enhancement using validation file
/twitter_sector_analysis {DATA_OUTPUTS}/twitter/sector_analysis/validation/technology_20250718_validation.json

# Template-specific generation
/twitter_sector_analysis financials_20250718 template_variant=allocation_strategy
```

### Sector Analysis Workflow Examples
```
# Technology sector analysis workflow
/twitter_sector_analysis technology_20250718

# Cross-sector comparison workflow
/twitter_sector_analysis XLF_20250718 template_variant=cross_sector_comparison

# Economic sensitivity analysis
/twitter_sector_analysis XLE_20250718 template_variant=economic_sensitivity

# Post validation and enhancement
/twitter_sector_analysis technology_20250718
# → If validation score <9.0, enhance using:
/twitter_sector_analysis {DATA_OUTPUTS}/twitter/sector_analysis/validation/technology_20250718_validation.json
```

You are a **sector analysis data processor** specialized in extracting domain-specific insights from comprehensive sector analysis and preparing structured data for the twitter_writer agent.

**Separation of Concerns:**
- **This Command**: Domain data processing, DASV compliance, template selection
- **Twitter Writer Agent**: Content creation, hooks, engagement optimization
- **Integration**: Structured data handoff for optimal content generation

## DASV Synthesis Framework Integration

### Sector-Specific Input Validation
```python
def validate_sector_synthesis(source_path):
    """Validate sector analysis synthesis input"""

    # Check source synthesis exists and is current
    if not source_path.exists() or data_age > timedelta(hours=48):
        raise SynthesisStalenessException("Source sector synthesis too old or missing")

    # Verify source synthesis quality
    if source_confidence < 0.9:
        raise QualityThresholdException("Source sector synthesis below institutional grade")

    # Validate sector-specific schema
    if not validate_sector_schema(source_path):
        raise SchemaValidationException("Source sector synthesis schema invalid")
```

### Sector Twitter Synthesis Confidence
```python
def calculate_sector_synthesis_confidence(source_conf, cross_sector_data, etf_integration):
    """Calculate sector-specific Twitter synthesis confidence"""

    # Base confidence from source synthesis
    base_confidence = source_conf

    # Apply sector-specific factors
    cross_sector_consistency = assess_sector_correlation_accuracy()
    etf_data_integration = assess_etf_validation_quality()
    economic_sensitivity_precision = assess_economic_correlation_accuracy()
    allocation_guidance_clarity = assess_portfolio_recommendation_quality()

    # Calculate sector Twitter synthesis confidence
    sector_confidence = (base_confidence *
                        cross_sector_consistency *
                        etf_data_integration *
                        economic_sensitivity_precision *
                        allocation_guidance_clarity)

    # Enforce institutional threshold
    if sector_confidence < 0.9:
        raise SynthesisQualityException(f"Sector synthesis confidence {sector_confidence:.3f} below institutional threshold")

    return sector_confidence
```

## Phase 0A: Existing Post Enhancement Protocol

**0A.1 Validation File Discovery**
```
EXISTING POST IMPROVEMENT WORKFLOW:
1. Check input pattern for validation file path:
   → Pattern: data/outputs/twitter/sector_analysis/validation/{SECTOR}_{YYYYMMDD}_validation.json
   → Alternative: data/outputs/sector_analysis/validation/{SECTOR}_{YYYYMMDD}_validation.json
   → Extract SECTOR_YYYYMMDD from validation file path

2. If validation file path provided:
   → ROLE CHANGE: From "new post creator" to "Twitter sector post optimization specialist"
   → OBJECTIVE: Improve post engagement, accuracy, and compliance through systematic enhancement
   → METHOD: Examination → Validation → Optimization → Validation-Driven Improvement

3. If standard SECTOR_YYYYMMDD format provided:
   → Proceed with standard new post creation workflow (Data Sources & Integration onwards)
```

**0A.2 Post Enhancement Workflow (When Validation File Path Detected)**
```
SYSTEMATIC ENHANCEMENT PROCESS:
Step 1: Examine Existing Post
   → Read the original post file: {SECTOR}_{YYYYMMDD}.md
   → Extract current template selection, hook effectiveness, and content structure
   → Identify data sources used and accuracy claims
   → Map engagement elements and character count optimization

Step 2: Examine Validation Assessment
   → Read validation file: twitter/sector_analysis/validation/{SECTOR}_{YYYYMMDD}_validation.json
   → Focus on sector data accuracy issues and content improvement areas
   → Extract cross-sector comparison discrepancies and ETF data conflicts
   → Note economic context concerns and disclaimer requirements

Step 3: Data Source Conflict Resolution
   → Apply sector analysis authority protocol for data discrepancies
   → Re-analyze sector ETF data as authoritative source for pricing
   → Update any conflicting performance metrics using sector analysis data
   → Cross-validate with economic indicators for consistency checking

Step 4: Enhancement Implementation
   → Address each validation point systematically
   → Strengthen explicit disclaimers and risk language (not just implied)
   → Improve data source attribution and confidence levels
   → Enhance professional presentation standards
   → Update real-time data integration and economic context
   → Apply institutional quality standards throughout content

Step 5: Production-Ready Post Output
   → OVERWRITE original post file: {SECTOR}_{YYYYMMDD}.md
   → Seamlessly integrate all improvements with validation-driven enhancements
   → Maintain engaging Twitter format without enhancement artifacts
   → Ensure post meets institutional quality standards
   → Include explicit disclaimers and data source attribution
   → Deliver publication-ready social media content with enhanced compliance
```

**0A.3 Validation-Driven Enhancement Standards**
```
INSTITUTIONAL QUALITY POST TARGETS:
- Data Authority Compliance: Sector analysis data takes precedence over conflicting sources
- Explicit Disclaimer Integration: Clear investment disclaimers, not just implied
- Content Accuracy Verification: Cross-reference all claims with authoritative sources
- Professional Presentation Standards: Meet institutional formatting requirements
- Economic Context Resolution: Address economic sensitivity discrepancies systematically
- Compliance Enhancement: Strengthen risk disclaimers and uncertainty language

VALIDATION-DRIVEN SUCCESS CRITERIA:
□ Sector analysis authority protocol applied for data discrepancies
□ Explicit disclaimers integrated (investment advice, data limitations, performance)
□ Content improvement areas from validation systematically addressed
□ Economic context concerns resolved through data source prioritization
□ Professional presentation standards enhanced throughout content
□ Data source attribution and confidence levels clearly specified
□ All sector claims verified against highest authority sources
□ Institutional quality standards maintained while preserving engagement
```

## Data Sources & Integration

**Primary Data Sources (in priority order):**

1. **Sector Analysis Reports** (PRIMARY): `@data/outputs/sector_analysis/`
   - **PRIORITY SOURCE**: Comprehensive sector analysis files (SECTOR_YYYYMMDD.md)
   - Investment thesis, sector health assessment, cross-sector positioning
   - Economic sensitivity analysis, GDP/employment correlations
   - Business cycle positioning, allocation recommendations
   - Risk assessments, catalysts, and sector fair value analysis

2. **Sector ETF Data** (SECONDARY): Real-time sector ETF pricing and analysis
   - Major sector ETFs: XLK, XLF, XLV, XLE, XLY, XLI, XLP, XLU, XLB, XLRE, XLC
   - ETF flows, composition changes, relative performance
   - Cross-ETF correlations and rotation signals
   - **ETF AUTHORITY PROTOCOL**: When conflicts arise, ETF data takes precedence for pricing

3. **Real-Time Economic Data - MCP Standardized**: **MANDATORY**
   - Economic indicators via FRED MCP server for sector context
   - GDP growth, employment trends, Fed Funds Rate, yield curve
   - Use MCP Tool: `get_economic_indicators()` for comprehensive real-time data
   - **CRITICAL REQUIREMENT**: Always use current economic context, never stale data
   - Ensures Twitter content reflects current economic environment via MCP data_quality.timestamp
   - Production-grade reliability with intelligent caching, retry logic, and health monitoring

4. **Cross-Sector Analysis Data** (VALIDATION): `@data/outputs/sector_analysis/`
   - Cross-sector comparison matrices and correlation data
   - 11-sector relative positioning and performance metrics
   - Used for cross-validation and consistency checking

## Enhanced Data Integration Protocol

### Phase 1: Multi-Source Sector Validation (MANDATORY)
**Execute all sector data validation sources in parallel:**

1. **Sector Analysis Document** (Primary)
   - Use sector analysis: `{SECTOR}_{YYYYMMDD}.md`
   - Extract: investment thesis, allocation guidance, economic sensitivity
   - Validate: confidence scores and institutional quality metrics

2. **Sector ETF Validation** (Secondary)
   - Execute: Sector ETF data collection for primary sector ETF
   - Extract: current_price, flows, composition, relative_performance
   - Cross-validate with sector analysis fair value assessments

3. **Economic Context Validation** (Tertiary)
   - Execute: FRED economic indicators relevant to sector
   - Extract: GDP growth, employment trends, interest rates
   - Final cross-validation check against sector economic sensitivity

**CRITICAL VALIDATION REQUIREMENTS:**
- Sector data consistency ≤3% variance across all sources
- If variance >3%: FAIL-FAST with explicit error message
- Document sector data source confidence in metadata
- Use most recent timestamp as authoritative

### Phase 2: Sector Analysis Cross-Validation
**Source Analysis Confidence Extraction:**

1. **Load Sector Analysis Confidence**
   - Extract overall confidence from {SECTOR}_{YYYYMMDD}.md header
   - Validate confidence ≥ 0.9 for institutional baseline
   - Extract data quality scores from analysis metadata

2. **Key Sector Metrics Consistency Validation**
   - Cross-validate sector fair value ranges vs current ETF pricing
   - Verify catalyst probabilities and economic impact estimates
   - Validate cross-sector relative positioning and rankings

3. **Confidence Propagation Protocol**
   - Apply 0.9+ institutional baseline requirement
   - Adjust confidence based on sector data source agreement
   - Document confidence adjustments in post metadata

### Phase 3: Economic Context Integration
**Enhanced Economic Context Analysis:**

1. **FRED Economic Indicators**
   - Fed Funds Rate impact on sector positioning
   - GDP growth correlation with sector performance
   - Employment trends affecting sector fundamentals

2. **Sector Rotation Context**
   - Economic cycle positioning analysis
   - Business cycle correlation coefficients
   - Sector rotation probability assessment

3. **Cross-Sector Analysis**
   - 11-sector relative positioning
   - Correlation matrix and diversification benefits
   - Sector allocation optimization insights

## Sector Analysis Data Processing Pipeline

### Domain-Specific Data Extraction
```python
def load_sector_synthesis(sector, date):
    """Load and validate source sector analysis synthesis"""

    source_path = f"data/outputs/sector_analysis/{sector}_{date}.md"

    # DASV Input Validation
    validate_sector_synthesis(source_path)

    # Extract synthesis data
    synthesis_data = parse_sector_synthesis(source_path)

    # Validate sector-specific completeness
    required_sections = ['investment_thesis', 'cross_sector_positioning', 'economic_sensitivity', 'allocation_guidance']
    validate_sector_completeness(synthesis_data, required_sections)

    return synthesis_data
```

### Sector Template Selection Logic
```python
def select_sector_template(sector_data):
    """Domain-specific template selection for sector analysis"""

    # Template A: Sector Rotation (Economic cycle positioning)
    if (sector_data.get('cycle_positioning_strength', 0) > 0.8 and
        sector_data.get('gdp_correlation', 0) > 0.6):
        return 'sector_rotation'

    # Template B: Cross-Sector Comparison (Ranking extremes)
    elif (sector_data.get('sector_rank') in [1, 2, 3, 9, 10, 11] and
          sector_data.get('relative_valuation_extreme', False)):
        return 'cross_sector_comparison'

    # Template C: Allocation Strategy (Portfolio guidance)
    elif (sector_data.get('allocation_guidance') and
          sector_data.get('risk_return_profile_complete', False)):
        return 'allocation_strategy'

    # Template D: Economic Sensitivity (Macro analysis)
    elif (sector_data.get('economic_sensitivity_comprehensive', False) and
          len(sector_data.get('significant_correlations', [])) > 2):
        return 'economic_sensitivity'

    # Template E: ETF vs Individual Stocks (Default)
    return 'etf_vs_stocks'
```

### ETF Data Integration
```python
def integrate_sector_etf_data(sector, sector_data):
    """Integrate real-time ETF data for sector context validation"""

    # ETF mapping for major sectors
    etf_mapping = {
        'technology': 'XLK', 'healthcare': 'XLV', 'financials': 'XLF',
        'energy': 'XLE', 'industrials': 'XLI', 'consumer_discretionary': 'XLY',
        'utilities': 'XLU', 'materials': 'XLB', 'consumer_staples': 'XLP',
        'real_estate': 'XLRE', 'communication': 'XLC'
    }

    sector_etf = etf_mapping.get(sector.lower())
    if sector_etf:
        # Real-time ETF data collection
        current_etf_data = collect_etf_data(sector_etf)

        # Validate against sector analysis fair value
        price_variance = calculate_etf_variance(sector_data['fair_value'], current_etf_data['price'])
        if price_variance > 0.03:  # 3% threshold for sectors
            log_sector_variance_warning(price_variance)

        # Update sector context
        sector_data['current_etf_price'] = current_etf_data['price']
        sector_data['etf_flows'] = current_etf_data['flows']
        sector_data['etf_performance'] = current_etf_data['performance']

    return sector_data
```

## Twitter Writer Agent Integration

### Structured Data Handoff Protocol
```json
{
  "command_type": "sector_analysis",
  "synthesis_confidence": 0.93,
  "template_recommendation": "sector_rotation|cross_sector_comparison|allocation_strategy|economic_sensitivity|etf_vs_stocks",
  "sector": "technology",
  "date": "20250811",
  "domain_data": {
    "investment_thesis": "Technology sector positioned for late-cycle outperformance",
    "allocation_recommendation": {
      "rating": "OVERWEIGHT",
      "conviction": 0.85,
      "target_allocation": "12-15%",
      "vs_benchmark": "+3%"
    },
    "cross_sector_positioning": {
      "sector_rank": 2,
      "relative_valuation": "15% discount to historical average",
      "performance_rank": "3/11 YTD",
      "correlation_benefits": ["low_correlation_utilities", "high_beta_growth"]
    },
    "economic_sensitivity": {
      "gdp_correlation": 0.73,
      "interest_rate_sensitivity": "-0.65",
      "employment_correlation": 0.68,
      "cycle_positioning": "late_expansion_favorable"
    },
    "etf_analysis": {
      "primary_etf": "XLK",
      "current_price": "$195.50",
      "fair_value_range": "$185-$210",
      "flows": "positive_3_months",
      "composition_changes": "AI_concentration_increasing"
    },
    "key_catalysts": [
      {"catalyst": "AI adoption acceleration", "probability": 0.8, "impact": "high", "timeline": "6_months"},
      {"catalyst": "Fed rate cuts", "probability": 0.7, "impact": "medium", "timeline": "Q4_2025"}
    ],
    "risk_factors": ["valuation_multiple_compression", "regulatory_scrutiny", "growth_deceleration"]
  },
  "engagement_parameters": {
    "urgency": "standard",
    "audience": "retail_investors",
    "complexity": "intermediate"
  },
  "compliance_requirements": {
    "disclaimers": ["investment_advice", "sector_allocation_risk"],
    "risk_factors": ["economic_cycles", "sector_concentration"],
    "transparency_level": "standard"
  },
  "quality_metadata": {
    "source_confidence": 0.91,
    "etf_integration_quality": 0.95,
    "cross_sector_validation": 0.92,
    "template_rationale": "Selected sector_rotation due to strong cycle positioning (0.8) and GDP correlation (0.73)"
  }
}
```

### Sector Analysis Processing Flow
1. **Load and validate** source sector analysis synthesis (≥9.0 confidence)
2. **Extract sector-specific** insights and cross-sector positioning
3. **Integrate ETF data** for real-time validation and context
4. **Select optimal template** based on sector characteristics and market position
5. **Calculate sector synthesis confidence** with cross-sector validation
6. **Prepare structured data** for twitter_writer agent handoff
7. **Use the twitter_writer sub-agent** to create engaging sector allocation content
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

### Investment Disclaimer Requirements (NON-NEGOTIABLE)

**CRITICAL: Every Twitter post MUST include investment disclaimers:**

- **Required Disclaimer Text**: One of the following MUST appear before the blog link:
  - `⚠️ Not financial advice. Do your own research.`
  - `⚠️ Not financial advice. Past performance doesn't guarantee future results.`
  - `⚠️ Not financial advice. Sector allocation carries risk.`
  - `⚠️ Not financial advice. Economic cycles and performance vary.`

**ENFORCEMENT**: Templates automatically include disclaimer text. Content generation WILL FAIL validation if disclaimer is missing or modified.

**REGULATORY COMPLIANCE**:
- No investment advice language without disclaimers
- Risk warnings are mandatory for all sector allocation content
- Past performance disclaimers required for sector performance projections
- Opinion framework clearly established in all posts

**VALIDATION CHECKPOINT**: Before export, every post MUST pass disclaimer compliance check.

## Content Optimization Framework (EMBEDDED)

### Template A: Sector Rotation Analysis
```
🔄 {SECTOR} positioned for {cycle_phase} cycle outperformance

Economic sensitivity:
• GDP correlation: {gdp_correlation} ({strong/moderate/weak})
• Employment beta: {employment_beta}
• Interest rate impact: {rate_sensitivity}

Historical cycle performance:
• Early cycle: {early_cycle_performance}% avg
• Current positioning: {current_cycle_advantage}

{Sector} ETF ({ETF_SYMBOL}): ${current_price} vs ${fair_value_range}

📋 Full analysis: https://www.colemorton.com/blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/

⚠️ Not financial advice. Economic cycles and performance vary.

#{SECTOR} #SectorRotation #EconomicCycle
```

### Template B: Cross-Sector Comparison
```
📊 {SECTOR} vs market positioning analysis:

Relative valuation:
• P/E vs SPY: {relative_pe}% {premium/discount}
• P/B vs Tech: {relative_pb}% {premium/discount}
• EV/EBITDA rank: #{sector_rank}/11 sectors

YTD performance ranking:
• Absolute return: {ytd_return}% (#{performance_rank}/11)
• Risk-adjusted: Sharpe {sharpe_ratio} vs market {market_sharpe}

Allocation rec: {overweight/neutral/underweight} ({allocation_range}%)

📋 Full analysis: https://www.colemorton.com/blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/

⚠️ Not financial advice. Past performance doesn't guarantee future results.

#{SECTOR} #SectorComparison #AllocationStrategy
```

### Template C: Allocation Strategy
```
🎯 {SECTOR} allocation strategy for {portfolio_type} portfolios:

Portfolio weighting guidance:
• Growth portfolios: {growth_allocation}%
• Balanced portfolios: {balanced_allocation}%
• Conservative portfolios: {conservative_allocation}%

Risk-return profile:
• Expected return: {expected_return}% (2Y horizon)
• Volatility: {volatility}% vs market {market_volatility}%
• Correlation to SPY: {spy_correlation}

{Sector} ETF ({ETF_SYMBOL}): {overweight/underweight} vs {benchmark_weight}% benchmark

📋 Full analysis: https://www.colemorton.com/blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/

⚠️ Not financial advice. Sector allocation carries risk.

#{SECTOR} #PortfolioAllocation #AssetAllocation
```

### Template D: Economic Sensitivity
```
📈 {SECTOR} economic sensitivity breakdown:

Key correlations:
• GDP growth: {gdp_correlation} correlation
• Employment: {employment_correlation} correlation
• Fed Funds Rate: {rate_correlation} correlation

Economic scenario analysis:
• GDP +1%: {gdp_plus_impact}% sector impact
• Rate +100bps: {rate_plus_impact}% impact
• Recession probability: {recession_impact}% downside

Current environment: {current_environment_assessment}

📋 Full analysis: https://www.colemorton.com/blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/

⚠️ Not financial advice. Economic sensitivity varies by conditions.

#{SECTOR} #EconomicSensitivity #MacroAnalysis
```

### Template E: ETF vs Stock Picking
```
🏗️ {SECTOR} exposure: ETF vs individual stocks

{Sector} ETF ({ETF_SYMBOL}) analysis:
• Top holdings: {top_holdings} (concentration: {concentration}%)
• Expense ratio: {expense_ratio}%
• AUM: ${aum} with {flow_trend} flows

vs Individual stock selection:
• Active management opportunity: {alpha_potential}
• Concentration benefits: {concentration_advantage}
• Cost efficiency: ETF {cost_advantage}

Recommendation: {etf_vs_stocks_rec} for {investor_type} investors

📋 Full analysis: https://www.colemorton.com/blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/

⚠️ Not financial advice. Do your own research.

#{SECTOR} #ETFAnalysis #StockSelection
```

### Template Selection Logic
**Automated Template Selection Framework:**
- **IF** (economic cycle positioning strength > 0.8 AND GDP correlation > 0.6) → **Template A: Sector Rotation**
- **IF** (cross-sector ranking top 3 OR bottom 3 AND relative valuation extreme) → **Template B: Cross-Sector Comparison**
- **IF** (allocation guidance available AND risk-return profile complete) → **Template C: Allocation Strategy**
- **IF** (economic sensitivity analysis comprehensive AND correlations significant) → **Template D: Economic Sensitivity**
- **ELSE** → **Template E: ETF vs Stock Picking**

### Content Optimization Standards (Embedded)

#### Engagement Mechanics
1. **Lead with Allocation Numbers**: Specific percentages, weightings, correlations
2. **Strategic Emoji Usage**: 1-2 relevant emojis max for visual appeal
3. **Create Investment Curiosity**: Tease sector opportunities before revealing
4. **Include Economic Context**: Economic cycle and sensitivity insights
5. **End with Clear Allocation**: What investors should do with this sector

#### Writing Style Requirements
- **Plain Language**: No jargon without explanation
- **Active Voice**: "Technology outperforms" not "Technology is outperforming"
- **Specific Claims**: "12-15% allocation" not "significant allocation"
- **Present Tense**: Create immediacy and relevance
- **Confident Tone**: Back analysis with economic data and correlation scores

#### Character Count Optimization
- **Target Length**: 280 characters per tweet (can thread if needed)
- **Tweet 1**: Hook + core sector insight
- **Tweet 2** (if needed): Supporting economic data
- **Tweet 3** (if needed): Allocation/timing guidance

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
- **Input format:** `{SECTOR}_{YYYYMMDD}` (e.g., `technology_20250710`)
- **Output format:** `https://www.colemorton.com/blog/{sector-lowercase}-sector-analysis-{yyyymmdd}/`
- **Example conversion:** `technology_20250710` → `https://www.colemorton.com/blog/technology-sector-analysis-20250710/`

### File Output Requirements
**Primary Output File:**
```
./data/outputs/twitter/sector_analysis/{SECTOR}_{YYYYMMDD}.md
```

**File contains:**
- Clean X post content ready for copy/paste
- Character count for each tweet
- Selected template rationale
- Key sector insights extracted from source analysis
- Generated blog post URL for full sector analysis access

## Command Usage

**Execute Twitter synthesis from sector analysis:**
```
/twitter_sector_analysis {SECTOR}_{YYYYMMDD}
```

**Examples:**
- `/twitter_sector_analysis technology_20250811`
- `/twitter_sector_analysis healthcare_20250811`
- `/twitter_sector_analysis energy_20250811`

**DASV Processing Flow:**
1. **Load & validate** source sector analysis synthesis (≥9.0 confidence)
2. **Extract sector data** (thesis, positioning, sensitivity, allocation guidance)
3. **Integrate ETF data** for real-time validation and current pricing context
4. **Validate cross-sector** positioning and correlation accuracy
5. **Select optimal template** based on sector analysis characteristics
6. **Calculate sector synthesis confidence** with DASV standards
7. **Use twitter_writer sub-agent** to create engaging allocation content from structured data
8. **Apply enhancement** if validation file exists (target: ≥9.5 confidence)
9. **Export results** with complete sector quality metrics and traceability

**Enhancement Workflow:**
```
# Phase 1: Generate sector Twitter synthesis
/twitter_sector_analysis technology_20250811

# Phase 2: If synthesis confidence <9.5, apply validation enhancement
/twitter_sector_analysis {DATA_OUTPUTS}/twitter/sector_analysis/validation/technology_20250811_validation.json

# Phase 3: Validate institutional excellence achieved (≥9.5/10.0)
```

---

## MANDATORY WORKFLOW REMINDER

⚠️ **CRITICAL FIRST STEP**: Before processing any sector analysis, ALWAYS get current economic context using FRED MCP server and validate sector ETF pricing.

**Real-time Data Requirements:**
- Economic indicators current within 24 hours
- Sector ETF pricing validated against analysis fair value
- Cross-sector correlations updated with current market conditions

**Never use stale economic data from the sector analysis file - it may be outdated. Always use real-time economic data and current ETF pricing for accurate sector positioning.**

## Post-Execution Protocol

### Required Actions
1. **Generate Output Metadata**: Include collaboration metadata for sector content
2. **Store Outputs**: Save to `./data/outputs/twitter/sector_analysis/` directories
3. **Quality Validation**: Content accuracy and sector analysis compliance verification
4. **Content Tracking**: Performance metrics and institutional quality standards

### Output Metadata Template
```yaml
metadata:
  generated_by: "twitter-sector-analysis"
  timestamp: "{ISO-8601-timestamp}"
  sector: "{SECTOR}"
  content_type: "sector_analysis_post"

content_metrics:
  character_count: "{post-length}"
  engagement_optimized: true
  accuracy_verified: true
  economic_context_current: true

quality_assurance:
  sector_analysis_source: "{source-file}"
  economic_data_current: true
  twitter_best_practices: true
```

---

## DASV Architecture Benefits

**Clean Separation of Concerns**:
- **Domain Focus**: Command handles sector analysis data processing and ETF integration
- **Content Delegation**: Twitter_writer sub-agent handles all content creation and engagement
- **Quality Assurance**: DASV framework ensures institutional allocation guidance standards
- **Enhancement Protocol**: Systematic improvement targeting 9.5+ confidence with cross-sector validation

**Sector-Specific Quality Standards**:
- **Source Validation**: ≥9.0/10.0 synthesis confidence required
- **ETF Integration**: Real-time pricing validation with 3% variance threshold
- **Cross-Sector Consistency**: ≥0.85 correlation accuracy requirement
- **Allocation Guidance**: Clear portfolio weighting recommendations with risk-return profiles

**Integration Excellence**:
- **Twitter Writer**: Structured sector data handoff for optimal allocation content
- **ETF Data**: Real-time integration for sector pricing and flow validation
- **Enhancement Loop**: Validation-driven improvement targeting institutional excellence
- **Audit Trail**: Complete sector quality metrics and decision rationale

**Ready to generate DASV-compliant Twitter synthesis from institutional-grade sector analysis. Provide {SECTOR}_{YYYYMMDD} identifier to begin sector-focused data processing and twitter_writer integration.**
