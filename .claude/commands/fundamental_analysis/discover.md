# Fundamental Analyst Discover

**DASV Phase 1: Data Collection and Context Gathering**

Comprehensive financial data collection and market intelligence gathering for institutional-quality fundamental analysis using systematic discovery protocols and researcher sub-agent orchestration.

## Purpose

The Fundamental Analysis Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive fundamental analysis. This specification focuses on **what** data is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/{SCRIPTS_BASE}/schemas/fundamental_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute fundamental analysis discovery. Ensure output conforms to `/{SCRIPTS_BASE}/schemas/fundamental_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: fundamental_analyst
**Action**: discover
**Output Location**: `./{DATA_OUTPUTS}/fundamental_analysis/discovery/`
**Next Phase**: fundamental_analyst_analyze
**Template Reference**: `./{TEMPLATES_BASE}/analysis/fundamental_analysis_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)

## Data Requirements

### Core Data Categories

**Company Intelligence Requirements**:
- Complete business model and revenue stream analysis
- Comprehensive financial statement data (income statement, balance sheet, cash flow)
- Management quality assessment and governance analysis
- Analyst recommendations and institutional price targets
- Insider trading patterns and ownership structure

**Market Data Requirements**:
- Current and historical pricing with multi-source validation
- Trading volume analysis and market performance metrics
- Technical indicators and market sentiment assessment
- Peer group identification and comparative positioning

**Economic Context Requirements**:
- Federal Reserve policy indicators and macroeconomic environment
- Interest rate sensitivity and economic cycle positioning
- Global economic factors affecting company operations
- Sector-specific economic implications and correlations

**Regulatory Intelligence Requirements**:
- SEC filing analysis and compliance status assessment
- Regulatory risk identification and impact analysis
- Corporate governance quality and transparency metrics

### Quality Standards
- **Multi-Source Validation**: Cross-validation across multiple data sources with confidence scoring
- **Institutional-Grade Thresholds**: Overall data quality ≥ 0.90 for institutional standards
- **Data Completeness**: ≥ 85% field population for comprehensive analysis
- **Service Reliability**: ≥ 80% health score across data services

## Output Structure and Schema

**File Naming**: `{TICKER}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./{DATA_OUTPUTS}/fundamental_analysis/discovery/`
**Schema Definition**: `/{SCRIPTS_BASE}/schemas/fundamental_analysis_discovery_schema.json`

### Required Output Components
- **Company Profile**: Business description, financial metrics, management information
- **Market Analysis**: Pricing data, trading metrics, technical indicators
- **Economic Context**: Federal Reserve indicators, global economic factors
- **Financial Statements**: Income statement, balance sheet, cash flow data
- **Peer Analysis**: Comparable companies with selection rationale
- **Quality Metrics**: Confidence scores, data completeness, source reliability

### Schema Compliance Standards
- Multi-source data validation targeting high confidence scores
- Complete discovery insights with research priorities identified
- Institutional-grade quality standards compliance

## Expected Outcomes

### Discovery Quality Targets
- **Overall Data Quality**: ≥ 97% confidence through multi-source validation
- **Data Completeness**: ≥ 92% across all required categories
- **Financial Statement Confidence**: ≥ 95% with complete cash flow integration
- **Service Health**: ≥ 80% operational status across data services

### Key Deliverables
- Comprehensive company profile with business intelligence
- Multi-source validated financial metrics and ratios
- Economic context with sector-specific implications
- Peer group analysis with selection rationale
- Discovery insights identifying research priorities and data gaps
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational data required for the subsequent analyze phase, ensuring high-quality input for systematic financial analysis.

**Author**: Cole Morton
