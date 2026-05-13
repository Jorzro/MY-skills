---
name: ai-hot-radar
description: Use when the user asks for current AI news, AI daily briefings, AI hot topics, OpenAI/Anthropic/Google updates, AI papers, GitHub AI trends, Chinese AI news summaries, AI news scoring, or AI news posters/小红书封面/朋友圈图/公众号封面.
metadata:
  version: 1.3.0
  category: news
  description_zh: 融合 AI HOT、精选 AI RSS 与 GitHub AI 趋势，首次使用先完成偏好问卷，之后按文字资讯或海报图片两种模式输出中文 AI 热点简报。
---

# AI Hot Radar

## Goal
Use public sources to answer current AI news questions as polished Chinese editorial briefings or generated poster images, with onboarding preferences, deduplication, 0-100 importance scoring, and persistent Markdown memory.

No custom backend or database is required. Markdown files under the memory directory are the long-term state. Poster image mode uses `scripts/generate_openai_poster.py` and can call OpenAI, MiniMax, Volcengine Ark, OpenRouter, or a custom OpenAI-compatible endpoint. API keys must come from environment variables or Agent Secrets.

## Completion Standard
Before replying or finishing a heartbeat, verify:
- First-time users completed the 5-question onboarding, or the user explicitly requested a one-off mode.
- Relevant public sources were attempted, with failures tolerated and mentioned only if they affect coverage.
- Items were normalized, deduplicated, scored from 0-100, and sorted by score first, recency second.
- English titles and summaries were translated and rewritten into natural Chinese before display.
- Text mode top items include score, Chinese headline, one-sentence takeaway, importance reason, audience, and source links.
- Poster mode either generated an actual image file, or stopped with a clear provider API key configuration instruction. Do not silently replace image mode with prompt-only output unless the user chose prompt-only mode.
- Previously briefed items in `ledger.md` were not repeated unless the user explicitly asks for history.
- Heartbeat runs updated `ledger.md` and the matching `briefings/*.md` file when a briefing is produced.

## Persistent Memory
Default memory root:

```bash
MEMORY_ROOT="${AI_HOT_RADAR_MEMORY_ROOT:-$HOME/.openclaw/skills/ai-hot-radar/memory}"
mkdir -p "$MEMORY_ROOT/briefings" "$MEMORY_ROOT/posters"
touch "$MEMORY_ROOT/ledger.md" "$MEMORY_ROOT/interests.md" "$MEMORY_ROOT/preferences.md"
```

If `$HOME/.openclaw` is not writable, use the agent's persistent workspace and keep the same suffix: `skills/ai-hot-radar/memory`.

Initialize `ledger.md` when empty:

```markdown
# AI Hot Radar Ledger

| fingerprint | title | first_seen_at | last_seen_at | score | category | sources | briefed_at | status |
|---|---|---:|---:|---:|---|---|---:|---|
```

Initialize `interests.md` after onboarding:

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

Initialize `preferences.md` after onboarding:

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

## Onboarding Questionnaire
If `preferences.md` is missing, empty, or does not contain `onboarding_completed: true`, stop and ask the user these 5 questions before fetching news. After the user answers, write `preferences.md` and `interests.md`, then continue only if the original request still has enough context.

Use concise Chinese multiple-choice wording:

```markdown
首次使用 AI Hot Radar，需要先做 5 个偏好选择，之后你可以随时说“重新配置 AI 热点偏好”修改。

1. 输出方式：A 文字资讯 / B 海报图片 / C 每次先问我
2. 关注方向，可多选：A 模型发布/能力更新 / B AI Agent/自动化 / C 开源项目/GitHub 趋势 / D 产品发布/工具 / E 行业融资/大厂动态 / F 论文研究
3. 受众视角，可多选：A 创业者/投资人 / B 开发者 / C 产品/运营 / D 研究者 / E 企业采购/管理者
4. 不想看什么，可多选：A 普通教程 / B Prompt 技巧 / C 炒冷饭资讯 / D 低质量营销稿 / E 暂时不过滤
5. 海报配置：A OpenAI Images / B MiniMax / C 火山引擎方舟 / D OpenRouter / E 只生成海报 prompt / F 暂不启用海报
```

Default choices when the user says "按默认":
- Output: `ask`
- Focus: 模型发布/能力更新, AI Agent/自动化, 开源项目/GitHub 趋势, 产品发布/工具
- Audience: 创业者/投资人, 开发者
- Negative filters: 普通教程, Prompt 技巧, 炒冷饭资讯
- Poster: OpenAI Images API direct image

Mode update commands:
- "重新配置 AI 热点偏好": run the questionnaire again and overwrite preferences/interests.
- "切换成文字模式": set `output_mode: text`, `ask_each_time: false`.
- "切换成海报模式": set `output_mode: poster`, `ask_each_time: false`, keep poster API settings.
- "切换海报 API 为 MiniMax/OpenAI/火山/OpenRouter": update `poster_provider`, `api_key_env`, and default model according to the Provider table.
- "每次都问我": set `output_mode: ask`, `ask_each_time: true`.

## Mode Selection
Resolve output mode before fetching unless the user explicitly asked for onboarding or history:

1. Direct wording wins for the current request:
   - Text mode: "文字版", "简报", "资讯", "列表", "日报", "周报".
   - Poster mode: "海报", "图片", "做成图", "小红书封面", "朋友圈图", "公众号封面".
2. If no direct wording, read `preferences.md`.
3. If `output_mode: ask` or `ask_each_time: true`, ask: `这次要哪种输出？A 文字资讯 / B 海报图片` and wait for the choice.
4. Heartbeats default to `heartbeat_output_mode: text` unless preferences explicitly set poster.

Do not generate both formats by default. If the user asks for both, produce text first, then poster.

## Routing
Use the user's wording to choose the data workflow:
- Broad questions such as "今天 AI 圈有什么", "最近 AI 有什么大事", "过去 24 小时 AI 新闻": fetch `AI HOT selected` plus high-quality RSS for the requested window.
- "日报": fetch `AI HOT daily`; only use this route when the user explicitly says "日报".
- "全部", "完整", "所有", "全量": fetch `AI HOT all`.
- Company or topic questions such as "OpenAI 最近发了什么", "Sora 相关": fetch `AI HOT items?q=<keyword>` plus matching RSS items.
- Category questions: map to `ai-models`, `ai-products`, `industry`, `paper`, or `tip`.
- GitHub or open-source questions: include GitHub AI trends.
- Heartbeat prompts: follow the Heartbeat section.

## Source Fetching
Always set a browser User-Agent for AI HOT:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
```

Examples:

```bash
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
curl -sL -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&since=$since&take=50"
curl -sL -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?q=OpenAI&take=30"
curl -sL -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

RSS and GitHub source details live in `references/source-map.md`. Read it when adding source coverage or debugging failed feeds.

## Chinese Editorial Layer
Before user-facing output, convert normalized items into Chinese editorial cards:

```json
{
  "score": 0,
  "chinese_title": "string",
  "one_sentence": "string",
  "why_it_matters": "string",
  "audience": "创业者|开发者|产品团队|研究者|投资人|企业采购|普通用户",
  "source_links": ["url"],
  "original_title": "string"
}
```

Rules:
- Never use an English title as the primary headline.
- Keep official names recognizable: OpenAI, Claude, Gemini, Sora, GitHub, Hugging Face, DeepMind, Meta, Mistral, Llama.
- Rewrite as a Chinese tech-media headline with clear subject, action, and impact.
- Hide original English titles unless the user asks for original text, details, or audit trail.
- Read `references/output-style.md` for briefing and poster copy rules.

## Normalize, Deduplicate, Score
Normalize every source item:

```json
{
  "title": "string",
  "summary": "string",
  "url": "string",
  "source": "string",
  "published_at": "ISO-8601 or best effort",
  "category": "ai-models|ai-products|industry|paper|tip|open-source|unknown",
  "source_tier": "aihot-selected|official|quality-media|github|social|other",
  "raw_source": "aihot|rss|github"
}
```

Deduplicate by canonical URL, normalized title, entities, and 24-hour publish window. Exact canonical URL match is a hard dedupe signal.

Primary item priority:
1. `AI HOT selected`
2. official first-party source
3. quality media or newsletter
4. GitHub trend source
5. social repost

Score every merged event from 0-100. Use `references/scoring-rubric.md` when scores are central or close:
- Rule base: 80 points from source authority, event level, AI relevance, impact, freshness, and source confirmation.
- Agent adjustment: 20 points from market expectation, officialness, urgency, and action value.
- `90-100`: major alert.
- `75-89`: heavyweight.
- `60-74`: important.
- `40-59`: normal; include only in full-list requests.
- `<40`: ignore unless explicitly requested.

Apply `interests.md` after the base score:
- Add up to `+8` for strong Focus match.
- Subtract up to `-12` for Negative Filters.
- Tune `why_it_matters` and `audience` to the selected Audience.

## Text Mode Output
Use this format in Chinese:

```markdown
时间窗：<start> - <end>

# 今日 AI 热点雷达

## 今日判断
<one short paragraph summarizing the main trend>

## 最值得看
1. **<score>/100｜<Chinese title>**
   一句话：<single clear takeaway>
   为什么重要：<one or two plain Chinese sentences>
   适合谁关注：<audience>
   来源：<source links>

## 分类补充
- 模型发布/更新：...
- 产品发布/更新：...
- 行业动态：...
- 论文研究：...
- 技巧与观点：...
- 开源项目：...
```

Keep the top section to 3-5 items unless the user asks for a full list. Mention source failures only when they materially affect the result.

For "查看最近已播报记录", read `ledger.md` and summarize recent rows by `briefed_at`, score, and status.

## Poster Image Generation
Trigger poster mode when selected by preferences or when the user asks for "海报", "图片", "做成图", "小红书封面", "朋友圈图", or "公众号封面".

Workflow:
1. Generate the Chinese editorial cards first.
2. Select top 3-5 items by score.
3. Read `references/poster-guide.md`.
4. Compress each item for image text: short Chinese title plus 7-12 character judgment.
5. Build a complete Chinese poster prompt with title, time window, Top 5, scores, and source footer.
6. If `poster_mode: prompt`, output the prompt only.
7. If `poster_mode: image`, require the selected provider's API key env var. If it is missing, stop and tell the user to configure it.
8. Run:

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

9. Return the generated PNG path and, if the agent UI supports it, display the image.

Provider table:

| Provider | `poster_provider` | Default key env | Default model | Endpoint |
|---|---|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-image-1.5` | `https://api.openai.com/v1/images/generations` |
| MiniMax | `minimax` | `MINIMAX_API_KEY` | `image-01` | `https://api.minimaxi.com/v1/image_generation` |
| 火山引擎方舟 | `volcengine` | `ARK_API_KEY` or `VOLCENGINE_API_KEY` | `doubao-seedream-4-5-251128` | `https://ark.cn-beijing.volces.com/api/v3/images/generations` |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | `google/gemini-3.1-flash-image-preview` | `https://openrouter.ai/api/v1/chat/completions` |
| 自定义兼容接口 | `custom` | `AI_HOT_RADAR_IMAGE_API_KEY` | user-defined | set `api_url` or `AI_HOT_RADAR_IMAGE_API_URL` |

API key instruction when missing:

```text
海报图片模式需要 <provider> API Key。请在 Agent Secret 或运行环境里设置 <api_key_env>，然后重新运行。
示例：export <api_key_env>="..."
```

Do not write API keys into `preferences.md`, `interests.md`, `ledger.md`, or any committed file.

## Heartbeat
Default timezone: `Asia/Shanghai`.

Default schedule:
- `08:30` morning: last 12 hours, new items with score `>=60`.
- `20:30` evening: last 24 hours, full summary with score `>=60`, plus category sections.
- Every 2 hours alert check: only new items with score `>=90`.

Heartbeat workflow:
1. Initialize memory files if needed.
2. Read `ledger.md`, latest briefing, `interests.md`, and `preferences.md`.
3. Fetch sources for the heartbeat window.
4. Normalize, deduplicate, score, and sort.
5. Remove events whose fingerprint already has `briefed_at` unless the new score crosses 90 and status was not `alerted`.
6. For alert checks, if no new score `>=90` item exists, do not produce a user-visible briefing; only update `last_seen_at`.
7. Produce text output unless `heartbeat_output_mode: poster`.
8. Write the briefing Markdown file when a briefing is produced.
9. Update `ledger.md` rows for all observed events.

Status values: `seen`, `briefed`, `alerted`, `suppressed`.

## Failure Handling
- AI HOT 403: retry once with the required User-Agent.
- AI HOT unavailable: continue with RSS and GitHub, and label coverage as incomplete.
- RSS feed unavailable: skip it.
- GitHub rate limited: skip GitHub trends.
- No new heartbeat items: avoid user-visible output for alert checks.
- Poster API key missing: stop with provider-specific setup instructions, do not downgrade to prompt unless user chose prompt-only mode.
- Poster API error: show the error summary and suggest checking provider key, model name, endpoint, account access, and billing.

## Install Notes For OpenClaw
Install the folder as a normal OpenClaw skill. The skill is self-contained:
- `SKILL.md` is the main instruction file.
- `references/scoring-rubric.md` defines scoring.
- `references/source-map.md` defines source coverage.
- `references/output-style.md` defines Chinese editorial output.
- `references/poster-guide.md` defines image poster prompts.
- `scripts/generate_openai_poster.py` generates poster PNG files via OpenAI, MiniMax, Volcengine Ark, OpenRouter, or custom compatible endpoints.

Configure OpenClaw heartbeat prompts:
- Morning: "使用 ai-hot-radar 执行早报心跳。"
- Evening: "使用 ai-hot-radar 执行晚报心跳。"
- Alert: "使用 ai-hot-radar 执行重大快讯心跳，只在有 90 分以上新增事件时输出。"
