# Fundamental Analysis

Generate institutional-quality fundamental analysis with sophisticated reasoning chains, self-validation, and transparent confidence assessments for any stock.

## Purpose

Produces comprehensive fundamental analysis that systematically identifies relevant business metrics, applies multi-perspective evaluation frameworks, and generates risk-adjusted investment recommendations with explicit confidence levels and reasoning transparency.

**Output Format**: Single file `TICKER_YYYYMMDD.md` in `/data/outputs/fundamental_analysis/` directory.

**Focus Requirement**: Analysis must remain strictly focused on the requested ticker symbol. Do not create additional industry or peer analysis files beyond the core fundamental analysis.

## Parameters

- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `peer_count`: Number of peer companies to include (optional, default: 3-5)
- `confidence_threshold`: Minimum confidence for recommendations - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `scenario_count`: Number of valuation scenarios - `3` | `5` | `7` (optional, default: 3)

## Data Management & Caching Strategy

**CACHING ARCHITECTURE**: All downloaded data must be cached in `/data/raw/` with proper versioning and refresh mechanisms to optimize performance and ensure data consistency.

### Caching Directory Structure
```
/data/raw/
├── financial_data/
│   ├── sec_filings/
│   │   ├── {TICKER}/
│   │   │   ├── 10k_{YYYYMMDD}.json
│   │   │   ├── 10q_{YYYYMMDD}.json
│   │   │   └── metadata.json
│   ├── fundamentals/
│   │   ├── {TICKER}/
│   │   │   ├── income_statement_{YYYYMMDD}.json
│   │   │   ├── balance_sheet_{YYYYMMDD}.json
│   │   │   ├── cash_flow_{YYYYMMDD}.json
│   │   │   └── ratios_{YYYYMMDD}.json
│   └── pricing/
│       ├── {TICKER}/
│       │   ├── daily_prices_{YYYYMMDD}.json
│       │   ├── historical_{timeframe}.json
│       │   └── options_{YYYYMMDD}.json
├── economic_data/
│   ├── fred/
│   │   ├── interest_rates_{YYYYMMDD}.json
│   │   ├── gdp_indicators_{YYYYMMDD}.json
│   │   └── inflation_data_{YYYYMMDD}.json
│   ├── bea/
│   │   ├── consumer_spending_{YYYYMMDD}.json
│   │   └── corporate_profits_{YYYYMMDD}.json
│   └── world_bank/
│       ├── global_indicators_{YYYYMMDD}.json
│       └── country_data_{YYYYMMDD}.json
├── alternative_data/
│   ├── sentiment/
│   │   ├── {TICKER}/
│   │   │   ├── social_media_{YYYYMMDD}.json
│   │   │   ├── news_sentiment_{YYYYMMDD}.json
│   │   │   └── earnings_transcript_{YYYYMMDD}.txt
│   ├── patents/
│   │   ├── {TICKER}/
│   │   │   ├── patent_filings_{YYYYMMDD}.json
│   │   │   └── innovation_metrics_{YYYYMMDD}.json
│   └── esg/
│       ├── {TICKER}/
│       │   ├── sustainability_report_{YYYY}.pdf
│       │   ├── cdp_data_{YYYY}.json
│       │   └── employee_reviews_{YYYYMMDD}.json
└── cache_metadata/
    ├── data_sources.json
    ├── refresh_schedule.json
    └── cache_stats.json
```

### Cache Management Protocol
```
CACHE_STRATEGY = {
    "refresh_intervals": {
        "real_time_prices": "15 minutes",
        "daily_fundamentals": "24 hours",
        "sec_filings": "Check daily, cache 90 days",
        "economic_indicators": "Weekly on release schedule",
        "earnings_transcripts": "Quarterly + earnings dates",
        "patent_data": "Monthly",
        "esg_reports": "Annual + sustainability report releases"
    },
    "retention_policy": {
        "pricing_data": "2 years",
        "fundamentals": "10 years",
        "sec_filings": "10 years",
        "economic_data": "20 years",
        "alternative_data": "5 years"
    },
    "validation_checks": {
        "data_integrity": "MD5 hash validation",
        "completeness": "Required field validation",
        "freshness": "Timestamp verification",
        "source_reliability": "API response validation"
    }
}
```

### Cache Implementation Framework
```python
CACHE_IMPLEMENTATION = {
    "pre_analysis_check": {
        "step_1": "Check cache for existing ticker data",
        "step_2": "Validate data freshness based on refresh intervals",
        "step_3": "Identify required data updates",
        "step_4": "Fetch only missing/stale data",
        "step_5": "Update cache with new data"
    },
    "data_retrieval_priority": {
        "cache_hit": "Use cached data if within refresh interval",
        "cache_miss": "Fetch from API, cache result",
        "cache_stale": "Refresh data, update cache",
        "api_failure": "Use last known good cached data with warning"
    },
    "performance_optimization": {
        "parallel_fetching": "Concurrent API calls for different data types",
        "incremental_updates": "Only fetch changed data when possible",
        "compression": "Gzip large datasets in cache",
        "indexing": "Create lookup tables for fast access"
    }
}
```

## Pre-Analysis Evaluation Check

**MANDATORY**: Before starting any new analysis, check for existing analysis improvement opportunities.

### Phase 0A: Existing Analysis Enhancement Protocol

**0A.1 Evaluation File Discovery**
```
EXISTING ANALYSIS IMPROVEMENT WORKFLOW:
1. Search for existing analysis file: TICKER_YYYYMMDD_evaluation.md (today's date)
   → Check /data/outputs/fundamental_analysis/ directory
   → Pattern: {TICKER}_{YYYYMMDD}_evaluation.md where YYYYMMDD = today's date

2. If evaluation file EXISTS:
   → ROLE CHANGE: From "new analysis" to "analysis optimization specialist"
   → OBJECTIVE: Improve Overall Reliability Score to 9+ through systematic enhancement
   → METHOD: Examination → Evaluation → Optimization

3. If evaluation file DOES NOT EXIST:
   → Proceed with standard new analysis workflow (Phase 0 onwards)
```

**0A.2 Analysis Enhancement Workflow (When Evaluation File Found)**
```
SYSTEMATIC ENHANCEMENT PROCESS:
Step 1: Examine Existing Analysis
   → Read the original fundamental analysis file: TICKER_YYYYMMDD.md
   → Extract current Overall Reliability Score and component scores
   → Identify analysis structure, methodology, and conclusions
   → Map confidence levels throughout the analysis

Step 2: Examine Evaluation Assessment
   → Read the evaluation file: TICKER_YYYYMMDD_evaluation.md
   → Understand specific criticisms and improvement recommendations
   → Extract reliability score breakdown and identified weaknesses
   → Note data quality, methodology, and reasoning gaps

Step 3: Optimization Implementation
   → Address each evaluation point systematically
   → Enhance data sources with higher confidence alternatives
   → Strengthen analytical rigor in identified weak areas
   → Improve reasoning chains and evidence backing
   → Recalculate confidence scores with enhanced methodology
   → Target Overall Reliability Score of 9.0+ out of 10.0

Step 4: Production-Ready Analysis Output
   → OVERWRITE original analysis file: TICKER_YYYYMMDD.md
   → Seamlessly integrate all improvements into original structure
   → Maintain professional presentation without enhancement artifacts
   → Ensure analysis appears as institutional-quality first draft
   → Remove any references to evaluation process or improvement workflow
   → Deliver publication-ready fundamental analysis
```

**0A.3 Institutional Quality Standards**
```
PRODUCTION-READY ANALYSIS TARGETS:
- Data Quality: Achieve 9.0+ confidence through verified premium sources
- Methodology Rigor: Implement robust analytical frameworks with cross-validation
- Evidence Backing: Provide quantitative support for all key assertions
- Reasoning Transparency: Document clear logic chains and explicit assumptions
- Risk Assessment: Deliver precise probability estimates with impact quantification
- Competitive Analysis: Present comprehensive moat assessment with industry positioning
- Valuation Confidence: Provide tight ranges through rigorous scenario modeling
- Overall Reliability: Maintain 9.0+ composite score through systematic rigor

INSTITUTIONAL SUCCESS CRITERIA:
□ All evaluation concerns addressed through methodological improvements
□ Analysis reliability score maintains 9.0+ institutional standard
□ Content integrates seamlessly without revealing optimization process
□ Data sources verified through multiple independent channels
□ Reasoning chains supported with quantitative evidence
□ Risk assessments calibrated with observable market metrics
□ Competitive advantages validated through verifiable sources
□ Valuation methods demonstrate internal consistency and external validation
```

**0A.4 Enhanced Methodology Requirements**
```
INSTITUTIONAL DATA VALIDATION PROTOCOL:
- Peer Group Verification: Cross-validate all peer comparisons with independent earnings reports
- Market Position Claims: Verify competitive advantages through OEM relationships and patents
- Catalyst Probabilities: Document methodology for probability estimates using observable metrics
- Financial Metrics: Cross-reference all calculations with multiple data sources
- Industry Dynamics: Validate HHI estimates and market concentration through industry reports
- Forward Projections: Base catalyst impact estimates on verifiable management guidance and trends

TRANSPARENCY ENHANCEMENT REQUIREMENTS:
- Methodology Notes: Specify data sources and calculation methods for all key metrics
- Confidence Attribution: Provide explicit confidence scoring rationale for each analysis section
- Risk Quantification: Support probability estimates with historical precedent and market indicators
- Peer Analysis: Document peer group composition rationale and size/mix adjustments
- Market Research: Reference specific industry reports and third-party validation sources
- Quality Assurance: Include variance analysis between projected and verified financial metrics
```

## Real-Time Data Acquisition

**MANDATORY**: All analysis must use the latest available market data. Before beginning analysis, systematically gather current information using the Yahoo Finance bridge system.

**CRITICAL WEB SEARCH REQUIREMENT**: When performing web searches for financial data, market information, or company updates:
- **NEVER use hardcoded years** (especially "2024") in search queries
- **ALWAYS use current year (2025)** or terms like "latest", "current", "recent", "Q1 2025", "2025 earnings"
- **Search examples**: "Apple latest earnings 2025", "AAPL current financial results", "Apple Q1 2025 performance"
- **Avoid**: "Apple 2024 earnings", "AAPL 2024 financial data", any 2024-specific searches

### Phase 0: Current Market Data Collection

**0.1 Yahoo Finance Data Integration**
```
YAHOO FINANCE DATA COLLECTION - PRODUCTION SERVICE:
Use the Yahoo Finance service class for reliable financial data:

SERVICE CLASS: scripts/yahoo_finance_service.py

1. Stock Quote Data
   → python scripts/yahoo_finance_service.py info TICKER
   → Real-time price, volume, market cap, key ratios
   → Market positioning and trading metrics
   → Automatic validation, retry logic, and caching

2. Historical Analysis
   → python scripts/yahoo_finance_service.py history TICKER [period]
   → Historical price data and performance metrics
   → Volatility analysis and trend identification
   → Comprehensive error handling and data quality validation

3. Financial Statements
   → python scripts/yahoo_finance_service.py financials TICKER
   → Balance sheet, income statement, cash flow data
   → Comprehensive financial statement analysis
   → Production-grade reliability with rate limiting

DATA INTEGRATION APPROACH:
- Use production service for systematic data collection
- Automatic caching with 15-minute TTL for performance
- Rate limiting prevents API abuse (10 requests/minute)
- Comprehensive error handling with specific exception types
- Cross-reference with Claude Desktop Yahoo Finance data when available
- Maintain data quality and freshness standards
```

**0.2 Required Data Points Collection**
```
SYSTEMATIC DATA GATHERING USING PRODUCTION SERVICE:
1. Current Stock Price & Trading Data
   → Use service class for real-time price, volume, market data
   → Extract market cap, shares outstanding, trading volume
   → Calculate 52-week high/low positioning
   → Assess liquidity via average volume comparison

2. Historical Performance Analysis
   → Use service class for historical performance data
   → Calculate relative performance vs benchmarks
   → Extract volatility metrics and beta calculations
   → Analyze price momentum and trend strength

3. Financial Statements & Ratios
   → Use service class for latest financial statements
   → Extract key valuation multiples and ratios
   → Calculate P/E, P/B, EV/EBITDA, P/S, P/FCF ratios
   → Compare metrics to sector medians and historical averages

4. Forward-Looking Data
   → Use available analyst consensus estimates
   → Extract earnings growth projections and guidance
   → Calculate PEG ratios with forward growth estimates
   → Analyze estimate revisions and trends
```

**0.3 Data Validation & Quality Assurance**
```
QUALITY ASSURANCE PROTOCOL:
□ Verify all price data is from current/recent trading sessions
□ Confirm financial statements are most recent available
□ Check data consistency across multiple sources
□ Flag any stale data points requiring refresh
□ Document data collection timestamp for all sources
□ Set confidence scores based on data recency and reliability
□ Validate data integrity and completeness
□ Cross-reference key metrics across sources for accuracy
```
```

## Real-Time Data Integration

### Yahoo Finance Service Data Collection
**MANDATORY**: Always use Yahoo Finance service class for current market data before analysis to ensure accurate valuation assessments.

```
PRODUCTION SERVICE DATA COLLECTION PROTOCOL:
1. Real-Time Quote Data (info command)
   → Current stock price, market cap, trading volume
   → 52-week high/low positioning and trend analysis
   → Key financial ratios and valuation metrics
   → Average volume comparison for liquidity assessment
   → Confidence score: [0.0-1.0] based on data freshness
   → Automatic retry and error handling for reliability

2. Historical Price Analysis (history command)
   → Price performance across multiple timeframes
   → Volatility metrics and return calculations
   → Moving averages and trend analysis
   → Volume-weighted average pricing patterns
   → Cached results for performance optimization

3. Financial Data Integration (financials command)
   → Comprehensive financial statement access
   → Key valuation multiples and ratios
   → Balance sheet, income, and cash flow metrics
   → Update recommendation strength with real-time data
   → Production-grade data validation and quality checks

4. Technical Context Enhancement
   → Support/resistance levels from price history
   → Momentum indicators and trend strength
   → Price action patterns and market sentiment
   → Volume patterns and trading behavior analysis
   → Rate-limited API access for sustainable operations
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

## Output Structure

**File Naming**: `TICKER_YYYYMMDD.md` (e.g., `AAPL_20250617.md`)
**Directory**: `/data/outputs/fundamental_analysis/`

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

## Quality Assurance Protocol

### Pre-Analysis Checks
1. **Data Availability Assessment**
   - Check filing recency and completeness
   - Identify data gaps and alternatives
   - Set confidence thresholds appropriately
   - Prioritize data collection based on materiality

2. **Industry Calibration**
   - Verify industry classification accuracy
   - Update peer group if needed
   - Confirm relevant KPIs for sector
   - Validate industry benchmarks

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

### Phase 0A Execution Validation
1. **Seamless Integration**
   - Enhanced analysis overwrites original file completely
   - No references to evaluation process or improvement workflow
   - No "Enhancement Summary" or before/after comparisons
   - Analysis appears as institutional-quality first draft

2. **Professional Presentation**
   - All improvements integrated naturally into existing structure
   - Methodology transparency without revealing optimization process
   - Enhanced confidence scores presented as original analytical rigor
   - Publication-ready format suitable for institutional distribution

3. **Artifact Removal**
   - No "_enhanced.md" files created
   - No tracking of improvement process in final output
   - No mention of reliability score improvements or evaluation feedback
   - Clean, professional analysis ready for public distribution

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

## Data Source Caching Implementation

### Free Data Source Cache Configuration

```python
FREE_DATA_SOURCES_CACHE = {
    "sec_edgar": {
        "api_endpoint": "https://data.sec.gov/api/",
        "cache_path": "/data/raw/financial_data/sec_filings/",
        "refresh_interval": "24h",
        "rate_limit": "10_req_per_second",
        "data_types": ["10-K", "10-Q", "8-K", "13F", "DEF14A"],
        "retention": "10_years",
        "cache_strategy": "file_per_filing_with_metadata"
    },
    "fred_economic": {
        "api_endpoint": "https://api.stlouisfed.org/fred/",
        "cache_path": "/data/raw/economic_data/fred/",
        "refresh_interval": "weekly_on_release",
        "rate_limit": "unlimited_with_key",
        "data_types": ["GDP", "inflation", "interest_rates", "employment"],
        "retention": "20_years",
        "cache_strategy": "time_series_json_files"
    },
    "financial_modeling_prep": {
        "api_endpoint": "https://financialmodelingprep.com/api/v3/",
        "cache_path": "/data/raw/financial_data/fundamentals/",
        "refresh_interval": "24h",
        "rate_limit": "500MB_per_month",
        "data_types": ["income_statement", "balance_sheet", "cash_flow", "ratios"],
        "retention": "10_years",
        "cache_strategy": "ticker_based_json_hierarchy"
    },
    "polygon_pricing": {
        "api_endpoint": "https://api.polygon.io/v2/",
        "cache_path": "/data/raw/financial_data/pricing/",
        "refresh_interval": "15min_for_prices_24h_for_fundamentals",
        "rate_limit": "5_req_per_minute",
        "data_types": ["daily_prices", "historical_data", "technical_indicators"],
        "retention": "2_years",
        "cache_strategy": "date_partitioned_json"
    },
    "world_bank": {
        "api_endpoint": "https://api.worldbank.org/v2/",
        "cache_path": "/data/raw/economic_data/world_bank/",
        "refresh_interval": "monthly",
        "rate_limit": "unlimited",
        "data_types": ["global_indicators", "country_data", "development_metrics"],
        "retention": "20_years",
        "cache_strategy": "indicator_based_json_files"
    },
    "uspto_patents": {
        "api_endpoint": "https://developer.uspto.gov/",
        "cache_path": "/data/raw/alternative_data/patents/",
        "refresh_interval": "monthly",
        "rate_limit": "varies_by_endpoint",
        "data_types": ["patent_applications", "grants", "assignments"],
        "retention": "permanent",
        "cache_strategy": "company_based_json_with_indexing"
    }
}
```

### Cache Performance Optimization

```python
CACHE_OPTIMIZATION_STRATEGY = {
    "parallel_processing": {
        "concurrent_api_calls": "Max 5 simultaneous connections per source",
        "batch_processing": "Group related data requests",
        "async_refresh": "Background cache updates during analysis"
    },
    "storage_optimization": {
        "compression": "Gzip JSON files >100KB",
        "indexing": "Create lookup tables for fast access",
        "partitioning": "Date/ticker-based directory structure"
    },
    "reliability_measures": {
        "fallback_strategy": "Use last known good cache on API failure",
        "integrity_checks": "MD5 hash validation on cache reads",
        "redundancy": "Mirror critical data across cache tiers"
    },
    "performance_monitoring": {
        "cache_hit_ratio": "Target >80% for repeat analysis",
        "api_call_reduction": "Target <20% of full refresh per analysis",
        "storage_efficiency": "Monitor cache size vs. usage patterns"
    }
}
```

### Cache Maintenance Schedule

```python
AUTOMATED_CACHE_MAINTENANCE = {
    "daily_tasks": [
        "Check SEC EDGAR for new filings",
        "Refresh pricing data for active tickers",
        "Validate cache integrity for critical data",
        "Clean up temporary processing files"
    ],
    "weekly_tasks": [
        "Update FRED economic indicators",
        "Refresh fundamentals for active analysis tickers",
        "Compress and archive older cache data",
        "Generate cache performance reports"
    ],
    "monthly_tasks": [
        "Full patent database updates",
        "World Bank indicator refresh",
        "Cache storage optimization",
        "Purge expired data per retention policies"
    ],
    "quarterly_tasks": [
        "Earnings season cache preparation",
        "Full data source validation",
        "Cache schema updates",
        "Performance benchmark analysis"
    ]
}
```

## Key Implementation Notes

### User-Facing Features
1. **Single File Output**: Always generate exactly one file named `TICKER_YYYYMMDD.md`
2. **Ticker Focus**: Analyze only the requested ticker - no additional industry files
3. **Quantitative Framework**: Include confidence scores (0.0-1.0) throughout analysis
4. **Risk-Adjusted Approach**: Use probability-weighted scenarios and sensitivity ranges
5. **Data Quality Transparency**: Clear confidence levels and data source attribution
6. **Current Data Requirement**: Always use current year (2025) data - never search for or reference 2024 data unless specifically comparing historical performance
7. **Institutional Standards**: When Phase 0A protocol applies, seamlessly integrate improvements without enhancement artifacts
8. **Production Quality**: Deliver publication-ready analysis that appears as institutional first draft

### Technical Implementation (Invisible to User)
9. **Cache-First Strategy**: Check cache before API calls, refresh only stale data
10. **Performance Optimization**: Target >80% cache hit ratio for repeat analysis
11. **Data Integrity**: MD5 validation and consistency checks across cached sources
12. **Intelligent Refresh**: Refresh intervals optimized per data type and source reliability
13. **Background Processing**: All caching operations happen transparently
14. **Enhancement Integration**: When Phase 0A applies, overwrite original file maintaining seamless professional presentation

This enhanced framework ensures institutional-quality analysis with transparent reasoning, quantified confidence levels, and actionable insights suitable for sophisticated investment decision-making. All performance optimizations through caching operate invisibly to provide fast, reliable analysis without exposing technical implementation details to the end user.
