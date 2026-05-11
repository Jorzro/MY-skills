# AI Hot Radar Source Map

Fetch sources serially and tolerate failures. Public endpoints change; a failed feed should not fail the whole briefing.

## Primary Source

### AI HOT
- Base: `https://aihot.virxact.com`
- Required header for `/api/public/*`: browser `User-Agent`
- Selected items: `/api/public/items?mode=selected&since=<ISO>&take=50`
- Full items: `/api/public/items?mode=all&since=<ISO>&take=100`
- Keyword search: `/api/public/items?q=<keyword>&take=30`
- Latest daily: `/api/public/daily`
- Daily archive: `/api/public/dailies?take=14`
- Categories: `ai-models`, `ai-products`, `industry`, `paper`, `tip`

AI HOT public item fields currently include:
- `id`
- `title`
- `title_en`
- `url`
- `source`
- `publishedAt`
- `summary`
- `category`

The API does not expose its internal score. Treat `mode=selected` as a quality signal, not as the final importance score.

## RSS Sources

Prefer these stable feeds:
- OpenAI News: `https://openai.com/news/rss.xml`
- Google DeepMind Blog: `https://deepmind.google/blog/rss.xml`
- Google AI: `https://blog.google/technology/ai/rss/`
- The Decoder: `https://the-decoder.com/feed/`
- Latent Space: `https://www.latent.space/feed`
- MarkTechPost: `https://www.marktechpost.com/feed/`

Attempt these feeds, but skip silently if unavailable:
- Anthropic News: `https://www.anthropic.com/news/rss.xml`
- Hugging Face Blog: `https://huggingface.co/blog/feed.xml`
- Mistral AI News: `https://mistral.ai/news/rss.xml`
- Meta AI Blog: `https://ai.meta.com/blog/rss/`

RSS parsing rules:
- Extract `title`, `link`, `pubDate` or `updated`, and `description`/`summary`.
- Prefer official RSS items over reposts when deduplicating.
- For company/topic prompts, filter titles and summaries by the requested keyword after fetching.
- Do not load entire article bodies unless the user asks for deeper analysis.

## GitHub AI Trends

Use GitHub only for explicit GitHub/open-source requests, evening summaries, weekly summaries, or broad "今天 AI 圈" style prompts.

Search pattern:

```bash
created=$(date -u -v-7d +%Y-%m-%d 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%d)
query='(AI OR LLM OR agent OR transformer OR diffusion OR rag) pushed:>'"$created"
curl -sL "https://api.github.com/search/repositories?q=${query}&sort=stars&order=desc&per_page=20"
```

If the GitHub API is rate limited, skip GitHub trends and continue.

Normalize GitHub repo items as `category=open-source` with:
- `title`: `<owner>/<repo>: <description>`
- `summary`: repo description plus stars and recent push date
- `url`: `html_url`
- `source`: `GitHub`
- `source_tier`: `github`

## Source Priority

When duplicate events appear:
1. AI HOT selected
2. Official first-party source
3. Specialist AI media/newsletter
4. GitHub repo
5. Social repost

Use alternate sources as evidence in the final source line.
