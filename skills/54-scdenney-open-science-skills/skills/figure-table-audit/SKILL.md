---
name: figure-table-audit
description: Audit figures, tables, captions, cross-references, and statistical notes.
argument-hint: "[path to manuscript, figures, tables, SI, or compiled PDF; include target journal if known]"
---

# Figure and Table Auditor

## Heritage and scope

This is an original Open Science Skills workflow for manuscript QA. It remixes general figure/table and citation-compliance ideas from Cheng-I Wu's *Academic Research Skills for Claude Code* (CC BY-NC 4.0), but is rewritten for open-science social-science manuscripts. It is not a visual hallucination engine: when a claim requires reading plotted values from an image, prefer source data or mark the issue as needing author verification.

This is the **end-stage** auditor. For figure design and production guidance during drafting, use the `figures` skill; for table design, use the `tables` skill. Run `figure-table-audit` once the figure and table set is stable and you are preparing for submission.

## Instructions

### 1. Orient before auditing

Identify:

- Manuscript source and compiled output, if any.
- Figure directory, table files, appendix/SI files, and build command.
- Target journal or style guide.
- Whether figures are generated from code, manually edited, or exported from software.
- Whether source data for figures/tables are available.

If only a PDF is available, state that cross-reference and value checks are lower confidence.

### 2. Inventory figures and tables

Build an inventory with:

- Figure/table number or label.
- File path or source location.
- Caption/title.
- First in-text callout.
- Appendix/SI location if applicable.
- Producing script or data source, if visible.

Check:

- Every in-text callout resolves to an existing figure/table.
- Every figure/table is called out in text before or near appearance.
- Numbering is gap-free and not duplicated.
- Main-text and SI labels do not collide.
- LaTeX/Markdown references compile without unresolved labels.

### 3. Check text-to-evidence consistency

For each figure/table used to support a substantive claim:

- Match the in-text claim to the exact row, column, panel, model, or plotted quantity.
- Verify direction, magnitude, uncertainty, subgroup, and denominator.
- Check whether text overstates non-significant or imprecise estimates.
- Check whether figure/table notes disclose model specification, N, weights, fixed effects, clustering, and missing-data handling.
- For experimental papers, check ITT vs per-protocol labeling, attrition-by-arm, baseline balance, and CONSORT/sample-flow consistency.

Do not infer exact values by eyeballing a plot unless the figure encodes labeled values. If source data are unavailable, write `VISUAL READ ONLY - AUTHOR VERIFY`.

### 4. Audit captions and notes

Captions and table notes should let a reader understand the evidence without hunting:

- Figure caption states what is plotted, units, sample, uncertainty interval, and panel meanings.
- Table title states the estimand or model family, not only "Results."
- Table notes define dependent variable, treatment/condition coding, omitted categories, controls, fixed effects, clustering, weights, and significance markers.
- All abbreviations are defined on first use.
- All transformations, scales, and index directions are explicit.
- Any data exclusions or subgroup restrictions are named.

For conjoint, list-experiment, topic-modeling, LLM-classification, and OCR studies, invoke or recommend the relevant sibling skill when table/figure interpretation depends on method-specific standards.

### 5. Check accessibility and production quality

Flag:

- Color palettes not interpretable in grayscale or by color-blind readers.
- Low-resolution or rasterized text in vector outputs.
- Axis labels too small or missing units.
- Legends that obscure data or use ambiguous labels.
- Inconsistent decimal precision.
- Overcrowded tables that should move to SI.
- Missing alt text when the target venue requires it.
- Non-reproducible manual edits that are not documented.

### 6. Audit SI and replication linkage

Check whether:

- Main-text claims that point to SI land on the correct appendix/table/figure.
- SI numbering and captions are internally consistent.
- Each main figure/table can be traced to a script or documented manual step.
- Replication README maps outputs to scripts and data files.
- Figure/table source data are archived or clearly restricted.

## Output

Produce a `Figure and Table Audit Report`:

```
# Figure and Table Audit Report

Scope:
Inputs checked:
Build/source status:
Summary: <N blocking, N recommended, N minor, N author-verification>

## Inventory
| ID | Path/location | Caption/title | First callout | Source/script |

## Blocking Issues
| Location | Figure/table | Issue | Evidence | Fix |

## Recommended Fixes
| Location | Figure/table | Issue | Fix |

## Minor / Production Issues
| Figure/table | Issue | Fix |

## Author Verification Needed
| Figure/table | Why verification is needed |

## Readiness Checklist
| Dimension | PASS/FAIL/PARTIAL/NA | Notes |
```

Severity:

- **Blocking:** missing figure/table, wrong referenced value, denominator mismatch, unresolved label, table contradicts text, missing sample-flow evidence for experimental paper, or non-reproducible main result output.
- **Recommended:** incomplete notes, unclear captions, missing units, missing source script, accessibility problem, imprecise uncertainty reporting.
- **Minor:** style, spacing, decimal precision, typography, cosmetic consistency.

## Quality checks

- [ ] Figure/table inventory was built before findings were listed.
- [ ] Every substantive text-to-table finding names the row/column/panel/model checked.
- [ ] Visual-only readings are flagged for author verification unless exact values are labeled.
- [ ] Captions and notes were checked for sample, units, uncertainty, and model details.
- [ ] SI and replication links were checked when files were available.
- [ ] Method-specific figures/tables triggered the relevant sibling skill when needed.
