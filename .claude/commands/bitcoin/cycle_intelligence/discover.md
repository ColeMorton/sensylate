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
- MVRV Z-Score, PI Cycle Top, and Rainbow Price Model calculations
- Realized price analysis and Net Unrealized Profit/Loss (NUPL) zones
- Reserve Risk Indicator and Long-Term Holder supply dynamics
- Bitcoin market performance across multiple cycle timeframes

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

### Quality Standards
- **Multi-Source Validation**: Cross-validation across multiple Bitcoin data sources with confidence scoring
- **Institutional-Grade Thresholds**: Overall Bitcoin data quality ≥ 0.90 for institutional standards
- **Data Completeness**: ≥ 85% field population for comprehensive Bitcoin cycle analysis
- **Service Reliability**: ≥ 80% health score across Bitcoin data services

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
- Multi-source Bitcoin data validation targeting high confidence scores
- Complete Bitcoin cycle discovery insights with analysis priorities identified
- Institutional-grade quality standards compliance for Bitcoin intelligence

## Expected Outcomes

### Discovery Quality Targets
- **Overall Data Quality**: ≥ 97% confidence through multi-source Bitcoin data validation
- **Data Completeness**: ≥ 92% across all required Bitcoin cycle categories
- **On-Chain Data Confidence**: ≥ 95% with complete blockchain metrics integration
- **Service Health**: ≥ 80% operational status across Bitcoin data services

### Key Deliverables
- Comprehensive Bitcoin network profile with blockchain intelligence
- Multi-source validated on-chain metrics and cycle indicators
- Economic context with Bitcoin-specific macro implications
- Institutional flow analysis with ETF and corporate adoption patterns
- Discovery insights identifying Bitcoin cycle analysis priorities and data gaps
- Quality assessment with confidence scoring and Bitcoin data source reliability metrics

**Integration with DASV Framework**: This command provides the foundational Bitcoin data required for the subsequent analyze phase, ensuring high-quality input for systematic Bitcoin cycle intelligence analysis.

**Author**: Cole Morton
