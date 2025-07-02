# Core Product Command Integration Clarification

**Document Type**: Standards Clarification
**Generated**: 2025-01-02
**Authority**: documentation-owner
**Reference**: Original audit findings correction

---

## Key Clarifications

### 1. Service Reference Updates
**Correction**: `yahoo_finance_bridge.py` → `yahoo_finance_service.py`
- System was renamed, not removed
- Method calls: `bridge.*` → `service.*`
- API functionality remains similar

### 2. Core Product Command Output Policy
**Critical Clarification**: Core Product Commands do NOT output to team-workspace directories

#### Correct Output Pattern:
```yaml
Core Product Commands:
  read_from: "./team-workspace/"  # Use team data for context
  write_to: "./data/outputs/{domain}/"  # Product-specific outputs
  examples:
    - fundamental_analysis_full → ./data/outputs/fundamental_analysis/
    - twitter_post_strategy → ./data/outputs/twitter_strategy/
    - trade_history → ./data/outputs/trade_history/

Infrastructure Commands:
  read_from: "./team-workspace/"  # Use team data for context
  write_to: "./team-workspace/commands/{command}/outputs/"  # Team collaboration
```

### 3. Lifecycle Integration Requirements

#### For Core Product Commands:
```markdown
## MANDATORY: Pre-Execution Coordination
- Pre-execution consultation (READ from team-workspace)
- Workspace validation
- Context enhancement from team data

## Post-Execution Protocol
- Generate output metadata
- Store in product-specific directories (NOT team-workspace)
- Update quality metrics
- NO team knowledge contribution (they create end-user products)
```

#### For Infrastructure Commands:
```markdown
## MANDATORY: Pre-Execution Coordination
- Pre-execution consultation
- Workspace validation
- Context enhancement from team data

## Post-Execution Protocol
- Generate output metadata
- Store in team-workspace/commands/{command}/outputs/
- Update team knowledge base
- Notify dependent commands
```

## Updated Template Requirements

### Core Product Commands
- **Input Integration**: MUST read team-workspace for context
- **Output Separation**: MUST write to product-specific directories
- **Lifecycle Integration**: Pre-execution coordination only
- **Knowledge Contribution**: Minimal (they are end products, not collaboration tools)

### Infrastructure Commands
- **Input Integration**: MUST read team-workspace for context
- **Output Integration**: MUST write to team-workspace for collaboration
- **Lifecycle Integration**: Full pre/post execution protocols
- **Knowledge Contribution**: Required (they enable team collaboration)

## Implementation Impact

### Reduced Scope for Core Product Commands
- Simpler lifecycle integration (input-only from team-workspace)
- Focus on product quality rather than team collaboration
- Clearer separation of concerns

### Updated Quality Metrics
- Core Product Commands: Focus on end-user deliverable quality
- Infrastructure Commands: Focus on team collaboration effectiveness
- Different success criteria for each command type

---

**Status**: ACTIVE - Supersedes original audit assumptions
**Next Action**: Update all documentation to reflect correct integration patterns
**Impact**: Simplifies Core Product Command lifecycle requirements
