# Command Collaboration Framework

## Executive Summary

```xml
<summary>
  <objective>Establish standardized inter-command communication protocol for collaborative workflow automation</objective>
  <approach>Shared data storage, standardized metadata schema, dependency resolution, and discovery system</approach>
  <value>Transform isolated command execution into coordinated team collaboration with data flow visibility</value>
</summary>
```

## Framework Architecture

### Core Components

1. **Shared Data Storage** (`/team-workspace/`)
2. **Metadata Schema** (`.command-meta.yaml`)
3. **Dependency Resolution** (command manifests)
4. **Discovery System** (registry + validation)

### Data Flow Model

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Data    │───▶│  Command Agent  │───▶│   Output Data   │
│   Dependencies  │    │   (Individual)  │    │   + Metadata    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       │                       │
         │                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Dependency      │    │ Collaboration   │    │ Team Workspace  │
│ Resolution      │    │ Orchestrator    │    │ (Shared Data)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Shared Data Storage Structure

```
/team-workspace/
├── commands/                    # Command registry and manifests
│   ├── registry.yaml           # Master command catalog
│   ├── architect/              # Command-specific data
│   │   ├── manifest.yaml      # Dependencies, outputs, metadata
│   │   ├── outputs/           # Generated deliverables
│   │   └── cache/            # Performance optimization
│   ├── product-owner/
│   ├── code-owner/
│   ├── business-analyst/
│   └── ...
├── shared/                     # Cross-command shared data
│   ├── project-context.yaml   # Current project state
│   ├── team-knowledge.yaml    # Accumulated insights
│   └── workflow-state.yaml    # Active workflow tracking
└── sessions/                   # Execution session logs
    └── YYYY-MM-DD_HH-MM-SS/   # Timestamped session data
        ├── execution-log.yaml
        └── command-outputs/
```

## Standardized Metadata Schema

### Command Manifest Structure

```yaml
# /team-workspace/commands/architect/manifest.yaml
command:
  name: "architect"
  version: "1.0.0"
  type: "framework"                    # framework|tool|analyzer|generator
  description: "Technical planning & implementation framework"
  
capabilities:
  reads:
    - codebase_structure
    - git_status
    - dependency_files
    - project_documentation
  produces:
    - implementation_plans
    - phase_summaries
    - technical_specifications
  
dependencies:
  required: []                         # Must have these command outputs
  optional:                           # Enhanced functionality with these
    - "code-owner.technical_health"
    - "business-analyst.requirements"
  conflicts: []                       # Cannot run with these
  
data_schema:
  inputs:
    project_context:
      type: "object"
      required: true
      schema: "project-context.schema.yaml"
  outputs:
    implementation_plan:
      type: "markdown"
      location: "/team-workspace/commands/architect/outputs/"
      format: "phase-based-plan"
      metadata_required: true
      
collaboration:
  consumption_pattern: "research-driven"
  output_sharing: "immediate"
  cache_strategy: "session-based"
  notification_events:
    - "plan_phase_completed"
    - "risk_identified"
    - "dependency_blocked"
```

### Output Metadata Standard

```yaml
# .command-meta.yaml (accompanies every output file)
metadata:
  generated_by: "architect"
  version: "1.0.0"
  timestamp: "2025-01-07T15:30:00Z"
  session_id: "2025-01-07_15-28-45"
  
source_data:
  dependencies:
    - command: "code-owner"
      output: "technical_health_matrix"
      version: "1.2.0"
      consumed_at: "2025-01-07T15:29:15Z"
  project_context:
    git_commit: "2dc8135"
    files_analyzed: 47
    
output_specification:
  type: "implementation_plan"
  format: "markdown"
  confidence_level: 0.92
  completeness: "full"
  
collaboration_data:
  intended_consumers:
    - "product-owner"
    - "business-analyst"
  notification_sent: true
  cache_expires: "2025-01-08T15:30:00Z"
  
quality_metrics:
  validation_passed: true
  review_required: false
  approval_status: "auto-approved"
```

## Command Discovery & Dependency Resolution

### Registry Management

```yaml
# /team-workspace/commands/registry.yaml
commands:
  architect:
    location: "/Users/colemorton/.claude/commands/architect.md"
    manifest: "/team-workspace/commands/architect/manifest.yaml"
    status: "active"
    last_execution: "2025-01-07T15:30:00Z"
    performance_metrics:
      avg_execution_time: "45s"
      success_rate: 0.96
      
  product-owner:
    location: "/Users/colemorton/.claude/commands/product_owner.md"
    manifest: "/team-workspace/commands/product-owner/manifest.yaml"
    status: "active"
    dependencies_on: ["architect", "business-analyst"]
    
workflow_patterns:
  analysis_chain:
    sequence: ["code-owner", "product-owner", "architect"]
    description: "Technical analysis → Business prioritization → Implementation"
    success_rate: 0.89
    
  content_creation:
    parallel: ["twitter-post", "twitter-post-strategy"]
    trigger: "trading_analysis_complete"
```

### Dependency Resolution Algorithm

```python
def resolve_command_dependencies(command_name, available_data):
    """
    1. Load command manifest
    2. Check required dependencies
    3. Validate optional dependencies
    4. Resolve conflicts
    5. Return execution plan with data sources
    """
    manifest = load_manifest(command_name)
    
    # Check required dependencies
    for dep in manifest.dependencies.required:
        if not is_available(dep, available_data):
            suggest_dependency_command(dep)
            
    # Optimize with optional dependencies
    optimization_data = {}
    for opt_dep in manifest.dependencies.optional:
        if is_available(opt_dep, available_data):
            optimization_data[opt_dep] = load_dependency_data(opt_dep)
            
    return ExecutionPlan(
        command=command_name,
        required_data=resolve_required_data(manifest),
        optimization_data=optimization_data,
        estimated_duration=calculate_duration(manifest, optimization_data)
    )
```

## Team Collaboration Protocols

### Data Sharing Standards

1. **Immediate Sharing**: Critical outputs (risks, blockers) shared immediately
2. **Session Sharing**: Standard outputs shared at session completion
3. **Cached Sharing**: Expensive computations cached with expiration
4. **Versioned Sharing**: All outputs versioned for dependency tracking

### Consumption Patterns

```yaml
command_behaviors:
  research_driven:
    commands: ["architect", "code-owner"]
    behavior: "Read all available team data before generating new content"
    
  context_aware:
    commands: ["product-owner", "business-analyst"]
    behavior: "Consume specific dependency outputs and project context"
    
  transform_focused:
    commands: ["twitter-post", "commit-push"]
    behavior: "Process provided inputs with minimal external dependencies"
```

### Workflow Orchestration

```yaml
# /team-workspace/shared/workflow-state.yaml
active_workflows:
  - id: "project_health_assessment"
    initiated_by: "user"
    started_at: "2025-01-07T15:00:00Z"
    sequence:
      - command: "code-owner"
        status: "completed"
        output: "/team-workspace/commands/code-owner/outputs/health-assessment-2025-01-07.md"
      - command: "product-owner"
        status: "in_progress"
        depends_on: ["code-owner"]
        estimated_completion: "2025-01-07T15:45:00Z"
      - command: "architect"
        status: "pending"
        depends_on: ["product-owner"]
        
notifications:
  - event: "dependency_available"
    target_command: "product-owner"
    message: "code-owner health assessment completed"
    timestamp: "2025-01-07T15:30:00Z"
```

## Implementation Protocol

### Pre-Execution (Every Command)

```python
def pre_execution_protocol(command_name):
    """Standard protocol executed before any command"""
    
    # 1. Register command execution
    register_execution_session(command_name)
    
    # 2. Load team workspace context
    project_context = load_shared_context()
    available_data = scan_team_workspace()
    
    # 3. Resolve dependencies
    execution_plan = resolve_dependencies(command_name, available_data)
    
    # 4. Load relevant team knowledge
    relevant_outputs = find_relevant_team_outputs(command_name, project_context)
    
    # 5. Prepare enhanced context
    enhanced_context = merge_contexts(
        project_context,
        relevant_outputs,
        execution_plan.optimization_data
    )
    
    return enhanced_context
```

### Post-Execution (Every Command)

```python
def post_execution_protocol(command_name, outputs):
    """Standard protocol executed after any command"""
    
    # 1. Generate metadata
    metadata = generate_output_metadata(command_name, outputs)
    
    # 2. Store outputs with metadata
    store_command_outputs(command_name, outputs, metadata)
    
    # 3. Update team workspace
    update_project_context(outputs)
    update_team_knowledge(command_name, outputs)
    
    # 4. Notify dependent commands
    notify_dependent_commands(command_name, outputs)
    
    # 5. Update workflow state
    update_workflow_progress(command_name, "completed")
    
    # 6. Cache optimization data
    cache_performance_data(command_name, execution_metrics)
```

## Quality Gates & Validation

### Data Validation Standards

```yaml
validation_rules:
  metadata_completeness:
    required_fields: ["generated_by", "timestamp", "source_data", "output_specification"]
    
  dependency_integrity:
    check_dependency_versions: true
    validate_dependency_freshness: "24h"
    require_source_traceability: true
    
  output_quality:
    schema_validation: true
    format_compliance: true
    completeness_check: true
```

### Cross-Command Consistency

```yaml
consistency_checks:
  naming_conventions:
    file_naming: "snake_case"
    command_naming: "kebab-case"
    variable_naming: "snake_case"
    
  documentation_standards:
    metadata_required: true
    source_attribution: true
    version_tracking: true
    
  workflow_compliance:
    dependency_declaration: true
    output_registration: true
    notification_protocol: true
```

## Usage Examples

### Example 1: Coordinated Analysis Workflow

```bash
# User initiates comprehensive project analysis
> "Run code analysis and create implementation plan"

# Framework execution:
1. code-owner: Generates technical health assessment
2. product-owner: Consumes code-owner output, creates business prioritization
3. architect: Consumes both outputs, creates implementation plan

# Result: Coordinated, data-driven implementation plan
```

### Example 2: Context-Aware Content Creation

```bash
# User requests social media content
> "Create twitter post about our trading strategy"

# Framework execution:
1. twitter-post-strategy: Checks team workspace for recent trading analysis
2. Finds: /team-workspace/outputs/trading-analysis-2025-01-07.md
3. Generates: Context-aware trading strategy post using existing data
```

### Example 3: Dependency-Driven Enhancement

```bash
# User runs architect command
> "/architect - implement user authentication system"

# Framework execution:
1. Checks dependencies: Finds recent business-analyst requirements
2. Loads: User story specifications, acceptance criteria
3. Enhances: Implementation plan with business context
4. Generates: Comprehensive plan aligned with business requirements
```

---

**Implementation Status**: Framework designed and ready for implementation. This creates a foundation for commands to collaborate as team members while maintaining individual autonomy and specialized functionality.