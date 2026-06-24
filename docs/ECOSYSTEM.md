<!-- Source of truth for the project list: ecosystem/ecosystem.json. Keep the two in sync; scripts/check-ecosystem.py enforces it. -->

# AERS in the Agentic-Research Ecosystem

A maintained, cited map of where **Auto-Empirical-Research-Skills (AERS)** sits among the
fast-growing set of open-source projects that automate parts of the research process —
and an honest account of what AERS *is* and *is not*.

Star counts are point-in-time snapshots (see `updated` in
[`ecosystem/ecosystem.json`](../ecosystem/ecosystem.json)) and drift quickly; treat them as
orders of magnitude, not live numbers. For concrete "use X together with AERS" pipelines,
see [INTEROP.md](INTEROP.md). For how AERS compares to other **skill libraries and
marketplaces** (a different axis), see [COMPETITIVE_LANDSCAPE.md](COMPETITIVE_LANDSCAPE.md).

## TL;DR — the niche

The ecosystem has converged on a few shapes. The **auto-paper** loop (Sakana's *The AI
Scientist*) is impressive but optimized for machine-learning research, where a result is
"correct" if the code runs. The **skills-library** shape (K-Dense's *Scientific Agent
Skills*, 29k★) is proven — but aimed at biology, chemistry, and medicine. The
**deep-research** shape (*GPT Researcher*, *Open Deep Research*) automates literature
review. None of them owns **empirical social science**, where the hard part is *credible
identification* (Was this really causal? Is the instrument weak? Are the standard errors
clustered correctly?) across **R / Python / Stata / Julia**.

That gap is AERS's niche: a large, open **Agent Skills** library specialized for
**reproducible, rigorous empirical research in the social sciences**, with the human kept
in the loop and method correctness checked by evals rather than assumed.

## The landscape, by shape

### 1. Closed-loop "auto-paper" systems
- **[The AI Scientist](https://github.com/SakanaAI/AI-Scientist)** (SakanaAI, ~14k★) —
  idea → experiments → LaTeX paper → AI review, end to end. Best on code-expressible ML
  problems; needs GPUs; quality varies; ships under a Responsible-AI-derived license with a
  mandatory AI-disclosure clause.

> **AERS contrast.** AERS does not chase full autonomy. In applied micro/macro the
> bottleneck is not "can the code run" but "is the design defensible" — so AERS keeps a
> human in the loop and invests in *checking* identification, not generating papers blindly.

### 2. Research orchestrators (human-in-the-loop)
- **[Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)** (~6k★, MIT) —
  lit review → experimentation → report, with a co-pilot mode.
- **[DeerFlow](https://github.com/bytedance/deer-flow)** (ByteDance) — long-horizon
  super-agent harness (sandboxes, memory, sub-agents, a "skills" slot); hit GitHub Trending
  #1 in Feb 2026.

> **AERS complement.** These are *hosts*. They lack domain-correct empirical methods; AERS
> skills drop into their skills/sub-agent slots to supply them.

### 3. Agent Skills libraries (AERS's own format)
- **[Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)**
  (K-Dense, ~29k★, MIT) — 147 skills + 100+ databases for life sciences; explicit
  compatibility matrix (Cursor, Claude Code, Codex, Antigravity, Pi, …) and a "tested
  examples" ethos.
- **AERS** (this repo) — 1,150 skills across ~69 collections and 8 social-science
  disciplines, R/Python/Stata/Julia, with a generated catalog, license/hygiene audits, an
  eval harness, and a reproducibility benchmark.

> **AERS positioning.** Same *format*, disjoint *domain*. K-Dense is the proof-of-thesis and
> the playbook to learn from (see "What we borrow" below); the two libraries are
> complementary, not competing.

### 4. Deep-research / literature engines
- **[GPT Researcher](https://github.com/assafelovic/gpt-researcher)** (~28k★, Apache-2.0) —
  aggregates 20+ sources into cited reports.
- **[Open Deep Research](https://github.com/langchain-ai/open_deep_research)** (LangChain,
  ~12k★, MIT) — configurable, multi-provider, **full MCP support**.

> **AERS complement.** These are the best *front-end* for the literature and data stages.
> Open Deep Research's MCP support means AERS data-source MCP servers (FRED, OpenAlex,
> EDGAR) plug straight in; AERS citation-hygiene and de-AIGC skills clean the back-end.

### 5. Domain execution & data-science agents
- **[Econometrics AI Agent](https://github.com/FromCSUZhou/Econometrics-Agent)** (~355★,
  Apache-2.0) — specialized agent for IV-2SLS, DiD, RDD, and propensity-score methods;
  paper *"Can AI Master Econometrics?"* (arXiv:2506.00856). **The closest technical sibling.**
- **[DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze)** (RUC) and
  **[DataMind](https://github.com/zjunlp/DataMind)** (ZJU, ICLR/AAAI 2026) — autonomous /
  open-source data-analysis agents.

> **AERS relation.** Econometrics-Agent is the strongest **interop target** as an execution
> back-end; AERS brings breadth and a battery of methodological-pitfall evals it could be
> scored against. DeepAnalyze/DataMind are adjacent (generic data analysis, light on causal
> identification) and useful as local, no-paid-API back-ends.

## At a glance

| Project | ★ (≈) | License | Shape | Domain | Relation to AERS |
|---|---|---|---|---|---|
| Scientific Agent Skills (K-Dense) | 29k | MIT | skills library | life sciences | format-peer |
| GPT Researcher | 28k | Apache-2.0 | deep research | general | complement |
| The AI Scientist (Sakana) | 14k | RAIL-derivative | auto-paper loop | ML | contrast |
| Open Deep Research (LangChain) | 12k | MIT | deep research | general (MCP) | complement |
| Agent Laboratory | 6k | MIT | orchestrator | general | complement |
| Econometrics AI Agent | 0.4k | Apache-2.0 | execution agent | econometrics | sibling |
| DeerFlow (ByteDance) | — | — | orchestrator | long-horizon | complement |
| DeepAnalyze / DataMind | — | — | data-science agent | data analysis | sibling |

## What AERS is — and is not

**AERS is:**
- An **open Agent Skills library** for the **empirical social sciences** (economics,
  finance, accounting, political science, sociology, and adjacent fields).
- **Multi-language** by design — R, Python, Stata, and Julia, with Stata first-class (a
  deliberate gap in most science-skill libraries).
- **Rigor-first**: the value is in correct identification, honest robustness, real
  citations, and runnable replication — checked by the eval harness and benchmark, not
  assumed.
- **Composable**: built to plug into the orchestrators, deep-research front-ends, and
  execution back-ends above rather than replace them.

**AERS is not:**
- A push-button "write my paper" system. Full autonomy is explicitly out of scope where it
  would hide identification risk.
- A life-sciences or general-science library (that is K-Dense's turf).
- A model, an execution runtime, or a closed product — it is a curated, audited, vendored
  collection of skills plus the tooling to keep it trustworthy.

## What we borrow from the ecosystem

The point of this map is to act on it. Concretely, AERS adopts the proven moves of the
leaders while staying in its lane:

- **From K-Dense** — a visible *compatibility matrix*, a *tested-examples* discipline, and a
  *unified data-access* story. AERS already has executable evals and a benchmark; the
  ongoing work is to make verification and compatibility as legible as K-Dense makes them.
- **From GPT Researcher / Open Deep Research** — *citation honesty as a first-class
  feature*. AERS encodes this as dedicated citation-hygiene and de-AIGC skills and an eval
  that fails fabricated references.
- **From Sakana / Agent Laboratory** — the *full-lifecycle* framing (ideation → submission),
  but rebuilt around human-in-the-loop checkpoints suited to social science.
- **From Econometrics-Agent** — treat it as a *peer to interoperate and benchmark against*,
  not a competitor.

## How AERS composes with these projects

AERS is designed to be one stage in a larger pipeline. The machine-readable role map lives
in [`ecosystem/ecosystem.json`](../ecosystem/ecosystem.json) (`interop_roles`), and concrete,
reproducible recipes — e.g. *Open Deep Research for the lit review → AERS identification
skills → Econometrics-Agent/StatsPAI for execution → AERS de-AIGC + citation checks for the
write-up* — are in **[INTEROP.md](INTEROP.md)**.

## Maintenance

- The project list is mirrored in [`ecosystem/ecosystem.json`](../ecosystem/ecosystem.json);
  `scripts/check-ecosystem.py` (run by `make validate`) keeps this doc and the JSON in sync
  and verifies that every referenced AERS collection exists.
- Update `star_snapshot` and `updated` opportunistically; the validator never asserts star
  counts, only structure and cross-references.
- Add a project by editing `ecosystem/ecosystem.json` first, then mentioning it here.

## Sources

- [The AI Scientist](https://github.com/SakanaAI/AI-Scientist) ·
  [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) ·
  [Scientific Agent Skills (K-Dense)](https://github.com/K-Dense-AI/scientific-agent-skills)
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher) ·
  [Open Deep Research](https://github.com/langchain-ai/open_deep_research) ·
  [DeerFlow](https://github.com/bytedance/deer-flow)
- [Econometrics AI Agent](https://github.com/FromCSUZhou/Econometrics-Agent) (arXiv:2506.00856) ·
  [DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze) ·
  [DataMind](https://github.com/zjunlp/DataMind)
