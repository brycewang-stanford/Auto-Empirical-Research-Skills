# Auto-Empirical Research Skills (AERS) — README-zh-CN

> **📣 本 README 已合并到 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)。** GitHub 默认 README 见 [`README.md`](README.md)。
>
> 中文读者请直接阅读 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)，那里包含完整的"先看这里"段、69 合集一览、目录、按用途分组、精确数字、2 分钟验证、三层信用锚点、旗舰流水线、30 秒入口、信任面表、浏览全景、安全扫描、更新日志与贡献引用。

---

## 关于本文件的去向（2026-07 P2.2 重构说明）

本 README-zh-CN.md 与 README.md 历史上承载完全相同的中文正文（约 60 KB 各一份），维护成本极高（每个数据点要同步两份）。P2.2 重构把**所有中文正文抽到 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)**，本文件与 README.md 都退化为"入口 banner + 简短指引 + 底部脚注"：

| 你想看 | 跳到这里 |
|---|---|
| 完整中文内容（先看这里 / 69 合集 / 目录 / 信任 / 旗舰流水线 / 浏览全景 / 安全扫描 / 引用） | **[`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)** |
| GitHub 默认 README（banner + badges + 简短入口） | [`README.md`](README.md) |
| 英文版 | [`README-en.md`](README-en.md) |
| 繁體中文 | [`README-zh-TW.md`](README-zh-TW.md) |
| 日本語 | [`README-ja.md`](README-ja.md) |
| 한국어 | [`README-ko.md`](README-ko.md) |

### 维护规则

- **改中文正文 → 改 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)**；
- **改顶部 banner / badges / 简短入口 / 底部脚注 → 改 [`README.md`](README.md)**；
- **本 README-zh-CN.md 只在以下情况需要改**：新增语言切换入口、或新增跨语言说明。

### 选 A：彻底去重（已选择）

任务要求在两个 README 之间做选择：

- 选 A：**彻底去重，让 `README-zh-CN.md` 也指向 `CONTENT_ZH.md`** ✅
- 选 B：保留 README-zh-CN.md 作为"完整中文 README"（不动它）

本次采用选 A：README-zh-CN.md 与 README.md 互为等价入口，都指向 CONTENT_ZH.md。

---

<div align="center">

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
> ### 🚀 Open the **[Skill Search →](docs/search.html)** to filter all 1,150 skills. The 5-minute tour (`make quickstart`) prints the same picture in your terminal.

---

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![Security audit: 52/52 CLEAN](https://img.shields.io/badge/security%20audit-52%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
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