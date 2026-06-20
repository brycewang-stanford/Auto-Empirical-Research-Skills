# Markdown转Word技能快速使用指南

## 功能概述

这个Claude Code技能可以将Markdown文档转换为格式良好的Word文档（.docx），特别优化了中文文档的处理。

**默认字体设置**：
- 中文：仿宋（正文）、黑体（标题）
- 英文：Times New Roman
- 字号：12磅

## 快速开始

### 1. 转换单个文件

```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py 输入.md 输出.docx
```

示例：
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py "AI赋能与数字化转型战略.md" "AI赋能与数字化转型战略.docx"
```

### 2. 批量转换文件夹中的所有Markdown文件

```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py --batch 输入文件夹/ 输出文件夹/
```

示例：
```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py --batch ./文档草稿/ ./Word文档/
```

### 3. 生成带目录的Word文档

```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py 输入.md 输出.docx --toc
```

### 4. 添加文档元数据

```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py 报告.md 报告.docx \
  --title "岭南学院教育改革方案" \
  --author "教育改革工作组" \
  --date "2025-11-20"
```

## 常用命令选项

| 选项 | 说明 |
|------|------|
| `--toc` | 生成目录 |
| `--no-chinese-template` | 不使用默认中文模板 |
| `--reference-doc 模板.docx` | 使用自定义Word模板 |
| `--title "标题"` | 设置文档标题 |
| `--author "作者"` | 设置作者信息 |
| `--date "日期"` | 设置文档日期 |
| `--batch` | 批量转换模式 |
| `--pattern "*.md"` | 批量转换时的文件匹配模式 |

## 支持的Markdown功能

- ✓ 标题（H1-H6）
- ✓ 粗体、斜体、删除线
- ✓ 有序列表和无序列表
- ✓ 表格
- ✓ 代码块和行内代码
- ✓ 引用块
- ✓ 图片（自动嵌入）
- ✓ 链接
- ✓ 中文标点符号

## 在Claude Code中使用

在Claude Code对话中，您可以直接请求：

- "将这个markdown文件转换为Word格式"
- "把AI赋能与数字化转型战略.md转成docx"
- "批量转换所有教改方案的markdown文档为Word"

Claude会自动调用这个技能完成转换。

## 自定义模板

如果您需要使用学院特定的Word模板：

1. 准备好您的Word模板文件（如：`岭南学院模板.docx`）
2. 使用 `--reference-doc` 参数指定：

```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py 文档.md 输出.docx \
  --reference-doc 岭南学院模板.docx
```

## 创建新的中文模板

如果您想创建新的中文字体模板：

```bash
python .claude/skills/md-to-docx/create_chinese_template.py -o 新模板.docx
```

然后使用这个模板：

```bash
python .claude/skills/md-to-docx/convert_md_to_docx.py 文档.md 输出.docx \
  --reference-doc 新模板.docx
```

## 常见问题

**Q: 转换后中文字体不是仿宋？**

A: 确保没有使用 `--no-chinese-template` 选项。默认会自动使用仿宋字体模板。

**Q: 图片没有显示在Word文档中？**

A: 检查Markdown中的图片路径是否正确。建议使用相对路径。

**Q: 表格格式不正确？**

A: 确认Markdown表格语法正确：

```markdown
| 列1 | 列2 |
|-----|-----|
| 内容1 | 内容2 |
```

**Q: 需要安装什么软件？**

A: 需要安装pandoc。macOS用户运行：`brew install pandoc`

## 技术支持

如有问题，请查看：
- `SKILL.md` - 完整技能文档
- `README.md` - 详细使用说明

## 适用场景

这个技能特别适用于：

- ✓ 教育改革方案文档的编写和转换
- ✓ 学术报告的格式化
- ✓ 会议纪要的整理
- ✓ 研究计划的准备
- ✓ 需要提交Word格式的任何文档
