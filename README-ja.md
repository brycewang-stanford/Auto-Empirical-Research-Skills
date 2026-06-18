# Auto-Empirical Research Skills (AERS)

<div align="center">

**🌐 言語: [English](README.md) | [简体中文](README-zh-CN.md) | [繁體中文](README-zh-TW.md) | 日本語 | [한국어](README-ko.md)**

<br/>

  <img src="images/aers-readme-cover-en.png" alt="Auto-Empirical Research Skills カバー" width="100%" />

  <br/>

  <table>
    <tr>
      <td align="center">
        <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="260" /></a>
      </td>
      <td width="60"></td>
      <td align="center">
        <img src="images/stanford-reap-logo.png" alt="Stanford REAP - Center on China's Economy & Institutions" width="380" />
      </td>
    </tr>
  </table>

  <br/>

  <strong>Stanford REAP × CoPaper.AI</strong> · 実証研究のための学術×産業 AI ツールキット<br/>
  <sub>スタンフォードの実証方法論チームが構築 — データクリーニングからトップジャーナル投稿までの全パイプライン</sub>

  <br/>
</div>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/Auto-Empirical-Research-Skills?style=social)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/brycewang-stanford/Auto-Empirical-Research-Skills/badge)](https://scorecard.dev/viewer/?uri=github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![Security audit: 52/52 CLEAN](https://img.shields.io/badge/security%20audit-52%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
[![Powered by StatsPAI](https://img.shields.io/badge/powered%20by-StatsPAI-orange)](https://github.com/brycewang-stanford/StatsPAI)

**実証研究の専門家のための agent-skills ディストリビューション。** マーケティング用のリストではありません —— 本リポジトリには **1,144 個のスキルを取り込み（vendored）、カタログ化**したうえで、**数値ベンチマーク・評価ハーネス・セキュリティ監査・CI** で品質を固定し、さらに広域エコシステムの **119 リポジトリにまたがる 23,000+ スキル**を精選したマップを重ねています。

AERS は同時に二つの性格を持ちます。(1) 完全な実証パイプライン — データクリーニング → 識別 → 推定 → 頑健性 → 表/図 → 投稿可能なドラフト — を回す、少数精鋭の**ファーストパーティ旗艦スキル**。そして (2) 実証研究スキルのエコシステムを、研究ワークフローの段階別に整理した**精選・セキュリティ配慮済みのカタログ**です。差別化の核心は数ではありません。旗艦の挙動が、口先で主張されたものではなく**既知の答えに対して検証されている**という点です。

> [!NOTE]
> **改名しました。** 本プロジェクトの旧称は *Awesome Agent Skills for Empirical Research* でした。GitHub は旧 URL を自動でリダイレクトしますが、リモートを更新してください:
> ```bash
> git remote set-url origin https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
> ```

---

## 目次

- [実際に得られるもの（数字を正確に）](#実際に得られるもの数字を正確に)
- [2 分で自分で検証する](#2-分で自分で検証する)
- [なぜ信頼できるのか — 3 つの層](#なぜ信頼できるのか--3-つの層)
- [旗艦パイプライン skills](#旗艦パイプライン-skills)
- [ここから始める — 30 秒でスキルを選ぶ](#ここから始める--30-秒でスキルを選ぶ)
- [23K スキルの寄せ集めで終わらない理由](#23k-スキルの寄せ集めで終わらない理由)
- [全体像を眺める](#全体像を眺める)
  - [研究段階別](#研究段階別)
  - [総合型スキルスイート](#総合型スキルスイート)
  - [アンチ AIGC 検出 & 学術文章の脱 AI 化](#アンチ-aigc-検出--学術文章の脱-ai-化)
  - [ツールカタログ（tools/）](#ツールカタログtools-自動化された実証因果推論ツール)
  - [マルチエージェントシステム · MCP サーバー · プラットフォーム · 学習](#マルチエージェントシステム--mcp-サーバー--プラットフォーム--学習)
- [セキュリティ](#セキュリティ)
- [変更履歴](#変更履歴)
- [貢献と引用](#貢献と引用)

---

## 実際に得られるもの（数字を正確に）

本 README の数字は常に正確で、混同を避けています。「vendored（取り込み済み）」とはファイルが本リポジトリ内に存在し、生成されたカタログで追跡されていることを指します。「カタログ化されたエコシステム」とは外部リポジトリへの精選されたリンクを指します。

| 内容 | 数 | 一次情報源 |
|---|---:|---|
| **本リポジトリに取り込み済み**でカタログ化されたスキル | **1,144** | [`catalog/skills.json`](catalog/skills.json) |
| 取り込み済み **コレクション（collections）** | **68** | [`catalog/skills.json`](catalog/skills.json) |
| **ファーストパーティ旗艦**の全パイプラインスキル（StatsPAI DSL + 明示的な Python/Stata/R） | **4** | [`skills/00*`](skills/) |
| 毎回データから gold 値を再計算する数値**ベンチマークタスク** | **5** | [`benchmark/`](benchmark/) |
| 挙動レベルの**評価シナリオ / ルーブリック項目** | **17 / 95** | [`eval-harness/`](eval-harness/) |
| **元のベースライン**のセキュリティ監査（コレクション / ファイル） | **52 / 2,940+**、52/52 CLEAN | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| **広域エコシステム**の精選マップ | **23,000+ スキル / 119 リポジトリ** | 本 README · [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md) |
| **ツールカタログ**（`tools/`）: 因果/計量ライブラリ、自律研究エージェント、MCP サーバー、因果探索、ベンチマークデータセット | **335 ツール / 6 カテゴリ** | [`tools/tools.json`](tools/tools.json) · [`tools/CATALOG.md`](tools/CATALOG.md) |

> セキュリティ監査が対象としたのは、元の **52 コレクション / 2,940 ファイルのベースライン（52/52 CLEAN）**です。そのベースライン以降に取り込まれたスキルは [`catalog/provenance.json`](catalog/provenance.json)、[`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md)、[`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) で追跡しています。高信頼が求められる文脈で利用する前には `make audit` を実行してください。

---

## 2 分で自分で検証する

ここで最も説得力があるのは数字ではなく、旗艦パイプラインの挙動が **API キーや有料モデルなしで検証できる**という点です。必要なのは Python 3 だけです:

```bash
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
cd Auto-Empirical-Research-Skills
make check        # repo validation + unit tests + eval lint + numeric benchmark
```

ベンチマークが決定的です。これは**実行のたびに生データセットから gold 答えを再計算する**ため、数字をハードコードして合格点を偽装することはできません。そのまま実行するだけで次を再現します:

- **LaLonde (1986) / Dehejia–Wahba (1999)** — 素朴な観察的比較は*符号を間違える*（−$635）。共変量調整を加えると正に反転し（≈ +$1,548）、実験ベンチマーク（≈ +$1,794）に近づきます。
- **Card (1995)** — IV による教育の収益率（0.131）は OLS（0.075）を*上回り*、第一段階 F 値（13.3）は隠さず報告されます。
- さらに staggered-DID（TWFE バイアス vs. group-time の真値）、シャープな **RDD**、そして**バッドコントロール / 処置後バイアス**の罠も含まれます。

パイプラインが合格となるのは、**罠を可視化し、誤解を招く数字を見出しに掲げることを拒み、再計算された真値に一致する**場合のみです。[`benchmark/`](benchmark/) と、完全な信頼性の概観 [`docs/TRUST.md`](docs/TRUST.md) を参照してください。

> 💡 **ホスト型でエンドツーエンドが欲しいですか?** 組み立ては不要です —— [**copaper.ai**](https://copaper.ai) が実証パイプラインを代わりに実行します。本カタログと同じスタンフォードの方法論チームによって、並行して構築されています。

---

## なぜ信頼できるのか — 3 つの層

| 層 | アンカー | もたらすもの |
|---|---|---|
| 🏛️ **学術的系譜** | **[Stanford REAP / SCCEI](https://sccei.fsi.stanford.edu/reap)** — Stanford Center on China's Economy and Institutions | 実証経済学の方法論で継続的な出版実績を持ち、応用因果推論に深い伝統を備えた研究センター。 |
| 🔧 **エンジニアリング実装** | **[CoPaper.AI](https://copaper.ai)** — 実証研究 AI アシスタント | Supervisor + 4 サブエージェントのアーキテクチャの背後で **20 個の計量方法論スキル**（DID / IV / RDD / PSM / DML …）を提供。一文のトリガー、自動で発表可能な出力。 |
| ⚙️ **オープンソースエンジン** | **[StatsPAI](https://github.com/brycewang-stanford/StatsPAI)** — 因果推論エンジン | **900+ 関数 · `import statspai as sp` の一行 · JOSS 投稿中 · MIT。** CoPaper.AI が生成するすべての DID / IV / RD / SCM 推定は StatsPAI によって駆動され、本カタログはそのエコシステムの一部です。 |

---

## 旗艦パイプライン skills

**同一の 8 ステップ実証ループ** — *データクリーニング → 変数構築 → 記述統計 → 診断 → 推定 → 頑健性 → メカニズム/異質性 → 発表可能な表と図* — を並行して実装した 4 つのバージョンに、投稿および脱 AIGC のスタックを加えたものです。それぞれが**漸進的開示（progressive disclosure）**を採用しています。`SKILL.md` には標準呼び出しの薄い背骨だけを置き、ステップごとの詳細なリファレンスマニュアルは必要なときだけ読み込みます。これらは共存します。スタックとユースケースで選んでください。

| Skill | スタック | 最適な用途 |
|---|---|---|
| **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)** 🔥 | Agent-native Python **DSL** — 一つの `sp.causal(...)` でループを実行。900+ 関数、自己記述型 API、統一された `CausalResult` | DSL を信頼できる場合に、エージェントの 1 呼び出しでパイプライン全体を自動化 |
| **[Full Empirical Analysis — Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md)** 📘 | **明示的**スタック: `pandas` · `statsmodels` · `linearmodels` · `pyfixest` · `rdrobust` · `econml` · `causalml` | 教育、レフェリーレベルの逐行監査、完全な制御を要する厳密なレプリケーション |
| **[Full Empirical Analysis — Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md)** 📊 | コミュニティ標準: `reghdfe` · `ivreg2` · `csdid` · `did_imputation` · `sdid` · `rdrobust` · `synth` · `psmatch2` · `boottest` · `esttab` | レフェリーや共著者が Stata のレプリケーションパックを求める場合（AER/QJE/JPE/ReStud スタイル） |
| **[Full Empirical Analysis — R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)** 📗 | モダンな tidyverse: `fixest` · `did` · `synthdid` · `HonestDiD` · `rdrobust` · `grf` · `DoubleML` · `marginaleffects` · **Quarto** | 単一の `.qmd` を一コマンドで PDF/HTML/Word にレンダリングする再現性レポート |
| **[AER-Skills](skills/50-brycewang-aer-skills/)** 📕 | 9 スキル: トピックルーティング → 識別監査 → 頑健性 → イントロ → 表 → レプリケーション → 投稿 → R&R → オーケストレーター | トップ 5 経済学（AER / AER:Insights / AEJ）への投稿: *識別ファースト* — 設計が脆弱なら、どんな文章でも救えない |
| **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/SKILL.md)** 🇨🇳 | 17 パターンの中国語 AI 痕跡ライブラリ、5 ステップの「特定→診断→書き換え→採点→レビュー」ループ | CNKI / Wanfang / VIP / Turnitin-Chinese 投稿向けの AI 文章シグナルの低減 |

> **なぜ DSL *と*明示的な移植版の両方が必要なのか?** ワンショットの DSL を信頼するときは StatsPAI を。教育・監査・各診断を手作業で差し替えなければならないときは 00.1/00.2/00.3 を選んでください。AER-skills はそのうえで、正しい分析を採択ラインまで押し上げます —— これらは*異なる*問題を解決し、互いに組み合わさります。

---

## ここから始める — 30 秒でスキルを選ぶ

| 目標 | まずこれを |
|---|---|
| 完全な実証パイプラインを実行 | [`StatsPAI`](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)（または [Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md) · [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md) · [R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)） |
| トップ 5 の識別戦略をまず監査 | [`aer-identification`](skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md) |
| AER / AEJ 投稿を準備 | [`aer-workflow`](skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md) |
| AEA 対応のレプリケーションパッケージを作成 | [`aer-replication`](skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md) |
| 中国語ドラフトの AI 文章シグナルを下げる | [`chinese-de-aigc`](skills/48-copaper-ai-chinese-de-aigc/SKILL.md) |

**さらなる入口:**

- **どのスキルか迷ったら?** → [`docs/CHOOSING_A_SKILL.md`](docs/CHOOSING_A_SKILL.md) · ファセット検索: [`docs/search.html`](docs/search.html)
- **最初の 10 分、エンドツーエンド** → [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- **完全なワークフローをコピペ** → [`docs/GOLDEN_WORKFLOWS.md`](docs/GOLDEN_WORKFLOWS.md)
- **ランタイムへのインストール / インストールせずに使う** → [`docs/INSTALL.md`](docs/INSTALL.md)
- **機械可読インデックス** → [`catalog/skills.json`](catalog/skills.json) · タクソノミー: [`docs/TAXONOMY.md`](docs/TAXONOMY.md) · 完全カタログ: [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)
- **FAQ** → [`docs/FAQ.md`](docs/FAQ.md)

---

## 23K スキルの寄せ集めで終わらない理由

公開スキルの数は容易に水増しでき、最近の研究は大規模なスキルインデックスがしばしば冗長で、時に安全でないことを示しています。AERS が競うのは**検証可能な品質**であって、生の数ではありません。以下の各層はすべて `make check` でローカルに、そして CI 上で実行されます。

| 層 | 何を捕捉するか | 場所 |
|---|---|---|
| **数値ベンチマーク** | 実データから再計算された真値と一致しない報告数字 —— 素朴 DID の符号の罠、第一段階 F なしの弱 IV、staggered なタイミング下での TWFE バイアス、RDD のトレンド交絡、処置後のバッドコントロール | [`benchmark/`](benchmark/) · 5 タスク |
| **評価ハーネス** | 文章レベルの失敗: 弱 IV の根拠なき安心、staggered-DID での TWFE 誤用、捏造引用、安全でない `curl \| bash` セットアップ、多重検定の濫用、AER 準拠のギャップ | [`eval-harness/`](eval-harness/) · 17 シナリオ / 95 ルーブリック項目 |
| **セキュリティ監査** | pipe-to-shell、リバースシェル、認証情報の流出、13 のリスクカテゴリにわたるプロンプトインジェクション —— 6 フェーズ、40+ フックスクリプトを手作業でレビュー | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| **来歴とライセンス** | 取り込まれていないソース、ライセンスリスク、1,144 個すべてのカタログ化スキルにわたる衛生のドリフト | [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md) · [`docs/SKILL_QUALITY.md`](docs/SKILL_QUALITY.md) |
| **CI と互換性** | カタログの鮮度、ローカルリンク切れ、GitHub Actions ポリシー、Python 3.9 **および** 3.12 の構文フロア | [`.github/workflows/`](.github/workflows/) · 6 ワークフロー |

```bash
make catalog     # regenerate catalog, provenance, audit, enrichment
make validate    # freshness + link / frontmatter checks
make check       # full gate: validate + Python compile + unit tests + eval lint + benchmark
```

この信頼の表面は**必要条件であって十分条件ではありません** —— 正規表現のルーブリックは文章を保証できず、小さなベンチマークはすべての設計を網羅できません。これは*既知の高コストな誤りに対して素早く失敗する*ように作られています。誠実なスコープは [`docs/TRUST.md`](docs/TRUST.md) と [`docs/QUALITY_GATE.md`](docs/QUALITY_GATE.md) を読んでください。

---

## 全体像を眺める

### 研究段階別

```
Topic Ideation → Lit Search → Deep Reading → Research Design → Data Collection
      │              │             │              │                │
      ▼              ▼             ▼              ▼                ▼
     01             02            03             01               04

Data Cleaning → Statistical Analysis → First Draft → Revision → Typesetting
      │              │                    │            │            │
      ▼              ▼                    ▼            ▼            ▼
     04             05                   06           07           08

Replication → Submission → Peer Review Response → Defense
      │           │              │                   │
      ▼           ▼              ▼                   ▼
     09          10             10                  10
```

段階別スキルノート（バイリンガル）: [01 選題と研究設計](docs/01-选题与研究设计.md) · [02 文献レビュー](docs/02-文献检索与综述.md) · [03 論文読解](docs/03-论文阅读与拆解.md) · [04 データと前処理](docs/04-数据获取与清洗.md) · [05 因果推論](docs/05-统计分析与因果推断.md) · [06 執筆](docs/06-论文写作.md) · [07 改稿](docs/07-论文修改与润色.md) · [08 引用とタイプセット](docs/08-引用管理与排版.md) · [09 レプリケーション](docs/09-论文复现与可复现研究.md) · [10 査読対応](docs/10-审稿回复与学术答辩.md)

### 総合型スキルスイート

> AERS が解消しようとする痛点: AI に「DID を回して」と頼むと、ベースライン回帰だけ出して止まる。「平行トレンドは?」と聞けば一つ足す。「プラセボは?」でまた一つ。*毎回、歯磨き粉を絞り出すように。* スキルとはエージェントのための**方法論プレイブック**です。完全な DID とは 平行トレンド → ベースライン → 頑健性バッテリー → 異質性 → メカニズム を意味し、各ステップで出力が定義されていることを、すでに知っています。

<details>
<summary><b>学術研究</b> — 汎用的な研究スイート（K-Dense、AI-Research-SKILLs、claude-scholar など）</summary>

| スイート | Stars | スキル数 | 主な特徴 |
|-------|-------|----------|-------------|
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 8,799 | 140+ | 28+ の科学データベース（OpenAlex、PubMed）; scientific-writing + literature-review + statistical-analysis |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 3,637 | 87 | 22 カテゴリ、ML 論文執筆、LaTeX テンプレート、引用検証 |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | ~1,790 | 複数 | 完全な論文パイプライン（research → write → review → revise → finalize）、スタイル較正、幻覚検出 |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | - | 25+ | 研究のフルライフサイクル: 構想 → レビュー → 実験 → 執筆 → 査読対応; Zotero MCP |
| [luwill/research-skills](https://github.com/luwill/research-skills) | 209 | 3 | 研究提案の生成、医学レビュー執筆、論文からスライド、バイリンガル |
| [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | 22 | 2 | Strategist（7 次元の査読者シミュレーション）+ Composer（体系的執筆） |
| [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) | - | 17 | 統計研究: arXiv 検索、DOI 照会、BibTeX、方法論執筆、レフェリー対応 |

</details>

<details>
<summary><b>経済学 / 因果推論</b> — ファーストパーティ旗艦 + コミュニティの Stata/IV/フィードバックスイート</summary>

ファーストパーティ旗艦（[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)、[Python](skills/00.1-Full-empirical-analysis-skill_Python/)、[Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)、[R](skills/00.3-Full-empirical-analysis-skill_R/)、[AER-skills](skills/50-brycewang-aer-skills/)）は[上記](#旗艦パイプライン-skills)で説明しています。コミュニティの補完:

| スイート | 主な特徴 | ユースケース |
|-------|-------------|----------|
| **[CoPaper.AI](https://copaper.ai)** | 20 個の方法論スキル、Supervisor + 4 サブエージェント、スマートルーティング、自動出力 | 実証経済学のフルワークフロー、ホスト型 |
| [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) | 2 エージェントのプレレビュー: 因果の過剰主張検出、識別評価（AER/QJE/JPE/Econometrica/REStud）; 6 エージェントのグラント審査 | 投稿前のセルフレビュー、グラント |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | LaTeX による統計論文執筆、フロントエンドのドラフト生成 | 統計学・計量経済学の論文 |
| [dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) | Stata の全カバレッジ: 構文、データ管理、計量経済学、因果推論、Mata、20+ パッケージ | Stata ユーザー |
| [SepineTam/stata-mcp](https://github.com/SepineTam/stata-mcp) | LLM が MCP 経由で Stata 回帰を直接駆動 | Stata 計量経済学 |
| [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) | Stata-MCP エディタ拡張（VS Code/Cursor/Antigravity）: `.do` を直接実行、ライブ出力、データ/グラフビューア; MIT · 414★（上記の SepineTam と同名だが別プロジェクト） | エディタ内での Stata との AI ペアリング |
| [tmonk/mcp-stata](https://github.com/tmonk/mcp-stata) · [`skills/64`](skills/64-tmonk-mcp-stata/) に取り込み済み | Stata MCP サーバー由来の **20 個の SKILL.md スキル**: レプリケーション / データ監査 / 発表 QA / レガシーのモダナイズ / レフェリー対応 / パワー / 因果推論; **AGPL-3.0**（別ライセンスの集合体として保持、サーバーコードは取り込まず） | Stata のレプリケーションと頑健性監査 |
| [PovertyAction/ipa-stata-template](https://github.com/PovertyAction/ipa-stata-template) | IPA の再現可能な Stata 研究テンプレート + `.claude/skills`: 番号付きパイプライン、アサーションベースの防御的プログラミング、LaTeX 表; MIT | 開発経済学 / フィールド RCT のレプリケーション |
| [lcrawfurd/claude-skills](https://github.com/lcrawfurd/claude-skills) | 学術スキル: 論文 / コードレビュー、レフェリー、投稿前; code-review が Stata/R/Python のコーディング規約（DIME / Reif / AEA Data Editor）を符号化 | 投稿前レビューとコード監査 |
| [AEADataEditor/replication-template](https://github.com/AEADataEditor/replication-template) | AEA Data Editor 公式のレプリケーションパッケージテンプレート（Stata 中心、`REPLICATION.md`）—— 再現性の「ゴールドスタンダード」 | AEA / トップジャーナルのレプリケーションパッケージング |

</details>

<details>
<summary><b>金融 · 教育と公衆衛生 · 法律 · マーケティング · プロダクト · 汎用エージェント</b></summary>

**金融と投資** — [financial-services-plugins](https://github.com/anthropics/financial-services-plugins)（Anthropic 公式）· [OctagonAI/skills](https://github.com/OctagonAI/skills) · [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) · [himself65/finance-skills](https://github.com/himself65/finance-skills) · [quant-sentiment-ai/claude-equity-research](https://github.com/quant-sentiment-ai/claude-equity-research)

**教育と公衆衛生** — [GarethManning/claude-education-skills](https://github.com/GarethManning/claude-education-skills) · [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills)（**869** の医学スキル: 疫学、サーベイランス、臨床研究、医薬品安全、生物統計）

**ガバナンス、コンプライアンス、法律** — [Claude-Skills-Governance-Risk-and-Compliance](https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance)（ISO 27001 / SOC 2 / GDPR / HIPAA）· [zubair-trabzada/ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude) · [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)

**マーケティングと消費者行動** — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) · [zubair-trabzada/ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) · [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)

**プロダクトと組織行動** — [phuryn/pm-skills](https://github.com/phuryn/pm-skills)（100+ スキル）· [mastepanoski/claude-skills](https://github.com/mastepanoski/claude-skills)（Nielsen ヒューリスティック、NIST AI RMF、ISO 42001）

**汎用エージェント能力** — [lyndonkl/claude](https://github.com/lyndonkl/claude)（85 スキル + 6 オーケストレーター）· [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)（220+ スキル、~5,200★）· [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) · [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)（1,367 スキル）· [posit-dev/skills](https://github.com/posit-dev/skills)（Posit 公式）

</details>

### アンチ AIGC 検出 & 学術文章の脱 AI 化

> 2026 年で最も鋭い痛点の一つ: AIGC 検出（Turnitin、GPTZero、CNKI）を通過できない論文は即座にリジェクトされ得ます。以下のスキルは最も完成度の高いオープンソースソリューションです —— すべて MIT、すべてローカルにアーカイブ（`skills/44-48`）。

| スイート | 主な特徴 | 最適な用途 | ローカル |
|-------|-------------|----------|-------|
| **chinese-de-aigc** 🇨🇳 | CoPaper.AI による**オリジナル**の中国語学術脱 AIGC; 17 パターンの中国語痕跡ライブラリ、5 ステップループ、セクション別戦略、5 次元採点。中国語学術の脱 AIGC に特化した唯一の GitHub スキル | CNKI / Wanfang / VIP / Turnitin-Chinese | [`48`](skills/48-copaper-ai-chinese-de-aigc/) |
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | 学術特化; 23 の AI 文章パターン; 正当な学術的接続表現を保持 | 医学、生命科学、自然科学の論文 | [`44`](skills/44-matsuikentaro1-humanizer_academic/) |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) | 正当な分野の慣習と AI 痕跡を区別; 5 次元採点 | 科学論文、技術ブログ | [`45`](skills/45-stephenturner-skill-deslop/) |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 3 層検出 + 5 次元採点; 禁止フレーズ、構造的クリシェ、文ルール | 一般的な散文、ブログ、レポート | [`46`](skills/46-hardikpandya-stop-slop/) |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 構造化監査 + 書き換え + 2 回目の監査; 監査可能、追跡可能 | 証跡を必要とするワークフロー | [`47`](skills/47-conorbronsdon-avoid-ai-writing/) |

> **組み合わせ:** 🇨🇳 中国語（CNKI/Wanfang/VIP）→ chinese-de-aigc · 🇬🇧 英語 → humanizer_academic · 監査証跡が必要 → avoid-ai-writing · 一般的な散文 → stop-slop。

### ツールカタログ（`tools/`）— 自動化された実証・因果推論ツール

> 上記のスキルとは異なり、[`tools/`](tools/) はエージェント（または研究者）が**実際に呼び出すソフトウェアとサービス**をカタログ化したものです —— 構造化され、ライセンスとメンテナンスを意識し、`make validate` に組み込まれています。一次情報源: [`tools/tools.json`](tools/tools.json); 閲覧可能なリスト: [`tools/CATALOG.md`](tools/CATALOG.md)。

**6 カテゴリにまたがる 335 ツール**（2026-06 精選）:

- **因果推論 / 処置効果ライブラリ（32）** — DoWhy · EconML · CausalML · DoubleML · CausalPy · causallib · grf · CATENets · TMLE ファミリー · メンデルランダム化 …
- **計量経済学 / 準実験ライブラリ（170）** — パネル FE · DiD（モダン/staggered を含む）· イベントスタディ · RDD · IV · 合成コントロール/SDID · マッチング & ウェイティング · 感度分析（fixest · did · HonestDiD · rdrobust · synthdid · reghdfe · csdid · sdid · pyfixest · linearmodels …）; **加えて**空間計量経済学（spdep · PySAL/spreg · GeoDa）、局所射影/IRF & (S)VAR（lpirfs · vars · svars）、調査ウェイティング/MRP/raking（survey · samplics · balance）、メタアナリシス（metafor · meta · netmeta · metan）—— R/Python/Stata/Julia にわたる。
- **自律研究 / データサイエンスエージェント（51）** — エンドツーエンドの研究 & データ分析: AI-Scientist · data-to-paper · Agent Laboratory · RD-Agent · AI-Researcher · STORM · PaperQA2 · gpt-researcher · DeepAnalyze · MetaGPT (DI) · Biomni …（⚠️ 非 OSI / LICENSE なしのリポジトリを含む —— 使用前に条件を確認）。
- **MCP サーバー（48）** — 統計実行（StatsPAI · stata-mcp · R/Jupyter MCP）+ データアクセス（FRED · World Bank · IMF · OECD · Eurostat · Census · BEA · BLS · SEC EDGAR · OpenAlex · Semantic Scholar · PubMed · Zotero · arXiv …）。
- **因果探索 / 構造学習（25）** — causal-learn · Tetrad/py-tetrad · gCastle · CDT · tigramite (PCMCI) · LiNGAM · NOTEARS/DAGMA · pcalg · bnlearn · pgmpy …
- **ベンチマーク & データセット（9）** — causaldata · IHDP/Twins · ACIC コンペティションデータ · RealCause · JustCause · Tübingen cause-effect pairs · bnlearn ネットワークリポジトリ …

完全な解説: [`tools/README.md`](tools/README.md)。

### マルチエージェントシステム · MCP サーバー · プラットフォーム · 学習

<details>
<summary><b>マルチエージェント協調システム</b> — 論文改稿、自律研究、データサイエンスチーム</summary>

役割分離が単一エージェントに勝るのは、レビュアーがドラフト作成者から独立しているからです —— 同行評価（ピアレビュー）と同じ論理です。

**論文改稿と執筆:** copy-edit-master（3 サブエージェント、Strunk & White / McCloskey ルール）· introduction-writer（strategist → drafter → reviewer → reviser）· CoPaper.AI PaperAgent（Supervisor + 4 サブエージェント）。

**自律研究とデータサイエンス:** [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze) · [business-science/ai-data-science-team](https://github.com/business-science/ai-data-science-team) · [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)（NeurIPS 2025 Spotlight）· [wanshuiyin/ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) · [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)（コスト 84% 削減）· [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) · [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) · [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)（Emory）。

</details>

<details>
<summary><b>学術データ MCP サーバー</b> — OpenAlex、Semantic Scholar、FRED、World Bank、Zotero など</summary>

[xingyulu23/Academix](https://github.com/xingyulu23/Academix) · [Eclipse-Cj/paper-distill-mcp](https://github.com/Eclipse-Cj/paper-distill-mcp) · [oksure/openalex-research-mcp](https://github.com/oksure/openalex-research-mcp)（2.4 億+ の作品）· [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)（20+ ソース）· [lzinga/us-gov-open-data-mcp](https://github.com/lzinga/us-gov-open-data-mcp)（40+ の米国政府 API）· [stefanoamorelli/fred-mcp-server](https://github.com/stefanoamorelli/fred-mcp-server)（FRED 80 万+ シリーズ）· [llnOrmll/world-bank-data-mcp](https://github.com/llnormll/world-bank-data-mcp) · [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)

</details>

<details>
<summary><b>スキル集約プラットフォームと学習リソース</b></summary>

**プラットフォーム:** [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)（1,000+）· [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)（1,340+）· [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)（5,400+）· [skills.sh](https://skills.sh/) · [ClawHub](https://clawhub.com)（13,729）· [Anthropic 公式スキル](https://github.com/anthropics/skills)。

**学習:** [Claude Code Skills ガイド（PDF）](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) · [Agent Skills Standard](https://agentskills.io/) · [Causal Inference for the Brave and True](https://github.com/xieliaing/CausalInferenceIntro) · [Awesome AI for Economists](https://github.com/hanlulong/awesome-ai-for-economists) · [Awesome Econ AI Stuff](https://github.com/meleantonio/awesome-econ-ai-stuff)。

</details>

---

## セキュリティ

**元の 52 スキルコレクション / 2,940+ ファイル**は体系的な監査を通過しました —— **52/52 CLEAN、FLAGGED ゼロ**: 悪意あるプロンプト、ウイルス、リバースシェル、プロンプトインジェクションは皆無。すべての「センシティブ」なヒットは、3 つの正当なカテゴリのいずれかとして検証されました: **防御的セキュリティルール**、**正当な学術 API 呼び出し**（arXiv / CrossRef / PubMed / FRED / World Bank / OECD / BLS）、または**標準的な Claude Code ワークフローフック**（すべてローカルファイル操作、ネットワーク IO ゼロ）。

![Skills Security Scan Overview](images/security-scan/security-scan-01-总览.png)

6 フェーズ、多層防御: **13 のリスクカテゴリ**にわたる自動 grep → **6 個のフックを持つスキルとその 40+ フックスクリプト**の 100% 手動レビュー（どこにも `Bash(*)` ワイルドカードなし）→ 3 つの並列エージェントによるコンテンツ監査 → 補足的な完全性チェック（隠れた Unicode、エンコーディング異常、HTML インジェクション、ネットワーク import）。

> **重要な洞察:** 最大 ≠ 最も危険。最大級のスキルはすべて通過しました; [17-DAAF](skills/17-DAAF-Contribution-Community-daaf/) はむしろセキュリティ意識の高い設計の基準を打ち立てています（14 個の防御フック + 32 のディナイルール + アクティブな認証情報スキャン）。

ベースライン以降に取り込まれた新規追加は [`catalog/provenance.json`](catalog/provenance.json) と [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) で追跡しています —— `make audit` を実行してください。完全なレポート: [**SECURITY-SCAN-REPORT.md**](SECURITY-SCAN-REPORT.md)。

---

## 変更履歴

物語形式の変更履歴は [**CHANGELOG.md**](CHANGELOG.md) に移動しました。最近のハイライト:

- **2026-05** — **AER-skills**（トップ 5 経済学投稿スタック、9 スキル）を週次の上流同期付きで取り込み; 数値ベンチマークを **5 つの因果回復タスク**に、評価ハーネスを **17 シナリオ / 95 ルーブリック項目**に拡張。
- **2026-04** — **52/52 のセキュリティベースライン**を完了; 4 つの全パイプライン旗艦（**StatsPAI** + 明示的な **Python / Stata / R**）を出荷; オリジナルの **chinese-de-aigc** スキルをローンチ。
- **それ以前** — 43 コレクションから **119 リポジトリ / 23,000+ スキル**の精選マップへ成長; バイリンガル README、学術データ MCP サーバー、マルチエージェントシステムを追加。

---

## 貢献と引用

貢献を歓迎します —— [CONTRIBUTING.md](CONTRIBUTING.md) と [`docs/SKILL_SUBMISSION_GUIDE.md`](docs/SKILL_SUBMISSION_GUIDE.md) を参照してください。特に社会科学スキル（経済学、政治学、社会学、心理学、教育、公衆衛生）、新しい因果推論の実装、学術/政府データ向けの MCP サーバー、中国語フレンドリーなスキル、マルチエージェントのケーススタディを歓迎します。新規提出は、来歴監査のために **ソース、ライセンス、カテゴリ** を申告する必要があります。

AERS があなたの研究に役立ったら、ぜひ**引用**し（[CITATION.cff](CITATION.cff)）、**リポジトリにスター**を付けて、より多くの研究者が見つけられるようにしてください。

<a href="https://www.star-history.com/#brycewang-stanford/Auto-Empirical-Research-Skills&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" width="600" />
 </picture>
</a>

---

<div align="center">

**AI は増幅器であって代替物ではありません。重労働は AI が引き受け、核心となる判断はあなたが保ちます。**

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

<sub><strong>Stanford REAP × CoPaper.AI</strong> · 実証研究のための学術×産業 AI ツールキット</sub>

<br/>

<table>
  <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-qrcode.png" alt="copaper.ai にアクセス" width="180" /></a><br/>
      <strong><a href="https://copaper.ai">copaper.ai</a> にアクセス</strong>
    </td>
    <td align="center">
      <img src="images/copaper-wechat.jpg" alt="CoPaper.AI WeChat" width="180" /><br/>
      <strong>WeChat: CoPaper.AI</strong>
    </td>
  </tr>
</table>

20 個の組み込み方法論スキル · 20 分で実証論文 · <a href="https://github.com/brycewang-stanford/StatsPAI">StatsPAI</a>（900+ 関数、MIT）駆動

<br/>

<a href="https://copaper.ai"><strong>CoPaper.AI</strong></a> が運営、<a href="https://sccei.fsi.stanford.edu/reap"><strong>Stanford REAP / SCCEI</strong></a> でインキュベート · 実証研究のための AI アシスタント

</div>
</output>
