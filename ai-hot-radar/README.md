# AI Hot Radar

AI Hot Radar 是一个面向 OpenClaw / Codex / Claude Code / Cursor 等 Agent 的 AI 资讯热点 skill。

它会抓取 `AI HOT`、精选 AI RSS 和 GitHub AI 趋势，对资讯做去重、聚合和 `0-100` 分重要度评分。首次使用会先做 5 题偏好问卷，之后按用户偏好输出中文文字资讯，或直接生成中文热点海报图片。

## 能做什么

- 查询“今天 AI 圈有什么”“最近 24 小时最重磅 AI 新闻”“OpenAI 最近发了什么”。
- 首次使用先配置：输出方式、关注方向、受众视角、过滤偏好、海报配置。
- 输出排版好的中文编辑型简报，不直接把英文标题当主标题。
- 支持海报图片模式：可用 OpenAI、MiniMax、火山引擎方舟、OpenRouter 或自定义兼容接口生成 PNG。
- 支持 prompt-only 海报模式，但必须由用户选择。
- 支持早报、晚报、重大快讯三类 OpenClaw 心跳。
- 用 Markdown 记忆文件记录历史，避免重复播报。

## 目录结构

```text
ai-hot-radar/
├── AGENT_USAGE.md
├── install.sh
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── output-style.md
│   ├── poster-guide.md
│   ├── scoring-rubric.md
│   └── source-map.md
└── scripts/
    └── generate_openai_poster.py
```

## 安装

让 Agent 自动安装：

```text
帮我安装这个 skill：https://github.com/Jorzro/MY-skills/tree/main/ai-hot-radar
```

一行命令安装到 OpenClaw 默认目录：

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

## 首次问卷

首次使用时，如果还没有配置，Agent 会先问 5 题：

1. 输出方式：文字资讯 / 海报图片 / 每次先问我。
2. 关注方向：模型发布、AI Agent、开源项目、产品工具、行业融资/大厂动态、论文研究，可多选。
3. 受众视角：创业者/投资人、开发者、产品/运营、研究者、企业采购/管理者。
4. 不想看什么：普通教程、Prompt 技巧、炒冷饭资讯、低质量营销稿、暂时不过滤。
5. 海报配置：OpenAI Images / MiniMax / 火山引擎方舟 / OpenRouter / 只生成海报 prompt / 暂不启用海报。

你也可以随时说：

```text
重新配置 AI 热点偏好
切换成文字模式
切换成海报模式
每次都问我
```

## 两种输出

文字资讯：

```text
文字版：今天 AI 圈有什么？
```

输出中文简报，包含分数、中文标题、一句话结论、为什么重要、适合谁关注、来源链接。

海报图片：

```text
把今天 AI 热点做成一张小红书海报。
```

默认用 OpenAI Images API，也可以在首次问卷或 `preferences.md` 里切换到 MiniMax、火山引擎方舟、OpenRouter 或自定义兼容接口。图片保存在：

```text
memory/posters/
```

海报图片模式需要配置对应 Provider 的 API Key：

```bash
export OPENAI_API_KEY="sk-..."
export MINIMAX_API_KEY="..."
export ARK_API_KEY="..."
export VOLCENGINE_API_KEY="..."
export OPENROUTER_API_KEY="..."
```

不要把 API Key 写进 `preferences.md`、`interests.md` 或仓库文件。

## 记忆文件

默认记忆目录：

```bash
$HOME/.openclaw/skills/ai-hot-radar/memory
```

可用环境变量覆盖：

```bash
AI_HOT_RADAR_MEMORY_ROOT=/path/to/persistent/memory
```

首次运行会创建：

```text
memory/
├── ledger.md
├── interests.md
├── preferences.md
├── briefings/
└── posters/
```

## OpenClaw 心跳

推荐配置：

```text
使用 ai-hot-radar 执行早报心跳。
使用 ai-hot-radar 执行晚报心跳。
使用 ai-hot-radar 执行重大快讯心跳，只在有 90 分以上新增事件时输出。
```

心跳默认走文字模式，除非你在 `preferences.md` 里明确设置 `heartbeat_output_mode: poster`。

## 数据源与评分

主数据源是 `AI HOT`，补充源包括官方/高质量 AI RSS 和 GitHub AI 趋势。详细源表见 `references/source-map.md`。

每条资讯最终得到 `0-100` 分。详细评分表见 `references/scoring-rubric.md`。

## License

MIT
