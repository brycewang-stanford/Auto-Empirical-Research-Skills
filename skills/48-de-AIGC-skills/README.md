# De-AIGC Skills · 中英双语学术降 AIGC

> **作者 Author**: CoPaper.AI · Stanford REAP
> **许可证 License**: CC-BY-SA-4.0 (repository default)
> **适用工具 Works with**: Claude Code / Cursor / Codex / Gemini CLI / any agent that speaks the Agent Skills standard

A bilingual (English + Chinese) skill that removes AI-generated writing
signatures from **empirical papers in economics, management, and the social
sciences** — 面向经管社科实证论文的中英双语降 AIGC Skill。

- **English side**: Turnitin AI, GPTZero, Originality.ai, Copyleaks
- **中文侧**: 知网 AMLC、万方、维普通达、Turnitin 中文版

## Why this skill 为什么需要它

Most humanizer skills handle one language and generic prose. Empirical papers
fail differently: the tell is not just "delve" and em dashes — it is
**overclaiming verbs hanging off observational coefficients, citation dumps,
uniform sentence rhythm, and conclusions that echo the abstract**. And Chinese
academic AI text has its own signature set (四字套话、虚词堆叠、总分总结构)
that English humanizers never touch.

This skill combines both, tuned for papers built on data and regression tables:

| Reference lineage | Language | What we took |
|-------------------|----------|--------------|
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | EN | academic pattern catalog; rhythm-first insight |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | EN | claim–evidence discipline; voice matching |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) · [harshaneel/humanize](https://harshaneel.github.io/humanize/) | EN | pattern taxonomy breadth |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) · [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) · [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | EN | audit-report format; scoring discipline |
| 本仓库前身 `chinese-de-aigc`（v1） | ZH | 17 类中文模式库、分章节策略、五维量表 |

## What's inside 结构

**Six-step loop 六步闭环**: intake/routing 定位路由 → audit 审计扫描 →
claim–evidence check 主张-证据核对 → differentiated rewrite 差异化改写 →
five-dimension self-score 五维自评 → cold-reader recheck 冷读复查

**Two pattern libraries 两套模式库**:

- [`references/patterns-en.md`](references/patterns-en.md) — EN01–EN22, with a
  preserve-list of legitimate academic phrases that must NOT be "fixed"
- [`references/patterns-zh.md`](references/patterns-zh.md) — ZH01–ZH17 中文模式库

**Section strategies 分章节策略**: [`references/sections.md`](references/sections.md)
— abstract through conclusion, bilingual symptoms, rewrite intensity per section

**Scoring 评分**: [`references/scoring.md`](references/scoring.md) — concreteness,
rhythm, calibration, implicit cohesion, researcher voice（含中英不同的句长阈值）

**Worked examples 案例**: [`references/examples-en.md`](references/examples-en.md)
(8 English cases) + [`references/examples-zh.md`](references/examples-zh.md)（12 组中文案例）

## Install 安装

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git /tmp/aers
cp -r /tmp/aers/skills/48-de-AIGC-skills ~/.claude/skills/de-aigc-skills
```

Or project-local: copy into `.claude/skills/de-aigc-skills`.

## Use 使用

Any of these triggers work 触发词示例:

- "Humanize this section / remove the AI writing patterns"
- "请对这段文本降 AIGC 检测率"
- "把这篇论文改得不像 AI 写的（中英文都要处理）"
- "Audit this draft for AI signatures before I submit"
- "诊断这段文字的 AI 痕迹，给出修改建议"

## Works well with 配合

| 场景 Scenario | 组合 Combo |
|------|---------|
| 中文论文投稿 | `de-aigc-skills` + [49 humanize-chinese](../49-voidborne-d-humanize-chinese/)（非学术语域）|
| SSCI submission | `de-aigc-skills` + [70 ssci-polish](../70-ssci-polish/) |
| Biomedical manuscripts | [44 humanizer_academic](../44-matsuikentaro1-humanizer_academic/) first, then this skill's Step 2 claim–evidence audit |
| General prose | [45 deslop](../45-stephenturner-skill-deslop/) / [46 stop-slop](../46-hardikpandya-stop-slop/) |

## Integrity statement 学术诚信声明

The goal is to return human-written and AI-assisted text to a real researcher's
language distribution — **not** to help fully AI-generated work evade detection.

- ✅ 研究者自己的初稿被检测器误判；AI 辅助起草 + 人工修改定稿
- ❌ 完全 AI 生成的论文求"零改动过检"；代写、抄袭、数据造假

**Academic integrity outranks detection scores. 学术诚信优先于检测率。**
Numbers, coefficients, citations, and claims are never altered — when a claim
lacks evidence, the skill flags it instead of hiding it.

## Contributing 贡献

PRs welcome: new patterns (either language), discipline-specific hedge
libraries (finance vs. sociology differ), more section-level cases, and
detector-behavior notes.
