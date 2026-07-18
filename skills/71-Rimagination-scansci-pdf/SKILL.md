---
name: scansci-pdf
description: >
  Use this skill whenever the user wants to download academic papers, search for research literature,
  get citations (BibTeX/RIS/EndNote), manage WebVPN institutional proxy for paper access,
  import .bib files, or batch-download papers. This skill orchestrates the scansci-pdf MCP server
  which has 13+ download sources, 100+ university WebVPNs, and parallel download.
  TRIGGER when: user mentions downloading papers, DOI, arXiv ID, Sci-Hub, paper search,
  literature review, citation export, WebVPN, institutional access, "帮我下载论文", "搜索文献",
  "批量下载", "论文下载", "文献检索", or provides a list of DOIs/arXiv IDs.
  SKIP: user is only discussing papers conceptually without intent to download/search/cite,
  or user asks about non-academic PDFs (invoices, reports, etc.).
---

# scansci-pdf — 学术论文下载 MCP 服务

## 概述

scansci-pdf 是一个 MCP 服务器，提供 21 个工具，覆盖学术论文的搜索、下载、引文导出和 WebVPN 机构代理管理。支持 13+ 数据源并行下载，100+ 中国高校 WebVPN。

## 能力边界

### 直接能力（单工具即可完成）

| 能力 | 对应工具 | 说明 |
|------|----------|------|
| 按 DOI/arXiv ID 下载单篇论文 | `scansci_pdf_download` | 支持 5 种下载策略（fastest/scihub_only/...） |
| 批量下载多篇论文 | `scansci_pdf_batch_download` | 并发下载，默认 10 线程 |
| 关键词/作者搜索论文 | `scansci_pdf_search` | 基于 OpenAlex，支持关键词、作者名、作者ID |
| 导出引文 | `scansci_pdf_citation` | BibTeX / RIS / EndNote 三种格式 |
| 导入 .bib 文件并下载 | `scansci_pdf_import_bib` | 自动提取 DOI 并批量下载 |
| 推送到 Zotero | `scansci_pdf_zotero_push` | 需先下载论文到缓存 |
| 解析论文列表文件 | `scansci_pdf_parse_list` | 支持 APA、BibTeX、DOI 列表 |
| WebVPN 登录/测试/状态查询 | `scansci_pdf_vpnsci_*` 系列 | 5 个工具管理 WebVPN |
| 系统配置和健康检查 | `scansci_pdf_config_*` / `scansci_pdf_health_check` | 配置、缓存、诊断 |

### 组合能力（需编排多工具）

| 能力 | 工具编排 | 流程 |
|------|----------|------|
| 模糊研究查询 → 下载 | search → download | 先搜索获取 DOI，再下载 PDF |
| 论文列表全文下载 | resolve_and_download | 解析列表 → 补全 DOI → 批量下载 |
| 搜索+筛选+批量下载 | search → 人工筛选 → batch_download | 按关键词搜索，选择后批量下载 |
| WebVPN 设置+下载 | vpnsci_set_school → vpnsci_login → download | 5 步 WebVPN 流程 |
| .bib 导入+引文补全 | import_bib → citation | 下载后补充引文格式 |

### 不可实现（超出 MCP 能力）

| 请求 | 原因 |
|------|------|
| 阅读/理解论文内容 | scansci-pdf 只下载 PDF，不解析内容 |
| 翻译论文 | 需要其他工具（如 PDF 阅读+翻译 API） |
| 生成文献综述/摘要 | 需要 LLM 读取 PDF 后生成 |
| 下载非学术 PDF | 不支持普通网页 PDF、报告、发票等 |
| 访问付费期刊全文（无机构代理） | 无合法途径时可能失败 |

## MCP 工具参考

### 论文下载

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_smart_download` | **推荐** 零配置下载，自动尝试所有源 + Tor | `identifier`（必需）、`output_dir`（可选）、`bibtex`（可选）、`strategy`（可选，覆盖全局下载策略） |
| `scansci_pdf_download` | 下载单篇论文（完整参数控制） | `identifier`（必需）、`scihub_enabled`（可选）、`use_vpnsci`（可选）、`use_tor`（可选）、`bibtex`（可选）、`strategy`（可选） |
| `scansci_pdf_batch_download` | 批量下载多篇论文 | `identifiers`（必需）、`scihub_enabled`（可选）、`use_vpnsci`（可选）、`use_tor`（可选）、`batch_id`（可选，断点续传 ID）、`resume`（默认 true） |
| `scansci_pdf_resolve_and_download` | 解析列表 → 补全 DOI → 批量下载 | `file_path`（必需）、`resolve_titles`（默认 true） |

**参数约束：**
- `identifier`: DOI（如 `10.1038/nature12373`）、DOI URL、或 arXiv ID（如 `2301.00001`）
- `use_vpnsci`: 需先通过 `vpnsci_login` 完成 CAS 认证
- `use_tor`: 启用 Tor 代理（优先使用已运行的外部 Tor，否则自动启动内嵌 Tor）

**返回值：**
- 成功：`{"success": true, "file": "/path/to/paper.pdf", "doi": "...", "source": "..."}`
- 失败：`{"success": false, "error": "..."}`

**下载源（13+ 并行）：**

包括出版商直链、Unpaywall、OpenAlex、SemanticScholar、Crossref、DOAJ、EuropePMC、CORE、PMC、LibGen、Sci-Hub 等。启用 WebVPN 后还可通过高校代理访问。部分高级源需配置 API key。

### 搜索与解析

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_search` | 关键词/作者搜索论文（OpenAlex） | `query`（关键词搜索）、`author`（按作者名）、`author_id`（按作者ID）、`limit`（默认 10）、`year_from`、`year_to`、`sort` |
| `scansci_pdf_parse_list` | 解析论文列表文件 | `file_path`（必需，.md/.txt/.bib） |

**参数约束：**
- `query`: 关键词搜索。留空时可配合 `author` 或 `author_id` 按作者搜索
- `author`: 作者名（如 "Fang Jingyun"），自动解析为 OpenAlex 作者 ID，支持中英文姓名顺序互换
- `author_id`: OpenAlex 作者 ID（如 "A5102961214"），跳过姓名解析直接搜索
- `sort`: `"cited_by_count"`（被引最多）、`"publication_date"`（最新）、省略为相关性排序
- `year_from` / `year_to`: 整数年份，如 `2020`

**返回值（search）：**
```json
{"results": [{"title": "...", "doi": "...", "authors": [...], "year": 2024, "cited_by_count": 42, "abstract": "..."}]}
```

### 引文管理

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_citation` | 获取论文引文 | `identifier`（必需）、`format`（"bibtex"/"ris"/"endnote"） |
| `scansci_pdf_import_bib` | 导入 .bib 文件并下载全部论文 | `bib_file`（必需） |
| `scansci_pdf_zotero_push` | 推送论文到 Zotero | `identifier`（必需，需先下载） |

### WebVPN 管理

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_vpnsci_login` | 浏览器 CAS 认证登录 | 无 |
| `scansci_pdf_vpnsci_test` | 测试 WebVPN 连接性 | `doi`（可选，默认 10.1038/nature12373） |
| `scansci_pdf_vpnsci_status` | 检查登录状态 | 无 |
| `scansci_pdf_vpnsci_schools` | 搜索支持的大学 | `query`（可选，如"清华"） |
| `scansci_pdf_vpnsci_set_school` | 设置当前大学 | `school`（必需，如"清华大学"） |

### 系统管理

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_auto_setup` | **推荐** 一键环境检测与自动配置（启动 Tor、探测 Sci-Hub 域名） | 无 |
| `scansci_pdf_setup_check` | 检测系统环境，返回安装建议 | 无 |
| `scansci_pdf_health_check` | 检查所有数据源可用性 | `detailed`（默认 false） |
| `scansci_pdf_source_scores` | 查看各源自适应健康评分（成功率、延迟） | 无 |
| `scansci_pdf_network_diagnose` | 网络诊断：测试 DNS、代理、Tor、FlareSolverr 状态，返回修复建议 | 无 |
| `scansci_pdf_config_get` | 查看当前配置 | 无 |
| `scansci_pdf_config_set` | 修改配置项 | `key`（必需）、`value`（必需） |

### 机构登录（通用，支持所有出版商）

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_login` | **推荐** 统一登录：输入 DOI 自动识别出版商并打开浏览器 SSO | `identifier`（必需，DOI 或出版商名称）、`max_wait`（默认 300） |
| `scansci_pdf_browser_login` | CloakBrowser 持久化浏览器登录（WebVPN/CARSI/EZProxy/自定义） | `login_type`（"webvpn"/"carsi"/"ezproxy"/"custom"）、`custom_url`（login_type=custom 时必需） |
| `scansci_pdf_browser_status` | 检查 CloakBrowser 运行状态 | 无 |
| `scansci_pdf_browser_import_cookies` | 导入 Netscape 格式 cookie 文件到浏览器 | `cookie_file`（必需，cookie 文件路径） |
| `scansci_pdf_import_browser_cookies` | 通过浏览器捕获登录 cookie | `url`（默认 ScienceDirect）、`max_wait`（默认 300） |

**支持的出版商名称：** `elsevier`, `wiley`, `springer`, `nature`, `science`, `ieee`, `tandfonline`, `pnas`, `acs`, `rsc`, `aip`, `aps`, `iop`, `oxford`, `acm`

**工作原理：**
1. 传入 DOI → 自动打开该论文页面（通用，支持所有出版商）
2. 传入出版商名称 → 打开该出版商首页
3. 用户在浏览器中点击 "Access through your institution" 或 "Log In"
4. 选择机构并完成 SSO 登录
5. 登录完成后关闭浏览器
6. Cookies 自动捕获并保存，后续所有下载自动使用

### EZProxy（图书馆代理）

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_ezproxy_login` | 打开浏览器进行 EZProxy 图书馆代理登录 | 无 |
| `scansci_pdf_ezproxy_status` | 检查 EZProxy 配置和登录状态 | 无 |

**配置方式：**
```
scansci_pdf_config_set(key="ezproxy_enabled", value="true")
scansci_pdf_config_set(key="ezproxy_login_url", value="https://libproxy.你的学校.edu.cn/login?url={url}")
scansci_pdf_ezproxy_login
```

**常用配置项：**

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `download_strategy` | `fastest` | 下载策略：`fastest`（全部源竞速）、`scihub_only`（仅 Sci-Hub/LibGen/SciBban）、`scihub_first`（灰色源优先）、`oa_first`（OA 源优先）、`legal_only`（仅合法源） |
| `scihub_enabled` | `true` | 启用 Sci-Hub/LibGen |
| `openalex_api_key` | `""` | OpenAlex Content API key（免费，每天 100 次） |
| `elsevier_api_key` | `""` | Elsevier API key（ScienceDirect Article Retrieval API） |
| `elsevier_insttoken` | `""` | Elsevier 机构令牌（需学校图书馆申请） |
| `network_proxy` | `""` | 全局代理（如 `socks5://127.0.0.1:1080`） |
| `batch_workers` | `10` | 批量下载并发数 |
| `auto_rename` | `true` | 自动重命名为作者+标题 |
| `ezproxy_enabled` | `false` | 启用 EZProxy 图书馆代理 |
| `ezproxy_login_url` | `""` | EZProxy 登录 URL 模板 |

**缓存管理：** `scansci_pdf_cache_clear`（`identifier` 可选，省略清除全部）

### Tor 管理（内嵌 Tor，无需 Docker）

| 工具 | 描述 | 关键参数 |
|------|------|----------|
| `scansci_pdf_tor_install` | 自动下载安装 Tor Expert Bundle 到 ~/.scansci-pdf/tor/ | 无 |
| `scansci_pdf_tor_start` | 启动内嵌 Tor SOCKS5 代理 | `use_bridges`（默认 false，受限网络启用 obfs4 桥接） |
| `scansci_pdf_tor_stop` | 停止内嵌 Tor 代理 | 无 |

**使用流程：**
1. `scansci_pdf_tor_install` — 首次使用时下载 Tor 二进制（~30MB）
2. `scansci_pdf_tor_start` — 启动 Tor SOCKS5 代理（自动分配端口）
3. 下载时设置 `use_tor=true`，自动通过 Tor 代理访问
4. 在受限网络（如防火墙封锁 Tor）中，使用 `scansci_pdf_tor_start(use_bridges=true)` 启用 obfs4 桥接

## 工作流编排指南

### 流程 1：模糊研究查询

用户说"帮我下载 2020 年后植物功能性状对气候变化响应的论文"：

```
1. scansci_pdf_search(query="plant functional traits climate change", year_from=2020, limit=20, sort="cited_by_count")
2. 展示搜索结果给用户，让用户选择要下载的论文
3. scansci_pdf_download(identifier=用户选择的DOI) 或 scansci_pdf_batch_download(identifiers=[...])
```

**关键点：** 搜索后必须让用户确认，不要自动下载所有结果。

### 流程 1b：按作者搜索

用户说"下载方精云院士被引最高的 10 篇论文"：

```
1. scansci_pdf_search(author="Fang Jingyun", limit=10, sort="cited_by_count")
   → 自动解析为 Jingyun Fang (OpenAlex ID: A5102961214, 407 works, 45536 cited)
2. 从结果中提取 DOIs
3. scansci_pdf_batch_download(identifiers=[...], scihub_enabled=true)
```

**关键点：** `author` 参数支持中英文姓名顺序（"Fang Jingyun" ↔ "Jingyun Fang"），自动匹配被引最高的作者档案。也可用 `author_id` 直接指定 OpenAlex ID 跳过姓名解析。

### 流程 2：论文列表全文下载

用户提供一个包含论文引用的文件：

```
1. scansci_pdf_parse_list(file_path="papers.md") → 查看解析结果
2. scansci_pdf_resolve_and_download(file_path="papers.md") → 自动补全 DOI + 批量下载
```

**关键点：** `resolve_and_download` 内部会自动调用 OpenAlex 补全缺失的 DOI。

### 流程 3：WebVPN 设置

用户想通过学校代理下载论文：

```
1. scansci_pdf_config_set(key="vpnsci_enabled", value="true")
2. scansci_pdf_vpnsci_set_school(school="你的学校名称")
3. scansci_pdf_vpnsci_login → 浏览器打开 CAS 认证
4. scansci_pdf_vpnsci_test → 确认连接正常
5. scansci_pdf_download(identifier="...", use_vpnsci=true)
```

### 流程 5：付费论文登录下载（通用）

当下载返回 `error_type="paywall"` 和 `action="login_required"` 时，自动触发此流程：

```
1. scansci_pdf_download(identifier="10.1126/science.aec6396")
   → 返回 {"success": false, "error_type": "paywall", "action": "login_required",
           "agent_hint": "请运行 scansci_pdf_login(identifier=\"10.1126/science.aec6396\")..."}

2. scansci_pdf_login(identifier="10.1126/science.aec6396")
   → 打开浏览器到论文页面
   → 提示用户："点击 Access through your institution → 选择你的机构 → 完成 SSO 登录 → 关闭浏览器"
   → 用户关闭浏览器后，cookies 自动保存并导入

3. scansci_pdf_download(identifier="10.1126/science.aec6396")
   → 使用已保存的 cookies 成功下载 PDF
```

**关键点：**
- `login` 和 `download` 使用相同的 identifier (DOI)
- 传入 DOI 时打开论文页面（而非通用登录页），用户可直接看到 "Access through your institution" 按钮
- 无需配置 WebVPN/CARSI — 任何有机构账号的用户都能用
- Cookies 持久化保存，登录一次后所有同出版商的论文都能下载
- 对于批量下载中的多篇付费论文，只需登录一次（同出版商共享 cookies）

**支持的机构类型：** 中国及海外高校、研究所、图书馆等任何提供 SSO/Shibboleth/CARSI 认证的机构。请在 `vpnsci_schools` 中搜索你的学校名称，或直接配置 CARSI IdP。工具不应预设任何特定学校作为默认值。

**技术要点：**
- 浏览器引擎为 **CloakBrowser**（Playwright 兼容反检测浏览器），能通过 Cloudflare Turnstile
- **PDF 必须通过浏览器下载**——出版社（PNAS、Elsevier 等）检测 TLS 指纹，Python HTTP 客户端（requests/httpx）即使带有效 cookies 也会返回 403
- SSO 联邦选择：中国高校通常支持 **CARSI (CERNET Federation)**，部分高校同时支持 **OpenAthens**。若 CARSI 列表中找不到目标大学，尝试 OpenAthens 或用搜索框搜大学名称
- SSO 回调可能出现 about:blank 中间态——等待最终 URL 落在出版社域名即可，不要中断

### 流程 6：Elsevier API Key 配置（ScienceDirect 快速通道）

当 Elsevier/ScienceDirect 论文（DOI 以 `10.1016/` 开头）下载失败或需要更快下载时触发：

```
1. scansci_pdf_elsevier_setup
   → 自动打开浏览器到 Elseveloper Developer Portal
   → 返回详细注册步骤（中文指引）

2. 用户在浏览器中：
   → 注册/登录 → 点击 "My API Key" → 创建应用
   → 选择 "ScienceDirect Article Retrieval" API → 复制 API Key

3. scansci_pdf_config_set(key="elsevier_api_key", value="用户的APIKey")

4. scansci_pdf_elsevier_setup(test=true)
   → 验证 key 有效性 → 返回成功/失败状态

5. 后续所有 Elsevier 论文自动走 API 直接下载（1-2秒）
```

**触发时机：**
- 下载返回结果中 `hint` 包含 "elsevier_setup" 时
- 用户提到 ScienceDirect/Elsevier 论文下载慢或失败时
- 用户主动要求配置 API key 时

**关键点：**
- 申请完全免费，无需机构邮箱
- 配置一次，所有 Elsevier/ScienceDirect/Cell Press 论文受益
- API 下载比浏览器快 10-30 倍，且不受 Cloudflare 拦截影响
- 不配置也能用（走浏览器登录回退），但配置后体验大幅提升

### 流程 7：指定下载策略

用户明确要求从 Sci-Hub 下载（不走 OA/机构代理）：

```
1. # MCP: 单次覆盖策略
   scansci_pdf_download(identifier="10.1038/nature07944", strategy="scihub_only")
   
   # CLI: 
   scansci-pdf get 10.1038/nature07944 --strategy scihub_only
   
   # 全局配置（持久生效）：
   scansci_pdf_config_set(key="download_strategy", value="scihub_only")

2. # 批量下载也支持：
   scansci_pdf_batch_download(identifiers=[...], scihub_enabled=true)
   # CLI:
   scansci-pdf batch dois.txt --scihub
```

**可用策略：**
- `fastest`（默认）：全部源并行竞速
- `scihub_only`：仅 Sci-Hub / LibGen / SciBban
- `scihub_first`：灰色源优先，失败后回退合法源
- `oa_first`：OA 源优先，失败后回退灰色源
- `legal_only`：仅合法源，不碰 Sci-Hub/LibGen

**关键点：** 策略可全局配置（`config_set`）或单次覆盖（`strategy=` 参数）。`batch` 命令默认用机构级联（不含 Sci-Hub），需 `--scihub` 标志或 MCP 的 `scihub_enabled=true` 来启用灰色源。

### 流程 4：故障排查

下载失败时的诊断流程：

```
1. scansci_pdf_network_diagnose → 一键诊断网络（DNS、代理、Tor、FlareSolverr）
2. 根据诊断结果修复：
   - "检测到系统代理但未使用" → config_set network_proxy "<代理地址>"
   - "DNS 解析失败" → 配置代理或更换 DNS
   - "连接超时" → 配置代理绕过封锁
   - "FlareSolverr 未运行" → docker run -d -p 8191:8191 ghcr.io/flareSolverr/flareSolverr
3. 重试下载，失败结果中 hint.guidance 包含针对性建议
```

**关键点：** 下载失败时，结果中的 `hint.guidance` 字段会自动给出具体操作步骤（配置代理、切换策略、启用 WebVPN 等），无需手动排查。

## 常见边界情况

| 场景 | 处理方式 |
|------|----------|
| 用户只给了论文标题，没有 DOI | 先用 `search` 搜索标题获取 DOI，再用 `download` 下载 |
| 用户想下载的论文不在 OpenAlex 中 | 告知用户需要提供 DOI 或 arXiv ID |
| 用户想批量下载 100+ 篇 | 使用 `batch_download`，并发数由配置 `batch_workers` 控制 |
| 用户所在网络封锁 Sci-Hub | 配置代理或禁用 Sci-Hub（`config_set scihub_enabled false`） |
| 用户想下载的论文需要机构权限 | 运行 `scansci_pdf_login(identifier=DOI)` 打开浏览器登录，然后重试下载 |
| 用户想读取已下载论文的内容 | 超出能力，建议使用 PDF 阅读工具 |
| 用户环境缺少组件 | 调用 `setup_check` 诊断并按返回的建议引导 |

## 环境安装引导

当用户首次使用或遇到下载问题时，用 `scansci_pdf_setup_check` 诊断环境：

```
1. scansci_pdf_setup_check → 获取环境状态和安装建议
2. 根据 readiness 判断：
   - "ready" → 一切就绪，可直接使用
   - "partial" → 部分功能受限，按建议安装缺失组件
   - "limited" → 核心组件缺失，部分下载源不可用
3. 按返回的建议逐步引导用户安装
```

### 组件说明

| 组件 | 用途 | 必需？ |
|------|------|--------|
| Elsevier API Key | ScienceDirect/Elsevier 论文直接 API 下载（1-2秒） | 推荐（免费申请） |
| Tor | 匿名访问 Sci-Hub/LibGen，自动下载管理 | 可选（Sci-Hub 被封时需要） |
| WebVPN | 通过高校代理访问付费论文 | 可选（需要高校账号） |

### 快速安装

```
# 0.（推荐）配置 Elsevier API Key，ScienceDirect 论文直接下载
scansci_pdf_elsevier_setup → 打开浏览器注册 → 复制 key → scansci_pdf_config_set

# 1. 自动下载安装 Tor（首次使用）
scansci_pdf_tor_install

# 2. 启动 Tor 代理
scansci_pdf_tor_start
# 受限网络（防火墙封锁 Tor）：
scansci_pdf_tor_start(use_bridges=true)

# 3. 使用 Tor 下载论文
scansci_pdf_download(identifier="10.1038/nature12373", use_tor=true)
```
