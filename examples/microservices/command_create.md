# Command Create Meta-Service
*Meta-command for intelligent command microservice creation and optimization*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - role: string               # Target role (fundamental_analyst, twitter_strategist, etc.)
  - action: string             # Framework action (discover, analyze, synthesize, validate)
  - framework: string          # Framework type (DASV, RPIV, TCEM)

optional_inputs:
  - product: string            # Optional product specification
  - complexity: string         # Simple|standard|advanced (default: standard)
  - integration_targets: array # Existing services to integrate with
  - quality_requirements: object # Specific quality and performance targets
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: command_specification
    format: markdown
    confidence_score: float
    implementation_ready: boolean

  generated_artifacts:
    - command_file: string     # Path to generated command file
    - test_specification: string # Path to validation test spec
    - integration_guide: string # Path to integration documentation

  metadata:
    execution_time: timestamp
    template_version: string
    quality_metrics: object
    optimization_recommendations: array
```

### Service Dependencies
- **Upstream Services**: None (meta-service entry point)
- **Downstream Services**: Various (depends on created command)
- **External APIs**: None required
- **Shared Resources**:
  - Template library: `/team-workspace/templates/commands/`
  - Existing commands: `/.claude/commands/`
  - Framework specifications: `/docs/`

## Data/File Dependencies

### Required Templates and Specifications
```yaml
input_dependencies:
  required_files:
    - path: "/docs/claude-command-development-framework.md"
      type: "markdown"
      freshness_requirement: "weekly"
      fallback_strategy: "error"
      confidence_impact: 0.4

    - path: "/docs/ai-command-microservices-specification.md"
      type: "markdown"
      freshness_requirement: "weekly"
      fallback_strategy: "error"
      confidence_impact: 0.4

    - path: "/team-workspace/templates/commands/"
      type: "directory"
      freshness_requirement: "monthly"
      fallback_strategy: "default_templates"
      confidence_impact: 0.2

  context_dependencies:
    - team_workspace_path: "/.claude/commands/"
      knowledge_area: "existing_commands"
      minimum_confidence: 0.8
      superseding_check: true

    - team_workspace_path: "/examples/microservices/"
      knowledge_area: "implementation_examples"
      minimum_confidence: 0.7
      superseding_check: false
```

### Dependency Validation Protocol
```yaml
pre_execution_checks:
  - Verify framework documentation is current
  - Check template library completeness
  - Validate existing command compatibility
  - Confirm naming convention compliance

runtime_monitoring:
  - Track template usage and effectiveness
  - Monitor command generation quality
  - Log integration complexity metrics
  - Alert on template versioning issues
```

## Framework Implementation

### Command Creation Methodology
```yaml
execution_sequence:
  pre_creation:
    - Analyze role and action requirements
    - Identify framework-specific patterns
    - Load appropriate templates and examples
    - Validate naming convention and uniqueness

  main_creation:
    - Generate core command structure
    - Implement framework-specific logic
    - Apply consistent standards and formatting
    - Create dependency specifications
    - Generate output/validation requirements

  post_creation:
    - Validate generated command compliance
    - Create integration documentation
    - Generate test specifications
    - Optimize for performance and quality
```

### Quality Assurance Gates
```yaml
command_validation:
  structure_compliance:
    - Follows microservices specification
    - Implements required framework phases
    - Includes proper dependency definitions
    - Contains complete output specifications

  standards_enforcement:
    - Consistent confidence score formatting
    - Proper file dependency declarations
    - Standardized metadata requirements
    - Template compliance verification

  integration_readiness:
    - Compatible with existing ecosystem
    - Clear upstream/downstream interfaces
    - Proper error handling and fallbacks
    - Performance optimization implemented
```

## Command Generation Templates

### Framework-Specific Templates
```yaml
template_library:
  dasv_template:
    discover_phase:
      - Data acquisition patterns
      - Cache integration strategies
      - Quality validation frameworks
      - Parallel processing optimization

    analyze_phase:
      - Systematic analysis methodologies
      - Cross-validation techniques
      - Confidence scoring algorithms
      - Evidence attribution systems

    synthesize_phase:
      - Integration and recommendation logic
      - Template-driven output generation
      - Multi-scenario modeling
      - Risk assessment integration

    validate_phase:
      - Quality assurance protocols
      - Output compliance verification
      - Performance measurement
      - Continuous improvement feedback

  rpiv_template:
    research_phase:
      - Comprehensive discovery patterns
      - Context gathering strategies
      - Evidence validation methods
      - Knowledge synthesis techniques

    plan_phase:
      - Strategic planning frameworks
      - Dependency mapping systems
      - Risk assessment protocols
      - Implementation roadmaps

    implement_phase:
      - Execution coordination patterns
      - Quality gate enforcement
      - Progress monitoring systems
      - Adaptive response mechanisms

    validate_phase:
      - Verification methodologies
      - Success measurement criteria
      - Optimization identification
      - Learning integration protocols
```

### Generated Command Structure
```markdown
# {Role} {Action} {Product} Microservice
*{Framework} Phase {N}: {Action Description}*

## Service Specification
[Generated based on role, action, and framework requirements]

### Input Interface
[Dynamically generated based on framework phase and role requirements]

### Output Interface
[Framework-specific output structure with confidence integration]

### Service Dependencies
[Intelligent dependency mapping based on ecosystem analysis]

## Data/File Dependencies
[Comprehensive dependency specification following standards]

### Required Files/Data
[Generated based on role requirements and framework needs]

### Dependency Validation Protocol
[Standard validation with role-specific customizations]

## Framework Implementation
[Framework-specific implementation with quality gates]

## Output/Generation Standards
[Consistent formatting with role-specific requirements]

## Performance Optimization
[Role and complexity-appropriate optimization strategies]

## Success Metrics
[Framework-aligned KPIs with role-specific targets]
```

## Intelligent Template Selection

### Role-Based Customization
```yaml
role_templates:
  fundamental_analyst:
    specializations:
      - Financial data integration patterns
      - Valuation methodology frameworks
      - Risk assessment templates
      - Peer comparison systems

    output_formats:
      - Structured financial analysis
      - Investment recommendation formats
      - Confidence-weighted scenarios
      - Evidence-backed conclusions

  twitter_strategist:
    specializations:
      - Content optimization patterns
      - Engagement prediction models
      - Platform compliance templates
      - Brand voice consistency

    output_formats:
      - Social media post structures
      - Engagement metric predictions
      - Content validation criteria
      - Multi-platform adaptations
```

### Product-Specific Enhancements
```yaml
product_customizations:
  trading_strategy:
    enhancements:
      - Technical analysis integration
      - Risk disclosure requirements
      - Market timing considerations
      - Position sizing frameworks

  fundamental_analysis:
    enhancements:
      - DCF modeling templates
      - Competitive analysis frameworks
      - Industry context integration
      - Long-term value assessment
```

## Output/Generation Standards

### Command File Generation
```yaml
output_specification:
  file_generation:
    - path_pattern: "/.claude/commands/{role}_{action}_{product}.md"
    - naming_convention: "microservice_naming_standard"
    - format_requirements: "full_microservice_specification"
    - content_validation: "framework_compliance_schema"
    - confidence_integration: "throughout_specification"

  supporting_artifacts:
    - test_specification: "/tests/commands/{role}_{action}_{product}_test.md"
    - integration_guide: "/docs/integration/{role}_{action}_{product}_integration.md"
    - performance_profile: "/team-workspace/performance/{role}_{action}_{product}_profile.json"
```

### Quality Metadata
```yaml
generated_command_metadata:
  creation_details:
    - generator_version: "command_create_v1.0"
    - template_version: "microservices_v2.1"
    - framework_compliance: "100%"
    - estimated_performance: "optimized"

  integration_metadata:
    - ecosystem_compatibility: "full"
    - dependency_complexity: "low|medium|high"
    - maintenance_requirements: "standard|enhanced"
    - optimization_opportunities: [....]
```

## Success Metrics

### Creation Quality
```yaml
microservice_kpis:
  generation_performance:
    - Command creation time: target <120 seconds
    - Template application accuracy: target >95%
    - Framework compliance: target 100%
    - Integration readiness: target >90%

  output_quality:
    - Generated command usability: target >90%
    - First-run success rate: target >85%
    - Template effectiveness: target >80%
    - User satisfaction: target >85%

  ecosystem_impact:
    - Integration complexity reduction: target 40%
    - Development time savings: target 60%
    - Quality consistency improvement: target 30%
    - Maintenance overhead reduction: target 50%
```

---

*This meta-service demonstrates the sophisticated command creation capabilities with intelligent template selection, framework compliance, and ecosystem integration optimization.*
