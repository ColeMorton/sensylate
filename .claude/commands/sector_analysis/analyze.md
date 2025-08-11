# Sector Analyst Analyze

**DASV Phase 2: Sector-Specific Analysis Requirements**

Generate comprehensive sector analysis focusing on economic cycle positioning, industry dynamics, and investment allocation recommendations through template gap analysis methodology.

## Purpose

Define the analytical requirements for transforming sector discovery data into comprehensive investment intelligence. This specification focuses on sector-specific analytical requirements while delegating template gap analysis methodology to the analyst sub-agent.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: sector_analyst
**Action**: analyze
**Input Source**: cli_enhanced_sector_analyst_discover
**Output Location**: `./data/outputs/sector_analysis/analysis/`
**Next Phase**: sector_analyst_synthesize
**Template Integration**: `./templates/analysis/sector_analysis_template.md`
**Implementation Delegation**: Analyst sub-agent handles template gap analysis methodology

## Analysis Parameters

### Core Requirements
- `discovery_file`: Path to sector discovery JSON file (required) - format: {SECTOR}_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Sector Analysis Features
- `business_cycle_analysis`: Enable business cycle positioning - `true` | `false` (optional, default: true)
- `liquidity_cycle_analysis`: Enable liquidity cycle assessment - `true` | `false` (optional, default: true)
- `industry_scorecard`: Enable A-F graded industry scorecard - `true` | `false` (optional, default: true)
- `valuation_framework`: Enable multi-method valuation - `true` | `false` (optional, default: true)
- `risk_quantification`: Enable quantified risk matrices - `true` | `false` (optional, default: true)

## Sector-Specific Analytical Requirements

### 1. Business Cycle Positioning Requirements

**Economic Cycle Sensitivity Assessment**:
- **Current Phase Identification**: Economic cycle classification with sector-specific sensitivity scoring
- **Recession Probability Impact**: Sector vulnerability and historical recession performance patterns
- **Interest Rate Sensitivity**: Duration analysis and leverage impact across sector companies
- **Inflation Hedge Capability**: Pricing power assessment and cost pass-through ability evaluation

**GDP Growth Correlation Analysis**:
- **Sector Elasticity Measurement**: Sensitivity coefficients to GDP growth rate changes
- **Historical Performance Patterns**: Correlation with quarterly GDP releases and expansion/contraction periods
- **Leading/Lagging Relationships**: Sector timing relative to GDP cycles and predictive value
- **Economic Driver Identification**: Primary economic factors influencing sector performance

**Monetary Policy Transmission**:
- **Fed Policy Stance Impact**: Sector response to accommodative/neutral/restrictive monetary policy
- **Credit Availability Effects**: Capital access implications and refinancing risk assessment
- **Forward Guidance Impact**: Policy communication effects on sector investment flows
- **International Policy Coordination**: Cross-border monetary policy impacts on sector dynamics

### 2. Liquidity Cycle Positioning Requirements

**Credit Market Integration**:
- **Corporate Bond Access**: Sector-specific issuance conditions and credit spread analysis
- **Banking Standards Impact**: Lending criteria changes and sector capital availability
- **Refinancing Risk Assessment**: Near-term debt maturity analysis across sector companies
- **Credit Quality Distribution**: Sector credit rating profile and default risk evaluation

**Money Supply and Velocity Effects**:
- **M2 Growth Sensitivity**: Sector correlation with money supply expansion/contraction
- **Asset Price Inflation Impact**: Valuation multiple effects and sector relative performance
- **Velocity Implications**: Money circulation changes and sector demand patterns
- **Liquidity Preference Shifts**: Risk appetite changes and sector allocation flow impacts

**Employment Sensitivity Integration**:
- **Payroll Correlation**: Sector sensitivity to nonfarm payroll changes and labor market conditions
- **Consumer Spending Linkage**: Employment-to-sector demand transmission mechanisms
- **Labor Participation Impact**: Sector dependence on labor force participation rate changes
- **Initial Claims Signaling**: Early warning correlation with sector stress indicators

### 3. Industry Dynamics Scorecard Requirements

**Financial Health Assessment (A-F Grading)**:
- **Profitability Scorecard**: Sector margin sustainability, ROE quality, and operating leverage evaluation
- **Balance Sheet Strength**: Debt trends, liquidity adequacy, and financial flexibility assessment
- **Cash Flow Quality**: Generation sustainability, allocation effectiveness, and reinvestment patterns
- **Capital Efficiency**: Asset utilization, ROIC trends, and competitive advantage sustainability

**Competitive Positioning Evaluation**:
- **Competitive Moat Scoring (1-10 Scale)**: Barrier height, pricing power, and customer switching costs
- **Market Concentration Analysis**: Industry structure, market share distribution, and consolidation trends
- **Network Effects Assessment**: Scale advantages and platform economics within sector
- **Regulatory Protection Evaluation**: Policy barriers, intellectual property strength, and regulatory moats

**Innovation and Disruption Risk**:
- **Technology Disruption Vulnerability**: Sector exposure to technological change and automation risk
- **Innovation Leadership Assessment**: R&D investment effectiveness and patent portfolio strength
- **Digital Transformation Progress**: Sector adaptation to digital economy trends
- **Competitive Threat Analysis**: New entrant risks and business model evolution requirements

### 4. Multi-Method Valuation Requirements

**Comprehensive Valuation Framework**:
- **DCF Analysis Integration**: Sector-appropriate discount rates, growth assumptions, and terminal value estimation
- **Relative Comparables Assessment**: Peer multiple analysis, cross-sector valuation comparison, and premium/discount justification
- **Technical Analysis Integration**: Sector momentum, support/resistance levels, and volume profile assessment
- **Scenario-Weighted Valuation**: Bull/base/bear case probability weighting and blended fair value calculation

**ETF Analysis and Pricing**:
- **ETF Composition Analysis**: Holdings concentration, weighting methodology, and rebalancing impact
- **Premium/Discount Assessment**: ETF price vs NAV analysis and arbitrage mechanism efficiency
- **Liquidity Analysis**: Trading volume, bid-ask spreads, and market maker participation
- **Cross-ETF Correlation**: Sector ETF relationships and diversification effectiveness

**Sector Rotation Intelligence**:
- **Historical Rotation Patterns**: Economic cycle-based sector performance and transition analysis
- **Forward-Looking Probabilities**: Sector rotation likelihood and timing considerations
- **Relative Strength Assessment**: Momentum factors and sector leadership identification
- **Tactical Allocation Recommendations**: Portfolio weighting optimization and rebalancing guidance

### 5. Investment Recommendation Framework

**Portfolio Allocation Context**:
- **Sector Weighting Optimization**: Recommended allocation percentages within diversified portfolio
- **Cross-Sector Correlation**: Portfolio impact of sector allocation changes and diversification benefits
- **Risk-Adjusted Positioning**: Sector contribution to portfolio risk and return optimization
- **Economic Cycle Allocation**: Tactical sector weighting based on business cycle positioning

**Risk-Return Profile Assessment**:
- **Sector Sharpe Ratio**: Risk-adjusted return calculations with economic cycle context
- **Downside Protection Analysis**: Sector defensive characteristics and bear market resilience
- **Volatility Profile**: Sector volatility patterns and correlation with market stress indicators
- **Recovery Characteristics**: Post-crisis recovery patterns and timeline expectations

**Investment Timing Considerations**:
- **Economic Cycle Timing**: Optimal sector allocation timing based on business cycle phase
- **Policy Impact Assessment**: Fed policy changes and sector investment attractiveness
- **Seasonal Patterns**: Monthly/quarterly sector performance patterns and calendar effects
- **Mean Reversion Analysis**: Sector relative performance cycles and contrarian opportunities

## Risk Assessment Requirements

### Sector-Specific Risk Matrix

**Quantified Risk Framework (Probability × Impact)**:
- **Economic Recession Risk**: Sector vulnerability scoring with historical recession impact analysis
- **Interest Rate Shock Risk**: Duration risk and earnings impact from rate environment changes
- **Regulatory Change Risk**: Policy implementation probability and sector compliance cost assessment
- **Competitive Disruption Risk**: Technology displacement and market share loss probability
- **Currency/Trade Risk**: International exposure and trade policy impact vulnerability

**Stress Testing Requirements**:
- **Bear Market Scenarios**: -20% market decline impact modeling with sector-specific factors
- **Recession Impact Modeling**: Historical recession performance and recovery timeline analysis
- **Policy Shock Analysis**: Regulatory change impact and implementation timeline assessment
- **Recovery Scenario Planning**: Post-stress recovery patterns and duration estimation

**Early Warning System**:
- **Leading Indicator Integration**: Economic indicators with predictive value for sector stress
- **Threshold Breach Analysis**: Critical metric levels that signal sector risk escalation
- **Cross-Asset Signal Integration**: Bond, currency, and commodity signals affecting sector outlook
- **Monitoring Framework**: KPI dashboard and risk escalation protocols

## Output Structure Requirements

**File Naming**: `{SECTOR}_{YYYYMMDD}_analysis.json`
**Primary Location**: `./data/outputs/sector_analysis/analysis/`

### Required Output Sections

1. **Business Cycle Positioning**
   - Economic phase classification and sector sensitivity scoring
   - Recession probability with sector vulnerability assessment
   - Interest rate and inflation sensitivity quantification
   - GDP correlation analysis with elasticity coefficients

2. **Liquidity Cycle Assessment**
   - Fed policy stance impact and credit market analysis
   - Money supply sensitivity and employment correlation
   - Capital access conditions and refinancing risk
   - Liquidity preference implications for sector flows

3. **Industry Dynamics Scorecard**
   - A-F financial health grades with supporting evidence
   - Competitive moat scores (1-10) and barrier assessment
   - Regulatory environment rating and innovation risk evaluation
   - Market structure analysis and consolidation trends

4. **Multi-Method Valuation**
   - DCF analysis with sector-appropriate assumptions
   - Relative valuation with peer comparison and justification
   - Technical analysis integration and momentum assessment
   - Blended fair value with probability weighting

5. **Investment Recommendation Framework**
   - Portfolio allocation recommendations and sector weighting
   - Risk-adjusted metrics and economic cycle positioning
   - ETF analysis with price vs fair value assessment
   - Investment timing considerations and rotation probabilities

6. **Quantified Risk Assessment**
   - Risk matrix with evidence-backed probability × impact scoring
   - Stress testing scenarios with historical context
   - Early warning indicators and monitoring framework
   - Risk mitigation strategies and hedging recommendations

## Quality Standards and Evidence Requirements

### Sector Specificity Standards
- **Industry Expertise**: Deep sector knowledge with business model understanding
- **Economic Sensitivity**: Comprehensive cycle sensitivity and correlation analysis
- **Competitive Intelligence**: Thorough market structure and competitive dynamics assessment
- **Regulatory Context**: Current and forward-looking regulatory environment integration

### Template Gap Analysis Standards
- **Gap Coverage**: All template requirements addressed with analytical depth
- **Discovery Integration**: Complete preservation and building upon discovery intelligence
- **Synthesis Preparation**: Output structured for efficient template generation
- **Quality Metrics**: Evidence strength and analytical rigor measurement

### Evidence and Validation Requirements
- **Historical Precedent**: Sector patterns validated against historical cycles and events
- **Cross-Validation**: Multi-source data consistency and reliability verification
- **Quantitative Support**: Numerical backing for all scores, grades, and recommendations
- **Confidence Attribution**: Explicit confidence scoring for all analytical conclusions

## Implementation Notes

**Analyst Sub-Agent Integration**: This specification defines WHAT sector analysis is required. The analyst sub-agent handles HOW through:
- Template gap analysis framework execution
- Universal quality standards enforcement
- Discovery data preservation and integration
- Multi-method valuation coordination

**Key Sector Focus Areas**:
- **Economic Cycle Sensitivity**: Comprehensive business and liquidity cycle analysis
- **Industry Dynamics**: A-F grading system with competitive moat evaluation
- **Investment Integration**: Portfolio context and rotation probability analysis
- **ETF Analysis**: Composition, pricing, and tactical allocation intelligence
- **Risk Quantification**: Evidence-based probability × impact assessment

**Template Integration**: Optimized for sector_analysis_template.md synthesis with focus on filling analytical gaps not present in discovery data while building upon existing economic context and sector intelligence.

---

**Framework Integration**: Optimized for DASV analyst sub-agent execution focusing on sector-specific domain requirements and template synthesis preparation.

**Author**: Cole Morton
**Optimization**: 50% complexity reduction through template gap analysis delegation to analyst sub-agent
**Confidence**: Sector analysis domain specification with institutional-grade investment recommendations
