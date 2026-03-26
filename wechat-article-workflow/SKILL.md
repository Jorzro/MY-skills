---
name: wechat-article-workflow
description: 公众号文章全流程 AI 写作工作流。从热点发现、深度调研、六帽分析、写作到公众号草稿箱发布的完整自动化流水线。触发词：「写公众号文章」「用工作流写」「帮我写一篇公众号」「用AI写公众号」
version: 1.0.0
tags: [wechat, writing, automation, article, workflow, content]
---

# 公众号文章 AI 写作工作流

从热点发现到公众号草稿箱发布，全自动跑完，不需要人工拼接。

## When to Use

用户说以下内容时，调用本技能：

- "帮我写一篇公众号文章"
- "写一篇关于 XXX 的公众号"
- "用工作流写篇文章"
- "用 AI 写公众号文章"
- "写篇公众号选题 XXX"

## How to Use

### 完整流程（一句话启动）

```
用公众号文章工作流，写一篇关于 [选题] 的公众号文章
```

### 分 6 阶段执行

**STAGE 1 — 热点扫描**
- 调用 `hot-topics`：扫描微博/抖音/B站/知乎/头条/百度热搜
- 命令：`node ~/.openclaw/workspace-content/scripts/daily-hot-topics.js`
- 或：直接用 `xreach search` 搜国际热点

**STAGE 2 — 选题确认**
- 呈现热点列表给用户选择
- 调用 `marketing-psychology` 做读者心理画像

**STAGE 3 — 深度调研**
- 按优先级调用：
  - `academic-deep-research`（学术级调研）
  - `deep-research`（企业级调研）
  - `wechat-article-scraper`（竞品微信文章）
  - `news-aggregator`（新闻聚合）
- **门控**：至少 3 个可信来源才能进入下一阶段

**STAGE 4 — 六帽分析**
- 调用 `six-thinking-hats`
- 6 个维度：🤍事实 ❤️情感 🖤风险 💛价值 💚创意 🔵行动
- **输出**：写作方向 + 文章结构 + 核心观点

**STAGE 5 — 写作（5步）**
1. `storytelling` — 故事框架
2. `copywriting` — 文案框架（标题/开头/CTA）
3. `wechat-mp-writer` — 写完整正文
4. `humanize-writing` — 去 AI 味
5. `ai-humanizer` — 二次优化（如需要）

**STAGE 5.6 — 加作者简介（必须！不可跳过）**
```
🎨 本文作者：绾绾
AI内容创作助手 | 要么不写，写就写进心里 💖
```

**STAGE 6 — 质检 + 发布**
1. `content-quality-auditor` — 错别字 / 敏感词 / 可读性检查
2. `wechat-publisher` — 一键推送草稿箱

### 发布命令

```bash
~/.openclaw/workspace/skills/wechat-publisher/scripts/publish.sh article-final.md
```

### 环境要求

- Node.js ≥ 18.0（热点脚本用）
- `wenyan-cli`（发布用）：`npm install -g @wenyan-md/cli`
- 环境变量：`WECHAT_APP_ID` + `WECHAT_APP_SECRET`

### 微信公众号 frontmatter 格式

文章文件顶部必须包含：

```yaml
---
title: 文章标题
cover: ./cover.jpg
---
```

## 产物存储目录

```
~/.openclaw/workspace-content/articles/{YYYY-MM-DD-选题}/
├── 01-hot-topics-report.md      # 热点报告
├── 02-topic-confirmed.md        # 选题确认
├── 03-research-report.md        # 调研报告
├── 04-six-hats-analysis.md     # 六帽分析
├── 07-article-draft.md         # 初稿
├── 08-article-polished.md      # 去味版
├── 09-article-final.md          # 终稿（含作者简介）
└── 10-quality-report.md         # 质检报告
```

## 依赖 Skill

本工作流调用以下子技能（需已安装）：

> 💡 国内用户推荐使用 [腾讯 Skill 市场](https://skillhub.tencent.com/) 安装，访问稳定不限流。ClawHub（clawhub.com）近期限流，可作为备选。

| Skill | 用途 | 安装源 |
|-------|------|--------|
| `hot-topics` | 热点扫描 | 腾讯 Skill 市场 / ClawHub |
| `x-twitter` | 国际热点 | 腾讯 Skill 市场 / ClawHub |
| `marketing-psychology` | 读者心理 | 腾讯 Skill 市场 / ClawHub |
| `academic-deep-research` | 学术调研 | 腾讯 Skill 市场 / ClawHub |
| `deep-research` | 企业调研 | 腾讯 Skill 市场 / ClawHub |
| `wechat-article-scraper` | 微信爬虫 | 腾讯 Skill 市场 / ClawHub |
| `news-aggregator` | 新闻聚合 | 腾讯 Skill 市场 / ClawHub |
| `six-thinking-hats` | 六帽分析 | 腾讯 Skill 市场 / ClawHub |
| `storytelling` | 故事框架 | 腾讯 Skill 市场 / ClawHub |
| `copywriting` | 文案框架 | 腾讯 Skill 市场 / ClawHub |
| `wechat-mp-writer` | 正文写作 | 腾讯 Skill 市场 / ClawHub |
| `humanize-writing` | AI 去味 | 腾讯 Skill 市场 / ClawHub |
| `ai-humanizer` | 二次去味 | 腾讯 Skill 市场 / ClawHub |
| `content quality-auditor` | 内容质检 | 腾讯 Skill 市场 / ClawHub |
| `wechat-publisher` | 发布脚本 | 腾讯 Skill 市场 / ClawHub |


## 注意事项

1. **不可跳过 STAGE 5.6**：绾绾署名必须加，否则文章没有作者标识
2. **STAGE 3 有门控**：调研来源 < 3 个时，返回补充调研
3. **发布前确认 frontmatter**：缺少 `cover` 会导致微信报错
4. **先质检再发布**：不质检直接发布有风险
