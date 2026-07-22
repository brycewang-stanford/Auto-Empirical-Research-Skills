# AERS — README-zh-CN (DEPRECATED · 2026-07-19)

> **本文件已弃用。** 自 2026-07-19 起，中文 README 内容（含 **74 行核心 Skills 总表**、**"从 idea 到论文"完整流水线叙事**、⭐ 7 个 Stanford REAP × CoPaper.AI 自研 skill 主干）已并入 GitHub 默认入口 [**`README.md`**](README.md)。
>
> 本文件仅保留为**向后兼容的占位** —— GitHub 会自动重定向访问 `#README-zh-CN` 的旧链接，但读者会看到这个弃用提示。

## 跳转到当前版

| 你想看 | 点这里 |
|---|---|
| GitHub 默认 README（banner + badges + 简短入口） | [`README.md`](README.md) |
| 英文版 | [`README-en.md`](README-en.md) |
| 繁體中文 | [`README-zh-TW.md`](README-zh-TW.md) |
| 日本語 | [`README-ja.md`](README-ja.md) |
| 한국어 | [`README-ko.md`](README-ko.md) |
| 🌟 **中文默认 README**（含 74 行总表 + 端到端流水线） | [**`README.md`**](README.md) |
| 📘 中文详细正文（按用途分组 / 旗舰流水线 / 信任面 / 浏览全景 / 引用） | [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md) |
| 🇬🇧 English | [`README-en.md`](README-en.md) |
| 🇹🇼 繁體中文 | [`README-zh-TW.md`](README-zh-TW.md) |
| 🇯🇵 日本語 | [`README-ja.md`](README-ja.md) |
| 🇰🇷 한국어 | [`README-ko.md`](README-ko.md) |

## 为什么会有这个文件？

| 时点 | 状态 |
|---|---|
| 2026-07 以前 | 本文件与 [`README.md`](README.md) 各自维护约 60 KB 中文正文（双源）。维护成本高。 |
| 2026-07 P2.2 重构 | 把两份内容合并到 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)，本文件与 README.md 退化为"极简入口"。 |
| 2026-07-19（本次） | [`README.md`](README.md) 升级为中文默认入口（含 73 行表 + 流水线）。本文件正式弃用，指向 README.md。 |

> **维护规则：** 改中文正文 → 改 [`README.md`](README.md)；改项目级说明 → 改 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)。本文件不再维护内容。

---


**🌐 语言: [English](README-en.md) | 简体中文（默认，本文件等价指向 [CONTENT_ZH.md](docs/CONTENT_ZH.md)） | [繁體中文](README-zh-TW.md) | [日本語](README-ja.md) | [한국어](README-ko.md)**

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
</div>

> ### 🇨🇳 **请阅读 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md) 获取完整中文 README。**
> ### 🚀 Open the **[Skill Search →](docs/search.html)** to filter all 1,094 skills. The 5-minute tour (`make quickstart`) prints the same picture in your terminal.

---

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![Security audit: baseline 52/52 CLEAN](https://img.shields.io/badge/security%20audit-baseline%2052%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
[![Rigor coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fbrycewang-stanford%2FAuto-Empirical-Research-Skills%2Fmain%2Fdocs%2Fbadges%2Frigor-coverage.json)](docs/RIGOR_COVERAGE.md)

---

### 信任面 · Trust surface (rigor stats)

| 严谨性通道 Rigor lane | 数量 Count | 位置 Where |
|---|---|---|
| 数值 **benchmark 任务** —— 每次运行从真实数据重算金标准 | **17** | [`benchmark/`](benchmark/) |
| 行为 **eval 场景 / 评分项** | **37 / 183** | [`eval-harness/`](eval-harness/) |

> 完整信任面：[`docs/TRUST.md`](docs/TRUST.md) · [`docs/RIGOR_COVERAGE.md`](docs/RIGOR_COVERAGE.md)

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
<sub>最后更新：2026-07-19 · 由 [README.md](README.md) 取代 · 继承自 [docs/CONTENT_ZH.md](docs/CONTENT_ZH.md)</sub>
