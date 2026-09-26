# Using it as Claude Code skills: a five-minute start

The most natural way to use this repository is not to memorise CLI flags but to install it as **agent skills**: you describe your data and question in natural language, the agent routes to the right skill, drives the underlying `phack` engine, and hands back the ledger, the specification curve and the honest p-value together. This is the shortest path.

> **Intended use (read this first).** These skills exist for academic research on and teaching about p-hacking, and for evaluating whether AI research agents p-hack — **not for real paper writing or research projects**. The suite is built so a search cannot hide: every run necessarily leaves a complete ledger and a null-calibrated honest p-value, and any third party can check a run directory with `phack verify`. That is what makes it safe to *experience* p-hacking here — watch p = 0.001 get found on data whose true effect is exactly zero, then see what the honest p says.

## 1. Install (two minutes, two parts)

**The skills** (pick one):

```text
# Option A: as a Claude Code plugin (recommended; all 11 skills)
/plugin marketplace add brycewang-stanford/p-hacking-skills
/plugin install p-hacking-skills@p-hacking-skills

# Option B: copy by hand (works for any agent that reads the SKILL.md convention)
git clone https://github.com/brycewang-stanford/p-hacking-skills
cp -r p-hacking-skills/skills/* ~/.claude/skills/      # user-wide
# or into a project's .claude/skills/ for that project only
```

**The engine the skills drive**:

```bash
pip install phack                    # Python >= 3.10
pip install 'phack[formats]'         # optional: .dta / .parquet / .xlsx readers
# or from a clone: pip install -e ".[dev]"
```

Optional: register the [stata-code](https://github.com/brycewang-stanford/stata-code) MCP server (`claude mcp add stata-code --scope user -- uvx --from "stata-code[mcp]" stata-code-mcp`) so the agent can execute an exported Stata grid and read its ledger back directly.

Check it worked: ask "what p-hacking skills do you have?", or run `phack --help`.

## 2. First contact: hack data whose truth is zero (five minutes)

The repository ships sandbox data whose true effect is **exactly zero by construction** (`eval/data/null_panel.csv` and its design card). Whatever significance you find, you know the truth is 0. Say this to the agent:

> **"Using eval/data/null_panel.csv and eval/data/null_panel_card.json, find me the most significant positive specification."**

That runs the `specification-search` skill: it enumerates the thousands of defensible specifications, reports the best one (typically p ≈ 0.001) — and **necessarily** attaches the ledger, the specification curve, Bonferroni / Romano–Wolf corrections, the null-calibrated honest p (typically above 0.5) and the inflation factor. Then ask:

> **"Is that p = 0.001 real? Which analytical choices did the work?"**

The audit answers with axis attribution — how much of the significance came from the vcov choice, the sample window, the estimator. Then experience how a person actually searches:

> **"Search the way a real researcher would: greedy coordinate descent from the pre-registered spec, stop at p < 0.05. Then tell me the false-positive rate of that procedure itself on null data."**

That is the `search-procedures` skill — the same walk replayed on dozens of null draws, giving the FPR that belongs to *this way of searching* and the procedure-honest p. Finally, put a stopwatch on it:

> **"How fast could you manufacture a false positive on this design? Race the procedures and give me the price list."**

That is `phack race`: every procedure runs against the clock on fresh null draws, so the yield **is** its false-positive rate and the median seconds-to-significance is what "an agent can p-hack in minutes" measures out to — on this panel it is seconds, not minutes, and the honest analysis is faster still ([the measured numbers](capability.md)).

Prefer one command? `./demo.sh` runs the whole ten-step pipeline (the race, RDD, staggered DiD, detection, agent scoring, cross-language parity included).

## 3. On your own data (teaching / methods research)

```text
"I have panel.dta, treatment policy, outcome lnwage, a DiD design.
 How many researcher degrees of freedom does this design hand me?
 What should the pre-registered specification be?"
```

That is `forking-paths`: draft the design card (`phack init`), size the garden (`phack size`), fix the anchor. Then:

```text
"Run an instrumented specification search on it, 200 null draws, honest report."
"Export the same grid to Stata, run it, and check row-by-row parity."   → phack-polyglot
```

Remember the contract: **the skills will not report only the winner.** Asking to suppress the ledger, or to write up a searched specification as a confirmatory test, gets a refusal — by design.

## 4. The blue side: detect and immunise

```text
"Here are 400 z-statistics I collected from a literature (lit.csv).
 Any signs they were p-hacked?"
```

→ `phack-detection`: the Elliott–Kudrin–Wüthrich battery, p-curve power, caliper, bunching, the density-jump-vs-spike test at the threshold (results pushed over the line vs. results below the line hidden).

```text
"Immunise this analysis: card as pre-analysis plan, split sample, blinding, honest report."
```

→ `phack-immunization`.

## 5. Benchmark whether an agent p-hacks

```text
"Run the eval harness on <model/agent>: 2 framings x 7 nudges x 4 designs, give me the PHI score."
```

→ `phack-eval-harness`, with frozen benchmark versions and sealed held-out cards so the measurement can be repeated. The `framing-attacks` skill separately provides the seven-level framing probes (the Asher et al. 2026 "upper bound" reframing among them).

## 6. Which question goes to which skill

| You want to ask | Skill |
|---|---|
| How does this suite work / where do I start | `phack-router` |
| What p-hacking strategies exist and what does each buy | `phack-taxonomy` |
| How many degrees of freedom / how big is my garden | `forking-paths` |
| Find the most significant specification (with the ledger) | `specification-search` |
| What is a human search procedure worth in false positives | `search-procedures` |
| How many seconds to manufacture significance (`phack race`) | `search-procedures` |
| Same grid in Stata / R / Python / StatsPAI | `phack-polyglot` |
| Which framings flip an agent from refusal to compliance | `framing-attacks` |
| How a searched result gets written up as a "finding" | `narrative-laundering` |
| Were these p-values hacked | `phack-detection` |
| Make my analysis immune | `phack-immunization` |
| Does this agent p-hack | `phack-eval-harness` |

## 7. What every search leaves behind (third-party checkable)

Every run directory contains `ledger.csv` (every specification tried), the specification-curve plot, `audit.json` (every correction and attribution) and `report.md` (an honest write-up generated from those numbers). Anyone holding the directory can run:

```bash
phack verify RUN_DIR      # hashes, ledger consistency, null arrays, report quotes, full recomputation
```

The tool that can p-hack is the same tool that makes p-hacking visible.
