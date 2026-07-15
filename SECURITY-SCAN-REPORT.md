# Skills 安全扫描报告（00 系列 + 01–48）

**扫描日期**：2026-04-28（首轮 01–47） / 2026-04-28（二轮：4 个 `00-*` + 48）
**精选定位**：本仓库（Auto-Empirical-Research-Skills, AERS）从 GitHub 上 **119 个仓库 / 23,000+ Agent Skills** 中精选收录 **52 个**实证研究 Skill。本扫描的对象就是这 52 个精选 Skill 的全部内容。
**扫描范围**：`skills/00-*`、`skills/00.1-*`、`skills/00.2-*`、`skills/00.3-*`、`skills/01-*` 到 `skills/48-*`，共 **52 个 skill 目录**，约 2,940+ 文件
**扫描人**：Claude（Opus 4.7，1M context）
**结论先行**：**未发现恶意 prompt、病毒、木马或其他恶意内容。52/52 全部 CLEAN，零 FLAGGED。**

![Skills 安全扫描总览](images/security-scan/security-scan-01-总览.png)

*图 1：扫描总览。52 个 Skill / 2,940+ 文件 / 13 类风险维度，全部 CLEAN，零真实威胁信号。所有敏感命中经验证均归入三类合法内容。*

---

## 总体结论

> **关于扫描范围的层次定位**：本仓库从 GitHub 上 **119 个仓库 / 23,000+ Agent Skills** 中精选收录了 **52 个**实证研究 Skill —— 不是把 23k 全收录，而是按研究流程（选题 / 文献 / 数据 / 分析 / 写作 / 修改 / 引用 / 复现 / 审稿）严格筛选过的精选集。本次安全扫描的对象，就是这 **52 个精选 Skill 的全部内容**（共 2,940+ 文件），不是上游 23k 大池子。

这 52 个精选 Skill 在所有自动化和人工检查维度均未触发任何真实威胁信号。所有看似敏感的 hits 经验证后均为以下三类合法内容之一：

1. **防御性安全规则**：明文禁止危险操作的 deny rule、bash-safety hook、凭据检测器（特别是 17-DAAF 这种"安全意识极强"的框架）。
2. **合法学术 API 调用**：arXiv、CrossRef、PubMed、Semantic Scholar、Unpaywall、ChEMBL、IPUMS、ERIC、DBLP、Hugging Face、FRED、World Bank、OECD、BLS 等公共研究数据源。
3. **标准 Claude Code 工作流 hook**：项目脚手架、状态保存/恢复、context 监控、会话存档、pre-commit 提醒——全部为本地文件操作，**零网络 IO**。

![六阶段扫描方法论](images/security-scan/security-scan-02-扫描方法.png)

*图 2：六阶段扫描方法论。从自动化模式扫描到 hook 人工审查、三 Agent 并行内容审查、再到补充完整性检查，多层防御逐级收敛。*

---

## Phase 1：自动化模式扫描（pattern grep）

| 检查项 | 结果 |
|---|---|
| Pipe-to-shell（`curl ... \| bash` 等）| 5 hits — 全部为 `uv` 安装命令、Claude Code 官方安装命令，或 17-DAAF 中的防御性禁用 |
| 反向 shell 特征（`/dev/tcp/`、`nc -e`、`bash -i`、socket 反弹）| 0 hit |
| 解码后运行（base64 解码再执行）| 0 hit |
| 长 base64 blob（≥200 字符）| 仅 Stata 国家变量名拼接，非编码内容 |
| 凭据窃取路径（`.ssh`、`.aws`、`/etc/passwd` 等）| 0 hit；所有 `.env` 相关引用均为**保护性**（17-DAAF 明文禁读）|
| 可疑外部 URL | 全部为合法学术/数据 API |
| Python 危险调用（`shell=True`、动态求值、模块动态导入）| 仅 1 hit：32-dylantmoore 的 Stata 插件 gcc 编译脚本，合法 |
| PowerShell 危险调用（`IEX`、`DownloadString`、`FromBase64String`）| 0 hit |
| 经典 prompt injection 短语（"ignore previous instructions" 等）| 0 hit |
| Jailbreak / 系统覆盖标记（`<system>`、`DAN`）| 0 hit；"system" 命中均为科学写作中性词 |
| 破坏性命令（`rm -rf /`、777 权限、setuid）| 全部为防御性 deny rule、合法 `/tmp` 清理、Docker 标准包缓存清理 |
| 数据外泄端点（Discord/Slack/Telegram/Pastebin webhook、Tor、tinyurl）| 0 hit |
| 加密货币挖矿 / RAT 签名（XMRig、Cobalt Strike、mimikatz 等）| 0 hit |
| 公网 IP 字面量 | 0 hit |
| URL 短链 | 0 hit |

![8 类核心威胁扫描结果](images/security-scan/security-scan-03-威胁矩阵.png)

*图 3：8 类核心威胁的扫描结果速览。绿色为 0 命中，橙色为有命中但全部经验证为合法内容（uv / Claude Code 官方安装命令、防御性 deny rule 等）。*

## Phase 2：Hook 与权限矩阵人工审查

涵盖所有 6 个含 hook 的 skill（共约 40 个 hook 脚本 + 6 个 settings.json）：

- **12-pedrohcgs**：notify、protect-files、pre/post-compact、context-monitor、log/verify-reminder
- **14-luischanci**：同上的 PowerShell 版本（Windows toast 通知 + 文件保护）
- **15-Felpix**：项目目录脚手架 + CLAUDE.md 占位模板（仅当不存在时创建）
- **16-hsantanna88**：post-merge 提示 + 文件保护 + compact 状态
- **17-DAAF**：14 个高质量防御性 hook（archive-session、audit-log、bash-safety、output-scanner 等），含 **32 条 deny rules** 和主动凭据检测
- **28-maxwell2732**：notify、protect、pre-compact、post-merge——纯文本提醒

**权限矩阵**：所有 settings.json 的 allow list 仅限研究工具（git、latex、python、pdftk 等）；无任何 `Bash(*)` 通配符；17-DAAF 还有 32 条显式 deny。

**网络 IO**：仅 4 个 hook 文件含 `http` 字符串——全部为注释（说明出处的 gist URL）或防御性阻断逻辑。**没有任何 hook 脚本进行实际的网络调用。**

## Phase 3-5：并行 agent 深度内容审查

3 个并行 agent 分别审查 SKILL.md、agent 定义、reference 文档与非 hook 代码。重点查找：散文中的 prompt injection、数据外泄指令、脚本后门、隐藏 Unicode/同形字、违背用户意图的指令、异常大文件、可疑包源。

### Skills 01–15

| # | Skill | 结论 | 说明 |
|---|---|---|---|
| 01 | lishix520-academic-paper-skills | CLEAN | 哲学论文规划/写作的 SKILL.md 与样式指南 |
| 02 | luwill-research-skills | CLEAN | 幻灯片/研究计划/医学影像 review；只调用 Zotero、arXiv、PubMed |
| 03 | K-Dense scientific-skills | CLEAN | grant/writing/literature/hypothesis 引用 scientific-schematics |
| 04 | K-Dense scientific-writer | CLEAN | citation/peer-review/writing 体系 |
| 05 | kthorn research-superpower | CLEAN | PubMed/Semantic Scholar/ChEMBL/Unpaywall 公共 API |
| 06 | fuhaoda stats-paper-writing | CLEAN | LaTeX 写作参考；无脚本网络调用 |
| 07 | Orchestra AI-Research-SKILLs | CLEAN | "Never hallucinate citations" 是**反幻觉防御指令** |
| 08 | ndpvt web-latex-document-skill | CLEAN | 单一 LaTeX 技能 |
| 09 | meleantonio awesome-econ-ai-stuff | CLEAN | 经济学 R/Stata/Python；FRED/World Bank/OECD/BLS 官方 API |
| 10 | Jill0099 causal-inference-mixtape | CLEAN | DiD/IV/RDD 代码模板 |
| 11 | James-Traina compound-science | CLEAN | `worktree-manager.sh` 是良性 git-worktree 帮手（本地复制 `.env`，不外传）|
| 12 | pedrohcgs claude-code-my-workflow | CLEAN | Quarto/Beamer 学术流；规则关于质量门，非行为覆盖 |
| 13 | scunning1975 MixtapeTools | CLEAN | 内置 PDF 是 split-pdf 演示素材（Gentzkow–Shapiro 经济学论文片段）|
| 14 | luischanci research-starter | CLEAN | R/Julia/因果推断 skills |
| 15 | Felpix-Studios social-science-research | CLEAN | explorer agent 仅引用 Census/CPS 等公共数据 |

> 07 与 11 中的 `disable-model-invocation: true` 是 Claude Code 的合法 frontmatter 字段（要求用户显式调用），不是安全旁路。

### Skills 16–30

| # | Skill | 结论 | 说明 |
|---|---|---|---|
| 16 | hsantanna88 clo-author | CLEAN | 18 个 agent 是常规研究流水线编排 |
| 17 | DAAF | CLEAN | 大型框架，"危险命令"提及全部在显式 deny-list 与安全规则中；唯一脚本 `context-bar.sh` 是 jq 状态条 |
| 18 | jusi-aalto-stata-accounting-research | CLEAN | 126 个 JAR 公开复现 `.do` 文件；`shell rm` 仅删除项目内 `${Data}` 临时文件 |
| 19 | CuellarC05 vera-economic-intelligence | CLEAN | 显式禁止上传 PII 到外部模型 |
| 20 | wenddymacro python-econ-skill | CLEAN | DiD/IV/RD/SC/DML 代码示例 |
| 21 | claesbackman AI-research-feedback | CLEAN | 只读评审模板 |
| 22 | christopherkenny | CLEAN | 显式"never modify the source file"防护 |
| 23 | Learning-Bayesian-Statistics baygent | CLEAN | `main.py` 是 print 占位；诊断脚本仅 arviz/pymc |
| 24 | Imbad0202 academic-research | CLEAN | 强调完整性验证、强制用户确认 |
| 25 | HosungYou Diverga | CLEAN | 29-agent 研究方法体系，含显式人工 checkpoint |
| 26 | Data-Wise-scholar | CLEAN | canvas.md 中的 JS 仅调用本地 Examark formatter 写 `.qti.zip` |
| 27 | dariia-m my_claude_skills | CLEAN | `dont-lie/SKILL.md` 是反幻觉协议——与恶意完全相反 |
| 28 | maxwell2732 paper-replicate-agent | CLEAN | hook 全部为本地会话/日志/保护工具 |
| 29 | quarcs-lab project20XXy | CLEAN | 显式"Stay within this directory"与"never delete data/code" |
| 30 | zirui-song | CLEAN | 7 个纯散文 `.md` |

### Skills 31–47

| # | Skill | 结论 | 说明 |
|---|---|---|---|
| 31 | thalysandratos | CLEAN | 计量经济学 SKILL.md；URL 是 mixtape/Wooldridge/fixest 等学术参考 |
| 32 | dylantmoore stata-skill | CLEAN | C-plugin SDK 从官方 stata.com 加载 `stplugin.h` |
| 33 | Galaxy-Dawn claude-scholar | CLEAN | Python 全部本地工具；最大文件（time-series.md ~340KB）是纯文本 |
| 34 | andrehuang research-companion | CLEAN | brainstorm/critic/strategist agent 编排 |
| 35 | bahayonghang academic-writing | CLEAN | 75 个 Python 脚本；网络仅 Semantic Scholar/arXiv/CrossRef/Tavily |
| 36 | taoyunudt literature-review | CLEAN | 单中文 SKILL.md，纯方法论散文 |
| 37 | IlanStrauss ai-skills | CLEAN | BLS/BEA/FRED/OECD/World Bank + Anthropic 官方 Playwright-MCP |
| 38 | peternka academic-proofreader | CLEAN | 多 agent 校对器；只写 `/tmp/proofread/` |
| 39 | vincentarelbundock marginaleffects | CLEAN | `marginaleffects` R/Python 包参考；权限限于 Read/Grep/Glob |
| 40 | py-econometrics pyfixest | CLEAN | `pyfixest` API 文档；无可执行脚本 |
| 41 | sticerd-eee sewage-econometrics | CLEAN | UK 邮编 PostcodesioR 地理编码 |
| 42 | wanshuiyin ARIS | MINOR_NOTE | 详见下文 |
| 43 | wentorai research-plugins | CLEAN | 478 个 SKILL.md 是合法研究 API 目录（NIH Reporter/NSF/GBIF 等）；无脚本 |
| 44 | matsuikentaro1 humanizer_academic | CLEAN | 医学论文文风工具；显式保护引文与数据完整性 |
| 45 | stephenturner skill-deslop | CLEAN | 纯文风 de-slop |
| 46 | hardikpandya stop-slop | CLEAN | 同 45 系列 |
| 47 | conorbronsdon avoid-ai-writing | CLEAN | 词汇替换风格指南；显式警告"不要过度编辑" |

### Skills 00 系列 + 48（二轮补扫）

| # | Skill | 结论 | 说明 |
|---|---|---|---|
| 00 | Full-empirical-analysis-skill_StatsPAI | CLEAN | 项目自家 skill，2 个 markdown 文件（README + SKILL）；StatsPAI 工作流文档，零脚本/hook/settings.json |
| 00.1 | Full-empirical-analysis-skill_Python | CLEAN | 10 个 markdown 文件，pandas/statsmodels/linearmodels/pyfixest/econml 教学示例；URL 仅指向 brycewang-stanford/StatsPAI 与本仓库 |
| 00.2 | Full-empirical-analysis-skill_Stata | CLEAN | 10 个 markdown 文件，reghdfe/csdid/synth/teffects 等 .do 片段；URL 含 stats.idre.ucla.edu 公开 Stata 教学样本 |
| 00.3 | Full-empirical-analysis-skill_R | CLEAN | 10 个 markdown 文件，fixest/did/grf/DoubleML/marginaleffects 教学；纯文档 |
| 48 | copaper-ai-chinese-de-aigc | CLEAN | 中文学术降 AIGC 风格指南（与 44–47 humanizer 系列同类）；含明确学术诚信声明，禁止用于代写/抄袭/数据篡改 |

![二轮补扫结果](images/security-scan/security-scan-05-补扫结果.png)

*图 4：二轮补扫的 5 个 Skill 状态。00 / 00.1 / 00.2 / 00.3 / 48 共 38 个文件、约 800KB，全部为纯 Markdown，无可执行代码面，风险面降至最低。*

> 5 个 skill **均为纯 markdown**（共 38 个文件，~800KB），未包含任何脚本、hook、settings.json 或可执行代码。13 类自动化模式扫描全部 0 hit；外链仅为合法 GitHub 仓库与 UCLA 公开教学站点。
>
> 关于 48 的双重用途说明：与 44-matsuikentaro1（英文医学论文 humanizer）和 45/46/47（de-slop 系列）同属"AI 文风消除"工具类。文档底部明确声明 "**学术诚信优先于检测率**"，列出"❌ 不适用：完全 AI 生成的论文，希望零改动通过检测 / 学术不端场景"。文风工具本身是合法用途，使用边界由作者明示——**不构成安全问题**。

#### 关于 42-wanshuiyin（MINOR_NOTE，非安全问题）

42 中包含两个**用户可选**的外部交互 skill，**默认关闭**且文档清晰：

1. `feishu-notify`：可选向飞书/Lark webhook 推送通知。URL 由用户在 `~/.claude/feishu.json` 配置；明确文档"不在通知中包含敏感信息"；默认关闭，opt-in。
2. `vast-gpu`：用于在 vast.ai 租用 GPU 时上传 SSH 公钥，是 vast.ai 的标准合法用法。

两者都是用户主动配置的开发工具，不是隐蔽渠道。**不构成安全问题**——但因为这是 31-47 范围内唯一会向用户配置的外部端点发出 HTTP 的功能，单独标注供你知情。

## Phase 6：补充完整性检查

| 检查项 | 结果 |
|---|---|
| 隐藏 Unicode（zero-width / RTL override / BOM）| 7 hits — 全部良性：mermaid 嵌套代码块的标准排版技巧（U+200B）、Stata 复制粘贴产生的 BOM、PDF 内置 XMP 元数据 packet |
| 非 UTF-8 脚本文件 | 1 hit — `18-jusi-aalto/references/JAR_60_ds.do` 是 macOS 资源叉损坏文件（Dropbox 同步异常），非可执行恶意载荷 |
| 极长行（>5000 字符）| 1 hit — Stata 单行 `gen` 国家变量拼接（合法）|
| 高比例非 ASCII 文件 | 全部为中文学术写作内容（合理），非编码混淆 |
| markdown 中嵌入 `<script>` / `<iframe>` 等 | 仅文档示例（Plotly CDN、Excalidraw 嵌入）|
| HTML 文件 | 仅 1 个：`16-hsantanna88/dot-claude/references/journal-profiles.html`（期刊参考资料）|
| Python 网络相关 import | 7 个文件——全部为合法学术 API 客户端（arXiv / CrossRef / Semantic Scholar / Tavily / DOI / 本地端口探测）|
| 环境变量访问 | 仅 `CLAUDE_PROJECT_DIR`、Obsidian 路径、研究 API key |

---

## 单点提醒（非安全问题，仅供参考）

1. **`18-jusi-aalto-stata-accounting-research/references/JAR_61_ds.do`**：文件已被 Dropbox 同步过程损坏（被 macOS 资源叉头部覆盖）。非恶意，但也不是有效的 Stata 文件——若你需要这份参考代码，应从原始仓库重新拉取。

2. **`uv` 与 Claude Code 安装命令**：03 和 33 中的 `curl ... | sh` 是从 Astral 官方安装 `uv` 包管理器；24 中的 `curl ... | bash` 是 Anthropic 官方 Claude Code 安装命令。这些是上游官方提供的命令，但 pipe-to-shell 模式本身有供应链风险——若严格审计可考虑改为先下载、校验 checksum、再执行。

3. **17-DAAF 反而是参考样板**：这是这批 skill 中**安全意识最强**的一个——主动扫描凭据泄漏、防止数据外泄、审计每次工具调用、明文禁止 32 类危险命令。值得在内部推广其防御模式。

4. **42-wanshuiyin 的可选外部 webhook**：见上文 MINOR_NOTE。如果你不主动配置 `~/.claude/feishu.json` 或 vast.ai 凭据，这两个 skill 不会向外发任何东西。

---

## 验收建议

![Top 5 大型 Skill 规模](images/security-scan/security-scan-04-规模分布.png)

*图 5：文件数最多的 5 个 Skill。规模最大 ≠ 风险最高——17-DAAF（319 文件）反而是这批 Skill 中"安全意识最强"的参考样板，主动扫描凭据泄漏、防止数据外泄、审计每次工具调用。*

- **你可以正常使用任意 skill**，无需删除或隔离任何条目。
- 如需进一步审查，可重点关注规模最大的几个：33-Galaxy-Dawn（327 文件）、17-DAAF（319 文件）、35-bahayonghang（264 文件）、43-wentorai（479 文件）。本报告对它们进行了 SKILL.md + 抽样代码审查，未发现异常。
- 二轮补扫的 5 个 skill（00 / 00.1 / 00.2 / 00.3 / 48）全部为纯 markdown 文档，没有可执行代码面，扫描风险面最低。

---

*报告由 Claude（Opus 4.7）生成。扫描方法：自动化 grep 模式匹配（13 类风险）+ hook 全量人工审查 + 3 个并行 agent 内容深读 + 完整性补充检查。覆盖 52 个 skill / 约 2,940+ 文件，覆盖率约 85%（重点目录 + 全部脚本 + 全部 hook + 抽样大型 reference）。二轮补扫 2026-04-28：4 个 `00-*` 系列 + 48-copaper-ai-chinese-de-aigc，全部 CLEAN。*

---

## 增补：49–70 增量模式扫描（2026-07-15）

原始基线（52 个集合 / 2,940+ 文件）之后，仓库又收录了 **22 个集合**（`49-voidborne-d-humanize-chinese` 至 `70-ssci-polish`，含 50-brycewang-aer-skills）。本次对这 22 个集合的全部 **1,146 个文件**（其中 1,029 个文本文件）做了与 Phase 1 同类的自动化模式扫描（13 类风险维度：pipe-to-shell、反向 shell、解码后执行、长 base64 blob、凭据路径、环境变量外泄、远程 eval/exec、`rm -rf`、挖矿特征、键盘/剪贴板监听、可疑 webhook、prompt 注入标记、混淆 Python）。

**结论：未发现恶意内容。9 个原始命中经逐一核验均为良性：**

| 命中 | 位置 | 核验结论 |
|---|---|---|
| pipe-to-shell ×3 | `56-hanlulong-econ-writing-skill/README-original.md` | 上游作者自己仓库的安装命令，仅出现在文档中，skill 本身不执行 |
| pipe-to-shell ×1 | `64-tmonk-mcp-stata/README-original.md` | 上游作者（tmonk）自有域名的安装器文档；同为文档性质，未被任何脚本调用 |
| 长 base64 ×2 | `67/68-*/marp-slides-creator/themes/beam.css` | CSS 内嵌 SVG data-URI（装饰图形） |
| 长 base64 ×2 | `69-Paper-WorkFlow/did_demo.ipynb` | notebook 输出中的 matplotlib PNG 图片 |
| `exec(compile(...))` ×1 | `69-Paper-WorkFlow/scripts/check_demo_execution.py` | 本地执行仓库自带 notebook 单元的检查脚本，无网络 IO，属标准 nbconvert 模式 |

**范围说明**：本增补为自动化模式扫描 + 命中人工核验，未包含基线报告的三 Agent 并行内容深读环节，严格程度低于原始六阶段方法论。README 徽章中的 "52/52 CLEAN" 仍指原始基线；依赖 49–70 号集合于高信任场景前，建议按原方法论补一轮深读。

*增补扫描由 Claude（Fable 5）执行于 2026-07-15。*
