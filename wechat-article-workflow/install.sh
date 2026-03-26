#!/usr/bin/env bash
# wechat-article-workflow 一键安装脚本
# 使用方式：bash install.sh
#
# 本脚本会自动安装：
#   1. 主工作流 SKILL
#   2. 13 个子技能（复制到正确路径）
#   3. 热点扫描脚本
#   4. 微信公众号发布脚本
#   5. 必要的 npm 全局工具
#   6. 各技能需要的 npm / Python 依赖
#
# 环境要求：Node.js ≥ 18.0，Python ≥ 3.10

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  公众号文章AI写作工作流 - 一键安装${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# -------------------------------------------------------
# 第一步：安装全局 npm 工具
# -------------------------------------------------------
echo -e "${YELLOW}📦 第一步：安装全局 npm 工具...${NC}"

install_npm_global() {
    local pkg="$1"
    if ! command -v "$pkg" &> /dev/null; then
        echo -n "  安装 $pkg... "
        npm install -g "$pkg" &> /dev/null && echo "✅" || echo "⚠️"
    else
        echo -e "  $pkg ✅ 已安装"
    fi
}

install_npm_global "@wenyan-md/cli"
echo -e "${GREEN}✅ 全局工具安装完成${NC}"

# -------------------------------------------------------
# 第二步：安装主工作流
# -------------------------------------------------------
echo ""
echo -e "${YELLOW}📦 第二步：安装主工作流 SKILL...${NC}"
mkdir -p ~/.openclaw/workspace/skills/wechat-article-workflow
cp "$SCRIPT_DIR/SKILL.md" ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md
echo -e "${GREEN}✅ 主工作流已安装${NC}"

# -------------------------------------------------------
# 第三步：安装热点脚本
# -------------------------------------------------------
echo ""
echo -e "${YELLOW}📦 第三步：安装热点扫描脚本...${NC}"
mkdir -p ~/.openclaw/workspace-content/scripts
cp "$SCRIPT_DIR/scripts/daily-hot-topics.js" ~/.openclaw/workspace-content/scripts/daily-hot-topics.js
echo -e "${GREEN}✅ 热点扫描脚本已安装${NC}"

# -------------------------------------------------------
# 第四步：安装发布脚本
# -------------------------------------------------------
echo ""
echo -e "${YELLOW}📦 第四步：安装微信公众号发布脚本...${NC}"
mkdir -p ~/.openclaw/workspace/skills/wechat-publisher/scripts
cp "$SCRIPT_DIR/scripts/publish.sh" ~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh
chmod +x ~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh
echo -e "${GREEN}✅ 发布脚本已安装${NC}"

# -------------------------------------------------------
# 第五步：安装子技能（按正确路径分类）
# -------------------------------------------------------
echo ""
echo -e "${YELLOW}📦 第五步：安装子技能到 ~/.agents/skills/...${NC}"
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
        # 复制所有文件
        cp -r "$src"/* "$dst/" 2>/dev/null || true
        echo -e "  ${GREEN}✅${NC} $skill_dir → $AGENTS_DIR/$skill_dir/"
        
        # 如果有 package.json，安装 npm 依赖
        if [ -f "$dst/package.json" ]; then
            echo -n "    安装 npm 依赖 ($skill_dir)... "
            (cd "$dst" && npm install --silent 2>/dev/null && echo "✅") || echo "⚠️ npm install 失败"
        fi
        
        # 如果有 requirements.txt，安装 Python 依赖
        if [ -f "$dst/requirements.txt" ]; then
            echo -n "    安装 Python 依赖 ($skill_dir)... "
            (pip install -q "$dst/requirements.txt" 2>/dev/null && echo "✅") || echo "⚠️ pip install 失败"
        fi
    else
        echo -e "  ${YELLOW}⚠️${NC} 未找到: $src"
    fi
done

echo ""
echo -e "${YELLOW}📦 第六步：安装子技能到 ~/.openclaw/workspace/skills/...${NC}"
OPENCLAW_DIR="$HOME/.openclaw/workspace/skills"
mkdir -p "$OPENCLAW_DIR"

declare -A OPENCLAW_SKILLS=(
    ["content quality-auditor"]="content quality-auditor"
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
        echo -e "  ${GREEN}✅${NC} $skill_dir → $dst_dir/"
        
        # 如果有 package.json，安装 npm 依赖
        if [ -f "$dst_dir/package.json" ]; then
            echo -n "    安装 npm 依赖 ($skill_dir)... "
            (cd "$dst_dir" && npm install --silent 2>/dev/null && echo "✅") || echo "⚠️ npm install 失败"
        fi
        
        # 如果有 requirements.txt，安装 Python 依赖
        if [ -f "$dst_dir/requirements.txt" ]; then
            echo -n "    安装 Python 依赖 ($skill_dir)... "
            (pip install -q "$dst_dir/requirements.txt" 2>/dev/null && echo "✅") || echo "⚠️ pip install 失败"
        fi
    else
        echo -e "  ${YELLOW}⚠️${NC} 未找到: $src"
    fi
done

# -------------------------------------------------------
# 第七步：验证安装
# -------------------------------------------------------
echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  安装验证${NC}"
echo -e "${CYAN}========================================${NC}"

verify() {
    local label="$1"
    local path="$2"
    if [ -f "$path" ]; then
        echo -e "  ${GREEN}✅${NC} $label"
    else
        echo -e "  ${RED}❌${NC} $label (缺失: $path)"
    fi
}

verify "主工作流"        ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md
verify "热点扫描脚本"    ~/.openclaw/workspace-content/scripts/daily-hot-topics.js
verify "发布脚本"        ~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh
verify "wenyan-cli"       $(which wenyan 2>/dev/null || echo "未找到")
verify "hot-topics"        ~/.agents/skills/hot-topics/SKILL.md
verify "六帽分析"         ~/.agents/skills/six-thinking-hats/SKILL.md
verify "AI去味"           ~/.agents/skills/humanize-writing/SKILL.md
verify "营销心理"         ~/.agents/skills/marketing-psychology/SKILL.md
verify "文案框架"         ~/.agents/skills/copywriting/SKILL.md
verify "深度调研"         ~/.agents/skills/deep-research/SKILL.md
verify "新闻聚合"         ~/.agents/skills/news-aggregator/SKILL.md
verify "微信爬虫"         ~/.agents/skills/wechat-article-scraper/SKILL.md
verify "内容质检"         ~/.openclaw/workspace/skills/content quality-auditor/SKILL.md
verify "故事框架"         ~/.openclaw/workspace/skills/storytelling/SKILL.md
verify "学术调研"         ~/.openclaw/workspace/skills/academic-deep-research/SKILL.md
verify "公众号写作"       ~/.openclaw/workspace/skills/wechat-mp-writer-skill-mxx/SKILL.md

# -------------------------------------------------------
# 完成
# -------------------------------------------------------
echo ""
echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo -e "${CYAN}下一步配置：${NC}"
echo ""
echo -e "  1. 配置微信公众号凭证："
echo -e "     在 ~/.bashrc 中添加："
echo -e "     export WECHAT_APP_ID=你的AppID"
echo -e "     export WECHAT_APP_SECRET=你的AppSecret"
echo ""
echo -e "  2. 使配置生效："
echo -e "     source ~/.bashrc"
echo ""
echo -e "  3. 开始写文章："
echo -e "     发送：'用公众号文章工作流，写一篇关于[选题]的文章'"
