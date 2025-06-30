# Fundamental Analysis Full

**Complete DASV Workflow for Fundamental Analysis**

Execute the complete DASV (Discover → Analyze → Synthesize → Validate) microservice workflow for comprehensive fundamental analysis with institutional-quality investment recommendations.

## Purpose

This command orchestrates the complete fundamental analysis microservice workflow, executing all four DASV phases sequentially to produce institutional-quality fundamental analysis with comprehensive investment recommendations.

## Workflow Integration

**Framework**: DASV Complete Workflow
**Microservices**: 4 sequential phases
**Output Location**: `./data/outputs/fundamental_analysis/`
**Quality Standard**: Institutional-grade fundamental analysis

## Parameters

- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for recommendations - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `scenario_count`: Number of valuation scenarios - `3` | `5` | `7` (optional, default: 3)

## DASV Workflow Execution

### Phase 1: Discover (fundamental_analyst_discover)
**Data Collection and Context Gathering**

Execute comprehensive data collection and foundational research:
- Current market data via Yahoo Finance service
- Financial statements and key metrics
- Business model and competitive landscape
- Peer group establishment and benchmarking

**Output**: Structured discovery data in JSON format
**Duration**: ~20s
**Next Phase**: Analyze

### Phase 2: Analyze (fundamental_analyst_analyze)
**Systematic Analysis and Evaluation**

Execute comprehensive systematic analysis:
- Financial health assessment (4-dimensional scorecard)
- Competitive position and moat analysis
- Growth driver identification and risk quantification
- Valuation model input preparation

**Input**: Discovery data from Phase 1
**Output**: Comprehensive analysis data in JSON format
**Duration**: ~40s
**Next Phase**: Synthesize

### Phase 3: Synthesize (fundamental_analyst_synthesize)
**Integration and Recommendation Generation**

**CRITICAL PHASE**: Generate institutional-quality investment analysis:
- Investment thesis construction and recommendation
- Multi-method valuation synthesis and scenario analysis
- Risk integration and sensitivity analysis
- Professional document generation

**Input**: Discovery and analysis data from Phases 1-2
**Output**: `./data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md`
**Duration**: ~30s
**Next Phase**: Validate
**Quality Requirement**: Institutional-grade fundamental analysis with professional presentation

### Phase 4: Validate (fundamental_analyst_validate)
**Quality Assurance and Confidence Verification**

Execute comprehensive validation and quality assurance:
- Financial metrics cross-validation with primary sources
- Investment thesis coherence and logic verification
- Confidence score format compliance and methodology assessment
- Institutional quality standards verification

**Input**: Generated analysis document from Phase 3
**Output**: Validation report in JSON format
**Duration**: ~25s
**Final Phase**: Complete workflow

## Execution Protocol

### Pre-Execution Validation
```python
# Load collaboration engine and validate microservice availability
from team_workspace.shared.collaboration_engine import CollaborationEngine

engine = CollaborationEngine()
dasv_workflow = engine.execute_dasv_workflow("fundamental_analyst", ticker=ticker)

if dasv_workflow["status"] != "ready_for_execution":
    raise RuntimeError(f"DASV workflow not ready: {dasv_workflow.get('error', 'Unknown error')}")
```

### Sequential Execution
```python
# Execute DASV phases sequentially
phases = ["discover", "analyze", "synthesize", "validate"]
results = {}

for phase in phases:
    command_name = f"fundamental_analyst_{phase}"

    # Load microservice
    microservice_info = engine.discover_command(command_name)
    if not microservice_info:
        raise RuntimeError(f"Microservice not found: {command_name}")

    # Execute phase with dependency data
    context, missing_deps = engine.resolve_dependencies(command_name)

    # Execute microservice logic
    # [Phase-specific execution logic would go here]

    # Store phase results
    results[phase] = {
        "status": "completed",
        "output_location": f"/team-workspace/microservices/fundamental_analyst/{phase}/outputs/",
        "confidence": "calculated_confidence_score",
        "next_phase_ready": True
    }

# Validate final output
final_file = f"./data/outputs/fundamental_analysis/{ticker}_{datetime.now().strftime('%Y%m%d')}.md"
if not os.path.exists(final_file):
    raise RuntimeError(f"Final analysis document not generated: {final_file}")
```

### Post-Execution Validation
```python
# Verify output requirements
validation_checks = [
    f"File exists: {final_file}",
    f"File location correct: ./data/outputs/fundamental_analysis/",
    f"File naming correct: {ticker}_YYYYMMDD.md",
    f"All DASV phases completed successfully",
    f"Validation report generated"
]

for check in validation_checks:
    # Perform validation
    pass

print(f"✅ DASV workflow completed successfully")
print(f"📄 Analysis document: {final_file}")
print(f"🔍 Validation report: {results['validate']['output_location']}")
```

## Quality Standards

### Output Requirements
- **File Output**: `./data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md`
- **Content Quality**: Institutional-grade investment analysis
- **Format Compliance**: Professional presentation with 0.0-1.0 confidence scoring
- **Author Attribution**: Consistent "Cole Morton" attribution

### Success Criteria
```
QUALITY ASSURANCE CHECKLIST:
□ All four DASV phases execute successfully
□ Comprehensive discovery data collection with 90%+ completeness
□ **CRITICAL: All financial calculations verified against Yahoo Finance exactly**
□ Rigorous financial analysis with institutional-grade methodology and enhanced risk assessment
□ Professional synthesis with consistent financial data usage and actionable investment recommendations
□ **CRITICAL: DAS output identical to fundamental_analysis.md command**
□ Content evaluator score 8.5+ minimum target
□ Complete audit trail with all phase outputs in ./data directory
□ Institutional-quality analysis maintained
□ All validation checks pass
□ Professional presentation standards met
```

## Performance Characteristics

**Total Estimated Duration**: 115 seconds
**Phase Breakdown**:
- Discover: 20s (data collection)
- Analyze: 40s (systematic analysis)
- Synthesize: 30s (document generation)
- Validate: 25s (quality assurance)

**Optimization Strategies**:
- Parallel data validation in discover phase
- Cached peer group data reuse
- Template-driven document generation
- Efficient microservice data passing

## Error Handling

### Fail-Fast Approach
- **Discovery Failure**: Stop execution if data quality below threshold
- **Analysis Failure**: Stop execution if confidence thresholds not met
- **Synthesis Failure**: Stop execution if document generation fails
- **Validation Failure**: Report issues but preserve generated document

### Enhanced Quality Gates
- **Pre-Phase**: Validate inputs and dependencies with data consistency checks
- **Critical Calculation Gate**: All margins/ratios must match Yahoo Finance exactly before proceeding
- **Inter-Phase**: Verify data flow, financial data consistency, and confidence maintenance
- **Critical Error Detection**: Flag calculation errors (e.g. 11.9% vs 10.3%) as blocking errors
- **Post-Phase**: Confirm expected outputs generated with quality score ≥8.5

## Usage Examples

```bash
# Standard comprehensive analysis (produces TICKER_YYYYMMDD.md)
/fundamental_analysis_full AAPL

# Deep dive with high confidence requirement
/fundamental_analysis_full MSFT depth=deep-dive confidence_threshold=0.8

# Quick summary with extended timeframe
/fundamental_analysis_full GOOGL depth=summary timeframe=10y

# Full analysis with extra scenarios
/fundamental_analysis_full TSLA scenario_count=7 timeframe=full
```

## Integration Notes

### Microservice Discovery
The workflow automatically discovers and validates all required microservices:
- `fundamental_analyst_discover`
- `fundamental_analyst_analyze`
- `fundamental_analyst_synthesize`
- `fundamental_analyst_validate`

### Data Flow Management
- **Phase 1 → 2**: Discovery data feeds into analysis
- **Phases 1,2 → 3**: Combined data feeds into synthesis
- **Phase 3 → 4**: Generated document feeds into validation
- **All Phases**: Confidence and quality metrics maintained throughout

### Collaboration Integration
- Uses enhanced collaboration engine for microservice orchestration
- Integrates with team workspace for output management
- Provides systematic DASV workflow execution
- Delivers institutional-quality investment analysis

**This command represents the complete microservice implementation of fundamental analysis, delivering sophisticated investment research through the systematic DASV methodology.**

**Author**: Cole Morton
**Confidence**: [Workflow confidence based on successful DASV execution]
**Data Quality**: [Data quality maintained across all microservice phases]
