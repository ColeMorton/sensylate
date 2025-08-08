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
**Template Reference**: `./templates/analysis/trade_history_template.md` (institutional-quality structure matching fundamental analysis standards)

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
- **MANDATORY Strategic Recommendations section** with quantified optimization targets
- Institutional-quality confidence propagation (target 90%+ for institutional grade)

**Data Processing Requirements:**
- Comprehensive dataset utilization with proper closed/active trade separation
- Performance metrics calculated exclusively from closed trades
- Portfolio composition analysis including active positions
- Cross-validation against analysis phase outputs
- **Complete report structural integrity** (4 required sections minimum)

**Quality Standards:**
- Minimum confidence threshold compliance (0.7+ for production grade, 0.9+ for institutional)
- Template standardization across all report types matching fundamental analysis quality
- Audience-specific content customization with professional presentation
- **Actionable Strategic Recommendations** with implementation timelines and impact quantification
- Comprehensive confidence disclosure and statistical limitations transparency

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

## Strategic Recommendations Framework

**MANDATORY SECTION REQUIREMENTS** (Required for validation compliance):

### Priority Classification System
**🔴 P1 Critical** (Immediate Action Required - Today):
- High-impact risk control issues (e.g., drawdown >-15%)
- Statistical adequacy failures requiring immediate attention
- System integrity breaches demanding instant resolution

**🟡 P2 Priority** (This Week):
- Performance optimization opportunities with quantified impact
- Risk-adjusted metric improvements with specific targets
- Strategy development needs with measurable outcomes

**🟢 P3 Monitor** (Ongoing/Monthly):
- Long-term strategic positioning adjustments
- Quality filter implementations and refinements
- Portfolio diversification and allocation optimizations

### Strategic Recommendations Content Requirements
**Risk Management Enhancement** (Always Required):
- Quantified risk metrics improvement targets (e.g., "Reduce drawdown from -31.22% to -15%")
- Implementation timelines with specific deadlines
- Expected impact calculations with dollar/percentage estimates
- Concrete action items with measurable success criteria

**Performance Optimization** (Always Required):
- Exit efficiency improvements with profit capture estimates
- Strategy allocation optimizations based on statistical significance
- Quality scoring implementations with win rate impact projections
- Risk-adjusted return enhancements with Sharpe ratio targets

**Statistical Validation Enhancements** (When Applicable):
- Sample size adequacy improvements for underdeveloped strategies
- Confidence interval narrowing through additional data collection
- Statistical significance achievement through methodology refinement
- Cross-validation improvements with baseline comparisons

## Implementation Framework

### Execution Requirements
**Primary Tool**: Use `/scripts/trade_history_synthesize.py` as the atomic synthesis tool
**Template System**: Implement institutional-quality templates matching fundamental analysis standards
**Quality Gates**: Ensure institutional-grade formatting and content accuracy (90%+ confidence target)
**Validation Integration**: Cross-check all metrics against analysis phase outputs with fail-fast validation

### Template Compliance Standards (Fundamental Analysis Quality)
**Document Structure Requirements:**
- Professional markdown formatting with consistent hierarchy
- Institutional-quality confidence scoring (0.0-1.0 format throughout)
- Author attribution consistency ("Cole Morton" across all outputs)
- Economic context integration with policy implications
- Risk probabilities in decimal format (0.0-1.0, not percentages)
- Monetary values with proper formatting ($X,XXX.XX with separators)

**Content Quality Standards:**
- Evidence-backed conclusions with statistical support
- Quantified risk assessments with probability/impact matrices
- Implementation timelines with specific deadlines and measurable outcomes
- Confidence intervals with transparent limitation disclosures
- Cross-validation consistency across discovery/analysis/synthesis phases

**Institutional Presentation Requirements:**
- Executive-level dashboard for quick decision-making
- Comprehensive statistical validation with power analysis
- Strategic recommendations with ROI calculations and implementation roadmaps
- Professional-grade formatting suitable for external presentation
- Complete audit trail with data source documentation and methodology transparency

### Success Criteria
- Three distinct reports generated with audience-appropriate content
- **MANDATORY 4-section structural integrity** (Executive Dashboard, P&L Analysis, Win Rate Assessment, Strategic Recommendations)
- Template compliance with institutional-quality formatting matching fundamental analysis standards
- Statistical honesty with transparent limitation disclosure and confidence scoring
- **Strategic Recommendations section with quantified optimization roadmap** and implementation timelines
- Institutional-grade confidence score achievement (target 90%+ for institutional certification)

### Report Structural Requirements (Validation Compliance)
**Section 1: Executive Dashboard** (MANDATORY)
- Portfolio health score with confidence intervals
- Critical issues framework with P1/P2/P3 prioritization
- Key performance metrics with trend indicators
- 30-second brief for executive summary

**Section 2: Comprehensive Performance Analysis** (MANDATORY)
- Complete P&L breakdown with CSV source validation
- Risk-adjusted performance metrics with statistical significance
- Advanced statistical measures with confidence scoring
- Performance attribution with sector/strategy analysis

**Section 3: Statistical Validation and Quality Assessment** (MANDATORY)
- Sample size adequacy with power analysis
- Confidence intervals with transparent limitations
- Cross-validation results with analysis phase consistency
- Quality metrics with institutional standards compliance

**Section 4: Strategic Recommendations and Optimization Roadmap** (MANDATORY)
- Priority-classified action items with quantified targets
- Implementation timelines with specific deadlines
- Expected impact calculations with confidence estimates
- Risk management enhancement with measurable improvements

## Output Structure and Schema

**File Naming**: `{PORTFOLIO}_{YYYYMMDD}_synthesis.json`
**Location**: `./data/outputs/trade_history/synthesis/`
**Schema Compliance**: Must validate against `/scripts/schemas/trade_history_synthesis_schema.json`

### Enhanced Synthesis Schema Structure (DASV Framework Integration)
```json
{
  "portfolio": "live_signals",
  "synthesis_metadata": {
    "execution_timestamp": "2025-08-07T12:00:00Z",
    "confidence_score": 0.90,
    "quality_grade": "institutional",
    "reports_generated": 3,
    "structural_integrity": {
      "sections_found": 4,
      "required_sections": 4,
      "completeness_score": 1.0,
      "strategic_recommendations": true
    }
  },
  "confidence_propagation": {
    "discovery_inherited": 0.90,
    "analysis_inherited": 0.84,
    "synthesis_achieved": 0.90,
    "validation_target": 0.92
  },
  "report_outputs": {
    "internal_report": {
      "executive_dashboard": {...},
      "performance_analysis": {...},
      "statistical_validation": {...},
      "strategic_recommendations": {...}
    },
    "live_monitor": {...},
    "historical_report": {...}
  },
  "quality_assurance": {
    "template_compliance": true,
    "content_accuracy_verified": true,
    "institutional_standards_met": true,
    "fundamental_analysis_quality_achieved": true
  },
  "validation_inputs": {
    "validation_ready": true,
    "structural_integrity_complete": true,
    "confidence_threshold_met": true,
    "strategic_recommendations_included": true
  }
}
```

## DASV Framework Integration Requirements

### Discovery→Analysis→Synthesis Data Flow
**Data Integrity Validation:**
- Cross-validate all statistical calculations between analysis and synthesis phases
- Ensure P&L accuracy propagation with ±$0.01 tolerance from CSV source
- Maintain confidence score consistency with transparent degradation tracking
- Validate sample size adequacy assessments across all phases

**Confidence Propagation Protocol:**
- **Discovery Confidence**: Load and validate discovery phase confidence (typically 0.90+)
- **Analysis Confidence**: Inherit and validate analysis phase confidence (typically 0.84+)
- **Synthesis Target**: Achieve institutional-grade synthesis confidence (0.90+ target)
- **Validation Handoff**: Prepare enhanced confidence for validation phase (0.92+ target)

### Synthesis→Validate Integration
**Validation Readiness Checklist:**
- ✅ All 4 required sections structurally complete
- ✅ Strategic recommendations with quantified targets included
- ✅ Institutional-quality formatting and confidence scoring
- ✅ Cross-phase consistency validation passed
- ✅ Template compliance with fundamental analysis standards achieved

**Enhanced Validation Inputs:**
- Complete structural integrity metadata for validation assessment
- Confidence propagation trail for quality assurance verification
- Strategic recommendations compliance for business logic validation
- Template quality metrics for institutional standards certification

---

*This enhanced synthesis phase provides institutional-quality report generation with comprehensive DASV framework integration for systematic trading assessment and multi-audience communication.*
