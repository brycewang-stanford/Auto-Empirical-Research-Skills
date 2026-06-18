# md-to-docx Skill 分发指南

本指南说明如何将 md-to-docx Skill 分享给其他人使用。

## 分发方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Git 仓库** | 版本控制、易更新、团队协作 | 需要 Git 知识 | 团队项目、开源分享 |
| **压缩包** | 简单直接、无需 Git | 更新麻烦 | 一次性分享 |
| **文件共享** | 适合内网 | 版本管理难 | 企业内部 |

## 方法一：通过 Git 仓库分发（推荐）

### 1. 准备 Git 仓库

```bash
# 在项目根目录
git add .claude/skills/md-to-docx
git commit -m "Add md-to-docx skill for team use"
git push origin main
```

### 2. 团队成员使用

```bash
# 克隆项目
git clone <repository-url>
cd <project>

# 安装依赖
brew install pandoc
pip install python-docx

# 启动 Claude Code，Skill 自动可用
claude
```

### 3. 更新 Skill

```bash
# 更新者
git add .claude/skills/md-to-docx
git commit -m "Update md-to-docx skill: add new features"
git push

# 使用者
git pull origin main
```

## 方法二：创建压缩包分发

### 1. 创建分发包

```bash
# 在技能文件夹的父目录
cd .claude/skills
tar -czf md-to-docx-skill.tar.gz md-to-docx/

# 或创建 zip 文件
zip -r md-to-docx-skill.zip md-to-docx/
```

### 2. 分享文件

通过邮件、云盘等方式分享 `md-to-docx-skill.tar.gz` 或 `md-to-docx-skill.zip`

### 3. 接收方安装

```bash
# 解压到项目 Skills 目录
mkdir -p .claude/skills
tar -xzf md-to-docx-skill.tar.gz -C .claude/skills/

# 或解压 zip
unzip md-to-docx-skill.zip -d .claude/skills/

# 安装依赖
brew install pandoc
pip install python-docx
```

## 方法三：安装为全局 Skill

如果希望在所有项目中使用：

```bash
# 复制到个人 Skills 目录
mkdir -p ~/.claude/skills
cp -r .claude/skills/md-to-docx ~/.claude/skills/

# 或解压到个人目录
tar -xzf md-to-docx-skill.tar.gz -C ~/.claude/skills/
```

## 方法四：创建安装脚本

创建自动安装脚本 `install.sh`：

```bash
#!/bin/bash

echo "Installing md-to-docx skill..."

# 检测安装类型
read -p "Install as [P]roject skill or [G]lobal skill? (P/G): " install_type

if [ "$install_type" = "G" ] || [ "$install_type" = "g" ]; then
    SKILLS_DIR="$HOME/.claude/skills"
    echo "Installing as global skill..."
else
    SKILLS_DIR=".claude/skills"
    echo "Installing as project skill..."
fi

# 创建目录
mkdir -p "$SKILLS_DIR"

# 复制文件
cp -r md-to-docx "$SKILLS_DIR/"

echo "✓ Skill files copied"

# 检查 pandoc
if ! command -v pandoc &> /dev/null; then
    echo "⚠ pandoc not found. Please install:"
    echo "  macOS: brew install pandoc"
    echo "  Linux: sudo apt-get install pandoc"
else
    echo "✓ pandoc found"
fi

# 检查 python-docx
if ! python3 -c "import docx" &> /dev/null; then
    echo "⚠ python-docx not found. Installing..."
    pip install python-docx
else
    echo "✓ python-docx found"
fi

echo ""
echo "Installation complete!"
echo "Skill location: $SKILLS_DIR/md-to-docx"
```

## 分发清单

分享时确保包含以下文件：

- ✅ `SKILL.md` - Skill 定义（必需）
- ✅ `README.md` - 详细文档
- ✅ `INSTALLATION.md` - 安装指南
- ✅ `快速使用指南.md` - 中文快速指南
- ✅ `convert_md_to_docx.py` - 主脚本
- ✅ `create_chinese_template.py` - 模板生成
- ✅ `fix_heading_fonts.py` - 后处理
- ✅ `chinese_template.docx` - 中文模板

## 版本管理建议

1. **在 SKILL.md 中添加版本信息**：
   ```markdown
   Version: 1.0.0
   Last Updated: 2025-11-20
   ```

2. **使用 Git 标签**：
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **维护更新日志**：
   创建 `CHANGELOG.md` 记录版本变更

## 企业级分发

对于企业环境：

1. **内部 Git 服务器**（GitLab/GitHub Enterprise）
2. **包管理系统**（Artifactory/Nexus）
3. **自动化部署**（CI/CD 流程）

## 许可证

如果开源分享，添加 LICENSE 文件（如 MIT License）：

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge...
```

## 支持与反馈

建议在分发包中包含：
- 问题反馈渠道（Issues/Email）
- 文档链接
- 示例项目

## 最佳实践

1. **清晰的文档**：README、INSTALLATION、快速指南
2. **依赖管理**：明确列出所有依赖
3. **版本控制**：使用语义化版本号
4. **测试覆盖**：提供测试用例和示例
5. **持续维护**：定期更新和修复 Bug
