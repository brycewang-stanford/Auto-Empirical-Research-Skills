# Marp 主题库

本文件夹包含精选的 Marp 演示文稿主题，支持多种风格和使用场景。

## 主题概览

| 主题名称 | 风格 | 适用场景 | 来源 |
|---------|------|----------|------|
| **academic** | 学术风格 | 学术报告、论文答辩 | kaisugi/marp-theme-academic |
| **beam** | LaTeX Beamer 风格 | 学术演讲、技术分享 | rnd195/my-marp-themes |
| **border** | 边框简约风格 | 通用演示 | rnd195/my-marp-themes |
| **gradient** | 渐变背景 | 创意展示 | rnd195/my-marp-themes |
| **graph_paper** | 方格纸风格 | 技术分享、教学 | rnd195/my-marp-themes |
| **companyLightBlue** | 企业浅蓝 | 企业汇报、商务演示 | zhaoluting/marp-themes |
| **companySZ** | 企业深色 | 企业汇报、正式场合 | zhaoluting/marp-themes |
| **zju** | 浙大风格 | 高校演示、学术报告 | zhaoluting/marp-themes |
| **socrates** | 苏格拉底风格 | 哲学、人文学科 | cunhapaulo/marpstyle |
| **turing** | 图灵风格 | 计算机科学、技术 | cunhapaulo/marpstyle |
| **jobs** | 乔布斯风格 | 产品发布、商业演示 | cunhapaulo/marpstyle |
| **einstein** | 爱因斯坦风格 | 科学、物理学 | cunhapaulo/marpstyle |
| **simple** | 极简风格 | 通用演示 | cunhapaulo/marpstyle |

## 主题详细说明

### 学术类主题

#### academic
- **特点**：maroon 红色标题栏，页码显示为"当前页/总页数"
- **字体**：Noto Sans JP（支持日文和中文）
- **适用**：学术论文报告、课堂演示
- **配置**：
  ```yaml
  theme: academic
  class: lead  # 用于标题页
  ```

#### beam
- **特点**：仿 LaTeX Beamer 风格，底部蓝黑双色装饰条
- **字体**：CMU Sans Serif / Segoe UI
- **适用**：学术演讲、技术研讨会
- **配置**：
  ```yaml
  theme: beam
  class: title    # 标题页
  class: tinytext # 小字体页面（如参考文献）
  ```

#### zju
- **特点**：浙江大学官方配色，校徽和校训元素
- **适用**：高校内部演示、学术答辩
- **配置**：
  ```yaml
  theme: zju
  ```

### 企业商务类主题

#### companyLightBlue
- **特点**：清新浅蓝配色，专业商务风格
- **适用**：企业内部汇报、商务提案

#### companySZ
- **特点**：深色企业风格，正式庄重
- **适用**：高层汇报、正式商务场合

#### jobs
- **特点**：仿 Apple 发布会风格，San Francisco 字体
- **字体**：San Francisco（Apple 官方字体）
- **适用**：产品发布、创业路演
- **配置**：
  ```yaml
  theme: jobs
  class: titlepage   # 标题页
  class: transition  # 过渡页
  class: cite        # 引用页
  ```

### 创意设计类主题

#### gradient
- **特点**：渐变色背景，现代感强
- **适用**：创意展示、设计分享

#### border
- **特点**：简约边框装饰
- **适用**：通用演示

#### socrates / einstein / turing
- **特点**：以历史名人命名，各有独特配色和排版风格
- **适用**：不同学科领域演示

### 通用类主题

#### graph_paper
- **特点**：方格纸背景，手写笔记感
- **适用**：技术分享、教学演示、草稿展示

#### simple
- **特点**：极简设计，最少装饰
- **适用**：通用场合、内容为王

## 主题标题格式要求

不同主题对标题 Markdown 语法有特殊要求。**制作 slides 时必须遵循对应主题的格式**：

| 主题 | 内容页标题 | 标题页指令 | 说明 |
|------|-----------|-----------|------|
| **beam** | `#` (h1) | `<!-- _class: title -->` | h1 显示在顶部蓝色装饰条中 |
| **academic** | `#` (h1) | `class: lead` | h1 用于页面标题 |
| **jobs** | `#` (h1) | `class: titlepage` | h1 有蓝色下划线样式 |
| graph_paper | `##` (h2) | 无特殊要求 | 标准 h2 标题 |
| simple | `##` (h2) | 无特殊要求 | 标准 h2 标题 |
| 其他主题 | `##` (h2) | 视主题而定 | 默认使用 h2 |

### beam 主题示例

```markdown
---
marp: true
theme: beam
---

<!-- _class: title -->

# 演示文稿标题

作者名称

---

# 内容页标题显示在蓝色条中

- 要点一
- 要点二
```

### 标准主题示例（graph_paper 等）

```markdown
---
marp: true
theme: graph_paper
---

# 标题页

副标题

---

## 内容页标题

- 要点一
- 要点二
```

## 使用方法

### 方法一：本地主题文件

在 Marp 文档的 YAML frontmatter 中指定主题：

```yaml
---
marp: true
theme: academic
---
```

使用 marp-cli 时指定主题目录：

```bash
marp --theme-set ./themes/ presentation.md -o output.html
```

### 方法二：远程 URL

部分主题支持直接使用 CDN 链接：

```yaml
---
marp: true
theme: https://rnd195.github.io/my-marp-themes/beam.css
---
```

### VS Code 配置

在 `.vscode/settings.json` 中添加主题路径：

```json
{
  "markdown.marp.themes": [
    "./themes/academic.css",
    "./themes/beam.css",
    "./themes/jobs.css"
  ]
}
```

## 主题选择建议

| 场景 | 推荐主题 | 备选 |
|------|----------|------|
| 学术答辩 | academic, beam | zju |
| 技术分享 | graph_paper, beam | turing |
| 产品发布 | jobs | gradient |
| 企业汇报 | companyLightBlue | companySZ |
| 教学演示 | simple, graph_paper | academic |
| 创意展示 | gradient | jobs |

## 主题来源和许可证

| 来源仓库 | 许可证 |
|----------|--------|
| [kaisugi/marp-theme-academic](https://github.com/kaisugi/marp-theme-academic) | MIT |
| [rnd195/my-marp-themes](https://github.com/rnd195/my-marp-themes) | GNU GPLv3 |
| [zhaoluting/marp-themes](https://github.com/zhaoluting/marp-themes) | MIT |
| [cunhapaulo/marpstyle](https://github.com/cunhapaulo/marpstyle) | MIT |
