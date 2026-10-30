"""Tests for skills/48-de-AIGC-skills/scripts/aigc_audit.py.

The audit script makes Step 1 (rule scan) and Step 5 (fidelity) of the de-AIGC
loop reproducible. The cases below pin its three promises: rules fire on the
skill's own AI drafts and stay silent on its own rewrites, quoted / cited text
is not "fixed", and any lost or invented number, citation or table reference
fails the compare gate. Stdlib only.
"""

from __future__ import annotations

import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import ROOT, load_module  # noqa: E402

audit = load_module("skills/48-de-AIGC-skills/scripts/aigc_audit.py", "aers_aigc_audit")
REFS = ROOT / "skills/48-de-AIGC-skills/references"


def fired(text: str, lang: str) -> set:
    return {h["rule"] for h in audit.run_rules(text, lang)}


def example_blocks(name: str):
    """(is_ai_draft, quoted text) for every ❌ / ✅ block of an examples file."""
    text = (REFS / name).read_text(encoding="utf-8")
    for block in re.split(r"^### ", text, flags=re.M)[1:]:
        head, body = block.split("\n", 1)
        body = body.split("\n## ")[0]
        quote = "\n".join(l[1:].strip() for l in body.splitlines() if l.startswith(">")).strip()
        if quote and ("❌" in head or "✅" in head):
            yield "❌" in head, quote


def run_cli(args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = audit.main(args)
    return rc, buf.getvalue()


class Rules(unittest.TestCase):
    def test_every_english_ai_draft_is_flagged_and_no_rewrite_is(self):
        for is_ai, quote in example_blocks("examples-en.md"):
            hits = fired(quote, "en")
            if is_ai:
                self.assertTrue(hits, f"no rule fired on AI draft: {quote[:60]}")
            else:
                self.assertEqual(hits, set(), f"rule fired on a rewrite: {quote[:60]}")

    def test_chinese_rewrites_stay_silent_and_most_drafts_fire(self):
        drafts = rewrites_clean = 0
        for is_ai, quote in example_blocks("examples-zh.md"):
            hits = fired(quote, "zh")
            if is_ai:
                drafts += bool(hits)
            else:
                self.assertEqual(hits, set(), f"rule fired on a rewrite: {quote[:40]}")
                rewrites_clean += 1
        self.assertGreaterEqual(drafts, 8)  # the rest need a reader (ZH05/06/10/14)
        self.assertEqual(rewrites_clean, 12)

    def test_quotations_citations_and_math_are_masked(self):
        self.assertEqual(fired('The ministry called it "a pivotal role in the evolving landscape".', "en"), set())
        self.assertEqual(fired("We estimate $\\beta$ \\cite{pivotal2020} as in Table 2.", "en"), set())
        self.assertEqual(fired("《意见》提出“毋庸置疑地赋能实体经济、打通堵点”。", "zh"), set())

    def test_preserve_list_is_not_flagged(self):
        self.assertEqual(fired("The coefficient is statistically significant at the 1% level (t = 3.81).", "en"), set())
        self.assertEqual(fired("Prior studies have shown that grants raise patenting (Howell 2017).", "en"), set())
        self.assertEqual(fired("系数在 1% 水平上显著为正，已有研究也发现了类似结果（张三等，2020）。", "zh"), set())

    def test_new_english_rules(self):
        self.assertIn("EN23", fired("Certainly! Here is the revised introduction.", "en"))
        self.assertIn("EN24", fired("See https://x.org/a?utm_source=chatgpt.com for details.", "en"))
        self.assertIn("EN25", fired("To the best of our knowledge, this is the first paper to do so.", "en"))
        self.assertIn("EN26", fired("Entry rose 12%. Taken together, these results highlight the role of credit.", "en"))
        self.assertIn("EN28", fired("Treated firms perform relatively better.", "en"))
        self.assertNotIn("EN28", fired("Treated firms perform relatively better (1.2 pp).", "en"))
        self.assertIn("EN29", fired("One might argue that the results reflect chance.", "en"))

    def test_new_chinese_rules(self):
        self.assertIn("ZH18", fired("问题不在于融资约束，而在于信息不对称。", "zh"))
        self.assertIn("ZH19", fired("本文的核心发现是：试点使 TFP 提高 6.8%。", "zh"))
        self.assertIn("ZH21", fired("作为影响创新的因素之一的融资约束值得关注。", "zh"))
        self.assertIn("ZH23", fired("这为推动高质量发展提供了有益借鉴。", "zh"))
        self.assertIn("ZH24", fired("这或许可能说明渠道存在。", "zh"))
        self.assertIn("ZH25", fired("边际贡献有三点：**视角创新**：首次引入。", "zh"))
        self.assertIn("ZH28", fired("随着数字经济的快速发展，相关问题受到了广泛关注。", "zh"))

    def test_demoted_connective_rule_needs_a_run(self):
        one = "此外，我们控制了年份固定效应。\n\n样本覆盖 2014–2022 年。"
        self.assertNotIn("ZH04", fired(one, "zh"))
        run = "此外，甲。\n\n因此，乙。\n\n进而，丙。"
        self.assertIn("ZH04", fired(run, "zh"))


class Metrics(unittest.TestCase):
    def test_metrics_are_report_only_and_count_dashes(self):
        m = audit.metrics("Entry rose — sharply. It fell later. Then it rose again in 2019.", "en")
        self.assertEqual(m["sentences"], 3)
        self.assertGreater(m["em_dashes_per_1000_words"], 0)
        z = audit.metrics("效应集中在民营企业——国企几乎不受影响。", "zh")
        self.assertGreater(z["dash_pairs_per_1000_zi"], 0)

    def test_echo_similarity_between_abstract_and_conclusion(self):
        doc = ("# Abstract\nDigital finance raises innovation among small firms.\n\n"
               "# Data\nWe use patents.\n\n"
               "# Conclusion\nDigital finance raises innovation among small firms.\n")
        echo = audit.metrics(doc, "en")["echo"]
        self.assertEqual(echo["pair"], "abstract↔conclusion")
        self.assertTrue(echo["flag"])


class Compare(unittest.TestCase):
    A = "The reform raised entry by 12% (Table 3, column 2; Chen and Li, 2021). The effect is not driven by demand."

    def test_faithful_rewrite_passes(self):
        b = "Entry rose 12% after the reform (Table 3, column 2; Chen and Li, 2021). Demand does not drive it."
        self.assertEqual(audit.compare(self.A, b, "en", "results", "agent")["hard_failures"], [])

    def test_lost_or_invented_facts_fail(self):
        for bad in (self.A.replace("12%", "13%"), self.A.replace("Table 3", "Table 4"),
                    self.A.replace("Chen and Li, 2021", "Chen and Li, 2022"),
                    self.A + " Effects reach 40% in coastal cities."):
            self.assertTrue(audit.compare(self.A, bad, "en", None, "agent")["hard_failures"], bad)

    def test_drift_warnings(self):
        w = audit.compare(self.A, self.A.replace("raised", "proves the reform raised"), "en", None, "agent")["warnings"]
        self.assertTrue(any("strong evidence verbs" in x for x in w))
        w = audit.compare(self.A, self.A.replace("is not driven", "is driven"), "en", None, "agent")["warnings"]
        self.assertTrue(any("negation" in x for x in w))
        w = audit.compare(self.A, self.A.replace("raised", "reduced"), "en", None, "agent")["warnings"]
        self.assertTrue(any("direction" in x for x in w))

    def test_section_cap_applies_to_agent_not_author(self):
        b = "Demand cannot explain it: entry climbed by 12% once the reform passed (Table 3, column 2; Chen and Li, 2021)."
        agent = audit.compare(self.A, b, "en", "data", "agent")["warnings"]
        author = audit.compare(self.A, b, "en", "data", "author")["warnings"]
        self.assertTrue(any("cap" in x for x in agent))
        self.assertFalse(any("cap" in x for x in author))

    def test_draft_retention_bounds(self):
        same = audit.compare(self.A, self.A, "en", None, "author")["draft_retention"]
        self.assertEqual(same["R4"], 1.0)
        fresh = audit.compare(self.A, "Demand cannot explain it; entry climbed by 12% (Table 3, column 2; "
                              "Chen and Li, 2021) once the reform passed.", "en", None, "author")["draft_retention"]
        self.assertLess(fresh["R4"], 0.5)

    def test_typography_is_not_drift(self):
        rep = audit.compare("−0.043 for 1,200 firms", "-0.043 for 1200 firms", "en", None, "agent")
        self.assertEqual(rep["hard_failures"], [])

    def test_chinese_citation_and_number_fidelity(self):
        z0 = "数字金融使专利申请增加 8.3%（表 4 第（2）列），这与张三等（2020）的结论一致。"
        z1 = "表 4 第（2）列显示，数字金融让专利申请增加 8.3%；张三等（2020）也有相近发现。"
        self.assertEqual(audit.compare(z0, z1, "zh", None, "agent")["hard_failures"], [])
        self.assertTrue(audit.compare(z0, z0.replace("张三等（2020）", "李四等（2020）"), "zh", None, "agent")["hard_failures"])


class CommandLine(unittest.TestCase):
    def test_audit_and_compare_exit_codes_and_docx_input(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a.md"
            b = Path(td) / "b.md"
            a.write_text("Studies have shown that the reform raised entry by 12%.\n", encoding="utf-8")
            b.write_text("Entry rose 13% after the reform.\n", encoding="utf-8")
            rc, out = run_cli(["audit", str(a)])
            self.assertEqual(rc, 0)
            self.assertIn("EN04", out)
            self.assertIn("not a detector score", out)
            rc, out = run_cli(["compare", str(a), str(b)])
            self.assertEqual(rc, 1)
            self.assertIn("B: unknown", out)
            rc, out = run_cli(["compare", "--json", str(a), str(a)])
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(out)["hard_failures"], [])
            d = Path(td) / "p.docx"
            with zipfile.ZipFile(d, "w") as z:
                z.writestr("word/document.xml", '<w:document><w:body><w:p><w:r><w:t>Certainly! Here is the '
                           'revised draft.</w:t></w:r></w:p></w:body></w:document>')
            rc, out = run_cli(["audit", "--json", str(d)])
            self.assertIn("EN23", {h["rule"] for h in json.loads(out)["hits"]})

    def test_self_test_passes(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit.self_test()
        self.assertEqual(rc, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main()
