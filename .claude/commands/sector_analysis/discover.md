# Sector Analyst Discover

**DASV Phase 1: Multi-Company Sector Data Collection and Context Gathering**

Comprehensive sector-wide financial data collection and market intelligence gathering context for institutional-quality sector analysis with investment recommendation synthesis using systematic multi-company discovery protocols and production-grade CLI data acquisition methodologies.

## Purpose

The Sector Analysis Discovery phase represents the systematic collection and initial structuring of all data required for comprehensive sector analysis with investment recommendation synthesis. This context guide provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on multi-company data acquisition standards, sector ETF analysis requirements, competitive landscape data collection criteria, investment recommendation data preparation, and foundational sector research requirements using production-grade CLI financial services.

**Expected Output Schema**: `/scripts/schemas/sector_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute sector analysis discovery. Ensure output conforms to `/scripts/schemas/sector_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: sector_analyst
**Action**: discover
**Output Location**: `./data/outputs/sector_analysis/discovery/`
**Next Phase**: sector_analyst_analyze

## Parameters

### Core Parameters
- `sector`: Sector identifier (required) - `XLK` | `XLF` | `XLE` | `technology` | `financials` | `energy` | etc.
- `companies_count`: Number of sector companies to analyze - `5` | `10` | `15` | `20` (optional, default: 10)
- `market_cap_range`: Market cap filter - `large` | `mid` | `small` | `all` (optional, default: large)
- `include_etfs`: Include sector ETFs in analysis - `true` | `false` (optional, default: true)

### Advanced Parameters
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)
- `economic_context`: Integrate sector-sensitive economic analysis - `true` | `false` (optional, default: true)

## Validation Enhancement Context

**Discovery Optimization Requirements**:
- Check for existing validation files to enable discovery enhancement protocols
- When validation files exist, apply systematic enhancement to improve discovery phase scores to 9.5+
- Target institutional-quality first collection appearance in optimized outputs
- Maintain schema compliance throughout enhancement process

## Data Sources and Integration Requirements

**Required Financial Services**:
1. **Yahoo Finance CLI** - Multi-company market data, sector ETF analysis, and financial statements across sector
2. **Alpha Vantage CLI** - Real-time quotes across sector companies, AI sentiment analysis, and technical indicators
3. **SEC EDGAR CLI** - Sector regulatory environment, compliance data, and industry-specific filings
4. **FRED Economic CLI** - Sector-sensitive economic indicators and industry cyclical data
5. **IMF Data CLI** - Global economic context affecting sector and international exposure assessment
6. **CoinGecko CLI** - Risk appetite analysis and sector correlation with cryptocurrency sentiment
7. **FMP CLI** - Advanced sector financials, competitive intelligence, and multi-company profiles

**Integration Requirements**:
- Multi-company price validation across all sector constituents with confidence scoring
- **MANDATORY: Current sector ETF price collection and validation**
- Sector ETF composition analysis and performance correlation validation
- Cross-validation with institutional-grade confidence scoring across multiple companies
- Competitive intelligence, sector valuation metrics, and industry sentiment analysis
- Sector-sensitive economic indicators for industry-specific macroeconomic context
- Cryptocurrency correlation analysis for sector risk appetite assessment
- Interest rate sensitivity analysis specific to sector characteristics
- Multi-company service health validation with graceful degradation capabilities

## Data Flow Integration

### Input Consumption Patterns
**sector_analysis_discover_inputs**:
```yaml
sector_analysis_inputs:
  required_parameters:
    - sector: "Sector identifier (XLK | XLF | XLE | technology | financials | energy)"
    - companies_count: "5 | 10 | 15 | 20 (default: 10)"
    - confidence_threshold: "9.0 | 9.5 | 9.8 (default: 9.0)"

  upstream_data_consumption:
    - fundamental_analysis_files: "./data/outputs/fundamental_analysis/{TICKER}_{DATE}.md"
    - fundamental_discovery_data: "./data/outputs/fundamental_analysis/discovery/{TICKER}_{DATE}_discovery.json"
    - fundamental_validation_scores: "./data/outputs/fundamental_analysis/validation/{TICKER}_{DATE}_validation.json"

  cli_services_consumed:
    - yahoo_finance_cli: "Multi-company market data + sector ETF analysis"
    - alpha_vantage_cli: "Real-time quotes across sector companies"
    - fmp_cli: "Sector financial intelligence + competitive metrics"
    - sec_edgar_cli: "Regulatory environment affecting sector"
    - fred_economic_cli: "Sector-sensitive economic indicators"
    - coingecko_cli: "Risk appetite + sector correlation analysis"
    - imf_cli: "Global context + sector international exposure"

  mandatory_etf_data:
    - sector_etf_prices: "MANDATORY current ETF price collection and validation"
    - cross_sector_etfs: "SPY, XLK, XLF, XLI, XLP, XLU, XLB, XLE, XLY, XLV, XLRE"
    - blocking_requirements: "Missing ETF prices prevent institutional certification"

sector_analysis_outputs:
  discovery_files: "./data/outputs/sector_analysis/discovery/{SECTOR}_{YYYYMMDD}_discovery.json"
  next_phase_inputs: "sector_analyst_analyze consumption"
  downstream_dependencies:
    - "twitter_sector_analysis: sector content generation"
    - "portfolio_allocation: sector insights for allocation decisions"
    - "social_media_strategist: sector themes integration"

  data_flow_architecture:
    - namespace: "sector_analysis"
    - pattern: "fundamental_analysis_inputs → multi_company_discovery → sector_analysis → sector_synthesis → validation"
    - integration_points: "Individual company data → sector aggregation → downstream consumption"
    - quality_inheritance: "Inherits fundamental analysis confidence scores → aggregates for sector confidence"
```

## Data Collection Requirements

### Company Selection Criteria
**Sector Company Selection Standards**:
1. **Market Cap Filtering**: Select companies based on market_cap_range parameter
2. **Sector Purity**: Prioritize companies with >70% revenue from target sector
3. **Liquidity Requirements**: Ensure adequate trading volume and market presence
4. **Geographic Distribution**: Include representative geographic/regional exposure
5. **Size Distribution**: Balance large, mid, and small-cap representation based on parameters

### Data Collection Standards
**Core Requirements**:
- Production CLI financial services for comprehensive 7-source sector data integration
- Institutional-grade data quality and multi-company validation across the entire sector
- Current date-relative data collection (never use hardcoded years in searches)
- Always use terms like "latest", "current", "recent", "current quarter", "year-to-date"

### Core Data Categories

**Multi-Company Analysis Requirements**:
- Company-level data collection across selected sector constituents
- Financial statements and cash flow analysis for all companies
- Multi-company integration with comparative financial metrics
- Cross-company validation with institutional-grade precision
- Real-time trading data, volume analysis, and sector performance correlation

**Sector ETF Analysis Requirements**:
- **MANDATORY: Current sector ETF price collection and validation**
- Sector ETF composition analysis and performance correlation validation
- Cross-sector ETF analysis (SPY, XLK, XLF, XLI, XLP, XLU, XLB, XLE, XLY, XLV, XLRE)
- Historical cross-sector data for correlation analysis and seasonality patterns

**Market Intelligence Requirements**:
- Real-time quotes across all sector companies with sentiment analysis
- VIX volatility analysis for sector risk assessment
- DXY dollar strength analysis for sector currency sensitivity
- Bitcoin correlation analysis for risk appetite assessment
- Advanced sector analytics and competitive sentiment assessment

**Economic Context Requirements**:
- Federal Reserve economic indicators with sector-specific sensitivity analysis
- Interest rate environment and yield curve analysis
- GDP and employment indicators with sector correlation analysis
- Cryptocurrency market sentiment correlation for sector risk appetite
- Global economic context and sector international exposure assessment

**Regulatory Intelligence Requirements**:
- Industry-specific regulatory filings and compliance data
- Sector regulatory intelligence and policy risk assessment
- Industry-wide regulatory framework analysis

### Advanced Analysis Requirements

**Multi-Company Intelligence Requirements**:
- Comprehensive sector company profiles across selected market cap ranges
- Cross-company financial performance validation and competitive positioning analysis
- Sector-wide business model analysis and revenue stream identification
- Management quality assessment and insider activity patterns across sector companies

**Market Context Requirements**:
- Real-time sector performance correlation with broader market indices
- Volatility analysis and risk assessment specific to sector characteristics
- Dollar strength sensitivity analysis for multinational sector exposure
- Interest rate environment implications and sector-specific economic sensitivity

**Economic Intelligence Requirements**:
- Federal Reserve policy implications and sector cyclical positioning
- GDP growth correlation analysis and employment sensitivity assessment
- Global economic indicators affecting sector international operations
- Liquidity conditions and credit market implications for sector funding

## Output Structure and Schema

**File Naming**: `{SECTOR}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/sector_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/sector_analysis_discovery_schema.json`

### Required Output Components
- **Multi-Company Data**: Individual company analysis across sector with aggregated metrics
- **Sector ETF Analysis**: Current ETF prices, composition, and performance correlation
- **Cross-Sector Analysis**: Comparison with all 11 sector ETFs and relative positioning
- **Economic Context**: Interest rates, GDP, employment data with sector sensitivity analysis
- **Volatility Analysis**: VIX correlation and risk-on/off behavior assessment
- **Market Intelligence**: Dollar strength, cryptocurrency correlation, and liquidity conditions
- **Regulatory Environment**: Industry-specific compliance and regulatory risk factors
- **Quality Metrics**: Confidence scores, data completeness, and source reliability assessment

### Schema Compliance Standards
- Minimum 3 CLI services utilized for institutional-grade analysis
- Mandatory current sector ETF price collection with <2% variance validation
- Multi-company price validation across sector constituents (targeting >90% confidence)
- Overall data quality ≥ 0.85 for institutional standards
- Complete sector discovery insights with investment recommendation readiness

## Quality Standards and Requirements

### Pre-Execution Requirements
- Sector identifier validation and company selection criteria application
- CLI services configuration and API key validation
- Confidence threshold configuration based on depth parameter
- Optional validation enhancement protocol activation for existing validation files

### Data Quality Standards
**Multi-Company Validation**:
- Price consistency verification across all sector companies
- Financial metrics cross-validation between companies
- Sector ETF composition and performance validation
- Economic indicators freshness and relevance assessment

**Institutional-Grade Thresholds**:
- Overall data quality ≥ 0.85 for sector-wide analysis
- Service reliability ≥ 80% health score across CLI services
- Mandatory ETF price collection with <2% variance requirement
- Multi-company confidence scoring targeting >90% sector coverage

### Enhanced Analysis Requirements
- Cross-sector analysis with all 11 sector ETFs for relative positioning
- Seasonality analysis with minimum 10-year historical data
- Economic sensitivity assessment with GDP and employment correlation
- Competitive landscape analysis with sector concentration metrics

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
- **ETF Price Collection**: 100% success rate with <2% variance validation
- **Multi-Company Coverage**: ≥ 90% confidence across sector constituents
- **Economic Integration**: ≥ 95% confidence in macroeconomic context analysis

### Key Deliverables
- Comprehensive sector company analysis with multi-source validation
- Mandatory sector ETF analysis with current pricing and composition data
- Cross-sector analysis with all 11 sector ETFs for relative positioning
- Economic context with sector-specific sensitivity analysis
- Volatility and market intelligence assessment including VIX and dollar strength
- Seasonality analysis with 10-year historical patterns
- Discovery insights identifying sector themes and research priorities
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational sector data required for the subsequent analyze phase, ensuring high-quality input for systematic sector analysis and investment recommendation synthesis.

**Author**: Cole Morton
