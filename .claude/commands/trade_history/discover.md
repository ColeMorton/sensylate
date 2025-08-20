# Trade History Discover

**DASV Phase 1: Trading Performance Data Collection and Market Context Gathering**

Comprehensive trading data collection and market intelligence gathering for institutional-quality trading performance analysis using systematic discovery protocols and production-grade data acquisition methodologies.

## Purpose

The Trading Performance Discovery phase represents the systematic collection and initial structuring of all data required for comprehensive trading performance analysis. This command provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on data acquisition standards, quality assessment criteria, and foundational research requirements.

**Expected Output Schema**: `/{SCRIPTS_BASE}/schemas/trade_history_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute trade history discovery. Ensure output conforms to `/{SCRIPTS_BASE}/schemas/trade_history_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: trade_history
**Action**: discover
**Output Location**: `./{DATA_OUTPUTS}/trade_history/discovery/`
**Next Phase**: trade_history_analyze
**Template Reference**: `./{TEMPLATES_BASE}/analysis/trade_history_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `portfolio`: Portfolio name or full filename (required)
- `timeframe`: Analysis period - `1m` | `3m` | `6m` | `1y` | `ytd` | `all` (optional, default: all)
- `benchmark`: Benchmark comparison - `SPY` | `QQQ` | `VTI` (optional, default: SPY)
- `confidence_threshold`: Minimum confidence for data quality - `0.7` | `0.8` | `0.9` (optional, default: 0.8)
- `strategy_filter`: Strategy focus - `SMA` | `EMA` | `all` (optional, default: all)

## Data Sources and Integration

**Required Data Sources:**
1. **Trade History CSV** - Authoritative portfolio trade data from `/data/raw/trade_history/`
2. **Yahoo Finance CLI** - Market data, benchmarks, and financial context
3. **SEC EDGAR CLI** - Regulatory filings and compliance data (if available)
4. **FRED Economic CLI** - Economic indicators and macroeconomic context

**Integration Requirements:**
- Multi-source data validation with confidence scoring
- Local-first approach for fundamental analysis integration
- Real-time market context with benchmark performance data
- Economic environment assessment for performance correlation

## Data Flow Integration

### Input Requirements
- `portfolio`: Portfolio identifier (required)
- `confidence_threshold`: Data quality threshold (0.7-0.9, default: 0.8)
- Local inventory check for existing fundamental analysis

### Output Integration
**Primary Output**: `./{DATA_OUTPUTS}/trade_history/discovery/{PORTFOLIO}_{YYYYMMDD}_discovery.json`
**Schema Compliance**: Must conform to `/{SCRIPTS_BASE}/schemas/trade_history_discovery_schema.json`
**Downstream Dependencies**:
- trade_history_analyze (next DASV phase)
- twitter_trade_history (social media content generation)
- portfolio_monitoring (trading system health)

## Data Collection Requirements

### Core Data Categories
**Portfolio Intelligence:**
- Trade history CSV data with comprehensive position tracking
- Strategy performance (SMA vs EMA) and signal effectiveness
- Position sizing methodology and portfolio composition
- Trade quality classification and performance attribution

**Market Context:**
- Benchmark performance data with multi-source validation
- Market volatility environment and regime analysis
- Economic indicators and Federal Reserve policy context
- Sector performance trends and relative positioning

**Fundamental Integration:**
- Local fundamental analysis file inventory and integration
- Investment thesis alignment with trading performance
- Price target correlation and recommendation accuracy
- Risk factor identification and catalyst tracking

### Discovery Requirements

**Data Processing Standards:**
- CSV trade data is authoritative and requires no validation
- Portfolio parameter resolution (exact filename vs latest file logic)
- Complete trade categorization (closed vs active positions)
- Comprehensive ticker universe extraction and sector mapping

**Quality Requirements:**
- Minimum confidence threshold compliance (0.7-0.9)
- Local-first approach for fundamental analysis integration
- Multi-source market data validation for institutional quality
- Complete data enhancement for all derivable fields

## Output Structure and Schema

**File Naming**: `{PORTFOLIO}_{YYYYMMDD}_discovery.json`
**Location**: `./{DATA_OUTPUTS}/trade_history/discovery/`
**Schema Compliance**: Must validate against `/{SCRIPTS_BASE}/schemas/trade_history_discovery_schema.json`

### Expected Discovery Schema Structure
```json
{
  "portfolio": "live_signals",
  "discovery_metadata": {
    "execution_timestamp": "2025-08-07T12:00:00Z",
    "confidence_score": 0.85,
    "data_completeness": 95.0
  },
  "authoritative_trade_data": {
    "total_trades": 38,
    "closed_trades": 33,
    "active_trades": 5,
    "strategy_distribution": {...}
  },
  "market_context": {
    "benchmark_data": {...},
    "economic_context": {...}
  },
  "fundamental_integration": {
    "analysis_coverage": {...},
    "integration_quality": {...}
  },
  "data_quality_assessment": {
    "overall_confidence": 0.85,
    "completeness_score": 0.95
  },
  "next_phase_inputs": {
    "analysis_ready": true
  }
}
```

## Implementation Framework

### Execution Requirements
**Primary Tool**: Use `/{SCRIPTS_BASE}/trade_history_discover.py` as the atomic discovery tool
**CLI Services**: Integrate Yahoo Finance CLI, FRED Economic CLI for market context
**Local Data Priority**: Inventory local fundamental analysis files before external calls
**Quality Gates**: Enforce minimum confidence thresholds and schema compliance

### Success Criteria
- Data completeness >95% with full trade categorization
- Market context integration with benchmark validation
- Local fundamental analysis integration where available
- Schema-compliant output ready for analysis phase

---

*This discovery phase establishes the foundation for comprehensive trading performance analysis through systematic data collection, market context integration, and quality-assured data preparation.*
