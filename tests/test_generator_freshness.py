"""Smoke tests for generator scripts whose outputs feed trust surfaces.

Each generator that owns a committed artifact must (a) run cleanly in
--check mode against the committed tree, proving the artifact is fresh, and
(b) actually be wired into `make validate` / `make catalog` (guarded here by
Makefile string checks so a lane cannot be silently dropped).

These are the scripts a 2026-07-22 audit found had zero test references
despite generating the repo's public trust claims (scoreboard, coverage map,
release notes).
"""

from __future__ import annotations

import subprocess
import sys
import unittest

from _helpers import ROOT, load_module

build_release_notes = load_module(
    "scripts/build-release-notes.py",
    "aers_build_release_notes",
)

CHECKABLE = [
    [sys.executable, "scripts/build-coverage-map.py", "--check"],
    [sys.executable, "scripts/build-release-notes.py", "--check"],
    [sys.executable, "scripts/build-benchmark-scoreboard.py", "--check"],
    [sys.executable, "scripts/build-evals.py", "--check"],
    [sys.executable, "scripts/check-mirror-sync.py"],
    [sys.executable, "scripts/check-catalog-coverage.py"],
    [sys.executable, "scripts/check-ecosystem.py"],
    [sys.executable, "scripts/check-plugin-source-location.py"],
]


class TestGeneratorFreshness(unittest.TestCase):
    def test_release_page_uses_canonical_upstream_not_contributor_fork(self):
        self.assertEqual(
            build_release_notes._repo_slug(),
            "brycewang-stanford/Auto-Empirical-Research-Skills",
        )

    def test_generators_pass_check_mode_against_committed_tree(self):
        for cmd in CHECKABLE:
            with self.subTest(cmd=" ".join(cmd[1:])):
                proc = subprocess.run(
                    cmd, cwd=ROOT, capture_output=True, text=True, timeout=300
                )
                self.assertEqual(
                    proc.returncode,
                    0,
                    msg=f"{' '.join(cmd)} failed:\n{proc.stdout}\n{proc.stderr}",
                )

    def test_validate_gate_wires_the_lanes(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        for script in (
            "check-readme-stats.py",
            "check-mirror-sync.py",
            "build-coverage-map.py --check",
            "build-release-notes.py --check",
            "build-benchmark-scoreboard.py --check",
        ):
            self.assertIn(script, makefile, msg=f"{script} not wired into Makefile")


class TestSkillDiscoveryExclusions(unittest.TestCase):
    def test_codex_ports_are_pruned(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import skill_discovery
        finally:
            sys.path.pop(0)
        dirnames = ["a", "skills-codex", "skills-codex-claude-review", ".git", "b"]
        self.assertEqual(skill_discovery.prune(dirnames), ["a", "b"])

    def test_catalog_contains_no_codex_port_paths(self):
        import json

        data = json.loads((ROOT / "catalog" / "skills.json").read_text(encoding="utf-8"))
        offenders = [
            s["path"] for s in data["skills"] if "/skills-codex" in s["path"]
        ]
        self.assertEqual(offenders, [])
