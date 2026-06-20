# EdgarTools AI

**Two parallel pathways for AI agents to access SEC EDGAR filing data.**

## Overview

`edgar.ai` provides AI-optimized integration for SEC financial data analysis through two approaches:

1. **Skills + Code Execution** (Recommended) - Learn patterns, write Python code, execute directly
2. **MCP Server** (Alternative) - Structured tool calling for parameter validation

Both integrate directly with the EdgarTools API - choose based on your workflow needs.

## Installation

```bash
# Install AI features
pip install "edgartools[ai]"

# For development
pip install -e ".[ai,ai-dev]"
```

---

## Integration Path 1: Skills + Code Execution (Primary)

**Best for:** Complex workflows, learning EdgarTools patterns, maximum performance

### What Are Skills?

Skills are AI-consumable documentation packages that teach agents how to use EdgarTools:
- Progressive disclosure (4-tier documentation hierarchy)
- Direct Python code execution (zero protocol overhead)
- Full composability (variables, chaining, reusable objects)
- Context-Oriented Programming (COP) aligned

### Installation

**Export to Claude Desktop:**
```python
from edgar.ai.skills import edgartools_skill

# Install to ~/.claude/skills/edgartools/
edgartools_skill.export(format="claude-skills")

# Or create portable ZIP
edgartools_skill.export(format="claude-desktop", create_zip=True)
```

**Manual Installation:**
```bash
# Copy skill directory
cp -r edgar/ai/skills/core ~/.claude/skills/edgartools/

# Restart Claude Desktop - skill automatically discovered
```

### Usage Example

Once installed, agents can read documentation and write code:

```python
from edgar import Company

# Agent learns from SKILL.md and writes code
company = Company("AAPL")
income = company.income_statement(periods=3)
balance = company.balance_sheet(periods=3)

print(f"Revenue trend: {income}")
print(f"Assets: {balance}")
```

**See:** `edgar/ai/skills/core/` for complete skill documentation

---

## Integration Path 2: MCP Server (Specialized for Complex Workflows)

**Best for:** Batch processing, automated pipelines, workflow orchestration (10% of users)

### What is MCP?

Model Context Protocol server that exposes EdgarTools as structured tools for complex workflows:
- Batch processing across 100+ companies
- Automated filing monitoring pipelines
- Scheduled report generation
- Workflow orchestration (n8n, Zapier, Make)
- Production data pipelines
- Parameter validation via JSON schemas

### Running the Server

```bash
python -m edgar.ai
# Or: edgartools-mcp (after pip install)
```

### Configuration

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "edgartools": {
      "command": "python",
      "args": ["-m", "edgar.ai"],
      "env": {
        "EDGAR_IDENTITY": "Your Name your.email@example.com"
      }
    }
  }
}
```

**Cline/Continue.dev**:
```json
{
  "mcpServers": {
    "edgartools": {
      "command": "python",
      "args": ["-m", "edgar.ai"],
      "env": {
        "EDGAR_IDENTITY": "Your Name your.email@example.com"
      }
    }
  }
}
```

**Note:** `EDGAR_IDENTITY` is required by SEC for API requests.

### Available Tools

- **edgar_company**: Company profile, financials, filings, and ownership in one call
- **edgar_search**: Search companies, filings, or both
- **edgar_filing**: Read filing content or specific sections
- **edgar_compare**: Compare multiple companies or analyze an industry
- **edgar_ownership**: Insider transactions, institutional holders, fund portfolios

**See:** [MCP Quickstart Guide](mcp/docs/MCP_QUICKSTART.md) for details

### When to Use MCP vs Skills

| Use Case | Recommended Approach |
|----------|---------------------|
| **Interactive analysis** | Skills + Code (PRIMARY) |
| **Learning EdgarTools patterns** | Skills + Code (PRIMARY) |
| **Ad-hoc research** | Skills + Code (PRIMARY) |
| **Single-company deep dives** | Skills + Code (PRIMARY) |
| **Batch processing 100+ companies** | MCP Tools (SPECIALIZED) |
| **Automated pipelines** | MCP Tools (SPECIALIZED) |
| **Scheduled reports** | MCP Tools (SPECIALIZED) |
| **Workflow orchestration** | MCP Tools (SPECIALIZED) |

**Recommendation:** Start with Skills only. Add MCP only if you need workflow automation.

---

## Core AI Infrastructure (Shared)

Both integration paths use these shared components:

### 1. Semantic Enrichment

Add business context to financial data:

```python
from edgar.ai import SemanticEnricher

# Get concept definitions
definition = SemanticEnricher.get_concept_definition("Revenue")
# "Total income generated from normal business operations"

# Get related concepts
related = SemanticEnricher.get_related_concepts("Revenue")
# ["GrossProfit", "OperatingIncome", "NetIncome"]

# Interpret values
interpretation = SemanticEnricher.interpret_value(
    "Revenue", 125_000_000_000, "USD"
)
# "The company is a billion-dollar business based on revenue"
```

### 2. Token Optimization

Optimize content for LLM context windows:

```python
from edgar.ai import TokenOptimizer

# Estimate tokens (~4 chars per token)
tokens = TokenOptimizer.estimate_tokens(content)

# Optimize for token limit
optimized = TokenOptimizer.optimize_for_tokens(
    content, max_tokens=1000
)
```

### 3. Helper Functions

Convenience wrappers with clear parameter names:

```python
from edgar.ai.helpers import (
    get_filings_by_period,
    get_revenue_trend,
    compare_companies_revenue
)

# Get Q1 2023 10-K filings
filings = get_filings_by_period(2023, 1, form="10-K")

# Get revenue trend (3 fiscal years)
income = get_revenue_trend("AAPL", periods=3)

# Compare multiple companies
comparison = compare_companies_revenue(["AAPL", "MSFT", "GOOGL"], periods=3)
```

## Package Structure

```
edgar/ai/
├── skills/              # Skills (Primary Integration)
│   ├── base.py          # BaseSkill abstract class
│   └── core/            # EdgarTools skill
│       ├── SKILL.md                  # Main documentation
│       ├── quickstart-by-task.md     # Quick routing
│       ├── workflows.md              # End-to-end examples
│       ├── objects.md                # Object reference
│       ├── data-objects.md           # Form-specific objects
│       └── form-types-reference.md   # 311 SEC forms
│
├── mcp/                 # MCP Server (Alternative Integration)
│   ├── server.py        # MCP server implementation
│   ├── tools/           # Tool handlers (all call EdgarTools directly)
│   └── docs/            # MCP documentation
│
├── core.py              # Shared AI infrastructure
│                        # - TokenOptimizer, SemanticEnricher
│                        # - AIEnabled base class
├── helpers.py           # Convenience wrappers
│                        # - get_revenue_trend(), compare_companies_revenue()
├── exporters/           # Skill export formats
│   ├── claude_skills.py     # ~/.claude/skills/ format
│   └── claude_desktop.py    # Portable ZIP format
│
└── examples/            # Usage examples
    └── basic_usage.py
```

## Development

To contribute to the AI features:

1. Install development dependencies:
   ```bash
   pip install -e ".[ai,ai-dev]"
   ```

2. Run tests:
   ```bash
   # Test MCP tools
   pytest tests/test_mcp_tools.py

   # Test AI features
   pytest tests/test_ai_features.py

   # Test AI skills
   pytest tests/test_ai_skill_export.py
   ```

3. Check AI capabilities:
   ```python
   from edgar.ai import check_ai_capabilities
   print(check_ai_capabilities())
   ```

## Documentation

**For Architects & Decision-Makers:**
- [ARCHITECTURE.md](ARCHITECTURE.md) - High-level technical overview, parallel pathways explained
- [CONTEXT_ORIENTED_ANALYSIS.md](CONTEXT_ORIENTED_ANALYSIS.md) - COP principles analysis, why Skills-first

**For Developers:**
- [Skills Documentation](skills/core/) - Complete skill package (SKILL.md, workflows.md, etc.)
- [MCP Quickstart Guide](mcp/docs/MCP_QUICKSTART.md) - MCP server setup in 5 minutes
- [examples/basic_usage.py](examples/basic_usage.py) - Code examples for all features

**For AI Agents:**
- Install Skills to `~/.claude/skills/edgartools/` - agents learn patterns automatically

## Key Concepts

### Skills-First Architecture

edgar.ai follows Context-Oriented Programming (COP) principles:
- **Progressive Disclosure**: 4-tier documentation (30s → 5min → detailed → comprehensive)
- **Context as Resource**: Token budgets, optimization, estimates for all operations
- **Direct API Access**: Both Skills and MCP call EdgarTools directly (zero abstraction)
- **Understanding as Primitive**: Documentation teaches patterns, not just syntax

### Why Skills > MCP?

- **Zero Protocol Overhead**: Direct Python code execution vs JSON-RPC
- **Full Composability**: Variables, chaining, loops in single code block
- **Better Learning**: Agents understand patterns, not just tool schemas
- **Simpler Maintenance**: Documentation only vs server + handlers + schemas

MCP remains available for clients that prefer tool calling or need parameter validation.

## Future Enhancements

**Short-term:**
- Usage metrics (Skills vs MCP adoption)
- Code-first API (Python API alongside MCP tools)
- Resource-based state management (MCP resources for workflow continuity)

**Long-term:**
- Skill composition framework (combine multiple domain skills)
- Temporal locality (skill activation/deactivation based on relevance)
- Vector embeddings for semantic search
- Multi-agent collaboration patterns