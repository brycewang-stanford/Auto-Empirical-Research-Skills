---
name: marp-export
description: Export Marp slide markdown files to PDF (default), HTML, PPTX, or PNG. Handles theme loading, Chrome/Chromium detection for PDF export, and batch conversion. Trigger when user says "export slides", "convert marp to pdf", "marp export", "slides to pdf", "slides to html", "导出slides", "slides转pdf", "导出演示文稿".
allowed-tools: Read, Bash, Glob, Grep
---

# Marp Export Skill

Export existing Marp markdown files to PDF (default), HTML, PPTX, or PNG.

## Quick Reference

```bash
# PDF (default) — requires Chrome/Chromium
npx @marp-team/marp-cli INPUT.md -o OUTPUT.pdf --theme-set ~/.claude/skills/marp-slides-creator/themes/ --allow-local-files --html

# HTML
npx @marp-team/marp-cli INPUT.md -o OUTPUT.html --theme-set ~/.claude/skills/marp-slides-creator/themes/ --html

# PPTX (editable, requires LibreOffice)
npx @marp-team/marp-cli INPUT.md -o OUTPUT.pptx --pptx-editable --theme-set ~/.claude/skills/marp-slides-creator/themes/ --allow-local-files

# PNG sequence
npx @marp-team/marp-cli INPUT.md --images png -o OUTPUT_DIR/ --theme-set ~/.claude/skills/marp-slides-creator/themes/
```

## Workflow

### Step 1: Locate Input File

Find the Marp markdown file. It must contain `marp: true` in YAML frontmatter.

```bash
# Verify it's a Marp file
head -5 INPUT.md  # should show "marp: true"
```

### Step 2: Theme Directory

Themes are stored in the marp-slides-creator skill:

```
THEME_DIR="$HOME/.claude/skills/marp-slides-creator/themes/"
```

Always use `--theme-set "$THEME_DIR/"` in all export commands.

### Step 3: Detect Chrome/Chromium (for PDF/PPTX)

PDF and PPTX export require a Chrome/Chromium browser. Marp-cli auto-detects, but if it fails:

```bash
# macOS Chrome paths (check in order)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
/Applications/Chromium.app/Contents/MacOS/Chromium --version
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version

# Set CHROME_PATH if auto-detection fails
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

If no browser found, fall back to HTML export and inform the user.

### Step 4: Export

Default format is **PDF**. User can specify otherwise.

**Output naming convention:**
- Same directory as input file
- Same base name, different extension
- Example: `presentation.md` → `presentation.pdf`

**PDF export:**
```bash
npx @marp-team/marp-cli INPUT.md \
  -o OUTPUT.pdf \
  --theme-set ~/.claude/skills/marp-slides-creator/themes/ \
  --allow-local-files \
  --html
```

**HTML export:**
```bash
npx @marp-team/marp-cli INPUT.md \
  -o OUTPUT.html \
  --theme-set ~/.claude/skills/marp-slides-creator/themes/ \
  --html
```

**Both PDF + HTML:**
```bash
# Run sequentially
npx @marp-team/marp-cli INPUT.md -o OUTPUT.pdf --theme-set ~/.claude/skills/marp-slides-creator/themes/ --allow-local-files --html
npx @marp-team/marp-cli INPUT.md -o OUTPUT.html --theme-set ~/.claude/skills/marp-slides-creator/themes/ --html
```

### Step 5: Verify & Report

```bash
# Check output exists and show file size
ls -lh OUTPUT.pdf OUTPUT.html 2>/dev/null
```

Report to user:
- Output file path(s)
- File size(s)
- Format(s) generated
- Any warnings from marp-cli

## Key Flags Reference

| Flag | Purpose | When to use |
|------|---------|-------------|
| `--theme-set DIR/` | Load custom themes | When custom .css themes exist |
| `--allow-local-files` | Allow local images | PDF/PPTX with local assets |
| `--html` | Enable HTML tags in markdown | Always recommended |
| `--pptx-editable` | Editable PPTX output | PPTX format (needs LibreOffice) |
| `--images png` | Export as PNG sequence | PNG format |
| `--pdf-notes` | Include speaker notes in PDF | When notes are present |
| `--pdf-outlines` | Add bookmarks to PDF | For long presentations |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Chrome/Chromium not found` | No browser for PDF | Set CHROME_PATH or fall back to HTML |
| `theme not found` | Missing theme CSS | Check --theme-set path, use built-in theme |
| `Could not find an input` | Bad file path | Verify path and marp: true frontmatter |
| Blank/empty PDF | HTML tags without --html | Add --html flag |

## Examples

```bash
# Export current project's slides to PDF
npx @marp-team/marp-cli slides_project/05_final/presentation.md \
  -o slides_project/05_final/slides.pdf \
  --theme-set ~/.claude/skills/marp-slides-creator/themes/ \
  --allow-local-files --html

# Quick HTML export (no Chrome needed)
npx @marp-team/marp-cli my-talk.md -o my-talk.html --html

# Batch export all .md files in a directory
for f in slides/*.md; do
  npx @marp-team/marp-cli "$f" -o "${f%.md}.pdf" --allow-local-files --html
done
```
