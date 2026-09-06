"""Tests for skills/48-de-AIGC-skills/scripts/provenance_scrub.py.

The script is the provenance layer of the de-AIGC skill: deterministic Layer A
(invisible-character carriers) and Layer C (container metadata). The cases below
pin the two things that make it safe on a bilingual academic manuscript —
carriers go, legitimate typography stays — plus lossless container handling.
Stdlib only.
"""

from __future__ import annotations

import contextlib
import io
import json
import struct
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import load_module  # noqa: E402

scrub = load_module("skills/48-de-AIGC-skills/scripts/provenance_scrub.py", "aers_provenance_scrub")


def clean(text: str, lang: str = "en", **kw) -> str:
    out, _, _ = scrub.clean_text(text, lang, **kw)
    return out


def run_cli(args):
    """Run the CLI with its report captured, so `make test` output stays clean."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = scrub.main(args)
    return rc, buf.getvalue()


class LayerACarriers(unittest.TestCase):
    def test_zero_width_space_removed_in_prose(self):
        self.assertEqual(clean("The re​form reduced entry."), "The reform reduced entry.")

    def test_soft_hyphen_and_word_joiner_removed(self):
        self.assertEqual(clean("iden­tification Table⁠3"), "identification Table3")

    def test_exotic_spaces_normalised(self):
        self.assertEqual(clean("p < 0.01 and 1 000"), "p < 0.01 and 1 000")

    def test_nbsp_normalised_unless_kept(self):
        self.assertEqual(clean("Table 3"), "Table 3")
        self.assertEqual(clean("Table 3", keep_nbsp=True), "Table 3")

    def test_bidi_controls_stripped_in_latin_kept_next_to_rtl(self):
        self.assertEqual(clean("abc‮def‬"), "abcdef")
        self.assertEqual(clean("‏שלום"), "‏שלום")

    def test_tag_characters_stripped_except_subdivision_flag(self):
        self.assertEqual(clean("hello\U000e0041\U000e0042"), "hello")
        flag = "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F"
        self.assertEqual(clean(flag), flag)

    def test_controls_and_line_separators(self):
        self.assertEqual(clean("a\x07b c"), "ab\nc")

    def test_leading_bom_reported_and_removed(self):
        out, findings, _ = scrub.clean_text("﻿Abstract", "en")
        self.assertEqual(out, "Abstract")
        self.assertTrue(any(cp == 0xFEFF for (cp, _a) in findings.counts))


class LayerAContextPreservation(unittest.TestCase):
    def test_zwj_kept_in_emoji_sequence_removed_in_prose(self):
        family = "\U0001F468‍\U0001F469‍\U0001F467"
        self.assertEqual(clean(family), family)
        scientist = "\U0001F469\U0001F3FD‍\U0001F52C"
        self.assertEqual(clean(scientist), scientist)
        self.assertEqual(clean("fir‍m"), "firm")

    def test_zwnj_kept_in_persian_removed_in_latin(self):
        self.assertEqual(clean("می‌خواهم"),
                         "می‌خواهم")
        self.assertEqual(clean("ab‌cd"), "abcd")

    def test_variation_selectors_context(self):
        self.assertEqual(clean("❤️"), "❤️")          # ❤️
        self.assertEqual(clean("1️⃣"), "1️⃣")        # keycap
        self.assertEqual(clean("data️"), "data")
        self.assertEqual(clean("邊\U000e0100氏", "zh"), "邊\U000e0100氏")  # IVS after CJK
        self.assertEqual(clean("a\U000e0100b"), "ab")

    def test_thai_zwsp_kept(self):
        thai = "สวัสดี​ครับ"
        self.assertEqual(clean(thai), thai)


class LayerANeverTouched(unittest.TestCase):
    def test_academic_typography_survives(self):
        s = "2014–2022, pp. 12–15, −0.043 (s.e. 0.011), R² = 0.31, β₁ ≤ 0, 7%–17%"
        self.assertEqual(clean(s), s)

    def test_chinese_typography_survives(self):
        s = "　　数字经济——另一个故事……（t = 3.81）。亚当·斯密“冲击”"
        self.assertEqual(clean(s, "zh"), s)
        self.assertEqual(clean(s, "zh", typography=True), s)

    def test_ideographic_space_language_aware(self):
        self.assertEqual(clean("　　数字", "zh"), "　　数字")
        self.assertEqual(clean("a　b", "en"), "a b")
        # English prose quoting Chinese keeps the U+3000 next to CJK
        self.assertEqual(clean("see 数　字", "en"), "see 数　字")

    def test_no_nfkc_folding(self):
        s = "ＡＢ ½ ﬁ"
        self.assertEqual(clean(s), s)

    def test_em_dash_reported_for_review_not_replaced(self):
        out, findings, _ = scrub.clean_text("entry — not credit", "en", typography=True)
        self.assertEqual(out, "entry — not credit")
        self.assertIn((0x2014, "review"), findings.counts)

    def test_typography_flag_is_english_only_and_opt_in(self):
        self.assertEqual(clean("“shock” …"), "“shock” …")
        self.assertEqual(clean("“shock” …", typography=True), '"shock" ...')

    def test_markdown_code_spans_untouched(self):
        md = "text​ here `code​` and\n```\nblock​\n```\n"
        self.assertEqual(clean(md, fmt="markdown"), "text here `code​` and\n```\nblock​\n```\n")

    def test_language_detection(self):
        self.assertEqual(scrub.detect_lang("数字经济的发展 with data"), "zh")
        self.assertEqual(scrub.detect_lang("Digital economy and regional growth"), "en")

    def test_builtin_fixtures_pass(self):
        for label, lang, src, expected in scrub.FIXTURES:
            with self.subTest(label=label):
                self.assertEqual(clean(src, lang), expected)


def _make_docx(body_xml: str, creator: str = "python-docx") -> bytes:
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f'<dc:title>Digital economy</dc:title><dc:creator>{creator}</dc:creator>'
        f'<cp:lastModifiedBy>{creator}</cp:lastModifiedBy><cp:keywords>DID; China</cp:keywords>'
        '</cp:coreProperties>'
    )
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>Microsoft Office Word</Application><Company>Stanford</Company></Properties>')
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
           f'{body_xml}</w:body></w:document>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("word/document.xml", doc)
        z.writestr("word/comments.xml", "<w:comments/>")
    return buf.getvalue()


class LayerCDocx(unittest.TestCase):
    def test_docx_text_runs_cleaned_and_docprops_scrubbed(self):
        body = ('<w:p><w:r><w:t xml:space="preserve">The re​form — 2014–2022, R²</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>&#8203;hidden&#x202F;space</w:t></w:r></w:p>'
                '<w:p><w:r><w:t>　　数字经济的发展对区域增长</w:t></w:r></w:p>')
        data = _make_docx(body)
        new, findings, meta, lang = scrub.process_docx(
            data, "auto", keep_nbsp=False, keep_bidi=False, typography=False, scrub_meta=True, do_clean=True)
        self.assertNotEqual(new, data)
        z = zipfile.ZipFile(io.BytesIO(new))
        doc = z.read("word/document.xml").decode("utf-8")
        self.assertIn('<w:t xml:space="preserve">The reform — 2014–2022, R²</w:t>', doc)
        self.assertIn("<w:t>hidden space</w:t>", doc)
        self.assertNotIn("&#8203;", doc)
        self.assertIn("　　数字", doc)  # zh indent kept (CJK-adjacent)
        core = z.read("docProps/core.xml").decode("utf-8")
        self.assertIn("<dc:creator></dc:creator>", core)
        self.assertIn("<cp:lastModifiedBy></cp:lastModifiedBy>", core)
        self.assertIn("<dc:title>Digital economy</dc:title>", core)      # title/keywords are legitimate
        self.assertIn("<cp:keywords>DID; China</cp:keywords>", core)
        app = z.read("docProps/app.xml").decode("utf-8")
        self.assertIn("<Company></Company>", app)
        self.assertIn("<Application>Microsoft Office Word</Application>", app)  # software identity kept
        self.assertEqual(meta["core"]["dc:creator"], "python-docx")
        self.assertEqual(meta["core_scrubbed"], ["dc:creator", "cp:lastModifiedBy"])
        self.assertTrue(meta["has_comments"])
        self.assertEqual(z.namelist(), zipfile.ZipFile(io.BytesIO(data)).namelist())
        self.assertIn((0x200B, "removed"), findings.counts)
        self.assertIn((0x202F, "→ U+0020"), findings.counts)

    def test_docx_inspect_does_not_modify(self):
        data = _make_docx("<w:p><w:r><w:t>plain​</w:t></w:r></w:p>")
        new, findings, meta, _ = scrub.process_docx(
            data, "en", keep_nbsp=False, keep_bidi=False, typography=False, scrub_meta=True, do_clean=False)
        self.assertEqual(new, data)
        self.assertEqual(findings.changed(), 1)
        self.assertNotIn("core_scrubbed", meta)

    def test_docx_keep_meta(self):
        data = _make_docx("<w:p><w:r><w:t>plain​</w:t></w:r></w:p>")
        new, _, meta, _ = scrub.process_docx(
            data, "en", keep_nbsp=False, keep_bidi=False, typography=False, scrub_meta=False, do_clean=True)
        core = zipfile.ZipFile(io.BytesIO(new)).read("docProps/core.xml").decode("utf-8")
        self.assertIn("<dc:creator>python-docx</dc:creator>", core)
        self.assertNotIn("core_scrubbed", meta)


def _png_chunk(ctype: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF)


def _make_png(with_meta: bool = True) -> bytes:
    ihdr = _png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0))
    raw = zlib.compress(b"\x00\x00")
    parts = [scrub.PNG_SIG, ihdr, _png_chunk(b"pHYs", struct.pack(">IIB", 2835, 2835, 1))]
    if with_meta:
        parts.append(_png_chunk(b"tEXt", b"Software\x00matplotlib"))
        parts.append(_png_chunk(b"iTXt", b"XML:com.adobe.xmp\x00\x00\x00\x00\x00<x:xmpmeta/>"))
        parts.append(_png_chunk(b"caBX", b"\x00\x00\x00\x10jumbc2pa-manifest"))
        parts.append(_png_chunk(b"eXIf", b"Exif\x00\x00"))
    parts.append(_png_chunk(b"IDAT", raw))
    parts.append(_png_chunk(b"IEND", b""))
    return b"".join(parts)


class LayerCImages(unittest.TestCase):
    def test_png_metadata_chunks_dropped_losslessly(self):
        data = _make_png()
        new, report = scrub.process_png(data, do_clean=True)
        self.assertTrue(report["c2pa"])
        self.assertIn("C2PA manifest (JUMBF)", report["metadata_found"])
        self.assertIn("XMP", report["metadata_found"])
        self.assertIn("tEXt 'Software'", report["metadata_found"])
        self.assertEqual(new, _make_png(with_meta=False))  # pixel data and pHYs byte-identical
        again, report2 = scrub.process_png(new, do_clean=False)
        self.assertEqual(report2["metadata_found"], [])

    def test_png_inspect_leaves_bytes_alone(self):
        data = _make_png()
        new, report = scrub.process_png(data, do_clean=False)
        self.assertEqual(new, data)
        self.assertTrue(report["metadata_found"])

    def test_jpeg_app_segments_dropped_except_jfif_icc_adobe(self):
        def seg(marker: int, body: bytes) -> bytes:
            return b"\xff" + bytes([marker]) + struct.pack(">H", len(body) + 2) + body

        jfif = seg(0xE0, b"JFIF\x00\x01\x02\x00\x00\x01\x00\x01\x00\x00")
        exif = seg(0xE1, b"Exif\x00\x00MM\x00*")
        xmp = seg(0xE1, b"http://ns.adobe.com/xap/1.0/\x00<x:xmpmeta/>")
        icc = seg(0xE2, b"ICC_PROFILE\x00\x01\x01profile")
        c2pa = seg(0xEB, b"JP\x00\x01\x00\x00\x00\x20jumbc2pa")
        com = seg(0xFE, b"Created with matplotlib")
        scan = b"\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00" + b"\x12\x34" + b"\xff\xd9"
        data = b"\xff\xd8" + jfif + exif + xmp + icc + c2pa + com + scan
        new, report = scrub.process_jpeg(data, do_clean=True)
        self.assertEqual(new, b"\xff\xd8" + jfif + icc + scan)
        self.assertTrue(report["c2pa"])
        self.assertEqual(report["metadata_found"],
                         ["EXIF (APP1)", "XMP (APP1)", "C2PA manifest (APP11 JUMBF)", "COM comment"])

    def test_svg_metadata_and_comments_removed(self):
        svg = ('<?xml version="1.0"?>\n<!-- Created with matplotlib (https://matplotlib.org/) -->\n'
               '<svg xmlns="http://www.w3.org/2000/svg"><metadata><rdf:RDF/></metadata><rect/></svg>')
        new, report = scrub.process_svg(svg, do_clean=True)
        self.assertNotIn("<metadata>", new)
        self.assertNotIn("Created with", new)
        self.assertIn("<rect/>", new)
        self.assertEqual(report["metadata_blocks"], 1)
        self.assertEqual(len(report["generator_comments"]), 1)


class LayerCPdf(unittest.TestCase):
    def test_pdf_inspect_reports_info_and_xmp(self):
        pdf = (b"%PDF-1.7\n1 0 obj << /Producer (LaTeX with hyperref) /Creator (pdfTeX) /Author (Jane Doe) >> endobj\n"
               b"2 0 obj << /Type /Metadata /Subtype /XML >> stream\n<x:xmpmeta/>\nendstream endobj\n%%EOF\n")
        report = scrub.inspect_pdf(pdf)
        self.assertEqual(report["info"]["Producer"], "LaTeX with hyperref")
        self.assertEqual(report["info"]["Author"], "Jane Doe")
        self.assertTrue(report["xmp"])
        self.assertFalse(report["c2pa"])


class CommandLine(unittest.TestCase):
    def test_inspect_exit_codes_and_clean_output_file(self):
        with tempfile.TemporaryDirectory() as td:
            dirty = Path(td) / "draft.md"
            dirty.write_text("Intro​ text here.\n", encoding="utf-8")
            clean_path = Path(td) / "clean.md"
            clean_path.write_text("Intro text here. 2014–2022\n", encoding="utf-8")
            self.assertEqual(run_cli(["inspect", str(dirty)])[0], 1)
            self.assertEqual(run_cli(["inspect", str(clean_path)])[0], 0)
            self.assertEqual(run_cli(["clean", str(dirty)])[0], 0)
            out = Path(td) / "draft.clean.md"
            self.assertTrue(out.exists())
            self.assertEqual(out.read_text(encoding="utf-8"), "Intro text here.\n")
            self.assertEqual(dirty.read_text(encoding="utf-8"), "Intro​ text here.\n")  # source untouched

    def test_in_place_keeps_backup_and_refuses_second_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "a.txt"
            f.write_text("x​y", encoding="utf-8")
            self.assertEqual(run_cli(["clean", "--in-place", str(f)])[0], 0)
            self.assertEqual(f.read_text(encoding="utf-8"), "xy")
            self.assertEqual((Path(td) / "a.txt.bak").read_text(encoding="utf-8"), "x​y")
            f.write_text("x​z", encoding="utf-8")
            self.assertEqual(run_cli(["clean", "--in-place", str(f)])[0], 2)
            self.assertEqual(f.read_text(encoding="utf-8"), "x​z")

    def test_json_report_shape_and_b_unknown_verdict(self):
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "a.md"
            f.write_text("x​y", encoding="utf-8")
            _, out = run_cli(["inspect", "--json", str(f)])
            entries = json.loads(out)
            self.assertEqual(entries[0]["kind"], "markdown")
            self.assertEqual(entries[0]["findings"]["rows"][0]["codepoint"], "U+200B")
            self.assertIn("B: unknown", entries[0]["verdict"])
            self.assertIn("B: unknown", scrub.render_report(entries[0]))

    def test_self_test_passes(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = scrub.self_test()
        self.assertEqual(rc, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main()
