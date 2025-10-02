#!/usr/bin/env bash
set -euo pipefail
AGENT="${AGENT:-Reviewer}"
DELETE_BRANCH="${DELETE_BRANCH:-1}"
# === Hämta alla REVIEW-titlar robust ===
titles=$(python3 - <<'PY'
import re, pathlib
txt = pathlib.Path('tasks/ProjectTasks.md').read_text(encoding='utf-8')
# Tålig blockmatchning: hanterar CRLF/LF och flerradiga notes
pat = r"^- TASK:\s*(?P<title>.+?)\r?\n\s*owner:\s*(?P<owner>.+?)\r?\n\s*status:\s*(?P<status>.+?)\r?\n\s*notes:\s*(?P<notes>(?:.*?))(?=\n- TASK:|\Z)"
blocks = re.finditer(pat, txt, flags=re.M|re.S)
print("\n".join(m.group('title').strip() for m in blocks if m.group('status').strip() == "REVIEW"))
PY
)

# === Iterera rad-för-rad (bevara mellanslag) ===
has_any=0
while IFS= read -r title; do
  [ -z "$title" ] && continue
  has_any=1
  echo "----------------------------------------------"
  echo "Task i REVIEW: $title"
  read -p "OK att merga? (J/N): " ans
  if [[ "$ans" =~ ^[JjYy]$ ]]; then
    # TODO: hitta PR, merga, sätt DONE osv (din befintliga logik här)
    :
  else
    echo "Hoppar över: $title"
  fi
done <<< "$titles"

if [ $has_any -eq 0 ]; then
  echo "Inga tasks i REVIEW just nu."
fi
