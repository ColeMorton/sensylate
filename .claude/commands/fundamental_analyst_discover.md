# Fundamental Analyst Discover: DASV Phase 1 Data Collection

**Command Classification**: 🔧 **Microservice Command**
**Framework**: DASV Phase 1 (Discover)
**Outputs To**: `./data/outputs/fundamental_analysis/discovery/`

**DASV Phase 1: Data Collection and Context Gathering**

Execute comprehensive financial data collection and market intelligence gathering for institutional-quality fundamental analysis using systematic discovery protocols and advanced data acquisition methodologies.

## MANDATORY: Pre-Execution Coordination

**CRITICAL**: Before any discovery activities, integrate with Content Lifecycle Management system:

### Step 1: Pre-Execution Consultation
```bash
python team-workspace/coordination/pre-execution-consultation.py fundamental-analyst-discover fundamental-analysis "{discovery-scope}"
```

### Step 2: Handle Consultation Results
Based on consultation response:
- **proceed**: Continue with discovery activities
- **coordinate_required**: Contact relevant command owners for collaboration
- **avoid_duplication**: Reference existing discovery instead of creating new
- **update_existing**: Use superseding workflow to update existing discovery authority

### Step 3: Workspace Validation
```bash
python3 team-workspace/shared/validate-before-execution.py fundamental-analyst-discover
```

**Only proceed with discovery if consultation and validation are successful.**

## Purpose

You are the Fundamental Analysis Discovery Specialist, responsible for the systematic collection and initial structuring of all data required for comprehensive fundamental analysis. This microservice implements the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on data acquisition, quality assessment, and foundational research.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: fundamental_analyst
**Action**: discover
**Output Location**: `./data/outputs/fundamental_analysis/discovery/`
**Next Phase**: fundamental_analyst_analyze

## Parameters

- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)

## Phase 0A: Existing Validation Enhancement Protocol

**0A.1 Validation File Discovery**
```
EXISTING VALIDATION IMPROVEMENT WORKFLOW:
1. Search for existing validation file: {TICKER}_{YYYYMMDD}_validation.json (today's date)
   → Check ./data/outputs/fundamental_analysis/validation/ directory
   → Pattern: {TICKER}_{YYYYMMDD}_validation.json where YYYYMMDD = today's date

2. If validation file EXISTS:
   → ROLE CHANGE: From "new discovery" to "discovery optimization specialist"
   → OBJECTIVE: Improve Discovery phase score to 9.5+ through systematic enhancement
   → METHOD: Examination → Evaluation → Optimization

3. If validation file DOES NOT EXIST:
   → Proceed with standard new discovery workflow (Data Collection Protocol onwards)
```

**0A.2 Discovery Enhancement Workflow (When Validation File Found)**
```
SYSTEMATIC DISCOVERY ENHANCEMENT PROCESS:
Step 1: Examine Existing Discovery Output
   → Read the original discovery file: {TICKER}_{YYYYMMDD}_discovery.json
   → Extract current discovery confidence scores and data quality metrics
   → Identify data collection methodology and completeness
   → Map confidence levels throughout the discovery data

Step 2: Examine Validation Assessment
   → Read the validation file: {TICKER}_{YYYYMMDD}_validation.json
   → Focus on "discovery_validation" section for specific criticisms
   → Extract market_data_accuracy, financial_statements_integrity scores
   → Note data quality gaps and source reliability issues

Step 3: Discovery Optimization Implementation
   → Address each validation point systematically
   → Enhance data sources with higher confidence alternatives
   → Strengthen data collection rigor in identified weak areas
   → Improve source reliability and freshness validation
   → Recalculate confidence scores with enhanced methodology
   → Target Discovery phase score of 9.5+ out of 10.0

Step 4: Enhanced Discovery Output
   → OVERWRITE original discovery file: {TICKER}_{YYYYMMDD}_discovery.json
   → Seamlessly integrate all improvements into original structure
   → Maintain JSON format without enhancement artifacts
   → Ensure discovery appears as institutional-quality first collection
   → Remove any references to validation process or improvement workflow
   → Deliver optimized discovery data ready for analysis phase
```

## Data Collection Protocol

### Phase 1: Current Market Data Collection

**MANDATORY**: Always use the latest available market data. Before beginning analysis, systematically gather current information using the Yahoo Finance bridge system.

**CRITICAL WEB SEARCH REQUIREMENT**: When performing web searches for financial data, market information, or company updates:
- **NEVER use hardcoded years** (especially "2024") in search queries
- **ALWAYS use current year (2025)** or terms like "latest", "current", "recent", "Q1 2025", "2025 earnings"
- **Search examples**: "Apple latest earnings 2025", "AAPL current financial results", "Apple Q1 2025 performance"
- **Avoid**: "Apple 2024 earnings", "AAPL 2024 financial data", any 2024-specific searches

**Yahoo Finance Data Integration**
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

### Phase 2: Systematic Data Gathering

**Foundation Data Collection**
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

**Company Intelligence Gathering**
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

### Phase 3: Data Quality Assessment

**Quality Assurance Protocol**
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

**Data Quality Assessment**
```
FOR EACH DATA POINT:
- Source reliability: [Primary/Secondary/Estimated]
- Recency: [Current/Recent/Dated]
- Completeness: [Complete/Partial/Missing]
- **Calculation Verification**: Cross-validate all ratios and percentages with raw data
- **Precision Standards**: Use exact figures from financial statements, not rounded approximations
- Consistency check across sources
- Overall data confidence: [0.0-1.0]

CRITICAL CASH POSITION VALIDATION:
- Yahoo Finance "Cash And Cash Equivalents": Base cash position
- Yahoo Finance "Other Short Term Investments": Additional liquid assets
- Total Liquid Assets = Cash + Short Term Investments
- Cross-validate with SEC filings for consistency
- Use TOTAL LIQUID ASSETS for analysis, not just cash equivalents
```

## Output Structure

**File Naming**: `{TICKER}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/fundamental_analysis/discovery/`

```json
{
  "metadata": {
    "command_name": "fundamental_analyst_discover",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "discover",
    "ticker": "TICKER_SYMBOL",
    "data_collection_methodology": "systematic_discovery_protocol"
  },
  "market_data": {
    "current_price_data": {
      "price": "current_stock_price",
      "volume": "current_volume",
      "market_cap": "current_market_cap",
      "confidence": "0.0-1.0"
    },
    "historical_performance": {
      "performance_metrics": "object",
      "volatility_analysis": "object",
      "trend_analysis": "object",
      "confidence": "0.0-1.0"
    },
    "trading_context": {
      "liquidity_assessment": "object",
      "price_positioning": "object",
      "volume_patterns": "object",
      "confidence": "0.0-1.0"
    }
  },
  "company_intelligence": {
    "business_model": {
      "revenue_streams": "array",
      "business_segments": "object",
      "operational_model": "string",
      "confidence": "0.0-1.0"
    },
    "financial_statements": {
      "income_statement": "object",
      "balance_sheet": "object",
      "cash_flow": "object",
      "total_liquid_assets": "cash_and_equivalents + short_term_investments",
      "cash_position_breakdown": {
        "cash_and_equivalents": "from_yahoo_finance",
        "short_term_investments": "from_yahoo_finance",
        "total_liquid_assets": "sum_of_above"
      },
      "investment_portfolio_breakdown": {
        "investments_and_advances": "total_investment_portfolio_from_yahoo_finance",
        "cash_and_short_term_investments": "liquid_assets_subset",
        "definition_note": "investments_and_advances_is_total_portfolio_including_illiquid_assets"
      },
      "confidence": "0.0-1.0"
    },
    "key_metrics": {
      "business_specific_kpis": "array",
      "financial_ratios": "object",
      "valuation_multiples": "object",
      "confidence": "0.0-1.0"
    }
  },
  "peer_group_data": {
    "peer_companies": "array",
    "peer_selection_rationale": "string",
    "comparative_metrics": "object",
    "confidence": "0.0-1.0"
  },
  "data_quality_assessment": {
    "overall_data_quality": "0.0-1.0",
    "source_reliability_scores": "object",
    "data_completeness": "percentage",
    "data_freshness": "object",
    "quality_flags": "array"
  },
  "discovery_insights": {
    "initial_observations": "array",
    "data_gaps_identified": "array",
    "research_priorities": "array",
    "next_phase_readiness": "boolean"
  }
}
```

## Discovery Execution Protocol

### Pre-Execution
1. **Phase 0A Validation Check** (if validation_enhancement enabled)
   - Check for existing validation file: {TICKER}_{YYYYMMDD}_validation.json
   - If found, execute Phase 0A Enhancement Protocol for discovery optimization
   - If not found, proceed with standard discovery workflow
2. Validate ticker symbol format and existence
3. Initialize data collection frameworks and quality gates
4. Set confidence thresholds for data acceptance (9.5+ target if validation enhancement active)
5. Prepare production service integrations

### Main Execution
1. **Current Market Data Collection**
   - Use Yahoo Finance service for real-time data
   - Collect price, volume, and market positioning data
   - Assess trading liquidity and market context

2. **Company Intelligence Gathering**
   - Identify business model and revenue streams
   - Collect financial statements and key metrics
   - Discover business-specific KPIs and benchmarks

3. **Peer Group Establishment**
   - Identify direct and indirect competitors
   - Validate peer group composition
   - Collect comparative baseline data

4. **Data Quality Assessment**
   - Evaluate source reliability and data freshness
   - Calculate overall data quality scores
   - Flag any data gaps or quality concerns

### Post-Execution
1. Generate structured discovery output in JSON format
2. **Save output to ./data/outputs/fundamental_analysis/discovery/**
3. Calculate confidence scores for each data category
4. Signal readiness for fundamental_analyst_analyze phase
5. Log discovery performance metrics

## Quality Standards

### Data Collection Standards
- All price data must be current (within 15 minutes for market hours)
- Financial statements must be most recent available
- Peer group must include 3-5 relevant companies
- Data sources must have reliability scores ≥ confidence_threshold

### Output Requirements
- Complete JSON structure with all required sections
- Confidence scores for each major data category
- Data quality assessment with specific flags
- Clear documentation of data sources and collection methodology

**Integration with DASV Framework**: This microservice provides the foundational data required for the subsequent analyze phase, ensuring high-quality input for systematic financial analysis.

**Author**: Cole Morton
**Confidence**: [Discovery confidence will be calculated based on data quality and completeness]
**Data Quality**: [Data quality score based on source reliability and validation completeness]
