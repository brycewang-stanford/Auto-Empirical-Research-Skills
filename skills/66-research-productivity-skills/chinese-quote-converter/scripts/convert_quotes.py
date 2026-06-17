#!/usr/bin/env python3
"""
Convert English straight quotation marks to Chinese curved quotation marks.

Converts:
- Straight double quotes "..." → " " (U+201C / U+201D)
- Straight single quotes '...' → ' ' (U+2018 / U+2019)

Handles nested quotes and preserves code blocks.
"""

import argparse
import re
import sys
from pathlib import Path


# Chinese curved quotation marks
LEFT_DOUBLE = '\u201C'   # "
RIGHT_DOUBLE = '\u201D'  # "
LEFT_SINGLE = '\u2018'   # '
RIGHT_SINGLE = '\u2019'  # '


def convert_quotes(text: str, preserve_code_blocks: bool = True) -> str:
    """
    Convert English straight quotes to Chinese curved quotes.

    Args:
        text: Input text with English quotes
        preserve_code_blocks: If True, don't convert quotes inside code blocks

    Returns:
        Text with Chinese quotes
    """
    if preserve_code_blocks:
        # Pattern for fenced code blocks, inline code, and math blocks (both $...$ and $$...$$)
        code_pattern = r'(```[\s\S]*?```|`[^`\n]+`|\$\$[\s\S]*?\$\$|\$[^$\n]+\$)'
        parts = re.split(code_pattern, text)

        result = []
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Code block - preserve as-is
                result.append(part)
            else:  # Regular text - convert quotes
                result.append(_convert_quotes_in_text(part))
        return ''.join(result)
    else:
        return _convert_quotes_in_text(text)


def _convert_quotes_in_text(text: str) -> str:
    """Convert quotes in plain text (no code blocks)."""
    result = []
    i = 0
    double_quote_open = False
    single_quote_open = False

    while i < len(text):
        char = text[i]

        # Handle straight double quote "
        if char == '"':
            if double_quote_open:
                result.append(RIGHT_DOUBLE)
                double_quote_open = False
            else:
                result.append(LEFT_DOUBLE)
                double_quote_open = True

        # Handle straight single quote '
        elif char == "'":
            # Check if it's likely an apostrophe (letter before and after)
            prev_char = text[i-1] if i > 0 else ''
            next_char = text[i+1] if i < len(text) - 1 else ''

            # If surrounded by letters, it's likely an apostrophe - keep as-is
            if prev_char.isalpha() and next_char.isalpha():
                result.append(char)
            else:
                if single_quote_open:
                    result.append(RIGHT_SINGLE)
                    single_quote_open = False
                else:
                    result.append(LEFT_SINGLE)
                    single_quote_open = True

        else:
            result.append(char)

        i += 1

    return ''.join(result)


def convert_file(input_path: str, output_path: str = None, in_place: bool = False,
                 preserve_code: bool = True) -> str:
    """
    Convert quotes in a file.

    Args:
        input_path: Path to input file
        output_path: Path to output file (optional)
        in_place: If True, modify the input file directly
        preserve_code: If True, preserve quotes in code blocks

    Returns:
        Converted text
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    text = input_file.read_text(encoding='utf-8')
    converted = convert_quotes(text, preserve_code_blocks=preserve_code)

    if in_place:
        input_file.write_text(converted, encoding='utf-8')
        print(f"Converted: {input_path}", file=sys.stderr)
    elif output_path:
        output_file = Path(output_path)
        output_file.write_text(converted, encoding='utf-8')
        print(f"Saved to: {output_path}", file=sys.stderr)

    return converted


def main():
    parser = argparse.ArgumentParser(
        description='Convert English quotes to Chinese curved quotes (U+201C/D, U+2018/9)'
    )
    parser.add_argument('input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-i', '--in-place', action='store_true',
                        help='Modify the input file in-place')
    parser.add_argument('--no-preserve-code', action='store_true',
                        help='Also convert quotes inside code blocks')

    args = parser.parse_args()

    try:
        result = convert_file(
            args.input,
            args.output,
            args.in_place,
            preserve_code=not args.no_preserve_code
        )

        if not args.in_place and not args.output:
            print(result)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
