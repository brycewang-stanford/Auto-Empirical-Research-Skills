# md-to-docx Skill 安装指南

## 快速安装

### 方法一：作为项目 Skill（推荐用于团队协作）

1. 将整个 `md-to-docx` 文件夹复制到项目的 `.claude/skills/` 目录：
   ```bash
   mkdir -p .claude/skills
   cp -r /path/to/md-to-docx .claude/skills/
   ```

2. 安装依赖：
   ```bash
   # 安装 pandoc
   brew install pandoc  # macOS
   # sudo apt-get install pandoc  # Linux

   # 安装 python-docx
   pip install python-docx
   ```

3. 验证安装：
   ```bash
   pandoc --version
   python3 .claude/skills/md-to-docx/convert_md_to_docx.py --help
   ```

### 方法二：作为个人 Skill（全局可用）

1. 将技能复制到个人 Skills 目录：
   ```bash
   mkdir -p ~/.claude/skills
   cp -r /path/to/md-to-docx ~/.claude/skills/
   ```

2. 安装依赖（同上）

### 方法三：通过 Git（推荐用于版本控制）

如果您的项目已经在 Git 中包含此 Skill：

```bash
# 克隆项目后，Skill 自动可用
git clone <repository-url>
cd <project>

# 安装依赖
brew install pandoc
pip install python-docx
```

## 验证安装

在 Claude Code 中测试：

```bash
# 启动 Claude Code
claude

# 在 Claude 中说：
"Convert test.md to test.docx"
```

Claude 应该自动识别并使用 md-to-docx Skill。

## 文件结构

```
.claude/skills/md-to-docx/
├── SKILL.md                    # Skill 定义文件（必需）
├── INSTALLATION.md             # 本文件
├── README.md                   # 详细文档
├── 快速使用指南.md             # 中文快速指南
├── convert_md_to_docx.py       # 主转换脚本
├── create_chinese_template.py  # 模板生成脚本
├── fix_heading_fonts.py        # 后处理脚本
└── chinese_template.docx       # 中文模板
```

## 系统要求

- Python 3.6+
- pandoc
- python-docx 库

## 故障排除

**"pandoc: command not found"**
- 安装 pandoc：`brew install pandoc`（macOS）

**"No module named 'docx'"**
- 安装 python-docx：`pip install python-docx`

**Skill 未被识别**
- 确保 `SKILL.md` 文件存在
- 检查文件夹位置：`.claude/skills/md-to-docx/`
- 重启 Claude Code

## 更新 Skill

如果此 Skill 在 Git 仓库中：

```bash
git pull origin main
```

如果是手动复制的：

```bash
# 重新复制新版本
cp -r /path/to/updated/md-to-docx .claude/skills/
```

## 卸载

```bash
# 删除项目 Skill
rm -rf .claude/skills/md-to-docx

# 或删除个人 Skill
rm -rf ~/.claude/skills/md-to-docx
```

## 获取帮助

查看完整文档：
- [SKILL.md](SKILL.md) - Skill 功能说明
- [README.md](README.md) - 详细使用指南
- [快速使用指南.md](快速使用指南.md) - 中文快速指南
