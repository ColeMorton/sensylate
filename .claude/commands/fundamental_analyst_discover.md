# Fundamental Analyst Discover

**DASV Phase 1: Data Collection and Context Gathering**

Execute comprehensive financial data collection and market intelligence gathering for institutional-quality fundamental analysis using systematic discovery protocols and production-grade CLI data acquisition methodologies.

## Purpose

You are the Fundamental Analysis Discovery Specialist, responsible for the systematic collection and initial structuring of all data required for comprehensive fundamental analysis. This microservice implements the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on data acquisition, quality assessment, and foundational research using production-grade CLI financial services.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: fundamental_analyst
**Action**: discover
**Output Location**: `./data/outputs/fundamental_analysis/discovery/`
**Next Phase**: fundamental_analyst_analyze

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
   → Yahoo Finance CLI: python yahoo_finance_cli.py analyze {ticker} --env prod --output-format json
   → Yahoo Finance CLI: python yahoo_finance_cli.py financials {ticker} --env prod --output-format json
   → Multi-source integration: Company overview, financial metrics, and market data
   → Automatic data validation with institutional-grade precision
   → Real-time trading data, volume analysis, and historical performance

2. Enhanced Market Intelligence
   → Alpha Vantage CLI: python alpha_vantage_cli.py quote {ticker} --env prod --output-format json
   → Real-time quote data with AI sentiment analysis and technical indicators
   → Automatic price cross-validation for confidence scoring (targeting 1.000)
   → Advanced analytics integration and market sentiment assessment

3. Advanced Company Intelligence
   → FMP CLI: python fmp_cli.py profile {ticker} --env prod --output-format json
   → FMP CLI: python fmp_cli.py financials {ticker} --statement-type cash-flow-statement --env prod --output-format json
   → FMP CLI: python fmp_cli.py insider {ticker} --env prod --output-format json (if available)
   → Advanced company profiles with detailed business descriptions
   → Complete cash flow statement integration for free cash flow calculation
   → Insider trading data and management activity analysis (German ADRs may not have data)
   → Comprehensive valuation metrics and analyst intelligence

4. Regulatory Framework Integration
   → SEC EDGAR CLI: python sec_edgar_cli.py search {ticker} --env prod --output-format json
   → Regulatory filings and SEC financial statements access
   → Compliance intelligence and regulatory risk assessment
   → 10-K/10-Q framework readiness for detailed analysis

5. Economic Context Analysis
   → FRED CLI: python fred_economic_cli.py rates --env prod --output-format json
   → FRED CLI: python fred_economic_cli.py indicator UNRATE --env prod --output-format json
   → Federal Reserve economic indicators (Fed funds, unemployment, yield curve)
   → Real-time economic policy analysis and interest rate environment
   → Economic regime assessment and sector implications

6. Cryptocurrency Market Sentiment
   → CoinGecko CLI: python coingecko_cli.py sentiment --env prod --output-format json
   → Bitcoin market sentiment for broader risk appetite assessment
   → Cryptocurrency correlation analysis for market context
   → Alternative investment sentiment and liquidity flows

7. Global Economic Intelligence
   → IMF CLI: python imf_cli.py country NGDP_RPCH USA --env prod --output-format json
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
   → Primary CLI: python yahoo_finance_cli.py stock {ticker} --env prod --output-format json
   → Secondary CLI: python alpha_vantage_cli.py quote {ticker} --env prod --output-format json
   → Tertiary CLI: python fmp_cli.py profile {ticker} --env prod --output-format json
   → Automatic price cross-validation with confidence scoring
   → Real-time sentiment analysis and analyst intelligence integration
   → Insider trading data and regulatory intelligence integration
   → FORMAT: Institutional-grade precision with multi-source validation

2. Economic Context Integration
   → FRED CLI: python fred_cli.py data FEDFUNDS --env prod --output-format json
   → FRED CLI: python fred_cli.py data UNRATE --env prod --output-format json
   → CoinGecko CLI: python coingecko_cli.py sentiment --env prod --output-format json
   → Automatic economic regime assessment (restrictive/neutral/accommodative)
   → Sector-specific economic implications and policy analysis
   → FORMAT: Real-time economic intelligence with sector correlation analysis

3. Data Quality Validation
   → Health Check: python yahoo_finance_cli.py health --env prod
   → Health Check: python alpha_vantage_cli.py health --env prod
   → Health Check: python fmp_cli.py health --env prod
   → Health Check: python fred_cli.py health --env prod
   → Health Check: python coingecko_cli.py health --env prod
   → Health Check: python sec_edgar_cli.py health --env prod
   → Health Check: python imf_cli.py health --env prod
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
   → Execute python yahoo_finance_cli.py stock {ticker} --env prod --output-format json
   → Execute python fmp_cli.py profile {ticker} --env prod --output-format json
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
   → Execute python fred_cli.py data FEDFUNDS --env prod for Fed funds rate
   → Execute python fred_cli.py data UNRATE --env prod for unemployment
   → Execute python coingecko_cli.py sentiment --env prod for crypto sentiment
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

## Enhanced Output Structure via CLI Services

**File Naming**: `{TICKER}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/fundamental_analysis/discovery/`

```json
{
  "metadata": {
    "command_name": "cli_enhanced_fundamental_analyst_discover",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "cli_enhanced_discover_7_source",
    "ticker": "TICKER_SYMBOL",
    "data_collection_methodology": "production_cli_services_unified_access",
    "cli_services_utilized": "dynamic_array_of_successfully_utilized_services",
    "api_keys_configured": "production_keys_from_config/financial_services.yaml"
  },
  "cli_comprehensive_analysis": {
    "metadata": "complete_cli_response_aggregation_from_multi_source_collection",
    "company_overview": "integrated_company_intelligence_multi_source",
    "market_data": "cross_validated_pricing_and_trading_data",
    "analyst_intelligence": "sentiment_and_recommendations_integrated",
    "data_validation": "multi_source_price_validation_with_confidence",
    "quality_metrics": "institutional_grade_assessment"
  },
  "market_data": {
    "current_price": "cross_validated_price_from_3_sources",
    "market_cap": "multi_source_validated_market_cap",
    "price_validation": {
      "yahoo_finance_price": "decimal_value",
      "alpha_vantage_price": "decimal_value",
      "fmp_price": "decimal_value",
      "price_consistency": "boolean",
      "confidence_score": "0.0-1.0_targeting_1.000"
    },
    "volume": "current_trading_volume",
    "beta": "decimal_value_2_places",
    "52_week_high": "exact_decimal_value",
    "52_week_low": "exact_decimal_value",
    "confidence": "multi_source_confidence_0.0-1.0"
  },
  "financial_metrics": {
    "revenue_ttm": "exact_integer_value",
    "net_income": "exact_integer_value",
    "earnings_per_share": "decimal_value_2_places",
    "pe_ratio": "decimal_value_2_places_exact",
    "profit_margin": "decimal_format_for_validation_0_to_1",
    "return_on_equity": "decimal_format_for_validation_0_to_1",
    "free_cash_flow": "exact_integer_value",
    "revenue_growth": "decimal_format_for_validation",
    "confidence": "0.0-1.0"
  },
  "company_intelligence": {
    "business_model": {
      "revenue_streams": "array",
      "business_segments": "object",
      "operational_model": "string",
      "confidence": "0.0-1.0"
    },
    "financial_statements": {
      "income_statement": "object",
      "balance_sheet": "object",
      "cash_flow": "object",
      "total_liquid_assets": "cash_and_equivalents + short_term_investments",
      "cash_position_breakdown": {
        "cash_and_equivalents": "from_yahoo_finance_cli",
        "short_term_investments": "from_yahoo_finance_cli",
        "total_liquid_assets": "sum_of_above"
      },
      "investment_portfolio_breakdown": {
        "investments_and_advances": "total_investment_portfolio_from_yahoo_finance_cli",
        "cash_and_short_term_investments": "liquid_assets_subset",
        "definition_note": "investments_and_advances_is_total_portfolio_including_illiquid_assets"
      },
      "confidence": "0.0-1.0"
    },
    "key_metrics": {
      "business_specific_kpis": "array",
      "financial_ratios": "object",
      "valuation_multiples": "object",
      "confidence": "0.0-1.0"
    }
  },
  "cli_market_context": {
    "metadata": "complete_cli_response_aggregation_from_fred_and_coingecko",
    "economic_indicators": "fred_cli_economic_data_real_time",
    "cryptocurrency_market": "coingecko_cli_sentiment_analysis",
    "market_summary": "economic_regime_assessment",
    "sector_implications": "business_model_specific_analysis"
  },
  "economic_analysis": {
    "interest_rate_environment": "restrictive_neutral_accommodative",
    "yield_curve_signal": "inverted_flat_normal",
    "policy_implications": "array_of_fed_policy_impacts",
    "sector_sensitivity": "industry_specific_rate_sensitivity"
  },
  "regulatory_intelligence": {
    "insider_trading_data": "fmp_cli_insider_activity_analysis",
    "sec_edgar_integration": "cli_framework_status_and_capabilities",
    "regulatory_analysis": "compliance_and_risk_assessment"
  },
  "cli_service_validation": {
    "service_health": "complete_health_check_response_all_7_services",
    "health_score": "0.0-1.0_operational_assessment",
    "services_operational": "count_of_working_cli_services",
    "services_healthy": "boolean_overall_status"
  },
  "cli_data_quality": {
    "overall_data_quality": "0.0-1.0_multi_source_weighted",
    "cli_service_health": "0.0-1.0_service_reliability",
    "institutional_grade": "boolean_targeting_true",
    "data_sources_via_cli": "array_of_7_sources",
    "cli_integration_status": "operational_or_degraded"
  },
  "cli_insights": {
    "cli_integration_observations": "array_unified_cli_benefits",
    "data_quality_insights": "array_multi_source_validation_results",
    "market_context_insights": "array_economic_and_crypto_analysis",
    "service_performance_insights": "array_cli_efficiency_observations"
  },
  "peer_group_data": {
    "peer_companies": "array_of_peer_company_objects_with_metrics",
    "peer_selection_rationale": "explanation_of_peer_selection_methodology",
    "comparative_metrics": "object_comparing_target_vs_peers",
    "confidence": "0.0-1.0_peer_analysis_confidence"
  },
  "discovery_insights": {
    "initial_observations": "array_key_business_and_financial_insights",
    "data_gaps_identified": "array_missing_data_points_for_analysis",
    "research_priorities": "array_next_phase_focus_areas",
    "next_phase_readiness": "boolean_analysis_phase_readiness"
  },
  "data_quality_assessment": {
    "source_reliability_scores": "object_cli_service_reliability_scoring",
    "data_completeness": "0.0-1.0_overall_completeness_score",
    "data_freshness": "object_data_recency_assessment",
    "quality_flags": "array_data_quality_observations"
  }
}
```

## Discovery Execution Protocol

### Pre-Execution
1. **Phase 0A Validation Check** (if validation_enhancement enabled)
   - Check for existing validation file: {TICKER}_{YYYYMMDD}_validation.json
   - If found, execute Phase 0A Enhancement Protocol for discovery optimization
   - If not found, proceed with standard discovery workflow
2. Validate ticker symbol format and existence
3. Initialize CLI data collection frameworks and quality gates
4. Set confidence thresholds for data acceptance (9.5+ target if validation enhancement active)
5. Prepare production CLI service integrations

### Main Execution - CLI-Enhanced Protocol
1. **Comprehensive Multi-Source Analysis**
   - Execute `python yahoo_finance_cli.py analyze {ticker} --env prod --output-format json` for core market data
   - Execute `python yahoo_finance_cli.py financials {ticker} --env prod --output-format json` for financial statements
   - Execute `python alpha_vantage_cli.py quote {ticker} --env prod --output-format json` for real-time data
   - Execute `python fmp_cli.py profile {ticker} --env prod --output-format json` for advanced intelligence
   - Execute `python fmp_cli.py financials {ticker} --statement-type cash-flow-statement --env prod --output-format json` for cash flow
   - Attempt `python fmp_cli.py insider {ticker} --env prod --output-format json` for insider trading (handle gracefully if unavailable)
   - Automatic cross-validation across Yahoo Finance, Alpha Vantage, and FMP CLIs
   - Real-time sentiment analysis and complete financial statement integration
   - Company profile integration with detailed business descriptions
   - Track successful CLI service responses in cli_services_utilized (only include services that provided data)

2. **Economic Context Integration**
   - Execute `python fred_economic_cli.py rates --env prod --output-format json` for comprehensive interest rates
   - Execute `python fred_economic_cli.py indicator UNRATE --env prod --output-format json` for unemployment
   - Execute `python coingecko_cli.py sentiment --env prod --output-format json` for crypto sentiment
   - Gather Fed funds rate, unemployment, yield curve data from unified FRED CLI
   - Economic context is integrated across multiple CLI sources with real-time indicators

3. **CLI Service Health Validation**
   - Execute health checks on all 7 CLI services to ensure operational status
   - Real-time validation of service availability and API configurations
   - Data source reliability assessment and performance metrics
   - Automatic quality scoring based on service health and data completeness

4. **Enhanced Financial Metrics Calculation**
   - **Calculate missing EPS**: Use FMP CLI actual data or derive from market cap and price
   - **Calculate missing ROE**: Net Income ÷ Stockholders Equity for comprehensive ratio analysis
   - **Calculate revenue growth**: YoY percentage change using multi-year income statement data
   - **Integrate complete cash flow**: Operating, investing, financing, and free cash flow from FMP CLI
   - **Handle unavailable data appropriately**: Mark insider trading as unavailable for German ADRs
   - **Validate calculations**: Cross-reference calculated values with authoritative sources

5. **Multi-Source Data Quality Assessment**
   - Automatic cross-validation of key metrics across multiple CLI sources
   - Price consistency verification targeting 1.000 confidence score
   - Institutional-grade confidence scoring based on multi-source validation
   - Economic context freshness validation and cryptocurrency sentiment analysis

### Post-Execution - CLI-Enhanced Protocol
1. Generate enhanced CLI discovery output in JSON format with comprehensive multi-source sections
2. **Apply Multi-Source Validation Optimization**:
   - Verify price consistency across Yahoo Finance, Alpha Vantage, and FMP CLIs (targeting 1.000 confidence)
   - Validate market_cap cross-validation between Yahoo Finance and FMP CLI sources
   - Ensure economic indicators freshness from FRED CLI with automatic timestamp validation
   - Verify cryptocurrency sentiment data currency from CoinGecko CLI integration
   - Cross-validate company profile data between Yahoo Finance basics and FMP detailed descriptions
3. **Apply Enhanced Financial Metrics Protocol**:
   - **Calculate Missing EPS**: Use FMP CLI actual EPS data if available, or calculate using Net Income ÷ Shares Outstanding
   - **Calculate Missing ROE**: Net Income ÷ Stockholders Equity for return on equity calculation
   - **Calculate Revenue Growth**: (Current Year Revenue - Previous Year Revenue) ÷ Previous Year Revenue
   - **Integrate Cash Flow Data**: Use FMP CLI cash flow statement for operating, investing, financing, and free cash flow
   - **Handle Null Values Appropriately**: P/E ratio remains null for negative earnings, insider trading marked as unavailable for German ADRs
   - **Fallback Logic**: Use historical data (2024 → 2023 → 2022 → 2021) for missing current-year values only when calculation not possible
   - Update confidence scores to reflect enhanced metric completeness (target 95%+ for financial statements)
4. **Generate Comprehensive Analysis Sections**:
   - Add peer group analysis with industry-specific competitor identification
   - Generate discovery insights with initial observations and research priorities
   - Implement source reliability scoring for all CLI services
   - Create data quality assessment with completeness and freshness metrics
5. **Save enhanced output to ./data/outputs/fundamental_analysis/discovery/**
6. Calculate institutional-grade confidence scores across all 7 CLI data sources (targeting >95%)
7. Validate CLI service health scores and integration status for next phase readiness
8. Log CLI service performance metrics and caching efficiency statistics
9. Signal readiness for fundamental_analyst_analyze phase with enhanced data package

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
