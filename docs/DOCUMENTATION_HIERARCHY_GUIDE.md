# Documentation Hierarchy Guide

**Version**: 1.0.0
**Last Updated**: 2024-12-30
**Purpose**: Establish clear precedence order for documentation conflicts

## Documentation Precedence Order

When documentation conflicts arise, follow this hierarchy (highest to lowest authority):

### 1. **Individual Command Files** (Authoritative)
- **Location**: `.claude/commands/*.md`
- **Authority**: Primary source of truth for command behavior
- **Scope**: Command-specific functionality and requirements
- **Examples**: `architect.md`, `twitter_post.md`, `fundamental_analyst_discover.md`
- **Update Frequency**: When command logic changes

### 2. **Framework Documentation** (Methodology Definitions)
- **Location**: `docs/ai-command-microservices-specification.md`, `docs/claude-command-development-framework.md`
- **Authority**: Framework patterns, methodologies (RPIV, DASV, TCEM), and architectural principles
- **Scope**: Cross-command standards and patterns
- **Examples**: DASV framework definition, microservice templates, quality standards
- **Update Frequency**: When framework evolves

### 3. **Integration Guides** (Operational Procedures)
- **Location**: `docs/coordination/*.md`, `docs/shared/*.md`
- **Authority**: Process and integration requirements
- **Scope**: How commands work together and validation requirements
- **Examples**: `UNIFIED_PRE_EXECUTION_GUIDE.md`, `INTEGRATION_GUIDE.md`, `command-collaboration-protocol.md`
- **Update Frequency**: When integration patterns change

### 4. **CLAUDE.md** (Project Overview)
- **Location**: Root directory `CLAUDE.md`
- **Authority**: Project-wide guidance and command summaries
- **Scope**: High-level overview and coordination between systems
- **Examples**: Command locations, workflow examples, memory guidance
- **Update Frequency**: When project structure changes

### 5. **README Files** (Introductory Material)
- **Location**: Various directories (`README.md`, `docs/README.md`)
- **Authority**: Getting started information and context
- **Scope**: Introduction to concepts and quick start guides
- **Examples**: Project overview, system introduction
- **Update Frequency**: When onboarding process changes

## Conflict Resolution Process

### When Documentation Conflicts Occur:

1. **Identify Sources**: Determine which documents contain conflicting information
2. **Apply Hierarchy**: Higher-numbered sources take precedence
3. **Update Lower Sources**: Align lower-precedence documents with authoritative source
4. **Add References**: Include cross-references to maintain consistency

### Example Conflict Resolution:

**Scenario**: Command summary in CLAUDE.md differs from actual command file

**Resolution**:
1. Command file (level 1) is authoritative
2. Update CLAUDE.md (level 4) to match command file
3. Add reference in CLAUDE.md pointing to command file for details

## Documentation Maintenance

### Version Control
- Each document should include version number and last updated date
- Track breaking changes that affect other documents
- Maintain compatibility between levels

### Update Triggers
- **Command Files**: When functionality changes
- **Framework Docs**: When patterns evolve
- **Integration Guides**: When processes change
- **CLAUDE.md**: When summaries drift from source
- **READMEs**: When onboarding needs update

### Cross-Reference Standards
- Always reference higher-authority sources
- Use relative paths for internal links
- Include version references for breaking changes
- Mark deprecated information clearly

## Authority Delegation

### Command-Specific Authority
Individual command files have complete authority over:
- Command behavior and logic
- Input/output specifications
- Framework implementation details
- Error handling procedures
- Performance characteristics

### Framework Authority
Framework documentation has complete authority over:
- Methodology definitions (RPIV, DASV, TCEM)
- Cross-command standards
- Quality requirements
- Template structures
- Naming conventions

### Integration Authority
Integration guides have complete authority over:
- Pre-execution requirements
- Validation procedures
- Collaboration protocols
- Workflow coordination
- Data sharing standards

## Documentation Quality Standards

### Consistency Requirements
- Follow established terminology
- Use consistent formatting
- Maintain version headers
- Include clear scope definitions
- Reference authoritative sources

### Update Responsibilities
- **Command Authors**: Keep command files current
- **Framework Architects**: Maintain framework documentation
- **Integration Leads**: Update coordination guides
- **Project Maintainers**: Keep CLAUDE.md synchronized
- **Contributors**: Update READMEs for clarity

### Validation Process
- Check hierarchy compliance before updates
- Verify cross-references remain valid
- Test examples and code snippets
- Ensure breaking changes are documented
- Validate consistency across levels

## Special Cases

### Emergency Updates
In critical situations (security, system failures):
1. Update authoritative source immediately
2. Mark temporary inconsistencies clearly
3. Schedule hierarchical updates within 24 hours
4. Document the emergency update process

### Deprecated Documentation
When documents become obsolete:
1. Add clear deprecation notices
2. Point to replacement documentation
3. Set removal timeline
4. Update all cross-references

### Multi-System Integration
When documentation spans multiple systems:
1. Establish clear ownership boundaries
2. Define integration points explicitly
3. Maintain consistent interfaces
4. Document external dependencies

---

**Implementation Status**: ✅ **ESTABLISHED**
**Next Review**: 2025-03-30
**Compliance**: All documentation should follow this hierarchy

*This guide ensures consistent, authoritative documentation throughout the Sensylate AI Command ecosystem.*
