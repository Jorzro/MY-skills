# 公众号文章 AI 写作工作流

> 一套从**热点发现**到**公众号草稿箱发布**的全自动文案生产系统。16 个 AI Skill 串联成流水线，无需手动拼接，写完即发布。

**仓库地址：** https://github.com/Jorzro/MY-skills/tree/main/wechat-article-workflow

---

## 目录

- [特性](#特性)
- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [工作流 6 阶段详解](#工作流-6-阶段详解)
- [Skill 清单与分工](#skill-清单与分工)
- [完整工作流产物](#完整工作流产物)
- [常见问题](#常见问题)
- [如何贡献](#如何贡献)

---

## 特性

- ✅ **全流程自动化**：热点搜索 → 选题 → 调研 → 六帽分析 → 写作 → 发布，6 个阶段全自动跑完
- ✅ **16 个专业 Skill 串联**：每个阶段由专项 AI Skill 负责
- ✅ **AI 去味**：自动消除 ChatGPT 写作痕迹，读起来像真人写的
- ✅ **一键发布**：直接推送到微信公众号草稿箱，无需手动复制粘贴
- ✅ **质检门控**：错别字 + 敏感词 + 可读性，发布前自动检查

---

## 系统要求

| 项目 | 要求 |
|------|------|
| Node.js | ≥ 18.0 |
| npm | ≥ 9.0 |
| Python | ≥ 3.10 |
| OpenClaw | 已安装并配置 |
| 微信公众号 | 已开通，AppID + AppSecret |

### 微信公众号凭证配置

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **开发 → 基本配置**，获取 AppID 和 AppSecret
3. 将服务器公网 IP 添加到 **IP 白名单**
4. 在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret
```

然后执行 `source ~/.bashrc` 使配置生效。

---

## 快速开始

### 第一步：安装 wenyan-cli

```bash
npm install -g @wenyan-md/cli
```

### 第二步：安装 OpenClaw + Skill 生态

确保 OpenClaw 已安装。然后将本仓库克隆到本地：

```bash
git clone https://github.com/Jorzro/MY-skills.git
cd MY-skills/wechat-article-workflow
```

### 第三步：配置微信公众号凭证

```bash
# 编辑配置文件
nano ~/.bashrc
# 添加：
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret

source ~/.bashrc
```

### 第四步：启动工作流

在支持 OpenClaw Skill 调用的 AI Agent 中，发送以下提示词即可启动完整流程：

```
帮我用公众号文章工作流写一篇关于[你的选题]的公众号文章。
```

工作流会自动执行以下步骤：
1. 扫描多平台热点
2. 确认选题方向 + 分析读者心理
3. 深度调研，整理事实依据
4. 六顶思考帽分析，把逻辑想透
5. 写出完整正文 + AI 去味
6. 自动质检 + 发布到草稿箱

---

## 工作流 6 阶段详解

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1：热点发现                                            │
│  hot-topics（中文6平台）+ x-twitter（国际平台）              │
│  扫描微博 / 知乎 / 抖音 / B站 / 今日头条 / 百度热搜         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2：选题确认 + 营销心理画像                              │
│  用户选定话题 → marketing-psychology 分析目标读者             │
│  输出：目标读者 / 核心痛点 / 情绪触发点                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3：深度调研                                            │
│  academic-deep-research（学术级）+ deep-research             │
│  + wechat-article-scraper + news-aggregator                │
│  至少 3 个可信来源才能进入下一阶段                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4：六顶思考帽分析                                      │
│  six-thinking-hats                                          │
│  🤍事实 ❤️情感 🖤风险 💛价值 💚创意 🔵行动                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5：文章写作（6步）                                    │
│  storytelling → copywriting → wechat-mp-writer            │
│  → humanize-writing → ai-humanizer → 加作者简介              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 6：质检 + 发布                                        │
│  content-quality-auditor → wechat-publisher → 草稿箱       │
└─────────────────────────────────────────────────────────────┘
```

---

## Skill 清单与分工

| Skill | 阶段 | 作用 |
|-------|------|------|
| `hot-topics` | STAGE 1 | 中文 6 平台热点扫描（微博/知乎/抖音/B站/头条/百度） |
| `x-twitter` | STAGE 1/3 | 国际热点搜索（Twitter/YouTube/Reddit） |
| `marketing-psychology` | STAGE 2 | 读者心理画像：痛点、情绪、心智模型 |
| `academic-deep-research` | STAGE 3 | 学术级深度调研，APA 引用，证据分级 |
| `deep-research` | STAGE 3 | 企业级多源综合研究 |
| `wechat-article-scraper` | STAGE 3 | 爬取竞品微信公众号文章 |
| `news-aggregator` | STAGE 3 | 新闻聚合（HN/GitHub/36Kr/腾讯新闻等） |
| `six-thinking-hats` | STAGE 4 | 六顶思考帽：6 维度想透选题逻辑 |
| `storytelling` | STAGE 5 | 故事叙述框架：开场/叙事弧线/情感高潮/结尾 |
| `copywriting` | STAGE 5 | 专业文案框架：标题/开头/结构/CTA |
| `wechat-mp-writer` | STAGE 5 | 公众号文章核心写作引擎 |
| `humanize-writing` | STAGE 5 | AI 去味：消除 ChatGPT 写作痕迹 |
| `ai-humanizer` | STAGE 5 | AI 去味备用方案（二次优化） |
| `content-quality-auditor` | STAGE 6 | 质检：错别字/敏感词/可读性/标题吸引力 |
| `wechat-publisher` | STAGE 6 | 一键发布 Markdown 到微信公众号草稿箱 |

---

## 完整工作流产物

每篇文章执行完后，会产生以下文件（保存在 `~/.openclaw/workspace-content/articles/{日期-选题}/`）：

```
├── 01-hot-topics-report.md      # 热点扫描报告
├── 02-topic-confirmed.md        # 选题确认 + 心理画像
├── 03-research-report.md        # 深度调研报告
├── 04-six-hats-analysis.md     # 六帽分析
├── 05-story-outline.md          # 故事线
├── 06-copy-framework.md         # 文案框架
├── 07-article-draft.md          # 文章初稿
├── 08-article-polished.md       # AI 去味后版本
├── 09-article-final.md          # 最终可发布版本（含作者简介）
├── 10-quality-report.md         # 质检报告
├── cover.jpg                   # 封面图
└── ending-poster.jpg           # 结尾配图
```

---

## 常见问题

### Q1：发布时报错 "ip not in whitelist"

**原因**：服务器公网 IP 未加入微信公众号后台白名单。

**解决方法**：
```bash
# 获取你的公网 IP
curl ifconfig.me

# 登录微信公众平台 → 开发 → 基本配置 → IP白名单 → 添加你的 IP
```

### Q2：发布时报错 "未能找到文章封面"

**原因**：Markdown 文件顶部 frontmatter 缺少 `cover` 字段。

**解决方法**：确保文件开头有完整 frontmatter：

```yaml
---
title: 文章标题
cover: ./cover.jpg
---
```

### Q3：wenyan-cli 安装失败

```bash
# 先检查 Node.js 版本
node --version  # 需要 ≥ 18.0

# 再重新安装
npm install -g @wenyan-md/cli
```

### Q4：credential helper 配置失败

**安装 Git Credential Helper**：
```bash
npm install -g @open-sauced/opensauced-pw
gh auth login
```

---

## 如何贡献

本工作流基于 [OpenClaw](https://github.com/openclaw/openclaw) 构建，Skill 生态基于 [ClawHub](https://clawhub.com)。

欢迎提交 Issue 和 Pull Request！

### 贡献流程

1. Fork 本仓库
2. 创建分支 (`git checkout -b feature/你的功能`)
3. 提交更改
4. 推送到你的 Fork
5. 提交 Pull Request

---

## 许可证

MIT License

---

**维护者**：Jorzro  
**版本**：v1.0  
**最后更新**：2026-03-26
