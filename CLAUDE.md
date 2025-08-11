# CLAUDE.md

This file provides critical guidance to Claude Code when working with this repository.

## Project Overview

Sensylate is a multi-modal platform combining **Python data processing** and **Astro frontend** for trading strategy analysis and content generation.

**Tech Stack**:
- **Frontend**: Astro 5.7+ with TailwindCSS 4+, TypeScript, React, MDX
- **Backend**: Python with black, mypy, flake8 quality gates
- **Data Pipeline**: Python scripts generate analysis outputs for frontend consumption

## Essential Commands

**Frontend** (run from `frontend/` directory):
```bash
yarn dev                 # Development server
yarn build               # Production build
yarn check               # TypeScript checking
yarn lint                # ESLint with auto-fix
yarn test                # Run tests
```

**Python** (run from root directory):
```bash
make format              # Format with black/isort
make lint                # Lint with flake8
make test                # Run Python tests
```

**Quality Gates**:
```bash
pre-commit run --all-files    # Run all quality checks
```

## Architecture

**Directory Structure**:
- `frontend/src/content/` - Markdown/MDX content
- `frontend/src/config/` - JSON configuration files
- `frontend/src/layouts/` - Astro components and templates
- `scripts/` - Python data processing
- `data/outputs/` - Analysis outputs and generated content

**Path Aliases**:
- `@/components/*` → `./src/layouts/components/*`
- `@/helpers/*` → `./src/layouts/helpers/*`
- `@/config/*` → `./src/config/*`
- `@/*` → `./src/*`

## Quality Standards

**Automated Quality Gates** (fail-fast approach):
- **Python**: black (88-char), isort, flake8, mypy, bandit
- **TypeScript**: prettier, eslint (React/Astro rules)
- **General**: trailing whitespace, file endings, syntax validation

All quality checks run on every commit. Failed checks prevent commits.

## Data Processing Pipeline

**Core Scripts**: Located in `scripts/` directory

**Key Capabilities**:
- Fundamental analysis generation
- Trading strategy analysis
- Social media content optimization
- Market data processing

**Data Flow**: Python scripts → `data/outputs/` → Frontend display

## Code Quality Principles

ALWAYS prefer editing an existing file to creating a new one.

**No narrative bloat**: Generate only essential comments that explain non-obvious business logic, avoiding redundant descriptions of what code obviously does.

**No leaky reasoning**: Keep implementation rationale internal; documentation should describe behavior and interface, never exposing underlying decision-making processes or alternatives considered.

**No historical artifacts**: Replace outdated patterns immediately when requirements change, maintaining consistent naming conventions and architectural approaches throughout the codebase.

**Strict YAGNI**: Implement only the specific functionality requested without anticipating future needs, avoiding generic frameworks or extensibility that isn't explicitly required.

## Documentation Lifecycle Rules

**CRITICAL**: Prevent documentation bloat through strict YAGNI enforcement.

**Documentation Minimization Standards**:
- **Single Source of Truth**: All DASV framework information consolidated in `.claude/DASV_Framework_Specification.md`
- **No Analysis Reports**: Implementation summaries limited to `.claude/DASV_Implementation_Summary.md` only
- **Agent Specifications**: Essential definitions only in `.claude/agents/` (50 lines max per agent)
- **Framework Documentation**: Maximum 1,000 lines for complete framework specification

**Anti-Bloat Enforcement**:
- **No Multiple Specifications**: Consolidate overlapping documentation immediately
- **No Analysis Reports**: Delete detailed reports, preserve essential outcomes only
- **No Historical Artifacts**: Remove outdated documentation when requirements change
- **No Duplicate Framework Files**: Single master specification serves all needs

**Creation Restrictions**:
- **Prohibited**: New documentation files in `docs/analysis_reports/`, `docs/specifications/`
- **Prohibited**: Framework explanation files beyond master specification
- **Prohibited**: Implementation detail documentation (delegate to sub-agents)
- **Required**: All new documentation must justify existence and consolidate existing content

## Project Configuration

**Timezone**: Brisbane, Australia (default)
**Memory Rules**: No author attribution in markdown unless requested
**Output Directories**: Outputs saved to `data/outputs/`
