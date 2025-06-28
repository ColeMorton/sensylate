# Universal Evaluation System

## Overview

The Universal Evaluation System is the core component of Sensylate's quality assurance framework, providing comprehensive 4-phase evaluation protocols for all AI commands.

## Architecture

### Core Components

```
evaluation/
├── command_evaluation_protocol.py    # Main evaluation engine
├── universal_dependency_validator.py # Dependency management system
└── results/                         # Evaluation execution results
    ├── *_evaluation_*.json          # Individual command evaluations
    ├── phase*_validation_results_*.json # Phase validation results
    └── universal_integration_results_*.json # Framework integration results
```

## Evaluation Protocol

### 4-Phase Evaluation Pipeline

#### Phase 0A: Pre-Execution Validation
**Purpose**: Validate inputs and dependencies before command execution

**Quality Gates**:
- **Input Validation** (Critical): Validate command parameters and context
- **Dependency Validation** (Critical): Check external dependencies and data sources
- **Enhancement Detection**: Detect evaluation files for enhanced mode
- **Historical Performance**: Check command performance metrics

**Thresholds**:
- Critical gates: 0.95+ (must pass to proceed)
- Non-critical gates: 0.7+ (advisory)

#### Phase 0B: Execution Monitoring
**Purpose**: Monitor command execution in real-time

**Quality Gates**:
- **Execution Progress**: Track command milestones and progress
- **Resource Monitoring**: Monitor system resource usage
- **Performance Tracking**: Real-time performance assessment

**Adaptive Thresholds**: Automatically adjust based on command complexity and historical performance

#### Phase 0C: Post-Execution Validation
**Purpose**: Validate outputs and ensure quality standards

**Quality Gates**:
- **Output Validation** (Critical): Validate format and completeness
- **Quality Scoring**: Score output against command standards
- **Template Compliance**: Ensure consistent formatting
- **Content Validation**: Verify content quality and accuracy

#### Phase 0D: Feedback Integration
**Purpose**: Learn from execution and improve future performance

**Quality Gates**:
- **Learning Integration**: Integrate results into learning systems
- **Performance Metrics**: Record metrics for optimization
- **Feedback Loop**: Update thresholds and parameters
- **Knowledge Base Update**: Contribute to team knowledge

### Evaluation Results

Each evaluation produces comprehensive results:

```python
@dataclass
class EvaluationResult:
    command: str
    overall_score: float           # 0.0-1.0 overall quality score
    can_proceed: bool             # Whether execution should continue
    phase_results: Dict[str, PhaseResult]  # Results for each phase
    execution_time: float         # Total evaluation time
    metadata: Dict[str, Any]      # Additional evaluation metadata
```

## Dependency Validation

### Intelligent Dependency Management

The Universal Dependency Validator provides:

- **Real-time Health Checks**: Validate dependency availability
- **Intelligent Fallbacks**: Automatic fallback strategy execution
- **Performance Optimization**: Cache validation results
- **Failure Recovery**: Graceful degradation when dependencies fail

### Dependency Types

**Supported Dependency Types**:
- `api`: External API services (Yahoo Finance, TrendSpider)
- `data_source`: Data files and databases
- `file_system`: Local file system resources
- `service`: External services and tools
- `internal`: Internal command dependencies

### Fallback Strategies

**Automatic Fallback Management**:
- **Cached Data**: Use previously cached data when APIs unavailable
- **Alternative Sources**: Switch to backup data providers
- **Degraded Mode**: Continue with reduced functionality
- **Local Mode**: Use local resources when external unavailable
- **Temporary Storage**: Use temporary storage when primary unavailable

### Validation Results

```python
@dataclass
class ValidationResult:
    dependency_name: str
    available: bool              # Whether dependency is available
    validation_score: float      # 0.0-1.0 quality score
    fallback_used: str          # Fallback strategy used (if any)
    error_message: str          # Error details (if failed)
    response_time: float        # Validation response time
```

## Usage

### Evaluation Protocol

```python
from evaluation.command_evaluation_protocol import CommandEvaluationProtocol

# Initialize evaluation protocol
protocol = CommandEvaluationProtocol()

# Load evaluation manifest
with open('.claude/commands/command.eval.yaml') as f:
    manifest = yaml.safe_load(f)

# Run evaluation
context = {"command": "example", "parameters": {...}}
result = protocol.evaluate_command("example", manifest, context)

# Check if execution should proceed
if result.can_proceed:
    # Execute command with validation
    execute_command_with_quality_assurance()
else:
    # Handle validation failure
    handle_evaluation_failure(result)
```

### Dependency Validation

```python
from evaluation.universal_dependency_validator import UniversalDependencyValidator

# Initialize validator
validator = UniversalDependencyValidator()

# Load dependency manifest
with open('.claude/commands/command.deps.yaml') as f:
    manifest = yaml.safe_load(f)

# Validate dependencies
result = validator.validate_command_dependencies("example", manifest)

# Use fallback strategies if needed
if not result["can_proceed"]:
    fallback_strategy = result["fallback_strategy"]
    execute_with_fallback(fallback_strategy)
```

## Configuration

### Evaluation Manifests

Define evaluation configuration in `.eval.yaml` files:

```yaml
command: example_command
version: "1.0"
evaluation:
  phases:
    0A_pre_execution:
      gates:
        - name: input_validation
          description: "Validate command input parameters"
          threshold: 1.0
          critical: true
          adaptive: false
        - name: dependency_validation
          description: "Validate external dependencies"
          threshold: 0.95
          critical: true
          adaptive: false
    0B_execution_monitoring:
      gates:
        - name: execution_progress
          threshold: 0.8
          critical: false
          adaptive: true
    0C_post_execution:
      gates:
        - name: output_validation
          threshold: 0.9
          critical: true
    0D_feedback_integration:
      gates:
        - name: learning_integration
          threshold: 0.8
          critical: false
  quality_targets:
    overall_threshold: 0.75
    critical_gate_threshold: 0.95
    performance_target: 0.85
```

### Dependency Manifests

Define dependencies in `.deps.yaml` files:

```yaml
command: example_command
version: "1.0"
dependencies:
  yahoo_finance_api:
    type: api
    required: true
    validation_method: api_test
    fallback_strategies:
      - strategy: cached_data
        description: "Use cached data if API unavailable"
        max_age_hours: 4
      - strategy: alternative_source
        description: "Use alternative data source"
        source: backup_api
  market_data_cache:
    type: data_source
    required: false
    validation_method: file_check
    fallback_strategies:
      - strategy: fresh_download
        description: "Download fresh data if cache unavailable"
```

## Performance Metrics

### Evaluation Performance

**Typical Performance**:
- Phase 0A: ~0.1 seconds per command
- Phase 0B: Real-time monitoring (minimal overhead)
- Phase 0C: ~0.05 seconds per command
- Phase 0D: ~0.02 seconds per command

**Total Overhead**: <0.2 seconds per command execution

### Quality Metrics

**Framework-wide Metrics**:
- Average Quality Score: 53.9%
- Integration Coverage: 100% (14/14 commands)
- Dependency Success Rate: 90%+ with fallbacks
- Template Compliance: Variable with automatic fixes

### Success Rates

**Evaluation Success Rates**:
- Critical Gate Pass Rate: 95%+
- Overall Evaluation Success: 90%+
- Dependency Validation Success: 90%+
- Template Compliance Success: 85%+ (with automatic fixes)

## Monitoring & Analytics

### Real-time Monitoring

- Command execution tracking
- Quality gate performance
- Dependency health status
- Performance metrics

### Analytics Dashboard

- Quality score trends
- Evaluation performance metrics
- Dependency reliability statistics
- Template compliance rates

### Results Storage

All evaluation results stored in `results/` directory:

```
results/
├── command_evaluation_YYYYMMDD_HHMMSS.json    # Individual evaluations
├── phase_validation_results_YYYYMMDD.json     # Phase validation summaries
└── universal_integration_results_YYYYMMDD.json # Framework integration results
```

## Development

### Adding New Quality Gates

1. **Define Gate Logic**: Implement gate validation logic
2. **Update Manifest Schema**: Add gate configuration options
3. **Test Gate**: Validate with test commands
4. **Document Gate**: Add documentation and examples

### Extending Dependency Types

1. **Implement Validator**: Create dependency type validator
2. **Add Fallback Strategies**: Define intelligent fallback options
3. **Update Schema**: Extend dependency manifest schema
4. **Test Integration**: Validate with real dependencies

### Custom Evaluation Phases

1. **Define Phase Logic**: Implement phase evaluation logic
2. **Integrate with Protocol**: Add to evaluation pipeline
3. **Update Configuration**: Extend manifest configuration
4. **Performance Testing**: Ensure minimal overhead

## Troubleshooting

### Common Issues

**Quality Gate Failures**:
```bash
# Check evaluation results
cat results/*_evaluation_*.json

# Review gate thresholds
grep -A 5 "threshold" .claude/commands/*.eval.yaml
```

**Dependency Validation Errors**:
```bash
# Check dependency cache
ls ../cache/*_validation.json

# Test dependency manually
python -c "from evaluation.universal_dependency_validator import UniversalDependencyValidator; validator = UniversalDependencyValidator(); print(validator.validate_dependency_by_name('yahoo_finance_api'))"
```

**Performance Issues**:
```bash
# Check evaluation times
grep "execution_time" results/*_evaluation_*.json

# Monitor resource usage during evaluation
python evaluation/command_evaluation_protocol.py --debug
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Evaluation components will output detailed debug information
from evaluation.command_evaluation_protocol import CommandEvaluationProtocol
protocol = CommandEvaluationProtocol(debug=True)
```

## Best Practices

### Quality Gate Design
- Keep critical gates focused on essential validation
- Use adaptive thresholds for performance-based gates
- Implement graceful degradation for non-critical failures
- Monitor gate performance and adjust thresholds

### Dependency Management
- Define comprehensive fallback strategies
- Cache validation results for performance
- Monitor dependency health proactively
- Implement circuit breaker patterns for unreliable dependencies

### Performance Optimization
- Minimize evaluation overhead (<0.2s per command)
- Use asynchronous validation where possible
- Implement intelligent caching strategies
- Profile evaluation performance regularly

---

**Status**: Universal Evaluation System active across all 14 commands with comprehensive quality assurance, intelligent dependency management, and performance optimization.
