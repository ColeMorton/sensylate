# Sector Analyst Discover

**DASV Phase 1: Multi-Company Sector Data Collection and Context Gathering**

Comprehensive sector-wide financial data collection and market intelligence gathering for institutional-quality sector analysis with investment recommendation synthesis using systematic discovery protocols and researcher sub-agent orchestration.

## Purpose

The Sector Analysis Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive sector analysis with investment recommendation synthesis. This specification focuses on **what** sector data and multi-company intelligence is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/scripts/schemas/sector_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute sector analysis discovery. Ensure output conforms to `/scripts/schemas/sector_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: sector_analyst
**Action**: discover
**Output Location**: `./data/outputs/sector_analysis/discovery/`
**Next Phase**: sector_analyst_analyze
**Template Reference**: `./templates/analysis/sector_analysis_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `sector`: Sector identifier (required) - `XLK` | `XLF` | `XLE` | `technology` | `financials` | `energy` | etc.
- `companies_count`: Number of sector companies to analyze - `5` | `10` | `15` | `20` (optional, default: 10)
- `market_cap_range`: Market cap filter - `large` | `mid` | `small` | `all` (optional, default: large)
- `include_etfs`: Include sector ETFs in analysis - `true` | `false` (optional, default: true)

### Advanced Parameters
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)
- `economic_context`: Integrate sector-sensitive economic analysis - `true` | `false` (optional, default: true)

## Data Requirements

### Core Data Categories

**Multi-Company Analysis Requirements**:
- Sector company selection based on market cap and liquidity criteria
- Individual company financial performance and competitive positioning
- Cross-company validation and comparative financial metrics
- Revenue diversification and geographic exposure analysis
- Management quality assessment across sector constituents

**Sector ETF Analysis Requirements**:
- Current sector ETF pricing and composition analysis
- Performance correlation validation across sector ETFs
- Cross-sector ETF comparative analysis (all 11 sectors)
- Historical sector rotation patterns and seasonality analysis
- ETF constituent weighting and concentration analysis

**Market Intelligence Requirements**:
- Real-time sector performance vs broader market indices
- Volatility analysis and sector-specific risk assessment
- Interest rate sensitivity and economic cycle positioning
- Dollar strength implications for multinational sector exposure
- Cryptocurrency correlation for sector risk appetite assessment

**Economic Context Requirements**:
- Sector-sensitive economic indicators and correlations
- Federal Reserve policy implications for sector dynamics
- GDP growth correlation and employment sensitivity assessment
- Global economic factors affecting sector international operations
- Regulatory environment and policy risk assessment

### Quality Standards
- **Multi-Company Coverage**: Balanced representation across market cap ranges
- **ETF Price Accuracy**: Current sector ETF prices with <2% variance validation
- **Cross-Sector Context**: Comparative positioning with all 11 sector ETFs
- **Economic Integration**: Sector-specific sensitivity analysis with macroeconomic indicators
- **Statistical Adequacy**: Sufficient sample sizes for meaningful sector analysis

## Output Structure and Schema

**File Naming**: `{SECTOR}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/sector_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/sector_analysis_discovery_schema.json`

### Required Output Components
- **Multi-Company Data**: Individual company analysis with sector aggregated metrics
- **Sector ETF Analysis**: Current ETF pricing, composition, and performance correlation
- **Cross-Sector Analysis**: Comparative positioning with all 11 sector ETFs
- **Economic Context**: Interest rates, GDP sensitivity, and policy implications
- **Market Intelligence**: Volatility analysis, dollar strength sensitivity, risk appetite correlation
- **Quality Metrics**: Confidence scores, data completeness, and source reliability assessment

### Schema Compliance Standards
- Sector company coverage meeting market cap distribution requirements
- Mandatory sector ETF integration with current pricing validation
- Cross-sector comparative framework with relative positioning metrics
- Economic context integration with sector-specific sensitivity analysis

## Expected Outcomes

### Discovery Quality Targets
- **Multi-Company Coverage**: ≥ 90% confidence across sector constituents
- **ETF Integration**: 100% success rate for sector ETF data collection
- **Cross-Sector Analysis**: Complete comparative framework with all 11 sectors
- **Economic Context**: ≥ 95% confidence in macroeconomic integration

### Key Deliverables
- Comprehensive sector company analysis with multi-source validation
- Complete sector ETF analysis with current pricing and composition data
- Cross-sector comparative analysis with relative positioning metrics
- Economic context with sector-specific sensitivity and policy analysis
- Seasonality and historical pattern analysis with 10-year data depth
- Quality assessment with confidence scoring and institutional compliance

**Integration with DASV Framework**: This command provides the foundational sector data required for the subsequent analyze phase, ensuring high-quality input for systematic sector analysis and investment recommendation synthesis.

**Author**: Cole Morton