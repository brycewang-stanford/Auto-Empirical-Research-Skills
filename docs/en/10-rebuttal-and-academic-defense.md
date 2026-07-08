# 10 - Rebuttal and Academic Defence

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  Reviewer reports often request supplementary analyses — "add a placebo
  test," "try a different instrumental variable." CoPaper.AI's methodology
  skills let you trigger a full supplementary-analysis pipeline with one
  sentence, letting you respond to reviewer demands quickly and shortening
  the R&R cycle substantially.
-->

> **The core strategy for rebuttal: respond point by point, with reasoning, and a courteous tone.** AI agents can help you draft a response framework and quickly run additional analyses requested by reviewers, but the strategy and tone of the response are yours to control.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the "Skills list" below gives per-method details (with selected upstream links) and complements this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [`24` academic-research-skills](../../skills/24-Imbad0202-academic-research-skills/) | 5-reviewer multi-perspective paper review | Pre-submission reviewer rehearsal; fill gaps before submission |
| [⭐ `50` AER-skills](../../skills/50-brycewang-aer-skills/) | Top-5 submission stack: identification → robustness → R&R | Systematic R&R response drafting |
| [`16` clo-author](../../skills/16-hsantanna88-clo-author/) | Multi-agent data analysis, including submit / review / talk sub-skills | Submission, response, and defence-talk material in one place |
| [`42` ARIS](../../skills/42-wanshuiyin-ARIS/) | Autonomous end-to-end research agent (104 skills; submission / presentation) | Generate cover letter, response letter, and presentation material |
| [`12` claude-code-my-workflow](../../skills/12-pedrohcgs-claude-code-my-workflow/) | Commit → PR → merge research workflow | Manage R&R revisions and version history |
| [`13` MixtapeTools](../../skills/13-scunning1975-MixtapeTools/) | Cunningham's causal-inference toolkit and lecture notes | Lecture notes and figures for defence / presentations |

---

## Skills List

### review-response (Reviewer Response)

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Respond point by point to reviewer comments |
| **Workflow** | 1. Parse reviewer comments and extract each specific demand<br>2. Categorise each comment (data issue / method issue / writing issue / interpretation issue)<br>3. Generate a response framework, including modification notes and new content<br>4. Flag places that require supplementary analysis |

### reviewer-response-drafting

| Attribute | Description |
|------|------|
| **Source** | [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) |
| **Function** | Reviewer-response drafting designed for statistical researchers |
| **Highlight** | Understands the nuances of statistical methodology and can produce professional responses to methodological critiques |

### paper-self-review (Pre-Submission Self-Review)

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Simulates a reviewer perspective to surface problems |
| **Scenario** | Run a self-review before submission; prepare likely responses in advance |

### AI-research-feedback (Economics Paper Pre-Review)

| Attribute | Description |
|------|------|
| **Source** | [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) |
| **Function** | 2-agent simulation of top-journal review |
| **Support** | AER, QJE, JPE, Econometrica, REStud, JF, JFE, RFS |
| **Checks** | Contribution assessment, identification strategy, over-claimed causal claims, unsupported assertions |

---

## Defence Presentation

### paper-slide-deck (Paper-to-Slides)

| Attribute | Description |
|------|------|
| **Source** | [luwill/research-skills](https://github.com/luwill/research-skills) |
| **Function** | Automatic conversion of paper to slides |
| **Highlight** | Auto-detect figures, 17 visual styles, AI image generation (Gemini API), PPTX/PDF export |
| **Install** | `git clone https://github.com/luwill/research-skills.git && cp -r research-skills/paper-slide-deck ~/.claude/skills/` |

### presentation-skills (Academic Presentation)

| Attribute | Description |
|------|------|
| **Source** | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Function** | Academic-presentation skill, helping you organise presentation content |

### claude-office-skills (PPT Generation)

| Attribute | Description |
|------|------|
| **Source** | [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) |
| **Stars** | 251 |
| **Function** | Direct PPTX file generation |

---

## Reviewer-Response Template

A good reviewer response usually follows this structure:

```markdown
## Response to Reviewer X

We thank the reviewer for the thoughtful and constructive comments. 
Below we address each point in detail.

### Comment 1: [Brief statement of the reviewer's comment]

**Response:** [Your response]

**Changes made:** [What exactly was changed, and where in the paper]

---

### Comment 2: ...
```

### Key Strategies

1. **Always thank first** — even when the reviewer is wrong.
2. **Respond point by point** — do not combine replies; respond to each comment separately.
3. **Distinguish "what you did" from "why you did it"** — reviewers want more than the changes; they want the reasoning.
4. **Embed supplementary analyses in the response** — new regression tables and robustness checks go directly into the response document.
5. **Use skills to quickly run additional analyses** — when the reviewer says "add a placebo test," use CoPaper.AI's robustness-check skill to produce it with one sentence.

---

## Practical Advice

1. **Run two simulated reviews before submission**: first `paper-self-review` for a general check, then `AI-research-feedback` for an economics-specific check. Together they cover most of what reviewers will raise.
2. **R&R cycle efficiency**: the most time-consuming part of a reviewer response is usually "running supplementary analyses." If your analysis pipeline is already skill-ified, adding a new robustness check is just one sentence.
3. **Don't rebuild the defence PPT from scratch**: use `paper-slide-deck` to auto-generate slides from the paper, then manually adjust the emphasis and pacing.

---

[← Previous chapter](09-replication-and-reproducible-research.md) | [Back to README →](../../README.md)