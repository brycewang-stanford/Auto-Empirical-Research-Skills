<!-- Vendored into AERS from https://github.com/keemanxp/thematic-analysis-skill on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`keemanxp/thematic-analysis-skill`](https://github.com/keemanxp/thematic-analysis-skill) for the AERS catalog (license: MIT). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# Thematic Analysis Skill for Claude

A Claude skill that walks you through a rigorous thematic analysis (TA) of qualitative data, following Braun and Clarke's (2006) six-phase framework. The skill produces a manuscript-style Word document and an annotated thematic map ready for academic writing.

Built and maintained by **Chuah Kee Man** (Faculty of Education, Language and Communication, Universiti Malaysia Sarawak).

## What this skill does

Most TA tutorials stop at "find patterns in your data". This skill is the longer version. It asks you upfront what the research is actually asking, then disciplines every phase against that question.

Specifically, it covers:

- **Step 0**: Elicits the research question or objective before anything else. The question shapes which codes earn their keep and which themes hold.
- **Phase 1 (Interview)**: Plans the analysis. The four upfront analytic decisions are made explicit (rich description vs detailed account, inductive vs theoretical, semantic vs latent, epistemological stance).
- **Phase 2 (Familiarisation)**: Active reading of the corpus, with notes per item.
- **Phase 3 (Coding)**: Inclusive, systematic coding tied back to the research question.
- **Phase 4 (Searching for themes)**: Sorting codes into candidate themes, sub-themes and an initial thematic map.
- **Phase 5 (Reviewing themes)**: Two-level review using Patton's internal homogeneity and external heterogeneity criteria.
- **Phase 6 (Defining and naming themes)**: Final theme definitions, sub-themes and punchy theme names.
- **Phase 7 (Producing the report)**: A manuscript-grade Word document in strict academic register, with an annotated thematic map as a figure.

It also bundles the 15-point quality checklist and the five common pitfalls from the original paper, so the analysis can be audited before write-up.

## Output

Two files land in your workspace at the end:

- `<study_title>_thematic_analysis.docx` — the full manuscript-style write-up with Introduction, Method, Findings, optional Discussion and an APA 7th Edition reference list.
- `phase6_final_map.png` — the final thematic map, used as a figure in the manuscript.

Intermediate working files (familiarisation notes, code lists, candidate maps, theme definitions) are also saved so you can audit the process or revisit a phase.

## Writing register

The manuscript body is written in formal academic register suitable for peer-reviewed publication. Personal writing-style skills are deliberately switched off for the manuscript and switched back on only if you ask for ancillary outputs like a plain-language summary or a blog version of the findings.

## Installation

1. Download `thematic-analysis.skill` from this repo (or the [Releases](../../releases) page).
2. Open Claude (claude.ai or the desktop app).
3. Go to **Customize → Skills**.
4. Click **Upload skill** and select the `.skill` file.

Once installed, just mention "thematic analysis", "Braun and Clarke", "qualitative coding" or a similar phrase and Claude will pick the skill up. You can start by providing the sources (e.g., upload the interview transripts) or point to your folder where the transcripts are saved (for Google Drive connection or via Claude CoWork). 

## Quick start

A typical session looks like this:

```
You: I've got 12 interview transcripts on teacher attitudes
     toward AI. Help me run a thematic analysis.

Claude: Before we start, what's the research question or objective
        driving this study? If you've got several, list them in priority order.

You: RQ1: How do secondary school teachers in Malaysia describe
     their use of AI tools in lesson planning?
     RQ2: What concerns, if any, shape their adoption decisions?

Claude: Got it. I'll anchor every phase to these. Now, the four upfront
        decisions: rich description across the full set, or detailed
        account of one aspect?
        ...
```

The skill then walks through each phase, asks the necessary decisions, codes inclusively, builds the thematic map and produces the .docx at the end.

## Reference

Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology, 3*(2), 77–101. https://doi.org/10.1191/1478088706qp063oa

Where the skill quotes or paraphrases the paper, those statements are the method's published position. Everywhere else the skill is operationalising the framework into a working process Claude can follow.

## What this skill does not cover

- Interpretative Phenomenological Analysis (IPA)
- Grounded Theory
- Discourse Analysis
- Conversation Analysis
- Narrative Analysis
- Meta-analysis or statistical pooling

If your method is one of those, use a different skill. TA is broader and more flexible than IPA but is not a substitute for it.

## Companion skills

The skill works well alongside:

- **apa-referencing** for in-text citations and reference list formatting.
- **docx** (Anthropic's public skill) for the Word document output.
- **slr-prisma** if you also need a systematic literature review to sit alongside the empirical analysis.

## Versioning

This repo uses semantic versioning. See [CHANGELOG.md](CHANGELOG.md) for the version history.

## Licence

MIT. See [LICENSE](LICENSE).

## Contributing

Issues and pull requests welcome. If you're using the skill on a real project and want to suggest a phase-level improvement (a clearer prompt, a missing edge case, a better default), open an issue with the prompt and Claude's response so the fix can be tested against a real example.


