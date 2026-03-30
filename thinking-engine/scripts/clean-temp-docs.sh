#!/bin/bash
# thinking-engine/scripts/clean-temp-docs.sh
# 清理各Agent临时文档目录（7天前文件）
# 注意：此脚本是辅助工具，thinking-engine skill 本身不需要它
# 它用于清理通过飞书发送的临时文档，避免误清核心框架文件

AGENTS=("content" "finance" "dev" "research" "ops" "fortune" "product" "secretary")
BASE_DIR="/root/.openclaw/agents"
MAX_AGE_DAYS=7

echo "=== 临时文档清理 $(date '+%Y-%m-%d %H:%M') ==="

for agent in "${AGENTS[@]}"; do
  TEMP_DIR="$BASE_DIR/$agent/workspace/temp-docs"
  if [[ -d "$TEMP_DIR" ]]; then
    COUNT=$(find "$TEMP_DIR" -type f -mtime +${MAX_AGE_DAYS} 2>/dev/null | wc -l)
    if [[ $COUNT -gt 0 ]]; then
      find "$TEMP_DIR" -type f -mtime +${MAX_AGE_DAYS} -delete 2>/dev/null
      echo "✅ $agent: 清理 $COUNT 个过期文件"
    else
      echo "➖ $agent: 无过期文件"
    fi
  else
    echo "⚠️  $agent: 目录不存在，跳过"
  fi
done

echo "=== 清理完成 ==="
