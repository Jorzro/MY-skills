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

### 第二步：一键安装（全部自动）

```bash
bash install.sh
```

> install.sh 会自动完成：
> - 安装全局工具（wenyan-cli）
> - 安装主工作流 SKILL
> - 安装热点扫描脚本
> - 安装发布脚本
> - 安装 14 个子技能到正确路径
> - 安装各技能需要的 npm / Python 依赖

### 第三步：配置凭证 + 开始写文章

```bash
# 在 ~/.bashrc 中添加：
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret
source ~/.bashrc

# 然后发送这句话给 AI：
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
> ⚠️ ClawHub（clawhub.com）近期限流，建议优先使用方式一或方式二。

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
│   ├── publish.sh           # 微信公众号发布脚本
│   └── daily-hot-topics.js # 热点扫描脚本
└── skills/                  # 14 个子技能（每个是独立目录）
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

## 环境要求

| 项目 | 最低版本 | 说明 |
|------|-----------|------|
| Node.js | ≥ 18.0 | 用于热点脚本和部分技能 |
| Python | ≥ 3.10 | 用于深度调研和新闻聚合技能 |
| npm | ≥ 9.0 | 安装全局工具和技能依赖 |

> install.sh 会自动检查并安装 `wenyan-cli`（npm 全局工具），
> 其余依赖（npm / Python 包）也会在安装过程中自动处理。

---

## 子技能安装路径

| Skill | 安装到 |
|-------|--------|
| `hot-topics` | `~/.agents/skills/` |
| `x-twitter` | `~/.agents/skills/` |
| `marketing-psychology` | `~/.agents/skills/` |
| `deep-research` | `~/.agents/skills/` |
| `news-aggregator` | `~/.agents/skills/` |
| `wechat-article-scraper` | `~/.agents/skills/` |
| `six-thinking-hats` | `~/.agents/skills/` |
| `copywriting` | `~/.agents/skills/` |
| `humanize-writing` | `~/.agents/skills/` |
| `content quality-auditor` | `~/.openclaw/workspace/skills/` |
| `storytelling` | `~/.openclaw/workspace/skills/` |
| `ai-humanizer` | `~/.openclaw/workspace/skills/` |
| `academic-deep-research` | `~/.openclaw/workspace/skills/` |
| `wechat-mp-writer` | `~/.openclaw/workspace/skills/` |
| `wechat-publisher` | `~/.openclaw/workspace/skills/` |

---

## 常见问题

### Q1：发布报错 "ip not in whitelist"
**解决**：微信公众平台 → 开发 → 基本配置 → IP白名单 → 添加你的公网 IP（用 `curl ifconfig.me` 查）

### Q2：报错 "未能找到文章封面"
**解决**：Markdown 文件顶部 frontmatter 必须包含：
```yaml
---
title: 文章标题
cover: ./cover.jpg
---
```

### Q3：install.sh 报某技能 npm install 失败
**解决**：手动进入该技能目录运行 `npm install`，或确保 Node.js 版本 ≥ 18.0

### Q4：热点扫描脚本报错
**解决**：
```bash
node ~/.openclaw/workspace-content/scripts/daily-hot-topics.js
```
确保 Node.js ≥ 18.0。

---

## 如何贡献

欢迎提交 Issue 和 Pull Request！

---

**维护者**：Jorzro  
**版本**：v1.2（含一键安装）  
**最后更新**：2026-03-27
