"""End-to-end gate tests: run each quality tool as a subprocess (hermetic).

These are the cheap versions of the repo's own preflight commands. Everything
here is offline: the citation gate runs against recorded responses, and the
validator only shells out to local tools.
"""

from __future__ import annotations

import subprocess
import sys

import pytest


def run_tool(repo_root, *args, timeout=120):
    return subprocess.run(
        [sys.executable, *args],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


@pytest.mark.slow
class TestValidateRepo:
    def test_validator_reports_no_errors_about_tests_dir(self, repo_root):
        """The validator scans the whole tree (text hygiene, markdown links,
        marker words), so this suite itself is in scope. Whatever in-progress
        errors the working tree carries elsewhere, tests/ must add none."""
        result = run_tool(repo_root, "scripts/validate_repo.py")
        offending = [
            line
            for line in result.stdout.splitlines()
            if line.startswith("ERROR:") and "tests/" in line
        ]
        assert offending == [], "validator errors caused by tests/:\n" + "\n".join(offending)

    @pytest.mark.xfail(
        reason=(
            "the working tree carries in-progress validator errors outside "
            "tests/ (e.g. new docs/*.md not yet linked from the READMEs); "
            "this test records the full gate and passes once those are fixed"
        ),
        strict=False,
    )
    def test_validator_exits_zero(self, repo_root):
        result = run_tool(repo_root, "scripts/validate_repo.py")
        assert result.returncode == 0, result.stdout


class TestSelftests:
    def test_skill_audit_selftest_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/skill_audit.py", "--selftest")
        assert result.returncode == 0, result.stdout
        assert "self-tests passed" in result.stdout

    def test_verify_citations_selftest_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/verify_citations.py", "--selftest")
        assert result.returncode == 0, result.stdout
        assert "selftest PASS" in result.stdout


class TestOtherGates:
    def test_skillopt_routing_gate_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/run_skillopt_gate.py")
        assert result.returncode == 0, result.stdout
        assert "SkillOpt gate passed" in result.stdout

    def test_skill_audit_makefile_gate_passes(self, repo_root):
        result = run_tool(
            repo_root, "scripts/skill_audit.py", "--gate", "85", "--substance-gate", "8"
        )
        assert result.returncode == 0, result.stdout
        assert "GATE PASSED" in result.stdout
        assert "SUBSTANCE GATE PASSED" in result.stdout

    def test_verify_citations_offline_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/verify_citations.py", "--offline")
        assert result.returncode == 0, result.stdout

    def test_verify_citations_structural_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/verify_citations.py")
        assert result.returncode == 0, result.stdout

    def test_verify_citations_groundedness_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/verify_citations.py", "--groundedness")
        assert result.returncode == 0, result.stdout

    def test_example_smoke_dry_run_passes(self, repo_root):
        result = run_tool(repo_root, "scripts/run_example_smoke.py", "--dry-run")
        assert result.returncode == 0, result.stdout
        assert "Dry run complete" in result.stdout

    def test_example_smoke_rejects_unknown_demo(self, repo_root):
        result = run_tool(
            repo_root, "scripts/run_example_smoke.py", "--demo", "no-such-demo", "--dry-run"
        )
        assert result.returncode == 2
        assert "unknown demo" in result.stdout
