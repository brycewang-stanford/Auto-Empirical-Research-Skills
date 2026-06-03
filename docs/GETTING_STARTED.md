# Getting Started — your first 10 minutes

AERS is two things at once: a **curated catalog** of 23,000+ agent skills for
empirical research, and a small set of **first-party flagship skills** that run the
full pipeline (data → identification → estimation → robustness → tables/figures →
submission-ready draft). This page is the on-ramp. By the end you will have
**proven the repo's claims on your own machine** and run your first skill.

It complements, and does not repeat, three pages you'll use constantly:

- [`INSTALL.md`](INSTALL.md) — the *mechanics* of loading skills into a runtime
- [`CHOOSING_A_SKILL.md`](CHOOSING_A_SKILL.md) — *which* skill for your goal
- [`GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md) — ready-to-paste prompts for common jobs

---

## Step 0 — Prove it works without an agent or API key (2 minutes)

Before you trust anything, run the executable evidence. None of this needs a paid
API or third-party packages — just Python 3.

```bash
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
cd Auto-Empirical-Research-Skills
make check
```

`make check` runs the whole local gate: repository validation, the unit tests, the
[`eval-harness/`](../eval-harness/) lint, and the numeric [`benchmark/`](../benchmark/).
The benchmark is the convincing part — it recovers known causal answers from real
data and **recomputes the gold values from the dataset every run**, so a passing
score can't be faked. You should see it recover the LaLonde training effect (a naive
comparison gets the sign *wrong*; covariate adjustment flips it positive) and the
Card return-to-schooling result (IV *exceeds* OLS, with the first-stage F reported).

If that passes, you've verified — not taken on faith — that the flagship pipeline
behaves correctly on problems with a known answer. For the full picture of what each
layer does and does **not** prove, read the trust overview in `docs/TRUST.md` and
[`QUALITY_GATE.md`](QUALITY_GATE.md).

---

## Step 1 — Pick how you'll use the skills

| Your situation | Path |
|---|---|
| I use **Claude Code / an agent runtime with plugins** | Install a skill bundle — see [`INSTALL.md`](INSTALL.md) |
| I just want the **methodology**, copy/paste into my own agent | Open the skill's `SKILL.md` and paste it as context |
| I want a **hosted, end-to-end** experience | Try [copaper.ai](https://copaper.ai) (the Stanford-incubated assistant this catalog was built alongside) |

Don't install everything. AERS is a *landscape*; you want one or two skills for the
job in front of you. Use [`CHOOSING_A_SKILL.md`](CHOOSING_A_SKILL.md) or the faceted
[`search.html`](search.html) to find them.

---

## Step 2 — Load your first skill

The fastest first win is the full-pipeline flagship in your language of choice:

- Python: [`StatsPAI`](../skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md) or [`00.1 Python`](../skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md)
- Stata: [`00.2 Stata`](../skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md)
- R: [`00.3 R`](../skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)

Follow the install mechanics in [`INSTALL.md`](INSTALL.md). If your runtime doesn't
support bundles, just open the `SKILL.md` and paste its contents into your agent's
context — these skills are *prompt-context*, not executable plugins.

---

## Step 3 — Run a real task

Open the agent with the skill loaded and give it a real job. A good first prompt
(from [`GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md)):

```text
Run a full DID empirical pipeline on this project. Start with the data contract
and sample-construction log, then produce Table 1, parallel-trends/event-study
evidence, main DID estimates, modern staggered-DID alternatives if treatment
timing varies, placebo checks, heterogeneity, and publication-ready tables and
figures. Keep every identifying assumption explicit and save a replication-ready
output folder.
```

What "good" looks like: the agent **states its identifying assumptions**, refuses to
headline a naive two-way-fixed-effects estimate when treatment timing is staggered,
reports instrument strength when it uses IV, and never invents a citation. Those are
exactly the behaviors the [`eval-harness/`](../eval-harness/) scenarios pin down.

---

## Step 4 — Read the result like a referee

Use the matching first-party skill to pressure-test the output before you rely on it:

| Concern | Skill |
|---|---|
| Is the **identification** valid? | [`aer-identification`](../skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md) |
| Are the **robustness** checks the ones referees expect? | [`aer-robustness`](../skills/50-brycewang-aer-skills/skills/aer-robustness/SKILL.md) |
| Is it **reproducible** enough for a data editor? | [`aer-replication`](../skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md) |
| Does the **prose** read AI-generated? | [`avoid-ai-writing`](../skills/47-conorbronsdon-avoid-ai-writing/SKILL.md) · [`chinese-de-aigc`](../skills/48-copaper-ai-chinese-de-aigc/SKILL.md) |

---

## Where to go next

- **Find the right skill:** [`CHOOSING_A_SKILL.md`](CHOOSING_A_SKILL.md) · [`TAXONOMY.md`](TAXONOMY.md) · [`search.html`](search.html)
- **Copy a full workflow:** [`GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md)
- **Understand the guarantees:** `docs/TRUST.md` · [`QUALITY_GATE.md`](QUALITY_GATE.md)
- **Check what each skill is worth:** [`SKILL_QUALITY.md`](SKILL_QUALITY.md) (hygiene) + [`eval-harness/`](../eval-harness/) (behavior) + [`benchmark/`](../benchmark/) (numbers)
- **Contribute a skill:** [`SKILL_SUBMISSION_GUIDE.md`](SKILL_SUBMISSION_GUIDE.md) · [`../CONTRIBUTING.md`](../CONTRIBUTING.md)

> Workflow-stage notes (中文): from [`01-选题与研究设计`](01-选题与研究设计.md) through
> [`10-审稿回复与学术答辩`](10-审稿回复与学术答辩.md) walk the whole research lifecycle.
