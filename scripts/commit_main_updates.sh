#!/usr/bin/env bash
set -Eeuo pipefail

# commit_main_updates.sh
# Commit & push updates to main (tasks/journal/notices) via a dedicated worktree.
# Usage:
#   scripts/commit_main_updates.sh [--agent "Name"] [--note "text"] [--main-dir PATH] [--extra "path1,path2,..."]
#
# Defaults:
#   --main-dir defaults to ../_main (override with WORKTREE_MAIN env or flag)
#
# Example:
#   AGENT="Gemini CLI" NOTE="PR #12 opened" scripts/commit_main_updates.sh --agent "$AGENT" --note "$NOTE"
#
# Requires: git 2.5+ (for worktree), remote 'origin' tracking main, and this repo as CWD.
#
# This script:
#   1) Ensures a worktree for 'main' exists at --main-dir (or creates it)
#   2) Pulls latest main (rebase)
#   3) Stages known status files (tasks/journal/ProjectInformation + optional extras)
#   4) Commits if there are changes, and pushes
#
# Notes:
#   - We use 'git -C <dir>' to safely run git in the worktree dir.
#   - We use 'git status --porcelain' to decide if there is anything to commit.
#
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

AGENT=""
NOTE=""
MAIN_DIR="${WORKTREE_MAIN:-../_main}"
EXTRA=""

usage() {
  cat <<EOF
Usage: $0 [--agent "Name"] [--note "text"] [--main-dir PATH] [--extra "path1,path2,..."]

Commits status files to 'main' via a dedicated worktree and pushes.
EOF
}

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)    AGENT="${2:-}"; shift 2;;
    --note)     NOTE="${2:-}"; shift 2;;
    --main-dir) MAIN_DIR="${2:-}"; shift 2;;
    --extra)    EXTRA="${2:-}"; shift 2;;
    -h|--help)  usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 2;;
  esac
done

# Ensure we're in a git repo
git rev-parse --git-dir >/dev/null 2>&1 || { echo "❌ Not a git repository here."; exit 1; }

# Ensure worktree exists for 'main'
if [[ ! -d "$MAIN_DIR/.git" ]]; then
  # Ensure local main exists; create tracking branch if needed
  if ! git show-ref --verify --quiet refs/heads/main; then
    if git show-ref --verify --quiet refs/remotes/origin/main; then
      echo "[commit-main] Creating local tracking branch 'main' for origin/main"
      git branch --track main origin/main
    else
      echo "❌ Cannot find 'main' locally or on origin. Aborting."; exit 3
    fi
  fi

  echo "[commit-main] Adding worktree for 'main' at: $MAIN_DIR"
  mkdir -p "$MAIN_DIR"
  git worktree add "$MAIN_DIR" main
fi

echo "[commit-main] Updating 'main' worktree..."
git -C "$MAIN_DIR" fetch --all --prune
git -C "$MAIN_DIR" pull --rebase --autostash || true

# Files we manage by default
paths=(
  "tasks/ProjectTasks.md"
  "journal/DeveloperJournal.md"
  "docs/ProjectInformation.md"
)

# Extra paths (comma-separated)
IFS=',' read -r -a extra_paths <<< "$EXTRA"
for p in "${extra_paths[@]:-}"; do
  [[ -n "$p" ]] && paths+=("$p")
done

# Stage files if present
for p in "${paths[@]}"; do
  if [[ -f "$MAIN_DIR/$p" ]]; then
    git -C "$MAIN_DIR" add "$p"
  fi
done

# Check if there is anything to commit (restrict to our paths)
if [[ -z "$(git -C "$MAIN_DIR" status --porcelain -- ${paths[@]})" ]]; then
  echo "[commit-main] No changes to commit on 'main'."
  exit 0
fi

ts="$(date -u +'%Y-%m-%d %H:%M:%S UTC')"
msg="chore(tasks): status update"
[[ -n "$AGENT" ]] && msg="$msg by $AGENT"
msg="$msg ($ts)"
[[ -n "$NOTE" ]] && msg="$msg — $NOTE"

echo "[commit-main] Committing: $msg"
git -C "$MAIN_DIR" commit -m "$msg"
echo "[commit-main] Pushing..."
git -C "$MAIN_DIR" push

echo "[commit-main] Done."
