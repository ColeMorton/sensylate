# Macro-Economic Analyst Discover

**DASV Phase 1: Macro-Economic Data Collection and Context Gathering**

Comprehensive macro-economic data collection and market intelligence gathering for institutional-quality macro-economic analysis using systematic discovery protocols and production-grade CLI data acquisition methodologies focusing on business cycles, monetary policy, economic indicators, and market regime analysis.

## Purpose

The Macro-Economic Analysis Discovery phase represents the systematic collection and initial structuring of all data required for comprehensive macro-economic analysis. This context guide provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on economic indicator acquisition standards, business cycle data collection criteria, monetary policy analysis requirements, and foundational macro-economic research requirements using production-grade CLI financial services.

**Expected Output Schema**: `/scripts/schemas/macro_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute macro-economic analysis discovery. Ensure output conforms to `/scripts/schemas/macro_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: macro_analyst
**Action**: discover
**Output Location**: `./data/outputs/macro_analysis/discovery/`
**Next Phase**: macro_analyst_analyze

## Parameters

### Core Parameters
- `region`: Geographic focus (required) - `US` | `global` | `europe` | `asia` | `americas` | etc.
- `indicators`: Economic indicators to analyze - `gdp` | `employment` | `inflation` | `monetary_policy` | `business_cycle` | `all` (optional, default: all)
- `timeframe`: Analysis period - `1y` | `2y` | `5y` | `10y` | `full` (optional, default: 5y)
- `include_forecasts`: Include forward-looking projections - `true` | `false` (optional, default: true)

### Advanced Parameters
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)
- `business_cycle_focus`: Include detailed business cycle analysis - `true` | `false` (optional, default: true)
- `market_regime_analysis`: Include market regime classification - `true` | `false` (optional, default: true)

## Validation Enhancement Context

**Discovery Optimization Requirements**:
- Check for existing validation files to enable discovery enhancement protocols
- When validation files exist, apply systematic enhancement to improve discovery phase scores to 9.5+
- Target institutional-quality first collection appearance in optimized outputs
- Maintain schema compliance throughout enhancement process

## Data Sources and Integration Requirements

**Required Financial Services**:
1. **FRED Economic CLI** - Federal Reserve economic data, business cycle indicators, and monetary policy analysis (MANDATORY)
2. **IMF Data CLI** - Global economic indicators, country risk assessment, and international economic forecasts
3. **Alpha Vantage CLI** - Real-time market data, economic sentiment analysis, and technical indicators
4. **EIA Energy CLI** - Energy market data, oil prices, natural gas, and electricity generation analysis
5. **CoinGecko CLI** - Cryptocurrency market data for risk appetite and monetary debasement analysis
6. **FMP CLI** - Advanced economic metrics, currency data, and cross-asset correlation analysis
7. **Economic Calendar CLI** - Economic calendar events and market impact analysis

**Integration Requirements**:
- Multi-source economic indicator validation with confidence scoring
- **MANDATORY: Current Federal Reserve policy stance and forward guidance collection**
- Business cycle indicator analysis with leading/coincident/lagging classification
- Cross-validation with institutional-grade confidence scoring across multiple economic data sources
- Market regime intelligence, volatility analysis, and cross-asset correlation assessment
- Global economic context integration for international economic exposure assessment
- Cryptocurrency correlation analysis for monetary policy and risk appetite assessment
- Interest rate sensitivity analysis across yield curve and policy transmission mechanisms
- Multi-service economic data validation with graceful degradation capabilities

## Data Flow Integration

### Input Consumption Patterns
**macro_analysis_discover_inputs**:
```yaml
macro_analysis_inputs:
  required_parameters:
    - region: "Geographic focus (US | global | europe | asia | americas)"
    - indicators: "gdp | employment | inflation | monetary_policy | business_cycle | all (default: all)"
    - confidence_threshold: "9.0 | 9.5 | 9.8 (default: 9.0)"

  upstream_data_consumption:
    - trade_history_files: "./data/outputs/trade_history/{PORTFOLIO}_{DATE}.md"
    - sector_analysis_data: "./data/outputs/sector_analysis/discovery/{SECTOR}_{DATE}_discovery.json"
    - industry_analysis_data: "./data/outputs/industry_analysis/discovery/{INDUSTRY}_{DATE}_discovery.json"

  cli_services_consumed:
    - fred_economic_cli: "Federal Reserve economic data + business cycle indicators (MANDATORY)"
    - imf_cli: "Global economic indicators + country risk assessment"
    - alpha_vantage_cli: "Real-time market data + economic sentiment analysis"
    - eia_energy_cli: "Energy market data + oil/gas price analysis"
    - coingecko_cli: "Cryptocurrency data + risk appetite analysis"
    - fmp_cli: "Advanced economic metrics + currency correlation"
    - economic_calendar_cli: "Economic calendar events + market impact analysis"

  mandatory_economic_data:
    - federal_reserve_data: "MANDATORY current Fed policy stance and forward guidance"
    - business_cycle_indicators: "GDP, employment, inflation, leading indicators"
    - blocking_requirements: "Missing Fed policy data prevents institutional certification"

macro_analysis_outputs:
  discovery_files: "./data/outputs/macro_analysis/discovery/{REGION}_{YYYYMMDD}_discovery.json"
  next_phase_inputs: "macro_analyst_analyze consumption"
  downstream_dependencies:
    - "portfolio_allocation: macro context for asset allocation decisions"
    - "sector_analysis: economic context for sector rotation analysis"
    - "social_media_strategist: macro themes integration"

  data_flow_architecture:
    - namespace: "macro_analysis"
    - pattern: "economic_indicators → business_cycle_analysis → macro_analysis → macro_synthesis → validation"
    - integration_points: "Economic data → macro aggregation → downstream consumption"
    - quality_inheritance: "Inherits economic data confidence scores → aggregates for macro confidence"
```

## Data Collection Requirements

### Economic Indicator Selection Criteria
**Macro-Economic Indicator Selection Standards**:
1. **Regional Filtering**: Select indicators based on region parameter (US, global, europe, asia)
2. **Indicator Relevance**: Prioritize indicators with high business cycle predictive power
3. **Data Frequency**: Ensure adequate update frequency for real-time economic assessment
4. **Geographic Coverage**: Include representative regional and global economic exposure
5. **Temporal Distribution**: Balance leading, coincident, and lagging economic indicators

### Data Collection Standards
**Core Requirements**:
- Production CLI financial services for comprehensive 7-source macro-economic data integration
- Institutional-grade data quality and multi-source validation across all economic indicators
- Current date-relative data collection (never use hardcoded years in searches)
- Always use terms like "latest", "current", "recent", "current quarter", "year-to-date"

### Core Data Categories

**Business Cycle Analysis Requirements**:
- Leading indicator data collection (yield curve, consumer confidence, stock market performance)
- Coincident indicator analysis (GDP, employment, industrial production, real income)
- Lagging indicator integration (unemployment rate, CPI, labor costs, consumer credit)
- Cross-indicator validation with institutional-grade statistical precision
- Real-time business cycle phase identification and transition probability analysis

**Monetary Policy Analysis Requirements**:
- **MANDATORY: Current Federal Reserve policy stance and forward guidance collection**
- Fed funds rate analysis with policy transmission mechanism assessment
- Quantitative easing program analysis and balance sheet composition
- Central bank communication analysis and forward guidance interpretation
- Cross-central bank policy coordination analysis (Fed, ECB, BoJ, PBoC)

**Market Intelligence Requirements**:
- Real-time market regime classification with volatility analysis
- VIX volatility analysis for economic stress assessment
- DXY dollar strength analysis for global economic transmission
- Bitcoin correlation analysis for monetary policy and risk appetite assessment
- Advanced cross-asset analytics and economic sentiment assessment

**Economic Growth Requirements**:
- GDP growth analysis with quarterly and annual trend assessment
- Employment indicators with nonfarm payrolls and labor force participation
- Inflation environment analysis with core vs headline CPI assessment
- Industrial production and manufacturing activity indicators
- Consumer spending and retail sales trend analysis

**Global Economic Context Requirements**:
- International economic indicators with cross-country correlation analysis
- Currency and trade flow analysis for global economic transmission
- Energy market integration with oil, natural gas, and electricity analysis
- Commodity price analysis for inflation and supply chain assessment
- Geopolitical risk assessment and economic policy coordination

### Advanced Analysis Requirements

**Cross-Asset Intelligence Requirements**:
- Comprehensive cross-asset correlation analysis across equities, bonds, commodities, currencies
- Inter-market analysis with bond-equity relationship and yield curve positioning
- Asset allocation flow analysis with institutional positioning and sentiment assessment
- Risk-on/risk-off behavior analysis across asset classes and geographic regions

**Market Context Requirements**:
- Real-time economic regime correlation with broader market performance
- Volatility analysis and economic stress assessment across business cycle phases
- Dollar strength transmission analysis for global economic and market implications
- Interest rate environment implications and cross-asset sensitivity analysis

**Economic Intelligence Requirements**:
- Federal Reserve policy implications and business cycle positioning analysis
- GDP growth transmission analysis and cross-sector economic sensitivity assessment
- Global economic indicators affecting international trade and capital flows
- Liquidity conditions and credit market implications for economic growth and asset markets

## Output Structure and Schema

**File Naming**: `{REGION}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/macro_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/macro_analysis_discovery_schema.json`

### Required Output Components
- **Economic Indicators**: Leading, coincident, and lagging indicator analysis with statistical validation
- **Business Cycle Analysis**: Current phase identification and transition probability assessment
- **Monetary Policy Context**: Fed policy stance, forward guidance, and transmission mechanisms
- **Market Regime Classification**: Volatility environment, risk-on/off behavior, and regime sustainability
- **Global Economic Intelligence**: International indicators, currency flows, and cross-country correlations
- **Cross-Asset Analysis**: Bond-equity relationships, commodity correlations, and asset allocation flows
- **Energy Market Integration**: Oil, gas, electricity analysis with inflation and supply chain implications
- **Quality Metrics**: Confidence scores, data completeness, and source reliability assessment

### Schema Compliance Standards
- Minimum 4 CLI services utilized for institutional-grade macro analysis
- Mandatory current Federal Reserve policy data collection with <1% variance validation
- Multi-source economic indicator validation across data providers (targeting >90% confidence)
- Overall data quality ≥ 0.85 for institutional standards
- Complete macro-economic discovery insights with policy analysis readiness
- Automated quality validation achieving ≥ 9.0/10.0 for institutional certification
- Region-specific analysis implementation (no generic templates)
- Dynamic confidence scoring (no hardcoded values)

## Quality Standards and Requirements

### Pre-Execution Requirements
- Regional identifier validation and economic indicator selection criteria application
- CLI services configuration and API key validation
- Confidence threshold configuration based on depth parameter
- Optional validation enhancement protocol activation for existing validation files

### Data Quality Standards
**Multi-Source Economic Validation**:
- Economic indicator consistency verification across all data providers
- Federal Reserve data cross-validation with IMF and regional sources
- Business cycle indicator composition and correlation validation
- Global economic indicators freshness and relevance assessment

**Institutional-Grade Thresholds**:
- Overall data quality ≥ 0.85 for macro-economic analysis
- Service reliability ≥ 80% health score across CLI services
- Mandatory Fed policy data collection with <1% variance requirement
- Multi-source confidence scoring targeting >90% indicator coverage

### Enhanced Analysis Requirements
- Cross-regional analysis with major economic zones for relative positioning
- Business cycle analysis with minimum 10-year historical data
- Economic transmission assessment with GDP, employment, and inflation correlation
- Central bank policy coordination analysis with cross-country policy metrics

### Automated Quality Validation Framework
**Fail-Fast Approach**:
- Pre-execution service availability validation (minimum 4 services required)
- FRED service mandatory validation (blocks execution if unavailable)
- Service health checks before data collection attempts
- No fallback mock data - graceful degradation with reduced confidence

**Quality Validation Checks**:
- **Service Availability**: Validates minimum CLI service requirements
- **Data Completeness**: Ensures all required sections are populated
- **Cross-Source Consistency**: Validates data consistency across services
- **Region Specificity**: Detects template artifacts and ensures region-appropriate analysis
- **Confidence Calibration**: Validates dynamic confidence scoring (no hardcoded values)

**Institutional Certification**:
- Overall quality score ≥ 9.0/10.0 required for institutional certification
- Automated blocking issue detection and recommendations
- Real-time quality assessment during discovery execution

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
- **Overall Data Quality**: ≥ 97% confidence through multi-source economic validation
- **Fed Policy Data Collection**: 100% success rate with <1% variance validation
- **Multi-Source Economic Coverage**: ≥ 90% confidence across economic indicators
- **Business Cycle Integration**: ≥ 95% confidence in business cycle phase identification

### Key Deliverables
- Comprehensive economic indicator analysis with multi-source validation
- Mandatory Federal Reserve policy analysis with current stance and forward guidance
- Cross-regional analysis with major economic zones for relative positioning
- Business cycle context with phase-specific sensitivity analysis
- Volatility and market regime assessment including VIX and cross-asset analysis
- Long-term business cycle analysis with 10-year historical patterns
- Discovery insights identifying macro-economic themes and policy priorities
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational macro-economic data required for the subsequent analyze phase, ensuring high-quality input for systematic macro-economic analysis and policy assessment synthesis.

**Author**: Cole Morton
