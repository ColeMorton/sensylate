# Command Scope Management Guide

## Overview

The Command Collaboration Framework supports two scopes of commands:

- **User Commands**: Global commands available across all projects (`/Users/colemorton/.claude/commands/`)
- **Project Commands**: Project-specific commands for this project (`/Users/colemorton/Projects/sensylate/.claude/commands/`)

## Command Resolution Order

The framework resolves commands with the following precedence:

1. **Project Commands First**: Check `/Users/colemorton/Projects/sensylate/.claude/commands/`
2. **User Commands Second**: Check `/Users/colemorton/.claude/commands/`
3. **Registry Fallback**: Use original location from registry

This allows project-specific commands to override user commands when needed.

## Scope Examples

### User-Scoped Commands (Global)

These commands are available across all your projects:

```yaml
# Registry entry for user command
architect:
  location: "/Users/colemorton/.claude/commands/architect.md"
  scope: "user"
  description: "Technical planning framework - available globally"

product-owner:
  location: "/Users/colemorton/.claude/commands/product_owner.md"
  scope: "user"
  description: "Business prioritization - available globally"
```

**Typical User Commands**:
- `architect` - Technical planning framework
- `product-owner` - Business prioritization and decision-making
- `code-owner` - Codebase health analysis
- `business-analyst` - Requirements gathering
- `twitter-post` - Social media content optimization
- `commit-push` - Automated git workflow
- `create-command` - Command creation utility

### Project-Scoped Commands

These commands are specific to the sensylate project:

```yaml
# Registry entry for project command  
sensylate-data-analyzer:
  location: "/Users/colemorton/Projects/sensylate/.claude/commands/sensylate-data-analyzer.md"
  scope: "project"
  description: "Sensylate-specific trading data analysis"

sensylate-report-generator:
  location: "/Users/colemorton/Projects/sensylate/.claude/commands/sensylate-report-generator.md"
  scope: "project"
  description: "Generate sensylate-specific trading reports"
```

**Typical Project Commands**:
- Domain-specific analyzers
- Project-specific report generators
- Custom workflow commands
- Integration-specific utilities

## Command Overrides

Project commands can override user commands by using the same name:

```bash
# User command (global)
/Users/colemorton/.claude/commands/data-processor.md

# Project override (takes precedence)
/Users/colemorton/Projects/sensylate/.claude/commands/data-processor.md
```

When `data-processor` is executed, the project version will be used instead of the user version.

## Directory Structure

```
Commands Organization:
├── /Users/colemorton/.claude/commands/          # User-global commands
│   ├── architect.md                             # Available in all projects
│   ├── product_owner.md                         # Available in all projects
│   ├── business_analyst.md                      # Available in all projects
│   └── ...
│
└── /Users/colemorton/Projects/sensylate/.claude/commands/  # Project-specific
    ├── sensylate-analyzer.md                   # Only in sensylate project
    ├── trading-strategy-optimizer.md           # Only in sensylate project
    └── data-processor.md                       # Overrides user version
```

## Best Practices

### When to Use User Commands

- **Cross-project utility**: Commands useful across multiple projects
- **General frameworks**: Architecture, planning, and business analysis
- **Development tools**: Git workflows, code analysis, documentation
- **Content creation**: Social media, general writing assistance

### When to Use Project Commands

- **Domain-specific logic**: Trading analysis, financial calculations
- **Project-specific integrations**: Custom APIs, databases, services
- **Specialized workflows**: Project-unique processes
- **Data formats**: Project-specific data structures and formats

### Command Naming Conventions

```bash
# User commands: Generic, reusable names
architect.md
product-owner.md
code-analyzer.md

# Project commands: Project-prefixed or domain-specific
sensylate-trading-analyzer.md
sensylate-backtest-generator.md
financial-risk-calculator.md
```

### Migration Strategy

To migrate from user to project command:

1. **Copy user command to project directory**:
```bash
cp /Users/colemorton/.claude/commands/my-command.md \
   /Users/colemorton/Projects/sensylate/.claude/commands/my-command.md
```

2. **Customize for project needs**:
```markdown
# Add project-specific context, data sources, or logic
```

3. **Update registry**:
```yaml
my-command:
  location: "/Users/colemorton/Projects/sensylate/.claude/commands/my-command.md"
  scope: "project"  # Changed from "user"
```

4. **Test execution**: Verify project version is used

## Command Discovery Process

The Collaboration Engine follows this discovery process:

```python
def discover_command(command_name):
    # 1. Check project commands first
    project_file = f"/Users/colemorton/Projects/sensylate/.claude/commands/{command_name}.md"
    if exists(project_file):
        return load_command(project_file, scope="project")
    
    # 2. Check user commands second
    user_file = f"/Users/colemorton/.claude/commands/{command_name}.md"
    if exists(user_file):
        return load_command(user_file, scope="user")
    
    # 3. Use registry location as fallback
    registry_location = get_registry_location(command_name)
    if exists(registry_location):
        return load_command(registry_location, scope="registry")
    
    # 4. Command not found
    return None
```

## Collaboration Implications

### Cross-Scope Dependencies

Project commands can depend on user commands and vice versa:

```yaml
# Project command depending on user command
sensylate-analyzer:
  dependencies:
    optional:
      - command: "architect"        # User command
        scope: "user"
        enhancement: "Incorporates technical architecture"

# User command enhanced by project data
architect:
  dependencies:
    optional:
      - command: "sensylate-analyzer"  # Project command
        scope: "project"
        enhancement: "Uses domain-specific analysis"
```

### Workspace Isolation

Each project maintains its own team workspace while sharing user commands:

```
Project A:
├── team-workspace-a/     # Project A's collaboration data
└── .claude/commands/     # Project A's specific commands

Project B:  
├── team-workspace-b/     # Project B's collaboration data
└── .claude/commands/     # Project B's specific commands

User Commands:
└── /Users/colemorton/.claude/commands/  # Shared across all projects
```

## Troubleshooting

### Command Not Found

```bash
# Check if command exists in expected locations
ls /Users/colemorton/Projects/sensylate/.claude/commands/my-command.md
ls /Users/colemorton/.claude/commands/my-command.md

# Check registry entry
grep -A 5 "my-command:" team-workspace/commands/registry.yaml
```

### Wrong Command Version Executed

```bash
# Verify resolution order
python team-workspace/shared/collaboration-engine.py discover my-command

# Check for project override
ls /Users/colemorton/Projects/sensylate/.claude/commands/
```

### Scope Conflicts

```bash
# List all commands by scope
grep -A 2 "scope:" team-workspace/commands/registry.yaml
```

This dual-scope system provides maximum flexibility while maintaining clear separation between global utilities and project-specific functionality.