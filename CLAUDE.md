# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sensylate is a multi-modal platform combining **Python data processing**, **Astro frontend**, and **AI command collaboration**. The system specializes in trading strategy analysis, content generation, and automated workflow orchestration.

### Core Components

**Frontend** (content management) located in the `frontend/` directory:

- **Astro 5.7+** as the main framework
- **TailwindCSS 4+** for styling
- **TypeScript** for type safety
- **React** for interactive components
- **MDX** for content authoring

## Development Commands

All commands should be run from the `frontend/` directory:

```bash
# Install dependencies
yarn install

# Start development server (generates JSON config first)
yarn dev

# Build for production (generates JSON config first)
yarn build

# Preview production build
yarn preview

# Type checking
yarn check

# Format code with Prettier
yarn format

# Generate JSON configuration files
yarn generate-json

# Remove dark mode and format
yarn remove-darkmode

# Testing
yarn test                # Run tests once
yarn test:watch          # Run tests in watch mode
yarn test:coverage       # Run tests with coverage report

# Code Quality
yarn lint                # Run ESLint and auto-fix issues
yarn lint:check          # Run ESLint without fixing
yarn check-git-tracking  # Check for untracked files being imported (prevents build failures)
yarn pre-commit          # Run all pre-commit checks manually

# Python Development (from root directory)
make format              # Format Python code with black and isort
make lint                # Run flake8 linting and black check
make test                # Run Python tests
python3 -m mypy scripts/ # Type checking for Python code

# Pre-commit Quality Enforcement
pre-commit run --all-files  # Run all quality checks on entire codebase
pre-commit install          # Install git hooks (already done)
pre-commit uninstall        # Remove git hooks if needed
```

## Quality Standards

This project enforces comprehensive code quality standards through automated pre-commit hooks:

**Python Quality Gates (scripts/ directory)**:
- **black**: Automatic code formatting (88-character line length)
- **isort**: Import statement sorting and organization
- **flake8**: Code linting and style checking
- **mypy**: Static type checking with import validation
- **bandit**: Security vulnerability scanning

**TypeScript/Frontend Quality Gates (frontend/ directory)**:
- **prettier**: Code formatting with Astro and TailwindCSS plugins
- **eslint**: Linting with React, TypeScript, and Astro rules

**General Quality Enforcement**:
- Trailing whitespace removal
- Consistent file endings
- YAML/JSON syntax validation
- Large file prevention
- Merge conflict detection

All quality checks run automatically on every commit. Failed checks prevent commits from proceeding.

## Platform Architecture

### Multi-Component System
- **Frontend**: Astro-powered blog and content management (`frontend/`)
- **Data Processing**: Python + YAML + Makefile framework (`scripts/`, `configs/`)
- **AI Collaboration**: Command team workspace (`team-workspace/`)
- **Content Pipeline**: Automated analysis → content generation → publication

### Frontend (Content Management)
- Content is authored in **Markdown/MDX** files in `src/content/`
- Authors, blog posts, pages managed via Astro's content collections
- Configuration-driven via JSON files in `src/config/`

#### Component Structure
- **Layouts**: Core page templates in `src/layouts/`
- **Components**: Reusable UI components in `src/layouts/components/`
- **Shortcodes**: MDX shortcodes in `src/layouts/shortcodes/`
- **Partials**: Page sections in `src/layouts/partials/`
- **Helpers**: React utilities in `src/layouts/helpers/`

### Path Aliases
TypeScript paths are configured for clean imports:
- `@/components/*` → `./src/layouts/components/*`
- `@/shortcodes/*` → `./src/layouts/shortcodes/*`
- `@/helpers/*` → `./src/layouts/helpers/*`
- `@/partials/*` → `./src/layouts/partials/*`
- `@/lib/*` → `./src/lib/*`
- `@/config/*` → `./src/config/*`
- `@/layouts/*` → `./src/layouts/*`
- `@/*` → `./src/*`

### Configuration System
Site settings, navigation, social links, and theme options are managed through JSON files in `src/config/`:
- `config.json` - Main site configuration
- `menu.json` - Navigation structure
- `social.json` - Social media links
- `theme.json` - Theme settings

### Key Platform Features

#### Frontend Capabilities
- Multi-author blog system with trading strategy content
- Dark/light mode theming
- Search functionality and tag/category taxonomy
- Responsive design with TailwindCSS
- Disqus comments integration
- Google Tag Manager support
- Docker support for containerized deployment
- Vitest testing framework with jsdom environment
- Auto-import for MDX shortcodes

#### Data Processing & Analysis
- Automated trading strategy backtesting
- Market data extraction and feature engineering
- Configuration-driven Python pipelines
- Makefile orchestration with dependency tracking
- Multi-environment support (dev/staging/prod)
- Timestamped outputs and data lineage

#### AI Command Collaboration
- Team of specialized AI agents working together
- Shared context and data between commands
- Automatic dependency resolution and optimization
- Performance caching and team knowledge accumulation
- Cross-command validation and quality assurance
- Session tracking and execution logs

## AI Command Collaboration Framework

Sensylate features an advanced **Command Collaboration Framework** with **Content Lifecycle Management** where AI agents work as a coordinated team. Commands automatically share context, prevent duplication, and maintain knowledge integrity through systematic content lifecycle management.

### Command Locations

**All commands are project-scoped** and located in:
- **Project Commands**: `/Users/colemorton/Projects/sensylate/.claude/commands/` (sensylate-specific)
- **Team Workspace**: `/team-workspace/` (collaboration data and outputs)

This ensures consistent command behavior and project-specific optimization.

### Collaboration Benefits

- **🔄 Shared Context**: Commands read each other's outputs for enhanced decision-making
- **📊 Data Lineage**: Full traceability of how insights were derived
- **⚡ Performance**: 20% faster execution with team data, 89% faster with cache hits
- **🎯 Quality**: Higher confidence outputs through cross-command validation
- **🚫 Duplication Prevention**: 25% conflict reduction through pre-execution consultation
- **📋 Content Authority**: Single source of truth maintained for all knowledge topics
- **🔄 Lifecycle Management**: Proper content superseding with full audit trails
- **👥 Ownership Coordination**: Clear topic ownership and collaboration permissions

### Available AI Team Members

Use these by asking Claude to execute them (e.g., "run the architect command" or "use /architect"):

#### **Core Product Commands** (User-facing AI functionality)
- **`/twitter_post`** - Expert social media content optimization for X/Twitter engagement
  - **Location**: `.claude/commands/twitter_post.md` (project scope)
  - **Collaboration**: Uses team workspace data for context-aware content
  - **Usage**: Social media content creation and optimization

- **`/twitter_post_strategy`** - Trading strategy analysis and social media post generation
  - **Location**: `.claude/commands/twitter_post_strategy.md` (project scope)
  - **Collaboration**: Reads trading analysis data from outputs/exports/markdown/
  - **Usage**: Financial strategy content for social media

- **`/fundamental_analysis_full`** - Complete DASV workflow for institutional-quality fundamental analysis
  - **Location**: `.claude/commands/fundamental_analysis_full.md` (project scope)
  - **Collaboration**: Orchestrates four specialized microservices through DASV framework
  - **Usage**: Comprehensive market analysis and trading insights via microservice architecture

#### **Collaboration Infrastructure Commands** (Enable product development)

##### Development & Architecture
- **`/architect`** - Technical planning & implementation framework with research-driven methodology
  - **Location**: `.claude/commands/architect.md` (project scope)
  - **Collaboration**: Reads code-owner health metrics, business-analyst requirements
  - **Usage**: Research-driven phase-based implementation planning

- **`/code-owner`** - Comprehensive codebase health analysis and strategic technical reviews
  - **Location**: `.claude/commands/code-owner.md` (project scope)
  - **Collaboration**: Provides technical health data to architect and product-owner
  - **Usage**: Technical debt assessment and architecture reviews

- **`/commit_push`** - Automated git workflow (stage all changes, generate commit message, push to remote)
  - **Location**: `.claude/commands/commit_push.md` (project scope)
  - **Collaboration**: Can be triggered after architect implementation phases
  - **Usage**: Streamlined git operations with generated commit messages

##### Product Management
- **`/product_owner`** - Transform technical findings into prioritized product decisions with business impact analysis
  - **Location**: `.claude/commands/product_owner.md` (project scope)
  - **Collaboration**: Consumes architect plans and code-owner assessments
  - **Usage**: Technical to business translation and prioritization

- **`/business_analyst`** - Requirements gathering, process optimization, and stakeholder alignment
  - **Location**: `.claude/commands/business_analyst.md` (project scope)
  - **Collaboration**: Provides requirements to architect and product-owner
  - **Usage**: Process analysis and requirements documentation

##### Command Management
- **`/command`** - Comprehensive command lifecycle management specialist with systematic methodology
  - **Location**: `.claude/commands/command.md` (project scope)
  - **Collaboration**: Full command management including creation, optimization, alignment, analysis, and maintenance
  - **Usage**: Complete command lifecycle management (create, optimize, align, analyze, maintain)

- **`/documentation_owner`** - Documentation lifecycle & quality management with institutional standards
  - **Location**: `.claude/commands/documentation_owner.md` (project scope)
  - **Collaboration**: Ensures documentation quality across all commands and maintains consistency
  - **Usage**: Documentation quality audits, template standardization, content lifecycle management

### Workflow Examples

```bash
# Enhanced execution with team collaboration
> "/architect - implement new trading strategy analyzer"
# → Automatically reads business requirements from business-analyst
# → Incorporates technical health metrics from code-owner
# → Generates comprehensive implementation plan

# Coordinated analysis workflow
> "Run comprehensive project analysis"
# → Executes: code-owner → product-owner → architect
# → Each command builds on previous outputs

# Context-aware content creation
> "/twitter-post about our latest AAPL analysis"
# → Finds recent trading analysis from team workspace
# → Creates engaging, data-driven social media content
```

**Note**: These are custom workflow commands with AI collaboration capabilities. Commands automatically share context and data through the team workspace for enhanced results.

## Content Lifecycle Management Integration

All AI commands **MUST** integrate with the Content Lifecycle Management system to prevent duplication and maintain knowledge integrity:

**Mandatory Pre-execution Requirements**: All commands must complete both workspace validation and content consultation before execution.

### Before Creating Any Analysis

**Required**: Run pre-execution consultation before starting new analysis:

```bash
python team-workspace/coordination/pre-execution-consultation.py <command_name> <topic> "<scope>"
```

**Example**:
```bash
python team-workspace/coordination/pre-execution-consultation.py architect technical-health "comprehensive security analysis"
```

### Integration Workflow

1. **Consult**: Check for existing knowledge and get coordination guidance
2. **Decide**: Use decision tree for structured update-vs-new analysis decisions
3. **Coordinate**: Work with topic owners when necessary
4. **Execute**: Create or update content following system guidance
5. **Supersede**: Use proper superseding workflow when replacing existing content

### Quick Commands

```bash
# Check topic ownership
python team-workspace/coordination/topic-ownership-manager.py ownership <topic>

# Get collaboration guidance
python team-workspace/coordination/decision-tree.py <command> <topic> "<scope>"

# Monitor system health
python team-workspace/coordination/knowledge-dashboard.py

# Declare content superseding
python team-workspace/coordination/superseding-workflow.py declare <command> <topic> <new_file> <old_files> "reason"
```

### Knowledge Structure

All authoritative content is organized in topic-centric structure:

```
team-workspace/knowledge/
├── technical-health/          # Technical assessments (owner: code-owner)
├── implementation-plans/      # Implementation plans (owner: architect)
├── product-strategy/         # Product decisions (owner: product-owner)
└── requirements/             # Requirements analysis (owner: business-analyst)
```

### Content Authority Rules

- **Single Source of Truth**: Each topic has one authoritative file in `knowledge/`
- **Proper Superseding**: Use superseding workflow when replacing content
- **Archive Preservation**: Superseded content archived with full recovery metadata
- **Ownership Respect**: Coordinate with topic owners before making changes

**Failure to integrate with lifecycle management will result in content conflicts and degraded team-workspace effectiveness.**

### Command Output Location Standards

**CRITICAL**: Command output locations are strictly defined by classification:

**Infrastructure Commands** (Collaboration enabling):
- **Architect**: `./team-workspace/commands/architect/outputs/`
- **Code Owner**: `./team-workspace/commands/code-owner/outputs/`
- **Product Owner**: `./team-workspace/commands/product-owner/outputs/`
- **Business Analyst**: `./team-workspace/commands/business-analyst/outputs/`
- **Command Management**: `./team-workspace/commands/command/outputs/`
- **Documentation Owner**: `./team-workspace/commands/documentation-owner/outputs/`

**Product Commands** (User-facing functionality):
- **Social Media**: `./outputs/social-media/` (twitter_post, twitter_post_strategy, twitter_fundamental_analysis, twitter_trade_history)
- **Trading**: `./outputs/trading/` (trade_history), `./outputs/trading/images/` (trade_history_images)
- **Content**: `./outputs/published/` (content_publisher), `./outputs/evaluations/` (content_evaluator)
- **Strategy**: `./outputs/social-strategy/` (social_media_strategist)
- **Analysis**: `./data/outputs/fundamental_analysis/` (fundamental_analysis_full)

**Microservices** (DASV Framework):
- **Discovery**: `./data/outputs/fundamental_analysis/discovery/`
- **Analysis**: `./data/outputs/fundamental_analysis/analysis/`
- **Synthesis**: `./data/outputs/fundamental_analysis/`
- **Validation**: `./data/outputs/fundamental_analysis/validation/`

### Command Framework Standards

**LEGITIMATE Frameworks Only**:
- **DASV** (Discover-Analyze-Synthesize-Validate) - Microservices only
- **RPIV** (Research-Plan-Implement-Validate) - Architect command
- **DQEM** (Document-Quality-Enforce-Maintain) - Documentation Owner
- **COALA** (Command-Optimization-Alignment-Lifecycle-Analysis) - Command Management

**PROHIBITED**: Any fictional or invented framework acronyms not documented in the command registry.

### Memory Notes

### Memory Guidance
- **Always refer to the current date and year to ensure the latest up-to-date data**

### Project Timezone Configuration
- The Brisbane, Australia timezone is the default timezone.

### Memory Rules
- Do not include author in markdown files unless specifically asked
- Never invent fictional framework acronyms - only use documented frameworks
- Strictly enforce output location standards based on command classification
- All commands must maintain pre-execution coordination integration
