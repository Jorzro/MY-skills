#!/usr/bin/env bash
# AI Hot Radar Agent Skill installer
# Default: OpenClaw skill directory.
# Override:
#   SKILL_DIR=$HOME/.codex/skills/ai-hot-radar bash <(curl -fsSL -H 'Accept: application/vnd.github.raw' 'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main')

set -e

DEFAULT_DIR="$HOME/.openclaw/skills/ai-hot-radar"
SKILL_DIR="${SKILL_DIR:-$DEFAULT_DIR}"
GITHUB_REF="${GITHUB_REF:-main}"
BASE_URL="${BASE_URL:-https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar}"
CURL_OPTS=(-fsSL --retry 3 --connect-timeout 10 --max-time 60)

download() {
  local path="$1"
  local output="$2"

  if [[ "$BASE_URL" == https://api.github.com/* ]]; then
    curl "${CURL_OPTS[@]}" \
      -H "Accept: application/vnd.github.raw" \
      "$BASE_URL/$path?ref=$GITHUB_REF" \
      -o "$output"
  else
    curl "${CURL_OPTS[@]}" "$BASE_URL/$path" -o "$output"
  fi
}

echo ""
echo "Installing AI Hot Radar Agent Skill"
echo "  -> $SKILL_DIR"
echo ""

mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/agents" "$SKILL_DIR/scripts"

download "SKILL.md" "$SKILL_DIR/SKILL.md"
download "README.md" "$SKILL_DIR/README.md"
download "AGENT_USAGE.md" "$SKILL_DIR/AGENT_USAGE.md"
download "LICENSE" "$SKILL_DIR/LICENSE"
download "references/scoring-rubric.md" "$SKILL_DIR/references/scoring-rubric.md"
download "references/source-map.md" "$SKILL_DIR/references/source-map.md"
download "references/output-style.md" "$SKILL_DIR/references/output-style.md"
download "references/poster-guide.md" "$SKILL_DIR/references/poster-guide.md"
download "scripts/generate_openai_poster.py" "$SKILL_DIR/scripts/generate_openai_poster.py"
download "scripts/render_news_poster.py" "$SKILL_DIR/scripts/render_news_poster.py"
download "agents/openai.yaml" "$SKILL_DIR/agents/openai.yaml"

chmod +x "$SKILL_DIR/scripts/generate_openai_poster.py"
chmod +x "$SKILL_DIR/scripts/render_news_poster.py"

echo ""
echo "Done."
echo ""
echo "Next: restart your Agent or start a new conversation, then try:"
echo "  - 今天 AI 圈有什么？按重要度打分。"
echo "  - 最近 24 小时最重磅 AI 新闻。"
echo "  - OpenAI 最近发了什么？"
echo "  - 把今天 AI 热点做成一张小红书海报。"
echo ""
echo "Poster images require the selected provider key in your Agent Secret or environment:"
echo "  OpenAI:     export OPENAI_API_KEY=\"sk-...\""
echo "  MiniMax:    export MINIMAX_API_KEY=\"...\""
echo "  Volcengine: export ARK_API_KEY=\"...\"  # or VOLCENGINE_API_KEY"
echo "  OpenRouter: export OPENROUTER_API_KEY=\"...\""
echo ""
echo "Other Agent platforms:"
echo "  Codex:  SKILL_DIR=\$HOME/.codex/skills/ai-hot-radar bash <(curl -fsSL -H 'Accept: application/vnd.github.raw' 'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main')"
echo "  Claude: SKILL_DIR=\$HOME/.claude/skills/ai-hot-radar bash <(curl -fsSL -H 'Accept: application/vnd.github.raw' 'https://api.github.com/repos/Jorzro/MY-skills/contents/ai-hot-radar/install.sh?ref=main')"
echo ""
