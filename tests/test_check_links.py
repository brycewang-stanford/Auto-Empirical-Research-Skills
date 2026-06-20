"""Tests for external-link checking helpers."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest

from _helpers import load_module

check_links = load_module("scripts/check-links.py", "aers_check_links")


class TestLinkExtraction(unittest.TestCase):
    def test_markdown_code_fences_are_skipped_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = check_links.Path(tmp)
            md = root / "README.md"
            md.write_text(
                "[rendered](https://example.com/page.)\n"
                "```markdown\n"
                "[example](https://example.invalid/placeholder)\n"
                "```\n",
                encoding="utf-8",
            )
            old_root = check_links.ROOT
            try:
                check_links.ROOT = root
                links = check_links.iter_links([md])
                self.assertEqual(links, {"https://example.com/page": ["README.md"]})

                with_examples = check_links.iter_links([md], include_code_fences=True)
                self.assertIn("https://example.invalid/placeholder", with_examples)
            finally:
                check_links.ROOT = old_root

    def test_html_links_and_repeated_files_are_normalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = check_links.Path(tmp)
            html = root / "docs" / "search.html"
            html.parent.mkdir()
            html.write_text(
                '<a href="https://example.com/a">one</a>'
                '<a href="https://example.com/a">two</a>',
                encoding="utf-8",
            )
            old_root = check_links.ROOT
            try:
                check_links.ROOT = root
                self.assertEqual(
                    check_links.iter_links([html]),
                    {"https://example.com/a": ["docs/search.html"]},
                )
            finally:
                check_links.ROOT = old_root


class TestCheckLinksCli(unittest.TestCase):
    def test_main_can_write_or_skip_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = check_links.Path(tmp)
            md = root / "README.md"
            md.write_text("[site](https://example.com)\n", encoding="utf-8")
            output = root / "catalog" / "external-link-check.json"

            old_root = check_links.ROOT
            old_maintained_docs = check_links.maintained_docs
            old_check_url = check_links.check_url
            try:
                check_links.ROOT = root
                check_links.maintained_docs = lambda: [md]
                check_links.check_url = lambda url, timeout: {
                    "url": url,
                    "status": 200,
                    "ok": True,
                }
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(check_links.main(["--output", str(output)]), 0)
                payload = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(payload["checked_links"], 1)
                self.assertEqual(payload["failures"], [])

                output.unlink()
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(
                        check_links.main(["--output", str(output), "--no-write"]),
                        0,
                    )
                self.assertFalse(output.exists())
            finally:
                check_links.ROOT = old_root
                check_links.maintained_docs = old_maintained_docs
                check_links.check_url = old_check_url

    def test_main_returns_failure_for_broken_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = check_links.Path(tmp)
            md = root / "README.md"
            md.write_text("[site](https://example.invalid)\n", encoding="utf-8")

            old_root = check_links.ROOT
            old_maintained_docs = check_links.maintained_docs
            old_check_url = check_links.check_url
            try:
                check_links.ROOT = root
                check_links.maintained_docs = lambda: [md]
                check_links.check_url = lambda url, timeout: {
                    "url": url,
                    "status": 404,
                    "ok": False,
                }
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(check_links.main(["--no-write"]), 1)
            finally:
                check_links.ROOT = old_root
                check_links.maintained_docs = old_maintained_docs
                check_links.check_url = old_check_url


if __name__ == "__main__":
    unittest.main()
