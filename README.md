[![Netlify Status](https://api.netlify.com/api/v1/badges/f076302a-1a27-49d4-a2b9-0bfa3a5c84af/deploy-status)](https://app.netlify.com/projects/colemorton/deploys)

# Sensylate - Multi-Modal Data Processing & Content Creation Platform

## Project Overview

Sensylate is a sophisticated platform combining **Python data processing** with **Astro-powered frontend** and **AI-driven command collaboration**. The system excels at trading strategy analysis, content generation, and automated workflow orchestration.

### Core Capabilities

- **📊 Trading Analysis**: Automated backtesting, strategy optimization, and performance reporting
- **🤖 AI Command Collaboration**: Intelligent team of AI agents working together with shared context
- **🌐 Modern Frontend**: Astro-powered blog and content management system
- **⚙️ Data Processing**: Python + YAML + Makefile framework for robust pipelines
- **📱 Content Creation**: Automated social media content generation from analysis data

## Architecture

```
sensylate/
├── frontend/                  # Astro frontend (blog, content management)
│   ├── src/                   # Astro source code
│   ├── public/               # Static assets
│   └── package.json          # Frontend dependencies
├── scripts/                   # Python data processing
│   ├── data_extraction.py    # Market data extraction
│   ├── feature_engineering.py # Technical indicators
│   ├── model_training.py     # Strategy development
│   └── report_generation.py  # Analysis reports
├── configs/                   # YAML configurations
│   ├── data_extraction.yaml  # Data source configs
│   ├── shared/              # Shared configurations
│   └── environments/        # Environment-specific settings
├── team-workspace/           # AI Command Collaboration Framework
│   ├── commands/            # Command registry and workspaces
│   ├── shared/             # Cross-command shared data
│   └── sessions/           # Execution session logs
├── data/                     # Data storage hierarchy
│   ├── raw/                 # Market data, screenshots
│   ├── images/             # Trading platform screenshots
│   └── external/           # Reference data
└── outputs/                  # Generated content and analysis
    ├── exports/             # Data exports (CSV, JSON, MD)
    ├── visualizations/      # Charts and plots
    └── logs/               # Execution logs
```

## Quick Start

### Frontend Development

```bash
cd frontend/
yarn install
yarn dev                    # Start development server
yarn build                  # Build for production
yarn test                   # Run tests
yarn lint                   # Code quality checks
```

### Data Processing

```bash
# Run complete analysis pipeline
make full-pipeline

# Individual components
make extract-data           # Get market data
make process-data          # Generate features
make generate-report       # Create analysis

# Environment-specific
make dev-pipeline          # Development environment
make prod-pipeline         # Production environment
```

### AI Command Collaboration

```bash
# Enhanced command execution with Universal Evaluation
> "/architect - implement new trading strategy analyzer"
# → 4-phase evaluation with quality gates
# → Dependency validation with intelligent fallbacks
# → Template compliance with automatic fixes
# → Comprehensive implementation plan with quality metrics

> "/twitter-post about latest AAPL analysis"
# → Pre-execution validation of data dependencies
# → Content quality assessment and optimization
# → Social media engagement scoring
# → Output template enforcement
```

## Command Collaboration Framework

### Universal Evaluation Framework ✨

Sensylate features a **Universal Evaluation Framework** deployed across all 14 AI commands, ensuring consistent quality and intelligent dependency management:

**Quality Assurance**:
- **4-Phase Evaluation**: Pre-execution (0A), monitoring (0B), post-execution (0C), feedback integration (0D)
- **Intelligent Gating**: Adaptive quality thresholds with critical gate enforcement
- **Template Enforcement**: Consistent output formatting with automatic compliance fixes
- **Dependency Validation**: Real-time dependency health checks with intelligent fallback strategies

**Framework Benefits**:
- **🎯 100% Coverage**: All 14 commands integrated with Universal Evaluation protocols
- **⚡ Smart Dependencies**: Intelligent fallback management with 90% success rate
- **📊 Quality Metrics**: Comprehensive quality scoring and compliance tracking
- **🔧 Enhanced Wrappers**: Integrated command execution with evaluation protocols

### AI Team Members

Your AI team includes specialized agents that collaborate automatically:

#### Core Product Commands (User-facing AI functionality)
| Agent | Role | Capabilities |
|-------|------|-------------|
| **twitter-post** | Content Creation | Social media optimization, engagement analysis |
| **twitter-post-strategy** | Financial Content | Trading strategy posts, performance summaries |
| **fundamental-analysis** | Market Analysis | Trading strategies, market insights, performance analysis |

#### Infrastructure Commands (Development/business support)
| Agent | Role | Capabilities |
|-------|------|-------------|
| **architect** | Technical Planning | Implementation plans, risk assessment, architecture decisions |
| **product-owner** | Business Strategy | Prioritization, stakeholder alignment, business cases |
| **code-owner** | Technical Health | Codebase analysis, technical debt assessment, quality metrics |
| **business-analyst** | Requirements | Process optimization, functional specifications, acceptance criteria |

### Collaboration Benefits

- **🔄 Shared Context**: Commands read each other's outputs for enhanced decision-making
- **📊 Data Lineage**: Full traceability of how insights were derived
- **⚡ Performance**: 20% faster execution with team data, 89% faster with cache hits
- **🎯 Quality**: Higher confidence outputs through cross-command validation
- **📈 Learning**: Accumulated team knowledge improves over time
- **✅ Universal Quality**: 100% evaluation coverage with intelligent quality gates

## Data Processing Framework

### Configuration-Driven Architecture

```yaml
# Example: Trading data extraction
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

### Makefile Orchestration

```makefile
# Dependency-aware execution
trading-analysis: data/processed/features_$(TIMESTAMP).parquet
	$(PYTHON) scripts/model_training.py \
		--config configs/model_training.yaml \
		--input $< \
		--env $(ENV)

# Parallel execution support
backtest-strategies: strategy-momentum strategy-mean-reversion
	@echo "All strategies backtested"
```

## Technology Stack

### Backend (Data Processing)
- **Python 3.9+** - Core processing language
- **YAML** - Configuration management
- **Make** - Workflow orchestration
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Frontend (Content Management)
- **Astro 5.7+** - Static site generation
- **TypeScript** - Type safety
- **TailwindCSS 4+** - Modern styling
- **React** - Interactive components
- **MDX** - Content authoring

### AI Collaboration
- **Python** - Command discovery and dependency resolution
- **YAML** - Metadata and configuration schemas
- **File System** - Shared workspace for team data

## Trading Strategy Workflow

### 1. Data Collection
```bash
# Extract market data with technical indicators
make extract-data ENV=prod
```

### 2. Strategy Development
```bash
# Generate features and backtest strategies
make process-data
```

### 3. Analysis & Reporting
```bash
# Create comprehensive analysis reports
make generate-report
```

### 4. Content Creation
```bash
# Generate social media content from analysis
> "/twitter-post-strategy using latest AAPL backtest"
```

### 5. Publication
```bash
# Deploy to blog and social platforms
cd frontend/ && yarn build && yarn deploy
```

## Best Practices

### Data Management
- **Timestamped Files**: All outputs include ISO timestamps
- **Environment Separation**: Dev/staging/prod configurations
- **Atomic Operations**: Safe, rerunnable data processing
- **Backup Strategy**: Automatic backups of critical data

### Code Quality
- **DRY Principle**: No code duplication
- **SOLID Design**: Well-structured, maintainable code
- **Fail-Fast**: Meaningful exceptions over silent failures
- **Type Safety**: TypeScript for frontend, type hints for Python

### Workflow Management
- **Dependency Tracking**: Make ensures proper execution order
- **Parallel Execution**: Optimize performance with `make -j`
- **Error Propagation**: Failed steps stop the pipeline
- **Status Reporting**: Clear success/failure messages

## Command Integration

### Adding Project-Specific Commands

```bash
# Create project command
touch .claude/commands/sensylate-analyzer.md

# Register in collaboration framework
echo "sensylate-analyzer:
  location: ./.claude/commands/sensylate-analyzer.md
  scope: project
  type: analyzer" >> team-workspace/commands/registry.yaml
```

### Command Collaboration Protocol

```markdown
## Pre-Execution
1. Load team workspace context
2. Scan for relevant command outputs
3. Resolve dependencies and optimize with available data

## Post-Execution
1. Store output with rich metadata
2. Update team knowledge base
3. Notify dependent commands
4. Cache optimization data
```

## Development Setup

### Prerequisites
```bash
# Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend dependencies
cd frontend/ && yarn install

# Verify installation
make test
cd frontend/ && yarn test
```

### Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Configure API keys and database connections
# Edit .env with your specific settings
```

## Performance Optimization

### Caching Strategy
- **Session-based**: Cache expensive computations within sessions
- **Dependency-based**: Cache outputs based on input changes
- **Quality-based**: Cache high-confidence outputs longer

### Execution Optimization
- **Make Dependencies**: Only rebuild what's changed
- **Parallel Processing**: Multi-core utilization where possible
- **Smart Reuse**: Command collaboration reduces redundant work

## Contributing

### Code Standards
- Follow existing naming conventions (snake_case for Python, kebab-case for configs)
- Include comprehensive tests for new functionality
- Document command dependencies and outputs
- Maintain configuration-driven design

### Command Development
- Define clear input/output specifications
- Include metadata schema compliance
- Implement collaboration protocol
- Provide usage examples and documentation

---

**Sensylate** transforms traditional data processing into an intelligent, collaborative system where AI agents work together to deliver superior analysis, content, and insights. The platform scales from individual research to automated content creation pipelines.
