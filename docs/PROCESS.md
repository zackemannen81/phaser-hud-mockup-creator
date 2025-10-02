# Team Development Process

This repository follows a *single-source-of-truth* model for tasks and journals. Changes to these are written directly to `main` through a dedicated worktree by the CLI.

## Branching
- `main` — protected. Never commit code directly.
- `feature/{agent_slug}/{task-slug}` — one per active task.
- Pull Requests always target `main`.

## Tasks & Journal
- The canonical list lives in `tasks/ProjectTasks.md`.
- The canonical journal lives in `journal/DeveloperJournal.md`.
- Agents must use `tools/agent_cli.py` for *all* updates. The CLI will:
  - Write to a `_main-worktree` checked out on `main`.
  - Commit & push immediately after each change.

## Status flow
OPEN/TODO → IN_PROGRESS → REVIEW → (DONE | NEEDS_INFO | BLOCKED | FAILED)

## Concurrency
- `pick` is atomic with file locking (UNIX).
- If you must take over someone else's task, pass `--force` to `start/update/finish` (use sparingly).

## Commits
- Small, isolated, with meaningful messages.
- PRs must **not** include changes to `tasks/` or `journal/`.
