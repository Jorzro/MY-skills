#!/usr/bin/env bash
# AI Hot Radar Agent Skill installer
# Default: OpenClaw skill directory.
# Override:
#   SKILL_DIR=$HOME/.codex/skills/ai-hot-radar bash <(curl -fsSL https://raw.githubusercontent.com/Jorzro/MY-skills/refs/heads/main/ai-hot-radar/install.sh)

set -e

DEFAULT_DIR="$HOME/.openclaw/skills/ai-hot-radar"
SKILL_DIR="${SKILL_DIR:-$DEFAULT_DIR}"
BASE_URL="${BASE_URL:-https://raw.githubusercontent.com/Jorzro/MY-skills/refs/heads/main/ai-hot-radar}"
CURL_OPTS=(-fsSL --retry 3 --connect-timeout 10 --max-time 60)

echo ""
echo "Installing AI Hot Radar Agent Skill"
echo "  -> $SKILL_DIR"
echo ""

mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/agents"

curl "${CURL_OPTS[@]}" "$BASE_URL/SKILL.md" -o "$SKILL_DIR/SKILL.md"
curl "${CURL_OPTS[@]}" "$BASE_URL/README.md" -o "$SKILL_DIR/README.md"
curl "${CURL_OPTS[@]}" "$BASE_URL/AGENT_USAGE.md" -o "$SKILL_DIR/AGENT_USAGE.md"
curl "${CURL_OPTS[@]}" "$BASE_URL/LICENSE" -o "$SKILL_DIR/LICENSE"
curl "${CURL_OPTS[@]}" "$BASE_URL/references/scoring-rubric.md" -o "$SKILL_DIR/references/scoring-rubric.md"
curl "${CURL_OPTS[@]}" "$BASE_URL/references/source-map.md" -o "$SKILL_DIR/references/source-map.md"
curl "${CURL_OPTS[@]}" "$BASE_URL/agents/openai.yaml" -o "$SKILL_DIR/agents/openai.yaml"

echo ""
echo "Done."
echo ""
echo "Next: restart your Agent or start a new conversation, then try:"
echo "  - 今天 AI 圈有什么？按重要度打分。"
echo "  - 最近 24 小时最重磅 AI 新闻。"
echo "  - OpenAI 最近发了什么？"
echo ""
echo "Other Agent platforms:"
echo "  Codex:  SKILL_DIR=\$HOME/.codex/skills/ai-hot-radar bash <(curl -fsSL $BASE_URL/install.sh)"
echo "  Claude: SKILL_DIR=\$HOME/.claude/skills/ai-hot-radar bash <(curl -fsSL $BASE_URL/install.sh)"
echo ""
