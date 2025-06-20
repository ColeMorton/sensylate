# Create Command

Interactive command creator for Claude Code with systematic validation and best practices.

## MANDATORY: Pre-Execution Coordination

**CRITICAL**: Before creating any new commands, you MUST integrate with the Content Lifecycle Management system to prevent duplication and maintain knowledge integrity.

### Step 1: Pre-Execution Consultation
```bash
python team-workspace/coordination/pre-execution-consultation.py create-command command-creation "{command-name-and-purpose}"
```

### Step 2: Handle Consultation Results
Based on consultation response:
- **proceed**: Continue with command creation
- **coordinate_required**: Contact existing command owners for coordination or enhancement
- **avoid_duplication**: Reference existing similar command instead of creating new one
- **update_existing**: Use superseding workflow to enhance existing command

### Step 3: Workspace Validation
```bash
python team-workspace/coordination/validate-before-execution.py create-command
```

**Only proceed with command creation if consultation and validation are successful.**

## Purpose

Creates well-structured commands following established patterns with built-in validation and optimization guidance.

## Workflow

### Step 1: Command Definition
**Required Information:**
- **Name**: lowercase, descriptive, unique (validate against existing)
- **Category**: workflow | automation | analysis | utility
- **Objective**: specific problem solved (1-2 sentences)
- **Success criteria**: measurable outcomes

### Step 2: Structure Design
**Core Components:**
- **Prerequisites**: dependencies, setup requirements
- **Parameters**: inputs with types and validation
- **Process steps**: sequential actions with decision points
- **Outputs**: expected results and formats
- **Error handling**: failure modes and recovery

### Step 3: Content Generation
**Template Application:**
```markdown
# [Command Name]

[One-line description]

## Purpose
[Problem solved and when to use - 2-3 sentences]

## Parameters
- `param`: description (type, required/optional, default)

## Process
1. **[Action]**: [specific steps]
2. **[Validation]**: [check criteria]
3. **[Output]**: [deliverable format]

## Usage
```
/project:[command-name] [parameters]
```

## Notes
- [Critical considerations]
- [Limitations or warnings]
```

### Step 4: Quality Assurance
**Validation Checklist:**
- [ ] Name follows conventions and is unique
- [ ] Purpose clearly states value proposition
- [ ] Steps are actionable and measurable
- [ ] Parameters are well-defined
- [ ] Examples demonstrate usage
- [ ] Error cases are addressed

### Step 5: Implementation
- Write to `.claude/commands/[name].md`
- Test with sample parameters
- Document in command registry

## Command Categories

**Workflow**: Multi-step processes with decision points
**Automation**: Repeatable tasks requiring minimal input
**Analysis**: Research, investigation, and reporting tasks
**Utility**: Specific tools for common operations

## Quality Standards

**Clarity**: Each step has clear success criteria
**Completeness**: All necessary information included
**Consistency**: Follows established patterns
**Actionability**: Instructions are executable
**Robustness**: Handles edge cases and errors

## Validation Rules

1. **Naming**: `[a-z0-9_-]+` pattern, max 20 chars
2. **Structure**: Required sections present and complete
3. **Content**: Specific, actionable instructions
4. **Examples**: Realistic usage scenarios included
5. **Testing**: Command works as documented

## Usage

```
/project:create_command
```

Starts interactive command creation session with systematic guidance and validation.

## MANDATORY: Post-Execution Lifecycle Management

After creating any new command, you MUST complete these lifecycle management steps:

### Step 1: Content Authority Establishment
```bash
python team-workspace/coordination/topic-ownership-manager.py claim command-creation create-command "New command: {command-name}"
```

### Step 2: Registry Update
Update topic registry with new command creation:
- Authority file: `team-workspace/knowledge/commands/{command-name}.md`
- Update `coordination/topic-registry.yaml` with new command entry
- Set create-command as primary owner for command creation topics

### Step 3: Cross-Command Integration Check
Ensure new command integrates with lifecycle management:
- Add pre-execution coordination sections if command creates content
- Include post-execution lifecycle management if command produces outputs
- Validate command follows team-workspace authority patterns

### Step 4: Command Registry Update
Update command registry and documentation:
- Add command to `.claude/commands/` directory
- Update CLAUDE.md with new command documentation
- Ensure command follows integration patterns

## Best Practices

- Start with user need, not technical capability
- Use action verbs for clarity
- Include realistic examples
- Plan for failure scenarios
- Test before deployment
- Document assumptions and limitations
- **Authority Integration**: Ensure new commands integrate with lifecycle management system
