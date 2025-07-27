# Fundamental Analyst Discover

**DASV Phase 1: Data Collection and Context Gathering**

Comprehensive financial data collection and market intelligence gathering context for institutional-quality fundamental analysis using systematic discovery protocols and production-grade CLI data acquisition methodologies.

## Purpose

The Fundamental Analysis Discovery phase represents the systematic collection and initial structuring of all data required for comprehensive fundamental analysis. This context guide provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on data acquisition standards, quality assessment criteria, and foundational research requirements using production-grade CLI financial services.

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

## Phase 0A: Existing Validation Enhancement Protocol

**0A.1 Validation File Discovery**
```
EXISTING VALIDATION IMPROVEMENT WORKFLOW:
1. Search for existing validation file: {TICKER}_{YYYYMMDD}_validation.json (today's date)
   → Check ./data/outputs/fundamental_analysis/validation/ directory
   → Pattern: {TICKER}_{YYYYMMDD}_validation.json where YYYYMMDD = today's date

2. If validation file EXISTS:
   → ROLE CHANGE: From "new discovery" to "discovery optimization specialist"
   → OBJECTIVE: Improve Discovery phase score to 9.5+ through systematic enhancement
   → METHOD: Examination → Evaluation → Optimization

3. If validation file DOES NOT EXIST:
   → Proceed with standard new discovery workflow (Data Collection Protocol onwards)
```

**0A.2 Discovery Enhancement Workflow (When Validation File Found)**
```
SYSTEMATIC DISCOVERY ENHANCEMENT PROCESS:
Step 1: Examine Existing Discovery Output
   → Read the original discovery file: {TICKER}_{YYYYMMDD}_discovery.json
   → Extract current discovery confidence scores and data quality metrics
   → Identify data collection methodology and completeness
   → Map confidence levels throughout the discovery data

Step 2: Examine Validation Assessment
   → Read the validation file: {TICKER}_{YYYYMMDD}_validation.json
   → Focus on "discovery_validation" section for specific criticisms
   → Extract market_data_accuracy, financial_statements_integrity scores
   → Note data quality gaps and source reliability issues

Step 3: Discovery Optimization Implementation
   → Address each validation point systematically
   → Enhance data sources with higher confidence alternatives
   → Strengthen data collection rigor in identified weak areas
   → Improve source reliability and freshness validation
   → Recalculate confidence scores with enhanced methodology
   → Target Discovery phase score of 9.5+ out of 10.0

Step 4: Enhanced Discovery Output
   → OVERWRITE original discovery file: {TICKER}_{YYYYMMDD}_discovery.json
   → Seamlessly integrate all improvements into original structure
   → Maintain JSON format without enhancement artifacts
   → Ensure discovery appears as institutional-quality first collection
   → Remove any references to validation process or improvement workflow
   → Deliver optimized discovery data ready for analysis phase
```

## Enhanced Data Collection via Production CLI Services

**Production CLI Financial Services Integration:**

1. **Yahoo Finance CLI** - Core market data, fundamentals, and financial statements
2. **Alpha Vantage CLI** - Real-time quotes, AI sentiment analysis, and technical indicators
3. **SEC EDGAR CLI** - Regulatory filings, SEC financial statements, and compliance data
4. **FRED Economic CLI** - Federal Reserve economic data and macroeconomic indicators
5. **IMF Data CLI** - Global economic indicators and country risk assessment
6. **CoinGecko CLI** - Cryptocurrency market data for broader sentiment analysis
7. **FMP CLI** - Advanced financials, insider trading data, and company profiles

**CLI-First Data Collection Method:**
Use the production CLI financial services for comprehensive multi-source analysis:

**Comprehensive Stock Analysis:**
- Multi-service CLI integration with price validation across Yahoo Finance, Alpha Vantage, and FMP
- Automatic cross-validation with confidence scoring and institutional-grade data quality assessment
- Integrated company intelligence, valuation metrics, and analyst sentiment analysis

**Market Context Integration:**
- FRED CLI economic indicators for specific macroeconomic data
- CoinGecko CLI cryptocurrency market data for broader sentiment analysis
- Fed funds rate, unemployment, yield curve analysis, and Bitcoin market sentiment
- Comprehensive market regime assessment integrated across services

**Service Health Validation:**
- Individual CLI service health checks for all 7 financial data services
- Service status monitoring, API key configuration verification, and data source reliability assessment

**Enhanced Discovery Benefits:**
- **Robust CLI Access**: Direct access to all 7 data sources with standardized CLI interfaces and production-grade reliability
- **Multi-Source Price Validation**: Automatic cross-validation between Yahoo Finance, Alpha Vantage, and FMP with confidence scoring
- **Economic Context Integration**: Real-time Fed policy, yield curve, and cryptocurrency sentiment analysis
- **Institutional-Grade Quality**: Advanced data validation, caching optimization, and quality scoring (targeting >90%)
- **Performance Optimization**: Production-grade caching and rate limiting reduces API calls and improves response times
- **Error Resilience**: Comprehensive error handling with graceful degradation and source reliability scoring

## Data Flow Integration

### Input Consumption Patterns
**fundamental_analysis_discover_inputs**:
```yaml
fundamental_analysis_inputs:
  required_parameters:
    - ticker: "Stock symbol (uppercase format)"
    - confidence_threshold: "9.0 | 9.5 | 9.8 (default: 9.0)"

  cli_services_consumed:
    - yahoo_finance_cli: "Core market data and financial statements"
    - alpha_vantage_cli: "Real-time quotes and sentiment analysis"
    - fmp_cli: "Advanced financials and company intelligence"
    - sec_edgar_cli: "Regulatory filings and compliance data"
    - fred_economic_cli: "Federal Reserve economic indicators"
    - coingecko_cli: "Cryptocurrency sentiment and risk appetite"
    - imf_cli: "Global economic indicators and country risk"

  validation_enhancement_inputs:
    - existing_validation_file: "./data/outputs/fundamental_analysis/validation/{TICKER}_{YYYYMMDD}_validation.json"
    - discovery_optimization_trigger: "Phase 0A enhancement protocol"

  dependency_workflows:
    - upstream_dependencies: "None (source command)"
    - data_inheritance: "No input data dependencies"
    - external_apis: "7-source CLI financial services integration"

fundamental_analysis_outputs:
  discovery_files: "./data/outputs/fundamental_analysis/discovery/{TICKER}_{YYYYMMDD}_discovery.json"
  next_phase_inputs: "fundamental_analyst_analyze consumption"
  downstream_dependencies:
    - "twitter_fundamental_analysis: analysis file consumption"
    - "sector_analyst: company analysis aggregation"
    - "social_media_strategist: investment themes extraction"

  data_flow_architecture:
    - namespace: "fundamental_analysis"
    - pattern: "source_command → discovery → analysis → synthesis → validation"
    - integration_points: "CLI services → JSON output → downstream consumption"
```

## Data Collection Protocol

### Phase 1: Comprehensive Multi-Source Data Collection via CLI Services

**MANDATORY**: Always use the production CLI financial services for comprehensive 7-source data integration. This unified approach ensures institutional-grade data quality and multi-source validation.

**CRITICAL WEB SEARCH REQUIREMENT**: When performing supplementary web searches for financial data:
- **NEVER use hardcoded years** (especially "2024") in search queries
- **ALWAYS use current year (2025)** or terms like "latest", "current", "recent", "Q1 2025", "2025 earnings"
- **Search examples**: "Apple latest earnings 2025", "AAPL current financial results", "Apple Q1 2025 performance"
- **Avoid**: "Apple 2024 earnings", "AAPL 2024 financial data", any 2024-specific searches

**Production CLI Services - 7-Source Integration**
```
PRODUCTION CLI SERVICES DATA COLLECTION:
Use the production-grade CLI financial services for unified multi-source data access:

Environment Configuration:
- All services configured with production API keys from ./config/financial_services.yaml
- API keys securely stored and never included in command outputs
- CLI services automatically access keys from secure configuration

1. Core Stock Data Collection
   → Yahoo Finance CLI: python scripts/yahoo_finance_cli.py analyze {ticker} --env prod --output-format json
   → Yahoo Finance CLI: python scripts/yahoo_finance_cli.py financials {ticker} --env prod --output-format json
   → Multi-source integration: Company overview, financial metrics, and market data
   → Automatic data validation with institutional-grade precision
   → Real-time trading data, volume analysis, and historical performance

2. Enhanced Market Intelligence
   → Alpha Vantage CLI: python scripts/alpha_vantage_cli.py quote {ticker} --env prod --output-format json
   → Real-time quote data with AI sentiment analysis and technical indicators
   → Automatic price cross-validation for confidence scoring (targeting 1.000)
   → Advanced analytics integration and market sentiment assessment

3. Advanced Company Intelligence
   → FMP CLI: python scripts/fmp_cli.py profile {ticker} --env prod --output-format json
   → FMP CLI: python scripts/fmp_cli.py financials {ticker} --statement-type cash-flow-statement --env prod --output-format json
   → FMP CLI: python scripts/fmp_cli.py insider {ticker} --env prod --output-format json (if available)
   → Advanced company profiles with detailed business descriptions
   → Complete cash flow statement integration for free cash flow calculation
   → Insider trading data and management activity analysis (German ADRs may not have data)
   → Comprehensive valuation metrics and analyst intelligence

4. Regulatory Framework Integration
   → SEC EDGAR CLI: python scripts/sec_edgar_cli.py search {ticker} --env prod --output-format json
   → Regulatory filings and SEC financial statements access
   → Compliance intelligence and regulatory risk assessment
   → 10-K/10-Q framework readiness for detailed analysis

5. Economic Context Analysis
   → FRED CLI: python scripts/fred_economic_cli.py rates --env prod --output-format json
   → FRED CLI: python scripts/fred_economic_cli.py indicator UNRATE --env prod --output-format json
   → Federal Reserve economic indicators (Fed funds, unemployment, yield curve)
   → Real-time economic policy analysis and interest rate environment
   → Economic regime assessment and sector implications

6. Cryptocurrency Market Sentiment
   → CoinGecko CLI: python scripts/coingecko_cli.py sentiment --env prod --output-format json
   → Bitcoin market sentiment for broader risk appetite assessment
   → Cryptocurrency correlation analysis for market context
   → Alternative investment sentiment and liquidity flows

7. Global Economic Intelligence
   → IMF CLI: python scripts/imf_cli.py country NGDP_RPCH USA --env prod --output-format json
   → International economic indicators and country risk assessment
   → Global GDP growth, inflation, and unemployment data
   → Macroeconomic context for multinational analysis

CLI INTEGRATION BENEFITS:
- Direct access to all 7 data sources with production-grade CLI interfaces
- Automatic multi-source price validation with institutional-grade confidence scoring
- Production caching and rate limiting improves API efficiency and reduces costs
- Comprehensive error handling with graceful degradation and source reliability scoring
- Real-time economic context integration with Fed policy and yield curve analysis
- Cryptocurrency market sentiment analysis for broader risk appetite assessment
- Production-grade reliability with built-in validation and health monitoring
- Seamless integration ensuring all data sources accessed through unified CLI framework
```

### Phase 2: Systematic Multi-Source Data Gathering via CLI Services

**Comprehensive Foundation Data Collection**
```
SYSTEMATIC 7-SOURCE DATA GATHERING VIA CLI SERVICES:

1. Multi-Source Stock Analysis
   → Primary CLI: python scripts/yahoo_finance_cli.py stock {ticker} --env prod --output-format json
   → Secondary CLI: python scripts/alpha_vantage_cli.py quote {ticker} --env prod --output-format json
   → Tertiary CLI: python scripts/fmp_cli.py profile {ticker} --env prod --output-format json
   → Automatic price cross-validation with confidence scoring
   → Real-time sentiment analysis and analyst intelligence integration
   → Insider trading data and regulatory intelligence integration
   → FORMAT: Institutional-grade precision with multi-source validation

2. Economic Context Integration
   → FRED CLI: python scripts/fred_cli.py data FEDFUNDS --env prod --output-format json
   → FRED CLI: python scripts/fred_cli.py data UNRATE --env prod --output-format json
   → CoinGecko CLI: python scripts/coingecko_cli.py sentiment --env prod --output-format json
   → Automatic economic regime assessment (restrictive/neutral/accommodative)
   → Sector-specific economic implications and policy analysis
   → FORMAT: Real-time economic intelligence with sector correlation analysis

3. Data Quality Validation
   → Health Check: python scripts/yahoo_finance_cli.py health --env prod
   → Health Check: python scripts/alpha_vantage_cli.py health --env prod
   → Health Check: python scripts/fmp_cli.py health --env prod
   → Health Check: python scripts/fred_cli.py health --env prod
   → Health Check: python scripts/coingecko_cli.py health --env prod
   → Health Check: python scripts/sec_edgar_cli.py health --env prod
   → Health Check: python scripts/imf_cli.py health --env prod
   → Real-time validation of all 7 CLI service integrations
   → Service status monitoring and API reliability assessment
   → Data completeness scoring and quality metrics
   → Multi-source consistency validation and error handling
   → FORMAT: Institutional-grade quality assurance with confidence scoring

4. Enhanced Intelligence Integration
   → Company profile intelligence via FMP CLI integration
   → SEC EDGAR regulatory framework via CLI (10-K/10-Q ready)
   → IMF global economic context via CLI (framework ready)
   → Cryptocurrency market correlation for broader sentiment analysis
   → Advanced valuation metrics with multi-source validation
   → FORMAT: Comprehensive institutional-grade data package
```

**CLI-Enhanced Company Intelligence Gathering**
```
MULTI-SOURCE REASONING CHAIN VIA CLI SERVICES:

1. Comprehensive Company Profile Analysis
   → Execute python scripts/yahoo_finance_cli.py stock {ticker} --env prod --output-format json
   → Execute python scripts/fmp_cli.py profile {ticker} --env prod --output-format json
   → Extract company intelligence from Yahoo Finance (basic profile) + FMP (detailed description)
   → Cross-validate business model and revenue streams across multiple sources
   → Integrate CEO information, employee count, and operational metrics
   → Confidence score: Multi-source validation with automatic scoring [0.0-1.0]

2. Enhanced Business Intelligence Discovery
   → Leverage FMP CLI for detailed business description and advanced company profile
   → Extract sector-specific KPIs and financial metrics via Yahoo Finance CLI integration
   → Analyze insider trading patterns and management activity via FMP CLI
   → Integrate analyst recommendations and price targets from multiple sources
   → Confidence score per metric: Cross-validated across data sources [0.0-1.0]

3. Economic Context Integration
   → Execute python scripts/fred_cli.py data FEDFUNDS --env prod for Fed funds rate
   → Execute python scripts/fred_cli.py data UNRATE --env prod for unemployment
   → Execute python scripts/coingecko_cli.py sentiment --env prod for crypto sentiment
   → Analyze interest rate sensitivity based on business model (R&D intensive, cyclical, etc.)
   → Assess cryptocurrency correlation for broader market sentiment context
   → Integrate Fed policy implications and yield curve analysis
   → Economic risk assessment with sector-specific considerations

4. Multi-Source Data Quality Validation
   → Execute health checks on all 7 CLI services to ensure operational status
   → Cross-validate key metrics (price, market cap, ratios) across Yahoo Finance, Alpha Vantage, FMP
   → Assess data completeness and source reliability scores
   → Generate institutional-grade confidence scoring for all collected intelligence
```

### Phase 3: Multi-Source Data Quality Assessment via CLI Services

**Enhanced Quality Assurance Protocol**
```
CLI-ENHANCED QUALITY ASSURANCE PROTOCOL:
□ Execute health checks on all 7 CLI services to validate operational status
□ Verify multi-source price consistency across Yahoo Finance, Alpha Vantage, and FMP (targeting 1.000 confidence)
□ Confirm real-time economic data freshness from FRED CLI (Fed funds, unemployment, yield curve)
□ Validate cryptocurrency market sentiment data currency from CoinGecko CLI
□ Cross-validate company profile data between Yahoo Finance and FMP CLI sources
□ Assess SEC EDGAR framework readiness and regulatory data availability via CLI
□ Document CLI service response times and caching efficiency
□ Generate institutional-grade confidence scores based on multi-source validation
□ Flag any CLI service degradation or API connectivity issues
□ Validate insider trading data availability and regulatory intelligence completeness
```

**CLI Multi-Source Data Quality Assessment**
```
FOR EACH DATA POINT VIA CLI SERVICES:
- Source reliability: [Multi-Source Validated/Single-Source/Estimated] via cross-validation
- Recency: [Real-time/Current/Recent/Dated] with automatic timestamp validation
- Completeness: [Complete/Partial/Missing] across all 7 integrated CLI data sources
- **Multi-Source Cross-Validation**: Automatic validation across Yahoo Finance, Alpha Vantage, FMP CLIs
- **Precision Standards**: Maintain exact figures with multi-source consistency verification
- **Institutional Validation**: Target >90% confidence through CLI service integration
- **Price Consistency**: Cross-validate pricing across 3 sources with confidence scoring
- Overall data confidence: [0.0-1.0] with multi-source weighting

CRITICAL CLI-ENHANCED FORMATTING STANDARDS:
- Market Cap: Cross-validated exact values across Yahoo Finance and FMP CLIs
- P/E Ratio: Multi-source precision verification (targeting exact 2-decimal consistency)
- Profit Margins: Decimal format validation with cross-source consistency checks
- Financial Metrics: Multi-source precision maintenance with automatic validation
- Price Validation: Automatic cross-validation targeting 1.000 confidence score

CRITICAL MULTI-SOURCE VALIDATION PROTOCOL:
- Primary Price: Yahoo Finance CLI "current_price" validated against Alpha Vantage real-time quote
- Secondary Validation: FMP CLI profile price for triple-source consistency verification
- Economic Context: FRED CLI real-time indicators with automatic freshness validation
- Crypto Sentiment: CoinGecko CLI market data for broader sentiment correlation
- Company Intelligence: FMP CLI detailed profile cross-validated with Yahoo Finance basics
- Insider Activity: FMP CLI insider trading data with regulatory intelligence integration
- Quality Scoring: Automatic confidence calculation based on multi-source consistency
```

## Output Structure and Schema

**File Naming**: `{TICKER}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/fundamental_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/fundamental_analysis_discovery_schema.json`

The discovery output must conform to the comprehensive JSON schema that defines:
- Required metadata fields for command execution tracking
- CLI service integration validation requirements
- Multi-source data validation with confidence scoring
- Financial metrics with appropriate null handling for loss-making companies
- Company intelligence including business model and financial statements
- Economic context and market analysis integration
- Peer group comparative analysis
- Data quality assessment with institutional-grade thresholds

All outputs are validated against the schema to ensure:
- Minimum 5 CLI services utilized for institutional-grade analysis
- Price consistency validation across multiple sources (targeting 1.0 confidence)
- Overall data quality ≥ 0.90 for institutional standards
- Complete discovery insights with research priorities identified

## Discovery Requirements and Standards

### Pre-Execution Requirements
1. **Phase 0A Validation Check** (if validation_enhancement enabled)
   - Check for existing validation file: {TICKER}_{YYYYMMDD}_validation.json
   - If found, apply Phase 0A Enhancement Protocol for discovery optimization
   - If not found, proceed with standard discovery workflow
2. Ticker symbol format validation (1-5 uppercase letters)
3. CLI data collection framework initialization with quality gates
4. Confidence threshold configuration (9.5+ target if validation enhancement active)
5. Production CLI service integration preparation

### Data Collection Requirements - CLI-Enhanced Standards
1. **Comprehensive Multi-Source Analysis Requirements**
   - Core market data from Yahoo Finance CLI (analyze and financials commands)
   - Real-time quotes from Alpha Vantage CLI for cross-validation
   - Advanced company intelligence from FMP CLI (profile, financials, insider)
   - Automatic cross-validation across multiple sources
   - Company profile integration with detailed business descriptions
   - Track successful CLI service responses dynamically

2. **Economic Context Integration Requirements**
   - Federal Reserve economic indicators via FRED CLI
   - Cryptocurrency sentiment analysis via CoinGecko CLI
   - Interest rate environment and yield curve analysis
   - Economic regime assessment (restrictive/neutral/accommodative)

3. **CLI Service Health Validation Standards**
   - Health checks required for all 7 CLI services
   - Minimum 5 operational services for institutional grade
   - Service reliability assessment and performance metrics
   - Automatic quality scoring based on service health

4. **Enhanced Financial Metrics Calculation Standards**
   - Calculate missing metrics when possible (EPS, ROE, revenue growth)
   - Integrate complete cash flow statements from FMP CLI
   - Handle null values appropriately (P/E for negative earnings)
   - Validate calculations against authoritative sources

5. **Multi-Source Data Quality Assessment Criteria**
   - Price consistency verification (targeting 1.000 confidence)
   - Institutional-grade confidence scoring (≥0.90 overall)
   - Economic context freshness validation
   - Data completeness assessment across all sources

### Post-Execution Quality Standards
1. **Schema Compliance Validation**
   - Output must validate against fundamental_analysis_discovery_schema.json
   - All required fields must be present with appropriate data types
   - Confidence scores must meet minimum thresholds

2. **Multi-Source Validation Requirements**
   - Price consistency across Yahoo Finance, Alpha Vantage, and FMP
   - Market cap cross-validation between sources
   - Economic indicators freshness verification
   - Company profile data consistency checks

3. **Enhanced Analysis Requirements**
   - Peer group analysis with 3-10 comparable companies
   - Discovery insights with minimum 3 initial observations
   - Data gaps identification for next phase planning
   - Source reliability scoring for all CLI services

4. **Output Standards**
   - Save to ./data/outputs/fundamental_analysis/discovery/
   - Institutional-grade confidence scores (>95% target)
   - CLI service health validation for phase readiness
   - Performance metrics logging for optimization

## Security and Implementation Notes

### API Key Security
- API keys are stored securely in `./config/financial_services.yaml`
- API keys MUST NEVER be included in discovery outputs or logs
- CLI services automatically access keys from secure configuration
- Output includes reference to config file: `"api_keys_configured": "production_keys_from_config/financial_services.yaml"`

### Dynamic Service Tracking
- `cli_services_utilized` field should only contain services that successfully provided data
- Do NOT include all 7 services statically - track actual successful responses
- Example: If SEC EDGAR fails, exclude "sec_edgar_cli" from the array
- Include services only after successful data retrieval and validation

## Quality Standards

### CLI-Enhanced Data Collection Standards
- All data accessed exclusively through production-grade CLI financial services
- Multi-source price validation targeting 1.000 confidence across 3 sources (Yahoo Finance, Alpha Vantage, FMP)
- Real-time economic data integration from FRED CLI with automatic freshness validation
- Cryptocurrency sentiment analysis from CoinGecko CLI for broader market context
- SEC EDGAR and IMF CLI framework integration ready for regulatory and global context
- **Enhanced Financial Metrics**: Automatic calculation for missing ratios (EPS from FMP CLI, ROE calculation, revenue growth)
- **Complete Cash Flow Integration**: FMP CLI cash flow statement for operating, investing, financing, and free cash flow
- **Intelligent Null Handling**: Appropriate treatment (P/E null for negative earnings, insider data unavailable for German ADRs)
- **Peer Group Analysis**: Comprehensive peer company identification and comparative metrics
- **Discovery Insights**: Research priorities and data gap identification
- **CLI Service Health**: All 7 data sources operational with >80% health score
- **Enhanced Quality Targets**: >97% overall data quality, >92% data completeness, >95% financial statement confidence

### Enhanced Output Requirements
- Complete CLI-enhanced JSON structure with all 7-source sections integrated
- Multi-source confidence scores for each major data category with cross-validation
- Comprehensive CLI service health assessment and performance metrics
- Economic context integration with sector-specific implications
- **Peer Group Data**: Industry-specific peer company analysis with selection rationale
- **Discovery Insights**: Initial observations, data gaps, and research priorities
- **Source Reliability Scoring**: Individual service reliability assessment
- **Enhanced Financial Metrics**: Calculated ratios including EPS (-0.56), ROE (-0.2058), revenue growth (0.0199), complete cash flow
- **Multi-Source Validation**: Price consistency verification across multiple CLI sources (1.000 confidence target)
- **Market Context Accuracy**: Real-time economic and cryptocurrency sentiment integration
- **Enhanced Quality Flags**: "comprehensive_financial_statement_data_including_cash_flow", "enhanced_financial_metrics_with_calculated_ratios"
- **Institutional-Grade Quality**: >97% overall confidence through production CLI services unified access

**Integration with DASV Framework**: This microservice provides the foundational data required for the subsequent analyze phase, ensuring high-quality input for systematic financial analysis.

**Author**: Cole Morton
**Confidence**: [Discovery confidence will be calculated based on data quality and completeness]
**Data Quality**: [Data quality score based on source reliability and validation completeness]
