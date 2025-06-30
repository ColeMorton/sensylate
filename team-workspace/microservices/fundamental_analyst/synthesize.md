# Fundamental Analyst Synthesize Microservice
*DASV Phase 3: Integration and Recommendation Generation*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - discovery_data: object       # Output from fundamental_analyst_discover
  - analysis_data: object        # Output from fundamental_analyst_analyze
  - ticker: string              # Stock symbol (uppercase format)
  - confidence_threshold: float # Minimum confidence requirement (default: 0.7)

optional_inputs:
  - depth: string               # Analysis depth: summary|standard|comprehensive|deep-dive (default: comprehensive)
  - scenario_count: integer     # Number of valuation scenarios (default: 3)
  - timeframe: string          # Analysis period (default: 5y)
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: markdown_document
    format: markdown
    confidence_score: float
    location: "./data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md"
    requirement: "Must produce identical files to current fundamental_analysis.md implementation"

  metadata:
    execution_time: timestamp
    data_sources: array
    quality_metrics: object
    next_phase_ready: boolean
```

### Service Dependencies
- **Upstream Services**: fundamental_analyst_discover, fundamental_analyst_analyze
- **Downstream Services**: fundamental_analyst_validate
- **External APIs**: None (uses synthesized data from upstream)
- **Shared Resources**: Team workspace, output directory

## Critical Output Requirements

**MANDATORY**: This microservice MUST produce files identical to the current fundamental_analysis.md command output. The files must be saved to `./data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md` with exactly the same format, content structure, and quality as the existing implementation.

## Valuation & Recommendation Synthesis

### 4.1 Valuation Framework
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

### 4.2 Investment Thesis Construction
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

**MANDATORY CONSISTENCY VALIDATION:**
```
□ ALL confidence scores use 0.0-1.0 format (reject any X/10 format)
□ Header format: "Confidence: [X.X/1.0] | Data Quality: [X.X/1.0]"
□ Author attribution: "Cole Morton" (consistent across all posts)
□ Risk probabilities in decimal format (0.0-1.0), never percentages in tables
□ Valuation table confidence column uses 0.X/1.0 format
□ All monetary values include $ symbol with appropriate formatting
□ Scenario analysis probabilities sum to 100%
□ Data completeness percentage included in metadata
□ Source quality scores in 0.X/1.0 format in metadata section
□ Tables properly formatted with consistent column headers
□ No X/10 or percentage formats in confidence/probability columns
```

## Exact Output Structure

**File Naming**: `TICKER_YYYYMMDD.md` (e.g., `AAPL_20250617.md`)
**Directory**: `./data/outputs/fundamental_analysis/`

```markdown
# [COMPANY NAME] (TICKER) - Fundamental Analysis
*Generated: [DATE] | Confidence: [X.X/1.0] | Data Quality: [X.X/1.0]*
<!-- Author: Cole Morton (MANDATORY - ensure consistency) -->

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
| DCF | $[XXX] | [XX]% | 0.X | [List] |
| Comps | $[XXX] | [XX]% | 0.X | [List] |
| Other | $[XXX] | [XX]% | 0.X | [List] |
| **Weighted Average** | **$[XXX]** | 100% | **0.X** | - |

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
| [Risk Name] | 0.X | [1-5] | [Score] | [Strategy] | [Metrics] |
<!-- MANDATORY: Use 0.0-1.0 decimal format for probability column -->

### Sensitivity Analysis
Key variables impact on fair value:
- [Variable 1]: ±10% change = ±$[XX] ([XX]%)
- [Variable 2]: ±10% change = ±$[XX] ([XX]%)
- [Variable 3]: ±10% change = ±$[XX] ([XX]%)

## 📋 Analysis Metadata

**Data Sources & Quality**:
- Primary Sources: [Source Name] (0.X), [Source Name] (0.X), [Source Name] (0.X)
- Data Completeness: [XX]%
- Latest Data Point: [Date]
- Data Freshness: All sources current as of analysis date
<!-- MANDATORY: Use 0.0-1.0 format for all source confidence scores -->

**Methodology Notes**:
- [Any specific adjustments or assumptions]
- [Limitations or caveats]
- [Areas requiring follow-up research]

## Investment Recommendation Summary

[Comprehensive 150-200 word summary synthesizing the entire analysis into institutional-quality investment decision framework. Include: (1) Core investment thesis with quantified risk-adjusted returns, (2) Key confidence drivers and methodology validation, (3) Balance sheet strength and downside protection, (4) Scenario analysis results with probability-weighted outcomes, (5) Position sizing recommendation within portfolio context, (6) Specific catalysts with impact quantification, (7) Stress-tested bear case limitations, (8) Monte Carlo/sensitivity analysis validation of fair value range, (9) Overall conviction level with supporting evidence, (10) Clear articulation of why this represents exceptional/adequate/poor risk-adjusted value at current levels. This summary should stand alone as complete investment recommendation suitable for institutional decision-making.]
```

## Synthesis Execution Protocol

### Pre-Execution
1. Validate discovery and analysis data completeness
2. Load discovery insights and analytical results
3. Initialize synthesis frameworks and templates
4. Set confidence thresholds and quality gates

### Main Execution
1. **Investment Thesis Construction**
   - Synthesize core thesis from analytical insights
   - Calculate risk-adjusted returns and conviction scores
   - Generate recommendation with position sizing

2. **Business Intelligence Integration**
   - Synthesize KPI dashboard from discovery data
   - Create financial health scorecard from analysis
   - Generate competitive position summary

3. **Valuation Synthesis**
   - Execute multi-method valuation triangulation
   - Create scenario analysis with probability weighting
   - Generate sensitivity analysis from key variables

4. **Risk Integration**
   - Synthesize quantified risk matrix
   - Integrate risk factors into investment decision
   - Generate mitigation and monitoring strategies

5. **Document Generation**
   - Create complete markdown document
   - Apply consistent formatting and validation
   - Ensure exact template compliance
   - Save to required output location

### Post-Execution
1. Validate output quality against institutional standards
2. Verify file saved to correct location with proper naming
3. Confirm identical format to existing implementation
4. Signal fundamental_analyst_validate readiness
5. Log synthesis performance metrics

## Quality Assurance Protocol

### Output Validation
1. **Structural Compliance**
   - Exact template adherence
   - Proper section hierarchy
   - Consistent table formatting
   - Mandatory metadata inclusion

2. **Content Quality**
   - All confidence scores in 0.0-1.0 format
   - Risk probabilities in decimal format
   - Monetary values with $ formatting
   - Author attribution consistency

3. **File Requirements**
   - Single file output: `TICKER_YYYYMMDD.md`
   - Saved to: `./data/outputs/fundamental_analysis/`
   - Analysis focused solely on requested ticker
   - No additional files generated

4. **Institutional Standards**
   - Publication-ready quality
   - Professional presentation
   - Complete investment framework
   - Actionable recommendations

### Integration Requirements
- Must produce identical output to current fundamental_analysis.md
- Zero functional regression in content quality
- Exact same file format and structure
- Compatible with existing workflow and tools

**Author**: Cole Morton
**Confidence**: [Synthesis confidence will be calculated based on upstream data quality]
**Data Quality**: [Data quality score based on discovery and analysis inputs]
