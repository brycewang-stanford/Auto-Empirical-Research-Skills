---
name: stat-writing
description: End-to-end statistical writing assistant for LaTeX - draft title/abstract/keywords, expand outlines into sections, audit manuscripts, write reviewer reports and response letters, and scaffold book manuscripts.
license: CC0-1.0
metadata:
  author: stat-writing-one-skill
  version: "3.0"
compatibility: Codex (CLI + IDE). Optional scripts require Python 3.
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/fuhaoda/stats-paper-writing-agent-skills
  项目名称: stats-paper-writing-agent-skills
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Statistical Writing (One Skill)

This is a single "workbench" skill for statistical manuscripts written in LaTeX.

Guidance is split into focused references under `references/`. Deterministic checks live in `scripts/`. Ready-to-use templates live in `assets/`.

## Positioning: Hybrid + JDS profile

Default behavior is journal-agnostic. For Journal of Data Science (JDS), apply the JDS profile:

- Maintain strong literature positioning and explicit novelty.
- Require clean cross-referencing and cleaned BibTeX.
- Prefer vector graphics for figures in the manuscript.
- Enable line numbers for review drafts.
- Include reproducibility artifacts (code/data/supplement) when possible.

## When to use this skill

Use this skill when the user wants to:

1. Generate compliant front matter (title, abstract, keywords).
2. Expand outlines into complete sections in LaTeX.
3. Audit a manuscript for structure, style, references, and reproducibility quality.
4. Draft reviewer reports.
5. Draft point-by-point response letters.
6. Scaffold a book manuscript from a chapter plan.

## Inputs to ask for (minimal)

Prefer file paths over pasted text.

- Manuscript tasks: root TeX file (for example `main.tex`).
- Reference checks: BibTeX file(s) (for example `refs.bib`).
- Response letters: full reviewer/editor comments + revised text if available.
- Reviewer report: manuscript or extended abstract being reviewed.
- Book manuscript: chapter list, audience, tone, and desired notation style.

If details are missing, proceed with placeholders like `	odo{...}` and ask only critical questions.

## Output conventions

Unless the user requests otherwise:

- Return LaTeX-ready output.
- For audits: rank issues as HIGH/MED/LOW with concrete fixes.
- For rewrites: include revised text and short change log.
- Never invent results or citations. Use `	odo{add citation}` or `	odo{verify result}`.

## Task routing map

Open only the reference files needed for the task.

- Title: `references/10-title.md`
- Abstract: `references/11-abstract.md`
- Keywords: `references/12-keywords.md`
- Outline to section drafting: `references/60-outline-to-section.md`
- Introduction: `references/20-introduction.md`
- Data: `references/21-data.md`
- Methods: `references/22-methods.md`
- Simulation (ADEMP): `references/23-simulation.md`
- Application/Results: `references/24-application.md`
- Discussion: `references/25-discussion.md`
- Other sections: `references/30-other-sections.md`
- General style/storyline: `references/31-general-style.md`
- English pitfalls: `references/32-english.md`
- BibTeX/natbib: `references/40-bibtex-natbib.md`
- Labels/cross-references: `references/41-cross-referencing.md`
- Reviewer report: `references/50-review-report.md`
- Response to reviewers: `references/51-response-to-reviewers.md`
- Research proposal/project cycle: `references/70-project-proposal.md`
- Book manuscript workflow: `references/71-book-manuscript.md`
- Tooling/reproducibility: `references/80-tooling.md`

## Built-in assets

- Response letter (LaTeX): `assets/response-letter-template.tex`
- Reviewer report (Markdown): `assets/reviewer-report-template.md`
- Reviewer report (LaTeX): `assets/reviewer-report-template.tex`
- Generic section skeleton: `assets/section-skeleton.tex`
- Manuscript starter (LaTeX): `assets/manuscript-template.tex`
- Book manuscript starter (LaTeX): `assets/book-manuscript-template.tex`

## Optional scripts (deterministic checks)

- Manuscript checks: `python scripts/check_tex.py path/to/main.tex`
- Citation/BibTeX checks: `python scripts/check_bib.py --tex path/to/main.tex --bib path/to/refs.bib`
- Combined run: `python scripts/audit_paper.py --tex path/to/main.tex --bib path/to/refs.bib`

These checks are heuristic and do not compile LaTeX.

## Workflows

### Workflow A - Finished paper to abstract + keywords

1. Read introduction/methods/results/discussion.
2. Use `references/11-abstract.md` and `references/12-keywords.md`.
3. Draft abstract (default 6-8 sentences, acceptable 4-10, no citations, no math notation).
4. Draft 6-10 keywords, alphabetized, avoid repeating title terms.
5. Return:
   - `egin{abstract}...nd{abstract}`
   - `\keywords{...}` (or venue-specific command)
   - short compliance checklist.

### Workflow B - Manuscript audit

1. Run `check_tex.py` (and `check_bib.py` if `.bib` exists).
2. Use `references/31-general-style.md`, `references/40-bibtex-natbib.md`, and section-specific references.
3. Return top issues ranked by severity and concrete LaTeX edits.
4. For JDS profile, explicitly call out line numbers, vector graphics, cleaned BibTeX, and reproducibility supplement readiness.

### Workflow C - Reviewer report drafting

1. Use `references/50-review-report.md`.
2. Write summary + overall assessment + numbered major/minor comments.
3. Keep tone constructive and professional.
4. If requested, output using `assets/reviewer-report-template.tex`.

### Workflow D - Response to reviewers

1. Use `references/51-response-to-reviewers.md`.
2. Structure by Editor, Associate Editor, Reviewer sections.
3. For every comment: quote, respond, quote manuscript change, add location.
4. If requested, render with `assets/response-letter-template.tex`.

### Workflow E - Outline to full section

1. Identify section type.
2. Use `references/60-outline-to-section.md` + relevant section reference.
3. Expand bullets into coherent paragraphs with transitions.
4. Use placeholders where information is missing.

### Workflow F - Book manuscript scaffolding

1. Use `references/71-book-manuscript.md`.
2. Start from `assets/book-manuscript-template.tex`.
3. Build frontmatter/mainmatter/backmatter and chapter map.
4. Keep notation generic by default; add optional custom notation block only when requested.

## Copy/paste prompt patterns

### Abstract + keywords
"Use `stat-writing`. Read `main.tex` and draft a compliant abstract (default 6-8 sentences, acceptable 4-10; no citations; no math notation) and 6-10 alphabetical keywords. Output LaTeX blocks."

### Full audit
"Use `stat-writing`. Audit `main.tex` (+ `refs.bib`). Run scripts if allowed. Return top issues with HIGH/MED/LOW and patch-ready LaTeX fixes."

### Response to reviewers
"Use `stat-writing`. Here are reviewer/editor comments. Write a point-by-point response letter with quoted manuscript revisions and locations."

### Reviewer report
"Use `stat-writing`. Draft a reviewer report with summary, overall assessment, numbered major comments, and numbered minor comments."

### Book manuscript
"Use `stat-writing`. Start a book manuscript from chapter bullets using the book template. Produce frontmatter/mainmatter/backmatter and chapter-by-chapter drafting plan."
