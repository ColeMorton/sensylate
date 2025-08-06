# Macro-Economic Analyst Synthesize

**DASV Phase 3: Macro-Economic Analysis Document Generation**

Generate institutional-quality macro-economic analysis documents with comprehensive Economic Outlook and Policy Assessment following the macro analysis template specification, leveraging discovery and analysis data with comprehensive economic intelligence, cross-regional positioning, and sophisticated policy context integration.

## Purpose

You are the Macro-Economic Analysis Synthesis Specialist, responsible for transforming validated discovery and analysis intelligence into comprehensive economic outlook and policy recommendations with institutional-quality presentation and Economic Policy Assessment. This microservice implements the "Synthesize" phase of the DASV framework, leveraging multi-source economic data, cross-regional analysis, and quantified policy transmission mechanisms to generate publication-ready macro-economic analysis with actionable economic conclusions following the macro analysis template specification.

## Microservice Integration

**Framework**: DASV Phase 3
**Role**: macro_analyst
**Action**: synthesize
**Input Sources**: macro_analyst_discover, macro_analyst_analyze
**Output Location**: `./data/outputs/macro_analysis/`
**Next Phase**: macro_analyst_validate
**Integration**: Production-grade multi-source economic data synthesis with cross-regional intelligence

## Output Requirements

**Professional Standard**: Generate institutional-quality macro-economic analysis documents following `./templates/analysis/macro_analysis_template.md` specification exactly, suitable for sophisticated economic policy assessment and asset allocation decision-making, combining rigorous multi-indicator analytical methodology with clear, actionable economic outlook.

## Parameters

### Core Parameters
- `discovery_file`: Path to macro discovery JSON file (required) - format: {REGION}_{YYYYMMDD}_discovery.json
- `analysis_file`: Path to macro analysis JSON file (required) - format: {REGION}_{YYYYMMDD}_analysis.json
- `confidence_threshold`: Minimum confidence requirement - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Analysis Parameters
- `synthesis_depth`: Analysis synthesis complexity - `institutional` | `comprehensive` | `executive` (optional, default: institutional)
- `cross_regional_analysis`: Enable cross-regional economic positioning - `true` | `false` (optional, default: true)
- `economic_context`: Integrate FRED/IMF/Alpha Vantage economic intelligence - `true` | `false` (optional, default: true)
- `risk_quantification`: Risk assessment methodology - `advanced` | `institutional` | `comprehensive` (optional, default: institutional)
- `policy_analysis`: Enable monetary and fiscal policy assessment - `true` | `false` (optional, default: true)

## Phase 0: Macro-Economic Data Integration Protocol

**0.1 Discovery and Analysis Data Loading**
```
MACRO-ECONOMIC DATA INTEGRATION WORKFLOW:
1. Load Discovery Data
   → Extract region and date from discovery_file parameter
   → Load discovery JSON: {REGION}_{YYYYMMDD}_discovery.json
   → Extract multi-source economic data from FRED, IMF, Alpha Vantage, EIA, CoinGecko
   → Validate economic indicators and cross-regional comparative intelligence

2. Load Analysis Data
   → Load analysis JSON: {REGION}_{YYYYMMDD}_analysis.json
   → Extract business cycle modeling, liquidity cycle positioning
   → Load quantified risk assessment and macroeconomic risk scoring
   → Import enhanced economic sensitivity and investment recommendation gap analysis

3. Cross-Regional Data Integration
   → Extract cross-regional economic comparisons (US, EU, Asia, Emerging Markets)
   → Load economic sensitivity matrix and monetary policy correlations
   → Import global economic context and policy coordination analysis
   → Validate cross-regional analysis completeness and data quality

4. Economic Policy Context Integration
   → Extract FRED monetary policy indicators and Fed communication
   → Load interest rate environment, yield curve, and credit market analysis
   → Integrate international economic coordination and currency dynamics
   → Map economic context to business cycle positioning and policy transmission

5. Validation Enhancement Check
   → Search for existing validation file: {REGION}_{YYYYMMDD}_validation.json
   → If found: Apply validation-driven enhancements targeting 9.5+ synthesis scores
   → If not found: Proceed with institutional-quality baseline using data
```

**0.2 Macro-Economic Confidence Score Inheritance and Quality Assessment**
```
MACRO-ECONOMIC CONFIDENCE PROPAGATION PROCESS:
Step 1: Multi-Source Economic Data Quality Assessment
   → Extract overall discovery confidence across all economic data sources
   → Validate multi-source data quality impact scores (typically 0.95+ for institutional-grade)
   → Assess economic indicator aggregation methodology and cross-source validation effectiveness
   → Evaluate economic context integration quality and regional economic consistency

Step 2: Analysis Quality Integration
   → Extract business cycle and liquidity cycle positioning confidence
   → Load macroeconomic risk scoring and early warning system confidence
   → Integrate investment recommendation gap analysis and economic sensitivity confidence
   → Map regional economic analytical quality to synthesis confidence targeting

Step 3: Cross-Regional Analysis Quality
   → Load cross-regional economic data completeness and consistency scores
   → Extract economic correlation matrix reliability and statistical significance
   → Validate policy transmission analysis confidence and economic sensitivity strength
   → Assess regional positioning accuracy and relative economic performance reliability

Step 4: Synthesis Quality Targeting
   → Target institutional-grade synthesis confidence: 0.9+ baseline
   → Apply validation enhancement for 0.95+ synthesis scores
   → Ensure cross-regional analysis integration throughout economic investment thesis
   → Maintain publication-ready quality standards with multi-source evidence backing
```

## Macro-Economic Analysis Synthesis Framework

### Economic Investment Thesis Construction

**Economic Decision Framework**
```
MACRO-ECONOMIC DECISION FRAMEWORK:
1. Economic Risk-Adjusted Asset Allocation
   → Expected asset class returns = Σ(scenario probability × Asset Return)
   → Risk-adjusted returns with economic cycle context adjustments
   → Asset class downside risk assessment using quantified economic risk matrices
   → Economic environment impact on asset allocation vs historical averages

2. Business Cycle Integration
   → Current business cycle phase impact on asset class performance
   → Business cycle positioning impact on asset allocation timing
   → Liquidity cycle positioning impact on risk asset flow considerations
   → Cross-regional economic positioning impact on geographic allocation decisions

3. Asset Allocation Framework
   → Asset allocation within portfolio context (equities, fixed income, alternatives)
   → Economic context impact on asset weighting recommendations
   → Asset correlation considerations for portfolio diversification
   → Interest rate environment impact on duration and credit positioning

4. Institutional-Grade Economic Conviction Scoring
   → Multi-source economic data quality score: [0.9-1.0] (inherited from discovery)
   → Cross-regional validation confidence: [0.9-1.0]
   → Economic context integration: [0.9-1.0]
   → Analysis methodology rigor: [0.8-1.0]
   → Evidence strength: [0.8-1.0]
   → OVERALL ECONOMIC CONVICTION: [weighted average 0.9+]

5. Economic Context Asset Allocation Impact
   → Interest rate environment impact on asset class thesis
   → Monetary policy implications for risk asset performance
   → Yield curve considerations for duration positioning
   → Economic phase transition probability and timing assessment

6. Economic Policy vs Asset Allocation Framework
   → Current economic indicators validation and accuracy verification
   → Economic positioning within business cycle range assessment
   → Asset allocation recommendation validation logic
   → Policy gap analysis impact on economic investment thesis
   → Economic consistency validation across all synthesis references
```

## Tool Integration Framework

**Primary Tool**: `macro_synthesis.py`
**Usage**: Execute the Python tool to generate institutional-quality macro-economic analysis documents
**Command**: `python scripts/macro_synthesis.py --region {REGION} --discovery-file {discovery_file} --analysis-file {analysis_file}`

### Tool Execution Protocol
```
MACRO-ECONOMIC SYNTHESIS TOOL INTEGRATION:
1. Execute Macro Synthesis Tool
   → Run: python scripts/macro_synthesis.py --region {REGION}
   → Tool automatically discovers and loads latest discovery and analysis files
   → Generates institutional-quality markdown document following macro_analysis_template.md
   → Produces comprehensive economic outlook with policy assessment

2. Enhanced Service Integration
   → Tool integrates economic calendar service for FOMC analysis
   → Global liquidity monitor provides central bank coordination analysis
   → Sector correlation service adds cross-asset economic transmission analysis
   → Real-time economic data validation and consistency checking

3. Document Generation Standards
   → Follows ./templates/analysis/macro_analysis_template.md specification exactly
   → Generates {REGION}_{YYYYMMDD}.md output file
   → Includes comprehensive Economic Outlook & Investment Recommendation Summary
   → Maintains institutional-quality confidence scores (0.9+ baseline)

4. Quality Assurance
   → Multi-source economic data validation and cross-checking
   → Schema compliance verification for all required sections
   → Real-time economic indicator validation and freshness checking
   → Confidence score propagation and quality metric calculation
```

### Economic Analysis Integration Framework

**Multi-Method Economic Analysis Approach**
```
MACRO-ECONOMIC ANALYSIS FRAMEWORK:
1. Business Cycle Analysis Integration
   → Business cycle modeling data integration from analysis phase
   → Current phase identification and transition probability assessment
   → Interest rate sensitivity analysis and inflation hedge assessment
   → GDP growth correlation and economic sensitivity matrix integration

2. Economic Policy Assessment
   → Monetary policy transmission analysis and Fed policy stance evaluation
   → Credit market conditions and money supply impact assessment
   → Employment dynamics analysis and labor market health indicators
   → Cross-regional economic comparison and relative positioning

3. Economic Risk Integration
   → Quantified risk assessment matrix with probability/impact scoring
   → Macroeconomic risk scoring including GDP and employment-based risks
   → Enhanced economic sensitivity including Fed funds correlation and DXY impact
   → Stress testing scenarios and early warning system integration

4. Investment Recommendation Gap Analysis
   → Portfolio allocation context and economic cycle investment positioning
   → Risk-adjusted investment metrics and economic factor weighting
   → Sector investment characteristics and economic sensitivity profiles
   → Economic policy recommendation framework and fair value positioning

MACRO-ECONOMIC SYNTHESIS APPROACH:
- Integrate all analysis components using macro_synthesis.py tool
- Generate comprehensive economic outlook with policy assessment
- Calculate confidence-weighted economic conclusions (targeting 0.9+)
- Identify key economic catalysts and policy transmission mechanisms
- Produce institutional-quality investment recommendation summary
```

### Economic Outlook & Investment Recommendation Synthesis Framework

**Comprehensive Economic Investment Conclusion Generation**
```
ECONOMIC INVESTMENT RECOMMENDATION SYNTHESIS:
1. Economic Investment Thesis Integration
   → Synthesize business cycle positioning with GDP/employment context
   → Integrate economic sensitivity characteristics and policy transmission coefficients
   → Economic cycle positioning and asset allocation probability synthesis
   → Cross-regional relative economic attractiveness assessment

2. Risk-Adjusted Economic Return Synthesis
   → Confidence-weighted expected asset class return calculations
   → Economic environment impact on asset class performance
   → Risk mitigation strategies and economic policy context
   → Asset allocation guidance within economic cycle framework

3. Portfolio Allocation Framework Integration
   → Growth/balanced/conservative portfolio allocation guidance
   → Economic cycle timing considerations for asset rotation
   → Overweight/neutral/underweight positioning recommendations across asset classes
   → Risk management and rebalancing trigger specifications

4. Economic Context Investment Implications
   → Monetary policy impact on asset class investment attractiveness
   → Interest rate environment and duration positioning considerations
   → GDP/employment correlation impact on economic investment thesis
   → Economic inflection points and policy transition signals

5. Confidence-Weighted Economic Investment Conclusions
   → Investment thesis confidence alignment with economic analysis quality
   → Economic factor confidence integration (business cycle, policy transmission)
   → Economic risk assessment confidence and asset allocation reliability
   → Portfolio allocation guidance confidence assessment

ECONOMIC INVESTMENT RECOMMENDATION SYNTHESIS REQUIREMENTS:
- Single comprehensive paragraph format (150-250 words) in template
- Integration of all economic analytical components into actionable guidance
- Confidence-weighted language based on economic analysis quality
- Economic sensitivity and business cycle positioning throughout
- Portfolio allocation context and policy timing considerations
- Economic risk management framework and monitoring specifications
```

### Document Generation Standards

**MANDATORY MACRO-ECONOMIC CONSISTENCY VALIDATION:**
```
□ ALL confidence scores use 0.0-1.0 format (baseline 0.9+)
□ Header format: "Confidence: [X.X/1.0] | Data Quality: [X.X/1.0] | Economic Context: Current"
□ Author attribution: "Cole Morton" (consistent across all documents)
□ Risk probabilities in decimal format (0.0-1.0) from economic risk matrices
□ **CRITICAL: ECONOMIC INDICATOR ACCURACY** - use validated current economic data throughout document
□ **CRITICAL: ECONOMIC DATA VALIDATION GATE** - verify economic indicators are current before synthesis generation
□ **CRITICAL: RECOMMENDATION CONSISTENCY** - validate asset allocation aligns with economic analysis
□ **CRITICAL: Cross-regional consistency validation** - all regional economic comparisons accurate
□ **CRITICAL: Multi-source data consistency** - use exact economic aggregates from discovery
□ **Business cycle integration** - prominently display current phase with transition probabilities
□ **Economic context integration** - FRED/IMF/Alpha Vantage insights throughout economic analysis
□ **Cross-regional positioning terminology** - distinguish regional allocation vs domestic focus
□ **Economic indicator tracking** - document economic data freshness and source reliability
□ **Quantified economic risk integration** - use probability/impact matrices from analysis
□ **Economic catalyst quantification** - specific probability and economic impact figures
□ **Economic policy assessment ratings** - numerical effectiveness scores and transmission mechanisms
□ Economic analysis confidence reflects data quality (0.9+ baseline)
□ All monetary values include $ symbol with precision for economic metrics
□ Economic scenario probabilities sum to 100% with FRED-informed economic weighting
□ Multi-source economic data utilization and health status in metadata
□ Cross-regional validation confidence scores in metadata section
□ Economic intelligence integration throughout synthesis
□ Interest rate environment economic impact explicitly addressed
□ Economic policy environment assessment with transmission credibility scores
□ **Economic Outlook & Investment Recommendation Summary** - comprehensive investment conclusion with portfolio allocation guidance
□ **Portfolio allocation framework** - growth/balanced/conservative guidance with business cycle timing
□ **Confidence-weighted economic language** - alignment between confidence scores and conclusion strength
□ **Economic Policy vs Asset Allocation Consistency** - ensure recommendations align with economic positioning
```

## Macro-Economic Output Structure Reference

**TEMPLATE SYSTEM**:
- **Authoritative Specification**: `./templates/analysis/macro_analysis_template.md`
- **Tool Implementation**: `./scripts/macro_synthesis.py`
- **Command Reference**: This command instructs AI agents to use the macro synthesis tool
- **Tool Execution**: Uses enhanced template rendering with macro-economic data integration

**File Naming**: `{REGION}_{YYYYMMDD}.md` (e.g., `US_20250805.md`)
**Directory**: `./data/outputs/macro_analysis/`
**Data Sources**: discovery and analysis with multi-source economic validation

**Template Features**:
- **Institutional-Quality Structure**: Executive summary, economic positioning dashboard, business cycle assessment
- **Cross-Regional Analysis**: Complete regional economic comparison with correlation matrix
- **Economic Sensitivity**: GDP/employment integration with FRED indicator correlations
- **Risk Assessment**: Quantified probability/impact matrices with economic stress testing scenarios
- **Economic Outlook & Investment Recommendation Summary**: Comprehensive investment conclusion with portfolio allocation guidance
- **Quality Standards**: 0.9+ confidence baseline, comprehensive economic validation, real-time context

## Synthesis Execution Protocol

### Pre-Execution: Macro-Economic Data Integration
1. **Discovery Data Loading**
   - Load macro-economic discovery JSON file from parameter
   - Extract region and date for synthesis file naming
   - **MANDATORY Economic Data Validation**: Verify current economic indicators are present and accurate
   - Validate multi-source economic data quality and completeness
   - Confirm discovery confidence scores (target: 0.9+ inherited)

### Main Execution: Execute Macro Synthesis Tool
1. **Run Macro Synthesis Tool**
   - Execute: `python scripts/macro_synthesis.py --region {REGION}`
   - Tool automatically discovers and integrates discovery and analysis files
   - Generates institutional-quality macro-economic analysis document
   - Follows ./templates/analysis/macro_analysis_template.md specification exactly

2. **Document Generation Process**
   - Creates comprehensive economic thesis with business cycle assessment
   - Integrates cross-regional economic positioning and policy analysis
   - Generates quantified risk assessment with economic stress testing
   - Produces Economic Outlook & Investment Recommendation Summary
   - Maintains institutional confidence standards (0.9+ baseline)

### Post-Execution: Quality Assurance
1. **Output Validation**
   - Verify document saved to ./data/outputs/macro_analysis/
   - Confirm proper naming: {REGION}_{YYYYMMDD}.md
   - Validate template compliance and schema consistency
   - Ensure Economic Outlook & Investment Recommendation Summary included

2. **Signal Readiness for Validation Phase**
   - Output ready for macro_analyst_validate phase
   - Provide synthesis confidence scores for validation input
   - Document macro-economic integration effectiveness
   - Log synthesis performance metrics

**Integration with DASV Framework**: This command instructs AI agents to properly utilize the macro_synthesis.py tool for generating institutional-quality macro-economic analysis documents following the authoritative template specification exactly, ensuring comprehensive economic intelligence and actionable investment conclusions through systematic DASV methodology.

**Author**: Cole Morton
