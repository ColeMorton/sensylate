# Industry Analyst Discover

**DASV Phase 1: Industry-Wide Data Collection and Context Gathering**

Comprehensive industry-wide data collection and market intelligence gathering for institutional-quality industry analysis using systematic discovery protocols and production-grade CLI data acquisition methodologies.

## Purpose

The Industry Analysis Discovery phase represents the systematic collection and initial structuring of all data required for comprehensive industry analysis. This command provides the requirements for the "Discover" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on industry-wide data acquisition standards, trend analysis requirements, and foundational industry research requirements.

**Expected Output Schema**: `/scripts/schemas/industry_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute industry analysis discovery. Ensure output conforms to `/scripts/schemas/industry_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: industry_analyst
**Action**: discover
**Output Location**: `./data/outputs/industry_analysis/discovery/`
**Next Phase**: industry_analyst_analyze
**Template Reference**: `./templates/analysis/industry_analysis_template.md` (final output structure awareness)

## Parameters

- `industry`: Industry identifier (required) - `software_infrastructure` | `semiconductors` | `consumer_electronics` | `internet_retail` | etc.
- `sector`: Parent sector (optional) - `technology` | `healthcare` | `financials` | `consumer` | etc.
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)

## Data Sources and Integration

**Required Financial Services:**
1. **Yahoo Finance CLI** - Industry performance metrics and representative company analysis
2. **Alpha Vantage CLI** - Real-time industry sentiment and trend validation
3. **FMP CLI** - Industry financial intelligence and competitive landscape data
4. **SEC EDGAR CLI** - Industry regulatory environment and compliance trends
5. **FRED Economic CLI** - Industry economic sensitivity and macroeconomic correlations
6. **CoinGecko CLI** - Risk appetite assessment and technology adoption indicators
7. **IMF CLI** - Global industry context and international expansion potential

**Integration Requirements:**
- Multi-source industry trend validation across financial services
- Automatic cross-validation with confidence scoring and institutional-grade data quality assessment
- Real-time economic context integration with industry sensitivity analysis
- Technology adoption and innovation metrics for competitive analysis
- Production-grade caching and rate limiting for API efficiency
- Comprehensive error handling with graceful degradation and source reliability scoring

## Data Flow Integration

### Input Requirements
- `industry`: Industry identifier (required)
- `sector`: Parent sector classification (optional)
- `confidence_threshold`: Data quality threshold (0.6-0.8, default: 0.7)
- `validation_enhancement`: Optional optimization based on existing validation files

### CLI Services Integration
- **7 Required Services**: Yahoo Finance, Alpha Vantage, FMP, SEC EDGAR, FRED, CoinGecko, IMF
- **Multi-Source Validation**: Cross-validation across industry data sources
- **Economic Context**: Industry-specific economic indicators and correlations
- **Technology Trends**: Innovation metrics and competitive intelligence

### Output Integration
**Primary Output**: `./data/outputs/industry_analysis/discovery/{INDUSTRY}_{YYYYMMDD}_discovery.json`
**Schema Compliance**: Must conform to `/scripts/schemas/industry_analysis_discovery_schema.json`
**Downstream Dependencies**:
- industry_analyst_analyze (next DASV phase)
- twitter_industry_analysis (social media content generation)
- sector_analyst (cross-sector comparative analysis)
- social_media_strategist (industry themes)

## Data Collection Requirements

### Core Data Categories
**Industry Intelligence**:
- Industry scope definition and sub-industry classification
- Market size, growth rates, and competitive landscape
- Technology trends and innovation metrics
- Regulatory environment and compliance requirements

**Representative Companies**:
- Leading companies representing industry dynamics
- Market position and competitive assessment
- Financial performance and operational metrics
- Geographic distribution and market exposure

**Economic Context**:
- Industry-specific economic indicators and correlations
- Interest rate sensitivity and cyclical analysis
- Global economic factors and international exposure
- Policy implications and regulatory trends

**Trend Analysis**:
- Technology adoption and innovation patterns
- Market evolution and competitive dynamics
- Consumer behavior and demand drivers
- Regulatory changes and policy implications

## Output Structure and Schema

**File Naming**: `{INDUSTRY}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/industry_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/industry_analysis_discovery_schema.json`

### Required Output Components
- **Industry Scope**: Industry definition, classification, and boundaries
- **Representative Companies**: Leading companies with selection rationale
- **Trend Analysis**: Technology, market, consumer, and regulatory trends
- **Economic Indicators**: Industry-sensitive economic data and correlations
- **Competitive Landscape**: Market structure and competitive dynamics
- **Quality Metrics**: Confidence scores, data completeness, source reliability

### Schema Compliance Standards
- Minimum 5 CLI services utilized for institutional-grade analysis
- Industry trend consistency validation across multiple sources
- Overall data quality ≥ 0.90 for institutional standards
- Complete industry insights with research priorities identified

## Quality Standards and Requirements

### Pre-Execution Requirements
- Industry identifier format validation and classification
- CLI services configuration and API key validation
- Confidence threshold configuration based on depth parameter
- Optional validation enhancement protocol activation

### Data Quality Standards
**Multi-Source Validation**:
- Industry trend consistency verification across 3+ sources
- Economic indicator correlation validation
- Technology adoption metrics cross-validation
- Competitive landscape data consistency checks

**Institutional-Grade Thresholds**:
- Overall data quality ≥ 0.90
- Service reliability ≥ 80% health score
- Confidence scoring for all major data categories
- Complete data validation with gap identification

### Enhanced Analysis Requirements
- Representative company analysis with 3-15 industry leaders
- Discovery insights with minimum 3 initial observations
- Data gaps identification for next phase planning
- Source reliability scoring for all CLI services

## Security and Implementation Notes

### API Key Security
- API keys stored securely in `./config/financial_services.yaml`
- API keys MUST NEVER be included in discovery outputs or logs
- CLI services automatically access keys from secure configuration
- Output references config file without exposing sensitive information

### Service Reliability
- Dynamic tracking of successful CLI service responses
- Include only services that successfully provided data in output
- Graceful degradation when services are unavailable
- Service health monitoring and performance metrics

## Expected Outcomes

### Discovery Quality Targets
- **Overall Data Quality**: ≥ 97% confidence through multi-source validation
- **Data Completeness**: ≥ 92% across all required categories
- **Industry Trend Confidence**: ≥ 95% with complete trend integration
- **Service Health**: ≥ 80% operational status across all CLI services

### Key Deliverables
- Comprehensive industry scope with classification and boundaries
- Multi-source validated industry trends and competitive dynamics
- Economic context with industry-specific correlations and sensitivity
- Representative company analysis with selection rationale
- Discovery insights identifying research priorities and data gaps
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational data required for the subsequent analyze phase, ensuring high-quality input for systematic industry analysis.

**Author**: Cole Morton
