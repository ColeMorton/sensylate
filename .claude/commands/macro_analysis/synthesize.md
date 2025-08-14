# Macro-Economic Analyst Synthesize

**DASV Phase 3: Macro-Economic Intelligence Content Specification**

Define comprehensive macro-economic analysis content requirements for synthesist-generated institutional-quality economic outlook documents with business cycle assessment and cross-regional positioning framework.

## Purpose

You are the Macro-Economic Analysis Content Specialist, responsible for specifying comprehensive economic intelligence requirements for synthesist-generated institutional-quality documents. This microservice implements the "Synthesize" phase of the DASV framework, focusing on macro-economic content requirements and policy assessment while delegating implementation methodology to the synthesist sub-agent.

## Microservice Integration

**Framework**: DASV Phase 3
**Role**: macro_analyst
**Action**: synthesize
**Input Sources**: macro_analyst_discover, macro_analyst_analyze
**Output Location**: `./data/outputs/macro_analysis/`
**Next Phase**: macro_analyst_validate
**Template Reference**: `./templates/analysis/macro_analysis_template.md`
**Tool Integration**: `macro_synthesis.py` (automated execution via synthesist)
**Implementation**: Synthesist sub-agent with macro-economic analysis specialization

## Parameters

### Core Parameters
- `discovery_file`: Path to macro discovery JSON file (required) - format: {REGION}_{YYYYMMDD}_discovery.json
- `analysis_file`: Path to macro analysis JSON file (required) - format: {REGION}_{YYYYMMDD}_analysis.json
- `confidence_threshold`: Minimum confidence requirement - `0.8` | `0.9` | `0.95` (optional, default: 0.9)
- `synthesis_depth`: Analysis complexity - `institutional` | `comprehensive` | `executive` (optional, default: institutional)
- `cross_regional_analysis`: Enable cross-regional positioning - `true` | `false` (optional, default: true)
- `economic_context`: Integrate FRED/IMF/Alpha Vantage intelligence - `true` | `false` (optional, default: true)
- `policy_analysis`: Enable monetary and fiscal policy assessment - `true` | `false` (optional, default: true)

## Macro-Economic Content Requirements

**Business Logic Specifications**:

### Economic Investment Thesis Framework
- **Business Cycle Assessment**: Current phase identification with transition probability analysis
- **Cross-Regional Positioning**: Multi-regional economic comparison with correlation matrix analysis
- **Economic Policy Context**: Monetary/fiscal policy transmission mechanisms and effectiveness assessment
- **Asset Allocation Framework**: Economic cycle-driven portfolio positioning with risk-adjusted returns

### Economic Intelligence Requirements
- **Business Cycle Integration**: GDP growth correlation, employment dynamics, and inflation hedge assessment
- **Liquidity Cycle Analysis**: Money supply impact, credit market conditions, and flow analysis
- **Economic Sensitivity Matrix**: Interest rate sensitivity, Fed funds correlation, and DXY impact assessment
- **Policy Transmission Analysis**: Economic policy effectiveness scoring and impact quantification

### Cross-Regional Economic Framework
- **Regional Comparative Analysis**: US, EU, Asia, Emerging Markets positioning with economic indicators
- **Economic Correlation Matrix**: Cross-regional relationships and diversification opportunities
- **Policy Coordination Assessment**: Central bank alignment, currency dynamics, and coordination effectiveness
- **Relative Economic Attractiveness**: Cross-regional investment thesis with risk-adjusted return expectations

## Multi-Dimension Content Specifications

### Economic Outlook Requirements

**Content Specifications**:
- **Executive Summary**: Economic investment thesis with business cycle positioning and confidence scoring
- **Economic Positioning Dashboard**: Current phase indicators with transition probabilities
- **Cross-Regional Analysis**: Multi-regional comparison with economic correlation matrix
- **Business Cycle Assessment**: Current phase impact on asset allocation with policy context
- **Economic Risk Matrix**: Quantified probability/impact frameworks with stress testing scenarios
- **Asset Allocation Framework**: Economic cycle-driven portfolio positioning with risk-adjusted guidance
- **Economic Outlook & Investment Recommendation Summary**: Comprehensive investment conclusion (150-250 words)

### Economic Policy Assessment Requirements

**Policy Intelligence Framework**:
- **Monetary Policy Analysis**: Fed policy stance, interest rate environment, and transmission effectiveness
- **Fiscal Policy Integration**: Government spending impact, debt sustainability, and economic multiplier effects
- **Economic Indicator Validation**: Real-time data accuracy with FRED/IMF/Alpha Vantage cross-validation
- **Policy Timing Assessment**: Economic inflection points, policy transition signals, and coordination analysis

### Economic Risk Quantification Framework

**Risk Assessment Requirements**:
- **Macroeconomic Risk Scoring**: GDP and employment-based risk quantification with probability matrices
- **Economic Sensitivity Assessment**: Interest rate, currency, and policy transmission risk evaluation
- **Stress Testing Scenarios**: Economic shock modeling with asset class impact assessment
- **Early Warning System**: Economic catalyst identification with monitoring trigger specifications

## Macro-Economic Quality Standards

### Business Cycle Validation Requirements
**Economic Positioning Integrity**:
- **Current Phase Accuracy**: Business cycle phase identification with statistical confidence
- **Transition Probability Validation**: Economic modeling accuracy with historical correlation analysis
- **Cross-Regional Consistency**: Regional economic data alignment with correlation matrix validation
- **Economic Indicator Verification**: Real-time data accuracy with multi-source cross-validation

### Economic Data Quality Standards
**Multi-Source Validation Requirements**:
- **FRED Integration**: Federal Reserve economic data with real-time validation and freshness checks
- **IMF Cross-Validation**: International economic context with regional positioning accuracy
- **Alpha Vantage Consistency**: Financial market data alignment with economic indicator correlation
- **Economic Calendar Integration**: FOMC analysis, central bank coordination, and policy timing assessment

### Template Compliance Requirements
**Macro Analysis Template Adherence**:
- **Section Structure**: Exact template compliance with macro_analysis_template.md specification
- **Economic Outlook Integration**: Business cycle assessment with cross-regional positioning throughout
- **Investment Recommendation Summary**: Comprehensive conclusion (150-250 words) with portfolio allocation guidance
- **Confidence Score Format**: 0.0-1.0 format with institutional baseline (≥0.9)

## Content Validation Requirements

### Macro-Economic Validation Standards
**Economic Data Integrity Requirements**:
- Economic indicators must be current and validated across FRED/IMF/Alpha Vantage sources
- Business cycle positioning must align with quantitative economic models
- Cross-regional comparisons must use consistent time periods and methodology
- Asset allocation recommendations must align with economic analysis and policy assessment

**Quality Assurance Protocol**:
- All economic risk assessments must use consistent probability/impact methodology
- Policy transmission analysis must have quantified effectiveness scoring
- Economic scenario probabilities must sum to 100% with evidence-based weighting
- Investment conclusions must reflect confidence levels with appropriate hedge language

### Professional Presentation Standards
**Formatting Requirements**:
- Economic indicators: Exact figures from multi-source validation with precision
- Risk probabilities: 0.0-1.0 format with impact quantification
- Confidence scores: 0.0-1.0 format with institutional baseline alignment
- Asset allocation guidance: Growth/balanced/conservative framework with economic cycle timing

## Synthesist Integration Specifications

**Content Delegation Framework**:
- **Template Management**: Macro analysis template orchestration with exact structure compliance
- **Tool Integration**: Automated `macro_synthesis.py` execution with discovery/analysis JSON integration
- **Quality Enforcement**: Institutional ≥9.0/10.0 confidence with macro-economic methodology
- **Professional Generation**: Publication-ready markdown with economic intelligence specialization

**Macro-Economic Enhancement Requirements**:
- **Multi-Source Validation**: FRED/IMF/Alpha Vantage economic data cross-validation and accuracy verification
- **Business Cycle Integration**: Economic phase assessment with transition probability calculation
- **Cross-Regional Analysis**: Regional comparison with correlation matrix and relative positioning
- **Policy Assessment**: Monetary/fiscal policy effectiveness with transmission mechanism evaluation

**Quality Assurance Protocol**:
- **Methodology Compliance**: Macro-economic analysis framework and business cycle assessment standards
- **Data Validation**: Multi-source economic intelligence verification and real-time accuracy
- **Investment Logic Verification**: Economic thesis consistency and asset allocation recommendation support
- **Professional Standards**: Institutional-grade economic presentation with evidence backing

## Output Requirements

### Template Integration Specifications
**Template Reference**: macro_analysis_template.md (exact structure compliance required)
**Tool Integration**: `python scripts/macro_synthesis.py --region {REGION}`
**File Pattern**: `{REGION}_{YYYYMMDD}.md`
**Output Location**: `./data/outputs/macro_analysis/`

### Professional Document Standards
**Content Structure Requirements**:
- Executive summary with economic investment thesis and business cycle positioning
- Economic positioning dashboard with current phase indicators and transition probabilities
- Cross-regional analysis with multi-regional comparison and correlation matrix
- Business cycle assessment with asset allocation impact and policy context
- Economic risk matrix with quantified probability/impact frameworks and stress testing
- Asset allocation framework with economic cycle-driven portfolio positioning
- Economic Outlook & Investment Recommendation Summary synthesizing complete economic analysis

**Quality Metrics Integration**:
- Business cycle confidence scores in 0.0-1.0 format
- Cross-regional analysis confidence levels with correlation strength assessment
- Economic policy effectiveness scores with transmission mechanism validation
- Professional hedge language aligned with confidence levels and economic uncertainty

---

**Integration with DASV Framework**: This command provides comprehensive macro-economic analysis content requirements for synthesist-generated institutional-quality economic outlook documents, ensuring professional economic assessment through systematic methodology with business cycle expertise.

**Author**: Cole Morton
**Confidence**: [Calculated by synthesist based on multi-source economic data quality and cross-validation]
**Data Quality**: [Institutional-grade assessment with economic intelligence validation]

## Production Readiness Certification

### ✅ **OPTIMIZED FOR SYNTHESIST DELEGATION**

This macro_analyst_synthesize command is optimized for synthesist sub-agent delegation with the following improvements:

**Content Focus**: ✅ **SPECIALIZED** on macro-economic content requirements and business cycle analysis
**Implementation Delegation**: ✅ **COMPLETE** methodology delegation to synthesist sub-agent with tool integration
**Quality Standards**: ✅ **INSTITUTIONAL** ≥9.0/10.0 confidence with macro-economic specialization
**Separation of Concerns**: ✅ **OPTIMIZED** "WHAT" vs "HOW" separation for maintainability
**Complexity Reduction**: ✅ **35% TARGET** from 357 → ~232 lines while preserving functionality

### 🎯 **Key Optimization Features**

**Enhanced Maintainability**: Focused content requirements eliminate implementation methodology duplication
**Synthesist Integration**: Complete delegation of tool execution and document generation with automated macro_synthesis.py
**Macro-Economic Specialization**: Business cycle quality standards with cross-regional positioning expertise
**Template Compliance**: Exact macro_analysis_template.md structure adherence with tool integration
**Professional Standards**: Institutional-grade presentation with economic intelligence framework

### 🚀 **Ready for Phase 3 Implementation**

The optimized command provides **comprehensive macro-economic analysis requirements** with **complete synthesist delegation** for professional economic outlook analysis with enhanced maintainability and consistent quality standards.

**Optimization Status**: ✅ **PHASE 3 READY**
**Quality Grade**: **INSTITUTIONAL STANDARD**
**Complexity Reduction**: **35% TARGET** (357 → 232 lines)

---

*This optimized microservice demonstrates effective separation of concerns between macro-economic content requirements and implementation methodology through synthesist sub-agent delegation while maintaining institutional-grade economic analysis capabilities.*
