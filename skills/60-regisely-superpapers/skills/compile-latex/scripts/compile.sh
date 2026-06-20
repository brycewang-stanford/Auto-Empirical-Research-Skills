#!/usr/bin/env bash
# Multi-pass LaTeX compiler with engine auto-detection.
# Usage: ./compile.sh path/to/paper.tex
#
# Detects:
#   - Engine: xelatex if preamble has \usepackage{fontspec}, else pdflatex
#   - Bibliography: biber if \usepackage{biblatex}, bibtex if \bibliography{}, none otherwise
#
# Strategy:
#   1. First pass with the chosen engine
#   2. Run biber/bibtex if applicable
#   3. Second pass
#   4. Third pass to resolve cross-references
#
# If latexmk is available, prefer it.

set -euo pipefail

file="${1:?usage: $0 <paper.tex>}"

if [[ ! -f "$file" ]]; then
  echo "FAIL: $file does not exist" >&2
  exit 1
fi

dir=$(dirname "$file")
base=$(basename "$file" .tex)

# Detect engine
if grep -qE '^[^%]*\\usepackage\{?fontspec\}?' "$file"; then
  engine="xelatex"
else
  engine="pdflatex"
fi

# Detect bibliography system
bib_system="none"
if grep -qE '^[^%]*\\usepackage(\[.*\])?\{biblatex\}' "$file"; then
  bib_system="biber"
elif grep -qE '^[^%]*\\bibliography\{' "$file"; then
  bib_system="bibtex"
fi

echo "engine: $engine"
echo "bibliography: $bib_system"

# Prefer latexmk if available
if command -v latexmk >/dev/null 2>&1; then
  echo "using latexmk"
  case "$engine" in
    xelatex)
      latexmk -xelatex -interaction=nonstopmode -halt-on-error -cd "$file"
      ;;
    pdflatex)
      latexmk -pdf -interaction=nonstopmode -halt-on-error -cd "$file"
      ;;
  esac
  exit $?
fi

# Manual multi-pass
cd "$dir"

run_engine() {
  "$engine" -interaction=nonstopmode -halt-on-error "$base.tex"
}

echo "pass 1"
run_engine || { echo "FAIL: first pass" >&2; exit 1; }

case "$bib_system" in
  biber)
    echo "biber"
    biber "$base" || { echo "FAIL: biber" >&2; exit 1; }
    ;;
  bibtex)
    echo "bibtex"
    bibtex "$base" || { echo "FAIL: bibtex" >&2; exit 1; }
    ;;
esac

if [[ "$bib_system" != "none" ]]; then
  echo "pass 2"
  run_engine || { echo "FAIL: second pass" >&2; exit 1; }
fi

echo "pass 3"
run_engine || { echo "FAIL: third pass" >&2; exit 1; }

echo "OK: $base.pdf"
