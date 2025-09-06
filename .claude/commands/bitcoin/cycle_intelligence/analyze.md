# Bitcoin Cycle Intelligence Analyze

**DASV Phase 2: Bitcoin-Specific Cycle Analysis Requirements**

Generate comprehensive Bitcoin cycle analysis focusing on market cycle positioning, on-chain intelligence evaluation, and institutional-grade strategic recommendations with quality standards.

## Purpose

Define the analytical requirements for transforming Bitcoin discovery data into comprehensive cycle intelligence. This specification focuses on Bitcoin cycle analysis domain requirements while delegating CLI-enhanced analytical methodology to the analyst sub-agent.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: bitcoin_cycle_intelligence
**Action**: analyze
**Input Source**: cli_enhanced_bitcoin_cycle_intelligence_discover
**Output Location**: `./{DATA_OUTPUTS}/bitcoin_cycle_intelligence/analysis/`
**Next Phase**: bitcoin_cycle_intelligence_synthesize
**Template Integration**: `./{TEMPLATES_BASE}/analysis/bitcoin_cycle_intelligence_template.md`
**Implementation Delegation**: Analyst sub-agent handles CLI-enhanced Bitcoin analysis methodology

## Analysis Parameters

### Core Requirements
- `discovery_file`: Path to Bitcoin cycle discovery JSON file (required) - format: bitcoin_cycle_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Bitcoin Cycle Analysis Features
- `cycle_indicators_dashboard`: Enable comprehensive cycle indicator analysis - `true` | `false` (optional, default: true)
- `valuation_framework`: Enable Bitcoin valuation models (MVRV, NUPL, etc.) - `true` | `false` (optional, default: true)
- `cycle_comparison_matrix`: Enable multi-cycle comparative analysis - `true` | `false` (optional, default: true)
- `network_health_assessment`: Enable mining and network security evaluation - `true` | `false` (optional, default: true)
- `risk_quantification`: Enable Bitcoin-specific risk matrices - `true` | `false` (optional, default: true)

## Bitcoin-Specific Cycle Analysis Requirements

### 1. Cycle Indicators Dashboard Requirements

**MVRV Z-Score Analysis Framework**:
- **Current Score Calculation**: MVRV Z-Score with historical cycle overlays and standard deviation bands
- **Bubble/Capitulation Zone Identification**: Analysis of current position relative to historical extremes
- **Time-weighted Trend Analysis**: Moving averages and trend identification for cycle positioning
- **Historical Accuracy Assessment**: Back-testing MVRV signals across previous Bitcoin cycles

**PI Cycle Top Indicator Evaluation**:
- **111-day MA vs 350-day MA Relationship**: Current signal strength and historical performance analysis
- **Lead Time Analysis**: Historical accuracy and advance warning capabilities for cycle tops
- **Signal Validation**: Cross-validation with other cycle indicators for confirmation
- **Cycle Integration**: Integration with broader market cycle analysis framework

**Long-Term Holder Behavior Analysis**:
- **LTH Supply Changes**: Accumulation vs distribution phases and supply dynamics
- **LTH Realized Price Analysis**: Cost basis evolution and market cycle implications
- **Age-Banded Distribution**: Coin age analysis and long-term holder conviction assessment
- **HODLer Behavior Patterns**: Historical patterns and current market cycle positioning

**Rainbow Price Model Integration**:
- **Current Band Position**: Analysis of current Bitcoin price within rainbow price bands
- **Fair Value Estimation**: Multiple model integration for Bitcoin valuation assessment
- **Historical Accuracy**: Back-testing rainbow model across Bitcoin market cycles
- **Cycle Phase Correlation**: Rainbow band correlation with cycle phase identification

### 2. Valuation Framework Requirements

**Realized Price Metrics Analysis**:
- **Market Price vs Realized Price Spread**: Current spread analysis and historical positioning
- **LTH vs STH Realized Price Divergences**: Long-term vs short-term holder cost basis analysis
- **Historical Valuation Percentiles**: Current valuation relative to historical Bitcoin price ranges
- **Realized Price Trend Analysis**: Direction and momentum of Bitcoin holder cost basis evolution

**NUPL (Net Unrealized Profit/Loss) Zone Analysis**:
- **Current Zone Classification**: Classification within Capitulation → Euphoria spectrum
- **LTH-NUPL vs STH-NUPL Behavior**: Long-term vs short-term holder profit/loss dynamics
- **Zone Transition Probabilities**: Statistical analysis of NUPL zone transitions and implications
- **Historical NUPL Accuracy**: Back-testing NUPL zones for cycle phase identification

**Reserve Risk Indicator Assessment**:
- **Price/HODL Bank Ratio Analysis**: Current ratio and historical trend assessment
- **Long-term Holder Conviction Levels**: Analysis of LTH resolve and accumulation patterns
- **Accumulation Opportunity Assessment**: Identification of strategic accumulation opportunities
- **Risk-Adjusted Entry Points**: Reserve Risk-based entry and exit strategy development

**Bitcoin Network Value Analysis**:
- **Stock-to-Flow Model Integration**: S2F model current positioning and historical accuracy
- **Metcalfe's Law Application**: Network value correlation with user growth and adoption
- **Hash Rate Value Correlation**: Network security valuation and mining economic analysis
- **Adoption-Based Valuation**: User growth, transaction volume, and network effect valuation

### 3. Cycle Comparison Matrix Requirements

**Multi-Cycle Analysis Framework**:
- **Current Cycle Progression**: Comparison vs 2011, 2017, 2021 cycles with time and price metrics
- **Time-Based Cycle Comparisons**: Duration analysis and cycle length comparison across eras
- **Price-Based Cycle Analysis**: Magnitude of moves and percentage gains across different cycles
- **Unique Characteristics Identification**: Current cycle distinctive features vs historical patterns

**Fractal Pattern Recognition**:
- **Cycle Extension/Compression Signals**: Identification of potential cycle timing variations
- **Key Milestone Targets**: Price and time-based targets from historical cycle analysis
- **Pattern Similarity Scoring**: Quantitative assessment of current vs historical cycle patterns
- **Probability-Weighted Scenario Analysis**: Statistical modeling of cycle outcome probabilities

**Hash Rate and Mining Analysis**:
- **Hash Ribbons Indicator**: 30-day vs 60-day moving averages for miner capitulation signals
- **Mining Difficulty Analysis**: Difficulty adjustments and network security assessment
- **Puell Multiple Assessment**: Mining profitability relative to historical averages
- **Miner Behavior Analysis**: On-chain miner selling/holding patterns and cycle implications

**Network Health Integration**:
- **Transaction Volume Trends**: Organic transaction growth and network utilization
- **Active Address Analysis**: Network growth metrics and adoption indicators
- **Fee Market Development**: Fee revenue trends and long-term security model assessment
- **Lightning Network Growth**: Second-layer adoption and Bitcoin scaling progress

### 4. Strategic Recommendations Requirements

**Cycle Phase Classification**:
- **Current Phase Identification**: Accumulation/Bull Market/Distribution/Bear Market classification
- **Confidence Level Assessment**: Evidence-backed confidence scoring for phase classification
- **Phase Transition Triggers**: Key indicators to monitor for cycle phase changes
- **Timeline Estimation**: Probability-weighted timeline assessment for phase transitions

**Risk/Reward Assessment**:
- **Expected Returns by Timeline**: Risk-adjusted return expectations across different time horizons
- **Downside Protection Strategies**: Risk management approaches for different cycle phases
- **Maximum Drawdown Scenarios**: Historical drawdown analysis and preparation strategies
- **Opportunity Cost Analysis**: Bitcoin allocation vs alternative investments by cycle phase

**Position Sizing Framework**:
- **Cycle-Adjusted Allocation**: Recommended Bitcoin allocation percentage by cycle phase
- **Dollar-Cost Averaging Optimization**: DCA strategy optimization based on cycle indicators
- **Rebalancing Trigger Points**: Specific on-chain metrics triggering portfolio rebalancing
- **Risk Management Integration**: Position sizing with comprehensive risk assessment

### 5. Bitcoin-Specific Risk Assessment and Quantification

**Bitcoin Market Risk Matrix (Probability × Impact)**:
- **Regulatory Risk**: Global regulatory changes, compliance requirements, and policy impact assessment
- **Technical Risk**: Network security threats, scaling challenges, and protocol upgrade risks
- **Market Structure Risk**: Exchange concentration, custody risks, and liquidity assessment
- **Adoption Risk**: Institutional adoption barriers, retail sentiment shifts, and mainstream acceptance
- **Macroeconomic Risk**: Interest rate sensitivity, inflation correlation, and economic cycle impact

**Network Security Risk Integration**:
- **Hash Rate Concentration**: Mining pool centralization and geographic concentration risks
- **51% Attack Scenarios**: Cost and probability assessment of network attack vectors
- **Mining Economics**: Miner profitability stress testing and network security implications
- **Protocol Development Risk**: Development centralization and upgrade implementation risks

**Stress Testing Requirements**:
- **Price Stress**: Extreme downside scenarios and historical drawdown analysis
- **Liquidity Stress**: Market stress impact on Bitcoin liquidity and exchange function
- **Regulatory Stress**: Adverse regulatory scenario impact on Bitcoin adoption and pricing
- **Recovery Analysis**: Post-stress recovery patterns and institutional confidence rebuilding

## Output Structure Requirements

**File Naming**: `bitcoin_cycle_{YYYYMMDD}_analysis.json`
**Primary Location**: `./{DATA_OUTPUTS}/bitcoin_cycle_intelligence/analysis/`

### Required Output Sections

1. **Cycle Indicators Dashboard**
   - MVRV Z-Score analysis with historical cycle overlays and confidence scoring
   - PI Cycle Top Indicator evaluation with signal strength assessment
   - Long-Term Holder behavior analysis with supply dynamics
   - Rainbow Price Model integration with fair value estimation

2. **Valuation Framework Assessment**
   - Realized Price metrics analysis with LTH vs STH divergences
   - NUPL zone classification with transition probabilities
   - Reserve Risk Indicator assessment with accumulation opportunity analysis
   - Bitcoin network value integration with multiple model validation

3. **Cycle Comparison Matrix Analysis**
   - Multi-cycle analysis with historical pattern comparison
   - Fractal pattern recognition with probability-weighted scenarios
   - Hash rate and mining analysis with miner capitulation signals
   - Network health integration with adoption and scaling metrics

4. **Strategic Recommendations Framework**
   - Cycle phase classification with confidence level assessment
   - Risk/reward assessment with timeline-based return expectations
   - Position sizing framework with cycle-adjusted allocation recommendations
   - Rebalancing triggers with comprehensive risk management integration

5. **Bitcoin-Specific Risk Assessment**
   - Risk matrix with evidence-backed probability × impact scoring for Bitcoin markets
   - Network security risk integration with hash rate and mining analysis
   - Stress testing scenarios with recovery pattern analysis
   - Risk mitigation strategies and Bitcoin-specific monitoring frameworks

## Quality Standards and Evidence Requirements

### Bitcoin Data Integration Standards
- **Multi-Source Validation**: CoinGecko, Mempool.space, CoinMetrics, and Glassnode data consistency
- **Service Health Monitoring**: Real-time Bitcoin data service status and quality assessment
- **Data Quality Attribution**: Source confidence scoring and cross-validation requirements
- **Fallback Protocols**: Service degradation handling and Bitcoin data reliability maintenance

### Bitcoin Analysis Standards
- **On-Chain Data Quality**: UTXO analysis accuracy, transaction validation, and blockchain consistency
- **Cycle Analysis Methodology**: Appropriate historical comparison and cycle identification
- **Historical Context**: Multi-cycle analysis and Bitcoin market evolution consideration
- **Forward-Looking Integration**: Network development, adoption trends, and institutional commentary

### Institutional-Grade Requirements
- **Analysis Confidence**: ≥9.0/10.0 baseline with Bitcoin CLI service quality integration
- **Evidence Requirement**: All cycle assessments and scores supported by quantitative on-chain analysis
- **Cross-Validation**: Multiple Bitcoin data sources and consistency verification
- **Professional Standards**: Institutional-level analytical rigor and Bitcoin-specific methodology

### Bitcoin Valuation Methodology Standards
- **Cycle Indicator Rigor**: Detailed on-chain modeling with explicit assumptions
- **Multi-Model Validation**: Cycle indicator appropriateness and historical accuracy validation
- **Scenario Analysis**: Comprehensive sensitivity and Bitcoin cycle scenario modeling
- **Fair Value Confidence**: Statistical confidence intervals and Bitcoin-specific assumption testing

## Implementation Notes

**Analyst Sub-Agent Integration**: This specification defines WHAT Bitcoin cycle intelligence analysis is required. The analyst sub-agent handles HOW through:
- CLI-enhanced Bitcoin analytical framework execution
- Universal quality standards and confidence scoring enforcement for Bitcoin data
- Discovery data preservation with multi-source Bitcoin validation
- Template synthesis preparation and Bitcoin intelligence structure optimization

**Key Bitcoin Cycle Focus Areas**:
- **Cycle Indicators**: Comprehensive MVRV, PI Cycle, NUPL analysis with evidence-backed assessment
- **Valuation Framework**: Detailed sustainability analysis and Bitcoin network value positioning
- **Cycle Comparison**: Multi-cycle approach with historical pattern weighting and sensitivity analysis
- **Risk Integration**: Comprehensive Bitcoin risk quantification with network security and regulatory stress testing
- **Strategic Recommendations**: Cycle-based positioning and institutional allocation guidance

**Bitcoin CLI Service Dependencies**: Optimized for multi-source Bitcoin data integration with real-time service health monitoring and quality attribution through analyst sub-agent orchestration.

---

**Framework Integration**: Optimized for DASV analyst sub-agent execution focusing on Bitcoin cycle intelligence domain expertise and institutional-grade Bitcoin research standards.

**Author**: Cole Morton
**Optimization**: 45% complexity reduction through CLI methodology delegation to analyst sub-agent
**Confidence**: Bitcoin cycle intelligence domain specification with institutional-grade research quality
