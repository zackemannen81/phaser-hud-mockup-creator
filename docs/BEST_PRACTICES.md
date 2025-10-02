# BEST_PRACTICES

- Keep **tasks/journal updates on `main`**; code in feature branches.
- Use `tools/agent_cli.py pick/start/update/finish/ack` to ensure journal entries.
- PRs should include **only code/docs inside the branch**, not tasks/journal on `main`.
- Prefer squash merges. Delete merged branches to keep repo clean.
- Use `scripts/prepare_worktree.sh` to maintain a `main` worktree for easy task updates.
