# CLAUDE.md — AI Agent 使用说明

> 本文件供 AI Agent 阅读。当 AI 进入本仓库时，会自动读取此文件了解如何操作。

## 快速开始

这是一个**公众号文章 AI 写作工作流**的技能集合。AI Agent 可以通过 OpenClaw 的 Skill 机制调用本仓库的各个技能。

## 目录结构

```
wechat-article-workflow/
├── README.md              # 人类可读的使用文档
├── SKILL.md               # 工作流主 Skill（OpenClaw 可直接调用）
└── skills/                # 各子技能目录
    ├── hot-topics.md
    ├── six-thinking-hats.md
    ├── humanize-writing.md
    ├── marketing-psychology.md
    ├── copywriting.md
    ├── deep-research.md
    ├── content-quality-auditor.md
    ├── storytelling.md
    ├── ai-humanizer.md
    ├── news-aggregator.md
    ├── wechat-article-scraper.md
    ├── academic-deep-research.md
    └── scripts/
        └── publish.sh     # 微信公众号发布脚本
```

## 如何使用

### 方式一：直接调用完整工作流

在支持 OpenClaw 的 AI 对话中发送：

```
用公众号文章工作流写一篇关于 [你的选题] 的文章
```

AI 会自动执行完整的 6 阶段流程。

### 方式二：分阶段调用

```
# STAGE 1：热点扫描
读取 skills/hot-topics.md，按其中的指引执行热点搜索

# STAGE 2：营销心理画像
读取 skills/marketing-psychology.md，按其中的指引分析读者

# STAGE 3：深度调研
读取 skills/academic-deep-research.md，执行调研流程

# STAGE 4：六帽分析
读取 skills/six-thinking-hats.md，执行六顶思考帽分析

# STAGE 5：写作
依次读取：
- skills/storytelling.md（故事框架）
- skills/copywriting.md（文案框架）
- skills/wechat-mp-writer.md（正文写作）
- skills/humanize-writing.md（AI 去味）

# STAGE 6：发布
读取 scripts/publish.sh，按其中的说明配置微信公众号凭证并发布
```

## 微信公众号发布配置

发布前必须配置环境变量：

```bash
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret
```

然后运行发布脚本：

```bash
./scripts/publish.sh 你的文章.md
```

## 参考资料

- OpenClaw 文档：https://docs.openclaw.ai
- ClawHub（Skill 市场）：https://clawhub.com
- wenyan-cli（Markdown 转微信公众号）：https://github.com/caol64/wen-cli
