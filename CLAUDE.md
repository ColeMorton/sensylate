# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Astroplate, an Astro + Tailwind CSS + TypeScript boilerplate for blogs and content sites. The project is located in the `frontend/` directory and built with:

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
```

## Architecture

### Content Management
- Content is authored in **Markdown/MDX** files in `src/content/`
- Authors, blog posts, pages managed via Astro's content collections
- Configuration-driven via JSON files in `src/config/`

### Component Structure
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
- `@/*` → `./src/*`

### Configuration System
Site settings, navigation, social links, and theme options are managed through JSON files in `src/config/`:
- `config.json` - Main site configuration
- `menu.json` - Navigation structure  
- `social.json` - Social media links
- `theme.json` - Theme settings

### Key Features
- Multi-author blog system
- Dark/light mode theming
- Search functionality  
- Tag and category taxonomy
- Responsive design with TailwindCSS
- Disqus comments integration
- Google Tag Manager support

## Custom Claude Commands

This project includes specialized workflow commands available in the `commands/` directory. Use these by asking Claude to execute them (e.g., "run the architect command" or "use /architect"):

### Development & Architecture
- **`/architect`** - Technical planning & implementation framework with research-driven methodology
  - Located: `commands/architect.md`
  - Usage: Research-driven phase-based implementation planning
  
- **`/code-owner`** - Comprehensive codebase health analysis and strategic technical reviews
  - Located: `commands/code-owner.md`
  - Usage: Technical debt assessment and architecture reviews
  
- **`/commit_push`** - Automated git workflow (stage all changes, generate commit message, push to remote)
  - Located: `commands/commit_push.md`
  - Usage: Streamlined git operations with generated commit messages

### Product Management
- **`/product_owner`** - Transform technical findings into prioritized product decisions with business impact analysis
  - Located: `commands/product_owner.md`
  - Usage: Technical to business translation and prioritization
  
- **`/business_analyst`** - Requirements gathering, process optimization, and stakeholder alignment
  - Located: `commands/business_analyst.md`
  - Usage: Process analysis and requirements documentation

### Content Creation
- **`/twitter_post`** - Expert social media content optimization for X/Twitter engagement
  - Located: `commands/twitter_post.md`
  - Usage: Social media content creation and optimization
  
- **`/twitter_post_strategy`** - Trading strategy analysis and social media post generation
  - Located: `commands/twitter_post_strategy.md`
  - Usage: Financial strategy content for social media

### Utilities
- **`/create_command`** - Interactive command creator with validation and best practices
  - Located: `commands/create_command.md`
  - Usage: Generate new custom command templates

**Note**: These are custom workflow commands, not built-in CLI slash commands. Reference them by name or use the `/` prefix when asking Claude to execute them.