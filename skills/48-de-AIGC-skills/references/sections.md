# 分章节差异化改写策略 · Section-by-section strategies

不同章节的 AI 痕迹表现不同，修复力度也应不同。**方法章节的"AI 味"其实是学术规范；文献综述的"AI 味"才是真的失真**。

本文件的症状描述以中文稿为主；英文稿的逐节对照见文末
[English-manuscript notes](#english-manuscript-notes)，两套规则号
（`patterns-zh.md` 的 ZH01–ZH17 与 `patterns-en.md` 的 EN01–EN22）在同一张
章节表上通用——同一章节在两种语言里的高危程度是一致的。

---

## 总览表

| 章节 | AI 风险等级 | 主要改写策略 | 保留要素 |
|------|-----------|------------|---------|
| 摘要 | 🔴 极高 | 大幅重写，注入具体数据 | 核心发现、研究对象 |
| 引言 | 🔴 极高 | 重构开头，加入真实文献张力 | 研究问题、贡献声明 |
| 文献综述 | 🔴 极高 | 彻底重写，补充具体作者+年份 | 文献脉络、分歧点 |
| 研究假设 | 🟡 中 | 注入 hedge，降级绝对断言 | 理论基础、假设逻辑 |
| 数据来源 | 🟢 低 | 细化具体步骤 | 数据源、样本期、清洗规则 |
| 计量模型 | 🟢 低 | 删除冗余虚词 | 模型形式、变量定义 |
| 基准结果 | 🟡 中 | 具体化数字、降级断言 | 系数、显著性水平 |
| 机制分析 | 🟡 中 | 打破总分总结构 | 机制链条、中介变量 |
| 异质性 | 🟡 中 | 制造句长方差 | 分组方式、系数差异 |
| 稳健性 | 🟢 低 | 每个检验对应一个担忧 | 检验方法、结果方向 |
| 讨论 | 🔴 极高 | 大幅重写，注入谨慎性 | 发现的意义、局限 |
| 结论 | 🔴 极高 | 避免回音壁，引入新信息 | 研究贡献、未来方向 |

---

## 章节细则

### 1. 摘要（Abstract）

**AI 典型症状**：
- 开头"本研究..."或"本文..."
- 中间全是"深入探讨/全面分析/系统研究"
- 末尾"具有重要的理论意义和实践价值"

**改写红线**：
- 字数控制在 200-300 字（中文）/ 150-250 词（英文）
- **必须包含 3 个具体数字**：样本量、时间窗口、关键系数
- **必须包含 1 个具体文献回应**："与 Smith (2020) 的结论一致/不一致"
- **必须去掉所有**"深远影响/重要意义/有益参考"类空话

**骨架模板**（参考用，不是直接套）：
```
[研究问题一句话] — [方法一句话] — [数据一句话，含样本量和时间窗口] —
[主要发现一句话，含具体系数] — [机制一句话] — [文献对话一句话] —
[边际贡献一句话]
```

---

### 2. 引言（Introduction）

**AI 典型症状**：
- 开头"近年来，XXX 受到广泛关注"
- 中间"相关研究主要从三个方面..."
- 结尾"本文的创新点主要体现在以下三个方面"

**改写红线**：
- **禁止**用"近年来"/"随着...的发展"开头
- **必须**以具体事件/数据/文献争论开头（如案例 2 的 AlphaGo 开场）
- 贡献声明**不要编号列出**三点，而是用段落陈述式写法，突出**相对现有文献的边际改进点**
- 文献引用**精确到作者+年份**，不用"相关研究"

**经济学顶刊常见引言套路**：
1. **争论性问题**："X 和 Y 的关系在文献中仍有争议"
2. **识别困难**："既有研究难以识别 X→Y 的因果，因为..."
3. **本文对策**："我们利用 [具体制度变化/自然实验] 克服了这一困难"
4. **主要发现**：具体数字
5. **边际贡献**：相对现有文献的两三点改进

---

### 3. 文献综述（Literature Review）

**AI 典型症状**：
- "首先...其次...再次...最后..."
- "部分学者认为...另一些学者则认为..."（不给具体作者）
- 每个观点都用"具有重要意义"结尾

**改写红线**：
- **每条观点必须跟至少 1 位具体作者和年份**
- **必须承认分歧**：如果两派观点都有，写出来；不要粉饰共识
- **不同意见的取舍**："Smith (2020) 认为 X，但我们用 [更新/更大/不同] 数据发现 Y"
- 文献综述的末段应**指出研究 gap**——但不要用"空白"这种词，改为"尚未被系统检验"或"既有研究的样本局限在..."

---

### 4. 研究假设（Hypotheses）

**AI 典型症状**：
- "基于上述分析，本文提出以下假设"
- 假设措辞："A 能够显著促进 B"

**改写红线**：
- 假设措辞用 hedge：用"A 对 B 有正向影响"或"在控制 X 后，A 与 B 正相关"
- **避免**用"能够"/"显著"——这些词会在结果段再出现，此时出现属于先入为主
- 如果有多个假设，**不必**编号为 H1/H2/H3，可以用段落陈述（看具体期刊风格）

---

### 5. 数据来源（Data）

**AI 典型症状**：
- "数据来源于：A、B、C、D 等权威数据库"
- "经过严格的整理、筛选、匹配、清洗"

**改写红线**：
- **每个数据源单独一句说明**：来源 + 变量 + 时间窗口
- **清洗步骤列具体规则**：剔除 ST 样本、缩尾 1%、按行业聚类——而不是"严格清洗"
- 如果样本期选择有政策理由，**必须说明**（如"2015 年政策试点为起点"）

---

### 6. 计量模型（Model）

**AI 典型症状**：
- "对于本文而言，由于...故而..."
- "在此基础上，以 Y 为被解释变量..."

**改写红线**：
- **禁用**"对于...而言"/"由于...故而"/"在此基础上"
- 直接写方程：`$Y_{it} = \alpha + \beta X_{it} + \gamma Z_{it} + \mu_i + \lambda_t + \varepsilon_{it}$`
- 每个变量下面一句话说明：`$X_{it}$` 是数字化转型指数...
- 估计策略说明**为什么用这个方法**：OLS、IV、DID、PSM 的选择理由

---

### 7. 基准结果（Baseline Results）

**AI 典型症状**：
- "由表 X 可以看出，系数非常显著为正"
- "这充分证明了..."

**改写红线**：
- **不说**"非常/极其/显著"的主观形容词，直接给 t 值、系数、置信区间
- 描述顺序：列 (1) 不加控制变量 → 逐步加控制变量 → 系数稳定性
- **禁用**"证明了"/"充分说明"，改为"与 H1 的预期方向一致"或"为 X 提供了证据"

---

### 8. 机制分析（Mechanism）

**AI 典型症状**：
- "首先...其次...因此..."的线性推演
- 每段末尾重复段首论点

**改写红线**：
- 用**问句**开启机制段：如"基准结果背后是什么机制在驱动？"
- 每个机制路径给**具体中介变量**和**统计量**
- 报告**中介效应占比**（如"这条路径解释了基准系数的 37%"）

---

### 9. 异质性（Heterogeneity）

**AI 典型症状**：
- "不同分组之间存在显著差异"
- 只报方向不报机制

**改写红线**：
- **报告分组系数的比值**（如"大企业系数是小企业的 1.8 倍"）
- **解释背后机制**：为什么这个分组效应更强/更弱
- 可以穿插短句制造节奏：如"效应在谁身上最强？"（见案例 9）

---

### 10. 稳健性（Robustness）

**AI 典型症状**：
- "为进一步验证结果的稳健性，本文进行了一系列稳健性检验"
- 列举但不说为什么要做每个检验

**改写红线**：
- **每个稳健性检验对应一个具体担忧**（测度误差、选择偏差、反向因果、偶然性）
- 给出**具体数字**证明结果稳健
- 安慰剂检验要报告**经验分布分位点**

---

### 11. 讨论（Discussion）

**AI 典型症状**：
- 只讲正向意义，不讲局限
- "填补了...空白"、"为...提供了重要参考"

**改写红线**：
- **必须**讨论与既有文献的对话——支持、反驳或补充
- **必须**承认局限：数据的局限、方法的局限、样本期的局限
- **禁用**"填补空白"——真正的学者不会这么说，改为"系统检验了既有文献未处理的 X 问题"

---

### 12. 结论（Conclusion）

**AI 典型症状**：
- 重复摘要内容
- "为政策制定和企业管理提供了参考"

**改写红线**：
- **不重复摘要**，结论段要引入**新信息**
- 必须包含：**未解决的问题** + **下一步研究方向**
- 政策启示要**具体**，避免"完善制度"/"加强监管"这种空话
- 可以承认研究的意外发现或局限，增加可信度

---

## 章节改写优先级

如果时间有限，按以下顺序改：

1. **摘要**（投稿前第一关，检测器重点扫描）
2. **引言开头三段**（第一印象决定整篇观感）
3. **结论段**（避免与摘要回音）
4. **文献综述**（AI 最容易露馅的章节）
5. **讨论段**（hedge 注入）
6. 其他章节

> 原则：**AI 最容易写"好看但空洞"的段落，最应该改；AI 写得相对保守的段落（如方法、稳健性），反而可以少改**。

---

## English-manuscript notes

Same sections, same risk ranking — the symptoms just wear English clothes.
Rule IDs refer to `patterns-en.md`.

| Section | Typical English AI symptoms | Key rules |
|---|---|---|
| Abstract | "This study comprehensively examines…", zero numbers, ends with "important implications" | EN01, EN12, EN16 |
| Introduction | "In recent years, X has attracted increasing attention"; three numbered contributions restating the abstract | EN05, EN16, EN06 |
| Literature review | citation dumps with no engagement; "Studies have shown" with no names; false consensus | EN17, EN04, EN07 |
| Hypotheses | "significantly improves" in the hypothesis itself; mechanism triads | EN11, EN07 |
| Data | "comprehensive dataset from various authoritative sources" | EN12, EN04 |
| Empirical strategy | "serves as an ideal natural experiment"; identification asserted, not argued | EN13, EN10 |
| Baseline results | "highly significant, demonstrating a strong effect" with no statistics; "-ing" tails after every table | EN11, EN02 |
| Mechanisms | Moreover/Furthermore chains walking through a mediation triad | EN06, EN07 |
| Heterogeneity | directions reported without magnitudes or explanations | EN01, EN11 |
| Robustness | "extensive robustness checks confirm our findings" | EN12, EN10 |
| Discussion | promotional framing of implications; no design-specific limitations | EN03, EN16, EN15 |
| Conclusion | re-abstracts the abstract; generic "future research" boilerplate | EN22, EN16 |

**Red lines that transfer directly** (see the Chinese sections above for detail):
abstract needs ≥3 concrete numbers; introduction may not open with a
recent-years formula; every literature claim gets an author-year; results
sections report coefficients and test statistics instead of adjectives;
conclusions must introduce new information rather than echo the abstract
(EN22 = ZH17, the same echo-chamber check in both languages).
