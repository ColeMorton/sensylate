# Integrated Framework Specification - 2025-06-28

## Overview

This document specifies the **Integrated Framework Stack** for the Sensylate AI command ecosystem, combining three foundational systems:

1. **Universal Evaluation Framework** - Systematic quality assurance
2. **Smart Workflow Orchestration** - Intelligent user interaction and workflow management
3. **Standardized Dependency Management** - Reliable command execution with intelligent fallbacks

## Universal Evaluation Framework

### Command Evaluation Protocol (CEP)

**Four-Phase Evaluation Structure**:

```yaml
# Universal Evaluation Phases
evaluation_phases:
  0A_pre_execution:
    - dependency_validation
    - input_validation
    - historical_performance_check
    - fallback_strategy_preparation

  0B_execution_monitoring:
    - progress_tracking
    - resource_monitoring
    - error_detection
    - performance_metrics

  0C_post_execution:
    - output_validation
    - confidence_scoring
    - business_rule_compliance
    - template_compliance_check

  0D_feedback_integration:
    - variant_generation
    - parameter_optimization
    - learning_integration
    - user_preference_updates
```

### Evaluation Manifest Schema

```yaml
# .claude/commands/{command}.eval.yaml
evaluation_manifest:
  version: "1.0"
  command: "{command_name}"

  quality_gates:
    pre_execution:
      - gate: "dependency_availability"
        threshold: 0.95
        critical: true
      - gate: "input_validation"
        threshold: 1.0
        critical: true

    post_execution:
      - gate: "confidence_score"
        threshold: 0.7
        adaptive: true
      - gate: "template_compliance"
        threshold: 0.9
        critical: false

  retry_strategies:
    - strategy: "enhanced_parameters"
      trigger: "confidence_score < threshold"
      max_attempts: 2
    - strategy: "fallback_data_sources"
      trigger: "dependency_failure"
      max_attempts: 1

  learning_config:
    track_user_preferences: true
    adaptive_thresholds: true
    failure_pattern_analysis: true
```

## Smart Workflow Orchestration

### Intelligent Workflow Engine

**Core Components**:

```python
# team-workspace/workflows/orchestrator.py
class SmartWorkflowOrchestrator:
    """Intelligent workflow management with user interaction."""

    def on_command_completion(self, command: str, result: dict, context: dict):
        """Triggered when any command completes successfully."""

        # Generate contextual suggestions
        suggestions = self.suggestion_engine.generate_suggestions(
            command, result, context
        )

        # Present intelligent options to user
        user_choice = self.present_interactive_options({
            'completed_task': f"{command} finished successfully",
            'key_results': self.extract_key_results(result),
            'suggested_actions': suggestions,
            'estimated_times': self.calculate_execution_times(suggestions),
            'user_history': self.get_user_preference_context(command)
        })

        # Execute user choice with context preservation
        if user_choice.action != 'stop':
            self.execute_next_step_with_context(user_choice, result)
```

### Suggestion Engine Configuration

```yaml
# team-workspace/workflows/suggestion_rules.yaml
suggestion_rules:
  fundamental_analysis:
    completion_actions:
      - action: "social_media_content"
        condition: "result.recommendation == 'BUY'"
        params:
          content_type: "fundamental_analysis"
          source: "{result.output_file}"
        priority: 1
        estimated_time: "2 minutes"

      - action: "content_publisher"
        condition: "result.reliability_score >= 0.9"
        params:
          content: "{result.output_file}"
          destination: "blog"
        priority: 2
        estimated_time: "1 minute"

      - action: "fundamental_analysis"
        condition: "always"
        params:
          ticker: "{suggested_peer_stocks}"
        priority: 3
        estimated_time: "{stock_count * 8} minutes"

  social_media_content:
    completion_actions:
      - action: "content_publisher"
        condition: "result.engagement_score >= 0.8"
        params:
          content: "{result.output_file}"
          schedule: "optimal_time"
        priority: 1
        estimated_time: "30 seconds"
```

### User Preference Learning

```python
# team-workspace/workflows/preference_engine.py
class UserPreferenceLearning:
    """Learns user workflow preferences for intelligent suggestions."""

    def record_user_decision(self, context: dict, suggestions: list, choice: str):
        """Track user decisions to improve future suggestions."""

        self.preference_history.append({
            'context': context,
            'suggestions': suggestions,
            'choice': choice,
            'timestamp': datetime.now(),
            'workflow_stage': context.get('stage'),
            'success_outcome': None  # Updated later
        })

    def predict_likely_choice(self, context: dict, suggestions: list) -> Prediction:
        """Predict user's likely choice based on historical patterns."""

        similar_contexts = self.find_similar_contexts(context)

        if len(similar_contexts) >= 5:  # Sufficient data
            most_common = self.analyze_choice_patterns(similar_contexts)
            confidence = self.calculate_prediction_confidence(most_common, similar_contexts)

            return Prediction(
                choice=most_common,
                confidence=confidence,
                reasoning=f"Based on {len(similar_contexts)} similar contexts"
            )

        return Prediction(choice=suggestions[0], confidence=0.5, reasoning="Insufficient data")
```

## Standardized Dependency Management

### Dependency Manifest Schema

```yaml
# .claude/commands/{command}.deps.yaml
dependency_manifest:
  version: "1.0"
  command: "{command_name}"

  external_dependencies:
    required:
      - name: "market_data"
        type: "api_endpoint"
        source: "yahoo_finance"
        validation: "real_time_price_available"
        fallback: "cached_data_max_age_24h"
        critical: true

    optional:
      - name: "analyst_ratings"
        type: "third_party_data"
        source: "multiple_providers"
        enhancement: "market_sentiment_context"

  user_inputs:
    required:
      - parameter: "ticker"
        type: "string"
        validation: "^[A-Z]{1,5}$"
        description: "Stock symbol for analysis"

    optional:
      - parameter: "depth"
        type: "enum"
        values: ["summary", "standard", "comprehensive", "deep_dive"]
        default: "comprehensive"

  internal_dependencies:
    commands:
      - name: "yahoo_finance_service"
        version: ">=2.0"
        purpose: "market_data_retrieval"
        critical: true

  environment_requirements:
    api_keys:
      - name: "YAHOO_FINANCE_API_KEY"
        required: false
        purpose: "enhanced_rate_limits"
        fallback: "public_api_with_limits"

  data_quality_requirements:
    freshness:
      market_data: "max_age_minutes: 15"
      financial_statements: "max_age_days: 90"
    completeness:
      minimum_data_coverage: 0.8
    reliability:
      confidence_threshold: 0.7
```

### Universal Dependency Validator

```python
# team-workspace/dependencies/validator.py
class UniversalDependencyValidator:
    """Standardized dependency validation for all commands."""

    def validate_all_dependencies(self, command_name: str,
                                user_inputs: Dict[str, Any]) -> ValidationResult:
        """Comprehensive dependency validation with intelligent fallbacks."""

        manifest = self.load_dependency_manifest(command_name)
        results = ValidationResult()

        # Validate external dependencies with fallback handling
        for dep in manifest.external_dependencies.required:
            primary_result = self.validate_dependency(dep)

            if primary_result.failed and dep.fallback:
                fallback_result = self.try_fallback(dep)
                if fallback_result.success:
                    results.add_degraded_dependency(dep.name, fallback_result)
                else:
                    results.add_failed_dependency(dep.name, primary_result)
            else:
                results.add_dependency_result(dep.name, primary_result)

        # Generate user guidance for failures
        if results.has_failures():
            results.resolution_guidance = self.generate_resolution_guidance(results)

        return results

    def generate_resolution_guidance(self, results: ValidationResult) -> List[ResolutionStep]:
        """Generate step-by-step guidance for resolving dependency issues."""

        guidance = []

        for failure in results.failed_dependencies:
            if failure.type == "api_key_missing":
                guidance.append(ResolutionStep(
                    step=f"Set environment variable: {failure.required_key}",
                    command=f"export {failure.required_key}=your_api_key_here",
                    optional=failure.fallback_available
                ))
            elif failure.type == "service_unavailable":
                guidance.append(ResolutionStep(
                    step=f"Service {failure.service} is unavailable",
                    suggestion="Wait for service recovery or use cached data",
                    auto_retry=True,
                    retry_interval_minutes=5
                ))

        return guidance
```

## Template System Integration

### Template Registry

```yaml
# team-workspace/templates/registry.yaml
template_registry:
  fundamental_analysis:
    version: "2.0"  # Updated for framework integration
    target_commands: ["fundamental_analysis"]
    structure:
      header:
        required_fields:
          - title: "pattern: '{TICKER} Fundamental Analysis - {YYYY-MM-DD}'"
          - author: "standardized: 'Cole Morton'"
          - publishDate: "auto-generated: YYYY-MM-DD format"
          - categories: "standardized: ['Fundamental Analysis', 'Stocks']"
          - tags: "auto-generated: ['{TICKER}', 'stock-analysis', 'investment']"
          - image: "pattern: '/images/tradingview/{TICKER}_{YYYYMMDD}.png'"
          - draft: "boolean: false"
      content_sections:
        - investment_thesis:
            word_range: [200, 400]
            required_elements: ["recommendation", "fair_value", "expected_returns"]
        - business_intelligence_dashboard:
            required_tables: 3+
            required_metrics: 40+
        - competitive_analysis:
            word_range: [1000, 1500]
        - valuation_analysis:
            required_methods: ["DCF", "Comparable_Companies"]
        - risk_matrix:
            required_format: "probability_x_impact_table"
        - analysis_metadata:
            required_confidence_scores: 15+
    quality_gates:
      total_word_count: [8000, 12000]
      confidence_score_average: 0.7+
      quantified_metrics: 50+
      external_sources: 5+
    evaluation_integration:
      phase_0C_validation: true
      compliance_threshold: 0.9
      auto_correction: true

  social_media:
    version: "2.0"  # Updated for framework integration
    target_commands: ["social_media_content"]
    structure:
      header:
        required_fields:
          - title: "descriptive and engaging"
          - author: "standardized: 'Cole Morton'"
          - categories: "standardized: ['Social Media', 'Trading']"
      content_sections:
        - hook_architecture:
            character_limit: 280
            engagement_elements: ["curiosity_gap", "value_proposition"]
        - value_delivery:
            format: "bullet_points"
            mobile_optimized: true
        - call_to_action:
            required: true
            placement: "end"
    quality_gates:
      total_character_count: [500, 4000]
      mobile_readability: true
      engagement_score: 0.8+
    evaluation_integration:
      phase_0C_validation: true
      compliance_threshold: 0.9
      auto_correction: true
```

## Implementation Roadmap

### Phase 1: Foundation (0-30 days)

**Week 1-2: Core Infrastructure**
- Implement Universal Dependency Validator
- Create evaluation manifest schema
- Build Smart Workflow Orchestrator base

**Week 3-4: Pilot Integration**
- Deploy framework on `fundamental_analysis` command
- Create `social_media_content` unified command
- Implement basic user preference tracking

### Phase 2: Ecosystem Migration (30-90 days)

**Month 2: Full Command Coverage**
- Create dependency manifests for all 16 commands
- Deploy evaluation framework across ecosystem
- Implement template validation for all content commands

**Month 3: Advanced Features**
- Deploy user preference learning
- Implement intelligent workflow suggestions
- Enable auto-execution for high-confidence predictions

### Phase 3: Intelligence Enhancement (90+ days)

**Months 4-6: Autonomous Features**
- Machine learning-based workflow prediction
- Adaptive dependency resolution
- Dynamic template optimization based on performance

## Success Criteria

### Technical Metrics
- **Framework Adoption**: 100% command coverage
- **Dependency Resolution**: 99%+ success rate with fallbacks
- **Evaluation Pass Rate**: 90%+ after optimization
- **Template Compliance**: 100% for content commands

### User Experience Metrics
- **Decision Time Reduction**: 60% faster workflow decisions
- **Workflow Completion**: 85%+ multi-step completion rate
- **User Satisfaction**: 80%+ acceptance of intelligent suggestions
- **Context Preservation**: 95% seamless data transfer success

### Business Impact Metrics
- **Content Quality**: 100% consistency vs current 95%
- **Automation Level**: 95% vs current 85%
- **Execution Reliability**: 98%+ vs current 94.2%
- **Development Velocity**: 40% faster command development with standardized frameworks

## Maintenance and Evolution

### Continuous Improvement
- Weekly evaluation metric analysis
- Monthly user preference pattern review
- Quarterly framework optimization cycles
- Semi-annual ecosystem health assessments

### Adaptive Learning
- Real-time threshold optimization based on success patterns
- Dynamic workflow suggestion improvements
- Continuous template optimization based on performance analytics
- Predictive dependency resolution enhancement

This integrated framework transforms the Sensylate ecosystem into an intelligent, self-improving platform that delivers institutional-quality content with seamless user experience and reliable execution.

---
*Specification authored by Command Management Specialist*
*Date: 2025-06-28*
*Version: 1.0*
