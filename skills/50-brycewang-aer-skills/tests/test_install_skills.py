"""Unit tests for scripts/install_skills.py.

Destination resolution is exercised against a monkeypatched HOME so no real
agent-profile directory (~/.claude, ~/.codex) is ever touched; installs go to
tmp_path.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import install_skills as inst


class TestDefaultDestination:
    def test_claude_uses_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        assert inst.default_destination("claude") == tmp_path / ".claude" / "skills"

    def test_codex_uses_home_without_codex_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        monkeypatch.delenv("CODEX_HOME", raising=False)
        assert inst.default_destination("codex") == tmp_path / ".codex" / "skills"

    def test_codex_home_env_override(self, tmp_path, monkeypatch):
        monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-profile"))
        assert inst.default_destination("codex") == tmp_path / "codex-profile" / "skills"

    def test_unknown_target_raises(self):
        with pytest.raises(ValueError, match="Unsupported target"):
            inst.default_destination("cursor")


class TestSkillDirs:
    def test_returns_only_aer_directories(self):
        dirs = inst.skill_dirs()
        assert dirs, "expected at least one aer-* skill"
        assert all(path.is_dir() and path.name.startswith("aer-") for path in dirs)

    def test_every_skill_dir_has_a_skill_md(self):
        for path in inst.skill_dirs():
            assert (path / "SKILL.md").is_file(), path.name


class TestInstall:
    def test_dry_run_previews_without_writing(self, tmp_path):
        destination = tmp_path / "skills"
        results = inst.install("codex", destination, replace=False, dry_run=True)
        assert results
        assert all(result.startswith("install ") for result in results)
        assert not destination.exists()

    def test_install_copies_every_skill(self, tmp_path):
        destination = tmp_path / "skills"
        results = inst.install("codex", destination, replace=False, dry_run=False)
        assert all(result.startswith("installed ") for result in results)
        expected = sorted(path.name for path in inst.skill_dirs())
        installed = sorted(path.name for path in destination.iterdir() if path.is_dir())
        assert installed == expected
        for name in installed:
            assert (destination / name / "SKILL.md").is_file()

    def test_second_install_skips_existing_by_default(self, tmp_path):
        destination = tmp_path / "skills"
        inst.install("codex", destination, replace=False, dry_run=False)
        results = inst.install("codex", destination, replace=False, dry_run=False)
        assert all(result.startswith("skip existing ") for result in results)

    def test_replace_reinstalls_existing(self, tmp_path):
        destination = tmp_path / "skills"
        inst.install("codex", destination, replace=False, dry_run=False)
        # Plant a stale file inside one installed skill to prove replacement.
        stale = next(destination.iterdir()) / "stale-marker.txt"
        stale.write_text("stale\n", encoding="utf-8")
        results = inst.install("codex", destination, replace=True, dry_run=False)
        assert all(result.startswith("installed ") for result in results)
        assert not stale.exists()

    def test_replace_dry_run_previews_replacement(self, tmp_path):
        destination = tmp_path / "skills"
        inst.install("codex", destination, replace=False, dry_run=False)
        results = inst.install("codex", destination, replace=True, dry_run=True)
        assert all(result.startswith("replace ") for result in results)

    def test_existing_non_directory_destination_raises(self, tmp_path):
        destination = tmp_path / "skills"
        destination.mkdir()
        first_skill = inst.skill_dirs()[0].name
        (destination / first_skill).write_text("occupied\n", encoding="utf-8")
        with pytest.raises(RuntimeError, match="not a directory"):
            inst.install("codex", destination, replace=False, dry_run=False)


class TestSafetyGuards:
    def test_refuses_source_skills_directory(self):
        with pytest.raises(RuntimeError, match="overlaps repository source"):
            inst.install("codex", inst.ROOT / "skills", replace=True, dry_run=True)

    def test_refuses_repository_root(self):
        with pytest.raises(RuntimeError, match="overlaps repository source"):
            inst.install("codex", inst.ROOT, replace=False, dry_run=True)

    def test_refuses_repository_internal_directory(self):
        with pytest.raises(RuntimeError, match="overlaps repository source"):
            inst.install("codex", inst.ROOT / "docs" / "nested", replace=False, dry_run=True)

    def test_ensure_destination_not_source_rejects_nesting(self):
        source = inst.skill_dirs()[0]
        with pytest.raises(RuntimeError, match="source tree"):
            inst.ensure_destination_not_source(source, source / "nested")

    def test_project_scoped_claude_dir_is_allowed_in_dry_run(self):
        # .claude/skills inside the repo is the documented project-scoped
        # install location and must not trip the guard (dry run: no writes).
        results = inst.install("claude", inst.ROOT / ".claude" / "skills", replace=False, dry_run=True)
        assert results


class TestMainCli:
    def test_main_success(self, tmp_path, capsys):
        destination = tmp_path / "skills"
        assert inst.main(["codex", "--dest", str(destination)]) == 0
        assert "installed" in capsys.readouterr().out
        assert destination.is_dir()

    def test_main_refusal_returns_one(self, capsys):
        assert inst.main(["codex", "--dest", str(inst.ROOT / "skills"), "--dry-run"]) == 1
        assert "error:" in capsys.readouterr().err

    def test_main_rejects_unknown_target(self, tmp_path):
        with pytest.raises(SystemExit):
            inst.main(["cursor", "--dest", str(tmp_path)])

    def test_main_dry_run_writes_nothing(self, tmp_path, capsys):
        destination = tmp_path / "skills"
        assert inst.main(["codex", "--dest", str(destination), "--dry-run"]) == 0
        assert not destination.exists()
        assert "install" in capsys.readouterr().out


def test_protected_destinations_include_core_source_trees():
    protected = set(inst.PROTECTED_REPO_DESTINATIONS)
    assert {inst.ROOT, inst.ROOT / "skills", inst.ROOT / "scripts"} <= protected
    assert all(isinstance(path, Path) for path in protected)
