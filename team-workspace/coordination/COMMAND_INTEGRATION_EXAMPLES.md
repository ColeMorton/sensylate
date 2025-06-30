# Command Integration Examples for Content Lifecycle Management

This document provides concrete examples of how each AI command should integrate with the Content Lifecycle Management system to prevent duplication and maintain knowledge integrity.

## Universal Integration Pattern

**Every AI command MUST follow this pattern before creating any analysis:**

```python
# Step 1: Import consultation system
from team_workspace.coordination.pre_execution_consultation import PreExecutionConsultant

# Step 2: Consult before execution
consultant = PreExecutionConsultant()
consultation_result = consultant.consult_before_execution(
    command_name="<your_command>",
    proposed_topic="<topic>",
    proposed_scope="<description_of_analysis>"
)

# Step 3: Follow recommendation
if consultation_result["recommendation"] == "proceed":
    # Safe to create new analysis
    create_new_analysis()
elif consultation_result["recommendation"] == "avoid_duplication":
    # Reference existing work instead
    reference_existing_authority(consultation_result["existing_knowledge"]["authority_path"])
elif consultation_result["recommendation"] == "coordinate_required":
    # Work with topic owner
    coordinate_with_owner(consultation_result["ownership_status"]["primary_owner"])
elif consultation_result["recommendation"] == "update_existing":
    # Update existing content with superseding workflow
    supersede_existing_content()
```

## Command-Specific Integration Examples

### Architect Command Integration

**Topics**: Implementation plans, technical architecture, system design

```bash
# Before creating any implementation plan
python team-workspace/coordination/pre-execution-consultation.py architect technical-debt-resolution "comprehensive debt resolution strategy"

# Example response: "update_existing" - you own stale content
# Action: Update existing plan with superseding workflow

python team-workspace/coordination/superseding-workflow.py declare architect technical-debt-resolution \
  "team-workspace/knowledge/implementation-plans/technical-debt-resolution-v2.md" \
  "team-workspace/knowledge/implementation-plans/technical-debt-resolution.md" \
  "Updated with new findings and revised timeline"
```

**Integration Code Example**:
```python
def create_implementation_plan(topic, scope, detailed_requirements):
    """Architect command implementation plan creation."""

    # Required: Pre-execution consultation
    consultant = PreExecutionConsultant()
    result = consultant.consult_before_execution("architect", topic, scope)

    if result["recommendation"] == "proceed":
        # Create new implementation plan
        plan_path = f"team-workspace/knowledge/implementation-plans/{topic}.md"

        # Claim ownership if unowned
        ownership_manager = TopicOwnershipManager()
        ownership_manager.claim_unowned_topic(topic, "architect",
                                            f"New implementation plan for {scope}")

        # Create plan content
        plan_content = generate_implementation_plan(detailed_requirements)
        write_plan(plan_path, plan_content)

        # Update registry
        update_topic_registry(topic, plan_path, "architect")

    elif result["recommendation"] == "update_existing":
        # Update existing plan using superseding workflow
        existing_path = result["existing_knowledge"]["authority_path"]
        new_path = existing_path.replace(".md", "-updated.md")

        # Create updated plan
        updated_content = update_implementation_plan(existing_path, detailed_requirements)
        write_plan(new_path, updated_content)

        # Declare superseding
        workflow = SupersedingWorkflow()
        workflow.declare_superseding("architect", topic, new_path, [existing_path],
                                   f"Updated implementation plan: {scope}")

    elif result["recommendation"] == "coordinate_required":
        primary_owner = result["ownership_status"]["primary_owner"]
        print(f"Coordination required with {primary_owner} for topic '{topic}'")
        print("Consider requesting secondary ownership or collaborative approach")
        return None

    else:  # avoid_duplication
        authority_path = result["existing_knowledge"]["authority_path"]
        print(f"Fresh implementation plan exists at: {authority_path}")
        print("Reference existing work instead of creating duplicate")
        return authority_path
```

### Code-Owner Command Integration

**Topics**: Technical health assessments, code quality analysis, security reviews

```bash
# Before creating technical health assessment
python team-workspace/coordination/pre-execution-consultation.py code-owner technical-health "quarterly security review"

# Example response: "consider_necessity" - you own fresh content
# Action: Review if update is truly needed, or reference existing

# If update needed:
python team-workspace/coordination/decision-tree.py code-owner technical-health "quarterly security review"

# Decision tree response: "update_existing" with high confidence
# Action: Update existing assessment
```

**Integration Code Example**:
```python
def perform_technical_health_assessment(focus_area=None):
    """Code-owner technical health assessment."""

    scope = f"Technical health assessment focusing on {focus_area}" if focus_area else "Comprehensive technical health assessment"

    # Required consultation
    consultant = PreExecutionConsultant()
    result = consultant.consult_before_execution("code-owner", "technical-health", scope)

    if result["recommendation"] == "consider_necessity":
        # We own fresh content - check if update is really needed
        decision_tree = DecisionTree()
        decision = decision_tree.make_decision("code-owner", "technical-health", scope)

        if decision["decision"] == "reference_existing":
            existing_path = result["existing_knowledge"]["authority_path"]
            print(f"Current assessment is sufficient: {existing_path}")
            return existing_path

        elif decision["decision"] == "update_existing":
            # Proceed with update using superseding workflow
            return update_health_assessment(result["existing_knowledge"]["authority_path"], focus_area)

    elif result["recommendation"] == "proceed":
        # Create new assessment
        return create_new_health_assessment(focus_area)

    else:
        # Handle coordination or duplication scenarios
        handle_coordination_scenario(result)

def update_health_assessment(existing_path, focus_area):
    """Update existing health assessment with superseding."""

    # Create updated assessment
    updated_content = enhance_health_assessment(existing_path, focus_area)
    new_path = existing_path.replace(".md", f"-{datetime.now().strftime('%Y%m%d')}.md")

    write_assessment(new_path, updated_content)

    # Declare superseding
    workflow = SupersedingWorkflow()
    result = workflow.declare_superseding(
        "code-owner", "technical-health", new_path, [existing_path],
        f"Updated assessment with focus on {focus_area}"
    )

    if result["success"]:
        print(f"Successfully updated health assessment: {new_path}")
        return new_path
    else:
        print(f"Superseding failed: {result['error']}")
        return None
```

### Product-Owner Command Integration

**Topics**: Strategic product decisions, business priorities, roadmap planning

```bash
# Before making strategic decisions
python team-workspace/coordination/pre-execution-consultation.py product-owner product-strategy "Q2 2025 roadmap priorities"

# Example response: "update_existing" - you own content that needs updating
# Action: Update strategic decisions with superseding workflow

# Check for business context from other analyses
python team-workspace/coordination/topic-ownership-manager.py collaborate product-owner technical-health

# Collaboration response: "secondary_owner" - you can contribute to technical health topic
# Action: Reference technical health in strategic decisions
```

**Integration Code Example**:
```python
def create_strategic_product_decisions(business_context, timeline="Q2 2025"):
    """Product-owner strategic decision making."""

    scope = f"Strategic product decisions for {timeline}"

    # Required consultation
    consultant = PreExecutionConsultant()
    result = consultant.consult_before_execution("product-owner", "product-strategy", scope)

    # Check related analyses for context
    related_analyses = gather_related_analyses(["technical-health", "requirements"])

    if result["recommendation"] == "update_existing":
        # Update existing strategic decisions
        existing_path = result["existing_knowledge"]["authority_path"]
        return update_strategic_decisions(existing_path, business_context, related_analyses, timeline)

    elif result["recommendation"] == "proceed":
        # Create new strategic decisions
        return create_new_strategic_decisions(business_context, related_analyses, timeline)

    else:
        # Handle other scenarios
        handle_product_owner_coordination(result)

def gather_related_analyses(topic_list):
    """Gather context from related analyses."""
    related_content = {}

    for topic in topic_list:
        # Check if we have ownership or access
        ownership_manager = TopicOwnershipManager()
        ownership_info = ownership_manager.get_topic_ownership(topic)

        if ownership_info["primary_owner"] == "product-owner" or \
           "product-owner" in ownership_info["secondary_owners"]:
            # We have access - can reference this content
            authority_path = get_topic_authority_path(topic)
            if authority_path and Path(authority_path).exists():
                related_content[topic] = read_analysis_summary(authority_path)

    return related_content

def update_strategic_decisions(existing_path, business_context, related_analyses, timeline):
    """Update strategic decisions with superseding workflow."""

    # Incorporate business context and related analyses
    updated_decisions = enhance_strategic_decisions(
        existing_path, business_context, related_analyses, timeline
    )

    new_path = f"team-workspace/knowledge/product-strategy/strategic-decisions-{timeline.lower().replace(' ', '-')}.md"
    write_decisions(new_path, updated_decisions)

    # Supersede existing decisions
    workflow = SupersedingWorkflow()
    result = workflow.declare_superseding(
        "product-owner", "product-strategy", new_path, [existing_path],
        f"Updated strategic decisions for {timeline} incorporating technical health insights"
    )

    return new_path if result["success"] else None
```

### Business-Analyst Command Integration

**Topics**: Requirements analysis, business process analysis, stakeholder analysis

```bash
# Before creating requirements analysis
python team-workspace/coordination/pre-execution-consultation.py business-analyst user-experience-requirements "mobile app UX improvements"

# Example response: "proceed" - no existing knowledge on this topic
# Action: Create new requirements analysis and claim ownership

python team-workspace/coordination/topic-ownership-manager.py claim user-experience-requirements business-analyst "New requirements area for mobile UX analysis"
```

**Integration Code Example**:
```python
def perform_requirements_analysis(analysis_type, scope_description):
    """Business-analyst requirements analysis."""

    topic = f"{analysis_type}-requirements"

    # Required consultation
    consultant = PreExecutionConsultant()
    result = consultant.consult_before_execution("business-analyst", topic, scope_description)

    if result["recommendation"] == "proceed":
        # Create new requirements analysis
        return create_new_requirements_analysis(topic, analysis_type, scope_description)

    elif result["recommendation"] == "coordinate_required":
        # Need to work with existing owner
        return coordinate_requirements_analysis(result, topic, scope_description)

    elif result["recommendation"] == "avoid_duplication":
        # Reference existing requirements
        existing_path = result["existing_knowledge"]["authority_path"]
        print(f"Existing requirements analysis available: {existing_path}")
        return existing_path

    elif result["recommendation"] == "update_existing":
        # Update existing requirements
        return update_requirements_analysis(result["existing_knowledge"]["authority_path"], scope_description)

def create_new_requirements_analysis(topic, analysis_type, scope_description):
    """Create new requirements analysis with ownership claim."""

    # Claim ownership
    ownership_manager = TopicOwnershipManager()
    ownership_result = ownership_manager.claim_unowned_topic(
        topic, "business-analyst", f"Requirements analysis for {analysis_type}"
    )

    if not ownership_result["success"]:
        print(f"Could not claim ownership: {ownership_result['error']}")
        return None

    # Create requirements analysis
    requirements_content = generate_requirements_analysis(analysis_type, scope_description)
    analysis_path = f"team-workspace/knowledge/requirements/{topic}.md"

    write_requirements(analysis_path, requirements_content)

    # Update topic registry
    update_topic_registry(topic, analysis_path, "business-analyst")

    print(f"Created new requirements analysis: {analysis_path}")
    return analysis_path

def coordinate_requirements_analysis(consultation_result, topic, scope_description):
    """Coordinate with existing topic owner."""

    primary_owner = consultation_result["ownership_status"]["primary_owner"]

    # Get collaboration guidance
    ownership_manager = TopicOwnershipManager()
    collaboration = ownership_manager.suggest_collaboration("business-analyst", topic)

    if collaboration["collaboration_type"] == "external_contributor":
        print(f"Topic '{topic}' owned by {primary_owner}")
        print("Suggested collaboration approaches:")
        for approach in collaboration["collaboration_approaches"]:
            print(f"  - {approach['type']}: {approach['description']}")

        # Request secondary ownership
        print(f"\nConsider requesting secondary ownership from {primary_owner}")
        return None

    else:
        # Handle other collaboration scenarios
        return handle_collaboration_scenario(collaboration, topic, scope_description)
```

### Twitter-Post Command Integration

**Topics**: Content creation, social media strategy

```bash
# Before creating twitter content
python team-workspace/coordination/pre-execution-consultation.py twitter-post social-media-content "AAPL analysis promotion"

# Example response: "proceed" - safe to create social content
# Action: Create content, potentially referencing other analyses

# Check for related trading analysis to reference
python team-workspace/coordination/topic-ownership-manager.py ownership fundamental-analysis
```

**Integration Code Example**:
```python
def create_twitter_content(stock_symbol, content_type="analysis_promotion"):
    """Twitter-post content creation with analysis integration."""

    topic = "social-media-content"
    scope = f"{content_type} for {stock_symbol}"

    # Consultation (twitter content is typically ephemeral, but still check)
    consultant = PreExecutionConsultant()
    result = consultant.consult_before_execution("twitter-post", topic, scope)

    # Look for related trading analyses to reference
    related_analysis = find_related_trading_analysis(stock_symbol)

    if result["recommendation"] in ["proceed", "reference_existing"]:
        # Create twitter content
        return create_social_media_content(stock_symbol, content_type, related_analysis)
    else:
        # Handle coordination if needed
        return handle_twitter_coordination(result, stock_symbol, content_type)

def find_related_trading_analysis(stock_symbol):
    """Find related trading analysis to reference in social content."""

    # Check for fundamental analysis
    analysis_paths = [
        f"data/outputs/fundamental_analysis/{stock_symbol}_*.md",
        f"team-workspace/knowledge/*/fundamental-analysis-{stock_symbol}.md"
    ]

    for pattern in analysis_paths:
        matching_files = glob.glob(pattern)
        if matching_files:
            # Found related analysis - extract key insights
            latest_analysis = max(matching_files, key=os.path.getctime)
            return extract_social_media_insights(latest_analysis)

    return None

def create_social_media_content(stock_symbol, content_type, related_analysis=None):
    """Create social media content with analysis integration."""

    if related_analysis:
        # Create content that references the analysis
        content = generate_analysis_promotion_content(stock_symbol, related_analysis)

        # Note: Twitter content is typically not stored in knowledge structure
        # But we log the creation for tracking
        log_social_media_creation(stock_symbol, content_type, related_analysis["source"])

    else:
        # Create standalone content
        content = generate_standalone_social_content(stock_symbol, content_type)
        log_social_media_creation(stock_symbol, content_type, None)

    return content
```

## Coordination Scenarios Examples

### Scenario 1: Cross-Command Collaboration

**Situation**: Architect wants to analyze technical debt, but Code-Owner already has fresh technical health assessment

```bash
# Architect consultation
python team-workspace/coordination/pre-execution-consultation.py architect technical-debt "comprehensive debt analysis"
# Response: "coordinate_required" - Code-Owner owns technical-health

# Get collaboration guidance
python team-workspace/coordination/topic-ownership-manager.py collaborate architect technical-health
# Response: "external_contributor" - coordination required

# Decision: Request secondary ownership
python team-workspace/coordination/topic-ownership-manager.py assign technical-health code-owner "architect,product-owner"
# Response: "success" - Architect now has secondary ownership

# Re-consult after ownership change
python team-workspace/coordination/pre-execution-consultation.py architect technical-debt "comprehensive debt analysis"
# Response: "coordinate_required" but now as secondary owner
```

### Scenario 2: Superseding Existing Content

**Situation**: Product-Owner needs to update strategic decisions with new business context

```bash
# Check current content
python team-workspace/coordination/knowledge-dashboard.py topic product-strategy
# Shows current authority and last update date

# Consult for update
python team-workspace/coordination/pre-execution-consultation.py product-owner product-strategy "Q3 strategic pivot"
# Response: "update_existing" - you own content that can be updated

# Declare superseding intent
python team-workspace/coordination/superseding-workflow.py declare product-owner product-strategy \
  "team-workspace/knowledge/product-strategy/strategic-decisions-q3-2025.md" \
  "team-workspace/knowledge/product-strategy/current-decisions.md" \
  "Strategic pivot for Q3 2025 based on market changes"
# Response: "success" with event_id for tracking
```

### Scenario 3: Claiming New Topic

**Situation**: Business-Analyst identifies new requirements area not covered by existing topics

```bash
# Check if topic exists
python team-workspace/coordination/topic-ownership-manager.py ownership customer-feedback-analysis
# Response: "has_primary_owner": false - topic is unowned

# Claim ownership
python team-workspace/coordination/topic-ownership-manager.py claim customer-feedback-analysis business-analyst "New requirements analysis area for customer feedback integration"
# Response: "success" - ownership claimed

# Create initial analysis
# [Business-Analyst creates analysis in knowledge/requirements/customer-feedback-analysis.md]

# Verify in dashboard
python team-workspace/coordination/knowledge-dashboard.py topic customer-feedback-analysis
# Shows new topic with business-analyst as owner
```

## Error Handling Examples

### Permission Denied Scenario

```python
def handle_permission_denied(command_name, topic, consultation_result):
    """Handle cases where command lacks permission for topic."""

    primary_owner = consultation_result["ownership_status"]["primary_owner"]

    print(f"Permission denied for topic '{topic}'")
    print(f"Primary owner: {primary_owner}")

    # Get collaboration options
    ownership_manager = TopicOwnershipManager()
    collaboration = ownership_manager.suggest_collaboration(command_name, topic)

    print("Available options:")
    for approach in collaboration["collaboration_approaches"]:
        print(f"  - {approach['type']}: {approach['action']}")

    # Recommend next steps
    print(f"\nRecommended next steps:")
    print(f"1. Contact {primary_owner} for coordination")
    print(f"2. Request secondary ownership if appropriate")
    print(f"3. Consider complementary analysis in different scope")

    return None
```

### Missing Authority File Scenario

```python
def handle_missing_authority_file(topic, expected_path):
    """Handle cases where authority file is missing."""

    print(f"Warning: Authority file missing for topic '{topic}': {expected_path}")

    # Check archive for recent superseding events
    superseding_log = load_superseding_log()
    recent_events = find_recent_superseding_events(topic, superseding_log)

    if recent_events:
        latest_event = recent_events[0]
        print(f"Recent superseding event found: {latest_event['event_id']}")
        print(f"Archive location: {latest_event['archive_location']}")

        # Offer recovery options
        print("Recovery options:")
        print(f"1. Restore from archive: {latest_event['archive_location']}")
        print(f"2. Create new authority file")
        print(f"3. Update registry to correct path")

    else:
        print("No recent superseding events found.")
        print("Manual intervention required to resolve missing authority file.")

    return None
```

## Testing Integration Examples

### Unit Test for Command Integration

```python
def test_architect_integration_workflow(self):
    """Test complete architect integration workflow."""

    # Setup test topic
    topic = "test-implementation-plan"
    scope = "test system architecture"

    # Test consultation
    consultant = PreExecutionConsultant(str(self.workspace_path))
    result = consultant.consult_before_execution("architect", topic, scope)

    # Should recommend proceed for new topic
    self.assertEqual(result["recommendation"], "proceed")

    # Test ownership claiming
    ownership_manager = TopicOwnershipManager(str(self.workspace_path))
    claim_result = ownership_manager.claim_unowned_topic(topic, "architect", "Test implementation")

    self.assertTrue(claim_result["success"])

    # Test superseding workflow
    old_file = self.workspace_path / "knowledge" / "implementation-plans" / f"{topic}.md"
    old_file.write_text("Original implementation plan")

    new_file = self.workspace_path / "knowledge" / "implementation-plans" / f"{topic}-v2.md"
    new_file.write_text("Updated implementation plan")

    workflow = SupersedingWorkflow(str(self.workspace_path))
    superseding_result = workflow.declare_superseding(
        "architect", topic, str(new_file), [str(old_file)], "Updated with new requirements"
    )

    self.assertTrue(superseding_result["success"])

    # Verify dashboard shows updated state
    dashboard = KnowledgeDashboard(str(self.workspace_path))
    topic_details = dashboard.get_topic_details(topic)

    self.assertEqual(topic_details["ownership_info"]["primary_owner"], "architect")
    self.assertTrue(topic_details["file_status"]["authority_exists"])
```

## Performance Monitoring

### Integration Performance Metrics

```python
def monitor_integration_performance():
    """Monitor performance of command integrations."""

    metrics = {
        "consultation_usage": count_consultation_calls(),
        "superseding_events": count_superseding_events(),
        "ownership_changes": count_ownership_changes(),
        "conflict_prevention": calculate_conflict_prevention_rate(),
        "system_health_trend": get_health_score_trend()
    }

    return metrics

def count_consultation_calls():
    """Count consultation API usage."""
    # Implementation would track consultation calls
    # Could use logging or separate metrics file
    pass

def calculate_conflict_prevention_rate():
    """Calculate how well integrations prevent conflicts."""

    # Compare conflicts before/after integration
    initial_conflicts = 203  # Baseline before implementation
    current_conflicts = run_conflict_detection()

    prevention_rate = (initial_conflicts - len(current_conflicts)) / initial_conflicts
    return prevention_rate
```

This comprehensive integration guide ensures all AI commands properly coordinate to maintain knowledge integrity and prevent the duplication, contradiction, and disorder that previously degraded team-workspace effectiveness.
