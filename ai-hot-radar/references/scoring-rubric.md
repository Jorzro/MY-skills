# AI Hot Radar Scoring Rubric

Use this rubric to score merged AI news events from 0-100. Score conservatively. A high score should mean the item is worth interrupting or prioritizing.

## Rule Base: 80 Points

### Source Authority: 0-15
- `15`: official company/research lab/blog, paper page, model card, GitHub repo from the project owner.
- `12`: AI HOT selected, high-quality specialist media, respected technical newsletter.
- `8`: mainstream media, known community account, GitHub trend without official release context.
- `4`: social repost or secondary commentary.
- `0`: unclear or low-trust source.

### Event Level: 0-20
- `20`: frontier model release, major platform/API launch, acquisition, regulation with direct AI impact, safety incident with wide implications.
- `16`: important model/product update, notable benchmark result, major open-source release, large partnership.
- `12`: useful tool release, research with practical implications, significant funding or adoption news.
- `8`: tutorial, opinion, small product update, incremental integration.
- `4`: generic content, listicle, repeated old material.
- `0`: not meaningfully AI-related.

### AI Core Relevance: 0-15
- `15`: models, agents, inference, training, evals, chips, safety, AI developer tooling.
- `12`: AI products, enterprise AI adoption, open-source AI infra.
- `8`: business news where AI is one part of the story.
- `4`: adjacent tech with weak AI connection.
- `0`: unrelated.

### Impact Scope: 0-10
- `10`: affects many developers, users, enterprises, or the AI ecosystem.
- `7`: affects a major niche such as researchers, builders, or creators.
- `4`: useful to a small audience.
- `1`: narrow or mostly anecdotal.

### Freshness: 0-10
- `10`: published in the last 12 hours.
- `8`: last 24 hours.
- `6`: last 72 hours.
- `4`: last 7 days.
- `1`: older, only include when explicitly requested or historically important.

### Confirmation / Selection: 0-10
- `10`: multiple independent sources, or official source plus AI HOT selected.
- `8`: AI HOT selected, or official source plus social discussion.
- `5`: single official or high-quality source.
- `2`: one secondary source.
- `0`: unconfirmed rumor.

## Agent Adjustment: 0-20

Add semantic judgment after the rule base:
- `0-5`: changes market or technical expectations.
- `0-5`: is formal, actionable, and not just rumor/commentary.
- `0-5`: matters to builders, founders, researchers, or product teams now.
- `0-5`: has clear next action value such as try, read, migrate, monitor, or avoid.

Do not use adjustment points to rescue weakly relevant items. If AI core relevance is under 8, the total score should normally stay below 60.

## Interest Adjustment

Read `interests.md` when available:
- Strong Focus match: `+5` to `+8`.
- Mild Focus match: `+1` to `+4`.
- Strong Negative Filter match: `-8` to `-12`.
- Mild Negative Filter match: `-3` to `-7`.

Clamp final score to `0-100`.

## Bands
- `90-100`: Major alert. Use for major releases, ecosystem-shifting events, or urgent risks.
- `75-89`: Heavyweight. Put near the top of morning/evening briefings.
- `60-74`: Important. Include in normal briefings.
- `40-59`: Normal. Include only when user asks for full list.
- `<40`: Ignore by default.

## Category Guardrails
- Safety incidents, lawsuits, regulation, policy, funding, partnerships, and enterprise adoption should normally be categorized as `industry`.
- Do not classify an event as `ai-models` just because the title mentions ChatGPT, Claude, Gemini, Sora, or another model name.
- Use `ai-models` only for model launches, model updates, model availability, model capability changes, model cards, or model benchmarks.

## Calibration Examples
- Official frontier model launch with API availability and many sources: `92-98`.
- Official model update or important open-source release: `78-88`.
- Strong paper with practical implications but no adoption yet: `68-82`.
- Popular tutorial or resource list: `45-65`, higher only if unusually valuable.
- Generic commentary thread without new facts: `25-50`.
