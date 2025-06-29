# AI Command Microservices Specification
*Atomic command architecture for sophisticated AI collaboration*

## Executive Summary

This specification defines the **AI Command Microservices Architecture** - a systematic approach to decomposing monolithic AI commands into atomic, composable services that follow the `{role}_{action}.md` naming convention and implement framework-driven execution patterns.

**Key Innovation**: Transform large, monolithic commands into focused microservices that can be independently optimized, composed into workflows, and systematically validated while maintaining the collaborative intelligence principles of the Sensylate ecosystem.

**Team-Workspace Enhancement**: The microservice architecture supports flexible **role-to-command relationships** where each role can map to one or many commands. A role like `fundamental_analyst` can generate multiple specialized commands (e.g., `fundamental_analyst_discover`, `fundamental_analyst_analyze`, etc.), creating a more granular and flexible command ecosystem.

## Core Architecture Principles

### 1. **Atomic Responsibility Principle**
Each command microservice handles exactly one phase of a framework methodology:
- **Single Action**: One framework phase per command (discover, analyze, synthesize, validate)
- **Clear Boundaries**: Explicit input/output specifications
- **Independent Execution**: Can run standalone or as part of composed workflows

### 2. **Role-Based Organization Principle**
Commands are organized by functional role within the AI collaboration ecosystem:
- **Domain Experts**: `fundamental_analyst_*`, `twitter_strategist_*`, `market_researcher_*`
- **Infrastructure Roles**: `architect_*`, `code_owner_*`, `product_owner_*`
- **Workflow Coordinators**: `command_*`, `workflow_*`, `orchestrator_*`

### 3. **Framework Alignment Principle**
Command structure directly maps to established methodologies:
- **DASV Framework**: Discover → Analyze → Synthesize → Validate
- **RPIV Framework**: Research → Plan → Implement → Validate
- **TCEM Framework**: Trigger → Coordinate → Execute → Monitor

## Naming Convention Standard

### File Naming Pattern
```
{role}_{action}.md
{role}_{action}_{product}.md  # Optional product specification
```

### Product-Specific Naming
When a command generates domain-specific outputs, the optional `{product}` component specifies the expected deliverable:

```yaml
product_examples:
  twitter_strategist_synthesize_trading_strategy.md    # Trading-focused social content
  twitter_strategist_synthesize_fundamental_analysis.md # Analysis-focused social content
  twitter_strategist_synthesize_market_commentary.md    # Market insight social content

  fundamental_analyst_validate_earnings_report.md      # Earnings-specific validation
  fundamental_analyst_validate_merger_analysis.md      # M&A-specific validation

  architect_implement_security_framework.md            # Security-focused implementation
  architect_implement_performance_optimization.md      # Performance-focused implementation
```

### Role Categories
```yaml
domain_experts:
  - fundamental_analyst    # Financial analysis and valuation
  - twitter_strategist     # Social media content optimization
  - market_researcher      # Market intelligence and trends
  - content_creator        # Content generation and optimization
  - business_analyst       # Requirements and process analysis

infrastructure_roles:
  - architect             # Technical planning and implementation
  - code_owner           # Codebase health and maintenance
  - product_owner        # Product strategy and prioritization
  - security_analyst     # Security assessment and compliance
  - performance_engineer # Optimization and efficiency

workflow_coordinators:
  - command              # Meta-command management
  - orchestrator         # Multi-command workflow coordination
  - validator            # Cross-command quality assurance
  - coordinator          # Resource allocation and scheduling
```

### Action Categories
```yaml
dasv_actions:
  - discover    # Data acquisition and context gathering
  - analyze     # Systematic analysis and evaluation
  - synthesize  # Integration and recommendation generation
  - validate    # Quality assurance and confidence verification

rpiv_actions:
  - research    # Comprehensive investigation and discovery
  - plan        # Strategic planning and implementation design
  - implement   # Execution coordination and delivery
  - validate    # Verification and quality gates

tcem_actions:
  - trigger     # Event detection and workflow initiation
  - coordinate  # Resource allocation and orchestration
  - execute     # Systematic operation execution
  - monitor     # Performance tracking and optimization
```

## Command Microservice Template

### Standard Structure
```markdown
# {Role} {Action} Microservice
*{Framework} Phase {N}: {Action Description}*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - parameter_name: data_type  # description
  - context_data: object      # shared context from previous phases

optional_inputs:
  - configuration: object     # service-specific settings
  - quality_threshold: float  # minimum confidence requirement
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: structured_data
    format: json/markdown/yaml
    confidence_score: float

  metadata:
    execution_time: timestamp
    data_sources: array
    quality_metrics: object
    next_phase_ready: boolean
```

### Service Dependencies
- **Upstream Services**: [List of services this depends on]
- **Downstream Services**: [List of services that depend on this]
- **External APIs**: [List of external data sources]
- **Shared Resources**: [Team workspace, knowledge base, cache]

## Framework Implementation

### Selective Phase Execution
**Key Principle**: Not all framework phases are mandatory for every workflow. Commands can implement only the phases that add value to their specific use case.

```yaml
phase_requirements:
  mandatory_phases:
    - At least one core action phase (discover/analyze/synthesize OR research/plan/implement)
    - Validate phase (quality assurance always required)

  optional_phases:
    - Discover: Optional if data/context already available
    - Analyze: Optional if synthesis can work directly from discovery
    - Research: Optional if planning can work from existing knowledge

  selective_examples:
    twitter_strategist_workflow:
      required: [synthesize, validate]  # Skip discover/analyze for content generation
      rationale: "Content synthesis can work directly from team workspace context"

    fundamental_analyst_workflow:
      required: [discover, analyze, synthesize, validate]  # Full DASV cycle
      rationale: "Financial analysis requires systematic data gathering and analysis"

    architect_quick_fix:
      required: [implement, validate]  # Skip research/plan for minor fixes
      rationale: "Small changes don't require full planning cycle"
```

### Phase Execution Protocol
```yaml
execution_sequence:
  pre_execution:
    - Validate input requirements and phase dependencies
    - Check upstream service completion (if applicable)
    - Load shared context and configuration
    - Initialize quality monitoring

  main_execution:
    - Execute core service logic
    - Apply framework-specific methodology
    - Generate structured outputs with confidence scores
    - Maintain data/file dependency tracking

  post_execution:
    - Validate output quality against standards
    - Update shared context and dependency graph
    - Signal downstream services (if applicable)
    - Log performance metrics and artifacts
```

### Quality Assurance Standards
```yaml
quality_gates:
  input_validation:
    - Required parameters present and validated
    - Data types and formats correct
    - Confidence thresholds met
    - File dependencies accessible and current

  execution_monitoring:
    - Progress tracking with milestone checkpoints
    - Error detection and recovery protocols
    - Performance measurement and optimization
    - Data/file dependency tracking throughout execution

  output_validation:
    - Structure compliance with service specification
    - Confidence score calculation (0.0-1.0 format mandatory)
    - Cross-validation checks against quality standards
    - Output artifact generation and validation
```

## Consistent Standards Enforcement

### Data/File Dependency Standards
```yaml
dependency_specification:
  input_dependencies:
    required_files:
      - path: "absolute/path/to/file"
        type: "json|csv|md|txt"
        freshness_requirement: "24h|weekly|monthly"
        fallback_strategy: "cache|error|default"
        confidence_impact: 0.0-1.0

    required_data:
      - source: "api_name|service_name"
        endpoint: "specific_endpoint"
        parameters: {key: value}
        cache_duration: "15m|1h|24h"
        retry_policy: {attempts: 3, backoff: "exponential"}

    context_dependencies:
      - team_workspace_path: "specific/workspace/location"
        knowledge_area: "topic_name"
        minimum_confidence: 0.7
        superseding_check: true

  dependency_validation:
    pre_execution_checks:
      - Verify all required files exist and are accessible
      - Validate file freshness against requirements
      - Check data source availability and authentication
      - Confirm context dependencies are current and authoritative

    runtime_monitoring:
      - Track dependency usage and performance
      - Monitor data quality degradation
      - Log cache hits/misses and refresh operations
      - Alert on dependency failures with fallback activation
```

### Output/Generation Definition Standards
```yaml
output_specification:
  primary_outputs:
    file_generation:
      - path_pattern: "/data/outputs/{domain}/{TICKER}_{YYYYMMDD}.{ext}"
        naming_convention: "snake_case_with_timestamps"
        format_requirements: "markdown|json|csv as specified"
        content_validation: "schema_validation_required"
        confidence_integration: "mandatory_in_headers_and_metadata"

    structured_data:
      - format: "json|yaml|csv"
        schema: "predefined_json_schema_reference"
        confidence_scores: "0.0-1.0 format throughout"
        metadata_requirements: ["timestamp", "data_sources", "quality_metrics"]

    content_generation:
      - template_compliance: "consistent_formatting_required"
      - confidence_transparency: "explicit_confidence_levels_mandatory"
      - evidence_attribution: "clear_source_validation_required"
      - author_consistency: "Cole Morton attribution mandatory"

  metadata_standards:
    execution_metadata:
      - command_name: "full_microservice_name"
      - execution_timestamp: "ISO_8601_format"
      - framework_phase: "discover|analyze|synthesize|validate"
      - confidence_methodology: "detailed_confidence_calculation_explanation"
      - data_dependencies: "complete_dependency_tree_with_freshness"

    quality_metadata:
      - overall_confidence: "0.0-1.0 weighted_average"
      - data_quality_score: "0.0-1.0 source_reliability_weighted"
      - completeness_percentage: "0-100 required_data_available"
      - validation_results: "all_quality_gates_status"
      - improvement_recommendations: "specific_enhancement_suggestions"

  consistency_enforcement:
    mandatory_formats:
      - Confidence scores: "0.X/1.0 format (never X/10 or percentages)"
      - Headers: "Confidence: [X.X/1.0] | Data Quality: [X.X/1.0]"
      - Author attribution: "Cole Morton (consistent across all outputs)"
      - Risk probabilities: "0.0-1.0 decimal format in tables"
      - Monetary values: "$ symbol with appropriate formatting"
      - Date formats: "YYYYMMDD for filenames, ISO 8601 for metadata"

    template_compliance:
      - Section headers: "Consistent hierarchy and formatting"
      - Table structures: "Standardized column headers and data types"
      - Confidence integration: "Throughout analysis, not just summary"
      - Evidence backing: "Quantitative support for all assertions"
      - Cross-references: "file_path:line_number format for code references"
```


## Command.md Meta-Service Specification

### Super-Command Responsibilities
```yaml
command_lifecycle_management:
  - Service creation and optimization
  - Cross-service orchestration design
  - Performance analysis and improvement
  - Quality standardization enforcement

meta_operations:
  - analyze_service_performance
  - optimize_workflow_composition
  - create_new_service_from_template
  - validate_ecosystem_health
  - evolve_framework_patterns
```

### Meta-Service Interface
```yaml
operations:
  create_service:
    inputs: [role, action, framework, requirements]
    outputs: [service_specification, template_implementation]

  optimize_workflow:
    inputs: [current_workflow, performance_metrics, requirements]
    outputs: [optimized_composition, efficiency_improvements]

  analyze_ecosystem:
    inputs: [service_inventory, usage_patterns, quality_metrics]
    outputs: [health_report, improvement_recommendations]
```

## Implementation Roadmap

### Phase 1: Fundamental Analyst Implementation
```yaml
fundamental_analyst:
  - fundamental_analyst_discover    # DASV Phase 1: Data acquisition and context gathering
  - fundamental_analyst_analyze     # DASV Phase 2: Systematic analysis and evaluation
  - fundamental_analyst_synthesize  # DASV Phase 3: Integration and recommendation generation
  - fundamental_analyst_validate    # DASV Phase 4: Quality assurance and confidence verification

scope:
  - Only fundamental_analyst role decomposed into microservices
  - All other existing commands remain unchanged
  - Team-workspace enhanced to support both patterns
```


## Service Registry Specification

### Service Discovery
```yaml
service_registry:
  location: ./team-workspace/services/registry.json
  structure:
    services:
      - name: string
        role: string
        action: string
        framework: string
        version: string
        status: active|deprecated|development
        dependencies: array
        performance_metrics: object
        last_updated: timestamp
```

### Service Health Monitoring
```yaml
health_checks:
  availability:
    - Service responds to ping
    - Required dependencies available
    - Resource allocation sufficient

  performance:
    - Execution time within SLA
    - Confidence scores meet thresholds
    - Error rates below acceptable limits

  quality:
    - Output validation passes
    - User satisfaction scores
    - Framework compliance verification
```

## Team-Workspace Integration

### Role-to-Command Mapping

The team-workspace supports flexible role-to-command relationships where each role maps to one or many commands:

```yaml
# Phase 1: Fundamental Analyst Implementation
microservice_mapping:
  fundamental_analyst:    # One role, multiple microservices
    - fundamental_analyst_discover
    - fundamental_analyst_analyze
    - fundamental_analyst_synthesize
    - fundamental_analyst_validate

  # All other commands continue functioning as-is
  # No changes to existing commands outside fundamental_analyst role
```

### Team-Workspace Registry Enhancement

The team-workspace registry supports microservice discovery and composition:

```yaml
# Registry Structure for Phase 1
registry:
  # Role Definitions
  roles:
    fundamental_analyst:
      classification: "domain_expert"
      maps_to: "core_product"
      description: "Financial analysis and valuation expert"
      microservices: ["discover", "analyze", "synthesize", "validate"]

  # Microservice Registry (Phase 1: fundamental_analyst only)
  microservices:
    fundamental_analyst_discover:
      role: "fundamental_analyst"
      action: "discover"
      framework: "DASV"
      location: "/team-workspace/microservices/fundamental_analyst/discover.md"
      manifest: "/team-workspace/microservices/fundamental_analyst/discover.yaml"

    fundamental_analyst_analyze:
      role: "fundamental_analyst"
      action: "analyze"
      framework: "DASV"
      location: "/team-workspace/microservices/fundamental_analyst/analyze.md"
      manifest: "/team-workspace/microservices/fundamental_analyst/analyze.yaml"

    fundamental_analyst_synthesize:
      role: "fundamental_analyst"
      action: "synthesize"
      framework: "DASV"
      location: "/team-workspace/microservices/fundamental_analyst/synthesize.md"
      manifest: "/team-workspace/microservices/fundamental_analyst/synthesize.yaml"

    fundamental_analyst_validate:
      role: "fundamental_analyst"
      action: "validate"
      framework: "DASV"
      location: "/team-workspace/microservices/fundamental_analyst/validate.md"
      manifest: "/team-workspace/microservices/fundamental_analyst/validate.yaml"

  # Workflow Compositions
  workflow_compositions:
    fundamental_analysis_full:
      description: "Complete fundamental analysis workflow"
      microservices:
        - fundamental_analyst_discover
        - fundamental_analyst_analyze
        - fundamental_analyst_synthesize
        - fundamental_analyst_validate
```

### Knowledge Structure for Fundamental Analyst

The knowledge base supports microservice-level ownership for the fundamental_analyst role:

```yaml
# Knowledge Structure (Phase 1: fundamental_analyst only)
knowledge_structure:
  market-analysis:
    primary_owner: "fundamental_analyst"  # Role level
    microservice_owners:
      data_discovery: "fundamental_analyst_discover"
      financial_analysis: "fundamental_analyst_analyze"
      investment_thesis: "fundamental_analyst_synthesize"
      confidence_validation: "fundamental_analyst_validate"

  # All other knowledge topics remain unchanged
  # Existing topic ownership continues as-is for other roles
```

### Collaboration Engine Updates

The collaboration engine supports flexible role-to-command mapping:

```python
# Collaboration Engine Enhancement for Phase 1
class CollaborationEngine:
    def resolve_command(self, command_request):
        """Resolve command request to appropriate execution strategy."""

        # Check if it's a fundamental_analyst role request
        if command_request.startswith("fundamental_analyst"):
            return self.handle_fundamental_analyst_request(command_request)

        # All other commands continue as existing monolithic commands
        return self.execute_existing_command(command_request)

    def handle_fundamental_analyst_request(self, request):
        """Handle fundamental_analyst microservice requests."""
        if "_" in request:
            # Specific microservice request (e.g., "fundamental_analyst_discover")
            return self.execute_microservice(request)
        else:
            # Role-based request - compose full workflow
            workflow = [
                "fundamental_analyst_discover",
                "fundamental_analyst_analyze",
                "fundamental_analyst_synthesize",
                "fundamental_analyst_validate"
            ]
            return self.execute_microservice_workflow(workflow)
```

### Role-to-Command Relationship Benefits

The fundamental_analyst role demonstrates flexible role-to-command mapping:

```yaml
fundamental_analyst_implementation:
  role: "fundamental_analyst"
  generates_commands: 4  # discover, analyze, synthesize, validate
  phases: ["discover", "analyze", "synthesize", "validate"]
  framework: "DASV"

benefits:
  - Granular optimization per phase
  - Selective workflow composition
  - Specialized implementations per analysis phase
  - Independent scaling and caching
  - Precise dependency management

implementation_advantages:
  - Each microservice can be optimized for its specific task
  - Phases can be executed independently or as complete workflow
  - Clear separation of concerns within financial analysis
  - Flexible composition based on analysis requirements
```

### Team-Workspace Structure for Phase 1

The team-workspace adds microservice support for fundamental_analyst:

```yaml
workspace_structure:
  commands/             # Existing commands continue unchanged
    architect/
    code-owner/
    product-owner/
    business-analyst/
    twitter-post/
    # ... all other existing commands

  microservices/        # New microservice organization (Phase 1 only)
    fundamental_analyst/
      discover/
        manifest.yaml
        outputs/
        cache/
      analyze/
        manifest.yaml
        outputs/
        cache/
      synthesize/
        manifest.yaml
        outputs/
        cache/
      validate/
        manifest.yaml
        outputs/
        cache/

  workflows/            # Workflow definitions
    fundamental_analysis_full.yaml
```

## Implementation Approach

### Phase 1: Fundamental Analyst Microservices
```yaml
implementation_focus:
  scope: "fundamental_analyst role only"
  approach: "additive - existing commands unchanged"

  fundamental_analyst_decomposition:
    - Create fundamental_analyst_discover microservice
    - Create fundamental_analyst_analyze microservice
    - Create fundamental_analyst_synthesize microservice
    - Create fundamental_analyst_validate microservice

  team_workspace_updates:
    - Add microservices/ directory structure
    - Update registry for fundamental_analyst role
    - Add workflow composition support
    - Enhance collaboration engine for role routing

  existing_commands:
    status: "unchanged - continue functioning as-is"
    scope: "all commands except fundamental_analyst related"


## Success Metrics

### Performance Indicators
```yaml
efficiency_metrics:
  - Cache hit ratio: target >95%
  - API success rate: target >95%
  - Data freshness compliance: target >95%

quality_metrics:
  - Output consistency across services: target 95%
  - Confidence score reliability: target >90%
  - Data validation accuracy: target >95%
  - Template compliance: target 100%

maintainability_metrics:
  - Service isolation: complete independence
  - Clear dependency documentation: 100%
  - Standardized interfaces: fully implemented
```

## Risk Management

### Technical Risks
```yaml
complexity_management:
  risk: Increased system complexity
  mitigation: Standardized templates and clear interfaces

data_consistency:
  risk: Dependency validation failures
  mitigation: Robust validation protocols and clear fallback strategies

quality_variance:
  risk: Inconsistent outputs across services
  mitigation: Strict template enforcement and quality gates
```

### Operational Risks
```yaml
service_reliability:
  risk: Single service failure affecting workflows
  mitigation: Independent service design with clear error handling

learning_curve:
  risk: User adaptation to new command structure
  mitigation: Clear documentation and consistent patterns

quality_consistency:
  risk: Inconsistent outputs across decomposed services
  mitigation: Standardized validation and quality gates
```

---

*This specification establishes the foundation for a sophisticated, scalable AI command architecture that maintains the collaborative intelligence principles while enabling unprecedented modularity, reusability, and performance optimization.*
