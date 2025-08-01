# Comparative Analyst Discover

**DASV Phase 1: Fundamental Analysis Data Aggregation and Cross-Stock Intelligence Gathering**

Comprehensive aggregation and validation of existing fundamental analysis data for institutional-quality comparative analysis, focusing on data completeness verification and cross-stock intelligence integration for sophisticated investment decision-making.

## Purpose

The Comparative Analysis Discovery phase represents the systematic aggregation and validation of existing fundamental analysis outputs required for comprehensive cross-stock comparative analysis. This command provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on fundamental analysis dependency validation, data quality cross-verification, and comparative intelligence requirements.

**Expected Output Schema**: `/scripts/schemas/comparative_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute comparative analysis discovery. Ensure output conforms to `/scripts/schemas/comparative_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: comparative_analyst
**Action**: discover
**Output Location**: `./data/outputs/comparative_analysis/discovery/`
**Next Phase**: comparative_analyst_analyze
**Template Reference**: `./data/outputs/comparative_analysis/MU_vs_DHR_20250730.md` (target output structure reference)

## Parameters

- `ticker_1`: Primary stock symbol for comparison (required, uppercase format)
- `ticker_2`: Secondary stock symbol for comparison (required, uppercase format)
- `comparison_depth`: Comparative analysis depth - `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `confidence_threshold`: Minimum confidence for comparative conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)
- `fundamental_analysis_validation`: Validate fundamental analysis dependencies - `true` | `false` (optional, default: true)
- `economic_context_integration`: Integrate comparative economic context - `true` | `false` (optional, default: true)

## Data Sources and Integration

**Primary Dependencies:**
1. **Fundamental Analysis Files** - Complete fundamental analysis JSON outputs from `./data/outputs/fundamental_analysis/analysis/`
2. **Discovery Data Inheritance** - Market data, company overviews, and economic context from fundamental analysis
3. **Sector/Industry Context** - Cross-sector positioning from `./data/outputs/sector_analysis/` and `./data/outputs/industry_analysis/`
4. **Economic Context Validation** - FRED economic indicators and policy implications from existing fundamental analysis
5. **Supplementary CLI Services** - Limited use for missing data validation when fundamental analysis incomplete

**Integration Requirements:**
- **FAIL-FAST Validation**: Immediate failure if required fundamental analysis files missing or incomplete
- Fundamental analysis data completeness verification (≥95% data quality required for both stocks)
- Cross-stock data consistency validation and confidence propagation
- Economic context preservation and comparative integration from existing analyses
- Sector positioning intelligence aggregation for cross-sector comparative framework
- Supplementary data collection only when critical comparative metrics unavailable locally

## Data Flow Integration

### Input Requirements
- `ticker_1`: Primary stock symbol (uppercase format, required)
- `ticker_2`: Secondary stock symbol (uppercase format, required)
- `confidence_threshold`: Comparative analysis quality threshold (0.8-0.95, default: 0.9)
- `fundamental_analysis_validation`: Dependency validation flag (default: true)

### Fundamental Analysis Dependencies
- **Required Files**: `{TICKER_1}_{YYYYMMDD}_analysis.json` and `{TICKER_2}_{YYYYMMDD}_analysis.json`
- **Data Completeness**: Both fundamental analysis files must have ≥95% data quality scores
- **Economic Context**: Preserved FRED economic indicators and policy implications from both analyses
- **Sector Context**: Cross-sector positioning intelligence when stocks from different sectors

### Output Integration
**Primary Output**: `./data/outputs/comparative_analysis/discovery/{TICKER_1}_vs_{TICKER_2}_{YYYYMMDD}_discovery.json`
**Schema Compliance**: Must conform to `/scripts/schemas/comparative_analysis_discovery_schema.json`
**Downstream Dependencies**:
- comparative_analyst_analyze (next DASV phase)
- twitter_comparative_analysis (social media content generation)
- portfolio_construction (allocation strategies)
- investment_decision_framework (comparative investment guidance)

## Data Aggregation Requirements

### Fundamental Analysis Data Extraction
**Company Intelligence Aggregation**:
- Business model comparison and revenue stream analysis from existing fundamental analysis
- Financial health scorecard aggregation (A-F grades) for both stocks
- Management assessment and track record comparison from fundamental analysis files
- Competitive moat strength and durability comparative assessment

**Market Data Inheritance**:
- Current price validation and consistency across both stock analyses
- Market cap positioning and trading metrics comparison
- Beta analysis and volatility profile comparative assessment
- Performance attribution across multiple timeframes from existing data

**Economic Context Integration**:
- Economic sensitivity matrices comparison from both fundamental analyses
- Interest rate environment impact assessment on both stocks
- Sector-specific economic implications and policy impact comparison
- Business cycle positioning comparative framework

**Cross-Sector Intelligence** (when applicable):
- Sector rotation implications and positioning assessment
- Industry dynamics comparison and competitive landscape analysis
- Regulatory environment comparative assessment across sectors
- Economic resilience and defensive characteristics comparison

## Output Structure and Schema

**File Naming**: `{TICKER_1}_vs_{TICKER_2}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/comparative_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/comparative_analysis_discovery_schema.json`

### Required Output Components
- **Comparative Company Profiles**: Business model comparison, sector positioning, scale analysis
- **Market Data Comparison**: Pricing validation, trading metrics, performance attribution
- **Economic Context Integration**: Comparative economic sensitivity, policy impact analysis
- **Financial Health Aggregation**: A-F grade comparison, trend analysis, strength assessment
- **Competitive Intelligence**: Moat strength comparison, industry positioning, market dynamics
- **Data Quality Assessment**: Cross-validation results, confidence propagation, dependency status

### Schema Compliance Standards
- Both fundamental analysis files validated with ≥95% data quality scores
- Cross-stock data consistency verification across all major metrics
- Overall comparative analysis confidence ≥ 0.90 for institutional standards
- Complete comparative intelligence with investment decision framework preparation

## Quality Standards and Requirements

### Pre-Execution Requirements
- **CRITICAL**: Both ticker symbols format validation (1-5 uppercase letters each)
- **FAIL-FAST**: Fundamental analysis file existence validation for both stocks
- Fundamental analysis data quality verification (≥95% required for both files)
- Confidence threshold configuration based on comparison depth parameter

### Data Quality Standards
**Fundamental Analysis Validation**:
- **MANDATORY**: Both required fundamental analysis files must exist and be complete
- Cross-stock data consistency verification across all major financial metrics
- Economic context preservation and comparative integration validation
- Financial health grade validation and confidence propagation

**Institutional-Grade Thresholds**:
- Overall comparative analysis confidence ≥ 0.90
- Both fundamental analyses must have ≥95% data quality scores
- Cross-validation confidence scoring for all comparative metrics
- Complete dependency validation with fail-fast error handling

### Enhanced Comparative Requirements
- Cross-sector intelligence aggregation when stocks from different sectors
- Comparative insights with minimum 5 initial comparative observations
- Data completeness gaps identification for comparative analysis enhancement
- Economic context integration and policy impact comparative assessment

## Security and Implementation Notes

### Data Privacy and Access
- Fundamental analysis files accessed securely from local data repository
- No external API keys required for primary comparative analysis discovery
- Supplementary CLI services (when needed) access keys from secure configuration
- All comparative data aggregated locally with no external data exposure

### Dependency Reliability
- **FAIL-FAST Protocol**: Immediate termination if required fundamental analysis files missing
- Fundamental analysis data quality validation before processing
- Cross-stock data consistency verification with error reporting
- Graceful handling of missing sector/industry context with supplementary data collection

## Expected Outcomes

### Comparative Discovery Quality Targets
- **Overall Comparative Confidence**: ≥ 90% through fundamental analysis data aggregation
- **Data Completeness**: ≥ 95% cross-stock data consistency and validation
- **Financial Health Integration**: Complete A-F grade comparison with trend analysis
- **Dependency Validation**: 100% fundamental analysis file completeness verification

### Key Deliverables
- Comprehensive comparative company intelligence with business model analysis
- Cross-validated financial metrics and performance attribution comparison
- Economic context integration with comparative policy impact assessment
- Competitive intelligence with moat strength and industry positioning analysis
- Comparative insights identifying investment decision framework priorities
- Quality assessment with cross-stock confidence propagation and validation results

**Integration with DASV Framework**: This command provides the foundational comparative intelligence required for the subsequent comparative analyze phase, ensuring high-quality aggregated data for sophisticated cross-stock investment analysis.

**Author**: Cole Morton
