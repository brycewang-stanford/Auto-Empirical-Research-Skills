#!/usr/bin/env python3
"""provenance_scrub.py — inspect and clean AI-provenance carriers in a manuscript package.

Part of the `de-aigc-skills` skill (AERS collection 48). Standard library only,
Python 3.9+. Two of the three kinds of "AI watermark" that circulate in 2026 are
deterministic and this script handles them; the third is not, and this script
says so instead of pretending.

  Layer A  invisible-character carriers inside text
           (zero-width characters, bidi controls, tag characters, stray
           variation selectors, script-bound format characters, exotic
           spaces, soft hyphens, C0/C1 controls, trailing-whitespace
           patterns) plus look-alike characters (Cyrillic / Greek letters
           inside Latin words, canonical-singleton punctuation, fullwidth
           Latin inside English words)
           -> .txt .md .qmd .Rmd .tex .bib .html .csv and the text runs of .docx

  Layer C  container metadata on the submission package
           (.docx docProps / custom.xml labels / rsids / template path /
            comments / people.xml / customXml / figures pasted into the
            document, .png / .jpg C2PA + EXIF + XMP, .svg <metadata>,
            .pdf Info + XMP incl. compressed streams and pdfTeX figure info,
            .zip __MACOSX AppleDouble entries, macOS download-origin xattrs,
            generator stamps in source files, model names in file names)
           -> reported for every format; lossless cleaning for docx / png / jpg
              / svg / zip (members cleaned in place); report + exact commands
              for pdf and xattrs

  Layer B  statistical token-sampling watermarks (Claude since 2026-08,
           Gemini SynthID) live in the *word choices*. No characters are added,
           so nothing here can detect or remove them. Only an author rewrite
           does. The report prints "B: unknown" for that reason, every time.

The cleaner is CJK-aware on purpose: a bilingual academic manuscript legitimately
contains U+3000 ideographic spaces (paragraph indents), fullwidth punctuation,
ideographic variation selectors in personal names, en dashes in year ranges,
U+2212 minus signs in tables and superscript digits in R². None of those are
touched, and NFKC is never applied. See ../references/watermarks.md for the
policy table this file implements.

Usage
    python3 provenance_scrub.py inspect  FILE [FILE ...] [--lang auto|zh|en] [--json]
    python3 provenance_scrub.py clean    FILE [FILE ...] [--lang auto|zh|en]
                                         [-o OUT] [--in-place] [--keep-nbsp]
                                         [--keep-bidi] [--typography]
                                         [--keep-meta] [--fold-homoglyphs]
                                         [--diff] [--json]
    python3 provenance_scrub.py self-test
    cat draft.md | python3 provenance_scrub.py clean - > draft.clean.md

`inspect` exits 1 when it finds something (so it can gate a submission
checklist) and 0 when the file is clean. `clean` writes `<name>.clean.<ext>`
unless `-o` or `--in-place` (which leaves a `.bak`) is given.
"""

from __future__ import annotations

import argparse
import difflib
import io
import json
import re
import struct
import subprocess
import sys
import unicodedata
import zipfile
import zlib
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

__version__ = "1.1.0"

# --------------------------------------------------------------------------- #
# Code-point policy (mirrors references/watermarks.md §3)
# --------------------------------------------------------------------------- #

TEXT_SUFFIXES = {".txt", ".md", ".markdown", ".qmd", ".rmd", ".tex", ".bib",
                 ".html", ".htm", ".csv", ".tsv", ".json", ".yaml", ".yml"}
MARKDOWN_SUFFIXES = {".md", ".markdown", ".qmd", ".rmd"}
HTML_SUFFIXES = {".html", ".htm"}


def _r(a: int, b: int) -> range:
    return range(a, b + 1)


# Always removed (no legitimate use inside prose of an EN/ZH manuscript).
STRIP_ALWAYS = set()
STRIP_ALWAYS.update({0x00AD})                    # soft hyphen
STRIP_ALWAYS.update({0x034F})                    # combining grapheme joiner
STRIP_ALWAYS.update(_r(0x2060, 0x2065))          # word joiner, invisible operators, reserved
STRIP_ALWAYS.update(_r(0x206A, 0x206F))          # deprecated format controls
STRIP_ALWAYS.update({0xFEFF})                    # zero width no-break space / BOM
STRIP_ALWAYS.update(_r(0xFFF0, 0xFFF8))          # unassigned specials
STRIP_ALWAYS.update(_r(0xFFF9, 0xFFFB))          # interlinear annotation
STRIP_ALWAYS.update(_r(0xFDD0, 0xFDEF))          # noncharacters
STRIP_ALWAYS.update({0xE0000})                   # reserved tag-block start
STRIP_ALWAYS.update(_r(0xE0080, 0xE00FF))        # reserved
STRIP_ALWAYS.update(_r(0xE01F0, 0xE0FFF))        # reserved
for _plane in range(0x11):
    STRIP_ALWAYS.update({_plane * 0x10000 + 0xFFFE, _plane * 0x10000 + 0xFFFF})

# C0 / C1 controls except tab, LF, CR.
CONTROLS = set(_r(0x00, 0x08)) | {0x0B, 0x0C} | set(_r(0x0E, 0x1F)) | {0x7F} | set(_r(0x80, 0x9F))
CONTROLS.discard(0x85)  # NEL is handled as a line separator below

LINE_SEPARATORS = {0x2028, 0x2029, 0x0085}

# Context-dependent.
ZWSP, ZWNJ, ZWJ = 0x200B, 0x200C, 0x200D
BIDI = {0x200E, 0x200F, 0x061C} | set(_r(0x202A, 0x202E)) | set(_r(0x2066, 0x2069))
TAGS = {0xE0001} | set(_r(0xE0020, 0xE007F))
VS_TEXT = set(_r(0xFE00, 0xFE0D))               # VS1–VS14
VS_EMOJI = {0xFE0E, 0xFE0F}                      # VS15 (text) / VS16 (emoji)
IVS = set(_r(0xE0100, 0xE01EF))                  # ideographic variation selectors
MONGOLIAN_FVS = set(_r(0x180B, 0x180F))          # FVS1–3, MVS, FVS4
HANGUL_FILLERS = {0x115F, 0x1160, 0x3164, 0xFFA0}

# Space homoglyphs normalised to U+0020 (U+3000 is CJK-aware, see below).
SPACE_HOMOGLYPHS = {0x1680, 0x202F, 0x205F} | set(_r(0x2000, 0x200A))
NBSP = 0x00A0
IDEOGRAPHIC_SPACE = 0x3000

# Script-bound format characters (the rest of Unicode's Cf category, hard-coded
# so the policy does not drift with the interpreter's Unicode version). Each is
# legitimate only next to letters of its own script; elsewhere it is a carrier.
SCRIPT_FORMAT: List[Tuple[set, List[range]]] = [
    (set(_r(0x0600, 0x0605)) | {0x06DD, 0x08E2} | set(_r(0x0890, 0x0891)),
     [_r(0x0600, 0x06FF), _r(0x0750, 0x077F), _r(0x0870, 0x08FF)]),   # Arabic number signs
    ({0x070F}, [_r(0x0700, 0x074F)]),                                   # Syriac abbreviation mark
    ({0x17B4, 0x17B5}, [_r(0x1780, 0x17FF)]),                           # Khmer inherent vowels
    ({0x110BD, 0x110CD}, [_r(0x11080, 0x110CF)]),                       # Kaithi number signs
    (set(_r(0x13430, 0x1343F)), [_r(0x13000, 0x1345F)]),                # Egyptian hieroglyph format
    (set(_r(0x1BCA0, 0x1BCA3)), [_r(0x1BC00, 0x1BCAF)]),                # shorthand format controls
    (set(_r(0x1D173, 0x1D17A)), [_r(0x1D100, 0x1D1FF)]),                # musical symbol format
]
SCRIPT_FORMAT_ALL = set().union(*(s for s, _ in SCRIPT_FORMAT))

# Look-alike code points whose canonical (NFC) form is a single other code
# point. Folding them is exactly what NFC would do to these characters and
# nothing else, so it is lossless; whole-text NFC is still never applied
# (it would rewrite CJK compatibility ideographs used in personal names).
CANONICAL_SINGLETONS = {0x037E: ";", 0x0387: "·", 0x0374: "ʹ", 0x1FEF: "`", 0x1FFD: "´",
                        0x212A: "K", 0x212B: "Å", 0x2126: "Ω",
                        0x0340: "̀", 0x0341: "́", 0x0343: "̓"}

# Fullwidth Latin letters and digits (folded only inside an otherwise-ASCII
# word of an English manuscript: "ＴFP" -> "TFP", "Table３" -> "Table3").
FULLWIDTH_ALNUM = set(_r(0xFF10, 0xFF19)) | set(_r(0xFF21, 0xFF3A)) | set(_r(0xFF41, 0xFF5A))

# Cyrillic / Greek letters that render like Latin ones. Only a word that mixes
# them with >= 2 ASCII letters is flagged ("Тhе" with Cyrillic Т and е); a word
# with no Latin letters (a Russian citation, a standalone β) is never touched.
HOMOGLYPHS = {
    # Cyrillic
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "і": "i", "ј": "j",
    "һ": "h", "ѕ": "s", "ԁ": "d", "ӏ": "l", "ԛ": "q", "ԝ": "w",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P", "С": "C",
    "Т": "T", "У": "Y", "Х": "X", "І": "I", "Ј": "J", "Ѕ": "S",
    # Greek (capitals plus omicron; μ, β, Δ and friends are notation, not look-alikes)
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K", "Μ": "M", "Ν": "N",
    "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X", "ο": "o",
}
_HOMO_WORD = re.compile(r"[A-Za-zͰ-ϿЀ-ԯ]+")
_MATH_SPANS = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$|\\\(.*?\\\)|\\\[.*?\\\]"
                         r"|\\begin\{(equation|align|gather|multline|eqnarray)\*?\}.*?\\end\{\1\*?\}", re.S)

# Model vendors that show up in exported file names ("claude_draft_v2.docx").
_VENDOR_NAME = re.compile(r"(?i)chat-?gpt|claude|gemini|deepseek|kimi|qwen|doubao|copilot|grok|\bgpt-?\d|perplexity")

# Script ranges used for the context rules.
RTL_RANGES = [_r(0x0590, 0x05FF), _r(0x0600, 0x06FF), _r(0x0700, 0x074F), _r(0x0750, 0x077F),
              _r(0x0780, 0x07BF), _r(0x07C0, 0x07FF), _r(0x0800, 0x083F), _r(0x08A0, 0x08FF),
              _r(0xFB1D, 0xFDFF), _r(0xFE70, 0xFEFF)]
JOINER_SCRIPT_RANGES = [_r(0x0600, 0x06FF), _r(0x0700, 0x074F), _r(0x0750, 0x077F),
                        _r(0x08A0, 0x08FF), _r(0xFB50, 0xFDFF), _r(0xFE70, 0xFEFF),
                        _r(0x0900, 0x0DFF), _r(0x0F00, 0x0FFF), _r(0x1000, 0x109F),
                        _r(0x1780, 0x17FF), _r(0x1800, 0x18AF)]
ZWSP_SCRIPT_RANGES = [_r(0x0E00, 0x0E7F), _r(0x0E80, 0x0EFF), _r(0x1000, 0x109F),
                      _r(0x1780, 0x17FF), _r(0x0F00, 0x0FFF)]
HANGUL_RANGES = [_r(0x1100, 0x11FF), _r(0x3130, 0x318F), _r(0xA960, 0xA97F),
                 _r(0xAC00, 0xD7AF), _r(0xD7B0, 0xD7FF), _r(0xFFA0, 0xFFDC)]
MONGOLIAN_RANGES = [_r(0x1800, 0x18AF), _r(0x11660, 0x1167F)]
CJK_RANGES = [_r(0x3400, 0x4DBF), _r(0x4E00, 0x9FFF), _r(0xF900, 0xFAFF), _r(0x20000, 0x323AF),
              _r(0x2E80, 0x2FDF), _r(0x3000, 0x303F), _r(0x3040, 0x30FF), _r(0x31F0, 0x31FF),
              _r(0xFF00, 0xFFEF)]
MATH_SYMBOL_RANGES = [_r(0x2200, 0x22FF), _r(0x27C0, 0x27EF), _r(0x2980, 0x29FF), _r(0x2A00, 0x2AFF)]
EMOJI_RANGES = [_r(0x1F000, 0x1FAFF), _r(0x2600, 0x27BF), _r(0x2B00, 0x2BFF), _r(0x2300, 0x23FF),
                _r(0x2190, 0x21FF), _r(0x25A0, 0x25FF), _r(0x2900, 0x297F), _r(0x3030, 0x303D),
                _r(0x3297, 0x3299), _r(0x1F1E6, 0x1F1FF)]
KEYCAP_BASES = set(_r(0x30, 0x39)) | {0x23, 0x2A, 0xA9, 0xAE, 0x203C, 0x2049, 0x2122, 0x2139, 0x24C2}
SUBDIVISION_FLAG_BASE = 0x1F3F4

CURLY_QUOTES = {0x2018: "'", 0x2019: "'", 0x201A: "'", 0x201B: "'",
                0x201C: '"', 0x201D: '"', 0x201E: '"', 0x201F: '"'}
ELLIPSIS = 0x2026
EM_DASH = 0x2014


def _in(cp: int, ranges: Iterable[range]) -> bool:
    return any(cp in r for r in ranges)


def cp_name(cp: int) -> str:
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        if cp in TAGS:
            return "TAG CHARACTER"
        if cp in STRIP_ALWAYS:
            return "UNASSIGNED / NONCHARACTER"
        if cp in CONTROLS:
            return "CONTROL"
        if cp in SCRIPT_FORMAT_ALL:
            return "SCRIPT FORMAT CHARACTER"
        if cp == 0x09:
            return "CHARACTER TABULATION"
        return "UNNAMED"


def detect_lang(text: str) -> str:
    """'zh' when CJK letters make up >= 30% of letters, else 'en'."""
    cjk = latin = 0
    for ch in text:
        cp = ord(ch)
        if _in(cp, CJK_RANGES[:4]):
            cjk += 1
        elif ch.isalpha() and cp < 0x0250:
            latin += 1
    total = cjk + latin
    if total == 0:
        return "en"
    return "zh" if cjk / total >= 0.30 else "en"


# --------------------------------------------------------------------------- #
# Layer A — text cleaning
# --------------------------------------------------------------------------- #

class Findings:
    """Counter of (code point, action) plus a few contexts per code point."""

    def __init__(self, max_samples: int = 5):
        self.counts: Counter = Counter()
        self.samples: Dict[int, List[str]] = {}
        self.max_samples = max_samples

    def add(self, cp: int, action: str, context: str = "", line: int = 0) -> None:
        self.counts[(cp, action)] += 1
        if context and len(self.samples.setdefault(cp, [])) < self.max_samples:
            self.samples[cp].append(f"line {line}: {context}")

    def merge(self, other: "Findings") -> None:
        self.counts.update(other.counts)
        for cp, ctx in other.samples.items():
            slot = self.samples.setdefault(cp, [])
            for c in ctx:
                if len(slot) < self.max_samples:
                    slot.append(c)

    def changed(self) -> int:
        return sum(n for (cp, action), n in self.counts.items() if action not in ("kept", "review"))

    def total(self) -> int:
        return sum(self.counts.values())

    def rows(self) -> List[Tuple[int, str, int]]:
        return sorted(((cp, action, n) for (cp, action), n in self.counts.items()),
                      key=lambda r: (r[1] == "kept", r[1] == "review", -r[2], r[0]))

    def to_dict(self) -> dict:
        return {
            "rows": [{"codepoint": f"U+{cp:04X}", "name": cp_name(cp), "action": action, "count": n}
                     for cp, action, n in self.rows()],
            "samples": {f"U+{cp:04X}": ctx for cp, ctx in self.samples.items()},
        }


def _visible(ch: str) -> str:
    return f"⟨U+{ord(ch):04X}⟩"


def _context(text: str, i: int, width: int = 18) -> str:
    lo, hi = max(0, i - width), min(len(text), i + width + 1)
    out = []
    for j in range(lo, hi):
        c = text[j]
        if j == i or ord(c) in STRIP_ALWAYS or ord(c) in BIDI or ord(c) in (ZWSP, ZWNJ, ZWJ):
            out.append(_visible(c))
        elif c == "\n":
            out.append("⏎")
        else:
            out.append(c)
    return "".join(out)


def _prev_significant(text: str, i: int) -> Optional[int]:
    """Code point before i, skipping variation selectors, ZWJ and skin-tone modifiers."""
    j = i - 1
    while j >= 0:
        cp = ord(text[j])
        if cp in VS_EMOJI or cp in VS_TEXT or cp == ZWJ or 0x1F3FB <= cp <= 0x1F3FF:
            j -= 1
            continue
        return cp
    return None


def _next_significant(text: str, i: int) -> Optional[int]:
    j = i + 1
    while j < len(text):
        cp = ord(text[j])
        if cp in VS_EMOJI or cp in VS_TEXT or cp == ZWJ or 0x1F3FB <= cp <= 0x1F3FF:
            j += 1
            continue
        return cp
    return None


def _neighbors(text: str, i: int) -> Tuple[Optional[int], Optional[int]]:
    prev_cp = ord(text[i - 1]) if i > 0 else None
    next_cp = ord(text[i + 1]) if i + 1 < len(text) else None
    return prev_cp, next_cp


def _is_emoji_base(cp: Optional[int]) -> bool:
    return cp is not None and (_in(cp, EMOJI_RANGES) or cp in KEYCAP_BASES)


def _line_has_rtl(line: str) -> bool:
    return any(_in(ord(c), RTL_RANGES) for c in line)


def clean_segment(text: str, lang: str, findings: Findings, *, keep_nbsp: bool = False,
                  keep_bidi: bool = False, typography: bool = False, line_offset: int = 1,
                  fold_homoglyphs: bool = False, trailing: str = "keep") -> str:
    """Clean one prose segment. `lang` is 'zh' or 'en' (already resolved).

    trailing: what to do with spaces / tabs before a line break — 'keep'
    (docx runs, csv / tsv where a trailing tab is an empty field), 'strip', or
    'markdown' (strip, except exactly two spaces after text = a hard break).
    """
    out: List[str] = []
    line_no = line_offset
    line_start = 0
    rtl_line_cache: Dict[int, bool] = {}

    def line_has_rtl_at(pos: int) -> bool:
        if line_start not in rtl_line_cache:
            end = text.find("\n", pos)
            end = len(text) if end == -1 else end
            rtl_line_cache[line_start] = _line_has_rtl(text[line_start:end])
        return rtl_line_cache[line_start]

    n = len(text)
    i = 0
    while i < n:
        ch = text[i]
        cp = ord(ch)
        ctx = None  # lazily built

        def record(action: str) -> None:
            findings.add(cp, action, _context(text, i), line_no)

        if ch == "\n":
            if trailing != "keep":
                k = len(out)
                while k > 0 and out[k - 1] in (" ", "\t"):
                    k -= 1
                tail = out[k:]
                hard_break = (trailing == "markdown" and tail == [" ", " "]
                              and not (k > 0 and out[k - 1] == "\n"))
                if tail and not hard_break:
                    for t in tail:
                        findings.add(ord(t), "trailing → removed", _context(text, i), line_no)
                    del out[k:]
            out.append(ch)
            line_no += 1
            line_start = i + 1
            i += 1
            continue

        # --- always strip -------------------------------------------------- #
        if cp in STRIP_ALWAYS or cp in CONTROLS:
            record("removed")
            i += 1
            continue
        if cp in LINE_SEPARATORS:
            record("→ newline")
            out.append("\n")
            line_no += 1
            line_start = i + 1
            i += 1
            continue

        # --- zero-width trio ------------------------------------------------ #
        if cp == ZWSP:
            p, q = _neighbors(text, i)
            if (p is not None and _in(p, ZWSP_SCRIPT_RANGES)) or (q is not None and _in(q, ZWSP_SCRIPT_RANGES)):
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue
        if cp == ZWNJ:
            p, q = _neighbors(text, i)
            if (p is not None and _in(p, JOINER_SCRIPT_RANGES)) or (q is not None and _in(q, JOINER_SCRIPT_RANGES)):
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue
        if cp == ZWJ:
            p, q = _prev_significant(text, i), _next_significant(text, i)
            emoji_seq = _is_emoji_base(p) and _is_emoji_base(q)
            script_seq = (p is not None and _in(p, JOINER_SCRIPT_RANGES)) or (q is not None and _in(q, JOINER_SCRIPT_RANGES))
            if emoji_seq or script_seq:
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue

        # --- bidi controls -------------------------------------------------- #
        if cp in BIDI:
            if keep_bidi or line_has_rtl_at(i):
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue

        # --- tag characters (only legal inside a subdivision flag) ---------- #
        if cp in TAGS:
            j = i - 1
            while j >= 0 and ord(text[j]) in TAGS:
                j -= 1
            if j >= 0 and ord(text[j]) == SUBDIVISION_FLAG_BASE:
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue

        # --- variation selectors ------------------------------------------- #
        if cp in VS_TEXT or cp in VS_EMOJI or cp in IVS:
            p = ord(text[i - 1]) if i > 0 else None
            keep = False
            if p is not None:
                if cp in IVS:
                    keep = _in(p, CJK_RANGES[:4])
                elif cp in VS_EMOJI:
                    keep = _is_emoji_base(p) or _in(p, CJK_RANGES) or _in(p, MATH_SYMBOL_RANGES)
                else:  # VS1–VS14
                    keep = _in(p, CJK_RANGES) or _in(p, MATH_SYMBOL_RANGES) or _in(p, EMOJI_RANGES)
            if keep:
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue

        # --- Mongolian / Hangul fillers ------------------------------------ #
        if cp in MONGOLIAN_FVS:
            p, q = _neighbors(text, i)
            if (p is not None and _in(p, MONGOLIAN_RANGES)) or (q is not None and _in(q, MONGOLIAN_RANGES)):
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue
        if cp in HANGUL_FILLERS:
            p, q = _neighbors(text, i)
            if (p is not None and _in(p, HANGUL_RANGES)) or (q is not None and _in(q, HANGUL_RANGES)):
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue

        # --- script-bound format characters -------------------------------- #
        if cp in SCRIPT_FORMAT_ALL:
            p, q = _neighbors(text, i)
            ranges = next(rs for s, rs in SCRIPT_FORMAT if cp in s)
            if (p is not None and _in(p, ranges)) or (q is not None and _in(q, ranges)):
                record("kept")
                out.append(ch)
            else:
                record("removed")
            i += 1
            continue

        # --- canonical look-alikes (lossless, NFC-equivalent) -------------- #
        if cp in CANONICAL_SINGLETONS:
            record("→ canonical")
            out.append(CANONICAL_SINGLETONS[cp])
            i += 1
            continue

        # --- fullwidth Latin inside an ASCII word (EN only) ---------------- #
        if lang == "en" and cp in FULLWIDTH_ALNUM:
            p = text[i - 1] if i > 0 else ""
            q = text[i + 1] if i + 1 < n else ""
            if (p.isascii() and p.isalnum()) or (q.isascii() and q.isalnum()):
                record("→ ASCII")
                out.append(chr(cp - 0xFEE0))
                i += 1
                continue

        # --- spaces --------------------------------------------------------- #
        if cp in SPACE_HOMOGLYPHS:
            record("→ U+0020")
            out.append(" ")
            i += 1
            continue
        if cp == NBSP:
            if keep_nbsp:
                record("kept")
                out.append(ch)
            else:
                record("→ U+0020")
                out.append(" ")
            i += 1
            continue
        if cp == IDEOGRAPHIC_SPACE:
            p, q = _neighbors(text, i)
            cjk_adjacent = (p is not None and _in(p, CJK_RANGES)) or (q is not None and _in(q, CJK_RANGES))
            if lang == "zh" or cjk_adjacent:
                record("kept")
                out.append(ch)
            else:
                record("→ U+0020")
                out.append(" ")
            i += 1
            continue

        # --- typography (English only, opt-in; dashes are never touched) --- #
        if lang == "en":
            if cp == EM_DASH:
                record("review")           # EN20: author decides comma / parenthesis / period
                out.append(ch)
                i += 1
                continue
            if typography and cp in CURLY_QUOTES:
                record("→ straight quote")
                out.append(CURLY_QUOTES[cp])
                i += 1
                continue
            if typography and cp == ELLIPSIS:
                record("→ ...")
                out.append("...")
                i += 1
                continue

        out.append(ch)
        i += 1

    return _homoglyph_pass("".join(out), findings, fold_homoglyphs, line_offset)


def _homoglyph_pass(text: str, findings: Findings, fold: bool, line_offset: int = 1) -> str:
    """Flag (and with `fold`, repair) Latin words carrying Cyrillic / Greek
    look-alike letters. Math spans are skipped so notation survives."""
    if not any(ch in HOMOGLYPHS for ch in text):
        return text
    masked = [(m.start(), m.end()) for m in _MATH_SPANS.finditer(text)]
    out = list(text)
    for m in _HOMO_WORD.finditer(text):
        if any(a <= m.start() < b for a, b in masked):
            continue
        word = m.group(0)
        latin = sum(1 for c in word if c.isascii())
        foreign = [c for c in word if not c.isascii()]
        if latin < 2 or not foreign or any(c not in HOMOGLYPHS for c in foreign):
            continue
        line_no = line_offset + text.count("\n", 0, m.start())
        for k, c in enumerate(word):
            if c in HOMOGLYPHS:
                findings.add(ord(c), "→ Latin (homoglyph)" if fold else "review (homoglyph)",
                             _context(text, m.start() + k), line_no)
                if fold:
                    out[m.start() + k] = HOMOGLYPHS[c]
    return "".join(out)


_MD_CODE = re.compile(r"(^```.*?^```[ \t]*$|^~~~.*?^~~~[ \t]*$|`[^`\n]*`)", re.S | re.M)
_HTML_CODE = re.compile(r"(<pre\b.*?</pre>|<code\b.*?</code>|<script\b.*?</script>|<style\b.*?</style>)", re.S | re.I)


def clean_text(text: str, lang: str = "auto", *, fmt: str = "text", keep_nbsp: bool = False,
               keep_bidi: bool = False, typography: bool = False, fold_homoglyphs: bool = False,
               trailing: Optional[str] = None) -> Tuple[str, Findings, str]:
    """Clean a whole document. Returns (cleaned, findings, resolved_lang).

    fmt: 'text' | 'markdown' | 'html'. Code spans/blocks are left untouched in
    markdown and html so that a document *about* invisible characters keeps
    its own examples. `trailing` defaults to 'markdown' for markdown and
    'strip' otherwise; callers pass 'keep' for csv / tsv.
    """
    resolved = detect_lang(text) if lang == "auto" else lang
    findings = Findings()
    if trailing is None:
        trailing = "markdown" if fmt == "markdown" else "strip"
    opts = dict(keep_nbsp=keep_nbsp, keep_bidi=keep_bidi, typography=typography,
                fold_homoglyphs=fold_homoglyphs, trailing=trailing)
    if fmt == "markdown":
        splitter = _MD_CODE
    elif fmt == "html":
        splitter = _HTML_CODE
    else:
        splitter = None

    if splitter is None:
        cleaned = clean_segment(text, resolved, findings, **opts)
        return cleaned, findings, resolved

    parts = splitter.split(text)
    out: List[str] = []
    line_no = 1
    for k, part in enumerate(parts):
        if k % 2 == 1:  # a code span / block captured by the splitter
            out.append(part)
        else:
            out.append(clean_segment(part, resolved, findings, line_offset=line_no, **opts))
        line_no += part.count("\n")
    return "".join(out), findings, resolved


# --------------------------------------------------------------------------- #
# Layer C — containers
# --------------------------------------------------------------------------- #

_WT = re.compile(r"(<w:t(?:\s[^>]*)?>)(.*?)(</w:t>)", re.S)
_NCR = re.compile(r"&#(?:x([0-9A-Fa-f]+)|([0-9]+));")
_DOCX_TEXT_PARTS = re.compile(r"^word/(document|footnotes|endnotes|comments|header\d*|footer\d*)\.xml$")
_CORE_FIELDS = ("dc:creator", "cp:lastModifiedBy", "dc:description", "cp:category", "cp:contentStatus")
_APP_FIELDS = ("Company", "Manager", "HyperlinkBase")


def _decode_target_ncrs(xml: str) -> str:
    """Turn numeric character references for carrier code points into literal
    characters so the context-aware cleaner can judge them. Named entities and
    ordinary characters are left alone."""
    def sub(m: "re.Match[str]") -> str:
        cp = int(m.group(1), 16) if m.group(1) else int(m.group(2))
        if (cp in STRIP_ALWAYS or cp in BIDI or cp in TAGS or cp in VS_TEXT or cp in VS_EMOJI
                or cp in IVS or cp in SPACE_HOMOGLYPHS or cp in (ZWSP, ZWNJ, ZWJ, NBSP, IDEOGRAPHIC_SPACE)
                or cp in HANGUL_FILLERS or cp in MONGOLIAN_FVS or cp in LINE_SEPARATORS
                or cp in SCRIPT_FORMAT_ALL or cp in CANONICAL_SINGLETONS):
            try:
                return chr(cp)
            except (ValueError, OverflowError):
                return m.group(0)
        return m.group(0)
    return _NCR.sub(sub, xml)


def _xml_field(xml: str, tag: str) -> Optional[str]:
    m = re.search(rf"<{re.escape(tag)}(?:\s[^>]*)?>(.*?)</{re.escape(tag)}>", xml, re.S)
    return None if m is None else m.group(1)


def _blank_xml_field(xml: str, tag: str) -> Tuple[str, Optional[str]]:
    old = _xml_field(xml, tag)
    if old is None or old == "":
        return xml, old
    new = re.sub(rf"(<{re.escape(tag)}(?:\s[^>]*)?>)(.*?)(</{re.escape(tag)}>)", r"\1\3", xml, count=1, flags=re.S)
    return new, old


_RSID_ATTR = re.compile(r'\s+w:rsid[A-Za-z]*="[0-9A-Fa-f]{8}"')
_RSIDS_BLOCK = re.compile(r"<w:rsids>.*?</w:rsids>", re.S)
_RSID_PARTS = re.compile(r"^word/(document|styles|numbering|footnotes|endnotes|comments|settings|header\d*|footer\d*)\.xml$")
_MEDIA = re.compile(r"^(?:word|ppt|xl)/media/[^/]+\.(png|jpe?g)$", re.I)
_TEMPLATE_REL = re.compile(r'(<Relationship\b[^>]*Type="[^"]*/attachedTemplate"[^>]*Target=")([^"]*)(")')
_CUSTOM_PROP = re.compile(r'<property\b[^>]*\bname="([^"]*)"[^>]*>.*?</property>', re.S)
# Custom properties that identify a person or tenant and do nothing for the
# manuscript: Microsoft sensitivity labels (owner e-mail, tenant id) and WPS
# build stamps. Zotero / Mendeley properties are kept — citations need them.
_CUSTOM_DROP = re.compile(r"^(MSIP_Label_|KSOProductBuildVer$|ICV$)")


def process_docx(data: bytes, lang: str, *, keep_nbsp: bool, keep_bidi: bool, typography: bool,
                 scrub_meta: bool, do_clean: bool, fold_homoglyphs: bool = False
                 ) -> Tuple[bytes, Findings, dict, str]:
    """Inspect or clean a .docx. Returns (new_bytes, text_findings, meta_report, lang)."""
    findings = Findings()
    meta: "OrderedDict[str, object]" = OrderedDict()
    zin = zipfile.ZipFile(io.BytesIO(data))
    names = zin.namelist()
    replacements: Dict[str, bytes] = {}

    def current(name: str) -> str:
        return replacements[name].decode("utf-8") if name in replacements else zin.read(name).decode("utf-8")

    # Resolve language from all text runs first.
    if lang == "auto":
        corpus = []
        for name in names:
            if _DOCX_TEXT_PARTS.match(name):
                corpus.extend(m.group(2) for m in _WT.finditer(zin.read(name).decode("utf-8", "replace")))
        lang = detect_lang("".join(corpus))

    for name in names:
        if _DOCX_TEXT_PARTS.match(name):
            xml = zin.read(name).decode("utf-8")
            xml = _decode_target_ncrs(xml)
            part_findings = Findings()

            def sub(m: "re.Match[str]", _pf: Findings = part_findings) -> str:
                cleaned = clean_segment(m.group(2), lang, _pf, keep_nbsp=keep_nbsp, keep_bidi=keep_bidi,
                                        typography=typography, fold_homoglyphs=fold_homoglyphs)
                return m.group(1) + cleaned + m.group(3)

            new_xml = _WT.sub(sub, xml)
            findings.merge(part_findings)
            if do_clean and new_xml != xml:
                replacements[name] = new_xml.encode("utf-8")
            if name == "word/document.xml":
                meta["tracked_changes"] = len(re.findall(r"<w:(?:ins|del)\b", xml))
                meta["comment_anchors"] = len(re.findall(r"<w:commentRangeStart\b", xml))

    if "docProps/core.xml" in names:
        core = zin.read("docProps/core.xml").decode("utf-8")
        fields: Dict[str, Optional[str]] = OrderedDict()
        for tag in _CORE_FIELDS:
            fields[tag] = _xml_field(core, tag)
        meta["core"] = fields
        if do_clean and scrub_meta:
            new_core = core
            for tag in _CORE_FIELDS:
                new_core, _ = _blank_xml_field(new_core, tag)
            if new_core != core:
                replacements["docProps/core.xml"] = new_core.encode("utf-8")
                meta["core_scrubbed"] = [t for t in _CORE_FIELDS if fields.get(t)]
    if "docProps/app.xml" in names:
        app = zin.read("docProps/app.xml").decode("utf-8")
        fields = OrderedDict()
        fields["Application"] = _xml_field(app, "Application")
        for tag in _APP_FIELDS:
            fields[tag] = _xml_field(app, tag)
        meta["app"] = fields
        if do_clean and scrub_meta:
            new_app = app
            for tag in _APP_FIELDS:
                new_app, _ = _blank_xml_field(new_app, tag)
            if new_app != app:
                replacements["docProps/app.xml"] = new_app.encode("utf-8")
                meta["app_scrubbed"] = [t for t in _APP_FIELDS if fields.get(t)]
    if "docProps/custom.xml" in names:
        custom = zin.read("docProps/custom.xml").decode("utf-8")
        props = [m.group(1) for m in _CUSTOM_PROP.finditer(custom)]
        meta["custom_properties"] = props
        drop = [p for p in props if _CUSTOM_DROP.match(p)]
        meta["custom_identifying"] = drop
        if do_clean and scrub_meta and drop:
            new_custom = _CUSTOM_PROP.sub(lambda m: "" if _CUSTOM_DROP.match(m.group(1)) else m.group(0), custom)
            replacements["docProps/custom.xml"] = new_custom.encode("utf-8")
            meta["custom_scrubbed"] = drop

    # Revision-session ids: stable per editing session and per machine, so they
    # can link an anonymised submission to the author's other files.
    rsid_count = 0
    for name in names:
        if _RSID_PARTS.match(name):
            xml = current(name)
            n_attr = len(_RSID_ATTR.findall(xml))
            n_block = len(_RSIDS_BLOCK.findall(xml))
            rsid_count += n_attr + n_block
            if do_clean and scrub_meta and (n_attr or n_block):
                replacements[name] = _RSIDS_BLOCK.sub("", _RSID_ATTR.sub("", xml)).encode("utf-8")
    meta["rsid_marks"] = rsid_count
    if do_clean and scrub_meta and rsid_count:
        meta["rsid_scrubbed"] = rsid_count

    # Attached template path, e.g. C:\Users\<name>\AppData\...\Normal.dotm.
    rels = "word/_rels/settings.xml.rels"
    if rels in names:
        xml = zin.read(rels).decode("utf-8")
        m = _TEMPLATE_REL.search(xml)
        if m and re.search(r"[\\/]", m.group(2)):
            meta["attached_template"] = m.group(2)
            if do_clean and scrub_meta:
                base = re.split(r"[\\/]", m.group(2))[-1]
                replacements[rels] = _TEMPLATE_REL.sub(lambda mm: mm.group(1) + base + mm.group(3), xml).encode("utf-8")
                meta["attached_template_scrubbed"] = base

    # Figures pasted into the document keep their own C2PA / EXIF / XMP.
    media: "OrderedDict[str, List[str]]" = OrderedDict()
    for name in names:
        mm = _MEDIA.match(name)
        if not mm:
            continue
        blob = zin.read(name)
        try:
            if mm.group(1).lower() == "png":
                new_blob, rep = process_png(blob, do_clean=do_clean and scrub_meta)
            else:
                new_blob, rep = process_jpeg(blob, do_clean=do_clean and scrub_meta)
        except ValueError:
            continue
        if rep.get("metadata_found"):
            media[name] = rep["metadata_found"]
            if do_clean and scrub_meta and new_blob != blob:
                replacements[name] = new_blob
                meta["embedded_media_scrubbed"] = sorted(set(meta.get("embedded_media_scrubbed", [])) | {name})
    meta["embedded_media_metadata"] = media
    meta["embedded_c2pa"] = [k for k, v in media.items() if any(x.startswith("C2PA") for x in v)]

    meta["custom_xml_parts"] = sorted(n for n in names if n.startswith("customXml/") and n.endswith(".xml"))
    meta["has_comments"] = "word/comments.xml" in names
    meta["has_people"] = "word/people.xml" in names
    meta["thumbnail"] = next((n for n in names if n.startswith("docProps/thumbnail")), None)

    if not do_clean or not replacements:
        return data, findings, meta, lang

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        for info in zin.infolist():
            payload = replacements.get(info.filename, zin.read(info.filename))
            new_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            new_info.compress_type = info.compress_type
            new_info.external_attr = info.external_attr
            zout.writestr(new_info, payload)
    return buf.getvalue(), findings, meta, lang


# ---- PNG ------------------------------------------------------------------ #

PNG_SIG = b"\x89PNG\r\n\x1a\n"
PNG_KEEP = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM", b"sRGB", b"iCCP",
            b"sBIT", b"bKGD", b"pHYs", b"hIST", b"sPLT", b"acTL", b"fcTL", b"fdAT"}


def _png_chunk_label(ctype: bytes, body: bytes) -> str:
    if ctype == b"caBX":
        return "C2PA manifest (JUMBF)"
    if ctype == b"eXIf":
        return "EXIF"
    if ctype in (b"tEXt", b"zTXt", b"iTXt"):
        key = body.split(b"\x00", 1)[0].decode("latin-1", "replace")
        if key == "XML:com.adobe.xmp":
            return "XMP"
        return f"{ctype.decode()} '{key}'"
    if ctype == b"tIME":
        return "tIME"
    return ctype.decode("latin-1", "replace")


def process_png(data: bytes, *, do_clean: bool) -> Tuple[bytes, dict]:
    if not data.startswith(PNG_SIG):
        raise ValueError("not a PNG file")
    pos = len(PNG_SIG)
    out = [PNG_SIG]
    dropped: List[str] = []
    kept_meta: List[str] = []
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 12 + length
        chunk = data[pos:end]
        body = data[pos + 8:pos + 8 + length]
        ancillary = bool(ctype[0] & 0x20)
        if ctype in PNG_KEEP or not ancillary:
            out.append(chunk)
            if ctype not in PNG_KEEP:
                kept_meta.append(ctype.decode("latin-1", "replace"))
        else:
            dropped.append(_png_chunk_label(ctype, body))
        pos = end
        if ctype == b"IEND":
            break
    trailing = data[pos:]
    report = {"format": "png", "metadata_found": list(dropped), "kept_unknown_critical": kept_meta,
              "trailing_bytes": len(trailing), "c2pa": any(d.startswith("C2PA") for d in dropped)}
    if not do_clean:
        return data, report
    if trailing:
        report["trailing_bytes_dropped"] = len(trailing)
    return b"".join(out), report


# ---- JPEG ----------------------------------------------------------------- #

def _jpeg_app_label(marker: int, body: bytes) -> str:
    head = body[:32]
    if marker == 0xE1 and head.startswith(b"Exif\x00"):
        return "EXIF (APP1)"
    if marker == 0xE1 and head.startswith(b"http://ns.adobe.com/xap/1.0/"):
        return "XMP (APP1)"
    if marker == 0xE1 and head.startswith(b"http://ns.adobe.com/xmp/extension/"):
        return "XMP extension (APP1)"
    if marker == 0xEB and (b"jumb" in body[:64] or b"JP" in head[:4] or b"c2pa" in body[:256].lower()):
        return "C2PA manifest (APP11 JUMBF)"
    if marker == 0xEB:
        return "APP11 (JUMBF?)"
    if marker == 0xED and head.startswith(b"Photoshop 3.0"):
        return "IPTC / Photoshop (APP13)"
    if marker == 0xFE:
        return "COM comment"
    return f"APP{marker - 0xE0}"


def process_jpeg(data: bytes, *, do_clean: bool) -> Tuple[bytes, dict]:
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("not a JPEG file")
    pos = 2
    out = [b"\xff\xd8"]
    dropped: List[str] = []
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            break
        marker = data[pos + 1]
        if marker == 0xD8 or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            out.append(data[pos:pos + 2])
            pos += 2
            continue
        if marker == 0xDA:  # start of scan: copy the rest verbatim
            out.append(data[pos:])
            pos = len(data)
            break
        seg_len = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        seg = data[pos:pos + 2 + seg_len]
        body = data[pos + 4:pos + 2 + seg_len]
        keep = True
        if 0xE0 <= marker <= 0xEF or marker == 0xFE:
            if marker == 0xE0 and body.startswith(b"JFIF"):
                keep = True
            elif marker == 0xE2 and body.startswith(b"ICC_PROFILE"):
                keep = True
            elif marker == 0xEE and body.startswith(b"Adobe"):
                keep = True
            else:
                keep = False
                dropped.append(_jpeg_app_label(marker, body))
        if keep:
            out.append(seg)
        pos += 2 + seg_len
    report = {"format": "jpeg", "metadata_found": list(dropped),
              "c2pa": any(d.startswith("C2PA") for d in dropped)}
    if not do_clean:
        return data, report
    return b"".join(out), report


# ---- SVG ------------------------------------------------------------------ #

_SVG_METADATA = re.compile(r"<metadata\b.*?</metadata>", re.S | re.I)
_SVG_COMMENT = re.compile(r"<!--.*?-->", re.S)


def process_svg(text: str, *, do_clean: bool) -> Tuple[str, dict]:
    metadata_blocks = _SVG_METADATA.findall(text)
    comments = _SVG_COMMENT.findall(text)
    generator = [c.strip() for c in comments if re.search(r"generat|created with|produced by", c, re.I)]
    c2pa = bool(re.search(r"c2pa", text, re.I))
    report = {"format": "svg", "metadata_blocks": len(metadata_blocks), "comments": len(comments),
              "generator_comments": generator[:3], "c2pa": c2pa}
    if not do_clean:
        return text, report
    cleaned = _SVG_METADATA.sub("", text)
    cleaned = _SVG_COMMENT.sub("", cleaned)
    report["c2pa_after"] = bool(re.search(r"c2pa", cleaned, re.I))
    return cleaned, report


# ---- PDF (report only) ---------------------------------------------------- #

_PDF_INFO = re.compile(rb"/(Producer|Creator|Author|Title|Subject|Keywords|CreationDate|ModDate)\s*(\((?:\\.|[^\\)]){0,300}\)|<[0-9A-Fa-f\s]{0,600}>)")


_PDF_STREAM = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)
_PDF_PTEX = re.compile(rb"/PTEX\.(FileName|InfoDict|PageNumber)")
_PDF_ABS_PATH = re.compile(rb"(?:/Users/|/home/|[A-Za-z]:\\\\?Users\\\\?)[^\s()<>/\\\\]{1,40}")


def _pdf_inflated(data: bytes, max_streams: int = 4000, max_out: int = 64 << 20) -> bytes:
    """Concatenate every Flate stream that inflates cleanly. Object streams and
    compressed XMP hide metadata from a raw-byte scan; this is the cheap fix."""
    parts: List[bytes] = []
    total = 0
    for k, m in enumerate(_PDF_STREAM.finditer(data)):
        if k >= max_streams or total >= max_out:
            break
        try:
            d = zlib.decompressobj()
            chunk = d.decompress(m.group(1), max_out - total)
        except zlib.error:
            continue
        parts.append(chunk)
        total += len(chunk)
    return b"\n".join(parts)


def inspect_pdf(data: bytes) -> dict:
    inflated = _pdf_inflated(data)
    scan = data + b"\n" + inflated
    info: Dict[str, str] = OrderedDict()
    for key, val in _PDF_INFO.findall(scan):
        k = key.decode()
        if k in info:
            continue
        if val.startswith(b"("):
            info[k] = val[1:-1].decode("latin-1", "replace")[:120]
        else:
            info[k] = "<hex string>"
    paths = sorted({p.decode("latin-1", "replace") for p in _PDF_ABS_PATH.findall(scan)})
    return {
        "format": "pdf",
        "info": info,
        "xmp": b"<x:xmpmeta" in scan or b"/Type /Metadata" in scan or b"/Type/Metadata" in scan,
        "c2pa": b"c2pa" in scan.lower() or b"jumb" in scan,
        "incremental_updates": data.count(b"%%EOF") - 1 if data.count(b"%%EOF") > 1 else 0,
        "compressed_bytes_scanned": len(inflated),
        "ptex_figure_info": len(_PDF_PTEX.findall(scan)),
        "absolute_paths": paths[:5],
    }


PDF_COMMANDS = [
    "exiftool -all= -overwrite_original {f}      # drops Info dictionary + XMP",
    "qpdf --linearize {f} {stem}.clean.pdf         # rewrites the file so old metadata is not left in an incremental update",
    "c2patool {stem}.clean.pdf                     # verify no C2PA manifest remains (official CAI tool)",
]
PDFTEX_COMMANDS = [
    "% pdfLaTeX preamble, then recompile — stops figures' own Info / file names riding along:",
    "\\pdfsuppressptexinfo=-1  \\pdftrailerid{}  \\pdfinfoomitdate=1",
]
IMAGE_VERIFY_COMMANDS = [
    "c2patool {f}                                  # confirm no manifest remains",
    "exiftool {f}                                  # confirm EXIF / XMP are gone",
    "# best practice for a paper: regenerate the figure from the replication package instead of scrubbing an exported file",
]


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

def _fmt_rows(findings: Findings) -> List[str]:
    lines = []
    for cp, action, n in findings.rows():
        lines.append(f"  U+{cp:04X} {cp_name(cp):<38.38} {n:>6}   {action}")
    return lines


def render_report(entry: dict) -> str:
    L: List[str] = []
    L.append(f"== Provenance-mark report · 溯源标记报告 · {entry['file']} ==")
    L.append(f"kind: {entry['kind']}   lang: {entry.get('lang', '-')}   mode: {entry['mode']}")
    f = entry.get("findings")
    L.append("Layer A · invisible-character carriers 隐藏字符")
    if f is None:
        L.append("  (not applicable to this format)")
    elif not f["rows"]:
        L.append("  none found")
    else:
        for r in f["rows"]:
            L.append(f"  {r['codepoint']} {r['name']:<38.38} {r['count']:>6}   {r['action']}")
        for cp, ctx in f["samples"].items():
            for c in ctx[:2]:
                L.append(f"      {cp} @ {c}")
    L.append("Layer C · container metadata 容器元数据")
    meta = entry.get("meta")
    if not meta:
        L.append("  (plain text: nothing to report)")
    else:
        for k, v in meta.items():
            if k == "members":
                for name, verdict in v.items():
                    L.append(f"  member {name}: {verdict}")
                continue
            if isinstance(v, dict):
                v = {kk: vv for kk, vv in v.items() if vv not in (None, "", [], {})}
            if v in (None, [], {}, "", 0, False):
                continue
            L.append(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
    if entry.get("commands"):
        L.append("  next commands:")
        for c in entry["commands"]:
            L.append(f"    {c}")
    L.append("Layer B · statistical watermark 统计水印: unknown — no public detector;"
             " only an author rewrite changes it (references/watermarks.md §4)")
    L.append(f"verdict: {entry['verdict']}")
    return "\n".join(L)


def _is_review(action: str) -> bool:
    return action.startswith("review")


def _docx_flags(meta: dict) -> List[str]:
    flagged = [k for k in ("has_comments", "has_people", "custom_xml_parts", "thumbnail",
                           "custom_identifying", "embedded_c2pa", "attached_template") if meta.get(k)]
    if meta.get("tracked_changes"):
        flagged.append("tracked_changes")
    if meta.get("rsid_marks"):
        flagged.append("rsid_marks")
    if meta.get("embedded_media_metadata") and not meta.get("embedded_c2pa"):
        flagged.append("embedded_media_metadata")
    return flagged


def _verdict(entry: dict) -> str:
    a = entry.get("findings")
    a_changed = sum(r["count"] for r in a["rows"] if r["action"] != "kept" and not _is_review(r["action"])) if a else 0
    a_dash = sum(r["count"] for r in a["rows"] if r["action"] == "review") if a else 0
    a_homo = sum(r["count"] for r in a["rows"] if r["action"] == "review (homoglyph)") if a else 0
    parts = []
    if entry["mode"] == "inspect":
        parts.append(f"A: {a_changed} carrier(s) to clean" if a_changed else "A: clean")
    else:
        parts.append(f"A: {a_changed} carrier(s) cleaned" if a_changed else "A: nothing to clean")
    if a_dash:
        parts.append(f"{a_dash} em dash(es) left for EN20 review")
    if a_homo:
        parts.append(f"{a_homo} look-alike letter(s) in Latin words — review, or re-run with --fold-homoglyphs")
    meta = entry.get("meta") or {}
    if entry["kind"] == "docx":
        flagged = _docx_flags(meta)
        core = meta.get("core") or {}
        app = meta.get("app") or {}
        props_present = any(core.get(k) for k in _CORE_FIELDS) or any(app.get(k) for k in _APP_FIELDS)
        if entry["mode"] == "clean":
            done = [k for k in ("core_scrubbed", "app_scrubbed", "custom_scrubbed", "rsid_scrubbed",
                                "attached_template_scrubbed", "embedded_media_scrubbed") if meta.get(k)]
            head = "scrubbed " + ", ".join(d.replace("_scrubbed", "") for d in done) if done else "docProps already clean"
            # what clean already handled is not left for review
            handled = {flag for flag, done_key in (("custom_identifying", "custom_scrubbed"),
                                                   ("rsid_marks", "rsid_scrubbed"),
                                                   ("attached_template", "attached_template_scrubbed"),
                                                   ("embedded_c2pa", "embedded_media_scrubbed"),
                                                   ("embedded_media_metadata", "embedded_media_scrubbed"))
                       if meta.get(done_key)}
            flagged = [k for k in flagged if k not in handled]
        else:
            head = "docProps carry author / generator fields" if props_present else "docProps clean"
        parts.append("C: " + head + ("; still review " + ", ".join(flagged) if flagged else ""))
    elif entry["kind"] in ("png", "jpeg"):
        found = meta.get("metadata_found") or []
        parts.append(("C: dropped " if entry["mode"] == "clean" else "C: found ") + (", ".join(found) if found else "no metadata segments"))
    elif entry["kind"] == "svg":
        parts.append(f"C: {meta.get('metadata_blocks', 0)} metadata block(s), {meta.get('comments', 0)} comment(s)"
                     + (" — c2pa string present" if meta.get("c2pa") else ""))
    elif entry["kind"] == "pdf":
        parts.append("C: report only — run the listed commands")
    elif entry["kind"] == "zip":
        junk = meta.get("junk_removed") if entry["mode"] == "clean" else len(meta.get("junk_entries") or [])
        word = "removed" if entry["mode"] == "clean" else "found"
        bits = [f"{junk} __MACOSX / .DS_Store entr(ies) {word}"] if junk else []
        bits.append(f"{len(meta.get('members_with_findings') or [])} member(s) with findings")
        parts.append("C: " + "; ".join(bits))
    elif meta.get("generator_markers") or meta.get("whitespace_pattern"):
        parts.append("C: " + "; ".join(x for x in (
            "generator stamp(s) in the source — remove by hand" if meta.get("generator_markers") else "",
            "trailing-whitespace pattern" if meta.get("whitespace_pattern") else "") if x))
    if meta.get("file_name_mentions_model"):
        parts.append("file name names a model vendor — rename before submission")
    if meta.get("macos_xattrs"):
        parts.append("macOS xattrs (download origin) — xattr -c")
    parts.append("B: unknown")
    return " · ".join(parts)


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def _kind_of(path: Path, data: bytes) -> str:
    suf = path.suffix.lower()
    if suf == ".docx":
        return "docx"
    if suf == ".zip":
        return "zip"
    if suf == ".png" or data.startswith(PNG_SIG):
        return "png"
    if suf in (".jpg", ".jpeg") or data.startswith(b"\xff\xd8"):
        return "jpeg"
    if suf == ".svg":
        return "svg"
    if suf == ".pdf" or data.startswith(b"%PDF"):
        return "pdf"
    if suf in MARKDOWN_SUFFIXES:
        return "markdown"
    if suf in HTML_SUFFIXES:
        return "html"
    return "text"


# Generator stamps left in source files by export tools and chat UIs. Reported,
# never auto-removed: front matter may be load-bearing for the build.
_GEN_MARKERS = [
    re.compile(r"(?mi)\A---[ \t]*\n(?:(?!---).*\n)*?[ \t]*(generator|model|llm|ai_generated|ai-generated|created_by)[ \t]*:.*$"),
    re.compile(r"(?i)<meta\s+name=[\"']generator[\"'][^>]*>"),
    re.compile(r"(?i)<!--\s*(?:generated|created|written)\s+(?:by|with)\b[^>]{0,80}-->"),
    re.compile(r"(?im)^\s*(?:%|#|//)?\s*(?:generated|created|written|drafted)\s+(?:by|with|using)\s+"
               r"(?:chat-?gpt|claude|gemini|deepseek|kimi|qwen|doubao|copilot|gpt-?\d)[^\n]{0,60}$"),
]


def _generator_markers(text: str) -> List[str]:
    hits: List[str] = []
    for rx in _GEN_MARKERS:
        for m in rx.finditer(text):
            hits.append(m.group(0).strip().splitlines()[-1][:100])
    return hits[:5]


def _whitespace_pattern(text: str) -> Optional[str]:
    """SNOW-style steganography hides bits in trailing spaces / tabs. One or two
    stray trailing spaces are ordinary; many of varying length, or a tab / space
    mix, are a pattern worth a human look."""
    tails = [m.group(0) for m in re.finditer(r"[ \t]+(?=\n)", text)]
    tails = [t for t in tails if t != "  "]  # markdown hard breaks
    if len(tails) >= 3 and (len(set(tails)) >= 2 or any("\t" in t for t in tails)):
        return (f"{len(tails)} lines end in spaces / tabs of {len(set(tails))} different shapes — "
                "possible whitespace steganography (SNOW-style); cleaned by `clean`")
    return None


def _xattrs(path: Path) -> List[str]:
    """macOS extended attributes such as kMDItemWhereFroms (the download URL)
    and com.apple.quarantine. Report only; `xattr -c` removes them."""
    if sys.platform != "darwin" or not path.is_file():
        return []
    try:
        out = subprocess.run(["xattr", str(path)], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return []
    keep = ("com.apple.quarantine", "com.apple.metadata:kMDItemWhereFroms",
            "com.apple.metadata:kMDItemDownloadedDate", "com.apple.metadata:kMDItemCreator")
    return [a for a in out.stdout.split() if a in keep]


_ZIP_JUNK = re.compile(r"(^|/)(__MACOSX/|\.DS_Store$|Thumbs\.db$|desktop\.ini$)")


def process_zip(data: bytes, mode: str, args: argparse.Namespace) -> Tuple[bytes, dict]:
    """A submission package. AppleDouble entries (__MACOSX/._*) carry the
    extended attributes — including the download URL — of every file; members
    of a known kind are inspected / cleaned in memory like standalone files."""
    zin = zipfile.ZipFile(io.BytesIO(data))
    junk = [n for n in zin.namelist() if _ZIP_JUNK.search(n)]
    members: "OrderedDict[str, str]" = OrderedDict()
    flagged: List[str] = []
    replacements: Dict[str, bytes] = {}
    for info in zin.infolist():
        name = info.filename
        if name.endswith("/") or name in junk:
            continue
        p = Path(name)
        if _kind_of(p, b"") == "text" and p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            entry, new_bytes = process_bytes(p, zin.read(name), mode, args, label=name)
        except (ValueError, zipfile.BadZipFile, UnicodeDecodeError):
            continue
        members[name] = entry["verdict"]
        if _has_findings(entry):
            flagged.append(name)
        if mode == "clean" and new_bytes is not None and new_bytes != zin.read(name):
            replacements[name] = new_bytes
    meta: "OrderedDict[str, object]" = OrderedDict()
    meta["format"] = "zip"
    meta["junk_entries"] = junk[:10] + (["…"] if len(junk) > 10 else [])
    meta["members_with_findings"] = flagged
    meta["members"] = members
    if mode != "clean":
        return data, meta
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        for info in zin.infolist():
            if info.filename in junk:
                continue
            payload = replacements.get(info.filename, zin.read(info.filename))
            new_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            new_info.compress_type = info.compress_type
            new_info.external_attr = info.external_attr
            zout.writestr(new_info, payload)
    meta["junk_removed"] = len(junk)
    return buf.getvalue(), meta


def process_path(path: Path, mode: str, args: argparse.Namespace) -> Tuple[dict, Optional[bytes]]:
    data = sys.stdin.buffer.read() if str(path) == "-" else path.read_bytes()
    entry, new_bytes = process_bytes(path, data, mode, args)
    if str(path) != "-":
        attrs = _xattrs(path)
        if attrs:
            entry["meta"] = entry.get("meta") or OrderedDict()
            entry["meta"]["macos_xattrs"] = attrs
            entry.setdefault("commands", []).append(f"xattr -c {path.name}   # drop download URL / quarantine stamps")
            entry["verdict"] = _verdict(entry)
    return entry, new_bytes


def process_bytes(path: Path, data: bytes, mode: str, args: argparse.Namespace,
                  label: Optional[str] = None) -> Tuple[dict, Optional[bytes]]:
    kind = _kind_of(path, data) if str(path) != "-" else "text"
    do_clean = mode == "clean"
    fold = getattr(args, "fold_homoglyphs", False)
    entry: dict = {"file": label or str(path), "kind": kind, "mode": mode}
    new_bytes: Optional[bytes] = None

    if kind in ("text", "markdown", "html", "svg"):
        text = data.decode("utf-8-sig") if data[:3] == b"\xef\xbb\xbf" else data.decode("utf-8")
        if kind == "svg":
            cleaned, meta = process_svg(text, do_clean=do_clean)
            entry["meta"] = meta
            entry["lang"] = "-"
            if meta.get("c2pa"):
                entry["commands"] = [c.format(f=path.name) for c in IMAGE_VERIFY_COMMANDS]
            new_bytes = cleaned.encode("utf-8") if do_clean else None
        else:
            trailing = "keep" if path.suffix.lower() in (".csv", ".tsv") else None
            cleaned, findings, lang = clean_text(text, args.lang, fmt=kind, keep_nbsp=args.keep_nbsp,
                                                 keep_bidi=args.keep_bidi, typography=args.typography,
                                                 fold_homoglyphs=fold, trailing=trailing)
            entry["lang"] = lang
            if data[:3] == b"\xef\xbb\xbf":
                findings.add(0xFEFF, "removed (leading BOM)")
            entry["findings"] = findings.to_dict()
            meta = OrderedDict()
            markers = _generator_markers(text)
            if markers:
                meta["generator_markers"] = markers
            ws = _whitespace_pattern(text) if trailing is None else None
            if ws:
                meta["whitespace_pattern"] = ws
            entry["meta"] = meta or None
            if do_clean and getattr(args, "diff", False):
                entry["diff"] = "\n".join(difflib.unified_diff(
                    [_show(l) for l in text.splitlines()], [_show(l) for l in cleaned.splitlines()],
                    fromfile=str(path), tofile=f"{path}.clean", lineterm="", n=0))
            new_bytes = cleaned.encode("utf-8") if do_clean else None
    elif kind == "docx":
        new_data, findings, meta, lang = process_docx(
            data, args.lang, keep_nbsp=args.keep_nbsp, keep_bidi=args.keep_bidi,
            typography=args.typography, scrub_meta=not args.keep_meta, do_clean=do_clean,
            fold_homoglyphs=fold)
        entry["lang"] = lang
        entry["findings"] = findings.to_dict()
        entry["meta"] = meta
        new_bytes = new_data if do_clean else None
    elif kind == "zip":
        new_data, meta = process_zip(data, mode, args)
        entry["meta"] = meta
        new_bytes = new_data if do_clean else None
    elif kind == "png":
        new_data, meta = process_png(data, do_clean=do_clean and not args.keep_meta)
        entry["meta"] = meta
        entry["commands"] = [c.format(f=path.name) for c in IMAGE_VERIFY_COMMANDS]
        new_bytes = new_data if do_clean else None
    elif kind == "jpeg":
        new_data, meta = process_jpeg(data, do_clean=do_clean and not args.keep_meta)
        entry["meta"] = meta
        entry["commands"] = [c.format(f=path.name) for c in IMAGE_VERIFY_COMMANDS]
        new_bytes = new_data if do_clean else None
    elif kind == "pdf":
        entry["meta"] = inspect_pdf(data)
        entry["commands"] = [c.format(f=path.name, stem=path.stem) for c in PDF_COMMANDS]
        if entry["meta"].get("ptex_figure_info") or entry["meta"].get("absolute_paths"):
            entry["commands"] += PDFTEX_COMMANDS
        new_bytes = None
    if _VENDOR_NAME.search(path.name):
        entry["meta"] = entry.get("meta") or OrderedDict()
        entry["meta"]["file_name_mentions_model"] = path.name
    entry["verdict"] = _verdict(entry)
    return entry, new_bytes


def _show(line: str) -> str:
    return "".join(_visible(c) if (ord(c) in STRIP_ALWAYS or ord(c) in BIDI or ord(c) in TAGS
                                   or ord(c) in (ZWSP, ZWNJ, ZWJ, NBSP) or ord(c) in SPACE_HOMOGLYPHS
                                   or ord(c) in VS_TEXT or ord(c) in VS_EMOJI or ord(c) in IVS) else c
                   for c in line)


def _output_path(path: Path, args: argparse.Namespace, n_inputs: int) -> Path:
    if args.in_place:
        return path
    if args.output and n_inputs == 1:
        return Path(args.output)
    return path.with_name(f"{path.stem}.clean{path.suffix}")


def _has_findings(entry: dict) -> bool:
    f = entry.get("findings")
    if f and any(r["action"] not in ("kept",) for r in f["rows"]):
        return True
    meta = entry.get("meta") or {}
    if meta.get("file_name_mentions_model") or meta.get("macos_xattrs"):
        return True
    if entry["kind"] == "docx":
        core = meta.get("core") or {}
        app = meta.get("app") or {}
        if any(core.get(k) for k in _CORE_FIELDS) or any(app.get(k) for k in _APP_FIELDS):
            return True
        return bool(_docx_flags(meta))
    if entry["kind"] in ("png", "jpeg"):
        return bool(meta.get("metadata_found"))
    if entry["kind"] == "svg":
        return bool(meta.get("metadata_blocks") or meta.get("comments") or meta.get("c2pa"))
    if entry["kind"] == "pdf":
        return bool(meta.get("info") or meta.get("xmp") or meta.get("c2pa") or meta.get("ptex_figure_info")
                    or meta.get("absolute_paths"))
    if entry["kind"] == "zip":
        return bool(meta.get("junk_entries") or meta.get("members_with_findings"))
    return bool(meta.get("generator_markers") or meta.get("whitespace_pattern"))


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="provenance_scrub.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("files", nargs="+", help="files to process; '-' reads text from stdin")
        p.add_argument("--lang", choices=("auto", "zh", "en"), default="auto",
                       help="manuscript language; governs U+3000 and the EN-only typography rules")
        p.add_argument("--keep-nbsp", action="store_true", help="leave U+00A0 alone")
        p.add_argument("--keep-bidi", action="store_true", help="never strip bidi controls")
        p.add_argument("--typography", action="store_true",
                       help="EN only: curly quotes -> straight, ellipsis -> ... (dashes are never touched)")
        p.add_argument("--keep-meta", action="store_true", help="do not scrub docx docProps / image metadata")
        p.add_argument("--fold-homoglyphs", action="store_true",
                       help="repair Cyrillic / Greek look-alike letters inside Latin words (default: report only)")
        p.add_argument("--json", action="store_true", help="machine-readable report on stdout")

    pi = sub.add_parser("inspect", help="report only; exit 1 if anything is found")
    common(pi)
    pc = sub.add_parser("clean", help="write cleaned copies")
    common(pc)
    pc.add_argument("-o", "--output", help="output path (single input only)")
    pc.add_argument("--in-place", action="store_true", help="overwrite the input, keeping a .bak")
    pc.add_argument("--diff", action="store_true", help="show a unified diff with carriers made visible (text formats)")
    sub.add_parser("self-test", help="run the built-in fixtures")

    args = parser.parse_args(argv)
    if args.cmd == "self-test":
        return self_test()

    entries: List[dict] = []
    found_any = False
    rc = 0
    for f in args.files:
        path = Path(f)
        try:
            entry, new_bytes = process_path(path, args.cmd, args)
        except (ValueError, zipfile.BadZipFile, UnicodeDecodeError) as exc:
            entries.append({"file": f, "kind": "error", "mode": args.cmd, "error": str(exc),
                            "verdict": f"error: {exc}"})
            rc = 2
            continue
        found_any = found_any or _has_findings(entry)
        if args.cmd == "clean" and new_bytes is not None:
            if str(path) == "-":
                sys.stdout.buffer.write(new_bytes)
            else:
                out = _output_path(path, args, len(args.files))
                if args.in_place:
                    bak = path.with_name(path.name + ".bak")
                    if bak.exists():
                        entries.append({"file": f, "kind": entry["kind"], "mode": "clean",
                                        "error": f"refusing to overwrite existing backup {bak}",
                                        "verdict": "error: backup exists"})
                        rc = 2
                        continue
                    bak.write_bytes(path.read_bytes())
                out.write_bytes(new_bytes)
                entry["written"] = str(out)
        entries.append(entry)

    stream = sys.stderr if (args.cmd == "clean" and any(f == "-" for f in args.files)) else sys.stdout
    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2), file=stream)
    else:
        for e in entries:
            if e["kind"] == "error":
                print(f"== {e['file']} == {e['verdict']}", file=stream)
                continue
            print(render_report(e), file=stream)
            if e.get("diff"):
                print(e["diff"], file=stream)
            if e.get("written"):
                print(f"written: {e['written']}", file=stream)
            print(file=stream)
    if rc:
        return rc
    if args.cmd == "inspect":
        return 1 if found_any else 0
    return 0


# --------------------------------------------------------------------------- #
# Self-test fixtures (also exercised by tests/test_de_aigc_provenance_scrub.py)
# --------------------------------------------------------------------------- #

FIXTURES: List[Tuple[str, str, str, str]] = [
    # (label, lang, input, expected)
    ("zwsp removed", "en", "The re​form reduced entry.", "The reform reduced entry."),
    ("soft hyphen removed", "en", "iden­tification", "identification"),
    ("word joiner removed", "en", "Table⁠3", "Table3"),
    ("narrow nbsp normalised", "en", "p < 0.01", "p < 0.01"),
    ("nbsp normalised", "en", "Table 3", "Table 3"),
    ("thin space normalised", "en", "1 000", "1 000"),
    ("en dash kept", "en", "2014–2022, pp. 12–15", "2014–2022, pp. 12–15"),
    ("minus sign kept", "en", "−0.043 (s.e. 0.011)", "−0.043 (s.e. 0.011)"),
    ("superscript kept", "en", "R² = 0.31", "R² = 0.31"),
    ("greek kept", "en", "β₁ ≤ 0", "β₁ ≤ 0"),
    ("bidi stripped in latin", "en", "abc‮def‬", "abcdef"),
    ("bidi kept next to hebrew", "en", "‏שלום", "‏שלום"),
    ("zwnj kept in persian", "en", "می‌خواهم", "می‌خواهم"),
    ("zwnj stripped in latin", "en", "ab‌cd", "abcd"),
    ("zwj kept in emoji sequence", "en", "\U0001F468‍\U0001F469‍\U0001F467", "\U0001F468‍\U0001F469‍\U0001F467"),
    ("zwj kept after skin tone", "en", "\U0001F469\U0001F3FD‍\U0001F52C", "\U0001F469\U0001F3FD‍\U0001F52C"),
    ("zwj stripped in prose", "en", "fir‍m", "firm"),
    ("vs16 kept after symbol", "en", "❤️", "❤️"),
    ("vs16 stripped in prose", "en", "data️", "data"),
    ("ivs kept after cjk", "zh", "邊\U000E0100氏", "邊\U000E0100氏"),
    ("ivs stripped after latin", "en", "a\U000E0100b", "ab"),
    ("tag chars stripped", "en", "hello\U000E0041\U000E0042", "hello"),
    ("subdivision flag kept", "en", "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F",
     "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F"),
    ("ideographic space kept in zh", "zh", "　　数字经济", "　　数字经济"),
    ("ideographic space normalised in en", "en", "a　b", "a b"),
    ("fullwidth punctuation kept", "zh", "结果显著（t = 3.81）。", "结果显著（t = 3.81）。"),
    ("chinese dash and ellipsis kept", "zh", "数据——另一个故事……", "数据——另一个故事……"),
    ("middle dot in name kept", "zh", "亚当·斯密", "亚当·斯密"),
    ("chinese curly quotes kept", "zh", "“数字经济”", "“数字经济”"),
    ("english curly quotes kept without flag", "en", "“shock”", "“shock”"),
    ("em dash kept for review", "en", "entry — not credit", "entry — not credit"),
    ("line separator to newline", "en", "a b", "a\nb"),
    ("bom removed", "en", "﻿Abstract", "Abstract"),
    ("control removed", "en", "a\x07b", "ab"),
    ("thai zwsp kept", "en", "สวัสดี​ครับ", "สวัสดี​ครับ"),
    # v1.1 — script-bound format characters, look-alikes, trailing whitespace
    ("arabic number sign kept", "en", "؀١٢", "؀١٢"),
    ("arabic number sign stripped in latin", "en", "a؀b", "ab"),
    ("khmer inherent vowel stripped in latin", "en", "a឴b", "ab"),
    ("greek question mark -> semicolon", "en", "Why;", "Why;"),
    ("kelvin sign -> K", "en", "300 K", "300 K"),
    ("ohm sign -> omega", "en", "Ω = 2", "Ω = 2"),
    ("fullwidth letter inside ascii word folded", "en", "ＴFP", "TFP"),
    ("fullwidth digit after ascii word folded", "en", "Table３", "Table3"),
    ("fullwidth digits kept in chinese", "zh", "表３", "表３"),
    ("russian citation untouched", "en", "Экономика России (2019)", "Экономика России (2019)"),
    ("greek notation untouched", "en", "β = 0.04, Δy and μ", "β = 0.04, Δy and μ"),
    ("homoglyph word reported, not folded by default", "en", "Тhe reform", "Тhe reform"),
    ("trailing spaces and tabs stripped", "en", "line \t \nnext", "line\nnext"),
]


def self_test() -> int:
    failures = 0
    for label, lang, src, expected in FIXTURES:
        got, _, _ = clean_text(src, lang)
        ok = got == expected
        failures += 0 if ok else 1
        print(f"[{'PASS' if ok else 'FAIL'}] {label}" + ("" if ok else f"\n       got      {got!r}\n       expected {expected!r}"))
    # typography flag, EN only
    got, _, _ = clean_text("“shock” …", "en", typography=True)
    ok = got == '"shock" ...'
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] typography flag converts EN quotes and ellipsis")
    got, _, _ = clean_text("“冲击”……", "zh", typography=True)
    ok = got == "“冲击”……"
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] typography flag never touches ZH punctuation")
    # markdown code spans untouched
    md = "text​ here `code​` and\n```\nblock​\n```\n"
    got, _, _ = clean_text(md, "en", fmt="markdown")
    ok = got == "text here `code​` and\n```\nblock​\n```\n"
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] markdown code spans and fences are left alone")
    # nfkc never applied
    got, _, _ = clean_text("ＡＢ ½ ﬁ", "en")
    ok = got == "ＡＢ ½ ﬁ"
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] no NFKC folding (fullwidth, fractions, ligatures survive)")
    # homoglyph folding is opt-in and skips math
    got, _, _ = clean_text("Тhe rеform and $Αx$", "en", fold_homoglyphs=True)
    ok = got == "The reform and $Αx$"
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] --fold-homoglyphs repairs Latin words, leaves math alone")
    # markdown hard break (exactly two trailing spaces) survives; other trailing runs go
    got, _, _ = clean_text("a  \nb   \nc", "en", fmt="markdown")
    ok = got == "a  \nb\nc"
    failures += 0 if ok else 1
    print(f"[{'PASS' if ok else 'FAIL'}] markdown hard breaks kept, other trailing whitespace removed")
    print(f"\n{len(FIXTURES) + 6 - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
