<!-- Vendored into AERS from https://github.com/keemanxp/slr-prisma on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`keemanxp/slr-prisma`](https://github.com/keemanxp/slr-prisma) for the AERS catalog (license: MIT). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# Claude Skill for Systematic Literature Review - PRISMA (slr-prisma)

<img width="1850" height="402" alt="slr-prisma" src="https://github.com/user-attachments/assets/111ee8e2-a2ae-4390-a4fc-ada0f50cb46a" />


A Claude skill that walks you through writing a systematic literature review following the PRISMA 2020 framework.

It covers the full 27-item PRISMA 2020 checklist, produces a Word document manuscript in **strict journal article format**, generates an **annotated PRISMA flow diagram**, and enforces **APA 7th Edition referencing** throughout. It does not cover meta-analysis or statistical pooling.

## What it does

The skill runs in six phases.

**Phase 1 — Interview.** Gathers your review topic, research questions, databases, eligibility criteria, screening process, quality appraisal tool, synthesis approach, and flow diagram numbers. You can upload existing documents (proposals, protocols, PROSPERO registrations, search logs, data extraction sheets, reference lists) and the skill will extract what it can, then only ask about whatever is missing.

**Phase 2 — Section-by-section drafting (strict journal format).** Works through the manuscript following the standard journal article structure: Title Page → Abstract → Introduction → Methods → Results → Discussion → Conclusions → Declarations → References → Tables → Figures → Appendices. Every section maps to its PRISMA 2020 checklist items. It pauses after each section for your feedback before moving on. Tone adjusts depending on whether you are a first-time reviewer or an experienced researcher.

**Phase 3 — PRISMA flow diagram.** Selects the correct template (new or updated review, databases only or other sources), confirms the numbers, and builds the diagram in two formats: as a table in the Word document, and as a visual using the Visualizer tool. Includes annotated guidance explaining what information belongs in each box of the diagram, so users learn the PRISMA flow structure as they go.

**Phase 4 — Referencing (APA 7th Edition).** All in-text citations and the reference list follow APA 7th Edition formatting. References are verified via web search to ensure they are real. Integrates with the `apa-referencing` skill for type-specific formatting rules.

**Phase 5 — Word document.** Compiles the full manuscript as a .docx with A4 formatting, double-spacing, heading styles, numbered sections, APA-style tables, and the flow diagram embedded in the Results section.

**Phase 6 — Checklist audit (optional).** Maps each of the 27 PRISMA items to where it appears in the manuscript, flagging anything missing or incomplete.

It also handles partial requests — just the Methods section, just a flow diagram, just a search strategy, checking references, or auditing an existing manuscript against the checklist.

## Key Features

- **✅Strict journal article format** — Manuscript structure now follows the standard format expected by peer-reviewed journals, with proper title page, numbered sections, declarations, and tables/figures at the end.
- **✅Annotated PRISMA flow diagram** — Detailed guidance explaining what goes in each box, with a visual diagram generated for learning purposes.
- **✅APA 7th Edition referencing** — Built-in enforcement of APA 7th for all citations and references, with verification via web search.
- **✅Drafting conventions** — Explicit rules for academic register, tense usage, citation requirements, and table/figure formatting.
- **✅Expanded flow diagram reference** — The `references/flow-diagram.md` now includes annotated tables showing what to put in each box and how to get each number.

## Installation

👉🏽Download the `slr-prisma.skill` file from [Releases](https://github.com/keemanxp/slr-prisma/releases) and install it in Claude (Customise > Skills).

Alternatively, copy the `SKILL.md` and `references/` folder into your Claude skills directory.

## How to start using

Enable this skill in Claude. Then whenever you prompt something like "Help me write a systematic literature review on TOPIC" or "Perform an SLR on TOPIC", it will begin reading the skill file to assist you. Respond to the questions clearly — this helps enhance the accuracy of your review.

For the best results, also install the companion skills:
- [`apa-referencing`](https://github.com/keemanxp/apa-referencing) — for APA 7th Edition reference formatting and verification
- `writing-style` — if you have one, it will be applied to all drafted prose

## File structure

```
slr-prisma/
├── SKILL.md                              # Main skill instructions
├── references/
│   ├── prisma-2020-checklist.md          # Full 27-item PRISMA 2020 checklist
│   └── flow-diagram.md                   # Flow diagram templates, guidance, and annotations
├── LICENSE
└── README.md
```

## PRISMA 2020

This skill is based on the [PRISMA 2020 statement](https://www.prisma-statement.org/prisma-2020) (Page et al., 2021). The checklist and flow diagram templates are distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

> Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71

## Licence

The PRISMA 2020 checklist and flow diagram content is licensed under CC BY 4.0 (see above). The skill itself is licensed under the [MIT Licence](LICENSE).
