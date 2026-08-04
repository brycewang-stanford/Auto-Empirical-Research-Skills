<!-- Recipes reference real collections under skills/. scripts/check-ecosystem.py verifies every skills/NN-... path mentioned here exists. -->

# Interoperability Recipes

AERS is built to be **one stage in a larger pipeline**, not a walled garden. This page gives
concrete, reproducible ways to combine AERS skills with the complementary open-source
projects mapped in [ECOSYSTEM.md](ECOSYSTEM.md). The machine-readable role map is
[`ecosystem/ecosystem.json`](../ecosystem/ecosystem.json) → `interop_roles`.

Design rules these recipes follow:
- **No paid API is required** to reproduce the AERS portion — every AERS step runs on local
  skills.
- **The human stays in the loop** at identification and robustness checkpoints.
- **Citations and replication are verified**, not assumed.

## The pipeline model

A typical empirical paper maps onto these stages. Each stage names the external project that
fits best and the AERS collection(s) that supply the domain-correct behavior.

| Stage | External fit | AERS collection(s) |
|---|---|---|
| Literature review | Open Deep Research, GPT Researcher | [36-literature-review](../skills/36-taoyunudt-literature-review-skill), [52-slr-prisma](../skills/52-keemanxp-slr-prisma), [59-openalex](../skills/59-shiquda-openalex-skill), [60-superpapers](../skills/60-regisely-superpapers) |
| Data access | Open Deep Research (MCP) | [57-edgartools](../skills/57-dgunning-edgartools), [58-econstack](../skills/58-charlescoverdale-econstack), [59-openalex](../skills/59-shiquda-openalex-skill) |
| Identification & methods | Econometrics-Agent | [10-causal-inference-mixtape](../skills/10-Jill0099-causal-inference-mixtape), [13-MixtapeTools](../skills/13-scunning1975-MixtapeTools), [50-aer-skills](../skills/50-brycewang-aer-skills), [51-CausalPy](../skills/51-pymc-labs-CausalPy) |
| Execution (R/Py/Stata) | Econometrics-Agent, DeepAnalyze, DataMind | [00-StatsPAI](../skills/00-Full-empirical-analysis-skill_StatsPAI), [00.2-Stata](../skills/00.2-Full-empirical-analysis-skill_Stata), [39-marginaleffects](../skills/39-vincentarelbundock-marginaleffects), [40-pyfixest](../skills/40-py-econometrics-pyfixest), [64-mcp-stata](../skills/64-tmonk-mcp-stata) |
| Writing & submission | Agent Laboratory | [01-academic-paper](../skills/01-lishix520-academic-paper-skills), [04-scientific-writer](../skills/04-K-Dense-AI-claude-scientific-writer), [06-stats-paper-writing](../skills/06-fuhaoda-stats-paper-writing), [56-econ-writing](../skills/56-hanlulong-econ-writing-skill) |
| Integrity & de-AIGC | — | [62-citation-checker](../skills/62-PHY041-claude-skill-citation-checker), [44-humanizer](../skills/44-matsuikentaro1-humanizer_academic), [45-deslop](../skills/45-stephenturner-skill-deslop), [48-de-AIGC-skills](../skills/48-de-AIGC-skills) |
| Reproduction | — | [28-paper-replicate](../skills/28-maxwell2732-paper-replicate-agent-demo), [54-open-science](../skills/54-scdenney-open-science-skills) |

## Recipe A — A reproducible empirical paper, end to end

The flagship composition. Each arrow is a handoff; the human reviews at the ★ checkpoints.

```
[Open Deep Research]  ──►  AERS lit-review skills      gather + screen prior work, real citations
        │
        ▼
[AERS data-access skills + MCP] ──► pull data           EDGAR / OpenAlex / FRED via MCP
        │
        ▼ ★ checkpoint: is the research design credible?
[AERS identification skills] ──► pick + justify design  DiD / IV / RDD / SC, with assumptions stated
        │
        ▼
[StatsPAI or Econometrics-Agent] ──► run the analysis   reproducible R/Python/Stata
        │
        ▼ ★ checkpoint: robustness honest?
[AERS robustness + tables/figures skills] ──► stress-test  pre-trends, weak-IV, clustering, multiple testing
        │
        ▼
[AERS writing skills] ──► draft the manuscript
        │
        ▼
[AERS citation-checker + de-AIGC] ──► verify refs, clean prose
        │
        ▼
[AERS reproduction skills] ──► package a runnable replication archive
```

Why this beats any single tool: deep-research front-ends do not know that a first-stage
**F ≈ 8 is a weak instrument** or that **two-way fixed effects is biased under staggered
adoption** — AERS skills (and the matching evals in `eval-harness/scenarios/`, e.g.
`statspai-weak-iv`, `causal-inference-twfe-trap`) do.

## Recipe B — AERS skills inside an orchestrator

Orchestrators like **Agent Laboratory** and **DeerFlow** expose a skills / sub-agent slot
but ship no empirical-social-science methods. Load AERS skills into that slot:

1. Point the orchestrator's skill directory at the relevant AERS collections (e.g.
   [50-aer-skills](../skills/50-brycewang-aer-skills) and
   [00-StatsPAI](../skills/00-Full-empirical-analysis-skill_StatsPAI)).
2. Let the orchestrator drive long-horizon planning and sandboxed execution.
3. Keep AERS's human-in-the-loop checkpoints (identification, robustness) as required
   approval steps in the orchestrator's plan.

This gives you the orchestrator's autonomy *and* AERS's domain correctness.

## Recipe C — Benchmark an execution agent against AERS evals

The **Econometrics AI Agent** is a sibling, so treat it as a peer to measure, not a rival:

1. Take the AERS reproducibility tasks in [`benchmark/tasks/`](../benchmark) (Card-IV,
   staggered-DiD, RDD, LaLonde, bad-control recovery).
2. Run Econometrics-Agent on the same task prompts.
3. Score both with the AERS rubric checker (`benchmark/check_benchmark.py`) and the
   methodological scenarios in `eval-harness/scenarios/`.

This produces an apples-to-apples comparison on correctness, not vibes — and surfaces where
each project is strong.

### The candidate protocol, step by step

Any agent (Econometrics-Agent, a Claude Code session, a LangGraph pipeline, a
human with Stata) is graded the same way. The whole exchange is one JSON file;
nothing about the harness assumes which runtime produced it.

1. **Pick tasks.** Every task spec in [`benchmark/tasks/`](../benchmark/tasks/) is a
   self-contained TOML: the dataset path, the story to hand your agent as a
   prompt (the `description`), and the graded fields. The datasets are small
   CSVs committed in [`benchmark/data/`](../benchmark/data/).
2. **Run your agent on the data.** Give it the dataset and the task story —
   *not* the gold values. It must produce the numeric fields named in the
   task's `gold` entries (e.g. `bartik_beta`, `ols_beta`, `first_stage_coef`
   for `bartik-recovery`).
3. **Drop a results file.** Write
   `benchmark/candidates/<your-agent-name>/results.json`:

   ```json
   {
     "task": "bartik-recovery",
     "method": "one line describing what your pipeline did",
     "bartik_beta": 0.5,
     "ols_beta": 1.1568,
     "first_stage_coef": 1.0
   }
   ```

   One directory per run; one results.json per task (use one directory per
   task, or grade task by task with `--task`).
4. **Grade.** `python3 benchmark/check_benchmark.py --task <task-id>` grades
   every candidate directory that declares that task. The checker recomputes
   all data-derived golds from the CSV itself, so reported numbers that don't
   match the data fail the `honest-*` checks — an agent cannot pass by
   guessing plausible values.
5. **Report both columns.** Pair the numeric score with the prose-side eval
   (`eval-harness/run_evals.py --grade <dir>`) so the comparison covers both
   "got the right number" and "reasoned about the right pitfalls".

The reference implementations in
[`benchmark/reference_pipeline.py`](../benchmark/reference_pipeline.py) are the
floor, not the ceiling: they are deliberately simple stdlib pipelines that any
competent agent should match exactly on the deterministic tasks.

## Live scoreboard

The same harness that grades *your* agent grades the reference pipeline and a
constructed "naive baseline" (the folk move on each task) every time the
catalog regenerates:

- [`BENCHMARK_SCOREBOARD.md`](BENCHMARK_SCOREBOARD.md) — per-task
  required-gold counts for reference vs naive, with the naive move each
  task is designed to catch.

  Latest commit on `main`: reference 16/16 tasks pass every required gold;
  the naive baseline fails required golds on 16/16 tasks. That is the gap
  your agent is expected to stay inside (or close further).

## MCP wiring note



[Open Deep Research](https://github.com/langchain-ai/open_deep_research) has full MCP
support, and several AERS data sources are exposed as MCP servers (e.g. FRED, OpenAlex via
[59-openalex](../skills/59-shiquda-openalex-skill), SEC EDGAR via
[57-edgartools](../skills/57-dgunning-edgartools)). Register those MCP servers with the
deep-research front-end and the literature/data stages share one tool surface — no glue code,
and the same provenance flows through to the citation checker.

## See also

- [ECOSYSTEM.md](ECOSYSTEM.md) — who's who and how AERS is positioned.
- [`ecosystem/ecosystem.json`](../ecosystem/ecosystem.json) — machine-readable role map.
- [SKILL_CATALOG.md](SKILL_CATALOG.md) — the full skill index.
