# CLAUDE.md

This file provides critical guidance to Claude Code when working with this repository.

## Project Overview

Sensylate is a multi-modal platform combining **Python data processing**, **Astro frontend**, and **AI command collaboration** for trading strategy analysis and content generation.

**Tech Stack**:
- **Frontend**: Astro 5.7+ with TailwindCSS 4+, TypeScript, React, MDX
- **Backend**: Python with black, mypy, flake8 quality gates
- **Commands**: Project-scoped AI commands in `.claude/commands/`

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
- `team-workspace/` - AI command collaboration data

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

## AI Command Integration

**Command Locations**: `.claude/commands/` (project-scoped)

**Key Commands**:
- `/architect` - Technical planning and implementation
- `/code-owner` - Codebase health analysis
- `/twitter_post` - Social media content optimization

**Team Workspace**: Commands share context via `team-workspace/` for enhanced collaboration.

## Code Quality Principles

ALWAYS prefer editing an existing file to creating a new one.

**No narrative bloat**: Generate only essential comments that explain non-obvious business logic, avoiding redundant descriptions of what code obviously does.

**No leaky reasoning**: Keep implementation rationale internal; documentation should describe behavior and interface, never exposing underlying decision-making processes or alternatives considered.

**No historical artifacts**: Replace outdated patterns immediately when requirements change, maintaining consistent naming conventions and architectural approaches throughout the codebase.

**Strict YAGNI**: Implement only the specific functionality requested without anticipating future needs, avoiding generic frameworks or extensibility that isn't explicitly required.

## Project Configuration

**Timezone**: Brisbane, Australia (default)
**Memory Rules**: No author attribution in markdown unless requested
**Output Directories**: Command outputs saved to `team-workspace/commands/{command}/outputs/`
