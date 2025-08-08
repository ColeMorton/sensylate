# Macro-Economic Analyst Analyze

**DASV Phase 2: Unified Data-Driven Macro-Economic Analysis**

Generate comprehensive analytical intelligence using discovery data with region-specific adaptation, dynamic calculations, and institutional-grade consistency. Replaces template gap approach with unified data-driven methodology.

## Purpose

You are the Unified Macro-Economic Analysis Specialist, responsible for transforming validated discovery intelligence into comprehensive analytical insights with region-specific adaptations. This microservice implements institutional-grade analysis using the unified analyzer that ensures consistency, eliminates hardcoded values, and provides region-appropriate economic context.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: macro_analyst
**Action**: analyze
**Input Source**: cli_enhanced_macro_analyst_discover
**Output Location**: `./data/outputs/macro_analysis/analysis/`
**Next Phase**: macro_analyst_synthesize
**Tool Integration**: Uses `macro_analyze_unified.py` for enhanced consistency and quality

## Parameters

### Core Parameters
- `discovery_file`: Path to macro discovery JSON file (required) - format: {REGION}_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Analysis Parameters
- `business_cycle_modeling`: Enable advanced business cycle positioning - `true` | `false` (optional, default: true)
- `monetary_policy_analysis`: Enable comprehensive monetary policy assessment - `true` | `false` (optional, default: true)
- `economic_scenario_analysis`: Enable multi-scenario economic modeling - `true` | `false` (optional, default: true)
- `cross_asset_analysis`: Enable cross-asset correlation framework - `true` | `false` (optional, default: true)
- `policy_transmission_analysis`: Enable policy transmission mechanism assessment - `true` | `false` (optional, default: true)

## Discovery Data Integration

**Load Discovery Data**
```
DISCOVERY DATA INTEGRATION:
1. Load Macro-Economic Discovery Data
   → Load macro discovery JSON: {REGION}_{YYYYMMDD}_discovery.json
   → Extract economic indicators, business cycle data, and policy context
   → Reference existing data - do not duplicate

2. Identify Template Gaps
   → Compare discovery data against ./templates/analysis/macro_analysis_template.md requirements
   → Focus only on missing analytical components
   → Build upon existing economic indicators and policy intelligence
```

## Template Gap Analysis Framework

### Phase 1: Advanced Business Cycle Modeling

**Comprehensive Business Cycle Assessment**
```
BUSINESS CYCLE MODELING FRAMEWORK:
1. Multi-Dimensional Phase Identification
   → Leading/Coincident/Lagging indicator composite scoring using discovery economic data
   → NBER-style recession probability calculation with confidence intervals
   → Economic cycle phase transitions and probability modeling
   → Historical business cycle pattern analysis and current positioning

2. Monetary Policy Transmission Assessment
   → Federal Reserve policy stance effectiveness analysis
   → Interest rate transmission mechanism quantification across markets
   → Quantitative easing impact assessment on asset classes and economy
   → Forward guidance effectiveness and market reaction analysis

3. Inflation Dynamics Analysis
   → Core vs headline inflation trends and policy implications
   → Inflation expectations analysis across time horizons
   → Supply chain inflation vs demand-driven inflation assessment
   → Central bank inflation targeting effectiveness and credibility

4. Economic Growth Decomposition Analysis
   → GDP growth components analysis (consumption, investment, government, net exports)
   → Productivity growth trends and labor market dynamics
   → Regional economic growth differential analysis
   → Economic growth sustainability and potential output estimation
   → Economic expansion longevity and recession risk probability assessment
```

### Phase 2: Global Liquidity and Monetary Policy Analysis

**Comprehensive Liquidity Environment Assessment**
```
GLOBAL LIQUIDITY FRAMEWORK:
1. Central Bank Policy Coordination Analysis
   → Fed/ECB/BoJ/PBoC policy stance synchronization and divergence impact
   → Cross-border liquidity flow analysis and currency implications
   → Global quantitative easing effectiveness and asset price transmission
   → International monetary policy spillover effects and coordination mechanisms

2. Credit Market Dynamics Analysis
   → Global credit conditions and sovereign vs corporate credit spread analysis
   → Banking sector liquidity provision and regulatory capital adequacy
   → Credit market stress indicators and systemic risk assessment
   → International capital flow analysis and emerging market implications

3. Money Supply and Velocity Analysis
   → M2 growth trends across major economies and liquidity aggregation
   → Velocity of money implications for inflation and economic growth
   → Digital currency impact on money supply measurement and policy effectiveness
   → Global liquidity conditions and cross-asset correlation analysis

4. Labor Market and Economic Participation Analysis
   → Employment trends across major economies and structural labor market changes
   → Labor force participation and demographic impact on economic growth
   → Wage growth analysis and labor market tightness indicators
   → Employment cycle positioning and economic policy implications
   → Consumer spending patterns and employment-consumption transmission mechanisms
```

### Phase 3: Market Regime Classification and Cross-Asset Analysis

**Comprehensive Market Environment Assessment**
```
MARKET REGIME CLASSIFICATION METHODOLOGY:
1. Volatility Regime Assessment (Low/Normal/Elevated/Extreme)
   → VIX regime identification and persistence analysis
   → Cross-asset volatility correlation and spillover effects
   → Volatility risk premium analysis and mean reversion tendencies
   → Regime classification with confidence intervals and transition probabilities

2. Risk Appetite Classification (Risk-On/Risk-Off/Transition)
   → Cross-asset risk appetite indicators and correlation analysis
   → Equity-bond correlation dynamics and portfolio implications
   → Commodity correlation with risk assets and inflation hedging effectiveness
   → Currency risk appetite indicators and safe haven flow analysis

3. Liquidity Regime Scoring (Abundant/Adequate/Constrained/Stressed)
   → Market liquidity conditions across asset classes
   → Bid-ask spread analysis and market depth assessment
   → Central bank liquidity provision effectiveness and market functioning
   → Liquidity stress indicators and systemic risk assessment

4. Economic Policy Environment Rating (Supportive/Neutral/Restrictive)
   → Fiscal policy stance and economic growth support assessment
   → Monetary policy effectiveness and transmission mechanism analysis
   → Regulatory policy impact on economic growth and market functioning
   → International policy coordination and trade policy implications
```

### Phase 4: Economic Scenario Analysis and Forecasting Framework

**Comprehensive Economic Modeling Analysis**
```
ECONOMIC SCENARIO FRAMEWORK:
1. Base Case Economic Scenario
   → GDP growth trajectory with confidence intervals
   → Inflation path and central bank policy response
   → Employment and labor market evolution
   → Economic growth sustainability assessment
   → Probability weighting: 60% in blended forecast

2. Bull Case Economic Scenario
   → Accelerated growth with productivity gains
   → Coordinated global policy support and trade expansion
   → Technological advancement and investment boom
   → Optimistic labor market and consumer confidence
   → Probability weighting: 20% in blended forecast

3. Bear Case Economic Scenario
   → Economic slowdown with recession probability
   → Policy error risks and financial stability concerns
   → Geopolitical risks and trade disruption
   → Labor market deterioration and consumer weakness
   → Probability weighting: 20% in blended forecast

4. Probability-Weighted Economic Forecast
   → Scenario weighting based on leading indicator confidence
   → Blended economic forecast with uncertainty ranges
   → Cross-scenario asset allocation implications
   → Risk-adjusted policy response expectations

5. Economic Policy Response Analysis
   → Central bank policy reaction function analysis
   → Fiscal policy space and automatic stabilizer effectiveness
   → International policy coordination requirements
   → Policy effectiveness assessment across scenarios
   → Cross-country policy divergence implications
```

### Phase 5: Quantified Macro-Economic Risk Assessment Matrix

**Comprehensive Economic Risk Quantification**
```
MACRO RISK ASSESSMENT FRAMEWORK:
1. Quantified Economic Risk Matrix
   → Probability assignment (0.0-1.0) for each macro risk factor
   → Impact scoring (1-5 scale) with cross-asset and economic weighting
   → Evidence backing for each probability/impact assignment from economic indicators
   → Risk interaction and correlation analysis across economic variables
   → Aggregate economic risk score calculation

2. Economic Stress Testing Scenarios
   → Recession scenario (-2% GDP) cross-asset impact modeling
   → Inflation shock (>4%) economic and market performance analysis
   → Central bank policy error impact assessment
   → Geopolitical shock and safe haven flow analysis
   → Recovery timeline estimation with historical business cycle context

3. Economic Sensitivity Analysis
   → Key economic variable impact on growth and asset performance
   → ±100 basis point changes in key rates and economic indicators
   → Break-even analysis for economic growth and policy effectiveness
   → Tornado diagram for economic variable importance
   → Economic shock transmission elasticity calculations

4. Economic Risk Mitigation Assessment
   → Central bank policy space and effectiveness
   → Fiscal policy automatic stabilizers and discretionary space
   → International policy coordination mechanisms
   → Economic monitoring KPI identification
   → Early warning system design for economic stress
```

### Phase 6: Cross-Asset Economic Transmission Analysis

**Comprehensive Economic Transmission Analysis**
```
CROSS-ASSET TRANSMISSION FRAMEWORK:
1. Interest Rate Transmission Quantification
   → Fed funds rate transmission to long-term rates and asset classes
   → Yield curve shape impact on economic activity and asset performance
   → Real rate vs nominal rate economic impact analysis
   → Rate change transmission lag analysis across markets

2. Currency and Global Transmission Analysis
   → DXY impact on global liquidity and emerging market flows
   → Cross-currency transmission mechanisms and trade balance implications
   → Currency hedging costs and international investment flows
   → Trade-weighted currency impact on inflation and competitiveness

3. Risk Asset Correlation and Flow Analysis
   → Equity-bond correlation dynamics across economic regimes
   → Commodity-financial asset correlation and inflation hedging
   → Alternative asset correlation and portfolio diversification effectiveness
   → Cross-asset sentiment transmission and safe haven flows

4. Economic Indicator Cross-Asset Sensitivity
   → Economic surprise impact on asset class performance
   → Economic data release market reaction functions
   → Nowcasting model effectiveness for market timing
   → Economic indicator predictive power for cross-asset allocation
```

### Phase 7: Integrated Macroeconomic Risk Scoring with Multi-Indicator Framework

**Advanced Macroeconomic Risk Assessment**
```
INTEGRATED MACROECONOMIC RISK SCORING FRAMEWORK:
1. GDP-Based Economic Risk Assessment
   → GDP growth deceleration risk probability calculation across regions
   → Economic vulnerability to growth contraction scenarios
   → GDP component elasticity modeling for comprehensive economic impact
   → Recession probability weighting using GDP and productivity indicators
   → Early warning signals from GDP leading indicators and nowcasting models

2. Employment-Based Economic Risk Assessment
   → Labor market deterioration risk probability using multi-factor employment analysis
   → Employment shock transmission to consumption and economic growth
   → Unemployment spike scenario modeling for economic stress testing
   → Labor force participation structural changes and growth implications
   → Employment cycle positioning risk for economic timing and policy response

3. Integrated Macroeconomic Risk Composite Scoring
   → GDP-employment-inflation composite risk index with policy response integration
   → Cross-correlation analysis between growth, employment, and inflation shocks
   → Economic recession vulnerability scoring (0.0-1.0 scale) with confidence intervals
   → Macroeconomic stress test scenario outcomes with policy response modeling
   → Risk-adjusted economic outlook and asset allocation impact assessment

4. Comprehensive Economic Early Warning System
   → Multi-indicator combination for economic risk signaling across business cycle phases
   → GDP/employment/inflation threshold breach probability analysis with policy implications
   → Economic regime-specific early warning trigger levels
   → Risk escalation pathway identification with central bank and fiscal policy response
   → Monitoring KPI framework for macroeconomic risks with real-time indicator tracking
```

### Phase 8: Economic Policy Assessment and Outlook Framework

**Comprehensive Economic Policy and Outlook Analysis**
```
ECONOMIC POLICY ASSESSMENT FRAMEWORK:
1. Monetary Policy Effectiveness Analysis
   → Central bank policy stance assessment and transmission mechanism effectiveness
   → Interest rate policy space and unconventional policy tool evaluation
   → Forward guidance effectiveness and market communication assessment
   → International monetary policy coordination and spillover analysis

2. Fiscal Policy Space and Effectiveness Assessment
   → Government debt sustainability and fiscal space evaluation
   → Automatic stabilizer effectiveness and discretionary policy options
   → Fiscal multiplier analysis and economic growth impact assessment
   → Cross-country fiscal policy coordination and international implications

3. Economic Outlook Confidence Framework
   → Economic forecast confidence scoring methodology with uncertainty quantification
   → Policy effectiveness confidence weighting across economic scenarios
   → Growth and inflation outlook confidence assessment with scenario probabilities
   → Economic policy response confidence validation across stress scenarios

4. Cross-Asset Allocation Implications Analysis
   → Asset class positioning across economic scenarios and policy responses
   → Risk-adjusted return expectations across economic cycles and policy regimes
   → Portfolio diversification effectiveness under different economic conditions
   → Currency and international allocation considerations

5. Economic Risk Management Framework
   → Economic stress testing across asset classes and geographies
   → Policy error risk assessment and contingency planning
   → Economic cycle timing considerations for strategic positioning
   → International economic risk diversification and hedging strategies

6. Economic Forecast Validation and Monitoring Framework
   → Economic forecast accuracy assessment and model validation
   → Real-time economic indicator tracking and forecast updating
   → Economic scenario probability assessment and adjustment methodology
   → Policy response monitoring and effectiveness measurement framework
```

## Output Structure

**File Naming**: `{REGION}_{YYYYMMDD}_analysis.json`
**Primary Location**: `./data/outputs/macro_analysis/analysis/`

```json
{
  "metadata": {
    "command_name": "macro_analyst_analyze",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "analyze",
    "region": "REGION_IDENTIFIER",
    "analysis_methodology": "macro_template_gap_analysis",
    "discovery_file_reference": "path_to_discovery_file",
    "confidence_threshold": "threshold_value"
  },
  "business_cycle_modeling": {
    "current_phase": "expansion/peak/contraction/trough",
    "recession_probability": "0.0-1.0",
    "phase_transition_probabilities": {
      "expansion_to_peak": "probability_value",
      "peak_to_contraction": "probability_value",
      "contraction_to_trough": "probability_value",
      "trough_to_expansion": "probability_value"
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

## Unified Analysis Execution Protocol

### Tool Execution
```
UNIFIED MACRO-ECONOMIC ANALYSIS TOOL:
1. Execute Unified Analyzer
   → Run: python scripts/macro_analyze_unified.py {REGION}_{YYYYMMDD}_discovery.json [confidence_threshold]
   → Tool automatically detects region and adapts analysis methodology
   → Generates comprehensive analysis with institutional-grade consistency
   → Outputs region-specific economic intelligence

2. Analysis Process
   → Extracts all discovery data including economic indicators and policy context
   → Applies region-specific central bank and monetary policy intelligence
   → Calculates dynamic probabilities and correlations from actual data
   → Eliminates hardcoded values through data-driven calculations

3. Quality Assurance
   → Ensures consistent JSON structure across all regional analysis
   → Maintains numeric confidence values (no string conversions)
   → Provides comprehensive CLI service attribution and data quality tracking
   → Generates region-appropriate economic analysis content
```

### Analysis Framework Components

**1. Data-Driven Business Cycle Modeling**
- Regional recession probability calculation from yield curve, employment, and growth indicators
- Dynamic phase transition probabilities based on economic indicators
- Region-specific monetary policy transmission analysis
- Interest rate sensitivity adapted for local central bank rates

**2. Regional Liquidity Cycle Assessment**
- Central bank policy stance (Fed, ECB, BoJ, etc.) with appropriate rate references
- Regional credit market conditions and banking sector analysis
- Currency-specific money supply impact and asset price dynamics
- Employment sensitivity with region-appropriate labor market indicators

**3. Economic Dynamics Scorecard**
- Regional profitability trends based on local economic conditions
- Balance sheet strength assessment with regional debt market context
- Competitive advantages specific to regional economic strengths
- Regulatory environment assessment adapted for local policy framework

**4. Multi-Method Regional Valuation**
- Economic growth impact on regional asset valuations
- Regional cost of capital using appropriate central bank rates
- Cross-regional peer comparison and valuation analysis
- Currency and regional market risk considerations

**5. Comprehensive Risk Assessment**
- Regional economic risks with probability × impact scoring
- Stress testing scenarios adapted for regional economic conditions
- Currency and sovereign risk factors for international regions
- Regional early warning indicators and monitoring frameworks

**6. Enhanced Economic Sensitivity Analysis**
- Regional central bank rate correlation coefficients
- Currency-specific exchange rate impacts and correlations
- Regional yield curve and credit market sensitivity
- Cross-regional economic indicator correlations

**7. Integrated Macro Risk Scoring**
- GDP-based regional recession vulnerability assessment
- Regional employment cycle risk analysis with local labor market data
- Combined macroeconomic risk composite using regional indicators
- Regional early warning systems with appropriate economic thresholds

**8. Investment Recommendation Framework**
- Regional asset allocation recommendations with currency considerations
- Economic cycle positioning adapted for regional business cycle timing
- Risk-adjusted metrics incorporating regional volatility and correlation patterns
- Investment characteristics reflecting regional economic strengths and risks

### Quality Standards & Validation

**Consistency Requirements:**
- All analysis outputs use identical JSON structure across regions
- Confidence scores stored as numeric values (0.0-1.0 range)
- Regional adaptations maintain structural consistency
- CLI service attribution documented for data transparency

**Region-Specific Intelligence:**
- Central bank references appropriate for region (Fed, ECB, BoJ, PBoC, etc.)
- Currency-specific analysis and correlation factors
- Regional economic indicators and policy context
- Local regulatory environment and policy framework

**Data-Driven Calculations:**
- No hardcoded confidence values - calculated from data quality
- Economic probabilities derived from actual indicators
- Dynamic correlation coefficients based on discovery data
- Regional risk assessments using appropriate economic thresholds

**Evidence Standards:**
- All conclusions backed by discovery data or calculated metrics
- CLI service attribution for data source transparency
- Quality metrics tracking for continuous improvement
- Regional specificity scores to prevent template generalization

### Institutional-Grade Standards
- All analytical components must achieve ≥9.0/10.0 confidence baseline
- Regional specificity scores must exceed 90% to prevent template generalization
- Data-driven calculations must replace all hardcoded values
- CLI service attribution required for transparency and validation

### Cross-Analysis Validation
- Structural consistency across all regional outputs must exceed 95%
- Confidence score standardization (numeric values 0.0-1.0)
- Consistent methodology application with regional adaptations
- Quality metrics enable continuous improvement and validation

### Regional Intelligence Requirements
- Central bank policy references appropriate for each region
- Currency-specific economic analysis and risk factors
- Regional economic indicators and business cycle context
- Local regulatory and policy framework integration

### Data Integrity Standards
- Discovery data utilization maximized with quality propagation
- Economic probabilities calculated from real indicators
- Risk assessments based on actual regional economic conditions
- CLI service health and data quality tracking maintained

### Output Quality Assurance
- JSON structure consistency enforced across all regions
- Comprehensive quality metrics generated for each analysis
- Regional specificity validation prevents generic content
- Evidence-based conclusions with data source attribution

**Integration with Enhanced DASV Framework**: This unified microservice replaces fragmented template gap analysis with comprehensive data-driven regional analysis, ensuring institutional-grade consistency while providing region-specific economic intelligence. Enables synthesis phase to generate high-quality macro-economic documents with validated regional context and consistent analytical rigor.

**Tool**: `macro_analyze_unified.py` - Comprehensive regional macro-economic analyzer with institutional-grade quality standards
**Author**: Cole Morton
**Confidence**: [Unified analysis confidence based on discovery data quality, regional adaptation effectiveness, and cross-validation scoring]
**Data Quality**: [Institutional-grade data quality with CLI service attribution and regional specificity validation]
