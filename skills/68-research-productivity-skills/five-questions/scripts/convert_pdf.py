#!/usr/bin/env python3
"""Convert PDF to Markdown using markitdown.

Usage:
    python3 convert_pdf.py <pdf_path> <output_md_path>

Requires: markitdown (conda run -n sci pip install 'markitdown[pdf]')
"""
import sys
import os


def convert(pdf_path: str, output_path: str) -> None:
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(pdf_path)
    md_text = result.text_content
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_text)
    char_count = len(md_text)
    print(f"Converted: {char_count:,} chars saved to {output_path}")
    if char_count < 2000:
        print(f"WARNING: Output is very short ({char_count} chars). "
              "This may be a scanned PDF with limited text extraction.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: convert_pdf.py <pdf_path> <output_md_path>")
        sys.exit(1)

    pdf_path, output_path = sys.argv[1], sys.argv[2]

    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF not found: {pdf_path}")
        sys.exit(1)

    try:
        convert(pdf_path, output_path)
    except ImportError:
        print("ERROR: markitdown not installed.")
        print("Fix: conda run -n sci pip install 'markitdown[pdf]'")
        sys.exit(1)
    except Exception as e:
        err_msg = str(e)
        if "password" in err_msg.lower() or "encrypted" in err_msg.lower():
            print("ERROR: PDF appears to be password-protected.")
            print("Fix: qpdf --decrypt input.pdf output.pdf")
        else:
            print(f"ERROR: Conversion failed: {e}")
        sys.exit(1)
