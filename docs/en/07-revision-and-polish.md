# 07 - Revision and Polish

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  Revision is the key leap from "readable" to "submit-ready." CoPaper.AI's
  multi-agent architecture natively supports a tiered revision workflow of
  structural editing → line-by-line polishing → independent review, with
  version tracking at every step.
-->

> **Revision is the most time-consuming part of academic writing.** Going from a draft that is "readable" to one that is "ready to submit" traditionally requires 8–10 hours of repeated polishing. AI-agent multi-agent systems can systematise and audit-trail this process.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the "Skills list" below gives per-method details (with selected upstream links) and complements this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [⭐ `48` chinese-de-aigc](../../skills/48-copaper-ai-chinese-de-aigc/) | Chinese de-AIGC (CNKI / Wanfang / Turnitin-CN) | De-AI Chinese papers; respond to domestic plagiarism checks |
| [`49` humanize-chinese](../../skills/49-voidborne-d-humanize-chinese/) | Detect and humanise AI-generated Chinese | Polish Chinese paragraphs to remove machine tone |
| [`44` humanizer_academic](../../skills/44-matsuikentaro1-humanizer_academic/) | De-AI medical / academic manuscripts (23 patterns) | Remove AI traces from English academic manuscripts |
| [`45` deslop](../../skills/45-stephenturner-skill-deslop/) | Remove AI-writing clichés (5-dimensional scoring) | Quantify and remove AI boilerplate |
| [`46` stop-slop](../../skills/46-hardikpandya-stop-slop/) | 3-layer AI-trace detection and rewrite | Detect → rewrite → recheck closed loop |
| [`47` avoid-ai-writing](../../skills/47-conorbronsdon-avoid-ai-writing/) | Audit → rewrite → re-audit (leaves an edit trail) | Compliant polishing that preserves modification history |
| [`38` academic-proofreader](../../skills/38-peternka-academic-proofreader/) | Academic proofreading | Grammar / spelling / formatting final pass |

---

## Skills List

### academic-writing-refiner (Academic-Paper Polishing)

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | Section-by-section polishing to top-conference standards (NeurIPS, ICML, ACL) |
| **Highlight** | You can feed a single section rather than the whole paper |
| **Best for** | Although the standards skew CS, the writing logic transfers: concise, precise, no filler |
| **Install** | `clawhub install academic-writing-refiner` |

### copy-edit-master (Systematic Paper Revision)

| Attribute | Description |
|------|------|
| **Source** | Open-source academic community project |
| **Architecture** | 3 sub-agents in a multi-agent system |
| **Principle** | The revision methodology is written into SKILL.md; the underlying reference standards (Strunk & White style rules, McCloskey's principles of academic writing) are **encoded into the skill** |

**Detailed workflow**:

```
Input: copy-edit papers/draft.md
  ↓
Auto-detect document type:
  → general academic paper → 2-stage flow
  → theoretical paper (with theorems / formal models) → 5-stage flow
  ↓
Stage 1: structure-editor
  - Global view, ultra-think mode
  - Adjust the paper's overall logic and structure
  ↓
Stage 2: line-editor
  - Section-by-section fine-grained work
  - Uses Sonnet to control cost
  ↓
quality-reviewer
  - Independent review to avoid "feel-good" bias
  - Maximum 2 iterations per stage; otherwise escalated to human
  ↓
Output: revised paper + stage reports + git checkpoints
```

**Safety mechanisms**:
- Automatic backups (`.backup`) + a `git commit` after each stage + stage reports
- The 3 revision agents will not automatically handle: re-positioning the research contribution, declaring data sources, asserting statistical significance — those are left to humans
- After 2 failed iterations, the system provides an explicit 3-option decision for the human

### introduction-writer (Four-Agent Introduction System)

| Attribute | Description |
|------|------|
| **Source** | Open-source academic community project (goyal-intro-writer) |
| **Architecture** | 4 distinct roles, each with its own responsibilities |

| Role | Function |
|------|------|
| `intro-strategist` | Analyses the full paper and devises a writing strategy |
| `intro-drafter` | Drafts the introduction following Keith Head's formula |
| `intro-reviewer` | Independently scores and flags unclear contribution claims |
| `intro-reviser` | Targets identified issues without breaking already-passed parts |

> **Why split roles?** Only when the reviewer and the drafter are independent does a real quality loop emerge. If the same agent writes and reviews, it tends to consider its own work correct by default.

### AI-research-feedback (Economics Paper Feedback)

| Attribute | Description |
|------|------|
| **Source** | [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) |
| **Function** | Pre-submission review; designed specifically for economics papers |
| **Checks** | Clarity of contribution, credibility of identification strategy, over-claimed causal claims, unsupported assertions |
| **Journal support** | Top-5 economics journals + top finance journals |

### revision-guard (Defence Against Over-Editing and Homogenisation)

| Attribute | Description |
|------|------|
| **Source** | [ShiyanW/ai-revision-guard](https://github.com/ShiyanW/ai-revision-guard) |
| **Function** | Prevents AI from making things worse — limits the number of revision rounds, detects homogenisation, protects the author's voice |
| **Install** | `git clone https://github.com/ShiyanW/ai-revision-guard.git ~/.claude/skills/revision-guard` |

**Problem it solves**:

The AI always finds room for "improvement" and the user iterates endlessly, ending up worse off — Liz Fosslien calls this "Frankenstein-ed slop." Studies show LLM edits are 3× as many as human edits and arguments drift toward neutral 70% of the time (CHI 2025; Georgetown 2025).

**Workflow**:

```
Step 0: Anchor — lock the content the user is satisfied with (not the draft; the version the user confirmed)
Step 1: Categorise — structure / substance / language / formatting / wholesale rewrite, each with explicit boundaries
Step 2: Execute — minimal effective change, 15 forbidden AI replacement patterns
Step 3: Report — self-evaluate: substantive improvement / fine-tune / marginal (marginal → recommend stopping)
Step 4: Cap — maximum 2 rounds per section; the 3rd round triggers a warning
Step 5: Detect — a 7-item homogenisation checklist; 2+ items trigger a warning and offer rollback
Step 5b: Cross-validate (optional) — send pre- and post-revision text to Codex/GPT for independent judgement
```

**Highlights**:
- 8 domain presets (economics, law, medicine, humanities, STEM, psychology, political science, education) automatically lock in core academic judgements
- Locking protects voice but does not protect factual errors — if the lock region contains an error, the system flags it actively
- Ships with `scripts/diff-check.py` that automatically detects homogenisation signals (word-count inflation, first-person disappearance, hedge-word increase, etc.)
- Research backing: 8 academic sources (CHI 2025, Georgetown 2025, Xie & Xie 2026, etc.)

### humanizer_academic

| Attribute | Description |
|------|------|
| **Source** | [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) |
| **Function** | Detects and removes 23 patterns of AI-writing traces in academic papers; reduces AIGC-detection scores |
| **Install** | `git clone https://github.com/matsuikentaro1/humanizer_academic.git ~/.claude/skills/humanizer_academic` |

**Problem it solves**:

AI-generated text has statistically detectable patterns — "LLMs use statistical algorithms to guess the next most likely word, which converges toward the broadest statistically-most-probable outcome" (Wikipedia). This causes academic papers to show patterns of exaggerated importance, hollow transitions, em-dash overuse, and artificial three-item lists that are easily flagged by AIGC detectors.

**23 detection patterns**:

- **Content patterns (6)**: importance exaggeration, prominence claims, shallow analysis, promotional language, vague attribution, formulaic problem statements
- **Language patterns (6)**: AI-preferred vocabulary ("pivotal"/"landscape"/"crucial"), avoidance of copular verbs, negative-coordinated parallelism ("not only…but also"), three-item lists, synonym rotation, false ranges
- **Style patterns (3)**: zero tolerance for em-dashes, title-case norms, curly-quote markers
- **Filler and hedging (3)**: redundant phrases ("in order to"→"to"), over-hedging, generalised conclusions
- **Word choice (5)**: unnatural phrase substitution, forced compression of expressions, insufficient hedging adjustment

**Highlights**:
- Examples drawn from cardiovascular research (EMPA-REG OUTCOME trial), well-suited to medicine / natural science
- Preserves legitimate academic transitions ("Notably", "Furthermore")
- Adapted from Wikipedia's "Signs of AI writing" guide

### skill-deslop

| Attribute | Description |
|------|------|
| **Source** | [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) |
| **Function** | A de-AI tool designed for scientific writing; respects disciplinary conventions (e.g. passive voice in the methods section) |
| **Use** | Just say "make this sound human" or use the 5-dimensional scoring rubric |

**Core highlights**:
- Intelligently distinguishes "legitimate scientific-writing conventions" from "AI generation traces" — will not damage the methods section's passive voice or domain-specific terminology
- 5-dimensional scoring rubric: Directness, Rhythm, Trust, Authenticity, Density
- Targets hollow transitions, repeated sentence patterns, false hedging, artificial enthusiasm, theatrical drama

### stop-slop (Generic De-AI)

| Attribute | Description |
|------|------|
| **Source** | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) |
| **Function** | Removes AI-writing characteristics from prose; 3-layer detection + 5-dimensional scoring |
| **Compatibility** | Claude Code, Claude Projects, custom instructions, API integration |

**3-layer detection**:
1. **Forbidden phrases**: throat-clearing openers, emphasis crutches, business jargon, vague statements, meta-commentary
2. **Structural tropes**: binary contrasts, negative lists, dramatic fragmentation, rhetorical setup, false agency, narrator voice, passive constructions
3. **Sentence-level rules**: forbid Wh-openers, em-dashes, broken fragments; require active voice

**Scoring**: each dimension is 1–10, total <35/50 suggests rewriting.

### humanize-chinese (Chinese Academic AI-Detection + Rewrite: Skill + CLI dual form)

| Attribute | Description |
|------|------|
| **Source** | voidborne-d/humanize-chinese (local vendor snapshot; upstream URL did not pass the 2026-05-31 outbound-link sweep) |
| **Form** | **Provides both SKILL.md and a standalone Python CLI/library** — the repo root contains SKILL.md (with frontmatter, topics tagged `claude-code-skill`), directly loadable inside Claude Code / OpenClaw / Hermes and similar agents; also a zero-third-party-dependency Python library that can be `pip install`-ed and run in any pipeline / CI / server for batch jobs. This entry focuses on the CLI/library form; agent-internal usage can refer to the chinese-de-aigc workflow positioning |
| **Function** | Chinese AI-text detection and rewriting: 17 detection features + 7 style rewriters (academic / novel / blog / casual / Xiaohongshu / WeChat / literary), tuned on CNKI / Wanfang / VIP / Turnitin Chinese-edition benchmarks |
| **Install** | `pip install humanize-chinese` or use the local copy in this repo [`skills/49`](../../skills/49-voidborne-d-humanize-chinese/) |
| **License** | **MIT (Non-Commercial)** — non-standard modified MIT, **commercial use explicitly prohibited** (no SaaS / paid API / integration into commercial products / paid content-rewriting services). Personal use, academic research, educational use, and non-commercial derivative open-source projects are allowed. Commercial downstream use requires separate authorisation from the author; it cannot be used under standard MIT terms |

**Comparison with chinese-de-aigc / humanizer_academic (focused on the CLI/library form's complementarity)**:

| Dimension | chinese-de-aigc | humanizer_academic | humanize-chinese (CLI/library form) |
|------|------------------|--------------------|-------------------------------|
| Primary form | Markdown SKILL.md (inside the agent) | Markdown SKILL.md (inside the agent) | Python CLI + library (pipeline-callable, also ships SKILL.md) |
| Language | Chinese academic | English academic | Chinese academic (incl. novel / blog / general) |
| Detection dimensions | 17 categories (agent self-check) | 23 categories (agent self-check) | 17 categories (programmatic scoring, logistic-regression ensemble) |
| Rewrite form | Agent five-step workflow | Agent pattern rewrite | 7 style rewriters, rule-based + best-of-n sampling, reproducible (seed=42) |
| Long-form support | General | General | Auto-switch to long-form LR for ≥1500 chars; paragraph-level features (intra-paragraph sentence-length CV, paragraph-length CV, cross-paragraph 3-gram repetition) |

**Core highlights (v5 paragraph-level specialisation)**:

- **Paragraph-level signals**: intra-paragraph sentence-length CV, paragraph-length CV, cross-paragraph 3-gram repetition. LR holdout 0.897 → 0.926
- **HC3 100 short-Q&A benchmark**: 95% correct separation; long-form average drop -55 / short samples -63
- **Reproducible**: default `--best-of-n 10 --seed 42`; scene-aware detector `--scene academic / novel / blog / news / auto`

**Usage recommendations**:

- Chinese paper batch processing (CI / server, outside Claude Code) → humanize-chinese CLI
- Agent-internal interactive rewriting → chinese-de-aigc Skill (or humanize-chinese's SKILL.md)
- Bilingual Chinese-English papers → humanize-chinese (Chinese sections) + humanizer_academic (English sections)
- Commercial use → humanize-chinese is NOT allowed (license restriction); use chinese-de-aigc / humanizer_academic / stop-slop (standard MIT)

---

## From Skill to Custom-Agent Systems

From user to designer, there are three levels:

```
Level 1: Tool (Claude Code's built-in read/write/search capabilities)
    ↓
Level 2: Skill (you write the operating manual; the agent executes per the manual)
    ↓
Level 3: Custom Agent (you define specialised sub-agents with independent identities, tool sets, and model choices)
```

**SKILL.md authoring principles**:
- Steps must be **executable**: write "apply Strunk & White Rule 13", not "polish appropriately"
- Outputs must be **verifiable**: write "produce stage-1-report.md", not "improve quality"
- Boundaries must be **clear**: which edits the agent does, which are left to humans

**Growth path**:
> Start with someone else's skill → record the tasks you repeat → write them as SKILL.md → split into multi-agent systems

---

## Practical Advice

1. **Don't skip the structure-editor**: many people rush to line-by-line polishing, but if the structure is broken, beautiful sentences can't save it.
2. **Use git checkpoints**: copy-edit-master's per-stage git commits let you roll back at any time; let the AI edit boldly.
3. **Pre-submission must-do**: run `AI-research-feedback` for a pre-review; see what the AI-simulated reviewers raise — these are likely the same points real reviewers will press.

---

[← Previous chapter](06-paper-writing.md) | [Next chapter: 08 - Citation Management and Typesetting →](08-citation-management-and-typesetting.md)