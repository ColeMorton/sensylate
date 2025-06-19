# Architect: Typography System Unification Implementation Plan

## Research Phase: Current System Analysis

### Current Implementation Analysis

**Typography System Architecture:**
- **Base CSS System** (`src/styles/base.css`): All headings set to `font-normal` (400 weight)
- **Prose/Content System** (`@tailwindcss/typography`): Typography plugin with default weights (H1:800, H2:700, H3:600)
- **Theme Configuration** (`src/config/theme.json`): Font families with limited weight ranges
- **Component Conflicts** (`src/styles/components.css`): Prose overrides creating dual hierarchy

**Current Font Configuration:**
```json
"primary": "Heebo:wght@400;600",    // Body text
"secondary": "Heebo:wght@700"       // Headers (insufficient range)
```

**Architecture Constraints:**
- Astro 5.7+ with TailwindCSS 4+
- Custom theme plugin system (`tw-theme.js`)
- Typography plugin integration required for content rendering
- PageHeader component vs content prose styling divergence

### Problem Scope

The Elements page reveals **two conflicting typography systems**:

| Element | Base CSS (PageHeader) | Prose (Content) | Expected Standard |
|---------|----------------------|-----------------|-------------------|
| H1 | 400 weight | 800 weight | **800** |
| H2 | 400 weight | 700 weight | **700** |
| H3 | 400 weight | 600 weight | **600** |

## Executive Summary

```xml
<summary>
  <objective>Unify typography system site-wide to match Elements page design standards</objective>
  <approach>Update base CSS as single source of truth, expand font weight range, remove prose conflicts</approach>
  <value>Consistent heading hierarchy across all pages, improved user experience, simplified maintenance</value>
</summary>
```

## Requirements Analysis

```xml
<requirements>
  <objective>Create unified typography system where Elements page style becomes site-wide standard</objective>
  <constraints>
    - Must maintain Astro/TailwindCSS architecture
    - Cannot break existing prose content rendering
    - Must support both light/dark themes
    - Font loading performance must remain optimal
  </constraints>
  <success_criteria>
    - PageHeader H1 matches content H1 styling (font-weight: 800)
    - All heading levels consistent across pages
    - No CSS overrides or conflicts
    - Elements page validation passes
  </success_criteria>
  <stakeholders>
    - Frontend developers maintaining the codebase
    - Content creators using the MDX system
    - End users experiencing consistent design
  </stakeholders>
</requirements>
```

## Architecture Design

### Current State Issues
- **Dual Typography Systems**: Base CSS and prose plugin create conflicts
- **Insufficient Font Weights**: Secondary font missing 800 weight
- **Override Architecture**: Components.css fighting typography plugin
- **Inconsistent Application**: PageHeader vs content styling divergence

### Target State Architecture
- **Single Source of Truth**: Base CSS defines all heading styles
- **Proper Font Weight Range**: Secondary font includes 700;800 weights
- **Clean Integration**: Typography plugin inherits from base styles
- **Universal Consistency**: Same heading styles everywhere

### Transformation Path
1. Expand font weight range in theme configuration
2. Update base CSS heading definitions to match Elements page
3. Remove prose overrides to eliminate conflicts
4. Validate across all page types

## Implementation Phases

```xml
<phase number="1" estimated_effort="0.5 days">
  <objective>Update font configuration to support required weight range</objective>
  <scope>Modify theme.json secondary font weights from 700 to 700;800</scope>
  <dependencies>None - isolated configuration change</dependencies>

  <implementation>
    <step>Update src/config/theme.json secondary font family to "Heebo:wght@700;800"</step>
    <validation>Verify font loading includes 800 weight in browser dev tools</validation>
    <rollback>Revert theme.json to previous state</rollback>
  </implementation>

  <deliverables>
    <deliverable>Updated theme.json with expanded font weight range</deliverable>
  </deliverables>

  <risks>
    <risk>Font loading performance impact → Monitor bundle size and loading times</risk>
  </risks>
</phase>
```

```xml
<phase number="2" estimated_effort="1 day">
  <objective>Establish base CSS as single source of truth for heading hierarchy</objective>
  <scope>Update src/styles/base.css heading definitions to match Elements page standards</scope>
  <dependencies>Phase 1 font weights must be available</dependencies>

  <implementation>
    <step>Update base.css heading rules:
      - H1: font-extrabold (800)
      - H2: font-bold (700)
      - H3: font-semibold (600)
      - H4: font-semibold (600)
      - H5: font-normal (400)
      - H6: font-normal (400)
    </step>
    <validation>Test PageHeader component shows correct font weights</validation>
    <rollback>Restore original base.css heading definitions</rollback>
  </implementation>

  <deliverables>
    <deliverable>Updated base.css with proper heading hierarchy</deliverable>
  </deliverables>

  <risks>
    <risk>Global heading changes affect unexpected components → Audit all page types during testing</risk>
  </risks>
</phase>
```

```xml
<phase number="3" estimated_effort="0.5 days">
  <objective>Remove prose typography conflicts to allow base CSS inheritance</objective>
  <scope>Clean prose overrides from src/styles/components.css .content class</scope>
  <dependencies>Phase 2 base CSS must be established</dependencies>

  <implementation>
    <step>Remove prose-h1, prose-h2, prose-h3 overrides from .content class</step>
    <step>Retain prose utilities for typography margins and colors only</step>
    <validation>Verify content headings inherit from base CSS correctly</validation>
    <rollback>Restore previous prose override rules</rollback>
  </implementation>

  <deliverables>
    <deliverable>Cleaned components.css with no heading font-weight conflicts</deliverable>
  </deliverables>

  <risks>
    <risk>Content rendering breaks → Test MDX content thoroughly before deployment</risk>
  </risks>
</phase>
```

```xml
<phase number="4" estimated_effort="0.5 days">
  <objective>Validate unified typography system across all page types</objective>
  <scope>Test Elements page, blog posts, PageHeader components, and content sections</scope>
  <dependencies>Phases 1-3 must be complete</dependencies>

  <implementation>
    <step>Run existing Puppeteer analysis on Elements page to verify consistency</step>
    <step>Visual regression test on homepage, blog, and other page types</step>
    <step>Verify dark mode theme compatibility</step>
    <validation>All heading elements show consistent font-weight hierarchy</validation>
    <rollback>Revert all changes if validation fails</rollback>
  </implementation>

  <deliverables>
    <deliverable>Validation report confirming typography consistency</deliverable>
    <deliverable>Updated documentation of typography system</deliverable>
  </deliverables>

  <risks>
    <risk>Unforeseen component conflicts → Create comprehensive test matrix</risk>
  </risks>
</phase>
```

## Success Metrics

### Technical Validation
- Elements page analysis shows consistent H1 font-weight (800) between title and examples
- No CSS conflicts or overrides in computed styles
- Font loading performance maintained or improved
- Dark/light theme compatibility verified

### User Experience Validation
- Visual consistency across all page types
- Improved reading hierarchy and typography clarity
- No regression in existing functionality

## Risk Mitigation Strategy

### High-Impact Risks
1. **Global CSS Changes**: Phased implementation with rollback procedures
2. **Typography Plugin Conflicts**: Isolated testing of prose integration
3. **Font Loading Performance**: Monitor bundle size and rendering times
4. **Theme Compatibility**: Explicit dark/light mode validation

### Monitoring Approach
- Automated visual regression testing
- Performance monitoring of font loading
- Cross-browser compatibility validation
- User accessibility testing

This implementation plan establishes a clean, maintainable typography system that eliminates the dual-hierarchy problem while ensuring the Elements page design standards become the site-wide norm.
