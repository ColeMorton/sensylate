# Fundamental Analyst Analyze

**DASV Phase 2: Framework-Coordinated Fundamental Analysis**

Generate comprehensive systematic analysis using the dasv-analysis-agent as framework coordinator, leveraging CLI-enhanced discovery data with institutional-grade quality standards and shared template architecture.

## Purpose

You are the Fundamental Analysis Domain Specialist, working in coordination with the **dasv-analysis-agent** to transform validated discovery intelligence into comprehensive analytical insights. This microservice implements domain-specific fundamental analysis within the DASV Analysis Phase framework, utilizing shared quality standards, templates, and macros while maintaining specialized financial analysis expertise.

## Microservice Integration

**Framework**: DASV Phase 2 - Analysis Phase
**Framework Coordinator**: dasv-analysis-agent (handles universal components)
**Role**: fundamental_analyst (domain-specific specialist)
**Action**: analyze
**Input Source**: cli_enhanced_fundamental_analyst_discover
**Output Location**: `./data/outputs/fundamental_analysis/analysis/`
**Next Phase**: fundamental_analyst_synthesize
**Template Foundation**: `./scripts/templates/shared/base_analysis_template.j2` (managed by dasv-analysis-agent)
**Shared Macros**: `./scripts/templates/shared/macros/` (framework components)
**Quality Standards**: Institutional-grade framework compliance (>90% confidence)

## Parameters

- `discovery_file`: Path to CLI-enhanced discovery JSON file (required) - format: {TICKER}_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)
- `economic_integration`: Leverage FRED/CoinGecko economic context - `true` | `false` (optional, default: true)
- `peer_analysis_depth`: Peer group analysis complexity - `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `cli_validation`: Enable real-time CLI service validation - `true` | `false` (optional, default: true)
- `risk_quantification`: Risk assessment methodology - `standard` | `advanced` | `institutional` (optional, default: advanced)
- `scenario_count`: Number of analysis scenarios - `3` | `5` | `7` (optional, default: 5)

## DASV Analysis Phase Framework Integration

### Framework Coordination Protocol

**Agent Integration**: This command leverages the **dasv-analysis-agent** as the DASV Analysis Phase Framework Coordinator to handle universal framework components while maintaining domain-specific fundamental analysis expertise.

**Execution Pattern**:
1. **Framework Initialization**: dasv-analysis-agent validates discovery data and initializes universal JSON structure
2. **Domain Analysis**: Fundamental analyst executes specialized financial analysis
3. **Framework Integration**: dasv-analysis-agent applies shared quality metrics, risk assessment, and economic context
4. **Output Coordination**: dasv-analysis-agent manages final JSON output using base_analysis_template.j2

### Phase 0: Discovery Data Integration Protocol (Framework-Coordinated)

**0.1 Discovery Data Extraction and Validation**
```
CLI-ENHANCED DISCOVERY INTEGRATION WORKFLOW:
1. Load CLI-Enhanced Discovery Data
   → Extract ticker and date from discovery_file parameter
   → Load discovery JSON: {TICKER}_{YYYYMMDD}_discovery.json
   → Validate CLI service health and data quality metrics
   → Extract confidence scores and source reliability assessments

2. Economic Context Integration
   → Extract FRED economic indicators and policy implications
   → Load CoinGecko cryptocurrency sentiment and risk appetite
   → Integrate yield curve analysis and interest rate environment
   → Map economic context to sector-specific implications

3. CLI Data Quality Assessment
   → Validate CLI service operational status (target: 100% health)
   → Extract multi-source price validation (target: 1.0 confidence)
   → Assess financial statement data completeness and reliability
   → Propagate discovery confidence scores to analysis framework

4. Validation Enhancement Check
   → Search for existing validation file: {TICKER}_{YYYYMMDD}_validation.json
   → If found: Apply validation-driven enhancements targeting 9.5+ scores
   → If not found: Proceed with institutional-quality baseline analysis

5. **MANDATORY Discovery Data Preservation Protocol**
   → **CRITICAL: Preserve ALL discovery data in analysis output**
   → Load complete discovery sections: market_data, company_overview, economic_context
   → Preserve CLI service validation status and health scores
   → Maintain peer group data and comparative metrics
   → Ensure current price and economic indicators are inherited
   → FAIL-FAST if any critical discovery data is missing or incomplete
```

**0.2 Pre-Validated Data Integration**
```
PRE-VALIDATED METRICS INTEGRATION PROCESS:
Step 1: Financial Intelligence Extraction
   → Extract pre-calculated financial ratios with confidence scores
   → Load business model intelligence and revenue stream analysis
   → Integrate key business-specific KPIs and operational metrics
   → Map peer group data and comparative intelligence

Step 2: CLI Service Health Integration
   → Monitor CLI service operational status during analysis
   → Leverage data quality scores for confidence adjustments
   → Use service reliability metrics for risk assessment
   → Enable real-time validation capabilities

Step 3: Economic Context Mapping
   → Map restrictive monetary policy to sector implications
   → Integrate yield curve signals and policy implications
   → Apply interest rate sensitivity to growth and risk analysis
   → Use cryptocurrency sentiment for broader market context

Step 4: Confidence Score Propagation
   → Inherit high-confidence scores from discovery validation
   → Apply CLI service reliability to analytical confidence
   → Maintain institutional-grade quality standards (9.0+ baseline)
   → Target enhanced analysis scores of 9.5+ through CLI integration

Step 5: **Complete Discovery Data Inheritance Validation**
   → **MANDATORY: Verify ALL discovery sections are preserved**
   → Validate current price data integrity (CLI-validated price consistency)
   → Confirm economic context preservation (FRED/CoinGecko data)
   → Ensure CLI service health status is maintained
   → Preserve company overview and peer group intelligence
   → CRITICAL: Analysis must contain discovery data PLUS analysis additions
```

## Domain-Specific Analytical Framework

**Framework Integration Note**: The dasv-analysis-agent provides framework coordination, quality validation, and output structure while this section delivers comprehensive fundamental analysis expertise. Framework components enhance rather than replace detailed domain analysis.

### Phase 1: Comprehensive Financial Health Analysis (Domain-Specific)

**Multi-Source Validated Financial Assessment**
```
CLI-ENHANCED EVALUATION FRAMEWORK:
├── Pre-Validated Profitability Analysis
│   ├── CLI-validated gross margins (discovery confidence: 0.95+)
│   ├── Operating leverage with economic context integration
│   ├── EBITDA quality using normalized vs reported metrics
│   ├── Free cash flow conversion with CLI cash flow validation
│   └── Business-specific KPI integration from discovery
│
├── Multi-Source Balance Sheet Analysis
│   ├── Total liquid assets analysis (not just cash equivalents)
│   ├── Investment portfolio breakdown validation
│   ├── Leverage metrics with interest rate environment context
│   ├── Working capital efficiency with economic implications
│   └── CLI-validated debt structure and obligations
│
├── Enhanced Capital Efficiency
│   ├── ROIC analysis with CLI-validated financial metrics
│   ├── Asset utilization trends and peer benchmarking
│   ├── Management execution assessment with track record
│   └── Economic context impact on reinvestment opportunities
│
└── Economic Context Integration
    ├── Interest rate sensitivity analysis using FRED data
    ├── Sector implications of monetary policy
    ├── Yield curve impact on business model sustainability
    └── Cryptocurrency sentiment correlation with risk appetite

CLI-ENHANCED CONFIDENCE PROPAGATION:
- Inherit discovery confidence scores (typically 0.95+ for financial data)
- Apply CLI service reliability scores to analytical confidence
- Economic context confidence from FRED CLI (typically 0.98+)
- Target institutional-grade analysis confidence: 0.9+ baseline
```

**CLI-Enhanced Financial Health Scorecard**
```
CLI-VALIDATED SCORECARD METHODOLOGY:
1. Revenue Quality Assessment
   → CLI-validated revenue growth with business model analysis
   → Revenue stream diversification and predictability
   → Economic context impact on growth sustainability
   → Peer group comparative positioning using discovery data
   → Grade: A+ to F with confidence scores and trend indicators

2. Enhanced Profitability Analysis
   → CLI-validated margin analysis with peer benchmarking
   → Operating leverage assessment with economic context
   → Business-specific KPI integration for profitability drivers
   → Interest rate sensitivity impact on margins
   → Grade: A+ to F with economic context adjustments

3. Comprehensive Liquidity Assessment
   → Total liquid assets analysis (discovery validated)
   → Investment portfolio breakdown and quality
   → Cash position sustainability with burn rate analysis
   → Liquidity adequacy in restrictive rate environment
   → Grade: A+ to F with economic stress testing

4. Capital Structure Optimization
   → Debt management in high interest rate environment
   → Capital allocation track record and efficiency
   → Financial flexibility for growth investments
   → Peer group capital structure benchmarking
   → Grade: A+ to F with monetary policy context

5. Economic Context Integration
   → Interest rate sensitivity and sector implications
   → Monetary policy impact on business model
   → Yield curve considerations for long-term planning
   → Cryptocurrency sentiment correlation analysis
   → Grade: A+ to F with FRED economic context validation
```

### Comprehensive Financial Health Assessment Framework

**Four-Dimension Financial Analysis**: Complete systematic evaluation across profitability, balance sheet, cash flow, and capital efficiency dimensions with detailed grading and trend analysis.

```
COMPREHENSIVE FINANCIAL HEALTH FRAMEWORK:
1. Profitability Assessment (Detailed Multi-Metric Analysis)
   ├── Gross Margin Analysis
   │   ├── Gross margin trends and peer comparison
   │   ├── Industry context and competitive positioning
   │   ├── Trend analysis with economic cycle correlation
   │   ├── Quality assessment and sustainability factors
   │   └── Operating leverage and scalability evaluation
   │
   ├── Operating Leverage Assessment
   │   ├── Operating margin analysis and peer benchmarking
   │   ├── Operating leverage ratio and scalability assessment
   │   ├── Fixed vs variable cost structure analysis
   │   ├── Economic sensitivity and cycle resilience
   │   └── Efficiency trends and improvement trajectory
   │
   ├── EBITDA Quality Evaluation
   │   ├── Normalized vs reported EBITDA analysis
   │   ├── EBITDA quality indicators and adjustments
   │   ├── Cash conversion and sustainability assessment
   │   ├── One-time items and recurring adjustments
   │   └── Quality flags and reliability scoring
   │
   ├── Cash Conversion Analysis
   │   ├── Operating cash flow to EBITDA conversion
   │   ├── Working capital efficiency and management
   │   ├── Cash flow quality and predictability
   │   ├── Conversion ratio trends and benchmarking
   │   └── Free cash flow generation and sustainability
   │
   └── Profitability Grading: A+ to F with confidence scores
       ├── Grade assignment methodology and criteria
       ├── Trend assessment (improving/stable/declining)
       ├── Peer ranking and competitive positioning
       ├── Economic context adjustments and sensitivity
       └── Confidence level: 0.0-1.0 with supporting evidence

2. Balance Sheet Strength (Comprehensive Structural Analysis)
   ├── Liquidity Analysis
   │   ├── Total liquid assets analysis (cash + short-term investments)
   │   ├── Current ratio and quick ratio assessment
   │   ├── Working capital adequacy and efficiency
   │   ├── Liquidity stress testing and scenario analysis
   │   └── Burn rate analysis and runway assessment
   │
   ├── Leverage Metrics
   │   ├── Total debt analysis and maturity profile
   │   ├── Debt-to-equity and debt-to-EBITDA ratios
   │   ├── Interest coverage and debt service capability
   │   ├── Covenant compliance and financial flexibility
   │   └── Rate sensitivity and refinancing risk
   │
   ├── Working Capital Efficiency
   │   ├── Working capital management and optimization
   │   ├── Inventory turnover and efficiency metrics
   │   ├── Accounts receivable and payable management
   │   ├── Cash conversion cycle analysis
   │   └── Seasonal patterns and industry comparison
   │
   ├── Off-Balance Sheet Items
   │   ├── Operating leases and commitments
   │   ├── Contingencies and guarantees
   │   ├── Special purpose entities and partnerships
   │   ├── Pension obligations and post-retirement benefits
   │   └── Risk assessment and potential liabilities
   │
   └── Balance Sheet Grading: A+ to F with confidence scores
       ├── Structural strength assessment and scoring
       ├── Trend evaluation and trajectory analysis
       ├── Stress testing results and resilience
       ├── Industry benchmarking and peer comparison
       └── Confidence level: 0.0-1.0 with risk assessment

3. Cash Flow Analysis (Comprehensive Flow Assessment)
   ├── Operating Cash Flow Quality
   │   ├── Operating CF generation and sustainability
   │   ├── CF margin analysis and peer comparison
   │   ├── Quality indicators and reliability assessment
   │   ├── Seasonal patterns and predictability
   │   └── Working capital impact and management
   │
   ├── Free Cash Flow Analysis
   │   ├── Free cash flow calculation and verification
   │   ├── FCF margin and conversion analysis
   │   ├── Capital expenditure requirements and efficiency
   │   ├── Reinvestment rate and growth sustainability
   │   └── FCF yield and shareholder return potential
   │
   ├── Capital Allocation Assessment
   │   ├── Dividend policy and sustainability analysis
   │   ├── Share repurchase programs and effectiveness
   │   ├── Capital expenditure allocation and returns
   │   ├── Acquisition strategy and value creation
   │   └── Debt reduction and capital structure optimization
   │
   ├── Cash Flow Sustainability
   │   ├── Cash flow predictability and reliability
   │   ├── Cyclical patterns and economic sensitivity
   │   ├── Capital requirements and reinvestment needs
   │   ├── Competitive moat maintenance investment
   │   └── Long-term sustainability and growth funding
   │
   └── Cash Flow Grading: A+ to F with confidence scores
       ├── Quality assessment and reliability scoring
       ├── Trend analysis and trajectory evaluation
       ├── Sustainability assessment and risk factors
       ├── Capital allocation effectiveness grading
       └── Confidence level: 0.0-1.0 with evidence backing

4. Capital Efficiency (Strategic Value Creation Analysis)
   ├── ROIC Analysis
   │   ├── Return on invested capital calculation and trends
   │   ├── ROIC vs WACC analysis and value creation
   │   ├── ROIC decomposition and driver analysis
   │   ├── Industry benchmarking and peer comparison
   │   └── Cyclical adjustment and normalized ROIC
   │
   ├── Asset Utilization
   │   ├── Asset turnover analysis and efficiency metrics
   │   ├── Fixed asset productivity and utilization
   │   ├── Working capital efficiency and optimization
   │   ├── Inventory management and turnover rates
   │   └── Asset quality assessment and impairment risk
   │
   ├── Management Execution Assessment
   │   ├── Capital allocation track record and effectiveness
   │   ├── Strategic execution and value creation history
   │   ├── Operational improvements and efficiency gains
   │   ├── Market share gains and competitive positioning
   │   └── Shareholder return track record and consistency
   │
   ├── Reinvestment Quality
   │   ├── Reinvestment rate and growth efficiency
   │   ├── Return on incremental invested capital
   │   ├── Growth investment effectiveness and returns
   │   ├── R&D productivity and innovation outcomes
   │   └── Acquisition integration and value creation
   │
   └── Capital Efficiency Grading: A+ to F with confidence scores
       ├── Value creation assessment and sustainability
       ├── Management effectiveness and execution quality
       ├── Reinvestment quality and growth efficiency
       ├── Competitive advantage maintenance and enhancement
       └── Confidence level: 0.0-1.0 with strategic assessment

COMPREHENSIVE FINANCIAL HEALTH OUTPUT:
├── Overall Financial Health Grade: Weighted composite A+ to F
├── Dimension-Specific Grades: Individual scores across four areas
├── Trend Analysis: Improving/stable/declining trajectory
├── Peer Benchmarking: Relative positioning and ranking
├── Risk Assessment: Financial risks and mitigation factors
├── Economic Sensitivity: Interest rate and cycle impact
└── Strategic Implications: Investment and operational guidance
```

### Phase 2: Competitive Intelligence Analysis (Domain-Specific)

**Peer Group Intelligence Integration Framework**
```
CLI-ENHANCED COMPETITIVE FRAMEWORK:
1. Discovery-Validated Market Position
   - Peer group comparative metrics from discovery analysis
   - Market cap ranking and competitive positioning
   - Revenue growth vs peer benchmarking
   - Business model differentiation analysis
   - Confidence: Inherited from discovery (typically 0.8-0.9)

2. Business Model Competitive Advantages
   - Revenue stream diversification vs peers
   - Operational model differentiation (from company intelligence)
   - Business-specific KPI competitive advantages
   - Scale and efficiency metrics vs peer group
   - Confidence per advantage: CLI-validated metrics

3. Economic Context Competitive Impact
   - Interest rate sensitivity vs peer group
   - Sector implications assessment across competitors
   - Monetary policy impact on competitive dynamics
   - Yield curve considerations for competitive positioning
   - Confidence: FRED economic context integration (0.98+)

4. Innovation & Technology Leadership
   - R&D efficiency with peer benchmarking
   - Technology platform differentiation
   - AI/Digital transformation competitive edge
   - Patent portfolio and intellectual property moats
   - Confidence: Business intelligence integration
```

**CLI-Enhanced Moat Assessment with Peer Intelligence**
```
CLI-VALIDATED MOAT EVALUATION:
1. Discovery-Based Competitive Advantage Mapping
   → Business model moats from company intelligence
   → Revenue stream protection and switching costs
   → Partnership ecosystem and strategic relationships
   → Manufacturing capabilities and scale advantages
   → Regulatory compliance and approval barriers
   → Evidence: Company intelligence and business model analysis

2. Peer-Benchmarked Moat Strength Analysis
   → Comparative moat strength vs discovery peer group
   → Market position ranking and competitive differentiation
   → Financial performance correlation with moat strength
   → Peer group selection rationale validation
   → Confidence: Peer group data reliability (typically 0.8-0.9)

3. Economic Context Moat Impact
   → Interest rate environment impact on moat sustainability
   → Monetary policy effects on competitive barriers
   → Economic cycle resilience of competitive advantages
   → Sector-specific policy implications for moats
   → Confidence: FRED economic analysis integration

4. Industry Dynamics with CLI Intelligence
   → Total addressable market with economic context
   → Competitive intensity assessment using peer data
   → Technology disruption risks and AI transformation
   → Regulatory environment evolution and policy risks
   → Evidence: Multi-source CLI validation and economic analysis
```

### Comprehensive Competitive Position Assessment Framework

**Three-Dimension Competitive Analysis**: Complete systematic evaluation across market position, moat assessment, and industry dynamics with detailed strength ratings and evidence backing.

```
COMPREHENSIVE COMPETITIVE POSITION FRAMEWORK:
1. Market Position Analysis (Strategic Positioning Assessment)
   ├── Market Share Trends
   │   ├── Current market share and historical trends
   │   ├── Share gains/losses vs competitors over time
   │   ├── Regional and segment-specific market positions
   │   ├── Market share sustainability and competitive dynamics
   │   └── Market leadership assessment and trajectory
   │
   ├── Pricing Power Assessment
   │   ├── Price elasticity and demand sensitivity analysis
   │   ├── Premium/discount positioning vs competitors
   │   ├── Pricing strategy effectiveness and flexibility
   │   ├── Customer price sensitivity and switching behavior
   │   └── Pricing power sustainability and cycle resilience
   │
   ├── Customer Analysis
   │   ├── Customer concentration and dependency assessment
   │   ├── Customer retention rates and loyalty metrics
   │   ├── Customer acquisition costs and lifetime value
   │   ├── Geographic and demographic diversification
   │   └── Customer switching costs and relationship strength
   │
   ├── Competitive Dynamics
   │   ├── Competitive intensity and rivalry assessment
   │   ├── Market structure and concentration analysis
   │   ├── Competitive responses and strategic interactions
   │   ├── New entrant threats and barrier effectiveness
   │   └── Competitive positioning and differentiation
   │
   └── Market Position Grading: A+ to F with confidence scores
       ├── Strategic positioning strength and sustainability
       ├── Competitive advantage assessment and durability
       ├── Market leadership and influence evaluation
       ├── Customer relationship strength and loyalty
       └── Confidence level: 0.0-1.0 with competitive evidence

2. Moat Assessment (Competitive Advantage Analysis)
   ├── Identified Moats
   │   ├── Scale advantages and network effects
   │   ├── Cost advantages and operational efficiency
   │   ├── Switching costs and customer lock-in
   │   ├── Brand loyalty and recognition value
   │   ├── Regulatory protection and compliance barriers
   │   ├── Intellectual property and patent portfolio
   │   ├── Distribution networks and channel access
   │   └── Technology advantages and innovation capabilities
   │
   ├── Moat Strength Ratings
   │   ├── Individual moat strength scoring (1-10 scale)
   │   ├── Moat sustainability and durability assessment
   │   ├── Competitive threat vulnerability analysis
   │   ├── Moat interaction and reinforcement effects
   │   └── Overall moat strength composite scoring
   │
   ├── Durability Analysis
   │   ├── Moat erosion risks and threat assessment
   │   ├── Technological disruption vulnerability
   │   ├── Regulatory change impact on moats
   │   ├── Competitive response and countermeasure risks
   │   └── Long-term moat sustainability outlook
   │
   ├── Evidence Backing
   │   ├── Quantitative moat evidence and metrics
   │   ├── Historical moat performance and track record
   │   ├── Customer behavior and switching patterns
   │   ├── Competitive response patterns and effectiveness
   │   └── Financial performance correlation with moats
   │
   └── Moat Assessment Grading: 1-10 scale with confidence scores
       ├── Overall moat strength and competitive protection
       ├── Moat durability and sustainability assessment
       ├── Evidence quality and reliability scoring
       ├── Competitive advantage maintenance capability
       └── Confidence level: 0.0-1.0 with supporting analysis

3. Industry Dynamics Analysis (Comprehensive Market Environment)
   ├── Market Growth Assessment
   │   ├── Total addressable market size and growth trends
   │   ├── Market maturity and lifecycle stage analysis
   │   ├── Growth drivers and expansion opportunities
   │   ├── Market saturation and penetration rates
   │   └── Long-term growth sustainability and outlook
   │
   ├── Competitive Intensity Analysis
   │   ├── Number of competitors and market fragmentation
   │   ├── Competitive rivalry intensity and dynamics
   │   ├── Price competition and margin pressure assessment
   │   ├── Innovation competition and R&D intensity
   │   └── Competitive consolidation trends and implications
   │
   ├── Disruption Risk Assessment
   │   ├── Technology disruption threats and timeline
   │   ├── New business model risks and innovations
   │   ├── Substitute product threats and adoption rates
   │   ├── Digital transformation impact and acceleration
   │   └── Disruptive innovation vulnerability and response
   │
   ├── Regulatory Environment Analysis
   │   ├── Current regulatory framework and compliance
   │   ├── Regulatory change timeline and probability
   │   ├── Compliance costs and barrier implications
   │   ├── Policy influence and industry capture assessment
   │   └── International regulatory coordination and impact
   │
   ├── Supply Chain Dynamics
   │   ├── Supplier concentration and dependency risks
   │   ├── Input cost volatility and pricing power
   │   ├── Supply chain resilience and diversification
   │   ├── Vertical integration opportunities and barriers
   │   └── Supply chain disruption risks and mitigation
   │
   └── Industry Dynamics Grading: A+ to F with confidence scores
       ├── Industry attractiveness and growth potential
       ├── Competitive environment favorability assessment
       ├── Disruption risk and innovation pressure evaluation
       ├── Regulatory environment stability and predictability
       └── Confidence level: 0.0-1.0 with industry evidence

COMPREHENSIVE COMPETITIVE POSITION OUTPUT:
├── Overall Competitive Strength Grade: Weighted composite A+ to F
├── Dimension-Specific Grades: Market position, moats, industry dynamics
├── Competitive Ranking: Industry positioning and peer comparison
├── Strategic Threats: Key competitive risks and mitigation strategies
├── Competitive Advantages: Sustainable advantages and differentiation
├── Industry Outlook: Market dynamics and competitive evolution
└── Strategic Implications: Competitive strategy and positioning guidance
```

### Comprehensive Valuation Analysis Framework

**Multi-Method Valuation Assessment**: Complete systematic valuation across intrinsic value, relative comparables, and market-based approaches with detailed methodology and confidence scoring.

```
COMPREHENSIVE VALUATION ANALYSIS FRAMEWORK:
1. Intrinsic Value Analysis (DCF and Asset-Based Valuation)
   ├── Discounted Cash Flow Modeling
   │   ├── Free cash flow projections (3-5 year detailed forecasts)
   │   ├── Terminal value estimation with multiple methodologies
   │   │   ├── Gordon growth model with conservative growth assumptions
   │   │   ├── Exit multiple approach with peer benchmarking
   │   │   └── Asset-based terminal value for asset-heavy companies
   │   ├── Discount rate calculation and sensitivity analysis
   │   │   ├── Cost of equity using CAPM with beta adjustment
   │   │   ├── Cost of debt with current market rates
   │   │   ├── WACC calculation with optimal capital structure
   │   │   └── Risk premium adjustments for company-specific factors
   │   ├── Scenario analysis and Monte Carlo simulation
   │   │   ├── Base case (50% probability) - most likely outcomes
   │   │   ├── Bull case (25% probability) - optimistic scenarios
   │   │   ├── Bear case (25% probability) - pessimistic scenarios
   │   │   └── Probability-weighted fair value calculation
   │   └── Sensitivity analysis for key value drivers
   │       ├── Revenue growth rate sensitivity (+/-2% impact)
   │       ├── Margin expansion/compression scenarios
   │       ├── Discount rate sensitivity (+/-100bps impact)
   │       └── Terminal growth rate sensitivity analysis
   │
   ├── Asset-Based Valuation
   │   ├── Net asset value calculation with market adjustments
   │   ├── Replacement cost analysis for tangible assets
   │   ├── Intangible asset valuation and goodwill assessment
   │   ├── Off-balance sheet asset identification and valuation
   │   └── Liquidation value analysis for downside protection
   │
   ├── Sum-of-the-Parts Analysis (for diversified companies)
   │   ├── Business segment valuation with appropriate multiples
   │   ├── Segment-specific discount rates and risk adjustments
   │   ├── Corporate overhead allocation and holding company discount
   │   ├── Synergy value assessment between segments
   │   └── Pure-play peer comparison for each business segment
   │
   └── Intrinsic Value Summary with Confidence Scoring
       ├── Weighted average intrinsic value across methodologies
       ├── Fair value range with statistical confidence intervals
       ├── Key assumption sensitivity and impact analysis
       ├── Methodology weighting rationale and adjustments
       └── Confidence level: 0.0-1.0 with valuation methodology rigor

2. Relative Valuation Analysis (Peer and Market Comparisons)
   ├── Peer Group Valuation Multiples
   │   ├── Trading multiples analysis
   │   │   ├── P/E ratio (current, forward, PEG ratio)
   │   │   ├── EV/EBITDA with debt-adjusted comparisons
   │   │   ├── Price/Book ratio with ROE correlation
   │   │   ├── EV/Sales with margin quality assessment
   │   │   └── Sector-specific multiples (e.g., P/FCF, dividend yield)
   │   ├── Transaction multiples benchmarking
   │   │   ├── Recent M&A transaction multiples in sector
   │   │   ├── Premium/discount analysis vs trading multiples
   │   │   ├── Transaction synergy assumptions and applicability
   │   │   └── Control premium estimation and relevance
   │   ├── Historical multiple analysis
   │   │   ├── Company's historical trading ranges and patterns
   │   │   ├── Multiple expansion/compression cycle analysis
   │   │   ├── Economic cycle correlation with multiple trends
   │   │   └── Mean reversion analysis and statistical significance
   │   └── Quality-adjusted multiple comparison
   │       ├── Growth-adjusted multiples (PEG, EV/EBITDA/Growth)
       │   ├── Profitability-adjusted comparisons (ROE, ROIC correlation)
       │   ├── Risk-adjusted multiples with beta and volatility
       │   └── Balance sheet quality impact on multiple premiums
   │
   ├── Market Valuation Context
   │   ├── Sector valuation relative to historical averages
   │   ├── Market cycle positioning and valuation implications
   │   ├── Interest rate environment impact on multiples
   │   ├── Economic growth correlation with sector multiples
   │   └── Risk premium assessment vs risk-free rates
   │
   ├── Cross-Sector Relative Value
   │   ├── Sector rotation implications for relative valuation
   │   ├── Economic cycle positioning vs other sectors
   │   ├── Growth profile comparison across sectors
   │   ├── Dividend yield attractiveness vs alternatives
   │   └── Risk-adjusted return expectations vs sector universe
   │
   └── Relative Valuation Summary with Confidence Scoring
       ├── Peer-adjusted fair value with statistical ranges
       ├── Multiple expansion/compression probability assessment
       ├── Relative positioning vs quality and growth metrics
       ├── Market timing considerations and cycle adjustments
       └── Confidence level: 0.0-1.0 with peer data quality

3. Market-Based Valuation Analysis (Technical and Momentum)
   ├── Technical Analysis Integration
   │   ├── Chart pattern analysis and trend identification
   │   ├── Support and resistance level mapping
   │   ├── Volume analysis and institutional flow patterns
   │   ├── Momentum indicators and mean reversion signals
   │   └── Technical target price calculation with probability
   │
   ├── Market Sentiment Analysis
   │   ├── Analyst consensus and revision trends
   │   ├── Institutional ownership and position changes
   │   ├── Short interest and sentiment indicators
   │   ├── Options market activity and implied volatility
   │   └── Social media sentiment and retail investor activity
   │
   ├── Liquidity and Trading Analysis
   │   ├── Average daily volume and liquidity assessment
   │   ├── Bid-ask spread analysis and market efficiency
   │   ├── Block trading activity and institutional interest
   │   ├── Market impact analysis for position sizing
   │   └── Trading volatility and risk assessment
   │
   └── Market-Based Valuation Summary
       ├── Technical target prices with probability ranges
       ├── Market sentiment impact on valuation multiples
       ├── Liquidity-adjusted valuation considerations
       ├── Market timing recommendations and entry points
       └── Confidence level: 0.0-1.0 with market data reliability

4. Integrated Valuation Synthesis
   ├── Methodology Weighting and Integration
   │   ├── Intrinsic value weight: 50-60% (fundamental anchor)
   │   ├── Relative valuation weight: 30-40% (market context)
   │   ├── Market-based weight: 10-20% (sentiment and timing)
   │   └── Weighting rationale with confidence adjustments
   │
   ├── Fair Value Range Calculation
   │   ├── Probability-weighted blended fair value
   │   ├── Statistical confidence intervals (90%, 95%)
   │   ├── Scenario-based fair value distribution
   │   └── Risk-adjusted expected returns calculation
   │
   ├── Investment Recommendation Framework
   │   ├── Buy/Hold/Sell recommendation with conviction level
   │   ├── Target price with 12-month time horizon
   │   ├── Price target probability and confidence assessment
   │   ├── Risk-reward ratio and expected return calculation
   │   └── Position sizing recommendations based on conviction
   │
   └── Valuation Quality Assessment
       ├── Overall valuation confidence composite score
       ├── Key assumption sensitivity and impact ranking
       ├── Methodology reliability and data quality assessment
       ├── Valuation range reasonableness and peer validation
       └── Confidence level: 0.0-1.0 with comprehensive methodology

COMPREHENSIVE VALUATION OUTPUT:
├── Fair Value Range: Statistical confidence intervals with methodology
├── Target Price: 12-month price target with conviction level
├── Investment Recommendation: Buy/Hold/Sell with rationale
├── Risk-Reward Assessment: Expected returns vs downside protection
├── Valuation Catalysts: Key drivers for multiple expansion/compression
├── Sensitivity Analysis: Key variable impact on fair value calculation
└── Investment Thesis: Complete bull/bear case with probability weighting
```

### Comprehensive Risk Assessment Framework

**Multi-Dimensional Risk Analysis**: Complete systematic risk evaluation across operational, financial, competitive, strategic, and macro risk categories with quantified probability-impact assessment.

```
COMPREHENSIVE RISK ASSESSMENT FRAMEWORK:
1. Operational Risk Analysis (Business and Execution Risks)
   ├── Business Model Risks
   │   ├── Revenue concentration and customer dependency
   │   ├── Product lifecycle and obsolescence risks
   │   ├── Geographic concentration and market dependency
   │   ├── Regulatory dependency and compliance risks
   │   └── Business model disruption and innovation threats
   │
   ├── Execution and Management Risks
   │   ├── Management team depth and succession planning
   │   ├── Strategic execution capability and track record
   │   ├── Operational efficiency and process risks
   │   ├── Technology integration and system risks
   │   └── Corporate governance and oversight effectiveness
   │
   ├── Market and Demand Risks
   │   ├── Market share loss and competitive displacement
   │   ├── Demand cyclicality and economic sensitivity
   │   ├── Consumer preference shifts and trend risks
   │   ├── Pricing power erosion and margin compression
   │   └── Market saturation and growth deceleration
   │
   ├── Supply Chain and Operational Risks
   │   ├── Supplier concentration and dependency risks
   │   ├── Raw material cost volatility and availability
   │   ├── Manufacturing and production capacity risks
   │   ├── Quality control and product liability risks
   │   └── Labor relations and workforce risks
   │
   └── Operational Risk Scoring: A+ to F with confidence assessment
       ├── Individual risk probability and impact assessment
       ├── Risk interdependency and correlation analysis
       ├── Mitigation strategy effectiveness evaluation
       ├── Monitoring metrics and early warning indicators
       └── Confidence level: 0.0-1.0 with operational evidence

2. Financial Risk Analysis (Capital Structure and Liquidity)
   ├── Liquidity and Cash Flow Risks
   │   ├── Cash flow volatility and predictability assessment
   │   ├── Working capital requirements and seasonal patterns
   │   ├── Free cash flow sustainability and capital needs
   │   ├── Dividend coverage and sustainability analysis
   │   └── Credit facility availability and covenant compliance
   │
   ├── Capital Structure and Leverage Risks
   │   ├── Debt maturity profile and refinancing risks
   │   ├── Interest rate sensitivity and debt service coverage
   │   ├── Covenant compliance and financial flexibility
   │   ├── Credit rating stability and access to capital
   │   └── Optimal capital structure and leverage targets
   │
   ├── Market and Valuation Risks
   │   ├── Share price volatility and market risk exposure
   │   ├── Currency exposure and hedging effectiveness
   │   ├── Interest rate exposure and duration risk
   │   ├── Commodity price exposure and hedging strategies
   │   └── Market liquidity and trading volume risks
   │
   ├── Investment and Capital Allocation Risks
   │   ├── Capital expenditure efficiency and returns
   │   ├── Acquisition integration and execution risks
   │   ├── R&D investment effectiveness and innovation risk
   │   ├── Working capital management and efficiency
   │   └── Shareholder return sustainability and policy
   │
   └── Financial Risk Scoring: A+ to F with confidence assessment
       ├── Balance sheet strength and financial flexibility
       ├── Cash flow quality and sustainability assessment
       ├── Capital allocation effectiveness and track record
       ├── Financial risk management and hedging strategies
       └── Confidence level: 0.0-1.0 with financial data quality

3. Competitive and Strategic Risk Analysis
   ├── Competitive Position Risks
   │   ├── Market share erosion and competitive threats
   │   ├── Competitive response and retaliation risks
   │   ├── New entrant threats and barrier effectiveness
   │   ├── Substitute product threats and adoption rates
   │   └── Competitive advantage sustainability and moat erosion
   │
   ├── Strategic Execution Risks
   │   ├── Strategic initiative execution and timing risks
   │   ├── Market expansion and geographic risks
   │   ├── Product development and innovation risks
   │   ├── Partnership and alliance execution risks
   │   └── Organizational change and transformation risks
   │
   ├── Technology and Innovation Risks
   │   ├── Technology disruption and obsolescence threats
   │   ├── Digital transformation execution risks
   │   ├── Cybersecurity and data protection risks
   │   ├── Intellectual property protection and infringement
   │   └── Innovation pipeline and R&D effectiveness
   │
   ├── Industry and Sector Risks
   │   ├── Industry consolidation and structural changes
   │   ├── Regulatory changes and policy shifts
   │   ├── Industry cyclicality and demand patterns
   │   ├── Supply chain disruption and restructuring
   │   └── ESG requirements and sustainability compliance
   │
   └── Strategic Risk Scoring: A+ to F with confidence assessment
       ├── Strategic positioning strength and adaptability
       ├── Innovation capability and competitive differentiation
       ├── Industry attractiveness and structural trends
       ├── Strategic option value and flexibility assessment
       └── Confidence level: 0.0-1.0 with strategic analysis depth

4. Macroeconomic and Systematic Risk Analysis
   ├── Economic Cycle and Growth Risks
   │   ├── GDP growth correlation and economic sensitivity
   │   ├── Recession probability and impact assessment
   │   ├── Interest rate cycle impact and sensitivity
   │   ├── Inflation exposure and pricing power assessment
   │   └── Economic policy changes and fiscal impact
   │
   ├── Financial Market and Systematic Risks
   │   ├── Market beta and systematic risk exposure
   │   ├── Credit market conditions and availability
   │   ├── Currency and exchange rate risks
   │   ├── Commodity price exposure and volatility
   │   └── Liquidity conditions and market stress scenarios
   │
   ├── Geopolitical and Regulatory Risks
   │   ├── Political stability and policy continuity
   │   ├── Trade policy and tariff risks
   │   ├── Regulatory change probability and impact
   │   ├── International sanctions and compliance risks
   │   └── Tax policy changes and optimization strategies
   │
   ├── Environmental and Social Risks
   │   ├── Climate change physical and transition risks
   │   ├── Environmental regulation and compliance costs
   │   ├── Social license and reputational risks
   │   ├── ESG investor requirements and capital access
   │   └── Stakeholder activism and engagement risks
   │
   └── Macro Risk Scoring: A+ to F with confidence assessment
       ├── Economic sensitivity and cycle correlation
       ├── Systematic risk exposure and beta analysis
       ├── Regulatory and policy risk assessment
       ├── ESG risk profile and sustainability metrics
       └── Confidence level: 0.0-1.0 with macro data integration

5. Integrated Risk Assessment and Scenario Analysis
   ├── Risk Correlation and Interaction Analysis
   │   ├── Risk factor interdependency mapping
   │   ├── Compound risk scenario identification
   │   ├── Risk concentration and diversification assessment
   │   └── Risk amplification and mitigation interactions
   │
   ├── Scenario-Based Risk Modeling
   │   ├── Base case risk profile (50% probability)
   │   ├── Stress case scenarios (25% probability each)
   │   │   ├── Economic recession impact modeling
   │   │   ├── Competitive disruption scenarios
   │   │   ├── Regulatory shock impact assessment
   │   │   └── Operational crisis simulation
   │   ├── Black swan event consideration and preparation
   │   └── Recovery timeline and resilience assessment
   │
   ├── Risk-Adjusted Valuation Impact
   │   ├── Risk premium adjustment to discount rates
   │   ├── Scenario probability weighting for fair value
   │   ├── Downside protection and value-at-risk analysis
   │   ├── Risk-adjusted expected returns calculation
   │   └── Portfolio diversification and risk management
   │
   ├── Risk Monitoring and Management Framework
   │   ├── Key risk indicators (KRIs) and dashboard metrics
   │   ├── Early warning system and trigger thresholds
   │   ├── Risk mitigation strategies and contingency planning
   │   ├── Management risk appetite and tolerance levels
   │   └── Board oversight and risk governance assessment
   │
   └── Comprehensive Risk Summary with Investment Implications
       ├── Overall risk profile grade and category breakdown
       ├── Key risk factors and probability-impact ranking
       ├── Risk-adjusted investment recommendation
       ├── Position sizing guidance based on risk assessment
       └── Confidence level: 0.0-1.0 with integrated analysis quality

COMPREHENSIVE RISK ASSESSMENT OUTPUT:
├── Risk Profile Grade: Overall risk assessment A+ to F with rationale
├── Key Risk Factors: Top 5 risks with probability and impact scores
├── Risk-Adjusted Returns: Expected returns with downside protection
├── Scenario Analysis: Base/bull/bear case impact on investment thesis
├── Risk Mitigation: Management actions and investor considerations
├── Monitoring Framework: Key indicators and early warning signals
└── Investment Risk Guidance: Position sizing and portfolio implications
```

### Phase 3: Growth Analysis and Valuation Preparation (Domain-Specific)

**Business Intelligence Growth Driver Analysis**
```
CLI-ENHANCED GROWTH FRAMEWORK:
1. Business Model Growth Decomposition
   → Revenue stream growth analysis from discovery intelligence
   → Business segment expansion opportunities
   → Partnership ecosystem growth catalysts
   → Business-specific KPI growth trajectory analysis
   → Confidence: Business intelligence validation (0.95+)

2. Economic Context Growth Impact
   → Interest rate environment impact on growth sustainability
   → Monetary policy effects on capital availability
   → Sector implications for long-term growth prospects
   → Yield curve considerations for growth financing
   → Confidence: FRED economic analysis integration (0.98+)

3. Peer-Benchmarked Growth Analysis
   → Growth rates vs discovery peer group comparative analysis
   → Market share growth potential within competitive landscape
   → Revenue growth sustainability vs peer benchmarks
   → Innovation and R&D efficiency compared to peers
   → Confidence: Peer group data reliability and selection rationale

4. Management Execution with Track Record
   → Capital allocation history and efficiency
   → Strategic execution vs guidance track record
   → Partnership development and business model evolution
   → Economic cycle management and resilience
   → Confidence: Historical performance and business intelligence
```

**CLI-Enhanced Economic Risk Assessment Matrix**
```
CLI-INTEGRATED RISK FRAMEWORK:
| Risk Category | Probability | Impact | Economic Context | CLI Evidence | Confidence |
|--------------|-------------|---------|------------------|--------------|------------|
| Economic/Macro| [0.0-1.0]  | [1-5]   | FRED Analysis   | Real-time    | [0.95-1.0] |
| Interest Rate | [0.0-1.0]  | [1-5]   | Yield Curve     | Fed Policy   | [0.95-1.0] |
| Operational   | [0.0-1.0]  | [1-5]   | Sector Impact   | Business KPIs| [0.8-0.95] |
| Financial     | [0.0-1.0]  | [1-5]   | Liquidity Stress| CLI Validated| [0.9-0.95] |
| Competitive   | [0.0-1.0]  | [1-5]   | Peer Analysis   | Market Data  | [0.8-0.9]  |
| Regulatory    | [0.0-1.0]  | [1-5]   | Policy Changes  | SEC Edgar    | [0.7-0.85] |
| Technology    | [0.0-1.0]  | [1-5]   | Innovation Pace | R&D Analysis | [0.7-0.8]  |
| Crypto/Sentiment| [0.0-1.0] | [1-5]   | Risk Appetite   | CoinGecko    | [0.85-0.9] |

ECONOMIC CONTEXT INTEGRATION:
- Interest rate sensitivity analysis using FRED data
- Yield curve implications for business model sustainability
- Cryptocurrency sentiment correlation with risk appetite
- Sector-specific monetary policy impact assessment

AGGREGATE RISK SCORE: CLI-weighted probability × economic impact
```

## Framework-Coordinated Output Structure

**File Naming**: `{TICKER}_{YYYYMMDD}_analysis.json` (managed by dasv-analysis-agent)
**Primary Location**: `./data/outputs/fundamental_analysis/analysis/`
**Template Foundation**: Uses `base_analysis_template.j2` with fundamental-specific extensions
**Shared Macros**: Leverages confidence_scoring_macro.j2, risk_assessment_macro.j2, economic_sensitivity_macro.j2

**Framework Integration**: The dasv-analysis-agent manages universal framework sections while this command provides domain-specific fundamental analysis content.

```json
{
  "metadata": {
    "command_name": "fundamental_analyst_analyze",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "analyze",
    "framework_coordinator": "dasv-analysis-agent",
    "domain_specialist": "fundamental_analyst",
    "ticker": "TICKER_SYMBOL",
    "analysis_methodology": "dasv_framework_coordinated_fundamental_analysis",
    "validation_enhanced": "boolean",
    "target_confidence_threshold": "threshold_value",
    "discovery_confidence_inherited": "discovery_data_quality_score",
    "economic_context_integration": "boolean",
    "cli_services_utilized": "array_of_operational_cli_services"
  },
  "discovery_data_inheritance": {
    "metadata": "framework_managed_discovery_preservation",
    "data_completeness": "percentage_of_discovery_data_preserved",
    "inheritance_validation": "dasv_analysis_agent_validation_status",
    "critical_data_preserved": {
      "market_data": "boolean",
      "entity_overview": "boolean",
      "economic_context": "boolean",
      "cli_validation": "boolean",
      "peer_data": "boolean"
    }
  },
  "market_data": {
    "current_price": "cli_validated_current_price",
    "market_cap": "value",
    "price_validation": {
      "yahoo_finance_price": "value",
      "alpha_vantage_price": "value",
      "fmp_price": "value",
      "price_consistency": "boolean",
      "confidence_score": "0.0-1.0"
    },
    "volume": "trading_volume",
    "beta": "value",
    "52_week_high": "value",
    "52_week_low": "value",
    "confidence": "0.0-1.0"
  },
  "company_overview": {
    "name": "company_name",
    "sector": "sector_classification",
    "industry": "industry_classification",
    "description": "business_description",
    "ceo": "chief_executive_officer",
    "employees": "employee_count",
    "headquarters": "headquarters_location",
    "website": "company_website",
    "ipo_date": "ipo_date"
  },
  "economic_context": {
    "metadata": "framework_managed_by_dasv_analysis_agent",
    "interest_rate_environment": "restrictive/neutral/accommodative",
    "yield_curve_signal": "normal/inverted/flat",
    "economic_indicators": {
      "fed_funds_rate": "value",
      "unemployment_rate": "value",
      "gdp_growth": "value",
      "inflation_rate": "value"
    },
    "policy_implications": "array_of_policy_impacts",
    "economic_sensitivity": "framework_managed_sensitivity_analysis"
  },
  "cli_service_validation": {
    "metadata": "framework_managed_by_dasv_analysis_agent",
    "service_health": {
      "service_name": "healthy/degraded/unavailable"
    },
    "health_score": "0.0-1.0_aggregate_health",
    "services_operational": "integer_count",
    "services_healthy": "boolean_overall_status",
    "data_quality_scores": {
      "service_name": "0.0-1.0_per_service"
    }
  },
  "peer_group_analysis": {
    "peer_companies": "array_of_peer_company_data",
    "peer_selection_rationale": "reason_for_peer_selection",
    "comparative_metrics": "peer_comparison_analysis",
    "confidence": "0.0-1.0"
  },
  "financial_health_analysis": {
    "profitability_assessment": {
      "gross_margin_analysis": {
        "gross_margin": "decimal_0.0-1.0",
        "gross_margin_trend": "improving/stable/declining",
        "peer_comparison": "above_average/average/below_average",
        "sustainability": "high/moderate/low",
        "quality_indicators": "array_of_margin_quality_factors",
        "margin_expansion_drivers": "array_of_improvement_catalysts",
        "competitive_positioning": "margin_vs_peers_analysis"
      },
      "operating_leverage": {
        "operating_margin": "decimal_0.0-1.0",
        "operating_leverage_ratio": "decimal_value",
        "scalability_assessment": "high/moderate/low",
        "efficiency_trends": "improving/stable/declining",
        "cost_structure_analysis": "fixed_vs_variable_breakdown",
        "margin_sensitivity": "revenue_change_impact_analysis"
      },
      "ebitda_quality": {
        "normalized_ebitda": "currency_value",
        "reported_ebitda": "currency_value",
        "adjustment_quality": "high/moderate/low",
        "cash_conversion": "ebitda_to_cash_conversion_rate",
        "recurring_vs_nonrecurring": "sustainability_breakdown",
        "ebitda_margin_trend": "historical_margin_progression"
      },
      "cash_conversion": {
        "operating_cash_flow": "currency_value",
        "free_cash_flow": "currency_value",
        "conversion_ratio": "decimal_0.0-1.0",
        "working_capital_efficiency": "working_capital_management_quality",
        "capex_intensity": "capex_as_percentage_of_revenue",
        "cash_generation_sustainability": "cycle_through_analysis"
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "trend": "improving/stable/declining",
      "confidence": "0.0-1.0_with_profitability_evidence"
    },
    "balance_sheet_strength": {
      "liquidity_analysis": {
        "total_liquid_assets": "currency_value",
        "cash_and_equivalents": "currency_value",
        "short_term_investments": "currency_value",
        "liquidity_ratio": "current_ratio_calculation",
        "debt_coverage": "liquid_assets_debt_coverage_months",
        "liquidity_adequacy": "stress_test_assessment",
        "credit_facilities": "available_credit_lines_and_terms"
      },
      "leverage_metrics": {
        "total_debt": "currency_value",
        "debt_to_equity": "decimal_ratio",
        "debt_to_ebitda": "decimal_ratio",
        "interest_coverage": "times_interest_earned_ratio",
        "leverage_assessment": "conservative/moderate/aggressive",
        "debt_maturity_profile": "near_medium_long_term_breakdown",
        "covenant_compliance": "financial_covenant_headroom_analysis"
      },
      "working_capital": {
        "working_capital": "currency_value",
        "working_capital_ratio": "decimal_calculation",
        "working_capital_efficiency": "days_sales_outstanding_inventory_payable",
        "seasonal_patterns": "working_capital_cyclicality_analysis",
        "cash_conversion_cycle": "days_in_working_capital_cycle"
      },
      "off_balance_sheet": {
        "operating_leases": "present_value_of_lease_commitments",
        "commitments": "future_contractual_obligations",
        "contingencies": "potential_liabilities_and_guarantees",
        "special_purpose_entities": "off_balance_sheet_structure_analysis"
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "trend": "improving/stable/declining",
      "confidence": "0.0-1.0_with_balance_sheet_evidence"
    },
    "cash_flow_analysis": {
      "operating_cash_flow": {
        "ocf": "currency_value",
        "ocf_margin": "decimal_0.0-1.0",
        "cash_flow_quality": "high/moderate/low",
        "seasonal_patterns": "quarterly_cash_flow_variability",
        "working_capital_impact": "working_capital_cash_flow_impact",
        "non_cash_adjustments": "depreciation_stock_compensation_analysis"
      },
      "free_cash_flow": {
        "free_cash_flow": "currency_value",
        "fcf_margin": "decimal_0.0-1.0",
        "fcf_conversion": "fcf_as_percentage_of_net_income",
        "capital_intensity": "capex_as_percentage_of_revenue",
        "maintenance_vs_growth_capex": "capex_category_breakdown",
        "fcf_yield": "fcf_as_percentage_of_market_cap"
      },
      "capital_allocation": {
        "capex": "currency_value",
        "share_buybacks": "currency_value",
        "dividends": "currency_value_and_yield",
        "acquisitions": "currency_value_m_and_a_spend",
        "debt_repayment": "debt_reduction_cash_allocation",
        "capital_allocation_quality": "value_creation_track_record"
      },
      "sustainability": {
        "fcf_sustainability": "sustainability_across_cycles",
        "reinvestment_needs": "maintenance_capex_requirements",
        "competitive_moat_investment": "investment_in_competitive_advantages",
        "dividend_coverage": "dividend_sustainability_analysis"
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "trend": "improving/stable/declining",
      "confidence": "0.0-1.0_with_cash_flow_evidence"
    },
    "capital_efficiency": {
      "roic_analysis": {
        "return_on_invested_capital": "decimal_0.0-1.0",
        "roic_vs_wacc": "value_creation_spread",
        "roic_trend": "improving/stable/declining",
        "value_creation": "economic_value_added_analysis",
        "roic_decomposition": "nopat_and_invested_capital_breakdown",
        "peer_roic_comparison": "roic_vs_industry_benchmarks"
      },
      "asset_utilization": {
        "asset_turnover": "decimal_revenue_per_asset_dollar",
        "asset_quality": "tangible_vs_intangible_asset_analysis",
        "asset_efficiency": "asset_productivity_and_utilization",
        "asset_growth": "asset_base_expansion_efficiency",
        "capacity_utilization": "operational_capacity_utilization_rates"
      },
      "management_execution": {
        "capital_allocation_track_record": "historical_capital_allocation_effectiveness",
        "strategic_execution": "strategic_initiative_success_rate",
        "shareholder_returns": "total_shareholder_return_analysis",
        "operational_improvements": "margin_and_efficiency_improvement_track_record",
        "cycle_management": "performance_through_economic_cycles"
      },
      "reinvestment_quality": {
        "reinvestment_rate": "capex_and_acquisitions_as_percentage_of_fcf",
        "growth_efficiency": "incremental_roic_on_reinvestment",
        "return_on_reinvestment": "marginal_returns_on_incremental_capital",
        "investment_discipline": "hurdle_rates_and_investment_criteria",
        "value_creation_from_growth": "growth_capex_value_creation_analysis"
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "trend": "improving/stable/declining",
      "confidence": "0.0-1.0_with_capital_efficiency_evidence"
    }
  },
  "competitive_position_assessment": {
    "market_position": {
      "market_share_trends": {
        "current_market_share": "percentage_or_ranking",
        "historical_trends": "gaining/maintaining/losing_share",
        "share_gains_losses": "quantified_share_movement_analysis",
        "regional_segment_positions": "geographic_and_segment_breakdown",
        "market_leadership_assessment": "leader/challenger/follower/niche",
        "trajectory": "market_position_momentum_and_outlook"
      },
      "pricing_power": {
        "price_elasticity": "demand_sensitivity_to_price_changes",
        "premium_discount_positioning": "price_positioning_vs_competitors",
        "pricing_strategy_effectiveness": "pricing_flexibility_and_execution",
        "customer_price_sensitivity": "customer_switching_behavior_analysis",
        "pricing_power_sustainability": "pricing_power_durability_assessment",
        "cycle_resilience": "pricing_power_through_economic_cycles"
      },
      "customer_analysis": {
        "customer_concentration": "top_customer_percentage_and_dependency",
        "customer_retention_rates": "churn_analysis_and_loyalty_metrics",
        "customer_acquisition_costs": "cac_and_lifetime_value_analysis",
        "geographic_demographic_diversification": "customer_base_diversification",
        "customer_switching_costs": "switching_barriers_and_lock_in_strength",
        "relationship_strength": "customer_satisfaction_and_engagement_metrics"
      },
      "competitive_dynamics": {
        "competitive_intensity": "rivalry_level_and_market_structure",
        "market_concentration": "hhi_and_competitive_landscape_analysis",
        "competitive_responses": "competitor_reaction_patterns_and_strategies",
        "new_entrant_threats": "barrier_effectiveness_and_entry_likelihood",
        "competitive_positioning": "differentiation_and_strategic_positioning",
        "competitive_advantages": "sustainable_competitive_advantage_assessment"
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "confidence": "0.0-1.0_with_market_position_evidence"
    },
    "moat_assessment": {
      "identified_moats": [
        "scale_advantages_and_network_effects",
        "cost_advantages_and_operational_efficiency",
        "switching_costs_and_customer_lock_in",
        "brand_loyalty_and_recognition_value",
        "regulatory_protection_and_compliance_barriers",
        "intellectual_property_and_patent_portfolio",
        "distribution_networks_and_channel_access",
        "technology_advantages_and_innovation_capabilities"
      ],
      "moat_strength_ratings": {
        "individual_moat_scores": "1-10_scale_scoring_by_moat_type",
        "moat_sustainability": "durability_assessment_by_moat",
        "competitive_threat_vulnerability": "threat_level_by_moat_type",
        "moat_interactions": "reinforcement_effects_between_moats",
        "overall_composite_score": "weighted_average_moat_strength"
      },
      "durability_analysis": {
        "moat_erosion_risks": "threats_to_competitive_advantages",
        "technological_disruption_vulnerability": "disruption_risk_by_moat_type",
        "regulatory_change_impact": "regulatory_threats_to_moats",
        "competitive_response_risks": "competitor_countermeasure_effectiveness",
        "long_term_sustainability": "10_year_moat_durability_outlook"
      },
      "evidence_backing": {
        "quantitative_moat_evidence": "financial_metrics_supporting_moats",
        "historical_performance": "moat_track_record_and_consistency",
        "customer_behavior_patterns": "switching_behavior_and_loyalty_evidence",
        "competitive_response_history": "competitor_response_effectiveness_analysis",
        "financial_correlation": "moat_strength_correlation_with_financial_performance"
      },
      "grade": "1-10_scale_overall_moat_strength",
      "confidence": "0.0-1.0_with_moat_evidence_quality"
    },
    "industry_dynamics": {
      "market_growth": {
        "addressable_market_size": "tam_sam_som_analysis",
        "market_maturity": "lifecycle_stage_and_growth_phase",
        "growth_drivers": "key_factors_driving_market_expansion",
        "market_saturation": "penetration_rates_and_saturation_analysis",
        "long_term_outlook": "5_10_year_growth_sustainability"
      },
      "competitive_intensity": {
        "number_of_competitors": "market_fragmentation_analysis",
        "rivalry_intensity": "price_innovation_marketing_competition_levels",
        "price_competition": "margin_pressure_and_price_war_risks",
        "innovation_competition": "r_and_d_intensity_and_technology_races",
        "consolidation_trends": "m_and_a_activity_and_market_consolidation"
      },
      "disruption_risk": {
        "technology_disruption": "disruptive_technology_threats_and_timeline",
        "business_model_innovation": "new_business_model_threats",
        "substitute_products": "substitute_threat_level_and_adoption_rates",
        "digital_transformation": "digitization_impact_and_acceleration",
        "vulnerability_assessment": "industry_disruption_susceptibility"
      },
      "regulatory_environment": {
        "current_framework": "existing_regulatory_structure_and_compliance",
        "regulatory_change_timeline": "pending_regulatory_changes_and_probability",
        "compliance_costs": "regulatory_burden_and_cost_implications",
        "policy_influence": "industry_influence_on_regulatory_outcomes",
        "international_coordination": "global_regulatory_harmonization_trends"
      },
      "supply_chain_dynamics": {
        "supplier_concentration": "supplier_dependency_and_concentration_risks",
        "input_cost_volatility": "raw_material_and_input_price_sensitivity",
        "supply_chain_resilience": "diversification_and_risk_mitigation",
        "vertical_integration": "integration_opportunities_and_barriers",
        "disruption_risks": "supply_chain_vulnerability_assessment"
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "confidence": "0.0-1.0_with_industry_evidence_quality"
    }
  },
  "growth_analysis": {
    "historical_decomposition": {
      "growth_drivers": "object",
      "growth_quality": "object",
      "sustainability": "object",
      "confidence": "0.0-1.0"
    },
    "future_catalysts": {
      "identified_catalysts": "array",
      "probability_estimates": "object",
      "impact_quantification": "object",
      "timeline_analysis": "object",
      "confidence": "0.0-1.0"
    },
    "management_assessment": {
      "track_record": "object",
      "capital_allocation": "object",
      "strategic_execution": "object",
      "credibility_score": "0.0-1.0",
      "confidence": "0.0-1.0"
    }
  },
  "comprehensive_valuation_analysis": {
    "intrinsic_value_analysis": {
      "dcf_modeling": {
        "free_cash_flow_projections": {
          "year_1_fcf": "currency_projection",
          "year_2_fcf": "currency_projection",
          "year_3_fcf": "currency_projection",
          "year_4_fcf": "currency_projection",
          "year_5_fcf": "currency_projection",
          "growth_assumptions": "revenue_and_margin_growth_drivers",
          "projection_confidence": "0.0-1.0_forecast_reliability"
        },
        "terminal_value_estimation": {
          "gordon_growth_method": {
            "terminal_growth_rate": "decimal_perpetual_growth_rate",
            "terminal_fcf": "currency_terminal_year_fcf",
            "terminal_value": "currency_gordon_growth_value"
          },
          "exit_multiple_method": {
            "terminal_ev_ebitda_multiple": "decimal_exit_multiple",
            "terminal_ebitda": "currency_terminal_ebitda",
            "terminal_value": "currency_exit_multiple_value"
          },
          "weighted_terminal_value": "currency_blended_terminal_value"
        },
        "discount_rate_calculation": {
          "cost_of_equity": {
            "risk_free_rate": "decimal_10_year_treasury_rate",
            "beta": "decimal_levered_beta",
            "market_risk_premium": "decimal_equity_risk_premium",
            "company_specific_premium": "decimal_additional_risk_premium",
            "cost_of_equity": "decimal_calculated_coe"
          },
          "cost_of_debt": {
            "interest_bearing_debt": "currency_total_debt",
            "interest_expense": "currency_annual_interest",
            "tax_rate": "decimal_effective_tax_rate",
            "after_tax_cost_of_debt": "decimal_calculated_cod"
          },
          "wacc": {
            "market_value_equity": "currency_market_cap",
            "market_value_debt": "currency_debt_market_value",
            "wacc": "decimal_calculated_wacc"
          }
        },
        "scenario_analysis": {
          "base_case": {
            "probability": "decimal_0.5_base_case_likelihood",
            "enterprise_value": "currency_base_case_ev",
            "equity_value": "currency_base_case_equity_value",
            "value_per_share": "currency_base_case_fair_value"
          },
          "bull_case": {
            "probability": "decimal_0.25_bull_case_likelihood",
            "enterprise_value": "currency_bull_case_ev",
            "equity_value": "currency_bull_case_equity_value",
            "value_per_share": "currency_bull_case_fair_value"
          },
          "bear_case": {
            "probability": "decimal_0.25_bear_case_likelihood",
            "enterprise_value": "currency_bear_case_ev",
            "equity_value": "currency_bear_case_equity_value",
            "value_per_share": "currency_bear_case_fair_value"
          },
          "probability_weighted_value": "currency_expected_dcf_value"
        },
        "sensitivity_analysis": {
          "revenue_growth_sensitivity": "value_impact_per_1pct_revenue_growth_change",
          "margin_sensitivity": "value_impact_per_100bps_margin_change",
          "wacc_sensitivity": "value_impact_per_100bps_wacc_change",
          "terminal_growth_sensitivity": "value_impact_per_100bps_terminal_growth_change"
        }
      },
      "asset_based_valuation": {
        "net_asset_value": "currency_book_value_adjusted_for_market",
        "replacement_cost": "currency_asset_replacement_cost_estimate",
        "liquidation_value": "currency_orderly_liquidation_estimate",
        "asset_valuation_relevance": "high/moderate/low_based_on_asset_intensity"
      },
      "sum_of_parts_analysis": {
        "business_segments": "array_of_segment_valuations_if_applicable",
        "segment_specific_multiples": "ev_ebitda_or_other_by_segment",
        "corporate_overhead_discount": "decimal_conglomerate_discount",
        "sum_of_parts_value": "currency_total_sotp_valuation"
      }
    },
    "relative_valuation_analysis": {
      "peer_group_multiples": {
        "trading_multiples": {
          "current_pe": "decimal_current_pe_ratio",
          "forward_pe": "decimal_forward_pe_ratio",
          "peg_ratio": "decimal_price_earnings_growth_ratio",
          "ev_ebitda": "decimal_ev_to_ebitda_multiple",
          "ev_sales": "decimal_ev_to_sales_multiple",
          "price_book": "decimal_price_to_book_ratio",
          "fcf_yield": "decimal_free_cash_flow_yield",
          "dividend_yield": "decimal_dividend_yield"
        },
        "peer_comparison": {
          "peer_median_pe": "decimal_peer_group_median_pe",
          "peer_median_ev_ebitda": "decimal_peer_group_median_ev_ebitda",
          "company_vs_peer_premium_discount": "decimal_premium_discount_to_peers",
          "valuation_justification": "rationale_for_premium_discount"
        },
        "transaction_multiples": {
          "recent_ma_multiples": "array_of_recent_transaction_multiples",
          "control_premium": "decimal_takeover_premium_estimate",
          "transaction_value_estimate": "currency_ma_based_valuation"
        },
        "historical_multiples": {
          "5_year_avg_pe": "decimal_historical_pe_average",
          "5_year_avg_ev_ebitda": "decimal_historical_ev_ebitda_average",
          "current_vs_historical": "premium_discount_to_historical_average",
          "cycle_adjustment": "economic_cycle_multiple_normalization"
        }
      },
      "market_valuation_context": {
        "sector_valuation_percentile": "percentile_rank_within_sector",
        "market_cycle_positioning": "early_mid_late_cycle_valuation_context",
        "interest_rate_impact": "multiple_sensitivity_to_rate_changes",
        "risk_premium_assessment": "equity_risk_premium_vs_historical"
      },
      "relative_value_summary": {
        "peer_adjusted_fair_value": "currency_peer_multiple_based_value",
        "multiple_expansion_contraction_probability": "likelihood_of_multiple_change",
        "relative_attractiveness": "attractive/neutral/expensive_vs_peers"
      }
    },
    "market_based_valuation": {
      "technical_analysis": {
        "chart_patterns": "support_resistance_trend_analysis",
        "momentum_indicators": "rsi_macd_moving_average_signals",
        "volume_analysis": "institutional_flow_and_volume_patterns",
        "technical_targets": "currency_technical_price_targets"
      },
      "market_sentiment": {
        "analyst_consensus": {
          "consensus_rating": "buy/hold/sell_analyst_average",
          "price_target_consensus": "currency_average_analyst_price_target",
          "revision_trends": "recent_estimate_revision_direction",
          "dispersion": "analyst_estimate_disagreement_level"
        },
        "institutional_activity": {
          "ownership_percentage": "decimal_institutional_ownership",
          "recent_position_changes": "buying_selling_pressure_from_institutions",
          "short_interest": "decimal_short_interest_as_percentage_of_float"
        }
      },
      "liquidity_considerations": {
        "average_daily_volume": "shares_daily_trading_volume",
        "bid_ask_spread": "decimal_liquidity_cost_measure",
        "market_impact": "estimated_price_impact_of_large_trades"
      }
    },
    "integrated_valuation_synthesis": {
      "methodology_weighting": {
        "dcf_weight": "decimal_0.5_to_0.6_intrinsic_value_weight",
        "relative_weight": "decimal_0.3_to_0.4_peer_comparison_weight",
        "market_based_weight": "decimal_0.1_to_0.2_technical_sentiment_weight",
        "weighting_rationale": "justification_for_methodology_weights"
      },
      "fair_value_calculation": {
        "weighted_fair_value": "currency_probability_weighted_target_price",
        "confidence_interval_90pct": {
          "lower_bound": "currency_90pct_confidence_lower_bound",
          "upper_bound": "currency_90pct_confidence_upper_bound"
        },
        "confidence_interval_95pct": {
          "lower_bound": "currency_95pct_confidence_lower_bound",
          "upper_bound": "currency_95pct_confidence_upper_bound"
        }
      },
      "investment_recommendation": {
        "recommendation": "BUY/HOLD/SELL_investment_conclusion",
        "conviction_level": "HIGH/MEDIUM/LOW_recommendation_strength",
        "target_price": "currency_12_month_price_target",
        "expected_return": "decimal_expected_total_return",
        "risk_reward_ratio": "decimal_upside_vs_downside_ratio",
        "time_horizon": "months_investment_time_frame"
      },
      "valuation_risks": {
        "key_assumption_risks": "array_of_critical_valuation_assumptions",
        "model_sensitivity": "high/medium/low_sensitivity_to_key_inputs",
        "execution_risks": "business_execution_risks_affecting_valuation"
      }
    }
  },
  "comprehensive_risk_assessment": {
    "operational_risk_analysis": {
      "business_model_risks": {
        "revenue_concentration": {
          "risk": "customer_geographic_product_concentration_risk",
          "probability": "0.0-1.0_likelihood_of_concentration_problems",
          "impact": "1-5_revenue_impact_severity",
          "evidence": "concentration_metrics_and_dependency_analysis",
          "mitigation": "diversification_strategies_and_risk_controls"
        },
        "product_lifecycle_risk": {
          "risk": "product_obsolescence_and_lifecycle_risk",
          "probability": "0.0-1.0_likelihood_of_disruption",
          "impact": "1-5_business_impact_severity",
          "evidence": "product_maturity_and_innovation_pipeline_analysis",
          "mitigation": "r_and_d_investment_and_innovation_strategy"
        },
        "regulatory_dependency": {
          "risk": "regulatory_approval_and_compliance_dependency",
          "probability": "0.0-1.0_likelihood_of_regulatory_issues",
          "impact": "1-5_business_disruption_severity",
          "evidence": "regulatory_history_and_compliance_track_record",
          "mitigation": "compliance_programs_and_regulatory_relationships"
        }
      },
      "execution_risks": {
        "management_execution": {
          "risk": "strategic_execution_and_management_capability_risk",
          "probability": "0.0-1.0_likelihood_of_execution_failure",
          "impact": "1-5_strategic_impact_severity",
          "evidence": "management_track_record_and_execution_history",
          "mitigation": "management_depth_and_succession_planning"
        },
        "operational_efficiency": {
          "risk": "operational_process_and_efficiency_degradation",
          "probability": "0.0-1.0_likelihood_of_operational_issues",
          "impact": "1-5_margin_and_profitability_impact",
          "evidence": "operational_metrics_and_efficiency_trends",
          "mitigation": "process_improvement_and_automation_initiatives"
        }
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "confidence": "0.0-1.0_operational_risk_assessment_confidence"
    },
    "financial_risk_analysis": {
      "liquidity_risks": {
        "cash_flow_volatility": {
          "risk": "cash_flow_predictability_and_volatility_risk",
          "probability": "0.0-1.0_likelihood_of_cash_flow_stress",
          "impact": "1-5_liquidity_impact_severity",
          "evidence": "historical_cash_flow_variability_analysis",
          "mitigation": "credit_facilities_and_cash_management"
        },
        "working_capital_risk": {
          "risk": "working_capital_requirements_and_seasonal_risk",
          "probability": "0.0-1.0_likelihood_of_working_capital_strain",
          "impact": "1-5_liquidity_strain_severity",
          "evidence": "working_capital_patterns_and_requirements",
          "mitigation": "working_capital_facilities_and_management"
        }
      },
      "leverage_risks": {
        "debt_maturity_risk": {
          "risk": "debt_refinancing_and_maturity_concentration_risk",
          "probability": "0.0-1.0_likelihood_of_refinancing_difficulty",
          "impact": "1-5_financial_distress_severity",
          "evidence": "debt_maturity_schedule_and_market_conditions",
          "mitigation": "refinancing_strategy_and_bank_relationships"
        },
        "covenant_compliance": {
          "risk": "financial_covenant_breach_and_compliance_risk",
          "probability": "0.0-1.0_likelihood_of_covenant_breach",
          "impact": "1-5_financing_restriction_severity",
          "evidence": "covenant_headroom_and_financial_trends",
          "mitigation": "covenant_management_and_amendment_strategies"
        }
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "confidence": "0.0-1.0_financial_risk_assessment_confidence"
    },
    "competitive_strategic_risks": {
      "competitive_position_risks": {
        "market_share_erosion": {
          "risk": "competitive_displacement_and_share_loss_risk",
          "probability": "0.0-1.0_likelihood_of_share_loss",
          "impact": "1-5_revenue_and_profitability_impact",
          "evidence": "competitive_dynamics_and_market_position_trends",
          "mitigation": "competitive_strategy_and_differentiation"
        },
        "new_entrant_threats": {
          "risk": "new_competitor_entry_and_disruption_risk",
          "probability": "0.0-1.0_likelihood_of_disruptive_entry",
          "impact": "1-5_market_disruption_severity",
          "evidence": "barrier_effectiveness_and_entry_economics",
          "mitigation": "moat_strengthening_and_competitive_response"
        }
      },
      "technology_innovation_risks": {
        "disruption_risk": {
          "risk": "technology_disruption_and_obsolescence_risk",
          "probability": "0.0-1.0_likelihood_of_technology_disruption",
          "impact": "1-5_business_model_disruption_severity",
          "evidence": "technology_trends_and_disruption_indicators",
          "mitigation": "innovation_investment_and_technology_partnerships"
        },
        "r_and_d_effectiveness": {
          "risk": "innovation_pipeline_and_r_and_d_execution_risk",
          "probability": "0.0-1.0_likelihood_of_innovation_failure",
          "impact": "1-5_competitive_position_impact",
          "evidence": "r_and_d_track_record_and_pipeline_quality",
          "mitigation": "innovation_process_and_talent_retention"
        }
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "confidence": "0.0-1.0_competitive_risk_assessment_confidence"
    },
    "macroeconomic_systematic_risks": {
      "economic_cycle_risks": {
        "recession_sensitivity": {
          "risk": "economic_downturn_and_recession_exposure_risk",
          "probability": "0.0-1.0_likelihood_of_economic_downturn_impact",
          "impact": "1-5_revenue_profitability_impact_severity",
          "evidence": "economic_sensitivity_and_cycle_correlation",
          "mitigation": "defensive_positioning_and_cost_flexibility"
        },
        "interest_rate_sensitivity": {
          "risk": "rising_interest_rate_and_monetary_policy_risk",
          "probability": "0.0-1.0_likelihood_of_rate_impact",
          "impact": "1-5_valuation_cost_of_capital_impact",
          "evidence": "interest_rate_sensitivity_and_debt_exposure",
          "mitigation": "hedging_strategies_and_debt_management"
        }
      },
      "regulatory_policy_risks": {
        "regulatory_change_risk": {
          "risk": "adverse_regulatory_and_policy_change_risk",
          "probability": "0.0-1.0_likelihood_of_adverse_regulation",
          "impact": "1-5_compliance_cost_business_impact",
          "evidence": "regulatory_environment_and_policy_trends",
          "mitigation": "regulatory_strategy_and_compliance_investment"
        },
        "esg_transition_risk": {
          "risk": "environmental_social_governance_transition_risk",
          "probability": "0.0-1.0_likelihood_of_esg_impact",
          "impact": "1-5_business_model_adaptation_requirement",
          "evidence": "esg_exposure_and_stakeholder_pressure",
          "mitigation": "sustainability_strategy_and_esg_investment"
        }
      },
      "grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F",
      "confidence": "0.0-1.0_macro_risk_assessment_confidence"
    },
    "integrated_risk_summary": {
      "overall_risk_profile": {
        "aggregate_risk_score": "decimal_weighted_average_risk_score",
        "risk_grade": "A+/A/A-/B+/B/B-/C+/C/C-/D+/D/F_overall_risk_grade",
        "risk_category_breakdown": {
          "operational_risk_weight": "decimal_operational_risk_contribution",
          "financial_risk_weight": "decimal_financial_risk_contribution",
          "competitive_risk_weight": "decimal_competitive_risk_contribution",
          "macro_risk_weight": "decimal_macro_risk_contribution"
        }
      },
      "scenario_based_risk_modeling": {
        "base_case_risk_profile": {
          "probability": "decimal_0.5_base_case_likelihood",
          "risk_impact": "expected_risk_impact_in_base_scenario",
          "key_risk_factors": "array_of_primary_risks_in_base_case"
        },
        "stress_case_scenarios": {
          "economic_recession": {
            "probability": "decimal_recession_scenario_likelihood",
            "risk_amplification": "risk_factor_interaction_in_recession",
            "recovery_timeline": "expected_recovery_duration"
          },
          "competitive_disruption": {
            "probability": "decimal_disruption_scenario_likelihood",
            "market_share_impact": "share_loss_in_disruption_scenario",
            "adaptation_timeline": "business_model_adaptation_timeframe"
          }
        }
      },
      "risk_adjusted_investment_impact": {
        "risk_premium_adjustment": "additional_discount_rate_for_risk",
        "downside_protection": "value_at_risk_and_downside_scenarios",
        "position_sizing_guidance": "recommended_position_size_based_on_risk",
        "risk_monitoring_framework": "key_risk_indicators_and_triggers"
      }
    }
  },
  "analytical_insights": {
    "metadata": "framework_managed_structured_findings",
    "key_findings": "array_minimum_3_findings",
    "investment_implications": "array_minimum_3_implications",
    "analysis_limitations": "array_minimum_2_limitations",
    "follow_up_research": "array_minimum_3_recommendations"
  },
  "quality_metrics": {
    "metadata": "framework_managed_using_confidence_scoring_macro",
    "analysis_confidence": "0.0-1.0_overall_confidence",
    "data_quality_impact": "0.0-1.0_data_influence",
    "methodology_rigor": "0.0-1.0_process_quality",
    "evidence_strength": "0.0-1.0_support_quality",
    "statistical_significance": "0.0-1.0_where_applicable",
    "sample_adequacy": "0.0-1.0_where_applicable"
  }
}
```

## DASV Analysis Phase Execution Protocol (Framework-Coordinated)

### Framework Integration Approach

**Execution Coordination**: This protocol leverages the **dasv-analysis-agent** as framework coordinator to enhance comprehensive fundamental analysis domain expertise through layered coordination rather than division of labor.

**10-Step DASV Analysis Process Integration**:
1. **Initialize Framework Structure** (dasv-analysis-agent provides universal scaffolding)
2. **Populate Universal Metadata** (dasv-analysis-agent enhances metadata completeness)
3. **Validate Discovery Data Inheritance** (dasv-analysis-agent ensures data preservation for comprehensive analysis)
4. **Integrate Economic Context** (dasv-analysis-agent provides economic foundation for domain analysis)
5. **Perform Comprehensive Domain Analysis** (fundamental_analyst with framework enhancement)
6. **Framework-Enhanced Risk Assessment** (comprehensive domain risk analysis with framework coordination)
7. **Generate Enhanced Analytical Insights** (domain expertise with framework structure)
8. **Calculate Framework-Coordinated Quality Metrics** (domain confidence enhanced by framework standards)
9. **Validate Comprehensive Schema Compliance** (full analytical depth with framework compatibility)
10. **Export Framework-Coordinated Output** (comprehensive analysis with framework organization)

### Pre-Execution (Framework-Coordinated)

**Agent Invocation**:
```
INVOKE dasv-analysis-agent WITH:
- discovery_file: {TICKER}_{YYYYMMDD}_discovery.json
- analysis_type: fundamental
- confidence_threshold: 0.9
- framework_phase: initialize
```

**Framework Validation** (Steps 1-4):
1. **Initialize Framework Structure**: dasv-analysis-agent sets up universal JSON architecture
2. **Populate Universal Metadata**: Framework execution context and methodology tracking
3. **Validate Discovery Data Inheritance**: Complete data preservation verification with fail-fast
4. **Integrate Economic Context**: Economic regime and indicator integration using economic_sensitivity_macro.j2

**Domain Preparation**:
- Load fundamental-specific parameters and thresholds
- Initialize financial health assessment frameworks
- Prepare peer group and industry benchmarks
- Set up domain-specific quality gates

### Main Execution (Comprehensive Domain Analysis with Framework Enhancement - Step 5)

**Framework-Enhanced Comprehensive Fundamental Analysis**:
1. **Comprehensive Financial Health Analysis** (Framework-Enhanced Domain Expertise)
   - Execute complete 4-dimension financial health assessment framework
   - Generate detailed profitability, balance sheet, cash flow, and capital efficiency analysis
   - Apply framework-coordinated confidence scoring to domain-specific financial metrics
   - Framework enhances analytical depth with quality standards and economic context integration

2. **Comprehensive Competitive Position Assessment** (Framework-Enhanced Domain Expertise)
   - Conduct complete 3-dimension competitive analysis: market position, moat assessment, industry dynamics
   - Execute detailed competitive intelligence with framework-coordinated peer benchmarking
   - Apply framework-enhanced competitive risk assessment with systematic probability-impact analysis
   - Framework enhances competitive analysis with economic context and quality validation

3. **Comprehensive Valuation Analysis** (Framework-Enhanced Domain Expertise)
   - Execute complete 4-methodology valuation framework: DCF, relative, market-based, and integrated synthesis
   - Conduct framework-enhanced scenario analysis with probability-weighted fair value calculation
   - Apply framework-coordinated sensitivity analysis and investment recommendation framework
   - Framework enhances valuation rigor with quality standards and confidence intervals

4. **Comprehensive Risk Assessment** (Framework-Enhanced Domain Expertise)
   - Execute complete 5-category risk analysis: operational, financial, competitive, strategic, macro
   - Conduct framework-enhanced quantified risk assessment with probability-impact matrices
   - Apply framework-coordinated scenario-based risk modeling and stress testing
   - Framework enhances risk analysis with systematic integration and monitoring frameworks

**Layered Coordination Approach**:
- Framework provides structure, standards, and validation while domain analysis maintains full analytical depth
- Economic context integration enhances rather than replaces domain-specific analysis
- Quality metrics coordination ensures institutional standards without limiting analytical comprehensiveness
- Risk assessment framework enhances domain risk analysis rather than handling it separately

### Post-Execution (Framework-Coordinated - Steps 6-10)

**Agent Coordination**:
```
INVOKE dasv-analysis-agent WITH:
- domain_analysis: fundamental_analysis_results
- framework_phase: finalize
- output_template: base_analysis_template.j2
```

**Framework Completion** (Steps 6-10):
6. **Framework-Enhanced Risk Assessment Coordination**: Integrate comprehensive domain risk analysis with framework standards and systematic validation
7. **Generate Framework-Coordinated Analytical Insights**: Structure comprehensive domain findings within framework requirements while maintaining analytical depth
8. **Calculate Framework-Enhanced Quality Metrics**: Apply institutional-grade confidence scoring to comprehensive domain analysis results
9. **Validate Comprehensive Schema Compliance**: Ensure full analytical depth meets framework compatibility without reducing content quality
10. **Export Framework-Coordinated Comprehensive Output**: Generate complete analysis output with framework organization and domain expertise integration

**Final Validation**:
- Verify >90% institutional confidence threshold achieved through comprehensive domain analysis
- Confirm framework schema compliance while maintaining full analytical depth
- Validate synthesis phase readiness with complete domain expertise integration
- Log performance metrics demonstrating both framework benefits and comprehensive analytical quality

**Layered Coordination Success Criteria**:
- Comprehensive analytical depth maintained at levels comparable to pre-framework analysis
- Framework benefits (structure, quality, consistency) successfully integrated without content reduction
- Domain expertise fully preserved and enhanced rather than limited by framework coordination
- Institutional-grade standards achieved through enhanced domain analysis rather than framework replacement

## Framework-Coordinated Quality Standards

### Institutional-Grade Framework Standards (Managed by dasv-analysis-agent)
- **Confidence Threshold**: >90% minimum for institutional grade (targeting >95% for enhanced)
- **Service Health**: >80% CLI service operational status requirement
- **Data Completeness**: >85% for comprehensive analysis certification
- **Multi-Source Validation**: <2% variance tolerance across data sources
- **Schema Compliance**: 100% validation against Analysis phase output specification

### Domain-Specific Quality Requirements (Fundamental Analysis)
- **Financial Metrics Accuracy**: All ratios and calculations verified against discovery data
- **Peer Comparison Validity**: Size and industry adjustments properly applied
- **Competitive Analysis Depth**: Moat assessment with quantified strength ratings
- **Valuation Input Quality**: Discount rates and projections with confidence intervals

### Framework Validation Requirements (Enforced by dasv-analysis-agent)
- **Required Field Presence**: All universal framework sections must be populated
- **Data Type Conformance**: Confidence scores 0.0-1.0, risk probabilities decimal format
- **Value Range Constraints**: Impact scores 1-5, timestamps ISO 8601 format
- **Minimum Array Lengths**: Key findings (3+), implications (3+), limitations (2+), research (3+)
- **File Organization**: Correct naming `{TICKER}_{YYYYMMDD}_analysis.json` in appropriate directory

### Fail-Fast Quality Enforcement (Framework-Managed)
- Discovery data inheritance below 100% for critical data points triggers immediate failure
- CLI service health below 80% operational threshold triggers immediate failure
- Confidence scores not meeting 90% institutional minimum triggers immediate failure
- Missing required framework sections triggers immediate failure
- Schema validation failures trigger immediate failure with specific violation details

### Integration Requirements (Framework-Coordinated)
- **Template Utilization**: Uses base_analysis_template.j2 with fundamental-specific inheritance blocks
- **Macro Integration**: Leverages shared macros for confidence scoring, risk assessment, economic sensitivity
- **Quality Propagation**: Framework confidence scores feed into overall analysis confidence
- **Synthesis Readiness**: Structured output compatible with synthesis phase requirements

**Integration with DASV Framework**: This domain-specific microservice works in coordination with the dasv-analysis-agent to transform discovery data into comprehensive fundamental analysis insights, utilizing shared framework components while maintaining specialized financial analysis expertise. The analysis provides domain-specific input for investment thesis construction and recommendation generation in the synthesis phase.

**Framework Coordination**: dasv-analysis-agent
**Domain Expertise**: Fundamental Analysis Specialist
**Template Foundation**: base_analysis_template.j2 with fundamental inheritance blocks
**Shared Components**: confidence_scoring_macro.j2, risk_assessment_macro.j2, economic_sensitivity_macro.j2
**Quality Standards**: Institutional-grade framework compliance (>90% confidence threshold)

**Author**: Cole Morton
**Confidence**: [Framework-coordinated analysis confidence calculated from discovery data quality, economic context validation, and institutional-grade quality standards]
**Data Quality**: [Framework-managed data quality score based on CLI service reliability, economic context freshness, and comprehensive validation protocols]

## CLI Service Integration Benefits

### Multi-Source Validation Enhancement
- **Price Consistency Validation**: Perfect 1.0 confidence across Yahoo Finance, Alpha Vantage, and FMP
- **Financial Statement Verification**: Complete validation of income statement, balance sheet, and cash flow data
- **Economic Context Integration**: Real-time FRED economic indicators with policy implications
- **Cryptocurrency Sentiment Analysis**: CoinGecko integration for broader market risk appetite assessment

### Institutional-Grade Confidence Propagation
- **Discovery Confidence Inheritance**: Leverage 0.95+ financial data confidence from discovery phase
- **Economic Context Reliability**: FRED CLI integration typically provides 0.98+ confidence
- **CLI Service Health Impact**: Real-time service operational status affects analytical confidence
- **Multi-Source Consistency**: Cross-validation enhances overall analytical reliability

### Real-Time Economic Intelligence
- **Interest Rate Environment**: Fed funds rate, yield curve, and monetary policy implications
- **Economic Indicators**: Unemployment, inflation, and sector-specific economic context
- **Policy Impact Analysis**: Federal Reserve policy implications for business model sustainability
- **Market Sentiment Integration**: Cryptocurrency sentiment correlation with broader risk appetite

### Enhanced Analytical Capabilities
- **Business Model Intelligence**: Detailed revenue streams, operational model, and key metrics
- **Peer Group Optimization**: Discovery-validated peer selection with comparative intelligence
- **Regulatory Intelligence**: SEC Edgar integration for compliance and regulatory risk assessment
- **Data Quality Assurance**: Comprehensive CLI service health and reliability monitoring
