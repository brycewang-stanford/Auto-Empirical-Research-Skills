<!-- Vendored into AERS from https://github.com/ab604/claude-code-r-skills on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`ab604/claude-code-r-skills`](https://github.com/ab604/claude-code-r-skills) for the AERS catalog (license: MIT). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# Claude Code R Skills

*Version 1.2.4 | Last updated: 2026-04-05*

A curated collection of Claude Code configurations for modern R use. These skills, rules, commands, and agents help Claude Code understand R best practices and generate idiomatic, high-quality R code. Additionally the rules and commands help with efficient token usage and enforce constraints, and agents can perform specific tasks. Obviously you can fork and adapt any of these to your case-use.

I use Positron, but if you are a VSCode user there is also a plugin for R language server for code intelligence.

To try and pre-empt some of the issues with LLMs being reinforced to please the user, I've added a scientific reasoning principle to CLAUDE.md: we test hypotheses; we never prove them. Claude is instructed to reason from evidence, maintain healthy scepticism, quantify uncertainty explicitly (preferring Bayesian framing), and never tell the user what it thinks the user wants to hear at the expense of accuracy. This doesn't seem to prevent the "telling you what it thinks you want to hear" problem entirely, but is hopefully better than nothing.

## Table of Contents

-   [Acknowledgments](#acknowledgments)
-   [Overview](#overview)
-   [Understanding Feature Types](#understanding-feature-types)
    -   [Skills](#skills)
    -   [Commands](#commands)
    -   [Rules](#rules)
    -   [Agents](#agents)
    -   [Hooks](#hooks)
    -   [Contexts](#contexts)
-   [Features](#features)
-   [Installation](#installation)
    -   [Option 1: Plugin Marketplace](#option-1-plugin-marketplace-recommended)
    -   [Option 2: Copy to your project](#option-2-copy-to-your-project)
    -   [Option 3: Copy to user configuration](#option-3-copy-to-user-configuration)
-   [Quick Reference](#quick-reference)
    -   [Essential Modern R Patterns](#essential-modern-r-patterns)
    -   [Key Anti-Patterns to Avoid](#key-anti-patterns-to-avoid)
-   [Directory Structure](#directory-structure)
-   [Core Principles](#core-principles)
-   [Recommended Workflow](#recommended-workflow)
-   [Requirements](#requirements)
-   [Environment Management](#environment-management)
-   [Token Optimization](#token-optimization)
-   [License](#license)

## Acknowledgments

This project uses and builds on the work of:

-   [**Sarah Johnson's Modern R Development Guide**](https://gist.github.com/sj-io/3828d64d0969f2a0f05297e59e6c15ad) - Original guide that formed the foundation for the R skills in this repository

-   [**Jeremy Allen's Claude Skills Repo**](https://github.com/jeremy-allen/claude-skills) - Jeremy's Claude Skills mostly derived from Sarah's guide

-   [**Affaan Mustafa's Everything Claude Code**](https://github.com/affaan-m/everything-claude-code) - Framework structure, rules, commands, and agents adapted for R development from Affan's Hackathon winning code

-   [**Posit's testing-r-packages Skill**](https://github.com/posit-dev/skills/tree/main/r-lib/testing-r-packages) - testthat Edition 3 patterns, test design principles, and comprehensive expectations reference incorporated into the tdd-workflow skill

-   [**statzhero's tidy-r-skill**](https://github.com/statzhero/tidy-r-skill) - Join quality control patterns (`relationship`, `na_matches`, `tidylog`), NA-safe filtering with `filter_out()`, `when_any()`/`when_all()`, `replace_when()` for in-place conditional updates, and `cli::cli_abort()` structured error messages incorporated into the tidyverse-patterns and r-style-guide skills

-   As an aside, I use Quarto in my workflow and use [Posit's Quarto plugin](https://github.com/posit-dev/skills) which you can add with: `/plugin marketplace add posit-dev/skills` and then `/plugin install quarto@posit-dev-skills`.

## Overview

This repository provides Claude Code configurations specifically for R users, combining:

-   **R-specific skills** for modern tidyverse patterns, rlang, performance, OOP, and more
-   **Development workflow tools** adapted from [everything-claude-code](https://github.com/affaan-m/everything-claude-code)
-   **Testing and quality rules** for R development

## Understanding Feature Types

Claude Code uses five official feature types to customise its behaviour for R development, plus a custom convention (Contexts) built on the CLI's `--system-prompt` flag. Each serves a distinct purpose in the development workflow.

### Skills

**What they are:** Markdown documents containing domain knowledge, best practices, and coding patterns that Claude references when writing code. Skills are passive knowledge resources loaded into Claude's context when relevant.

**When to use:** Claude automatically activates skills based on the code you're working on. For example, when you're writing tidyverse code, the `tidyverse-patterns` skill provides guidance on modern pipes, joins, and grouping.

**How they work:** Skills live in `.claude/skills/` and contain detailed guidance, anti-patterns to avoid, and code examples. Claude consults these when making implementation decisions.

**How to use:**

``` bash
# Skills are automatically activated - no manual invocation needed
# You can also explicitly request skill usage in your prompts:
"Write a function using tidyverse-patterns to summarize data by group"
```

### Commands

**What they are:** User-invocable shortcuts (prefixed with `/`) that trigger specific workflows or behaviours. Commands are active - you call them explicitly to perform actions.

**When to use:** Use commands when you want Claude to follow a specific workflow, such as planning before implementation (`/plan`) or conducting a code review (`/code-review`).

**How they work:** Commands are defined in the `commands/` directory and can trigger agents, enforce specific behaviours, or structure Claude's responses in particular ways.

**How to use:**

``` bash
# In your Claude Code conversation:
/plan Add bootstrap confidence intervals to model output

# After seeing the plan, respond:
yes  # or "proceed" to start implementation

# Review code before committing:
/code-review
```

### Rules

**What they are:** Mandatory constraints and requirements that Claude must follow. Rules enforce project standards like test coverage thresholds, security practices, and git workflows.

**When to use:** Rules are always active - Claude automatically enforces them throughout the session. They're particularly important for maintaining code quality, security, and testing standards.

**How they work:** Rules are markdown files in the `rules/` directory that define requirements (e.g., "80% test coverage required") and constraints (e.g., "never commit credentials"). Claude validates actions against these rules.

**How to use:**

``` bash
# Rules are automatically enforced - no manual invocation needed
# Claude will:
# - Require 80% test coverage (from testing.md)
# - Validate credential handling (from security.md)
# - Format commits correctly (from git-workflow.md)

# You can reference rules explicitly:
"Make sure this follows our testing rules"
```

### Agents

**What they are:** Specialized sub-agents with specific roles, expertise, and limited tool access. Agents are focused workers that handle particular types of tasks.

**When to use:** Agents are invoked by commands or automatically by Claude when specialised expertise is needed. The `planner` agent creates implementation plans, while the `code-reviewer` agent analyses code for issues.

**How they work:** Agents are defined in the `agents/` directory with specific tools and prompts. They receive a task, complete it with their specialised knowledge, and return results to the main conversation.

**How to use:**

``` bash
# Agents are typically invoked via commands:
/plan Feature description      # Activates the planner agent
/code-review                   # Activates the code-reviewer agent

# Claude may also invoke agents automatically when appropriate
```

### Hooks

**What they are:** Event-driven JavaScript scripts that execute automatically at specific points in Claude's workflow (e.g., before editing files, on session start/end, before context compaction).

**When to use:** Hooks run automatically in response to events - you don't invoke them directly. They're useful for context management, state persistence, and workflow optimisations.

**How they work:** Hooks are configured in `hooks/hooks.json` (for plugin users) and `.claude/settings.json` (for repo development). Matchers use simple tool names (`"Bash"`, `"Write"`, `"Edit|Write"`, `"*"`). Script-based hooks reference files via `${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/`; simple hooks use inline `node -e` commands.

**How to use:**

``` bash
# Hooks run automatically. Configured hooks in this repo:
# - suggest-compact: Suggests /compact after 50 tool uses
# - pre-compact: Saves session state before compaction
# - session-start: Reports available history on startup
# - session-end: Persists session state for continuity
# - doc-blocker: Warns about creating random .md files
# - git-push-warn: Warns before any git push

# Hooks are transparent - you'll see their output in the session:
[StrategicCompact] 50 tool calls reached - consider /compact if transitioning phases
[Hook] WARNING: About to run: git push origin main
[Hook] Confirm this push is intentional before proceeding.
```

### Contexts

**What they are:** Dynamic system prompt injection contexts — markdown files containing scenario-specific instructions passed to Claude at session start via the `--system-prompt` CLI flag.

**When to use:** Use a context alias when starting a session with a specific focus. Your `.claude/rules/` files handle baseline project rules; contexts layer scenario-specific behaviour on top.

**How they work:** Shell aliases inject context files as system prompts when launching Claude — no tool call overhead, system-level authority.

**How to use:**

``` bash
# Add to ~/.bashrc or ~/.zshrc
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'

# Launch Claude in the mode you need:
claude-research    # Exploration mode
claude-dev         # Implementation mode
claude-review      # Code quality/security review
```

> **Note:** For most workflows the difference between placing context in `.claude/rules/` and using the CLI `--system-prompt` approach is marginal. The CLI approach is faster (no tool call), more reliable (system-level authority), and slightly more token-efficient — but requires shell setup and may not be worth the overhead for everyone.

**Recommended workflow sequence:**

```
claude-research → /plan → claude-dev → /tdd → implement → /verify → claude-review → commit
```

## Features

### Skills (8 public + 1 local)

| Skill | Description |
|--------------------------|----------------------------------------------|
| **tidyverse-patterns** | Modern pipes, joins, grouping, purrr, stringr |
| **rlang-patterns** | Data-masking, injection operators, dynamic dots |
| **r-performance** | Profiling, benchmarking, vctrs, optimisation |
| **r-style-guide** | Naming, spacing, function design |
| **r-oop** | S7, S3, S4, vctrs decision guide |
| **r-package-development** | Dependencies, API design, testing |
| **r-bayes** | brms, DAG validation, multilevel models, marginaleffects |
| **tdd-workflow** | Test-driven development with testthat |

*Local-only (not in public repo):*

| Skill                  | Description                                        |
|-----------------------|-------------------------------------------------|
| **r-machine-learning** | XGBoost, LightGBM, CatBoost, Elastic Net, ExtraTrees, ridge stacking, stratified CV — updated 2026-02-20 |

### Commands

| Command        | Description                                        |
|----------------|----------------------------------------------------|
| `/plan`        | Create implementation plans before coding          |
| `/tdd`         | Test-driven development workflow                   |
| `/code-review` | Review code for security and quality               |
| `/verify`      | Full quality gate before committing (build → lint → coverage → review) |

### Rules

| Rule             | Description                          |
|------------------|--------------------------------------|
| **security**     | Credential handling, data protection |
| **testing**      | 80% coverage, testthat patterns      |
| **git-workflow** | Commit format, PR workflow           |

### Agents

| Agent             | Model | Description                        |
|-------------------|-------|------------------------------------|
| **planner**       | Opus  | Implementation planning specialist |
| **tdd-guide**     | —     | TDD enforcement and test-first workflow |
| **code-reviewer** | —     | Security and quality review        |

### Hooks (Context Window Management)

| Hook | Trigger | Description |
|---------------------|------------------------|--------------------------------|
| **suggest-compact** | PreToolUse (Edit/Write) | Suggests `/compact` after 50 tool calls, then every 25 |
| **pre-compact** | PreCompact | Saves session state before context compaction |
| **session-start** | SessionStart | Reports available session history and learned skills |
| **session-end** | SessionEnd | Persists session state for continuity |
| **doc-blocker** | PreToolUse (Write .md) | Warns about creating random .md files |
| **git-push-warn** | PreToolUse (Bash) | Warns before any `git push` to prevent accidental pushes |

These hooks help optimise context window usage and workflow safety by:

-   Suggesting strategic compaction at logical task boundaries
-   Preserving session state across compaction events
-   Consolidating documentation to reduce context bloat
-   Requiring confirmation before irreversible git operations

### Contexts

System prompt injection contexts — launch Claude with a specific focus using CLI aliases (`--system-prompt`).

| Context      | Description                                        |
|--------------|----------------------------------------------------|
| **dev**      | Implementation focus — write first, short responses, TDD defaults |
| **research** | Exploration focus — thorough reading before acting  |
| **review**   | Audit focus — find issues, rate by severity, verdict |

## Installation

### Option 1: Plugin Marketplace (recommended)

``` bash
# Add the marketplace
/plugin marketplace add ab604/claude-code-r-skills

# Install R skills
/plugin install r-skills@r-skills

# Install R language server (optional, for code intelligence in VS Code/terminal)
# Note: Not needed if using Positron, which has built-in R language server support
/plugin install r-lsp@r-skills
```

The `r-lsp` plugin requires the R languageserver package:

``` r
install.packages(c("languageserver", "lintr", "styler"))
```

See [r-lsp](https://github.com/ab604/r-lsp) for more details.

### Option 2: Copy to your project

``` bash
# Clone this repository
git clone https://github.com/ab604/claude-code-r-skills.git

# Copy to your R project
cp -r claude-code-r-skills/.claude/ /path/to/your/project/
cp -r claude-code-r-skills/rules/ /path/to/your/project/
cp -r claude-code-r-skills/commands/ /path/to/your/project/
cp -r claude-code-r-skills/agents/ /path/to/your/project/
cp -r claude-code-r-skills/contexts/ /path/to/your/project/
```

### Option 3: Copy to user configuration

``` bash
# Create directories if they don't exist, then copy
mkdir -p ~/.claude/skills ~/.claude/rules ~/.claude/commands ~/.claude/agents ~/.claude/contexts

# Copy skills to global config
cp -r .claude/skills/* ~/.claude/skills/

# Copy rules, commands, agents, contexts
cp -r rules/* ~/.claude/rules/
cp -r commands/* ~/.claude/commands/
cp -r agents/* ~/.claude/agents/
cp -r contexts/* ~/.claude/contexts/
```

## Quick Reference

### Essential Modern R Patterns

``` r
# Always use native pipe
data |>
  filter(x > 0) |>
  summarise(mean(y))

# Modern joins with join_by()
inner_join(x, y, by = join_by(a == b))

# Per-operation grouping with .by
summarise(data, mean(value), .by = category)

# Embrace for function arguments
my_func <- function(data, var) {
  data |> summarise(mean = mean({{ var }}))
}

# Type-stable iteration
map_dbl(data, mean)  # Not sapply()
```

### Key Anti-Patterns to Avoid

``` r
# Avoid legacy magrittr pipe
data %>% filter(x > 0)  # Use |> instead

# Avoid old join syntax
by = c("a" = "b")  # Use join_by(a == b)

# Avoid group_by/ungroup
group_by(x) |> summarise(y) |> ungroup()  # Use .by instead

# Avoid sapply (type-unstable)
sapply(x, f)  # Use map_*() instead
```

## Directory Structure

``` text
claude-code-r-skills/
├── README.md
├── LICENSE
├── .gitignore
├── .claude-plugin/
│   ├── plugin.json                  # Plugin manifest
│   └── marketplace.json             # Marketplace catalog
├── .claude/
│   ├── CLAUDE.md                    # Project instructions
│   ├── settings.json                # Project-level hooks (for repo dev)
│   ├── settings.local.json          # Local permissions (gitignored)
│   ├── hooks/
│   │   └── scripts/
│   │       ├── utils.js             # Shared utilities
│   │       ├── suggest-compact.js   # Strategic compaction
│   │       ├── pre-compact.js       # Save state before compact
│   │       ├── session-start.js     # Load previous context
│   │       ├── session-end.js       # Persist session state
│   │       ├── doc-blocker.js       # Warn about random .md file creation
│   │       └── git-push-warn.js     # Warn before git push
│   └── skills/
│       ├── tidyverse-patterns/
│       ├── rlang-patterns/
│       ├── r-performance/
│       ├── r-style-guide/
│       ├── r-oop/
│       ├── r-package-development/
│       ├── r-bayes/
│       └── tdd-workflow/
├── hooks/
│   └── hooks.json                   # Plugin hooks (bundled with plugin)
├── contexts/
│   ├── dev.md                       # Coding mode (write first, TDD)
│   ├── research.md                  # Exploration mode (read before acting)
│   └── review.md                    # Audit mode (find issues, verdict)
├── rules/
│   ├── security.md
│   ├── testing.md
│   └── git-workflow.md
├── commands/
│   ├── plan.md
│   ├── tdd.md
│   ├── code-review.md
│   └── verify.md                    # Full quality gate before committing
└── agents/
    ├── planner.md                   # Uses Opus model
    ├── tdd-guide.md                 # TDD enforcement specialist
    └── code-reviewer.md
```

Note: `r-machine-learning` skill is local-only and not included in the public repository. Updated 2026-02-20 based on the WARND competition final model (4-model ridge stacked ensemble: XGBoost, Elastic Net, CatBoost, ExtraTrees; OOF AUC 0.8187). Key additions: Elastic Net and ExtraTrees patterns, stratified participant-level CV, expanded temporal feature engineering, ridge meta-learner stacking, and model selection guidance including documented TabNet failure.

## Core Principles

1.  **Use modern tidyverse patterns** - dplyr 1.1+, native pipe, current APIs
2.  **Profile before optimising** - Use profvis and bench
3.  **Write readable code first** - Optimize only when necessary
4.  **Follow tidyverse style guide** - Consistent naming and structure
5.  **Test-driven development** - Write tests before implementation
6.  **80% minimum coverage** - Comprehensive testing required

## Recommended Workflow

For any non-trivial feature or fix, follow this sequence:

``` text
claude-research    # Start in exploration mode
/plan              # Design the approach (uses Opus)
claude-dev         # Restart in implementation mode
/tdd               # Write tests first (RED)
                   # Implement (GREEN → REFACTOR)
/verify            # Full quality gate before committing
claude-review      # Restart in audit mode if needed
```

## Requirements

-   R 4.3+ (for native pipe `|>`)
-   dplyr 1.1+ (for `.by`, `join_by()`, `reframe()`)
-   purrr 1.0+ (for `list_rbind()`)
-   tidyr 1.3+ (for `separate_wider_*()`)
-   testthat 3.0+ (for snapshot testing)

## Environment Management

-   **R packages**: Use `pak` for installation
-   **R environments**: Use `renv` for project isolation
-   **Python**: Use `uv` for Python environments (if needed)

## Token Optimization

Claude Code usage can be expensive if you don't manage token consumption. These settings significantly reduce costs without sacrificing quality. Adapted from [Affaan Mustafa's Everything Claude Code](https://github.com/affaan-m/everything-claude-code).

### Recommended Settings

Add to `~/.claude/settings.json`:

```json
{
  "model": "sonnet",
  "env": {
    "MAX_THINKING_TOKENS": "10000",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"
  }
}
```

| Setting | Default | Recommended | Impact |
|---------|---------|-------------|--------|
| `model` | opus | **sonnet** | ~60% cost reduction; handles 80%+ of coding tasks |
| `MAX_THINKING_TOKENS` | 31,999 | **10,000** | ~70% reduction in hidden thinking cost per request |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 95 | **50** | Compacts earlier — better quality in long sessions |

Switch to Opus only when you need deep architectural reasoning:
```
/model opus
```

### Daily Workflow Commands

| Command | When to Use |
|---------|-------------|
| `/model sonnet` | Default for most tasks |
| `/model opus` | Complex architecture, debugging, deep reasoning |
| `/clear` | Between unrelated tasks (free, instant reset) |
| `/compact` | At logical task breakpoints (research done, milestone complete) |
| `/cost` | Monitor token spending during session |

### Strategic Compaction

The `suggest-compact` hook (included in this plugin) suggests `/compact` at logical breakpoints instead of relying on auto-compaction at 95% context.

**When to compact:**
- After research/exploration, before implementation
- After completing a milestone, before starting the next
- After debugging, before continuing feature work
- After a failed approach, before trying a new one

**When NOT to compact:**
- Mid-implementation (you'll lose variable names, file paths, partial state)

## License

MIT License - see [LICENSE](LICENSE) for details.
