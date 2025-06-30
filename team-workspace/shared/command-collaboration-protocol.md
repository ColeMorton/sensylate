# Command Collaboration Protocol

**Version**: 2.0.0
**Last Updated**: 2024-12-30
**Related**: See [Unified Pre-execution Guide](../coordination/UNIFIED_PRE_EXECUTION_GUIDE.md) for complete validation protocol
**Integration**: Part 1 of 2-step validation (Step 1: workspace validation, Step 2: content consultation)

## MANDATORY: Pre-Execution Validation

**ALL collaboration infrastructure commands MUST run workspace validation BEFORE execution to prevent the collaboration failure that occurred with P0 security configuration exposure.**

**Note**: This protocol covers **workspace state validation only**. For complete pre-execution validation, see the [Unified Pre-execution Guide](../coordination/UNIFIED_PRE_EXECUTION_GUIDE.md) which combines workspace validation with content lifecycle management.

### Required Steps for Every Command Execution

1. **Pre-Execution Validation** (MANDATORY):
   ```bash
   python3 team-workspace/shared/validate-before-execution.py <command-name>
   ```

2. **Read Current Workspace Status** (MANDATORY):
   - Check `team-workspace/commands/*/outputs/` for latest completions
   - Verify dependencies are actually complete, not just assumed
   - Read completion evidence in implementation files

3. **Update Analysis Based on Current State** (MANDATORY):
   - Modify any references to "pending" work that is actually complete
   - Acknowledge completed achievements in decision-making
   - Adjust priorities based on current reality

### Integration Points

**Product Owner Command**:
- MUST validate workspace before generating decisions
- MUST read architect/code-owner outputs first
- MUST update original priority analysis when work is complete

**Architect Command**:
- MUST update implementation status in workspace
- MUST mark phases as complete when finished
- MUST provide completion evidence

**Code Owner Command**:
- MUST update technical health assessments
- MUST reflect completed security work
- MUST maintain current system status

### Workspace Status Files

**Global Status**: `team-workspace/shared/status/global-status.yaml`
**Validation Log**: `team-workspace/shared/status/validation.log`
**Status Reports**: `team-workspace/shared/status-report.md`

### Failure Prevention

The collaboration framework failure occurred because:

1. ❌ Product-owner operated from stale analysis
2. ❌ Didn't read architect completion status
3. ❌ Treated completed work as pending
4. ❌ No automated validation of workspace state

This protocol prevents recurrence by:

1. ✅ Mandatory pre-execution validation
2. ✅ Automated status synchronization
3. ✅ Cross-command completion tracking
4. ✅ Evidence-based status verification

### Command Template Updates

All collaboration commands should include:

```
## Pre-Execution Validation
Before executing this command:
1. Run: python3 team-workspace/shared/validate-before-execution.py <command-name>
2. Review workspace status report for current completion state
3. Read latest outputs from dependent commands
4. Acknowledge any completed work in analysis
```

### Implementation

The status synchronizer automatically:
- Scans all command outputs for completion indicators
- Validates cross-command consistency
- Generates workspace status reports
- Tracks completion timeline
- Prevents collaboration failures

**This protocol is MANDATORY to maintain team workspace integrity.**
