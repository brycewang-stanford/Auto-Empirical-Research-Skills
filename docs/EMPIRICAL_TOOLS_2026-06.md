# Empirical-Tools Catalog — 2026-06

This pass added a new first-party module, [`tools/`](../tools/), cataloging **335
software tools** for automated empirical research and causal inference — a layer
distinct from the agent **skills** under [`skills/`](../skills/). A *skill* is an
instruction pack an agent reads; a *tool* is the external software or service an
agent (or researcher) actually invokes. The two were deliberately separated so the
new index does not dilute the semantics of the skills catalog.

> **Updated 2026-06-04:** grew from the initial 200 tools to **335** over three
> waves — (1) the original five categories, (2) the **51-entry `research-agent`
> category** (autonomous research & data-science agents), and (3) an **84-entry
> niche-econometrics expansion** (spatial econometrics, local projections/IRF &
> (S)VAR, survey weighting/MRP/raking, meta-analysis) growing `econometrics-library`
> from 86 to 170. The "deferred" notes that originally appeared below are superseded.

Source of truth: [`tools/tools.json`](../tools/tools.json). Browsable view:
[`tools/CATALOG.md`](../tools/CATALOG.md) (generated). Both are validated and kept
fresh by [`scripts/build-tools-catalog.py`](../scripts/build-tools-catalog.py),
wired into `make catalog` (build) and `make validate` (`--check`).

## Scope (this pass)

Three categories were requested, plus two adjacent support categories:

| Category | Count | What it covers |
|---|---:|---|
| `causal-inference-library` | 32 | Treatment-effect / causal-ML estimation: DoWhy, EconML, CausalML, DoubleML (py+R), CausalPy, causallib, grf, CATENets, TMLE family, Mendelian randomization, uplift modeling |
| `econometrics-library` | 170 | Panel FE, DiD (incl. modern/staggered), event study, RDD, IV, synthetic control/SDID, matching & weighting, sensitivity — **plus** spatial econometrics (spdep, PySAL/spreg, GeoDa, Stata `sp`), local projections/IRF & (S)VAR (lpirfs, vars, svars), survey weighting/MRP/raking (survey, samplics, balance, anesrake), and meta-analysis (metafor, meta, netmeta, metan) — across R / Python / Stata / Julia |
| `mcp-server` | 48 | Stats-execution MCPs (StatsPAI, Stata, R, Jupyter) + data-access MCPs (FRED, World Bank, IMF, OECD, Eurostat, Census, BEA, BLS, SEC EDGAR, OpenAlex, Semantic Scholar, PubMed, Zotero, arXiv) |
| `causal-discovery` | 25 | Structure learning: causal-learn, Tetrad/py-tetrad, gCastle, CDT, tigramite (PCMCI), LiNGAM, NOTEARS/DAGMA, pcalg, bnlearn, pgmpy |
| `research-agent` | 51 | Autonomous research & data-science agents: AI-Scientist, data-to-paper, Agent Laboratory, RD-Agent, AI-Researcher, STORM, PaperQA2, gpt-researcher, DeepAnalyze, MetaGPT (Data Interpreter), Biomni, AIDE, AutoGluon-Assistant |
| `benchmark-dataset` | 9 | Known-ground-truth datasets/simulators: causaldata, IHDP/Twins, ACIC competition data, RealCause, JustCause, Tübingen pairs, bnlearn network repository |

Coverage signals (snapshot, June 2026): **165 Python · 109 R · 53 Stata · 16 TypeScript
· 11 Julia**; **181 active · 95 maintained · 59 dormant**; **184 permissive · 104 copyleft
· 39 unverified/unmapped · 8 proprietary/non-OSI/custom** licenses. Every record is
`verified: true` (its repo was fetched during curation to confirm license and activity).

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

**Third wave (2026-06-04) — niche-econometrics expansion (`econometrics-library` 86 → 170):**
84 packages from two verified sweeps closing the gaps flagged in the original backlog:
**spatial econometrics** (R: spdep, spatialreg, sphet, splm, spsur, spmoran, spaMM, rgeoda;
Python PySAL: libpysal, spreg, esda, mgwr, giddy; Stata `sp`/`sppack`/`xsmle`; GeoDa; Julia
SpatialDependence.jl), **local projections / IRF & (S)VAR** (R: lpirfs, vars, svars, BVAR,
ARDL; Python: localprojections, statsmodels VAR; Stata `lpirf`/`var`/`svar`, `locproj`; Julia
LocalProjections.jl), **survey weighting / MRP / raking** (R: survey, srvyr, anesrake, autumn,
PracTools; Python: samplics, ipfn, balance; Stata: ipfraking, sreweight, `svy`; MRP engines
brms, rstanarm), and **meta-analysis** (R: metafor, meta, netmeta, metaSEM, robumeta, dmetar,
RoBMA; Python: PythonMeta, PyMARE; Stata: metan, admetan, ipdmetan, `meta`). Built-in Stata
commands are recorded `license: proprietary`, `automation_level: built-in-command`; SSC modules
`community-command` (GPL-3 per RePEc); CRAN-only packages use the canonical CRAN URL with
`owner_repo: cran/<pkg>`. `spaMM` is CeCILL-2.0. One overlap (`statsmodels`) was de-duplicated
against the existing entry.

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
- ~~Spatial econometrics, local projections / impulse responses, MRP / survey weighting,
  meta-analysis tooling~~ — **done 2026-06-04** (84 entries; see "Third wave" above).
- ~~Periodic link/license re-check workflow for the catalog~~ — **done 2026-06-04**
  ([`scripts/check-tools-links.py`](../scripts/check-tools-links.py) +
  [`.github/workflows/check-tools-links.yml`](../.github/workflows/check-tools-links.yml),
  scheduled monthly). Re-verifying `stars_approx` / `last_activity` still needs a manual
  GitHub-API pass.
- **Remaining:** ARDL depth (`dLagM`, `ardl.nardl`), a dedicated Julia spatial-regression
  package (none mature as of 2026-06), and broadening `research-agent` as that space evolves.
