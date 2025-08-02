# Content Publisher

**Command Classification**: 📊 **Core Product Command**
**Knowledge Domain**: `content-publication-workflow`
**Ecosystem Version**: `2.1.0` *(Last Updated: 2025-07-18)*
**Outputs To**: `frontend/src/content/blog/`

## Script Integration Mapping

**Primary Script**: `{SCRIPTS_BASE}/content_publishing/content_publisher_script.py`
**Script Class**: `ContentPublisherScript`
**Registry Name**: `content_publisher`
**Content Types**: `["blog_publication", "asset_coordination", "comparative_analysis"]`
**Requires Validation**: `true`

**Registry Decorator**:
```python
@twitter_script(
    name="content_publisher",
    content_types=["blog_publication", "asset_coordination", "comparative_analysis"],
    requires_validation=True
)
class ContentPublisherScript(BaseScript):
    """Transform analytical insights into publication-ready blog content with absolute content fidelity"""
```

**Additional Scripts** (multi-phase workflow):
```yaml
discovery_script:
  path: "{SCRIPTS_BASE}/content_publishing/content_discovery.py"
  class: "ContentDiscoveryScript"
  phase: "Phase 1 - Content Discovery & Assessment"

asset_script:
  path: "{SCRIPTS_BASE}/content_publishing/asset_coordinator.py"
  class: "AssetCoordinatorScript"
  phase: "Phase 2 - Asset Management & Synchronization"

transformation_script:
  path: "{SCRIPTS_BASE}/content_publishing/content_transformer.py"
  class: "ContentTransformerScript"
  phase: "Phase 3 - Content Transformation"

publication_script:
  path: "{SCRIPTS_BASE}/content_publishing/frontend_publisher.py"
  class: "FrontendPublisherScript"
  phase: "Phase 4 - Publication & Validation"

comparative_analysis_discovery_script:
  path: "{SCRIPTS_BASE}/comparative_analysis/comparative_discovery.py"
  class: "ComparativeDiscoveryScript"
  phase: "DASV Phase 1 - Comparative Discovery"

comparative_analysis_script:
  path: "{SCRIPTS_BASE}/comparative_analysis/comparative_analyzer.py"
  class: "ComparativeAnalyzerScript"
  phase: "DASV Phase 2 - Comparative Analysis"

comparative_synthesis_script:
  path: "{SCRIPTS_BASE}/comparative_analysis/comparative_synthesizer.py"
  class: "ComparativeSynthesizerScript"
  phase: "DASV Phase 3 - Comparative Synthesis"
```

## Purpose

Systematically manages the content publication pipeline by discovering unpublished analysis content, coordinating visual assets, and publishing analytical content with **absolute content fidelity** to maintain the integrity and accuracy of financial analysis while ensuring quality publication standards throughout the Sensylate content ecosystem.

### Content Fidelity Mandate

**CRITICAL**: This command serves as a faithful custodian of analytical content. The primary responsibility is preserving 100% content accuracy without any transformation, summarization, or editorial modification. The only permitted change is removing the H1 title heading to prevent duplication with frontmatter titles.

**Output Location**: Published content in `frontend/src/content/blog/` with supporting assets in `frontend/public/images/`

## Template Integration Architecture

**Template Directory**: `{TEMPLATES_BASE}/content_publishing/`

**Template Mappings**:
| Template ID | File Path | Selection Criteria | Purpose |
|------------|-----------|-------------------|---------|
| fundamental_analysis_blog | `publishing/fundamental_analysis_blog.j2` | Content type fundamental analysis | Investment research blog posts |
| trade_history_blog | `publishing/trade_history_blog.j2` | Content type trade history | Trading performance blog posts |
| sector_analysis_blog | `publishing/sector_analysis_blog.j2` | Content type sector analysis | Sector analysis blog posts |
| comparative_analysis_blog | `publishing/comparative_analysis_blog.j2` | Content type comparative analysis | Cross-stock comparative investment analysis |
| blog_frontmatter | `publishing/blog_frontmatter.j2` | All blog content | Standardized frontmatter generation |

**Shared Components**:
```yaml
frontmatter_base:
  path: "{TEMPLATES_BASE}/content_publishing/shared/frontmatter_base.j2"
  purpose: "Base frontmatter template with common metadata and SEO optimization"

content_fidelity:
  path: "{TEMPLATES_BASE}/content_publishing/shared/content_fidelity.j2"
  purpose: "Content preservation template ensuring 100% analytical integrity"

asset_integration:
  path: "{TEMPLATES_BASE}/content_publishing/shared/asset_integration.j2"
  purpose: "Asset coordination and image optimization templates"
```

**Template Selection Algorithm**:
```python
def select_publication_template(content_analysis):
    """Select optimal template for content publication"""

    # Fundamental analysis blog template
    if content_analysis.get('content_type') == 'fundamental_analysis':
        return 'publishing/fundamental_analysis_blog.j2'

    # Trade history blog template
    elif content_analysis.get('content_type') == 'trade_history':
        return 'publishing/trade_history_blog.j2'

    # Sector analysis blog template
    elif content_analysis.get('content_type') == 'sector_analysis':
        return 'publishing/sector_analysis_blog.j2'

    # Comparative analysis blog template
    elif content_analysis.get('content_type') == 'comparative_analysis':
        return 'publishing/comparative_analysis_blog.j2'

    # Default blog template
    return 'publishing/blog_frontmatter.j2'
```

## Content Pipeline Management

### Content Discovery & Assessment
```
CONTENT AUDIT PROTOCOL:
1. Scan @data/outputs/fundamental_analysis/ for unpublished fundamental analysis markdown files
2. Scan @data/outputs/trade_history/ for unpublished trade history reports
3. Scan @data/outputs/sector_analysis/ for unpublished sector analysis markdown files
4. Scan @data/outputs/comparative_analysis/ for unpublished comparative analysis markdown files
5. Check @frontend/src/content/blog/ for existing publications
6. Identify content gaps and publication opportunities across all content types
7. Assess content quality and readiness for publication
8. Prioritize content by relevance, timeliness, and audience value
```

### Asset Management & Synchronization
```
ASSET COORDINATION WORKFLOW:
1. Map analysis files to corresponding visualizations in @data/images/
   → tradingview/ - Trading charts and technical analysis
   → trendspider_full/ - Comprehensive market analysis charts
   → trendspider_tabular/ - Data visualization tables
   → sector_analysis/ - Sector-specific charts and comparative analysis
   → comparative_analysis/ - Cross-stock comparative charts and side-by-side analysis
2. Verify image availability and quality standards
3. Copy/optimize images to @frontend/public/images/
   → Maintain directory structure: tradingview/, trendspider_full/, trendspider_tabular/, sector_analysis/, comparative_analysis/
4. Validate image paths and accessibility
5. Ensure consistent asset naming and organization
   → Sector analysis: {sector-slug}_{YYYYMMDD}.png format
   → Comparative analysis: {ticker1}_vs_{ticker2}_{YYYYMMDD}.png format
```

### Content Transformation
```
ASTRO CONTENT CONVERSION - CRITICAL CONTENT FIDELITY RULES:
1. **NEVER TRANSFORM SOURCE CONTENT**: Content from @data/outputs/fundamental_analysis/, @data/outputs/trade_history/, and @data/outputs/comparative_analysis/ must be preserved 100% without any modifications, summarization, or editorial changes
2. **ONLY REMOVE TITLE HEADING**: Remove the H1 title heading (e.g., "# Company Name - Fundamental Analysis", "# Historical Trading Performance - Closed Positions", or "# Stock A vs Stock B - Comprehensive Investment Analysis") to prevent duplication with frontmatter title
3. **PRESERVE ALL ANALYSIS CONTENT**: Maintain exact confidence scores, data quality metrics, investment recommendations, financial data, trading performance metrics, comparative analysis matrices, cross-stock valuations, and methodology
4. **ADD FRONTMATTER ONLY**: Add proper frontmatter with metadata, SEO data, tags, categories without altering content body
5. **MAINTAIN ANALYTICAL INTEGRITY**: Preserve the analytical voice, formatting, tables, bullet points, comparative frameworks, risk matrices, and structure exactly as generated
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

## CLI Service Integration

**Service Commands**:
```yaml
astro_dev_server:
  command: "cd frontend && yarn dev"
  usage: "Start development server for content validation"
  purpose: "Real-time content rendering validation"
  health_check: "curl http://localhost:4321/health"
  priority: "primary"

content_validator:
  command: "cd frontend && yarn check"
  usage: "TypeScript and content validation"
  purpose: "Content integrity and type safety validation"
  health_check: "cd frontend && yarn check --help"
  priority: "primary"

image_optimizer:
  command: "python {SCRIPTS_BASE}/image_processing/optimize_images.py"
  usage: "{command} --source {source_path} --dest {dest_path}"
  purpose: "Image optimization and responsive asset generation"
  health_check: "{command} --help"
  priority: "secondary"
```

**Publication Integration Protocol**:
```bash
# Content validation
cd frontend && yarn check

# Development server validation
cd frontend && yarn dev &
sleep 5 && curl http://localhost:4321/blog/

# Image optimization
python {SCRIPTS_BASE}/image_processing/optimize_images.py --source data/images/ --dest frontend/public/images/
```

**Data Authority Protocol**:
```yaml
authority_hierarchy:
  source_content: "HIGHEST_AUTHORITY"  # Data outputs are authoritative source
  frontmatter_templates: "METADATA_AUTHORITY"  # Templates control metadata structure
  astro_framework: "RENDERING_AUTHORITY"  # Astro framework controls final presentation

conflict_resolution:
  content_precedence: "source_content"  # Source content takes priority
  metadata_standards: "frontmatter_templates"  # Templates enforce standardization
  rendering_compatibility: "astro_framework"  # Framework requirements must be met
  action: "preserve_content_fidelity"  # Resolution strategy
```

## Data Flow & File References

**Input Sources**:
```yaml
fundamental_analysis:
  path: "{DATA_OUTPUTS}/fundamental_analysis/{TICKER}_{YYYYMMDD}.md"
  format: "markdown"
  required: true
  description: "Fundamental analysis reports for publication"

trade_history:
  path: "{DATA_OUTPUTS}/trade_history/trading-performance-{TYPE}-{YYYYMMDD}.md"
  format: "markdown"
  required: false
  description: "Trade history reports for publication"

sector_analysis:
  path: "{DATA_OUTPUTS}/sector_analysis/{SECTOR}-sector-analysis-{YYYYMMDD}.md"
  format: "markdown"
  required: false
  description: "Sector analysis reports for publication"

comparative_analysis:
  path: "{DATA_OUTPUTS}/comparative_analysis/{TICKER_1}_vs_{TICKER_2}_{YYYYMMDD}.md"
  format: "markdown"
  required: false
  description: "Cross-stock comparative analysis reports for publication"

visual_assets:
  path: "{DATA_IMAGES}/{asset_type}/{IDENTIFIER}_{YYYYMMDD}.png"
  format: "png|jpg"
  required: false
  description: "Visual assets for content enhancement"
```

**Output Structure**:
```yaml
blog_content:
  path: "frontend/src/content/blog/{identifier}-{type}-{YYYYMMDD}.md"
  format: "markdown"
  description: "Published blog content with standardized frontmatter (includes comparative analysis: {ticker1}-vs-{ticker2}-comparative-analysis-{YYYYMMDD}.md)"

optimized_images:
  path: "frontend/public/images/{asset_type}/{IDENTIFIER}_{YYYYMMDD}.png"
  format: "png|jpg"
  description: "Optimized images for web presentation"

publication_metadata:
  path: "{DATA_OUTPUTS}/content_publication/{IDENTIFIER}_{YYYYMMDD}_metadata.json"
  format: "json"
  description: "Publication metadata and validation results"
```

## Parameters

### Core Parameters
- `content_type`: Content type to publish - `fundamental_analysis` | `trade_history` | `sector_analysis` | `comparative_analysis` | `all` (optional, default: all)
- `ticker`: Specific ticker to publish (optional)
- `priority`: Publication priority - `high` | `medium` | `low` (optional, default: medium)
- `mode`: Publication mode - `full` | `assets_only` | `validation_only` (optional, default: full)

### Advanced Parameters
- `scope`: Publication scope - `comprehensive` | `selective` | `targeted` (optional, default: comprehensive)
- `validation_level`: Validation depth - `basic` | `standard` | `comprehensive` (optional, default: standard)
- `asset_optimization`: Enable image optimization - `true` | `false` (optional, default: true)
- `frontend_validation`: Enable frontend rendering validation - `true` | `false` (optional, default: true)

### Workflow Parameters (Multi-Phase Commands)
- `phase_start`: Starting phase - `discovery` | `asset` | `transformation` | `publication` (optional)
- `phase_end`: Ending phase - `discovery` | `asset` | `transformation` | `publication` (optional)
- `continue_on_error`: Continue workflow despite errors - `true` | `false` (optional, default: false)
- `report_type`: Trade history report type - `historical` | `internal` | `live_signals` (optional)

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

## Comparative Analysis Standard Template

### MANDATORY FRONTMATTER TEMPLATE

All comparative analysis posts MUST use this exact template with NO deviations:

```yaml
---
title: "{Company_1_Name} ({TICKER_1}) vs {Company_2_Name} ({TICKER_2}) - Comparative Investment Analysis"
meta_title: "{Company_1_Name} vs {Company_2_Name} Comparative Analysis - Investment Decision Framework"
description: "Institutional-quality comparative analysis of {Company_1_Name} ({TICKER_1}) vs {Company_2_Name} ({TICKER_2}) with cross-sector investment framework. {Primary_recommendation} vs {Secondary_recommendation} with {confidence}% confidence."
date: {YYYY-MM-DD}T{HH:MM:SS}Z
image: "/images/comparative_analysis/{TICKER_1}_vs_{TICKER_2}_{YYYYMMDD}.png"
authors: ["Cole Morton", "Claude"]
categories: ["Investing", "Analysis", "Comparative Analysis", "{Sector_1}", "{Sector_2}"]
tags: ["{ticker1-lowercase}", "{ticker2-lowercase}", "comparative-analysis", "{primary-recommendation-lowercase}", "{cross-sector}", "{investment-theme}"]
draft: false
comparative_data:
  comparison_confidence: {0.XX}
  data_quality: {0.XX}
  economic_context: "{Current/Expansion/Contraction}"
  primary_recommendation: "{BUY/HOLD/SELL}"
  secondary_recommendation: "{BUY/HOLD/SELL}"
  risk_adjusted_winner: "{TICKER_1/TICKER_2}"
  portfolio_allocation: "{XX%} {TICKER_1} / {XX%} {TICKER_2}"
  expected_returns: "{XX.X%} vs {XX.X%}"
  risk_differential: "{X.X/5.0} vs {X.X/5.0}"
---
```

### STRICT STANDARDIZATION RULES

#### Title Standards
- **Format**: `{Company_1_Name} ({TICKER_1}) vs {Company_2_Name} ({TICKER_2}) - Comparative Investment Analysis`
- **Remove**: ALL specific ratings, returns, and complex themes from title
- **Example**: `"Amazon.com Inc. (AMZN) vs Microsoft Corporation (MSFT) - Comparative Investment Analysis"`

#### Meta_title Standards
- **Always include** for SEO optimization
- **Format**: `{Company_1_Name} vs {Company_2_Name} Comparative Analysis - Investment Decision Framework`
- **Example**: `"Amazon vs Microsoft Comparative Analysis - Investment Decision Framework"`

#### Description Standards
- **Length**: 150-200 characters
- **Include**: Both recommendations, confidence level, cross-sector context
- **Template**: `"Institutional-quality comparative analysis of {Company_1} ({TICKER_1}) vs {Company_2} ({TICKER_2}) with cross-sector investment framework. {Primary_rec} vs {Secondary_rec} with {confidence}% confidence."`

#### Date Standards
- **Format**: ISO 8601 with timezone `YYYY-MM-DDTHH:MM:SSZ`
- **Example**: `2025-08-01T16:30:00Z`
- **Required**: Must include timezone Z suffix

#### Authors Standards
- **Field**: Use `authors` (NOT `author`)
- **Value**: `["Cole Morton", "Claude"]` (EXACT format)
- **Required**: Present in ALL posts

#### Categories Standards
- **Order**: `["Investing", "Analysis", "Comparative Analysis", "{Sector_1}", "{Sector_2}"]`
- **Count**: Exactly 5 categories
- **Cross-Sector**: Include both sectors when different (Technology, Healthcare, Financial Services, etc.)
- **Same-Sector**: Use sector twice when comparing within same sector

#### Tags Standards
- **Tickers**: ALWAYS lowercase (`amzn`, `msft`, NOT `AMZN`, `MSFT`)
- **Required**: `"comparative-analysis"` in ALL posts
- **Cross-Sector**: Include `"cross-sector"` when companies from different sectors
- **Recommendations**: Include both recommendation tags (`"buy"`, `"hold"`, `"sell"`) when different
- **Count**: 6-8 tags maximum
- **Format**: Lowercase with hyphens

#### Image Standards
- **Path**: `/images/comparative_analysis/{TICKER_1}_vs_{TICKER_2}_{YYYYMMDD}.png`
- **Tickers**: Uppercase in filename
- **Date**: Match publication date exactly
- **Order**: Primary ticker first (typically the focus or winner)

#### Comparative Data Standards
- **Comparison Confidence**: Decimal format (0.XX) matching source analysis
- **Data Quality**: Decimal format (0.XX) matching source analysis
- **Economic Context**: One of "Current", "Expansion", "Contraction"
- **Recommendations**: Both as "BUY", "HOLD", or "SELL"
- **Risk Adjusted Winner**: The ticker symbol of the preferred choice after risk adjustment
- **Portfolio Allocation**: Suggested allocation percentages for both stocks
- **Expected Returns**: Expected return percentages for both stocks
- **Risk Differential**: Risk scores in format "X.X/5.0" for both stocks

### STANDARDIZATION VALIDATION PROTOCOL

**MANDATORY PRE-PUBLICATION CHECKS**: Every comparative analysis post MUST pass ALL validation checks before publication:

```
FRONTMATTER COMPLIANCE VALIDATION:
□ **TITLE FORMAT**: Exact format "{Company_1} ({TICKER_1}) vs {Company_2} ({TICKER_2}) - Comparative Investment Analysis"
□ **META_TITLE PRESENCE**: Must exist with comparative framework information
□ **DESCRIPTION LENGTH**: 150-200 characters with required elements
□ **DATE FORMAT**: ISO 8601 with timezone (YYYY-MM-DDTHH:MM:SSZ)
□ **AUTHORS FORMAT**: Exact format ["Cole Morton", "Claude"]
□ **CATEGORIES STRUCTURE**: Exact format ["Investing", "Analysis", "Comparative Analysis", "{Sector_1}", "{Sector_2}"]
□ **TAGS COMPLIANCE**: Lowercase tickers + "comparative-analysis" + recommendations + themes
□ **IMAGE PATH**: Correct format with uppercase tickers and matching date
□ **COMPARATIVE DATA STRUCTURE**: Complete comparative_data object with all required fields
□ **CONFIDENCE SCORES**: Decimal format matching source analysis confidence and data quality
□ **RECOMMENDATIONS**: Valid recommendations for both stocks with risk-adjusted winner
□ **DRAFT STATUS**: Set to false for publication
```

**AUTOMATIC REJECTION**: Any post that fails validation MUST be corrected before publication. No exceptions.

**STANDARDIZATION ENFORCEMENT**: The content_publisher command will automatically verify and correct any frontmatter issues to ensure 100% compliance with the comparative analysis standard template.

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

#### Comparative Analysis Content
- **Naming Convention**: `[ticker1]-vs-[ticker2]-comparative-analysis-[YYYYMMDD].md`
- **Frontmatter Schema**: MANDATORY compliance with Comparative Analysis Standard Template
- **Tag Taxonomy**: STRICT adherence to standardized tag structure (see Comparative Analysis Standard Template)

#### Universal Requirements
- **Image Integration**: Consistent paths to `/images/tradingview/`, `/images/trendspider_full/`, `/images/sector_analysis/`, or `/images/comparative_analysis/`
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
□ **COMPARATIVE ANALYSIS INTEGRITY**: Cross-stock comparisons, risk matrices, portfolio allocation recommendations, and winner determinations preserved exactly
□ **ECONOMIC DATA ACCURACY**: GDP correlations, employment sensitivity, interest rate impacts, and economic cycle analysis unchanged
□ **FORMATTING PRESERVATION**: Tables, bullet points, section structure, and emphasis maintained exactly
□ **NO EDITORIAL CHANGES**: Zero summarization, optimization, or content modifications applied
□ **FRONTMATTER COMPLIANCE**: MANDATORY adherence to respective Standard Templates (Fundamental Analysis, Sector Analysis, Trade History, or Comparative Analysis)
□ **AUTHOR STANDARDIZATION**: Must use authors: ["Cole Morton", "Claude"]
□ **CATEGORY STANDARDIZATION**: Must use proper category structure per content type
□ **TAG STANDARDIZATION**: Must use lowercase identifiers + standardized tag structure per content type
□ **DATE STANDARDIZATION**: Must use ISO 8601 with timezone format
□ **TITLE STANDARDIZATION**: Must use clean format without ratings/returns per content type
□ **META_TITLE STANDARDIZATION**: Must include rating information in standardized format per content type
□ **SECTOR DATA VALIDATION**: For sector analysis, must include complete sector_data object with confidence scores
□ **COMPARATIVE DATA VALIDATION**: For comparative analysis, must include complete comparative_data object with both recommendations
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

## Quality Standards Framework

### Confidence Scoring
**Publication-Quality Thresholds**:
- **Content Fidelity**: 100% preservation of source analytical content (mandatory)
- **Frontmatter Compliance**: 100% adherence to standardized templates
- **Asset Integration**: 95% successful image optimization and linking
- **Frontend Validation**: 98% rendering compatibility across devices

### Validation Protocols
**Multi-Phase Validation Standards**:
- **Content Integrity**: 0% variance from source analytical content
- **Metadata Accuracy**: 100% compliance with frontmatter templates
- **Asset Optimization**: <500KB image sizes with responsive breakpoints
- **Frontend Health**: Development server rendering validation

### Quality Gate Enforcement
**Critical Validation Points**:
1. **Discovery Phase**: Content completeness and publication readiness
2. **Asset Phase**: Image optimization and responsive asset generation
3. **Transformation Phase**: Content fidelity and frontmatter compliance
4. **Publication Phase**: Frontend validation and cross-platform compatibility

## Cross-Command Integration

### Upstream Dependencies
**Commands that provide input to this command**:
- `fundamental_analyst`: Provides fundamental analysis reports via {DATA_OUTPUTS}/fundamental_analysis/
- `trade_history`: Provides trade history reports via {DATA_OUTPUTS}/trade_history/
- `sector_analyst`: Provides sector analysis reports via {DATA_OUTPUTS}/sector_analysis/
- `comparative_analyst`: Provides comparative analysis reports via {DATA_OUTPUTS}/comparative_analysis/ (DASV framework)

### Downstream Dependencies
**Commands that consume this command's outputs**:
- `content_evaluator`: Evaluates published content for quality assurance
- `documentation_owner`: Documents publication workflows and standards

### Coordination Workflows
**Multi-Command Orchestration**:
```bash
# Sequential publication workflow
/fundamental_analyst TICKER
/content_publisher ticker=TICKER content_type=fundamental_analysis
/content_evaluator filename="frontend/src/content/blog/{ticker}-fundamental-analysis-{date}.md"

# Comparative analysis workflow
/comparative_analyst/discover ticker_1=AAPL ticker_2=MSFT
/comparative_analyst/analyze discovery_file="data/outputs/comparative_analysis/discovery/AAPL_vs_MSFT_{date}_discovery.json"
/comparative_analyst/synthesize analysis_file="data/outputs/comparative_analysis/analysis/AAPL_vs_MSFT_{date}_analysis.json"
/content_publisher content_type=comparative_analysis

# Multi-content publication
/content_publisher content_type=all scope=comprehensive
```

## Usage Examples

### Basic Usage
```
/content_publisher
/content_publisher content_type=fundamental_analysis
/content_publisher content_type=comparative_analysis
```

### Advanced Usage
```
/content_publisher ticker=AAPL priority=high validation_level=comprehensive
/content_publisher content_type=comparative_analysis scope=comprehensive
```

### Comparative Analysis Publication
```
/content_publisher content_type=comparative_analysis priority=high
/content_publisher content_type=comparative_analysis mode=assets_only
```

### Validation Enhancement
```
/content_publisher mode=validation_only frontend_validation=true
/content_publisher content_type=comparative_analysis mode=validation_only
```

---

**Integration with Framework**: This command integrates with the broader Sensylate ecosystem through standardized script registry, template system, CLI service integration, and validation framework protocols.

**Author**: Cole Morton
**Framework**: Content Publication Workflow Framework
**Confidence**: High - Standardized publication methodology
**Data Quality**: High - Content fidelity preservation protocols

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
1. **Content Discovery**: Scan @data/outputs/trade_history/ for unpublished reports
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
5. **Comparative Analysis Data**: Cross-stock comparisons, risk matrices, portfolio allocations, and winner determinations unchanged
6. **Methodology**: Analysis methodology and data sources maintained verbatim
7. **Author Voice**: Analytical voice and technical language preserved completely

This ensures readers receive the exact analytical output generated by the fundamental analysis system, trade history analysis system, and comparative analysis system, maintaining credibility and accuracy in all financial content publication.

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

## Comparative Analysis Content Management

### Comparative Analysis Content Types

**CROSS_STOCK_COMPARATIVE_ANALYSIS**: Institutional-quality comparative investment analysis with cross-sector framework
- **Content Structure**: Comparative company intelligence, financial health comparison, risk-adjusted recommendations, portfolio allocation guidance
- **Key Metrics**: Cross-stock confidence scores, comparative risk matrices, winner determinations, expected returns differential
- **Publication Priority**: High - provides sophisticated investment decision frameworks for portfolio construction

**SECTOR_COMPARATIVE_ANALYSIS**: Cross-sector comparative analysis with economic integration
- **Content Structure**: Sector positioning comparison, economic sensitivity differential, regulatory environment analysis
- **Key Metrics**: Sector rotation scores, economic context impact, cross-sector valuation metrics
- **Publication Priority**: Medium - strategic sector allocation insights with comparative framework

**INDUSTRY_COMPARATIVE_ANALYSIS**: Within-industry comparative analysis with competitive intelligence
- **Content Structure**: Market positioning comparison, competitive moat analysis, industry dynamics assessment
- **Key Metrics**: Market share analysis, competitive advantage scoring, industry disruption risk assessment
- **Publication Priority**: Medium - tactical positioning insights within industry contexts

### Comparative Analysis Publication Workflow

```
COMPARATIVE ANALYSIS SPECIFIC PIPELINE:
1. **Content Discovery**: Scan @data/outputs/comparative_analysis/ for unpublished comparative reports
2. **Report Classification**: Identify comparison type (Cross-Stock, Cross-Sector, Within-Industry)
3. **Asset Mapping**: Link to comparative charts, side-by-side visualizations, and cross-stock analysis
4. **Schema Application**: Apply comparative-specific frontmatter templates with confidence scores
5. **Fidelity Preservation**: Maintain 100% accuracy of comparative metrics, risk matrices, and investment recommendations
6. **Publication**: Deploy to @frontend/src/content/blog/ with comparative analysis categories
7. **Validation**: Verify comparative data accuracy and cross-stock chart accessibility
```

### Comparative Analysis Quality Gates

```
COMPARATIVE ANALYSIS CONTENT VALIDATION:
□ **COMPARATIVE METRICS ACCURACY**: Cross-stock financial ratios, valuation comparisons, and performance attribution exactly preserved
□ **RISK MATRIX INTEGRITY**: Probability-impact matrices, stress testing scenarios, and risk differential analysis unchanged
□ **INVESTMENT RECOMMENDATION PRESERVATION**: Primary and secondary recommendations, portfolio allocations, and winner determinations maintained
□ **CONFIDENCE SCORE FIDELITY**: Comparative analysis confidence and data quality metrics preserved exactly
□ **METHODOLOGY DOCUMENTATION**: Cross-stock analytical framework and comparative selection rationale unchanged
□ **COMPARATIVE DATA OBJECT COMPLETION**: Complete comparative_data frontmatter with all required fields
□ **VISUAL ASSET COORDINATION**: Comparative charts and cross-stock visualizations properly linked
□ **ECONOMIC CONTEXT ACCURACY**: Interest rate sensitivity differential and economic impact analysis preserved
```

## Multi-Content Type Integration

### Unified Content Pipeline

The content_publisher command now supports four distinct content types with unified quality standards:

1. **Fundamental Analysis**: Company-specific investment analysis with valuation models
2. **Trade History Reports**: Trading performance analysis with statistical validation
3. **Sector Analysis**: Sector-level strategic analysis with economic integration
4. **Comparative Analysis**: Cross-stock comparative investment analysis with risk-adjusted decision frameworks

### Content Type Detection

```
AUTOMATED CONTENT TYPE DETECTION:
- **Fundamental Analysis**: Files matching pattern `[ticker]-fundamental-analysis-[YYYYMMDD].md`
- **Trade History**: Files matching pattern `trading-performance-[type]-[YYYYMMDD].md`
- **Sector Analysis**: Files matching pattern `[sector]-sector-analysis-[YYYYMMDD].md`
- **Comparative Analysis**: Files matching pattern `[ticker1]_vs_[ticker2]_[YYYYMMDD].md`
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
