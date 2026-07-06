"""Unit tests for scripts/run_example_smoke.py helper functions."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

import run_example_smoke as smoke
import validate_repo


class TestNumericChecksIn:
    def test_counts_pass_and_fail_lines(self):
        output = "\n".join(
            [
                "some setup text",
                "NUMERIC-CHECK | a | got=1.0000 | target=1 tol=0.1 | PASS",
                "NUMERIC-CHECK | b | got=9.0000 | target=1 tol=0.1 | FAIL",
                "NUMERIC-CHECK | c | got=0.9500 | >=0.94 | PASS",
                "trailing text",
            ]
        )
        assert smoke.numeric_checks_in(output) == (3, 1)

    def test_empty_output_counts_zero(self):
        assert smoke.numeric_checks_in("") == (0, 0)

    def test_non_protocol_lines_are_ignored(self):
        output = "\n".join(
            [
                "  NUMERIC-CHECK | indented is not protocol | PASS",
                "NUMERIC-CHECKX| wrong prefix | PASS",
                "the word FAIL alone does not count",
            ]
        )
        assert smoke.numeric_checks_in(output) == (0, 0)

    def test_trailing_whitespace_on_fail_line_still_counts_failed(self):
        output = "NUMERIC-CHECK | x | got=2.0000 | <=1 | FAIL   "
        assert smoke.numeric_checks_in(output) == (1, 1)

    def test_pass_line_is_not_counted_as_failed(self):
        output = "NUMERIC-CHECK | x | got=0.5000 | <=1 | PASS"
        assert smoke.numeric_checks_in(output) == (1, 0)


class TestTextTail:
    def test_short_text_returned_whole(self):
        assert smoke.text_tail("a\nb\nc") == "a\nb\nc"

    def test_long_text_truncated_with_ellipsis_marker(self):
        text = "\n".join(str(i) for i in range(40))
        tail = smoke.text_tail(text, lines=30)
        lines = tail.splitlines()
        assert lines[0] == "..."
        assert lines[1:] == [str(i) for i in range(10, 40)]

    def test_custom_line_budget(self):
        assert smoke.text_tail("a\nb\nc", lines=2) == "...\nb\nc"

    def test_surrounding_whitespace_is_stripped(self):
        assert smoke.text_tail("\n\na\nb\n\n") == "a\nb"


class TestPackageImportNames:
    def test_mapped_package_returns_import_name(self):
        assert smoke.package_import_names("python-dateutil") == ["dateutil"]

    def test_identity_mapping(self):
        assert smoke.package_import_names("numpy") == ["numpy"]

    def test_unmapped_package_falls_back_to_underscored_name(self):
        assert smoke.package_import_names("some-unmapped-pkg") == ["some_unmapped_pkg"]

    def test_every_mapped_name_is_returned_sorted(self):
        for package in set(validate_repo.PYTHON_IMPORT_PACKAGE_MAP.values()):
            names = smoke.package_import_names(package)
            assert names == sorted(names)
            assert names


class TestRVector:
    def test_sorted_quoted_vector(self):
        assert smoke.r_vector({"fixest", "did"}) == 'c("did", "fixest")'

    def test_single_package(self):
        assert smoke.r_vector({"did"}) == 'c("did")'

    def test_empty_set(self):
        assert smoke.r_vector(set()) == "c()"


class TestCommandFor:
    def test_python_script_uses_current_interpreter(self):
        command = smoke.command_for(Path("/somewhere/demo.py"))
        assert command == [sys.executable, "demo.py"]

    def test_r_script_uses_rscript(self):
        command = smoke.command_for(Path("/somewhere/demo.R"))
        assert Path(command[0]).name == "Rscript"
        assert command[1] == "demo.R"

    def test_unsupported_suffix_raises(self):
        with pytest.raises(ValueError, match="unsupported script suffix"):
            smoke.command_for(Path("/somewhere/demo.do"))


class TestIterDemoScripts:
    def test_python_filter_yields_only_python_scripts(self):
        scripts = list(smoke.iter_demo_scripts(None, "python"))
        assert scripts
        assert all(path.suffix == ".py" for _, path in scripts)

    def test_r_filter_yields_only_r_scripts(self):
        scripts = list(smoke.iter_demo_scripts(None, "r"))
        assert scripts
        assert all(path.suffix == ".R" for _, path in scripts)

    def test_selected_demo_restricts_output(self):
        scripts = list(smoke.iter_demo_scripts({"shift-share-demo"}, "all"))
        assert scripts
        assert {demo for demo, _ in scripts} == {"shift-share-demo"}

    def test_all_yielded_scripts_exist_on_disk(self):
        for _, path in smoke.iter_demo_scripts(None, "all"):
            assert path.is_file(), path
