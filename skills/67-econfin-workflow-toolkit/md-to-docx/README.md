# Markdown to DOCX Converter Skill

A Claude Code skill that converts Markdown files to professionally formatted Word documents (.docx).

## Quick Start

1. **Verify pandoc installation:**
   ```bash
   pandoc --version
   ```

2. **If pandoc is not installed:**
   ```bash
   # macOS
   brew install pandoc

   # Linux (Debian/Ubuntu)
   sudo apt-get install pandoc

   # Windows (with Chocolatey)
   choco install pandoc
   ```

3. **Convert a markdown file:**
   ```bash
   python .claude/skills/md-to-docx/convert_md_to_docx.py input.md output.docx
   ```

## Usage Examples

### Single File Conversion
```bash
# Basic conversion
python .claude/skills/md-to-docx/convert_md_to_docx.py README.md README.docx

# With table of contents
python .claude/skills/md-to-docx/convert_md_to_docx.py report.md report.docx --toc

# With metadata
python .claude/skills/md-to-docx/convert_md_to_docx.py paper.md paper.docx \
  --title "研究报告" \
  --author "张三" \
  --date "2025-01-20"

# Using a reference template for consistent styling
python .claude/skills/md-to-docx/convert_md_to_docx.py doc.md doc.docx \
  --reference-doc template.docx
```

### Batch Conversion
```bash
# Convert all .md files in a directory
python .claude/skills/md-to-docx/convert_md_to_docx.py \
  --batch \
  ./markdown_files/ \
  ./word_documents/

# Convert specific pattern
python .claude/skills/md-to-docx/convert_md_to_docx.py \
  --batch \
  ./reports/ \
  ./output/ \
  --pattern "report_*.md"
```

## Features

- ✓ Preserves markdown formatting (headings, lists, tables, code blocks)
- ✓ Handles Chinese text and punctuation correctly
- ✓ Embeds images referenced in markdown
- ✓ Supports custom Word templates for consistent styling
- ✓ Batch processing for multiple files
- ✓ Table of contents generation
- ✓ Document metadata (title, author, date)

## Command Line Options

```
python convert_md_to_docx.py [-h] [--reference-doc REFERENCE_DOC]
                             [--toc] [--no-standalone]
                             [--title TITLE] [--author AUTHOR] [--date DATE]
                             [--batch] [--pattern PATTERN]
                             input [output]
```

**Arguments:**
- `input`: Input markdown file (or directory in batch mode)
- `output`: Output DOCX file (or directory in batch mode)

**Options:**
- `--reference-doc`: Path to a reference DOCX file for styling
- `--toc`: Generate table of contents
- `--no-standalone`: Don't create standalone document
- `--title`: Document title metadata
- `--author`: Document author metadata
- `--date`: Document date metadata
- `--batch`: Enable batch conversion mode
- `--pattern`: File pattern for batch mode (default: `*.md`)

## How It Works

This skill uses `pandoc`, a universal document converter, to transform markdown into Word format while preserving:

1. **Text Formatting**: Bold, italic, strikethrough
2. **Structure**: Headings (H1-H6), paragraphs, line breaks
3. **Lists**: Ordered and unordered lists, nested lists
4. **Tables**: Markdown tables with alignment
5. **Code**: Inline code and code blocks with syntax
6. **Media**: Embedded images and links
7. **Metadata**: Document properties

## Customization

### Using a Reference Template

Create a Word document with your desired styling (fonts, colors, margins, headers/footers) and use it as a reference:

```bash
python convert_md_to_docx.py input.md output.docx --reference-doc my_template.docx
```

This ensures all converted documents follow your organization's style guidelines.

### For Chinese Documents

The script automatically handles Chinese text. Make sure your markdown files:
- Use UTF-8 encoding
- Include proper Chinese punctuation: 。，""（）；！？
- Have correct image paths for embedded figures

## Troubleshooting

**Problem: "pandoc: command not found"**
- Solution: Install pandoc using your system's package manager

**Problem: "No such file or directory"**
- Solution: Check that input file path is correct
- Use absolute paths if relative paths aren't working

**Problem: Images not appearing in output**
- Solution: Verify image paths in markdown are correct
- Use relative paths from the markdown file location
- Ensure image files exist at the specified paths

**Problem: Table formatting issues**
- Solution: Verify markdown table syntax:
  ```markdown
  | Header 1 | Header 2 |
  |----------|----------|
  | Cell 1   | Cell 2   |
  ```

## Integration with Claude Code

When using this skill with Claude Code, you can simply ask:

- "Convert README.md to Word format"
- "Turn this markdown into a docx file"
- "Batch convert all markdown files in the docs folder to Word"

Claude will automatically use this skill to perform the conversion.

## License

This skill is provided as-is for use with Claude Code.
