#!/usr/bin/env bash
set -euo pipefail
DEST="${1:-../worktree-main}"
git worktree add "$DEST" main
echo "[worktree] Created at $DEST"
