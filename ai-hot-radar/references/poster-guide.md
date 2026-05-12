# AI Hot Radar Poster Guide

Use this file when the user asks for a poster, cover image, social graphic, 小红书封面, 朋友圈图, 公众号封面, or "做成图".

## Default Poster

- Ratio: `9:16`
- Use case: 小红书 / 朋友圈 / 手机端资讯卡片
- Style: Chinese tech-media infographic, clean hierarchy, editorial, high contrast, modern but not cyberpunk
- Content: Top 3-5 scored AI news items
- Language: Simplified Chinese

## Content Structure

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
生成一张 9:16 竖版中文 AI 资讯海报，适合小红书和朋友圈发布。

视觉风格：中文科技媒体信息图，干净、高级、层次清晰，白色或浅灰背景，蓝绿色点缀，少量渐变块，卡片式信息层级，避免赛博霓虹、避免杂乱背景、避免夸张 3D 机器人。

版式要求：
- 顶部大标题：今日 AI 热点雷达
- 副标题：过去 24 小时最值得关注的 5 件事
- 中部用 5 个信息卡片展示热点，每张卡片包含分数、中文短标题、7-12 字判断
- 右上角可有小标签：AI NEWS / 24H
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
- Do not include URLs on the poster.
- Do not include source names per item unless the user asks.

Examples:

```text
83｜Claude 接入 AWS｜企业采购提速
78｜OpenAI 推 DeployCo｜落地服务加码
76｜新开源模型发布｜开发者可试用
```

## baoyu-imagine Handoff

If `baoyu-imagine` is installed or available, hand off the final prompt to it.

Recommended settings:

```text
provider: auto
quality: 2k
aspect ratio: 9:16
output filename: ai-hot-radar-YYYY-MM-DD.png
```

Do not block the news briefing if image generation is unavailable. In that case, output the prompt and say it can be copied into `baoyu-imagine` or any text-to-image tool.

## Fallback Output

When no image-generation tool is available, output:

```markdown
## 海报生成 Prompt
用途：小红书/朋友圈竖版资讯海报
比例：9:16
风格：中文科技媒体信息图，干净、高级、层次清晰

<complete prompt>
```
