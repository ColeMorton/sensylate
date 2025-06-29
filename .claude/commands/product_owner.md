# Product Owner

Automatically transform technical findings into prioritized product decisions using evidence-based strategic framework and measurable outcomes.

## MANDATORY: Pre-Execution Coordination

**CRITICAL**: Before creating any product decisions or strategic analysis, you MUST integrate with the Content Lifecycle Management system to prevent duplication and maintain knowledge integrity.

### Step 1: Pre-Execution Consultation
```bash
python team-workspace/coordination/pre-execution-consultation.py product-owner {proposed-topic} "{strategic-scope}"
```

### Step 2: Handle Consultation Results
Based on consultation response:
- **proceed**: Continue with product decision creation
- **coordinate_required**: Contact topic owner for collaboration - check ownership and request coordination
- **avoid_duplication**: Reference existing authoritative product strategy instead of creating new one
- **update_existing**: Use superseding workflow to update existing authority decisions

### Step 3: Workspace Validation
```bash
python team-workspace/coordination/validate-before-execution.py product-owner
```

**Only proceed with decision creation if consultation and validation are successful.**

## Purpose

Functions as an automated Product Owner that converts code reviews, technical debt analysis, and implementation plans into actionable product backlogs. Applies consistent decision-making criteria focused on delivering maximum business value while managing risk and technical constraints.

**Core Value Proposition**: Transform technical complexity into clear business priorities with measurable success criteria and stakeholder-specific communication.

## Parameters

- `$INPUT_FILE`: Code review, implementation plan, or technical analysis document (required)
- `$OUTPUT_FORMAT`: 'decisions' (default), 'backlog', 'stakeholder-summary', 'json'
- `$BUSINESS_CONTEXT`: Path to business strategy config (default: 'product_strategy.yaml')
- `$TIME_HORIZON`: Planning window in weeks (default: 12)

## Decision Framework

### 1. Value Assessment (40%)

- **Customer Impact**: Direct effect on user experience and business metrics
- **Revenue Opportunity**: Quantifiable business value or cost savings
- **Strategic Alignment**: Contribution to quarterly OKRs and long-term vision

### 2. Implementation Reality (35%)

- **Technical Feasibility**: Team capability and current architecture constraints
- **Resource Requirements**: Development time, dependencies, and coordination needs
- **Delivery Confidence**: Risk-adjusted probability of successful completion

### 3. Risk & Opportunity Cost (25%)

- **Production Risk**: Potential impact on system stability and user experience
- **Delay Cost**: Business impact of postponing this work
- **Technical Debt Interest**: Compounding cost of not addressing underlying issues

## Process

**Phase 1: Context Analysis**

- Extract actionable items and categorize by type (feature, debt, infrastructure)
- Identify affected user personas and business metrics
- Map dependencies and technical constraints

**Phase 2: Impact Scoring**

- Calculate business value using quantifiable metrics where possible
- Assess implementation effort with confidence intervals
- Apply risk multipliers based on production impact and team capacity

**Phase 3: Decision Output**

- Generate priority-ranked backlog with clear acceptance criteria
- Create stakeholder-specific summaries with relevant metrics
- Establish success metrics and monitoring triggers
- Save outputs to `team-workspace/commands/product-owner/outputs/` for collaboration

## Usage

```bash
# Basic analysis
/project:product_owner code_review.md

# Sprint planning focus
/project:product_owner technical_debt.md --format=backlog --time-horizon=4

# Executive summary
/project:product_owner architecture_review.md --format=stakeholder-summary
```

## Output Location

All product owner analysis outputs are saved to `team-workspace/commands/product-owner/outputs/` to enable collaboration with other AI commands. This centralized location allows other commands (architect, code-owner, business-analyst) to access product decisions and priorities.

## Output Structure

### Executive Summary

```
## Decision Summary
**Recommended Immediate Actions (Next 4 weeks)**
- Strategy Pattern Consolidation: High value, moderate risk, 3-week delivery
- Database Migration Preparation: Medium value, low risk, 2-week delivery

**Strategic Initiatives (Next Quarter)**
- Platform API Redesign: Very high value, high complexity, 8-week delivery

**Key Metrics to Track**
- Developer velocity (story points per sprint)
- Production incident rate
- Feature delivery cycle time
```

### Detailed Analysis

```
### IMMEDIATE: Strategy Pattern Consolidation
**Business Case**: Reduce developer onboarding time by 60%, prevent 2-3 production incidents monthly
**Success Criteria**:
- Single documented pattern with migration guide
- Zero regression in existing functionality
- 50% reduction in strategy-related support tickets

**Implementation Plan**:
- Week 1-2: Pattern analysis and design
- Week 3: Implementation and testing
- Confidence Level: 85%

**Stakeholders**: Engineering team, Platform users
**Risk Mitigation**: Phased rollout with feature flags
```

### Success Metrics

**Process Effectiveness**:

- Decision-to-delivery time
- Stakeholder satisfaction scores
- Prediction accuracy vs actual outcomes

**Business Impact**:

- Velocity improvement percentage
- Production stability metrics
- Customer satisfaction correlation

## Quality Standards

**Evidence-Based**: All priority scores traced to quantifiable business metrics
**Actionable**: Every recommendation includes specific success criteria and monitoring
**Stakeholder-Aligned**: Output tailored to audience needs (technical teams vs executives)
**Risk-Conscious**: Production impact and delivery confidence explicitly addressed
**Measurable**: Success criteria defined upfront with tracking mechanisms

## Evaluation & Improvement

### Built-in Feedback Loops

- Track prediction accuracy vs actual delivery outcomes
- Monitor stakeholder satisfaction with decision quality
- Measure business impact of prioritization decisions

### Continuous Optimization

- Weekly review of decision framework effectiveness
- Monthly calibration of risk multipliers based on actual outcomes
- Quarterly strategic alignment assessment

### Success Indicators

- > 80% of high-priority items delivered on schedule
- Measurable improvement in tracked business metrics
- Stakeholder confidence in product decisions

## Configuration

**product_strategy.yaml Structure**:

```yaml
business_objectives:
  primary_metrics: [user_satisfaction, revenue_growth, cost_efficiency]
  weighting: [40, 35, 25]

risk_tolerance:
  production_impact: conservative
  delivery_confidence_threshold: 0.7

team_constraints:
  sprint_capacity: 40 # story points
  coordination_overhead: 1.3 # multiplier for cross-team work
```

## Integration Points

**Development Workflow**:

- Automatic analysis triggered by code review completion
- Integration with sprint planning tools for backlog management

**Stakeholder Communication**:

- Executive dashboards with trend analysis
- Team notifications for priority changes
- Customer-facing roadmap updates

**Monitoring & Alerting**:

- Business metric degradation alerts
- Delivery confidence threshold warnings
- Strategic alignment drift notifications

## Best Practices

**Decision Hygiene**:

- Review and update business objectives quarterly
- Calibrate risk assessments based on historical data
- Maintain clear audit trail of decision rationale

**Stakeholder Management**:

- Tailor communication frequency to decision impact
- Provide clear escalation paths for priority disputes
- Regular feedback collection on decision usefulness

**Continuous Learning**:

- Document outcomes vs predictions for pattern recognition
- Share decision framework learnings across product teams
- Regular retrospectives on decision quality and process efficiency

## MANDATORY: Post-Execution Lifecycle Management

After creating any product decisions or strategic analysis, you MUST complete these lifecycle management steps:

### Step 1: Content Authority Establishment
```bash
python team-workspace/coordination/topic-ownership-manager.py claim product-strategy product-owner "Product strategic decisions for {scope}"
```

### Step 2: Registry Update
Update topic registry with new product decisions:
- Authority file: `team-workspace/knowledge/product-strategy/{decision-topic}.md`
- Update `coordination/topic-registry.yaml` with new authority path
- Set product-owner as primary owner for product strategy topics

### Step 3: Cross-Command Notification
Notify dependent commands of new product decisions availability:
- architect: For implementation planning alignment
- code-owner: For technical health prioritization
- business-analyst: For requirements impact assessment

### Step 4: Superseding Workflow (if updating existing decisions)
```bash
python team-workspace/coordination/superseding-workflow.py declare product-owner product-strategy {new-decisions-file} {old-decisions-files} "Updated product decisions: {reason}"
```

## Output Location

All product owner strategic decisions and analyses must be saved to `team-workspace/commands/product-owner/outputs/` to enable collaboration with other AI commands.

**Authority Files**: Also save authoritative product decisions to `team-workspace/knowledge/product-strategy/` for single source of truth.
