# CLAUDE.md — AI Agent 使用指南

> 本文件供 AI Agent 阅读。当 AI 进入本仓库时，会自动读取此文件。

## 这是什么

这是一个**公众号文章 AI 写作工作流**，包含：
- 1 个主工作流 Skill（协调所有子技能）
- 13 个子技能 Skill（各司其职）
- 1 个发布脚本（微信公众号草稿箱）

## 快速开始（AI Agent 直接可用提示词）

把以下任一提示词发给 AI，即可启动完整工作流：

```
用公众号文章工作流写一篇关于 [你的选题] 的文章。
工作流会自动执行：热点搜索 → 选题确认 → 深度调研 → 六帽分析 → 写作 → 发布到草稿箱。
```

## 目录结构

```
wechat-article-workflow/
├── README.md                  # 人类使用文档
├── CLAUDE.md                 # AI Agent 使用指南（本文件）
├── SKILL.md                  # ⭐ 工作流主 Skill（OpenClaw 直接调用）
└── skills/                  # 子技能 Skill 文件（需安装到正确路径）
    ├── hot-topics.md
    ├── six-thinking-hats.md
    ├── humanize-writing.md
    ├── marketing-psychology.md
    ├── copywriting.md
    ├── deep-research.md
    ├── content quality-auditor.md
    ├── storytelling.md
    ├── ai-humanizer.md
    ├── news-aggregator.md
    ├── wechat-article-scraper.md
    └── academic-deep-research.md
```

## AI Agent 安装指南

### 方式一：直接从本仓库安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/Jorzro/MY-skills.git ~/MY-skills

# 2. 安装主工作流
cp ~/MY-skills/wechat-article-workflow/SKILL.md \
   ~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md

# 3. 安装所有子技能（复制到对应目录）
cp ~/MY-skills/wechat-article-workflow/skills/*.md \
   ~/.agents/skills/

# 4. 验证安装
ls ~/.agents/skills/ | grep -E "hot-topics|six-thinking|humanize|copywriting"
```

### 方式二：通过 clawhub 安装（如已发布到 clawhub）

```bash
npx clawhub@latest install wechat-article-workflow
```

### 方式三：逐个安装所需技能

```bash
# 核心技能（必须）
npx clawhub@latest install hot-topics
npx clawhub@latest install six-thinking-hats
npx clawhub@latest install humanize-writing
npx clawhub@latest install marketing-psychology
npx clawhub@latest install copywriting

# 发布（必须）
npx clawhub@latest install wechat-publisher

# 调研（推荐）
npx clawhub@latest install deep-research
npx clawhub@latest install news-aggregator-skill

# AI 去味备用
npx clawhub@latest install ai-humanizer-2-1-0
```

## 环境配置（发布前必须）

### 1. 安装 wenyan-cli

```bash
npm install -g @wenyan-md/cli
wenyan --version  # 验证安装
```

### 2. 配置微信公众号凭证

```bash
# 在 ~/.bashrc 中添加：
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret

# 使配置生效
source ~/.bashrc
```

微信公众号凭证获取：微信公众平台 → 开发 → 基本配置

### 3. 配置 GitHub Token（推送更新时需要）

```bash
# 在 ~/.bashrc 中添加：
export GH_ORG_TOKEN_JORZRO="你的Token"

# 克隆仓库进行更新时：
git remote set-url origin \
  https://${GH_ORG_TOKEN_JORZRO}@github.com/Jorzro/MY-skills.git
```

## 工作流调用方式

### 完整流程（一句话启动）

```
用公众号文章工作流写一篇关于 [选题] 的文章。
```

### 分阶段调用

```bash
# STAGE 1：热点扫描
cat skills/hot-topics.md  # 读取指引，执行热点搜索

# STAGE 2：营销心理画像
cat skills/marketing-psychology.md

# STAGE 3：深度调研
cat skills/academic-deep-research.md
cat skills/deep-research.md

# STAGE 4：六帽分析
cat skills/six-thinking-hats.md

# STAGE 5：写作
cat skills/storytelling.md
cat skills/copywriting.md
# 读取 wechat-mp-writer 指引后执行写作

# STAGE 5.4：AI 去味
cat skills/humanize-writing.md

# STAGE 6：发布
./scripts/publish.sh article-final.md
```

## 工作流内部数据流

```
用户输入选题
    ↓
STAGE 1：热点搜索（hot-topics + x-twitter）
    → 输出：热点报告
    ↓
STAGE 2：选题确认 + 营销心理画像（marketing-psychology）
    → 输出：选题确认文件 + 读者画像
    ↓
STAGE 3：深度调研（academic-deep-research + deep-research + 新闻聚合）
    → 输出：调研报告（至少3个来源）
    ↓
STAGE 4：六帽分析（six-thinking-hats）
    → 输出：六帽分析结论
    ↓
STAGE 5：写作
    storytelling → copywriting → wechat-mp-writer
    → humanize-writing → ai-humanizer
    → 添加作者简介（绾绾）
    → 输出：article-final.md
    ↓
STAGE 6：质检（content-quality-auditor） → 发布（wechat-publisher）
    → 输出：草稿箱
```

## 重要路径约定

| 用途 | 路径 |
|------|------|
| 文章工作流主 Skill | `~/.openclaw/workspace/skills/wechat-article-workflow/SKILL.md` |
| 子技能 | `~/.agents/skills/{skill-name}/SKILL.md` |
| 文章输出目录 | `~/.openclaw/workspace-content/articles/{日期-选题}/` |
| 发布脚本 | `~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh` |

## 微信公众号发布格式要求

发布前，Markdown 文件**必须**包含以下 frontmatter：

```yaml
---
title: 文章标题
cover: ./cover.jpg
---
```

缺少 `cover` 会报错：`未能找到文章封面`

## 常见错误排查

| 错误 | 原因 | 解决 |
|------|------|------|
| `wenyan: command not found` | 未安装 wenyan-cli | `npm install -g @wenyan-md/cli` |
| `WECHAT_APP_ID is required` | 环境变量未设置 | `source ~/.bashrc` 后重试 |
| `ip not in whitelist` | IP 未加入白名单 | 微信公众平台 → 开发 → 基本配置 → IP白名单 |
| `未能找到文章封面` | frontmatter 缺少 cover | 添加 `cover: ./cover.jpg` |

## 参考资料

- OpenClaw 文档：https://docs.openclaw.ai
- ClawHub（Skill 市场）：https://clawhub.com
- wenyan-cli：https://github.com/caol64/wen-cli
- 微信公众号 API：https://developers.weixin.qq.com/doc/offiaccount/
