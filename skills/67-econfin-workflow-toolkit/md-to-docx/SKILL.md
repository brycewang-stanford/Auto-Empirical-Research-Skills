---
name: md-to-docx
description: Convert Markdown files to Word documents (.docx) with proper formatting, Chinese font support (FangSong for all text including headings), black font color, 1.5x line spacing, precise first-line indent (24pt), heading spacing after (1 line), no italic headings, and automatic superscript conversion for citation numbers. Use when converting .md files to .docx, creating Word documents from markdown, or when user mentions Word, DOCX, or document conversion. Requires pandoc.
allowed-tools: Bash, Read, Write, Glob
---

# Markdown to Word (DOCX) Converter

Convert markdown files to professionally formatted Word documents (.docx) using pandoc.

## What this Skill does

This Skill enables Claude to convert Markdown files to Word documents with proper formatting, including:

- Headings and text formatting (H1-H6, bold, italic, strikethrough)
- Lists (ordered and unordered, nested)
- Tables with proper formatting
- Images (automatically embedded)
- Links and references
- Code blocks and inline code
- Chinese punctuation preservation (。，""（）；！？)
- **Citation superscript**: Automatically converts citation numbers (e.g., `文献1。` → `文献¹。`) to superscript format for academic documents
- **Default Chinese template**: Uses FangSong (仿宋) font for all Chinese text (body, headings, and subtitles), Times New Roman for English text, black color for all text, 1.5x line spacing, first-line indent of two characters (24pt, precisely aligned), heading spacing after (1 line / 12pt), and no italic style for headings

## Requirements

Packages must be installed in your environment before using this Skill:

**pandoc** (required):
```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt-get install pandoc

# Windows
choco install pandoc
```

**python-docx** (required for template creation):
```bash
pip install python-docx
```

Verify pandoc installation:
```bash
pandoc --version
```

## Instructions

When the user requests to convert a Markdown file to Word format:

1. **Check if pandoc is installed** by running `pandoc --version`
   - If not installed, guide the user to install it (see Requirements section)

2. **Identify the input and output files**
   - Ask for clarification if the user hasn't specified the output filename
   - Use meaningful names (e.g., if input is `report.md`, suggest `report.docx`)

3. **Run the conversion script** using the Bash tool:
   ```bash
   python .claude/skills/md-to-docx/convert_md_to_docx.py input.md output.docx
   ```

4. **Use additional options as needed**:
   - Add `--toc` for table of contents (default: no TOC)
   - Add `--no-chinese-template` if user doesn't want FangSong font
   - Add `--no-superscript-citations` to disable automatic citation superscript conversion
   - Add `--reference-doc template.docx` for custom styling
   - Add `--title`, `--author`, `--date` for document metadata

5. **For batch conversions**:
   ```bash
   python .claude/skills/md-to-docx/convert_md_to_docx.py --batch input_dir/ output_dir/
   ```

6. **Verify the conversion** succeeded and inform the user of the output location

**Default behavior**: The script automatically uses a Chinese template with FangSong (仿宋) font for Chinese text unless `--no-chinese-template` is specified.

## Examples

**Convert a single file** (uses default Chinese template):
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py "教育改革方案.md" "教育改革方案.docx"
```

**Convert with table of contents** (optional, default is no TOC):
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py report.md report.docx --toc
```

**Convert with metadata**:
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py paper.md paper.docx \
  --title "研究报告" \
  --author "张三" \
  --date "2025-11-20"
```

**Batch convert all markdown files**:
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py --batch ./markdown_files/ ./word_docs/
```

**Use custom template for organizational styling**:
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py doc.md doc.docx \
  --reference-doc company_template.docx
```

## Supporting Files

This Skill includes additional resources:

- **[README.md](README.md)**: Detailed usage guide with examples
- **[快速使用指南.md](快速使用指南.md)**: Quick start guide in Chinese
- **convert_md_to_docx.py**: Main conversion script with automatic post-processing
- **create_chinese_template.py**: Utility to create custom Chinese templates
- **fix_heading_fonts.py**: Post-processing script for font and spacing fixes
- **chinese_template.docx**: Default Chinese font template (FangSong, 1.5x line spacing, heading spacing)

## Troubleshooting

**"pandoc: command not found"**
- Install pandoc using your package manager (see Requirements section)

**Images not appearing in output**
- Ensure image paths in markdown are correct (use relative paths from markdown file location)
- Verify image files exist at specified paths

**Table formatting issues**
- Verify markdown table syntax:
  ```markdown
  | Header 1 | Header 2 |
  |----------|----------|
  | Cell 1   | Cell 2   |
  ```

**Script execution errors**
- Ensure script has execute permissions: `chmod +x convert_md_to_docx.py`
- Use forward slashes in all file paths (Unix style)

## Chinese Document Best Practices

When converting Chinese documents:

1. **Encoding**: Ensure markdown files use UTF-8 encoding
2. **Punctuation**: Use proper Chinese punctuation (。，""（）；！？)
3. **Font**: Default template uses FangSong for all Chinese text (body, headings, and subtitles) with black color
4. **Line spacing**: 1.5x line spacing for all paragraphs (符合中文文档标准)
5. **Paragraph formatting**: First-line indent of two characters (24pt, precisely aligned) for proper Chinese document style
6. **Heading spacing**: 1 line (12pt) spacing after all headings for better readability
7. **Heading style**: All headings use FangSong font without italic style
8. **Custom templates**: Create organizational templates with `create_chinese_template.py`

## Command Line Options Reference

| Option | Description |
|--------|-------------|
| `input.md` | Input Markdown file path |
| `output.docx` | Output Word document path |
| `--toc` | Generate table of contents (default: no TOC) |
| `--no-chinese-template` | Don't use default Chinese font template |
| `--no-superscript-citations` | Don't convert citation numbers to superscript |
| `--reference-doc FILE` | Use custom Word template for styling |
| `--title TEXT` | Set document title metadata |
| `--author TEXT` | Set document author metadata |
| `--date TEXT` | Set document date metadata |
| `--batch` | Enable batch conversion mode |
| `--pattern PATTERN` | File pattern for batch mode (default: `*.md`) |

## Default Document Formatting

The Chinese template automatically applies:

- **Font**: FangSong (仿宋) for Chinese text, Times New Roman for English
- **Font size**: 12pt (body text)
- **Font color**: Black for all text
- **Line spacing**: 1.5x for all paragraphs
- **First-line indent**: 24pt (2 Chinese characters)
- **Heading spacing**: 12pt (1 line) after each heading
- **Heading style**: Bold, no italic
- **Citation superscript**: Numbers before sentence-ending punctuation (。；) are automatically converted to superscript (e.g., `参考文献1。` → `参考文献¹。`). Only converts numbers 1-60 that directly follow Chinese characters or letters.
- **Table of contents**: Not generated by default (use `--toc` to add)

For complete documentation, see [README.md](README.md).
