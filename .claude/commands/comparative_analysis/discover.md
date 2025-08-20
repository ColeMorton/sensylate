# Comparative Analyst Discover

**DASV Phase 1: Fundamental Analysis Data Aggregation and Cross-Stock Intelligence Gathering**

Comprehensive aggregation and validation of existing fundamental analysis data for institutional-quality comparative analysis, focusing on data completeness verification and cross-stock intelligence integration for sophisticated investment decision-making using researcher sub-agent orchestration.

## Purpose

The Comparative Analysis Discovery phase defines the requirements for systematic aggregation and validation of existing fundamental analysis outputs required for comprehensive cross-stock comparative analysis. This specification focuses on **what** comparative intelligence and data validation is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/{SCRIPTS_BASE}/schemas/comparative_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute comparative analysis discovery. Ensure output conforms to `/{SCRIPTS_BASE}/schemas/comparative_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: comparative_analyst
**Action**: discover
**Output Location**: `./{DATA_OUTPUTS}/comparative_analysis/discovery/`
**Next Phase**: comparative_analyst_analyze
**Template Reference**: `./{TEMPLATES_BASE}/analysis/comparative_analysis_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `ticker_1`: Primary stock symbol for comparison (required, uppercase format)
- `ticker_2`: Secondary stock symbol for comparison (required, uppercase format)
- `comparison_depth`: Comparative analysis depth - `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `confidence_threshold`: Minimum confidence for comparative conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)
- `fundamental_analysis_validation`: Validate fundamental analysis dependencies - `true` | `false` (optional, default: true)
- `economic_context_integration`: Integrate comparative economic context - `true` | `false` (optional, default: true)

## Data Requirements

### Core Data Categories

**Fundamental Analysis Data Integration Requirements**:
- Complete fundamental analysis JSON outputs from both comparison entities
- Market data, company overviews, and economic context inheritance validation
- Financial health scorecard aggregation and comparative grading
- Management assessment and competitive positioning comparison
- Valuation methodology comparison and relative value assessment

**Cross-Stock Intelligence Requirements**:
- Business model comparison and revenue stream diversification analysis
- Competitive moat strength assessment and durability comparison
- Market positioning evaluation and industry leadership analysis
- Geographic exposure comparison and international market sensitivity
- Innovation pipeline assessment and R&D investment comparison

**Economic Context Integration Requirements**:
- Economic sensitivity matrix comparison across both entities
- Interest rate environment impact assessment and comparative resilience
- Business cycle positioning analysis and economic defensiveness
- Sector-specific economic implications and cross-sector comparison
- Policy impact assessment and regulatory environment comparison

**Cross-Sector Intelligence Requirements** (when applicable):
- Sector rotation implications and relative positioning assessment
- Industry dynamics comparison and competitive landscape analysis
- Regulatory environment comparative assessment across sectors
- Economic resilience comparison and defensive characteristic evaluation
- Market correlation analysis and diversification benefit assessment

### Quality Standards
- **Dependency Validation**: FAIL-FAST approach if required fundamental analysis files missing
- **Data Completeness**: ≥95% data quality scores required for both comparison entities
- **Cross-Validation**: Comprehensive data consistency verification across entities
- **Economic Integration**: Complete preservation of economic context from source analyses
- **Comparative Intelligence**: Statistical validation of cross-entity comparison methodology

## Output Structure and Schema

**File Naming**: `{TICKER_1}_vs_{TICKER_2}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./{DATA_OUTPUTS}/comparative_analysis/discovery/`
**Schema Definition**: `/{SCRIPTS_BASE}/schemas/comparative_analysis_discovery_schema.json`

### Required Output Components
- **Comparative Company Profiles**: Business model comparison, sector positioning, scale analysis
- **Market Data Comparison**: Pricing validation, trading metrics, performance attribution
- **Economic Context Integration**: Comparative economic sensitivity and policy impact analysis
- **Financial Health Aggregation**: A-F grade comparison, trend analysis, strength assessment
- **Competitive Intelligence**: Moat strength comparison, industry positioning, market dynamics
- **Quality Metrics**: Cross-validation results, confidence propagation, dependency status assessment

### Schema Compliance Standards
- Both fundamental analysis files validated with ≥95% data quality scores
- Cross-stock data consistency verification across all major financial metrics
- Comparative analysis confidence ≥ 0.90 for institutional standards compliance
- Complete comparative intelligence with investment decision framework preparation

## Expected Outcomes

### Discovery Quality Targets
- **Fundamental Data Integration**: ≥ 95% confidence in source data quality validation
- **Cross-Stock Consistency**: ≥ 92% confidence in comparative data validation
- **Economic Context Preservation**: ≥ 90% confidence in economic factor integration
- **Comparative Intelligence**: ≥ 90% confidence in cross-entity analysis framework

### Key Deliverables
- Comprehensive comparative company intelligence with business model analysis
- Cross-validated financial metrics and performance attribution comparison
- Economic context integration with comparative policy impact assessment
- Competitive intelligence with moat strength and industry positioning analysis
- Investment decision framework with comparative risk and opportunity assessment
- Quality assessment with cross-validation results and confidence propagation metrics

**Integration with DASV Framework**: This command provides the foundational comparative intelligence required for the subsequent comparative analyze phase, ensuring high-quality aggregated data for sophisticated cross-stock investment analysis.

**Author**: Cole Morton
