# AI Hot Radar Output Style

Use this file whenever producing a user-facing briefing, company report, daily report, weekly report, heartbeat output, or poster copy.

## Default Voice

Write as a Chinese AI industry editor for founders, builders, product teams, researchers, and investors.

The output should feel like a concise Chinese tech briefing, not a raw feed dump.

## Translation Rules

- English titles must be translated and rewritten into natural Chinese before display.
- Keep official names recognizable: OpenAI, Claude, Gemini, Sora, GitHub, Hugging Face, DeepMind, Meta, Mistral, Llama.
- Do not use literal machine translation when it sounds unnatural. Rewrite the headline around `主体 + 动作 + 影响`.
- Do not invent facts not present in sources. If the source is thin, use a conservative headline.
- Keep original English titles hidden by default. Show them only when the user asks for original text, details, or audit trail.

## Editorial Card

Every top item should have this shape:

```markdown
**<score>/100｜<Chinese headline>**
一句话：<one clear takeaway in Chinese>
为什么重要：<impact, novelty, or urgency>
适合谁关注：<创业者/开发者/产品团队/研究者/投资人/企业采购/普通用户>
来源：<source name + URL>
```

## Output Modes

When the user selected text mode, produce the full editorial card format above.

When the user selected poster mode, first prepare editorial cards internally, then compress them for image use. The poster should not contain long explanations, URLs, or raw English titles.

If the saved preference is `output_mode: ask`, ask the user to choose `文字资讯` or `海报图片` before fetching unless the request wording already makes the mode obvious.

## Headline Guidelines

Good headlines:
- `OpenAI 推出 DeployCo，想把企业 AI 落地做成服务生意`
- `Claude 全面接入 AWS 平台，企业采购路径更顺了`
- `Google Finance AI 版扩展到欧洲，搜索入口继续产品化`

Avoid:
- `The new AI-powered Google Finance is expanding to Europe.`
- `OpenAI launches DeployCo to help businesses build around intelligence`
- `谷歌金融人工智能正在扩展到欧洲`

## Today Judgment

For broad briefings, add a short `今日判断` section after the time window.

It should summarize the pattern across items, for example:

```markdown
## 今日判断
过去 24 小时的重点不在单个模型炸场，而在企业落地、云平台分发和开发者工具继续加速。值得优先看的是能改变采购路径、开发工作流或开源生态的事件。
```

## Category Names

Use these Chinese category labels:

- 模型发布/更新
- 产品发布/更新
- 行业动态
- 论文研究
- 技巧与观点
- 开源项目

## Length Defaults

- Normal briefing: top 3-5 items plus category supplement.
- Full list: include 40-59 scores only when the user asks for `全部`, `完整`, `所有`, or `全量`.
- Company/topic report: top 5, then timeline if useful.
- Heartbeat alert: one event only unless multiple events are independently `90+`.
- Poster: top 3-5 items, each compressed to one short Chinese title plus one 7-12 character judgment.

## Poster Copy Rules

Poster copy is not a miniature article.

- Main title: `今日 AI 热点雷达` unless the user requests another title.
- Subtitle: state the time window, e.g. `过去 24 小时最值得关注的 5 件事`.
- Item title: 8-18 Chinese characters when possible.
- Item judgment: 7-12 Chinese characters, e.g. `企业采购提速`, `开发者可试用`, `监管风险升温`.
- Use scores, but do not include long scoring explanations on the image.
- Keep source footer short: `数据源：AI HOT / 官方 RSS / GitHub`.

## Source Presentation

Always include source links. Prefer:

```markdown
来源：OpenAI Blog｜https://...
```

For merged events:

```markdown
来源：AI HOT；OpenAI Blog｜https://...
```

Mention failed sources only when they materially affect coverage.
