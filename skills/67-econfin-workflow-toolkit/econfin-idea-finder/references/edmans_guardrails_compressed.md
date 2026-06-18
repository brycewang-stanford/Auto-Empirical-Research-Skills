# Edmans Guardrails — 5 项硬测试 + 失败模式诊断

**Source**: Edmans, Alex (2024) "Learnings From 1000 Rejections" — 内化版

**用途**：Phase 4 强制硬测试；任何 idea 必须通过这 5 项才能进入 Phase 5。

---

## Test 1: Convex Combination Detection（红线 — 直接 KILL）

### 定义

> "If we already know X→Z (paper A) and Z→Y (paper B), showing X→Y is not a contribution."

### 检测程序

对每个 candidate idea 的 X → Y 关系，问：
1. 文献中是否已发表 X → Z 的因果证据？（Z 是任何中间机制 / mediator）
2. 文献中是否已发表 Z → Y 的因果证据？
3. 如果两者都是 yes，那么 X → Y 仅是 transitive closure，**不是新 contribution**

### 例外情况（不算 convex combination）

- ✅ X → Y 的方向**与** transitive prediction **相反**（surprising finding）
- ✅ X → Y 的 magnitude 超出 X → Z × Z → Y 简单乘积可解释
- ✅ X → Y 揭示了一个 X → Z 或 Z → Y **之外**的新通道
- ✅ X 和 Y 的具体定义在已有 X → Z 和 Z → Y 文献中**不可观测**

### 例子（用户最近的失败）

**v2 Idea 1（跨境 PE → inventor 跨国流向 acquirer 母国）**：
- 已知 1：Stiebale (JIE 2016) → 跨境 M&A → 创新从 target 国 reallocate 到 acquirer 国
- 已知 2：Davis-Herkenhoff → PE → 工人 reallocation
- 推论：跨境 PE → inventor 跨国流向 acquirer 国 = **convex combination → KILL**

---

## Test 2: Just-Another-Determinant Test

### 定义

> "Finding 'yet another factor that affects Y' is not enough."

### 检测程序

问 3 个问题：
1. 如果 X 显著影响 Y，会改变现有理论吗？还是只是补充一个因素？
2. 如果 X 不显著，会有人在意这个 null result 吗？
3. **政策制定者 / 公司管理者会因为这个 finding 改变行为吗？**

### KILL 条件

- ✅ "X is yet another factor affecting Y, just like Z and W" — KILL
- ✅ 失败的 null result 没有 narrative weight — KILL
- ✅ 没有清晰的 actionable implication — KILL

### 例子

❌ "[New cultural variable] affects [investment decision]" — 文献已经有 50 个 cultural variables 影响投资，多一个不构成 contribution
✅ "[New cultural variable] **reverses** the prediction of [established theory]" — 改变现有理解 = contribution

---

## Test 3: Survey Paper Test

### 定义

> "Would a future survey paper on Y dedicate a section to your X?"

### 检测程序

设想 5 年后某顶刊（JF/JFE/RFS）的 Y 综述论文：
- 它会用一段引用本研究吗？
- 它会用一句话引用？
- 还是仅在脚注？
- 或者完全不引用？

### KILL 条件
- "完全不引用" 或 "仅脚注" → KILL
- "一句话引用" → 仍可能是 incremental，需 Phase 5 复核
- "一段引用" + 改变后续研究方向 → PASS

### 例子

✅ Babina-Fedyk-He-Hodson (2024 JFE) 关于 AI 投资 — 未来 AI & finance 综述会有专门一节
❌ "X 国 Y 行业的 Z 政策对 W 的影响" — 综述不会单独引

---

## Test 4: Both Sides Trade-off Requirement

### 定义

> "If studying whether X creates value, you must address both costs and benefits — documenting only one side is insufficient."

### 检测程序

对每个 X → Y 因果论断，问：
- 主效应是 cost 还是 benefit？
- 反方向（cost 还是 benefit）有 evidence 吗？
- 净效应在样本中是 + 还是 -？
- 异质性中 cost 主导 vs benefit 主导的 subgroup 分别是什么？

### 处罚（不是 KILL，但 -2 分）

- ✅ 仅记录 benefit 不记录 cost → -2 分
- ✅ 仅记录 cost 不记录 benefit → -2 分
- ✅ 不计算净效应 → -1 分

### 例子

❌ "性别配额提升公司绩效" — 没说 token 成本、关键人才离职、监管负担
✅ "性别配额：在 X 条件下提升业绩，在 Y 条件下降低，净效应是 Z%" — 平衡

---

## Test 5: Identification Scrutiny

### 定义

> "The IV must satisfy both relevance AND exclusion restriction with explicit justification. DID must have credible parallel trends. RDD must have a meaningful discontinuity."

### 检测程序

按识别策略分类检查：

**IV (Instrumental Variable)**：
- Relevance：First-stage F > 10？预期 F > 30 才 strong
- Exclusion：IV 通过非 X 通道影响 Y 的可能渠道有哪些？显式排除每一个
- Monotonicity：处理效应方向一致？

**DID (Difference-in-Differences)**：
- 平行趋势：pre-treatment trends 显示出来了吗？
- 处理时间：交错 DID 的话，用 Sun-Abraham / Callaway-Sant'Anna？
- 安慰剂：假设 treatment 提前 / 推后的 placebo？

**RDD (Regression Discontinuity)**：
- 不连续是 meaningful 的吗？running variable 是 manipulable 的吗？
- McCrary density test？
- Bandwidth 选择鲁棒？

**Shift-share / Bartik**：
- Goldsmith-Pinkham et al. (2020) 诊断？
- Borusyak-Hull-Jaravel diagnostic？

### 处罚（-2 分）

- ✅ IV 没有显式 exclusion 论证 → -2 分
- ✅ DID 没有平行趋势检验 → -2 分
- ✅ RDD 没有 manipulation test → -2 分

---

## Borrowed Wisdom, Original Angle 原则

### 5 个具体落地策略

1. **借识别策略，换问题**：用已发表论文的 DID/RDD/IV 设计，但应用到不同问题/情境
2. **借理论镜头，跨学科**：把 behavioral finance 的 insights 应用到 corporate governance；把 labor economics 方法应用到 financial markets
3. **不复制**：JF 已发"X 在美国"，不能简单做"X 在中国"——除非中国制度特征产生**genuinely 不同**的预测
4. **找文献交集的 gap**：最好的 idea 在两个还未 cross-pollinate 的子领域之间
5. **用 micro data 改写 macro question**：现有研究只有 firm-level 测量，新 idea 用 individual-level（Revelio 优势）

### 示例

✅ Stiebale 用 PATSTAT 发明者地址做 firm-level；用 Revelio worker-month panel **不能仅** "用更细数据复制"。需要 Revelio 揭示 firm-level 数据**不可观测**的现象（如 acqui-hire 到 GP 同集团其他子公司）。

---

## Failure Mode Diagnosis（用户历史失败模式）

| 失败模式 | 诊断 | 解决 |
|---------|-----|-----|
| "10 个 idea 都 5-7 分" | Phase 1 frontier 没扫深 | 必须搜 ≥3 个文献集群 |
| "selected idea 在 proposal 阶段降分" | Phase 5 漏了 adjacent literature（如 JIE 跨境 M&A） | 强制 Phase 5 调用 Codex 反对论 + 多 cluster |
| "convex combination 没识别" | Edmans Test 1 没硬执行 | Phase 4 强制 KILL，不商量 |
| "数据不可行" | Phase 0 跳过了 | Phase 0 是 mandatory |

---

## Quick Reference: 一个 idea 通过 Edmans 5 项的 checklist

```
□ Test 1: 不是 convex combination of [A] and [B]（必过）
□ Test 2: 不是 just-another-determinant of [Y]（必过）
□ Test 3: 未来 Y 综述会用 ≥1 段引用本研究（必过）
□ Test 4: 已识别 cost AND benefit 两面（弱失败 -2 分）
□ Test 5: 识别策略经得起 standard 审稿人质疑（弱失败 -2 分）
```

如果全部 ✅ → 进入 Phase 5 deep novelty check
如果 Test 1-3 任何 fail → 立即 KILL
如果 Test 4-5 fail → 降分 -2，仍可进入 Phase 5
