# Empirical-Tools Catalog — 2026-06

This pass added a new first-party module, [`tools/`](../tools/), cataloging **251
software tools** for automated empirical research and causal inference — a layer
distinct from the agent **skills** under [`skills/`](../skills/). A *skill* is an
instruction pack an agent reads; a *tool* is the external software or service an
agent (or researcher) actually invokes. The two were deliberately separated so the
new index does not dilute the semantics of the skills catalog.

> **Updated 2026-06-04:** added the **51-entry `research-agent` category**
> (autonomous research & data-science agents) in a second wave — superseding the
> "deferred" note that originally appeared below.

Source of truth: [`tools/tools.json`](../tools/tools.json). Browsable view:
[`tools/CATALOG.md`](../tools/CATALOG.md) (generated). Both are validated and kept
fresh by [`scripts/build-tools-catalog.py`](../scripts/build-tools-catalog.py),
wired into `make catalog` (build) and `make validate` (`--check`).

## Scope (this pass)

Three categories were requested, plus two adjacent support categories:

| Category | Count | What it covers |
|---|---:|---|
| `causal-inference-library` | 32 | Treatment-effect / causal-ML estimation: DoWhy, EconML, CausalML, DoubleML (py+R), CausalPy, causallib, grf, CATENets, TMLE family, Mendelian randomization, uplift modeling |
| `econometrics-library` | 86 | Panel FE, DiD (incl. modern/staggered), event study, RDD, IV, synthetic control/SDID, matching & weighting, sensitivity — across R / Python / Stata / Julia |
| `mcp-server` | 48 | Stats-execution MCPs (StatsPAI, Stata, R, Jupyter) + data-access MCPs (FRED, World Bank, IMF, OECD, Eurostat, Census, BEA, BLS, SEC EDGAR, OpenAlex, Semantic Scholar, PubMed, Zotero, arXiv) |
| `causal-discovery` | 25 | Structure learning: causal-learn, Tetrad/py-tetrad, gCastle, CDT, tigramite (PCMCI), LiNGAM, NOTEARS/DAGMA, pcalg, bnlearn, pgmpy |
| `research-agent` | 51 | Autonomous research & data-science agents: AI-Scientist, data-to-paper, Agent Laboratory, RD-Agent, AI-Researcher, STORM, PaperQA2, gpt-researcher, DeepAnalyze, MetaGPT (Data Interpreter), Biomni, AIDE, AutoGluon-Assistant |
| `benchmark-dataset` | 9 | Known-ground-truth datasets/simulators: causaldata, IHDP/Twins, ACIC competition data, RealCause, JustCause, Tübingen pairs, bnlearn network repository |

Coverage signals (snapshot, June 2026): **147 Python · 65 R · 36 Stata · 16 TypeScript
· 7 Julia**; **142 active · 75 maintained · 34 dormant**; **161 permissive · 50 copyleft
· 37 unverified/unmapped · 3 non-OSI/custom** licenses. Every record is `verified: true`
(its repo was fetched during curation to confirm license and activity).

**Second wave (2026-06-04) — `research-agent`:** 51 end-to-end *autonomous research &
data-science agents*, split across two verified sweeps (AI-scientist / paper-writing
systems, and data-science / deep-research agents) then de-duplicated. **License caution:**
SakanaAI's **AI-Scientist** and **AI-Scientist-v2** now ship a custom *AI Scientist Source
Code License v1.0* (Responsible-AI behavioral-use, non-OSI); **Coscientist** is Apache-2.0
**+ Commons Clause** (no commercial use); and 7 agent repos ship no `LICENSE` file (recorded
`unverified`). These are catalogued (indexed, not redistributed) with the license recorded
verbatim. Pure general-purpose agents with only a data sub-module (OpenManus, AutoAgent,
JoyAgent) and closed/hosted systems (Google AI co-scientist, Intology Zochi, Autoscience
Carl, FutureHouse hosted platform) were excluded; their open components (PaperQA2, Aviary,
Robin) are included.

## Method

Four parallel research agents each swept one sub-domain (causal-ML libraries;
econometrics/quasi-experimental packages; data & stats-execution MCP servers; causal
discovery + benchmarks). Each agent was required to **fetch the upstream repo / CRAN /
SSC page** to confirm license, approximate stars, and last-activity month before
recording an entry — not to rely on memory. Results were merged, normalized, and
de-duplicated by [an assembly step](../scripts/build-tools-catalog.py) into the sorted
`tools.json`.

## Curation decisions

- **Cross-category de-duplication.** `WhyNot` and `JustCause` surfaced in both the
  causal-ML and benchmark sweeps; they are catalogued once, under `benchmark-dataset`.
- **Estimation vs. discovery boundary.** `causallib`, `DoWhy`, `grf` are effect-estimation
  libraries (kept in `causal-inference-library`), not structure-learning; the discovery
  agent's near-misses were dropped to the correct bucket. Methods like TARNet/DragonNet/
  CEVAE are represented via the maintained `CATENets` library rather than unmaintained
  paper code.
- **MCP redundancy.** Many servers wrap the same source (FRED, Yahoo Finance, Stata,
  OpenAlex, PubMed each have several). The catalog keeps the most authoritative/active
  one plus up to one or two meaningfully different alternatives, and drops low-signal
  (≤1★, stale) duplicates. Official servers (World Bank Data360, US Census, Data Commons,
  Alpha Vantage) are preferred where they exist.
- **License precision.** 30 entries carry `unverified` or `NOASSERTION`. These are (a)
  Stata SSC packages that ship no formal `LICENSE` file (8), and (b) MCP repos whose
  license GitHub could not map to an SPDX id or that declared none. They are included
  (real, installable, widely cited) but flagged so downstream users confirm terms.
- **Datasets without a clean repo.** The Tübingen cause-effect pairs (MPI WebDAV/Zenodo)
  and the bnlearn Bayesian Network Repository (hosted files) are recorded with
  `owner_repo: null` and a homepage URL.

## Security / supply-chain note

This pass adds **no executable third-party code** to the repository — `tools/` is a
metadata index (JSON + generated Markdown), not vendored source. The only new code is
first-party: [`scripts/build-tools-catalog.py`](../scripts/build-tools-catalog.py) (stdlib
only, no network) and [`tests/test_tools_catalog.py`](../tests/test_tools_catalog.py).
The listed tools themselves are external dependencies the user chooses to install;
inclusion is not an endorsement of their security. The existing
[`SECURITY-SCAN-REPORT.md`](../SECURITY-SCAN-REPORT.md) baseline (skills) is unaffected.

## Maintenance

- Edit `tools/tools.json`, then run `python3 scripts/build-tools-catalog.py` to
  regenerate `tools/CATALOG.md` and the README summary block.
- `make validate` runs `build-tools-catalog.py --check` (schema + generated-view
  freshness); `make test` runs `tests/test_tools_catalog.py`. Both gate CI.
- Snapshots (`stars_approx`, `last_activity`, `maintained`) will age; a periodic
  re-verification pass should refresh them and re-bucket any tool whose status changed.

## Backlog (not added yet)

- ~~Autonomous research agents as a sixth category~~ — **done 2026-06-04** (`research-agent`, 51 entries).
- **Spatial econometrics, local projections / impulse responses, MRP / survey weighting,
  meta-analysis** tooling — present as functions inside broader packages already listed,
  but a few dedicated libraries (e.g. `spdep`, `lpirfs`, `metafor`) could be added.
- **Periodic link/license re-check** for the catalog, analogous to the skills
  external-link workflow — especially important for the fast-moving `research-agent`
  entries (stars/activity/licenses change quickly).
