# Fundamental Analyst Discover

**DASV Phase 1: Data Collection and Context Gathering**

Comprehensive financial data collection and market intelligence gathering for institutional-quality fundamental analysis using systematic discovery protocols and production-grade CLI data acquisition methodologies.

## Purpose

The Fundamental Analysis Discovery phase represents the systematic collection and initial structuring of all data required for comprehensive fundamental analysis. This command provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on data acquisition standards, quality assessment criteria, and foundational research requirements.

**Expected Output Schema**: `/scripts/schemas/fundamental_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute fundamental analysis discovery. Ensure output conforms to `/scripts/schemas/fundamental_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: fundamental_analyst
**Action**: discover
**Output Location**: `./data/outputs/fundamental_analysis/discovery/`
**Next Phase**: fundamental_analyst_analyze
**Template Reference**: `./templates/analysis/fundamental_analysis_template.md` (final output structure awareness)

## Parameters

- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)

## Data Sources and Integration

**Required Financial Services:**
1. **Yahoo Finance CLI** - Core market data, fundamentals, and financial statements
2. **Alpha Vantage CLI** - Real-time quotes, AI sentiment analysis, and technical indicators
3. **SEC EDGAR CLI** - Regulatory filings, SEC financial statements, and compliance data
4. **FRED Economic CLI** - Federal Reserve economic data and macroeconomic indicators
5. **IMF Data CLI** - Global economic indicators and country risk assessment
6. **CoinGecko CLI** - Cryptocurrency market data for broader sentiment analysis
7. **FMP CLI** - Advanced financials, insider trading data, and company profiles

**Integration Requirements:**
- Multi-source price validation across Yahoo Finance, Alpha Vantage, and FMP
- Automatic cross-validation with confidence scoring and institutional-grade data quality assessment
- Real-time economic context integration with Fed policy and yield curve analysis
- Cryptocurrency sentiment analysis for broader risk appetite assessment
- Production-grade caching and rate limiting for API efficiency
- Comprehensive error handling with graceful degradation and source reliability scoring

## Data Flow Integration

### Input Requirements
- `ticker`: Stock symbol (uppercase format, required)
- `confidence_threshold`: Data quality threshold (0.6-0.8, default: 0.7)
- `validation_enhancement`: Optional optimization based on existing validation files

### CLI Services Integration
- **7 Required Services**: Yahoo Finance, Alpha Vantage, FMP, SEC EDGAR, FRED, CoinGecko, IMF
- **Multi-Source Validation**: Cross-validation across primary data sources
- **Economic Context**: Federal Reserve and global economic indicators
- **Market Sentiment**: Cryptocurrency and broader market sentiment analysis

### Output Integration
**Primary Output**: `./data/outputs/fundamental_analysis/discovery/{TICKER}_{YYYYMMDD}_discovery.json`
**Schema Compliance**: Must conform to `/scripts/schemas/fundamental_analysis_discovery_schema.json`
**Downstream Dependencies**:
- fundamental_analyst_analyze (next DASV phase)
- twitter_fundamental_analysis (social media content generation)
- sector_analyst (comparative analysis)
- social_media_strategist (investment themes)

## Data Collection Requirements

### Core Data Categories
**Company Intelligence**:
- Business model, revenue streams, competitive positioning
- Financial statements and cash flow analysis
- Management information and insider trading patterns
- Analyst recommendations and price targets

**Market Data**:
- Real-time pricing with multi-source validation
- Trading volumes and market performance metrics
- Technical indicators and sentiment analysis
- Historical performance across specified timeframes

**Economic Context**:
- Federal Reserve policy indicators (rates, unemployment, yield curve)
- Cryptocurrency market sentiment for risk appetite assessment
- Global economic indicators and country risk factors
- Sector-specific economic implications

**Regulatory Intelligence**:
- SEC filings and compliance status
- Regulatory risk assessment
- Corporate governance factors

## Output Structure and Schema

**File Naming**: `{TICKER}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/fundamental_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/fundamental_analysis_discovery_schema.json`

### Required Output Components
- **Company Profile**: Business description, financial metrics, management information
- **Market Analysis**: Pricing data, trading metrics, technical indicators
- **Economic Context**: Federal Reserve indicators, global economic factors
- **Financial Statements**: Income statement, balance sheet, cash flow data
- **Peer Analysis**: Comparable companies with selection rationale
- **Quality Metrics**: Confidence scores, data completeness, source reliability

### Schema Compliance Standards
- Minimum 5 CLI services utilized for institutional-grade analysis
- Price consistency validation across multiple sources (targeting 1.0 confidence)
- Overall data quality ≥ 0.90 for institutional standards
- Complete discovery insights with research priorities identified

## Quality Standards and Requirements

### Pre-Execution Requirements
- Ticker symbol format validation (1-5 uppercase letters)
- CLI services configuration and API key validation
- Confidence threshold configuration based on depth parameter
- Optional validation enhancement protocol activation

### Data Quality Standards
**Multi-Source Validation**:
- Price consistency verification across 3+ sources
- Financial metrics cross-validation
- Economic indicators freshness validation
- Company profile data consistency checks

**Institutional-Grade Thresholds**:
- Overall data quality ≥ 0.90
- Service reliability ≥ 80% health score
- Confidence scoring for all major data categories
- Complete data validation with gap identification

### Enhanced Analysis Requirements
- Peer group analysis with 3-10 comparable companies
- Discovery insights with minimum 3 initial observations
- Data gaps identification for next phase planning
- Source reliability scoring for all CLI services

## Security and Implementation Notes

### API Key Security
- API keys stored securely in `./config/financial_services.yaml`
- API keys MUST NEVER be included in discovery outputs or logs
- CLI services automatically access keys from secure configuration
- Output references config file without exposing sensitive information

### Service Reliability
- Dynamic tracking of successful CLI service responses
- Include only services that successfully provided data in output
- Graceful degradation when services are unavailable
- Service health monitoring and performance metrics

## Expected Outcomes

### Discovery Quality Targets
- **Overall Data Quality**: ≥ 97% confidence through multi-source validation
- **Data Completeness**: ≥ 92% across all required categories
- **Financial Statement Confidence**: ≥ 95% with complete cash flow integration
- **Service Health**: ≥ 80% operational status across all CLI services

### Key Deliverables
- Comprehensive company profile with business intelligence
- Multi-source validated financial metrics and ratios
- Economic context with sector-specific implications
- Peer group analysis with selection rationale
- Discovery insights identifying research priorities and data gaps
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational data required for the subsequent analyze phase, ensuring high-quality input for systematic financial analysis.

**Author**: Cole Morton
