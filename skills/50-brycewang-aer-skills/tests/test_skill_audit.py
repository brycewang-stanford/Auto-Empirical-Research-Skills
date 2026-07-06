"""Unit tests for scripts/skill_audit.py scorers plus repo-level gate invariants."""

from __future__ import annotations

import skill_audit as sa
import validate_repo as vr


class TestEstimateTokens:
    def test_four_chars_per_token(self):
        assert sa.estimate_tokens("x" * 400) == 100

    def test_rounds_up(self):
        assert sa.estimate_tokens("abc") == 1
        assert sa.estimate_tokens("abcde") == 2

    def test_monotonic(self):
        assert sa.estimate_tokens("x" * 400) > sa.estimate_tokens("x" * 40)


class TestScoreBudget:
    def test_in_band_scores_full(self):
        assert sa.score_budget(sa.TOKEN_BUDGET_LOW) == 1.0
        assert sa.score_budget(1500) == 1.0
        assert sa.score_budget(sa.TOKEN_BUDGET_HIGH) == 1.0

    def test_thin_document_penalized_proportionally(self):
        assert sa.score_budget(150) == 0.5

    def test_over_budget_decays_to_zero(self):
        assert sa.score_budget(sa.TOKEN_BUDGET_HIGH + sa.TOKEN_OVER_SLACK) == 0.0
        # One tenth of the slack over budget costs one tenth of the score.
        assert sa.score_budget(sa.TOKEN_BUDGET_HIGH + sa.TOKEN_OVER_SLACK // 10) == 0.9


class TestScoreTrigger:
    def test_full_score_description(self):
        score, issues = sa.score_trigger("Use when drafting after the data exist, before submission.")
        assert score == 1.0
        assert issues == []

    def test_missing_use_when_flagged(self):
        score, issues = sa.score_trigger("Draft the results once the tables exist.")
        assert score < 1.0
        assert "no-use-when" in issues

    def test_empty_description(self):
        assert sa.score_trigger("") == (0.0, ["no-description"])

    def test_over_long_description_flagged(self):
        _, issues = sa.score_trigger("Use when " + "x " * 250)
        assert "too-long" in issues

    def test_too_short_description_flagged(self):
        _, issues = sa.score_trigger("Use when short.")
        assert "too-short" in issues


class TestScoreStructure:
    def test_all_house_sections_present(self):
        score, missing = sa.score_structure(list(sa.HOUSE_SECTIONS))
        assert score == 1.0
        assert missing == []

    def test_missing_sections_reported(self):
        score, missing = sa.score_structure(["Overview"])
        assert score == 0.25
        assert set(missing) == {"When to Use", "Handoff", "Anti-Patterns"}

    def test_match_is_case_insensitive_substring(self):
        score, _ = sa.score_structure(["1. overview of the task"])
        assert score == 0.25


class TestScoreDirective:
    def test_bullets_beat_prose(self):
        bullets = "\n".join(f"- step {i}" for i in range(10))
        prose = "\n".join("This sentence explains a concept at length." for _ in range(10))
        assert sa.score_directive(bullets)[0] > sa.score_directive(prose)[0]

    def test_empty_body_scores_zero(self):
        assert sa.score_directive("") == (0.0, 0, 0)

    def test_directive_verb_line_counts(self):
        assert sa.is_directive_line("Report the exact sample size.")
        assert sa.is_directive_line("- any list item")
        assert sa.is_directive_line("| any | table | row |")
        assert not sa.is_directive_line("The model is a linear specification.")


class TestScoreHygiene:
    def test_filler_scores_hits(self):
        _, hits = sa.score_hygiene("The model delve into the data and plays a crucial role here.\n", 12)
        assert hits

    def test_quoted_filler_is_skipped(self):
        _, hits = sa.score_hygiene('Avoid writing "this plays a crucial role" in the body.\n', 12)
        assert not hits

    def test_anti_pattern_section_is_negation_context(self):
        body = "## Anti-Patterns\n- delve into the literature without naming papers\n"
        _, hits = sa.score_hygiene(body, 12)
        assert not hits

    def test_econometric_leverage_not_flagged(self):
        _, hits = sa.score_hygiene("Report leverage and Cook's distance.\n", 8)
        assert not hits

    def test_leverage_as_verb_is_flagged(self):
        _, hits = sa.score_hygiene("We leverage the panel structure here.\n", 8)
        assert "leverage (verb)" in hits

    def test_clean_body_scores_full(self):
        score, hits = sa.score_hygiene("Report the point estimate and its cluster-robust SE.\n", 10)
        assert score == 1.0
        assert hits == []


class TestScoreHandoff:
    def test_section_and_routing_score_full(self):
        assert sa.score_handoff(["Handoff"], "NEXT SKILL: aer-submission") == 1.0

    def test_section_only(self):
        assert sa.score_handoff(["Handoff"], "no routing text") == 0.6

    def test_routing_only(self):
        assert sa.score_handoff(["Overview"], "NEXT STEP: draft tables") == 0.4

    def test_arrow_counts_as_routing(self):
        assert sa.score_handoff(["Overview"], "results → tables") == 0.4

    def test_absent_everywhere(self):
        assert sa.score_handoff(["Overview"], "no routing here") == 0.0


class TestScoreSubstance:
    RICH = (
        'The reform raises earnings by 4.2 percent (p = 0.01) over 48,212 firms.\n'
        '> "The point estimate implies a $4.5 billion gain," the authors write.\n'
        '```latex\nY = \\beta D\n```\n'
        'Here $\\beta$ is the object of interest.\n'
    )

    def test_rich_body_clears_floor(self):
        assert sa.score_substance(self.RICH)["anchors"] >= sa.SUBSTANCE_FLOOR

    def test_thin_body_trips_floor(self):
        thin = "Draft the section. Keep it tight. Route onward when done.\n"
        assert sa.score_substance(thin)["anchors"] < sa.SUBSTANCE_FLOOR

    def test_figures_counted(self):
        assert sa.score_substance("4.2 percent and 0.042 and 48,212")["figures"] >= 3

    def test_short_quotes_are_not_exemplars(self):
        assert sa.score_substance('say "no" here')["exemplars"] == 0

    def test_long_quote_is_an_exemplar(self):
        body = '"identification comes from within-state variation over time" is quoted.\n'
        assert sa.score_substance(body)["exemplars"] == 1

    def test_blockquote_counts_once_per_block(self):
        body = "> quoted line one\n> quoted line two\nplain\n> second block\n"
        assert sa.score_substance(body)["exemplars"] == 2

    def test_anchor_total_is_sum_of_parts(self):
        substance = sa.score_substance(self.RICH)
        assert substance["anchors"] == (
            substance["figures"] + substance["exemplars"] + substance["blocks"]
        )


class TestGrade:
    def test_cutoffs(self):
        assert sa.grade(95) == "A"
        assert sa.grade(90) == "A"
        assert sa.grade(89.9) == "B"
        assert sa.grade(75) == "C"
        assert sa.grade(60) == "D"
        assert sa.grade(59.9) == "F"


class TestSplitFrontmatter:
    def test_fields_and_body_separated(self):
        text = "---\nname: aer-demo\ndescription: Use when testing.\n---\n# Body\n"
        fields, body = sa.split_frontmatter(text)
        assert fields == {"name": "aer-demo", "description": "Use when testing."}
        assert body == "# Body\n"

    def test_no_frontmatter_returns_whole_text(self):
        fields, body = sa.split_frontmatter("# Just a body\n")
        assert fields == {}
        assert body == "# Just a body\n"


class TestAuditSkill:
    def test_synthetic_skill_audit_shape(self, tmp_path):
        skill_dir = tmp_path / "aer-synthetic"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: aer-synthetic\n"
            "description: Use when testing the auditor after fixtures exist.\n"
            "---\n"
            "## Overview\n"
            "- Report the effect as 4.2 percent (p = 0.01) over 48,212 firms.\n"
            "## When to Use\n"
            "- Use after the estimates exist.\n"
            "## Handoff\n"
            "NEXT SKILL: aer-submission\n"
            "## Anti-Patterns\n"
            "- Never round p-values to zero.\n",
            encoding="utf-8",
        )
        result = sa.audit_skill(skill_md)
        assert result["name"] == "aer-synthetic"
        assert set(result["dimensions"]) == set(sa.WEIGHTS)
        assert 0 <= result["score"] <= 100
        assert result["grade"] in "ABCDF"
        assert result["dimensions"]["structure"] == 1.0
        assert result["dimensions"]["handoff"] == 1.0
        assert result["substance"]["anchors"] > 0

    def test_recommendations_flag_thin_substance(self, tmp_path):
        skill_dir = tmp_path / "aer-thin"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\nname: aer-thin\ndescription: Use when testing.\n---\n## Overview\nShort.\n",
            encoding="utf-8",
        )
        result = sa.audit_skill(skill_md)
        assert result["substance"]["anchors"] < sa.SUBSTANCE_FLOOR
        assert any("THIN" in tip for tip in result["recommendations"])


class TestRepoGateInvariants:
    """The shipped skills must clear the Makefile audit-skills-gate thresholds."""

    SCORE_GATE = 85
    SUBSTANCE_GATE = 8

    def test_makefile_gate_matches_asserted_thresholds(self, repo_root):
        body = vr.make_target_body((repo_root / "Makefile").read_text(encoding="utf-8"), "audit-skills-gate")
        assert f"--gate {self.SCORE_GATE} --substance-gate {self.SUBSTANCE_GATE}" in body

    def test_every_skill_clears_the_score_gate(self):
        results = sa.collect(None)
        assert results, "no skills audited"
        failing = [(r["name"], r["score"]) for r in results if r["score"] < self.SCORE_GATE]
        assert failing == []

    def test_every_skill_clears_the_substance_gate(self):
        results = sa.collect(None)
        thin = [
            (r["name"], r["substance"]["anchors"])
            for r in results
            if r["substance"]["anchors"] < self.SUBSTANCE_GATE
        ]
        assert thin == []

    def test_dimension_weights_sum_to_100(self):
        assert sum(sa.WEIGHTS.values()) == 100
