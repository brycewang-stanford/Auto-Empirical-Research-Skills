"""Regression checks for SkillOpt-style gates in first-party empirical skills."""

from __future__ import annotations

import unittest

from _helpers import ROOT


CORE_SKILLS = [
    ROOT / "skills" / "00-Full-empirical-analysis-skill_StatsPAI" / "SKILL.md",
    ROOT / "skills" / "00.1-Full-empirical-analysis-skill_Python" / "SKILL.md",
    ROOT / "skills" / "00.2-Full-empirical-analysis-skill_Stata" / "SKILL.md",
    ROOT / "skills" / "00.3-Full-empirical-analysis-skill_R" / "SKILL.md",
]


class TestSkillOptStyleGates(unittest.TestCase):
    def test_core_empirical_skills_keep_validation_gate(self):
        required_terms = [
            "SkillOpt-style execution gate",
            "best_skill:",
            "train_signal:",
            "selection_split:",
            "heldout_gate:",
            "accepted_patterns:",
            "rejected_patterns:",
            "patch_scope:",
            "reject_if:",
            "Route card",
            "Bounded edit",
            "Selection split discipline",
            "Held-out gate",
            "Reject buffer",
            "Slow/meta update",
            "Promote only after validation",
        ]

        for skill_path in CORE_SKILLS:
            with self.subTest(skill=skill_path.relative_to(ROOT)):
                text = skill_path.read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
