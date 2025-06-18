# Fundamental Analysis

Generate institutional-quality fundamental analysis with sophisticated reasoning chains, self-validation, and transparent confidence assessments for any stock.

## Purpose

Produces comprehensive fundamental analysis that systematically identifies relevant business metrics, applies multi-perspective evaluation frameworks, and generates risk-adjusted investment recommendations with explicit confidence levels and reasoning transparency.

**Output Format**: Single file `TICKER_YYYYMMDD.md` in `/data/outputs/analysis_fundamental/` directory.

**Focus Requirement**: Analysis must remain strictly focused on the requested ticker symbol. Do not create additional industry or peer analysis files beyond the core fundamental analysis.

## Parameters

- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `peer_count`: Number of peer companies to include (optional, default: 3-5)
- `confidence_threshold`: Minimum confidence for recommendations - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `scenario_count`: Number of valuation scenarios - `3` | `5` | `7` (optional, default: 3)

## Real-Time Data Acquisition

**MANDATORY**: All analysis must use the latest available market data. Before beginning analysis, systematically gather current information using multiple data sources.

### Phase 0: Current Market Data Collection

**0.1 Live Price & Market Data**
```
REQUIRED DATA POINTS:
1. Current Stock Price & Trading Data
   → Real-time price, volume, bid/ask spread
   → Intraday price movement and volatility
   → Market cap calculation with latest share count
   → 52-week high/low context
   → Trading volume vs average (liquidity assessment)

2. Recent Price Performance
   → 1D, 1W, 1M, 3M, 6M, 1Y returns
   → Relative performance vs S&P 500 and sector ETF
   → Recent volatility metrics (30-day, 90-day)
   → Beta calculation with recent price data

3. Current Valuation Multiples
   → P/E, P/B, EV/EBITDA using latest price
   → P/S, P/FCF with most recent financials
   → PEG ratio with forward growth estimates
   → Compare to sector median multiples
```

**0.2 Financial Data Sources (Latest Available)**
```
DATA ACQUISITION PRIORITY:
1. SEC Filings (Primary)
   → Most recent 10-K, 10-Q filings
   → Latest 8-K announcements
   → Proxy statements for governance insights
   → Insider trading activity (Form 4s)

2. Real-Time Financial APIs
   → Yahoo Finance, Alpha Vantage, or similar
   → Current financial metrics and ratios
   → Analyst estimates and revisions
   → Recent earnings call transcripts

3. News & Market Intelligence
   → Recent news sentiment analysis
   → Analyst rating changes (last 30 days)
   → Industry developments affecting stock
   → Regulatory updates or changes
```

**0.3 Data Validation & Freshness Check**
```
QUALITY ASSURANCE PROTOCOL:
□ Verify all price data is from current trading session
□ Confirm financial statements are most recent available
□ Check data consistency across multiple sources
□ Flag any stale data points (>1 trading day for prices)
□ Document data collection timestamp for all sources
□ Set confidence scores based on data recency and reliability
```

## Systematic Analysis Framework

### Phase 1: Foundation & Discovery (Confidence Building)

**1.1 Company Intelligence Gathering**
```
REASONING CHAIN:
1. Identify primary revenue streams and business model
   → Validate against SEC filings and company reports
   → Cross-reference with industry classifications
   → Confidence score: [0.0-1.0]

2. Discover business-specific KPIs
   → Start with industry standard metrics
   → Identify company-specific disclosed metrics
   → Validate relevance through earnings call analysis
   → Prioritize by management focus and investor questions
   → Confidence score per metric: [0.0-1.0]

3. Establish peer group
   → Direct competitors by revenue overlap
   → Similar business model companies
   → Market cap and geographic comparables
   → Validate through competitive mentions in 10-Ks
```

**1.2 Data Quality Assessment**
```
FOR EACH DATA POINT:
- Source reliability: [Primary/Secondary/Estimated]
- Recency: [Current/Recent/Dated]
- Completeness: [Complete/Partial/Missing]
- Consistency check across sources
- Overall data confidence: [0.0-1.0]
```

### Phase 2: Multi-Dimensional Analysis (Systematic Evaluation)

**2.1 Financial Health Analysis**
```
EVALUATION FRAMEWORK:
├── Profitability Analysis
│   ├── Gross margins (trend, stability, drivers)
│   ├── Operating leverage assessment
│   ├── EBITDA quality and adjustments
│   └── Free cash flow conversion
│
├── Balance Sheet Strength
│   ├── Liquidity analysis (current, quick, cash ratios)
│   ├── Leverage metrics (debt/equity, interest coverage)
│   ├── Working capital efficiency
│   └── Off-balance sheet obligations
│
└── Capital Efficiency
    ├── ROIC vs WACC spread
    ├── Asset turnover trends
    ├── Capital allocation track record
    └── Reinvestment opportunities

CONFIDENCE WEIGHTING:
- Each metric gets confidence score [0.0-1.0]
- Overall section confidence = weighted average
- Flag any metric below confidence_threshold
```

**2.2 Competitive Position Assessment**
```
MULTI-PERSPECTIVE FRAMEWORK:
1. Market Position
   - Market share trends (gaining/stable/losing)
   - Pricing power indicators
   - Customer concentration analysis
   - Confidence: [0.0-1.0]

2. Competitive Advantages
   - Network effects assessment
   - Switching costs analysis
   - Brand value quantification
   - Scale advantages measurement
   - Confidence per moat: [0.0-1.0]

3. Innovation & Disruption
   - R&D efficiency (output/spend)
   - Patent portfolio strength
   - Digital transformation progress
   - Disruption vulnerability score
   - Confidence: [0.0-1.0]
```

### Phase 3: Forward-Looking Synthesis (Scenario Construction)

**3.1 Growth Driver Identification**
```
SYSTEMATIC PROCESS:
1. Historical growth decomposition
   → Volume vs price contribution
   → Organic vs inorganic growth
   → Geographic vs product expansion

2. Future catalyst assessment
   → Probability-weight each catalyst
   → Estimate revenue impact
   → Timeline to realization
   → Dependencies and risks

3. Management credibility scoring
   → Track record vs guidance
   → Capital allocation history
   → Strategic pivot success rate
   → Confidence: [0.0-1.0]
```

**3.2 Risk Factor Quantification**
```
RISK ASSESSMENT MATRIX:
| Risk Category | Probability | Impact | Mitigation | Confidence |
|--------------|-------------|---------|------------|------------|
| Operational   | [0.0-1.0]  | [1-5]   | [Strategy] | [0.0-1.0] |
| Financial     | [0.0-1.0]  | [1-5]   | [Strategy] | [0.0-1.0] |
| Competitive   | [0.0-1.0]  | [1-5]   | [Strategy] | [0.0-1.0] |
| Regulatory    | [0.0-1.0]  | [1-5]   | [Strategy] | [0.0-1.0] |
| Macro         | [0.0-1.0]  | [1-5]   | [Strategy] | [0.0-1.0] |

AGGREGATE RISK SCORE: Weighted probability × impact
```

### Phase 4: Valuation & Recommendation (Multi-Method Validation)

**4.1 Valuation Framework**
```
TRIANGULATION APPROACH:
1. DCF Analysis
   → Build revenue scenarios (bear/base/bull + variants)
   → Margin progression modeling
   → Terminal value sensitivity
   → WACC calculation with justification
   → Confidence interval: [low, high]

2. Relative Valuation
   → P/E vs growth rate (PEG)
   → EV/EBITDA vs peers
   → P/B for asset-heavy businesses
   → Industry-specific multiples
   → Regression analysis for fair multiple

3. Sum-of-Parts (if applicable)
   → Business segment valuation
   → Hidden asset identification
   → Subsidiary stake values
   → Cross-validation with comparables

VALUATION SYNTHESIS:
- Weight methods by reliability for this company
- Calculate weighted average fair value
- Determine confidence interval
- Identify key sensitivities
```

**4.2 Investment Thesis Construction**
```
DECISION FRAMEWORK:
1. Calculate risk-adjusted returns
   → Expected return = Σ(Scenario probability × Return)
   → Sharpe ratio estimation
   → Downside risk assessment

2. Position sizing recommendation
   → Kelly criterion application
   → Portfolio context consideration
   → Liquidity constraints

3. Conviction scoring
   → Data quality score: [0.0-1.0]
   → Analysis confidence: [0.0-1.0]
   → Thesis differentiation: [0.0-1.0]
   → Time horizon clarity: [0.0-1.0]
   → OVERALL CONVICTION: [Weighted average]
```

## Self-Validation Checklist

**Pre-Output Validation:**
```
□ All key metrics have confidence scores ≥ confidence_threshold
□ Valuation methods show <20% divergence (or explained)
□ Risk factors are quantified, not just listed
□ Growth assumptions tied to specific evidence
□ Competitive advantages validated with data
□ Management assessment based on track record
□ Industry dynamics reflect latest developments
□ ESG factors material to valuation included
□ Black swan risks explicitly considered
□ Output internally consistent (no contradictions)
```

## Output Structure

**File Naming**: `TICKER_YYYYMMDD.md` (e.g., `AAPL_20250617.md`)
**Directory**: `/data/outputs/analysis_fundamental/`

```markdown
# [COMPANY NAME] (TICKER) - Fundamental Analysis
*Generated: [DATE] | Confidence: [X.X/1.0] | Data Quality: [X.X/1.0]*

## 🎯 Investment Thesis & Recommendation

### Core Thesis
[2-3 sentence thesis with key value drivers]

### Recommendation: [BUY/HOLD/SELL] | Conviction: [X.X/1.0]
- **Fair Value Range**: $[XXX] - $[XXX] (Current: $[XXX])
- **Expected Return**: [XX]% ([X]Y horizon)
- **Risk-Adjusted Return**: [XX]% (Sharpe: [X.X])
- **Position Size**: [X-X]% of portfolio

### Key Catalysts (Next 12-24 Months)
1. [Catalyst 1] - Probability: [XX]% | Impact: $[XX]/share
2. [Catalyst 2] - Probability: [XX]% | Impact: $[XX]/share
3. [Catalyst 3] - Probability: [XX]% | Impact: $[XX]/share

## 📊 Business Intelligence Dashboard

### Business-Specific KPIs
| Metric | Current | 3Y Avg | 5Y Trend | vs Peers | Confidence | Insight |
|--------|---------|---------|-----------|----------|------------|---------|
| [Auto-discovered metrics with relevance scores and confidence levels] |

### Financial Health Scorecard
| Category | Score | Trend | Key Metrics | Red Flags |
|----------|-------|-------|-------------|-----------|
| Profitability | [A-F] | [↑→↓] | [Details] | [If any] |
| Balance Sheet | [A-F] | [↑→↓] | [Details] | [If any] |
| Cash Flow | [A-F] | [↑→↓] | [Details] | [If any] |
| Capital Efficiency | [A-F] | [↑→↓] | [Details] | [If any] |

## 🏆 Competitive Position Analysis

### Moat Assessment
| Competitive Advantage | Strength | Durability | Evidence | Confidence |
|----------------------|----------|------------|----------|------------|
| [Identified moats with quantified strength and supporting data] |

### Industry Dynamics
- **Market Growth**: [XX]% CAGR | TAM: $[XXX]B
- **Competitive Intensity**: [Low/Medium/High] | HHI: [XXXX]
- **Disruption Risk**: [Low/Medium/High] | Key Threats: [List]
- **Regulatory Outlook**: [Favorable/Neutral/Challenging]

## 📈 Valuation Analysis

### Multi-Method Valuation
| Method | Fair Value | Weight | Confidence | Key Assumptions |
|--------|-----------|---------|------------|-----------------|
| DCF | $[XXX] | [XX]% | [X.X/1.0] | [List] |
| Comps | $[XXX] | [XX]% | [X.X/1.0] | [List] |
| Other | $[XXX] | [XX]% | [X.X/1.0] | [List] |
| **Weighted Average** | **$[XXX]** | 100% | **[X.X/1.0]** | - |

### Scenario Analysis
| Scenario | Probability | Price Target | Return | Key Drivers |
|----------|------------|--------------|---------|-------------|
| Bear | [XX]% | $[XXX] | [XX]% | [Assumptions] |
| Base | [XX]% | $[XXX] | [XX]% | [Assumptions] |
| Bull | [XX]% | $[XXX] | [XX]% | [Assumptions] |
| **Expected Value** | 100% | **$[XXX]** | **[XX]%** | - |

## ⚠️ Risk Matrix

### Quantified Risk Assessment
| Risk Factor | Probability | Impact | Risk Score | Mitigation | Monitoring |
|-------------|------------|---------|------------|------------|------------|
| [Specific risks with numerical assessments and action plans] |

### Sensitivity Analysis
Key variables impact on fair value:
- [Variable 1]: ±10% change = ±$[XX] ([XX]%)
- [Variable 2]: ±10% change = ±$[XX] ([XX]%)
- [Variable 3]: ±10% change = ±$[XX] ([XX]%)

## 🎬 Action Plan

### Entry Strategy
- **Optimal Entry**: Below $[XXX] ([XX]% margin of safety)
- **Accumulation Zone**: $[XXX] - $[XXX]
- **Position Building**: [Gradual/Opportunistic/Immediate]

### Monitoring Framework
**Weekly Indicators**:
- [Metric 1]: Alert if [condition]
- [Metric 2]: Alert if [condition]

**Quarterly Checkpoints**:
- [ ] Revenue growth vs guidance
- [ ] Margin progression on track
- [ ] Competitive position stable/improving
- [ ] Key risks materialization check

### Exit Triggers
1. **Thesis Broken**: [Specific conditions]
2. **Valuation Target**: $[XXX] ([XX]% gain)
3. **Better Opportunity**: Required excess return: [XX]%
4. **Risk Materialization**: [Specific scenarios]

## 📋 Analysis Metadata

**Data Sources & Quality**:
- Primary Sources: [List with confidence scores]
- Data Completeness: [XX]%
- Latest Data Point: [Date]

**Methodology Notes**:
- [Any specific adjustments or assumptions]
- [Limitations or caveats]
- [Areas requiring follow-up research]
```

## Quality Assurance Protocol

### Pre-Analysis Checks
1. **Data Availability Assessment**
   - Check filing recency and completeness
   - Identify data gaps and alternatives
   - Set confidence thresholds appropriately

2. **Industry Calibration**
   - Verify industry classification accuracy
   - Update peer group if needed
   - Confirm relevant KPIs for sector

### During Analysis
1. **Cross-Validation Points**
   - Management guidance vs analyst consensus
   - Historical accuracy of projections
   - Peer company developments impact

2. **Reasoning Documentation**
   - Document key assumptions explicitly
   - Note confidence level for each conclusion
   - Flag areas of high uncertainty

### Post-Analysis Validation
1. **Internal Consistency**
   - Recommendation aligns with analysis
   - Scenarios are realistic and distinct
   - Risk assessment matches recommendation

2. **Actionability Check**
   - Clear entry/exit points defined
   - Monitoring plan is executable
   - Time horizons are specified

3. **Output Validation**
   - Single file output in correct format: `TICKER_YYYYMMDD.md`
   - Analysis focused solely on requested ticker
   - No additional industry/peer files generated
   - Confidence scores integrated throughout analysis

## Usage Examples

```bash
# Standard comprehensive analysis (generates TICKER_YYYYMMDD.md)
/fundamental_analysis TICKER

# Deep dive with high confidence requirement
/fundamental_analysis TICKER depth=deep-dive confidence_threshold=0.8

# Quick summary with extended timeframe
/fundamental_analysis TICKER depth=summary timeframe=10y

# Full analysis with extra scenarios
/fundamental_analysis TICKER scenario_count=7 peer_count=7
```

## Key Implementation Notes

1. **Single File Output**: Always generate exactly one file named `TICKER_YYYYMMDD.md`
2. **Ticker Focus**: Analyze only the requested ticker - no additional industry files
3. **Quantitative Framework**: Include confidence scores (0.0-1.0) throughout analysis
4. **Risk-Adjusted Approach**: Use probability-weighted scenarios and sensitivity ranges
5. **Actionable Structure**: Clear entry/exit triggers and monitoring framework

This enhanced framework ensures institutional-quality analysis with transparent reasoning, quantified confidence levels, and actionable insights suitable for sophisticated investment decision-making.
