#!/usr/bin/env bash
# wechat-article-workflow 一键安装脚本
# 使用方式：bash install.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo -e "${GREEN}🚀 开始安装公众号文章AI写作工作流${NC}"
echo ""

# 1. 安装主工作流
echo -e "${YELLOW}📦 安装主工作流 SKILL...${NC}"
mkdir -p ~/.openclaw/workspace/skills/wechat-article-workflow
cp "$SCRIPT_DIR/SKILL.md" ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md
echo "  ✅ 主工作流已安装到 ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md"

# 2. 安装子技能到 ~/.agents/skills/
echo ""
echo -e "${YELLOW}📦 安装子技能到 ~/.agents/skills/...${NC}"
AGENTS_DIR="$HOME/.agents/skills"
mkdir -p "$AGENTS_DIR"

declare -A AGENTS_SKILLS=(
    ["hot-topics"]="hot-topics"
    ["six-thinking-hats"]="six-thinking-hats"
    ["humanize-writing"]="humanize-writing"
    ["marketing-psychology"]="marketing-psychology"
    ["copywriting"]="copywriting"
    ["deep-research"]="deep-research"
    ["news-aggregator"]="news-aggregator"
    ["wechat-article-scraper"]="wechat-article-scraper"
    ["x-twitter"]="x-twitter"
)

for skill_dir in "${!AGENTS_SKILLS[@]}"; do
    src="$SCRIPT_DIR/skills/$skill_dir"
    dst="$AGENTS_DIR/$skill_dir"
    if [ -d "$src" ]; then
        mkdir -p "$dst"
        cp -r "$src"/* "$dst/" 2>/dev/null || true
        echo "  ✅ $skill_dir → $AGENTS_DIR/$skill_dir/"
    else
        echo "  ⚠️  未找到: $src"
    fi
done

# 3. 安装子技能到 ~/.openclaw/workspace/skills/
echo ""
echo -e "${YELLOW}📦 安装子技能到 ~/.openclaw/workspace/skills/...${NC}"
OPENCLAW_DIR="$HOME/.openclaw/workspace/skills"
mkdir -p "$OPENCLAW_DIR"

declare -A OPENCLAW_SKILLS=(
    ["content-quality-auditor"]="content-quality-auditor"
    ["storytelling"]="storytelling"
    ["ai-humanizer"]="ai-humanizer-2-1-0"
    ["academic-deep-research"]="academic-deep-research"
    ["wechat-mp-writer"]="wechat-mp-writer-skill-mxx"
)

for skill_dir in "${!OPENCLAW_SKILLS[@]}"; do
    src="$SCRIPT_DIR/skills/$skill_dir"
    dst_dir="$OPENCLAW_DIR/${OPENCLAW_SKILLS[$skill_dir]}"
    if [ -d "$src" ]; then
        mkdir -p "$dst_dir"
        cp -r "$src"/* "$dst_dir/" 2>/dev/null || true
        echo "  ✅ $skill_dir → $dst_dir/"
    else
        echo "  ⚠️  未找到: $src"
    fi
done

# 4. 复制发布脚本
echo ""
echo -e "${YELLOW}📦 安装发布脚本...${NC}"
mkdir -p ~/.openclaw/workspace/skills/wechat-publisher/scripts
cp "$SCRIPT_DIR/scripts/publish.sh" ~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh
chmod +x ~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh
echo "  ✅ publish.sh → ~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh"

# 5. 验证安装
echo ""
echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo "验证安装："
echo "  ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md $([ -f ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md ] && echo '✅' || echo '❌')"
echo "  ~/.agents/skills/hot-topics/SKILL.md          $([ -f ~/.agents/skills/hot-topics/SKILL.md ] && echo '✅' || echo '❌')"
echo "  ~/.openclaw/workspace/skills/storytelling/SKILL.md $([ -f ~/.openclaw/workspace/skills/storytelling/SKILL.md ] && echo '✅' || echo '❌')"
echo ""
echo "下一步："
echo "  1. 配置微信公众号凭证（见 README.md）"
echo "  2. 安装 wenyan-cli: npm install -g @wenyan-md/cli"
echo "  3. 开始写文章：发送 '用公众号文章工作流写一篇关于[选题]的文章'"
