# Paper-WorkFlow — 社科实证论文全流程演示包

一套面向「社科实证论文 workflow」的演示物料：**一份 30 页 PPTX** 讲清楚从选题到投稿的
端到端研究流水线，外加 **一个可一键运行的 DiD 演示 Notebook**，把工作流里「计量估计」
这一步真正跑给观众看。

全部内容参考并对应 [`skills/67-econfin-workflow-toolkit`](../67-econfin-workflow-toolkit/)
里的 47 个技能。

---

## 交付物

| 文件 | 说明 |
|---|---|
| `社科实证论文工作流.pptx` | **主交付物**：30 页演示文稿（16:9，可编辑） |
| `社科实证论文工作流.pdf` | 上面的 PDF 导出，方便不开 PowerPoint 直接预览 |
| `did_demo.ipynb` | **配套演示 Notebook**：6 步跑通一个完整 DiD（已带运行结果与图） |
| `assets/fig_raw_trends.png` | Notebook ② 步产出：原始趋势图 |
| `assets/fig_event_study.png` | Notebook ④ 步产出：事件研究图 |
| `assets/did_table.tex` | Notebook ⑥ 步产出：回归表（LaTeX 三线表） |
| `build_pptx.py` | PPTX 生成脚本（改主题/内容后可一键重生成） |
| `build_notebook.py` | Notebook 生成脚本 |

---

## 30 页 PPTX 的结构

围绕实证研究的 **8 个阶段** 展开，并在第 5 板块聚焦本次演示方法 **DiD**：

| 页 | 内容 |
|---|---|
| 1–2 | 封面 · 目录 |
| 3–6 | **板块一 为什么需要工作流**：痛点 → 八阶段总览图 → 47 技能全景地图 |
| 7–9 | **板块二 选题与设计**：idea-finder / novelty-check / significance-search / proposal / journal-digest |
| 10–12 | **板块三 数据**：data-fetcher（取数与合并键）/ data-cleaning（清洗清单） |
| 13–15 | **板块四 计量识别**：八种识别策略地图 + 方法选择决策树 |
| 16–21 | **板块五 聚焦 DiD**：2×2 核心逻辑 → 平行趋势/事件研究 → 交错偏误与现代估计量 → 稳健性清单 → Notebook 演示说明 |
| 22–24 | **板块六 结果呈现**：table（出版级回归表）/ figure（事件研究图） |
| 25–28 | **板块七 写作·评审·投稿**：paper-pipeline 五步流水线 / referee / reference-verify / submission |
| 29–30 | 全流程复盘表 · 结束页 |

---

## 选用的技能与演示方法

- **演示主线技能：[`did-analysis`](../67-econfin-workflow-toolkit/did-analysis/SKILL.md)**
  —— 双重差分是社科实证里最具教学价值、最适合现场演示的方法（政策评估 / 自然实验），
  且单凭模拟数据就能把「识别假设 → 估计 → 检验 → 稳健性」完整走一遍。
- Notebook 严格对应该技能 `SKILL.md` 的工作流：设计检查 → 平行趋势 → 基准回归 →
  交错设计 → 稳健性，并把它的 Python 代码模板（`smf.ols` / TWFE / 事件研究）落成可运行 cell。

### `did_demo.ipynb` 的 6 步（+1 个进阶）

1. **生成模拟面板**：200 个体 × 12 年，植入已知真实 `ATT = 2.0`，便于对照「估计是否还原真值」。
2. **可视化原始趋势**：处理组 vs 对照组均值时间序列，肉眼看处理后分叉。
3. **基准估计**：手算 2×2 → 简单 OLS → 双向固定效应 TWFE，个体层聚类稳健标准误；三者一致还原 ≈1.95。
4. **事件研究 + 平行趋势检验**：相对时间系数图 + 处理前联合 F 检验（生成论文级 Figure）。
5. **稳健性**：伪处理时点 + 伪处理组两类安慰剂，均不显著 → 主效应可信。
6. **导出表与图**：回归表（文本 + LaTeX）与两张 PNG，直接进入第⑤阶段 table / figure。
7. **进阶**：用一个小模拟演示「交错处理 + 异质动态效应」下朴素 TWFE 为何有偏，引出 CS / SA / BJS。

> 想换成你自己的数据：把第①步替换为 `df = pd.read_csv("your_panel.csv")`，
> 保证含 `unit, year, treat, post, treat_post, y` 列即可，后续 cell 无需改动。

---

## 如何使用

### 看/改幻灯片
直接打开 `社科实证论文工作流.pptx`（PowerPoint / Keynote / WPS 均可编辑）。
若要批量改样式或内容，编辑 `build_pptx.py` 后重新生成：

```bash
python3 build_pptx.py        # 依赖: pip install python-pptx
```

### 跑演示 Notebook
在 VS Code（Jupyter 扩展）或 JupyterLab 打开 `did_demo.ipynb`，从上到下逐 cell 运行。
也可命令行一键执行：

```bash
pip install pandas numpy statsmodels matplotlib   # 可选: linearmodels
jupyter nbconvert --to notebook --execute --inplace did_demo.ipynb
```

> 现场演示建议：先放 PPTX 讲到第 16–21 页（聚焦 DiD），切到 Notebook 现跑第 ②④ 步出图，
> 再切回第 22–24 页讲表图规范，节奏紧凑。

---

## 环境

- Python 3.9+，`python-pptx`、`pandas`、`numpy`、`statsmodels`、`matplotlib`（`linearmodels` 可选）。
- Notebook 已在 Python 3.13 / statsmodels 0.14 下执行通过，输出与图均已内嵌。
- 中文图表字体在 macOS 上自动选用 Hiragino Sans GB / STHeiti 等；其它系统会自动回退，
  找不到中文字体也不影响计算结果。
