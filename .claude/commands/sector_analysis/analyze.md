# Sector Analyst Analyze

**DASV Phase 2: Framework-Coordinated Sector Analysis**

Generate sector-specific analytical intelligence using the dasv-analysis-agent as framework coordinator, focusing on domain-specific sector analysis components while leveraging shared framework infrastructure for universal elements.

## Purpose

You are the Sector Analysis Domain Specialist, working in coordination with the **dasv-analysis-agent** to generate sector-specific analytical components within the DASV Analysis Phase framework. This microservice provides specialized sector analysis expertise while utilizing shared quality standards, templates, and macros managed by the framework coordinator.

## Microservice Integration

**Framework**: DASV Phase 2 - Analysis Phase
**Framework Coordinator**: dasv-analysis-agent (handles universal components)
**Role**: sector_analyst (domain-specific specialist)
**Action**: analyze
**Input Source**: cli_enhanced_sector_analyst_discover
**Output Location**: `./data/outputs/sector_analysis/analysis/`
**Next Phase**: sector_analyst_synthesize
**Template Foundation**: `./scripts/templates/shared/base_analysis_template.j2` (managed by dasv-analysis-agent)
**Shared Macros**: `./scripts/templates/shared/macros/` (framework components)
**Domain Focus**: Sector-specific analysis components within framework structure

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

## DASV Analysis Phase Framework Integration

### Framework Coordination Protocol

**Agent Integration**: This command leverages the **dasv-analysis-agent** as the DASV Analysis Phase Framework Coordinator to handle universal framework components while maintaining domain-specific sector analysis expertise.

**Execution Pattern**:
1. **Framework Initialization**: dasv-analysis-agent validates discovery data and initializes universal JSON structure
2. **Domain Analysis**: Sector analyst executes specialized sector analysis components
3. **Framework Integration**: dasv-analysis-agent applies shared quality metrics, risk assessment, and economic context
4. **Output Coordination**: dasv-analysis-agent manages final JSON output using base_analysis_template.j2

### Discovery Data Integration (Framework-Coordinated)

**Framework-Managed Discovery Integration**:
```
FRAMEWORK-COORDINATED DATA INTEGRATION:
1. Load Sector Discovery Data (dasv-analysis-agent)
   → Validate sector discovery JSON: {SECTOR}_{YYYYMMDD}_discovery.json
   → Ensure complete data preservation with fail-fast validation
   → Initialize universal framework structure

2. Domain-Specific Analysis Preparation (sector_analyst)
   → Extract sector aggregates and financial metrics for domain analysis
   → Identify sector-specific analytical components needed
   → Build upon framework-managed economic context and sector intelligence
```

## Domain-Specific Analytical Framework

**Framework Note**: Universal components (economic context, risk assessment, quality metrics) are handled by dasv-analysis-agent using shared macros. This section focuses on sector analysis domain expertise.

### Phase 1: Business Cycle Positioning Analysis (Domain-Specific)

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

### Phase 2: Liquidity Cycle Positioning Analysis (Domain-Specific)

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

### Phase 3: Industry Dynamics Scorecard (Domain-Specific)

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

### Phase 4: Multi-Method Valuation Framework (Domain-Specific)

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

### Phase 5: Sector-Specific Risk Analysis (Domain-Specific)

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

## Framework-Coordinated Output Structure

**File Naming**: `{SECTOR}_{YYYYMMDD}_analysis.json` (managed by dasv-analysis-agent)
**Primary Location**: `./data/outputs/sector_analysis/analysis/`
**Template Foundation**: Uses `base_analysis_template.j2` with sector-specific extensions
**Shared Macros**: Leverages confidence_scoring_macro.j2, risk_assessment_macro.j2, economic_sensitivity_macro.j2

**Framework Integration**: The dasv-analysis-agent manages universal framework sections while this command provides domain-specific sector analysis content.

```json
{
  "metadata": {
    "command_name": "sector_analyst_analyze",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "analyze",
    "framework_coordinator": "dasv-analysis-agent",
    "domain_specialist": "sector_analyst",
    "sector": "SECTOR_SYMBOL",
    "analysis_methodology": "dasv_framework_coordinated_sector_analysis",
    "discovery_file_reference": "path_to_discovery_file",
    "target_confidence_threshold": "threshold_value",
    "discovery_confidence_inherited": "discovery_data_quality_score",
    "economic_context_integration": "boolean",
    "cli_services_utilized": "array_of_operational_cli_services"
  },
  "discovery_data_inheritance": {
    "metadata": "framework_managed_discovery_preservation",
    "data_completeness": "percentage_of_discovery_data_preserved",
    "inheritance_validation": "dasv_analysis_agent_validation_status",
    "critical_data_preserved": {
      "market_data": "boolean",
      "entity_overview": "boolean",
      "economic_context": "boolean",
      "cli_validation": "boolean",
      "peer_data": "boolean"
    }
  },
  "economic_context": {
    "metadata": "framework_managed_by_dasv_analysis_agent",
    "interest_rate_environment": "restrictive/neutral/accommodative",
    "yield_curve_signal": "normal/inverted/flat",
    "economic_indicators": {
      "fed_funds_rate": "value",
      "unemployment_rate": "value",
      "gdp_growth": "value",
      "inflation_rate": "value"
    },
    "policy_implications": "array_of_policy_impacts",
    "economic_sensitivity": "framework_managed_sensitivity_analysis"
  },
  "cli_service_validation": {
    "metadata": "framework_managed_by_dasv_analysis_agent",
    "service_health": {
      "service_name": "healthy/degraded/unavailable"
    },
    "health_score": "0.0-1.0_aggregate_health",
    "services_operational": "integer_count",
    "services_healthy": "boolean_overall_status",
    "data_quality_scores": {
      "service_name": "0.0-1.0_per_service"
    }
  },
  "sector_analysis": {
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
    }
  },
  "risk_assessment": {
    "metadata": "framework_managed_using_risk_assessment_macro",
    "risk_matrix": {
      "risk_category": [{
        "risk": "string",
        "probability": "0.0-1.0",
        "impact": "1-5",
        "risk_score": "probability_x_impact",
        "evidence": "string",
        "monitoring_kpis": ["string"]
      }]
    },
    "quantified_assessment": {
      "aggregate_risk_score": "number",
      "risk_probability_distribution": "object",
      "detailed_probability_impact_matrix": "object",
      "mitigation_strategies": "object",
      "monitoring_metrics": "object"
    },
    "scenario_analysis": {
      "scenario_name": {
        "probability": "number",
        "impact": "string",
        "recovery_timeline": "string",
        "confidence": "number"
      }
    }
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
  "analytical_insights": {
    "metadata": "framework_managed_structured_findings",
    "key_findings": "array_minimum_3_findings",
    "investment_implications": "array_minimum_3_implications",
    "analysis_limitations": "array_minimum_2_limitations",
    "follow_up_research": "array_minimum_3_recommendations"
  },
  "quality_metrics": {
    "metadata": "framework_managed_using_confidence_scoring_macro",
    "analysis_confidence": "0.0-1.0_overall_confidence",
    "data_quality_impact": "0.0-1.0_data_influence",
    "methodology_rigor": "0.0-1.0_process_quality",
    "evidence_strength": "0.0-1.0_support_quality",
    "statistical_significance": "0.0-1.0_where_applicable",
    "sample_adequacy": "0.0-1.0_where_applicable"
  }
}
```

## DASV Analysis Phase Execution Protocol (Framework-Coordinated)

### Framework Integration Approach

**Execution Coordination**: This protocol leverages the **dasv-analysis-agent** to handle universal framework components while maintaining sector analysis domain expertise.

**10-Step DASV Analysis Process Integration**:
1. **Initialize Framework Structure** (dasv-analysis-agent)
2. **Populate Universal Metadata** (dasv-analysis-agent)
3. **Validate Discovery Data Inheritance** (dasv-analysis-agent)
4. **Integrate Economic Context** (dasv-analysis-agent)
5. **Perform Domain-Specific Analysis** (sector_analyst)
6. **Apply Risk Assessment Framework** (dasv-analysis-agent using risk_assessment_macro.j2)
7. **Generate Analytical Insights** (coordinated)
8. **Calculate Quality Metrics** (dasv-analysis-agent using confidence_scoring_macro.j2)
9. **Validate Against Schema** (dasv-analysis-agent)
10. **Export JSON Output** (dasv-analysis-agent using base_analysis_template.j2)

### Pre-Execution (Framework-Coordinated)

**Agent Invocation**:
```
INVOKE dasv-analysis-agent WITH:
- discovery_file: {SECTOR}_{YYYYMMDD}_discovery.json
- analysis_type: sector
- confidence_threshold: 0.9
- framework_phase: initialize
```

**Framework Validation** (Steps 1-4):
1. **Initialize Framework Structure**: dasv-analysis-agent sets up universal JSON architecture
2. **Populate Universal Metadata**: Framework execution context and methodology tracking
3. **Validate Discovery Data Inheritance**: Complete data preservation verification with fail-fast
4. **Integrate Economic Context**: Economic regime and indicator integration using economic_sensitivity_macro.j2

**Domain Preparation**:
- Load sector-specific parameters and thresholds
- Initialize sector analysis frameworks and metrics
- Prepare sector aggregates and financial data
- Set up domain-specific quality gates

### Main Execution (Domain-Specific Analysis - Step 5)

**Sector Analysis Domain Expertise**:
1. **Business Cycle Positioning Analysis**
   - Classify current economic cycle phase for sector impact
   - Calculate recession probability using sector-specific factors
   - Quantify interest rate sensitivity and inflation hedge capability
   - Analyze GDP growth correlation and sector elasticity

2. **Liquidity Cycle Assessment**
   - Analyze Fed policy stance impact on sector dynamics
   - Evaluate credit market conditions and sector capital access
   - Assess money supply impact and liquidity preferences
   - Calculate employment sensitivity and consumer spending linkage

3. **Industry Dynamics Scorecard**
   - Generate A-F grades for sector profitability and balance sheet strength
   - Score competitive moats on 1-10 scale with sector context
   - Rate regulatory environment as favorable/neutral/hostile
   - Assess sector-specific competitive dynamics

4. **Multi-Method Valuation Framework**
   - Calculate DCF fair values with sector-specific assumptions
   - Perform relative sector comparables analysis
   - Integrate technical analysis for sector target prices
   - Generate probability-weighted blended sector valuations
   - Analyze ETF price vs fair value positioning

5. **Investment Recommendation Analysis**
   - Develop portfolio allocation context and sector weighting recommendations
   - Analyze economic cycle investment positioning and rotation probabilities
   - Calculate risk-adjusted investment metrics with sector context
   - Establish investment conclusion confidence framework
   - Define sector investment characteristics and risk-reward profiles

**Framework Integration Points**:
- Risk assessment handled by dasv-analysis-agent (Step 6)
- Economic context provided by framework coordination
- Quality metrics calculated using shared confidence scoring

### Post-Execution (Framework-Coordinated - Steps 6-10)

**Agent Coordination**:
```
INVOKE dasv-analysis-agent WITH:
- domain_analysis: sector_analysis_results
- framework_phase: finalize
- output_template: base_analysis_template.j2
```

**Framework Completion** (Steps 6-10):
6. **Apply Risk Assessment Framework**: Generate quantified risk matrices using risk_assessment_macro.j2
7. **Generate Analytical Insights**: Structured findings and implications with minimum requirements
8. **Calculate Quality Metrics**: Institutional-grade confidence scoring using confidence_scoring_macro.j2
9. **Validate Against Schema**: Framework compliance verification with fail-fast
10. **Export JSON Output**: File generation using base_analysis_template.j2 with proper naming conventions

**Final Validation**:
- Verify >90% institutional confidence threshold
- Confirm framework schema compliance
- Validate synthesis phase readiness
- Log performance metrics and quality scores

## Framework-Coordinated Quality Standards

### Institutional-Grade Framework Standards (Managed by dasv-analysis-agent)
- **Confidence Threshold**: >90% minimum for institutional grade (targeting >95% for enhanced)
- **Service Health**: >80% CLI service operational status requirement
- **Data Completeness**: >85% for comprehensive analysis certification
- **Multi-Source Validation**: <2% variance tolerance across data sources
- **Schema Compliance**: 100% validation against Analysis phase output specification

### Domain-Specific Quality Requirements (Sector Analysis)
- **Business Cycle Analysis**: Quantified correlations and elasticity measurements
- **Valuation Framework**: Multi-method approach with probability weighting
- **Industry Scorecard**: A-F grades with quantitative support and evidence
- **Investment Analysis**: Portfolio allocation guidance with confidence intervals

### Framework Validation Requirements (Enforced by dasv-analysis-agent)
- **Required Field Presence**: All universal framework sections must be populated
- **Data Type Conformance**: Confidence scores 0.0-1.0, risk probabilities decimal format
- **Value Range Constraints**: Impact scores 1-5, timestamps ISO 8601 format
- **Minimum Array Lengths**: Key findings (3+), implications (3+), limitations (2+), research (3+)
- **File Organization**: Correct naming `{SECTOR}_{YYYYMMDD}_analysis.json` in appropriate directory

### Fail-Fast Quality Enforcement (Framework-Managed)
- Discovery data inheritance below 100% for critical data points triggers immediate failure
- CLI service health below 80% operational threshold triggers immediate failure
- Confidence scores not meeting 90% institutional minimum triggers immediate failure
- Missing required framework sections triggers immediate failure
- Schema validation failures trigger immediate failure with specific violation details

### Integration Requirements (Framework-Coordinated)
- **Template Utilization**: Uses base_analysis_template.j2 with sector-specific inheritance blocks
- **Macro Integration**: Leverages shared macros for confidence scoring, risk assessment, economic sensitivity
- **Quality Propagation**: Framework confidence scores feed into overall analysis confidence
- **Synthesis Readiness**: Structured output compatible with synthesis phase requirements

**Integration with DASV Framework**: This domain-specific microservice works in coordination with the dasv-analysis-agent to provide sector-specific analytical components within the DASV Analysis Phase framework, utilizing shared framework components while maintaining specialized sector analysis expertise. The analysis provides domain-specific input for sector investment recommendations and synthesis phase document generation.

**Framework Coordination**: dasv-analysis-agent
**Domain Expertise**: Sector Analysis Specialist
**Template Foundation**: base_analysis_template.j2 with sector inheritance blocks
**Shared Components**: confidence_scoring_macro.j2, risk_assessment_macro.j2, economic_sensitivity_macro.j2
**Quality Standards**: Institutional-grade framework compliance (>90% confidence threshold)

**Author**: Cole Morton
**Confidence**: [Framework-coordinated analysis confidence calculated from discovery data quality, economic context validation, and institutional-grade quality standards]
**Data Quality**: [Framework-managed data quality score based on CLI service reliability, economic context freshness, and comprehensive validation protocols]
