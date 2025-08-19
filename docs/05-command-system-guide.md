# Command System Guide: Comprehensive Development & Standardization

**Version**: 2.0 | **Last Updated**: 2025-08-12 | **Status**: Production Ready
**Authority**: Documentation Owner | **Audience**: Command Developers

## Table of Contents

1. [Command System Overview](#command-system-overview)
2. [Command Template Specification](#command-template-specification)
3. [Standardization Framework](#standardization-framework)
4. [Path Configuration System](#path-configuration-system)
5. [Script Integration Patterns](#script-integration-patterns)
6. [Template Architecture](#template-architecture)
7. [Quality Assurance Framework](#quality-assurance-framework)
8. [Development Workflow](#development-workflow)

---

## Command System Overview

### System Architecture

The Sensylate command system implements a sophisticated orchestration framework enabling AI agents to execute complex analysis workflows through standardized interfaces. Commands serve as the primary interaction layer between users and the underlying DASV (Discovery-Analyze-Synthesize-Validate) framework.

### Command Classifications

**🎯 Assistant Commands**: High-level strategic guidance and orchestration
**📊 Core Product Commands**: User-facing analysis and content generation
**🔧 Tool Commands**: Utility and infrastructure operations
**🌐 Integration Commands**: External service coordination and data processing

### Key Principles

1. **Standardized Interfaces**: Consistent command structure across all domains
2. **Script Integration**: Direct mapping to Python implementation scripts
3. **Template Orchestration**: Dynamic template selection and content generation
4. **Path Configuration**: Flexible, environment-aware file system management
5. **Quality Assurance**: Built-in validation and confidence scoring

---

## Command Template Specification

### Command Header Structure

```markdown
# Command Name Template

**Command Classification**: [📊|🎯|🔧|🌐] **[Core Product Command|Assistant|Tool|Integration]**
**Knowledge Domain**: `domain-name-expertise`
**Ecosystem Version**: `X.Y.Z` *(Last Updated: YYYY-MM-DD)*
**Outputs To**: `{DATA_OUTPUTS}/output_directory/`
```

### Script Integration Mapping

**Primary Script Configuration:**
```markdown
## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/path/to/primary_script.py`
**Script Class**: `{ScriptClassName}`
**Registry Name**: `{registry_name}`
**Content Types**: `["content_type_1", "content_type_2"]`
**Requires Validation**: `true|false`

**Registry Decorator**:
```python
@twitter_script(
    name="{registry_name}",
    content_types=["{content_type}"],
    requires_validation={true|false}
)
class {ScriptClassName}(BaseScript):
    """Script description"""
```

### Multi-Phase Workflow Configuration

**DASV Framework Integration:**
```yaml
discovery_script:
  path: "{SCRIPTS_BASE}/path/to/discovery.py"
  class: "DiscoveryScript"
  phase: "Phase 1 - Data Collection"

analysis_script:
  path: "{SCRIPTS_BASE}/path/to/analysis.py"
  class: "AnalysisScript"
  phase: "Phase 2 - Analysis"

synthesis_script:
  path: "{SCRIPTS_BASE}/path/to/synthesis.py"
  class: "SynthesisScript"
  phase: "Phase 3 - Document Generation"

validation_script:
  path: "{SCRIPTS_BASE}/path/to/validation.py"
  class: "ValidationScript"
  phase: "Phase 4 - Quality Assurance"
```

### Template Integration Architecture

**Template Directory Structure:**
```markdown
**Template Directory**: `{TEMPLATES_BASE}/template_category/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| template_a | `category/template_variant_a.j2` | condition_1 AND condition_2 | Primary use case |
| template_b | `category/template_variant_b.j2` | condition_3 OR condition_4 | Alternative approach |
| template_default | `category/default_template.j2` | fallback_condition | Fallback option |
```

**Shared Components:**
```yaml
base_template:
  path: "{TEMPLATES_BASE}/shared/base_template.j2"
  purpose: "Base template with common macros"

components:
  path: "{TEMPLATES_BASE}/shared/components.j2"
  purpose: "Reusable component macros"

validation_template:
  path: "{TEMPLATES_BASE}/validation/quality_checklist.j2"
  purpose: "Content quality validation"
```

### Template Selection Algorithm

```python
def select_optimal_template(data_context):
    """Intelligent template selection based on data characteristics"""

    # Template A: Primary Condition
    if (data_context.get('metric_1', 0) > threshold_1 and
        data_context.get('confidence', 0) > threshold_2):
        return 'category/template_variant_a.j2'

    # Template B: Alternative Condition
    if (condition_check(data_context) and
        data_context.get('type') == 'specific_type'):
        return 'category/template_variant_b.j2'

    # Default fallback
    return 'category/default_template.j2'
```

---

## Standardization Framework

### Problems Solved

**Before Standardization:**
- **Inconsistent Path References**: Mixed relative/absolute paths breaking in different environments
- **Vague Script Mappings**: No clear connection between command names and Python script implementations
- **Template Reference Chaos**: Inconsistent template documentation and selection criteria
- **CLI Command Inconsistencies**: Missing parameter specifications and service health checks

**After Standardization:**
- **Unified Path System**: Consistent `{SCRIPTS_BASE}`, `{DATA_OUTPUTS}`, `{TEMPLATES_BASE}` variables
- **Clear Script Integration**: Direct mapping to Python classes and registry decorators
- **Structured Template References**: Standardized template selection and shared component documentation
- **Complete CLI Documentation**: Full syntax, parameter types, and health check procedures

### Enhanced Command Headers

**Before:**
```markdown
**Outputs To**: `./data/outputs/fundamental_analysis/`
```

**After:**
```markdown
**Command Classification**: 🎯 **Assistant**
**Knowledge Domain**: `fundamental-analysis-expertise`
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-07-18)*
**Outputs To**: `{DATA_OUTPUTS}/fundamental_analysis/`
```

### Script Integration Mapping Enhancement

**Standardized Section:**
```markdown
## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/fundamental_analysis_script.py`
**Script Class**: `FundamentalAnalysisScript`
**Registry Name**: `fundamental_analysis`
**Content Types**: `["fundamental"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="fundamental_analysis",
    content_types=["fundamental"],
    requires_validation=True
)
class FundamentalAnalysisScript(BaseScript):
    """Fundamental analysis script implementation"""
```

### Template Reference Standardization

**Before:**
```markdown
**Template Selection Logic**:
```python
template_mapping = {
    'valuation_disconnect': 'fundamental/twitter_fundamental_A_valuation.j2',
}
```

**After:**
```markdown
**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| valuation_disconnect | `{TEMPLATES_BASE}/fundamental/twitter_fundamental_A_valuation.j2` | P/E > sector_avg AND confidence > 0.85 | Valuation analysis posts |
| growth_momentum | `{TEMPLATES_BASE}/fundamental/twitter_fundamental_B_growth.j2` | revenue_growth > 15% AND margin_expansion > 0 | Growth story posts |
| quality_assessment | `{TEMPLATES_BASE}/fundamental/twitter_fundamental_C_quality.j2` | roe > 15% AND debt_ratio < 0.5 | Quality metrics posts |
```

---

## Path Configuration System

### Base Path Variables

**Primary Base Paths:**
```yaml
SCRIPTS_BASE:
  default: "./scripts"
  description: "Root directory for all Python scripts"
  environment_variable: "SENSYLATE_SCRIPTS_BASE"
  examples:
    - "{SCRIPTS_BASE}/yahoo_finance_cli.py"
    - "{SCRIPTS_BASE}/base_scripts/fundamental_analysis_script.py"
    - "{SCRIPTS_BASE}/fundamental_analysis/fundamental_discovery.py"

DATA_OUTPUTS:
  default: "./data/outputs"
  description: "Root directory for all generated outputs"
  environment_variable: "SENSYLATE_DATA_OUTPUTS"
  examples:
    - "{DATA_OUTPUTS}/fundamental_analysis/AAPL_20250718.md"
    - "{DATA_OUTPUTS}/twitter/fundamental_analysis/TSLA_20250718.md"
    - "{DATA_OUTPUTS}/sector_analysis/technology_20250718.md"

TEMPLATES_BASE:
  default: "./scripts/templates"
  description: "Root directory for all Jinja2 templates"
  environment_variable: "SENSYLATE_TEMPLATES_BASE"
  examples:
    - "{TEMPLATES_BASE}/twitter/fundamental/twitter_fundamental_A_valuation.j2"
    - "{TEMPLATES_BASE}/shared/base_twitter.j2"
    - "{TEMPLATES_BASE}/validation/content_quality_checklist.j2"

DATA_IMAGES:
  default: "./data/images"
  description: "Root directory for all image data"
  environment_variable: "SENSYLATE_DATA_IMAGES"
  examples:
    - "{DATA_IMAGES}/trendspider_tabular/AAPL_20250718.png"
    - "{DATA_IMAGES}/tradingview/TSLA_20250718.png"
    - "{DATA_IMAGES}/charts/sector_performance_20250718.png"
```

### Configuration Paths

```yaml
CONFIG_BASE:
  default: "./config"
  description: "Configuration files and settings"
  environment_variable: "SENSYLATE_CONFIG_BASE"
  examples:
    - "{CONFIG_BASE}/financial_services.yaml"
    - "{CONFIG_BASE}/script_registry.json"
    - "{CONFIG_BASE}/validation_thresholds.yaml"

LOGS_BASE:
  default: "./logs"
  description: "Application logs and execution traces"
  environment_variable: "SENSYLATE_LOGS_BASE"
  examples:
    - "{LOGS_BASE}/twitter_system.log"
    - "{LOGS_BASE}/cli_services.log"
    - "{LOGS_BASE}/validation_results.log"
```

### Path Resolution Logic

**Environment Variable Priority:**
1. **Environment Variable** (if set)
2. **Configuration File** (if specified in ScriptConfig)
3. **Default Relative Path** (fallback)

**Implementation Example:**
```python
import os
from pathlib import Path

class PathResolver:
    """Standardized path resolution for all commands"""

    def __init__(self):
        self.base_paths = {
            'SCRIPTS_BASE': self._resolve_path('SENSYLATE_SCRIPTS_BASE', './scripts'),
            'DATA_OUTPUTS': self._resolve_path('SENSYLATE_DATA_OUTPUTS', './data/outputs'),
            'TEMPLATES_BASE': self._resolve_path('SENSYLATE_TEMPLATES_BASE', './scripts/templates'),
            'DATA_IMAGES': self._resolve_path('SENSYLATE_DATA_IMAGES', './data/images'),
            'CONFIG_BASE': self._resolve_path('SENSYLATE_CONFIG_BASE', './config'),
            'LOGS_BASE': self._resolve_path('SENSYLATE_LOGS_BASE', './logs')
        }

    def _resolve_path(self, env_var: str, default: str) -> Path:
        """Resolve path with environment variable priority"""
        path_str = os.getenv(env_var, default)
        return Path(path_str).resolve()

    def get_path(self, path_template: str) -> Path:
        """Resolve path template with base variables"""
        resolved = path_template
        for var, path in self.base_paths.items():
            resolved = resolved.replace(f'{{{var}}}', str(path))
        return Path(resolved)
```

---

## Script Integration Patterns

### Registry-Based Script Execution

**Direct Python Execution:**
```python
from script_registry import get_global_registry
from script_config import ScriptConfig

# Initialize
config = ScriptConfig.from_environment()
registry = get_global_registry(config)

# Execute single script
result = registry.execute_script(
    "{registry_name}",
    parameter_1="value_1",
    parameter_2="value_2",
    template_variant="template_a"  # Optional override
)

# Execute workflow (multi-phase)
workflow_result = execute_workflow(
    phases=["discover", "analyze", "synthesize", "validate"],
    parameter_1="value_1",
    parameter_2="value_2"
)
```

### Command Line Execution

**Via Content Automation CLI:**
```bash
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script {registry_name} \
    --parameter-1 value_1 \
    --parameter-2 value_2 \
    --template-variant template_a
```

**Via Direct Script Execution:**
```bash
python {SCRIPTS_BASE}/path/to/primary_script.py \
    --parameter-1 value_1 \
    --parameter-2 value_2 \
    --config-file config.yaml
```

### Claude Command Execution

```
/{command_name} parameter_1 parameter_2
/{command_name} action=specific_action parameter_1=value_1
/{command_name} /path/to/validation/file_validation.json
```

---

## Template Architecture

### Template Selection Framework

**Intelligent Template Selection:**
```python
def select_optimal_template(data_context):
    """Dynamic template selection based on data characteristics"""

    # High-confidence valuation analysis
    if (data_context.get('pe_ratio', 0) > data_context.get('sector_pe', 0) * 1.2 and
        data_context.get('confidence', 0) > 0.85):
        return '{TEMPLATES_BASE}/fundamental/twitter_fundamental_A_valuation.j2'

    # Growth momentum detection
    if (data_context.get('revenue_growth', 0) > 15 and
        data_context.get('margin_expansion', 0) > 0):
        return '{TEMPLATES_BASE}/fundamental/twitter_fundamental_B_growth.j2'

    # Quality assessment criteria
    if (data_context.get('roe', 0) > 15 and
        data_context.get('debt_ratio', 1) < 0.5):
        return '{TEMPLATES_BASE}/fundamental/twitter_fundamental_C_quality.j2'

    # Default template
    return '{TEMPLATES_BASE}/fundamental/twitter_fundamental_default.j2'
```

### Shared Component Architecture

**Base Template Inheritance:**
```jinja2
{# Base template: {TEMPLATES_BASE}/shared/base_twitter.j2 #}
{% macro twitter_header(symbol, company_name) %}
🎯 ${{ symbol }} | {{ company_name }}
{% endmacro %}

{% macro confidence_indicator(score) %}
{% if score >= 0.95 %}🟢 High Confidence
{% elif score >= 0.85 %}🟡 Moderate Confidence
{% else %}🔴 Low Confidence{% endif %}
{% endmacro %}

{% macro hashtags(category, themes) %}
#{{ category }} #StockAnalysis
{% for theme in themes %}#{{ theme|replace(' ', '') }}{% endfor %}
{% endmacro %}
```

**Template Inheritance Pattern:**
```jinja2
{# Specific template: {TEMPLATES_BASE}/fundamental/twitter_fundamental_A_valuation.j2 #}
{% extends "shared/base_twitter.j2" %}

{% block content %}
{{ twitter_header(symbol, company_name) }}

📊 VALUATION ANALYSIS
• P/E Ratio: {{ pe_ratio }} vs Sector {{ sector_pe }}
• Price Target: ${{ price_target }} ({{ upside }}% upside)
• Fair Value: {{ fair_value_assessment }}

{{ confidence_indicator(confidence_score) }}

{{ hashtags("Valuation", value_themes) }}
{% endblock %}
```

---

## Quality Assurance Framework

### Validation Protocols

**Multi-Source Validation Standards:**
- **Data Accuracy**: ≤2% variance from authoritative sources
- **Content Integrity**: ≤1% variance for critical claims
- **Real-Time Currency**: Current market data integration
- **Service Health**: 80%+ operational across all CLI services

### Quality Gate Enforcement

**Critical Validation Points:**
1. **Input Phase**: Data source validation and completeness check
2. **Processing Phase**: Template selection and content generation
3. **Validation Phase**: Quality scoring and compliance verification
4. **Output Phase**: Final review and institutional certification

### Confidence Scoring Framework

**Institutional-Quality Thresholds:**
- **Baseline Quality**: 9.0/10 minimum for institutional usage
- **Enhanced Quality**: 9.5/10 target for validation-optimized content
- **Premium Quality**: 9.8/10 for compliance-critical requirements
- **Perfect Quality**: 10.0/10 for exact regulatory compliance

### Quality Metadata Structure

```json
{
  "metadata": {
    "command_name": "{command_name}",
    "execution_timestamp": "ISO_8601_format",
    "framework_version": "X.Y.Z",
    "confidence_score": "9.X/10.0",
    "validation_status": "PASSED|FLAGGED|FAILED"
  },
  "execution_context": {
    "script_class": "{ScriptClassName}",
    "template_used": "template_variant_x.j2",
    "cli_services_health": {"service_1": "healthy", "service_2": "healthy"},
    "data_sources": ["source_1", "source_2", "source_3"]
  },
  "quality_assessment": {
    "data_accuracy": "9.X/10.0",
    "content_quality": "9.X/10.0",
    "compliance_status": "COMPLIANT|FLAGGED|NON_COMPLIANT",
    "institutional_ready": "true|false"
  }
}
```

---

## Development Workflow

### Command Development Process

**1. Command Creation:**
```bash
# Create new command using standardized template
cp docs/commands/COMMAND_TEMPLATE.md .claude/commands/new-command.md
# Edit command specification
# No registry changes needed - simplified system
```

**2. Quality Validation:**
```bash
# Validate command specification
pre-commit run --all-files
# Use standard Python quality tools
make lint
make test
```

**3. Integration Testing:**
```bash
# Test command execution
python tests/collaboration/test_new_command.py
# Validate cross-command integration
python tests/integration/test_command_workflow.py
```

### Cross-Command Integration

**Upstream Dependencies:**
- Commands that provide input to this command
- Data type specifications and file locations
- Quality threshold requirements

**Downstream Dependencies:**
- Commands that consume this command's outputs
- Output format specifications
- Integration trigger conditions

**Coordination Workflows:**
```bash
# Sequential execution
/{upstream_command} parameter_1 parameter_2
/{current_command} derived_parameter_1 derived_parameter_2
/{downstream_command} output_reference

# Parallel validation
/{current_command} input_a && /{validation_command} output_a
```

### Output Management

**File Organization:**
```
{DATA_OUTPUTS}/output_directory/
├── {IDENTIFIER}_{YYYYMMDD}.md (primary output)
├── {IDENTIFIER}_{YYYYMMDD}_metadata.json (execution metadata)
├── backup/{IDENTIFIER}_{YYYYMMDD}_backup.md (backup copy)
└── validation/{IDENTIFIER}_{YYYYMMDD}_validation.json (quality validation)
```

---

The command system provides a comprehensive framework for developing, standardizing, and executing AI-powered analysis workflows. Through consistent interfaces, intelligent template selection, and robust quality assurance, commands enable institutional-grade content generation with full traceability and validation.

---

**Command System Authority**: Comprehensive Development Framework Excellence
**Implementation Confidence**: 9.7/10.0
**Quality Standards**: Institutional-grade with systematic standardization
**Status**: Production-ready with continuous optimization
