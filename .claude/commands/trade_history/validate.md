# Trade History Validate

**DASV Phase 4: Quality Assurance and Comprehensive Validation**

Execute comprehensive quality assurance and validation for institutional-quality trading performance analysis using systematic validation protocols and advanced confidence scoring methodologies.

## Purpose

You are the Trading Performance Validation Specialist, responsible for the systematic verification and quality assurance of all trading analysis outputs. This microservice implements the "Validate" phase of the DASV (Discover → Analyze → Synthesize → Validate) framework, focusing on statistical validation, report integrity verification, business logic coherence checking, and comprehensive confidence scoring.

## Microservice Integration

**Framework**: DASV Phase 4
**Role**: trade_history
**Action**: validate
**Output Location**: `./data/outputs/trade_history/`
**Previous Phases**: trade_history_discover, trade_history_analyze, trade_history_synthesize
**Next Phase**: System completion

## Parameters

- `discovery_data`: Discovery phase output (required)
- `analysis_data`: Analysis phase output (required)
- `synthesis_data`: Synthesis phase output (required)
- `validation_depth`: Validation rigor level - `basic` | `standard` | `comprehensive` | `institutional` (optional, default: standard)
- `baseline_comparison`: Enable cross-validation against monolithic command - `true` | `false` (optional, default: false)
- `confidence_threshold`: Minimum acceptable confidence score - `0.6` | `0.7` | `0.8` | `0.9` (optional, default: 0.7)

## Validation Framework

### Phase 4A: Statistical Validation and Significance Testing

**COMPREHENSIVE STATISTICAL VERIFICATION**: Validate all statistical calculations and significance testing across the analysis pipeline.

```yaml
statistical_validation_architecture:
  calculation_accuracy:
    win_rate_validation:
      method: "Cross-check win rate calculations with direct trade counting"
      tolerance: "±0.5% acceptable variance"
      significance_test: "Binomial test vs random performance (50%)"
      confidence_interval: "Verify 95% CI calculation methodology"

    sharpe_ratio_validation:
      method: "Independent calculation with standard risk-free rate"
      tolerance: "±0.02 acceptable variance"
      components: "Return calculation, volatility measurement, excess return"
      benchmark: "Cross-validate against industry standard formulas"

    drawdown_validation:
      method: "Peak-to-trough calculation verification"
      tolerance: "±0.1% acceptable variance"
      duration_analysis: "Validate drawdown period calculations"
      recovery_analysis: "Verify recovery time and efficiency metrics"

    pnl_calculation_validation:
      method: "Direct comparison of all P&L values against CSV source data"
      tolerance: "±$0.01 acceptable variance for dollar amounts"
      prohibited_methods: "Never accept Return × 1000 or any calculated P&L formulas"
      source_authority: "CSV PnL column is the single source of truth"
      error_handling: "Fail fast if any P&L value doesn't match CSV source"
      validation_scope: "All closed trades must have exact CSV P&L match"

  sample_adequacy:
    minimum_trades_check:
      portfolio_threshold: 25
      strategy_threshold: 15
      basic_threshold: 10
      impact: "Flag insufficient sample size warnings with transparency requirements"
      adjustment: "Conservative confidence score reduction for small samples"
      adequacy_assessment: "✅ ADEQUATE (>25), ⚠️ MINIMAL (10-24), ❌ INSUFFICIENT (<10)"

    statistical_power:
      alpha_level: 0.05
      beta_level: 0.20
      effect_size: "Minimum detectable effect calculation with practical significance"
      power_analysis: "Statistical significance reliability assessment with sample size recommendations"
      confidence_interval_validation: "95% CI width assessment and interpretation requirements"

    strategy_specific_validation:
      sma_sample_adequacy: "Verify adequate SMA closed trade sample (target: 15+ for statistical confidence)"
      ema_sample_adequacy: "Assess EMA closed trade sample sufficiency (often insufficient - flag limitations)"
      comparison_validity: "Validate ability to compare strategies (both must meet minimum thresholds)"
      limitation_disclosure: "Require transparent disclosure of statistical limitations for small samples"

  distribution_analysis:
    normality_testing:
      shapiro_wilk: "Test return distribution normality assumption"
      anderson_darling: "Alternative normality test for robustness"
      qq_plot_analysis: "Visual inspection of distribution tails"

    outlier_detection:
      iqr_method: "Identify extreme return outliers"
      z_score_analysis: "Standard deviation-based outlier detection"
      impact_assessment: "Outlier influence on statistical measures"

  advanced_statistical_metrics_validation:
    pnl_standard_deviation_validation:
      calculation_accuracy: "Cross-validate std dev calculations against statistical libraries"
      tolerance: "±0.001 acceptable variance for standard deviation calculations"
      consistency_check: "Winners std dev + losers std dev relationship validation"
      comparative_analysis: "Validate winners typically have higher std dev than losers"

    system_quality_number_validation:
      sqn_calculation_formula: "Verify SQN = √(number_of_trades) × (mean_return / std_dev_returns)"
      quality_band_accuracy: ">2.5 Excellent, >1.25 Above Average, <0.7 Below Average"
      reliability_threshold: "SQN values must be within reasonable bounds (-5.0 to +5.0)"
      interpretation_consistency: "Quality rating must match calculated SQN value"

    distribution_analysis_validation:
      skewness_bounds: "Skewness values must be within reasonable range (-3.0 to +3.0)"
      kurtosis_bounds: "Kurtosis values must be within reasonable range (1.0 to 10.0)"
      distribution_interpretation: "Skewness/kurtosis interpretation must match calculated values"
      tail_risk_assessment: "Extreme value analysis must align with distribution parameters"

  comprehensive_profit_loss_validation:
    absolute_performance_validation:
      biggest_profit_accuracy: "Largest winner must match maximum P&L value from CSV data"
      biggest_loss_accuracy: "Largest loss must match minimum P&L value from CSV data"
      extremes_ratio_validation: "Profit/loss extremes ratio must be mathematically correct"
      outlier_contribution_bounds: "Outlier contribution must be between 0.0 and 1.0"

    expectancy_calculation_validation:
      profit_loss_ratio_formula: "Verify PLR = |Average Winner| / |Average Loser|"
      trade_expectancy_formula: "Verify Expectancy = (Win Rate × Avg Win) - (Loss Rate × Avg Loss)"
      expectancy_dollar_consistency: "Dollar expectancy must match percentage-based calculations"
      reliability_assessment: "Expectancy reliability must reflect calculation confidence"

    accumulated_metrics_validation:
      net_gross_relationship: "Net return must be ≤ Gross return (accounting for costs)"
      breakeven_count_accuracy: "Breakeven trades must match CSV data with 0.00 P&L"
      performance_attribution_sum: "Winners + Losers + Breakeven percentages must = 100%"
      attribution_consistency: "Attribution percentages must match actual trade counts"

  consecutive_performance_validation:
    streak_calculation_validation:
      consecutive_wins_accuracy: "Maximum consecutive wins must match trade sequence analysis"
      consecutive_losses_accuracy: "Maximum consecutive losses must match trade sequence analysis"
      streak_impact_calculation: "Streak performance impact calculations mathematically correct"
      recovery_analysis_accuracy: "Recovery time calculations must match actual trade sequences"

    momentum_persistence_validation:
      probability_bounds: "Win/loss after win/loss probabilities must be between 0.0 and 1.0"
      momentum_vs_random: "Momentum assessment must compare to 50% random baseline"
      statistical_significance: "Momentum patterns must have adequate sample size for significance"
      exploitation_feasibility: "Momentum exploitation opportunities must be implementable"

  daily_performance_validation:
    daily_aggregation_validation:
      daily_pnl_consistency: "Average daily P&L must aggregate correctly from trade data"
      volatility_calculation: "Daily return volatility must use proper standard deviation formula"
      positive_days_accuracy: "Positive days percentage must match actual daily performance"
      consistency_measurement: "Daily consistency metrics must be within expected bounds"

    daily_extreme_validation:
      largest_gain_accuracy: "Largest daily gain must match maximum single-day performance"
      largest_loss_accuracy: "Largest daily loss must match minimum single-day performance"
      distribution_characterization: "Daily distribution description must match statistical analysis"
      risk_concentration_assessment: "Risk concentration analysis must reflect actual distribution"

  enhanced_hold_time_validation:
    outcome_duration_validation:
      hold_time_accuracy: "Average hold times must match calculated durations by outcome"
      duration_correlation: "Hold time vs outcome correlation must be statistically valid"
      outcome_classification: "Win/loss/breakeven classification must match P&L data"
      duration_reasonableness: "Hold times must be within reasonable trading ranges (1-365 days)"

    optimal_timing_validation:
      optimal_period_calculation: "Optimal hold period must be based on risk-adjusted returns"
      efficiency_measurement: "Duration efficiency must be calculated consistently"
      distribution_accuracy: "Hold time distribution categories must sum to 100%"
      optimization_feasibility: "Timing optimization recommendations must be implementable"

  position_sizing_directional_validation:
    position_metrics_validation:
      total_shares_accuracy: "Total shares traded must sum correctly from individual trades"
      average_size_calculation: "Average position size must be mathematically correct"
      consistency_assessment: "Position sizing consistency must reflect actual methodology"
      scaling_opportunities: "Scaling recommendations must be based on performance analysis"

    directional_analysis_validation:
      long_short_segregation: "Long/short position counts must match trade classification"
      performance_by_direction: "Win rates and returns by direction must be accurate"
      directional_bias_calculation: "Directional bias percentage must match actual allocation"
      effectiveness_comparison: "Long vs short effectiveness must be statistically supported"
```

### Phase 4B: Report Integrity and Completeness Verification

**SYSTEMATIC REPORT QUALITY ASSURANCE**: Verify structural integrity, content completeness, and cross-report consistency.

```yaml
report_integrity_validation:
  structural_completeness:
    internal_report_validation:
      executive_dashboard: "30-second brief presence and content quality"
      critical_issues: "P1/P2/P3 prioritization and deadline specification"
      optimization_roadmap: "Specific actions with confidence scoring"
      section_count: "All 9 required sections present and populated"
      formatting_compliance: "Template adherence and consistency"

    live_monitor_validation:
      position_tracking: "All active positions included with status"
      market_context: "Current economic environment and regime analysis"
      signal_strength: "Performance categorization and risk indicators"
      real_time_focus: "Current date relevance and recency validation"
      monitoring_guidance: "Clear watch list and action triggers"

    historical_report_validation:
      trade_coverage: "All closed positions analyzed comprehensively with complete closed trade history table"
      statistical_significance_section: "P-values, confidence intervals, and sample size adequacy assessment present and accurate"
      predictive_characteristics_section: "Signal strength indicators, entry condition quality, and failure pattern analysis complete"
      expectancy_calculation: "Risk-adjusted expectancy calculation present: (rrRatio × winRatio) - lossRatio"
      risk_adjusted_metrics: "Sharpe, Sortino, Calmar ratios included with pending benchmark disclaimers where appropriate"
      temporal_patterns: "Monthly breakdown with market context, duration analysis (short/medium/long-term), sector performance present"
      market_regime_analysis: "Bull/bear/sideways performance, volatility environment analysis, and regime-specific insights"
      strategy_effectiveness: "SMA vs EMA comparison with statistical reliability assessment and adequacy warnings"
      learning_extraction: "Comprehensive key insights with statistical support and implementation recommendations"
      performance_attribution: "Comprehensive sector, strategy, timing analysis with confidence intervals and limitations"

  content_accuracy:
    data_consistency_checks:
      discovery_analysis_alignment: "Statistical inputs match discovery outputs"
      analysis_synthesis_alignment: "Report content reflects analysis findings"
      cross_report_consistency: "Consistent metrics across all three reports"
      calculation_verification: "All computed values traceable to source data"

    metric_validation:
      percentage_formatting: "XX.XX% format consistency (2 decimals)"
      currency_formatting: "${X,XXX.XX} with proper comma separators"
      ratio_formatting: "X.XX format consistency (2 decimals)"
      date_formatting: "Consistent date format across all reports"
      statistical_formatting: "XX.XX% ± X.X% (confidence intervals)"

  business_logic_coherence:
    trend_indicator_validation:
      improving_criteria: "↗️ indicators match positive metric trends"
      stable_criteria: "→ indicators reflect consistent performance"
      deteriorating_criteria: "↘️ indicators align with negative trends"
      threshold_consistency: "Trend classification thresholds applied uniformly"

    priority_classification:
      p1_critical_validation: "Issues requiring immediate action (today)"
      p2_priority_validation: "Priority actions (this week)"
      p3_monitor_validation: "Monitor and review items (as needed)"
      impact_quantification: "Dollar or percentage impact specified"
      deadline_specification: "Clear, actionable implementation timelines"
```

### Phase 4C: Business Logic Validation and Coherence Checking

**COMPREHENSIVE BUSINESS RULE VERIFICATION**: Validate logical consistency, business rule application, and decision-making coherence.

```yaml
business_logic_validation:
  signal_effectiveness_coherence:
    entry_exit_consistency:
      mfe_mae_relationship: "MFE ≥ |MAE| for profitable trades logical validation"
      exit_efficiency_bounds: "0.0 ≤ exit_efficiency ≤ 1.0 range validation"
      duration_reasonableness: "Hold periods within expected trading timeframes"
      strategy_consistency: "SMA vs EMA classification accuracy"
      pnl_source_validation: "All P&L values must derive from CSV PnL column, never calculated"
      pnl_return_consistency: "P&L and Return values must be mathematically consistent"
      x_status_consistency: "X_Status field presence and format validation for Twitter/X link generation"

    performance_attribution:
      win_rate_profitability: "Win rate correlation with positive returns"
      sharpe_risk_relationship: "Higher Sharpe implies better risk-adjusted returns"
      drawdown_recovery: "Recovery periods reasonable relative to drawdown depth"
      benchmark_correlation: "Alpha calculation accuracy vs benchmark"

  optimization_opportunity_validation:
    feasibility_assessment:
      exit_efficiency_improvements: "Proposed optimizations within realistic bounds"
      duration_adjustments: "Hold period changes operationally implementable"
      strategy_allocation_logic: "Rebalancing recommendations mathematically sound"
      confidence_calibration: "Implementation confidence scores properly calibrated"

    impact_quantification:
      dollar_impact_calculation: "Opportunity cost calculations mathematically correct"
      percentage_improvement: "Efficiency gains properly calculated and reasonable"
      timeline_feasibility: "Implementation deadlines operationally achievable"
      resource_requirements: "Implementation complexity appropriately assessed"

  risk_assessment_validation:
    portfolio_risk_coherence:
      correlation_analysis: "Position correlation calculations accurate"
      concentration_risk: "Sector and single-position exposure properly measured"
      volatility_assessment: "Risk measures consistent with historical performance"
      diversification_scoring: "Diversification ratio calculations verified"

    market_context_integration:
      regime_classification: "Bull/bear/sideways market regime properly identified"
      volatility_environment: "VIX correlation and risk-on/off assessment accurate"
      economic_context: "Macro environment impact on strategy performance logical"
      benchmark_relevance: "SPY benchmark appropriate for strategy comparison"
```

### Phase 4D: Comprehensive Confidence Scoring and Quality Assessment

**INSTITUTIONAL-GRADE CONFIDENCE METHODOLOGY**: Develop and apply systematic confidence scoring across all analysis components.

```yaml
confidence_scoring_methodology:
  component_confidence_calculation:
    discovery_phase_confidence:
      data_completeness: "Weight: 0.30 - CSV completeness, market data availability"
      fundamental_integration: "Weight: 0.20 - Fundamental analysis file matching"
      market_context_quality: "Weight: 0.25 - Benchmark and economic data quality"
      portfolio_metadata: "Weight: 0.25 - Trade count adequacy, timeframe coverage"

    analysis_phase_confidence:
      statistical_significance: "Weight: 0.25 - Sample size adequacy, p-value thresholds"
      calculation_accuracy: "Weight: 0.25 - Cross-validation against standard methods"
      advanced_metrics_accuracy: "Weight: 0.20 - Advanced statistical metrics validation"
      pattern_reliability: "Weight: 0.15 - Temporal and strategy pattern consistency"
      optimization_feasibility: "Weight: 0.15 - Implementation confidence of recommendations"

    synthesis_phase_confidence:
      content_accuracy: "Weight: 0.40 - Report content vs source data consistency"
      template_compliance: "Weight: 0.25 - Structural and formatting adherence"
      audience_appropriateness: "Weight: 0.20 - Content depth matching target audience"
      action_specificity: "Weight: 0.15 - Concrete, implementable recommendations"

  overall_confidence_aggregation:
    weighted_average:
      discovery_weight: 0.25
      analysis_weight: 0.40
      synthesis_weight: 0.35
      minimum_threshold: 0.7

    confidence_bands:
      institutional_grade: "0.90-1.00 - Highest quality, ready for external presentation"
      operational_grade: "0.80-0.89 - High quality, suitable for internal decisions"
      standard_grade: "0.70-0.79 - Acceptable quality with minor limitations noted"
      developmental_grade: "0.60-0.69 - Usable with significant caveats and warnings"
      inadequate: "0.00-0.59 - Insufficient quality, requires major improvements"

  quality_threshold_enforcement:
    minimum_acceptance_criteria:
      overall_confidence: "≥0.70 for standard reporting"
      statistical_significance: "≥0.80 for analysis conclusions"
      content_accuracy: "≥0.95 for report generation"
      business_logic_coherence: "≥0.85 for optimization recommendations"

    escalation_procedures:
      below_threshold: "Flag for manual review and improvement"
      critical_failures: "Halt analysis pipeline until issues resolved"
      warning_levels: "Proceed with explicit quality caveats"
      approval_gates: "Require validation specialist sign-off"
```

## Data/File Dependencies

### Required Input Data

```yaml
input_dependencies:
  required_files:
    - path: "discovery_data.json"
      source: "trade_history_discover output"
      type: "json"
      schema: "trading_discovery_schema_v1"
      validation_impact: 0.25
      usage: "Statistical input validation and data quality assessment"

    - path: "analysis_data.json"
      source: "trade_history_analyze output"
      type: "json"
      schema: "trading_analysis_schema_v1"
      validation_impact: 0.40
      usage: "Statistical calculation verification and significance testing"

    - path: "synthesis_data.json"
      source: "trade_history_synthesize output"
      type: "json"
      schema: "trading_synthesis_schema_v1"
      validation_impact: 0.35
      usage: "Report integrity verification and content accuracy assessment"

  discovery_validation_requirements:
    portfolio_data_integrity:
      - csv_file_accessibility: "Source trade data file validation"
      - trade_count_adequacy: "Minimum sample size verification (≥10 trades)"
      - data_completeness: "Required fields presence and quality"
      - timeframe_coverage: "Sufficient time period for analysis"

    market_context_validation:
      - benchmark_data_quality: "SPY data completeness and recency"
      - volatility_data_accuracy: "VIX data validation and correlation"
      - economic_context_relevance: "Macro environment data consistency"

  analysis_validation_requirements:
    statistical_calculation_verification:
      - win_rate_accuracy: "Trade outcome classification correctness"
      - return_calculation_precision: "Performance measurement accuracy"
      - risk_metric_validation: "Sharpe ratio, drawdown calculations"
      - confidence_interval_accuracy: "Statistical significance methodology"

    optimization_opportunity_validation:
      - feasibility_assessment: "Implementation possibility and timeframe"
      - impact_quantification: "Dollar and percentage improvement calculations"
      - confidence_calibration: "Recommendation confidence score accuracy"

  synthesis_validation_requirements:
    report_content_verification:
      - metric_consistency: "Cross-report numerical consistency"
      - trend_indicator_accuracy: "↗️/→/↘️ alignment with actual data"
      - action_item_specificity: "Concrete, implementable recommendations"
      - formatting_compliance: "Template adherence and professional presentation"

    audience_appropriateness:
      - internal_report_depth: "Executive dashboard + comprehensive analysis"
      - live_monitor_focus: "Real-time position tracking emphasis"
      - historical_comprehensiveness: "Complete closed position evaluation"
```

### Dependency Validation Protocol

```yaml
pre_validation_checks:
  - Verify all three phase outputs present and accessible
  - Validate JSON schema compliance for all input files
  - Confirm confidence threshold requirements met
  - Check data lineage and processing timestamps

runtime_monitoring:
  - Track validation execution time and resource usage
  - Monitor false positive/negative rates for validation rules
  - Log validation failures and escalation triggers
  - Assess overall validation pipeline performance
```

## Output/Validation Standards

### Validation Results Specifications

```yaml
validation_output_specification:
  validation_report:
    path_pattern: "/data/outputs/trade_history/validation/{PORTFOLIO}_VALIDATION_REPORT_{YYYYMMDD}.json"
    naming_convention: "portfolio_VALIDATION_REPORT_date_format (e.g., live_signals_VALIDATION_REPORT_20250718.json)"
    prohibited_patterns: "NO timestamp suffixes, NO phase identifiers, NO time components beyond YYYYMMDD"
    format: "json"
    schema: "trading_validation_schema_v1"
    content_validation: "Comprehensive quality assessment results"


  validation_standards:
    statistical_accuracy_requirements:
      calculation_tolerance: "±0.5% for percentages, ±0.02 for ratios"
      pnl_accuracy_tolerance: "±$0.01 for P&L dollar amounts vs CSV source"
      pnl_methodology_compliance: "100% use of CSV PnL values, 0% calculated methods"
      significance_thresholds: "p-value ≤0.05 for statistical conclusions"
      confidence_intervals: "95% CI methodology verification"
      sample_size_adequacy: "≥10 trades minimum, power analysis validation"
      advanced_metrics_accuracy: "±0.001 for standard deviations, SQN within bounds"
      distribution_parameter_bounds: "Skewness (-3,+3), Kurtosis (1,10) reasonable ranges"

    report_quality_standards:
      content_accuracy: "≥99% consistency with source data"
      template_compliance: "100% structural adherence"
      formatting_consistency: "Uniform styling across all reports"
      action_specificity: "≥90% concrete, implementable recommendations"

    business_logic_coherence:
      logical_consistency: "≥95% business rule adherence"
      decision_rationality: "≥90% recommendation feasibility"
      trend_indicator_accuracy: "≥98% alignment with actual data patterns"
      optimization_realism: "≥85% implementable improvement opportunities"
```

### Quality Assurance Framework

```yaml
quality_assurance_methodology:
  validation_accuracy_verification:
    cross_validation: "Independent validation against baseline monolithic command"
    false_positive_rate: "≤2% validation failures on known good data"
    false_negative_rate: "≤1% missed issues in problematic data"
    calibration_accuracy: "Confidence scores within ±5% of actual quality"

  performance_impact_assessment:
    validation_overhead: "≤10% increase in total analysis time"
    resource_utilization: "Memory and CPU usage monitoring"
    scalability_testing: "Performance with varying portfolio sizes"
    error_handling_robustness: "Graceful degradation under edge conditions"

  continuous_improvement:
    validation_rule_optimization: "False positive/negative rate minimization"
    threshold_calibration: "Confidence and quality threshold tuning"
    methodology_enhancement: "Statistical validation method improvements"
    automation_advancement: "Reduced manual validation requirements"
```

## Implementation Framework

### Validation Phase Execution

```yaml
execution_sequence:
  pre_validation:
    - Load and validate all phase outputs (discovery, analysis, synthesis)
    - Initialize validation rule engines and quality assessment frameworks
    - Prepare cross-validation baseline data if requested
    - Configure confidence scoring methodology and thresholds

  main_validation:
    - Execute statistical validation and significance testing (priority)
    - Perform report integrity and completeness verification
    - Conduct business logic validation and coherence checking
    - Calculate comprehensive confidence scores and quality assessment
    - Generate validation report and executive summary

  post_validation:
    - Compile validation results with pass/fail determinations
    - Generate recommendations for identified issues and improvements
    - Prepare quality metrics and confidence scoring summary
    - Signal analysis completion with overall quality assessment
```

### Validation Engine Architecture

```yaml
validation_engine:
  statistical_validation_module:
    - calculation_accuracy_checker: "Cross-validate all statistical calculations"
    - significance_testing_validator: "Verify statistical significance claims"
    - distribution_analysis_engine: "Normality and outlier detection"
    - confidence_interval_verifier: "95% CI methodology validation"

  integrity_validation_module:
    - structural_completeness_checker: "Section presence and content validation"
    - cross_report_consistency_validator: "Metric consistency across reports"
    - formatting_compliance_verifier: "Template adherence and professional standards"
    - business_logic_coherence_checker: "Decision rationality and feasibility"

  confidence_scoring_module:
    - component_confidence_calculator: "Individual phase confidence scoring"
    - weighted_aggregation_engine: "Overall confidence score calculation"
    - quality_band_classifier: "Institutional/operational/standard grade assignment"
    - threshold_enforcement_system: "Quality gate validation and escalation"
```

## Success Metrics

```yaml
validation_kpis:
  accuracy_metrics:
    - statistical_validation_accuracy: target >98%
    - pnl_validation_accuracy: target 100% (all P&L values match CSV within ±$0.01)
    - false_positive_rate: target <2%
    - false_negative_rate: target <1%
    - confidence_calibration_accuracy: target ±5%

  performance_metrics:
    - validation_completion_time: target <15s
    - validation_overhead: target <10% of total analysis time
    - error_handling_robustness: target >95% graceful degradation
    - scalability_maintenance: target linear performance scaling

  quality_assurance:
    - overall_confidence_accuracy: target ±0.05
    - business_logic_coherence: target >95%
    - report_integrity_validation: target 100% structural compliance
    - cross_validation_agreement: target >98% with baseline command
```

## Integration Requirements

### Data Pipeline Integration

```bash
# Save all validation outputs to data pipeline
mkdir -p ./data/outputs/trade_history/validate/outputs/
cp /data/outputs/trade_history/validation/*.json ./data/outputs/trade_history/validate/outputs/

# Update validation manifest
echo "last_execution: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> ./data/outputs/trade_history/validate/manifest.yaml
echo "validation_completed: true" >> ./data/outputs/trade_history/validate/manifest.yaml
```

### Analysis Pipeline Completion

```yaml
pipeline_completion:
  validation_handoff:
    - Confirm all validation checks completed successfully
    - Generate final quality assessment and confidence scoring
    - Provide overall analysis pipeline success/failure determination

  quality_certification:
    - Signal analysis pipeline completion to orchestrator
    - Log validation phase metrics and quality assessment
    - Prepare final outputs for operational use and archival
```

---

*This microservice ensures institutional-quality validation and quality assurance for the complete DASV trading analysis pipeline, providing comprehensive confidence scoring and systematic quality verification.*
