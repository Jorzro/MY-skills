---
name: ai-hot-radar
description: Use when the user asks for AI news or Chinese prompts like "今天 AI 圈有什么", "AI 日报", "AI 热点", "最近 24 小时最重磅 AI 新闻", "OpenAI/Anthropic/Google 最近发了什么", "最近一周 AI 论文", "AI 开源项目趋势", or asks an OpenClaw agent to run AI news heartbeats. This skill fetches public AI sources, merges duplicates, scores importance from 0-100, writes Markdown memory, and produces Chinese briefings without requiring a custom backend.
metadata:
  version: 1.0.0
  category: news
  description_zh: 融合 AI HOT、精选 AI RSS 与 GitHub AI 趋势，自动抓取 AI 资讯、去重聚合、按 100 分制判断重磅程度，并通过 Markdown 记忆文件支持 OpenClaw 云端心跳。
---

# AI Hot Radar

## Goal
Use public sources to answer current AI news questions in Chinese, with deduplication, 0-100 importance scoring, and persistent Markdown memory for OpenClaw heartbeats.

This skill does not require a custom backend or database. Treat the Markdown files under the memory directory as the long-term state.

## Completion Standard
Before replying or finishing a heartbeat, verify these items:
- Relevant public sources were attempted, with failures tolerated and mentioned only if they affect coverage.
- Items were normalized, deduplicated, scored from 0-100, and sorted by score first, recency second.
- Previously briefed items in `ledger.md` were not repeated unless the user explicitly asks for history.
- The response states the time window and includes source links.
- For heartbeat runs, `ledger.md` and the matching `briefings/*.md` file were updated.

## Persistent Memory
Default memory root:

```bash
MEMORY_ROOT="${AI_HOT_RADAR_MEMORY_ROOT:-$HOME/.openclaw/skills/ai-hot-radar/memory}"
mkdir -p "$MEMORY_ROOT/briefings"
touch "$MEMORY_ROOT/ledger.md"
touch "$MEMORY_ROOT/interests.md"
```

If `$HOME/.openclaw` is not writable in OpenClaw cloud, use the agent's persistent workspace and keep the same suffix: `skills/ai-hot-radar/memory`.

Required files:
- `ledger.md`: long-term event ledger.
- `briefings/YYYY-MM-DD-morning.md`: morning briefing.
- `briefings/YYYY-MM-DD-evening.md`: evening briefing.
- `briefings/YYYY-MM-DD-alert-HHMM.md`: major alert.
- `interests.md`: user focus areas and negative filters.

Initialize `ledger.md` with this header when it is empty:

```markdown
# AI Hot Radar Ledger

| fingerprint | title | first_seen_at | last_seen_at | score | category | sources | briefed_at | status |
|---|---|---:|---:|---:|---|---|---:|---|
```

Initialize `interests.md` with this template when it is empty:

```markdown
# AI Hot Radar Interests

## Focus
- frontier models
- AI agents
- developer tools
- AI product launches
- open source AI projects

## Negative Filters
- generic prompt tips
- recycled listicles
- old tutorials without new release information
```

## Routing
Use the user's wording to choose the workflow:
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

AI HOT examples:

```bash
# Selected items for a rolling window.
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
curl -sL -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&since=$since&take=50"

# Keyword search.
curl -sL -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?q=OpenAI&take=30"

# Daily report.
curl -sL -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

RSS and GitHub source details live in `references/source-map.md`. Read it when adding source coverage or debugging failed feeds.

## Normalize Items
Convert every source item into this internal shape before reasoning:

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

## Deduplication
Deduplicate before scoring final output.

Build a fingerprint from:
- lowercase title with punctuation, whitespace, tracking parameters, and common filler words removed;
- canonical URL domain and path when available;
- extracted company/model/product names;
- published date rounded to a 24-hour window.

Merge items when they share the same canonical URL, or when title/entity similarity is clearly the same event.

Choose the primary item in this priority order:
1. `AI HOT selected`
2. official first-party source
3. quality media or newsletter
4. GitHub trend source
5. social repost

Keep alternate sources in a `sources` list and use them as scoring evidence.

## Scoring
Score every merged event from 0-100.

Use `references/scoring-rubric.md` when scoring is central to the user request or when scores are close. The short version:
- Rule base: 80 points from source authority, event level, AI relevance, impact, freshness, and source confirmation.
- Agent adjustment: 20 points from semantic judgment about market expectation, officialness, urgency, and practical action value.
- `90-100`: major alert.
- `75-89`: heavyweight.
- `60-74`: important.
- `40-59`: normal; include only in full-list requests.
- `<40`: ignore unless explicitly requested.

`AI HOT selected` is a quality prior, not the final score.

Apply `interests.md` after the base score:
- Add up to `+8` for strong match with Focus.
- Subtract up to `-12` for strong match with Negative Filters.
- Never push weakly AI-related content above 60 only because it matches a focus word.

## Heartbeat
Default timezone: `Asia/Shanghai`.

Default schedule:
- `08:30` morning: last 12 hours, new items with score `>=60`.
- `20:30` evening: last 24 hours, full summary with score `>=60`, plus category sections.
- Every 2 hours alert check: only new items with score `>=90`.

Heartbeat workflow:
1. Initialize memory files if needed.
2. Read `ledger.md`, the latest briefing, and `interests.md`.
3. Fetch AI HOT selected for the heartbeat window.
4. Fetch selected RSS feeds from `references/source-map.md`; skip failed feeds.
5. Include GitHub AI trends only for evening or explicit open-source/GitHub prompts.
6. Normalize, deduplicate, score, and sort.
7. Remove events whose fingerprint already has `briefed_at` unless the new score crosses 90 and status was not `alerted`.
8. For alert checks, if no new score `>=90` item exists, do not produce a user-visible briefing; only update `last_seen_at` for observed ledger rows.
9. Write the briefing Markdown file when a briefing is produced.
10. Update `ledger.md` rows for all observed events.

Use these status values:
- `seen`: observed but not briefed.
- `briefed`: included in morning/evening.
- `alerted`: sent as major alert.
- `suppressed`: filtered by low score or negative interest.

## Output Format
For normal user questions, answer in Chinese:

```markdown
时间窗：<start> - <end>

## 最值得看
1. **<score>/100｜<title>**
   为什么重要：<one or two plain sentences>
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

For alert heartbeat output:

```markdown
# AI 重大快讯

**<score>/100｜<title>**

为什么重要：...
影响判断：...
来源：...
```

For "查看最近已播报记录", read `ledger.md` and summarize recent rows by `briefed_at`, score, and status.

## Failure Handling
- AI HOT 403: retry once with the required User-Agent and say the first request was blocked by User-Agent only if the retry also fails.
- AI HOT unavailable: continue with RSS and GitHub, and label coverage as incomplete.
- RSS feed unavailable: skip it.
- GitHub rate limited: skip GitHub trends.
- No new heartbeat items: avoid user-visible output for alert checks; for morning/evening say there are no new score `>=60` items.

## Install Notes For OpenClaw
Install the folder as a normal OpenClaw skill. The skill is self-contained:
- `SKILL.md` is the main instruction file.
- `references/scoring-rubric.md` defines scoring.
- `references/source-map.md` defines source coverage.

Configure OpenClaw heartbeat prompts to invoke:
- Morning: "使用 ai-hot-radar 执行早报心跳。"
- Evening: "使用 ai-hot-radar 执行晚报心跳。"
- Alert: "使用 ai-hot-radar 执行重大快讯心跳，只在有 90 分以上新增事件时输出。"
