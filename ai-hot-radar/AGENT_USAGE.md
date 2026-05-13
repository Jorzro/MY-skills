# AI Hot Radar — Agent Skill 使用手册

让 Agent 用自然中文查询最新 AI 资讯，并自动完成抓取、去重、聚合、`0-100` 分重要度评分、中文编辑型简报、首次偏好问卷、早晚报、重大快讯记忆和热点海报图片生成。

> 适用于 OpenClaw / Codex / Claude Code / Cursor / Gemini CLI / OpenCode / Cline / Windsurf 等支持 `SKILL.md` 的 Agent 平台。

## 安装

在 Agent 里直接说：

```text
帮我安装这个 skill：https://github.com/Jorzro/MY-skills/tree/main/ai-hot-radar
```

Agent 应读取整个目录，而不是只读取 `SKILL.md`。目录包含评分规则、数据源表、中文排版规则、海报规则和 OpenAI 海报生成脚本。

一行命令安装：

```bash
curl -fsSL -H 'Accept: application/vnd.github.raw' \
  'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main' | bash
```

Codex：

```bash
SKILL_DIR=$HOME/.codex/skills/ai-hot-radar \
  bash <(curl -fsSL -H 'Accept: application/vnd.github.raw' \
    'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main')
```

## 首次运行必须问卷

如果 `preferences.md` 不存在、为空，或没有 `onboarding_completed: true`，Agent 不要直接抓新闻，先问：

```markdown
首次使用 AI Hot Radar，需要先做 5 个偏好选择，之后你可以随时说“重新配置 AI 热点偏好”修改。

1. 输出方式：A 文字资讯 / B 海报图片 / C 每次先问我
2. 关注方向，可多选：A 模型发布/能力更新 / B AI Agent/自动化 / C 开源项目/GitHub 趋势 / D 产品发布/工具 / E 行业融资/大厂动态 / F 论文研究
3. 受众视角，可多选：A 创业者/投资人 / B 开发者 / C 产品/运营 / D 研究者 / E 企业采购/管理者
4. 不想看什么，可多选：A 普通教程 / B Prompt 技巧 / C 炒冷饭资讯 / D 低质量营销稿 / E 暂时不过滤
5. 海报配置：A OpenAI Images / B MiniMax / C 火山引擎方舟 / D OpenRouter / E 只生成海报 prompt / F 暂不启用海报
```

用户说“按默认”时写入：

- 输出方式：每次先问我
- 关注方向：模型发布、AI Agent、开源项目、产品工具
- 受众视角：创业者/投资人、开发者
- 过滤：普通教程、Prompt 技巧、炒冷饭资讯
- 海报：启用 OpenAI Images API；也可选 MiniMax、火山引擎方舟、OpenRouter

## 偏好文件

写入 `preferences.md`：

```markdown
# AI Hot Radar Preferences

onboarding_completed: true

## Output
language: zh-CN
style: editorial
output_mode: ask
ask_each_time: true
show_original_title: false

## Poster
enabled: true
poster_mode: image
poster_provider: openai
image_model: gpt-image-1.5
image_size: 1024x1536
image_aspect_ratio: 9:16
image_quality: medium
api_key_env: OPENAI_API_KEY
api_url:
prompt_fallback: false

## Heartbeat
heartbeat_output_mode: text
timezone: Asia/Shanghai
```

写入 `interests.md`：

```markdown
# AI Hot Radar Interests

## Focus
- 模型发布/能力更新
- AI Agent/自动化
- 开源项目/GitHub 趋势
- 产品发布/工具

## Audience
- 创业者/投资人
- 开发者

## Negative Filters
- 普通教程
- Prompt 技巧
- 炒冷饭资讯
```

## 模式选择

每次执行前先决定输出模式：

- 用户说“文字版 / 简报 / 资讯 / 列表 / 日报 / 周报”：文字模式。
- 用户说“海报 / 图片 / 做成图 / 小红书封面 / 朋友圈图 / 公众号封面”：海报模式。
- 没有明确说时，读取 `preferences.md`。
- 如果 `output_mode: ask` 或 `ask_each_time: true`，先问：`这次要哪种输出？A 文字资讯 / B 海报图片`。

用户可随时切换：

```text
切换成文字模式
切换成海报模式
每次都问我
重新配置 AI 热点偏好
```

## 什么时候必须触发

用户询问任何“当前 AI 行业事实”时，不要凭训练数据回答，必须抓取最新数据。

| 用户在说 | Agent 应该做什么 |
|---|---|
| 今天 AI 圈有什么、过去 24 小时 AI 新闻 | 拉 `AI HOT selected` + RSS |
| AI 日报、看下今天日报 | 走 `AI HOT daily` |
| 全部、完整、所有、全量 AI 动态 | 走 `AI HOT mode=all` |
| OpenAI / Anthropic / Google 最近发了什么 | 走关键词搜索 + 官方 RSS |
| 最近一周 AI 论文 | 走 `paper` 分类 + RSS |
| 最近 AI 开源项目、GitHub AI 趋势 | 加入 GitHub 趋势层 |
| 给今天热点按重要度打分 | 每条输出 `0-100` 分和理由 |
| 生成海报、做成图、小红书封面 | 生成中文热点海报图片 |
| 查看最近已播报记录 | 读取 `ledger.md` |

## 数据源

AI HOT API 调用 `/api/public/*` 时必须带浏览器 `User-Agent`：

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&take=50"
```

宽问题默认走：

```bash
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&since=$since&take=50"
```

详细源表见 `references/source-map.md`。

## 文字模式输出

默认中文编辑稿：

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

## 海报图片模式

海报模式流程：

1. 先抓新闻并生成中文编辑卡片。
2. 选 Top 3-5 条。
3. 按 `references/poster-guide.md` 压缩成海报 prompt。
4. 如果 `poster_mode: prompt`，只输出 prompt。
5. 如果 `poster_mode: image`，检查当前 Provider 对应的 API Key 环境变量。
6. 有 key 时运行：

```bash
python3 scripts/generate_openai_poster.py \
  --prompt-file "$MEMORY_ROOT/posters/latest-prompt.txt" \
  --output-dir "$MEMORY_ROOT/posters" \
  --provider "openai" \
  --model "gpt-image-1.5" \
  --size "1024x1536" \
  --aspect-ratio "9:16" \
  --quality "medium"
```

7. 返回生成的 PNG 路径，并在支持图片展示的 Agent UI 中展示图片。

注意：不要依赖生图模型直接渲染中文正文。默认做法是先让 Provider 生成无文字科技背景，再用 `scripts/render_news_poster.py` 把真实中文标题、摘要、发布时间、来源、类型和分数叠加到最终 PNG。

支持的 Provider：

| Provider | Key 环境变量 | 默认模型 |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `gpt-image-1.5` |
| MiniMax | `MINIMAX_API_KEY` | `image-01` |
| 火山引擎方舟 | `ARK_API_KEY` 或 `VOLCENGINE_API_KEY` | `doubao-seedream-4-5-251128` |
| OpenRouter | `OPENROUTER_API_KEY` | `recraft/recraft-v4` |
| 自定义兼容接口 | `AI_HOT_RADAR_IMAGE_API_KEY` | 用户自定义 |

如果缺少 key，输出：

```text
海报图片模式需要 <provider> API Key。请在 Agent Secret 或运行环境里设置 <api_key_env>，然后重新运行。
示例：export <api_key_env>="..."
```

不要把 API Key 写进 Markdown 记忆文件或仓库。

## 记忆与心跳

默认记忆目录：

```bash
$HOME/.openclaw/skills/ai-hot-radar/memory
```

结构：

```text
memory/
├── ledger.md
├── interests.md
├── preferences.md
├── briefings/
└── posters/
```

心跳默认时区：`Asia/Shanghai`。

- `08:30` 早报：过去 12 小时新增重点资讯。
- `20:30` 晚报：过去 24 小时完整总结。
- 每 2 小时重大快讯：只在出现 `90+` 且未播报的新事件时输出。

心跳默认文字模式，不要在无人值守场景反复生成图片，除非 `heartbeat_output_mode: poster`。

## 验收要求

合格运行必须包含：

- 首次无配置时先问 5 题。
- 明确时间窗。
- 抓取公开源，不凭旧知识回答。
- 去重后的条目。
- 每条 `0-100` 分。
- 中文标题、中文判断、来源链接。
- 海报模式有 key 时直接出 PNG，无 key 时要求配置。
