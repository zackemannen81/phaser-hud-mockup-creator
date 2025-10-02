#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${1:-}"
git init -q
git branch -m main || true
git add .
git commit -m "chore: bootstrap project from template v3" -q
if [ -n "$REPO_URL" ]; then
  git remote add origin "$REPO_URL" || true
  git push -u origin main || true
fi
echo "[init_repo] Done."
