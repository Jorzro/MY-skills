# AI Hot Radar Poster Guide

Use this file when the user selects poster output or asks for a poster, image, cover, 小红书封面, 朋友圈图, 公众号封面, or "做成图".

## Output Modes

- `poster_mode: image`: Generate an actual PNG with the selected provider. This requires the provider API key env var.
- `poster_mode: prompt`: Output the full poster prompt only. Use this only when the user chose prompt-only mode.
- `enabled: false`: Do not produce posters; ask the user to enable poster output first.

Do not silently fall back from image mode to prompt mode. If image mode is selected and the provider key is missing, stop and ask the user to configure it.

## Default Image Settings

- Provider: `openai`
- Model: provider default
- Size: `1024x1536`
- Ratio: `9:16`
- Quality: `medium`
- Output directory: `memory/posters/`
- Filename: `ai-hot-radar-YYYY-MM-DD-HHMM.png`

## Poster Structure

```text
标题：今日 AI 热点雷达
副标题：过去 24 小时最值得关注的 AI 资讯
时间窗：<start> - <end>

Card 1:
- 分数：<score>/100
- 类型：<category>
- 标题：<Chinese title>
- 摘要：<one sentence summary>
- 发布时间：<published_at>
- 来源：<source>

Card 2...

底部：数据源：AI HOT / 官方 RSS / GitHub
```

## Prompt Template

Use this prompt for the image provider background. Do not ask the image model to render Chinese news text; the local renderer handles all readable text.

```text
Generate a 9:16 vertical editorial AI news poster background. No readable text, no letters, no numbers, no fake UI labels.

Visual style: premium Chinese technology media, clean data-dashboard atmosphere, warm off-white background, deep teal and graphite accents, subtle paper grain, soft geometric gradients, faint abstract circuit lines, layered card-like spaces, high contrast but calm.

Composition: leave a clean header area at the top, four large readable card zones in the middle, and a footer band at the bottom. Keep plenty of whitespace for text overlay. Make it look like a serious editorial briefing cover, not a cyberpunk poster.

Avoid: cyberpunk neon, clutter, robots, human faces, fake text, fake Chinese characters, screenshots, dense charts, overdecorated 3D objects.
```

## Text Compression

Poster text must be detailed enough to be useful but still shorter than the full briefing:

- Default detailed poster: top 4 items.
- Each item must include title, summary, published time, source, category/type, and score.
- Title: 12-24 Chinese characters when possible.
- Summary: one short Chinese sentence, 24-42 Chinese characters.
- Published time: compact, e.g. `2026-05-13 08:20`.
- Source: source name or domain, not full URL.
- Keep model, product, and company names recognizable.

Examples:

```text
分数：83/100
类型：产品
标题：Claude Code 增加目标功能
摘要：开发者可以把任务目标写进会话，减少偏航和返工。
发布时间：2026-05-13 08:20
来源：AI HOT
```

## Generation Command

Write the final prompt to:

```bash
$MEMORY_ROOT/posters/latest-prompt.txt
```

Then run:

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

When successful, treat the provider image as the background. Then render the final readable poster with:

```bash
python3 scripts/render_news_poster.py \
  --items-json "$MEMORY_ROOT/posters/latest-items.json" \
  --background "$MEMORY_ROOT/posters/<provider-background>.png" \
  --output "$MEMORY_ROOT/posters/ai-hot-radar-final-YYYY-MM-DD-HHMM.png" \
  --time-window "<start> - <end>" \
  --max-items 4
```

Return the final rendered PNG path to the user and display it if the UI supports local images. Do not rely on the image model to render Chinese text accurately; API-generated text may be garbled.

## Providers

| Provider | Key env | Default model | Notes |
|---|---|---|---|
| `openai` | `OPENAI_API_KEY` | `gpt-image-1.5` | Uses OpenAI Images API. |
| `minimax` | `MINIMAX_API_KEY` | `image-01` | Uses MiniMax image generation; ratio is controlled by `--aspect-ratio`. |
| `volcengine` | `ARK_API_KEY` or `VOLCENGINE_API_KEY` | `doubao-seedream-4-5-251128` | Uses Volcengine Ark image generation; users may need to replace the model with their enabled Seedream model. |
| `openrouter` | `OPENROUTER_API_KEY` | `recraft/recraft-v4` | Uses OpenRouter chat completions with image output; users may choose any image-output model they have access to. |
| `custom` | `AI_HOT_RADAR_IMAGE_API_KEY` | user-defined | Requires `--api-url` or `AI_HOT_RADAR_IMAGE_API_URL`; expects OpenAI-compatible image generation output. |

Provider examples:

```bash
# MiniMax
python3 scripts/generate_openai_poster.py --provider minimax \
  --prompt-file "$MEMORY_ROOT/posters/latest-prompt.txt" \
  --output-dir "$MEMORY_ROOT/posters"

# Volcengine Ark
python3 scripts/generate_openai_poster.py --provider volcengine \
  --prompt-file "$MEMORY_ROOT/posters/latest-prompt.txt" \
  --output-dir "$MEMORY_ROOT/posters" \
  --model "doubao-seedream-4-5-251128"

# OpenRouter
python3 scripts/generate_openai_poster.py --provider openrouter \
  --prompt-file "$MEMORY_ROOT/posters/latest-prompt.txt" \
  --output-dir "$MEMORY_ROOT/posters" \
  --model "recraft/recraft-v4"
```

## Missing API Key

If the selected provider key is missing in image mode, output:

```text
海报图片模式需要 <provider> API Key。请在 Agent Secret 或运行环境里设置 <api_key_env>，然后重新运行。
示例：export <api_key_env>="..."
```

Do not store API keys in Markdown memory files or committed files.
