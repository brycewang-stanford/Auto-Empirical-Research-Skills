---
name: chinese-ppt2
description: Upgrade of chinese-ppt for Chinese Beamer decks (xelatex + ctex + fandol, CUFE template). Same 7-section outline and X→M→Y framework, but adds (a) mandatory 1.3 line-spacing + 3pt paragraph spacing, (b) overflow-prevention line budget + balanced split-frame rules, (c) prose rewrites that strip AI-ish "关键比较/理论映射" labels and redundant 章节括号注释, (d) stricter CJK-space + middle-dot rules, (e) retrofit workflow for existing chinese-ppt decks, (f) mandatory local linespread reset inside TikZ / table / fixed-geometry frames. Use for "做中文学术PPT 2 版"、"中文 Beamer 改进版"、"答辩 PPT chinese-ppt2"、"防越界 PPT"等请求。用户在 Overleaf 编译，只产出 .tex + figures/，不要附加 compile 脚本。
---

# chinese-ppt2

## 相对 chinese-ppt 的升级点（先读这一节）

本 skill 继承 chinese-ppt 的全部硬规则，并追加 7 项一级强规则。新规则均来自
实践中发现的排版问题与用户反馈，**不得关闭**。

### 升级 1 — 全局行距与段距（强制）

导言区必须包含：

```latex
\usepackage{enumitem}
\usepackage{etoolbox}

% 行距 1.3 + 段前/段后 3pt（对应 Word "多倍行距 1.3"）
\linespread{1.3}
\setlength{\parskip}{3pt plus 1pt minus 0pt}
\setlist[itemize]{topsep=3pt, itemsep=3pt, parsep=3pt, partopsep=0pt}
% enumerate 必须显式指定 label —— 否则 enumitem 继承的 \labelenumi 在
% ctex + fandol + beamer 下偶发自引用 (\labelenumi -> {\labelenumi)，
% 引爆 "TeX capacity exceeded, input stack size=10000"。
\setlist[enumerate,1]{label=\arabic*., topsep=3pt, itemsep=3pt, parsep=3pt, partopsep=0pt}
\setlist[enumerate,2]{label=(\alph*), topsep=2pt, itemsep=2pt}
\renewcommand{\labelenumi}{\arabic{enumi}.}

% 关键：固定几何环境（tabular / tikz）内部自动重置为 1.0 行距，
% 防全局 1.3 顶破 minimum height 节点与 tabular 行高。
% 这一对 hook 是升级 7 的首选实现，免去手工逐帧包装。
% 注意：不要在 hook 里加 \selectfont —— 在 ctex+fandol+beamer 下会触发
% 中文字体重载的递归，引发 "TeX capacity exceeded, input stack size=10000"。
% 省掉 \selectfont，linespread 的新值会在环境内下一次字体切换
% （\small / \scriptsize / \node 文本）时自然生效，对 tabular / tikzpicture
% 已足够；tabular 再叠加 \arraystretch=1.0 作为第二保险。
\AtBeginEnvironment{tabular}{\linespread{1.0}\renewcommand{\arraystretch}{1.0}}
\AtBeginEnvironment{tikzpicture}{\linespread{1.0}}
```

理由：PPT 正文过密会让观众读不完第一屏。1.3 行距 + 3pt 段距是 Word
学术排版的默认手感，也让 beamer 10pt 字体有呼吸空间。`\AtBeginEnvironment`
两行 hook 自动把 tabular 与 tikzpicture 的内容行距压回 1.0，避免图表因全局
1.3 越界（见升级 7）。

### 升级 2 — 帧内容行数预算（强制）

启用 `\linespread{1.3}` 后，每帧的可用行数（正文，不含标题、页脚）
**严格按下表上限**。超过 → 强制拆帧（见升级 3）。

| 帧类型 | 最多正文行数 | 备注 |
|---|---|---|
| 纯段落（§1 / §2） | **12 行** | 每段 2--3 句，不超 4 段 |
| 段落 + 列表 | **10 行** | 列表 ≤ 4 项 |
| 纯列表 | 列表 ≤ **4 顶层项**，每项 ≤ 2 行 | 嵌套 subitem ≤ 2 层 |
| 表格 + 讨论 | 表格 ≤ **6 中间行**，讨论 ≤ 2 行 | 超了拆讨论帧 + 表格帧 |
| 表格单帧 | 表格 ≤ **10 中间行** | 超了拆两张表 |

行数估算（重要）：

- 短项（一句半以内、无括号引用） ≈ **1.5 行**
- 中项（一个英文括号引用 `(Xxx, 20xx)` 或一句完整陈述） ≈ **2 行**
- 长项（2--3 个串联引用 `（A 等, 2022；B 等, 2023；C 等, 2024）` 或双分号
  的复合句） ≈ **3 行**
- 每段 2--3 句正文引子 ≈ **2 行**

写前先数：`3 长项 × 3 行 = 9 行` 已占满纯列表帧预算。
文献综述类（每条几乎都是长项）**再加引子就必超 10 行**，要么压引子、
要么按主线再拆。典型反例：一帧里塞 主线 A（2 长项）+ 主线 B（3 长项）
+ 两段引子 = 约 14--16 行，**必然越界**，应拆成主线 A 单帧 + 主线 B 单帧。

### 升级 3 — 越界时的"均分拆帧"策略（强制）

按溢出幅度分档处理。**优先级从上到下**：

| 溢出程度 | 首选做法 |
|---|---|
| 溢出 ≤ 1 行 | 帧内局部 `\setlist[itemize]{topsep=1pt, itemsep=1pt, parsep=1pt}`；必要时把一个长句拆短 |
| 溢出 2--4 行（不够撑满新帧） | **对半拆**：前帧只留一半内容，另一半到新帧，新帧用一段 2--3 句的承接话 + 结论扩展把空间填匀。不能前 90% 后 10% |
| 溢出 > 4 行 或 含表格 | 自然拆两帧，各自完整 |

#### 对半拆的具体做法（关键）

- **按概念维度拆**，不是按机械位置切一刀：
  - 4 个 bullet 的机制帧 → 拆成"(上) 披露 + 责任" / "(下) 认知 + 治理"，每帧 2 项
  - 2 个表格的变量定义帧 → 拆成"核心 X" / "控制 X_it"，各 1 表
  - 两条主线 + 交叉空白 → "(一) 两条主线" / "(二) 交叉空白 + 本文切入"
- **每个半帧补一段承接 / 小结**，避免稀疏：
  - 后帧开头：一句"X—Y 的外部压力继续传导到决策层："（衔接）
  - 后帧结尾：一句"机制推论：…"（把下沉的结论留给后帧）
- **命名约定**（任选其一，一份 deck 内统一）：
  - 序号式：`变量定义（二）` / `变量定义（三）`
  - 概念式：`机制（软实力）：披露与责任` / `机制（软实力）：认知与治理`
  - 上下式：`主要研究结论（上）` / `主要研究结论（下）`

**错误示例**（禁止）：

- 禁止前帧 5 条 bullet、后帧只有 1 条 bullet + 1 句话（后帧空虚）
- 禁止后帧完全是前帧的续写、没有独立的引子（观众看页码以为漏了内容）
- 禁止用 `\begin{frame}[allowframebreaks]` 自动分页（破坏手工设计的章节页码）

### 升级 4 — 禁止 AI 味表达（强制）

观众和导师一眼能识别"AI 写的"PPT。以下模式必须全部清除：

#### 4a. 结论前的标签式短语 → 改成自然句

| AI 味 | 自然表达 |
|---|---|
| `\textbf{关键比较：} ...的符号与显著性差异。` | `我们重点看 β₁ 与 β₂ 在符号和显著性上是否不同。` |
| `\textbf{理论映射：} 验证可观察性推论——...` | `这与前文的可观察性逻辑一致：...` |
| `\textbf{核心机制：} ...传导路径...` | `传导路径是这样的：...` |
| `\textbf{理论含义：} ...` | `这说明 ...` |
| `\textbf{政策含义：} ...` | `对政策制定者而言，...` |

规则：**不要以"关键 X：/ 理论 Y：/ 核心 Z："开头 + 冒号 + 一句话** 的三段式
模板写结论。直接用完整陈述句。

#### 4b. H1/H2/H3 假设后不加章节括号

- 错：`\textbf{H1（第四章·信号传递）：} HSGT 显著提升 GTFP。`
- 对：`\textbf{H1：} HSGT 显著提升 GTFP。`

章节归属在下面的 `\section{}` 和页脚 `\insertsectionhead` 已经显示，
在假设旁边再标一遍是 AI 的冗余模式。

#### 4c. 概念后不加"（xxx）"型自注释

- 错：`\textbf{政策窗口（样本中部）：}`
- 对：`\textbf{政策窗口：}`
- 错：`双碳目标（碳达峰 + 碳中和）`
- 对：`双碳目标 —— 碳达峰 + 碳中和`（用破折号自然衔接）

规则：如果括号内是对前面短语的**同义复述**，删；如果是**补充事实**
（人名、年份、缩写英文名），保留。

#### 4d. 结论 / 创新 / 建议页禁用 "F1 / F2 / F3" 编号前缀

主要研究结论、创新点、政策建议这类总结页，**不要在每个 bullet 前加
"F1：/ F2：/ C1：/ P1：/ 结论 1：/ 发现 1："之类的字母或数字编号前缀**。
这是 AI 模板的典型标记，很丑，观众一眼能识别。

| AI 味（禁） | 自然表达（对） |
|---|---|
| `\textbf{F1 主效应成立。} 绿色基金...` | `\textbf{主效应成立。} 绿色基金...` |
| `\textbf{F2：} 情境依赖明显...` | `\textbf{情境依赖明显。} ...` |
| `\textbf{C1 视角创新。} ...` | `\textbf{视角创新。} ...` |
| `\textbf{P1 顶层设计：} ...` | `\textbf{顶层设计。} ...` |
| `\textbf{结论 1：} ...` / `\textbf{发现 1：} ...` | `\textbf{...（自然短语）。} ...` |

规则：

- bullet 的序号已经由 `\begin{itemize}` / `\begin{enumerate}` 自动表达，
  **不要在正文里再手写 F1 / C1 / P1 / 发现 1 / 结论 1** 这类机械编号。
- 起始粗体只写**自然主语短语** + **句号 / 冒号**：如"主效应成立。"、
  "情境依赖明显。"、"视角创新。"、"顶层设计。"、"监督机制。"
- 创新点帧用 `\begin{enumerate}` 让 1. 2. 3. 自动编号，**不要** 再写
  `创新 1：` / `1. 视角创新：` —— 前者是 AI 模板，后者是重复编号。
- H1/H2/H3（研究假设）**可以**保留（它们是论文里的正式假设编号，读者
  有预期）；但**结论页对应假设时**用"主效应成立 / 转型驱动获验证"等
  自然短语，不要再出现"F1 / F2 / F3"这种并行编号。

### 升级 5 — CJK 空格与中点（·）严守规则

xeCJK 默认会对 CJK—Latin 过渡插入小空格；**不要在 CJK—CJK 之间人为加空格**。

#### 5a. 中文之间不能有空格

- 错：`我们 重点 看 两者 差异`
- 对：`我们重点看两者差异`
- 错：`中 · 英 混排`（中点两侧空格让视觉突兀）
- 对：`中·英混排` 或 `中、英混排`

#### 5b. 中点（`·`）使用规则

- 允许：frame 标题的视觉分层（`第五章 · 基准讨论：GII 主要在下游`）
- 允许：作者姓名缩写（`Fama · French`）
- 禁止：正文括号内当章节注脚（如 `（第四章 · 信号传递）`）
- 禁止：并列概念之间（改成 `、`、`+`、`/`）

#### 5c. 中英混排空格保留

`HSGT 显著提升 GTFP`、`N = 7{,}551`、`2012 年` 这类英文 / 数字两侧的空格
**不要去**，xeCJK 依赖它们正确排版。

### 升级 6 — 表格横向越界处理

4+ 列 + 长列头（"超效率 GTFP"、"非重污染子样本"）横向很容易越界。
首选做法：**组标题行 + `\multicolumn` + `\cmidrule`**，而不是把全部
文字塞进第二行：

```latex
\begin{tabular}{lcccc}
  \toprule
        & \multicolumn{2}{c}{超效率 GTFP} & \multicolumn{2}{c}{非重污染子样本} \\
  \cmidrule(lr){2-3} \cmidrule(lr){4-5}
        & (1) Preresi & (2) Presenti & (3) Preresi & (4) Presenti \\
  \midrule
  ...
\end{tabular}
```

配合 `\setlength{\tabcolsep}{4pt}` 与 `\small`。仍超再升级到 `\scriptsize`
或拆帧。

### 升级 7 — TikZ / 固定几何环境必须重置 `\linespread{1.0}`（强制）

**为什么会有这条规则。** 全局 `\linespread{1.3}`（升级 1）作用在任何会读
`\baselineskip` 的地方，包括：

- **TikZ 节点**里的 `\\` 换行 —— 节点内容按 1.3× 行高排版，撑破
  `minimum height` 设计的节点框，把整张画布顶进页脚；
- **tabular 的行高** —— 每行 `\\` 多占 30% 垂直空间，6 行的表变成 8 行的高；
- `\begin{center}` 的 `topsep` —— 画布整体向下偏移；
- `\includegraphics` 后 caption 的垂直间距；
- `\node` 文本与 `minipage` 里的 baseline。

这些都是按 **linespread=1.0 设计** 的固定几何元素。升级 1 的 1.3 只应该
作用在正文段落与列表项。

#### 首选实现：全局 hook（升级 1 已内置）

在导言区（升级 1 的配置块里）加：

```latex
\usepackage{etoolbox}
\AtBeginEnvironment{tabular}{\linespread{1.0}\renewcommand{\arraystretch}{1.0}}
\AtBeginEnvironment{tikzpicture}{\linespread{1.0}}
```

这两行让任何 `\begin{tabular}...\end{tabular}` 和 `\begin{tikzpicture}...`
在进入时自动把行距压回 1.0，免去逐帧手工包装。**这是 chinese-ppt2 的默认
方案**。

#### ⚠ 不要在 hook 里加 `\selectfont`（实战教训）

早期版本的 hook 是 `\linespread{1.0}\selectfont`。**实测在 ctex + fandol +
beamer 组合下会触发 "TeX capacity exceeded, input stack size=10000" 编译
失败。** 原因是 `\selectfont` 在 tabular / tikzpicture 起始位置触发中文
字体重载，而 fandol 的字体表在 beamer frame 的 overlay 上下文里会与
hook 形成内部递归，push 到输入栈深度上限。

修复：**去掉 `\selectfont`**。`\linespread{1.0}` 单独使用时，新 baseline
不会立刻生效，但环境内部下一次 `\small` / `\scriptsize` / TikZ `\node`
文本都会触发隐式 selectfont，把新 linespread 应用到后续内容，对
tabular 行高与 tikz 节点内容已足够。`tabular` 再叠加 `\arraystretch=1.0`
做第二保险，覆盖那些 baseline 来不及更新的边缘场景。

自检：

```bash
grep -n 'AtBeginEnvironment{tabular}{\\\\linespread{1.0}\\\\selectfont' report.tex
grep -n 'AtBeginEnvironment{tikzpicture}{\\\\linespread{1.0}\\\\selectfont' report.tex
# 命中任何一行说明用了老版本 hook，必须删掉 \selectfont
```

#### ⚠ enumerate 必须显式指定 label（实战教训 2）

只写 `\setlist[enumerate]{topsep=3pt, itemsep=3pt, parsep=3pt, partopsep=0pt}`
不设 `label=...` 时，enumerate 帧会在 ctex + fandol + beamer 下偶发
编译失败，错误信息：

```
TeX capacity exceeded, sorry [input stack size=10000].
\labelenumi ->{\labelenumi
1.806 \end{frame}
```

`\labelenumi -> {\labelenumi` 是自引用——说明 enumitem 继承的 `\labelenumi`
在 ctex 初始化过程中被污染成递归定义，enumerate 帧展开时无限深度递归。

**修复**：在 `\setlist[enumerate,N]` 里\textbf{显式给出 `label=...`}，
并在导言区显式 renewcommand `\labelenumi` 截断递归：

```latex
\setlist[enumerate,1]{label=\arabic*., topsep=3pt, itemsep=3pt, parsep=3pt, partopsep=0pt}
\setlist[enumerate,2]{label=(\alph*), topsep=2pt, itemsep=2pt}
\renewcommand{\labelenumi}{\arabic{enumi}.}
```

不需要在 itemize 上做这个——itemize 的 `\labelitemi` 是 itemize 专用，
不走 enumi 那条被污染的路径。

自检：

```bash
grep -n 'setlist\[enumerate\]{' report.tex  # 命中说明没带 ",1" + label=，必须改
grep -n 'setlist\[enumerate,1\]{label=' report.tex  # 必须 >= 1
```

#### 不要在 hook 已生效时再手工包装（实战教训 3）

早期版本建议"hook + 手工 `{\linespread{1.0}\selectfont ... }` 双保险"。
**实测证明这会触发 TikZ 整帧变白**（X→M→Y 框架帧编译后空白）。怀疑原因：

- `\selectfont` 在 frame body 开头触发时，beamer 还在做 frame 初始化，
  字体状态未就绪；
- 外层 `{...}` 与 `\begin{center}` 嵌套后，TikZ 的 `remember picture`
  overlay 坐标锚点错位；
- 或者 `\selectfont` 与 `\AtBeginEnvironment` 注入的 `\selectfont` 在
  TikZ 节点字体切换时互相抵消。

**规则**：全局 hook 已经处理好 tabular / tikzpicture 内部行距，**不要** 在
frame body 再包一层 `{\linespread{1.0}\selectfont ... }`。如果外层的
`\begin{center}` 或 `\vspace` 让画布偏下，用 `\vspace*{-0.4em}` ~ 
`\vspace*{-0.8em}` 向上微调，不要动 linespread。

#### 不要用的做法

- **不要** 在已有全局 hook 的前提下，再手工 `{\linespread{1.0}\selectfont ...}`
  包装 frame body —— 实测会把整帧编译成空白。
- 不要尝试给 `\linespread` 设条件分支（如用 `\ifx` 判断环境）——不可靠。
- 不要去掉全局 `\linespread{1.3}`（升级 1 是强制的）。
- 不要用 `\setstretch{1.0}` 覆盖（效果等价但需要 `setspace` 包，额外依赖）。
- 不要只包 `\begin{tikzpicture}` —— 外层 `\begin{center}` 的 `\topsep`
  还是按 1.3 算。**要么用 hook，要么包整个 frame body**。

#### 检测（retrofit 时）

确保导言区有 `\AtBeginEnvironment{tabular}` 和 `\AtBeginEnvironment{tikzpicture}`
两条 hook：

```bash
grep -c 'AtBeginEnvironment{tabular}' defense.tex   # 应该 = 1
grep -c 'AtBeginEnvironment{tikzpicture}' defense.tex  # 应该 = 1
```

若缺失，按"首选实现"补上。补完后只有大型 TikZ 诊断帧（例如 X→M→Y 框架图）
需要手工再加 frame body wrapper —— 通常就 1 张。

### 升级 8 — §7 必须包含"政策建议"帧（强制）

中文学术 PPT 的 §7 不能只有"研究结论"和"研究不足"。中文学术传统
（答辩、学术会议、组会汇报）对 §7 的预期结构里，\textbf{政策建议 /
实践启示}是必备环节——导师和听众会主动寻找"这项研究对政策 / 实践有
什么用"。缺失会被直接追问。

#### 强制结构

§7 至少按此顺序包含以下 4 类帧：

1. **主要研究结论**（1 帧）—— 对照 H1/H2/H3 逐条收束，用自然短语起头
   （见升级 4d），\textbf{不要用 F1 / F2 编号}。
2. **主要创新点**（1 帧）—— 视角 / 方法 / 结论三选一到三，用 `enumerate`
   自动编号。
3. **政策建议 / 实践启示**（\textbf{1--2 帧，必填}）—— 分层给出具体
   可操作的建议。超过 10 行按升级 3 对半拆（上 / 下）。
4. **研究不足与未来展望**（1 帧）—— 样本、变量、机制、外部推广。

常见的"政策建议"对半拆法：

- "顶层设计 + 转型机制" 为一帧；
- "监督机制 + 差异化配套" 为一帧。

#### 政策建议的写法

- **以实施主体为锚点**（监管部门 / 行业协会 / 企业管理层 / 金融机构 /
  学界），不要以"第一、第二、第三"或"P1 / P2"开头。
- **每条 = 对象 + 动作 + 抓手**，避免空洞的"加强、完善、促进"：
  - 错：`完善绿色基金监管体系。`
  - 对：`监管部门应制定统一的绿色基金认定标准，区分泛 ESG 基金与
    绿色专项基金，并将该分类写入基金募集说明书的披露要求。`
- **每条建议对应一个具体实证发现**（主效应 → 顶层设计；异质性 → 差异化
  配套；机制 → 治理与披露），不要脱离论文自创建议。
- 帧标题允许"政策建议（上）/ 政策建议（下）"或"政策建议：顶层设计与
  转型机制"这类概念式命名。

#### 政策建议帧的排版（严格列表化，不用连续段落）

政策建议帧\textbf{必须用 `itemize` 结构}，不要写成 3 段 3--4 行的粗体
段落——在 1.3 行距 + 3pt 段距下，3 段段落式写法几乎必然顶破页脚，
导致后面的帧被挤到下一页编译失败，表现为\textbf{页码停留在政策建议
帧的前一页，后续帧不出现在 PDF 中}。

**正确写法**（列表化、每条 1--2 行、帧正文总行数 ≤ 10）：

```latex
\begin{frame}{政策建议：顶层设计与转型机制}
  \textbf{监管部门。}
  \begin{itemize}
    \item 制定统一的绿色基金认定标准，写入基金募集说明书披露要求；
    \item 区分泛 ESG 基金与绿色专项基金，明确运作边界；
    \item 按区域经济水平推行差异化监管策略。
  \end{itemize}
  \textbf{基金管理人。}
  \begin{itemize}
    \item 重点支持原创性、突破性绿色发明专利研发；
    \item 将绿色责任履行水平纳入投资评价与绩效考核。
  \end{itemize}
\end{frame}
```

**错误写法**（连续段落 + 粗体引导 + 每段 3--4 行）：

```latex
% 反例：实测会在编译时把后续帧挤丢
\begin{frame}{政策建议（上）}
  \textbf{顶层设计。} 建议由官方对"绿色基金"作出明确定义……（3 行）

  \textbf{转型机制。} 鼓励绿色基金重点支持……（3 行）

  将\textbf{绿色责任履行水平}纳入……（3 行）
\end{frame}
```

行数预算：政策建议帧正文 **≤ 10 行**（含列表分隔）。超了就按升级 3
对半拆成"政策建议（上）/（下）"。

#### 自检

```bash
grep -c '政策建议\|实践启示' report.tex   # 必须 >= 1
```

若 §7 内无任何政策建议类帧，视为\textbf{结构性缺失}，必须补齐。

### 升级 9 — 帧标题禁用"（一）（二）（三）"数字 / 汉字序号前缀（强制）

帧标题\textbf{不要}用"（一）（二）（三）（四）"或"（1）（2）（3）"
这类机械顺序号来区分同一主题的多张帧。序号由帧顺序与目录页自动表达，
观众不需要再看数字才能理解帧间关系。序号前缀也是 AI 模板的强标记。

- 错：`研究背景（一）：双碳战略` / `研究背景（二）：融资困境` / `研究背景（三）：已有研究` / `研究背景（四）：制度窗口`
- 对：`研究背景：双碳战略与新质生产力` / `研究背景：绿色转型的融资困境` / `研究背景：绿色金融工具版图` / `研究背景：绿色基金的制度窗口`

**规则**：

- 同主题的多帧用\textbf{"主题：核心概念"结构}区分，由冒号后的概念名
  表达差异，不要用数字 / 汉字序号。
- 理论基础分多帧时，用概念副题（如"理论基础：代理视角——漂绿与私利
  的双重遏制"）或括号点明视角（"理论基础（代理视角）"），但\textbf{不
  要用"理论基础（一）（二）（三）"}。
- **允许的例外**：`主要研究结论（上）/（下）`、`政策建议（上）/（下）`
  这类\textbf{对半拆帧}的命名约定（见升级 3）—— 它们表达的是"同一帧被
  拆成两页"，不是"多个平行主题的顺序编号"，语义不同，允许保留。

自检：

```bash
grep -nE '\\begin\{frame\}\{[^}]*（[一二三四五六七八九十0-9]+）' report.tex
```

命中行逐一改写为概念式标题。

### 升级 10 — 章节顺序：文献必须在 X→M→Y 框架之前（强制）

X→M→Y 框架图是对\textbf{研究假设}的图示化总结，应当出现在读者已经
看过文献综述、理论基础、假设之后，而不是抢在文献综述之前。

**强制顺序**：

- §1 **只放** "研究背景帧 × N + 研究问题帧"（**不放**框架图）；
- §2 按此顺序：
  1. 文献综述（主线 / 缺口）
  2. 理论基础（至少 2 帧，见升级 11）
  3. 研究假设（H1/H2/H3）
  4. **X→M→Y 研究框架帧**（放在 §2 末尾）。

早期 chinese-ppt 模板把框架图放在 §1 研究问题之后，是一个应当纠正的
历史设计。在 chinese-ppt2 中，框架图一律进入 §2 末尾。

理由：观众在看到 X→M→Y 图之前，应当先理解"为什么是这些 X、这些 M、
这些 Y"——这需要文献缺口与理论基础铺垫。框架图抢在文献之前会让观众
误以为这是一项\textbf{事先假定好结构}的论证，而不是\textbf{从理论
推出}的框架。

### 升级 10.5 — 页脚只显示 `\insertframenumber`，不要用 "X / N" 格式（强制）

页脚\textbf{不要写}成 `\insertframenumber\,/\,\inserttotalframenumber`。
`\inserttotalframenumber` 在 ctex + fandol + beamer 组合下会\textbf{偶发
返回诡异值}——实测观察到 34 帧的 deck 在页脚输出 `32 / 80` 这样的奇怪
分母（真实总数 34，aux 文件里写入了一个毫无根据的 80）。原因可能与
以下因素有关：

- beamer 的 `\c@framenumber` 计数器在 `AtBeginEnvironment{tabular}` /
  `{tikzpicture}` hook 叠加时被污染；
- ctex 的中文章节注入机制与 `\beamer@inserttotalframenumber` 的 aux
  写入时机冲突；
- 编译轮次不足时 aux 缓存的陈旧值被直接读取。

无论根因，**最稳的做法是放弃分母，直接只显示当前帧号**。观众并不需要
"X / 总数"就能理解进度，目录页已经给出了整体结构。

**正确写法**：

```latex
\raggedleft{\color{cufenavy}\footnotesize%
  \insertframenumber}
```

**禁止写法**：

```latex
\raggedleft{\color{cufenavy}\footnotesize%
  \insertframenumber\,/\,\inserttotalframenumber}  % ← 会输出 "X / 80"
```

自检：

```bash
grep -n 'inserttotalframenumber' report.tex  # 必须为空
```

### 升级 11 — §2 理论基础必须具体详细（最少 2 帧）

理论基础\textbf{不能压成 1 帧大概念综述}。把两条理论视角（代理 /
融资 / 契约 / 信号 / 委托代理 / ...）合在一帧里各写 2--3 句话，观众
会感觉"理论没讲清楚"。中文答辩和学术会议对理论部分的详细度要求明显
高于英文 seminar。

**强制结构**：

- §2 理论基础\textbf{最少 2 帧}，每帧聚焦一条理论视角；
- 视角丰富的论文（≥ 3 条视角）可扩展到 3 帧，并可加 1 帧"理论整合 /
  逻辑之变"作收束；
- 每帧\textbf{必须包含}：
  1. **视角名称**（帧标题或首行粗体）；
  2. **核心文献引用**（2--3 篇代表文献）；
  3. **该视角下 X → Y 的具体传导链**（2--4 条，每条 1--2 行）；
  4. **可观察预期 / 落地到 H 的映射**（一句话）。

**禁止**：

- 禁：一帧内把代理视角 + 融资视角压成两段 3 行的段落；
- 禁：只讲"绿色基金可以缓解融资约束、提升企业治理"这种无具体传导
  链的高度抽象话；
- 禁：不引用具体文献的纯宏大叙事（"基于委托代理理论，……"后面
  没引就停）。

时长调节：§2 帧数表（升级自 chinese-ppt）是\textbf{下限}；理论视角
多的论文可上浮 2--3 帧而不违反规则。

---

## 以下内容继承自 chinese-ppt（原硬规则全部保留）

## 用途

生成 **可直接在 Overleaf 编译的中文 Beamer PPT**，适用于：

- 博士 / 硕士学位论文答辩
- 中文学术会议 / 研讨会汇报
- 课题汇报、开题答辩、中期答辩

输出 **确定性**：同一篇论文 + 同一时长 ⇒ 同一套 PPT。

## 何时调用

- "做一份中文 PPT / Beamer"（新版）
- "中文 Beamer 改进版 / chinese-ppt2"
- "答辩 PPT 排版优化 / 防越界"
- "Retrofit 已有 chinese-ppt deck 到新版规范"
- 任何"做中文学术 PPT"类请求，默认优先 chinese-ppt2

## 输出规则

**只交付 `.tex` + `figures/` 文件夹**，不写 `compile.bat` / `Makefile` /
`latexmkrc` 等本地编译脚本——用户在 **Overleaf** 编译（compiler 必须设为
**XeLaTeX**，需连续编译两次让目录页对齐）。

## 硬规则（不得偏离）

1. **引擎锁定**：`xelatex`（两次编译），禁止 `pdflatex`。
2. **字体锁定**：`\usepackage[UTF8,fontset=fandol]{ctex}`。
3. **主题锁定**：`\usetheme{default} + \useinnertheme{circles}` + 自建 CUFE
   金融学院模板。
4. **宽高比锁定**：`aspectratio=169, 10pt`。
5. **色板锁定**：

   ```latex
   \definecolor{cufenavy}{HTML}{1F3A60}
   \definecolor{cufetext}{HTML}{2A2A2A}
   \definecolor{cuferule}{HTML}{7F8FAA}
   ```

6. **框架样式锁定**：

   - 顶部 0.15cm 深蓝色窄带
   - 右上角小 logo，`anchor=east, yshift=-0.70cm`
   - 帧标题 TikZ 绝对定位：`anchor=north west, xshift=0.40cm, yshift=-0.50cm`
   - 帧标题 `text width=\paperwidth-5.0cm`，字号 `\large`，颜色 `cufetext`
   - 帧标题模板末尾 `\vspace*{0.55cm}`（不是 1.35cm）
   - 页脚：左 `\insertsectionhead` + 右 页码
   - 左下角不放东西

7. **7 章节大纲锁定**：

   | # | 章节名（默认） |
   |---|---|
   | 1 | 研究背景与问题 |
   | 2 | 文献综述与理论基础 |
   | 3 | 数据与变量 |
   | 4 | [第四章实证标题] |
   | 5 | [第五章实证标题] |
   | 6 | [第六章实证标题] |
   | 7 | 三章综合对比与研究结论 |

8. **X→M→Y 框架帧必填**（§1 内）。

9. **所有回归表 Control Yes/No 格式**，底部 `Controls / Firm FE /
   行业×年份 FE / N / Adj.R²`，星号 `***/**/*`。

10. **每个实证结果 = 讨论帧 + 表格帧 二元对**。例外：小表合并单帧。

11. **每个异质性维度 = 1 帧**，按概念维度归并指标。

12. **每个机制通道 = 1 对帧**（讨论+表，或合并）。讨论侧 > 12 行按升级 3 拆。

13. **每个进一步分析 = 1 对帧**，不得合并缩水。

14. **标题页格式**：大 logo 左上、主标题深蓝加粗、副标题斜体、底部日期。

15. **致谢页格式**：正中"敬请各位老师批评指正！" + `Thank You \& Q\,\&\,A`。

16. **目录页**：footline 局部覆盖为空；`\linespread{1.15}\selectfont` 把
    1.3 全局行距在目录页临时压回，防 7 条目溢出。

17. **无 emoji / 无图标 / 无 tcolorbox / 无 `\begin{block}`**（除研究
    问题帧"核心问题"块）。

18. **数值必须真实或标 `[TODO 0.xxx]`**。禁用占位符。

19. **每张从 PDF 提取的图必须插入**（零孤儿）。

20. **图片尺寸锁定**：全屏 `height=0.62\textheight`，双栏 `0.55\textheight`，
    本模板默认 `0.50--0.55\textheight`。

21. **表格列标题必须两行**：第一行 `(1)(2)(3)`，第二行标签；4+ 列用
    multicolumn 组标题（见升级 6）。

22. **中文帧标题禁止 math mode**：`$\times$` → `×`，`$\to$` → `→`，
    `$\Rightarrow$` → `⇒`，`$+$` → `+`。表格内的 math 不受限。

23. **标点符号**：中文内容全角，表格内数字英文半角。

## 输入收集（一次性问全）

1. 论文标题
2. 答辩人 / 作者
3. 指导教师（1--2 人）
4. 机构（默认"中央财经大学金融学院"）
5. 场合（默认"博士学位论文答辩 · 20XX"）
6. 时长（分钟）— 20 / 25 / 30 / 35 / 40 / 45 / 60 / 90
7. 研究问题
8. X 和 Y
9. 机制通道 M
10. 异质性维度
11. 进一步分析 / 扩展
12. 样本区间与来源
13. 输出目录

若用户提供 PDF/docx，**先读论文**自动提取 7--12。

## 时长调节

| 时长 | §1 背景帧 | §2 文献+理论帧 |
|---|---|---|
| 20 min | 2 | 2 |
| 25 min | 3 | 2 |
| 30 min | 4 | 3 |
| 35 min | 5 | 3 |
| 40 min | 5 | 4 |
| 45 min | 6 | 4 |
| 60 min | 7 | 5 |
| 90 min | 8 | 6 |

§3--§7 不随时长变化。

## 前置章节（§1 § 2）必须用段落文字

每帧 2--4 段完整段落，每段 2--3 句、约 30--50 字，关键词用 `\textbf{}` 粗体。
禁止纯项目符号。升级 2 的 12 行预算仍然生效。

## 生成前的自检流程（新增）

写完每一帧，在标记为"最终"之前，按顺序做 9 项检查：

1. **行数估算**：对照升级 2 的表，超了就按升级 3 拆。政策建议帧尤需
   严格对照升级 8 的列表化写法，正文 ≤ 10 行。
2. **AI 味扫描**：`grep '关键比较：\|理论映射：\|核心机制：\|理论含义：\|政策含义：'` —— 命中改写。
3. **章节括号扫描**：`grep '（第[四五六七]章\|（跨章'`（非 `\section` 行）—— 命中删除。
4. **CJK 空格 / 中点扫描**：正文行内 ` · `、两个中文字之间的空格 —— 命中调整。
5. **编号前缀扫描（升级 4d）**：`grep -nE '\\textbf\{(F[0-9]|C[0-9]|P[0-9]|结论 ?[0-9]|发现 ?[0-9]|观察 ?[0-9])'`
   —— 命中删除机械编号，改成自然短语。
6. **政策建议存在性（升级 8）**：`grep -c '政策建议\|实践启示'` 必须 ≥ 1；
   若为 0，§7 缺失政策建议帧，按升级 8 补齐。
7. **政策建议排版检查（升级 8）**：政策建议帧正文必须是 `itemize` 结构，
   不能是 3 段连续粗体引导段落。若看到 `\textbf{...。} ...\n\n\textbf{...。} ...`
   这种三段式，改为列表。
8. **帧标题序号前缀（升级 9）**：`grep -nE '\\begin\{frame\}\{[^}]*（[一二三四五六七八九十0-9]+）'`
   —— 命中行除"（上）/（下）"外全部改为概念式标题。
9. **章节顺序（升级 10）**：§1 最后一帧必须是"研究问题"类，不是
   X→M→Y 框架帧；X→M→Y 框架帧必须出现在 §2 的最末尾（在理论与假设之后）。
10. **页脚格式（升级 10.5）**：`grep -n 'inserttotalframenumber' report.tex`
   必须为空；页脚只显示 `\insertframenumber`。

对已有 deck 做 retrofit 时，按页号扫编译输出的 PDF，重复上述 4 项 + 越界检查
（PyMuPDF 提取每页文本 line，过滤掉 y ≈ 249 的 footer 行后，看 y1 是否 > 239
或 x1 是否 > 450）。

### 越界检测脚本模板

```python
import fitz
doc = fitz.open('defense.pdf')
W, H = 453.54, 255.12  # 16:9 beamer page
def is_footer(bbox):
    x0, y0, x1, y1 = bbox
    return 239 < y0 < 250 and (x0 < 70 or x0 > 400)

for i, page in enumerate(doc):
    d = page.get_text('dict')
    crowd = h_over = None
    for b in d['blocks']:
        if 'lines' not in b: continue
        for line in b['lines']:
            bbox = line['bbox']
            if is_footer(bbox): continue
            if bbox[3] > 239 and not crowd: crowd = bbox[3]
            if bbox[2] > 450 and not h_over: h_over = bbox[2]
    if crowd or h_over:
        print(f'Page {i+1}: crowd={crowd} h_over={h_over}')
```

## 框架帧（X→M→Y）锁定模板

§1 内，放在研究问题帧之后。参考 chinese-ppt 的三类 X / 六通道 M / 单 Y 模板，
本 skill 不变动。

## 表格格式自适应

### 自适应项

1. 括号内容：SE 或 t，论文用什么就写什么。
2. 固定效应行：用论文实际结构。
3. 第二行列标签：用论文实际变量或分组。

### 不变项

- 第一行永远 `(1)(2)(3)`。
- 底部永远 `Controls / FE行 / N / Adj.R²`。
- 星号永远 `***/**/*`。

### 宽表处理

6+ 列：`\centering\scriptsize + \setlength{\tabcolsep}{3.5pt}`；
4+ 列长列头：升级 6 的 multicolumn 组标题。

## 数值提取与填充

PyMuPDF + 正则扫 `Table N` 和 `\d\.\d{3,4}\*{1,3}`，直接填 `.tex`。
`grep -c '[TODO 0' .tex` 必须为 0。

## 图片提取

PyMuPDF `page.get_images(full=True)` 提取到 `<outdir>/figures/`：

| 论文图类型 | 文件名 |
|---|---|
| 框架图 | `fig_framework.png` |
| 平行趋势 | `fig_ch4_parallel.png` |
| PSM 平衡 | `fig_ch4_psm.png` |
| CSDID 事件研究 | `fig_ch4_csdid.png` |
| 安慰剂检验 | `fig_chN_placebo.png` |
| CNKI 趋势 | `fig_cnki_trend.png` |

验证：每张 `figures/*.png` 在 `.tex` 中出现至少一次；零孤儿。

## 交付清单（必报）

```
生成文件：<path>/defense.tex
时长：<N> min
总帧数：<count>

排版检查（chinese-ppt2 新增）：
  \linespread 1.3：已启用
  parskip 3pt：已启用
  enumitem 列表间距：已配置
  行数预算超标帧：0
  AI 味短语（关键比较：/理论映射：...）：0
  章节括号注释（（第 N 章·XX））：0
  CJK—CJK 空格：0
  PDF 越界页（y>239 / x>450）：0

数值覆盖率：
  带真实系数的表格：X / Y
  [TODO 0 剩余：0
  占位符检查：0

图片处理：
  从 PDF 提取：N 张
  已插入 .tex：N 张
  尺寸：0.62 / 0.55 / 0.50 \textheight

帧清单：
  §1 研究背景与问题：X 帧
  §2 文献综述与理论基础：X 帧
  §3 数据与变量：X 帧
  §4--§6 实证：各 X 帧
  §7 三章综合对比与研究结论：X 帧

Overleaf 编译：
  1. 新建 Blank Project
  2. 上传 defense.tex + figures/
  3. Settings → Compiler → XeLaTeX
  4. Recompile × 2
```

## 工作流（新建 deck）

1. 读本 `SKILL.md` 和 `templates/empirical_paper_cn.tex`。
2. 若用户提供 PDF/docx，先读论文提取 X、Y、机制、异质性、进一步分析、
   基准系数、样本量。
3. 一次性询问缺失的输入项。
4. 按时长表确定 §1/§2 帧数。
5. 按论文实际展开 §4/§5/§6。
6. **按升级 2 的行数预算逐帧估行数**；预判要拆的帧，按升级 3 均分拆。
7. **按升级 4 审查每一帧**：无"关键比较 / 理论映射"标签，无章节括号注释。
8. **按升级 5 扫空格与中点**。
9. **升级 1 的导言区配置写入**。
10. 复制模板 + 填充 + 图像提取 + 系数填充。
11. 编译前做自检 4 项 + 越界检测脚本。
12. 输出交付清单。
13. 不生成 compile 脚本——用户在 Overleaf 编译。

## 工作流（retrofit 已有 chinese-ppt 的 deck）

对已经存在的 chinese-ppt 生成的 `defense.tex`：

1. **注入导言**：加 `\usepackage{enumitem}`、`\linespread{1.3}`、
   `\setlength{\parskip}{3pt...}`、`\setlist[...]`。
2. **扫 AI 味**：
   ```bash
   grep -n '关键比较：\|理论映射：\|核心机制：\|理论含义：\|政策含义：' defense.tex
   ```
   每一条改写成自然句。
3. **扫章节括号**：
   ```bash
   grep -n '（第[四五六七]章\|（跨章' defense.tex
   ```
   出现在非 `\section` 行的全部删除。
4. **编译、用 PyMuPDF 扫每页**（见上方检测脚本）。
5. **按升级 3 分级处理**：
   - 溢出 ≤ 1 行：帧内 `\setlist[itemize]{topsep=1pt,itemsep=1pt,parsep=1pt}`
   - 溢出 2--4 行：按概念对半拆帧（见升级 3 的对半拆做法）
   - 溢出 > 4 行或含表：自然拆两帧
6. **再编译、再扫**，收敛到 0 越界。
7. **注意目录页**：加 `\linespread{1.15}\selectfont` 局部覆盖，
   防 7 条目在 1.3 行距下溢出。

## 为何锁定这些约束

继承 chinese-ppt 的全部理由，并追加：

- **行距 1.3 + 段距 3pt** —— 用户反馈："行间距：多倍行距 1.3，段前 3 磅，
  段后 3 磅"（Word 标准学术排版手感）。
- **越界均分拆帧** —— 用户反馈："只超出一点点就另起一页，但这一点点也
  到不了一页，是否可以前面这一页拿出一半"。
- **禁 AI 味短语** —— 用户反馈："关键比较和理论映射，这两个东西就很像是
  AI 写的"。
- **禁章节括号注释** —— 用户反馈："研究假设提出，后面别加括号"。
- **CJK 中点空格** —— 用户反馈："中间空格显得很突兀"。

## 文件

```
chinese-ppt2/
├── SKILL.md                          # 本文件
└── templates/
    ├── empirical_paper_cn.tex        # 模板 .tex（含占位符）
    └── figures/
        ├── logo_cufe_full.png
        └── logo_cufe_small.png
```

模板复用 chinese-ppt 的 templates（本 skill 复制了一份）。
后续迭代可以在模板 .tex 里直接写死升级 1 的导言区配置。
