# Fundamental Analyst Discover Microservice
*DASV Phase 1: Data Acquisition and Context Gathering*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - ticker: string              # Stock symbol (uppercase format)
  - timeframe: string           # Analysis period: 3y|5y|10y|full (default: 5y)
  - peer_count: integer         # Number of peer companies (default: 3-5)

optional_inputs:
  - depth: string               # Analysis depth: summary|standard|comprehensive|deep-dive (default: comprehensive)
  - confidence_threshold: float # Minimum confidence for data: 0.6|0.7|0.8 (default: 0.7)
  - cache_refresh: boolean      # Force cache refresh (default: false)
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: structured_data
    format: json
    confidence_score: float
    location: "/team-workspace/microservices/fundamental_analyst/discover/outputs/{TICKER}_{YYYYMMDD}_discovery.json"

  metadata:
    execution_time: timestamp
    data_sources: array
    quality_metrics: object
    next_phase_ready: boolean
```

### Service Dependencies
- **External APIs**: Yahoo Finance, SEC EDGAR, Economic Data APIs
- **Shared Resources**: Data cache (/data/raw/), Team workspace
- **Upstream Services**: None (initial phase)
- **Downstream Services**: fundamental_analyst_analyze

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

## Company Intelligence Gathering

**1.1 Company Intelligence Discovery**
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

## Execution Protocol

### Pre-Execution
1. Validate input requirements (ticker, timeframe, peer_count)
2. Check data cache for existing information
3. Initialize quality monitoring
4. Load shared context and configuration

### Main Execution
1. Execute Yahoo Finance service data collection
2. Gather company intelligence using systematic discovery
3. Validate data quality and completeness
4. Generate structured output with confidence scores
5. Cache all collected data according to retention policy

### Post-Execution
1. Validate output quality against discovery standards
2. Update shared context with discovered data
3. Signal fundamental_analyst_analyze service readiness
4. Log performance metrics and data sources

## Output Format

The discover microservice generates structured JSON output containing:

```json
{
  "metadata": {
    "command_name": "fundamental_analyst_discover",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "discover",
    "ticker": "TICKER_SYMBOL",
    "confidence_methodology": "detailed_confidence_calculation_explanation",
    "data_dependencies": "complete_dependency_tree_with_freshness"
  },
  "discovery_results": {
    "market_data": {
      "current_price": "float",
      "market_cap": "float",
      "trading_volume": "float",
      "confidence": "0.0-1.0"
    },
    "financial_statements": {
      "income_statement": "object",
      "balance_sheet": "object",
      "cash_flow": "object",
      "confidence": "0.0-1.0"
    },
    "company_intelligence": {
      "business_model": "string",
      "revenue_streams": "array",
      "key_metrics": "object",
      "peer_group": "array",
      "confidence": "0.0-1.0"
    }
  },
  "quality_metrics": {
    "overall_confidence": "0.0-1.0",
    "data_quality_score": "0.0-1.0",
    "completeness_percentage": "0-100",
    "validation_results": "object"
  },
  "next_phase_ready": true
}
```

**Author**: Cole Morton
**Confidence**: [Discovery confidence will be calculated based on data quality and completeness]
**Data Quality**: [Data quality score based on source reliability and freshness]
