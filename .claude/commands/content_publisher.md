# Content Publisher

Transform analytical insights from data pipeline outputs into publication-ready blog content for the "Cole Morton" frontend.
Specializes in content synchronization between `data/outputs/` and `frontend/src/content/` with quality assurance and asset coordination.

## Core Product Command Profile

**Type**: Core Product Command (User-facing AI functionality)

## Purpose

Systematically manages the content publication pipeline by discovering unpublished analysis content, coordinating visual assets, transforming analytical insights into web-optimized blog posts, and ensuring quality publication standards are maintained throughout the Sensylate content ecosystem.

**Output Location**: Published content in `frontend/src/content/blog/` with supporting assets in `frontend/public/images/`

## Content Pipeline Management

### Content Discovery & Assessment
```
CONTENT AUDIT PROTOCOL:
1. Scan @data/outputs/analysis_fundamental/ for unpublished analysis
2. Check @frontend/src/content/blog/ for existing publications
3. Identify content gaps and publication opportunities
4. Assess content quality and readiness for publication
5. Prioritize content by relevance, timeliness, and audience value
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
ASTRO CONTENT CONVERSION:
1. Transform analysis markdown to blog-compatible format
2. Add proper frontmatter with metadata, SEO data, tags, categories
3. Optimize content structure for web readability
4. Integrate image references with proper paths
5. Maintain analytical depth while ensuring accessibility
6. Cross-reference related content for internal linking
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
- **Naming Convention**: `[ticker]-fundamental-analysis-[YYYYMMDD].md`
- **Frontmatter Schema**: Match existing blog post structure
- **Image Integration**: Consistent paths to `/images/tradingview/` or `/images/trendspider_full/`
- **Tag Taxonomy**: Use established categories (fundamental-analysis, trading, stocks)
- **SEO Optimization**: Complete titles, descriptions, tags, and metadata

### Quality Assurance Checklist
```
PRE-PUBLICATION VALIDATION:
□ Content accuracy verified against source analysis
□ All referenced images properly linked and accessible
□ SEO metadata complete and optimized
□ Consistent formatting and style maintained
□ Proper categorization and tagging applied
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

# Publish specific analysis with priority handling
/content_publisher ticker=AAPL priority=high

# Asset synchronization and optimization only
/content_publisher mode=assets_only

# Quality assurance and validation check
/content_publisher mode=validation_only
```

This content publisher command ensures Sensylate maintains high-quality, consistent content publication that properly leverages both analytical depth and visual presentation for maximum reader engagement and technical accuracy while integrating seamlessly with the team workspace collaboration framework.
