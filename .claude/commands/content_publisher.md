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
1. Scan @data/outputs/analysis_fundamental/ for unpublished fundamental analysis
2. Scan @data/outputs/analysis_trade_history/ for unpublished trade history reports
3. Check @frontend/src/content/blog/ for existing publications
4. Identify content gaps and publication opportunities across all content types
5. Assess content quality and readiness for publication
6. Prioritize content by relevance, timeliness, and audience value
```

### Asset Management & Synchronization
```
ASSET COORDINATION WORKFLOW:
1. Map analysis files to corresponding visualizations in @data/images/
   → tradingview/ - Trading charts and technical analysis
   → trendspider_full/ - Comprehensive market analysis charts
   → trendspider_tabular/ - Data visualization tables
2. Verify image availability and quality standards
3. Copy/optimize images to @frontend/public/images/
4. Validate image paths and accessibility
5. Ensure consistent asset naming and organization
```

### Content Transformation
```
ASTRO CONTENT CONVERSION - CRITICAL CONTENT FIDELITY RULES:
1. **NEVER TRANSFORM SOURCE CONTENT**: Content from @data/outputs/analysis_fundamental/ and @data/outputs/analysis_trade_history/ must be preserved 100% without any modifications, summarization, or editorial changes
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

## Content Standards & Quality Gates

### Publication Requirements

#### Fundamental Analysis Content
- **Naming Convention**: `[ticker]-fundamental-analysis-[YYYYMMDD].md`
- **Frontmatter Schema**: Company-focused blog post structure
- **Tag Taxonomy**: Use categories (fundamental-analysis, trading, stocks, [ticker])

#### Trade History Reports
- **Naming Convention**: `trading-performance-[report-type]-[YYYYMMDD].md`
- **Frontmatter Schema**: Performance-focused blog post structure
- **Tag Taxonomy**: Use categories (trading-performance, trade-history, signals, analysis)

#### Universal Requirements
- **Image Integration**: Consistent paths to `/images/tradingview/` or `/images/trendspider_full/`
- **SEO Optimization**: Complete titles, descriptions, tags, and metadata

### Quality Assurance Checklist
```
PRE-PUBLICATION VALIDATION - CONTENT FIDELITY ENFORCEMENT:
□ **CONTENT FIDELITY**: Source content preserved 100% without any transformations
□ **TITLE REMOVAL ONLY**: H1 title heading removed, all other content identical to source
□ **ANALYTICAL INTEGRITY**: All confidence scores, data quality metrics, recommendations, and trading performance metrics exactly as generated
□ **FINANCIAL DATA ACCURACY**: Investment thesis, valuations, risk assessments, trading results, and methodology unchanged
□ **PERFORMANCE DATA INTEGRITY**: Win rates, profit factors, trade durations, and statistical analysis preserved exactly
□ **FORMATTING PRESERVATION**: Tables, bullet points, section structure, and emphasis maintained exactly
□ **NO EDITORIAL CHANGES**: Zero summarization, optimization, or content modifications applied
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

# Publish specific analysis with priority handling
/content_publisher ticker=AAPL priority=high
/content_publisher report_type=historical_performance priority=high

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
