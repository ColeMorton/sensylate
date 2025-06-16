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

Sensylate features an advanced **Command Collaboration Framework** where AI agents work as a coordinated team. Commands automatically share context, data, and insights to deliver superior results.

### Command Locations

- **User Commands**: `/Users/colemorton/.claude/commands/` (global, cross-project)
- **Project Commands**: `/Users/colemorton/Projects/sensylate/.claude/commands/` (sensylate-specific)
- **Team Workspace**: `/team-workspace/` (collaboration data and outputs)

### Collaboration Benefits

- **🔄 Shared Context**: Commands read each other's outputs for enhanced decision-making
- **📊 Data Lineage**: Full traceability of how insights were derived
- **⚡ Performance**: 20% faster execution with team data, 89% faster with cache hits
- **🎯 Quality**: Higher confidence outputs through cross-command validation

### Available AI Team Members

Use these by asking Claude to execute them (e.g., "run the architect command" or "use /architect"):

#### Development & Architecture
- **`/architect`** - Technical planning & implementation framework with research-driven methodology
  - **Location**: `/Users/colemorton/.claude/commands/architect.md` (user scope)
  - **Collaboration**: Reads code-owner health metrics, business-analyst requirements
  - **Usage**: Research-driven phase-based implementation planning

- **`/code-owner`** - Comprehensive codebase health analysis and strategic technical reviews
  - **Location**: `/Users/colemorton/.claude/commands/code-owner.md` (user scope)
  - **Collaboration**: Provides technical health data to architect and product-owner
  - **Usage**: Technical debt assessment and architecture reviews

- **`/commit_push`** - Automated git workflow (stage all changes, generate commit message, push to remote)
  - **Location**: `/Users/colemorton/.claude/commands/commit_push.md` (user scope)
  - **Collaboration**: Can be triggered after architect implementation phases
  - **Usage**: Streamlined git operations with generated commit messages

#### Product Management
- **`/product_owner`** - Transform technical findings into prioritized product decisions with business impact analysis
  - **Location**: `/Users/colemorton/.claude/commands/product_owner.md` (user scope)
  - **Collaboration**: Consumes architect plans and code-owner assessments
  - **Usage**: Technical to business translation and prioritization

- **`/business_analyst`** - Requirements gathering, process optimization, and stakeholder alignment
  - **Location**: `/Users/colemorton/.claude/commands/business_analyst.md` (user scope)
  - **Collaboration**: Provides requirements to architect and product-owner
  - **Usage**: Process analysis and requirements documentation

#### Content Creation
- **`/twitter_post`** - Expert social media content optimization for X/Twitter engagement
  - **Location**: `/Users/colemorton/.claude/commands/twitter_post.md` (user scope)
  - **Collaboration**: Uses team workspace data for context-aware content
  - **Usage**: Social media content creation and optimization

- **`/twitter_post_strategy`** - Trading strategy analysis and social media post generation
  - **Location**: `/Users/colemorton/.claude/commands/twitter_post_strategy.md` (user scope)
  - **Collaboration**: Reads trading analysis data from outputs/exports/markdown/
  - **Usage**: Financial strategy content for social media

#### Utilities
- **`/create_command`** - Interactive command creator with validation and best practices
  - **Location**: `/Users/colemorton/.claude/commands/create_command.md` (user scope)
  - **Collaboration**: Can create project-specific commands in .claude/commands/
  - **Usage**: Generate new custom command templates

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

### Memory Notes
- **Architect Command Outputs**: Output from the architect commands should be saved into: `./team-workspace/commands/architect/outputs`
