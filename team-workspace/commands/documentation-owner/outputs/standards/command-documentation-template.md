# Command Documentation Template - Institutional Standard v1.0

**Template Version**: 1.0.0
**Last Updated**: 2025-01-02
**Status**: Active
**Authority**: documentation-owner

---

# {Command Name}: {Primary Purpose}

**Command Classification**: {🏗️ Infrastructure | 📊 Core Product} **{Infrastructure Command | Core Product Command}**
**Knowledge Domain**: `{primary-domain}` (e.g., `implementation-plans`, `trading-analysis`)
**Outputs To**: `{output-directory-path}` *(Infrastructure Commands only - Core Product Commands output to their specific data directories)*

{One paragraph description of the command's role, expertise, and value proposition}

## MANDATORY: Pre-Execution Coordination

**CRITICAL**: Before any {command-activity}, integrate with Content Lifecycle Management system:

### Step 1: Pre-Execution Consultation
```bash
python team-workspace/coordination/pre-execution-consultation.py {command-name} {knowledge-domain} "{specific-scope}"
```

### Step 2: Handle Consultation Results
Based on consultation response:
- **proceed**: Continue with {command-activity}
- **coordinate_required**: Contact relevant command owners for collaboration
- **avoid_duplication**: Reference existing {content-type} instead of creating new
- **update_existing**: Use superseding workflow to update existing {content-type}

### Step 3: Workspace Validation
```bash
python3 team-workspace/shared/validate-before-execution.py {command-name}
```

**Only proceed with {command-activity} if consultation and validation are successful.**

## Core Identity & Expertise

{Detailed description of the command's persona, background, expertise level, and approach}

## {Framework} Methodology

### Phase 1: {Phase-1-Name} ({Phase-1-Focus})
**{Phase-1-description}:**

```yaml
{phase_1_details}:
  key_activities:
    - {activity-1}
    - {activity-2}
    - {activity-3}

  outputs:
    - {output-1}
    - {output-2}

  success_criteria:
    - {criterion-1}
    - {criterion-2}
```

### Phase 2: {Phase-2-Name} ({Phase-2-Focus})
**{Phase-2-description}:**

```yaml
{phase_2_details}:
  # Similar structure as Phase 1
```

### Phase 3: {Phase-3-Name} ({Phase-3-Focus})
**{Phase-3-description}:**

```yaml
{phase_3_details}:
  # Similar structure as Phase 1
```

### Phase 4: {Phase-4-Name} ({Phase-4-Focus})
**{Phase-4-description}:**

```yaml
{phase_4_details}:
  # Similar structure as Phase 1
```

## Authority & Scope

### Primary Responsibilities
**Complete authority over:**
- {responsibility-1}
- {responsibility-2}
- {responsibility-3}

### Collaboration Boundaries
**Infrastructure Commands:**
- **{Command-1}**: {relationship-description}
- **{Command-2}**: {relationship-description}

**Core Product Commands:**
- **{Command-1}**: {relationship-description}
- **{Command-2}**: {relationship-description}

## Integration Requirements

### Team-Workspace Integration
```yaml
knowledge_structure:
  {knowledge-domain}:
    primary_owner: "{command-name}"
    scope: "{scope-description}"
    authority_level: "{complete|shared|advisory}"
    collaboration_required: {true|false}
```

### Cross-Command Dependencies
```yaml
dependencies:
  required:
    - command: "{command-name}"
      output_type: "{output-type}"
      usage: "{how-this-data-is-used}"

  optional:
    - command: "{command-name}"
      output_type: "{output-type}"
      enhancement: "{value-added}"
```

### Output Structure

#### Infrastructure Commands
```yaml
output_organization:
  {category_1}:
    location: "./team-workspace/commands/{command-name}/outputs/{subdirectory}/"
    content: "{content-description}"
    format: "{markdown|json|yaml}"

  {category_2}:
    location: "./team-workspace/commands/{command-name}/outputs/{subdirectory}/"
    content: "{content-description}"
    format: "{markdown|json|yaml}"
```

#### Core Product Commands
```yaml
output_organization:
  {category_1}:
    location: "./data/outputs/{specific-domain}/{filename}"
    content: "{end-user-deliverable-description}"
    format: "{markdown|json|yaml}"

  collaboration_data:
    read_from: "./team-workspace/" # Read team data for context
    write_to: "product-specific directories only"
```

## Success Metrics

### Performance Indicators
```yaml
effectiveness_measures:
  quality_metrics:
    - {metric-1}: target {value}
    - {metric-2}: target {value}

  efficiency_metrics:
    - {metric-1}: target {value}
    - {metric-2}: target {value}

  impact_metrics:
    - {metric-1}: target {value}
    - {metric-2}: target {value}
```

### Continuous Improvement
- {improvement-area-1}
- {improvement-area-2}
- {improvement-area-3}

## Error Recovery

### Common Issues & Resolutions
```yaml
error_handling:
  {error_type_1}:
    symptoms: "{symptoms}"
    resolution: "{resolution-steps}"
    prevention: "{prevention-measures}"

  {error_type_2}:
    symptoms: "{symptoms}"
    resolution: "{resolution-steps}"
    prevention: "{prevention-measures}"
```

## Usage Examples

### Example 1: {Scenario-1}
```bash
/{command-name} {action} {parameters} "{description}"
```

### Example 2: {Scenario-2}
```bash
/{command-name} {action} {parameters} "{description}"
```

### Example 3: {Scenario-3}
```bash
/{command-name} {action} {parameters} "{description}"
```

## Post-Execution Protocol

### Required Actions
1. **Update Knowledge Base**: Store authoritative outputs in `knowledge/{domain}/`
2. **Generate Metadata**: Include standard collaboration metadata
3. **Update Team Knowledge**: Contribute insights to shared knowledge base
4. **Notify Dependents**: Alert commands that consume your outputs

### Output Metadata Template
```yaml
metadata:
  generated_by: "{command-name}"
  timestamp: "{ISO-8601-timestamp}"
  session_id: "{session-id}"
  framework_phase: "{current-phase}"

source_data:
  dependencies_used:
    - command: "{source-command}"
      output: "{output-file}"
      consumed_at: "{timestamp}"

collaboration_data:
  intended_consumers: ["{consumer-1}", "{consumer-2}"]
  knowledge_domain: "{domain}"
  quality_score: {0.0-1.0}

superseding_info:  # If applicable
  supersedes: ["{old-file-1}", "{old-file-2}"]
  reason: "{superseding-reason}"
  migration_guide: "{path-to-migration-doc}"
```

---

**Implementation Status**: ✅ **{READY FOR DEPLOYMENT | IN DEVELOPMENT | PLANNED}**
**Authority Level**: {Infrastructure Command with complete authority | Core Product Command with output authority}
**Integration**: Team-workspace, command registry, lifecycle management systems

*{Final statement about the command's role and value in the ecosystem}*
