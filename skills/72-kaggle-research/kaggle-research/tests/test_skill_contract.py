from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_ROOT / "SKILL.md"
REFERENCE_NAMES = {
    "authentication.md",
    "datasets.md",
    "competitions.md",
    "kernels.md",
    "models.md",
    "testing-and-safety.md",
}


class SkillContractTests(unittest.TestCase):
    def test_skill_frontmatter_and_progressive_disclosure_contract(self):
        text = SKILL_FILE.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, r"(?m)^name: kaggle-research$")
        self.assertRegex(text, r"(?m)^description: .+Kaggle.+$")
        self.assertIn("scripts/kaggle_research.py doctor", text)
        self.assertIn("scripts/kaggle_research.py run --dry-run", text)
        self.assertIn("scripts/kaggle_research.py smoke-readonly", text)
        self.assertIn("AERS_KAGGLE_LIVE=1", text)
        self.assertIn("references/testing-and-safety.md", text)

    def test_all_required_reference_pages_exist_and_are_linked(self):
        text = SKILL_FILE.read_text(encoding="utf-8")
        reference_root = SKILL_ROOT / "references"
        observed = {path.name for path in reference_root.glob("*.md")}
        self.assertEqual(observed, REFERENCE_NAMES)
        for name in sorted(REFERENCE_NAMES):
            self.assertIn(f"references/{name}", text)

    def test_shipped_docs_do_not_encode_local_secrets_or_machine_paths(self):
        documents = [
            SKILL_FILE,
            *(SKILL_ROOT / "references").glob("*.md"),
        ]
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in documents
        )
        self.assertNotIn(r"D:\Download\Kaggle", combined)
        self.assertNotIn("print-access-token", combined)
        self.assertIsNone(
            re.search(
                r"(?i)KAGGLE_(?:API_TOKEN|KEY)\s*=\s*(?!<|\$|\[)",
                combined,
            )
        )


if __name__ == "__main__":
    unittest.main()
