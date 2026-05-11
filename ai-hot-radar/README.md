# AI Hot Radar

AI Hot Radar 是一个面向 OpenClaw / Codex / Claude Code / Cursor 等 Agent 的 AI 资讯热点 skill。

它会直接抓取公开 AI 资讯源，融合 `AI HOT`、精选 AI RSS 和 GitHub AI 趋势，对资讯做去重、聚合和 `0-100` 分重要度评分，并通过 Markdown 文件把历史播报记录外化保存下来。

这个版本不需要自建后端、不需要数据库、不需要 API Key。只要求 Agent 能联网，并能在自己的持久化空间里读写文件。

## 能做什么

- 查询“今天 AI 圈有什么”“最近 24 小时最重磅 AI 新闻”“OpenAI 最近发了什么”。
- 自动抓取 `AI HOT`、官方/高质量 AI RSS、GitHub AI 开源趋势。
- 对同一事件做去重和合并，避免重复播报。
- 给每条资讯打 `0-100` 分，并说明为什么重要。
- 支持早报、晚报、重大快讯三类 OpenClaw 心跳。
- 把历史记录写入 `ledger.md`，下次心跳时自动跳过已播报内容。
- 允许用户通过 `interests.md` 写关注方向和负向过滤词。

## 目录结构

```text
ai-hot-radar/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── scoring-rubric.md
    └── source-map.md
```

## 安装

把整个 `ai-hot-radar` 文件夹放到你的 Agent skill 目录里。

常见位置示例：

```text
~/.openclaw/skills/ai-hot-radar/
~/.codex/skills/ai-hot-radar/
~/.claude/skills/ai-hot-radar/
```

如果你的平台使用的是技能市场或上传式安装，把这个目录作为一个完整 skill 包上传即可。

## 基础用法

安装后可以直接这样问：

```text
今天 AI 圈有什么？
```

```text
最近 24 小时最重磅 AI 新闻，按重要程度打分。
```

```text
OpenAI 最近发了什么？
```

```text
最近一周 AI 论文里哪些值得看？
```

```text
查看最近已播报记录。
```

## OpenClaw 心跳用法

推荐配置三类心跳。

早报：

```text
使用 ai-hot-radar 执行早报心跳。
```

晚报：

```text
使用 ai-hot-radar 执行晚报心跳。
```

重大快讯：

```text
使用 ai-hot-radar 执行重大快讯心跳，只在有 90 分以上新增事件时输出。
```

默认策略：

- `08:30` 早报：过去 12 小时，输出新增重点资讯。
- `20:30` 晚报：过去 24 小时，输出完整总结。
- 每 2 小时重大快讯：只播报 `90` 分以上且未播报过的新增事件。

## 记忆文件

skill 默认使用这个目录保存状态：

```bash
$HOME/.openclaw/skills/ai-hot-radar/memory
```

可通过环境变量覆盖：

```bash
AI_HOT_RADAR_MEMORY_ROOT=/path/to/persistent/memory
```

首次运行时会创建：

```text
memory/
├── ledger.md
├── interests.md
└── briefings/
```

`ledger.md` 是长期账本，记录每个事件的指纹、标题、首次发现时间、最近发现时间、分数、分类、来源、播报时间和状态。

`briefings/` 保存每次早报、晚报和重大快讯内容。

`interests.md` 用来写你的关注方向和负向过滤词，例如：

```markdown
# AI Hot Radar Interests

## Focus
- AI agents
- frontier models
- developer tools
- open source AI projects

## Negative Filters
- generic prompt tips
- old tutorials without new release information
```

## 数据源

主数据源：

- `AI HOT`: `https://aihot.virxact.com`

补充 RSS：

- OpenAI News
- Google DeepMind Blog
- Google AI
- The Decoder
- Latent Space
- MarkTechPost
- Anthropic / Hugging Face / Mistral / Meta AI 等尝试源

补充开源趋势：

- GitHub Search API

详细数据源定义见 `references/source-map.md`。

## 评分规则

每条资讯最终得到 `0-100` 分。

规则底座共 `80` 分：

- 来源权威性：`0-15`
- 事件级别：`0-20`
- 与 AI 核心相关度：`0-15`
- 影响范围：`0-10`
- 时效性：`0-10`
- 多源印证/是否被精选：`0-10`

Agent 语义校正共 `20` 分：

- 是否改变行业预期
- 是否是正式发布而非传闻
- 是否值得创业者/开发者立即关注
- 是否有明确行动价值

分数解释：

- `90-100`: 爆炸级，适合重大快讯。
- `75-89`: 重磅，优先进入早晚报头部。
- `60-74`: 重点，进入正常简报。
- `40-59`: 一般，只在完整列表里展示。
- `<40`: 默认忽略。

详细评分表见 `references/scoring-rubric.md`。

## 去重逻辑

skill 会把不同来源中的同一事件合并成一条。

合并依据包括：

- 规范化标题
- 链接域名和路径
- 公司名、模型名、产品名
- 发布时间窗口

同一事件的主条目优先级：

1. `AI HOT selected`
2. 官方一手来源
3. 高质量 AI 媒体或 newsletter
4. GitHub 趋势
5. 社交平台转述

## 容错

- `AI HOT` 返回 403 时，skill 会用浏览器 `User-Agent` 重试。
- 单个 RSS 源失败时直接跳过。
- GitHub API 被限流时跳过开源趋势部分。
- 如果重大快讯心跳没有新内容，不输出打扰消息，只更新账本。

## 适用范围

完整使用需要 Agent 支持：

- 读取标准 `SKILL.md`
- 联网请求公开 URL
- 持久化读写 Markdown 文件

如果某个 Agent 只能读取提示词，不能联网或不能写文件，也可以参考 `SKILL.md` 里的流程，但无法完整实现心跳去重和历史记忆。

## License

MIT
