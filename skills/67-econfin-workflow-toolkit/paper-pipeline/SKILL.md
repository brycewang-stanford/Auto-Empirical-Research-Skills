---
name: paper-pipeline
description: "Orchestrate the complete post-first-draft polishing pipeline for an academic LaTeX paper by invoking five existing skills in fixed order: (1) paper-polish, (2) paper-self-revise, (3) paper-style, (4) paper-polish again, (5) reference-verify. Trigger when user says \"paper pipeline\" / \"paper-pipeline\" / \"论文流水线\" / \"全流程打磨\" / \"一条龙打磨\" / \"初稿打磨\" / \"full polish pipeline\" / \"run the whole pipeline\", or wants the entire post-draft polishing sequence run on a paper folder. Use this skill whenever the user asks for several paper-finishing steps (polish + revise + style + reference check) on one manuscript in one go, even if they don't name every individual skill."
allowed-tools: Skill, Read, Edit, Write, Glob, Grep, Bash, AskUserQuestion, WebSearch, WebFetch, Agent
argument-hint: [path-to-project-folder] [target-journal(optional)]
---

# Paper Pipeline

## Overview

This skill runs the **full post-first-draft polishing process** on an academic paper by invoking five existing skills in a fixed order. It is an orchestrator: it does not duplicate any sub-skill's logic. Each stage is executed by invoking the corresponding skill with the **Skill tool** and following that skill's own workflow to full completion before moving on.

**The pipeline (fixed order — never reorder or skip without explicit user request):**

| Stage | Skill | Purpose in the pipeline |
|-------|-------|------------------------|
| 1 | `paper-polish` | Clean mechanical, consistency, and citation errors so the self-review can focus on substance |
| 2 | `paper-self-revise` | Deep internal review and content revision on a clean draft |
| 3 | `paper-style` | Restructure title + sections to the target journal, after content has stabilized |
| 4 | `paper-polish` | Second pass: catch issues introduced by Stages 2–3 (cross-references, merge seams, new prose) |
| 5 | `reference-verify` | Final reference audit, once the citation set is settled by all prior edits |

The order matters: polishing before reviewing keeps the review substantive; restructuring after content revision avoids churn; the second polish exists specifically because Stages 2–3 modify text and structure; reference verification runs last because earlier verification would be partially invalidated by later edits.

**Input**: A project folder containing `main.tex` (plus tables/figures, `ref.bib`).
**Output**: The fully polished `main.tex` + `ref.bib`, per-stage backups, a `ref_verify_report.xlsx`, and a final pipeline report.

---

## Phase 0: Setup (do all of this BEFORE invoking any sub-skill)

1. **Receive folder path** from `$ARGUMENTS` or ask. Verify `main.tex` exists with Glob.

2. **Dropbox conflict check**: Glob the project folder for `*冲突副本*` and `*conflicted copy*`. If found, stop and ask the user to resolve which version is canonical before anything else. Re-run this check between every stage (concurrent Overleaf editing can silently revert edits, and a 5-stage pipeline is a long exposure window).

3. **Check for a previous pipeline run**: if `pipeline_state.json` exists in the folder and has incomplete stages, show its status and ask: resume from the first incomplete stage, or start over from Stage 1? If resuming, skip directly to that stage.

4. **Collect the target journal now** (needed by Stage 3, asked upfront so the pipeline never stalls mid-run). If given in `$ARGUMENTS`, use it. Otherwise use AskUserQuestion with common options (JFE / JF / RFS / Management Science) plus "Other" for free-form input.

5. **Ask for the interaction mode** with AskUserQuestion — this is the single most important setup question, because five interactive skills back-to-back can mean hundreds of approval prompts:
   - **全程交互** — every sub-skill runs in its native item-by-item approval mode. Choose for final pre-submission runs.
   - **阶段确认** (recommended default) — within each stage, changes are applied without per-item prompts, but the pipeline pauses at each stage boundary to show that stage's summary and get a go-ahead before the next stage starts.
   - **全自动** — run all five stages straight through; only the final report at the end. The user's upfront choice of this mode counts as the explicit opt-in that each sub-skill's fast path requires.

6. **Create the backup baseline**: make a `pipeline_backups/` subfolder and copy `main.tex` → `pipeline_backups/main_stage0.tex` and `ref.bib` → `pipeline_backups/ref_stage0.bib`. After each completed stage, snapshot `main.tex` as `main_after_stage<N>.tex`. These snapshots are the rollback path if a later stage goes wrong.

7. **Write `pipeline_state.json`** in the project folder:

```json
{
  "folder": "<path>",
  "target_journal": "<journal>",
  "mode": "stage-confirm",
  "started": "<date via Bash>",
  "stages": {
    "1_paper_polish": "pending",
    "2_paper_self_revise": "pending",
    "3_paper_style": "pending",
    "4_paper_polish_2nd": "pending",
    "5_reference_verify": "pending"
  }
}
```

Update the relevant stage to `"in_progress"` when it starts and `"done"` when it completes. This file is what makes the pipeline resumable after an interrupted session.

---

## Stage Execution Protocol

For every stage, follow this exact sequence:

1. **Announce the stage** with a banner so the user always knows where the pipeline is:

```
════════════════════════════════════════
  Stage N/5: <skill-name>  —  <one-line purpose>
════════════════════════════════════════
```

2. **Mark the stage `in_progress`** in `pipeline_state.json`.

3. **Invoke the sub-skill with the Skill tool** (e.g., `skill: paper-polish`, `args: <folder path>`). Then follow the loaded skill's instructions **to full completion** — all of its checks/comments/phases, including its own completion summary. Never paraphrase or shortcut a sub-skill's workflow; the whole point of the pipeline is that each stage runs exactly as it would standalone.

4. **Apply the interaction mode**:
   - 全程交互: follow the sub-skill's native approval flow unchanged.
   - 阶段确认 / 全自动: the user's mode choice in Phase 0 is the explicit authorization each sub-skill's fast path requires — treat it as the user having already said "accept all remaining" (paper-polish), "yes to all" (paper-self-revise), "直接改" (paper-style), and `apply: auto` (reference-verify). Still display each change block as the sub-skill specifies, so the user can scroll back and audit; just don't wait for input.

5. **On stage completion**: snapshot `main.tex` to `pipeline_backups/`, mark the stage `"done"`, re-run the Dropbox conflict check, and record a 3–5 line stage summary (counts of changes applied/skipped, sections touched, anything flagged).

6. **Stage boundary**: in 阶段确认 mode, show the stage summary and ask "继续下一阶段？(yes / pause)". In 全自动 mode, continue directly. In 全程交互 mode, a brief "Stage N 完成，进入 Stage N+1" notice suffices since the user has been involved throughout.

---

## Stage-Specific Notes

**Stage 1 — paper-polish (first pass)**: Run all 19 checks as the skill specifies. Pass the project folder path as args.

**Stage 2 — paper-self-revise**: The skill's Phase 0 asks whether a review report already exists. In the pipeline context, prefer a **fresh review**: if a `review.pdf`/`review.md` from an earlier round is present, ask the user whether to reuse it or regenerate (stale comments may already be addressed); in 全自动 mode, regenerate without asking. The generated review excludes anything requiring new empirical work, which matches the pipeline's text-only scope.

**Stage 3 — paper-style**: Pass both the folder path and the target journal collected in Phase 0 as args, so the skill's Phase 0 journal question is already answered. In 全自动 mode the skill's fast path picks the title itself; when in doubt there, prefer keeping the current title (case-adjusted) — the title is the most subjective change in the whole pipeline and the easiest to get wrong silently.

**Stage 4 — paper-polish (second pass)**: Run all 19 checks again in full. Expect the yield to concentrate in: hardcoded section references broken by Stage 3 renumbering, merge-seam transitions, abbreviations re-defined or orphaned by moved text, text–table consistency in paragraphs Stage 2 rewrote, and em-dashes introduced by new prose. A second full pass is deliberate — do not skip checks just because Stage 1 ran them.

**Stage 5 — reference-verify**: Run on the project directory (Excel output, default settings). Map the pipeline mode onto `APPLY_FIXES`: 全程交互 → `interactive`; 阶段确认/全自动 → `auto`. The skill makes its own timestamped backups before editing and writes `ref_verify_changes.md`.

---

## Final Report

After Stage 5, mark all stages done in `pipeline_state.json` and present:

```
# Paper Pipeline 完成报告

论文: <title>    目标期刊: <journal>    模式: <mode>

| Stage | Skill | 应用 | 跳过 | 要点 |
|-------|-------|------|------|------|
| 1 | paper-polish | 12 | 3 | 修正 5 处文表不一致 |
| 2 | paper-self-revise | 9 | 1 | 审稿报告 14 条意见，强化引言张力 |
| 3 | paper-style | — | — | 10→8 节，标题改为 sentence case |
| 4 | paper-polish (2nd) | 6 | 0 | 修复 3 处硬编码 Section 引用 |
| 5 | reference-verify | 4 | 1 | 50 条引用，2 条元数据修正，报告见 xlsx |

备份: pipeline_backups/ （main_stage0 … main_after_stage5）
报告文件: review.pdf · ref_verify_report.xlsx · ref_verify_changes.md
遗留事项: <anything any stage flagged but did not fix, e.g. abstract over word limit>
```

The 遗留事项 list matters: sub-skills (especially paper-style Phase 5 and reference-verify) flag out-of-scope issues they deliberately don't fix — collect them all in one place so nothing silently evaporates.

---

## Rules

- **One stage at a time, in order.** Never start a stage before the previous one's skill workflow has fully completed. Never run two sub-skills' steps interleaved.
- **The pipeline is text-only.** No stage re-runs regressions or changes empirical results; if a sub-skill surfaces an issue that would require new empirics, flag it in 遗留事项 instead.
- **Partial pipelines on request**: if the user asks to start from a specific stage or skip one ("跳过 paper-style"), honor it and record the skipped stage as `"skipped"` in the state file.
- **If a stage fails or the user aborts mid-stage**: leave the state file showing `in_progress` for that stage, summarize what was applied so far, and remind the user the pipeline can resume later by re-invoking paper-pipeline on the same folder.
- Communicate with the user in **Chinese**; all LaTeX content stays in **English**. No em-dash (`---`) in any newly written prose, per house rules.
