# Fundamental Analysis Full

**Complete DASV Workflow for Fundamental Analysis**

Execute the complete DASV (Discover → Analyze → Synthesize → Validate) microservice workflow by invoking each phase command sequentially to produce institutional-quality fundamental analysis with comprehensive investment recommendations.

## Purpose

This command orchestrates the complete fundamental analysis microservice workflow by executing all four individual DASV phase commands in sequence, ensuring proper data flow and maintaining institutional-quality standards throughout.

## Workflow Integration

**Framework**: DASV Complete Workflow
**Microservices**: 4 sequential command invocations
**Output Location**: `./data/outputs/fundamental_analysis/`
**Quality Standard**: Institutional-grade fundamental analysis

## Parameters

- `ticker`: Stock symbol (required, uppercase format)
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Analysis period - `3y` | `5y` | `10y` | `full` (optional, default: 5y)
- `confidence_threshold`: Minimum confidence for recommendations - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `scenario_count`: Number of valuation scenarios - `3` | `5` | `7` (optional, default: 3)

## DASV Workflow Execution

Execute each microservice command sequentially, waiting for completion before proceeding to the next phase.

### Phase 1: Execute Discovery Command
```
/fundamental_analyst_discover {ticker} depth={depth} timeframe={timeframe} confidence_threshold={confidence_threshold}
```

**Expected Output**: `./data/outputs/fundamental_analysis/discovery/{TICKER}_{YYYYMMDD}_discovery.json`
**Duration**: ~20s
**Verification**: Confirm discovery file exists before proceeding

### Phase 2: Execute Analysis Command
```
/fundamental_analyst_analyze {ticker} confidence_threshold={confidence_threshold} peer_comparison=true risk_analysis=true scenario_count={scenario_count}
```

**Expected Output**: `./data/outputs/fundamental_analysis/analysis/{TICKER}_{YYYYMMDD}_analysis.json`
**Duration**: ~40s
**Verification**: Confirm analysis file exists before proceeding

### Phase 3: Execute Synthesis Command
```
/fundamental_analyst_synthesize {ticker} confidence_threshold={confidence_threshold} scenario_count={scenario_count}
```

**Expected Output**: `./data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md`
**Duration**: ~30s
**Verification**: Confirm markdown analysis document exists before proceeding

### Phase 4: Execute Validation Command
```
/fundamental_analyst_validate {ticker} confidence_threshold={confidence_threshold}
```

**Expected Output**: `./data/outputs/fundamental_analysis/validation/{TICKER}_{YYYYMMDD}_validation.json`
**Duration**: ~25s
**Final Verification**: Confirm all four output files exist

## Execution Protocol

### Sequential Command Invocation
Execute each command individually in order, ensuring each phase completes successfully before proceeding:

1. **Invoke Discovery**: Execute fundamental_analyst_discover command
2. **Wait for Completion**: Verify discovery output file exists
3. **Invoke Analysis**: Execute fundamental_analyst_analyze command
4. **Wait for Completion**: Verify analysis output file exists
5. **Invoke Synthesis**: Execute fundamental_analyst_synthesize command
6. **Wait for Completion**: Verify synthesis output file exists
7. **Invoke Validation**: Execute fundamental_analyst_validate command
8. **Final Verification**: Confirm all expected outputs generated

### Error Handling
- **Phase Failure**: Stop execution if any command fails
- **Missing Output**: Stop execution if expected output file not generated
- **Quality Gate**: Stop execution if confidence thresholds not met
- **File Verification**: Verify each output exists before proceeding to next phase

## Output Requirements

### Complete File Set
After successful execution, the following files must exist:
- **Discovery**: `./data/outputs/fundamental_analysis/discovery/{TICKER}_{YYYYMMDD}_discovery.json`
- **Analysis**: `./data/outputs/fundamental_analysis/analysis/{TICKER}_{YYYYMMDD}_analysis.json`
- **Synthesis**: `./data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md`
- **Validation**: `./data/outputs/fundamental_analysis/validation/{TICKER}_{YYYYMMDD}_validation.json`

### Quality Standards
- **Content Quality**: Institutional-grade investment analysis
- **Format Compliance**: Professional presentation with 0.0-1.0 confidence scoring
- **Author Attribution**: Consistent "Cole Morton" attribution
- **Data Accuracy**: All financial calculations verified against Yahoo Finance

## Success Criteria

```
QUALITY ASSURANCE CHECKLIST:
□ All four DASV phase commands execute successfully
□ Discovery JSON file generated in correct location
□ Analysis JSON file generated in correct location
□ Synthesis markdown document generated in correct location
□ Validation JSON file generated in correct location
□ All financial calculations verified against Yahoo Finance exactly
□ Content evaluator score 8.5+ minimum target
□ Complete audit trail with all phase outputs accessible
□ Institutional-quality analysis maintained throughout
□ Professional presentation standards met
```

## Performance Characteristics

**Total Estimated Duration**: 115 seconds
**Phase Breakdown**:
- Discover: 20s (data collection)
- Analyze: 40s (systematic analysis)
- Synthesize: 30s (document generation)
- Validate: 25s (quality assurance)

## Usage Examples

```bash
# Standard comprehensive analysis
/fundamental_analysis_full AAPL

# Deep dive with high confidence requirement
/fundamental_analysis_full MSFT depth=deep-dive confidence_threshold=0.8

# Quick summary with extended timeframe
/fundamental_analysis_full GOOGL depth=summary timeframe=10y

# Full analysis with extra scenarios
/fundamental_analysis_full TSLA scenario_count=7 timeframe=full
```

## Integration Notes

### Command Dependency Chain
Each command builds on the previous phase's output:
- **Discover → Analyze**: Discovery data feeds into analysis
- **Analyze → Synthesize**: Combined discovery and analysis data feeds into synthesis
- **Synthesize → Validate**: Generated document feeds into validation

### Data Flow Verification
Verify proper data flow between phases by confirming each expected output file exists before invoking the next command.

### Quality Maintenance
Each individual command maintains its own quality standards and confidence scoring, ensuring institutional-grade output throughout the complete workflow.

**This command executes the complete DASV microservice workflow by invoking each individual phase command sequentially, maintaining the same output quality and file structure as manual execution.**

**Author**: Cole Morton
**Confidence**: [Based on successful sequential command execution]
**Data Quality**: [Maintained across all microservice phases]
