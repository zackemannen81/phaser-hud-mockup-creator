#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI="$ROOT/tools/agent_cli.py"
if [ "${AUTO_ASSIGN:-0}" = "1" ]; then
  agents=()
  if [ -n "${ONLY_AGENT:-}" ]; then IFS=',' read -r -a agents <<< "$ONLY_AGENT"
  elif [ -n "${AGENT_LIST:-}" ]; then IFS=',' read -r -a agents <<< "$AGENT_LIST"
  else agents=("Gemini CLI" "Gemini CLI #2" "Claude Code (CLI)" "OpenAI Codex CLI #1" "OpenAI Codex CLI #2"); fi
  max=${MAX_ASSIGN:-0}; count=0
  for a in "${agents[@]}"; do python3 "$CLI" ack NOTICE-2025-10-03 --agent "$a" --notes "Auto-ACK" || true; done
  while true; do
    for a in "${agents[@]}"; do
      python3 "$CLI" pick --agent "$a" --notes "Auto-assign by orchestrator" || true
      count=$((count+1)); if [ "$max" -gt 0 ] && [ "$count" -ge "$max" ]; then exit 0; fi
    done
    [ "${LOOP:-0}" = "1" ] || break
    sleep "${SLEEP:-5}"
  done
fi
echo "Done."
