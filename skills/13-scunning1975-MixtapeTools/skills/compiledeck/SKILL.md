---
name: compiledeck
description: Create and compile beautiful Beamer presentations following the Rhetoric of Decks philosophy. Use when making slides, creating decks, or compiling .tex presentation files.
allowed-tools: Bash(pdflatex*), Bash(latexmk*), Bash(ls*), Bash(open*), Bash(python*), Read, Write, Edit, Glob, Grep
argument-hint: "[topic-or-tex-file-path]"
---

# Compile Deck

Create beautiful Beamer presentations. This skill enforces the **Rhetoric of Decks** philosophy through concrete, measurable rules — not aspirational guidance.

## Step 1: Triage

Before touching anything, answer three questions:

**Q1: New deck or editing existing?**
- If editing: Read the `.tex` file first. Understand its palette, structure, and style before changing anything.
- If new: Proceed to Q2.

**Q2: Who is the audience?**
1. **Academic seminar** — sparse, one idea per slide, titles carry the argument
2. **Teaching lecture** — clarity over compression, repetition OK, progressive revelation
3. **Working deck** (coauthors) — more detail OK, document choices, preserve uncertainty
4. **External non-academic** — storytelling, visual impact, minimal jargon

See `domain_patterns.md` in this skill directory for detailed guidance per audience type.

**Q3: What's the tone?**
1. **Professional/Academic** — use the Warm Professional palette (default) or Academic Muted
2. **Colorful/Expressive** — create something new each time. See `palette_reference.md` for inspiration.

---

## Step 2: The Non-Negotiable Rules

These are not guidelines. They are constraints.

### ONE idea per slide
If a slide has two ideas, split it. No exceptions.

### Titles are assertions, not labels
- Bad: "Results"
- Good: "Treatment increased distance by 61 miles on average"
- Bad: "Literature Review"
- Good: "Prior work ignores the supply-side margin"

If someone reads only the slide titles in sequence, they should understand the entire argument.

### Typography minimums
- Body text: 24pt minimum
- Absolute floor (footnotes, source notes): 18pt
- Sans-serif fonts only
- Never justify text — always ragged right

### No bullet lists (usually)
Bullets are a confession that you haven't found the structure. Look for:
- A sequence (use a flow diagram)
- A contrast (use two columns)
- A hierarchy (use size/color differentiation)
- A causal chain (use arrows)

Exception: genuinely parallel items (e.g., a list of axioms in a teaching deck).

### Charts: one message, direct labels
- Every chart communicates ONE finding
- Title states the finding ("Enrollment doubled after 2015"), not the chart type ("Enrollment Over Time")
- Label data directly on the chart — no legends requiring eye movement
- Remove all chartjunk: gridlines, borders, unnecessary axis marks

### White space is confidence, not waste
Empty space on a slide signals that you chose carefully. A full slide signals anxiety.

### Zero compile warnings
Not "try to fix." Zero. See the Compile Loop below.

---

## Step 3: The Preamble

For new decks, use this template. It is extracted from real decks that work.

### Default: Warm Professional Palette (10 colors)

```latex
\documentclass[aspectratio=169,11pt]{beamer}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{xcolor}
\usepackage{ragged2e}
\usepackage{colortbl}
\usepackage{array}
\usepackage{hyperref}
\usepackage{adjustbox}

\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc,
                backgrounds, decorations.pathreplacing, shadows, fadings}
\pgfplotsset{compat=1.18}

% --- Color Palette: Warm Professional ---
\definecolor{DeepNavy}{HTML}{2E4057}
\definecolor{Teal}{HTML}{048A81}
\definecolor{WarmOrange}{HTML}{E85D04}
\definecolor{SoftPurple}{HTML}{9D4EDD}
\definecolor{WarmGray}{HTML}{6C757D}
\definecolor{LightGray}{HTML}{E9ECEF}
\definecolor{Cream}{HTML}{FBF8F1}
\definecolor{DeepRed}{HTML}{D62828}
\definecolor{Gold}{HTML}{D4A03A}
\definecolor{SoftWhite}{HTML}{FAFAFA}

% Beamer colors
\setbeamercolor{normal text}{fg=DeepNavy, bg=SoftWhite}
\setbeamercolor{structure}{fg=DeepNavy}
\setbeamercolor{alerted text}{fg=DeepRed}
\setbeamercolor{example text}{fg=Teal}
\setbeamercolor{frametitle}{fg=DeepNavy, bg=SoftWhite}
\setbeamercolor{title}{fg=DeepNavy}
\setbeamercolor{subtitle}{fg=WarmGray}
\setbeamercolor{block title}{bg=DeepNavy, fg=SoftWhite}
\setbeamercolor{block body}{bg=LightGray, fg=DeepNavy}
\setbeamercolor{itemize item}{fg=WarmOrange}
\setbeamercolor{itemize subitem}{fg=Gold}

% Fonts
\usefonttheme{professionalfonts}
\setbeamerfont{title}{size=\huge, series=\bfseries}
\setbeamerfont{frametitle}{size=\Large, series=\bfseries}

% Strip chrome
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{headline}{}

% Minimal footline
\setbeamertemplate{footline}{%
    \hfill
    \begin{beamercolorbox}[wd=3cm,ht=2.5ex,dp=1ex,right,rightskip=0.6cm]{page number}
        \usebeamercolor[fg]{WarmGray}\scriptsize\insertframenumber
    \end{beamercolorbox}
    \vspace{0.3cm}
}

% Bullets
\setbeamertemplate{itemize item}{\footnotesize\raisebox{0.3ex}{\tikz\fill[WarmOrange] (0,0) circle (0.45ex);}}
\setbeamertemplate{itemize subitem}{\footnotesize\raisebox{0.3ex}{\tikz\fill[Gold] (0,0) circle (0.35ex);}}

% Custom commands
\newcommand{\transitionslide}[2]{%
    {\setbeamercolor{normal text}{fg=SoftWhite,bg=DeepNavy}
    \begin{frame}[plain]\vfill\begin{center}
        {\huge\bfseries\textcolor{Gold}{#1}}\\[0.6cm]
        {\large\textcolor{LightGray}{#2}}
    \end{center}\vfill\end{frame}}
}

\graphicspath{{figures/}}
```

For alternative palettes, see `palette_reference.md` in this skill directory.

---

## Step 4: Slide Architecture Patterns

### Opening slide (first content slide after title)
**NOT** "Motivation" with bullet points. Instead:
- A surprising fact or statistic (big number, centered)
- A puzzle or unanswered question
- A provocative claim that the deck will support

### Transition slides
Use `\transitionslide{Section Title}{Subtitle}` for dark-background section dividers.

### Closing slide
**NOT** "Questions?" or "Thank you." Instead:
- The ONE sentence the audience should remember tomorrow
- Full-bleed dark background with the takeaway centered

### Devil's Advocate slide (academic decks)
Present the strongest objection to your argument, then respond to it. This builds credibility.
Format: "A skeptic would say..." followed by your response.

### TikZ diagram slides
Read `tikz_rules.md` in this skill directory BEFORE creating any TikZ figure. The rules are measurement-based — they prevent text from overlapping arrows, boxes, and other objects.

**Critical rule preview**: Before placing a label between two nodes, CALCULATE the edge-to-edge gap and compare it to the estimated text width. If the text is wider than the gap minus 0.6cm padding, the label WILL collide. Move it above/below or shorten the text.

---

## Step 5: The Compile Loop

After EVERY edit to a .tex file:

### 5a: Compile
```bash
pdflatex -interaction=nonstopmode [file].tex
```

### 5b: Check for fatal errors
```bash
grep "^!" [file].log
```
If any: fix, recompile, repeat.

### 5c: Check for ALL warnings
```bash
grep -cE "Overfull|Underfull" [file].log
```

This must return **0**. For EACH warning:

| Warning | Fix |
|---------|-----|
| Overfull \hbox | Rephrase shorter, use `\adjustbox`, add `@{}` to table columns |
| Underfull \hbox | Rephrase or adjust paragraph breaks |
| Overfull \vbox | Split the slide or reduce `\vspace`, tighten content |
| Underfull \vbox | Add `\vfill` or adjust spacing |

Even 0.5pt overfull must be fixed. Do NOT proceed until the count is 0.

### 5d: Check fonts
```bash
grep -i "font" [file].log | grep -i "warning"
```

### 5e: TikZ verification (Bézier-first workflow)

TikZ errors don't trigger compile warnings. You must catch them yourself. Follow this order — curves first, everything else second:

**Pass 1 — Find and fix all Bézier curves:**
```bash
grep -n "bend" [file].tex
```
For EACH curved arrow found:
1. Calculate max depth: `(chord / 2) × tan(bend_angle / 2)`
2. Add 0.5cm safety margin
3. Check: is any label within the danger zone? Move it if so.
4. Check: does the curve cross any other arrow? Re-route if so.

**Pass 2 — Everything else:**
- Gap calculation: for every label between two nodes, is estimated text width < usable gap?
- Arrow labels: does every one have `above`, `below`, `left`, or `right`?
- No nodes clipped by slide edges
- All arrows pointing to intended targets

**Pass 3 — Open the PDF and visually confirm.**

Full rules and formulas are in `tikz_rules.md`. This verification runs on ALL TikZ figures in the deck, not just the one you just edited.

### 5f: Open the PDF
```bash
open [file].pdf
```

---

## Step 6: The Narrative Arc

Every deck tells a story. The structure depends on context, but the principle is universal:

**Act I — Setup**: Establish the problem or question. Make the audience feel it.
**Act II — Development**: Present evidence, analysis, investigation. Build the logical case.
**Act III — Resolution**: Deliver the insight. State implications. Give the audience something to do or remember.

Within this arc, apply the **Pyramid Principle**: lead with the conclusion, then support it. Academic audiences expect this. Do not build suspense — state the finding, then prove it.

For domain-specific structures, see `domain_patterns.md`.

---

## Step 7: Figure Generation

When a deck needs data visualizations:

1. Write a Python script (`generate_figures.py`) using matplotlib
2. Use the same color palette as the LaTeX deck
3. Save figures as PDF (vector, not raster) to a `figures/` subdirectory
4. Every figure: one message, direct labels, title states the finding
5. Match the deck's background color in `fig.set_facecolor()`
6. **Save the script** alongside the figures — never generate a figure without preserving the code that created it
7. **Boundary Rule applies to figures too**: When placing `ax.text()` near patches (`FancyBboxPatch`, `Circle`, `Rectangle`), compute the patch boundary and verify text has ≥0.4cm clearance. See `tikz_rules.md` Pass 4.
8. **Anchor-Based Centering Rule**: When a container holds multiple text elements (title + math), do NOT use `va='center'` for both at symmetric offsets — multi-line text extends further from its anchor than single-line, creating visual asymmetry. Instead, **anchor outward from center**: upper element uses `va='bottom'` at `center + gap`, lower uses `va='top'` at `center - gap`. See `tikz_rules.md` Pass 4.
9. **Bézier-first for matplotlib arrows**: When labeling curved arrows (`arc3`), compute the actual Bézier curve position using the arc3 control point formula (`cx = mid_x + rad*dy, cy = mid_y - rad*dx`), then offset labels perpendicular to the **computed** curve position. Never guess where curves pass. Use a white-background bbox on labels for readability. See `tikz_rules.md` Pass 4 for the full formula and workflow.

---

## Quick Reference

| Principle | Rule |
|-----------|------|
| Ideas per slide | ONE |
| Title style | Assertion, not label |
| Minimum font | 24pt (18pt floor) |
| Bullets | Avoid — find the structure |
| White space | Confidence, not waste |
| Charts | One message, direct labels |
| Compile target | Zero warnings |
| Opening slide | Puzzle, surprise, or provocation |
| Closing slide | One memorable takeaway |
| TikZ labels | Calculate the gap (see tikz_rules.md) |
| Color palette | 10+ colors, warm by default |
| Narrative | Setup, Development, Resolution |

---

## Supporting Files

All in this skill directory (`~/.claude/skills/compiledeck/`):

- **tikz_rules.md** — Measurement-based TikZ collision prevention rules. READ THIS before creating any TikZ diagram.
- **palette_reference.md** — Four real palettes extracted from existing decks, with a selection guide.
- **domain_patterns.md** — Detailed structural patterns for academic seminars, teaching lectures, and working decks.

## Full Philosophy Reference

For the complete essay behind these principles:
`~/MixtapeTools/presentations/rhetoric_of_decks.md`
`~/MixtapeTools/presentations/rhetoric_of_decks_full_essay.md`

This skill distills those essays into operational rules. You don't need to re-read them — just follow the rules above.
