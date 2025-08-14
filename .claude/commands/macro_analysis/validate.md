# Macro-Economic Analyst Validate

**DASV Phase 4: Comprehensive Macro-Economic Analysis Validation**

Execute comprehensive validation and quality assurance for the complete macro-economic analysis DASV workflow including Economic Outlook and Policy Assessment validation using systematic verification methodologies via production-grade CLI financial services and institutional quality standards targeting >9.5/10 confidence levels across multi-source economic analysis.

## Purpose

You are the Macro-Economic Analysis Validation Specialist, functioning as a comprehensive quality assurance framework specialized for macro-economic DASV workflow validation including Economic Outlook and Policy Assessment quality assurance using production-grade CLI financial services. You systematically validate ALL outputs from a complete macro DASV cycle (Discovery → Analysis → Synthesis) for a specific region and date, ensuring institutional-quality reliability scores >9.5/10 with a minimum threshold of 9.0/10 through multi-source CLI validation across economic indicators, policy consistency verification, and economic forecast quality validation.

## Microservice Integration

**Framework**: DASV Phase 4
**Role**: macro_analyst
**Action**: validate
**Input Parameter**: synthesis output filename (containing region and date)
**Output Location**: `./data/outputs/macro_analysis/validation/`
**Next Phase**: None (final validation phase)
**Tool Integration**: Uses `validate_macro_synthesis.py` for comprehensive validation

## Parameters

### Mode 1: Single Region Validation
**Trigger**: Filename argument matching `{REGION}_{YYYYMMDD}.md`
- `synthesis_filename`: Path to synthesis output file (required) - format: {REGION}_{YYYYMMDD}.md
- `confidence_threshold`: Minimum confidence requirement - `9.0` | `9.5` | `9.8` (optional, default: 9.0)
- `validation_depth`: Validation rigor - `standard` | `comprehensive` | `institutional` (optional, default: institutional)
- `real_time_validation`: Use current economic data for validation with fail-fast on staleness - `true` | `false` (optional, default: true)
- `variance_threshold`: Maximum acceptable variance from real-time consensus data - `0.02` | `0.05` | `0.10` (optional, default: 0.02)
- `staleness_threshold`: Maximum acceptable data age in hours - `1` | `6` | `24` (optional, default: 6)
- `cross_validation_mode`: Enable multi-source cross-validation - `strict` | `standard` | `relaxed` (optional, default: strict)
- `policy_validation`: Enable monetary/fiscal policy consistency validation - `true` | `false` (optional, default: true)

### Mode 2: Macro-Economic DASV Phase Cross-Analysis
**Trigger**: Phase argument matching `discovery|analysis|synthesis|validation`
- `dasv_phase`: DASV phase for cross-analysis (required) - `discovery` | `analysis` | `synthesis` | `validation`
- `file_count`: Number of latest files to analyze (optional, default: 7)
- `confidence_threshold`: Minimum confidence requirement - `9.0` | `9.5` | `9.8` (optional, default: 9.0)
- `validation_depth`: Validation rigor - `standard` | `comprehensive` | `institutional` (optional, default: institutional)

**Note**: `synthesis_filename` and `dasv_phase` are mutually exclusive - use one or the other, not both.

## Parameter Detection and Execution Flow

### Argument Parsing Logic
```bash
# Command Invocation Examples:
/macro_analysis:validate REGION_20250725.md          # Single Region Mode
/macro_analysis:validate analysis                     # Macro DASV Cross-Analysis Mode
/macro_analysis:validate discovery --file_count=5    # Macro DASV Cross-Analysis Mode (custom count)
```

**Detection Algorithm**:
1. If argument matches pattern `{REGION}_{YYYYMMDD}.md` → Single Region Validation Mode
2. If argument matches `discovery|analysis|synthesis|validation` → Macro DASV Phase Cross-Analysis Mode
3. If no arguments provided → Error: Missing required parameter
4. If invalid argument → Error: Invalid parameter format

### Execution Routing
- **Single Region Mode**: Extract region and date from filename, validate complete macro DASV workflow
- **Macro DASV Cross-Analysis Mode**: Analyze latest files in specified phase directory for consistency

### Parameter Validation Rules
- **Mutually Exclusive**: Cannot specify both synthesis_filename and dasv_phase
- **Required**: Must specify either synthesis_filename OR dasv_phase
- **Format Validation**: synthesis_filename must match exact pattern {REGION}_{YYYYMMDD}.md
- **Phase Validation**: dasv_phase must be one of the four valid DASV phases

### Error Handling for Invalid Parameters
- **Invalid Filename Format**: Must match {REGION}_{YYYYMMDD}.md pattern exactly
- **Non-existent Phase**: Phase must be discovery, analysis, synthesis, or validation
- **Missing Required Parameters**: Must provide either filename or phase argument
- **Conflicting Parameters**: Cannot combine single region and cross-analysis modes

## Tool Integration Framework

**Primary Validation Tool**: `validate_macro_synthesis.py`
**Usage**: Execute the Python validation tool to comprehensively validate macro-economic analysis documents
**Command**: `python scripts/validate_macro_synthesis.py {REGION}_{YYYYMMDD}.md`

**Production CLI Financial Services Integration:**

1. **FRED Economic CLI** - GDP, employment, inflation indicators validation and macroeconomic context verification
2. **IMF CLI** - Global economic indicators validation and cross-regional comparison verification
3. **Alpha Vantage CLI** - Real-time market indicators and economic sentiment validation
4. **EIA Energy CLI** - Energy market data validation for economic context
5. **CoinGecko CLI** - Cryptocurrency market sentiment validation for risk appetite assessment
6. **Yahoo Finance CLI** - Market indices and yield curve validation
7. **FMP CLI** - Advanced economic metrics and currency data validation

**CLI-Enhanced Macro-Economic Validation Method:**
Use production CLI financial services for comprehensive multi-source economic validation:

**Multi-Source Economic Validation:**
- Multi-service CLI integration with economic data validation across all major indicators
- **MANDATORY Economic Data Validation**: Current economic indicators must be validated
- **BLOCKING Economic Consistency**: Economic data vs analysis vs recommendations validation
- Automatic cross-validation with confidence scoring and institutional-grade data quality assessment
- Business cycle positioning and economic sensitivity verification

**GDP/Employment/Policy Integration Validation:**
- Complete GDP indicators validation (GDP, GDPC1, A191RL1Q225SBEA) via FRED CLI
- Employment metrics validation (PAYEMS, CIVPART, ICSA) with economic correlation verification
- Monetary policy context integration validation with economic transmission analysis

**Economic Indicator Consistency Validation:**
- Real-time economic indicator accuracy verification against multiple sources
- Cross-regional economic comparison validation between discovery and real-time data
- Economic policy transmission mechanism validation

**CLI Validation Benefits:**
- **Robust Multi-Source CLI Access**: Direct access to all 7 data sources across multiple economic indicators
- **Economic Data Validation**: Automatic economic indicator accuracy and consistency verification
- **MANDATORY Economic Data Validation**: Current economic data validated for accuracy and consistency
- **BLOCKING Recommendation Consistency**: Economic analysis vs asset allocation recommendations validation
- **Policy/Economic Validation**: Real-time economic data validation with policy transmission analysis
- **Institutional-Grade Quality**: Advanced economic validation, caching optimization, and quality scoring (targeting >97%)
- **Error Resilience**: Comprehensive error handling with graceful degradation and economic-wide reliability scoring

## Macro-Economic DASV Phase Cross-Analysis Methodology

**Purpose**: Validate consistency, quality, and region-specificity across the latest files within a specific DASV phase to ensure systematic analysis quality and eliminate hardcoded template artifacts.

### Cross-Analysis Framework

**File Discovery and Selection**:
- Automatically locate latest 7 files (configurable) in specified phase directory
- Sort by modification timestamp for most recent analysis outputs
- Phase-specific directory mapping:
  - `discovery`: `./data/outputs/macro_analysis/discovery/`
  - `analysis`: `./data/outputs/macro_analysis/analysis/`
  - `synthesis`: `./data/outputs/macro_analysis/` (root level)
  - `validation`: `./data/outputs/macro_analysis/validation/`

### Core Validation Dimensions

#### 1. Structural Consistency Analysis
**Objective**: Ensure uniform structure and format compliance across phase outputs
```
STRUCTURAL VALIDATION PROTOCOL:
- JSON Schema Consistency: Validate all files follow identical structure
- Required Field Verification: Confirm all mandatory fields are present
- Data Type Consistency: Ensure consistent field types across files
- Metadata Format Compliance: Verify consistent metadata structure
- Confidence Score Format: Validate decimal format (0.0-1.0) consistency
- CLI Services Integration: Confirm consistent service utilization patterns
- Overall Structural Score: 9.0+/10.0 for institutional quality
```

#### 2. Hardcoded/Magic Value Detection
**Objective**: Identify and flag non-region-specific repeated values that indicate template artifacts
```
MAGIC VALUE DETECTION FRAMEWORK:
- Repeated String Patterns: Detect identical non-region strings across files
- Numerical Value Analysis: Flag suspicious repeated numbers not related to economic data
- Template Artifact Identification: Identify placeholder text or example values
- Generic Description Detection: Find non-specific regional descriptions
- Default Value Flagging: Identify unchanged template defaults
- Threshold: <5% repeated non-region-specific content for institutional quality
```

#### 3. Region Specificity Validation
**Objective**: Ensure all data and analysis content is appropriately specific to each region/economy
```
REGION SPECIFICITY ASSESSMENT:
- Regional Name Accuracy: Verify correct regional names match economic data
- Economic Classification: Confirm economic indicators are region-specific
- Economic Metrics Uniqueness: Validate economic data varies appropriately by region
- Economic Model Descriptions: Ensure region-specific economic model analysis
- Policy Analysis Specificity: Verify region-appropriate policy context
- Economic Data Correlation: Confirm economic ranges and indicators align with region
- Specificity Score: 9.5+/10.0 for institutional region-specific analysis
```

#### 4. CLI Services Integration Consistency
**Objective**: Validate consistent and appropriate use of CLI economic services across phase files
```
CLI INTEGRATION VALIDATION:
- Service Utilization Patterns: Verify consistent CLI service usage
- Data Source Attribution: Confirm proper CLI service citations
- Quality Score Consistency: Validate CLI confidence scoring alignment
- Service Health Documentation: Ensure operational status tracking
- Multi-Source Validation: Confirm cross-validation across CLI services
- Service Integration Score: 9.0+/10.0 for production-grade integration
```

### Cross-Analysis Output Structure

**File Naming**: `{PHASE}_cross_analysis_{YYYYMMDD}_validation.json`
**Location**: `./data/outputs/macro_analysis/validation/`

```json
{
  "metadata": {
    "command_name": "macro_analyst_validate_dasv_cross_analysis",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "dasv_phase_cross_analysis",
    "dasv_phase_analyzed": "discovery|analysis|synthesis|validation",
    "files_analyzed_count": 7,
    "analysis_methodology": "comprehensive_cross_phase_consistency_validation"
  },
  "files_analyzed": [
    {
      "filename": "REGION_YYYYMMDD_phase.json",
      "region": "REGION_IDENTIFIER",
      "modification_timestamp": "ISO_8601_format",
      "file_size_bytes": "numeric_file_size",
      "structural_compliance": "9.X/10.0"
    }
  ],
  "cross_analysis_results": {
    "structural_consistency_score": "9.X/10.0",
    "hardcoded_values_score": "9.X/10.0",
    "region_specificity_score": "9.X/10.0",
    "cli_integration_score": "9.X/10.0",
    "overall_cross_analysis_score": "9.X/10.0"
  },
  "detected_issues": {
    "structural_inconsistencies": [
      {
        "issue_type": "missing_field|data_type_mismatch|format_violation",
        "files_affected": ["filename_array"],
        "description": "specific_issue_description",
        "severity": "high|medium|low",
        "recommendation": "specific_fix_recommendation"
      }
    ],
    "hardcoded_values": [
      {
        "value": "detected_hardcoded_string_or_number",
        "files_affected": ["filename_array"],
        "occurrences": "count_of_occurrences",
        "suspected_template_artifact": "true|false",
        "recommendation": "region_specific_replacement_suggestion"
      }
    ],
    "region_specificity_violations": [
      {
        "field_path": "json_path_to_field",
        "generic_content": "detected_generic_content",
        "files_affected": ["filename_array"],
        "recommendation": "region_specific_content_requirement"
      }
    ],
    "cli_integration_inconsistencies": [
      {
        "service_name": "cli_service_name",
        "inconsistency_type": "missing_service|inconsistent_usage|data_quality_variation",
        "files_affected": ["filename_array"],
        "recommendation": "standardization_approach"
      }
    ]
  },
  "quality_assessment": {
    "institutional_quality_certified": "true|false",
    "minimum_threshold_met": "true|false",
    "phase_consistency_grade": "A+|A|A-|B+|B|B-|C+|C|F",
    "ready_for_production": "true|false"
  },
  "recommendations": {
    "immediate_fixes": ["array_of_critical_issues_to_address"],
    "template_improvements": ["suggestions_for_template_enhancement"],
    "validation_enhancements": ["process_improvement_recommendations"],
    "cli_integration_optimizations": ["service_utilization_improvements"]
  }
}
```

## Comprehensive Macro-Economic DASV Validation Methodology

**Before beginning validation, establish macro-economic context:**
- Extract region identifier and date from synthesis filename
- Locate ALL macro-economic DASV outputs for validation:
  - Discovery: `./data/outputs/macro_analysis/discovery/{REGION}_{YYYYMMDD}_discovery.json`
  - Analysis: `./data/outputs/macro_analysis/analysis/{REGION}_{YYYYMMDD}_analysis.json`
  - Synthesis: `./data/outputs/macro_analysis/{REGION}_{YYYYMMDD}.md`
- Document validation date and economic data freshness requirements
- Initialize systematic macro-economic validation framework targeting >9.5/10 reliability

## Validation Execution Protocol

### Tool Execution
```
MACRO-ECONOMIC VALIDATION TOOL INTEGRATION:
1. Execute Validation Tool
   → Run: python scripts/validate_macro_synthesis.py {REGION}_{YYYYMMDD}.md
   → Tool automatically discovers and validates all DASV phase outputs
   → Performs comprehensive validation against schemas and templates
   → Generates institutional-quality validation report

2. Validation Process
   → Validates discovery data completeness and accuracy
   → Verifies analysis schema compliance and confidence scores
   → Validates synthesis document against macro_analysis_template.md
   → Performs real-time economic data consistency checks

3. Quality Assurance
   → Generates validation confidence scores (targeting >9.5/10)
   → Identifies blocking issues and improvement recommendations
   → Documents institutional certification status
   → Provides comprehensive validation metadata
```

### Phase 1: Macro-Economic Discovery Data Validation

**Multi-Source Economic Discovery Output Systematic Verification**
```
CLI-ENHANCED MACRO-ECONOMIC DISCOVERY VALIDATION PROTOCOL:
1. Multi-Source Economic Data Accuracy
   → Verify current economic indicators across FRED, IMF, Alpha Vantage, EIA, CoinGecko
   → Cross-validate GDP indicators (GDP, GDPC1, A191RL1Q225SBEA) via FRED CLI
   → Integrate IMF CLI verification for cross-regional economic data and global indicators
   → Validate economic aggregates (GDP growth, inflation, employment, interest rates)
   → Cross-reference economic performance calculations with multi-source data
   → Confidence threshold: 9.5/10 (allow ≤2% variance for real-time economic data)
   → **CRITICAL: Economic indicator accuracy deviation >2% is BLOCKING for institutional usage**
   → **MANDATORY: Economic aggregates must be consistent across all synthesis references**
   → **ENHANCED: All rate data must match real-time consensus from multiple sources**
   → **ENHANCED: Key indicators validated against FRED/Bloomberg/Reuters consensus**
   → **ENHANCED: Cross-validation required when variance exceeds threshold**
   → **FAIL-FAST: Stale data (exceeding staleness_threshold) triggers automatic validation failure**

2. Business Cycle Data Validation
   → **MANDATORY Business Cycle Positioning**: Verify current cycle phase identification accuracy
   → **BLOCKING Economic Phase Consistency**: Business cycle phase must be validated across all synthesis references
   → Verify recession probability calculations via yield curve and NBER indicators
   → Validate leading/coincident/lagging indicator composites and statistical significance
   → Cross-check business cycle timing with historical precedents and current data
   → Verify economic transition probabilities and confidence intervals
   → Confidence threshold: 9.8/10 (allow ≤1% variance for cycle positioning data)
   → **BLOCKING**: Missing business cycle data prevents institutional certification

3. Employment/Monetary Policy Integration Validation
   → Validate employment metrics (PAYEMS, CIVPART, ICSA) freshness and accuracy
   → Verify monetary policy indicators (Fed Funds Rate, yield curve, credit spreads)
   → Cross-check policy transmission mechanisms with economic correlation data
   → Validate macroeconomic policy context integration in economic analysis
   → Confidence threshold: 9.0/10 (allow quarterly policy data, monthly employment data)

4. Cross-Regional Economic Analysis Validation
   → Verify all major regional economic data collection (US, EU, Asia, Emerging Markets)
   → Validate cross-regional correlation matrix accuracy and statistical significance
   → Cross-check relative economic performance calculations across regions
   → Verify global economic sensitivity analysis consistency
   → Confidence threshold: 9.5/10 (comprehensive cross-regional validation)
```

### Phase 2: Macro-Economic Analysis Quality Verification

**Analysis Output Institutional Validation**
```
MACRO-ECONOMIC ANALYSIS VALIDATION FRAMEWORK:
1. Business Cycle Modeling Validation
   → Verify economic cycle phase classification using NBER methodology and current FRED indicators
   → Validate recession probability calculations with yield curve, GDP, and employment data
   → Cross-check business cycle transition probabilities with historical pattern analysis
   → Verify monetary policy transmission mechanism assessments and effectiveness
   → Confidence threshold: 9.5/10 with supporting quantitative evidence

2. Economic Policy Assessment Validation
   → Validate monetary policy stance analysis using Fed communication and data
   → Cross-check fiscal policy space evaluation with debt sustainability metrics
   → Verify policy effectiveness confidence scoring methodology
   → Validate cross-country policy coordination and spillover analysis
   → Confidence threshold: 9.0/10 with policy framework validation

3. Economic Risk Scoring Validation
   → Verify GDP-based risk assessment calculations and recession probabilities
   → Validate employment-based risk factors with comprehensive labor market data
   → Cross-check integrated macroeconomic risk scoring methodology
   → Verify economic early warning system thresholds and monitoring framework
   → Confidence threshold: 9.5/10 with statistical significance validation

4. Economic Forecasting Framework Verification
   → Validate multi-method economic outlook methodology and scenario analysis
   → Cross-check economic scenario probabilities and forecast confidence
   → Verify cross-asset allocation implications and risk-adjusted returns
   → Validate economic calendar integration and policy timeline assessment
   → Confidence threshold: 9.0/10 with evidence-based forecasting
```

### Phase 3: Macro-Economic Synthesis Document Validation

**Publication-Ready Quality Assurance**
```
MACRO-ECONOMIC SYNTHESIS VALIDATION PROTOCOL:
1. Economic Investment Thesis Coherence
   → **MANDATORY Economic Positioning Validation**: Verify current business cycle phase positioning
   → **BLOCKING Asset Allocation Consistency**: Validate asset allocation aligns with economic analysis
   → Validate economic thesis integration with business cycle/employment/policy context
   → Cross-check economic environment consistency (growth trajectory, policy stance, risk assessment)
   → Verify risk-adjusted asset allocation calculations with economic cycle weighting
   → Validate key economic catalysts probability and impact assessments
   → Confidence threshold: 9.5/10 for institutional presentation quality

2. Economic Sensitivity Matrix Accuracy
   → Verify Fed Funds Rate correlation coefficients with FRED data validation
   → Cross-check GDP/employment growth correlations with economic data
   → Validate all economic indicator correlations and current levels
   → Verify data source attribution and confidence scoring across economic metrics
   → Confidence threshold: 9.8/10 with real-time economic data validation

3. Economic Risk Assessment Framework Validation
   → Verify GDP growth deceleration and employment deterioration risk probabilities
   → Cross-check economic stress testing scenarios with historical performance
   → Validate economic monitoring KPI selection and threshold levels
   → Verify economic risk mitigation strategies and policy response frameworks
   → Confidence threshold: 9.5/10 with quantified economic risk-return analysis

4. Cross-Regional Economic Positioning Verification
   → Validate cross-regional economic analysis table accuracy (US vs EU vs Asia vs EM)
   → Cross-check regional economic growth, policy stance, and correlation calculations
   → Verify global economic sensitivity and risk appetite analysis
   → Validate economic sensitivity comparison across regions and asset classes
   → Confidence threshold: 9.8/10 with multi-regional economic data consistency

5. Economic Outlook & Investment Recommendation Validation
   → **CRITICAL**: Validate economic outlook accuracy and policy assessment consistency
   → **BLOCKING**: Verify asset allocation recommendations align with economic positioning
   → Cross-check economic forecasting methodology and scenario probability weighting
   → Validate investment implications logic and economic thesis consistency
   → Confidence threshold: 9.8/10 with economic-investment alignment validation
```

### Phase 4: Real-Time Economic Data Consistency Validation

**Current Economic Data Verification**
```
REAL-TIME MACRO-ECONOMIC VALIDATION PROTOCOL:
1. Multi-Source Economic Indicator Validation
   → Execute real-time validation for all major economic indicators
   → Cross-validate current data across FRED, IMF, Alpha Vantage, EIA CLIs
   → Verify economic aggregate calculations with updated data
   → Validate cross-regional economic data consistency and correlations
   → Real-time threshold: ≤2% variance for all economic data

2. Business Cycle Current Data Validation
   → Verify latest business cycle indicators via FRED CLI for current economic context
   → Cross-check leading/coincident/lagging indicators freshness (monthly data within 30 days)
   → Validate business cycle context relevance with current phase positioning
   → Verify economic transition probabilities with most recent data
   → Real-time threshold: Business cycle data quarterly (≤90 days), Monthly indicators (≤30 days)

3. Economic Policy Indicator Validation
   → Execute FRED CLI validation for all referenced monetary and fiscal policy indicators
   → Cross-check yield curve, Fed communication, and policy transmission data
   → Verify global economic coordination and policy spillover indicators
   → Validate economic policy analysis with current policy environment
   → Real-time threshold: All policy indicators current within 24 hours

4. Cross-Regional Economic Real-Time Validation
   → Verify cross-regional economic data and performance with real-time sources
   → Cross-check global economic flows and capital market indicators
   → Validate regional economic allocation consistency with current conditions
   → Verify cross-regional correlation matrix accuracy and statistical significance
   → Real-time threshold: Regional economic data current within 24 hours
```

### Phase 5: Economic Outlook & Investment Recommendation Summary Validation

**Comprehensive Economic Investment Conclusion Quality Assurance**
```
ECONOMIC OUTLOOK & INVESTMENT RECOMMENDATION VALIDATION PROTOCOL:
1. Economic Investment Thesis Coherence Validation
   → Verify economic investment thesis integration with business cycle/employment/policy context
   → Cross-check economic sensitivity characteristics and policy transmission coefficients
   → Validate business cycle positioning and asset allocation probability accuracy
   → Verify cross-regional relative economic attractiveness assessment coherence
   → Confidence threshold: 9.5/10 for institutional economic investment conclusions

2. Asset Allocation Guidance Validation
   → Validate growth/balanced/conservative asset allocation recommendations across classes
   → Cross-check economic cycle timing considerations for asset class rotation
   → Verify overweight/neutral/underweight positioning rationale across asset classes
   → Validate economic risk management and rebalancing trigger specifications
   → Confidence threshold: 9.0/10 for asset allocation guidance

3. Risk-Adjusted Economic Investment Metrics Validation
   → Verify confidence-weighted expected asset class return calculations
   → Cross-check economic environment impact assessment on asset class performance
   → Validate economic risk mitigation strategies and portfolio context integration
   → Verify asset allocation guidance within economic policy framework
   → Confidence threshold: 9.5/10 for risk-adjusted economic return calculations

4. Economic Policy Investment Implications Validation
   → Validate monetary policy impact assessment on asset class investment attractiveness
   → Cross-check interest rate environment and duration positioning considerations
   → Verify business cycle correlation impact on economic investment thesis accuracy
   → Validate economic inflection points and policy transition signal accuracy
   → Confidence threshold: 9.0/10 for economic policy context integration

5. Confidence-Weighted Economic Investment Language Validation
   → Verify economic investment thesis confidence alignment with language strength
   → Cross-check economic factor confidence integration (business cycle, policy transmission)
   → Validate economic risk assessment confidence and asset allocation reliability
   → Verify asset allocation guidance confidence assessment accuracy
   → Confidence threshold: 9.5/10 for confidence-language alignment

ECONOMIC OUTLOOK VALIDATION REQUIREMENTS:
- Economic Outlook & Investment Recommendation Summary format compliance (150-250 words, single paragraph)
- Integration of all economic analytical components into actionable investment guidance
- Confidence-weighted language based on economic analysis quality (>=9.0/10)
- Economic sensitivity and business cycle positioning throughout investment conclusion
- Asset allocation context and policy timing considerations
- Economic risk management framework and monitoring specifications
```

## Output Structure

**File Naming**: `{REGION}_{YYYYMMDD}_validation.json`
**Primary Location**: `./data/outputs/macro_analysis/validation/`

```json
{
  "metadata": {
    "command_name": "sector_analyst_validate",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "validate",
    "sector": "SECTOR_SYMBOL",
    "synthesis_file_validated": "path_to_synthesis_file",
    "validation_methodology": "comprehensive_sector_validation",
    "confidence_threshold": "threshold_value",
    "real_time_validation": "boolean"
  },
  "macro_discovery_validation": {
    "multi_source_economic_accuracy": {
      "indicators_validated": "count_of_economic_indicators_validated",
      "data_consistency_score": "0.0-1.0",
      "economic_data_reliability": "aggregate_confidence_across_sources",
      "economic_aggregates_accuracy": "validation_of_gdp_employment_inflation_rates",
      "data_freshness": "real_time_current_recent_dated",
      "confidence": "0.0-1.0"
    },
    "business_cycle_integrity": {
      "cycle_phase_validation": "current_business_cycle_phase_accuracy_and_consistency",
      "recession_probability_consistency": "recession_probability_calculation_validation",
      "transition_probability_consistency": "phase_transition_vs_indicator_validation",
      "leading_indicator_accuracy": "leading_indicator_composite_verification_score",
      "nber_methodology_correlation": "nber_vs_analysis_methodology_validation",
      "historical_pattern_consistency": "current_vs_historical_cycle_validation",
      "confidence": "0.0-1.0"
    },
    "policy_employment_integration": {
      "employment_indicators_validation": "payems_civpart_icsa_accuracy",
      "monetary_policy_validation": "fed_funds_yield_curve_credit_spreads_freshness",
      "policy_correlation_accuracy": "policy_transmission_coefficient_validation",
      "macroeconomic_context": "policy_integration_quality_assessment",
      "confidence": "0.0-1.0"
    },
    "cross_regional_analysis": {
      "all_regions_data_quality": "us_eu_asia_em_validation_score",
      "correlation_matrix_accuracy": "cross_regional_statistical_significance_validation",
      "relative_performance_accuracy": "cross_regional_calculation_validation",
      "economic_sensitivity_consistency": "regional_sensitivity_validation",
      "confidence": "0.0-1.0"
    }
  },
  "macro_analysis_validation": {
    "business_cycle_modeling_validation": {
      "cycle_phase_accuracy": "nber_methodology_economic_cycle_classification_validation",
      "recession_probability_accuracy": "yield_curve_gdp_employment_based_calculation_validation",
      "transition_probability_accuracy": "historical_business_cycle_transition_validation",
      "policy_transmission_assessment": "monetary_policy_transmission_mechanism_validation",
      "confidence": "0.0-1.0"
    },
    "economic_policy_assessment_validation": {
      "monetary_policy_accuracy": "fed_policy_stance_and_effectiveness_validation",
      "fiscal_policy_space": "debt_sustainability_and_policy_space_validation",
      "policy_coordination": "cross_country_policy_spillover_validation",
      "policy_effectiveness_confidence": "policy_response_scenario_validation",
      "confidence": "0.0-1.0"
    },
    "economic_risk_scoring_validation": {
      "gdp_risk_assessment_accuracy": "gdp_based_recession_risk_calculation_validation",
      "employment_risk_accuracy": "employment_shock_scenario_validation",
      "integrated_risk_scoring": "composite_macroeconomic_risk_validation",
      "early_warning_system": "economic_threshold_and_monitoring_validation",
      "confidence": "0.0-1.0"
    },
    "economic_forecasting_validation": {
      "multi_method_accuracy": "econometric_leading_indicator_survey_validation",
      "scenario_probability_weighting": "base_bull_bear_recession_scenario_validation",
      "forecast_confidence_assessment": "uncertainty_quantification_validation",
      "cross_asset_implications": "asset_allocation_economic_environment_validation",
      "confidence": "0.0-1.0"
    }
  },
  "macro_synthesis_validation": {
    "economic_investment_thesis_coherence": {
      "thesis_business_cycle_integration": "business_cycle_employment_policy_context_consistency",
      "economic_context_accuracy": "growth_trajectory_policy_stance_risk_validation",
      "risk_adjusted_asset_allocation": "economic_cycle_weighting_validation",
      "economic_catalysts_probability_validation": "policy_transmission_catalyst_accuracy",
      "confidence": "0.0-1.0"
    },
    "economic_sensitivity_matrix": {
      "fed_funds_correlation_accuracy": "real_time_fed_funds_correlation_validation",
      "gdp_employment_correlation_accuracy": "gdp_employment_correlation_validation",
      "data_source_attribution": "fred_imf_alpha_vantage_source_validation",
      "confidence_scoring_accuracy": "economic_indicator_confidence_validation",
      "confidence": "0.0-1.0"
    },
    "economic_risk_assessment_framework": {
      "economic_risk_probability_accuracy": "macroeconomic_risk_probability_validation",
      "economic_stress_testing_scenarios": "gdp_employment_policy_shock_scenario_validation",
      "economic_monitoring_kpi_validation": "economic_risk_monitoring_framework_validation",
      "economic_mitigation_strategies": "policy_response_hedging_validation",
      "confidence": "0.0-1.0"
    },
    "cross_regional_positioning": {
      "relative_economic_analysis_accuracy": "us_eu_asia_em_comparison_validation",
      "economic_correlation_matrix_validation": "regional_economic_correlation_accuracy",
      "global_risk_appetite_accuracy": "cross_asset_risk_relationship_validation",
      "economic_sensitivity_comparison": "cross_regional_sensitivity_validation",
      "confidence": "0.0-1.0"
    },
    "economic_outlook_investment_recommendation_validation": {
      "economic_outlook_accuracy": "current_economic_positioning_validation_score",
      "asset_allocation_consistency": "cross_reference_asset_allocation_validation",
      "economic_forecast_validation": "forecasting_methodology_accuracy",
      "recommendation_alignment": "asset_allocation_vs_economic_positioning_consistency",
      "economic_positioning_logic": "economic_outlook_within_forecast_range_validation",
      "confidence": "0.0-1.0"
    }
  },
  "real_time_economic_validation": {
    "current_economic_indicator_validation": {
      "multi_source_consistency": "real_time_economic_indicator_variance_validation",
      "economic_aggregate_accuracy": "updated_economic_calculations",
      "cross_regional_consistency": "regional_economic_data_validation",
      "data_source_agreement": "fred_imf_alpha_vantage_eia_consistency",
      "confidence": "0.0-1.0"
    },
    "business_cycle_current_data": {
      "cycle_indicators_freshness": "monthly_business_cycle_data_currency_validation",
      "employment_metrics_freshness": "monthly_employment_data_currency",
      "business_cycle_context_relevance": "current_cycle_positioning_accuracy",
      "transition_probability_validity": "recent_data_transition_validation",
      "confidence": "0.0-1.0"
    },
    "economic_policy_indicators_current": {
      "fred_policy_indicators_currency": "all_fred_policy_indicators_24hour_validation",
      "yield_curve_accuracy": "current_yield_curve_data_validation",
      "global_coordination_current": "cross_country_policy_coordination_validation",
      "policy_transmission_current": "economic_policy_environment_transmission_validation",
      "confidence": "0.0-1.0"
    },
    "cross_regional_real_time": {
      "regional_economic_data_current": "real_time_regional_economic_validation",
      "regional_performance_current": "current_regional_economic_performance_validation",
      "capital_flow_analysis_current": "recent_cross_border_flow_data_validation",
      "cross_regional_correlation_current": "real_time_regional_correlation_validation",
      "confidence": "0.0-1.0"
    }
  },
  "economic_outlook_investment_recommendation_summary_validation": {
    "economic_investment_thesis_coherence_validation": {
      "thesis_business_cycle_employment_integration": "economic_investment_thesis_business_cycle_context_consistency_validation",
      "economic_sensitivity_characteristics": "policy_transmission_coefficient_and_economic_factor_validation",
      "business_cycle_positioning": "asset_allocation_probability_and_timing_accuracy_validation",
      "cross_regional_relative_attractiveness": "relative_economic_positioning_assessment_coherence_validation",
      "confidence": "0.0-1.0"
    },
    "asset_allocation_guidance_validation": {
      "growth_balanced_conservative_allocation": "asset_allocation_recommendation_accuracy_validation",
      "economic_cycle_timing": "asset_rotation_and_investment_timing_consideration_validation",
      "overweight_neutral_underweight_positioning": "asset_class_positioning_rationale_validation",
      "economic_risk_management_rebalancing_triggers": "economic_risk_management_framework_specification_validation",
      "confidence": "0.0-1.0"
    },
    "risk_adjusted_economic_investment_metrics_validation": {
      "confidence_weighted_expected_asset_returns": "expected_asset_return_calculation_and_confidence_weighting_validation",
      "economic_environment_impact": "economic_factor_impact_on_asset_class_performance_validation",
      "economic_risk_mitigation_strategies": "economic_risk_management_strategy_validation",
      "asset_allocation_guidance": "economic_portfolio_framework_integration_validation",
      "confidence": "0.0-1.0"
    },
    "economic_policy_investment_implications_validation": {
      "monetary_policy_impact": "fed_policy_asset_class_investment_attractiveness_validation",
      "interest_rate_environment": "duration_risk_and_asset_class_considerations_validation",
      "business_cycle_correlation_impact": "macroeconomic_correlation_economic_thesis_validation",
      "economic_inflection_points": "asset_allocation_signal_accuracy_validation",
      "confidence": "0.0-1.0"
    },
    "confidence_weighted_economic_investment_language_validation": {
      "economic_investment_thesis_confidence_alignment": "confidence_score_language_strength_consistency_validation",
      "economic_factor_confidence_integration": "business_cycle_policy_transmission_confidence_validation",
      "economic_risk_confidence_reliability": "risk_adjusted_economic_return_confidence_assessment_validation",
      "asset_allocation_confidence": "allocation_guidance_confidence_reliability_validation",
      "confidence": "0.0-1.0"
    },
    "economic_outlook_validation_requirements": {
      "format_compliance": "150_250_word_single_paragraph_format_validation",
      "economic_analytical_component_integration": "all_economic_analytical_components_actionable_guidance_integration_validation",
      "confidence_weighted_language": "economic_analysis_quality_based_language_confidence_validation",
      "economic_sensitivity_integration": "business_cycle_positioning_throughout_conclusion_validation",
      "asset_allocation_context": "tactical_timing_and_allocation_context_validation",
      "economic_risk_management_framework": "monitoring_specification_and_economic_risk_management_validation",
      "confidence": "0.0-1.0"
    }
  },
  "overall_validation_assessment": {
    "institutional_certification": "boolean_9.5_confidence_achieved",
    "macro_reliability_score": "0.0-1.0_overall_macro_economic_confidence",
    "business_cycle_integration_quality": "business_cycle_employment_policy_integration_assessment",
    "multi_source_validation_success": "macro_economic_wide_validation_score",
    "economic_consistency_validation": "economic_positioning_validation_score",
    "economic_outlook_validation_success": "current_economic_positioning_accuracy_and_consistency_score",
    "asset_allocation_consistency_validation": "asset_allocation_vs_economic_positioning_alignment_score",
    "real_time_economic_data_quality": "current_economic_data_validation_score",
    "usage_safety_assessment": "decision_making_reliability_for_asset_allocation",
    "blocking_issues": "array_of_critical_validation_failures_including_economic_positioning_issues",
    "recommendations": "array_of_validation_improvement_recommendations"
  },
  "validation_metadata": {
    "cli_services_health": "health_status_all_7_services",
    "validation_execution_time": "total_validation_duration",
    "data_sources_validated": "count_of_successful_cli_integrations",
    "validation_completeness": "percentage_of_validation_checks_completed",
    "confidence_distribution": "breakdown_of_confidence_scores_by_category"
  }
}
```

## Validation Execution Protocol

### Pre-Execution
1. **Load Macro-Economic DASV Outputs**
   - Load macro discovery JSON: {REGION}_{YYYYMMDD}_discovery.json
   - Load macro analysis JSON: {REGION}_{YYYYMMDD}_analysis.json
   - Load macro synthesis MD: {REGION}_{YYYYMMDD}.md
   - Validate all files exist and are accessible

2. **Initialize Macro-Economic Validation Framework**
   - Set confidence thresholds for macro-economic validation (9.0+ minimum)
   - Prepare CLI services health checks for all 7 services
   - Initialize multi-source economic data validation protocols
   - Set up real-time economic data validation requirements

3. **Extract Macro-Economic Context**
   - Identify all economic indicators from discovery data
   - Extract business cycle positioning and recession probability data
   - Load employment/policy correlation data for validation
   - Prepare cross-regional economic analysis validation framework

### Main Execution
1. **Phase 1: Multi-Source Economic Discovery Validation**
   - Validate economic indicator consistency across all data sources
   - Verify business cycle positioning and recession probability calculations
   - Validate employment/policy data integration accuracy
   - Cross-check economic aggregates and cross-regional performance

2. **Phase 2: Macro-Economic Analysis Quality Verification**
   - Verify business cycle modeling with NBER methodology and current indicators
   - Validate economic policy assessment accuracy and effectiveness
   - Cross-check macroeconomic risk scoring methodology
   - Verify economic forecasting framework evidence

3. **Phase 3: Economic Synthesis Document Validation**
   - Validate economic investment thesis business cycle/employment/policy integration
   - Verify economic sensitivity matrix accuracy
   - Cross-check economic risk assessment framework completeness
   - Validate cross-regional economic positioning accuracy

4. **Phase 4: Real-Time Economic Data Consistency**
   - Execute real-time validation across all economic indicators
   - **MANDATORY Economic Positioning Validation**: Verify current business cycle positioning accuracy and consistency
   - **BLOCKING Asset Allocation Consistency**: Validate asset allocation aligns with economic positioning
   - Verify current business cycle/employment/policy data accuracy
   - Validate economic policy indicators currency
   - Cross-check cross-regional economic real-time consistency

### Post-Execution
1. **Generate Comprehensive Economic Validation Report**
   - Create JSON output with detailed economic validation results
   - Include confidence scores for all economic validation categories
   - Document blocking issues and economic improvement recommendations
   - Provide institutional economic certification status

2. **Economic Quality Certification**
   - Verify 9.5/10 minimum confidence threshold achievement
   - Validate institutional-grade quality across all economic components
   - Document usage safety for asset allocation decisions
   - Generate economic validation metadata and performance metrics

## Usage Examples

### Single Region Validation Examples

**Basic Single Region Validation:**
```bash
/macro_analysis:validate US_20250725.md
```
- Validates complete DASV workflow for US economic analysis on July 25, 2025
- Uses default institutional validation depth
- Performs real-time economic data validation
- Output: `US_20250725_validation.json`

**Advanced Single Region Validation:**
```bash
/macro_analysis:validate EU_20250725.md --confidence_threshold=9.5 --validation_depth=comprehensive
```
- Higher confidence threshold requiring 9.5/10 minimum
- Comprehensive validation rigor
- Output: `EU_20250725_validation.json`

### Macro DASV Phase Cross-Analysis Examples

**Analysis Phase Cross-Analysis:**
```bash
/macro_analysis:validate analysis
```
- Analyzes latest 7 analysis files for consistency
- Detects hardcoded values and template artifacts
- Validates region specificity across files
- Output: `analysis_cross_analysis_20250725_validation.json`

**Discovery Phase Cross-Analysis:**
```bash
/macro_analysis:validate discovery --file_count=5
```
- Analyzes latest 5 discovery files
- Focuses on economic data collection consistency
- Output: `discovery_cross_analysis_20250725_validation.json`

**Synthesis Phase Cross-Analysis:**
```bash
/macro_analysis:validate synthesis --confidence_threshold=9.8
```
- Institutional-grade synthesis validation
- Higher confidence threshold for final documents
- Output: `synthesis_cross_analysis_20250725_validation.json`

**Validation Phase Cross-Analysis:**
```bash
/macro_analysis:validate validation
```
- Meta-validation of validation reports
- Ensures validation consistency and quality
- Output: `validation_cross_analysis_20250725_validation.json`

### Error Examples

**Invalid Parameter Format:**
```bash
/macro_analysis:validate US_2025  # Missing .md extension
# Error: Invalid filename format. Must match {REGION}_{YYYYMMDD}.md
```

**Invalid Phase Specification:**
```bash
/macro_analysis:validate testing   # Invalid phase name
# Error: Invalid phase. Must be discovery, analysis, synthesis, or validation
```

**Missing Parameters:**
```bash
/macro_analysis:validate           # No arguments
# Error: Missing required parameter. Specify filename or phase
```

## Security and Compliance

### Multi-Source Economic API Management
- **Efficient Usage**: Optimized CLI calls across multiple economic data sources
- **Rate Limiting**: Production-grade rate management for economic validation
- **Error Handling**: Graceful degradation for individual economic indicator validation failures
- **Quality Monitoring**: Real-time health assessment across economic and policy validation

**Integration with Macro-Economic DASV Framework**: This validation command serves as the final quality assurance checkpoint for the entire macro-economic analysis ecosystem, ensuring institutional-quality reliability for asset allocation strategies through comprehensive multi-source economic validation, business cycle consistency verification, and policy/employment integration validation. Validates compliance with `./templates/analysis/macro_analysis_template.md` specification (authoritative standard implemented via enhanced Jinja2 templates with macro-economic customization).

**Author**: Cole Morton
**Confidence**: [Validation confidence reflects comprehensive sector framework verification and institutional-quality standards]
**Data Quality**: [Institutional-grade validation quality through multi-company CLI verification and sector-specific context validation]
