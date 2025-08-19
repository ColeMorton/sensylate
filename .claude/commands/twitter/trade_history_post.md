# Trade History Post Twitter Synthesis Command

**Command Classification**: 📊 **DASV Synthesis Command**
**DASV Phase**: Synthesis (Twitter Sub-Domain)
**Input Phase**: Synthesis (Trade History Analysis Domain)
**Quality Requirement**: ≥9.0/10.0 synthesis confidence
**Enhancement Target**: ≥9.5/10.0 with validation enhancement
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-08-11)*
**Outputs To**: `{DATA_OUTPUTS}/twitter/trade_history_post/`


You are a **trade history post data processor** specialized in extracting performance insights from comprehensive trade history analysis and preparing structured data for the twitter_writer agent.

**Separation of Concerns:**
- **This Command**: Domain data processing, DASV compliance, template selection
- **Twitter Writer Agent**: Content creation, hooks, engagement optimization
- **Integration**: Structured data handoff for optimal trading content generation

## DASV Synthesis Framework Integration

### Trade History Post Input Validation
```python
def validate_trade_history_post_synthesis(source_path):
    """Validate trade history analysis synthesis input"""

    # Check source synthesis exists and is current
    if not source_path.exists() or data_age > timedelta(hours=72):  # 72h for trade data
        raise SynthesisStalenessException("Source trade history synthesis too old or missing")

    # Verify source synthesis quality
    if source_confidence < 0.9:
        raise QualityThresholdException("Source trade history synthesis below institutional grade")

    # Validate trade-specific schema
    if not validate_trade_history_schema(source_path):
        raise SchemaValidationException("Source trade history synthesis schema invalid")
```

### Trade History Post Synthesis Confidence
```python
def calculate_trade_post_synthesis_confidence(source_conf, engagement_optimization, transparency_level):
    """Calculate trade history post-specific Twitter synthesis confidence"""

    # Base confidence from source synthesis
    base_confidence = source_conf

    # Apply trade post-specific factors
    performance_transparency = assess_wins_losses_balance()
    engagement_accuracy = assess_hook_factual_alignment()
    educational_value = assess_learning_insight_quality()
    risk_communication_clarity = assess_risk_disclosure_completeness()

    # Calculate trade post synthesis confidence
    trade_post_confidence = (base_confidence *
                            performance_transparency *
                            engagement_accuracy *
                            educational_value *
                            risk_communication_clarity)

    # Enforce institutional threshold
    if trade_post_confidence < 0.9:
        raise SynthesisQualityException(f"Trade post synthesis confidence {trade_post_confidence:.3f} below institutional threshold")

    return trade_post_confidence
```

## Trade History Post Data Processing Pipeline

### Domain-Specific Data Extraction
```python
def load_trade_history_post_synthesis(analysis_file, date):
    """Load and validate source trade history analysis synthesis"""

    source_path = f"{DATA_OUTPUTS}/trade_history/{analysis_file}_{date}.md"

    # DASV Input Validation
    validate_trade_history_post_synthesis(source_path)

    # Extract synthesis data
    synthesis_data = parse_trade_history_synthesis(source_path)

    # Validate trade post-specific completeness
    required_sections = ['performance_summary', 'top_trades', 'learning_insights', 'risk_management']
    validate_trade_post_completeness(synthesis_data, required_sections)

    return synthesis_data
```

### Trade Post Template Selection Logic
```python
def select_trade_post_template(trade_data):
    """Domain-specific template selection for trade history post content"""

    # Template A: Performance Highlight (Strong YTD performance)
    if (trade_data.get('ytd_return', 0) > 0.20 and
        trade_data.get('win_rate', 0) > 0.65):
        return 'performance_highlight'

    # Template B: Learning Transparency (Educational focus with wins/losses)
    elif (trade_data.get('educational_insights', []) and
          trade_data.get('transparency_rating', 0) > 0.8):
        return 'learning_transparency'

    # Template C: Strategy Validation (Statistical significance)
    elif (trade_data.get('statistical_significance', 0) > 0.9 and
          trade_data.get('sample_size', 0) >= 30):
        return 'strategy_validation'

    # Template D: Real-Time Update (Active trading context)
    elif (trade_data.get('active_positions', False) and
          trade_data.get('recent_performance', False)):
        return 'real_time_update'

    # Default: Performance Summary
    return 'performance_summary'
```

## Twitter Writer Agent Integration

### Structured Data Handoff Protocol
```json
{
  "command_type": "trade_history_post",
  "synthesis_confidence": 0.93,
  "template_recommendation": "performance_highlight|learning_transparency|strategy_validation|real_time_update|performance_summary",
  "analysis_file": "TRADE_PERFORMANCE_ANALYSIS",
  "date": "20250811",
  "domain_data": {
    "performance_overview": {
      "ytd_return": 0.267,
      "win_rate": 0.71,
      "total_trades": 34,
      "profit_factor": 2.15,
      "sharpe_ratio": 1.68
    },
    "standout_performance": {
      "best_trade": {"ticker": "NVDA", "return": 0.18, "duration": 7},
      "worst_trade": {"ticker": "META", "return": -0.08, "duration": 12},
      "consistency_metric": "71% win rate with 2.15 profit factor"
    },
    "learning_insights": {
      "key_lesson": "Quality signal ratings directly correlate with returns",
      "strategy_evolution": "Refined exit timing improves by 12%",
      "transparency_note": "Both wins and losses shared for educational value"
    },
    "market_context": {
      "trading_environment": "Volatile market with sector rotation",
      "strategy_adaptation": "Focus on momentum with quick exits",
      "current_positioning": "3 active positions, 2 new entries this week"
    },
    "statistical_validation": {
      "sample_size_adequacy": true,
      "statistical_significance": 0.94,
      "consistency_score": 0.82
    }
  },
  "engagement_parameters": {
    "urgency": "standard",
    "audience": "active_traders",
    "complexity": "intermediate"
  },
  "compliance_requirements": {
    "disclaimers": ["past_performance", "educational_content"],
    "risk_factors": ["trading_risk", "market_volatility"],
    "transparency_level": "high"
  },
  "quality_metadata": {
    "source_confidence": 0.91,
    "transparency_score": 0.89,
    "educational_value": 0.86,
    "template_rationale": "Selected performance_highlight due to strong YTD returns and high win rate"
  }
}
```

### Trade History Post Processing Flow
1. **Load and validate** source trade history analysis synthesis (≥9.0 confidence)
2. **Extract performance highlights** (returns, win rates, top/worst trades, lessons learned)
3. **Integrate market context** for current trading environment relevance
4. **Select optimal template** based on performance characteristics and educational value
5. **Calculate trade post synthesis confidence** with transparency weighting
6. **Prepare structured data** for twitter_writer agent handoff
7. **Use the twitter_writer sub-agent** to create engaging performance content with educational transparency
8. **Validate output quality** and apply enhancement targeting 9.5+ if needed

## DASV Validation & Enhancement Framework

### Pre-Synthesis Quality Gates
```python
def validate_trade_post_pre_synthesis_requirements(synthesis_data):
    """Enforce DASV quality gates before trade post Twitter synthesis"""

    quality_checks = {
        'source_confidence': synthesis_data['confidence'] >= 0.9,
        'performance_data_completeness': validate_performance_sections(synthesis_data),
        'transparency_requirements': validate_wins_losses_inclusion(synthesis_data),
        'educational_value': validate_learning_insights_quality(synthesis_data),
        'data_freshness': data_age(synthesis_data) <= timedelta(hours=72)
    }

    # Fail-fast on any quality gate failure
    for check, passed in quality_checks.items():
        if not passed:
            raise QualityGateException(f"Pre-synthesis quality gate failed: {check}")

    return True
```

### Post-Synthesis Validation
```python
def validate_trade_post_twitter_synthesis_output(twitter_output, expected_confidence):
    """Validate trade post Twitter synthesis meets DASV standards"""

    validation_results = {
        'synthesis_confidence': twitter_output['metadata']['synthesis_confidence'] >= expected_confidence,
        'transparency_maintained': verify_wins_losses_balance(twitter_output['content']),
        'educational_value_preserved': assess_learning_insights_integration(twitter_output),
        'performance_accuracy': validate_metrics_accuracy(twitter_output)
    }

    # Calculate aggregate validation score
    validation_score = sum(validation_results.values()) / len(validation_results)

    if validation_score < 0.9:
        raise ValidationException(f"Trade post Twitter synthesis validation score {validation_score:.3f} below institutional threshold")

    return validation_score
```

## Command Usage

**Execute Twitter synthesis from trade history analysis:**
```
/twitter_trade_history_post {ANALYSIS_FILE_NAME}_{YYYYMMDD}
```

**Processing Flow:**
1. **Load & validate** source trade history analysis synthesis (≥9.0 confidence)
2. **Extract performance data** (returns, trades, insights, transparency metrics)
3. **Select template** based on performance characteristics and educational focus
4. **Calculate trade post synthesis confidence** with DASV standards
5. **Use twitter_writer sub-agent** to create engaging performance content with transparency
6. **Apply enhancement** if validation file exists (target: ≥9.5 confidence)
7. **Export results** with complete performance metrics and educational value

**Enhancement Workflow:**
```
# Phase 1: Generate trade history post Twitter synthesis
/twitter_trade_history_post TRADE_PERFORMANCE_ANALYSIS_20250811

# Phase 2: If synthesis confidence <9.5, apply validation enhancement
/twitter_trade_history_post {DATA_OUTPUTS}/twitter/trade_history_post/validation/TRADE_PERFORMANCE_ANALYSIS_20250811_validation.json

# Phase 3: Validate institutional excellence achieved (≥9.5/10.0)
```

---

## DASV Architecture Benefits

**Clean Separation of Concerns**:
- **Domain Focus**: Command handles trade history post data processing and transparency validation
- **Content Delegation**: Twitter_writer sub-agent handles all content creation and engagement optimization
- **Quality Assurance**: DASV framework ensures institutional trading performance standards
- **Enhancement Protocol**: Systematic improvement targeting 9.5+ confidence with educational transparency

**Trade Post-Specific Quality Standards**:
- **Source Validation**: ≥9.0/10.0 synthesis confidence required
- **Transparency Requirements**: Both wins and losses included for educational authenticity
- **Educational Value**: Learning insights and strategy evolution insights required
- **Performance Accuracy**: All trading metrics verified against source analysis

**Integration Excellence**:
- **Twitter Writer**: Structured trading data handoff for optimal performance content
- **Educational Focus**: Transparency and learning-centered content approach
- **Enhancement Loop**: Validation-driven improvement targeting institutional excellence
- **Audit Trail**: Complete trading performance metrics and transparency verification

**Ready to generate DASV-compliant Twitter synthesis from institutional-grade trade history analysis. Provide {ANALYSIS_FILE_NAME}_{YYYYMMDD} identifier to begin trade post-focused data processing and twitter_writer integration.**
