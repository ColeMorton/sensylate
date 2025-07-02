# Unified Pre-execution Guide

**Version**: 1.0.0
**Last Updated**: 2024-12-30
**Supersedes**: Integration guide and protocol differences

## Overview

This guide establishes the **unified pre-execution protocol** that combines workspace validation and content lifecycle management into a single, comprehensive validation framework. All AI commands must follow this protocol before execution.

## Mandatory Pre-execution Requirements

**All commands** (except utilities) must complete **both validation steps** before execution:

### Step 1: Workspace State Validation
**Purpose**: Prevent operating on stale workspace data
**Mandatory for**: ALL command executions

```bash
python3 team-workspace/shared/validate-before-execution.py <command-name>
```

**What it validates**:
- Workspace data currency and freshness
- Dependency availability and status
- Cache coherence and synchronization
- Previous execution completion status

### Step 2: Content Lifecycle Consultation
**Purpose**: Prevent content duplication and conflicts
**Mandatory for**: ALL commands creating or updating content

```bash
python team-workspace/coordination/pre-execution-consultation.py <command-name> <topic> "<scope-description>"
```

**What it validates**:
- Existing content on the topic
- Topic ownership and permissions
- Content superseding requirements
- Collaboration coordination needs

## Command Classification and Requirements

### Infrastructure Commands
**Commands**: architect, code-owner, product_owner, business_analyst, command

**Requirements**:
- ✅ Workspace validation (Step 1) - MANDATORY
- ✅ Content consultation (Step 2) - MANDATORY
- ✅ Knowledge authority validation
- ✅ Topic ownership coordination

### Product Commands
**Commands**: twitter_post, fundamental_analysis_full, content_publisher, etc.

**Requirements**:
- ✅ Workspace validation (Step 1) - MANDATORY
- ✅ Content consultation (Step 2) - MANDATORY
- ⚠️ Cannot conflict with infrastructure command documentation
- ✅ Output directory validation

### Microservice Commands
**Commands**: fundamental_analyst_discover, fundamental_analyst_analyze, etc.

**Requirements**:
- ✅ Workspace validation (Step 1) - MANDATORY
- ✅ Content consultation (Step 2) - MANDATORY
- ✅ Framework phase validation
- ✅ Upstream dependency verification

### Utility Commands
**Commands**: commit_push

**Requirements**:
- ❌ Pre-execution validation - OPTIONAL
- ✅ Basic operational checks only

## Unified Pre-execution Workflow

```bash
#!/bin/bash
# Unified Pre-execution Protocol

COMMAND_NAME="$1"
TOPIC="$2"
SCOPE="$3"

echo "🔍 Starting unified pre-execution validation for: $COMMAND_NAME"

# Step 1: Workspace State Validation
echo "📊 Step 1: Validating workspace state..."
python3 team-workspace/shared/validate-before-execution.py "$COMMAND_NAME"
if [ $? -ne 0 ]; then
    echo "❌ Workspace validation failed. Fix workspace state before proceeding."
    exit 1
fi
echo "✅ Workspace state validation passed"

# Step 2: Content Lifecycle Consultation (if creating content)
if [ ! -z "$TOPIC" ]; then
    echo "📋 Step 2: Content lifecycle consultation..."
    python team-workspace/coordination/pre-execution-consultation.py "$COMMAND_NAME" "$TOPIC" "$SCOPE"
    if [ $? -ne 0 ]; then
        echo "❌ Content consultation failed. Review existing content and coordination requirements."
        exit 1
    fi
    echo "✅ Content lifecycle consultation passed"
else
    echo "⏭️ Step 2: Skipped (no content creation specified)"
fi

echo "🎯 Pre-execution validation complete. Command ready for execution."
```

## Integration Examples

### Example 1: Infrastructure Command (Architect)
```bash
# Full validation required
python3 team-workspace/shared/validate-before-execution.py architect
python team-workspace/coordination/pre-execution-consultation.py architect implementation-plans "new feature architecture"

# Proceed with architect execution
```

### Example 2: Product Command (Twitter Post)
```bash
# Full validation required
python3 team-workspace/shared/validate-before-execution.py twitter_post
python team-workspace/coordination/pre-execution-consultation.py twitter_post social-media-content "AAPL analysis post"

# Proceed with twitter_post execution
```

### Example 3: Microservice Command (Fundamental Analyst Discover)
```bash
# Full validation + framework phase verification
python3 team-workspace/shared/validate-before-execution.py fundamental_analyst_discover
python team-workspace/coordination/pre-execution-consultation.py fundamental_analyst_discover market-data "AAPL discovery phase"

# Proceed with microservice execution
```

### Example 4: Utility Command (Commit Push)
```bash
# Optional validation
git status  # Basic operational check
# Proceed with commit_push execution
```

## Validation Results and Actions

### Workspace Validation Results
- **PASS**: Workspace is current, proceed to content consultation
- **STALE**: Update workspace data, retry validation
- **DEPENDENCY_MISSING**: Install/update dependencies, retry validation
- **CONFLICT**: Resolve workspace conflicts, retry validation

### Content Consultation Results
- **PROCEED_NEW**: Create new content as planned
- **UPDATE_EXISTING**: Update existing content using superseding workflow
- **COORDINATE_OWNER**: Contact topic owner before proceeding
- **DUPLICATE_DETECTED**: Use existing content instead of creating new
- **CONFLICT_RESOLUTION**: Resolve conflicts before proceeding

## Error Handling and Recovery

### Workspace Validation Failures
1. **Check workspace synchronization**: Ensure team-workspace is current
2. **Verify dependencies**: Confirm all required tools and data are available
3. **Clear cache conflicts**: Remove stale cache entries
4. **Retry validation**: Re-run validation after fixes

### Content Consultation Failures
1. **Review existing content**: Check for similar analysis or documentation
2. **Contact topic owners**: Coordinate with knowledge authorities
3. **Use superseding workflow**: Replace existing content properly
4. **Adjust scope**: Modify analysis scope to avoid conflicts

## Enforcement Mechanisms

### Pre-commit Hooks
- Validate that commands include pre-execution calls
- Check for proper validation sequence
- Ensure both steps completed before execution

### Command File Standards
- All command files must reference this guide
- Include validation examples in command documentation
- Specify command classification and requirements

### Registry Integration
- Command registry tracks validation requirements
- Automated validation based on command classification
- Performance metrics for validation compliance

## Migration from Previous Systems

### From Integration Guide Only
- **Old**: `pre-execution-consultation.py` only
- **New**: Add `validate-before-execution.py` first
- **Impact**: More robust validation, prevents stale data issues

### From Protocol Only
- **Old**: `validate-before-execution.py` only
- **New**: Add `pre-execution-consultation.py` for content
- **Impact**: Prevents content duplication and conflicts

### Command Updates Required
- Update all command files to reference unified guide
- Add both validation steps to command workflows
- Include error handling for validation failures

## Performance Optimization

### Caching Strategy
- Cache validation results for repeated calls
- Share validation state between related commands
- Optimize validation scripts for performance

### Parallel Validation
- Run workspace validation and content consultation in parallel when possible
- Cache results to avoid repeated validation
- Batch validation for workflow executions

## Quality Assurance

### Validation Testing
- Test all validation scenarios and edge cases
- Verify error handling and recovery procedures
- Ensure validation performance meets requirements

### Documentation Consistency
- Keep this guide synchronized with implementation
- Update examples when commands change
- Maintain version control for guide updates

---

**Implementation Status**: ✅ **COMPLETED**
**Validation**: ✅ **TESTED**
**Integration**: ✅ **UNIFIED PROTOCOL ESTABLISHED**

*This unified guide eliminates the confusion between integration guide and protocol differences by establishing a single, comprehensive pre-execution validation framework.*
