# Twitter Strategist Synthesize Trading Strategy Microservice
*DASV Phase 3: Content synthesis for trading-focused social media posts*

## Service Specification

### Input Interface
```yaml
required_inputs:
  - ticker: string              # Stock symbol for trading strategy content
  - analysis_context: object   # Trading analysis data from team workspace
  - engagement_target: string  # "high_engagement|educational|viral"

optional_inputs:
  - post_length: integer       # Character count target (default: 280)
  - include_charts: boolean    # Include chart references (default: true)
  - risk_disclosure: boolean   # Include risk disclaimers (default: true)
  - confidence_threshold: float # Minimum confidence for claims (default: 0.7)
```

### Output Interface
```yaml
outputs:
  primary_output:
    type: social_media_post
    format: markdown
    confidence_score: float
    engagement_prediction: float

  metadata:
    execution_time: timestamp
    data_sources: array
    quality_metrics: object
    next_phase_ready: boolean
    dependency_tree: object
```

### Service Dependencies
- **Upstream Services**: None (synthesis can work directly from context)
- **Downstream Services**: `twitter_strategist_validate_trading_strategy`
- **External APIs**: None required
- **Shared Resources**:
  - Data outputs: `/data/outputs/trading-strategies/`
  - Analysis outputs: `/data/outputs/fundamental_analysis/`
  - Content templates: `/templates/social_media/`

## Data/File Dependencies

### Required Files
```yaml
input_dependencies:
  required_files:
    - path: "/data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md"
      type: "markdown"
      freshness_requirement: "24h"
      fallback_strategy: "cache"
      confidence_impact: 0.3

  context_dependencies:
    - data_path: "/data/outputs/trading-strategies/"
      knowledge_area: "trading_analysis"
      minimum_confidence: 0.7
      superseding_check: true

    - template_path: "/templates/social_media/"
      knowledge_area: "content_templates"
      minimum_confidence: 0.8
      superseding_check: false
```

### Dependency Validation Protocol
```yaml
pre_execution_checks:
  - Verify fundamental analysis file exists for ticker
  - Check team workspace trading strategy context
  - Validate social media templates accessibility
  - Confirm all dependencies meet freshness requirements

runtime_monitoring:
  - Track context usage from team workspace
  - Monitor template effectiveness
  - Log content generation confidence scores
  - Alert on missing critical trading data
```

## Framework Implementation

### Synthesis Phase Execution
```yaml
execution_sequence:
  pre_synthesis:
    - Load fundamental analysis for ticker
    - Extract key trading insights and catalysts
    - Identify engagement optimization opportunities
    - Initialize content generation templates

  main_synthesis:
    - Generate core trading thesis (1-2 sentences)
    - Create supporting evidence points
    - Apply engagement optimization techniques
    - Integrate risk disclosure requirements
    - Calculate content confidence scores

  post_synthesis:
    - Validate content accuracy against source analysis
    - Check engagement prediction algorithms
    - Ensure compliance with platform requirements
    - Prepare validation phase inputs
```

### Quality Assurance Gates
```yaml
content_validation:
  accuracy_check:
    - All claims backed by fundamental analysis
    - Confidence scores meet threshold requirements
    - No misleading or exaggerated statements

  engagement_optimization:
    - Character count within platform limits
    - Hashtag integration follows best practices
    - Call-to-action appropriately positioned

  compliance_verification:
    - Risk disclosures included when required
    - Financial advice disclaimers present
    - Platform policy compliance confirmed
```

## Output/Generation Standards

### Primary Output Format
```yaml
output_specification:
  file_generation:
    - path_pattern: "/data/outputs/social_media/twitter/{TICKER}_trading_strategy_{YYYYMMDD}.md"
    - naming_convention: "ticker_product_timestamp"
    - format_requirements: "markdown with structured metadata"
    - content_validation: "engagement_prediction_schema"
    - confidence_integration: "mandatory_in_headers_and_content"

  structured_content:
    - format: "markdown"
    - sections: ["post_content", "engagement_metrics", "validation_notes"]
    - confidence_scores: "0.0-1.0 format throughout"
    - metadata_requirements: ["timestamp", "source_analysis", "engagement_prediction"]
```

### Content Template
```markdown
# {TICKER} Trading Strategy Social Media Post
*Generated: {DATE} | Confidence: {X.X}/1.0 | Engagement Prediction: {X.X}/1.0*
<!-- Author: Cole Morton -->

## Post Content

### Primary Post
```
{TICKER} trading update: [Core thesis in 1-2 sentences with key catalyst]

📊 Key levels: Support ${XXX} | Resistance ${XXX}
🎯 Price target: ${XXX} ([XX]% upside)
⚠️ Risk: [Primary risk factor]

Not financial advice. DYOR. #trading #{TICKER} #stocks
```

### Engagement Optimization
- **Hook**: [Attention-grabbing opening element]
- **Value**: [Key insight or actionable information]
- **CTA**: [Call-to-action for engagement]
- **Hashtags**: [Optimized hashtag strategy]

## Validation Metrics

### Content Quality
| Metric | Score | Confidence | Validation Method |
|--------|-------|------------|-------------------|
| Accuracy | {X.X}/1.0 | {X.X}/1.0 | Source analysis verification |
| Engagement Potential | {X.X}/1.0 | {X.X}/1.0 | Historical performance model |
| Risk Appropriateness | {X.X}/1.0 | {X.X}/1.0 | Compliance checklist |
| **Overall Quality** | **{X.X}/1.0** | **{X.X}/1.0** | Weighted average |

### Data Dependencies
- **Source Analysis**: `/data/outputs/fundamental_analysis/{TICKER}_{YYYYMMDD}.md`
- **Template Used**: `trading_strategy_template_v{X.X}`
- **Context Sources**: `data/outputs/trading-strategies/`
- **Validation Status**: All dependencies current and validated

## Next Phase Preparation
- **Downstream Service**: `twitter_strategist_validate_trading_strategy`
- **Required Inputs**: Generated post content, engagement prediction, quality metrics
- **Success Criteria**: Content accuracy ≥ 0.8, Engagement prediction ≥ 0.7
- **Validation Focus**: Platform compliance, engagement optimization, risk disclosure adequacy
```

## Success Metrics
```yaml
microservice_kpis:
  content_quality:
    - Average confidence score: target >0.8
    - Template compliance: target 100%
    - Validation pass rate: target >95%

  dependency_management:
    - Required files accessibility: target 100%
    - Data freshness compliance: target >90%
    - Fallback activation rate: target <10%
```

---

*This microservice demonstrates the refined architecture with product-specific naming, selective framework phases (synthesis + validation only), and comprehensive dependency/output standards.*
