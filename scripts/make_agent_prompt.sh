#!/usr/bin/env bash
set -euo pipefail
AGENT="${1:-Gemini CLI}"
SLUG="$(echo "$AGENT" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr -cd '[:alnum:]_')"
OUT="agent_prompts/${SLUG}.md"
sed "s/{{AGENT_NAME}}/${AGENT}/g; s/{{AGENT_SLUG}}/${SLUG}/g" docs/AGENT_PROMPT_TEMPLATE.md > "$OUT"
echo "[agent_prompt] Wrote $OUT"
