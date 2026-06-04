"""Tests for the tools-catalog link re-check helper (no network)."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest

from _helpers import load_module

check_tools = load_module("scripts/check-tools-links.py", "aers_check_tools_links")

FIXTURE = [
    {"id": "a", "url": "https://example.com/a", "homepage": "https://example.com/a-home"},
    {"id": "b", "url": "https://example.com/b", "homepage": None},
    {"id": "c", "url": "https://example.com/a", "homepage": None},  # shares a's url
]


def _patch(results_by_url):
    """Return a fake check_url that maps url -> {ok, status} from results_by_url."""
    def fake(url, timeout):
        ok = results_by_url.get(url, True)
        return {"url": url, "status": 200 if ok else 404, "ok": ok}
    return fake


class TestToolsLinkCheck(unittest.TestCase):
    def _run(self, results_by_url, extra_args=None):
        old_load, old_check = check_tools.load_tools, check_tools.check_url
        try:
            check_tools.load_tools = lambda: FIXTURE
            check_tools.check_url = _patch(results_by_url)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = check_tools.main(["--no-write", *(extra_args or [])])
            return code
        finally:
            check_tools.load_tools, check_tools.check_url = old_load, old_check

    def test_all_reachable_passes_and_dedupes_urls(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = check_tools.Path(tmp) / "report.json"
            old_load, old_check = check_tools.load_tools, check_tools.check_url
            try:
                check_tools.load_tools = lambda: FIXTURE
                check_tools.check_url = _patch({})
                with contextlib.redirect_stdout(io.StringIO()):
                    code = check_tools.main(["--output", str(output)])
                payload = json.loads(output.read_text(encoding="utf-8"))
            finally:
                check_tools.load_tools, check_tools.check_url = old_load, old_check
        self.assertEqual(code, 0)
        # 3 tools, but url "a" is shared -> 2 unique primary urls, 1 homepage.
        self.assertEqual(payload["checked_primary_urls"], 2)
        self.assertEqual(payload["checked_homepages"], 1)
        self.assertEqual(payload["failures"], [])

    def test_dead_primary_url_fails(self):
        self.assertEqual(self._run({"https://example.com/b": False}), 1)

    def test_dead_homepage_is_nonfatal(self):
        self.assertEqual(self._run({"https://example.com/a-home": False}), 0)

    def test_skip_homepages_flag(self):
        old_load, old_check = check_tools.load_tools, check_tools.check_url
        try:
            check_tools.load_tools = lambda: FIXTURE
            calls = []
            check_tools.check_url = lambda url, timeout: (calls.append(url), {"url": url, "status": 200, "ok": True})[1]
            with contextlib.redirect_stdout(io.StringIO()):
                check_tools.main(["--no-write", "--skip-homepages"])
        finally:
            check_tools.load_tools, check_tools.check_url = old_load, old_check
        self.assertNotIn("https://example.com/a-home", calls)


if __name__ == "__main__":
    unittest.main()
