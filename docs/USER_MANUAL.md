# 📖 Sensylate User Manual

> **Complete guide to using Sensylate's multi-modal platform for trading analysis, content creation, and AI command collaboration.**

## 🎯 Quick Navigation

- [🚀 Getting Started](#-getting-started)
- [🤝 AI Command Integration](#-ai-command-integration)
- [📊 Trading Analysis](#-trading-analysis)
- [🌐 Frontend Features](#-frontend-features)
- [🤖 AI Commands](#-ai-commands)
- [⚙️ Configuration](#-configuration)
- [🔧 Troubleshooting](#-troubleshooting)

---

## 🚀 Getting Started

### System Requirements

- **Node.js**: 18+ for frontend development
- **Python**: 3.9+ for data processing
- **Git**: For version control and collaboration
- **Claude Code**: For AI command collaboration

### Initial Setup

1. **Clone and Install**:
   ```bash
   git clone [repository-url]
   cd sensylate

   # Frontend setup
   cd frontend/
   yarn install

   # Python setup (from root)
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Environment Configuration**:
   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit with your settings
   # Configure API keys and database connections
   ```

3. **Verify Installation**:
   ```bash
   # Test frontend
   cd frontend/
   yarn test

   # Test Python pipeline
   make test

   # Test data pipeline
   make test-pipeline
   ```

### First Run

1. **Start Development Environment**:
   ```bash
   cd frontend/
   yarn dev
   ```

2. **Run Your First Analysis**:
   ```bash
   make dev-pipeline
   ```

3. **Try AI Commands**:
   ```bash
   > "/code-owner - analyze project health"
   ```

---

## 🤝 AI Command Integration

> **⭐ FEATURE**: AI commands integrate with your data pipeline, using analysis outputs to provide contextual insights.

### What is AI Command Integration?

AI commands work with your data pipeline outputs:
- **Use Analysis Data**: Commands read from data/outputs/ directories
- **Contextual Insights**: Analysis results inform AI responses
- **Data-Driven Decisions**: Commands leverage existing analysis outputs
- **Integrated Workflow**: Seamless connection between analysis and AI commands

### Quick Start (2 Minutes)

1. **Check Core Data Pipeline**:
   ```bash
   ls data/outputs/
   # Should show analysis outputs: fundamental_analysis/ sector_analysis/ etc.
   ```

2. **Try Data-Integrated Commands**:
   ```bash
   > "/code-owner - analyze current project health"
   > "/architect - create improvement plan"
   ```

3. **See Integration**: Commands automatically reference existing analysis data when available!

### Best Workflow Patterns

#### Complete Project Analysis
```bash
> "Run comprehensive project analysis"
# Executes commands that reference existing data/outputs/ analysis
```

#### Feature Development
```bash
> "/code-owner - analyze authentication module"         # Technical assessment
> "/architect - refactor auth for better security"      # References existing analysis
> "/product-owner - estimate effort for auth refactor"  # Uses available data context
```

#### Content Creation
```bash
> "/architect - summarize recent improvements"          # Reviews project data
> "/twitter-post - create content about improvements"   # Uses available analysis data
```

### Available AI Team Members

> **Command Categories**:
> - **Core Product**: User-facing AI capabilities that ARE the product
> - **Infrastructure**: Development tools that ENABLE the product

#### 🚀 Core Product Commands (User-facing AI functionality)
| Command | Role | Best For |
|---------|------|----------|
| `/twitter-post` | Content Creation | Social media content optimization |
| `/twitter-post-strategy` | Financial Content | Trading/financial social media content |
| `/fundamental-analysis` | Market Analysis | Trading strategies and market insights |

#### 🔧 Infrastructure Commands (Enable product development)
| Command | Role | Best For |
|---------|------|----------|
| `/architect` | Technical Planning | Implementation design, system architecture |
| `/product-owner` | Business Strategy | Feature prioritization, resource planning |
| `/code-owner` | Technical Health | Code quality assessment, technical debt |
| `/business-analyst` | Requirements | Process analysis, stakeholder needs |
| `/commit-push` | Git Workflow | Automated commit and push operations |
| `/create-command` | Command Creation | Building new AI commands |

📚 **Full Guide**: See command documentation in `.claude/commands/` for complete usage examples.

---

## 📊 Trading Analysis

### Data Processing Pipeline

Sensylate provides a complete trading analysis framework:

#### 1. Data Extraction
```bash
# Extract market data for specific symbols
make extract-data ENV=prod

# Quick development extraction
make quick-extract
```

**What it does**: Downloads market data, applies technical indicators, validates data quality.

#### 2. Feature Engineering
```bash
# Process extracted data
make process-data

# Quick processing for development
make quick-process
```

**What it does**: Generates technical indicators, calculates features, prepares data for analysis.

#### 3. Strategy Development
```bash
# Train trading models
make train-model

# Full pipeline (extract → process → train)
make full-pipeline
```

**What it does**: Develops trading strategies, backtests performance, generates model files.

#### 4. Report Generation
```bash
# Create analysis reports
make generate-report

# Environment-specific
make prod-pipeline
```

**What it does**: Creates comprehensive analysis reports with interactive Plotly visualizations, multi-format dashboard exports, and performance summaries.

### Configuration Files

All trading analysis is configuration-driven:

#### Data Sources (`config/pipelines/data_extraction.yaml`)
```yaml
symbols: ["AAPL", "GOOGL", "TSLA"]
timeframe: "1d"
indicators: ["SMA", "EMA", "RSI", "MACD"]
```

#### Strategy Parameters (`config/pipelines/model_training.yaml`)
```yaml
strategy_type: "momentum"
lookback_period: 20
risk_tolerance: 0.02
```

#### Environment Settings (`config/environments/`)
- `dev.yaml` - Development settings
- `staging.yaml` - Testing environment
- `prod.yaml` - Production parameters

### Output Structure

All analysis outputs are organized in `data/outputs/`:
```
data/outputs/
├── fundamental_analysis/  # Fundamental analysis results
├── sector_analysis/      # Sector-specific analysis
├── reports/             # Analysis reports (HTML, PDF, Markdown)
├── visualizations/      # Interactive Plotly charts (PNG, PDF, SVG, HTML)
├── dashboards/          # Performance dashboards with multi-format export
├── frontend_configs/    # JSON configurations for React integration
├── exports/            # Data exports (CSV, JSON, Parquet)
└── logs/              # Execution logs
```

### AI-Enhanced Analysis

Use AI commands to enhance your trading analysis:

```bash
# Analyze strategy performance
> "/architect - analyze the momentum strategy backtest results"

# Create social content about performance
> "/twitter-post-strategy - post about our AAPL analysis results"

# Prioritize strategy improvements
> "/product-owner - prioritize trading strategy enhancements"
```

---

## 🌐 Frontend Features

### Blog and Content Management

The Astro-powered frontend provides:

#### Multi-Author Blog System
- **Content Types**: Blog posts, pages, author profiles
- **Authoring**: Markdown/MDX with custom shortcodes
- **Organization**: Categories, tags, series support
- **SEO**: Automatic meta tags, sitemaps, RSS feeds

#### Theme System
- **Dark/Light Mode**: Automatic or manual toggle
- **Responsive Design**: Mobile-first with TailwindCSS
- **Customization**: Theme settings in `src/config/theme.json`

#### Interactive Features
- **Search**: Full-text search across all content
- **Comments**: Disqus integration
- **Analytics**: Google Tag Manager support
- **Social Sharing**: Automatic social media cards

### Development Workflow

#### Content Creation
```bash
cd frontend/

# Start development server
yarn dev

# Create new blog post
# Add file to src/content/blog/my-new-post.md

# Generate optimized builds
yarn build
```

#### Configuration Management
```bash
# Generate JSON configs from YAML
yarn generate-json

# Update all configurations
yarn format

# Type checking
yarn check
```

#### Testing and Quality
```bash
# Run tests
yarn test
yarn test:watch
yarn test:coverage

# Code quality
yarn lint
yarn format
yarn pre-commit
```

### Content Integration with Trading Analysis

The frontend automatically integrates with your trading analysis:

1. **Analysis Reports**: Automatically displayed in blog format
2. **Interactive Visualizations**: Plotly charts with hover, zoom, and pan capabilities
3. **Dashboard Integration**: Performance dashboards exported in multiple formats
4. **Frontend Components**: JSON schema configurations for React chart components
5. **Performance Updates**: AI-generated content from trading results
6. **Social Media**: Auto-generated posts about trading performance

### Configuration Files

#### Site Settings (`src/config/config.json`)
```json
{
  "title": "Sensylate Trading Analysis",
  "description": "Multi-modal trading strategy platform",
  "author": "Your Name",
  "social": {
    "twitter": "@yourhandle"
  }
}
```

#### Navigation (`src/config/menu.json`)
```json
{
  "main": [
    {"name": "Blog", "url": "/blog"},
    {"name": "Analysis", "url": "/analysis"},
    {"name": "About", "url": "/about"}
  ]
}
```

---

## 🤖 AI Commands

### Command Overview

Sensylate includes specialized AI commands for different aspects of your workflow:

#### Core Product Commands
- **`/twitter-post`**: Social media content optimization
- **`/twitter-post-strategy`**: Financial/trading content for social media
- **`/fundamental-analysis`**: Market analysis and trading insights

#### Infrastructure Commands (Development)
- **`/architect`**: Technical planning and implementation design
- **`/code-owner`**: Codebase health analysis and technical reviews
- **`/commit-push`**: Automated git workflow

#### Infrastructure Commands (Business)
- **`/product-owner`**: Business strategy and feature prioritization
- **`/business-analyst`**: Requirements analysis and process optimization

### Command Collaboration

Commands automatically work together:

#### Data Integration
```bash
> "/code-owner - analyze authentication security"
# Creates technical assessment

> "/architect - improve authentication based on analysis"
# References available analysis data
# Result: Data-informed implementation plan
```

#### Quality Enhancement
- **Context Awareness**: Commands understand project state from data/outputs/
- **Informed Decisions**: Analysis results inform AI responses
- **Consistency**: Aligned with existing analysis and project direction

### Usage Patterns

#### Individual Commands
```bash
# Direct command execution
> "/architect - implement user authentication"

# Specific context requests
> "/product-owner - prioritize Q2 features based on latest tech assessment"
```

#### Workflow Integration
```bash
# Analysis-informed workflows
> "Run comprehensive project analysis"

# Sequential command execution
> "/code-owner" followed by "/architect" followed by "/product-owner"
```

#### Context-Aware Content
```bash
# Content based on analysis data
> "/twitter-post about our latest performance improvements"

# Strategy-driven content using analysis results
> "/twitter-post-strategy for Q2 feature releases"
```

---

## ⚙️ Configuration

### Environment Configuration

#### Development Environment
```bash
# .env.development
NODE_ENV=development
API_BASE_URL=http://localhost:3000
LOG_LEVEL=debug
```

#### Production Environment
```bash
# .env.production
NODE_ENV=production
API_BASE_URL=https://api.sensylate.com
LOG_LEVEL=info
```

### Trading Analysis Configuration

#### Data Sources (`config/pipelines/data_extraction.yaml`)
```yaml
metadata:
  name: "Market Data Pipeline"
  version: "1.0.0"

input:
  api:
    endpoint: "https://api.tradingview.com/data"
    symbols: ["AAPL", "GOOGL", "TSLA"]
    timeframe: "1d"

output:
  file_path: "data/raw/market_data_{timestamp}.parquet"
  format: "parquet"

processing:
  indicators: ["SMA", "EMA", "RSI", "MACD"]
  validation: true
```

#### Strategy Parameters (`config/pipelines/model_training.yaml`)
```yaml
strategy:
  type: "momentum"
  parameters:
    lookback_period: 20
    signal_threshold: 0.02
    risk_management:
      max_position_size: 0.1
      stop_loss: 0.05
      take_profit: 0.15

backtesting:
  start_date: "2023-01-01"
  end_date: "2024-01-01"
  initial_capital: 100000
```

### Frontend Configuration

#### Site Configuration (`frontend/src/config/config.json`)
```json
{
  "site": {
    "title": "Sensylate",
    "description": "Multi-modal trading analysis platform",
    "author": "Your Name",
    "url": "https://sensylate.com"
  },
  "features": {
    "darkMode": true,
    "search": true,
    "comments": true,
    "analytics": true
  },
  "social": {
    "twitter": "@sensylate",
    "github": "sensylate/platform"
  }
}
```

#### Theme Settings (`frontend/src/config/theme.json`)
```json
{
  "colors": {
    "primary": "#3b82f6",
    "secondary": "#64748b",
    "accent": "#f59e0b"
  },
  "typography": {
    "headingFont": "Inter",
    "bodyFont": "Inter"
  },
  "layout": {
    "maxWidth": "1280px",
    "sidebar": true
  }
}
```

### AI Command Configuration

#### Data Output Structure (`data/outputs/`)
```yaml
analysis_outputs:
  fundamental_analysis:
    location: "data/outputs/fundamental_analysis/"
    format: "json, markdown"
    status: "active"
  sector_analysis:
    location: "data/outputs/sector_analysis/"
    format: "json, markdown"
    status: "active"

command_integration:
  data_sources: ["data/outputs/fundamental_analysis/", "data/outputs/sector_analysis/"]
  output_format: "markdown, json"
```

---

## 🔧 Troubleshooting

### Common Issues

#### Frontend Issues

**Issue**: Development server won't start
```bash
# Check Node.js version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules yarn.lock
yarn install

# Check for port conflicts
lsof -i :4321
```

**Issue**: Build failures
```bash
# Check TypeScript errors
yarn check

# Run linting
yarn lint

# Check configuration
yarn generate-json
```

#### Trading Analysis Issues

**Issue**: Data extraction fails
```bash
# Check API credentials
cat .env | grep API

# Validate configuration
make validate-configs

# Check network connectivity
ping api.tradingview.com
```

**Issue**: Pipeline execution errors
```bash
# Check Python environment
python --version  # Should be 3.9+
pip list | grep pandas

# Run individual steps
make extract-data
make process-data
make train-model
```

#### AI Command Integration Issues

**Issue**: Commands not accessing data
```bash
# Check data pipeline structure
ls data/outputs/
ls data/outputs/*/

# Verify recent analysis outputs
# Check Python script logs for any issues

# Test with simple workflow
> "/code-owner - quick project health check"
> "/architect - suggest one improvement"
```

**Issue**: Missing analysis context
```bash
# Check analysis data availability
ls data/outputs/fundamental_analysis/
ls data/outputs/sector_analysis/

# Verify recent analysis runs
find data/outputs -name "*.json" -mtime -1

# Run analysis if needed
make fundamental-analysis
```

### Performance Optimization

#### Frontend Performance
```bash
# Optimize images
yarn build --analyze

# Check bundle size
yarn build && ls -la dist/

# Lighthouse audit
yarn preview  # Then run Lighthouse on localhost:4321
```

#### Trading Analysis Performance
```bash
# Parallel execution
make -j4 full-pipeline

# Profile execution
time make extract-data

# Optimize data processing
# Edit config/pipelines/feature_engineering.yaml to reduce indicators
```

#### AI Command Performance
```bash
# Check data access patterns
ls -la data/outputs/*/

# Monitor analysis output freshness
find data/outputs -name "*.json" -mtime -1
```

### Getting Help

#### Log Files
- **Frontend**: Browser developer tools console
- **Trading Analysis**: `data/outputs/logs/`
- **AI Commands**: `.claude/commands/` directory

#### Debug Information
```bash
# System information
make check-env-vars
yarn check
python --version

# Analysis data status
ls -la data/outputs/*/
cat data/outputs/fundamental_analysis/latest.json
```

#### Contact Support
- **GitHub Issues**: [Repository issues page]
- **Documentation**: This manual and inline code documentation
- **Community**: [Discord/Slack if available]

---

## 📚 Additional Resources

- **[AI Command Documentation](.claude/commands/)**: Complete guide to AI command usage
- **[Technical Documentation](../README.md)**: Detailed technical implementation
- **[API Reference](../docs/API.md)**: Trading analysis API documentation
- **[Contributing Guide](../CONTRIBUTING.md)**: How to contribute to the project

---

**🎉 You're ready to use Sensylate!** This platform combines powerful trading analysis with intelligent AI collaboration to deliver superior insights and content. Start with the Quick Start guide above, then explore the advanced features as you become comfortable with the system.
