# Trade History Synthesize

**DASV Phase 3: Report Generation and Document Creation**

Comprehensive report generation and document creation for institutional-quality trading performance communication using systematic synthesis protocols and advanced content generation methodologies.

## Purpose

The Trading Performance Synthesis phase represents the systematic integration and presentation of trading data and analysis into professional reports tailored for different audiences. This command provides the requirements for the "Synthesize" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on multi-audience document generation, template compliance, and actionable insight presentation.

**Expected Output Schema**: `/scripts/schemas/trade_history_synthesis_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute trade history synthesis. Ensure output conforms to `/scripts/schemas/trade_history_synthesis_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 3
**Role**: trade_history
**Action**: synthesize
**Output Location**: `./data/outputs/trade_history/`
**Previous Phases**: trade_history_discover, trade_history_analyze
**Next Phase**: trade_history_validate
**Template Reference**: `./templates/synthesis/trade_history_template.md` (report structure awareness)

## Parameters

- `discovery_data`: Discovery phase output (required)
- `analysis_data`: Analysis phase output (required)
- `report_type`: Report generation scope - `internal` | `live` | `historical` | `all` (optional, default: all)
- `audience_level`: Detail level - `executive` | `operational` | `detailed` (optional, default: operational)
- `confidence_threshold`: Minimum confidence for report generation - `0.7` | `0.8` | `0.9` (optional, default: 0.7)

## Synthesis Requirements

**Core Synthesis Standards:**
- Multi-audience report generation (internal, live, historical)
- Template compliance with institutional formatting standards
- Statistical honesty with sample size limitation disclosure
- Finance-grade precision using CSV P&L as authoritative source

**Data Processing Requirements:**
- Comprehensive dataset utilization with proper closed/active trade separation
- Performance metrics calculated exclusively from closed trades
- Portfolio composition analysis including active positions
- Cross-validation against analysis phase outputs

**Quality Standards:**
- Minimum confidence threshold compliance (0.7+ for production grade)
- Template standardization across all report types
- Audience-specific content customization
- Actionable recommendation generation with implementation specificity

## Report Generation Framework

**Multi-Report Architecture:**
- **Internal Trading Report**: Comprehensive operational analysis with executive dashboard and action plans
- **Live Signals Monitor**: Real-time performance monitoring and position tracking for daily followers
- **Historical Performance Report**: Closed positions analysis and pattern identification for performance analysts

**Critical Data Handling Rules:**
- CSV P&L values as authoritative source (±$0.01 tolerance)
- Closed trades only for performance calculations
- Active trades for portfolio composition and risk assessment
- Statistical significance disclosure for small samples

## Implementation Framework

### Execution Requirements
**Primary Tool**: Use `/scripts/trade_history_synthesize.py` as the atomic synthesis tool
**Template System**: Implement standardized report templates with audience customization
**Quality Gates**: Ensure institutional-grade formatting and content accuracy
**Validation Integration**: Cross-check all metrics against analysis phase outputs

### Success Criteria
- Three distinct reports generated with audience-appropriate content
- Template compliance with standardized formatting
- Statistical honesty with transparent limitation disclosure
- Actionable recommendations with specific implementation guidance

## Output Structure and Schema

**File Naming**: `{PORTFOLIO}_{YYYYMMDD}_synthesis.json`
**Location**: `./data/outputs/trade_history/synthesis/`
**Schema Compliance**: Must validate against `/scripts/schemas/trade_history_synthesis_schema.json`

### Expected Synthesis Schema Structure
```json
{
  "portfolio": "live_signals",
  "synthesis_metadata": {
    "execution_timestamp": "2025-08-07T12:00:00Z",
    "confidence_score": 0.75,
    "reports_generated": 3
  },
  "report_outputs": {
    "internal_report": {...},
    "live_monitor": {...},
    "historical_report": {...}
  },
  "quality_assurance": {
    "template_compliance": true,
    "content_accuracy_verified": true
  },
  "next_phase_inputs": {
    "validation_ready": true
  }
}
```

---

*This synthesis phase provides comprehensive report generation for institutional-quality trading assessment and multi-audience communication.*
