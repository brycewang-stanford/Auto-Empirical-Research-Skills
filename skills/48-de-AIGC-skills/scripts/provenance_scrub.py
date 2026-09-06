#!/usr/bin/env python3
"""provenance_scrub.py — inspect and clean AI-provenance carriers in a manuscript package.

Part of the `de-aigc-skills` skill (AERS collection 48). Standard library only,
Python 3.9+. Two of the three kinds of "AI watermark" that circulate in 2026 are
deterministic and this script handles them; the third is not, and this script
says so instead of pretending.

  Layer A  invisible-character carriers inside text
           (zero-width characters, bidi controls, tag characters, stray
           variation selectors, exotic spaces, soft hyphens, C0/C1 controls)
           -> .txt .md .qmd .Rmd .tex .bib .html .csv and the text runs of .docx

  Layer C  container metadata on the submission package
           (.docx docProps / comments / people.xml / customXml,
            .png / .jpg C2PA + EXIF + XMP, .svg <metadata>, .pdf Info + XMP)
           -> reported for every format; lossless cleaning for docx / png / jpg
              / svg; report + exact commands for pdf

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
                                         [--keep-meta] [--diff] [--json]
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
import sys
import unicodedata
import zipfile
import zlib
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

__version__ = "1.0.0"

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
                  keep_bidi: bool = False, typography: bool = False, line_offset: int = 1) -> str:
    """Clean one prose segment. `lang` is 'zh' or 'en' (already resolved)."""
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

    return "".join(out)


_MD_CODE = re.compile(r"(^```.*?^```[ \t]*$|^~~~.*?^~~~[ \t]*$|`[^`\n]*`)", re.S | re.M)
_HTML_CODE = re.compile(r"(<pre\b.*?</pre>|<code\b.*?</code>|<script\b.*?</script>|<style\b.*?</style>)", re.S | re.I)


def clean_text(text: str, lang: str = "auto", *, fmt: str = "text", keep_nbsp: bool = False,
               keep_bidi: bool = False, typography: bool = False) -> Tuple[str, Findings, str]:
    """Clean a whole document. Returns (cleaned, findings, resolved_lang).

    fmt: 'text' | 'markdown' | 'html'. Code spans/blocks are left untouched in
    markdown and html so that a document *about* invisible characters keeps
    its own examples.
    """
    resolved = detect_lang(text) if lang == "auto" else lang
    findings = Findings()
    if fmt == "markdown":
        splitter = _MD_CODE
    elif fmt == "html":
        splitter = _HTML_CODE
    else:
        splitter = None

    if splitter is None:
        cleaned = clean_segment(text, resolved, findings, keep_nbsp=keep_nbsp,
                                keep_bidi=keep_bidi, typography=typography)
        return cleaned, findings, resolved

    parts = splitter.split(text)
    out: List[str] = []
    line_no = 1
    for k, part in enumerate(parts):
        if k % 2 == 1:  # a code span / block captured by the splitter
            out.append(part)
        else:
            out.append(clean_segment(part, resolved, findings, keep_nbsp=keep_nbsp,
                                     keep_bidi=keep_bidi, typography=typography,
                                     line_offset=line_no))
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
                or cp in HANGUL_FILLERS or cp in MONGOLIAN_FVS or cp in LINE_SEPARATORS):
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


def process_docx(data: bytes, lang: str, *, keep_nbsp: bool, keep_bidi: bool, typography: bool,
                 scrub_meta: bool, do_clean: bool) -> Tuple[bytes, Findings, dict, str]:
    """Inspect or clean a .docx. Returns (new_bytes, text_findings, meta_report, lang)."""
    findings = Findings()
    meta: "OrderedDict[str, object]" = OrderedDict()
    zin = zipfile.ZipFile(io.BytesIO(data))
    names = zin.namelist()
    replacements: Dict[str, bytes] = {}

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
                cleaned = clean_segment(m.group(2), lang, _pf, keep_nbsp=keep_nbsp,
                                        keep_bidi=keep_bidi, typography=typography)
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


def inspect_pdf(data: bytes) -> dict:
    info: Dict[str, str] = OrderedDict()
    for key, val in _PDF_INFO.findall(data):
        k = key.decode()
        if k in info:
            continue
        if val.startswith(b"("):
            info[k] = val[1:-1].decode("latin-1", "replace")[:120]
        else:
            info[k] = "<hex string>"
    return {
        "format": "pdf",
        "info": info,
        "xmp": b"<x:xmpmeta" in data or b"/Type /Metadata" in data or b"/Type/Metadata" in data,
        "c2pa": b"c2pa" in data.lower() or b"jumb" in data,
        "incremental_updates": data.count(b"%%EOF") - 1 if data.count(b"%%EOF") > 1 else 0,
    }


PDF_COMMANDS = [
    "exiftool -all= -overwrite_original {f}      # drops Info dictionary + XMP",
    "qpdf --linearize {f} {stem}.clean.pdf         # rewrites the file so old metadata is not left in an incremental update",
    "c2patool {stem}.clean.pdf                     # verify no C2PA manifest remains (official CAI tool)",
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


def _verdict(entry: dict) -> str:
    a = entry.get("findings")
    a_changed = sum(r["count"] for r in a["rows"] if r["action"] not in ("kept", "review")) if a else 0
    a_review = sum(r["count"] for r in a["rows"] if r["action"] == "review") if a else 0
    parts = []
    if entry["mode"] == "inspect":
        parts.append(f"A: {a_changed} carrier(s) to clean" if a_changed else "A: clean")
    else:
        parts.append(f"A: {a_changed} carrier(s) cleaned" if a_changed else "A: nothing to clean")
    if a_review:
        parts.append(f"{a_review} em dash(es) left for EN20 review")
    meta = entry.get("meta") or {}
    if entry["kind"] == "docx":
        flagged = [k for k in ("has_comments", "has_people", "custom_xml_parts", "thumbnail") if meta.get(k)]
        if meta.get("tracked_changes"):
            flagged.append("tracked_changes")
        core = meta.get("core") or {}
        app = meta.get("app") or {}
        props_present = any(core.get(k) for k in _CORE_FIELDS) or any(app.get(k) for k in _APP_FIELDS)
        if entry["mode"] == "clean":
            head = "docProps scrubbed" if (meta.get("core_scrubbed") or meta.get("app_scrubbed")) else "docProps already clean"
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
    parts.append("B: unknown")
    return " · ".join(parts)


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def _kind_of(path: Path, data: bytes) -> str:
    suf = path.suffix.lower()
    if suf == ".docx":
        return "docx"
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


def process_path(path: Path, mode: str, args: argparse.Namespace) -> Tuple[dict, Optional[bytes]]:
    data = sys.stdin.buffer.read() if str(path) == "-" else path.read_bytes()
    kind = _kind_of(path, data) if str(path) != "-" else "text"
    do_clean = mode == "clean"
    entry: dict = {"file": str(path), "kind": kind, "mode": mode}
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
            cleaned, findings, lang = clean_text(text, args.lang, fmt=kind, keep_nbsp=args.keep_nbsp,
                                                 keep_bidi=args.keep_bidi, typography=args.typography)
            entry["lang"] = lang
            entry["findings"] = findings.to_dict()
            if data[:3] == b"\xef\xbb\xbf":
                findings.add(0xFEFF, "removed (leading BOM)")
                entry["findings"] = findings.to_dict()
            if do_clean and getattr(args, "diff", False):
                entry["diff"] = "\n".join(difflib.unified_diff(
                    [_show(l) for l in text.splitlines()], [_show(l) for l in cleaned.splitlines()],
                    fromfile=str(path), tofile=f"{path}.clean", lineterm="", n=0))
            new_bytes = cleaned.encode("utf-8") if do_clean else None
    elif kind == "docx":
        new_data, findings, meta, lang = process_docx(
            data, args.lang, keep_nbsp=args.keep_nbsp, keep_bidi=args.keep_bidi,
            typography=args.typography, scrub_meta=not args.keep_meta, do_clean=do_clean)
        entry["lang"] = lang
        entry["findings"] = findings.to_dict()
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
        new_bytes = None
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
    if entry["kind"] == "docx":
        core = meta.get("core") or {}
        app = meta.get("app") or {}
        if any(core.get(k) for k in _CORE_FIELDS) or any(app.get(k) for k in _APP_FIELDS):
            return True
        return bool(meta.get("has_comments") or meta.get("has_people") or meta.get("custom_xml_parts")
                    or meta.get("tracked_changes") or meta.get("thumbnail"))
    if entry["kind"] in ("png", "jpeg"):
        return bool(meta.get("metadata_found"))
    if entry["kind"] == "svg":
        return bool(meta.get("metadata_blocks") or meta.get("comments") or meta.get("c2pa"))
    if entry["kind"] == "pdf":
        return bool(meta.get("info") or meta.get("xmp") or meta.get("c2pa"))
    return False


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
    print(f"\n{len(FIXTURES) + 4 - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
