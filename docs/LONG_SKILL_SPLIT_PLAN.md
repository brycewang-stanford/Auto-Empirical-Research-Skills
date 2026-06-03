# Long-Skill Split Plan

The repo audit flags **75 SKILL.md files over 500 lines**; the enrichment layer
flags **56 as "long without a `references/` directory."** Agent-skill best
practice is a lean spine (~< 500 lines) plus a `references/` directory the agent
loads on demand. This document says *which* files to split, *how*, and — crucially
— *where*, because most long files here are mirrors we must not edit in place.

## Policy: split upstream, not in this repo

| Class | Examples | What to do |
|---|---|---|
| **Auto-synced first-party** | `00-…StatsPAI` (`weekly GitHub Actions sync`) | Split in the **upstream** repo (`brycewang-stanford/StatsPAI`). Editing the copy here is pointless — the weekly sync overwrites it. |
| **Manual vendor snapshots** | `25-HosungYou-Diverga`, `04-…scientific-writer`, `42-…ARIS`, etc. (`manual vendor snapshot`) | These are faithful third-party mirrors; the repo deliberately preserves them. **Do not** restructure them here. If worthwhile, open a PR in the *original* author's repo. |
| **First-party, not synced** | (none currently long-without-references) | Safe to split directly here with the tool below. |

Net: the one clear, high-value action is **splitting StatsPAI upstream**. The
00.1/00.2/00.3 pipeline skills already use `references/` and are owned by the
distribution track.

## Tooling: `scripts/split-skill.py`

Read-only by default; never edits the input. `--apply OUTDIR` writes a proposed
split to a fresh directory for review.

```bash
# Inspect the proposed section split (line counts + keep/move decisions)
python3 scripts/split-skill.py skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md

# Materialize it into a directory you can copy into the upstream repo
python3 scripts/split-skill.py skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md \
    --apply /tmp/statspai-split
#  -> /tmp/statspai-split/SKILL.md (~494 lines) + references/01..11-*.md
```

The tool splits at top-level `##` headings, keeps orientation sections inline,
and moves any section longer than `--threshold` (default 80) lines into
`references/NN-slug.md` with a one-line summary + link left in the spine. The
frontmatter and any leading provenance banner stay in the spine.

## Worked example: StatsPAI (1943 → ~494 spine + 11 references)

| Kept in spine (orientation) | Moved to `references/` (deep detail) |
|---|---|
| Why for Agents; pipeline overview; three domain modes; figure/table inventory; export cookbook; Step −1 PAP; Table 1; Step 6 mechanisms; regtable cookbook; figure factory; common mistakes; agent integration; when-to-use | Notebook setup (87); Step 0 sample construction (81); Step 2 empirical strategy (102); Step 3 ID graphics (103); **Step 4 main results (214)**; Step 5 heterogeneity (109); **Step 7 robustness gauntlet (232)**; Step 8 replication (102); Epi pipeline (169); ML-causal pipeline (169); method catalog (126) |

This keeps the agent-facing "what to do, in order" spine small while the
language- and step-specific recipes load on demand — the same progressive
disclosure the 00.1/00.2/00.3 ports already use.

## Suggested upstream procedure (StatsPAI)

1. In `brycewang-stanford/StatsPAI`, run the tool against the skill and
   `--apply` into the skill directory (or hand-curate the section summaries).
2. Replace the section bodies in `SKILL.md` with a 1–2 sentence summary + a
   `See [references/NN-….md]` link; commit the `references/` files alongside.
3. Tighten the auto-generated summaries (the tool leaves a stub link; a human
   sentence reads better).
4. Merge upstream. The weekly `sync-statspai-skill` workflow then brings the
   lean spine into this repo automatically — no divergence, no manual edit here.

## Tracking

Re-run the enrichment to watch the flag count fall as upstream splits land:

```bash
make catalog            # regenerates catalog/skills-enriched.json
grep -c "no-references" docs/SKILL_QUALITY.md   # improvement targets remaining
```
