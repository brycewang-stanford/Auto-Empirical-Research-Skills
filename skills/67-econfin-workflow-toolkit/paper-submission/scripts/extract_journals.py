"""
Extract journal data from ABS journal list PDF.

Usage:
    python extract_journals.py --pdf "path/to/ABS.pdf" --fields "FINANCE,ECON" --stars "3,4" --output journals.json

Outputs a JSON file with filtered journal entries.
"""

import json
import re
import sys
import argparse
from pathlib import Path

import fitz  # PyMuPDF


def extract_all_journals(pdf_path: str) -> list[dict]:
    """Extract all journal entries from the ABS PDF."""
    doc = fitz.open(pdf_path)
    journals = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()
        lines = text.strip().split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Try to match ISSN pattern at start of a journal entry
            issn_match = re.match(r"^(\d{4}-\d{3}[\dX])\s*$", line)
            if issn_match:
                issn = issn_match.group(1)

                # Next line(s): Field
                i += 1
                if i >= len(lines):
                    break
                field = lines[i].strip()

                # Next line(s): Journal Title
                i += 1
                if i >= len(lines):
                    break
                title = lines[i].strip()

                # Next lines: ABS, ABDC, SSCI, JCR, JIF, UTD24, FT50
                # These may span multiple lines
                remaining = []
                for j in range(1, 8):
                    if i + j < len(lines):
                        remaining.append(lines[i + j].strip())

                entry = {
                    "issn": issn,
                    "field": field,
                    "title": title,
                    "abs": "",
                    "abdc": "",
                    "ssci": "",
                    "jcr": "",
                    "jif": "",
                    "utd24": False,
                    "ft50": False,
                }

                # Parse remaining values
                vals = []
                for r in remaining:
                    if r and r not in ["", " "]:
                        # Split on whitespace but keep values
                        vals.extend(r.split())

                # ABS rating: 4*, 4, 3, 2, 1
                if vals:
                    v = vals[0]
                    if v in ["4*", "4", "3", "2", "1"]:
                        entry["abs"] = v
                        vals = vals[1:]

                # ABDC rating: A*, A, B, C
                if vals:
                    v = vals[0]
                    if v in ["A*", "A", "B", "C"]:
                        entry["abdc"] = v
                        vals = vals[1:]

                # SSCI: Yes/No
                if vals:
                    v = vals[0]
                    if v in ["Yes", "No"]:
                        entry["ssci"] = v
                        vals = vals[1:]

                # JCR: Q1, Q2, Q3, Q4, N/A
                if vals:
                    v = vals[0]
                    if v in ["Q1", "Q2", "Q3", "Q4", "N/A"]:
                        entry["jcr"] = v
                        vals = vals[1:]

                # JIF: float or empty
                if vals:
                    v = vals[0]
                    try:
                        entry["jif"] = float(v)
                        vals = vals[1:]
                    except ValueError:
                        pass

                # UTD24, FT50: Yes or empty
                if vals:
                    if "Yes" in vals:
                        idx = vals.index("Yes")
                        entry["utd24"] = True
                        vals = vals[idx + 1:]
                        if vals and vals[0] == "Yes":
                            entry["ft50"] = True
                    elif len(vals) >= 2 and vals[0] == "" and vals[1] == "Yes":
                        entry["ft50"] = True

                journals.append(entry)
                i += len(remaining) + 1
                continue

            i += 1

    doc.close()
    return journals


def extract_journals_robust(pdf_path: str) -> list[dict]:
    """More robust extraction using the full text line patterns."""
    doc = fitz.open(pdf_path)
    journals = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        # Find all ISSN patterns and extract surrounding context
        # The PDF text format per entry appears as:
        # ISSN\nFIELD\nJournal Title\nABS\nABDC\nSSCI\nJCR\nJIF\n[UTD24]\n[FT50]
        entries = re.split(r"(?=\d{4}-\d{3}[\dX]\s*\n)", text)

        for entry_text in entries:
            entry_text = entry_text.strip()
            if not entry_text:
                continue

            lines = [l.strip() for l in entry_text.split("\n") if l.strip()]
            if len(lines) < 4:
                continue

            # First line: ISSN
            if not re.match(r"^\d{4}-\d{3}[\dX]$", lines[0]):
                continue

            issn = lines[0]
            field = lines[1]
            title = lines[2]

            # Remaining lines contain the ratings
            rest = lines[3:]
            rest_str = " ".join(rest)

            entry = {
                "issn": issn,
                "field": field,
                "title": title,
                "abs": "",
                "abdc": "",
                "ssci": "",
                "jcr": "",
                "jif": "",
                "utd24": False,
                "ft50": False,
            }

            # Parse ABS: 4*, 4, 3, 2, 1
            for val in ["4*", "4", "3", "2", "1"]:
                if val in rest:
                    entry["abs"] = val
                    break

            # Parse ABDC: A*, A, B, C
            abdc_vals = re.findall(r"\b(A\*|A|B|C)\b", rest_str)
            if abdc_vals:
                entry["abdc"] = abdc_vals[0]

            # Parse SSCI
            if "Yes" in rest:
                entry["ssci"] = "Yes"
            elif "No" in rest:
                entry["ssci"] = "No"

            # Parse JCR
            jcr_match = re.search(r"(Q[1-4]|N/A)", rest_str)
            if jcr_match:
                entry["jcr"] = jcr_match.group(1)

            # Parse JIF
            jif_match = re.findall(r"\b(\d+\.\d+)\b", rest_str)
            if jif_match:
                entry["jif"] = float(jif_match[0])

            # UTD24 / FT50
            yes_count = rest_str.count("Yes")
            if yes_count >= 3:
                entry["utd24"] = True
                entry["ft50"] = True
            elif yes_count >= 2:
                # Depends on position - SSCI=Yes counts as one
                if entry["ssci"] == "Yes":
                    entry["utd24"] = True
                    if yes_count >= 3:
                        entry["ft50"] = True

            journals.append(entry)

    doc.close()
    return journals


def filter_journals(
    journals: list[dict],
    fields: list[str] | None = None,
    stars: list[str] | None = None,
    ssci_only: bool = False,
) -> list[dict]:
    """Filter journals by field, star rating, and SSCI status."""
    result = journals
    if fields:
        fields_upper = [f.upper() for f in fields]
        result = [j for j in result if j["field"].upper() in fields_upper]
    if stars:
        result = [j for j in result if j["abs"] in stars]
    if ssci_only:
        result = [j for j in result if j["ssci"] == "Yes"]
    return result


def main():
    parser = argparse.ArgumentParser(description="Extract journals from ABS PDF")
    parser.add_argument("--pdf", required=True, help="Path to ABS journal list PDF")
    parser.add_argument("--fields", default="", help="Comma-separated field codes (e.g., FINANCE,ECON)")
    parser.add_argument("--stars", default="", help="Comma-separated star ratings (e.g., 3,4)")
    parser.add_argument("--ssci-only", action="store_true", help="Only include SSCI-indexed journals")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    print(f"Extracting journals from: {args.pdf}")
    journals = extract_journals_robust(args.pdf)
    print(f"Total journals extracted: {len(journals)}")

    # Show field distribution
    field_counts = {}
    for j in journals:
        field_counts[j["field"]] = field_counts.get(j["field"], 0) + 1
    print("Fields found:")
    for f, c in sorted(field_counts.items()):
        print(f"  {f}: {c}")

    # Apply filters
    fields = [f.strip() for f in args.fields.split(",") if f.strip()] if args.fields else None
    stars = [s.strip() for s in args.stars.split(",") if s.strip()] if args.stars else None

    filtered = filter_journals(journals, fields=fields, stars=stars, ssci_only=args.ssci_only)
    print(f"After filtering: {len(filtered)} journals")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
