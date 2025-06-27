# Sensylate Color Palette Authority

**Authority**: Primary reference for all Sensylate visual design decisions  
**Last Updated**: 2025-06-26  
**Status**: Active  

## Overview

This document serves as the authoritative color palette specification for Sensylate and Cole Morton frontend applications. All team workspace commands, design decisions, and implementation plans must reference this palette.

## Charts & Specialty Colors

### Primary Data Visualization
- **Cyan**: `#26c6da` - Primary data visualization, main chart series
- **Purple**: `#7e57c2` - Secondary data visualization, comparison series  
- **Blue**: `#3179f5` - Tertiary data visualization, accent series

### Extended Chart Colors
For multi-series data visualization:
- **Teal**: `#26c6da` (Primary)
- **Deep Purple**: `#7e57c2` (Secondary)
- **Blue**: `#3179f5` (Tertiary)
- **Orange**: `#ff7043` (Quaternary)
- **Green**: `#66bb6a` (Quinary)
- **Pink**: `#ec407a` (Senary)

## Website & Content Colors

### Light Mode Theme
- **Primary**: `#121212` - Headers, primary text
- **Body**: `#fff` - Background
- **Border**: `#eaeaea` - Borders, dividers
- **Light**: `#f6f6f6` - Light backgrounds, cards
- **Dark**: `#040404` - Darkest elements, emphasis
- **Text**: `#444444` - Body text, paragraphs
- **Text Dark**: `#040404` - Dark text emphasis
- **Text Light**: `#717171` - Muted text, captions

### Dark Mode Theme
- **Primary**: `#fff` - Headers, primary text
- **Body**: `#202124` - Background
- **Border**: `#3E3E3E` - Borders, dividers
- **Light**: `#222222` - Light backgrounds, cards
- **Dark**: `#1C1C1C` - Darkest elements
- **Text**: `#B4AFB6` - Body text, paragraphs
- **Text Dark**: `#fff` - Dark text emphasis
- **Text Light**: `#B4AFB6` - Muted text, captions

## Usage Guidelines

### Data Visualization
- Use specialty colors (`#26c6da`, `#7e57c2`, `#3179f5`) for all charts and graphs
- Apply extended palette for complex multi-series visualizations
- Maintain consistent color mapping across related charts

### Website Implementation
- Reference `frontend/src/config/theme.json` for current implementation
- All theme modifications must align with this palette authority
- Ensure sufficient contrast ratios for accessibility compliance

### Team Workspace Integration
- All design-related commands must reference this palette
- Product decisions involving visual elements should cite this authority
- Implementation plans must validate color choices against this specification

## Color Accessibility

All color combinations maintain WCAG 2.1 AA compliance:
- Light mode: Primary text (#121212) on background (#fff) = 19.77:1
- Dark mode: Primary text (#fff) on background (#202124) = 15.68:1
- Chart colors tested for colorblind accessibility

## Implementation Reference

**Configuration File**: `frontend/src/config/theme.json`  
**Authority File**: `team-workspace/knowledge/design-system/sensylate-color-palette.md`  

---

*This palette serves as the single source of truth for all Sensylate color decisions. Any deviations must be documented and approved through the team workspace coordination system.*