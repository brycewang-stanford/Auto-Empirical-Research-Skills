"""Tests for routing: curation tiers, ranked search, and the routing eval."""

from __future__ import annotations

import json
import unittest

from _helpers import ROOT, load_module

enrich = load_module("scripts/build-catalog-enrich.py", "aers_enrich_routing")
finder = load_module("scripts/find-skill.py", "aers_find_skill")
routing = load_module("scripts/check-routing.py", "aers_check_routing")


def _skill(path, name):
    return {"path": path, "name": name}


class TestAssignTiers(unittest.TestCase):
    CURATION = {
        "core_prefixes": ["skills/50-x/"],
        "out_of_domain": {"prefixes": ["skills/43-x/domains/physics/"]},
        "canonical": {"_why": "ignored", "proofread": "skills/12-a/proofread/SKILL.md"},
    }

    def test_precedence(self):
        skills = [
            _skill("skills/12-a/proofread/SKILL.md", "proofread"),
            _skill("skills/50-x/proofread/SKILL.md", "proofread"),
            _skill("skills/50-x/aer/SKILL.md", "aer"),
            _skill("skills/43-x/domains/physics/q/SKILL.md", "q"),
            _skill("skills/60-y/other/SKILL.md", "other"),
        ]
        tiers, uncurated = enrich.assign_tiers(skills, self.CURATION)
        self.assertEqual(tiers["skills/12-a/proofread/SKILL.md"], {"tier": "extended", "canonical_of": 2})
        # A non-preferred copy is a duplicate even inside a core collection.
        self.assertEqual(tiers["skills/50-x/proofread/SKILL.md"]["tier"], "duplicate")
        self.assertEqual(tiers["skills/50-x/aer/SKILL.md"]["tier"], "core")
        self.assertEqual(tiers["skills/43-x/domains/physics/q/SKILL.md"]["tier"], "out-of-domain")
        self.assertEqual(tiers["skills/60-y/other/SKILL.md"]["tier"], "extended")
        self.assertEqual(uncurated, [])

    def test_stale_canonical_raises(self):
        with self.assertRaises(ValueError):
            enrich.assign_tiers([_skill("skills/1/a/SKILL.md", "a")],
                                {"canonical": {"a": "skills/2/a/SKILL.md"}})

    def test_uncurated_duplicates_reported(self):
        _, uncurated = enrich.assign_tiers(
            [_skill("skills/1/a/SKILL.md", "a"), _skill("skills/2/a/SKILL.md", "a")], {})
        self.assertEqual(uncurated, ["a"])


class TestCommittedCuration(unittest.TestCase):
    def test_every_duplicate_name_is_curated(self):
        summary = json.loads((ROOT / "catalog" / "skills-enriched.json").read_text())["summary"]
        self.assertEqual(summary["uncurated_duplicate_names"], [],
                         "add a canonical entry to catalog/curation.json for each new duplicated name")
        self.assertEqual(sum(summary["tiers"].values()), summary["skills"])


class TestFinder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = finder.load_index()

    def test_expand_query_aliases_and_cjk(self):
        q = finder.expand_query("双重差分 DiD")
        self.assertIn("difference-in-differences", q)
        self.assertIn("did", q)
        self.assertIn("marginaleffects", finder.expand_query("marginal effects"))

    def test_duplicates_are_folded(self):
        names = [s["name"] for _, s in self.index.search("proofread", k=10)]
        self.assertEqual(names.count("proofread"), 1)

    def test_out_of_domain_surfaces_when_named(self):
        top = self.index.search("PubChem compound lookup", k=3)
        self.assertTrue(any("/domains/chemistry/" in s["path"] for _, s in top))

    def test_no_match_returns_empty(self):
        self.assertEqual(self.index.search("zzqxj", k=5), [])


class TestRoutingEval(unittest.TestCase):
    def test_cases_are_consistent_and_gate_passes(self):
        self.assertEqual(routing.main(["--min-hit3", "0.85"]), 0)

    def test_validate_cases_flags_dead_prefix(self):
        problems = routing.validate_cases(
            [{"id": "x", "query": "q", "accept": ["skills/nope/"]}], ["skills/a/SKILL.md"])
        self.assertTrue(any("matches no cataloged skill" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
