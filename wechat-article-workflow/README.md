# 公众号文章 AI 写作工作流

> 从热点发现到公众号草稿箱发布，全自动跑完，不需要人工拼接。

**仓库地址：** https://github.com/Jorzro/MY-skills/tree/main/wechat-article-workflow

---

## 快速开始（3 步上手）

### 第一步：克隆仓库

```bash
git clone https://github.com/Jorzro/MY-skills.git ~/MY-skills
cd ~/MY-skills/wechat-article-workflow
```

### 第二步：一键安装

```bash
bash install.sh
```

安装脚本会自动把主工作流、13 个子技能、发布脚本全部复制到正确位置。

### 第三步：配置凭证

```bash
# 在 ~/.bashrc 中添加：
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret

# 安装发布工具：
npm install -g @wenyan-md/cli

# 使配置生效：
source ~/.bashrc
```

### 第四步：开始写文章

```
用公众号文章工作流，写一篇关于 [你的选题] 的文章
```

---

## 安装方式选择

### 方式一：本仓库一键安装（最推荐）
```bash
git clone https://github.com/Jorzro/MY-skills.git ~/MY-skills
cd ~/MY-skills/wechat-article-workflow
bash install.sh
```
**优点**：无需网络，不依赖任何平台，clone 即可用。

### 方式二：腾讯 Skill 市场安装（国内用户推荐）
访问 https://skillhub.tencent.com/ 搜索安装。

### 方式三：ClawHub 安装（可能限速）
```bash
npx clawhub@latest install wechat-article-workflow
```
> ⚠️ 注意：ClawHub（clawhub.com）近期限流，建议优先使用方式一或方式二。

---

## 工作流 6 阶段

```
STAGE 1：热点发现（hot-topics）
    ↓
STAGE 2：选题确认 + 读者心理（marketing-psychology）
    ↓
STAGE 3：深度调研（academic-deep-research + deep-research）
    ↓
STAGE 4：六帽分析（six-thinking-hats）
    ↓
STAGE 5：写作（storytelling → copywriting → wechat-mp-writer → 去味 → 加署名）
    ↓
STAGE 6：质检 + 发布（content-quality-auditor → wechat-publisher）
```

---

## 目录结构

```
wechat-article-workflow/
├── README.md                 # 本文档
├── CLAUDE.md                # AI Agent 使用指南
├── SKILL.md                 # 工作流主 Skill
├── install.sh               # ⭐ 一键安装脚本（运行这个即可）
├── scripts/
│   └── publish.sh           # 微信公众号发布脚本
└── skills/                  # 13 个子技能
    ├── hot-topics/
    ├── six-thinking-hats/
    ├── humanize-writing/
    ├── marketing-psychology/
    ├── copywriting/
    ├── deep-research/
    ├── content quality-auditor/
    ├── storytelling/
    ├── ai-humanizer/
    ├── news-aggregator/
    ├── wechat-article-scraper/
    ├── academic-deep-research/
    ├── wechat-mp-writer/
    └── x-twitter/
```

---

## 依赖 Skill

| Skill | 用途 | 安装到 |
|-------|------|--------|
| `hot-topics` | 热点扫描 | `~/.agents/skills/` |
| `x-twitter` | 国际热点 | `~/.agents/skills/` |
| `marketing-psychology` | 读者心理 | `~/.agents/skills/` |
| `deep-research` | 企业调研 | `~/.agents/skills/` |
| `news-aggregator` | 新闻聚合 | `~/.agents/skills/` |
| `wechat-article-scraper` | 微信爬虫 | `~/.agents/skills/` |
| `six-thinking-hats` | 六帽分析 | `~/.agents/skills/` |
| `copywriting` | 文案框架 | `~/.agents/skills/` |
| `humanize-writing` | AI 去味 | `~/.agents/skills/` |
| `content quality-auditor` | 内容质检 | `~/.openclaw/workspace/skills/` |
| `storytelling` | 故事框架 | `~/.openclaw/workspace/skills/` |
| `ai-humanizer` | 二次去味 | `~/.openclaw/workspace/skills/` |
| `academic-deep-research` | 学术调研 | `~/.openclaw/workspace/skills/` |
| `wechat-mp-writer` | 正文写作 | `~/.openclaw/workspace/skills/` |
| `wechat-publisher` | 发布脚本 | `~/.openclaw/workspace/skills/` |

---

## 常见问题

### Q1：发布报错 "ip not in whitelist"
**解决**：登录微信公众平台 → 开发 → 基本配置 → IP白名单 → 添加你的公网 IP

### Q2：报错 "未能找到文章封面"
**解决**：确保 Markdown 文件顶部有完整 frontmatter：
```yaml
---
title: 文章标题
cover: ./cover.jpg
---
```

### Q3：wenyan-cli 安装失败
```bash
npm install -g @wenyan-md/cli
```

---

## 如何贡献

欢迎提交 Issue 和 Pull Request！

---

**维护者**：Jorzro  
**版本**：v1.1（可一键安装）  
**最后更新**：2026-03-27
