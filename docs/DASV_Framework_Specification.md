# DASV Framework Specification
**Discovery → Analyze → Synthesize → Validate**

**Version**: 2.1
**Status**: Production
**Quality Standard**: Institutional Grade (≥9.0/10.0)
**Last Updated**: 2025-08-11

---

## Framework Overview

The DASV Framework provides systematic progression from raw data collection to validated analysis outputs with institutional-grade quality standards.

**Core Principles**:
- **Progressive Refinement**: Raw Data → Structured Data → Analytical Insights → Publication-Ready Output
- **Quality Gates**: ≥9.0/10.0 confidence at each phase with fail-fast architecture
- **Domain Extensibility**: Universal patterns enabling specialized implementations
- **Sub-Agent Delegation**: Researcher, analyst, and synthesist handle technical implementation

### Framework Phases

| Phase | Purpose | Input | Output | Quality Target |
|-------|---------|-------|--------|----------------|
| **Discovery** | Data Collection & Validation | External APIs | Structured JSON | ≥9.0/10.0 |
| **Analysis** | Statistical Analysis | Discovery JSON | Analysis JSON | ≥9.0/10.0 |
| **Synthesis** | Document Generation | Analysis JSON | Publication-ready markdown | ≥9.0/10.0 |
| **Validation** | Quality Assurance | All outputs | Validation report | ≥9.5/10.0 |

### File Organization

```
data/outputs/{analysis_type}/
├── {IDENTIFIER}_{YYYYMMDD}.md                          # Synthesis output
├── discovery/{IDENTIFIER}_{YYYYMMDD}_discovery.json    # Discovery data
├── analysis/{IDENTIFIER}_{YYYYMMDD}_analysis.json      # Analysis insights
└── validation/{IDENTIFIER}_{YYYYMMDD}_validation.json  # Validation assessment
```

---

## Quality Standards

### Universal Quality Tiers

| Quality Tier | Confidence Range | Certification | Use Case |
|--------------|------------------|---------------|----------|
| **Institutional Excellence** | 0.95-1.00 | Premium Grade | Publication ready |
| **Institutional Standard** | 0.90-0.94 | Institutional Grade | Professional analysis |
| **Professional Standard** | 0.80-0.89 | Professional Grade | Internal analysis |
| **Insufficient** | <0.80 | Rejected | Requires rework |

### Quality Thresholds

```yaml
institutional_minimum:
  overall_confidence: "≥ 0.90"
  data_completeness: "≥ 0.85"
  service_health: "≥ 0.80"
  source_reliability: "≥ 0.85"

premium_targets:
  overall_confidence: "≥ 0.95"
  data_completeness: "≥ 0.92"
  service_health: "≥ 0.90"
  source_reliability: "≥ 0.90"
```

---

## Sub-Agent Architecture

### Delegation Patterns

**Discovery Files ("WHAT")**: Define requirements without implementation
- Data requirements and quality standards
- Output specifications and parameters
- Expected outcomes and deliverables

**Sub-Agents ("HOW")**: Handle technical implementation
- **Researcher**: CLI service orchestration, data collection, quality enhancement
- **Analyst**: Statistical analysis, risk quantification, valuation modeling
- **Synthesist**: Template integration, document generation, professional presentation

### Quality Enhancement Protocol

When validation files exist (`{IDENTIFIER}_{YYYYMMDD}_validation.json`):
1. **Detection**: Search for existing validation file
2. **Integration**: Parse validation findings and gaps
3. **Enhancement**: Target 9.5+ confidence scores
4. **Generation**: Overwrite original files with improvements

---

## Implementation Guidelines

### Command Structure
Each DASV domain implements four commands:
- `{domain}_discover`: Data collection specifications
- `{domain}_analyze`: Analysis requirements
- `{domain}_synthesize`: Document generation specifications
- `{domain}_validate`: Quality assessment protocols

### Schema Requirements
- **Discovery JSON**: Structured data with metadata and confidence scores
- **Analysis JSON**: Statistical insights with risk quantification
- **Synthesis Markdown**: Publication-ready documents with template compliance
- **Validation JSON**: Quality scores and improvement recommendations

### CLI Integration
- **Service Health**: Automated health checks for data sources
- **Multi-Source Validation**: Cross-validation across APIs (Yahoo Finance, Alpha Vantage, FMP, FRED, CoinGecko)
- **Fail-Fast Implementation**: Immediate exception throwing on quality threshold violations

---

## Domain Extensions

### Supported Analysis Types
- **Fundamental Analysis**: Company financial health and investment thesis
- **Sector Analysis**: 11-sector ETF framework with economic positioning
- **Industry Analysis**: Competitive landscape with A-F grading system
- **Macro Analysis**: Business cycle assessment with cross-regional positioning
- **Comparative Analysis**: Dual-stock winner/loser determination
- **Trade History**: Performance tracking with strategy optimization

### Template System
Each domain uses standardized templates located in `./templates/analysis/`:
- Template compliance enforced by synthesist sub-agent
- Professional formatting with evidence integration
- Generic placeholder elimination required

---

## Quality Assurance

### Confidence Calculation Components
- **Data Quality**: Completeness, accuracy, freshness (weight: 30%)
- **Methodology Rigor**: Analytical framework application (weight: 25%)
- **Template Compliance**: Professional presentation standards (weight: 25%)
- **Evidence Strength**: Traceability and validation (weight: 20%)

### Validation Enhancement
- **Automatic Detection**: Existing validation files trigger enhancement mode
- **Systematic Improvement**: Target 9.5+ confidence scores
- **Quality-Driven Output**: Enhanced files with artifacts removal

### Fail-Fast Architecture
- Quality thresholds enforced at phase transitions
- Immediate exception throwing prevents degraded output progression
- Meaningful error messages for proper issue resolution

---

**Framework Authority**: Comprehensive Analysis Architecture
**Implementation Confidence**: 9.6/10.0
**Data Quality**: Institutional-grade with multi-source validation
**Status**: Production-ready with universal sub-agent delegation
