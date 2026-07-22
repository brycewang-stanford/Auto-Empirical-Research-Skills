"""Unit tests for scripts/scaffold_project.py using tmp_path destinations."""

from __future__ import annotations

import pytest

import scaffold_project as sp


EXPECTED_ENTRY_FILE = {
    "stata": "run_all.do",
    "r": "run_all.R",
    "python": "run_all.py",
    "skeleton": "run_all.do",
}


class TestScaffoldTemplates:
    @pytest.mark.parametrize("kind", sorted(sp.SOURCES))
    def test_scaffold_creates_expected_entry_file(self, kind, tmp_path):
        destination = tmp_path / kind
        actions = sp.scaffold(kind=kind, destination=destination, replace=False, dry_run=False)
        assert actions
        assert (destination / EXPECTED_ENTRY_FILE[kind]).is_file()
        assert (destination / "README.md").is_file()

    @pytest.mark.parametrize("kind", sorted(sp.SOURCES))
    def test_scaffold_copies_full_source_tree(self, kind, tmp_path):
        destination = tmp_path / kind
        sp.scaffold(kind=kind, destination=destination, replace=False, dry_run=False)
        source_names = {item.name for item in sp.SOURCES[kind].iterdir()}
        copied_names = {item.name for item in destination.iterdir()}
        assert copied_names == source_names

    def test_skeleton_scaffold_includes_registers(self, tmp_path):
        destination = tmp_path / "pkg"
        sp.scaffold(kind="skeleton", destination=destination, replace=False, dry_run=False)
        assert (destination / "docs" / "exhibit-register.md").is_file()
        assert (destination / "data" / "codebook" / "source-register.md").is_file()


class TestDryRun:
    def test_dry_run_lists_actions_without_writing(self, tmp_path):
        destination = tmp_path / "planned"
        actions = sp.scaffold(kind="python", destination=destination, replace=False, dry_run=True)
        assert actions
        assert all(action.startswith("copy ") for action in actions)
        assert not destination.exists()


class TestSafetyRefusals:
    def test_refuses_non_empty_destination_without_replace(self, tmp_path):
        destination = tmp_path / "busy"
        destination.mkdir()
        (destination / "keep.md").write_text("existing\n", encoding="utf-8")
        with pytest.raises(RuntimeError, match="not empty"):
            sp.scaffold(kind="python", destination=destination, replace=False, dry_run=False)

    def test_replace_overwrites_non_empty_destination(self, tmp_path):
        destination = tmp_path / "busy"
        destination.mkdir()
        (destination / "stale.md").write_text("old\n", encoding="utf-8")
        sp.scaffold(kind="python", destination=destination, replace=True, dry_run=False)
        assert not (destination / "stale.md").exists()
        assert (destination / "run_all.py").is_file()

    def test_empty_existing_destination_is_allowed(self, tmp_path):
        destination = tmp_path / "empty"
        destination.mkdir()
        sp.scaffold(kind="python", destination=destination, replace=False, dry_run=False)
        assert (destination / "run_all.py").is_file()

    def test_refuses_destination_that_is_a_file(self, tmp_path):
        destination = tmp_path / "a-file"
        destination.write_text("occupied\n", encoding="utf-8")
        with pytest.raises(RuntimeError, match="not a directory"):
            sp.scaffold(kind="python", destination=destination, replace=False, dry_run=False)

    def test_refuses_template_source_as_destination(self):
        with pytest.raises(RuntimeError):
            sp.scaffold(kind="stata", destination=sp.SOURCES["stata"], replace=True, dry_run=True)

    def test_refuses_destination_nested_inside_source(self):
        with pytest.raises(RuntimeError):
            sp.scaffold(
                kind="stata",
                destination=sp.SOURCES["stata"] / "nested-output",
                replace=False,
                dry_run=True,
            )

    def test_refuses_repository_root(self):
        # The repo root is both a parent of the template source and the repo
        # itself; either guard must reject it.
        with pytest.raises(RuntimeError):
            sp.scaffold(kind="stata", destination=sp.ROOT, replace=False, dry_run=True)

    def test_refuses_repository_internal_destination(self):
        with pytest.raises(RuntimeError, match="inside this repository"):
            sp.scaffold(kind="stata", destination=sp.ROOT / "docs" / "out", replace=False, dry_run=True)


class TestMainCli:
    def test_main_success_prints_actions_and_returns_zero(self, tmp_path, capsys):
        destination = tmp_path / "proj"
        assert sp.main(["python", str(destination)]) == 0
        out = capsys.readouterr().out
        assert "copy " in out
        assert (destination / "run_all.py").is_file()

    def test_main_error_returns_one_with_stderr_message(self, tmp_path, capsys):
        destination = tmp_path / "busy"
        destination.mkdir()
        (destination / "x.md").write_text("existing\n", encoding="utf-8")
        assert sp.main(["python", str(destination)]) == 1
        assert "error:" in capsys.readouterr().err

    def test_main_rejects_unknown_kind(self, tmp_path):
        with pytest.raises(SystemExit):
            sp.main(["fortran", str(tmp_path / "x")])
