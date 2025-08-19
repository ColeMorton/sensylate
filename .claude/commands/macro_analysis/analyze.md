# Macro-Economic Analyst Analyze

**DASV Phase 2: Regional Macro-Economic Analysis Requirements**

Generate comprehensive regional macro-economic analysis focusing on business cycle positioning, monetary policy transmission, and cross-asset implications with region-specific adaptations.

## Purpose

Define the analytical requirements for transforming macro-economic discovery data into comprehensive regional economic intelligence. This specification focuses on domain-specific requirements while delegating implementation methodology to the analyst sub-agent.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: macro_analyst
**Action**: analyze
**Input Source**: cli_enhanced_macro_analyst_discover
**Output Location**: `./{DATA_OUTPUTS}/macro_analysis/analysis/`
**Next Phase**: macro_analyst_synthesize
**Tool Integration**: Uses `macro_analyze_unified.py` via analyst sub-agent orchestration
**Implementation Delegation**: Analyst sub-agent handles execution methodology

## Analysis Parameters

### Core Requirements
- `discovery_file`: Path to macro discovery JSON file (required) - format: {REGION}_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Enhanced Analysis Feature Toggles
- `business_cycle_modeling`: Enable advanced business cycle positioning with validation - `true` | `false` (optional, default: true)
- `monetary_policy_analysis`: Enable comprehensive monetary policy assessment with real-time validation - `true` | `false` (optional, default: true)
- `economic_scenario_analysis`: Enable multi-scenario economic modeling with cross-validation - `true` | `false` (optional, default: true)
- `cross_asset_analysis`: Enable cross-asset correlation framework with variance monitoring - `true` | `false` (optional, default: true)
- `policy_transmission_analysis`: Enable policy transmission mechanism assessment with consistency checks - `true` | `false` (optional, default: true)
- `real_time_validation`: Enable fail-fast validation against current market data - `true` | `false` (optional, default: true)
- `staleness_detection`: Enable automatic detection of outdated data - `true` | `false` (optional, default: true)

## Regional Economic Analysis Requirements

### 1. Business Cycle Positioning Requirements

**Multi-Dimensional Economic Phase Assessment**:
- **Leading Indicator Analysis**: Composite scoring using yield curve, employment trends, and growth indicators
- **Recession Probability Modeling**: NBER-style probability calculation with confidence intervals
- **Phase Transition Analysis**: Economic cycle transitions and probability modeling
- **Historical Pattern Integration**: Business cycle positioning relative to historical patterns

**Monetary Policy Context Integration**:
- **Central Bank Policy Stance**: Region-appropriate central bank assessment (Fed/ECB/BoJ/PBoC)
- **Interest Rate Transmission**: Quantification across regional markets and asset classes
- **Policy Effectiveness Analysis**: Forward guidance impact and market reaction assessment
- **Currency-Specific Considerations**: Regional currency impact on policy transmission

**Economic Growth Components**:
- **GDP Decomposition**: Consumption, investment, government, net exports analysis
- **Productivity Integration**: Growth trends and labor market dynamics
- **Regional Growth Differentials**: Cross-regional comparative assessment
- **Sustainability Assessment**: Long-term growth potential and recession risk evaluation

### 2. Global Liquidity and Regional Policy Analysis

**Central Bank Coordination Assessment**:
- **Policy Synchronization**: Fed/ECB/BoJ/PBoC coordination and divergence implications
- **Cross-Border Flow Analysis**: Liquidity flows and regional currency impacts
- **Quantitative Easing Impact**: Regional asset price transmission and effectiveness
- **International Spillover Effects**: Policy coordination mechanisms and regional impacts

**Regional Credit Market Dynamics**:
- **Credit Condition Assessment**: Regional vs global credit spread analysis
- **Banking Sector Analysis**: Regional liquidity provision and capital adequacy
- **Systemic Risk Evaluation**: Regional credit stress indicators and risk assessment
- **Capital Flow Integration**: International flows and regional market implications

**Money Supply Regional Analysis**:
- **Regional Money Supply Trends**: M2 growth and velocity implications by region
- **Asset Price Impact**: Regional valuation effects and inflation transmission
- **Digital Currency Considerations**: Regional CBDC impact on money supply measurement
- **Liquidity Condition Classification**: Regional liquidity regime assessment

### 3. Market Regime and Cross-Asset Requirements

**Regional Market Regime Classification**:
- **Volatility Regime Assessment**: Regional volatility patterns and persistence analysis
- **Risk Appetite Classification**: Regional risk-on/risk-off dynamics and correlation
- **Liquidity Regime Scoring**: Regional market liquidity conditions and stress assessment
- **Policy Environment Rating**: Regional fiscal/monetary policy support classification

**Cross-Asset Regional Correlation**:
- **Interest Rate Transmission**: Regional rate impact on asset classes and economic activity
- **Currency Impact Analysis**: Regional currency effects on trade balance and competitiveness
- **Risk Asset Flow Patterns**: Regional equity-bond correlation dynamics and safe haven flows
- **Economic Indicator Sensitivity**: Regional surprise impact on cross-asset allocation

### 4. Economic Scenario and Risk Assessment Requirements

**Multi-Scenario Regional Modeling**:
- **Base Case Regional Scenario**: GDP trajectory, inflation path, and employment evolution
- **Bull Case Regional Scenario**: Accelerated growth with regional policy support coordination
- **Bear Case Regional Scenario**: Economic slowdown with region-specific policy error risks
- **Probability-Weighted Integration**: Regional scenario weighting and blended forecasting

**Regional Economic Risk Matrix**:
- **GDP-Based Risk Assessment**: Regional GDP deceleration and recession vulnerability
- **Employment-Based Risk Assessment**: Regional labor market deterioration and sector demand impact
- **Inflation Risk Analysis**: Regional inflation shock scenarios and central bank response capacity
- **Geopolitical Risk Integration**: Region-specific geopolitical risks and safe haven implications

**Regional Policy Response Analysis**:
- **Central Bank Reaction Functions**: Regional policy space and tool effectiveness
- **Fiscal Policy Assessment**: Regional automatic stabilizers and discretionary capacity
- **International Coordination**: Regional policy coordination requirements and mechanisms
- **Recovery Timeline Estimation**: Regional business cycle context and historical recovery patterns

## Tool Integration Requirements

### Python Tool Orchestration
**Primary Tool**: `macro_analyze_unified.py`
- **Regional Adaptation**: Automatic detection and adaptation for analysis region
- **Data-Driven Calculations**: Elimination of hardcoded values through discovery data integration
- **Consistency Enforcement**: Institutional-grade quality standards across all regional outputs
- **Dynamic Probabilities**: Real indicator-based probability and correlation calculations

**Tool Execution Requirements**:
- **Command Pattern**: `python {SCRIPTS_BASE}/macro_analyze_unified.py {REGION}_{YYYYMMDD}_discovery.json [confidence_threshold]`
- **Regional Intelligence**: Automatic central bank and currency adaptation
- **Quality Assurance**: Numeric confidence values and JSON structure consistency
- **CLI Integration**: Service health monitoring and data quality attribution

## Regional Adaptation Requirements

### Currency and Central Bank Context
- **North America**: Fed policy, USD impact, NAFTA trade considerations
- **Europe**: ECB policy, EUR dynamics, EU regulatory coordination
- **Asia-Pacific**: BoJ/PBoC policy, JPY/CNY considerations, regional trade flows
- **Emerging Markets**: Regional central bank capacity, currency risk assessment

### Regional Economic Indicators
- **Growth Metrics**: Region-appropriate GDP, productivity, and employment indicators
- **Inflation Measures**: Regional core vs headline inflation, policy target effectiveness
- **Trade Integration**: Regional trade balance, competitiveness, and flow analysis
- **Financial Stability**: Regional banking health, credit conditions, and systemic risk

## Output Structure Requirements

**File Naming**: `{REGION}_{YYYYMMDD}_analysis.json`
**Primary Location**: `./{DATA_OUTPUTS}/macro_analysis/analysis/`

### Required Output Sections
1. **Business Cycle Positioning**
   - Current phase classification with regional context
   - Recession probability with confidence intervals
   - Interest rate sensitivity and inflation hedge assessment
   - GDP growth correlation with regional elasticity

2. **Liquidity Cycle Positioning**
   - Regional central bank policy stance impact
   - Credit market conditions and capital access
   - Money supply impact and asset price dynamics
   - Employment sensitivity with regional labor indicators

3. **Multi-Method Regional Valuation**
   - Economic growth impact on regional valuations
   - Cost of capital using regional central bank rates
   - Currency and market risk considerations
   - Cross-regional comparative assessment

4. **Quantified Regional Risk Assessment**
   - Risk matrix with region-specific probability × impact scoring
   - Stress testing with regional economic conditions
   - Early warning indicators and monitoring frameworks
   - Regional policy response capacity assessment

## Quality and Confidence Requirements

### Regional Specificity Standards
- **Central Bank References**: Appropriate for analysis region (Fed/ECB/BoJ/PBoC/etc)
- **Currency Analysis**: Region-specific exchange rate impacts and correlations
- **Economic Indicators**: Regional indicators and business cycle context
- **Policy Framework**: Local regulatory and monetary policy integration

### Enhanced Institutional-Grade Standards
- **Analysis Confidence**: ≥9.0/10.0 institutional baseline with real-time validation
- **Data Freshness Validation**: All key indicators validated against real-time consensus data
- **Regional Specificity**: >90% regional adaptation with fail-fast on template artifacts
- **Data-Driven Quality**: Real calculations with staleness detection and cross-validation
- **CLI Attribution**: Service transparency with health monitoring and quality validation
- **Variance Monitoring**: Configurable deviation thresholds from consensus with automatic flagging
- **Cross-Validation Requirements**: Multi-source validation across all key indicators

### Evidence Requirements
- **Quantitative Backing**: All regional conclusions supported by discovery data
- **Historical Context**: Regional business cycle patterns and precedent analysis
- **Cross-Validation**: Multi-source regional indicator consistency
- **Policy Integration**: Regional central bank and fiscal policy framework alignment

## Implementation Notes

**Analyst Sub-Agent Integration**: This specification defines WHAT regional economic analysis is required. The analyst sub-agent handles HOW to execute the analysis through:
- Universal 4-phase analytical framework application
- Tool orchestration for macro_analyze_unified.py execution
- Discovery data preservation and quality enforcement
- Regional adaptation and consistency validation

**Key Differentiators**:
- **Regional Intelligence**: Automatic adaptation for Fed/ECB/BoJ/PBoC policy contexts
- **Tool Integration**: Python script orchestration with quality assurance
- **Data-Driven Methodology**: Elimination of hardcoded assumptions
- **Cross-Asset Integration**: Regional correlation and transmission analysis
- **Policy Response Assessment**: Regional capacity and coordination evaluation

**Domain Focus**: This specification emphasizes regional economic requirements and unique macro-economic factors while delegating universal analytical methodology to the analyst sub-agent for consistent institutional-grade execution.

---

**Framework Integration**: Optimized for DASV analyst sub-agent execution with focus on regional macro-economic domain requirements rather than implementation methodology.

**Author**: Cole Morton
**Optimization**: 60% complexity reduction through implementation delegation to analyst sub-agent
**Confidence**: Domain requirements specification with institutional-grade regional analysis standards
