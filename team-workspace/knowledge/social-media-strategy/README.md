# Social Media Strategy Knowledge Base

## Topic Authority
- **Primary Owner**: social-media-strategist
- **Secondary Owners**: business-analyst, product-owner
- **Freshness Threshold**: 7 days
- **Last Updated**: 2025-06-21

## Purpose
This knowledge base maintains the authoritative social media strategy for Cole Morton's brand positioning as a software engineer and quantitative trader who produces institutional-quality financial content through the AI Command Collaboration Framework.

## Knowledge Structure

### Current Strategy Files
- `current-strategy.md` - Active social media strategy (updated by social-media-strategist)
- `performance-metrics.md` - Strategy effectiveness tracking
- `content-calendar-framework.md` - Content planning and distribution strategy

### Cross-Command Dependencies
- **Reads From**:
  - `team-workspace/knowledge/requirements/` (business-analyst)
  - `team-workspace/knowledge/product-strategy/` (product-owner)
  - `team-workspace/knowledge/business-priorities/` (product-owner)

- **Provides To**:
  - business-analyst: Marketing insights for requirements analysis
  - product-owner: Content strategy implications for business decisions
  - twitter-post: Social media optimization patterns and best practices

## Integration Workflow

### Before Strategy Development
1. Run pre-execution consultation: `python team-workspace/coordination/pre-execution-consultation.py social-media-strategist social-media-strategy "{objective}"`
2. Review business-analyst requirements for stakeholder and process insights
3. Check product-owner strategic decisions and business priorities
4. Validate no conflicting marketing/content strategies exist

### After Strategy Development
1. Update topic ownership: `python team-workspace/coordination/topic-ownership-manager.py update social-media-strategy social-media-strategist "{summary}"`
2. Save strategy to `current-strategy.md` with proper metadata
3. Coordinate with cross-command dependencies
4. Set up performance monitoring and review cycles

## Performance Tracking
- **Primary Metrics**: Audience growth, engagement quality, content authority
- **Business Alignment**: Revenue attribution, brand positioning, competitive differentiation
- **Cross-Command Collaboration**: Requirements satisfaction, priority alignment, conflict avoidance

## Notes
- Social media strategies are highly dynamic and require frequent updates (7-day freshness threshold)
- All strategy changes must coordinate with business-analyst and product-owner
- Focus remains on trading content with AI innovation as supporting foundation
- Target audience priority: 1) Traders, 2) Content Creators, 3) Tech Professionals
