"""Unit tests for scripts/verify_citations.py.

Covers bib parsing, LaTeX/Unicode normalization, verdict classification with a
synthetic recorded resolver, two-way cite<->bib correspondence, and the
prose-level groundedness checks --- all hermetic (no network).
"""

from __future__ import annotations

import json

import pytest

import verify_citations as vc


SYNTHETIC_BIB = """@article{oster_2019,
  author = {Oster, Emily},
  title = {Unobservable Selection and Coefficient Stability: Theory and Evidence},
  journal = {Journal of Business \\& Economic Statistics},
  year = {2019},
  doi = {10.1080/07350015.2016.1227711}
}

@article{dcdh_2020,
  author = {de Chaisemartin, Cl{\\'e}ment and D'Haultf{\\oe}uille, Xavier},
  title = "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects",
  year = 2020,
  doi = {10.1257/aer.20181169}
}

@comment{ignore_me, editorial note that verification must skip}
"""


@pytest.fixture(scope="module")
def entries():
    return vc.parse_bib(SYNTHETIC_BIB)


@pytest.fixture(scope="module")
def bib_index(entries):
    return vc.BibIndex.from_entries(entries)


class TestParseBib:
    def test_all_entries_parsed(self, entries):
        assert [e.key for e in entries] == ["oster_2019", "dcdh_2020", "ignore_me"]

    def test_entry_type_lowercased(self, entries):
        assert entries[0].entry_type == "article"
        assert entries[2].entry_type == "comment"

    def test_braced_field_value_stripped(self, entries):
        assert entries[0].get("year") == "2019"
        assert entries[0].get("author") == "Oster, Emily"

    def test_quoted_and_bareword_values(self, entries):
        assert entries[1].get("title").startswith("Two-Way Fixed Effects")
        assert entries[1].get("year") == "2020"

    def test_missing_field_returns_empty_string(self, entries):
        assert entries[0].get("nonexistent") == ""

    def test_comment_entries_excluded_from_verification(self, entries, bib_index):
        findings = vc.verify_bibliography(entries, resolver=None)
        assert {f.key for f in findings} == {"oster_2019", "dcdh_2020"}
        assert bib_index.keys == {"oster_2019", "dcdh_2020"}


class TestNormalization:
    def test_latex_accents_folded(self):
        assert "clement" in vc.norm_name(r"Cl{\'e}ment")

    def test_latex_oe_ligature(self):
        assert "haultfoeuille" in vc.norm_name(r"D'Haultf{\oe}uille")

    def test_unicode_ligature_folded(self):
        assert vc.norm_name("Haultfœuille") == "haultfoeuille"

    def test_norm_title_strips_punctuation_and_case(self):
        assert vc.norm_title("Two-Way Fixed Effects!") == "two way fixed effects"

    def test_bib_surnames_comma_form(self):
        assert vc.bib_surnames("Oster, Emily") == ["oster"]

    def test_bib_surnames_given_first_form(self):
        assert vc.bib_surnames("Emily Oster and John Smith") == ["oster", "smith"]

    def test_bib_surnames_keeps_significant_particle_token(self):
        assert vc.bib_surnames(r"de Chaisemartin, Cl{\'e}ment") == ["chaisemartin"]

    def test_title_similarity_identical(self):
        assert vc.title_similarity("Mostly Harmless Econometrics", "Mostly Harmless Econometrics") == 1.0

    def test_title_similarity_disjoint_is_low(self):
        sim = vc.title_similarity(
            "Unobservable Selection and Coefficient Stability",
            "Synthetic Control Methods for Comparative Case Studies",
        )
        assert sim < vc.TITLE_SIM_THRESHOLD


class TestVerifyEntryVerdicts:
    DOI = "10.1000/real.doi"

    def _resolver(self, **overrides):
        record = {
            "found": True,
            "source": "test-index",
            "title": "Unobservable Selection and Coefficient Stability: Theory and Evidence",
            "surnames": ["oster"],
            "year": 2019,
            "venue": "JBES",
            "status": "ok",
        }
        record.update(overrides)
        return vc.RecordedResolver({self.DOI: record})

    def _verify(self, resolver, **overrides):
        kwargs = {
            "key": "oster_2019",
            "doi": self.DOI,
            "title": "Unobservable Selection and Coefficient Stability: Theory and Evidence",
            "author": "Oster, Emily",
            "year": 2019,
            "note": "",
            "resolver": resolver,
        }
        kwargs.update(overrides)
        return vc.verify_entry(**kwargs)

    def test_verified_when_metadata_matches(self):
        assert self._verify(self._resolver()).verdict == "VERIFIED"

    def test_missing_doi_without_note_warns(self):
        assert self._verify(None, doi="").verdict == "MISSING_DOI"

    def test_missing_doi_with_no_doi_note_is_exempt(self):
        finding = self._verify(None, doi="", note="No Crossref DOI; JSTOR stable URL only")
        assert finding.verdict == "EXEMPT"

    def test_malformed_doi_fails(self):
        assert self._verify(None, doi="not-a-doi").verdict == "BAD_DOI"

    def test_no_resolver_is_structural_only(self):
        assert self._verify(None).verdict == "STRUCTURAL_OK"

    def test_unknown_doi_is_fabricated(self):
        resolver = vc.RecordedResolver({})
        assert self._verify(resolver).verdict == "FABRICATED"

    def test_index_error_is_unresolved_warning(self):
        resolver = self._resolver(found=False, status="error: HTTP 500")
        finding = self._verify(resolver)
        assert finding.verdict == "UNRESOLVED"
        assert finding.severity == "warn"

    def test_title_mismatch(self):
        finding = self._verify(self._resolver(), title="A Completely Different Manuscript About Volcanoes")
        assert finding.verdict == "TITLE_MISMATCH"

    def test_author_mismatch(self):
        finding = self._verify(self._resolver(), author="Smith, John")
        assert finding.verdict == "AUTHOR_MISMATCH"

    def test_year_mismatch_beyond_tolerance(self):
        finding = self._verify(self._resolver(), year=2016)
        assert finding.verdict == "YEAR_MISMATCH"

    def test_year_within_tolerance_passes(self):
        assert self._verify(self._resolver(), year=2018).verdict == "VERIFIED"

    def test_severity_mapping(self):
        assert vc.Finding("k", "VERIFIED").severity == "ok"
        assert vc.Finding("k", "MISSING_DOI").severity == "warn"
        assert vc.Finding("k", "FABRICATED").severity == "fail"
        # Unknown verdicts fail closed.
        assert vc.Finding("k", "SOMETHING_NEW").severity == "fail"


class TestCitedKeysAndTwoWay:
    def test_latex_cite_commands(self):
        text = r"\citep{oster_2019} and \citet{dcdh_2020, goodman_bacon_2021}"
        assert vc.cited_keys(text) == {"oster_2019", "dcdh_2020", "goodman_bacon_2021"}

    def test_pandoc_bracketed_citations(self):
        assert vc.cited_keys("as shown [@oster_2019; @dcdh_2020]") == {"oster_2019", "dcdh_2020"}

    def test_plain_at_outside_brackets_ignored(self):
        assert vc.cited_keys("email me @example please") == set()

    def test_two_way_reports_undefined_and_uncited(self):
        findings = vc.check_two_way({"oster_2019", "unused_2020"}, r"\cite{oster_2019} \cite{ghost_2021}")
        verdicts = {(f.key, f.verdict) for f in findings}
        assert ("ghost_2021", "UNDEFINED_CITATION") in verdicts
        assert ("unused_2020", "UNCITED") in verdicts

    def test_two_way_clean_manuscript(self):
        findings = vc.check_two_way({"oster_2019"}, r"\cite{oster_2019}")
        assert findings == []


class TestCodeSpanHandling:
    def test_strip_code_fences_preserves_line_numbers(self):
        text = "line one\n```\nhidden_key_2020\n```\nline five"
        stripped = vc._strip_code_fences(text)
        assert len(stripped.split("\n")) == len(text.split("\n"))
        assert "hidden_key_2020" not in stripped

    def test_inline_code_spans_commonmark_pairing(self):
        spans = [content for _, content in vc._inline_code_spans("``a ` b`` and `oster_2019`")]
        assert spans == ["a ` b", "oster_2019"]

    def test_unterminated_backtick_is_not_a_span(self):
        assert vc._inline_code_spans("stray ` only") == []

    def test_line_of(self):
        text = "a\nb\nc"
        assert vc._line_of(text, text.index("c")) == 3


class TestSurnameTokens:
    def test_nobiliary_particles_dropped(self):
        assert vc.surname_tokens("de Chaisemartin") == {"chaisemartin"}

    def test_first_author_tokens_from_group(self):
        assert vc.first_author_tokens("Callaway and Sant'Anna") == {"callaway"}

    def test_et_al_removed(self):
        assert vc.first_author_tokens("Oster et al.") == {"oster"}

    def test_entry_surname_tokens_all_authors(self):
        tokens = vc.entry_surname_tokens("Oster, Emily and de Chaisemartin, Clement")
        assert {"oster", "chaisemartin"} <= tokens


class TestGroundedness:
    def test_author_year_grounded(self, bib_index):
        findings = vc.groundedness_findings(
            "Oster (2019) proposes a bounding approach.",
            bib_index, label="doc.md", check_author_year=True,
        )
        assert [f.verdict for f in findings] == ["GROUNDED"]

    def test_parenthetical_citation_grounded(self, bib_index):
        findings = vc.groundedness_findings(
            "The bias-corrected estimator (Oster, 2019) is used.",
            bib_index, label="doc.md", check_author_year=True,
        )
        assert [f.verdict for f in findings] == ["GROUNDED"]

    def test_multi_author_group_grounds_on_first_author(self, bib_index):
        findings = vc.groundedness_findings(
            "Chaisemartin and D'Haultfoeuille (2020) document the bias.",
            bib_index, label="doc.md", check_author_year=True,
        )
        assert [f.verdict for f in findings] == ["GROUNDED"]

    def test_phantom_citation_flagged(self, bib_index):
        findings = vc.groundedness_findings(
            "Fictional (2018) proves the impossible.",
            bib_index, label="doc.md", check_author_year=True,
        )
        assert [f.verdict for f in findings] == ["PHANTOM_CITATION"]

    def test_year_tolerance_in_resolution(self, bib_index):
        # Bib year 2019, prose says 2020: within YEAR_TOLERANCE, so grounded.
        findings = vc.groundedness_findings(
            "Oster (2020) proposes a bounding approach.",
            bib_index, label="doc.md", check_author_year=True,
        )
        assert [f.verdict for f in findings] == ["GROUNDED"]

    def test_stopword_before_year_is_not_a_citation(self, bib_index):
        findings = vc.groundedness_findings(
            "Table (2021) reports the estimates.",
            bib_index, label="doc.md", check_author_year=True,
        )
        assert findings == []

    def test_inline_code_key_grounded(self, bib_index):
        findings = vc.groundedness_findings(
            "Cite `oster_2019` here.", bib_index, label="doc.md", check_author_year=False,
        )
        assert [f.verdict for f in findings] == ["GROUNDED"]

    def test_dangling_key_flagged(self, bib_index):
        findings = vc.groundedness_findings(
            "Cite `phantom_key_2022` here.", bib_index, label="doc.md", check_author_year=False,
        )
        assert [f.verdict for f in findings] == ["DANGLING_KEY"]

    def test_keys_inside_code_fences_ignored(self, bib_index):
        text = "```\nphantom_key_2022\n```\n"
        findings = vc.groundedness_findings(text, bib_index, label="doc.md", check_author_year=True)
        assert findings == []

    def test_cite_exempt_marker_skips_line(self, bib_index):
        text = "Fictional (2018) argues otherwise. <!-- cite-exempt: style example -->"
        findings = vc.groundedness_findings(text, bib_index, label="doc.md", check_author_year=True)
        assert findings == []

    def test_author_year_disabled_for_key_only_surfaces(self, bib_index):
        findings = vc.groundedness_findings(
            "Fictional (2018) argues otherwise.",
            bib_index, label="doc.md", check_author_year=False,
        )
        assert findings == []

    def test_finding_label_carries_line_number(self, bib_index):
        text = "first line\n\nFictional (2018) argues otherwise.\n"
        findings = vc.groundedness_findings(text, bib_index, label="doc.md", check_author_year=True)
        assert findings[0].key == "doc.md:3"

    def test_resolve_author_year_none_without_tokens(self, bib_index):
        assert bib_index.resolve_author_year(set(), 2019) is None


class TestGoldSetOffline:
    """The shipped gold set must classify exactly as recorded (hermetic)."""

    def test_gold_tuples_match_expected_verdicts(self, repo_root):
        gold = json.loads((repo_root / "scripts" / "citation_gold" / "gold_set.json").read_text(encoding="utf-8"))
        resolver = vc.RecordedResolver.from_file()
        for case in gold["tuples"]:
            finding = vc.verify_entry(
                key=case["key"],
                doi=case.get("doi", ""),
                title=case.get("title", ""),
                author=case.get("author", ""),
                year=case.get("year"),
                note=case.get("note", ""),
                resolver=resolver,
            )
            assert finding.verdict == case["expected"], (case["id"], finding.detail)

    def test_shipped_bibliography_verifies_clean_offline(self, repo_root):
        entries = vc.parse_bib((repo_root / "references.bib").read_text(encoding="utf-8"))
        assert entries
        findings = vc.verify_bibliography(entries, vc.RecordedResolver.from_file())
        fails = [f for f in findings if f.severity == "fail"]
        assert fails == [], [(f.key, f.verdict, f.detail) for f in fails]

    def test_repo_prose_groundedness_scans_clean(self, repo_root):
        entries = vc.parse_bib((repo_root / "references.bib").read_text(encoding="utf-8"))
        findings = vc.check_groundedness(vc.BibIndex.from_entries(entries))
        fails = [f for f in findings if f.severity == "fail"]
        assert fails == [], [(f.key, f.verdict, f.detail) for f in fails]
