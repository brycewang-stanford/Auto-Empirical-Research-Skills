---
name: paper-style
description: Restructure an academic paper's title and section structure to match a target journal's house style. Asks the user to specify the target journal first, then adjusts main.tex accordingly (title wording and case, section skeleton, heading case, numbering scheme, merging/splitting sections). Trigger when user says "paper style" / "paper-style" / "期刊风格" / "按目标期刊调整" / "调整为XX风格" / "JFE风格" / "convert to journal style" / "restructure for [journal]", or wants a paper's title/sections reformatted for a specific journal submission.
allowed-tools: Read, Edit, Write, Glob, Grep, AskUserQuestion, Bash, WebSearch, WebFetch
argument-hint: [path-to-project-folder] [target-journal(optional)]
---

# Paper Style

## Overview

This skill adapts an existing academic paper (`main.tex`) to the **house style of a target journal**, focusing on two things:

1. **Title** — wording, length, case, and subtitle conventions.
2. **Section structure** — the section skeleton, heading case, numbering scheme, section count, and whether sections should be renamed, merged, split, or reordered.

The skill asks the user for the target journal **first**, before analyzing the paper, because the journal determines every subsequent judgment. It then proposes a complete restructuring plan, gets approval, and applies the changes to `main.tex` in place.

**Scope discipline**: This skill changes *structure*, not *content*. Body prose is never rewritten, except for minimal transition sentences where sections are merged (the opening sentence of a merged section must announce its combined contents). Empirical results, tables, figures, citations, and arguments are untouched.

**Input**: A project folder containing `main.tex` (plus tables/figures subfolders, `ref.bib`, possibly journal `.sty`/`.bst` files).

**Output**: Revised `main.tex` with journal-conforming title and section structure.

---

## Workflow

### Phase 0: Target Journal

1. **Receive folder path** from user (via `$ARGUMENTS` or ask). Verify `main.tex` exists with Glob.
2. **Check for Dropbox conflict copies** before any editing: Glob for files matching `*冲突副本*` or `*conflicted copy*` in the project folder. If found, warn the user and stop until they resolve which version is canonical (concurrent Overleaf editing can silently revert edits).
3. **Ask for the target journal** — unless it was already given in `$ARGUMENTS`. Use AskUserQuestion with the most common targets as options plus free-form "Other":
   - Journal of Financial Economics (JFE)
   - Journal of Finance (JF)
   - Review of Financial Studies (RFS)
   - Management Science
   - (User selects "Other" to type any journal: AER, QJE, RAND, Research Policy, JIE, JCF, JBF, JAR/JAE/TAR, ...)

   Ask this **before** reading the paper. The journal choice drives the entire analysis.

### Phase 1: Load the Journal's Style Profile

1. **Read `references/journal-profiles.md`** and locate the profile for the chosen journal. Each profile specifies: title conventions, numbering scheme, heading case, introduction treatment, canonical section skeleton, literature-review placement, hypothesis conventions, and typical section count.
2. **If the journal is not in the reference file**, derive a profile rather than guessing:
   a. Map it to the closest family in the reference file (e.g., any Elsevier economics/finance journal → JFE-family conventions; any AEA journal → AER-family).
   b. If the family is unclear, use WebSearch to pull the table of contents and 2–3 recent articles from the journal's latest issue, and extract: how titles are phrased, how sections are numbered and cased, whether a standalone literature review exists, and the typical skeleton.
   c. Present the derived profile to the user in one short paragraph for confirmation before proceeding.
3. **Check the project for existing journal artifacts** (e.g., `jfe.bst`, `jfe.sty`, `ecta.cls`): if style files for the *target* journal are already present, numbering and case may be partially handled by the class — note this and avoid fighting the style file.

### Phase 2: Map the Current Paper

1. **Read `main.tex` in full.**
2. **Extract the current state**:
   - Title (`\title{}`), running head if any, abstract length, keywords/JEL.
   - The full section tree: every `\section`, `\subsection`, `\subsubsection` with its heading text and `\label`.
   - All in-text section references: `\ref{sec:...}` and any **hardcoded** "Section 5"-style mentions (Grep for `Section~?\s*\d` and `Sections~?\s*\d`). Hardcoded numbers will break under renumbering and must be tracked.
   - Appendix / Online Appendix boundaries (these are normally left untouched).

### Phase 3: Propose the Restructuring Plan

Present one complete plan covering both deliverables, then get approval. Do not edit anything before approval.

#### 3a. Title proposal

Offer the current title plus 2–3 candidates that conform to the journal's title conventions, with one-line rationales. Use AskUserQuestion so the user picks (options: keep current title — case-adjusted if needed — or one of the candidates; "Other" lets them type their own).

#### 3b. Structure proposal

Present a mapping table:

```
现有结构 → 目标结构（JFE 风格）

| # | 现有章节 | 动作 | 目标章节 | 理由 |
|---|---------|------|---------|------|
| 1 | Introduction | 保留 | 1. Introduction | — |
| 2 | Rating Environment and Hypothesis Development | 改名 | 2. Institutional background | JFE 标题用 sentence case、短标题 |
| 6 | How Issuers Respond to a Downgrade | 改名 | 5. Mechanisms | 叙事式标题不符合 JFE 惯例 |
| 8 | Dynamics and Welfare Effects | 合并入 | 7. Additional analyses | JFE 偏好 6–8 节的紧凑结构 |
| 9 | Cross-Rater Evidence | 合并入 | 7. Additional analyses | 同上 |
...

章节数：10 → 8。受影响的交叉引用：3 处硬编码 "Section 9" 需更新。
```

Actions vocabulary: 保留 (keep), 改名 (rename), 合并 (merge), 拆分 (split), 移动 (reorder), 降级 (demote to subsection), 升级 (promote to section).

Explain *why* each change follows from the journal profile, not just *what* changes. Then use AskUserQuestion: approve the whole plan / adjust specific rows / cancel.

**Fast path**: if the user has said "直接改" / "无需确认" / "apply directly", skip the approval questions: pick the best title candidate yourself and apply the full plan.

### Phase 4: Apply the Changes

Edit `main.tex` with the approved plan. Craft rules:

1. **Title**: update `\title{}` and any running-head command. Do not rename the folder or file.
2. **Heading case conversion**: when converting to sentence case, keep proper nouns and acronyms capitalized (ETF, Morningstar, China, DiD, IV). When converting to title case, follow standard title-case rules (lowercase short prepositions/articles).
3. **Merging sections**: convert the absorbed section's `\section` to `\subsection` (or fold its text in). **Keep every `\label` intact** — a dissolved section's label stays attached to the absorbed subsection so all `\ref`s still resolve. Update the merged section's opening sentence to announce all the content it now covers. Remove `\clearpage`/`\newpage` commands that the merge has orphaned.
4. **Splitting/reordering**: move whole blocks verbatim (including their "Insert Table X about here" placement blocks, which always travel with their text). Never reorder paragraphs within a section.
5. **Cross-references**: after renumbering, fix every hardcoded "Section N" mention found in Phase 2 — preferably by converting it to `Section~\ref{sec:...}`; otherwise update the number.
6. **Numbering scheme**: section numbering (arabic vs. Roman, lettered subsections) is normally produced by the document class or `.sty` file. If the target journal's style file is present, rely on it. If not, do **not** hand-fake Roman numerals inside `\section{}` text; instead add the appropriate `\renewcommand{\thesection}{...}` lines in the preamble, and tell the user what was added.
7. **Unnumbered introductions** (JF/AER convention): use `\section*{}` plus manual TOC/label handling only if the user's template doesn't already handle it; mention the change explicitly.
8. **Appendices and the Online Appendix**: leave their internal structure untouched unless the plan explicitly includes them.

### Phase 5: Report

1. **Summary**: title before/after; section tree before/after; count of renames/merges/cross-reference fixes.
2. **Flag, don't fix**: list any *other* journal-style mismatches noticed along the way (bibliography style mismatch, abstract over the journal's word limit, missing/extra keywords or JEL codes, table-note conventions) as suggestions for follow-up. These are out of scope for this skill — report them in 2–3 lines, do not change them.
3. **Offer a consistency pass**: re-read the edited regions to verify all `\ref`s resolve, transitions at merge seams read naturally, and no duplicate section numbers exist.

---

## Writing Rules

- Communicate with the user in **Chinese**; all LaTeX content stays in **English**.
- **Minimal diff**: never rewrite prose while restructuring. The only new sentences allowed are merge-seam transitions.
- Preserve all `\label{}`, `\ref{}`, `\cite{}`/`\citep{}`, math, and table/figure environments exactly.
- **Avoid the em-dash (`---`)** in any newly written sentence (merge transitions, revised headings). Use a colon, comma, parentheses, or two sentences instead. Leave en-dashes (`--`) in ranges untouched.
- Never invent content: if the journal skeleton calls for a section the paper lacks (e.g., a formal model for RAND), flag the gap to the user instead of writing one.
- If the same heading change appears in multiple files (e.g., a standalone `abstract.tex` or chapter files via `\input`), apply it consistently across them.
