# Industry Analyst Discover

**DASV Phase 1: Industry-Wide Data Collection and Context Gathering**

Comprehensive industry-wide data collection and market intelligence gathering for institutional-quality industry analysis using systematic discovery protocols and researcher sub-agent orchestration.

## Purpose

The Industry Analysis Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive industry analysis. This specification focuses on **what** industry-wide data and competitive intelligence is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

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

### Core Parameters
- `industry`: Industry identifier (required) - `software_infrastructure` | `semiconductors` | `consumer_electronics` | `internet_retail` | etc.
- `sector`: Parent sector (optional) - `technology` | `healthcare` | `financials` | `consumer` | etc.
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)

## Data Requirements

### Core Data Categories

**Industry Intelligence Requirements**:
- Industry scope definition and sub-industry classification framework
- Market size estimation and growth rate analysis across timeframes
- Technology trend identification and innovation pattern analysis
- Regulatory environment assessment and compliance requirement analysis
- Competitive landscape structure and market concentration metrics

**Representative Company Requirements**:
- Leading company identification representing industry dynamics
- Market position assessment and competitive advantage analysis
- Financial performance evaluation and operational efficiency metrics
- Geographic distribution mapping and international market exposure
- Innovation pipeline analysis and R&D investment patterns

**Economic Context Requirements**:
- Industry-specific economic sensitivity and correlation analysis
- Interest rate impact assessment and cyclical behavior patterns
- Global economic factor influence and international trade implications
- Policy impact analysis and regulatory change sensitivity
- Supply chain dynamics and cost structure analysis

**Trend Analysis Requirements**:
- Technology adoption patterns and innovation diffusion analysis
- Market evolution assessment and competitive dynamic shifts
- Consumer behavior analysis and demand driver identification
- Regulatory change impact and policy implication assessment
- Disruption risk evaluation and competitive threat analysis

### Quality Standards
- **Industry Coverage**: Comprehensive industry scope with clear boundary definition
- **Representative Sample**: Balanced selection of industry-leading companies
- **Trend Validation**: Multi-source validation of industry trend analysis
- **Economic Integration**: Industry-specific economic correlation assessment
- **Competitive Intelligence**: Thorough market structure and competitive analysis

## Output Structure and Schema

**File Naming**: `{INDUSTRY}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./data/outputs/industry_analysis/discovery/`
**Schema Definition**: `/scripts/schemas/industry_analysis_discovery_schema.json`

### Required Output Components
- **Industry Scope**: Industry definition, classification, and boundary framework
- **Representative Companies**: Leading companies with selection rationale and analysis
- **Trend Analysis**: Technology, market, consumer, and regulatory trend assessment
- **Economic Indicators**: Industry-sensitive economic data and correlation analysis
- **Competitive Landscape**: Market structure and competitive dynamic evaluation
- **Quality Metrics**: Confidence scores, data completeness, and source reliability assessment

### Schema Compliance Standards
- Industry classification with clear scope and boundary definitions
- Representative company analysis with selection rationale and competitive positioning
- Trend analysis with multi-source validation and confidence measurement
- Economic context integration with industry-specific sensitivity assessment

## Expected Outcomes

### Discovery Quality Targets
- **Industry Definition**: ≥ 95% confidence in scope and classification accuracy
- **Company Representation**: ≥ 90% confidence in industry leadership coverage
- **Trend Analysis**: ≥ 85% confidence in trend identification and validation
- **Economic Integration**: ≥ 88% confidence in economic correlation analysis

### Key Deliverables
- Comprehensive industry scope with classification and competitive framework
- Representative company analysis with competitive positioning and market dynamics
- Technology and market trend analysis with innovation pattern identification
- Economic context with industry-specific correlation and sensitivity assessment
- Competitive landscape evaluation with market structure and concentration analysis
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational industry data required for the subsequent analyze phase, ensuring high-quality input for systematic industry analysis.

**Author**: Cole Morton
