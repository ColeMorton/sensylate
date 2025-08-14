# Trade History Analysis Twitter Synthesis Command

**Command Classification**: 📊 **DASV Synthesis Command**
**DASV Phase**: Synthesis (Twitter Sub-Domain)
**Input Phase**: Synthesis (Trade History Analysis Domain)
**Quality Requirement**: ≥9.0/10.0 synthesis confidence
**Enhancement Target**: ≥9.5/10.0 with validation enhancement
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-08-11)*
**Outputs To**: `{DATA_OUTPUTS}/twitter/trade_history/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/base_scripts/trade_history_twitter_script.py`
**Script Class**: `TradeHistoryTwitterScript`
**Registry Name**: `trade_history_twitter`
**Content Types**: `["trade_history_twitter"]`
**Requires Validation**: `true`

**Registry Integration**:
```python
@twitter_script(
    name="trade_history_twitter",
    content_types=["trade_history_twitter"],
    requires_validation=True
)
class TradeHistoryTwitterScript(BaseScript):
    """
    Trade history performance Twitter content generation script

    Parameters:
        analysis_file (str): Trade history analysis identifier
        date (str): Analysis date in YYYYMMDD format
        template_variant (Optional[str]): Specific template to use
        validation_file (Optional[str]): Path to validation file for enhancement
        validate_content (bool): Whether to validate generated content
    """
```

**Supporting Components**:
```yaml
trade_performance_analyzer:
  path: "{SCRIPTS_BASE}/trade_history/trade_performance_analyzer.py"
  class: "TradePerformanceAnalyzer"
  purpose: "Trade history data extraction and performance metrics calculation"

market_context_collector:
  path: "{SCRIPTS_BASE}/market_data/market_context_collector.py"
  class: "MarketContextCollector"
  purpose: "Real-time market context for performance validation"

twitter_command_processor:
  path: "{SCRIPTS_BASE}/twitter_command_processor.py"
  class: "TwitterCommandProcessor"
  purpose: "Unified Twitter content processing and validation"

unified_validation_framework:
  path: "{SCRIPTS_BASE}/unified_validation_framework.py"
  class: "UnifiedValidationFramework"
  purpose: "Institutional quality standards for trading content"
```

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/twitter/trade_history/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| performance_summary | `trade_history/twitter_performance_summary.j2` | YTD performance focus AND comprehensive metrics available | Overall performance overview |
| top_trades_showcase | `trade_history/twitter_top_trades.j2` | Best performing trades >3 AND detailed trade data | Highlight winning trades |
| learning_transparency | `trade_history/twitter_learning_transparency.j2` | Both wins and losses available AND educational focus | Transparent performance analysis |
| real_time_performance | `trade_history/twitter_real_time_performance.j2` | Active positions available AND current market context | Live trading performance |
| statistical_validation | `trade_history/twitter_statistical_validation.j2` | Signal quality data available AND statistical analysis | Strategy validation focus |

**Shared Components**:
```yaml
trade_base_template:
  path: "{TEMPLATES_BASE}/twitter/shared/base_twitter.j2"
  purpose: "Base template with common macros and trading formatting"

performance_components:
  path: "{TEMPLATES_BASE}/twitter/shared/performance_components.j2"
  purpose: "Performance metrics components and risk disclaimers"

validation_template:
  path: "{TEMPLATES_BASE}/twitter/validation/trade_performance_validation.j2"
  purpose: "Trading performance compliance and transparency validation"
```

**Template Selection Algorithm**:
```python
def select_trade_history_template(trade_data):
    """Select optimal template for trade history Twitter content"""

    # Performance summary for comprehensive YTD metrics
    if (trade_data.get('ytd_metrics_available', False) and
        trade_data.get('comprehensive_data', False)):
        return 'trade_history/twitter_performance_summary.j2'

    # Top trades showcase for highlighting wins
    elif (len(trade_data.get('best_trades', [])) >= 3 and
          trade_data.get('detailed_trade_data', False)):
        return 'trade_history/twitter_top_trades.j2'

    # Learning transparency for balanced narrative
    elif (trade_data.get('wins_and_losses_available', False) and
          trade_data.get('educational_focus', False)):
        return 'trade_history/twitter_learning_transparency.j2'

    # Real-time performance for current context
    elif (trade_data.get('active_positions', False) and
          trade_data.get('current_market_context', False)):
        return 'trade_history/twitter_real_time_performance.j2'

    # Statistical validation for strategy analysis
    elif (trade_data.get('signal_quality_data', False) and
          trade_data.get('statistical_analysis', False)):
        return 'trade_history/twitter_statistical_validation.j2'

    # Default to performance summary
    return 'trade_history/twitter_performance_summary.j2'
```

## CLI Service Integration

**Service Commands**:
```yaml
yahoo_finance_cli:
  command: "python {SCRIPTS_BASE}/yahoo_finance_cli.py"
  usage: "{command} quote {ticker} --env prod --output-format json"
  purpose: "Real-time market data for performance validation and context"
  health_check: "{command} health --env prod"
  priority: "primary"

market_data_cli:
  command: "python {SCRIPTS_BASE}/market_data_cli.py"
  usage: "{command} market-overview --env prod --output-format json"
  purpose: "Current market context and sentiment analysis"
  health_check: "{command} health --env prod"
  priority: "primary"

fred_economic_cli:
  command: "python {SCRIPTS_BASE}/fred_economic_cli.py"
  usage: "{command} indicators VIX,DXY,TNX --env prod --output-format json"
  purpose: "Economic indicators for market environment context"
  health_check: "{command} health --env prod"
  priority: "secondary"

trade_analyzer_cli:
  command: "python {SCRIPTS_BASE}/trade_analyzer_cli.py"
  usage: "{command} performance-metrics {analysis_file} --env prod"
  purpose: "Trade performance analysis and metrics calculation"
  health_check: "{command} health --env prod"
  priority: "primary"

alpha_vantage_cli:
  command: "python {SCRIPTS_BASE}/alpha_vantage_cli.py"
  usage: "{command} market-sentiment --env prod --output-format json"
  purpose: "Market sentiment validation for performance context"
  health_check: "{command} health --env prod"
  priority: "tertiary"
```

**Trade History Twitter Integration Protocol**:
```bash
# Real-time market context validation
python {SCRIPTS_BASE}/yahoo_finance_cli.py quote SPY --env prod --output-format json

# Market environment assessment
python {SCRIPTS_BASE}/market_data_cli.py market-overview --env prod --output-format json

# Trade performance analysis
python {SCRIPTS_BASE}/trade_analyzer_cli.py performance-metrics {analysis_file} --env prod

# Economic context for performance interpretation
python {SCRIPTS_BASE}/fred_economic_cli.py indicators VIX,DXY,TNX --env prod --output-format json
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  trade_history_analysis: "HIGHEST_AUTHORITY"  # Primary trade history documents
  real_time_market: "CONTEXT_AUTHORITY"  # Current market data for validation
  performance_calculations: "METRICS_AUTHORITY"  # Trade analyzer for accurate metrics
  economic_indicators: "ENVIRONMENT_AUTHORITY"  # Economic context for interpretation

conflict_resolution:
  trade_data_precedence: "analysis_document_primary"  # Trade analysis takes priority
  market_context_authority: "yahoo_finance"  # Primary source for current market
  performance_validation: "trade_analyzer_cli"  # Authoritative performance calculations
  staleness_threshold: "24_hours"  # Maximum age for market context data
  action: "validate_and_contextualize"  # Resolution strategy
```

## Data Flow & File References

**Input Sources**:
```yaml
trade_history_analysis:
  path: "{DATA_OUTPUTS}/trade_history/{ANALYSIS_FILE_NAME}_{YYYYMMDD}.md"
  format: "markdown"
  required: true
  description: "Primary trade history analysis with performance metrics and insights"

real_time_market_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Current market context for performance validation"

trade_performance_metrics:
  path: "{DATA_OUTPUTS}/trade_analysis/{ANALYSIS_FILE_NAME}_{YYYYMMDD}_metrics.json"
  format: "json"
  required: false
  description: "Calculated performance metrics and statistical analysis"

market_context_data:
  path: "CLI_SERVICES_REAL_TIME"
  format: "json"
  required: true
  description: "Market environment and sentiment for performance interpretation"

validation_file:
  path: "{DATA_OUTPUTS}/twitter/trade_history/validation/{ANALYSIS_FILE_NAME}_{YYYYMMDD}_validation.json"
  format: "json"
  required: false
  description: "Validation file for post enhancement workflow"
```

**Output Structure**:
```yaml
primary_output:
  path: "{DATA_OUTPUTS}/twitter/trade_history/{ANALYSIS_FILE_NAME}_{YYYYMMDD}.md"
  format: "markdown"
  description: "Generated trading performance Twitter content"

metadata_output:
  path: "{DATA_OUTPUTS}/twitter/trade_history/{ANALYSIS_FILE_NAME}_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Template selection and performance validation metadata"

validation_output:
  path: "{DATA_OUTPUTS}/twitter/trade_history/validation/{ANALYSIS_FILE_NAME}_{YYYYMMDD}_validation.json"
  format: "json"
  description: "Content validation results and enhancement recommendations"

blog_url_output:
  path: "{DATA_OUTPUTS}/twitter/trade_history/{ANALYSIS_FILE_NAME}_{YYYYMMDD}_blog_url.txt"
  format: "text"
  description: "Generated blog URL for full trade history analysis access"

performance_summary:
  path: "{DATA_OUTPUTS}/twitter/trade_history/{ANALYSIS_FILE_NAME}_{YYYYMMDD}_summary.json"
  format: "json"
  description: "Performance metrics summary for content tracking"
```

**Data Dependencies**:
```yaml
content_generation_flow:
  data_validation:
    - "trade history analysis loaded and validated"
    - "current market context ≤ 24 hours"
    - "performance metrics calculated and verified"
    - "market environment assessment completed"

  template_selection:
    - "trade performance data evaluation"
    - "market context integration"
    - "transparency and educational value assessment"
    - "engagement optimization criteria check"

  content_optimization:
    - "Twitter character limit compliance"
    - "performance transparency standards"
    - "educational value maximization"
    - "blog URL generation and validation"
```

## Execution Examples

### Direct Python Execution
```python
from script_registry import get_global_registry
from script_config import ScriptConfig

# Initialize
config = ScriptConfig.from_environment()
registry = get_global_registry(config)

# Execute trade history Twitter content generation
result = registry.execute_script(
    "trade_history_twitter",
    analysis_file="HISTORICAL_PERFORMANCE_REPORT",
    date="20250718",
    validate_content=True
)

# Execute with specific template override
result = registry.execute_script(
    "trade_history_twitter",
    analysis_file="TRADE_HISTORY_ANALYSIS_YTD",
    date="20250718",
    template_variant="performance_summary",
    validate_content=True
)

# Execute post enhancement from validation file
result = registry.execute_script(
    "trade_history_twitter",
    validation_file="twitter/trade_history/validation/LIVE_SIGNALS_MONITOR_20250718_validation.json"
)
```

### Command Line Execution
```bash
# Via content automation CLI
python {SCRIPTS_BASE}/content_automation_cli.py \
    --script trade_history_twitter \
    --analysis-file HISTORICAL_PERFORMANCE_REPORT \
    --date 20250718 \
    --validate-content true

# Via direct script execution
python {SCRIPTS_BASE}/base_scripts/trade_history_twitter_script.py \
    --analysis-file TRADE_HISTORY_ANALYSIS_YTD \
    --date 20250718 \
    --template-variant performance_summary

# Post enhancement workflow
python {SCRIPTS_BASE}/base_scripts/trade_history_twitter_script.py \
    --validation-file "{DATA_OUTPUTS}/twitter/trade_history/validation/LIVE_SIGNALS_MONITOR_20250718_validation.json"

# With custom market context
python {SCRIPTS_BASE}/base_scripts/trade_history_twitter_script.py \
    --analysis-file INTERNAL_TRADING_REPORTS \
    --date 20250718 \
    --market-context-override true
```

### Claude Command Execution
```
# Historical performance report
/twitter_trade_history HISTORICAL_PERFORMANCE_REPORT_20250718

# Live signals monitoring
/twitter_trade_history LIVE_SIGNALS_MONITOR_20250718

# YTD performance analysis
/twitter_trade_history TRADE_HISTORY_ANALYSIS_YTD_20250718

# Post enhancement using validation file
/twitter_trade_history {DATA_OUTPUTS}/twitter/trade_history/validation/HISTORICAL_PERFORMANCE_REPORT_20250718_validation.json

# Template-specific generation
/twitter_trade_history STRATEGY_OPTIMIZATION_ANALYSIS_20250718 template_variant=statistical_validation
```

### Trade Performance Workflow Examples
```
# Performance transparency workflow
/twitter_trade_history HISTORICAL_PERFORMANCE_REPORT_20250718

# Top trades showcase
/twitter_trade_history TRADE_HISTORY_ANALYSIS_YTD_20250718 template_variant=top_trades_showcase

# Real-time performance update
/twitter_trade_history LIVE_SIGNALS_MONITOR_20250718 template_variant=real_time_performance

# Post validation and enhancement
/twitter_trade_history HISTORICAL_PERFORMANCE_REPORT_20250718
# → If validation score <9.0, enhance using:
/twitter_trade_history {DATA_OUTPUTS}/twitter/trade_history/validation/HISTORICAL_PERFORMANCE_REPORT_20250718_validation.json
```

You are a **trade history analysis data processor** specialized in extracting performance insights from comprehensive trade history analysis and preparing structured data for the twitter_writer agent.

**Separation of Concerns:**
- **This Command**: Domain data processing, DASV compliance, template selection
- **Twitter Writer Agent**: Content creation, hooks, engagement optimization
- **Integration**: Structured data handoff for optimal trading content generation

## DASV Synthesis Framework Integration

### Trade History Input Validation
```python
def validate_trade_history_synthesis(source_path):
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

### Trade History Synthesis Confidence
```python
def calculate_trade_synthesis_confidence(source_conf, statistical_significance, sample_size):
    """Calculate trade history-specific Twitter synthesis confidence"""

    # Base confidence from source synthesis
    base_confidence = source_conf

    # Apply trade-specific factors
    statistical_validity = assess_statistical_significance()
    sample_size_adequacy = assess_trade_sample_adequacy()
    performance_transparency = assess_transparency_completeness()
    risk_disclosure_quality = assess_risk_communication_clarity()

    # Calculate trade Twitter synthesis confidence
    trade_confidence = (base_confidence *
                       statistical_validity *
                       sample_size_adequacy *
                       performance_transparency *
                       risk_disclosure_quality)

    # Enforce institutional threshold
    if trade_confidence < 0.9:
        raise SynthesisQualityException(f"Trade synthesis confidence {trade_confidence:.3f} below institutional threshold")

    return trade_confidence
```

## Trade History Data Processing Pipeline

### Domain-Specific Data Extraction
```python
def load_trade_history_synthesis(analysis_file, date):
    """Load and validate source trade history analysis synthesis"""

    source_path = f"data/outputs/trade_history/{analysis_file}_{date}.md"

    # DASV Input Validation
    validate_trade_history_synthesis(source_path)

    # Extract synthesis data
    synthesis_data = parse_trade_history_synthesis(source_path)

    # Validate trade-specific completeness
    required_sections = ['performance_summary', 'trade_analysis', 'statistical_validation', 'risk_assessment']
    validate_trade_completeness(synthesis_data, required_sections)

    return synthesis_data
```

### Trade Template Selection Logic
```python
def select_trade_template(trade_data):
    """Domain-specific template selection for trade history content"""

    # Template A: Performance Summary (YTD comprehensive metrics)
    if (trade_data.get('ytd_metrics_available', False) and
        trade_data.get('comprehensive_data', False)):
        return 'performance_summary'

    # Template B: Top Trades Showcase (Best performers highlight)
    elif (len(trade_data.get('best_trades', [])) >= 3 and
          trade_data.get('detailed_trade_data', False)):
        return 'top_trades_showcase'

    # Template C: Learning Transparency (Wins and losses balance)
    elif (trade_data.get('wins_and_losses_available', False) and
          trade_data.get('educational_focus', False)):
        return 'learning_transparency'

    # Template D: Real-Time Performance (Active positions and current context)
    elif (trade_data.get('active_positions', False) and
          trade_data.get('current_market_context', False)):
        return 'real_time_performance'

    # Template E: Statistical Validation (Strategy analysis focus)
    elif (trade_data.get('signal_quality_data', False) and
          trade_data.get('statistical_analysis', False)):
        return 'statistical_validation'

    # Default: Performance Summary
    return 'performance_summary'
```

### Market Context Integration for Trades
```python
def integrate_trade_market_context(trade_data):
    """Integrate real-time market data for trading performance context"""

    # Current market environment assessment
    current_market = collect_market_overview()

    # Validate performance context relevance
    market_regime_consistency = validate_market_regime_context(trade_data, current_market)

    # Update trade context
    trade_data['current_market_context'] = current_market['environment']
    trade_data['market_regime_validation'] = market_regime_consistency
    trade_data['performance_context_quality'] = assess_context_relevance(trade_data, current_market)

    return trade_data
```

## Twitter Writer Agent Integration

### Structured Data Handoff Protocol
```json
{
  "command_type": "trade_history",
  "synthesis_confidence": 0.94,
  "template_recommendation": "performance_summary|top_trades_showcase|learning_transparency|real_time_performance|statistical_validation",
  "analysis_file": "HISTORICAL_PERFORMANCE_REPORT",
  "date": "20250811",
  "domain_data": {
    "performance_overview": {
      "total_closed_trades": 47,
      "win_rate": 0.67,
      "ytd_return": 0.238,
      "profit_factor": 1.85,
      "avg_trade_duration": 12.4
    },
    "top_trades": [
      {"ticker": "AAPL", "return": 0.165, "duration": 8, "strategy": "SMA_10_25", "quality": "Excellent"},
      {"ticker": "MSFT", "return": 0.142, "duration": 15, "strategy": "EMA_8_21", "quality": "Good"},
      {"ticker": "GOOGL", "return": 0.128, "duration": 11, "strategy": "SMA_10_25", "quality": "Excellent"}
    ],
    "statistical_validation": {
      "signal_quality_distribution": {"excellent": 0.34, "good": 0.42, "poor": 0.24},
      "strategy_effectiveness": "SMA crossovers outperforming EMA by 3.2%",
      "sample_size_adequacy": true,
      "statistical_significance": 0.92
    },
    "risk_management": {
      "max_drawdown": 0.085,
      "avg_loss": 0.045,
      "risk_adjusted_returns": "Sharpe: 1.42, Sortino: 1.78",
      "exit_efficiency": 0.78
    },
    "learning_insights": {
      "key_lesson": "Quality ratings directly correlate with returns",
      "strategy_optimization": "SMA parameters showing consistency edge",
      "transparency_note": "Both wins and losses included for educational value"
    },
    "current_portfolio": {
      "active_positions": 3,
      "recent_signals": "2 new entries this week",
      "market_adaptation": "Adjusting to current volatility regime"
    }
  },
  "engagement_parameters": {
    "urgency": "standard",
    "audience": "active_traders",
    "complexity": "intermediate"
  },
  "compliance_requirements": {
    "disclaimers": ["past_performance", "educational_content"],
    "risk_factors": ["trading_risk", "performance_variability"],
    "transparency_level": "high"
  },
  "quality_metadata": {
    "source_confidence": 0.92,
    "statistical_significance": 0.92,
    "sample_size_adequacy": true,
    "template_rationale": "Selected performance_summary due to comprehensive YTD metrics and statistical validity"
  }
}
```

### Trade History Processing Flow
1. **Load and validate** source trade history analysis synthesis (≥9.0 confidence)
2. **Extract performance data** (returns, win rates, trade details, statistical metrics)
3. **Integrate market context** for performance validation and current relevance
4. **Select optimal template** based on data availability and educational value
5. **Calculate trade synthesis confidence** with statistical significance weighting
6. **Prepare structured data** for twitter_writer agent handoff
7. **Use the twitter_writer sub-agent** to create engaging performance content with transparency
8. **Validate output quality** and apply enhancement targeting 9.5+ if needed

## Data Extraction Protocol

### Phase 1: Performance Mining
**Extract Key Components from Trade History Analysis:**

1. **Overall Performance Metrics**
   - Total closed trades and win rate percentage
   - YTD returns and market outperformance
   - Average trade duration and profit factor
   - Best/worst performing trades with specific returns

2. **Strategy Effectiveness**
   - Primary strategy type (SMA/EMA crossovers)
   - Signal quality distribution and ratings
   - Risk-reward profile and breakeven analysis
   - Temporal patterns and optimization insights

3. **Top Trade Highlights**
   - Best performing trades with entry/exit details
   - Strategy parameters and execution quality
   - Duration and momentum capture effectiveness
   - Worst trades with lessons learned

4. **Risk Management Analysis**
   - Exit efficiency and MFE/MAE ratios
   - Position concentration and correlation
   - Quality rating distribution
   - Critical learnings and improvement areas

### Phase 2: Narrative Development
**Content Angle Selection (choose 1):**

**A. Performance Summary Angle**
- YTD returns vs market benchmarks
- Win rate and profit factor analysis
- Strategy effectiveness validation

**B. Top Trades Showcase Angle**
- Best performing trades with specifics
- Strategy execution excellence
- Momentum capture examples

**C. Learning & Improvement Angle**
- Lessons from both wins and losses
- Strategy optimization insights
- Risk management effectiveness

**D. Real-Time Performance Angle**
- Current portfolio performance
- Active signals and market context
- Strategy adaptation in current market

**E. Statistical Validation Angle**
- Signal quality and effectiveness
- Risk-reward optimization
- Performance consistency analysis

## Content Templates

### Template A: Performance Summary
```
📊 YTD Trading Performance Update:

• Total Trades: [X] completed signals
• Win Rate: [X]% ([X] wins, [X] losses)
• YTD Return: +[X]% on closed positions
• Profit Factor: [X.XX]
• Avg Trade Duration: [X] days

Strategy: [Primary strategy description]

Top performer: $[TICKER] +[X]% ([X] days)
Biggest lesson: $[TICKER] -[X]% ([learning])

Beating [strategy requirement] breakeven threshold ✅

📋 Full analysis: [Analysis URL]

#TradingResults #PortfolioUpdate #TradingStrategy
```

### Template B: Top Trades Showcase
```
🏆 Best trades from recent closed positions:

🥇 $[TICKER]: +[X]% in [X] days
   Strategy: [SMA/EMA parameters]
   Quality: [Rating]

🥈 $[TICKER]: +[X]% in [X] days
   Strategy: [SMA/EMA parameters]
   Quality: [Rating]

🥉 $[TICKER]: +[X]% in [X] days
   Strategy: [SMA/EMA parameters]
   Quality: [Rating]

Combined return: +[X]% across [X] days avg

Key insight: [Strategy effectiveness observation]

📋 Full analysis: [Analysis URL]

#TopTrades #TradingWins #MomentumCapture
```

### Template C: Learning & Transparency
```
📈 Trading transparency update - both wins & losses:

Winners ([X] trades):
• Avg return: +[X]%
• Avg duration: [X] days
• Best strategy: [Parameters]

Losers ([X] trades):
• Avg loss: -[X]%
• Avg duration: [X] days
• Key lesson: [Learning]

Current profit factor: [X.XX]
Win rate: [X]% (vs [X]% needed)

Strategy evolution: [Optimization insight]

This is how we improve 📊

📋 Full analysis: [Analysis URL]

#TradingTransparency #TradingEducation #ContinuousImprovement
```

### Template D: Real-Time Performance
```
🔥 Live trading performance check:

Active positions: [X] signals
YTD closed: +[X]% ([X] trades)
Current portfolio: [Status description]

Recent exits:
• $[TICKER]: +[X]% ([Strategy])
• $[TICKER]: +[X]% ([Strategy])

Active signals showing: [Market context]
Strategy adaptation: [Current focus]

Market conditions: [Current environment]

Time to [action/observation] 🎯

📋 Full analysis: [Analysis URL]

#LiveTrading #TradingSignals #MarketUpdate
```

### Template E: Statistical Validation
```
🔍 Strategy validation update:

Signal Quality Distribution:
• Excellent: [X]% ([X] trades)
• Good: [X]% ([X] trades)
• Poor: [X]% ([X] trades)

Quality correlation:
• Excellent trades: +[X]% avg return
• Poor trades: [X]% avg return

Statistical insight: [Key finding]

Strategy optimization: [Focus area]

Data doesn't lie 📊

📋 Full analysis: [Analysis URL]

#TradingStatistics #StrategyValidation #DataDriven
```

## Content Optimization Guidelines

### Engagement Mechanics
1. **Lead with Performance**: Specific percentages, trade counts, win rates
2. **Show Transparency**: Include both wins and losses for credibility
3. **Use Emojis Strategically**: 1-2 relevant emojis max for visual appeal
4. **Create Educational Value**: Share insights that help followers learn
5. **Include Specific Examples**: Real trades with real results

### Writing Style Requirements
- **Plain Language**: No jargon without explanation
- **Active Voice**: "Strategy delivered" not "Strategy was delivering"
- **Specific Claims**: "+16.58% return" not "significant return"
- **Present Tense**: Create immediacy and relevance
- **Confident Tone**: Back analysis with actual trade data

### Character Count Optimization
- **Target Length**: 280 characters per tweet (can thread if needed)
- **Tweet 1**: Hook + core performance metrics
- **Tweet 2** (if needed): Supporting trade examples
- **Tweet 3** (if needed): Insights/lessons/next steps

## Quality Assurance Protocol

### Content Validation
- [ ] **Current Market Context**: Real-time validation of market conditions
- [ ] **Accuracy**: All numbers match source analysis exactly
- [ ] **Trade Attribution**: Specific trades referenced correctly
- [ ] **Analysis URL Generated**: URL follows established pattern
- [ ] **Performance Transparency**: Both wins and losses represented fairly
- [ ] **Completeness**: Key insights fully explained
- [ ] **Educational Value**: Content teaches something valuable
- [ ] **Engagement**: Hook creates discussion potential

### Data Integrity
- [ ] **Trade Data Accuracy**: All trade results verified against analysis
- [ ] **Metric Consistency**: Performance calculations validated
- [ ] **Date Verification**: Entry/exit dates and durations correct
- [ ] **Strategy Attribution**: Correct strategy parameters referenced
- [ ] **Quality Ratings**: Trade quality assessments included accurately

### Risk Management
- [ ] **Disclaimer Implied**: Performance presented as historical results
- [ ] **No Guarantees**: Language avoids promises of future returns
- [ ] **Educational Context**: Presented as learning/transparency exercise
- [ ] **Balanced Perspective**: Both successes and failures acknowledged

### Output Verification
- [ ] **Character Count**: Within Twitter limits
- [ ] **Hashtag Strategy**: 2-4 relevant hashtags maximum
- [ ] **Call to Action**: Clear value proposition for reader
- [ ] **Thread Cohesion**: If multi-tweet, logical flow maintained

## Export Protocol

**REQUIRED: Save Twitter-ready content to:**
```
./data/outputs/twitter/trade_history/{ANALYSIS_FILE_NAME}_{YYYYMMDD}.md
```

**File contains:**
- Clean X post content ready for copy/paste
- Character count for each tweet
- Selected template rationale
- Key insights extracted from source analysis
- Generated analysis URL for full report access

### Analysis URL Generation

**URL Pattern:** Convert analysis file identifier to blog post URL
- **Input format:** `{ANALYSIS_FILE_NAME}_{YYYYMMDD}`
- **Output format:** `https://www.colemorton.com/blog/[analysis-name]-[yyyymmdd]/`
- **Example conversion:** `HISTORICAL_PERFORMANCE_REPORT_20250626` → `https://www.colemorton.com/blog/historical-performance-report-20250626/`

**Conversion Rules:**
1. Convert analysis name to lowercase with hyphens
2. Keep date format as YYYYMMDD
3. Use hyphen separators in URL path
4. Include trailing slash

**Analysis attribution note:**
```
Based on comprehensive trade history analysis: {ANALYSIS_FILE_NAME}_{YYYYMMDD}.md
Performance metrics: [Key stats] | Data quality: [Rating]
Full analysis link: https://www.colemorton.com/blog/[analysis-name-yyyymmdd]/
```

## Command Usage

**Execute Twitter synthesis from trade history analysis:**
```
/twitter_trade_history {ANALYSIS_FILE_NAME}_{YYYYMMDD}
```

**Examples:**
- `/twitter_trade_history HISTORICAL_PERFORMANCE_REPORT_20250811`
- `/twitter_trade_history LIVE_SIGNALS_MONITOR_20250811`
- `/twitter_trade_history TRADE_HISTORY_ANALYSIS_YTD_20250811`

**DASV Processing Flow:**
1. **Load & validate** source trade history analysis synthesis (≥9.0 confidence)
2. **Extract performance data** (trades, returns, statistical metrics, risk data)
3. **Integrate market context** for current relevance and performance validation
4. **Validate statistical significance** and sample size adequacy requirements
5. **Select optimal template** based on data availability and transparency focus
6. **Calculate trade synthesis confidence** with DASV standards
7. **Use twitter_writer sub-agent** to create engaging performance content with educational value
8. **Apply enhancement** if validation file exists (target: ≥9.5 confidence)
9. **Export results** with complete trading performance metrics and transparency

**Enhancement Workflow:**
```
# Phase 1: Generate trade history Twitter synthesis
/twitter_trade_history HISTORICAL_PERFORMANCE_REPORT_20250811

# Phase 2: If synthesis confidence <9.5, apply validation enhancement
/twitter_trade_history {DATA_OUTPUTS}/twitter/trade_history/validation/HISTORICAL_PERFORMANCE_REPORT_20250811_validation.json

# Phase 3: Validate institutional excellence achieved (≥9.5/10.0)
```

---

## MANDATORY WORKFLOW REMINDER

⚠️ **CRITICAL FIRST STEP**: Before processing any analysis, ALWAYS validate current market context using Yahoo Finance MCP server. Example:
```
Use: MCP Tool get_stock_fundamentals(\"SPY\") for market overview
Extract: market sentiment, major index performance, sector rotation
Validate: current trading environment context
```

**Always provide current market context to make historical trading performance relevant to today's conditions.**

**Unified System Integration:**
- All processing handled through TwitterCommandProcessor
- Automatic validation using UnifiedValidationFramework
- Enhancement detection and application via SharedEnhancementProtocol
- Standardized output with UnifiedDataSchema compliance

## Post-Execution Protocol

### Required Actions
1. **Generate Output Metadata**: Include collaboration metadata for social content
2. **Store Outputs**: Save to `./data/outputs/twitter/trade_history/` directories
3. **Quality Validation**: Ensure content accuracy and market context relevance
4. **Content Tracking**: Record content performance metrics

### Output Metadata Template
```yaml
metadata:
  generated_by: "twitter-trade-history"
  timestamp: "{ISO-8601-timestamp}"
  analysis_source: "{source-file}"
  content_type: "trading_performance_post"

content_metrics:
  character_count: "{post-length}"
  engagement_optimized: true
  performance_data_verified: true
  market_context_current: true

quality_assurance:
  data_accuracy_verified: true
  transparency_maintained: true
  educational_value: true
```

---

## DASV Architecture Benefits

**Clean Separation of Concerns**:
- **Domain Focus**: Command handles trade history data processing and statistical validation
- **Content Delegation**: Twitter_writer sub-agent handles all content creation and engagement optimization
- **Quality Assurance**: DASV framework ensures institutional trading performance standards
- **Enhancement Protocol**: Systematic improvement targeting 9.5+ confidence with transparency requirements

**Trade-Specific Quality Standards**:
- **Source Validation**: ≥9.0/10.0 synthesis confidence required
- **Statistical Significance**: ≥0.9 significance requirement for performance claims
- **Sample Size Adequacy**: Minimum trade count validation for reliability
- **Transparency Requirements**: Both wins and losses included for educational authenticity

**Integration Excellence**:
- **Twitter Writer**: Structured trading data handoff for optimal performance content
- **Market Context**: Real-time validation for performance relevance and current conditions
- **Enhancement Loop**: Validation-driven improvement targeting institutional excellence
- **Audit Trail**: Complete trading performance metrics and decision rationale

**Ready to generate DASV-compliant Twitter synthesis from institutional-grade trade history analysis. Provide {ANALYSIS_FILE_NAME}_{YYYYMMDD} identifier to begin trade-focused data processing and twitter_writer integration.**
