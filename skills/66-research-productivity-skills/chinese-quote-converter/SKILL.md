---
name: chinese-quote-converter
description: Convert English straight quotation marks ("...") to Chinese curved quotation marks ("..." U+201C/D). Use when processing Chinese text documents, markdown files, or any content that needs proper Chinese typography with directional quotes. Triggers on keywords like "转换引号", "中文引号", "英文引号转中文", "quote conversion", "convert quotes".
---

# Chinese Quote Converter

Convert English straight quotes to Chinese curved quotes:
- `"..."` → `"..."` (U+201C / U+201D)
- `'...'` → `'...'` (U+2018 / U+2019)

## Usage

Run the conversion script:

```bash
# Preview conversion (output to stdout)
python3 scripts/convert_quotes.py <input_file>

# Save to new file
python3 scripts/convert_quotes.py <input_file> -o <output_file>

# Modify file in-place
python3 scripts/convert_quotes.py <input_file> --in-place
```

## Features

- Preserves code blocks (```, `, $$) by default
- Handles nested quotes correctly
- Detects English apostrophes (don't, it's) and leaves them unchanged
- Use `--no-preserve-code` to also convert quotes inside code blocks
