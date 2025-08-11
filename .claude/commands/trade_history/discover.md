# Trade History Discover

**DASV Phase 1: Trading Performance Data Collection and Market Context Gathering**

Comprehensive trading data collection and market intelligence gathering for institutional-quality trading performance analysis using systematic discovery protocols and researcher sub-agent orchestration.

## Purpose

The Trade History Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive trading performance analysis. This specification focuses on **what** trading data and market context is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/scripts/schemas/trade_history_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute trading performance discovery. Ensure output conforms to `/scripts/schemas/trade_history_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: trade_history
**Action**: discover
**Output Location**: `./data/outputs/trade_history/discovery/`
**Next Phase**: trade_history_analyze
**Template Reference**: `./templates/analysis/trade_history_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `portfolio`: Portfolio name or full filename (required)
- `timeframe`: Analysis period - `1m` | `3m` | `6m` | `1y` | `ytd` | `all` (optional, default: all)
- `benchmark`: Benchmark comparison - `SPY` | `QQQ` | `VTI` (optional, default: SPY)
- `confidence_threshold`: Minimum confidence for data quality - `0.9` | `0.95` | `0.99` (optional, default: 0.95)
- `strategy_filter`: Strategy focus - `SMA` | `EMA` | `all` (optional, default: all)

## Data Requirements

### Core Data Categories

**Trading Data Requirements**:
- Complete trade history with entry/exit timestamps and pricing
- Position sizing and direction (long/short) for all trades
- Strategy classification (SMA/EMA) and parameter identification
- Trade status categorization (closed vs active positions)
- Performance metrics (P&L, returns, MFE/MAE, trade quality)
- Trade duration analysis and efficiency metrics

**Market Context Requirements**:
- Benchmark performance data for comparative analysis
- Market volatility environment during trade periods
- Economic context and policy environment correlation
- Sector performance context for traded securities
- Risk-on/risk-off market regime identification

**Portfolio Analysis Requirements**:
- Portfolio composition and exposure analysis
- Risk-adjusted performance measurement
- Strategy effectiveness assessment across timeframes
- Active position monitoring and unrealized P&L tracking
- Trade signal effectiveness and timing analysis

**Fundamental Integration Requirements**:
- Individual security fundamental analysis correlation
- Sector analysis integration for traded securities
- Economic sensitivity analysis for trade performance
- Market regime correlation with strategy effectiveness

### Quality Standards
- **Authoritative Data**: CSV trade data is 100% accurate and authoritative
- **Data Completeness**: All derivable fields must be calculated (no null values for calculable data)
- **Trade Categorization**: Proper separation of closed vs active trades with complete metrics
- **Multi-Source Validation**: Market context data validated across multiple sources
- **Performance Accuracy**: P&L calculations must match CSV source data exactly

## Output Structure and Schema

**File Naming**: `{PORTFOLIO}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/trade_history/discovery/`
**Schema Definition**: `/scripts/schemas/trade_history_discovery_schema.json`

### Required Output Components
- **Authoritative Trade Data**: Complete trade history with proper categorization
- **Market Context**: Benchmark data, volatility environment, economic indicators  
- **Portfolio Analysis**: Composition, risk metrics, performance attribution
- **Fundamental Integration**: Cross-reference with existing fundamental analysis
- **Quality Metrics**: Confidence scores, data completeness, validation results

### Schema Compliance Standards
- All trades properly categorized (closed vs active) with complete data
- Market context integration with multi-source validation
- Statistical adequacy assessment for meaningful analysis
- Integration with existing fundamental and sector analysis data

## Expected Outcomes

### Discovery Quality Targets
- **Trade Data Authority**: 100% accuracy from authoritative CSV source
- **Market Context Quality**: ≥ 95% confidence through multi-source validation
- **Data Completeness**: ≥ 98% across all required trade metrics
- **Integration Coverage**: ≥ 70% correlation with existing analysis data

### Key Deliverables
- Complete trade history analysis with proper closed/active categorization
- Market context integration with benchmark and volatility analysis
- Portfolio composition and risk assessment with active position monitoring
- Strategy effectiveness evaluation with statistical significance testing
- Integration with existing fundamental analysis for traded securities
- Quality assessment with confidence scoring and validation metrics

**Integration with DASV Framework**: This command provides the foundational trading data required for the subsequent analyze phase, ensuring high-quality input for systematic trading performance analysis.

**Author**: Cole Morton