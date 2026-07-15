---
name: paper-slide-deck
description: Generate professional slide deck images from academic papers and content. Creates comprehensive outlines with style instructions, auto-detects figures from PDFs, then generates individual slide images. Use when user asks to "create slides", "make a presentation", "generate deck", or "slide deck" for papers.
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/luwill/research-skills
  项目名称: research-skills
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Paper Slide Deck Generator

Transform academic papers and content into professional slide deck images with automatic figure extraction.

## Usage

```bash
/paper-slide-deck path/to/paper.pdf
/paper-slide-deck path/to/paper.pdf --style academic-paper
/paper-slide-deck path/to/content.md --style sketch-notes
/paper-slide-deck path/to/content.md --audience executives
/paper-slide-deck path/to/content.md --lang zh
/paper-slide-deck path/to/content.md --slides 10
/paper-slide-deck path/to/content.md --outline-only
/paper-slide-deck  # Then paste content
```

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/generate-slides.py` | Generate AI slides via Gemini API (Python) |
| `scripts/merge-to-pptx.ts` | Merge slides into PowerPoint |
| `scripts/merge-to-pdf.ts` | Merge slides into PDF |
| `scripts/detect-figures.ts` | Auto-detect figures/tables in PDF |
| `scripts/extract-figure.ts` | Extract figure from PDF page (uses PyMuPDF fallback) |
| `scripts/apply-template.ts` | Apply figure container template |

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style (see Style Gallery) |
| `--audience <type>` | Target audience: beginners, intermediate, experts, executives, general |
| `--lang <code>` | Output language (en, zh, ja, etc.) |
| `--slides <number>` | Target slide count |
| `--outline-only` | Generate outline only, skip image generation |

## Style Gallery

| Style | Description | Best For |
|-------|-------------|----------|
| `academic-paper` | Clean professional, precise charts | Conference talks, thesis defense |
| `blueprint` (Default) | Technical schematics, grid texture | Architecture, system design |
| `chalkboard` | Black chalkboard, colorful chalk | Education, tutorials, classroom |
| `notion` | SaaS dashboard, card-based layouts | Product demos, SaaS, B2B |
| `bold-editorial` | Magazine cover, bold typography, dark | Product launches, keynotes |
| `corporate` | Navy/gold, structured layouts | Investor decks, proposals |
| `dark-atmospheric` | Cinematic dark mode, glowing accents | Entertainment, gaming |
| `editorial-infographic` | Magazine explainers, flat illustrations | Tech explainers, research |
| `fantasy-animation` | Ghibli/Disney style, hand-drawn | Educational, storytelling |
| `intuition-machine` | Technical briefing, bilingual labels | Technical docs, academic |
| `minimal` | Ultra-clean, maximum whitespace | Executive briefings, premium |
| `pixel-art` | Retro 8-bit, chunky pixels | Gaming, developer talks |
| `scientific` | Academic diagrams, precise labeling | Biology, chemistry, medical |
| `sketch-notes` | Hand-drawn, warm & friendly | Educational, tutorials |
| `vector-illustration` | Flat vector, retro & cute | Creative, children's content |
| `vintage` | Aged-paper, historical styling | Historical, heritage, biography |
| `watercolor` | Hand-painted textures, natural warmth | Lifestyle, wellness, travel |

## Auto Style Selection

| Content Signals | Selected Style |
|-----------------|----------------|
| paper, thesis, defense, conference, ieee, acm, icml, neurips, cvpr, acl, aaai, iclr | `academic-paper` |
| tutorial, learn, education, guide, intro, beginner | `sketch-notes` |
| classroom, teaching, school, chalkboard, blackboard | `chalkboard` |
| architecture, system, data, analysis, technical | `blueprint` |
| creative, children, kids, cute, illustration | `vector-illustration` |
| briefing, bilingual, infographic, concept | `intuition-machine` |
| executive, minimal, clean, simple, elegant | `minimal` |
| saas, product, dashboard, metrics, productivity | `notion` |
| investor, quarterly, business, corporate, proposal | `corporate` |
| launch, marketing, keynote, bold, impact, magazine | `bold-editorial` |
| entertainment, music, gaming, creative, atmospheric | `dark-atmospheric` |
| explainer, journalism, science communication | `editorial-infographic` |
| story, fantasy, animation, magical, whimsical | `fantasy-animation` |
| gaming, retro, pixel, developer, nostalgia | `pixel-art` |
| biology, chemistry, medical, pathway, scientific | `scientific` |
| history, heritage, vintage, expedition, historical | `vintage` |
| lifestyle, wellness, travel, artistic, natural | `watercolor` |
| Default | `blueprint` |

## Layout Gallery

Optional layout hints for individual slides. Specify in outline's `// LAYOUT` section.

### Slide-Specific Layouts

| Layout | Description | Best For |
|--------|-------------|----------|
| `title-hero` | Large centered title + subtitle | Cover slides, section breaks |
| `quote-callout` | Featured quote with attribution | Testimonials, key insights |
| `key-stat` | Single large number as focal point | Impact statistics, metrics |
| `split-screen` | Half image, half text | Feature highlights, comparisons |
| `icon-grid` | Grid of icons with labels | Features, capabilities, benefits |
| `two-columns` | Content in balanced columns | Paired information, dual points |
| `three-columns` | Content in three columns | Triple comparisons, categories |
| `image-caption` | Full-bleed image + text overlay | Visual storytelling, emotional |
| `agenda` | Numbered list with highlights | Session overview, roadmap |
| `bullet-list` | Structured bullet points | Simple content, lists |

### Infographic-Derived Layouts

| Layout | Description | Best For |
|--------|-------------|----------|
| `linear-progression` | Sequential flow left-to-right | Timelines, step-by-step |
| `binary-comparison` | Side-by-side A vs B | Before/after, pros-cons |
| `comparison-matrix` | Multi-factor grid | Feature comparisons |
| `hierarchical-layers` | Pyramid or stacked levels | Priority, importance |
| `hub-spoke` | Central node with radiating items | Concept maps, ecosystems |
| `bento-grid` | Varied-size tiles | Overview, summary |
| `funnel` | Narrowing stages | Conversion, filtering |
| `dashboard` | Metrics with charts/numbers | KPIs, data display |
| `venn-diagram` | Overlapping circles | Relationships, intersections |
| `circular-flow` | Continuous cycle | Recurring processes |
| `winding-roadmap` | Curved path with milestones | Journey, timeline |
| `tree-branching` | Parent-child hierarchy | Org charts, taxonomies |
| `iceberg` | Visible vs hidden layers | Surface vs depth |
| `bridge` | Gap with connection | Problem-solution |

### Academic-Specific Layouts

| Layout | Description | Best For |
|--------|-------------|----------|
| `paper-title` | Title, authors, affiliations, venue | Conference paper cover |
| `outline-agenda` | Numbered section list with highlights | Talk structure overview |
| `methods-diagram` | Central architecture/pipeline diagram | Methods, system design |
| `results-chart` | Chart area + data annotations | Quantitative results |
| `equation-focus` | Centered equation + variable definitions | Mathematical derivations |
| `qualitative-grid` | 2x2 or 3x2 image comparison grid | Visual results, ablations |
| `references-list` | Numbered citation list | Key references slide |
| `contributions` | Numbered contribution points | Contributions summary |

**Usage**: Add `Layout: <name>` in slide's `// LAYOUT` section to guide visual composition.

## Design Philosophy

This deck is designed for **reading and sharing**, not live presentation:
- Each slide must be **self-explanatory** without verbal commentary
- Structure content for **logical flow** when scrolling
- Include **all necessary context** within each slide
- Optimize for **social media sharing** and offline reading

## File Management

### Output Directory

Each session creates an independent directory named by content slug:

```
slide-deck/{topic-slug}/
├── source-{slug}.{ext}    # Source files (text, images, etc.)
├── outline.md
├── outline-{style}.md     # Style variant outlines
├── prompts/
│   └── 01-slide-cover.md, 02-slide-{slug}.md, ...
├── 01-slide-cover.png, 02-slide-{slug}.png, ...
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

**Slug Generation**:
1. Extract main topic from content (2-4 words, kebab-case)
2. Example: "Introduction to Machine Learning" → `intro-machine-learning`

### Conflict Resolution

If `slide-deck/{topic-slug}/` already exists:
- Append timestamp: `{topic-slug}-YYYYMMDD-HHMMSS`
- Example: `intro-ml` exists → `intro-ml-20260118-143052`

### Source Files

Copy all sources with naming `source-{slug}.{ext}`:
- `source-article.md` (main text content)
- `source-diagram.png` (image from conversation)
- `source-data.xlsx` (additional file)

Multiple sources supported: text, images, files from conversation.

## Workflow

### Step 1: Analyze Content

1. Save source content (if pasted, save as `source.md`)
2. Follow `references/analysis-framework.md` for deep content analysis
3. Determine style (use `--style` or auto-select from signals)
4. Detect languages (source vs. user preference)
5. Plan slide count (`--slides` or dynamic)
6. **For academic papers (PDF with figures)**: Run automatic figure detection:
   ```bash
   npx -y bun ${SKILL_DIR}/scripts/detect-figures.ts --pdf source-paper.pdf --output figures.json
   ```
   This outputs a JSON file with all detected figures/tables, their page numbers, and captions.

### Step 2: Generate Outline Variants

1. Generate 3 style variant outlines based on content analysis
2. Follow `references/outline-template.md` for structure
3. **Auto-populate IMAGE_SOURCE** for academic papers:
   - Read `figures.json` from Step 1
   - Map figures to slides using rules in `references/analysis-framework.md` Section 8
   - Automatically add `// IMAGE_SOURCE` blocks to appropriate slides:
     - Architecture/pipeline figures → Methods slides (`Source: extract`)
     - Results tables → Quantitative results slides (`Source: extract`)
     - Comparison images → Qualitative results slides (`Source: extract`)
     - Conceptual/simple diagrams → Leave for AI generation (`Source: generate` or omit)
4. Save as `outline-{style}.md` for each variant

### Step 3: User Confirmation

**Single AskUserQuestion with all applicable options:**

| Question | When to Ask |
|----------|-------------|
| Style variant | Always (3 options + custom) |
| Language | Only if source ≠ user language |

After selection:
- Copy selected `outline-{style}.md` to `outline.md`
- Regenerate in different language if requested
- User may edit `outline.md` for fine-tuning

If `--outline-only`, stop here.

### Step 4: Generate Prompts

1. Read `references/base-prompt.md`
2. Combine with style instructions from outline
3. Add slide-specific content
4. If `Layout:` specified in outline, include layout guidance in prompt:
   - Reference layout characteristics for image composition
   - Example: `Layout: hub-spoke` → "Central concept in middle with related items radiating outward"
5. Save to `prompts/` directory

### Step 5: Image Generation Method Selection

**Before generating images**, ask user to choose generation method:

**Use AskUserQuestion** with options:

| Option | Label | Description |
|--------|-------|-------------|
| 1 | **Gemini API (Recommended)** | Official Google API via Python. Requires GOOGLE_API_KEY env var. |
| 2 | **Gemini Web (Browser-based)** | ⚠️ Uses reverse-engineered web API. No API key needed but may break. |

**Based on selection:**

#### Option 1: Gemini API (Python)

1. **Verify API key**: Check `GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variable
2. **Run generation script**:
   ```bash
   python ${SKILL_DIR}/scripts/generate-slides.py <slide-deck-dir> --model gemini-3-pro-image-preview
   ```

**Script Features**:
- Auto-installs `google-genai` package if missing
- Retry logic with exponential backoff (3 retries)
- Skips already-generated slides (> 10KB)
- Supports custom model via `--model` flag
- Outputs to `slides/` subdirectory

**Troubleshooting**:
- If server disconnection errors occur, script auto-retries
- For persistent failures, re-run the script (it skips completed slides)
- Check API quota if many failures occur

#### Option 2: Gemini Web Skill

1. **Consent Check**: Read consent file at:
   - Windows: `$APPDATA/baoyu-skills/gemini-web/consent.json`
   - macOS: `~/Library/Application Support/baoyu-skills/gemini-web/consent.json`
   - Linux: `~/.local/share/baoyu-skills/gemini-web/consent.json`

2. **If no consent or version mismatch**, display disclaimer and ask:
   ```
   ⚠️ DISCLAIMER: This uses a reverse-engineered Gemini Web API (NOT official).
   Risks: May break anytime, no support, possible account risk.
   ```

3. **For each slide**, run:
   ```bash
   npx -y bun ${GEMINI_WEB_SKILL_DIR}/scripts/main.ts \
     --promptfiles prompts/01-slide-cover.md \
     --image 01-slide-cover.png \
     --sessionId slides-{topic-slug}-{timestamp}
   ```

   Where `GEMINI_WEB_SKILL_DIR` = path to `baoyu-danger-gemini-web` skill directory.

4. **Proxy support**: If user is in restricted network, prepend:
   ```bash
   HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890
   ```

### Step 5.5: Process IMAGE_SOURCE (Automatic Figure Extraction)

For academic presentations, IMAGE_SOURCE metadata was auto-populated in Step 2 based on figure detection from Step 1.

**Automatic Execution**:

1. **Parse outline** to identify slides with `Source: extract`
2. **Create figures directory**: `mkdir -p figures`
3. **For each extract slide**, automatically:
   - Read the Figure number, Page, and Caption from metadata
   - Run figure extraction script:
     ```bash
     npx -y bun ${SKILL_DIR}/scripts/extract-figure.ts \
       --pdf source-paper.pdf \
       --page <page-number> \
       --output figures/figure-<N>.png
     ```
   - Run template application script:
     ```bash
     npx -y bun ${SKILL_DIR}/scripts/apply-template.ts \
       --figure figures/figure-<N>.png \
       --title "<slide-headline>" \
       --caption "Figure <N>: <caption-text>" \
       --output <NN>-slide-<slug>.png
     ```
   - Report: "Extracted: Figure N → slide NN"

4. **For slides with `Source: generate`** (or no IMAGE_SOURCE):
   - Proceed to Step 6 for AI generation

**Note**: Source PDF must be saved as `source-paper.pdf` in output directory.

**Troubleshooting**:
- If figure detection missed a figure: manually add `// IMAGE_SOURCE` block to outline
- If wrong figure mapped: edit the `Figure:` and `Page:` values in outline
- If extraction fails: check PDF page number (1-indexed)

**PyMuPDF Fallback for Page Extraction**:
If `extract-figure.ts` fails with "Image or Canvas expected" error (common with complex PDFs), use PyMuPDF:
```python
import fitz
doc = fitz.open("source-paper.pdf")
page = doc[page_num - 1]  # 0-indexed
mat = fitz.Matrix(3, 3)  # 3x scale for high resolution
pix = page.get_pixmap(matrix=mat)
pix.save(f"extracted/page-{page_num}.png")
```
Then apply template using `apply-template.ts`.

### Step 6: Generate Images

1. Use selected method from Step 5
2. **Skip slides already processed in Step 5.5** (those with `Source: extract`)
3. Generate session ID: `slides-{topic-slug}-{timestamp}`
4. Generate each remaining slide with same session ID
5. Report progress: "Generated X/N"
6. Auto-retry once on generation failure

### Step 7: Merge to PPTX and PDF

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pptx.ts <slide-deck-dir>
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <slide-deck-dir>
```

### Step 8: Output Summary

```
Slide Deck Complete!

Topic: [topic]
Style: [style name]
Location: [directory path]
Slides: N total

- 01-slide-cover.png ✓ Cover
- 02-slide-intro.png ✓ Content
- ...
- {NN}-slide-back-cover.png ✓ Back Cover

Outline: outline.md
PPTX: {topic-slug}.pptx
PDF: {topic-slug}.pdf
```

## Slide Modification

See `references/modification-guide.md` for:
- Edit single slide workflow
- Add new slide (with renumbering)
- Delete slide (with renumbering)
- File naming conventions

## Image Generation Dependencies

### Gemini API (Option 1 - Recommended)

Requires:
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variable
- Python 3.8+ with pip
- `google-genai` package (auto-installed by script)

Model: `gemini-3-pro-image-preview` (default)

### Gemini Web Skill (Option 2)

Requires:
- `baoyu-danger-gemini-web` skill installed at `.claude/skills/baoyu-danger-gemini-web`
- Google Chrome browser with logged-in Google account
- User consent for reverse-engineered API disclaimer

### PDF Figure Extraction

Requires:
- **Primary**: `pdfjs-dist` npm package (use legacy build for Node.js)
- **Fallback**: `pymupdf` Python package (more reliable for complex PDFs)
- `canvas` npm package for apply-template.ts

## References

| File | Content |
|------|---------|
| `references/analysis-framework.md` | Deep content analysis for presentations |
| `references/outline-template.md` | Outline structure and STYLE_INSTRUCTIONS format |
| `references/modification-guide.md` | Edit, add, delete slide workflows |
| `references/content-rules.md` | Content and style guidelines |
| `references/base-prompt.md` | Base prompt for image generation |
| `references/figure-container-template.md` | Visual specs for extracted figure containers |
| `references/styles/<style>.md` | Full style specifications |

## Notes

### Image Generation

- **Nano Banana Pro API**: Recommended. Stable, reliable, requires API key
- **Gemini Web**: No API key needed, but uses reverse-engineered API with account risk
- Generation time: 10-30 seconds per slide
- Auto-retry once on generation failure
- Maintain style consistency via session ID

### Content Guidelines

- Use stylized alternatives for sensitive public figures
- Both methods use the same underlying Gemini model for image generation

## Extension Support

Custom styles and configurations via EXTEND.md.

**Check paths** (priority order):
1. `.paper-skills/paper-slide-deck/EXTEND.md` (project)
2. `~/.paper-skills/paper-slide-deck/EXTEND.md` (user)

If found, load before Step 1. Extension content overrides defaults.
