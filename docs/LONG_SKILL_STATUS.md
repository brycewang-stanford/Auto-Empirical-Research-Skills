<!-- Generated companion to LONG_SKILL_SPLIT_PLAN.md. Source of truth is the
catalog generator; this file is hand-curated. Run `make catalog` and
re-run `python3 scripts/build-skill-status.py` (if installed) or copy the
output of the snippet in §1 to refresh. -->

# Long-Skill Status

This is the **operational status** companion to
[`LONG_SKILL_SPLIT_PLAN.md`](LONG_SKILL_SPLIT_PLAN.md) (the *plan*). The plan
said *split upstream, not in this repo*. This file tracks whether each
problem file has been *split*, *blocked on upstream*, or *intentionally
left as-is* (manual vendor snapshot). It also lists the lowest-hygiene
non-vendored skills so reviewers can see who is actually waiting for
attention.

The two-column [`SKILL_HYGIENE.md`](SKILL_HYGIENE.md) scorecard classifies each
skill on the structural column (form) and the eval column (depth). This
file adds the **operational** column (what is being done about it).

---

## 0. Decision log

**2026-07-08 — Confirmed: no mass in-repo split.** An audit re-examined all 91
`SKILL.md` files over 500 lines against provenance:

- **24** already ship a `references/` directory (progressive disclosure) and are
  therefore **not** penalized by the hygiene score — including the three
  repo-owned flagships `00.1`/`00.2`/`00.3` (Python/Stata/R), whose 2,000+-line
  spines already offload deep detail to `references/NN-*.md` (23 pointers in the
  Python spine alone). Splitting them further would move text without raising the
  score and risks breaking a tuned pipeline.
- **67** lack `references/` but are **manual vendor snapshots** — faithful
  third-party mirrors. Rewriting them under our authorship would break the
  provenance chain (§3, 🟠 rows). The correct fix is an upstream issue/PR.
- The **one** first-party auto-synced long skill is StatsPAI (`00`); its split
  must happen upstream (§4, 🟡).

Net: the 500-line flag is **advisory for vendored content**, not a to-do list of
in-repo edits. The same pass fixed the four skills that had been scoring 57 for
missing YAML frontmatter (`04/scholar-evaluation`, `28/replicate-paper`, `38`,
`40`) — they now carry `name` + `description` and have left the low-hygiene set
(§3). See [`QUALITY_ASSESSMENT_2026-07.md`](QUALITY_ASSESSMENT_2026-07.md).

---

## 1. How to refresh this list

The repo's standard build does not write this file — the columns below
are *operational* judgments that change as maintainers act on them. To
regenerate the "blocked on upstream" list from the latest catalog:

```bash
# Lowest-hygiene skills
python3 -c "
import json
data = json.load(open('catalog/skills-enriched.json'))
for sk in sorted(data['skills'], key=lambda x: x['quality_score'])[:30]:
    eval_n = len(sk.get('eval_coverage', []))
    print(f'  {sk[\"quality_score\"]:3d}  lc={sk[\"line_count\"]:4d}  eval={eval_n}  {sk[\"path\"]}')"
```

The output of that one-liner as of the 2026-07-08 catalog is in §3.

---

## 2. Status legend

| Status | Meaning | Action |
|---|---|---|
| **🟢 Split** | Skill's upstream has been split into a lean spine + `references/` | Mirror should be re-vendored on the next sync. |
| **🟡 Blocked on upstream** | First-party auto-synced collection; we cannot edit the mirror without it being overwritten | Open an issue / PR in the upstream repo. |
| **🟠 Manual vendor snapshot** | Faithful third-party mirror; deliberately preserved | Do not restructure here. The right place is the *original* author's repo. |
| **⚪ Not long** | Short skill, nothing to do | — |
| **🟤 Evaluated, keep** | Reviewed; structural quirks are acceptable for this skill's role (e.g. pro-forma reference dump at end) | — |
| **🔴 Replace** | Quality / consistency so low the better fix is to drop the skill or replace it with a maintained alternative | Open a "Skill: replace" issue. |

---

## 3. Long / low-hygiene inventory (top 30 by lowest hygiene)

| Score | Lines | Evals | Path | Status (as of 2026-07-08) |
|---:|---:|---:|---|---|
| 85 | 2256 | 15 | `skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md` | 🟡 Blocked on upstream — first-party, weekly-synced; anchors 15 eval scenarios. The one split to drive upstream. |
| 85 | 1502 | 0 | `skills/25-HosungYou-Diverga/skills/d2/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 1308 | 0 | `skills/25-HosungYou-Diverga/skills/c2/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 1215 | 0 | `skills/04-K-Dense-AI-claude-scientific-writer/citation-management/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 1201 | 0 | `skills/25-HosungYou-Diverga/skills/e1/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 1103 | 0 | `skills/42-wanshuiyin-ARIS/skills/skills-codex-gemini-review/paper-poster/SKILL.md` | 🟠 Manual vendor snapshot (ARIS family). |
| 85 | 1097 | 0 | `skills/42-wanshuiyin-ARIS/skills/paper-poster/SKILL.md` | 🟠 Manual vendor snapshot (ARIS family). |
| 85 | 1097 | 0 | `skills/42-wanshuiyin-ARIS/skills/skills-codex/paper-poster/SKILL.md` | 🟠 Manual vendor snapshot (ARIS family). |
| 85 | 1069 | 0 | `skills/67-econfin-workflow-toolkit/Foreign-CF-study/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 1022 | 0 | `skills/25-HosungYou-Diverga/skills/c1/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 1000 | 0 | `skills/25-HosungYou-Diverga/skills/d4/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 982 | 0 | `skills/63-tondevrel-scientific-agent-skills/dowhy/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 981 | 0 | `skills/20-wenddymacro-python-econ-skill/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 952 | 0 | `skills/04-K-Dense-AI-claude-scientific-writer/research-grants/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 923 | 0 | `skills/25-HosungYou-Diverga/skills/b1/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 891 | 0 | `skills/25-HosungYou-Diverga/skills/e2/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 881 | 0 | `skills/67-econfin-workflow-toolkit/chinese-ppt/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 875 | 0 | `skills/67-econfin-workflow-toolkit/China-CF-study/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 874 | 0 | `skills/26-Data-Wise-scholar/skills/writing/methods-paper-writer/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 840 | 0 | `skills/55-ab604-claude-code-r-skills/skills/tdd-workflow/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 832 | 0 | `skills/33-Galaxy-Dawn-claude-scholar/skills/uv-package-manager/SKILL.md` | 🟠 Manual vendor snapshot. |
| 85 | 812 | 0 | `skills/25-HosungYou-Diverga/skills/c3/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 85 | 809 | 0 | `skills/25-HosungYou-Diverga/skills/memory/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 92 | 785 | 0 | `skills/67-econfin-workflow-toolkit/data-fetcher/SKILL.md` | 🟠 Manual vendor snapshot. |
| 92 | 782 | 0 | `skills/25-HosungYou-Diverga/skills/g6/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 92 | 759 | 0 | `skills/58-charlescoverdale-econstack/cost-benefit/SKILL.md` | 🟠 Manual vendor snapshot. |
| 92 | 741 | 1 | `skills/56-hanlulong-econ-writing-skill/econ-write/SKILL.md` | 🟠 Manual vendor snapshot. |
| 92 | 740 | 0 | `skills/25-HosungYou-Diverga/skills/humanize/SKILL.md` | 🟠 Manual vendor snapshot (Diverga family). |
| 92 | 735 | 0 | `skills/42-wanshuiyin-ARIS/skills/research-refine/SKILL.md` | 🟠 Manual vendor snapshot (ARIS family). |
| 92 | 716 | 0 | `skills/26-Data-Wise-scholar/skills/research/method-transfer-engine/SKILL.md` | 🟠 Manual vendor snapshot. |

> **Read this as a triage table.** A 🔴 / 🟡 row is an *action* the maintainer team has decided to take. A 🟠 row is **deliberately preserved** — do not "fix" these by editing in place. The repo's value here is faithful mirrors; rewriting them under our own authorship would defeat the provenance chain.

---

## 4. Single highest-leverage action: split StatsPAI upstream

Out of the 1,150 skills in the catalog, only one has both

1. A **first-party auto-synced upstream** we can change in one place, and
2. **>900 lines** of SKILL.md (line count 2256 — second only to a handful of large Diverga / ARIS / Galaxy-Dawn mirrors).

That is `skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md`, which also happens to anchor **15 of 17 numeric-benchmark tasks** and one of the largest eval-coverage rows in `SKILL_HYGIENE.md`. Splitting it upstream into a lean spine + `references/` will:

- Halve the time-to-load for any agent that only needs the routing header
- Make the weekly sync diffs smaller and reviewable
- Free us to keep the mirror in this repo as a faithful copy

This is the **one** split the maintainer team should drive upstream. All other long skills in §3 are manual vendor snapshots, where the right action is an upstream issue, not an in-repo edit.

---

## 5. Cross-reference

- **Plan / why split?** → [`LONG_SKILL_SPLIT_PLAN.md`](LONG_SKILL_SPLIT_PLAN.md)
- **Scores by collection** → [`SKILL_HYGIENE.md`](SKILL_HYGIENE.md)
- **Eval coverage** → [`SKILL_HYGIENE.md`](SKILL_HYGIENE.md) (second column)
- **Tooling** → `python3 scripts/split-skill.py <path>` (read-only by default)
- **Skill structure conventions** → `docs/SKILL_SUBMISSION_GUIDE.md`
