# AI Hot Radar Poster Guide

Use this file when the user selects poster output or asks for a poster, image, cover, 小红书封面, 朋友圈图, 公众号封面, or "做成图".

## Output Modes

- `poster_mode: image`: Generate an actual PNG with OpenAI Images API. This requires `OPENAI_API_KEY`.
- `poster_mode: prompt`: Output the full poster prompt only. Use this only when the user chose prompt-only mode.
- `enabled: false`: Do not produce posters; ask the user to enable poster output first.

Do not silently fall back from image mode to prompt mode. If image mode is selected and `OPENAI_API_KEY` is missing, stop and ask the user to configure it.

## Default Image Settings

- Provider: `openai`
- Model: `gpt-image-1.5`
- Size: `1024x1536`
- Ratio: `9:16`
- Quality: `medium`
- Output directory: `memory/posters/`
- Filename: `ai-hot-radar-YYYY-MM-DD-HHMM.png`

## Poster Structure

```text
标题：今日 AI 热点雷达
副标题：过去 24 小时最值得关注的 5 件事
时间窗：<start> - <end>

Top 1: <score>｜<short Chinese title>｜<7-12 character judgment>
Top 2: ...
Top 3: ...
Top 4: ...
Top 5: ...

底部：数据源：AI HOT / 官方 RSS / GitHub
```

## Prompt Template

```text
生成一张 9:16 竖版中文 AI 资讯海报，适合小红书、朋友圈和公众号封面二次裁切。

视觉风格：中文科技媒体信息图，干净、高级、层次清晰，白色或浅灰背景，蓝绿色点缀，少量渐变块，卡片式信息层级，深浅对比明确。避免赛博霓虹、避免杂乱背景、避免夸张 3D 机器人。

版式要求：
- 顶部大标题：今日 AI 热点雷达
- 副标题：过去 24 小时最值得关注的 5 件事
- 右上角小标签：AI NEWS / 24H
- 中部用 5 个信息卡片展示热点，每张卡片包含分数、中文短标题、短判断
- 底部小字：数据源：AI HOT / 官方 RSS / GitHub
- 中文字体清晰可读，信息密度适中，留白充足

画面文字：
1. <score>/100｜<short title>｜<short judgment>
2. ...
```

## Text Compression

Poster text must be shorter than briefing text:

- Title: 8-18 Chinese characters when possible.
- Judgment: 7-12 Chinese characters.
- Avoid full URLs on the poster.
- Avoid per-item source names unless the user asks.
- Keep model, product, and company names recognizable.

Examples:

```text
83｜Claude 接入 AWS｜企业采购提速
78｜OpenAI 推企业服务｜落地服务加码
76｜新开源模型发布｜开发者可试用
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
  --model "gpt-image-1.5" \
  --size "1024x1536" \
  --quality "medium"
```

When successful, return the generated PNG path to the user and display the image if the UI supports local images.

## Missing API Key

If `OPENAI_API_KEY` is missing in image mode, output:

```text
海报图片模式需要 OpenAI Images API。请在 Agent Secret 或运行环境里设置 OPENAI_API_KEY，然后重新运行。
示例：export OPENAI_API_KEY="sk-..."
```

Do not store API keys in Markdown memory files or committed files.
