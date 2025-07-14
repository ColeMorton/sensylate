# Fundamental Analyst Discover Microservice
*DASV Phase 1: Data acquisition and context gathering for financial analysis*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - ticker: string              # Stock symbol for analysis
  - timeframe: string          # Analysis period (3y|5y|10y|full)

optional_inputs:
  - peer_count: integer        # Number of peer companies (default: 4)
  - data_sources: array        # Preferred data source priority
  - confidence_threshold: float # Minimum data confidence (default: 0.7)
  - cache_refresh: boolean     # Force cache refresh (default: false)
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: financial_dataset
    format: json
    confidence_score: float
    completeness_percentage: float

  metadata:
    execution_time: timestamp
    data_sources: array
    quality_metrics: object
    next_phase_ready: boolean
    dependency_tree: object
```

### Service Dependencies
- **Upstream Services**: None (entry point for DASV workflow)
- **Downstream Services**: `fundamental_analyst_analyze`
- **External APIs**: Yahoo Finance, SEC EDGAR, Financial Modeling Prep
- **Shared Resources**:
  - Cache system: `/data/raw/financial_data/`
  - Yahoo Finance service: `scripts/yahoo_finance_service.py`
  - Data outputs: `/data/outputs/financial-data/`

## Data/File Dependencies

### Required External Data
```yaml
input_dependencies:
  required_data:
    - source: "yahoo_finance_service"
      endpoint: "info"
      parameters: {ticker: ticker}
      cache_duration: "15m"
      retry_policy: {attempts: 3, backoff: "exponential"}
      confidence_impact: 0.4

    - source: "yahoo_finance_service"
      endpoint: "financials"
      parameters: {ticker: ticker}
      cache_duration: "24h"
      retry_policy: {attempts: 3, backoff: "exponential"}
      confidence_impact: 0.3

    - source: "yahoo_finance_service"
      endpoint: "history"
      parameters: {ticker: ticker, period: timeframe}
      cache_duration: "1h"
      retry_policy: {attempts: 3, backoff: "exponential"}
      confidence_impact: 0.3

  cache_dependencies:
    - path: "/data/raw/financial_data/fundamentals/{ticker}/"
      type: "json"
      freshness_requirement: "24h"
      fallback_strategy: "api_refresh"
      confidence_impact: 0.2

    - path: "/data/raw/financial_data/pricing/{ticker}/"
      type: "json"
      freshness_requirement: "15m"
      fallback_strategy: "api_refresh"
      confidence_impact: 0.1
```

### Dependency Validation Protocol
```yaml
pre_execution_checks:
  - Validate ticker symbol format and exchange listing
  - Check Yahoo Finance service availability
  - Verify cache system accessibility
  - Confirm rate limiting compliance

runtime_monitoring:
  - Track API call success rates and response times
  - Monitor cache hit ratios and refresh operations
  - Log data quality metrics throughout collection
  - Alert on critical data source failures
```

## Framework Implementation

### Discovery Phase Execution
```yaml
execution_sequence:
  pre_discovery:
    - Validate ticker and parameter inputs
    - Initialize cache system and data collectors
    - Set up rate limiting and retry mechanisms
    - Prepare data quality tracking systems

  main_discovery:
    - Execute Yahoo Finance service calls (parallel)
    - Collect current market data and pricing history
    - Gather financial statements and key ratios
    - Identify and collect peer company data
    - Validate data completeness and quality

  post_discovery:
    - Calculate overall dataset confidence scores
    - Prepare structured output for analysis phase
    - Update cache with fresh data
    - Log performance metrics and data lineage
```

### Quality Assurance Gates
```yaml
data_validation:
  completeness_check:
    - All required financial statements present
    - Pricing data covers requested timeframe
    - Peer group identification successful
    - Key ratios calculable from available data

  accuracy_verification:
    - Cross-validate key metrics across sources
    - Check for data anomalies and outliers
    - Verify currency and unit consistency
    - Confirm data freshness requirements

  confidence_calculation:
    - Weight data sources by reliability
    - Penalize missing or stale data points
    - Factor in API response quality
    - Generate overall confidence score
```

## Output/Generation Standards

### Primary Output Format
```yaml
output_specification:
  file_generation:
    - path_pattern: "/data/raw/financial_data/discovered/{ticker}_{YYYYMMDD}.json"
    - naming_convention: "ticker_timestamp_discovered"
    - format_requirements: "structured_json_with_schema_validation"
    - content_validation: "financial_data_schema_v2"
    - confidence_integration: "metadata_and_data_point_level"

  structured_data:
    - format: "json"
    - schema: "financial_discovery_schema_v2.json"
    - confidence_scores: "0.0-1.0 format at data point level"
    - metadata_requirements: ["data_sources", "collection_timestamp", "quality_metrics"]
```

### Data Structure Template
```json
{
  "ticker": "AAPL",
  "discovery_metadata": {
    "execution_timestamp": "2025-06-29T10:30:00Z",
    "confidence_score": 0.85,
    "data_completeness": 92.5,
    "collection_duration": "45.2s",
    "data_sources_used": ["yahoo_finance", "cache"],
    "cache_hit_ratio": 0.73
  },
  "current_market_data": {
    "price": {
      "current": 192.50,
      "currency": "USD",
      "confidence": 0.95,
      "timestamp": "2025-06-29T10:28:00Z",
      "source": "yahoo_finance_real_time"
    },
    "market_cap": {
      "value": 2856000000000,
      "confidence": 0.90,
      "calculation_method": "shares_outstanding * current_price"
    },
    "trading_metrics": {
      "volume": 45234567,
      "avg_volume_10d": 52341234,
      "confidence": 0.88
    }
  },
  "financial_statements": {
    "income_statement": {
      "annual_data": [
        {
          "fiscal_year": 2024,
          "revenue": 391036000000,
          "gross_profit": 169148000000,
          "operating_income": 123456000000,
          "net_income": 98765000000,
          "confidence": 0.92,
          "source": "yahoo_finance_financials"
        }
      ],
      "quarterly_data": [...],
      "data_confidence": 0.90
    },
    "balance_sheet": {...},
    "cash_flow": {...}
  },
  "peer_comparison": {
    "peers_identified": ["MSFT", "GOOGL", "META", "AMZN"],
    "peer_selection_confidence": 0.85,
    "peer_data": {
      "MSFT": {
        "market_cap": 2234000000000,
        "pe_ratio": 28.5,
        "confidence": 0.88
      }
    }
  },
  "data_quality_assessment": {
    "overall_confidence": 0.87,
    "completeness_score": 0.925,
    "freshness_score": 0.95,
    "source_reliability": 0.90,
    "cross_validation_score": 0.82,
    "missing_data_impact": 0.08,
    "quality_issues": [],
    "improvement_recommendations": [
      "Consider premium data source for enhanced peer comparison",
      "Add earnings call transcript data for qualitative insights"
    ]
  },
  "next_phase_inputs": {
    "analysis_ready": true,
    "required_confidence_met": true,
    "data_package_path": "/data/raw/financial_data/discovered/AAPL_20250629.json",
    "analysis_focus_areas": ["profitability_trends", "competitive_position", "valuation_metrics"]
  }
}
```

## Success Metrics
```yaml
microservice_kpis:
  data_collection:
    - Yahoo Finance service success rate: target >95%
    - Data freshness compliance: target >90%
    - Cache utilization: monitor existing cache system

  quality_metrics:
    - Data completeness: target >90%
    - Overall confidence score: target >0.8
    - Cross-validation accuracy: target >85%
    - Dependency validation success: target 100%

  reliability_metrics:
    - Service execution success: target >95%
    - Error handling effectiveness: target >90%
    - Data consistency validation: target >95%
```

---

*This microservice demonstrates comprehensive data discovery with robust dependency management and quality assurance following the refined microservices architecture.*
