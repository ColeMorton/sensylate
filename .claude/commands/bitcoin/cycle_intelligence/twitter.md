# Bitcoin Cycle Intelligence Twitter Synthesis Command

**Command Classification**: ₿ **DASV Synthesis Command**
**DASV Phase**: Synthesis (Twitter Sub-Domain)
**Input Phase**: Synthesis (Bitcoin Cycle Intelligence Domain)
**Quality Requirement**: ≥9.0/10.0 synthesis confidence
**Enhancement Target**: ≥9.5/10.0 with validation enhancement
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-09-09)*
**Outputs To**: `{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/bitcoin_cycle_twitter_script.py`
**Script Class**: `BitcoinCycleTwitterScript`
**Registry Name**: `bitcoin_cycle_twitter`
**Content Types**: `["bitcoin_cycle_twitter"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="bitcoin_cycle_twitter",
    content_types=["bitcoin_cycle_twitter"],
    requires_validation=True
)
class BitcoinCycleTwitterScript(BaseScript):
    """
    Bitcoin cycle intelligence Twitter content generation script

    Parameters:
        analysis_date (str): Analysis date in YYYYMMDD format
        cycle_phase (Optional[str]): Bitcoin cycle phase override
        template_variant (Optional[str]): Specific template to use
        validation_file (Optional[str]): Path to validation file for enhancement
        validate_content (bool): Whether to validate generated content
    """
```

**Supporting Components**:
```yaml
bitcoin_cycle_analyzer:
  path: "{SCRIPTS_BASE}/bitcoin_cycle_intelligence/bitcoin_cycle_analyzer.py"
  class: "BitcoinCycleAnalyzer"
  purpose: "Bitcoin cycle analysis data extraction and validation"

onchain_data_collector:
  path: "{SCRIPTS_BASE}/bitcoin_data/onchain_data_collector.py"
  class: "OnchainDataCollector"
  purpose: "Real-time Bitcoin on-chain metrics collection (MVRV, NUPL, hash rate)"

bitcoin_valuation_analyzer:
  path: "{SCRIPTS_BASE}/bitcoin_data/bitcoin_valuation_analyzer.py"
  class: "BitcoinValuationAnalyzer"
  purpose: "Multi-model Bitcoin valuation and cycle position analysis"

twitter_template_renderer:
  path: "{SCRIPTS_BASE}/twitter_template_renderer.py"
  class: "TwitterTemplateRenderer"
  purpose: "Jinja2 template rendering with Bitcoin cycle intelligence optimization"
```

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/twitter/bitcoin_cycle/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| bitcoin_cycle_analysis | `bitcoin_cycle/twitter_cycle_analysis.j2` | MVRV Z-Score >2.0 AND cycle phase = bull_market | Bitcoin cycle positioning and phase analysis |
| onchain_metrics | `bitcoin_cycle/twitter_onchain_metrics.j2` | NUPL zone = optimism AND LTH accumulation active | On-chain indicators and network health |
| network_health | `bitcoin_cycle/twitter_network_health.j2` | Hash rate growth >5% AND mining health score >8.0 | Network security and mining economics |
| valuation_framework | `bitcoin_cycle/twitter_valuation.j2` | Multiple valuation models AND fair value confidence >0.85 | Bitcoin valuation and price discovery |
| cycle_dashboard | `bitcoin_cycle/twitter_cycle_dashboard.j2` | Default fallback for Bitcoin cycle intelligence | Comprehensive cycle indicator dashboard |

**Shared Components**:
```yaml
bitcoin_base_template:
  path: "{TEMPLATES_BASE}/twitter/shared/base_twitter.j2"
  purpose: "Base template with common macros and Bitcoin cycle formatting"

bitcoin_cycle_components:
  path: "{TEMPLATES_BASE}/twitter/shared/bitcoin_cycle_components.j2"
  purpose: "Bitcoin-specific components for on-chain indicators and cycle analysis"

compliance_template:
  path: "{TEMPLATES_BASE}/twitter/validation/bitcoin_compliance.j2"
  purpose: "Bitcoin investment compliance and risk disclaimer validation"
```

**Template Selection Algorithm**:
```python
def select_bitcoin_cycle_template(bitcoin_cycle_data):
    """Select optimal template for Bitcoin cycle Twitter content"""

    # Bitcoin cycle analysis template for cycle phase focus
    if (bitcoin_cycle_data.get('mvrv_z_score', 0) > 2.0 and
        bitcoin_cycle_data.get('cycle_phase') == 'bull_market'):
        return 'bitcoin_cycle/twitter_cycle_analysis.j2'

    # On-chain metrics for NUPL optimism zone
    elif (bitcoin_cycle_data.get('nupl_zone') == 'optimism' and
          bitcoin_cycle_data.get('lth_accumulation_active', False)):
        return 'bitcoin_cycle/twitter_onchain_metrics.j2'

    # Network health for hash rate and mining focus
    elif (bitcoin_cycle_data.get('hash_rate_growth', 0) > 0.05 and
          bitcoin_cycle_data.get('mining_health_score', 0) > 8.0):
        return 'bitcoin_cycle/twitter_network_health.j2'

    # Valuation framework for multi-model analysis
    elif (bitcoin_cycle_data.get('fair_value_confidence', 0) > 0.85 and
          bitcoin_cycle_data.get('multiple_valuation_models', False)):
        return 'bitcoin_cycle/twitter_valuation.j2'

    # Default Bitcoin cycle dashboard
    return 'bitcoin_cycle/twitter_cycle_dashboard.j2'
```

## CLI Service Integration

**Service Commands**:
```yaml
coingecko_cli:
  command: "python {SCRIPTS_BASE}/coingecko_cli.py"
  usage: "{command} bitcoin-metrics price,market-cap,volume,mvrv --env prod --output-format json"
  purpose: "Bitcoin price data and fundamental metrics for cycle analysis"
  health_check: "{command} health --env prod"
  priority: "primary"

mempool_space_cli:
  command: "python {SCRIPTS_BASE}/mempool_space_cli.py"
  usage: "{command} onchain-metrics hash-rate,difficulty,fees,addresses --env prod --output-format json"
  purpose: "Bitcoin network health and on-chain activity metrics"
  health_check: "{command} health --env prod"
  priority: "primary"

coinmetrics_cli:
  command: "python {SCRIPTS_BASE}/coinmetrics_cli.py"
  usage: "{command} cycle-indicators mvrv,nupl,sopr,lth-supply --env prod --output-format json"
  purpose: "Advanced Bitcoin cycle indicators and long-term holder metrics"
  health_check: "{command} health --env prod"
  priority: "primary"

glassnode_cli:
  command: "python {SCRIPTS_BASE}/glassnode_cli.py"
  usage: "{command} network-analysis realized-price,hodl-waves,exchange-flows --env prod --output-format json"
  purpose: "Bitcoin network analysis and institutional flow data"
  health_check: "{command} health --env prod"
  priority: "secondary"

alternative_me_cli:
  command: "python {SCRIPTS_BASE}/alternative_me_cli.py"
  usage: "{command} fear-greed-index --env prod --output-format json"
  purpose: "Bitcoin sentiment indicators and market psychology metrics"
  health_check: "{command} health --env prod"
  priority: "tertiary"
```

**Bitcoin Cycle Twitter Integration Protocol**:
```bash
# Bitcoin price and market data collection
python {SCRIPTS_BASE}/coingecko_cli.py bitcoin-metrics price,market-cap,volume,mvrv --env prod --output-format json

# Bitcoin network health and on-chain metrics
python {SCRIPTS_BASE}/mempool_space_cli.py onchain-metrics hash-rate,difficulty,fees,addresses --env prod --output-format json

# Advanced Bitcoin cycle indicators
python {SCRIPTS_BASE}/coinmetrics_cli.py cycle-indicators mvrv,nupl,sopr,lth-supply --env prod --output-format json

# Bitcoin network analysis and flow data
python {SCRIPTS_BASE}/glassnode_cli.py network-analysis realized-price,hodl-waves,exchange-flows --env prod --output-format json
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  bitcoin_cycle_analysis: "HIGHEST_AUTHORITY"  # Primary Bitcoin cycle intelligence documents
  coinmetrics_data: "ONCHAIN_AUTHORITY"  # Advanced Bitcoin cycle indicators
  mempool_space_data: "NETWORK_AUTHORITY"  # Network health and mining data
  coingecko_data: "PRICE_AUTHORITY"  # Bitcoin price and market data

conflict_resolution:
  bitcoin_precedence: "bitcoin_cycle_analysis_primary"  # Bitcoin cycle analysis takes priority
  onchain_authority: "coinmetrics_primary_glassnode_secondary"  # CoinMetrics for MVRV/NUPL, Glassnode for flows
  data_staleness: "1_hour"  # Maximum age for Bitcoin price data
  variance_threshold: "2%"  # BLOCKING if Bitcoin price variance exceeds
  action: "fail_fast_on_conflict"  # Resolution strategy
```

## Data Flow & File References

**Input Sources**:
```yaml
bitcoin_cycle_document:
  path: "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/bitcoin_cycle_{YYYYMMDD}.md"
  format: "markdown"
  required: true
  description: "Primary Bitcoin cycle analysis with cycle thesis and network assessment"

bitcoin_onchain_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Real-time Bitcoin on-chain indicators (MVRV, NUPL, hash rate, LTH metrics)"

bitcoin_price_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Bitcoin price and market data from multiple exchanges"

network_health_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: false
  description: "Bitcoin network security and mining economics data"

validation_file:
  path: "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_{YYYYMMDD}_validation.json"
  format: "json"
  required: false
  description: "Validation file for post enhancement workflow"
```

**Output Structure**:
```yaml
primary_output:
  path: "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/bitcoin_cycle_{YYYYMMDD}.md"
  format: "markdown"
  description: "Generated Bitcoin cycle Twitter content ready for posting"

metadata_output:
  path: "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/bitcoin_cycle_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Template selection metadata and Bitcoin cycle quality assurance metrics"

validation_output:
  path: "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_{YYYYMMDD}_validation.json"
  format: "json"
  description: "Content validation results and Bitcoin cycle enhancement recommendations"

blog_url_output:
  path: "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/bitcoin_cycle_{YYYYMMDD}_blog_url.txt"
  format: "text"
  description: "Generated blog URL for full Bitcoin cycle intelligence access"
```

**Data Dependencies**:
```yaml
content_generation_flow:
  data_validation:
    - "bitcoin cycle analysis confidence ≥ 0.9"
    - "bitcoin price data currency ≤ 1 hour"
    - "on-chain data currency ≤ 24 hours"
    - "bitcoin price variance ≤ 2%"

  template_selection:
    - "bitcoin cycle analysis content evaluation"
    - "cycle phase positioning assessment"
    - "on-chain indicator priority determination"
    - "valuation model availability check"

  content_optimization:
    - "Twitter character limit compliance"
    - "bitcoin investment disclaimer inclusion"
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

# Execute Bitcoin cycle Twitter content generation
result = registry.execute_script(
    "bitcoin_cycle_twitter",
    analysis_date="20250718",
    validate_content=True
)

# Execute with specific template override
result = registry.execute_script(
    "bitcoin_cycle_twitter",
    analysis_date="20250718",
    template_variant="bitcoin_cycle_analysis",
    validate_content=True
)

# Execute post enhancement from validation file
result = registry.execute_script(
    "bitcoin_cycle_twitter",
    validation_file="bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_20250718_validation.json"
)
```

### Command Line Execution
```bash
# Via content automation CLI
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script bitcoin_cycle_twitter \
    --analysis-date 20250718 \
    --validate-content true

# Via direct script execution
python {SCRIPTS_BASE}/base_scripts/bitcoin_cycle_twitter_script.py \
    --analysis-date 20250718 \
    --template-variant onchain_metrics

# Post enhancement workflow
python {SCRIPTS_BASE}/base_scripts/bitcoin_cycle_twitter_script.py \
    --validation-file "{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_20250718_validation.json"

# With custom cycle phase override
python {SCRIPTS_BASE}/base_scripts/bitcoin_cycle_twitter_script.py \
    --analysis-date 20250718 \
    --cycle-phase bull_market
```

### Claude Command Execution
```
# Standard Bitcoin cycle Twitter content generation
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718

# Bitcoin cycle analysis with specific template
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718 template_variant=bitcoin_cycle_analysis

# On-chain metrics focus
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718 template_variant=onchain_metrics

# Post enhancement using validation file
/bitcoin_cycle_intelligence:twitter {DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_20250718_validation.json

# Network health template generation
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718 template_variant=network_health
```

### Bitcoin Cycle Intelligence Workflow Examples
```
# Bitcoin cycle intelligence workflow
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718

# Multi-cycle comparison workflow
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718 template_variant=onchain_metrics

# Network health analysis
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718 template_variant=network_health

# Post validation and enhancement
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250718
# → If validation score <9.0, enhance using:
/bitcoin_cycle_intelligence:twitter {DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_20250718_validation.json
```

You are a **Bitcoin cycle intelligence data processor** specialized in extracting domain-specific insights from comprehensive Bitcoin cycle analysis and preparing structured data for the twitter_writer agent.

**Separation of Concerns:**
- **This Command**: Bitcoin cycle data processing, DASV compliance, template selection
- **Twitter Writer Agent**: Content creation, hooks, engagement optimization
- **Integration**: Structured data handoff for optimal Bitcoin cycle content generation

## DASV Synthesis Framework Integration

### Bitcoin Cycle-Specific Input Validation
```python
def validate_bitcoin_cycle_synthesis(source_path):
    """Validate Bitcoin cycle intelligence synthesis input"""

    # Check source synthesis exists and is current
    if not source_path.exists() or data_age > timedelta(hours=48):
        raise SynthesisStalenessException("Source Bitcoin cycle synthesis too old or missing")

    # Verify source synthesis quality
    if source_confidence < 0.9:
        raise QualityThresholdException("Source Bitcoin cycle synthesis below institutional grade")

    # Validate Bitcoin cycle-specific schema
    if not validate_bitcoin_cycle_schema(source_path):
        raise SchemaValidationException("Source Bitcoin cycle synthesis schema invalid")
```

### Bitcoin Cycle Twitter Synthesis Confidence
```python
def calculate_bitcoin_cycle_synthesis_confidence(source_conf, onchain_data, network_integration):
    """Calculate Bitcoin cycle-specific Twitter synthesis confidence"""

    # Base confidence from source synthesis
    base_confidence = source_conf

    # Apply Bitcoin cycle-specific factors
    onchain_data_consistency = assess_onchain_data_accuracy()
    network_health_integration = assess_network_metrics_quality()
    cycle_positioning_precision = assess_cycle_phase_accuracy()
    valuation_model_clarity = assess_bitcoin_valuation_quality()

    # Calculate Bitcoin cycle Twitter synthesis confidence
    bitcoin_cycle_confidence = (base_confidence *
                               onchain_data_consistency *
                               network_health_integration *
                               cycle_positioning_precision *
                               valuation_model_clarity)

    # Enforce institutional threshold
    if bitcoin_cycle_confidence < 0.9:
        raise SynthesisQualityException(f"Bitcoin cycle synthesis confidence {bitcoin_cycle_confidence:.3f} below institutional threshold")

    return bitcoin_cycle_confidence
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

1. **Bitcoin Cycle Intelligence Reports** (PRIMARY): `@{DATA_OUTPUTS}/bitcoin_cycle_intelligence/`
   - **PRIORITY SOURCE**: Comprehensive Bitcoin cycle analysis files (bitcoin_cycle_YYYYMMDD.md)
   - Bitcoin cycle thesis, network health assessment, valuation framework
   - On-chain analysis, cycle positioning, mining economics integration
   - Bitcoin risk assessments, catalysts, and cycle scenario analysis
   - Multi-model valuation and institutional adoption metrics

2. **Real-Time Bitcoin On-Chain Data - CLI Standardized**: **MANDATORY**
   - Bitcoin cycle indicators via CoinMetrics/Glassnode for cycle context
   - MVRV Z-Score, NUPL, LTH metrics, hash rate, network health indicators
   - Use Bitcoin CLI Tools: `coinmetrics_cli()`, `mempool_space_cli()` for real-time data
   - **CRITICAL REQUIREMENT**: Always use current Bitcoin network context, never stale data
   - Ensures Twitter content reflects current Bitcoin cycle environment via CLI data validation
   - Production-grade reliability with intelligent caching, retry logic, and health monitoring

3. **Bitcoin Price and Market Data** (SECONDARY): Real-time Bitcoin market analysis
   - Multiple exchange price feeds: Coinbase, Binance, Kraken integration
   - Market cap, volume, volatility metrics, exchange flows
   - Bitcoin ETF flows, institutional adoption, custody metrics
   - **COINGECKO AUTHORITY PROTOCOL**: When conflicts arise, CoinGecko aggregated data takes precedence

4. **Bitcoin Network Health Data** (VALIDATION): Network security and mining frameworks
   - Hash rate trends, mining difficulty, network security budget
   - Mining pool distribution, geographic hash rate concentration
   - Used for network health validation and security assessment

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

## Bitcoin Cycle Intelligence Data Processing Pipeline

### Domain-Specific Data Extraction
```python
def load_bitcoin_cycle_synthesis(date):
    """Load and validate source Bitcoin cycle intelligence synthesis"""

    source_path = f"{DATA_OUTPUTS}/bitcoin_cycle_intelligence/bitcoin_cycle_{date}.md"

    # DASV Input Validation
    validate_bitcoin_cycle_synthesis(source_path)

    # Extract synthesis data
    synthesis_data = parse_bitcoin_cycle_synthesis(source_path)

    # Validate Bitcoin cycle-specific completeness
    required_sections = ['bitcoin_cycle_thesis', 'network_health_assessment', 'valuation_framework', 'risk_analysis']
    validate_bitcoin_cycle_completeness(synthesis_data, required_sections)

    return synthesis_data
```

### Bitcoin Cycle Template Selection Logic
```python
def select_bitcoin_cycle_template(bitcoin_data):
    """Domain-specific template selection for Bitcoin cycle analysis"""

    # Template A: Bitcoin Cycle Analysis (Cycle phase focus)
    if (bitcoin_data.get('mvrv_z_score', 0) > 2.0 and
        bitcoin_data.get('cycle_phase') == 'bull_market'):
        return 'bitcoin_cycle_analysis'

    # Template B: On-Chain Metrics (NUPL and LTH behavior)
    elif (bitcoin_data.get('nupl_zone') == 'optimism' and
          bitcoin_data.get('lth_accumulation_active', False)):
        return 'onchain_metrics'

    # Template C: Network Health (Hash rate and mining focus)
    elif (bitcoin_data.get('hash_rate_growth', 0) > 0.05 and
          bitcoin_data.get('mining_health_score', 0) > 8.0):
        return 'network_health'

    # Template D: Valuation Framework (Multi-model focus)
    elif (bitcoin_data.get('fair_value_confidence', 0) > 0.85 and
          bitcoin_data.get('multiple_valuation_models', False)):
        return 'valuation_framework'

    # Template E: Cycle Dashboard (Default)
    return 'cycle_dashboard'
```

### Bitcoin On-Chain Data Integration
```python
def integrate_bitcoin_onchain_data(bitcoin_data):
    """Integrate real-time Bitcoin on-chain indicators for cycle context validation"""

    # Bitcoin on-chain indicator mapping
    onchain_indicators = {
        'cycle_indicators': ['mvrv', 'nupl', 'pi_cycle_top', 'rainbow_price'],
        'network_health': ['hash_rate', 'difficulty', 'puell_multiple', 'fees'],
        'holder_behavior': ['lth_supply', 'sth_nupl', 'coin_days_destroyed'],
        'market_structure': ['exchange_flows', 'whale_activity', 'institutional_flows']
    }

    # Real-time Bitcoin on-chain data collection
    current_onchain = collect_bitcoin_onchain_data(onchain_indicators)

    # Validate against Bitcoin cycle analysis forecasts
    mvrv_variance = calculate_indicator_variance(bitcoin_data['mvrv_forecast'], current_onchain['mvrv'])
    if mvrv_variance > 0.02:  # 2% threshold for Bitcoin data
        log_bitcoin_variance_warning(mvrv_variance)

    # Update Bitcoin cycle context
    bitcoin_data['current_mvrv'] = current_onchain['mvrv']
    bitcoin_data['current_nupl'] = current_onchain['nupl']
    bitcoin_data['current_hash_rate'] = current_onchain['hash_rate']
    bitcoin_data['current_lth_supply'] = current_onchain['lth_supply']

    return bitcoin_data
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

### Bitcoin Investment Disclaimer Requirements (NON-NEGOTIABLE)

**CRITICAL: Every Twitter post MUST include Bitcoin investment disclaimers:**

- **Required Disclaimer Text**: One of the following MUST appear before the blog link:
  - `⚠️ Bitcoin investments carry significant risk. Past cycles don't guarantee future patterns.`
  - `⚠️ Bitcoin cycle analysis reflects current data. Market dynamics evolve rapidly.`
  - `⚠️ Bitcoin predictions carry uncertainty. Network conditions affect outcomes.`
  - `⚠️ Bitcoin valuations are estimates. Multiple scenarios possible.`
  - `⚠️ Bitcoin cycle indicators reflect current data. Trends may vary significantly.`

**ENFORCEMENT**: Templates automatically include disclaimer text. Content generation WILL FAIL validation if disclaimer is missing or modified.

**REGULATORY COMPLIANCE**:
- No definitive Bitcoin price predictions without uncertainty disclaimers
- Risk warnings are mandatory for all Bitcoin investment content
- Investment limitations disclaimers required for Bitcoin cycle projections
- Analytical framework clearly established in all posts

**VALIDATION CHECKPOINT**: Before export, every post MUST pass Bitcoin investment disclaimer compliance check.

## Content Optimization Framework (EMBEDDED)

### Template A: Bitcoin Cycle Analysis
```
₿ Bitcoin positioned in {cycle_phase} with MVRV Z-Score at {mvrv_z_score}

Bitcoin cycle metrics:
• Current phase: {current_phase} ({cycle_duration} days)
• Cycle completion: {cycle_completion}%
• NUPL zone: {nupl_zone} ({nupl_value})

On-chain indicators:
• Hash rate: {hash_rate} EH/s ({hash_rate_trend})
• LTH supply: {lth_supply}% ({lth_trend})
• Network value: {network_value_assessment}

📋 Full analysis: https://www.colemorton.com/blog/bitcoin-cycle-intelligence-{yyyymmdd}/

⚠️ Bitcoin investments carry significant risk. Past cycles don't guarantee future patterns.

#Bitcoin #CycleAnalysis #OnChain
```

### Template B: On-Chain Metrics Dashboard
```
📊 Bitcoin on-chain metrics analysis:

Cycle positioning indicators:
• MVRV Z-Score: {mvrv_z_score} ({mvrv_zone})
• NUPL: {nupl_value} ({nupl_zone})
• PI Cycle signal: {pi_cycle_status}

Network health metrics:
• Hash rate growth: {hash_rate_growth}%
• Mining difficulty: {difficulty_adjustment}
• LTH behavior: {lth_behavior_trend}

Valuation assessment: {valuation_grade} vs historical range

📋 Full analysis: https://www.colemorton.com/blog/bitcoin-cycle-intelligence-{yyyymmdd}/

⚠️ On-chain data reflects point-in-time metrics. Network dynamics evolve.

#Bitcoin #OnChain #CycleMetrics
```

### Template C: Network Health Assessment
```
🎯 Bitcoin network health outlook and security implications:

Network security assessment:
• Hash rate: {hash_rate} EH/s ({hash_rate_trend})
• Mining health: {mining_health_score}/10
• Decentralization: {decentralization_grade}

Network economics:
• Security budget: ${security_budget}M
• Puell Multiple: {puell_multiple}
• Mining profitability: {mining_profitability_status}

Network adoption: {adoption_trend} ({institutional_flows})

📋 Full analysis: https://www.colemorton.com/blog/bitcoin-cycle-intelligence-{yyyymmdd}/

⚠️ Network metrics reflect current conditions. Mining dynamics evolve.

#Bitcoin #NetworkHealth #Mining
```

### Template D: Bitcoin Valuation Framework
```
📈 Bitcoin valuation outlook and price discovery analysis:

Multi-model valuation:
• Stock-to-Flow: ${s2f_value} ({s2f_deviation}% deviation)
• Realized Price: ${realized_price} ({price_vs_realized}%)
• Network Value: {network_value_grade}

Valuation scenario probabilities:
• Fair value: {fair_value_probability}% - ${fair_value_range}
• Upside: {upside_probability}% - ${upside_target}
• Downside: {downside_probability}% - ${downside_support}

Key cycle catalysts: {primary_catalyst} ({catalyst_probability}%)

📋 Full analysis: https://www.colemorton.com/blog/bitcoin-cycle-intelligence-{yyyymmdd}/

⚠️ Bitcoin valuations are estimates. Multiple scenarios possible.

#Bitcoin #Valuation #CycleAnalysis
```

### Template E: Bitcoin Cycle Dashboard
```
📊 Bitcoin cycle intelligence comprehensive dashboard:

Core cycle metrics:
• Cycle phase: {cycle_phase} ({cycle_confidence}% confidence)
• MVRV Z-Score: {mvrv_z_score} ({mvrv_trend})
• NUPL zone: {nupl_zone} ({nupl_value})

Network conditions:
• Hash rate: {hash_rate} EH/s ({hash_rate_change})
• Network health: {network_health_score}/10 ({health_trend})
• Mining economics: {mining_economics_grade} ({profitability_trend})

Cycle momentum: {cycle_momentum_assessment}

📋 Full analysis: https://www.colemorton.com/blog/bitcoin-cycle-intelligence-{yyyymmdd}/

⚠️ Bitcoin cycle indicators reflect current data. Trends may vary.

#Bitcoin #CycleDashboard #BitcoinIntelligence
```

### Template Selection Logic
**Automated Template Selection Framework:**
- **IF** (MVRV Z-Score > 2.0 AND cycle phase = bull_market) → **Template A: Bitcoin Cycle Analysis**
- **IF** (NUPL zone = optimism AND LTH accumulation active) → **Template B: On-Chain Metrics Dashboard**
- **IF** (hash rate growth > 5% AND mining health score > 8.0) → **Template C: Network Health Assessment**
- **IF** (fair value confidence > 0.85 AND multiple valuation models available) → **Template D: Bitcoin Valuation Framework**
- **ELSE** → **Template E: Bitcoin Cycle Dashboard**

### Content Optimization Standards (Embedded)

#### Engagement Mechanics
1. **Lead with Bitcoin Data**: Specific percentages, MVRV scores, cycle phase probabilities
2. **Strategic Emoji Usage**: Bitcoin ₿ and cycle emojis for visual appeal
3. **Create Cycle Curiosity**: Tease Bitcoin cycle opportunities before revealing
4. **Include Network Context**: Hash rate trends and network security insights
5. **End with Clear Outlook**: What the Bitcoin cycle trajectory suggests

#### Writing Style Requirements
- **Plain Language**: No jargon without explanation
- **Active Voice**: "Bitcoin advances" not "Bitcoin is advancing"
- **Specific Claims**: "MVRV Z-Score 2.15" not "high valuation"
- **Present Tense**: Create immediacy and relevance
- **Evidence-Based Tone**: Back analysis with on-chain data and cycle probability scores

#### Character Count Optimization
- **Target Length**: 280 characters per tweet (can thread if needed)
- **Tweet 1**: Hook + core Bitcoin cycle insight
- **Tweet 2** (if needed): Supporting on-chain indicators
- **Tweet 3** (if needed): Network health/valuation implications

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
- **Input format:** `bitcoin_cycle_{YYYYMMDD}` (e.g., `bitcoin_cycle_20250710`)
- **Output format:** `https://www.colemorton.com/blog/bitcoin-cycle-intelligence-{yyyymmdd}/`
- **Example conversion:** `bitcoin_cycle_20250710` → `https://www.colemorton.com/blog/bitcoin-cycle-intelligence-20250710/`

### File Output Requirements
**Primary Output File:**
```
./{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/bitcoin_cycle_{YYYYMMDD}.md
```

**File contains:**
- Clean X post content ready for copy/paste
- Character count for each tweet
- Selected template rationale
- Key Bitcoin cycle insights extracted from source analysis
- Generated blog post URL for full Bitcoin cycle intelligence access

## Command Usage

**Execute Twitter synthesis from Bitcoin cycle intelligence:**
```
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_{YYYYMMDD}
```

**Examples:**
- `/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250811`
- `/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250812`
- `/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250813`

**DASV Processing Flow:**
1. **Load & validate** source Bitcoin cycle intelligence synthesis (≥9.0 confidence)
2. **Extract Bitcoin cycle data** (cycle thesis, network health, valuation framework, risk analysis)
3. **Integrate on-chain indicators** for real-time validation and current Bitcoin cycle context
4. **Validate network health** positioning and cycle accuracy
5. **Select optimal template** based on Bitcoin cycle analysis characteristics
6. **Calculate Bitcoin cycle synthesis confidence** with DASV standards
7. **Use twitter_writer sub-agent** to create engaging Bitcoin cycle content from structured data
8. **Apply enhancement** if validation file exists (target: ≥9.5 confidence)
9. **Export results** with complete Bitcoin cycle quality metrics and traceability

**Enhancement Workflow:**
```
# Phase 1: Generate Bitcoin cycle Twitter synthesis
/bitcoin_cycle_intelligence:twitter bitcoin_cycle_20250811

# Phase 2: If synthesis confidence <9.5, apply validation enhancement
/bitcoin_cycle_intelligence:twitter {DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/validation/bitcoin_cycle_20250811_validation.json

# Phase 3: Validate institutional excellence achieved (≥9.5/10.0)
```

---

## MANDATORY WORKFLOW REMINDER

⚠️ **CRITICAL FIRST STEP**: Before processing any Bitcoin cycle intelligence, ALWAYS get current Bitcoin on-chain context using Bitcoin CLI services and validate network health indicators.

**Real-time Data Requirements:**
- Bitcoin price data current within 1 hour
- On-chain data validated against cycle analysis forecasts
- Network health correlations updated with current Bitcoin conditions

**Never use stale Bitcoin data from the cycle analysis file - it may be outdated. Always use real-time Bitcoin on-chain indicators and current network data for accurate cycle positioning.**

## Post-Execution Protocol

### Required Actions
1. **Generate Output Metadata**: Include collaboration metadata for Bitcoin cycle content
2. **Store Outputs**: Save to `./{DATA_OUTPUTS}/bitcoin_cycle_intelligence/twitter/` directories
3. **Quality Validation**: Content accuracy and Bitcoin cycle intelligence compliance verification
4. **Content Tracking**: Performance metrics and institutional quality standards

### Output Metadata Template
```yaml
metadata:
  generated_by: "twitter-bitcoin-cycle-intelligence"
  timestamp: "{ISO-8601-timestamp}"
  analysis_date: "{YYYYMMDD}"
  content_type: "bitcoin_cycle_intelligence_post"

content_metrics:
  character_count: "{post-length}"
  engagement_optimized: true
  accuracy_verified: true
  bitcoin_context_current: true

quality_assurance:
  bitcoin_cycle_source: "{source-file}"
  onchain_data_current: true
  twitter_best_practices: true
```

---

## DASV Architecture Benefits

**Clean Separation of Concerns**:
- **Domain Focus**: Command handles Bitcoin cycle intelligence data processing and on-chain indicators integration
- **Content Delegation**: Twitter_writer sub-agent handles all content creation and engagement
- **Quality Assurance**: DASV framework ensures institutional Bitcoin cycle analysis standards
- **Enhancement Protocol**: Systematic improvement targeting 9.5+ confidence with network health validation

**Bitcoin Cycle-Specific Quality Standards**:
- **Source Validation**: ≥9.0/10.0 synthesis confidence required
- **On-Chain Integration**: Real-time indicators validation with 2% variance threshold
- **Network Health Consistency**: ≥0.85 network metrics accuracy requirement
- **Cycle Guidance**: Clear Bitcoin cycle phase assessments with valuation confidence levels

**Integration Excellence**:
- **Twitter Writer**: Structured Bitcoin cycle data handoff for optimal cycle intelligence content
- **Bitcoin Data**: Real-time integration for on-chain indicators and network validation
- **Enhancement Loop**: Validation-driven improvement targeting institutional excellence
- **Audit Trail**: Complete Bitcoin cycle quality metrics and decision rationale

**Ready to generate DASV-compliant Twitter synthesis from institutional-grade Bitcoin cycle intelligence. Provide bitcoin_cycle_{YYYYMMDD} identifier to begin Bitcoin cycle-focused data processing and twitter_writer integration.**
