# Historical Performance Dashboard - Image Specification

**Authority**: Primary visual specification for historical trading performance reports  
**Last Updated**: 2025-06-26  
**Status**: Active  
**Color Reference**: [Sensylate Color Palette Authority](./sensylate-color-palette.md)

## Overview

This document defines the authoritative image specification for the Scalable Performance Overview Dashboard used in historical trading performance reports. The design supports dual-mode presentation (light/dark) and scales from small datasets (3 months, 15 trades) to large datasets (12 months, 200 trades).

## Design Specifications

### **Scalability Parameters**
- **Monthly Data Range**: 1-12 months (full year support)
- **Trade Volume Range**: 15-200 individual trades
- **Responsive Elements**: Auto-scaling visualizations with progressive disclosure

### **Layout Structure**
- **Format**: Single high-quality image
- **Grid**: 2x2 main visualization area with metrics header
- **Typography**: Heebo font family exclusively (400/600 weights)
- **Aspect Ratio**: Optimized for report embedding

---

## Light Mode Variant

### **Color Scheme**
```
Background: #fff (white)
Card Backgrounds: #f6f6f6 (light gray)
Primary Text: #121212 (black headers)
Body Text: #444444 (gray text)
Muted Text: #717171 (light gray)
Borders/Grid: #eaeaea (light borders)
```

### **Chart Colors**
```
Primary Data: #26c6da (cyan)
Secondary Data: #7e57c2 (purple)
Tertiary Data: #3179f5 (blue)
Extended Palette: #ff7043, #66bb6a, #ec407a
```

---

## Dark Mode Variant

### **Color Scheme**
```
Background: #202124 (dark gray)
Card Backgrounds: #222222 (darker cards)
Primary Text: #fff (white headers)
Body Text: #B4AFB6 (light gray text)
Muted Text: #B4AFB6 (consistent with body)
Borders/Grid: #3E3E3E (dark borders)
```

### **Chart Colors**
```
Primary Data: #26c6da (cyan - unchanged)
Secondary Data: #7e57c2 (purple - unchanged)
Tertiary Data: #3179f5 (blue - unchanged)
Extended Palette: #ff7043, #66bb6a, #ec407a (unchanged)
```

---

## Layout Components

### **Top Section - Key Metrics Row** (Fixed Height)
- **Win Rate Gauge**: Semi-circular gauge in `#26c6da`
- **Total Return Card**: Percentage with trend indicator
- **Profit Factor Meter**: Value with breakeven reference line
- **Trade Summary**: Total count with win/loss breakdown

### **Main Section - Scalable Visualizations (2x2 Grid)**

#### **Top Left: Monthly Performance Timeline**
**Scalable Design for 1-12 months:**
- **1-3 months**: Full month names, wider bars
- **4-8 months**: Month abbreviations, medium bars
- **9-12 months**: Compact view, thin bars
- **Colors**: Rotating pattern of `#7e57c2`, `#26c6da`, `#3179f5`

#### **Top Right: Quality Distribution Donut** (Fixed Scale)
**Quality Categories:**
- **Excellent**: `#26c6da`
- **Good**: `#3179f5`
- **Poor**: `#7e57c2`
- **Failed**: `#ff7043`
- **Poor Setup**: `#66bb6a`

#### **Bottom Left: Trade Performance Distribution**
**Adaptive Visualization:**
- **≤50 trades**: Individual trade waterfall chart
- **51-100 trades**: Grouped performance bands
- **101-200 trades**: Statistical distribution histogram
- **Colors**: Wins `#26c6da`, Losses `#7e57c2`

#### **Bottom Right: Duration vs Return Scatter**
**Density Management:**
- **≤50 points**: Full opacity, standard size
- **51-150 points**: Reduced opacity, smaller points
- **151-200 points**: Point clustering with density indicators
- **Quality Color Coding**: Using full extended palette

---

## Typography Specifications

### **Font Requirements**
- **Primary Font**: Heebo (weights: 400, 600 only)
- **Fallback**: Sans-serif system fonts

### **Text Hierarchy**
```
Main Title: Heebo 600 (responsive sizing)
Subtitle: Heebo 400 
Chart Titles: Heebo 600
Data Labels: Heebo 400 (auto-hide at high density)
Metrics: Heebo 600 (emphasis)
```

### **Content Text**
- **Main Title**: "Historical Trading Performance Dashboard"
- **Subtitle**: "[N] Closed Positions | [Date Range]"
- **Dynamic Elements**: Adapt based on dataset scope

---

## Scalability Solutions

### **Monthly Timeline Scaling**
| Month Count | Display Style | Bar Width | Labels |
|-------------|---------------|-----------|---------|
| 1-3 months | Full names | Wide | Complete |
| 4-8 months | Abbreviations | Medium | Abbreviated |
| 9-12 months | Compact | Thin | Minimal |

### **Trade Volume Scaling**
| Trade Count | Visualization | Detail Level | Interaction |
|-------------|---------------|--------------|-------------|
| 15-50 | Waterfall chart | Individual bars | Full labels |
| 51-100 | Performance bands | Grouped ranges | Selective labels |
| 101-200 | Distribution histogram | Statistical bins | Summary labels |

### **Performance Optimization**
- **Efficient rendering** for high-density visualizations
- **Progressive disclosure** maintains readability
- **Consistent color mapping** across all scales
- **Automatic legend adjustment** based on data complexity

---

## Implementation Guidelines

### **Data Integration**
- Source data from historical performance reports
- Auto-detect dataset scale for appropriate visualization selection
- Maintain consistent color assignments across report series

### **Quality Assurance**
- Verify color contrast ratios meet WCAG 2.1 AA standards
- Test readability at typical report viewing sizes
- Validate chart accuracy with source data

### **Export Specifications**
- **Format**: High-resolution PNG or SVG
- **DPI**: Minimum 300 for print quality
- **Dimensions**: Optimized for report embedding
- **File Naming**: `historical-performance-dashboard-[light|dark]-[date].png`

---

## Usage Notes

### **Mode Selection**
- **Light Mode**: Default for printed reports and light-background documents
- **Dark Mode**: Optimal for digital presentations and dark-themed interfaces
- **Consistent Data**: Both modes present identical information with theme-appropriate styling

### **Report Integration**
- Embed as primary visual summary in historical performance reports
- Position after executive summary, before detailed trade analysis
- Include both modes when report supports multiple viewing contexts

### **Maintenance**
- Update specification when new quality categories or performance metrics are introduced
- Validate color palette alignment with [Sensylate Color Palette Authority](./sensylate-color-palette.md)
- Test scalability with maximum parameter datasets (12 months, 200 trades)

---

*This specification ensures consistent, professional, and scalable visualization of historical trading performance data across all Sensylate reporting contexts.*