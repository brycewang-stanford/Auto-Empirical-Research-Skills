#!/usr/bin/env python3
"""
Convert PDF pages to individual PNG images for better table/figure reading.

Usage:
    python pdf_to_images.py <input.pdf> [--output-dir OUTPUT_DIR] [--pages 1-5,8,10-12] [--dpi 200]

Requires: pip install pymupdf (or pip install PyMuPDF)
"""

import argparse
import sys
from pathlib import Path

def parse_page_ranges(pages_str, max_page):
    """Parse page range string like '1-5,8,10-12' into list of 0-based page indices."""
    pages = set()
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(1, int(start))
            end = min(max_page, int(end))
            pages.update(range(start - 1, end))
        else:
            p = int(part)
            if 1 <= p <= max_page:
                pages.add(p - 1)
    return sorted(pages)

def convert_pdf_to_images(pdf_path, output_dir=None, pages=None, dpi=200):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("Error: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    print(f"PDF has {total_pages} pages.")

    if pages:
        page_indices = parse_page_ranges(pages, total_pages)
    else:
        page_indices = list(range(total_pages))

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    output_files = []

    for i in page_indices:
        page = doc[i]
        pix = page.get_pixmap(matrix=matrix)
        out_file = output_dir / f"page_{i+1:03d}.png"
        pix.save(str(out_file))
        output_files.append(out_file)
        print(f"  Saved: {out_file}")

    doc.close()
    print(f"\nDone. {len(output_files)} images saved to {output_dir}")
    return output_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF pages to PNG images")
    parser.add_argument("pdf", help="Path to input PDF file")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: <pdf_name>_pages/)")
    parser.add_argument("--pages", "-p", help="Page ranges, e.g. '1-5,8,10-12' (default: all)")
    parser.add_argument("--dpi", "-d", type=int, default=200, help="Resolution in DPI (default: 200)")
    args = parser.parse_args()
    convert_pdf_to_images(args.pdf, args.output_dir, args.pages, args.dpi)
