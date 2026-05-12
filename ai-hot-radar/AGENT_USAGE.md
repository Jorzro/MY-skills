# AI Hot Radar — Agent Skill 使用手册

让 Agent 用自然中文查询最新 AI 资讯，并自动完成抓取、去重、聚合、`0-100` 分重要度评分、中文编辑型简报、早晚报、重大快讯记忆和热点海报 prompt。

本 skill 融合 `AI HOT`、精选 AI RSS 和 GitHub AI 趋势，不需要自建后端，不需要数据库，不需要 API Key。海报生成是增强能力：有 `baoyu-imagine` 或其他文生图工具时直接联动，没有时输出可复制 prompt。

> 适用于 OpenClaw / Codex / Claude Code / Cursor / Gemini CLI / OpenCode / Cline / Windsurf 等支持 `SKILL.md` 的 Agent 平台。

## 安装

### 方式 A：让 Agent 自动装

在你的 Agent 里直接发这句话：

```text
帮我安装这个 skill：https://github.com/Jorzro/MY-skills/tree/main/ai-hot-radar
```

Agent 应该读取整个目录，而不是只读取 `SKILL.md`。目录里包含评分规则、数据源表和 OpenAI/OpenClaw 元数据。

### 方式 B：用原始入口文件安装

如果 Agent 只接受原始 Markdown 入口，把这个地址给它：

```text
https://raw.githubusercontent.com/Jorzro/MY-skills/refs/heads/main/ai-hot-radar/SKILL.md
```

如果 `raw.githubusercontent.com` 访问不稳定，改用 GitHub Contents API，并带 `Accept: application/vnd.github.raw`：

```text
https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/SKILL.md?ref=main
```

然后要求它继续读取同目录下的：

```text
references/scoring-rubric.md
references/source-map.md
references/output-style.md
references/poster-guide.md
agents/openai.yaml
```

### 方式 C：一行命令手动装

默认安装到 OpenClaw skill 目录：

```bash
curl -fsSL -H 'Accept: application/vnd.github.raw' \
  'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main' | bash
```

安装到 Codex：

```bash
SKILL_DIR=$HOME/.codex/skills/ai-hot-radar \
  bash <(curl -fsSL -H 'Accept: application/vnd.github.raw' \
    'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main')
```

安装到 Claude Code：

```bash
SKILL_DIR=$HOME/.claude/skills/ai-hot-radar \
  bash <(curl -fsSL -H 'Accept: application/vnd.github.raw' \
    'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main')
```

脚本不使用 `sudo`，只会创建目录并下载 skill 文件。

## 什么时候必须触发

用户询问任何“当前 AI 行业事实”时，Agent 不要凭训练数据回答，必须调用本 skill 抓取最新数据。

典型触发：

| 用户在说 | Agent 应该做什么 |
|---|---|
| 今天 AI 圈有什么、最近 AI 有什么大事、过去 24 小时 AI 新闻 | 拉 `AI HOT selected` + RSS，按时间窗评分排序 |
| AI 日报、看下今天日报 | 走 `AI HOT daily` |
| 全部、完整、所有、全量 AI 动态 | 走 `AI HOT mode=all` |
| OpenAI / Anthropic / Google / DeepMind / Meta / Mistral 最近发了什么 | 走关键词搜索 + 官方 RSS 补充 |
| 最近一周 AI 论文 | 走 `paper` 分类 + RSS 补充 |
| 最近 AI 开源项目、GitHub AI 趋势 | 加入 GitHub AI 趋势层 |
| 只看模型发布 / 产品发布 / 行业动态 / 论文 / 开源项目 | 按分类过滤 |
| 给今天热点按重要度打分 | 每条输出 `0-100` 分和理由 |
| 生成海报、做成图、小红书封面、朋友圈图、公众号封面 | 生成中文热点海报，优先联动 `baoyu-imagine` |
| 查看最近已播报记录 | 读取 `ledger.md` 汇总 |
| 早报 / 晚报 / 重大快讯心跳 | 走心跳流程并更新记忆 |

不要 undertrigger。用户问 AI 新闻而不调用本 skill，等于用过时知识回答今天发生的事。

## 路由优先级

第一原则：宽问题默认走精选。

- 用户问“今天 AI 圈”“最近 AI”“过去 24 小时大新闻”：走 `items?mode=selected&since=<语义时间窗>`。
- 只有用户明确说“日报”：才走 `daily`。
- 只有用户明确说“全部 / 完整 / 所有 / 全量”：才走 `mode=all`。
- 用户说公司、模型、产品名：走 `q=<关键词>`，再用 RSS 补洞。
- 用户说“开源 / GitHub / 项目趋势”：加入 GitHub AI 趋势。
- 用户说“只看我关心的方向”：读取 `interests.md` 做过滤和加权。
- 用户说“海报 / 做成图 / 小红书 / 朋友圈 / 公众号封面”：先生成中文编辑稿，再走海报模式。

## 数据源

主源：

```text
https://aihot.virxact.com
```

AI HOT API 调用 `/api/public/*` 时必须带浏览器 `User-Agent`，否则可能 403：

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&take=50"
```

补充源：

- OpenAI News
- Google DeepMind Blog
- Google AI
- The Decoder
- Latent Space
- MarkTechPost
- Anthropic / Hugging Face / Mistral / Meta AI 尝试源
- GitHub Search API，用于开源趋势

详细源表见 `references/source-map.md`。

## 工作流

### 默认：今天 AI 圈有什么

```bash
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&since=$since&take=50"
```

然后拉取 RSS 补充源，归一化、去重、评分，输出最高分 3-5 条。

输出前必须做中文编辑：英文标题和摘要不能直接当主标题展示，要翻译并改写成自然中文标题。完整规范见 `references/output-style.md`。

### 日报：用户明确说“日报”

```bash
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

不要把“过去 24 小时”误判成日报。日报是固定日切片，宽问题应该走滚动时间窗。

### 公司或主题：OpenAI 最近发了什么

```bash
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?q=OpenAI&take=30"
```

再补 OpenAI 官方 RSS，并合并同一事件。

### 分类：最近一周 AI 论文

```bash
since=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&category=paper&since=$since&take=100"
```

分类对照：

| 用户分类 | API category |
|---|---|
| 模型发布/更新 | `ai-models` |
| 产品发布/更新 | `ai-products` |
| 行业动态 | `industry` |
| 论文研究 | `paper` |
| 技巧与观点 | `tip` |
| 开源项目 | GitHub 趋势层 |

## 去重与主条目选择

同一事件只输出一条，其他来源放入“来源”列表。

合并依据：

- 规范化标题。
- URL 域名和路径。
- 公司名、模型名、产品名。
- 发布时间窗口。

同一个 canonical URL 必须合并，即使一个来源是中文标题、另一个来源是英文标题。

主条目优先级：

1. `AI HOT selected`
2. 官方一手来源
3. 高质量媒体或 newsletter
4. GitHub 趋势
5. 社交平台转述

## 评分规则

每条资讯必须给 `0-100` 分。

规则底座 `80` 分：

- 来源权威性：`0-15`
- 事件级别：`0-20`
- AI 核心相关度：`0-15`
- 影响范围：`0-10`
- 时效性：`0-10`
- 多源印证/精选信号：`0-10`

Agent 语义校正 `20` 分：

- 是否改变行业预期。
- 是否正式发布，而不是传闻。
- 是否值得创业者或开发者立即关注。
- 是否有明确行动价值。

分数段：

| 分数 | 含义 |
|---:|---|
| `90-100` | 爆炸级，必须进入重大快讯 |
| `75-89` | 重磅，早晚报头部 |
| `60-74` | 重点，正常列表 |
| `40-59` | 一般，只在完整列表展示 |
| `<40` | 默认忽略 |

详细评分见 `references/scoring-rubric.md`。

分类时要避免关键词误判：安全事故、诉讼、监管、政策、融资、合作和企业采用归到“行业动态”，即使标题里出现 ChatGPT、Claude、Gemini 等模型名；只有真正的模型发布、模型更新、能力变化或模型可用性事件才归到“模型发布/更新”。

## 中文简报格式

默认输出：

```markdown
时间窗：<开始时间> - <结束时间>

# 今日 AI 热点雷达

## 今日判断
<用一段中文总结今天 AI 圈主要趋势>

## 最值得看
1. **<分数>/100｜<中文标题>**
   一句话：<一句中文结论>
   为什么重要：<影响判断>
   适合谁关注：<创业者/开发者/产品团队/研究者/投资人>
   来源：<链接>
```

每条资讯必须用中文标题和中文判断。除非用户明确要求，不要把英文原始标题放在主展示位。

## 海报模式

触发词：

```text
生成海报
做成图
小红书封面
朋友圈图
公众号封面
今日 AI 热点海报
把前三条做成一张图
```

流程：

1. 先生成中文编辑型简报。
2. 选 Top 3-5 条做海报内容。
3. 读取 `preferences.md`，默认比例 `9:16`，风格 `editorial-tech`，图像 skill `baoyu-imagine`。
4. 如果当前 Agent 已安装 `baoyu-imagine` 或有文生图工具，直接把 prompt 交给图像工具。
5. 如果没有图像能力，输出完整中文海报 prompt，用户可以复制到任意生图工具。

详细海报 prompt 模板见 `references/poster-guide.md`。

## 记忆与心跳

默认记忆目录：

```bash
$HOME/.openclaw/skills/ai-hot-radar/memory
```

如果平台有自己的持久化目录，保留同样结构：

```text
memory/
├── ledger.md
├── interests.md
├── preferences.md
└── briefings/
```

心跳默认时区：`Asia/Shanghai`。

推荐心跳：

- `08:30` 早报：过去 12 小时新增重点资讯。
- `20:30` 晚报：过去 24 小时完整总结。
- 每 2 小时重大快讯：只在出现 `90+` 且未播报的新事件时输出。

重大快讯没有新增内容时，不发空消息，只更新账本。

## 输出格式

正常查询用中文输出：

```markdown
时间窗：<开始时间> - <结束时间>

## 最值得看
1. **<分数>/100｜<标题>**
   为什么重要：<一句到两句话>
   来源：<链接>

## 分类补充
- 模型发布/更新：...
- 产品发布/更新：...
- 行业动态：...
- 论文研究：...
- 开源项目：...
```

默认只给 3-5 条最高分。用户说“全部 / 完整列表 / 所有”时才展开低分条目。

重大快讯输出：

```markdown
# AI 重大快讯

**<分数>/100｜<标题>**

为什么重要：...
影响判断：...
来源：...
```

## 容错要求

不能因为单个源失败导致整次失败。

- `AI HOT` 403：用浏览器 `User-Agent` 重试。
- RSS 失败：跳过该源。
- GitHub 限流：跳过开源趋势层。
- 记忆文件不存在：自动创建。
- 时间解析失败：保留条目，但降低时效性分。

## 安装后自检

Agent 安装后应测试：

```text
使用 ai-hot-radar 测试：最近 24 小时 AI 圈最重要的 5 条新闻，给出 0-100 分、为什么重要和来源。
```

合格结果必须包含：

- 明确时间窗。
- 抓取到公开源。
- 去重后的条目。
- 每条 `0-100` 分。
- 重要性解释。
- 来源链接。
- 记忆文件可创建或可读取。
