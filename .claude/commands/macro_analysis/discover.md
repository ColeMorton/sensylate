# Macro-Economic Analyst Discover

**DASV Phase 1: Macro-Economic Data Collection and Context Gathering**

Comprehensive macro-economic data collection and market intelligence gathering for institutional-quality macro-economic analysis using systematic discovery protocols and researcher sub-agent orchestration focusing on business cycles, monetary policy, economic indicators, and market regime analysis.

## Purpose

The Macro-Economic Analysis Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive macro-economic analysis. This specification focuses on **what** economic indicators and macroeconomic context is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/scripts/schemas/macro_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute macro-economic analysis discovery. Ensure output conforms to `/scripts/schemas/macro_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: macro_analyst
**Action**: discover
**Output Location**: `./data/outputs/macro_analysis/discovery/`
**Next Phase**: macro_analyst_analyze
**Template Reference**: `./templates/analysis/macro_analysis_template.md` (final output structure awareness)

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

## Data Requirements

### Core Data Categories

**Business Cycle Analysis Requirements**:
- Leading economic indicators (yield curve, consumer confidence, stock market performance)
- Coincident indicators (GDP, employment, industrial production, real income)
- Lagging indicators (unemployment rate, CPI, labor costs, consumer credit)
- Business cycle phase identification and transition probability analysis
- NBER-style recession modeling and economic contraction assessment

**Monetary Policy Analysis Requirements**:
- Federal Reserve policy stance and forward guidance analysis
- Interest rate environment and policy transmission mechanisms
- Quantitative easing programs and central bank balance sheet analysis
- Cross-central bank policy coordination (Fed, ECB, BoJ, PBoC)
- Yield curve analysis and inversion signals for recession probability

**Market Regime Classification Requirements**:
- Real-time market regime identification (bull/bear/sideways markets)
- Volatility environment analysis and economic stress assessment
- Risk-on/risk-off behavior across asset classes and regions
- Cross-asset correlation analysis and market transmission mechanisms
- Asset allocation flow analysis with institutional positioning assessment

**Economic Growth Requirements**:
- GDP growth analysis with quarterly and annual trend assessment
- Employment indicators with labor force participation and productivity metrics
- Inflation environment analysis with core vs headline decomposition
- Industrial production and manufacturing activity indicators
- Consumer spending patterns and retail sales trend analysis

**Global Economic Context Requirements**:
- International economic indicators with cross-country correlation analysis
- Currency relationships and trade flow analysis
- Energy market integration with commodity price transmission
- Geopolitical risk assessment and economic policy coordination
- Regional economic development and emerging market dynamics

### Quality Standards
- **Multi-Source Validation**: Cross-validation across multiple economic data providers
- **Economic Data Freshness**: Current quarter economic indicators with <24 hour latency
- **Business Cycle Accuracy**: Statistical validation of cycle classification methodology
- **Policy Analysis Depth**: Comprehensive central bank communication analysis
- **Global Integration**: Multi-regional economic context with correlation assessment

## Output Structure and Schema

**File Naming**: `{REGION}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/macro_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/macro_analysis_discovery_schema.json`

### Required Output Components
- **Economic Indicators**: Leading, coincident, and lagging indicator comprehensive analysis
- **Business Cycle Analysis**: Current phase identification and transition probability assessment
- **Monetary Policy Context**: Federal Reserve policy stance with transmission mechanism analysis
- **Market Regime Classification**: Volatility environment and cross-asset risk assessment
- **Global Economic Intelligence**: International indicators with cross-country correlation analysis
- **Quality Metrics**: Confidence scores, data completeness, and source reliability assessment

### Schema Compliance Standards
- Economic indicator coverage across all major categories (growth, employment, inflation, policy)
- Business cycle classification with statistical validation and confidence measurement
- Monetary policy integration with forward guidance and transmission analysis
- Global economic context with multi-regional correlation and sensitivity assessment

## Expected Outcomes

### Discovery Quality Targets
- **Economic Data Quality**: ≥ 97% confidence through multi-source validation
- **Business Cycle Confidence**: ≥ 90% confidence in phase classification accuracy
- **Policy Analysis Depth**: ≥ 95% confidence in monetary policy assessment
- **Global Integration**: ≥ 85% confidence in cross-regional correlation analysis

### Key Deliverables
- Comprehensive economic indicator analysis with statistical significance validation
- Business cycle assessment with phase identification and transition probabilities
- Monetary policy analysis with central bank communication and forward guidance
- Market regime classification with volatility and cross-asset analysis
- Global economic context with regional correlation and transmission mechanisms
- Long-term economic trend analysis with historical pattern recognition

**Integration with DASV Framework**: This command provides the foundational macro-economic data required for the subsequent analyze phase, ensuring high-quality input for systematic macro-economic analysis and policy assessment synthesis.

**Author**: Cole Morton