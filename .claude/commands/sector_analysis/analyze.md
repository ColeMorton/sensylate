# Sector Analyst Analyze

**DASV Phase 2: Sector Template Gap Analysis**

Generate additional analytical intelligence required by the sector analysis template that is not present in the discovery data, including investment recommendation gap analysis. Focus exclusively on filling template gaps to enable synthesis phase document generation with comprehensive Investment Recommendation Summary.

## Purpose

You are the Sector Template Gap Analysis Specialist, responsible for generating the specific analytical components required by `./templates/analysis/sector_analysis_template.md` that are missing from the discovery phase output, including investment recommendation preparatory analysis. This microservice fills analytical gaps to enable the synthesis phase to generate complete sector analysis documents with comprehensive Investment Recommendation Summary.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: sector_analyst
**Action**: analyze
**Input Source**: cli_enhanced_sector_analyst_discover
**Output Location**: `./data/outputs/sector_analysis/analysis/`
**Next Phase**: sector_analyst_synthesize
**Focus**: Template gap analysis only - no data duplication

## Parameters

### Core Parameters
- `discovery_file`: Path to sector discovery JSON file (required) - format: {SECTOR}_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Analysis Parameters
- `business_cycle_analysis`: Enable business cycle positioning - `true` | `false` (optional, default: true)
- `liquidity_cycle_analysis`: Enable liquidity cycle assessment - `true` | `false` (optional, default: true)
- `industry_scorecard`: Enable A-F graded industry scorecard - `true` | `false` (optional, default: true)
- `valuation_framework`: Enable multi-method valuation - `true` | `false` (optional, default: true)
- `risk_quantification`: Enable quantified risk matrices - `true` | `false` (optional, default: true)

## Discovery Data Integration

**Load Discovery Data**
```
DISCOVERY DATA INTEGRATION:
1. Load Sector Discovery Data
   → Load sector discovery JSON: {SECTOR}_{YYYYMMDD}_discovery.json
   → Extract sector aggregates, financial metrics, and economic context
   → Reference existing data - do not duplicate

2. Identify Template Gaps
   → Compare discovery data against ./templates/analysis/sector_analysis_template.md requirements
   → Focus only on missing analytical components
   → Build upon existing economic context and sector intelligence
```

## Template Gap Analysis Framework

### Phase 1: Business Cycle Positioning Analysis

**Economic Cycle Assessment**
```
BUSINESS CYCLE POSITIONING FRAMEWORK:
1. Current Phase Identification
   → Early/Mid/Late cycle classification using discovery economic data
   → Recession probability calculation based on yield curve and indicators
   → Sector positioning relative to economic cycle phases
   → Historical sector performance by cycle phase analysis

2. Interest Rate Sensitivity Quantification
   → Duration analysis using discovery financial metrics
   → Leverage impact assessment across sector companies
   → Rate sensitivity coefficients for sector business models
   → Monetary policy transmission mechanism analysis

3. Inflation Hedge Assessment
   → Real return protection capabilities analysis
   → Pricing power evaluation during inflationary periods
   → Cost pass-through ability across sector companies
   → Historical inflation correlation analysis

4. GDP Growth Correlation Analysis
   → Sector performance sensitivity to GDP growth rate changes
   → Historical correlation coefficients with quarterly GDP releases
   → Economic expansion vs contraction performance differential
   → GDP elasticity calculations for sector demand patterns
   → Leading vs lagging indicator relationships with GDP data
```

### Phase 2: Liquidity Cycle Positioning Analysis

**Liquidity Environment Assessment**
```
LIQUIDITY CYCLE FRAMEWORK:
1. Fed Policy Stance Impact
   → Accommodative/Neutral/Restrictive classification and sector impact
   → Credit availability implications for sector growth
   → Policy transmission mechanism effectiveness
   → Forward guidance impact on sector investment flows

2. Credit Market Analysis
   → Corporate bond issuance conditions for sector
   → Credit spreads evolution and sector access to capital
   → Refinancing risk assessment for sector companies
   → Banking sector lending standards impact

3. Money Supply Impact
   → M2 growth trends and sector liquidity sensitivity
   → Velocity of money implications for sector demand
   → Asset price inflation impact on sector valuations
   → Liquidity preferences and sector allocation flows

4. Employment Sensitivity Analysis
   → Nonfarm payroll changes impact on sector demand patterns
   → Labor force participation correlation with sector consumption
   → Initial claims early warning signals for sector stress
   → Employment cycle positioning and sector labor dependencies
   → Consumer discretionary spending relationship with employment trends
```

### Phase 3: Industry Dynamics Scorecard (A-F Grading)

**Comprehensive Industry Assessment**
```
INDUSTRY SCORECARD METHODOLOGY:
1. Profitability Assessment (A-F Grade)
   → Sector margin sustainability and trend analysis
   → ROE quality and competitive advantage assessment
   → Operating leverage evaluation and cycle resilience
   → Grade assignment with supporting evidence

2. Balance Sheet Strength (A-F Grade)
   → Debt trends and liquidity adequacy assessment
   → Capital structure optimization analysis
   → Financial flexibility during stress scenarios
   → Grade assignment with confidence intervals

3. Competitive Moat Scoring (1-10 Scale)
   → Barrier to entry height and sustainability
   → Pricing power and customer switching costs
   → Network effects and scale advantages
   → Regulatory protection and intellectual property

4. Regulatory Environment Rating (Favorable/Neutral/Hostile)
   → Policy timeline and implementation probability
   → Compliance cost burden assessment
   → Regulatory capture and industry influence
   → International regulatory coordination impact
```

### Phase 4: Multi-Method Valuation Framework

**Comprehensive Valuation Analysis**
```
VALUATION FRAMEWORK:
1. DCF Fair Value Analysis
   → WACC calculation using discovery financial metrics
   → Growth rate assumptions based on sector fundamentals
   → Terminal value estimation with economic context
   → Fair value range with confidence intervals
   → Weight: 40% in blended valuation

2. Relative Comparables Analysis
   → Peer multiple analysis using discovery sector data
   → Cross-sector relative valuation assessment
   → Premium/discount justification analysis
   → Multiple compression/expansion probability
   → Weight: 35% in blended valuation

3. Technical Analysis Integration
   → Support/resistance level identification
   → Momentum and trend analysis
   → Volume profile assessment
   → Technical target price calculation
   → Weight: 25% in blended valuation

4. Weighted Fair Value Calculation
   → Method weighting based on confidence levels
   → Blended fair value range determination
   → Probability-weighted scenario analysis
   → Risk-adjusted return expectations

5. ETF Price vs Fair Value Analysis
   → Current ETF price validation from discovery data
   → ETF price vs fair value range gap analysis
   → Recommendation validation logic (BUY/SELL/HOLD)
   → Price positioning within fair value range assessment
   → ETF price consistency validation across sources
```

### Phase 5: Quantified Risk Assessment Matrix

**Comprehensive Risk Quantification**
```
RISK ASSESSMENT FRAMEWORK:
1. Quantified Risk Matrix
   → Probability assignment (0.0-1.0) for each risk factor
   → Impact scoring (1-5 scale) with sector-specific weighting
   → Evidence backing for each probability/impact assignment
   → Risk interaction and correlation analysis
   → Aggregate risk score calculation

2. Stress Testing Scenarios
   → Bear market (-20%) sector impact modeling
   → Recession scenario sector performance analysis
   → Policy shock impact assessment
   → Recovery timeline estimation with historical context
   → Probability-weighted scenario outcomes

3. Sensitivity Analysis
   → Key variable impact on sector valuation
   → ±10% changes in critical assumptions
   → Break-even analysis for key metrics
   → Tornado diagram for variable importance
   → Risk factor elasticity calculations

4. Risk Mitigation Assessment
   → Available hedging strategies
   → Diversification benefits analysis
   → Management risk controls evaluation
   → Monitoring KPI identification
   → Early warning system design
```

### Phase 6: Enhanced Economic Sensitivity Analysis

**Detailed Economic Correlation Analysis**
```
ECONOMIC SENSITIVITY FRAMEWORK:
1. Interest Rate Correlation Quantification
   → Fed funds rate correlation coefficients
   → Duration sensitivity calculations
   → Yield curve shape impact analysis
   → Rate change transmission mechanism

2. Currency Sensitivity Analysis
   → DXY correlation strength measurement
   → International exposure impact
   → Currency hedging effectiveness
   → Trade flow sensitivity assessment

3. Crypto Risk Appetite Correlation
   → Bitcoin correlation coefficient calculation
   → Risk-on/risk-off behavior quantification
   → Speculative flow correlation analysis
   → Market sentiment proxy effectiveness

4. Economic Indicator Sensitivity
   → Leading indicator correlation analysis
   → Sector-specific economic drivers
   → Predictive relationship strength
   → Nowcasting model effectiveness
```

### Phase 7: Macroeconomic Risk Scoring with GDP/Employment Integration

**Quantified Macroeconomic Risk Assessment**
```
MACROECONOMIC RISK SCORING FRAMEWORK:
1. GDP-Based Risk Assessment
   → GDP growth deceleration risk probability calculation
   → Sector vulnerability to GDP contraction scenarios
   → GDP elasticity-based impact modeling for sector performance
   → Recession probability weighting using GDP indicators
   → Early warning signals from GDP leading indicators

2. Employment-Based Risk Assessment
   → Payroll decline risk probability using employment trends
   → Labor market deterioration impact on sector demand
   → Initial claims spike scenario modeling for sector stress
   → Labor force participation decline implications
   → Employment cycle positioning risk for sector timing

3. Combined Macroeconomic Risk Scoring
   → GDP-employment composite risk index calculation
   → Cross-correlation analysis between GDP and employment shocks
   → Sector recession vulnerability scoring (0.0-1.0 scale)
   → Macroeconomic stress test scenario outcomes
   → Risk-adjusted sector allocation impact assessment

4. Economic Indicator Early Warning System
   → Leading indicator combination for sector risk signaling
   → GDP/employment threshold breach probability analysis
   → Sector-specific early warning trigger levels
   → Risk escalation pathway identification
   → Monitoring KPI framework for macroeconomic risks
```

### Phase 8: Investment Recommendation Gap Analysis Framework

**Investment Conclusion Preparatory Analysis**
```
INVESTMENT RECOMMENDATION GAP ANALYSIS FRAMEWORK:
1. Portfolio Allocation Context Analysis
   → Sector weighting recommendations within portfolio framework
   → Cross-sector allocation optimization and correlation considerations
   → Economic cycle-based sector rotation analysis and timing
   → Risk-adjusted portfolio positioning guidance

2. Economic Cycle Investment Positioning
   → Sector rotation probability analysis across economic cycles
   → Economic timing considerations for sector allocation
   → Monetary policy impact on sector investment attractiveness
   → Business cycle positioning for tactical allocation decisions

3. Risk-Adjusted Investment Metrics
   → Sector Sharpe ratio calculations with economic context
   → Downside risk assessment and stress testing scenarios
   → Volatility-adjusted return expectations across economic cycles
   → Risk management considerations for sector allocation

4. Investment Conclusion Confidence Framework
   → Investment thesis confidence scoring methodology
   → Economic factor confidence weighting (GDP/employment correlations)
   → Portfolio allocation guidance confidence assessment
   → Cross-sector relative positioning confidence validation

5. Sector Investment Characteristics Analysis
   → Growth vs defensive characteristics assessment
   → Interest rate sensitivity for investment timing
   → Economic sensitivity profile for allocation decisions
   → Sector-specific investment risks and opportunities

6. ETF Price vs Fair Value Recommendation Framework
   → Current ETF price validation and accuracy assessment
   → ETF price positioning within fair value range analysis
   → BUY/SELL/HOLD recommendation validation logic
   → Price gap analysis for recommendation consistency
   → ETF price-based risk assessment and opportunity identification
```

## Output Structure

**File Naming**: `{SECTOR}_{YYYYMMDD}_analysis.json`
**Primary Location**: `./data/outputs/sector_analysis/analysis/`

```json
{
  "metadata": {
    "command_name": "sector_analyst_analyze",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "analyze",
    "sector": "SECTOR_SYMBOL",
    "analysis_methodology": "template_gap_analysis",
    "discovery_file_reference": "path_to_discovery_file",
    "confidence_threshold": "threshold_value"
  },
  "business_cycle_positioning": {
    "current_phase": "early/mid/late_cycle",
    "recession_probability": "0.0-1.0",
    "historical_performance_by_phase": {
      "early_cycle": "performance_metrics",
      "mid_cycle": "performance_metrics",
      "late_cycle": "performance_metrics",
      "recession": "performance_metrics"
    },
    "interest_rate_sensitivity": {
      "duration_analysis": "sector_duration_estimate",
      "leverage_impact": "debt_sensitivity_analysis",
      "rate_coefficients": "correlation_values"
    },
    "inflation_hedge_assessment": {
      "pricing_power": "ability_to_pass_through_costs",
      "real_return_protection": "historical_inflation_correlation",
      "cost_structure_flexibility": "variable_vs_fixed_cost_analysis"
    },
    "gdp_growth_correlation": {
      "gdp_elasticity": "sector_sensitivity_to_gdp_growth_changes",
      "historical_correlation": "correlation_coefficient_with_quarterly_gdp",
      "expansion_performance": "sector_performance_during_gdp_expansions",
      "contraction_performance": "sector_performance_during_gdp_contractions",
      "leading_lagging_relationship": "sector_timing_relative_to_gdp_cycles"
    },
    "confidence": "0.0-1.0"
  },
  "liquidity_cycle_positioning": {
    "fed_policy_stance": "accommodative/neutral/restrictive",
    "credit_market_conditions": {
      "corporate_bond_issuance": "sector_access_to_capital",
      "credit_spreads": "sector_vs_treasury_spreads",
      "refinancing_risk": "near_term_debt_maturity_analysis",
      "banking_standards": "lending_criteria_impact"
    },
    "money_supply_impact": {
      "m2_growth_sensitivity": "sector_liquidity_correlation",
      "velocity_implications": "money_velocity_sector_impact",
      "asset_price_inflation": "valuation_multiple_impact"
    },
    "liquidity_preferences": {
      "sector_allocation_flows": "institutional_flow_analysis",
      "risk_appetite_correlation": "flight_to_quality_impact"
    },
    "employment_sensitivity": {
      "payroll_correlation": "correlation_coefficient_with_nonfarm_payrolls",
      "labor_participation_impact": "sector_sensitivity_to_participation_rate",
      "initial_claims_signaling": "early_warning_correlation_with_claims_spikes",
      "employment_cycle_positioning": "sector_timing_relative_to_employment_cycles",
      "consumer_spending_linkage": "employment_to_sector_demand_transmission"
    },
    "confidence": "0.0-1.0"
  },
  "industry_dynamics_scorecard": {
    "profitability_score": {
      "grade": "A-F",
      "trend": "improving/stable/declining",
      "key_metrics": "margin_sustainability_analysis",
      "supporting_evidence": "quantitative_backing"
    },
    "balance_sheet_score": {
      "grade": "A-F",
      "trend": "improving/stable/declining",
      "debt_trends": "leverage_trajectory_analysis",
      "liquidity_adequacy": "stress_scenario_assessment"
    },
    "competitive_moat_score": {
      "score": "1-10",
      "moat_strength": "barrier_height_assessment",
      "sustainability": "moat_durability_analysis",
      "evidence": "competitive_advantage_validation"
    },
    "regulatory_environment_rating": {
      "rating": "favorable/neutral/hostile",
      "policy_timeline": "regulatory_change_schedule",
      "compliance_costs": "burden_assessment",
      "industry_influence": "regulatory_capture_analysis"
    },
    "confidence": "0.0-1.0"
  },
  "multi_method_valuation": {
    "dcf_analysis": {
      "fair_value": "dcf_calculated_value",
      "wacc": "weighted_average_cost_of_capital",
      "growth_assumptions": "terminal_and_near_term_growth",
      "sensitivity_analysis": "key_assumption_impacts",
      "weight": "40_percent"
    },
    "relative_comps": {
      "fair_value": "peer_multiple_derived_value",
      "peer_multiples": "comparable_company_ratios",
      "premium_discount": "valuation_gap_analysis",
      "multiple_trends": "compression_expansion_analysis",
      "weight": "35_percent"
    },
    "technical_analysis": {
      "fair_value": "technical_target_price",
      "support_resistance": "key_technical_levels",
      "momentum_indicators": "trend_and_momentum_analysis",
      "volume_profile": "trading_pattern_analysis",
      "weight": "25_percent"
    },
    "blended_valuation": {
      "weighted_fair_value": "probability_weighted_target",
      "confidence_intervals": "valuation_range_estimates",
      "scenario_weighting": "bull_base_bear_probabilities"
    },
    "etf_price_vs_fair_value_analysis": {
      "current_etf_price": "current_etf_price_from_discovery_data",
      "fair_value_range": "calculated_fair_value_range",
      "price_gap_analysis": "current_price_vs_fair_value_gap_percentage",
      "recommendation_validation": "buy_sell_hold_logic_validation",
      "price_positioning": "within_below_above_fair_value_range",
      "etf_price_consistency": "cross_source_price_validation_score"
    },
    "confidence": "0.0-1.0"
  },
  "quantified_risk_assessment": {
    "risk_matrix": {
      "economic_recession": {"probability": "0.0-1.0", "impact": "1-5", "risk_score": "calculated"},
      "interest_rate_shock": {"probability": "0.0-1.0", "impact": "1-5", "risk_score": "calculated"},
      "dollar_strength": {"probability": "0.0-1.0", "impact": "1-5", "risk_score": "calculated"},
      "regulatory_changes": {"probability": "0.0-1.0", "impact": "1-5", "risk_score": "calculated"},
      "market_volatility": {"probability": "0.0-1.0", "impact": "1-5", "risk_score": "calculated"}
    },
    "stress_testing": {
      "bear_market_scenario": {"probability": "percentage", "sector_impact": "decline_estimate", "recovery_timeline": "quarters"},
      "recession_scenario": {"probability": "percentage", "sector_impact": "performance_analysis", "recovery_phases": "timeline"},
      "policy_shock_scenario": {"probability": "percentage", "regulatory_impact": "implementation_analysis"}
    },
    "sensitivity_analysis": {
      "key_variables": "most_impactful_assumptions",
      "elasticity_calculations": "percentage_change_impacts",
      "break_even_analysis": "critical_threshold_identification",
      "tornado_diagram": "variable_importance_ranking"
    },
    "aggregate_risk_score": "weighted_total_risk_assessment",
    "confidence": "0.0-1.0"
  },
  "enhanced_economic_sensitivity": {
    "fed_funds_correlation": "correlation_coefficient_with_fed_rates",
    "dxy_impact": "dollar_strength_correlation_and_impact",
    "yield_curve_analysis": "basis_point_impact_per_curve_change",
    "crypto_correlation": "bitcoin_correlation_coefficient",
    "economic_indicators": {
      "unemployment_sensitivity": "correlation_with_unemployment_rate",
      "inflation_sensitivity": "cpi_correlation_analysis",
      "gdp_correlation": "economic_growth_relationship"
    },
    "confidence": "0.0-1.0"
  },
  "macroeconomic_risk_scoring": {
    "gdp_based_risk_assessment": {
      "gdp_deceleration_probability": "probability_of_gdp_growth_decline",
      "recession_vulnerability": "sector_vulnerability_to_gdp_contraction",
      "gdp_elasticity_impact": "impact_modeling_based_on_gdp_elasticity",
      "early_warning_signals": "gdp_leading_indicator_risk_flags"
    },
    "employment_based_risk_assessment": {
      "payroll_decline_probability": "probability_of_employment_deterioration",
      "labor_market_impact": "sector_demand_impact_from_employment_decline",
      "claims_spike_scenarios": "initial_claims_stress_scenario_modeling",
      "employment_cycle_risk": "risk_from_employment_cycle_positioning"
    },
    "combined_macroeconomic_risk": {
      "composite_risk_index": "gdp_employment_combined_risk_score_0.0-1.0",
      "cross_correlation_analysis": "gdp_employment_shock_interaction_effects",
      "recession_probability": "overall_recession_probability_assessment",
      "stress_test_outcomes": "macroeconomic_stress_scenario_results"
    },
    "early_warning_system": {
      "leading_indicators": "array_of_gdp_employment_warning_signals",
      "threshold_breach_probability": "probability_of_critical_threshold_breaches",
      "monitoring_kpis": "key_performance_indicators_for_risk_monitoring",
      "risk_escalation_triggers": "threshold_levels_for_risk_escalation"
    },
    "confidence": "0.0-1.0"
  },
  "investment_recommendation_gap_analysis": {
    "portfolio_allocation_context": {
      "sector_weighting_recommendations": "optimal_sector_allocation_percentages_within_portfolio",
      "cross_sector_optimization": "correlation_based_allocation_adjustments",
      "economic_cycle_rotation": "sector_rotation_timing_and_probability_analysis",
      "risk_adjusted_positioning": "portfolio_level_risk_management_guidance",
      "confidence": "0.0-1.0"
    },
    "economic_cycle_investment_positioning": {
      "rotation_probability_analysis": "sector_rotation_likelihood_across_cycles",
      "economic_timing_considerations": "monetary_fiscal_policy_investment_timing",
      "business_cycle_allocation": "tactical_allocation_based_on_cycle_phase",
      "policy_impact_assessment": "fed_policy_sector_investment_implications",
      "confidence": "0.0-1.0"
    },
    "risk_adjusted_investment_metrics": {
      "sector_sharpe_calculation": "risk_adjusted_return_with_economic_context",
      "downside_risk_assessment": "sector_specific_downside_protection_analysis",
      "volatility_adjusted_returns": "economic_cycle_volatility_considerations",
      "stress_testing_scenarios": "sector_performance_under_economic_stress",
      "confidence": "0.0-1.0"
    },
    "investment_conclusion_confidence": {
      "thesis_confidence_methodology": "investment_conclusion_confidence_scoring",
      "economic_factor_weighting": "gdp_employment_correlation_confidence_impact",
      "allocation_guidance_confidence": "portfolio_allocation_recommendation_reliability",
      "relative_positioning_confidence": "cross_sector_comparison_confidence_assessment",
      "confidence": "0.0-1.0"
    },
    "sector_investment_characteristics": {
      "growth_defensive_classification": "sector_style_and_characteristics_assessment",
      "interest_rate_sensitivity": "duration_risk_and_rate_cycle_positioning",
      "economic_sensitivity_profile": "sector_economic_cycle_sensitivity_analysis",
      "investment_risk_opportunities": "sector_specific_investment_risk_reward_analysis",
      "confidence": "0.0-1.0"
    },
    "etf_price_recommendation_framework": {
      "etf_price_validation": "current_etf_price_accuracy_and_consistency_validation",
      "fair_value_positioning": "etf_price_position_within_calculated_fair_value_range",
      "recommendation_logic": "buy_sell_hold_recommendation_validation_framework",
      "price_gap_assessment": "quantified_price_vs_fair_value_gap_analysis",
      "etf_price_risk_assessment": "etf_price_based_risk_and_opportunity_identification",
      "confidence": "0.0-1.0"
    }
  },
  "analysis_quality_metrics": {
    "gap_coverage": "percentage_of_template_gaps_filled",
    "confidence_propagation": "discovery_confidence_inheritance",
    "analytical_rigor": "methodology_quality_score",
    "evidence_strength": "supporting_data_quality"
  }
}
```

## Analysis Execution Protocol

### Pre-Execution
1. **Load Discovery Data**
   - Load sector discovery JSON: {SECTOR}_{YYYYMMDD}_discovery.json
   - Extract relevant data sections for reference (do not duplicate)
   - Validate discovery data completeness and quality

2. **Identify Template Gaps**
   - Compare discovery data against sector_analysis_template.md requirements
   - Map missing analytical components needed for synthesis
   - Prioritize gaps based on template criticality

3. **Initialize Analysis Framework**
   - Set confidence thresholds for analytical conclusions
   - Prepare economic context from discovery data
   - Load sector aggregates and financial metrics

### Main Execution
1. **Business Cycle Positioning Analysis**
   - Classify current economic cycle phase
   - Calculate recession probability using yield curve data
   - Quantify interest rate sensitivity and inflation hedge capability

2. **Liquidity Cycle Assessment**
   - Analyze Fed policy stance impact on sector
   - Evaluate credit market conditions and capital access
   - Assess money supply impact and liquidity preferences

3. **Industry Dynamics Scorecard**
   - Generate A-F grades for profitability and balance sheet strength
   - Score competitive moats on 1-10 scale
   - Rate regulatory environment as favorable/neutral/hostile

4. **Multi-Method Valuation Framework**
   - Calculate DCF fair values with sensitivity analysis
   - Perform relative comparables analysis
   - Integrate technical analysis for target prices
   - Generate probability-weighted blended valuations

5. **Quantified Risk Assessment**
   - Build probability/impact risk matrices
   - Model stress testing scenarios
   - Perform sensitivity analysis on key variables
   - Calculate aggregate risk scores

6. **Enhanced Economic Sensitivity**
   - Quantify correlations with key economic indicators
   - Measure currency and volatility sensitivities
   - Analyze crypto correlation for risk appetite

7. **GDP/Employment Macroeconomic Integration**
   - Integrate GDP analysis data from discovery phase (GDP, GDPC1, A191RL1Q225SBEA)
   - Incorporate employment indicators from discovery (PAYEMS, CIVPART, ICSA)
   - Calculate GDP growth correlation and employment sensitivity coefficients
   - Generate macroeconomic risk scoring using GDP/employment composite indicators

8. **ETF Price vs Fair Value Recommendation Analysis**
   - Validate current ETF price from discovery data
   - Calculate ETF price vs fair value range gap analysis
   - Apply BUY/SELL/HOLD recommendation validation logic
   - Assess ETF price positioning and recommendation consistency
   - Generate ETF price-based risk assessment and opportunity identification

8. **Investment Recommendation Gap Analysis**
   - Develop portfolio allocation context and sector weighting recommendations
   - Analyze economic cycle investment positioning and rotation probabilities
   - Calculate risk-adjusted investment metrics with economic context
   - Establish investment conclusion confidence framework
   - Define sector investment characteristics and risk-reward profiles

### Post-Execution
1. **Generate Analysis Output**
   - Create JSON output with only NEW analytical insights
   - Reference discovery data without duplication
   - Include confidence scores for all conclusions

2. **Quality Validation**
   - Verify all template gaps are addressed
   - Validate analytical rigor and evidence backing
   - Confirm synthesis phase readiness

3. **Save and Signal**
   - Save output to ./data/outputs/sector_analysis/analysis/
   - Signal readiness for sector_analyst_synthesize phase

## Quality Standards

### Template Gap Coverage
- All template requirements not in discovery must be addressed
- Business cycle and liquidity cycle analysis completed
- Industry scorecard with A-F grades generated
- Multi-method valuation framework implemented
- Quantified risk assessment with probability/impact matrices

### Analytical Rigor
- All conclusions must have confidence scores ≥ confidence_threshold
- Quantitative support for all grading and scoring decisions
- Clear methodology documentation for calculations
- Evidence backing for all probability and impact assignments

### Discovery Data Integration
- Reference discovery data without duplication
- Build upon existing economic context and sector intelligence
- Inherit and propagate discovery confidence scores
- Maintain data continuity for synthesis phase

### Synthesis Phase Readiness
- Output structure compatible with template generation
- All template gaps filled with institutional-quality analysis
- Quality metrics that inform synthesis confidence
- Clear analytical handoff for document generation

**Integration with DASV Framework**: This microservice fills specific analytical gaps required by `./templates/analysis/sector_analysis_template.md`, including investment recommendation preparatory analysis, enabling the synthesis phase to generate complete sector analysis documents with comprehensive Investment Recommendation Summary without additional data collection.

**Author**: Cole Morton
**Confidence**: [Gap analysis confidence based on discovery data quality and analytical methodology rigor]
**Data Quality**: [Template coverage completeness and analytical evidence strength]
