"""Unit tests for scripts/validate_repo.py pure helpers and registries."""

from __future__ import annotations

import re

import validate_repo as vr


# Assembled at runtime so this test file does not itself trip the repository's
# unfinished-work marker scan.
_TODO_MARKER = "TO" + "DO"


class TestRel:
    def test_rel_returns_posix_relative_path(self):
        assert vr.rel(vr.ROOT / "scripts" / "validate_repo.py") == "scripts/validate_repo.py"

    def test_rel_nested_path(self):
        path = vr.ROOT / "examples" / "shift-share-demo" / "README.md"
        assert vr.rel(path) == "examples/shift-share-demo/README.md"


class TestDeclaredDeps:
    def test_python_comment_style(self, tmp_path):
        script = tmp_path / "demo.py"
        script.write_text("# Deps: numpy, pandas\nimport numpy\n", encoding="utf-8")
        assert vr.declared_deps(script) == ["numpy", "pandas"]

    def test_docstring_style(self, tmp_path):
        script = tmp_path / "demo.py"
        script.write_text('"""Demo.\nDeps: numpy, scipy\n"""\n', encoding="utf-8")
        assert vr.declared_deps(script) == ["numpy", "scipy"]

    def test_parenthetical_note_is_stripped(self, tmp_path):
        script = tmp_path / "demo.py"
        script.write_text("# Deps: numpy, rdrobust (optional extras)\n", encoding="utf-8")
        assert vr.declared_deps(script) == ["numpy", "rdrobust"]

    def test_names_are_lowercased(self, tmp_path):
        script = tmp_path / "demo.R"
        script.write_text("# Deps: Fixest, DID\n", encoding="utf-8")
        assert vr.declared_deps(script) == ["fixest", "did"]

    def test_no_declaration_returns_empty(self, tmp_path):
        script = tmp_path / "demo.py"
        script.write_text("import numpy\n", encoding="utf-8")
        assert vr.declared_deps(script) == []

    def test_only_first_declaration_wins(self, tmp_path):
        script = tmp_path / "demo.py"
        script.write_text("# Deps: numpy\n# Deps: pandas\n", encoding="utf-8")
        assert vr.declared_deps(script) == ["numpy"]


class TestHeadingSlugsAndTargets:
    def test_numbered_heading_slug(self):
        assert (
            vr.github_heading_slug("1. Difference-in-differences (staggered adoption)")
            == "1-difference-in-differences-staggered-adoption"
        )

    def test_slash_becomes_double_hyphen(self):
        assert vr.github_heading_slug("3. Shift-share / Bartik") == "3-shift-share--bartik"

    def test_inline_code_and_links_are_unwrapped(self):
        assert vr.github_heading_slug("AER: Insights `word-count` PDF") == "aer-insights-word-count-pdf"
        assert vr.github_heading_slug("[methods reference](./methods-reference.md)") == "methods-reference"

    def test_normalize_markdown_target_angle_brackets(self):
        assert vr.normalize_markdown_target("<./file.md>") == "./file.md"

    def test_normalize_markdown_target_drops_link_title(self):
        assert vr.normalize_markdown_target('path.md "title"') == "path.md"

    def test_normalize_markdown_target_unquotes_percent_encoding(self):
        assert vr.normalize_markdown_target("my%20file.md") == "my file.md"


class TestMarkdownAnchors:
    def test_headings_and_html_anchors(self, tmp_path):
        fixture = tmp_path / "anchors.md"
        fixture.write_text(
            "# Methods Reference\n"
            "## Methods Reference\n"
            '<a id="custom-anchor"></a>\n'
            '<span name="legacy-anchor"></span>\n',
            encoding="utf-8",
        )
        anchors = vr.markdown_anchors(fixture)
        assert {
            "methods-reference",
            "methods-reference-1",
            "custom-anchor",
            "legacy-anchor",
        } <= anchors


class TestMakeTargetBody:
    FIXTURE = "\n".join(
        [
            ".PHONY: first second",
            "",
            "first:",
            "\tpython3 scripts/validate_repo.py",
            "\tgit diff --check",
            "",
            "second:",
            "\tgit diff --cached --check",
            "",
        ]
    )

    def test_body_of_named_target(self):
        body = vr.make_target_body(self.FIXTURE, "first")
        assert "python3 scripts/validate_repo.py" in body
        assert "git diff --check" in body

    def test_body_stops_at_next_target(self):
        assert "cached" not in vr.make_target_body(self.FIXTURE, "first")

    def test_missing_target_returns_empty(self):
        assert vr.make_target_body(self.FIXTURE, "absent") == ""


class TestUnfinishedMarkers:
    def test_standalone_marker_detected(self):
        assert vr.unfinished_marker_in_text(f"finish this {_TODO_MARKER} soon") == _TODO_MARKER

    def test_marker_is_case_insensitive(self):
        assert vr.unfinished_marker_in_text(_TODO_MARKER.lower()) == _TODO_MARKER

    def test_marker_inside_word_not_flagged(self):
        assert vr.unfinished_marker_in_text(f"prefix{_TODO_MARKER}suffix") is None

    def test_clean_text_returns_none(self):
        assert vr.unfinished_marker_in_text("this method is fully documented") is None


class TestInlineCodeSpans:
    def test_simple_spans(self):
        assert vr.inline_code_spans("`a1a` and `b2b`") == ["a1a", "b2b"]

    def test_fence_pairs_with_matching_run_length(self):
        # A triple-backtick fence closes only on a triple run, so the inline
        # span after it is still parsed correctly.
        assert vr.inline_code_spans("```\npoly4\n``` then `rdrobust`") == ["\npoly4\n", "rdrobust"]

    def test_double_backtick_span_may_contain_single_backtick(self):
        assert vr.inline_code_spans("``a ` b``") == ["a ` b"]

    def test_unterminated_run_is_not_a_span(self):
        assert vr.inline_code_spans("stray ` backtick only") == []

    def test_tool_tokens_extracts_snake_case_words(self):
        text = "Use `callaway_santanna` then `aggte`; ignore plain aggte and `ab`."
        assert vr.tool_tokens_in(text) == {"callaway_santanna", "aggte"}


class TestToolBindingBlock:
    FIXTURE = "\n".join(
        [
            "intro prose",
            vr.TOOL_BINDING_OPEN,
            "| Design | Call (StatsPAI) | Do not hand-roll |",
            "|---|---|---|",
            "| Staggered DiD | `callaway_santanna` then `aggte` | a `poly4` TWFE by hand |",
            "| RDD | `rdrobust`, `rddensity` | a global polynomial |",
            vr.TOOL_BINDING_CLOSE,
            "trailing prose",
        ]
    )

    def test_block_extraction(self):
        block = vr.extract_tool_binding_block(self.FIXTURE)
        assert block is not None
        assert "callaway_santanna" in block
        assert "trailing prose" not in block

    def test_missing_markers_return_none(self):
        assert vr.extract_tool_binding_block("no markers here") is None

    def test_bound_tools_come_only_from_statspai_column(self):
        block = vr.extract_tool_binding_block(self.FIXTURE)
        tools = vr.bound_tools_in_block(block)
        assert tools == {"callaway_santanna", "aggte", "rdrobust", "rddensity"}
        assert "poly4" not in tools

    def test_block_without_statspai_header_binds_nothing(self):
        block = "| Design | Estimator |\n|---|---|\n| DiD | `did_thing` |\n"
        assert vr.bound_tools_in_block(block) == set()


class TestStatspaiRegistry:
    def test_load_registry_ignores_comments_and_blanks(self, tmp_path):
        registry_file = tmp_path / "tools.txt"
        registry_file.write_text("# comment\n\nrdrobust\naggte\n", encoding="utf-8")
        assert vr.load_statspai_registry(registry_file) == {"rdrobust", "aggte"}

    def test_shipped_registry_entries_are_unique_and_well_formed(self):
        raw_entries = [
            line.strip()
            for line in vr.STATSPAI_REGISTRY_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        assert raw_entries, "registry should not be empty"
        assert len(raw_entries) == len(set(raw_entries)), "registry has duplicate tools"
        for tool in raw_entries:
            assert re.fullmatch(r"[a-z][a-z0-9_]+", tool), tool

    def test_every_registry_tool_documented_in_hub_skill(self):
        registry = vr.load_statspai_registry(vr.STATSPAI_REGISTRY_FILE)
        hub = vr.ROOT / "skills" / vr.STATSPAI_HUB_SKILL / "SKILL.md"
        hub_tokens = vr.tool_tokens_in(hub.read_text(encoding="utf-8"))
        assert registry <= hub_tokens


class TestRepositoryResources:
    def test_resources_parsed_from_section_only(self):
        fixture = "\n".join(
            [
                "# Skill",
                "",
                "## Repository Resources",
                "",
                "- Docs: `docs/methods-reference.md`",
                "- Demo: `examples/rdd-polynomial-demo/`",
                "- Non-resource token: `aer-identification`",
                "",
                "## Handoff",
                "",
                "- `templates/python/` mentioned after the section is ignored",
            ]
        )
        assert vr.repository_resources_from_skill(fixture) == [
            "docs/methods-reference.md",
            "examples/rdd-polynomial-demo/",
        ]

    def test_no_section_returns_empty(self):
        assert vr.repository_resources_from_skill("# Skill\n\nprose only\n") == []


class TestPythonImportHelpers:
    def test_top_level_imports_collects_import_and_from(self, tmp_path):
        script = tmp_path / "mod.py"
        script.write_text(
            "import numpy as np\n"
            "import os.path\n"
            "from pandas import DataFrame\n"
            "from . import sibling\n",
            encoding="utf-8",
        )
        assert vr.top_level_python_imports(script) == {"numpy", "os", "pandas"}

    def test_syntax_error_returns_empty_set(self, tmp_path):
        script = tmp_path / "broken.py"
        script.write_text("def broken(:\n", encoding="utf-8")
        assert vr.top_level_python_imports(script) == set()

    def test_third_party_packages_exclude_stdlib(self, tmp_path):
        script = tmp_path / "mod.py"
        script.write_text("import json\nimport numpy\nimport dateutil\n", encoding="utf-8")
        assert vr.third_party_python_import_packages(script) == {"numpy", "python-dateutil"}

    def test_stdlib_module_set_contains_common_modules(self):
        modules = vr.python_stdlib_modules()
        assert {"json", "sys", "pathlib", "argparse"} <= modules

    def test_r_library_packages(self, tmp_path):
        script = tmp_path / "demo.R"
        script.write_text(
            "suppressMessages({\n  library(fixest)\n  library(did)\n})\nlibrary( ggplot2 )\n",
            encoding="utf-8",
        )
        assert vr.r_library_packages(script) == {"fixest", "did", "ggplot2"}


class TestExecutableBit:
    def test_mode_644_is_not_executable(self, tmp_path):
        path = tmp_path / "script.py"
        path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        path.chmod(0o644)
        assert not vr.has_executable_bit(path)

    def test_mode_755_is_executable(self, tmp_path):
        path = tmp_path / "script.py"
        path.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        path.chmod(0o755)
        assert vr.has_executable_bit(path)


class TestBibKeyCandidateRe:
    def test_valid_key_shapes(self):
        for key in ("oster_2019", "callaway_santanna_2021", "dcdh_2020"):
            assert vr.BIB_KEY_CANDIDATE_RE.fullmatch(key), key

    def test_invalid_key_shapes(self):
        for key in ("Oster_2019", "oster_1875", "oster2019", "_oster_2019"):
            assert not vr.BIB_KEY_CANDIDATE_RE.fullmatch(key), key


class TestRegistryConsistency:
    """The module-level registries must agree with what is on disk."""

    def test_every_registered_demo_directory_exists(self):
        for demo_name, expected_files in vr.EXPECTED_EXAMPLE_DEMOS.items():
            demo_dir = vr.ROOT / "examples" / demo_name
            assert demo_dir.is_dir(), demo_name
            for file_name in expected_files:
                assert (demo_dir / file_name).is_file(), f"{demo_name}/{file_name}"

    def test_every_demo_declares_a_readme(self):
        for demo_name, expected_files in vr.EXPECTED_EXAMPLE_DEMOS.items():
            assert "README.md" in expected_files, demo_name

    def test_required_resource_links_point_at_existing_files(self):
        for skill_path, resources in vr.REQUIRED_RESOURCE_LINKS.items():
            assert skill_path.is_file(), skill_path
            for resource in resources:
                assert (vr.ROOT / resource.rstrip("/")).exists(), resource

    def test_required_cli_scripts_exist_and_are_executable(self):
        for path in vr.REQUIRED_CLI_SCRIPTS:
            assert path.is_file(), path
            assert vr.has_executable_bit(path), path

    def test_import_map_packages_are_pinned_in_requirements(self):
        pinned = vr.python_requirement_names()
        assert set(vr.PYTHON_IMPORT_PACKAGE_MAP.values()) <= pinned

    def test_numeric_check_helper_exists(self):
        assert vr.NUMERIC_CHECK_HELPER.is_file()
