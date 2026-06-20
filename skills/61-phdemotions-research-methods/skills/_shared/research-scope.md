# Research Project Scope Discovery

> How to determine what to audit or review in a research project.
> Used by /research-intake, /research-review, /research-audit, and session-end reviews.

## Full project scope (for /research-intake, /research-audit --full)

Inventory everything in the project. Walk these directories in order:

### 1. Data inventory
```
data/raw/          → What raw data files exist? Formats? Sizes?
data/processed/    → Is there cleaned data? What stage?
data/codebook/     → Is there a codebook? How complete?
```

### 2. Documentation inventory
```
docs/pre-registration.md    → Does a pre-registration exist?
docs/decisions/             → Is there a decision log? How many entries?
docs/irb/                   → Is there ethics documentation?
README.md                   → Does it follow Cornell template?
CITATION.cff                → Is it present?
```

### 3. Code inventory
```
R/                 → R analysis scripts. How many? What stages covered?
python/            → Python analysis scripts. Same questions.
_targets.R         → Is there an R pipeline?
Snakefile          → Is there a Python pipeline?
renv.lock          → Is the R environment locked?
uv.lock            → Is the Python environment locked?
tests/             → Are there tests?
```

### 4. Output inventory
```
output/figures/    → Are there figures? What format/resolution?
output/tables/     → Are there tables? What format?
output/results/    → Are there intermediate results?
reports/           → Are there Quarto documents? Manuscript draft?
```

### 5. External materials (ask the researcher)
- Survey instruments, interview protocols
- IRB approval letters
- Pre-registration links (AsPredicted, OSF)
- Data use agreements
- Prior analysis scripts (SPSS .sps, Stata .do, etc.)

## Session scope (for session-end reviews)

Same approach as the Opus Vita session-scope pattern:

1. **Conversation transcript** — inspect for Edit/Write/NotebookEdit tool calls. Most reliable.
2. **Git diff** — `git diff --name-only HEAD` for uncommitted changes.
3. **Recently modified files** — last resort, use Glob with mtime sort.

### What to do with session scope

1. **Print the scope** at the top of the review.
2. **Compare to previous intake** — which gaps were closed this session?
3. **Note new gaps** — did any changes introduce new issues?
4. **Check for suite-learning opportunities** — did the researcher use anything our skills don't cover?

## When scope is empty

For full project scope: this shouldn't happen — if `/research-intake` is running, there must be *something* to review. If truly empty (no data, no code, no docs), help the researcher start from scratch with `/research-init`.

For session scope: exit early with one line:
> *No changes this session — session review skipped.*
