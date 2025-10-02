#!/usr/bin/env bash
set -euo pipefail
AGENT="${AGENT:-Reviewer}"
DELETE_BRANCH="${DELETE_BRANCH:-1}"
titles=$(python3 - <<'PY'
import re, pathlib
txt = pathlib.Path('tasks/ProjectTasks.md').read_text(encoding='utf-8')
print("\n".join([t.strip() for t,_,_ in re.findall(r"- TASK:\s*(.+?)\n\s*owner:\s*(.+?)\n\s*status:\s*REVIEW\s*\n", txt, flags=re.S)]))
PY
)
[ -z "$titles" ] && echo "No tasks in REVIEW." && exit 0
for title in $titles; do
  echo "------------------------------------------------------------"
  echo "Task in REVIEW: $title"
  read -p "OK to merge? (J/N): " ans
  if [[ ! "$ans" =~ ^[Jj]$ ]]; then echo "Skipping."; continue; fi
  python3 tools/agent_cli.py finish "$title" --agent "$AGENT" --status "DONE" --notes "Approved by reviewer"
  if command -v gh >/dev/null 2>&1; then
    prnum=$(gh pr list --state open --search "$title" --json number --jq '.[0].number' || echo "")
    if [ -n "$prnum" ]; then
      del="--delete-branch"; [ "$DELETE_BRANCH" = "1" ] || del=""
      gh pr merge "$prnum" --squash $del || true
    else
      echo "No open PR found for '$title'."
    fi
  else
    echo "gh CLI not found; please merge manually."
  fi
  git checkout main
  git pull --rebase || true
done
