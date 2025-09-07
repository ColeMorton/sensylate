# Bitcoin Cycle Intelligence Discover

**DASV Phase 1: Bitcoin Data Collection and Market Cycle Context Gathering**

Comprehensive Bitcoin data collection and cycle intelligence gathering for institutional-quality Bitcoin market cycle analysis using systematic discovery protocols and researcher sub-agent orchestration.

## Purpose

The Bitcoin Cycle Intelligence Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive Bitcoin cycle analysis. This specification focuses on **what** Bitcoin data is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/{SCRIPTS_BASE}/schemas/bitcoin_cycle_intelligence_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute Bitcoin cycle intelligence discovery. Ensure output conforms to `/{SCRIPTS_BASE}/schemas/bitcoin_cycle_intelligence_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: bitcoin_cycle_intelligence
**Action**: discover
**Output Location**: `./{DATA_OUTPUTS}/bitcoin_cycle_intelligence/discovery/`
**Next Phase**: bitcoin_cycle_intelligence_analyze
**Template Reference**: `./{TEMPLATES_BASE}/analysis/bitcoin_cycle_intelligence_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `analysis_date`: Analysis date for Bitcoin cycle positioning (optional, defaults to current date)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `cycle_timeframe`: Bitcoin cycle analysis period - `current_cycle` | `multi_cycle` | `historical_full` (optional, default: current_cycle)
- `confidence_threshold`: Minimum confidence for Bitcoin data quality - `0.6` | `0.7` | `0.8` | `0.9` (optional, default: 0.8)
- `validation_enhancement`: Enable multi-source validation enhancement - `true` | `false` (optional, default: true)

## Data Requirements

### Core Data Categories

**Bitcoin On-Chain Intelligence Requirements**:
- Complete blockchain metrics and transaction flow analysis
- UTXO age distribution and long-term holder behavior patterns
- Network hash rate, mining economics, and security metrics
- Exchange inflows/outflows and institutional accumulation patterns
- Whale transaction tracking and large holder activity

**Market Cycle Indicator Requirements**:
- Current and historical pricing with multi-source Bitcoin exchange validation
- **MVRV Z-Score: MUST be acquired EXCLUSIVELY via web search from verified on-chain analytics platforms (Glassnode, CryptoQuant, MacroMicro, etc.) - NO API or CLI service usage permitted**
- **Net Unrealized Profit/Loss (NUPL) zones: MUST be acquired EXCLUSIVELY via web search from verified on-chain analytics platforms (Glassnode, CryptoQuant, MacroMicro, etc.) - NO API or CLI service usage permitted**
- PI Cycle Top and Rainbow Price Model calculations (via CLI services)
- Realized price analysis (via CLI services)
- Reserve Risk Indicator and Long-Term Holder supply dynamics (via CLI services)
- Bitcoin market performance across multiple cycle timeframes (via CLI services)

**Economic Context Requirements**:
- Federal Reserve policy impact on Bitcoin as digital asset
- Interest rate sensitivity and Bitcoin correlation with traditional markets
- Global liquidity conditions affecting cryptocurrency adoption
- Institutional adoption patterns and regulatory environment assessment

**Network Health Intelligence Requirements**:
- Mining difficulty adjustments and hash rate security analysis
- Bitcoin network transaction throughput and fee market dynamics
- Lightning Network growth and second-layer development
- Developer activity and protocol upgrade assessment

### Data Acquisition Methodology

**Web Search Requirements (CRITICAL)**:
- **MVRV Z-Score**: Must be acquired using WebSearch tool targeting verified on-chain analytics platforms including but not limited to:
  - Glassnode Studio charts and data
  - CryptoQuant Bitcoin MVRV indicators
  - MacroMicro Bitcoin MVRV Z-Score data
  - Bitcoin Magazine Pro on-chain metrics
  - Any established on-chain analytics platform with current MVRV Z-Score data
- **NUPL (Net Unrealized Profit/Loss)**: Must be acquired using WebSearch tool targeting verified platforms including but not limited to:
  - CryptoQuant Bitcoin NUPL charts
  - Glassnode NUPL indicators
  - MacroMicro Bitcoin NUPL data
  - Bitcoin Magazine Pro NUPL metrics
  - Any established on-chain analytics platform with current NUPL data

**CLI Service Requirements**:
- All other Bitcoin metrics (pricing, network health, mining data, institutional flows) must continue using production CLI services
- Multi-source CLI validation required for price consistency and institutional flows
- CLI service health monitoring for operational reliability

### Quality Standards
- **Multi-Source Validation**: Cross-validation across multiple Bitcoin data sources with confidence scoring
- **Web Search Data Quality**: MVRV Z-Score and NUPL must include source attribution and timestamp validation
- **Institutional-Grade Thresholds**: Overall Bitcoin data quality ≥ 0.90 for institutional standards
- **Data Completeness**: ≥ 85% field population for comprehensive Bitcoin cycle analysis
- **Service Reliability**: ≥ 80% health score across Bitcoin CLI services (excluding web search metrics)

## Output Structure and Schema

**File Naming**: `bitcoin_cycle_{YYYYMMDD}_discovery.json`
**Primary Location**: `./{DATA_OUTPUTS}/bitcoin_cycle_intelligence/discovery/`
**Schema Definition**: `/{SCRIPTS_BASE}/schemas/bitcoin_cycle_intelligence_discovery_schema.json`

### Required Output Components
- **Bitcoin Network Profile**: Blockchain health, network security, mining ecosystem
- **Cycle Analysis**: On-chain metrics, cycle indicators, market position assessment
- **Economic Context**: Federal Reserve indicators, macro factors affecting Bitcoin
- **On-Chain Data**: UTXO analysis, transaction flows, holder behavior patterns
- **Institutional Analysis**: ETF flows, corporate treasury adoption, whale activity
- **Quality Metrics**: Confidence scores, data completeness, source reliability

### Schema Compliance Standards
- **Web Search Attribution**: MVRV Z-Score and NUPL data must include explicit source attribution indicating web search methodology and specific platform sources
- Multi-source Bitcoin CLI data validation targeting high confidence scores for other metrics
- Complete Bitcoin cycle discovery insights with analysis priorities identified
- Institutional-grade quality standards compliance for Bitcoin intelligence
- **Mixed Methodology Documentation**: Clear distinction between web search sourced metrics (MVRV Z-Score, NUPL) and CLI service sourced metrics in output structure

## Expected Outcomes

### Discovery Quality Targets
- **Overall Data Quality**: ≥ 97% confidence through multi-source Bitcoin data validation and web search verification
- **Web Search Metrics Quality**: MVRV Z-Score and NUPL must include current timestamp, source platform attribution, and confidence assessment based on data recency and source authority
- **CLI Metrics Quality**: ≥ 95% confidence for CLI-sourced metrics (pricing, network health, institutional flows)
- **Data Completeness**: ≥ 92% across all required Bitcoin cycle categories (including web search sourced metrics)
- **Service Health**: ≥ 80% operational status across Bitcoin CLI services

### Key Deliverables
- Comprehensive Bitcoin network profile with blockchain intelligence (via CLI services)
- **Web Search Validated Cycle Indicators**: Current MVRV Z-Score and NUPL with source attribution and timestamp validation
- **CLI Validated Metrics**: Multi-source validated pricing, network health, and institutional flow data
- Economic context with Bitcoin-specific macro implications (via CLI services)
- Institutional flow analysis with ETF and corporate adoption patterns (via CLI services)
- Discovery insights identifying Bitcoin cycle analysis priorities and data gaps
- Quality assessment with confidence scoring distinguishing web search vs CLI data source reliability metrics

**Integration with DASV Framework**: This command provides the foundational Bitcoin data required for the subsequent analyze phase, ensuring high-quality input for systematic Bitcoin cycle intelligence analysis.

**Author**: Cole Morton
