# Auto-Empirical Research Skills (AERS)

> **⚠️ 中文版已迁出本文件。** 中文 README 内容（先看这里段、70 合集表格、目录、信任面、旗舰流水线等正文）已抽取到
> [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)。本文件只保留顶部 banner + badges + 简短入口 + 底部脚注；
> **完整中文内容请看 [docs/CONTENT_ZH.md](docs/CONTENT_ZH.md)。**
>
> English version: [`README-en.md`](README-en.md) · 中文完整正文：[`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md) · 旧版完整中文 README：[`README-zh-CN.md`](README-zh-CN.md)（已迁出，与本文件等效指向 CONTENT_ZH.md）

<div align="center">

**🌐 语言: [English](README-en.md) | 简体中文（默认） | [繁體中文](README-zh-TW.md) | [日本語](README-ja.md) | [한국어](README-ko.md)**

<br/>

  <table>
    <tr>
      <td align="center">
        <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="300" /></a>
      </td>
      <td width="72"></td>
      <td align="center">
        <img src="images/stanford-reap-logo.png" alt="Stanford REAP - Center on China's Economy & Institutions" width="440" />
      </td>
    </tr>
  </table>

  <br/>

  <strong>Stanford REAP × CoPaper.AI</strong> · 实证研究 AI 工具的学术工业级产品<br/>
  <sub>由斯坦福实证研究方法论团队打造，覆盖从数据清洗到顶刊投稿的完整工作流</sub>

  <br/>
  <br/>

  <img src="images/aers-readme-cover-cn.png" alt="实证研究智能体技能大全封面图" width="100%" />

  <br/>
</div>

> ### 🚀 New here? Open the **[Skill Search →](docs/search.html)** to filter all 1,151 skills by method, stage, language, and license. The 5-minute tour (`make quickstart`) prints the same picture in your terminal.
>
> ### 🇨🇳 **中文用户请直接看 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)** —— 完整中文内容已迁出本文件。📖 **English readers:** see [`README-en.md`](README-en.md) — this file is just the GitHub default README (banner + badges + footer).

---

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/Auto-Empirical-Research-Skills?style=social)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/brycewang-stanford/Auto-Empirical-Research-Skills/badge)](https://scorecard.dev/viewer/?uri=github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![Security audit: 52/52 CLEAN](https://img.shields.io/badge/security%20audit-52%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
[![Rigor coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fbrycewang-stanford%2FAuto-Empirical-Research-Skills%2Fmain%2Fdocs%2Fbadges%2Frigor-coverage.json)](docs/RIGOR_COVERAGE.md)
[![Powered by StatsPAI](https://img.shields.io/badge/powered%20by-StatsPAI-orange)](https://github.com/brycewang-stanford/StatsPAI)

---

### 信任面 · Trust surface (rigor stats)

| Rigor lane | Count | Where |
|---|---|---|
| Numeric **benchmark tasks** — gold values recomputed from real data each run | **17** | [`benchmark/`](benchmark/) |
| Behavioral **eval scenarios / rubric items** | **37 / 183** | [`eval-harness/`](eval-harness/) |

> Full trust overview: [`docs/TRUST.md`](docs/TRUST.md) · [`docs/RIGOR_COVERAGE.md`](docs/RIGOR_COVERAGE.md)

---

## 中文版指引（P2.2 重构）

本文件（P2.2 重构后）只承担 GitHub 默认入口的角色，**完整中文内容已迁出到 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)**：

- **先看这里段 / 70 合集一览 / 目录 / 按用途分组 / 精确数字 / 2 分钟验证 / 三层信任 / 旗舰流水线 / 30 秒入口 / 信任面表 / 浏览全景 / 安全扫描 / 更新日志 / 贡献与引用** → 全部在 CONTENT_ZH.md。
- **顶部 banner / badges / 底部脚注** → 保留在本文件（GitHub 默认渲染）。
- **入口分流**：
  - 中文读者 → [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)（新唯一权威中文版）
  - 英文读者 → [`README-en.md`](README-en.md)
  - 繁中 → [`README-zh-TW.md`](README-zh-TW.md)
  - 日文 → [`README-ja.md`](README-ja.md)
  - 韩文 → [`README-ko.md`](README-ko.md)

> [!NOTE]
> **维护规则：** 任何对正文（先看这里 / 70 合集 / 旗舰流水线 / 信任说明等）的改动，请改 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)；本 README 仅维护顶部 banner、badges、底部脚注与本节简短入口。
>
> **贡献者（Contributors）：** 提交前请在本地跑通完整门禁 `make check`（catalog 校验 + 链接 + 单元测试 + eval-harness + benchmark）。详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
>
> **旧版归档：** [`README-zh-CN.md`](README-zh-CN.md) 已重写为同一指向 CONTENT_ZH.md 的极简入口（与本文件等价）。原 README.md 的完整中文正文未删，仅迁移到 CONTENT_ZH.md，并在所有内部链接前缀前加 `../`（保留可用性）。

---

<div align="center">

**AI 是放大器，不是替代品。它替你做最耗时的"搬砖"，你保留最核心的"判断"。**

<br/>

<table>
  <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="220" /></a>
    </td>
    <td width="40"></td>
    <td align="center">
      <img src="images/stanford-reap-logo.png" alt="Stanford REAP" width="320" />
    </td>
  </tr>
</table>

<sub><strong>Stanford REAP × CoPaper.AI</strong> · 实证研究 AI 工具的学术工业级产品</sub>

<br/>

<table>
 <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-qrcode.png" alt="扫码访问 copaper.ai" width="180" /></a><br/>
      <strong>扫码访问 <a href="https://copaper.ai">copaper.ai</a></strong>
    </td>
    <td align="center">
      <img src="images/copaper-wechat.jpg" alt="CoPaper.AI 公众号" width="180" /><br/>
      <strong>关注公众号「CoPaper.AI」</strong>
    </td>
  </tr>
</table>

内置 20 个方法论 skill · 20 分钟完成实证论文 · 自研 <a href="https://github.com/brycewang-stanford/StatsPAI"><strong>StatsPAI</strong></a>（900+ 函数 / MIT 开源）

</div>