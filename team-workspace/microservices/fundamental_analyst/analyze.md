# Fundamental Analyst Analyze Microservice
*DASV Phase 2: Systematic Analysis and Evaluation*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - discovery_data: object        # Output from fundamental_analyst_discover
  - ticker: string               # Stock symbol (uppercase format)
  - confidence_threshold: float  # Minimum confidence requirement (default: 0.7)

optional_inputs:
  - peer_comparison: boolean     # Include peer analysis (default: true)
  - risk_analysis: boolean       # Include detailed risk assessment (default: true)
  - scenario_count: integer      # Number of scenarios to model (default: 3)
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: structured_data
    format: json
    confidence_score: float
    location: "/team-workspace/microservices/fundamental_analyst/analyze/outputs/{TICKER}_{YYYYMMDD}_analysis.json"

  metadata:
    execution_time: timestamp
    data_sources: array
    quality_metrics: object
    next_phase_ready: boolean
```

### Service Dependencies
- **Upstream Services**: fundamental_analyst_discover
- **Downstream Services**: fundamental_analyst_synthesize
- **External APIs**: None (uses discovery data)
- **Shared Resources**: Team workspace, cached discovery data

## Multi-Dimensional Analysis Framework

### Financial Health Analysis

**2.1 Profitability Analysis**
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

### Growth Driver Analysis

**3.1 Historical Growth Decomposition**
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

### Risk Factor Quantification

**3.2 Risk Assessment Matrix**
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

### Valuation Analysis Foundation

**4.1 Valuation Preparation**
```
TRIANGULATION APPROACH PREPARATION:
1. DCF Model Inputs
   → Revenue scenario building (bear/base/bull + variants)
   → Margin progression modeling framework
   → Terminal value assumption development
   → WACC calculation components
   → Sensitivity analysis preparation

2. Relative Valuation Setup
   → Peer group validation and adjustments
   → Multiple regression analysis preparation
   → Industry-specific metric identification
   → Historical multiple analysis
   → Fair value multiple estimation

3. Sum-of-Parts Foundation (if applicable)
   → Business segment identification
   → Hidden asset discovery
   → Spin-off value assessment
   → Conglomerate discount analysis
```

### Financial Metrics Calculation

**Key Ratio Analysis**
```
SYSTEMATIC RATIO CALCULATION:
Profitability Ratios:
- Gross Profit Margin = (Revenue - COGS) / Revenue
- Operating Margin = Operating Income / Revenue
- Net Margin = Net Income / Revenue
- ROE = Net Income / Shareholders' Equity
- ROA = Net Income / Total Assets
- ROIC = NOPAT / Invested Capital

Liquidity Ratios:
- Current Ratio = Current Assets / Current Liabilities
- Quick Ratio = (Current Assets - Inventory) / Current Liabilities
- Cash Ratio = Cash & Equivalents / Current Liabilities

Leverage Ratios:
- Debt-to-Equity = Total Debt / Total Equity
- Interest Coverage = EBIT / Interest Expense
- Debt Service Coverage = Operating Cash Flow / Total Debt Service

Efficiency Ratios:
- Asset Turnover = Revenue / Average Total Assets
- Inventory Turnover = COGS / Average Inventory
- Receivables Turnover = Revenue / Average Accounts Receivable

Valuation Ratios:
- P/E Ratio = Price per Share / EPS
- P/B Ratio = Price per Share / Book Value per Share
- EV/EBITDA = Enterprise Value / EBITDA
- P/S Ratio = Market Cap / Revenue
- PEG Ratio = P/E Ratio / Earnings Growth Rate
```

## Execution Protocol

### Pre-Execution
1. Validate discovery data completeness and quality
2. Load peer group data and industry benchmarks
3. Initialize analytical frameworks
4. Set confidence thresholds for analysis phases

### Main Execution
1. Execute financial health analysis using discovery data
2. Perform competitive position assessment
3. Analyze growth drivers and historical patterns
4. Quantify risk factors across categories
5. Calculate comprehensive financial metrics
6. Prepare valuation model inputs
7. Generate confidence scores for all analysis components

### Post-Execution
1. Validate analysis quality against standards
2. Cross-check internal consistency of metrics
3. Update shared context with analytical insights
4. Signal fundamental_analyst_synthesize readiness
5. Log performance metrics and confidence levels

## Output Format

The analyze microservice generates structured JSON output containing:

```json
{
  "metadata": {
    "command_name": "fundamental_analyst_analyze",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "analyze",
    "ticker": "TICKER_SYMBOL",
    "confidence_methodology": "detailed_confidence_calculation_explanation",
    "data_dependencies": "discovery_data_with_freshness"
  },
  "analysis_results": {
    "financial_health": {
      "profitability_metrics": "object",
      "liquidity_metrics": "object",
      "leverage_metrics": "object",
      "efficiency_metrics": "object",
      "confidence": "0.0-1.0"
    },
    "competitive_position": {
      "market_position": "object",
      "competitive_advantages": "object",
      "innovation_metrics": "object",
      "confidence": "0.0-1.0"
    },
    "growth_analysis": {
      "historical_growth": "object",
      "growth_drivers": "array",
      "management_credibility": "object",
      "confidence": "0.0-1.0"
    },
    "risk_assessment": {
      "risk_matrix": "object",
      "aggregate_risk_score": "float",
      "mitigation_strategies": "array",
      "confidence": "0.0-1.0"
    },
    "valuation_inputs": {
      "dcf_model_inputs": "object",
      "relative_valuation_setup": "object",
      "sum_of_parts_foundation": "object",
      "confidence": "0.0-1.0"
    }
  },
  "quality_metrics": {
    "overall_confidence": "0.0-1.0",
    "analysis_completeness": "0-100",
    "internal_consistency": "0.0-1.0",
    "validation_results": "object"
  },
  "next_phase_ready": true
}
```

## Quality Assurance Standards

### Analysis Validation
- All financial metrics cross-validated against multiple sources
- Peer comparisons adjusted for size and business mix differences
- Risk assessments calibrated with observable market metrics
- Growth projections anchored in historical performance patterns
- Confidence scores reflect methodology rigor and data quality

### Consistency Checks
- Internal ratio consistency (e.g., ROE = ROA × Equity Multiplier)
- Temporal consistency in trend analysis
- Cross-sectional consistency with peer group
- Logical consistency between risk assessment and financial health

### Evidence Requirements
- Quantitative support for all key assertions
- Clear methodology documentation for calculations
- Explicit confidence attribution for each analysis section
- Data source validation and quality assessment

**Author**: Cole Morton
**Confidence**: [Analysis confidence will be calculated based on data quality and methodology rigor]
**Data Quality**: [Data quality score based on discovery data and analytical validation]
