# Trade History Analyze

**DASV Phase 2: Statistical Analysis and Performance Measurement**

Comprehensive statistical analysis and performance measurement for institutional-quality trading performance evaluation using systematic analytical protocols and advanced quantitative methodologies.

## Purpose

The Trading Performance Analysis phase represents the systematic analysis and quantitative evaluation of trading data collected from the discovery phase. This command provides the requirements for the "Analyze" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on signal effectiveness analysis, statistical measurement, and performance attribution.

**Expected Output Schema**: `/scripts/schemas/trade_history_analysis_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute trade history analysis. Ensure output conforms to `/scripts/schemas/trade_history_analysis_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: trade_history
**Action**: analyze
**Output Location**: `./data/outputs/trade_history/analysis/`
**Previous Phase**: trade_history_discover
**Next Phase**: trade_history_synthesize
**Template Reference**: `./templates/analysis/trade_history_template.md` (final output structure awareness)

## Parameters

- `discovery_data`: Discovery phase output (required)
- `analysis_depth`: Analysis detail level - `summary` | `standard` | `comprehensive` | `institutional` (optional, default: comprehensive)
- `confidence_threshold`: Minimum confidence for calculations - `0.7` | `0.8` | `0.9` (optional, default: 0.8)
- `benchmark_focus`: Primary benchmark for analysis - `SPY` | `QQQ` | `VTI` (optional, default: from discovery)
- `statistical_rigor`: Statistical testing level - `basic` | `standard` | `institutional` (optional, default: institutional)

## Analysis Requirements

**Core Analysis Standards:**
- Statistical analysis using closed trades only for performance metrics
- Complete portfolio analysis including both closed and active positions
- Signal effectiveness measurement with proper strategy separation
- Risk-adjusted performance calculation with institutional-grade precision

**Data Processing Requirements:**
- Comprehensive trade categorization (closed vs active positions)
- Strategy-specific analysis with sample size validation
- Pattern recognition and quality classification
- Optimization opportunity identification with implementation confidence

**Quality Standards:**
- Minimum confidence threshold compliance (0.8+ for institutional grade)
- Statistical significance testing with appropriate confidence intervals
- Cross-validation of key metrics against discovery phase data
- Comprehensive error handling and limitation documentation

## Output Structure and Schema

**File Naming**: `{PORTFOLIO}_{YYYYMMDD}_analysis.json`
**Location**: `./data/outputs/trade_history/analysis/`
**Schema Compliance**: Must validate against `/scripts/schemas/trade_history_analysis_schema.json`

### Expected Analysis Schema Structure
```json
{
  "portfolio": "live_signals",
  "analysis_metadata": {
    "execution_timestamp": "2025-08-07T12:00:00Z",
    "confidence_score": 0.82,
    "statistical_significance": 0.95
  },
  "signal_effectiveness": {
    "entry_signal_analysis": {...},
    "exit_signal_analysis": {...}
  },
  "statistical_analysis": {
    "performance_metrics": {...},
    "risk_adjusted_metrics": {...}
  },
  "pattern_recognition": {
    "trade_quality_classification": {...}
  },
  "optimization_opportunities": {
    "entry_signal_enhancements": [...],
    "exit_signal_refinements": [...]
  },
  "risk_assessment": {
    "portfolio_risk_metrics": {...}
  },
  "next_phase_inputs": {
    "synthesis_ready": true
  }
}
```

## Implementation Framework

### Execution Requirements
**Primary Tool**: Use `/scripts/trade_history_analyze.py` as the atomic analysis tool
**Statistical Methods**: Implement proper significance testing and confidence intervals
**Sample Size Validation**: Enforce minimum trade requirements for statistical claims
**Quality Gates**: Ensure institutional-grade confidence scoring and error handling

### Success Criteria
- Statistical significance testing with >95% confidence where applicable
- Proper separation of closed vs active trade analysis
- Signal effectiveness measurement with optimization recommendations
- Risk-adjusted performance metrics with benchmark comparison

---

*This analysis phase provides comprehensive statistical evaluation and performance measurement for institutional-quality trading assessment and optimization.*
