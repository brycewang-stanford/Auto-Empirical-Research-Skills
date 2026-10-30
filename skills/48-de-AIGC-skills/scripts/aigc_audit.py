#!/usr/bin/env python3
"""aigc_audit.py — deterministic audit and fidelity gate for the de-AIGC loop.

Part of the `de-aigc-skills` skill (AERS collection 48). Standard library only,
Python 3.9+. Two jobs the six-step loop used to leave to the model's own
judgement, now made reproducible:

  audit    Step 1. Scan an EN or ZH manuscript for the pattern-library rules
           that a regex can see (EN/ZH ids from references/patterns-*.md),
           plus report-only distribution metrics (sentence-length spread,
           long-sentence share, dash rate). Quotations, code, math, \\cite
           and tables are masked first. Rules that need a reader — rhythm
           *quality*, total-score structure, elegant variation — stay with
           the model; the report says which ones those are.

  compare  Step 5 (and the Step 3 ownership pass). Diff an original against
           its rewrite: every number, citation, table/figure reference and
           significance statement must survive; negation, direction words,
           hedges and evidence-verb strength are checked for drift; change
           rate is compared with a per-section cap. When the original is a
           model draft and the rewrite is the author's, the draft-retention
           block (n-gram containment, verbatim coverage) says how much of the
           model's wording is still there — the only honest number available
           for a statistical watermark, which itself stays "B: unknown".

This is not an AI detector and prints no "AI probability". Upstream projects
that measured their own composite scores found them close to a coin flip at
paragraph level; a rule hit here is a place to look, not a verdict.

Usage
    python3 aigc_audit.py audit   FILE [--lang auto|en|zh] [--json]
    python3 aigc_audit.py compare ORIGINAL REWRITE [--lang auto|en|zh]
                                  [--section abstract|intro|literature|data|model|
                                             results|robustness|discussion|conclusion]
                                  [--by agent|author] [--json]
    python3 aigc_audit.py self-test

FILE may be .txt .md .tex .docx (text runs are extracted) or '-' for stdin.
`audit` exits 0; `compare` exits 1 when a hard fidelity check fails (a number,
citation or table reference lost or invented), else 0.
"""

from __future__ import annotations

import argparse
import difflib
import io
import json
import math
import re
import statistics
import sys
import zipfile
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

__version__ = "1.0.0"

CJK = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
_CJK_CHAR = re.compile(f"[{CJK}]")

# --------------------------------------------------------------------------- #
# Reading and masking
# --------------------------------------------------------------------------- #

_W_P = re.compile(r"<w:p[ >].*?</w:p>", re.S)
_W_T = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    p = Path(path)
    data = p.read_bytes()
    if p.suffix.lower() == ".docx":
        xml = zipfile.ZipFile(io.BytesIO(data)).read("word/document.xml").decode("utf-8")
        paras = ["".join(_W_T.findall(m.group(0))) for m in _W_P.finditer(xml)]
        text = "\n\n".join(x for x in paras if x.strip())
        return (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&apos;", "'"))
    return data.decode("utf-8-sig")


def detect_lang(text: str) -> str:
    cjk = len(_CJK_CHAR.findall(text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return "zh" if cjk and cjk / max(1, cjk + latin) >= 0.30 else "en"


# Spans that are somebody else's words or not prose at all. They are blanked
# (same length, so offsets survive) before any rule runs.
_MASKS = [
    re.compile(r"^```.*?^```[ \t]*$", re.S | re.M),                       # fenced code
    re.compile(r"`[^`\n]+`"),                                              # inline code
    re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$|\\\(.*?\\\)|\\\[.*?\\\]", re.S),  # math
    re.compile(r"\\begin\{(equation|align|gather|multline|table|tabular|figure)\*?\}.*?\\end\{\1\*?\}", re.S),
    re.compile(r"\\(?:cite[tp]?|citeauthor|ref|eqref|label|autoref)\{[^}]*\}"),
    re.compile(r"^\s*\|.*\|\s*$", re.M),                                  # markdown table rows
    re.compile(r"^>.*$", re.M),                                            # block quotes
    re.compile(r"“[^”\n]{1,300}”|\"[^\"\n]{1,300}\"|「[^」\n]{1,300}」|『[^』\n]{1,300}』"),  # quotations
    re.compile(r"^\s*%.*$", re.M),                                         # LaTeX comments
]


def mask(text: str) -> str:
    chars = list(text)
    for rx in _MASKS:
        for m in rx.finditer(text):
            for k in range(m.start(), m.end()):
                if chars[k] != "\n":
                    chars[k] = " "
    return "".join(chars)


def paragraphs(text: str) -> List[Tuple[int, str]]:
    """(start offset, paragraph) pairs; blank-line separated."""
    out = []
    for m in re.finditer(r"(?:[^\n]+\n?)+", text):
        block = m.group(0)
        if block.strip():
            out.append((m.start(), block))
    return out


_EN_ABBR = re.compile(r"\b(?:e\.g|i\.e|et al|cf|vs|Fig|Figs|Eq|Eqs|No|Vol|pp|Dr|Mr|Ms|Prof|approx|resp|ca)\.$")


def sentences(par: str, lang: str) -> List[str]:
    if lang == "zh":
        parts = re.split(r"(?<=[。！？!?])", par)
        return [s.strip() for s in parts if len(re.sub(r"\s", "", s)) >= 2]
    raw = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(\[])", par.strip())
    out: List[str] = []
    for s in raw:
        if out and _EN_ABBR.search(out[-1]):
            out[-1] = out[-1] + " " + s
        else:
            out.append(s)
    return [s.strip() for s in out if s.strip()]


def slen(s: str, lang: str) -> int:
    if lang == "zh":
        return len(_CJK_CHAR.findall(s)) + len(re.findall(r"[A-Za-z]+|\d+(?:\.\d+)?", s))
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.\-]*", s))


# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #

class Rule:
    """One regex-visible rule. scope: 'text' (match anywhere), 'sentence'
    (the predicate sees one sentence), 'paragraph', or 'para_end'."""

    def __init__(self, rid: str, sev: str, name: str, pattern: str = "", *, scope: str = "text",
                 flags: int = re.I, min_hits: int = 1, unless: str = "", note: str = ""):
        self.rid, self.sev, self.name, self.scope = rid, sev, name, scope
        self.rx = re.compile(pattern, flags) if pattern else None
        self.min_hits = min_hits
        self.unless = re.compile(unless, flags) if unless else None
        self.note = note


_HAS_CITE_EN = r"\(\s*(?:[A-Z][^()]{0,80})?(?:1[89]|20)\d{2}[a-z]?\s*[;,)]|\b(?:1[89]|20)\d{2}[a-z]?\)|\\cite|\[\d+(?:[,–-]\s*\d+)*\]"
_HAS_STAT = r"\d|\bp\s*[<=>]|\bt\s*=|s\.e\.|standard error|\*"
_HAS_CITE_ZH = r"(?:1[89]|20)\d{2}|\\cite|\[\d+\]|等\s*[（(]"

EN_RULES: List[Rule] = [
    Rule("EN01", "🔴", "inflated significance",
         r"\bplays? an? (?:pivotal|crucial|vital|key|critical|central) role\b|\bunderscor(?:es|ing|e) the (?:importance|need|critical|significance)"
         r"|\bpaves? the way\b|\bparadigm shift\b|\b(?:evolving|ever-changing|shifting|rapidly changing) landscape\b"
         r"|\btestament to\b|\bfar-reaching (?:implications|consequences)\b|\bin today'?s (?:rapidly )?(?:changing|evolving|globali[sz]ed)\b"),
    Rule("EN02", "🔴", "-ing tail",
         r",\s+(?:highlighting|underscoring|emphasi[sz]ing|showcasing|reflecting|signall?ing|illustrating|demonstrating|contributing to|paving)\b[^.;]{0,140}[.;]\s*$",
         scope="sentence"),
    Rule("EN03", "🟡", "promotional adjective",
         r"\b(?:groundbreaking|remarkabl[ey]|striking(?:ly)?|dramatic(?:ally)?|impressive(?:ly)?|cutting-edge|state-of-the-art|unprecedented)\b"),
    Rule("EN04", "🔴", "vague attribution (no citation in the sentence)",
         r"\b(?:(?:many|some|several|prior|previous|recent|existing) )?(?:studies|research|scholars|researchers|experts|the literature)"
         r" (?:have |has )?(?:shown|suggested|argued|noted|found|indicated|demonstrated|documented)\b|\bit is (?:widely|generally) (?:believed|accepted|recogni[sz]ed)\b",
         scope="sentence", unless=_HAS_CITE_EN),
    Rule("EN05", "🔴", "formulaic opener",
         r"^\s*(?:In recent (?:years|decades)|With the rapid development of|In today'?s|Despite (?:recent|significant) advances|Over the past (?:few )?(?:years|decades))\b"
         r"|\bhas (?:attracted|received|garnered) (?:increasing|growing|considerable|significant) attention\b",
         scope="sentence"),
    Rule("EN06", "🔴", "connective chain (≥2 sentence-initial additives in one paragraph)",
         r"(?:^|(?<=[.!?])\s+)(?:Moreover|Furthermore|Additionally|In addition|Also),", scope="paragraph", min_hits=2),
    Rule("EN08", "🟡", "negative parallelism / staged contrast",
         r"\bnot only\b[^.]{1,120}\bbut also\b|\bis not (?:just|merely|simply)\b|\bdoes not merely\b|\bthe question is not\b"
         r"|\bThis does not mean\b[^.]{0,120}\.\s+(?:It|This) means\b|\bisn't just\b"),
    Rule("EN10", "🔴", "overclaiming verb — check against the design (Step 2)",
         r"\b(?:prove[sd]?|proves|demonstrates?|establish(?:es|ed)?|confirms?|guarantees?|clearly shows?|undoubtedly|unequivocally)\b"),
    Rule("EN11", "🔴", "'significant' with no statistic in the sentence",
         r"\bsignificant(?:ly)?\b", scope="sentence", unless=_HAS_STAT),
    Rule("EN12", "🟡", "empty intensifier cluster (≥2 in a paragraph)",
         r"\b(?:comprehensive(?:ly)?|extensive(?:ly)?|thorough(?:ly)?|various|numerous|a wide range of|multifaceted|holistic|meticulous(?:ly)?|rigorous(?:ly)? (?:verified|cleaned|checked))\b",
         scope="paragraph", min_hits=2),
    Rule("EN14", "🟡", "AI-vocabulary cluster (≥2 in a paragraph)",
         r"\b(?:delve[sd]?|delving|intricate|interplay|tapestry|realm|pivotal|crucial|foster(?:s|ing|ed)?|showcas(?:e|es|ing|ed)"
         r"|underscor(?:e|es|ed|ing)|garner(?:s|ed)?|seamless(?:ly)?|nuanced|navigat(?:e|es|ing) the|landscape)\b",
         scope="paragraph", min_hits=2),
    Rule("EN16", "🔴", "generic contribution / implication",
         r"\bfills? (?:an? |the )?(?:important |critical |significant )?gap\b|\bvaluable insights?\b|\bimportant implications for (?:policymakers|practitioners|managers)\b"
         r"|\bcontributes? to (?:the|several|three|two) (?:literature|strands)[^.]{0,40}\bin (?:two|three|several|four) ways\b"),
    Rule("EN17", "🟡", "citation dump (≥5 references in one bracket)",
         r"\((?:[^()]*?(?:1[89]|20)\d{2}[a-z]?\s*;){4,}[^()]*?(?:1[89]|20)\d{2}[a-z]?\)", flags=0),
    Rule("EN23", "🔴", "chatbot residue",
         r"^\s*(?:Certainly|Of course|Sure|Absolutely)[!,.]|\bHere(?:'s| is) (?:a|an|the) (?:revised|rewritten|updated|polished|improved)\b|\bI hope this helps\b"
         r"|\bLet me know if\b|\bGreat question\b|\bYou'?re absolutely right\b|\bas of my (?:last|knowledge) (?:update|cutoff)\b|\bAs an AI\b"
         r"|\bLet'?s (?:dive|delve|explore|unpack)\b|\bHere'?s what you need to know\b", flags=re.I | re.M),
    Rule("EN24", "🔴", "generation artifact (markup / citation leak / placeholder)",
         r"utm_source=(?:chatgpt\.com|openai)|【\d+†[^】]*】|\[oaicite:\d+\]|contentReference\[oaicite|\bturn\d+(?:search|view|news|file)\d+"
         r"|\[(?:Author|Citation|Insert|TODO|TBD|XX|Year|Ref)[^\]]{0,40}\]|\b(?:19|20)XX\b|\bXX(?:\.X+)?\s?%|^\s*[-*]\s+\*\*[^*\n]{1,60}:\*\*",
         flags=re.I | re.M),
    Rule("EN25", "🟡", "novelty padding",
         r"\bto the best of (?:our|my) knowledge\b|\b(?:the )?first (?:paper|study|article|work) to\b|\bfor the first time\b|\bnovel\b"),
    Rule("EN26", "🟡", "takeaway closer",
         r"^\s*(?:(?:This|These|Such) (?:finding|result|evidence|pattern)s? (?:underscores?|highlights?|demonstrates?|reveals?|speaks? to)"
         r"|Taken together,? these|Overall,? (?:these|our) (?:findings|results)|Collectively,? these)\b", scope="para_end"),
    Rule("EN27", "🟡", "boilerplate emphasis / filler",
         r"\bit is (?:worth|important to) not(?:e|ing) that\b|\bit should be (?:noted|emphasi[sz]ed|stressed) that\b|\bin order to\b|\bat its core\b|\bwhen it comes to\b"),
    Rule("EN28", "🟡", "vague magnitude with no number in the sentence",
         r"\b(?:somewhat|relatively|fairly|to some extent|to a certain extent|quite)\b", scope="sentence", unless=r"\d"),
    Rule("EN29", "🟡", "arguing with no one",
         r"\b(?:one might argue|some (?:may|might) argue|while some may argue|this is not to say|to be clear)\b"),
]

ZH_RULES: List[Rule] = [
    Rule("ZH01", "🔴", "四字套话（任意 200 字内 ≥3 个）",
         r"众所周知|不可否认|毋庸置疑|显而易见|综上所述|由此可见|与此同时|除此之外|不仅如此|总而言之|归根结底|不言而喻|可想而知|自不待言",
         scope="window200", min_hits=3, flags=0),
    Rule("ZH01", "🟡", "高危套话（单次即标）", r"毋庸置疑|众所周知|不可否认|显而易见|不言而喻|综上所述", flags=0),
    Rule("ZH28", "🔴", "套路化开篇 / 广泛关注",
         r"^\s*(?:近年来|近些年来|随着[^，。；\n]{2,20}的(?:快速|迅速|不断|深入|蓬勃)?发展|在[^，。；\n]{2,15}(?:背景|时代|浪潮)下)"
         r"|(?:引起|受到|引发)了?(?:学术界|学者们?|社会各界|政策制定者)?的?(?:广泛|越来越多的|日益(?:广泛的)?|高度)关注",
         scope="sentence", flags=0),
    Rule("ZH03", "🟡", "AI 偏好形容词（同段 ≥2）",
         r"深远|深刻的|全方位|立体化|颠覆性|革命性|前瞻性|多维度?的|多层次的?|全面的", scope="paragraph", min_hits=2, flags=0,
         note="「显著的」不计入：「在 1% 水平上显著」是规范表述"),
    Rule("ZH04", "🟢", "连续段首连接词（相邻 3 段）",
         r"^\s*(?:此外|而且|并且|因此|所以|从而|于是|进而|同时)[，,]?", scope="para_run", min_hits=3, flags=0),
    Rule("ZH07", "🟡", "模糊主语（同句无文献）",
         r"(?:相关|已有|现有|大量|诸多|许多)?(?:研究|文献|学者)(?:普遍|均|已经)?(?:表明|指出|发现|认为|证实)", scope="sentence", unless=_HAS_CITE_ZH, flags=0),
    Rule("ZH11", "🟢", "序数链（同段 首先…其次…最后）",
         r"首先[^。]*?[。；].*?其次.*?(?:再次|最后)", scope="paragraph", flags=re.S),
    Rule("ZH12", "🔴", "绝对化断言 —— 对照识别设计核查（Step 2）",
         r"证明了|充分(?:说明|证明|表明)|完全证实|毫无疑问|必然(?:导致|会)|毋庸置疑|一定会导致", flags=0),
    Rule("ZH15", "🟢", "程度副词堆叠（同段 ≥2）", r"非常|极其|极大地|巨大地|尤为|格外|十分", scope="paragraph", min_hits=2, flags=0),
    Rule("ZH18", "🔴", "否定对举 / 假揭示",
         r"(?:不是|并非|不在于|与其说|看似|表面上)[^。！？\n]{1,24}?[，,]?\s*(?:而是|而在于|不如说|实则|实际上)", flags=0),
    Rule("ZH19", "🟡", "结论提示冒号",
         r"(?:核心|关键|本质|根本原因|答案|重点|真相)[^，。：:\n]{0,4}?(?:在于|就是|是)[：:]", flags=0),
    Rule("ZH21", "🟡", "翻译腔 / 欧化句式",
         r"当[^，。；\n]{1,20}时[，,]|对于[^，。；\n]{1,20}(?:来说|而言)|就[^，。；\n]{1,15}而言|作为[^，。；\n]{2,20}之一的"
         r"|(?:进行|作出|做出)了?[^，。；\n]{0,8}的(?:分析|研究|探讨|考察|讨论)|被[^，。；\n]{1,15}所(?:[^，。；\n]{1,6})", flags=0),
    Rule("ZH23", "🟡", "升华套话（结论节外每处都标；结论节内至多留一次）",
         r"(?:为|对)[^。]{0,24}提供了[^。]{0,8}?(?:借鉴|参考|启示|支撑|思路|指导|依据)|具有(?:重要|一定|较强)的?(?:理论|现实|实践|政策)(?:意义|价值)"
         r"|填补了[^。]{0,20}(?:空白|不足)|彰显了|标志着", flags=0),
    Rule("ZH24", "🟡", "限定词堆叠（同一分句 ≥2）",
         r"可能|或许|也许|在一定程度上|某种程度上|似乎|较为", scope="clause", min_hits=2, flags=0),
    Rule("ZH25", "🟡", "加粗标签 / 列表化行文",
         r"\*\*[^*\n]{1,30}\*\*[：:]|^\s*[-*•]\s+\S", flags=re.M),
    Rule("ZH27", "🟢", "黑话 / 元话语（同段 ≥2）",
         r"赋能|抓手|闭环|底层逻辑|打通|赛道|值得注意的是|需要指出的是|不难发现|值得一提的是", scope="paragraph", min_hits=2, flags=0,
         note="政策原文引语已被屏蔽，不计入"),
]

MODEL_JUDGED = {
    "en": "EN07 rule-of-three · EN09 elegant variation · EN13 copula avoidance · EN15 hedge calibration · "
          "EN18 false ranges · EN19 rhythm quality · EN20 em dashes (counted below) · EN21 word choice · "
          "EN22 echo (similarity below) · EN30 repeated openers",
    "zh": "ZH02 虚词堆叠 · ZH05 并列过度 · ZH06 节奏（指标见下）· ZH08 被动 · ZH09 嵌套 · ZH10 总分总 · ZH13 观点-证据 · "
          "ZH14 缺 hedge · ZH16 三段对称 · ZH17 回音壁（相似度见下）· ZH20 破折号（计数见下）· ZH22 同义轮换 · ZH26 相邻句同构",
}


def _excerpt(text: str, a: int, b: int, width: int = 70) -> str:
    s = max(0, a - 12)
    e = min(len(text), max(b, a + 1) + 12)
    frag = re.sub(r"\s+", " ", text[s:e]).strip()
    return frag if len(frag) <= width else frag[: width - 1] + "…"


def run_rules(raw: str, lang: str) -> List[dict]:
    text = mask(raw)
    rules = ZH_RULES if lang == "zh" else EN_RULES
    hits: List[dict] = []
    pars = paragraphs(text)
    for rule in rules:
        if rule.scope == "text":
            for m in rule.rx.finditer(text):
                hits.append(_hit(rule, raw, pars, m.start(), m.end()))
        elif rule.scope in ("sentence", "para_end", "clause"):
            for p0, par in pars:
                sents = sentences(par, lang)
                if rule.scope == "para_end":
                    sents = sents[-1:]
                elif rule.scope == "clause":
                    sents = [c for s in sents for c in re.split(r"[，,；;：:]", s)]
                for s in sents:
                    off = par.find(s)
                    found = list(rule.rx.finditer(s))
                    if len(found) < rule.min_hits:
                        continue
                    if rule.unless is not None and rule.unless.search(s):
                        continue
                    a = p0 + max(off, 0) + found[0].start()
                    hits.append(_hit(rule, raw, pars, a, a + len(found[0].group(0))))
        elif rule.scope == "paragraph":
            for p0, par in pars:
                found = list(rule.rx.finditer(par))
                if len(found) >= rule.min_hits:
                    a = p0 + found[0].start()
                    h = _hit(rule, raw, pars, a, p0 + found[-1].end())
                    h["count"] = len(found)
                    hits.append(h)
        elif rule.scope == "window200":
            pos = [m.start() for m in rule.rx.finditer(text)]
            k = 0
            while k < len(pos):
                j = k
                while j + 1 < len(pos) and pos[j + 1] - pos[k] <= 200:
                    j += 1
                if j - k + 1 >= rule.min_hits:
                    h = _hit(rule, raw, pars, pos[k], pos[k] + 4)
                    h["count"] = j - k + 1
                    hits.append(h)
                    k = j + 1
                else:
                    k += 1
        elif rule.scope == "para_run":
            run: List[int] = []
            for p0, par in pars:
                if rule.rx.search(par):
                    run.append(p0)
                    if len(run) == rule.min_hits:
                        hits.append(_hit(rule, raw, pars, run[0], run[0] + 6))
                else:
                    run = []
    hits.sort(key=lambda h: (h["para"], h["rule"]))
    return hits


def _hit(rule: Rule, raw: str, pars: Sequence[Tuple[int, str]], a: int, b: int) -> dict:
    para = 1
    for k, (p0, _) in enumerate(pars, 1):
        if p0 <= a:
            para = k
    h = {"para": para, "rule": rule.rid, "severity": rule.sev, "name": rule.name, "excerpt": _excerpt(raw, a, b)}
    if rule.note:
        h["note"] = rule.note
    return h


# --------------------------------------------------------------------------- #
# Report-only metrics
# --------------------------------------------------------------------------- #

def _cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))


_STOP_EN = set("""a an the of in on at to for from by with and or but as is are was were be been being this that these those
it its we our they their he she his her which who whom whose than then there here into over under about between
across after before during while not no can could may might will would should must do does did has have had""".split())


def _content_bag(text: str, lang: str) -> Counter:
    if lang == "zh":
        chars = _CJK_CHAR.findall(text)
        return Counter(a + b for a, b in zip(chars, chars[1:]))
    return Counter(w for w in re.findall(r"[a-z]+", text.lower()) if w not in _STOP_EN and len(w) > 2)


_HEAD_PREFIX = r"^(?:#{1,6}\s*|\\(?:sub)*section\*?\{|\\begin\{abstract\}|[一二三四五六七八九十]+、|\d+(?:\.\d+)*\.?\s+)?\s*"
# Any heading line ends a span; only a short line counts, so a sentence that
# merely starts with "Introduction of the reform …" is not a heading.
_ANY_HEAD = re.compile(r"^(?:#{1,6}\s+\S|\\(?:sub)*section\*?\{|\\(?:begin|end)\{abstract\}|[一二三四五六七八九十]+、\S"
                       r"|\d+(?:\.\d+)*\.?\s+\S)[^\n。.]{0,60}$", re.M)
_SECTION_HEAD = re.compile(
    _HEAD_PREFIX + r"(abstract|introduction|conclusions?|concluding remarks|摘\s*要|引\s*言|结\s*论|研究结论)"
    r"(?![A-Za-z])[^\n。.]{0,40}$", re.I | re.M)


def echo_similarity(raw: str, lang: str) -> Optional[dict]:
    """EN22 / ZH17: content-word cosine between the abstract (or introduction)
    and the conclusion, when headings make them findable."""
    named = {m.start(): m.group(1).lower() for m in _SECTION_HEAD.finditer(raw)}
    if len(named) < 2:
        return None
    bounds = sorted(set(named) | {m.start() for m in _ANY_HEAD.finditer(raw)} | {len(raw)})
    spans: Dict[str, str] = {}
    for start, name in sorted(named.items()):
        end = next(b for b in bounds if b > start)
        key = ("abstract" if name.startswith(("abstract", "摘")) else
               "intro" if name.startswith(("intro", "引")) else "conclusion")
        body_start = raw.find("\n", start)
        spans.setdefault(key, raw[body_start if 0 <= body_start < end else start:end])
    if "conclusion" not in spans:
        return None
    other = "abstract" if "abstract" in spans else "intro" if "intro" in spans else None
    if other is None:
        return None
    sim = _cosine(_content_bag(spans[other], lang), _content_bag(spans["conclusion"], lang))
    return {"pair": f"{other}↔conclusion", "cosine": round(sim, 3), "flag": sim > 0.75}


def metrics(raw: str, lang: str) -> dict:
    text = mask(raw)
    sents = [s for _, p in paragraphs(text) for s in sentences(p, lang)]
    lens = [slen(s, lang) for s in sents if slen(s, lang) > 0]
    units = sum(lens) or 1
    m: "OrderedDict[str, object]" = OrderedDict()
    m["sentences"] = len(lens)
    m["length_unit"] = "字" if lang == "zh" else "words"
    if len(lens) >= 2:
        mean = statistics.mean(lens)
        m["mean_sentence_length"] = round(mean, 1)
        m["sentence_length_cv"] = round(statistics.pstdev(lens) / mean, 2) if mean else 0.0
    short_cut, long_cut = (15, 60) if lang == "zh" else (8, 40)
    m["short_share"] = round(sum(1 for x in lens if x <= short_cut) / max(1, len(lens)), 3)
    m["long_share"] = round(sum(1 for x in lens if x >= long_cut) / max(1, len(lens)), 3)
    runs, cur = 0, 1
    for a, b in zip(lens, lens[1:]):
        if a and abs(a - b) / max(a, b) <= 0.15:
            cur += 1
            if cur == 4:
                runs += 1
        else:
            cur = 1
    m["similar_length_runs_4plus"] = runs
    per_k = 1000.0 / units
    if lang == "zh":
        m["dash_pairs_per_1000_zi"] = round(raw.count("——") * per_k, 2)
        hedges = len(re.findall(r"可能|或许|也许|在一定程度上|似乎|倾向于|在本文样本中|与[^。]{1,20}一致", text))
    else:
        m["em_dashes_per_1000_words"] = round(raw.count("—") * per_k, 2)
        hedges = len(re.findall(r"\b(?:suggests?|is consistent with|are consistent with|associated with|may|might|in our sample|we cannot rule out)\b", text, re.I))
    m["hedges_per_1000"] = round(hedges * per_k, 2)
    echo = echo_similarity(raw, lang)
    if echo:
        m["echo"] = echo
    return m


METRIC_NOTE = ("report only — no study supports a fixed cut-off for sentence-length spread "
               "(sepia research/rhythm-syntax.md; lieflat RESEARCH.md), and prompting a model to "
               "'vary sentence length' made text easier to detect. Read them against the author's own "
               "earlier writing, not as targets.")


# --------------------------------------------------------------------------- #
# compare: fidelity + change rate + draft retention
# --------------------------------------------------------------------------- #

_NUM = re.compile(r"(?<![A-Za-z\d.])[-−+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?(?:%|‰|万|亿)?|(?<![A-Za-z\d.])[-−+]?\d+(?:\.\d+)?(?:%|‰|万|亿)?")
_CITE_EN = re.compile(r"\b([A-Z][A-Za-z'’\-]+)(?:\s+et al\.?|\s+(?:and|&)\s+[A-Z][A-Za-z'’\-]+)?,?\s*\(?((?:1[89]|20)\d{2}[a-z]?)\b")
_CITE_ZH = re.compile(f"([{CJK}]{{2,4}})(?:等|和[{CJK}]{{2,4}})?\\s*[（(]?\\s*((?:19|20)\\d{{2}}[a-z]?)")
_CITE_KEYS = re.compile(r"\\cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")
_REFS = re.compile(r"\b(?:Table|Figure|Fig\.|Column|Panel|Appendix|Equation|Eq\.)\s*\(?[A-Z]?\d+[A-Za-z]?\)?|[表图]\s*[A-Z]?\d+|第\s*[（(]?\d+[）)]?\s*列|式\s*[（(]\d+[）)]")
_SIG = re.compile(r"(?:在\s*)?\d+(?:\.\d+)?\s*%\s*(?:的)?(?:统计)?(?:水平|置信水平)上?(?:显著|通过)|significant at the \d+(?:\.\d+)?\s*(?:%|percent) level", re.I)
_NEG_EN = re.compile(r"\b(?:not|no|never|neither|nor|cannot|without|none|nothing)\b|n't\b", re.I)
_NEG_EN_PSEUDO = re.compile(r"\bnot only\b|\bno longer\b|\bnot just\b|\bnothing but\b", re.I)
_NEG_ZH = re.compile(r"不|没有?|未|无|非|并非|否")
_NEG_ZH_PSEUDO = re.compile(r"不仅|不但|不断|无论|非常|不过|不少|无疑|除非|是否|与否|不同|并不意味|未来")
_DIR = {
    "up": re.compile(r"\b(?:increas\w*|rais\w*|ris(?:e|es|ing)|rose|higher|boost\w*|improv\w*|positive(?:ly)?|promot\w*)\b|提高|提升|增加|上升|促进|正向|改善", re.I),
    "down": re.compile(r"\b(?:decreas\w*|reduc\w*|lower\w*|declin\w*|fell|fall\w*|negative(?:ly)?|inhibit\w*|suppress\w*|curb\w*)\b|降低|下降|减少|抑制|负向|削弱", re.I),
}
_VERB_STRENGTH = [  # (level, pattern) — Step 2's evidence-verb scale
    (3, re.compile(r"\b(?:prove[sd]?|proves|demonstrat\w*|establish\w*|confirm\w*|clearly shows?)\b|证明|证实|充分说明|充分表明|必然", re.I)),
    (2, re.compile(r"\b(?:show[sn]?|find[s]?|found|indicat\w*|reveal\w*)\b|表明|发现|显示|揭示", re.I)),
    (1, re.compile(r"\b(?:suggest\w*|consistent with|associated with|may|might|could)\b|可能|或许|与[^。]{1,20}一致|相关", re.I)),
]
_HEDGE = re.compile(r"\b(?:suggest\w*|consistent with|associated with|may|might|in our sample|we cannot rule out)\b|可能|或许|也许|在一定程度上|在本文样本中|与[^。]{1,20}一致", re.I)

SECTION_CAPS = {"data": 0.15, "model": 0.15, "robustness": 0.15, "results": 0.25,
                "abstract": 0.40, "intro": 0.40, "literature": 0.40, "discussion": 0.40, "conclusion": 0.40}


def _norm_num(s: str) -> str:
    s = s.replace("−", "-").replace(",", "")
    return s[1:] if s.startswith("+") else s


def numbers(text: str) -> Counter:
    return Counter(_norm_num(m.group(0)) for m in _NUM.finditer(text))


def citations(text: str) -> Counter:
    c: Counter = Counter()
    for m in _CITE_EN.finditer(text):
        if m.group(1) not in ("Table", "Figure", "Column", "Panel", "Appendix", "In", "Since", "From", "By", "The", "After", "Before", "During"):
            c[f"{m.group(1)} {m.group(2)}"] += 1
    for m in _CITE_ZH.finditer(text):
        # the CJK run may swallow a preceding word ("这与张三"); the last two
        # characters before 等 / 和 / the year are the stable part of the name
        c[f"{m.group(1).rstrip('等')[-2:]} {m.group(2)}"] += 1
    for m in _CITE_KEYS.finditer(text):
        for k in m.group(1).split(","):
            if k.strip():
                c[f"\\cite{{{k.strip()}}}"] += 1
    return c


def refs(text: str) -> Counter:
    return Counter(re.sub(r"\s+", "", m.group(0)) for m in _REFS.finditer(text))


def _count(rx: "re.Pattern[str]", text: str, pseudo: Optional["re.Pattern[str]"] = None) -> int:
    if pseudo is not None:
        text = pseudo.sub(" ", text)
    return len(rx.findall(text))


def tokens(text: str, lang: str) -> List[str]:
    if lang == "zh":
        return re.findall(f"[{CJK}]|[A-Za-z]+|\\d+(?:\\.\\d+)?", text)
    return [w.lower() for w in re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?|\d+(?:[.,]\d+)*", text)]


def change_rate(a: List[str], b: List[str]) -> float:
    return round(1.0 - difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 3)


def retention(draft: List[str], final: List[str], lang: str) -> dict:
    """How much of the draft's wording survives in the final text.
    R_n = Σ_g min(c_F(g), c_D(g)) / Σ_g c_F(g) over n-grams g;
    V_k = share of final tokens inside verbatim runs of ≥ k tokens."""
    ns = (3, 4, 6, 8) if lang == "zh" else (2, 3, 4, 5)
    out: "OrderedDict[str, object]" = OrderedDict()
    for n in ns:
        cf = Counter(tuple(final[i:i + n]) for i in range(len(final) - n + 1))
        cd = Counter(tuple(draft[i:i + n]) for i in range(len(draft) - n + 1))
        total = sum(cf.values())
        out[f"R{n}"] = round(sum((cf & cd).values()) / total, 3) if total else 0.0
    k = 12 if lang == "zh" else 8
    blocks = difflib.SequenceMatcher(None, draft, final, autojunk=False).get_matching_blocks()
    covered = sum(b.size for b in blocks if b.size >= k)
    out[f"V{k}"] = round(covered / max(1, len(final)), 3)
    out["longest_verbatim_run"] = max((b.size for b in blocks), default=0)
    return out


def compare(orig: str, new: str, lang: str, section: Optional[str], by: str) -> dict:
    rep: "OrderedDict[str, object]" = OrderedDict()
    hard: List[str] = []
    warn: List[str] = []

    def diff_counter(name: str, a: Counter, b: Counter, is_hard: bool) -> None:
        lost = sorted((a - b).elements())
        added = sorted((b - a).elements())
        rep[name] = {"original": sum(a.values()), "rewrite": sum(b.values()), "lost": lost[:20], "added": added[:20]}
        if lost or added:
            msg = f"{name}: lost {lost[:6]} added {added[:6]}"
            (hard if is_hard else warn).append(msg)

    diff_counter("numbers", numbers(orig), numbers(new), True)
    diff_counter("citations", citations(orig), citations(new), True)
    diff_counter("table_figure_refs", refs(orig), refs(new), True)
    diff_counter("significance_statements", Counter(re.sub(r"\s+", "", m.group(0)) for m in _SIG.finditer(orig)),
                 Counter(re.sub(r"\s+", "", m.group(0)) for m in _SIG.finditer(new)), False)

    if lang == "zh":
        n0, n1 = _count(_NEG_ZH, orig, _NEG_ZH_PSEUDO), _count(_NEG_ZH, new, _NEG_ZH_PSEUDO)
    else:
        n0, n1 = _count(_NEG_EN, orig, _NEG_EN_PSEUDO), _count(_NEG_EN, new, _NEG_EN_PSEUDO)
    rep["negations"] = {"original": n0, "rewrite": n1}
    if n0 != n1:
        warn.append(f"negation count changed {n0} → {n1}: check that no claim flipped polarity")
    for d, rx in _DIR.items():
        a, b = len(rx.findall(orig)), len(rx.findall(new))
        rep[f"direction_{d}"] = {"original": a, "rewrite": b}
        if (a == 0) != (b == 0):
            warn.append(f"direction words '{d}' {a} → {b}: check the sign of every effect")
    strength = {}
    for level, rx in _VERB_STRENGTH:
        strength[level] = (len(rx.findall(orig)), len(rx.findall(new)))
    rep["evidence_verbs"] = {f"level{lv}": {"original": a, "rewrite": b} for lv, (a, b) in strength.items()}
    if strength[3][1] > strength[3][0]:
        warn.append(f"strong evidence verbs (prove / 证明 …) rose {strength[3][0]} → {strength[3][1]}: the rewrite claims more than the original")
    h0, h1 = len(_HEDGE.findall(orig)), len(_HEDGE.findall(new))
    rep["hedges"] = {"original": h0, "rewrite": h1}
    if h1 < h0 and by == "agent":
        warn.append(f"hedges fell {h0} → {h1}: fine if the original stacked them, a problem if a claim lost its only hedge")

    t0, t1 = tokens(orig, lang), tokens(new, lang)
    rate = change_rate(t0, t1)
    ratio = round(len(t1) / max(1, len(t0)), 2)
    rep["change_rate"] = rate
    rep["length_ratio"] = ratio
    cap = SECTION_CAPS.get(section or "", None)
    if by == "agent":
        if cap is not None and rate > cap:
            warn.append(f"change rate {rate:.0%} exceeds the {section} cap of {cap:.0%}: revert edits that no rule asked for")
        elif cap is None and rate > 0.50:
            warn.append(f"change rate {rate:.0%} > 50%: this is a recreation, not an edit — it belongs in the author's ownership pass")
        if ratio > 1.10:
            warn.append(f"rewrite is {ratio:.0%} of the original's length: cut words the edit added (deletion test)")
    rep["draft_retention"] = retention(t0, t1, lang)
    rep["hard_failures"] = hard
    rep["warnings"] = warn
    r4 = rep["draft_retention"].get("R4") if lang == "en" else rep["draft_retention"].get("R6")
    rep["layer_b"] = ("B: unknown · draft-retention " + ", ".join(f"{k}={v}" for k, v in rep["draft_retention"].items())
                      + (" — most of the draft's phrasing is still here" if r4 is not None and r4 > 0.5 else ""))
    return rep


# --------------------------------------------------------------------------- #
# Rendering and CLI
# --------------------------------------------------------------------------- #

def render_audit(path: str, lang: str, hits: List[dict], m: dict) -> str:
    L = [f"## AI-signature audit / AI 痕迹审计 · {path}", f"lang: {lang} · deterministic rules only — not a detector score", ""]
    if hits:
        L.append("| ¶ | Excerpt 原文片段 | Rule 规则 | Severity 严重度 |")
        L.append("|---|---|---|---|")
        for h in hits:
            name = h["name"] + (f" ×{h['count']}" if h.get("count") else "")
            L.append(f"| {h['para']} | {h['excerpt'].replace('|', '/')} | {h['rule']} {name} | {h['severity']} |")
    else:
        L.append("No regex-visible rule fired.")
    sev = Counter(h["severity"] for h in hits)
    worst = Counter(h["para"] for h in hits if h["severity"] == "🔴").most_common(3)
    L.append("")
    L.append(f"summary: 🔴 {sev.get('🔴', 0)} · 🟡 {sev.get('🟡', 0)} · 🟢 {sev.get('🟢', 0)}"
             + (f" · most 🔴 in ¶ {', '.join(str(p) for p, _ in worst)}" if worst else ""))
    L.append(f"left to the model (Step 1 reads these): {MODEL_JUDGED[lang]}")
    L.append("")
    L.append("metrics (" + METRIC_NOTE + "):")
    for k, v in m.items():
        L.append(f"  {k}: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(L)


def render_compare(a: str, b: str, rep: dict) -> str:
    L = [f"## Fidelity check / 保真核对 · {a} → {b}"]
    for k in ("numbers", "citations", "table_figure_refs", "significance_statements"):
        v = rep[k]
        mark = "✅" if not (v["lost"] or v["added"]) else ("❌" if k != "significance_statements" else "⚠️")
        L.append(f"{mark} {k}: {v['original']} → {v['rewrite']}"
                 + (f"  lost {v['lost']}" if v["lost"] else "") + (f"  added {v['added']}" if v["added"] else ""))
    for k in ("negations", "direction_up", "direction_down", "hedges"):
        L.append(f"   {k}: {rep[k]['original']} → {rep[k]['rewrite']}")
    ev = rep["evidence_verbs"]
    L.append("   evidence verbs (strong/medium/weak): "
             + " · ".join(f"{ev[f'level{lv}']['original']}→{ev[f'level{lv}']['rewrite']}" for lv in (3, 2, 1)))
    L.append(f"   change rate: {rep['change_rate']:.0%} · length ratio: {rep['length_ratio']}")
    L.append(f"   {rep['layer_b']}")
    if rep["hard_failures"]:
        L.append("hard failures (roll back these edits):")
        L.extend(f"  ❌ {x}" for x in rep["hard_failures"])
    if rep["warnings"]:
        L.append("warnings (author decides):")
        L.extend(f"  ⚠️ {x}" for x in rep["warnings"])
    L.append("verdict: " + ("FAIL — facts drifted" if rep["hard_failures"] else "PASS — facts intact")
             + (f" · {len(rep['warnings'])} warning(s)" if rep["warnings"] else ""))
    return "\n".join(L)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="aigc_audit.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("audit", help="Step 1: rule hits + report-only metrics")
    pa.add_argument("file")
    pa.add_argument("--lang", choices=("auto", "en", "zh"), default="auto")
    pa.add_argument("--json", action="store_true")
    pc = sub.add_parser("compare", help="Step 5: fidelity gate, change rate, draft retention")
    pc.add_argument("original")
    pc.add_argument("rewrite")
    pc.add_argument("--lang", choices=("auto", "en", "zh"), default="auto")
    pc.add_argument("--section", choices=sorted(SECTION_CAPS))
    pc.add_argument("--by", choices=("agent", "author"), default="agent",
                    help="agent: change-rate caps apply; author: the ownership pass, caps off")
    pc.add_argument("--json", action="store_true")
    sub.add_parser("self-test", help="run the built-in fixtures")
    args = ap.parse_args(argv)

    if args.cmd == "self-test":
        return self_test()
    if args.cmd == "audit":
        raw = read_text(args.file)
        lang = detect_lang(raw) if args.lang == "auto" else args.lang
        hits = run_rules(raw, lang)
        m = metrics(raw, lang)
        if args.json:
            print(json.dumps({"file": args.file, "lang": lang, "hits": hits, "metrics": m,
                              "model_judged": MODEL_JUDGED[lang]}, ensure_ascii=False, indent=2))
        else:
            print(render_audit(args.file, lang, hits, m))
        return 0
    orig, new = read_text(args.original), read_text(args.rewrite)
    lang = detect_lang(orig) if args.lang == "auto" else args.lang
    rep = compare(orig, new, lang, args.section, args.by)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render_compare(args.original, args.rewrite, rep))
    return 1 if rep["hard_failures"] else 0


# --------------------------------------------------------------------------- #
# Self-test
# --------------------------------------------------------------------------- #

AUDIT_FIXTURES: List[Tuple[str, str, str, Optional[str]]] = [
    # (label, lang, text, rule that must fire — None means nothing may fire)
    ("EN01 pivotal role", "en", "Digital finance plays a pivotal role in firm growth.", "EN01"),
    ("EN02 -ing tail", "en", "The estimate is stable across columns, highlighting the robustness of our design.", "EN02"),
    ("EN04 vague attribution", "en", "Studies have shown that credit constraints hinder innovation.", "EN04"),
    ("EN04 silent with citation", "en", "Studies have shown that credit constraints hinder innovation (Howell 2017).", None),
    ("EN11 bare significant", "en", "The reform significantly improves productivity.", "EN11"),
    ("EN11 silent with statistic", "en", "The coefficient is significant at the 1% level (t = 3.81).", None),
    ("EN23 chatbot residue", "en", "Certainly! Here is the revised results section.", "EN23"),
    ("EN24 citation leak", "en", "Entry rose sharply [oaicite:2] in treated cities.", "EN24"),
    ("EN24 placeholder", "en", "Entry rose by XX% relative to [Author, 20XX].", "EN24"),
    ("EN27 filler", "en", "It is worth noting that we cluster at the city level.", "EN27"),
    ("quoted text is masked", "en", "The ministry called it \"a pivotal role in the evolving landscape\" in 2019.", None),
    ("ZH01 window", "zh", "众所周知，数字经济发展迅速。毋庸置疑，其作用显而易见。", "ZH01"),
    ("ZH12 absolute", "zh", "回归结果充分证明了数字金融必然导致创新提升。", "ZH12"),
    ("ZH18 negation contrast", "zh", "促进创新的关键不是缓解融资约束，而是降低信息不对称。", "ZH18"),
    ("ZH19 reveal colon", "zh", "本文的核心发现是：试点使全要素生产率提高 6.8%。", "ZH19"),
    ("ZH21 translationese", "zh", "当融资约束得到缓解时，企业对研发投入进行了显著的分析。", "ZH21"),
    ("ZH28 formulaic opener", "zh", "近年来，人工智能技术的快速发展引起了学术界的广泛关注。", "ZH28"),
    ("ZH23 elevation tail", "zh", "系数在 1% 水平上显著为正，这为推动高质量发展提供了有益借鉴。", "ZH23"),
    ("ZH24 stacked hedges", "zh", "这在一定程度上或许可能说明渠道存在。", "ZH24"),
    ("ZH07 silent with citation", "zh", "已有研究表明数字金融缓解了融资约束（张三等，2020）。", None),
    ("ZH significance phrase is not ZH03", "zh", "系数在 1% 水平上显著为正，经济含义也不小。", None),
]


def self_test() -> int:
    failures = 0
    for label, lang, text, rule in AUDIT_FIXTURES:
        fired = {h["rule"] for h in run_rules(text, lang)}
        ok = (rule in fired) if rule else not fired
        failures += 0 if ok else 1
        print(f"[{'PASS' if ok else 'FAIL'}] audit · {label}" + ("" if ok else f"   fired={sorted(fired)}"))

    def check(label: str, cond: bool) -> None:
        nonlocal failures
        failures += 0 if cond else 1
        print(f"[{'PASS' if cond else 'FAIL'}] compare · {label}")

    a = "The reform raised entry by 12% (Table 3, column 2; Chen and Li, 2021). The effect is not driven by demand."
    b = "Entry rose 12% after the reform (Table 3, column 2; Chen and Li, 2021). Demand does not drive it."
    rep = compare(a, b, "en", "results", "agent")
    check("faithful EN rewrite passes", not rep["hard_failures"])
    rep = compare(a, a.replace("12%", "13%"), "en", None, "agent")
    check("changed number is a hard failure", any("numbers" in x for x in rep["hard_failures"]))
    rep = compare(a, a.replace("Chen and Li, 2021", "Chen, 2021"), "en", None, "agent")
    check("dropped co-author changes the citation key only if surname changes",
          not any("citations" in x for x in rep["hard_failures"]))
    rep = compare(a, a.replace("Table 3", "Table 4"), "en", None, "agent")
    check("table reference drift is a hard failure", any("table_figure_refs" in x for x in rep["hard_failures"]))
    rep = compare(a, a.replace("raised", "proves the reform raised"), "en", None, "agent")
    check("evidence-verb escalation warns", any("strong evidence verbs" in x for x in rep["warnings"]))
    rep = compare(a, a.replace("is not driven", "is driven"), "en", None, "agent")
    check("negation drift warns", any("negation" in x for x in rep["warnings"]))
    z0 = "数字金融使企业专利申请增加 8.3%（表 4 第（2）列），在 1% 水平上显著，这与张三等（2020）的结论一致。"
    z1 = "表 4 第（2）列显示，数字金融让企业专利申请增加 8.3%，在 1% 水平上显著；张三等（2020）也有相近发现。"
    rep = compare(z0, z1, "zh", "results", "agent")
    check("faithful ZH rewrite passes", not rep["hard_failures"])
    rep = compare(z0, z0.replace("8.3%", "8.5%"), "zh", None, "agent")
    check("ZH changed number is a hard failure", bool(rep["hard_failures"]))
    rep = compare(a, a, "en", None, "author")
    check("identical text has full retention", rep["draft_retention"]["R4"] == 1.0 and rep["change_rate"] == 0.0)
    rep = compare("−0.043 and 1,200 firms", "-0.043 and 1200 firms", "en", None, "agent")
    check("minus sign and thousands separator are typography, not drift", not rep["hard_failures"])
    print(f"\n{len(AUDIT_FIXTURES) + 10 - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
