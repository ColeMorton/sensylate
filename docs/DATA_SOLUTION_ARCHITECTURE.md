# Sensylate Data Solution Architecture Specification

## Executive Summary

The Sensylate platform implements a **contract-driven, local-first data architecture** that combines Python data processing with an Astro frontend. The system prioritizes data freshness, schema consistency, and frontend-first requirements discovery through automated contract generation and validation.

## Core Architecture Principles

### 1. Contract-First Architecture
- **Frontend directory structure** (`frontend/public/data/`) serves as the authoritative source of truth for data requirements
- **Automatic contract discovery** infers schemas from existing CSV files and directory organization
- **Schema validation** ensures data consistency across the pipeline

### 2. Local-First Data Strategy
- **Local data sources** (`data/raw/`) are checked before external API calls
- **Fail-fast approach** with meaningful exceptions instead of fallback mechanisms
- **Cached results** improve performance and reduce external dependencies

### 3. Multi-Modal Processing
- **Python backend** handles data processing, analysis, and external service integration
- **Astro frontend** provides static site generation with dynamic chart rendering
- **CLI wrapper system** enables external service integration and automation

## System Components

### Data Pipeline Manager (`scripts/data_pipeline_manager.py`)

**Purpose**: Core orchestration engine that manages data processing contracts and service execution.

**Key Features**:
- **Contract-based execution**: Processes 11 predefined data contracts
- **Schema validation**: Validates output data against expected schemas with error/warning categorization
- **Service health checks**: Validates CLI service availability before execution
- **Local-first processing**: Checks local data sources before external API calls
- **Quality gates**: Implements comprehensive data quality validation

**Contract Types**:
1. **Portfolio Data**: Multi-strategy and buy-and-hold portfolio metrics
2. **Trade History**: Historical trade data with PnL calculations
3. **Live Signals**: Real-time trading signal equity curves and drawdowns
4. **Open Positions**: Current position tracking and PnL monitoring
5. **Stock Data**: Individual stock price and fundamental analysis

### CLI Wrapper System (`scripts/cli_wrapper.py`)

**Purpose**: Manages external service integration through standardized CLI interfaces.

**Supported Services**:
- `yahoo_finance`: Stock price and fundamental data retrieval
- `alpha_vantage`: Alternative stock data provider
- `trade_history_cli`: Historical trade analysis and processing
- `live_signals_dashboard`: Real-time trading signal processing

**Features**:
- **Health checking**: Validates service availability via `--help` commands
- **Timeout management**: Configurable execution timeouts per service
- **Error handling**: Comprehensive error capture and logging
- **Output validation**: Ensures service outputs meet expected formats

### Data Contract Discovery (`scripts/data_contract_discovery.py`)

**Purpose**: Automatically discovers and validates data contracts from frontend requirements.

**Discovery Process**:
1. **Directory scanning**: Recursively scans `frontend/public/data/` for CSV files
2. **Schema inference**: Analyzes CSV content to determine column types and constraints
3. **Contract generation**: Creates formal contract specifications with quality requirements
4. **Dependency mapping**: Links contracts to appropriate CLI services

**Schema Types Detected**:
- **DateTime**: Multiple format patterns (ISO, YYYY-MM-DD, etc.)
- **Numeric**: Integer and float detection with precision analysis
- **UUID**: Position IDs and standard UUID formats
- **Categorical**: Trading directions, status values, strategy types

### Frontend Data Consumption

**Data Flow**:
```
CSV Files → Data Hooks → Chart Components → Plotly Visualization
```

**Key Components**:
- **`usePortfolioData`** hooks: React hooks for data fetching and caching
- **`PortfolioChart.tsx`**: Main chart rendering component with multiple chart types
- **`ChartDataService.ts`**: Data transformation and processing service

**Chart Types Supported**:
1. **Portfolio Comparisons**: Multi-strategy vs buy-and-hold analysis
2. **Equity Curves**: Time-series portfolio performance tracking
3. **Drawdown Analysis**: Risk assessment and maximum drawdown visualization
4. **Trade Waterfalls**: Individual trade PnL contribution analysis
5. **Position Tracking**: Open and closed position monitoring

## Data Processing Contracts

### Contract Execution Matrix

| Contract ID | Data Source | CLI Service | Output Location | Freshness |
|-------------|-------------|-------------|-----------------|-----------|
| `portfolio_multi_strategy_portfolio_value` | Local + Yahoo | `yahoo_finance` | `frontend/public/data/portfolio/` | 24h |
| `portfolio_multi_strategy_returns` | Local + Yahoo | `yahoo_finance` | `frontend/public/data/portfolio/` | 24h |
| `portfolio_multi_strategy_drawdowns` | Local + Yahoo | `yahoo_finance` | `frontend/public/data/portfolio/` | 24h |
| `portfolio_buy_and_hold_returns` | Local + Yahoo | `yahoo_finance` | `frontend/public/data/portfolio/` | 24h |
| `portfolio_live_signals_equity` | Local + Live Signals | `live_signals_dashboard` | `frontend/public/data/portfolio/live-signals/` | 1h |
| `trade_history_live_signals` | Local + Trade History | `trade_history_cli` | `frontend/public/data/trade-history/` | 6h |
| `trade_history_waterfall_sorted` | Local Processing | Internal | `frontend/public/data/trade-history/` | 6h |
| `open_positions_pnl_current` | Local + Trade History | `trade_history_cli` | `frontend/public/data/open-positions/` | 1h |

### Schema Validation System

**Validation Levels**:
- **ERROR**: Critical schema violations that prevent data usage
- **WARNING**: Non-critical issues that don't break functionality
- **SUCCESS**: Full schema compliance

**Validation Rules**:
1. **Required columns**: Presence of essential columns (Ticker, Date, PnL)
2. **Data type consistency**: Numeric, datetime, and string type validation
3. **Format patterns**: UUID, timestamp, and categorical value format checking
4. **Referential integrity**: Cross-contract data consistency validation

**Ticker Uniqueness Implementation**:
```python
# Waterfall chart requires unique tickers - duplicates numbered by Exit_Timestamp order
# Example: TSLA → TSLA1, TSLA2 (where TSLA1 has older Exit_Timestamp)
for ticker in closed_trades['Ticker'].unique():
    ticker_trades = closed_trades[closed_trades['Ticker'] == ticker].copy()
    ticker_trades = ticker_trades.sort_values('Exit_Timestamp_dt', ascending=True)

    if len(ticker_trades) > 1:
        for i, idx in enumerate(ticker_trades.index.tolist()):
            sequence_number = i + 1
            numbered_ticker = f"{ticker}{sequence_number}"
            closed_trades.loc[idx, 'Ticker'] = numbered_ticker
```

## Quality Assurance Framework

### Data Quality Gates
1. **Schema Validation**: Automated schema compliance checking
2. **Freshness Validation**: Timestamp-based data currency verification
3. **Completeness Validation**: Row count and required column presence
4. **Format Validation**: Data type and pattern consistency checking

### Error Handling Strategy
- **Fail-Fast Approach**: Immediate exception throwing for schema violations
- **Meaningful Exceptions**: Detailed error context with troubleshooting information
- **No Fallback Logic**: Avoids masking data quality issues with degraded functionality
- **Comprehensive Logging**: Detailed operation tracking for debugging

## Service Integration Architecture

### Health Check System
```python
# CLI service validation via --help command execution
def health_check(service_name: str) -> bool:
    result = subprocess.run([service_name, '--help'],
                          capture_output=True, timeout=30)
    return result.returncode == 0
```

### Local Data Priority
1. **Check local sources** (`data/raw/stocks/`) first
2. **Fall back to CLI services** only when local data unavailable
3. **Cache external results** locally for future use
4. **Validate all data** regardless of source

## Performance Characteristics

### Processing Times
- **Full pipeline execution**: ~45-90 seconds (11 contracts)
- **Individual contract processing**: 2-15 seconds
- **Schema validation**: <1 second per contract
- **Frontend data loading**: <500ms per chart type

### Resource Usage
- **Memory footprint**: ~200-500MB during processing
- **Disk space**: ~50MB for complete dataset
- **Network requests**: Minimized through local-first strategy

## Monitoring and Observability

### Success Metrics
- **Contract success rate**: Percentage of contracts processed successfully
- **Schema compliance rate**: Percentage of outputs passing validation
- **Data freshness**: Age of data relative to freshness thresholds
- **Service availability**: CLI service health check success rates

### Failure Scenarios
1. **CLI service unavailability**: Health check failures
2. **Schema validation failures**: Data format inconsistencies
3. **External API failures**: Network or authentication issues
4. **Local data corruption**: File system or format issues

## Development Workflow

### Quality Commands
```bash
# Frontend development
cd frontend/
yarn dev                 # Development server
yarn build               # Production build
yarn check               # TypeScript validation
yarn lint                # Code quality checks

# Python development
make format              # Code formatting (black, isort)
make lint                # Code quality (flake8, mypy)
make test                # Test execution
pre-commit run --all-files  # Complete quality gate
```

### Data Pipeline Execution
```bash
# Full pipeline execution
python scripts/data_pipeline_manager.py

# Contract discovery
python scripts/data_contract_discovery.py

# Individual service testing
python scripts/cli_wrapper.py yahoo_finance --test
```

## Future Architecture Considerations

### Scalability Enhancements
1. **Parallel contract processing**: Concurrent execution of independent contracts
2. **Incremental updates**: Delta processing for large datasets
3. **Distributed processing**: Multi-node execution for complex analysis

### Data Source Expansion
1. **Real-time streaming**: WebSocket integration for live data feeds
2. **Database integration**: PostgreSQL/TimescaleDB for historical data storage
3. **Cloud storage**: S3/GCS integration for large dataset management

### Frontend Enhancements
1. **Real-time updates**: Server-sent events for live chart updates
2. **Interactive filtering**: Dynamic data filtering and aggregation
3. **Export capabilities**: PDF/Excel export for analysis results

---

*Last updated: August 6, 2025*
*Architecture version: 2.1.0*
*Document status: Production*
