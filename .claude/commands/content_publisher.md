# Content Publisher

Transform analytical insights from data pipeline outputs into publication-ready blog content for the "Cole Morton" frontend.
Specializes in content synchronization between `data/outputs/` and `frontend/src/content/` with quality assurance and asset coordination.

**Multi-Content Type Support**: Handles both fundamental analysis and trade history reports with content-specific publication workflows.

## Core Product Command Profile

**Type**: Core Product Command (User-facing AI functionality)

## Purpose

Systematically manages the content publication pipeline by discovering unpublished analysis content, coordinating visual assets, and publishing analytical content with **absolute content fidelity** to maintain the integrity and accuracy of financial analysis while ensuring quality publication standards throughout the Sensylate content ecosystem.

### Content Fidelity Mandate

**CRITICAL**: This command serves as a faithful custodian of analytical content. The primary responsibility is preserving 100% content accuracy without any transformation, summarization, or editorial modification. The only permitted change is removing the H1 title heading to prevent duplication with frontmatter titles.

**Output Location**: Published content in `frontend/src/content/blog/` with supporting assets in `frontend/public/images/`

## Content Pipeline Management

### Content Discovery & Assessment
```
CONTENT AUDIT PROTOCOL:
1. Scan @data/outputs/fundamental_analysis/ for unpublished fundamental analysis markdown files
2. Scan @data/outputs/analysis_trade_history/ for unpublished trade history reports
3. Scan @data/outputs/sector_analysis/ for unpublished sector analysis markdown files
4. Check @frontend/src/content/blog/ for existing publications
5. Identify content gaps and publication opportunities across all content types
6. Assess content quality and readiness for publication
7. Prioritize content by relevance, timeliness, and audience value
```

### Asset Management & Synchronization
```
ASSET COORDINATION WORKFLOW:
1. Map analysis files to corresponding visualizations in @data/images/
   → tradingview/ - Trading charts and technical analysis
   → trendspider_full/ - Comprehensive market analysis charts
   → trendspider_tabular/ - Data visualization tables
   → sector_analysis/ - Sector-specific charts and comparative analysis
2. Verify image availability and quality standards
3. Copy/optimize images to @frontend/public/images/
   → Maintain directory structure: tradingview/, trendspider_full/, trendspider_tabular/, sector_analysis/
4. Validate image paths and accessibility
5. Ensure consistent asset naming and organization
   → Sector analysis: {sector-slug}_{YYYYMMDD}.png format
```

### Content Transformation
```
ASTRO CONTENT CONVERSION - CRITICAL CONTENT FIDELITY RULES:
1. **NEVER TRANSFORM SOURCE CONTENT**: Content from @data/outputs/fundamental_analysis/ and @data/outputs/analysis_trade_history/ must be preserved 100% without any modifications, summarization, or editorial changes
2. **ONLY REMOVE TITLE HEADING**: Remove the H1 title heading (e.g., "# Company Name - Fundamental Analysis" or "# Historical Trading Performance - Closed Positions") to prevent duplication with frontmatter title
3. **PRESERVE ALL ANALYSIS CONTENT**: Maintain exact confidence scores, data quality metrics, investment recommendations, financial data, trading performance metrics, and methodology
4. **ADD FRONTMATTER ONLY**: Add proper frontmatter with metadata, SEO data, tags, categories without altering content body
5. **MAINTAIN ANALYTICAL INTEGRITY**: Preserve the analytical voice, formatting, tables, bullet points, and structure exactly as generated
6. **NO CONTENT OPTIMIZATION**: Do not modify content for "web readability" - analytical accuracy takes precedence over accessibility
```

### Publication & Validation
```
FRONTEND INTEGRATION:
1. Publish content to @frontend/src/content/blog/
2. Validate content rendering on development server
3. Test image display and responsive behavior
4. Verify cross-references and internal links
5. Confirm search functionality includes new content
6. Validate SEO metadata and social sharing
```

## Fundamental Analysis Standard Template

### MANDATORY FRONTMATTER TEMPLATE

All fundamental analysis posts MUST use this exact template with NO deviations:

```yaml
---
title: "{Company Name} ({TICKER}) - Fundamental Analysis"
meta_title: "{Company Name} ({TICKER}) Fundamental Analysis - {RATING} Rating"
description: "Comprehensive fundamental analysis of {Company Name} ({TICKER}) with {RATING} recommendation. Fair value ${LOW}-${HIGH} vs current ${CURRENT}. {Brief investment thesis 1-2 sentences}."
date: {YYYY-MM-DD}T{HH:MM:SS}Z
image: "/images/tradingview/{TICKER}_{YYYYMMDD}.png"
authors: ["Cole Morton", "Claude"]
categories: ["Investing", "Analysis", "Fundamental Analysis", "{Sector}", "{Industry}"]
tags: ["{ticker-lowercase}", "fundamental-analysis", "{rating-lowercase}", "{sector-tag}", "{key-theme-1}", "{key-theme-2}"]
draft: false
---
```

### STRICT STANDARDIZATION RULES

#### Title Standards
- **Format**: `{Company Name} ({TICKER}) - Fundamental Analysis`
- **Remove**: ALL ratings, returns, and specific themes from title
- **Example**: `"Amazon.com Inc. (AMZN) - Fundamental Analysis"`

#### Meta_title Standards
- **Always include** for SEO optimization
- **Format**: `{Company Name} ({TICKER}) Fundamental Analysis - {RATING} Rating`
- **Example**: `"Amazon (AMZN) Fundamental Analysis - BUY Rating"`

#### Description Standards
- **Length**: 150-200 characters
- **Include**: Rating, fair value range, current price, key thesis
- **Template**: `"Comprehensive fundamental analysis of {Company} ({TICKER}) with {RATING} recommendation. Fair value ${LOW}-${HIGH} vs current ${CURRENT}. {Investment thesis}."`

#### Date Standards
- **Format**: ISO 8601 with timezone `YYYY-MM-DDTHH:MM:SSZ`
- **Example**: `2025-07-02T10:00:00Z`
- **Required**: Must include timezone Z suffix

#### Authors Standards
- **Field**: Use `authors` (NOT `author`)
- **Value**: `["Cole Morton", "Claude"]` (EXACT format)
- **Required**: Present in ALL posts

#### Categories Standards
- **Order**: `["Investing", "Analysis", "Fundamental Analysis", "{Sector}", "{Industry}"]`
- **Count**: Exactly 5 categories
- **Sectors**: Technology, Healthcare, Financial Services, Consumer Discretionary, Industrials, etc.
- **Industries**: Specific industry within sector

#### Tags Standards
- **Ticker**: ALWAYS lowercase (`amzn`, NOT `AMZN`)
- **Required**: `"fundamental-analysis"` in ALL posts
- **Rating**: Include rating tag (`"buy"`, `"hold"`, `"sell"`)
- **Count**: 5-7 tags maximum
- **Format**: Lowercase with hyphens

#### Image Standards
- **Path**: `/images/tradingview/{TICKER}_{YYYYMMDD}.png`
- **Ticker**: Uppercase in filename
- **Date**: Match publication date exactly

### STANDARDIZATION VALIDATION PROTOCOL

**MANDATORY PRE-PUBLICATION CHECKS**: Every fundamental analysis post MUST pass ALL validation checks before publication:

```
FRONTMATTER COMPLIANCE VALIDATION:
□ **TITLE FORMAT**: Exact format "{Company Name} ({TICKER}) - Fundamental Analysis"
□ **META_TITLE PRESENCE**: Must exist with rating information
□ **DESCRIPTION LENGTH**: 150-200 characters with required elements
□ **DATE FORMAT**: ISO 8601 with timezone (YYYY-MM-DDTHH:MM:SSZ)
□ **AUTHORS FORMAT**: Exact format ["Cole Morton", "Claude"]
□ **CATEGORIES STRUCTURE**: Exact format ["Investing", "Analysis", "Fundamental Analysis", "{Sector}", "{Industry}"]
□ **TAGS COMPLIANCE**: Lowercase ticker + "fundamental-analysis" + rating + themes
□ **IMAGE PATH**: Correct format with uppercase ticker and matching date
□ **DRAFT STATUS**: Set to false for publication
```

**AUTOMATIC REJECTION**: Any post that fails validation MUST be corrected before publication. No exceptions.

**STANDARDIZATION ENFORCEMENT**: The content_publisher command will automatically verify and correct any frontmatter issues to ensure 100% compliance with the standard template.

**CRITICAL COMPLIANCE NOTE**: All existing fundamental analysis posts have been standardized to this template. The content_publisher command MUST maintain this standardization for all future publications and validate existing content against these rules.

## Sector Analysis Standard Template

### MANDATORY FRONTMATTER TEMPLATE

All sector analysis posts MUST use this exact template with NO deviations:

```yaml
---
title: "{Sector Name} Sector Analysis - {Month} {YYYY}"
meta_title: "{Sector Name} Sector Analysis - {RECOMMENDATION} Rating | {Month} {YYYY}"
description: "Comprehensive {Sector Name} sector analysis with {RECOMMENDATION} recommendation. Fair value ${LOW}-${HIGH} with {CONFIDENCE}% confidence. {Brief sector thesis 1-2 sentences}."
date: {YYYY-MM-DD}T{HH:MM:SS}Z
image: "/images/sector_analysis/{sector-slug}_{YYYYMMDD}.png"
authors: ["Cole Morton", "Claude"]
categories: ["Investing", "Analysis", "Sector Analysis", "{Sector}", "Market Analysis"]
tags: ["{sector-slug}", "sector-analysis", "{recommendation-lowercase}", "{economic-indicator}", "{key-theme-1}", "{key-theme-2}"]
draft: false
sector_data:
  confidence: {0.XX}
  data_quality: {0.XX}
  economic_context: "{Current/Expansion/Contraction}"
  recommendation: "{BUY/HOLD/SELL}"
  position_size: "{XX-XX%}"
  fair_value_range: "${XX.XX} - ${XX.XX}"
  expected_return: "{XX.X%}"
  risk_score: "{X.X/5.0}"
---
```

### STRICT STANDARDIZATION RULES

#### Title Standards
- **Format**: `{Sector Name} Sector Analysis - {Month} {YYYY}`
- **Remove**: ALL specific ratings, returns, and complex themes from title
- **Example**: `"Technology Sector Analysis - July 2025"`

#### Meta_title Standards
- **Always include** for SEO optimization
- **Format**: `{Sector Name} Sector Analysis - {RECOMMENDATION} Rating | {Month} {YYYY}`
- **Example**: `"Technology Sector Analysis - BUY Rating | July 2025"`

#### Description Standards
- **Length**: 150-200 characters
- **Include**: Recommendation, fair value range, confidence level, key thesis
- **Template**: `"Comprehensive {Sector} sector analysis with {RECOMMENDATION} recommendation. Fair value ${LOW}-${HIGH} with {CONFIDENCE}% confidence. {Sector thesis}."`

#### Date Standards
- **Format**: ISO 8601 with timezone `YYYY-MM-DDTHH:MM:SSZ`
- **Example**: `2025-07-10T10:00:00Z`
- **Required**: Must include timezone Z suffix

#### Authors Standards
- **Field**: Use `authors` (NOT `author`)
- **Value**: `["Cole Morton", "Claude"]` (EXACT format)
- **Required**: Present in ALL posts

#### Categories Standards
- **Order**: `["Investing", "Analysis", "Sector Analysis", "{Sector}", "Market Analysis"]`
- **Count**: Exactly 5 categories
- **Sectors**: Technology, Healthcare, Finance, Energy, Consumer Discretionary, etc.
- **Required**: "Market Analysis" as 5th category

#### Tags Standards
- **Sector**: ALWAYS lowercase with hyphens (`technology`, `healthcare`, `finance`)
- **Required**: `"sector-analysis"` in ALL posts
- **Recommendation**: Include recommendation tag (`"buy"`, `"hold"`, `"sell"`)
- **Economic**: Include economic indicator tag (`"mid-cycle"`, `"expansion"`, `"contraction"`)
- **Count**: 5-7 tags maximum
- **Format**: Lowercase with hyphens

#### Image Standards
- **Path**: `/images/sector_analysis/{sector-slug}_{YYYYMMDD}.png`
- **Sector**: Lowercase with hyphens in filename
- **Date**: Match publication date exactly

#### Sector Data Standards
- **Confidence**: Decimal format (0.XX) matching source analysis
- **Data Quality**: Decimal format (0.XX) matching source analysis
- **Economic Context**: One of "Current", "Expansion", "Contraction"
- **Recommendation**: One of "BUY", "HOLD", "SELL"
- **Position Size**: Percentage range format "XX-XX%"
- **Fair Value Range**: Dollar range format "${XX.XX} - ${XX.XX}"
- **Expected Return**: Percentage format with decimal "XX.X%"
- **Risk Score**: Decimal format "X.X/5.0"

### STANDARDIZATION VALIDATION PROTOCOL

**MANDATORY PRE-PUBLICATION CHECKS**: Every sector analysis post MUST pass ALL validation checks before publication:

```
FRONTMATTER COMPLIANCE VALIDATION:
□ **TITLE FORMAT**: Exact format "{Sector Name} Sector Analysis - {Month} {YYYY}"
□ **META_TITLE PRESENCE**: Must exist with recommendation information
□ **DESCRIPTION LENGTH**: 150-200 characters with required elements
□ **DATE FORMAT**: ISO 8601 with timezone (YYYY-MM-DDTHH:MM:SSZ)
□ **AUTHORS FORMAT**: Exact format ["Cole Morton", "Claude"]
□ **CATEGORIES STRUCTURE**: Exact format ["Investing", "Analysis", "Sector Analysis", "{Sector}", "Market Analysis"]
□ **TAGS COMPLIANCE**: Lowercase sector + "sector-analysis" + recommendation + economic indicator + themes
□ **IMAGE PATH**: Correct format with lowercase sector slug and matching date
□ **SECTOR DATA STRUCTURE**: Complete sector_data object with all required fields
□ **CONFIDENCE SCORES**: Decimal format matching source analysis confidence and data quality
□ **ECONOMIC CONTEXT**: Valid economic context matching source analysis
□ **DRAFT STATUS**: Set to false for publication
```

**AUTOMATIC REJECTION**: Any post that fails validation MUST be corrected before publication. No exceptions.

**STANDARDIZATION ENFORCEMENT**: The content_publisher command will automatically verify and correct any frontmatter issues to ensure 100% compliance with the sector analysis standard template.

## Content Standards & Quality Gates

### Publication Requirements

#### Fundamental Analysis Content
- **Naming Convention**: `[ticker]-fundamental-analysis-[YYYYMMDD].md`
- **Frontmatter Schema**: MANDATORY compliance with Fundamental Analysis Standard Template
- **Tag Taxonomy**: STRICT adherence to standardized tag structure (see Standard Template below)

#### Sector Analysis Content
- **Naming Convention**: `[sector-slug]-sector-analysis-[YYYYMMDD].md`
- **Frontmatter Schema**: MANDATORY compliance with Sector Analysis Standard Template
- **Tag Taxonomy**: STRICT adherence to standardized tag structure (see Sector Analysis Standard Template)

#### Trade History Reports
- **Naming Convention**: `trading-performance-[report-type]-[YYYYMMDD].md`
- **Frontmatter Schema**: Performance-focused blog post structure
- **Tag Taxonomy**: Use categories (trading-performance, trade-history, signals, analysis)

#### Universal Requirements
- **Image Integration**: Consistent paths to `/images/tradingview/`, `/images/trendspider_full/`, or `/images/sector_analysis/`
- **SEO Optimization**: Complete titles, descriptions, tags, and metadata
- **MANDATORY COMPLIANCE**: All frontmatter MUST follow respective Standard Templates (Fundamental Analysis, Sector Analysis, or Trade History)

### Quality Assurance Checklist
```
PRE-PUBLICATION VALIDATION - CONTENT FIDELITY ENFORCEMENT:
□ **CONTENT FIDELITY**: Source content preserved 100% without any transformations
□ **TITLE REMOVAL ONLY**: H1 title heading removed, all other content identical to source
□ **ANALYTICAL INTEGRITY**: All confidence scores, data quality metrics, recommendations, and trading performance metrics exactly as generated
□ **FINANCIAL DATA ACCURACY**: Investment thesis, valuations, risk assessments, trading results, and methodology unchanged
□ **PERFORMANCE DATA INTEGRITY**: Win rates, profit factors, trade durations, and statistical analysis preserved exactly
□ **SECTOR ANALYSIS INTEGRITY**: Economic indicators, correlation data, sector performance metrics, and risk assessments preserved exactly
□ **ECONOMIC DATA ACCURACY**: GDP correlations, employment sensitivity, interest rate impacts, and economic cycle analysis unchanged
□ **FORMATTING PRESERVATION**: Tables, bullet points, section structure, and emphasis maintained exactly
□ **NO EDITORIAL CHANGES**: Zero summarization, optimization, or content modifications applied
□ **FRONTMATTER COMPLIANCE**: MANDATORY adherence to respective Standard Templates (Fundamental Analysis, Sector Analysis, or Trade History)
□ **AUTHOR STANDARDIZATION**: Must use authors: ["Cole Morton", "Claude"]
□ **CATEGORY STANDARDIZATION**: Must use proper category structure per content type
□ **TAG STANDARDIZATION**: Must use lowercase identifiers + standardized tag structure per content type
□ **DATE STANDARDIZATION**: Must use ISO 8601 with timezone format
□ **TITLE STANDARDIZATION**: Must use clean format without ratings/returns per content type
□ **META_TITLE STANDARDIZATION**: Must include rating information in standardized format per content type
□ **SECTOR DATA VALIDATION**: For sector analysis, must include complete sector_data object with confidence scores
□ All referenced images properly linked and accessible
□ SEO metadata complete and optimized (frontmatter only)
□ Proper categorization and tagging applied (frontmatter only)
□ Cross-references validated and functional
□ Mobile responsiveness confirmed
□ Development server rendering verified
```

### Post-Publication Verification
```
INTEGRATION VALIDATION:
□ Content displays correctly on frontend
□ Images render properly across devices
□ Internal linking functions correctly
□ Search functionality includes new content
□ Analytics tracking implemented
□ Social sharing metadata functional
```

## Current Content State Management

### Published Content Tracking
Monitor existing publications in `@frontend/src/content/blog/`:
- Track publication dates and content freshness
- Identify opportunities for content updates
- Maintain publication calendar and content gaps
- Monitor audience engagement and content performance

### Content Publication Queue
Systematically process unpublished analysis for publication opportunities and content pipeline optimization.

## Publication Metrics & Success Criteria

### Content Quality Metrics
- **Content Fidelity Score**: 100% preservation of source analytical content (mandatory)
- **Publication Readiness Score**: Comprehensive assessment of content completeness
- **Asset Integration Rate**: Percentage of content with proper visual assets
- **SEO Optimization Score**: Metadata completeness and search optimization
- **Cross-Reference Density**: Internal linking and content interconnection

### Performance Indicators
- **Publication Velocity**: Time from analysis to published content
- **Content Freshness**: Timeliness of market analysis publication
- **Audience Engagement**: Reader interaction and content sharing
- **Search Performance**: Organic discovery and keyword ranking

## Integration Requirements

### Data Pipeline Coordination
- Monitor `@data/outputs/` for new analysis content
- Coordinate with analysis generation commands for publication timing
- Maintain content freshness through automated discovery

### Frontend Platform Integration
- Ensure compatibility with Astro 5.7+ framework requirements
- Maintain TailwindCSS 4+ styling consistency
- Support TypeScript type safety and React component integration
- Validate MDX content authoring and shortcode functionality

### Quality Enforcement
- Enforce comprehensive pre-commit quality standards
- Maintain publication consistency with established style guide
- Validate cross-platform compatibility and responsive design
- Ensure SEO optimization and social media integration

## Usage Examples

```bash
# Complete content discovery and publication workflow
/content_publisher

# Audit specific content type for publication opportunities
/content_publisher content_type=fundamental_analysis
/content_publisher content_type=trade_history
/content_publisher content_type=sector_analysis

# Publish specific analysis with priority handling
/content_publisher ticker=AAPL priority=high
/content_publisher report_type=historical_performance priority=high
/content_publisher sector=technology priority=high
/content_publisher sector=finance priority=high

# Asset synchronization and optimization only
/content_publisher mode=assets_only

# Quality assurance and validation check
/content_publisher mode=validation_only

# Multi-content type processing
/content_publisher content_type=all scope=comprehensive
```

This content publisher command ensures Sensylate maintains high-quality, consistent content publication with **absolute analytical integrity** - preserving 100% content fidelity while adding proper web infrastructure (frontmatter, images, navigation). This approach maintains the trust and accuracy that readers depend on for investment decisions while integrating seamlessly with the team workspace collaboration framework.

## Trade History Report Management

### Trade History Content Types

**HISTORICAL_PERFORMANCE_REPORT**: Comprehensive analysis of closed trading positions
- **Content Structure**: Performance metrics, trade analysis, quality distribution, temporal analysis
- **Key Metrics**: Win rate, profit factor, average returns, risk-reward profiles
- **Publication Priority**: High - provides validated trading system performance data

**INTERNAL_TRADING_REPORT**: Internal trading system analysis and optimization insights
- **Content Structure**: System performance, signal quality, operational metrics
- **Key Metrics**: Signal accuracy, execution efficiency, system reliability
- **Publication Priority**: Medium - technical insights for trading system development

**LIVE_SIGNALS_MONITOR**: Real-time signal monitoring and market analysis
- **Content Structure**: Current signals, market conditions, real-time analysis
- **Key Metrics**: Active signals, market sentiment, timing analysis
- **Publication Priority**: High - time-sensitive market insights

### Trade History Publication Workflow

```
TRADE HISTORY SPECIFIC PIPELINE:
1. **Content Discovery**: Scan @data/outputs/analysis_trade_history/ for unpublished reports
2. **Report Classification**: Identify report type (HISTORICAL, INTERNAL, LIVE_SIGNALS)
3. **Asset Mapping**: Link to performance charts and trading visualizations
4. **Schema Application**: Apply trading-specific frontmatter templates
5. **Fidelity Preservation**: Maintain 100% accuracy of trading metrics and analysis
6. **Publication**: Deploy to @frontend/src/content/blog/ with trading categories
7. **Validation**: Verify trading data accuracy and chart accessibility
```

### Trade History Quality Gates

```
TRADING CONTENT VALIDATION:
□ **PERFORMANCE METRICS ACCURACY**: Win rates, profit factors, return percentages exactly preserved
□ **TRADE DATA INTEGRITY**: Entry/exit dates, prices, durations, and tickers unchanged
□ **STATISTICAL ANALYSIS PRESERVATION**: Quality distributions, temporal analysis, strategy performance maintained
□ **RISK ASSESSMENT FIDELITY**: Risk-reward profiles, drawdown analysis, volatility metrics preserved
□ **METHODOLOGY DOCUMENTATION**: Trading system logic and signal generation process unchanged
□ **VISUAL ASSET COORDINATION**: Performance charts and trading visualizations properly linked
```

## Content Fidelity Enforcement

**ZERO TOLERANCE POLICY**: Any transformation, summarization, optimization, or editorial modification of source analytical content is strictly prohibited. The content publisher role is to be a faithful custodian, not an editor, ensuring that:

1. **Investment Recommendations**: BUY/SELL/HOLD ratings remain exactly as generated
2. **Confidence Scores**: All analytical confidence metrics preserved precisely
3. **Financial Data**: Valuations, price targets, and risk assessments unchanged
4. **Trading Performance Data**: Win rates, profit factors, trade statistics, and performance metrics unchanged
5. **Methodology**: Analysis methodology and data sources maintained verbatim
6. **Author Voice**: Analytical voice and technical language preserved completely

This ensures readers receive the exact analytical output generated by both the fundamental analysis system and trade history analysis system, maintaining credibility and accuracy in all financial content publication.

## Sector Analysis Content Management

### Sector Analysis Content Types

**SECTOR_ANALYSIS_REPORT**: Comprehensive cross-sector analysis with economic integration
- **Content Structure**: Economic sensitivity matrix, market positioning, valuation framework, risk assessment
- **Key Metrics**: GDP correlation, employment sensitivity, interest rate impacts, sector rotation scores
- **Publication Priority**: High - provides strategic sector allocation guidance

**SECTOR_COMPARATIVE_ANALYSIS**: Multi-sector comparison with relative performance metrics
- **Content Structure**: Cross-sector valuations, performance attribution, risk-adjusted returns
- **Key Metrics**: Relative P/E ratios, sector betas, correlation analysis, momentum indicators
- **Publication Priority**: Medium - tactical sector rotation insights

**SECTOR_THEMATIC_ANALYSIS**: Sector-specific thematic deep dives with catalyst identification
- **Content Structure**: Industry dynamics, competitive positioning, regulatory environment, innovation trends
- **Key Metrics**: Market share analysis, R&D intensity, regulatory impact scores, disruptive risk assessment
- **Publication Priority**: Medium - long-term sector positioning insights

### Sector Analysis Publication Workflow

```
SECTOR ANALYSIS SPECIFIC PIPELINE:
1. **Content Discovery**: Scan @data/outputs/sector_analysis/ for unpublished sector reports
2. **Report Classification**: Identify sector type (Technology, Healthcare, Finance, Energy, etc.)
3. **Asset Mapping**: Link to sector charts, economic indicators, and comparative visualizations
4. **Schema Application**: Apply sector-specific frontmatter templates with confidence scores
5. **Fidelity Preservation**: Maintain 100% accuracy of economic data, correlations, and risk assessments
6. **Publication**: Deploy to @frontend/src/content/blog/ with sector analysis categories
7. **Validation**: Verify economic data accuracy and sector-specific chart accessibility
```

### Sector Analysis Quality Gates

```
SECTOR ANALYSIS CONTENT VALIDATION:
□ **ECONOMIC DATA ACCURACY**: GDP correlations, employment sensitivity, interest rate impacts exactly preserved
□ **SECTOR METRICS INTEGRITY**: P/E ratios, sector betas, performance attribution, and risk metrics unchanged
□ **CORRELATION ANALYSIS PRESERVATION**: Cross-sector correlations, VIX relationships, and economic sensitivity maintained
□ **CONFIDENCE SCORE FIDELITY**: Analysis confidence and data quality metrics preserved exactly
□ **METHODOLOGY DOCUMENTATION**: Economic integration methodology and data sources unchanged
□ **SECTOR DATA OBJECT COMPLETION**: Complete sector_data frontmatter with all required fields
□ **VISUAL ASSET COORDINATION**: Sector charts and comparative visualizations properly linked
□ **ECONOMIC CONTEXT ACCURACY**: Current economic cycle positioning and recession probabilities preserved
```

## Multi-Content Type Integration

### Unified Content Pipeline

The content_publisher command now supports three distinct content types with unified quality standards:

1. **Fundamental Analysis**: Company-specific investment analysis with valuation models
2. **Trade History Reports**: Trading performance analysis with statistical validation
3. **Sector Analysis**: Sector-level strategic analysis with economic integration

### Content Type Detection

```
AUTOMATED CONTENT TYPE DETECTION:
- **Fundamental Analysis**: Files matching pattern `[ticker]-fundamental-analysis-[YYYYMMDD].md`
- **Trade History**: Files matching pattern `trading-performance-[type]-[YYYYMMDD].md`
- **Sector Analysis**: Files matching pattern `[sector]-sector-analysis-[YYYYMMDD].md`
```

### Cross-Content Type Validation

```
UNIVERSAL CONTENT STANDARDS:
□ **100% Content Fidelity**: All analytical content preserved without transformation
□ **Standardized Frontmatter**: Proper template compliance per content type
□ **Asset Integration**: Consistent image linking and optimization
□ **SEO Optimization**: Complete metadata and social sharing tags
□ **Publication Readiness**: Quality gates passed for all content types
```
