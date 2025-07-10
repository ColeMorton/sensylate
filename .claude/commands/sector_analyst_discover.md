# Sector Analyst Discover

**DASV Phase 1: Multi-Company Sector Data Collection and Context Gathering**

Execute comprehensive sector-wide financial data collection and market intelligence gathering for institutional-quality sector analysis with investment recommendation synthesis using systematic multi-company discovery protocols and production-grade CLI data acquisition methodologies.

## Purpose

You are the Sector Analysis Discovery Specialist, responsible for the systematic collection and initial structuring of all data required for comprehensive sector analysis with investment recommendation synthesis. This microservice implements the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on multi-company data acquisition, sector ETF analysis, competitive landscape data collection, investment recommendation data preparation, and foundational sector research using production-grade CLI financial services.

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

## Phase 0A: Existing Sector Validation Enhancement Protocol

**0A.1 Sector Validation File Discovery**
```
EXISTING SECTOR VALIDATION IMPROVEMENT WORKFLOW:
1. Search for existing validation file: {SECTOR}_{YYYYMMDD}_validation.json (today's date)
   → Check ./data/outputs/sector_analysis/validation/ directory
   → Pattern: {SECTOR}_{YYYYMMDD}_validation.json where YYYYMMDD = today's date

2. If validation file EXISTS:
   → ROLE CHANGE: From "new sector discovery" to "sector discovery optimization specialist"
   → OBJECTIVE: Improve Sector Discovery phase score to 9.5+ through systematic enhancement
   → METHOD: Examination → Evaluation → Optimization across all sector companies

3. If validation file DOES NOT EXIST:
   → Proceed with standard new sector discovery workflow (Multi-Company Data Collection Protocol onwards)
```

**0A.2 Sector Discovery Enhancement Workflow (When Validation File Found)**
```
SYSTEMATIC SECTOR DISCOVERY ENHANCEMENT PROCESS:
Step 1: Examine Existing Sector Discovery Output
   → Read the original discovery file: {SECTOR}_{YYYYMMDD}_discovery.json
   → Extract current multi-company confidence scores and sector data quality metrics
   → Identify sector data collection methodology and completeness across companies
   → Map confidence levels throughout the sector discovery data and ETF analysis

Step 2: Examine Sector Validation Assessment
   → Read the validation file: {SECTOR}_{YYYYMMDD}_validation.json
   → Focus on "sector_discovery_validation" section for specific criticisms
   → Extract multi_company_accuracy, sector_etf_integrity, competitive_landscape_quality scores
   → Note sector data gaps and multi-source reliability issues across companies

Step 3: Sector Discovery Optimization Implementation
   → Address each validation point systematically across all sector companies
   → Enhance data sources with higher confidence alternatives for each company
   → Strengthen sector ETF analysis and composition verification
   → Improve competitive landscape data collection and industry metrics
   → Recalculate confidence scores with enhanced sector methodology
   → Target Sector Discovery phase score of 9.5+ out of 10.0

Step 4: Enhanced Sector Discovery Output
   → OVERWRITE original discovery file: {SECTOR}_{YYYYMMDD}_discovery.json
   → Seamlessly integrate all improvements into original sector structure
   → Maintain JSON format without enhancement artifacts
   → Ensure sector discovery appears as institutional-quality first collection
   → Remove any references to validation process or improvement workflow
   → Deliver optimized sector data ready for sector analysis phase
```

## Enhanced Multi-Company Sector Data Collection via Production CLI Services

**Production CLI Financial Services Integration for Sector Analysis:**

1. **Yahoo Finance CLI** - Multi-company market data, sector ETF analysis, and financial statements across sector
2. **Alpha Vantage CLI** - Real-time quotes across sector companies, AI sentiment analysis, and technical indicators
3. **SEC EDGAR CLI** - Sector regulatory environment, compliance data, and industry-specific filings
4. **FRED Economic CLI** - Sector-sensitive economic indicators and industry cyclical data
5. **IMF Data CLI** - Global economic context affecting sector and international exposure assessment
6. **CoinGecko CLI** - Risk appetite analysis and sector correlation with cryptocurrency sentiment
7. **FMP CLI** - Advanced sector financials, competitive intelligence, and multi-company profiles

**CLI-First Sector Data Collection Method:**
Use the production CLI financial services for comprehensive multi-company sector analysis:

**Comprehensive Sector Analysis:**
- Multi-company CLI integration with price validation across all sector constituents
- Sector ETF composition analysis and performance correlation validation
- Automatic cross-validation with confidence scoring across multiple companies
- Integrated competitive intelligence, sector valuation metrics, and industry sentiment analysis

**Sector Market Context Integration:**
- FRED CLI sector-sensitive economic indicators for industry-specific macroeconomic data
- CoinGecko CLI cryptocurrency correlation analysis for sector risk appetite assessment
- Interest rate sensitivity analysis specific to sector characteristics
- Comprehensive sector regime assessment integrated across economic services

**Multi-Company Service Health Validation:**
- Individual CLI service health checks optimized for multi-company sector analysis
- Service status monitoring across all sector companies with rate limiting optimization
- Data source reliability assessment for sector-wide consistency

**Enhanced Sector Discovery Benefits:**
- **Robust Multi-Company CLI Access**: Direct access to all 7 data sources across multiple sector companies
- **Sector-Wide Price Validation**: Automatic cross-validation across all sector companies with aggregated confidence scoring
- **Sector Economic Context**: Real-time Fed policy impact on specific sectors and industry cyclical analysis
- **Institutional-Grade Sector Quality**: Advanced sector validation, caching optimization, and sector-wide quality scoring (targeting >90%)
- **Multi-Company Performance Optimization**: Production-grade caching and rate limiting optimized for sector analysis
- **Sector Error Resilience**: Comprehensive error handling with graceful degradation for individual companies within sector

## Multi-Company Sector Data Collection Protocol

### Phase 1: Comprehensive Multi-Company Sector Data Collection via CLI Services

**MANDATORY**: Always use the production CLI financial services for comprehensive 7-source sector data integration. This unified approach ensures institutional-grade data quality and multi-company validation across the entire sector.

**SECTOR COMPANY SELECTION ALGORITHM**:
1. **Market Cap Filtering**: Select companies based on market_cap_range parameter
2. **Sector Purity**: Prioritize companies with >70% revenue from target sector
3. **Liquidity Requirements**: Ensure adequate trading volume and market presence
4. **Geographic Distribution**: Include representative geographic/regional exposure
5. **Size Distribution**: Balance large, mid, and small-cap representation based on parameters

**CRITICAL WEB SEARCH REQUIREMENT**: When performing supplementary web searches for sector financial data:
- **NEVER use hardcoded years** in search queries
- **ALWAYS use current date-relative terms**: "latest", "current", "recent", "current quarter", "year-to-date"
- **Search examples**: "Technology sector latest earnings", "XLK sector current performance", "Technology sector recent results"
- **Dynamic date usage**: Use current date context for quarterly references (e.g., if current date is 2025, use "Q2 2025" for current quarter)
- **Avoid**: Any hardcoded year references in search queries

**Production CLI Services - 7-Source Sector Integration**
```
PRODUCTION CLI SERVICES SECTOR DATA COLLECTION:
Use the production-grade CLI financial services for unified multi-company sector data access:

Environment Configuration:
- All services configured with production API keys from ./config/financial_services.yaml
- API keys securely stored and never included in command outputs
- CLI services automatically access keys from secure configuration
- Optimized rate limiting for multi-company sector analysis

1. Multi-Company Core Data Collection
   → FOR EACH company in selected_sector_companies:
      → Yahoo Finance CLI: python yahoo_finance_cli.py analyze {company_ticker} --env prod --output-format json
      → Yahoo Finance CLI: python yahoo_finance_cli.py financials {company_ticker} --env prod --output-format json
   → Sector ETF Analysis: python yahoo_finance_cli.py analyze {sector_etf} --env prod --output-format json
   → Cross-Sector ETF Analysis: python yahoo_finance_cli.py analyze SPY XLK XLF XLI XLP XLU XLB XLE XLY XLV XLRE --env prod --output-format json
   → Historical Cross-Sector Data: python yahoo_finance_cli.py history SPY XLK XLF XLI XLP XLU XLB XLE XLY XLV XLRE --period 1y --env prod --output-format json
   → Multi-company integration: Sector overview, comparative financial metrics, and market data
   → Automatic cross-company validation with institutional-grade precision
   → Real-time trading data, volume analysis, and sector performance correlation

2. Enhanced Sector Market Intelligence
   → FOR EACH company in selected_sector_companies:
      → Alpha Vantage CLI: python alpha_vantage_cli.py quote {company_ticker} --env prod --output-format json
   → Sector ETF real-time data: python alpha_vantage_cli.py quote {sector_etf} --env prod --output-format json
   → VIX Volatility Analysis: python yahoo_finance_cli.py quote VIXY --env prod --output-format json
   → VIX Historical Data: python yahoo_finance_cli.py history VIXY --period 2y --env prod --output-format json
   → DXY Dollar Index: python yahoo_finance_cli.py quote UUP --env prod --output-format json
   → DXY Historical Data: python yahoo_finance_cli.py history UUP --period 1y --env prod --output-format json
   → Bitcoin Correlation: python alpha_vantage_cli.py quote BTCUSD --env prod --output-format json
   → Real-time quote aggregation with sector sentiment analysis and technical indicators
   → Automatic price cross-validation across all sector companies (targeting 1.000 per company)
   → Advanced sector analytics integration and competitive sentiment assessment

3. Advanced Sector Intelligence
   → FOR EACH company in selected_sector_companies:
      → FMP CLI: python fmp_cli.py profile {company_ticker} --env prod --output-format json
      → FMP CLI: python fmp_cli.py financials {company_ticker} --statement-type cash-flow-statement --env prod --output-format json
      → FMP CLI: python fmp_cli.py insider {company_ticker} --env prod --output-format json (if available)
   → Sector ETF composition: python fmp_cli.py etf {sector_etf} --env prod --output-format json
   → Advanced sector competitive profiles with detailed business descriptions
   → Complete cash flow statement integration across all sector companies
   → Sector-wide insider trading activity and management intelligence
   → Comprehensive sector valuation metrics and competitive positioning

4. Sector Regulatory Framework Integration
   → SEC EDGAR CLI: python sec_edgar_cli.py sector {sector} --env prod --output-format json
   → Industry-specific regulatory filings and compliance data access
   → Sector regulatory intelligence and policy risk assessment
   → Industry-wide regulatory framework readiness for detailed analysis

5. Sector Economic Context Analysis
   → FRED CLI: python fred_economic_cli.py rates --env prod --output-format json
   → FRED CLI: python fred_economic_cli.py indicator UNRATE --env prod --output-format json
   → FRED CLI: python fred_economic_cli.py indicator DGS10 --env prod --output-format json (10-Year Treasury)
   → FRED CLI: python fred_economic_cli.py indicator DGS2 --env prod --output-format json (2-Year Treasury)
   → FRED CLI: python fred_economic_cli.py indicator DEXUSEU --env prod --output-format json (USD/EUR for DXY proxy)
   → FRED CLI: python fred_economic_cli.py indicator BAMLH0A0HYM2 --env prod --output-format json (High Yield Credit Spreads)
   → FRED CLI: python fred_economic_cli.py indicator M2SL --env prod --output-format json (M2 Money Supply)
   → FRED CLI: python fred_economic_cli.py indicator NFCI --env prod --output-format json (Financial Conditions Index)
   → FRED CLI: python fred_economic_cli.py indicator GDP --env prod --output-format json (Gross Domestic Product)
   → FRED CLI: python fred_economic_cli.py indicator GDPC1 --env prod --output-format json (Real GDP)
   → FRED CLI: python fred_economic_cli.py indicator A191RL1Q225SBEA --env prod --output-format json (GDP Growth Rate)
   → FRED CLI: python fred_economic_cli.py indicator PAYEMS --env prod --output-format json (Nonfarm Payrolls)
   → FRED CLI: python fred_economic_cli.py indicator CIVPART --env prod --output-format json (Labor Force Participation)
   → FRED CLI: python fred_economic_cli.py indicator ICSA --env prod --output-format json (Initial Claims)
   → FRED CLI: python fred_economic_cli.py sector_indicator {sector_specific_indicator} --env prod --output-format json
   → Federal Reserve economic indicators with sector-specific sensitivity analysis
   → Real-time economic policy analysis and sector interest rate impact
   → Economic regime assessment with sector-specific implications and cyclical patterns

6. Sector Cryptocurrency Correlation Analysis
   → CoinGecko CLI: python coingecko_cli.py sentiment --env prod --output-format json
   → Bitcoin market sentiment for sector risk appetite correlation assessment
   → Alpha Vantage CLI: python alpha_vantage_cli.py quote BTCUSD --env prod --output-format json
   → Alpha Vantage CLI: python alpha_vantage_cli.py daily BTCUSD --outputsize compact --env prod --output-format json
   → Cryptocurrency correlation analysis for sector market context
   → Alternative investment sentiment and sector liquidity flow analysis
   → Risk-on/risk-off behavior assessment using Bitcoin as proxy

7. Global Sector Economic Intelligence
   → IMF CLI: python imf_cli.py country NGDP_RPCH USA --env prod --output-format json
   → IMF CLI: python imf_cli.py sector_exposure {sector} --env prod --output-format json (if available)
   → International economic indicators and sector country risk assessment
   → Global GDP growth impact on sector and inflation sensitivity
   → Macroeconomic context for sector international exposure and trade implications

SECTOR CLI INTEGRATION BENEFITS:
- Direct access to all 7 data sources across multiple sector companies with production-grade CLI interfaces
- Automatic multi-company price validation with institutional-grade confidence scoring across sector
- Sector ETF composition and performance correlation analysis with real-time validation
- Production caching and rate limiting optimized for multi-company sector analysis efficiency
- Comprehensive error handling with graceful degradation and sector-wide reliability scoring
- Real-time economic context integration with sector-specific Fed policy and yield curve analysis
- Cryptocurrency market sentiment correlation analysis for sector risk appetite assessment
- Production-grade reliability with built-in validation and sector health monitoring
- Seamless sector integration ensuring all data sources accessed through unified CLI framework
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

## Enhanced Sector Output Structure via CLI Services

**File Naming**: `{SECTOR}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/sector_analysis/discovery/`

```json
{
  "metadata": {
    "command_name": "cli_enhanced_sector_analyst_discover",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "cli_enhanced_sector_discover_7_source",
    "sector": "SECTOR_SYMBOL",
    "companies_analyzed": "array_of_selected_sector_companies",
    "sector_etfs_analyzed": "array_of_sector_etfs",
    "data_collection_methodology": "production_cli_services_multi_company_access",
    "cli_services_utilized": "dynamic_array_of_successfully_utilized_services",
    "api_keys_configured": "production_keys_from_config/financial_services.yaml"
  },
  "cli_comprehensive_sector_analysis": {
    "metadata": "complete_cli_response_aggregation_from_multi_company_collection",
    "sector_overview": "integrated_sector_intelligence_multi_company",
    "sector_market_data": "cross_validated_pricing_across_all_companies_and_etfs",
    "competitive_landscape": "sector_competitive_intelligence_integrated",
    "sector_etf_analysis": "etf_composition_and_performance_correlation",
    "data_validation": "multi_company_price_validation_with_confidence",
    "quality_metrics": "institutional_grade_sector_assessment"
  },
  "sector_companies_data": {
    "companies": "array_of_company_objects_with_complete_data",
    "sector_aggregates": {
      "total_market_cap": "sum_of_all_company_market_caps",
      "average_pe_ratio": "weighted_average_pe_across_companies",
      "sector_price_performance": "aggregated_price_performance_metrics",
      "confidence": "multi_company_confidence_0.0-1.0"
    },
    "price_validation_summary": {
      "companies_validated": "count_of_successfully_validated_companies",
      "average_confidence_score": "0.0-1.0_across_all_companies",
      "consistency_issues": "array_of_companies_with_price_inconsistencies"
    }
  },
  "sector_etf_data": {
    "primary_etf": "main_sector_etf_data_object",
    "secondary_etfs": "array_of_additional_sector_etfs",
    "etf_composition": "holdings_and_weightings_analysis",
    "etf_performance": "performance_correlation_with_individual_companies",
    "confidence": "etf_analysis_confidence_0.0-1.0"
  },
  "cross_sector_analysis": {
    "all_sector_etfs": {
      "SPY": "s_and_p_500_etf_data_object",
      "XLK": "technology_etf_data_object",
      "XLF": "financials_etf_data_object",
      "XLI": "industrials_etf_data_object",
      "XLP": "consumer_staples_etf_data_object",
      "XLU": "utilities_etf_data_object",
      "XLB": "materials_etf_data_object",
      "XLE": "energy_etf_data_object",
      "XLY": "consumer_discretionary_etf_data_object",
      "XLV": "healthcare_etf_data_object",
      "XLRE": "real_estate_etf_data_object"
    },
    "sector_relative_performance": {
      "vs_spy": "sector_performance_vs_sp500",
      "vs_other_sectors": "performance_comparison_matrix",
      "sector_ranking": "current_sector_rank_1_to_11",
      "ytd_performance": "year_to_date_performance_vs_all_sectors"
    },
    "sector_correlations": {
      "correlation_matrix": "11x11_sector_correlation_matrix",
      "highest_correlated_sector": "most_correlated_sector_with_coefficient",
      "lowest_correlated_sector": "least_correlated_sector_with_coefficient",
      "diversification_benefit": "sector_diversification_score"
    },
    "confidence": "cross_sector_analysis_confidence_0.0-1.0"
  },
  "sector_financial_metrics": {
    "aggregate_revenue_ttm": "sum_of_all_company_revenues",
    "aggregate_net_income": "sum_of_all_company_net_incomes",
    "weighted_average_pe_ratio": "market_cap_weighted_pe_across_sector",
    "sector_profit_margin": "weighted_average_profit_margin",
    "sector_return_on_equity": "weighted_average_roe",
    "aggregate_free_cash_flow": "sum_of_all_company_fcf",
    "sector_revenue_growth": "weighted_average_revenue_growth",
    "financial_health_distribution": {
      "strong_companies": "count_and_percentage",
      "moderate_companies": "count_and_percentage",
      "weak_companies": "count_and_percentage"
    },
    "confidence": "sector_financial_confidence_0.0-1.0"
  },
  "sector_intelligence": {
    "sector_business_models": {
      "dominant_revenue_streams": "array_of_primary_sector_revenue_sources",
      "business_model_diversity": "analysis_of_business_model_variation_within_sector",
      "sector_operational_characteristics": "common_operational_patterns_across_companies",
      "confidence": "sector_business_model_confidence_0.0-1.0"
    },
    "competitive_landscape": {
      "market_concentration": "hhi_index_and_market_share_analysis",
      "competitive_intensity": "assessment_of_competitive_dynamics",
      "barriers_to_entry": "analysis_of_sector_entry_barriers",
      "disruption_risk": "assessment_of_technological_regulatory_disruption",
      "confidence": "competitive_analysis_confidence_0.0-1.0"
    },
    "sector_key_metrics": {
      "sector_specific_kpis": "array_of_industry_relevant_kpis",
      "comparative_ratios": "cross_company_ratio_analysis",
      "valuation_multiples": "sector_valuation_multiple_ranges",
      "confidence": "sector_metrics_confidence_0.0-1.0"
    }
  },
  "vix_volatility_analysis": {
    "vix_proxy_ticker": "VIXY",
    "vix_proxy_name": "ProShares VIX Short-Term Futures ETF",
    "vix_proxy_current_price": "current_vixy_price_from_yahoo_finance_cli",
    "vix_historical_data": "2_year_vixy_historical_data_from_yahoo_finance",
    "sector_vix_correlation": "historical_correlation_coefficient_with_vixy_as_vix_proxy",
    "volatility_regime": "low_moderate_high_volatility_classification",
    "risk_on_off_behavior": "sector_performance_during_vixy_spikes_as_vix_proxy",
    "volatility_sensitivity": "sector_beta_to_vixy_movements",
    "data_source": "yahoo_finance_cli_vixy_as_vix_proxy",
    "data_validation": {
      "vixy_range_check": "validated_vixy_price_positive_value",
      "data_freshness": "real_time_vixy_data_from_yahoo_finance",
      "proxy_rationale": "vixy_tracks_vix_short_term_futures_for_volatility_analysis"
    },
    "confidence": "vix_proxy_analysis_confidence_0.0-1.0"
  },
  "cli_sector_market_context": {
    "metadata": "complete_cli_response_aggregation_from_fred_and_coingecko_for_sector",
    "sector_economic_indicators": "fred_cli_sector_specific_economic_data",
    "cryptocurrency_correlation": {
      "bitcoin_correlation": "sector_correlation_coefficient_with_btc",
      "crypto_sentiment": "coingecko_sentiment_analysis",
      "bitcoin_current_price": "current_btc_price_from_alpha_vantage",
      "bitcoin_daily_data": "btc_daily_price_movements",
      "risk_appetite_proxy": "bitcoin_as_risk_appetite_indicator",
      "correlation_strength": "weak_moderate_strong_correlation_classification",
      "confidence": "crypto_correlation_confidence_0.0-1.0"
    },
    "sector_market_summary": "economic_regime_assessment_with_sector_implications",
    "sector_cyclical_analysis": "sector_specific_economic_cycle_positioning"
  },
  "sector_economic_analysis": {
    "interest_rate_environment": "restrictive_neutral_accommodative",
    "yield_curve_signal": "inverted_flat_normal",
    "yield_curve_spread": "dgs10_minus_dgs2_spread_in_basis_points",
    "fed_funds_rate": "current_federal_funds_rate_from_fred",
    "unemployment_rate": "current_unemployment_rate_from_fred",
    "gdp_analysis": {
      "nominal_gdp": "current_gdp_level_billions",
      "real_gdp": "current_real_gdp_level_billions",
      "gdp_growth_rate": "quarterly_gdp_growth_rate_percent",
      "gdp_trend": "increasing_decreasing_stable",
      "sector_gdp_correlation": "correlation_coefficient_with_gdp_growth",
      "latest_gdp_date": "most_recent_gdp_release_date"
    },
    "employment_analysis": {
      "nonfarm_payrolls": "current_payrolls_thousands",
      "payrolls_change_monthly": "monthly_change_in_payrolls",
      "labor_force_participation": "current_participation_rate_percent",
      "initial_claims": "current_initial_claims_level",
      "employment_trend": "strengthening_weakening_stable",
      "sector_employment_sensitivity": "sector_correlation_with_employment_indicators",
      "employment_cyclical_position": "early_mid_late_cycle_assessment"
    },
    "dollar_strength": {
      "dxy_proxy_ticker": "UUP",
      "dxy_proxy_name": "Invesco DB US Dollar Index Bullish Fund",
      "dxy_proxy_current_price": "current_uup_price_from_yahoo_finance_cli",
      "dxy_historical_data": "1_year_uup_historical_data_from_yahoo_finance",
      "usd_eur_rate": "usd_eur_exchange_rate_from_fred",
      "sector_dollar_sensitivity": "sector_exposure_to_dollar_movements",
      "data_source": "yahoo_finance_cli_uup_as_dxy_proxy",
      "data_validation": {
        "uup_range_check": "validated_uup_price_positive_value",
        "data_freshness": "real_time_uup_data_from_yahoo_finance",
        "proxy_rationale": "uup_tracks_us_dollar_index_for_currency_strength_analysis"
      }
    },
    "liquidity_conditions": {
      "credit_spreads": "high_yield_credit_spreads_bamlh0a0hym2",
      "money_supply_growth": "m2_money_supply_growth_rate",
      "financial_conditions_index": "nfci_financial_conditions_index",
      "liquidity_regime": "tight_neutral_accommodative_classification"
    },
    "sector_policy_implications": "array_of_fed_policy_impacts_on_sector",
    "sector_sensitivity": "detailed_industry_specific_rate_sensitivity",
    "cyclical_positioning": "sector_position_in_economic_cycle",
    "historical_correlation": {
      "with_gdp_growth": "correlation_coefficient_with_quarterly_gdp_growth",
      "with_employment_growth": "correlation_coefficient_with_payroll_changes",
      "with_inflation": "correlation_coefficient_with_cpi_changes",
      "with_dollar_strength": "correlation_coefficient_with_dxy_movements"
    }
  },
  "sector_macroeconomic_context": {
    "gdp_impact_analysis": {
      "gdp_elasticity": "sector_sensitivity_to_gdp_growth_changes",
      "recession_performance": "sector_performance_during_gdp_contractions",
      "expansion_performance": "sector_performance_during_gdp_expansions",
      "gdp_leading_indicators": "sector_correlation_with_gdp_leading_indicators",
      "quarterly_patterns": {
        "q1_gdp_correlation": "correlation_with_q1_gdp_releases",
        "q2_gdp_correlation": "correlation_with_q2_gdp_releases",
        "q3_gdp_correlation": "correlation_with_q3_gdp_releases",
        "q4_gdp_correlation": "correlation_with_q4_gdp_releases"
      },
      "confidence": "gdp_impact_analysis_confidence_0.0-1.0"
    },
    "employment_impact_analysis": {
      "employment_elasticity": "sector_sensitivity_to_employment_changes",
      "payrolls_correlation": "historical_correlation_with_nonfarm_payrolls",
      "unemployment_sensitivity": "sector_response_to_unemployment_rate_changes",
      "labor_market_indicators": {
        "participation_rate_impact": "correlation_with_labor_force_participation",
        "initial_claims_sensitivity": "sector_response_to_claims_spikes",
        "job_creation_correlation": "correlation_with_monthly_job_creation"
      },
      "employment_cycle_positioning": "sector_position_relative_to_employment_cycle",
      "confidence": "employment_impact_analysis_confidence_0.0-1.0"
    },
    "macroeconomic_risk_assessment": {
      "recession_vulnerability": "sector_vulnerability_to_economic_downturns",
      "gdp_shock_sensitivity": "estimated_impact_of_1_percent_gdp_decline",
      "employment_shock_sensitivity": "estimated_impact_of_employment_deterioration",
      "early_warning_indicators": "array_of_gdp_employment_warning_signals",
      "defensive_characteristics": "sector_defensive_qualities_during_macro_stress",
      "confidence": "macro_risk_assessment_confidence_0.0-1.0"
    }
  },
  "sector_regulatory_intelligence": {
    "sector_insider_trading_data": "aggregated_fmp_cli_insider_activity_across_sector",
    "sector_regulatory_environment": "industry_specific_regulatory_framework",
    "regulatory_risk_assessment": "sector_wide_compliance_and_policy_risk",
    "upcoming_regulatory_changes": "analysis_of_pending_industry_regulations"
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
  "seasonality_analysis": {
    "historical_data_period": "10_year_historical_data_for_seasonality",
    "monthly_patterns": {
      "best_months": "array_of_historically_best_performing_months",
      "worst_months": "array_of_historically_worst_performing_months",
      "seasonal_strength": "statistical_significance_of_seasonal_patterns"
    },
    "quarterly_patterns": {
      "earnings_cycle_impact": "quarterly_earnings_performance_patterns",
      "q1_performance": "q1_historical_performance_vs_annual_average",
      "q2_performance": "q2_historical_performance_vs_annual_average",
      "q3_performance": "q3_historical_performance_vs_annual_average",
      "q4_performance": "q4_historical_performance_vs_annual_average"
    },
    "economic_cycle_patterns": {
      "recession_performance": "sector_performance_during_recessions",
      "expansion_performance": "sector_performance_during_expansions",
      "recovery_timeline": "average_recovery_time_after_drawdowns",
      "drawdown_analysis": "historical_maximum_drawdown_periods"
    },
    "confidence": "seasonality_analysis_confidence_0.0-1.0"
  },
  "sector_comparative_data": {
    "sector_vs_market": "sector_performance_vs_broader_market_indices",
    "sector_vs_peers": "comparison_with_related_sectors",
    "internal_rankings": "ranking_of_companies_within_sector",
    "competitive_positioning": "market_share_and_competitive_strength_analysis",
    "confidence": "0.0-1.0_sector_comparative_confidence"
  },
  "sector_discovery_insights": {
    "sector_initial_observations": "array_key_sector_and_competitive_insights",
    "sector_data_gaps": "array_missing_sector_data_points_for_analysis",
    "sector_research_priorities": "array_next_phase_sector_focus_areas",
    "sector_themes": "identified_sector_investment_themes_and_trends",
    "investment_recommendation_readiness": {
      "portfolio_allocation_data": "sector_weighting_and_allocation_context_preparation",
      "economic_cycle_positioning": "sector_rotation_and_timing_data_collection",
      "risk_adjusted_metrics": "sector_risk_return_characteristics_foundation",
      "cross_sector_comparative": "relative_attractiveness_data_preparation"
    },
    "next_phase_readiness": "boolean_sector_analysis_phase_readiness"
  },
  "sector_data_quality_assessment": {
    "multi_company_reliability_scores": "object_cli_service_reliability_across_all_companies",
    "sector_data_completeness": "0.0-1.0_overall_sector_completeness_score",
    "sector_data_freshness": "object_data_recency_assessment_across_sector",
    "sector_quality_flags": "array_sector_data_quality_observations",
    "etf_data_quality": "assessment_of_etf_data_reliability_and_freshness"
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
   - Execute `python yahoo_finance_cli.py history {sector_etf} --period 10y --env prod --output-format json` for seasonality analysis
   - Execute `python yahoo_finance_cli.py history {sector_etf} --period max --env prod --output-format json` for maximum historical data
   - Execute `python yahoo_finance_cli.py analyze SPY XLK XLF XLI XLP XLU XLB XLE XLY XLV XLRE --env prod --output-format json` for cross-sector analysis
   - Execute `python yahoo_finance_cli.py history SPY XLK XLF XLI XLP XLU XLB XLE XLY XLV XLRE --period 1y --env prod --output-format json` for sector correlations
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
   - Execute `python fred_economic_cli.py indicator DGS10 --env prod --output-format json` for 10-Year Treasury
   - Execute `python fred_economic_cli.py indicator DGS2 --env prod --output-format json` for 2-Year Treasury
   - Execute `python fred_economic_cli.py indicator DEXUSEU --env prod --output-format json` for USD/EUR
   - Execute `python fred_economic_cli.py indicator BAMLH0A0HYM2 --env prod --output-format json` for credit spreads
   - Execute `python fred_economic_cli.py indicator M2SL --env prod --output-format json` for money supply
   - Execute `python fred_economic_cli.py indicator NFCI --env prod --output-format json` for financial conditions
   - Execute `python fred_economic_cli.py indicator GDP --env prod --output-format json` for nominal GDP
   - Execute `python fred_economic_cli.py indicator GDPC1 --env prod --output-format json` for real GDP
   - Execute `python fred_economic_cli.py indicator A191RL1Q225SBEA --env prod --output-format json` for GDP growth rate
   - Execute `python fred_economic_cli.py indicator PAYEMS --env prod --output-format json` for nonfarm payrolls
   - Execute `python fred_economic_cli.py indicator CIVPART --env prod --output-format json` for labor force participation
   - Execute `python fred_economic_cli.py indicator ICSA --env prod --output-format json` for initial claims
   - Execute `python yahoo_finance_cli.py quote VIXY --env prod --output-format json` for volatility
   - Execute `python yahoo_finance_cli.py history VIXY --period 2y --env prod --output-format json` for VIX historical data
   - Execute `python yahoo_finance_cli.py quote UUP --env prod --output-format json` for dollar strength
   - Execute `python yahoo_finance_cli.py history UUP --period 1y --env prod --output-format json` for DXY historical data
   - Execute `python alpha_vantage_cli.py quote BTCUSD --env prod --output-format json` for crypto correlation
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

5. **Enhanced Data Processing and Calculations**
   - **Cross-Sector Relative Analysis**: Calculate sector performance vs all 11 sector ETFs
   - **Yield Curve Calculation**: Compute DGS10 - DGS2 spread in basis points
   - **VIX Correlation Analysis**: Calculate historical correlation coefficients with VIX
   - **Dollar Sensitivity Assessment**: Analyze sector exposure to DXY movements
   - **Seasonality Pattern Detection**: Identify monthly and quarterly performance patterns
   - **Economic Cycle Positioning**: Assess sector position relative to economic indicators
   - **Correlation Matrix Generation**: Create 11x11 sector correlation matrix
   - **Risk-On/Risk-Off Classification**: Determine sector behavior during market stress
   - **Multi-Source Fallback Logic**: Implement graceful degradation for VIX/DXY data collection
     - **Primary Source**: Yahoo Finance CLI (VIXY, UUP) with 1.0 reliability score and tested API responses
     - **Secondary Source**: Alpha Vantage CLI (VIX, DXY) as fallback if Yahoo Finance fails
     - **Tertiary Source**: FRED CLI for volatility/currency proxies if both primary sources fail
     - **Data Validation**: Range validation (VIXY: >$10, UUP: >$20) for all sources
     - **API Testing Confirmed**: VIXY current price $44.20, UUP current price $27.09 with full historical data

6. **Multi-Source Data Quality Assessment**
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
   - **Fallback Logic**: Use historical data (current year → previous 3 years) for missing current-year values only when calculation not possible
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
- **Enhanced Quality Targets**: >97% overall data quality, >92% data completeness, >95% financial statement confidence, >90% investment recommendation readiness
- **Cross-Sector Analysis Quality**: >90% confidence in all 11 sector ETF correlations and relative performance metrics
- **Economic Sensitivity Quality**: >95% confidence in yield curve, dollar strength, and liquidity condition indicators
- **GDP Analysis Quality**: >90% confidence in GDP growth correlation and sector economic sensitivity assessment
- **Employment Analysis Quality**: >90% confidence in payroll correlation and labor market impact analysis
- **VIX Correlation Quality**: >90% confidence in volatility regime assessment and risk-on/off behavior analysis via Yahoo Finance CLI
- **Seasonality Analysis Quality**: >80% confidence in 10-year historical patterns and quarterly earnings cycles

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
- **Enhanced Quality Flags**: "comprehensive_financial_statement_data_including_cash_flow", "enhanced_financial_metrics_with_calculated_ratios", "cross_sector_analysis_with_11_etf_coverage", "vix_volatility_correlation_analysis_yahoo_finance_cli", "dxy_dollar_strength_analysis_yahoo_finance_cli", "yield_curve_and_economic_sensitivity_complete", "gdp_analysis_with_sector_correlation", "employment_analysis_with_sector_sensitivity", "macroeconomic_context_integration_complete", "investment_recommendation_data_prepared", "portfolio_allocation_context_ready"
- **Institutional-Grade Quality**: >97% overall confidence through production CLI services unified access
- **Cross-Sector Validation**: All 11 sector ETFs successfully collected with <2% price variance
- **Economic Indicator Validation**: All FRED economic indicators current within 24 hours
- **VIX Correlation Validation**: Historical VIX data spans minimum 2 years for reliable correlation via Yahoo Finance CLI
- **VIX Data Quality Validation**: VIX level validated within 10-50 range using Yahoo Finance CLI primary source
- **Dollar Sensitivity Validation**: DXY and USD/EUR data consistency verified across Yahoo Finance CLI (primary) and FRED sources
- **DXY Data Quality Validation**: DXY level validated within 90-120 range using Yahoo Finance CLI primary source
- **GDP Data Quality Validation**: GDP indicators validated for quarterly frequency with current data within 90 days
- **Employment Data Quality Validation**: Employment indicators validated for monthly frequency with current data within 30 days
- **Macroeconomic Integration Validation**: GDP and employment correlations calculated using minimum 5 years of historical data
- **Seasonality Data Validation**: Minimum 10 years of historical data for statistical significance

**Integration with DASV Framework**: This microservice provides the foundational data required for the subsequent analyze phase, ensuring high-quality input for systematic financial analysis and template-driven synthesis with Investment Recommendation Summary following `/docs/sector_analysis_template.md`.

**Author**: Cole Morton
**Confidence**: [Discovery confidence will be calculated based on data quality and completeness]
**Data Quality**: [Data quality score based on source reliability and validation completeness]
