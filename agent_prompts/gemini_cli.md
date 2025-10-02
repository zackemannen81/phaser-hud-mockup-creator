# Agent Start Prompt — Gemini CLI

You are **Gemini CLI** working in this repository. Follow the process exactly.

Read: docs/BEST_PRACTICES.md, docs/PROJECT_OVERVIEW.md, docs/ProjectInformation.md, docs/DEVELOPMENT_PLAN.md, docs/ROADMAP.md

ACK notice:
```bash
python3 tools/agent_cli.py ack NOTICE-2025-10-03 --agent "Gemini CLI" --notes "Policy OK"
```

Self-pick (atomic):
```bash
python3 tools/agent_cli.py pick --agent "Gemini CLI" --notes "Auto-picked" || echo "No OPEN tasks"
python3 tools/agent_cli.py current --agent "Gemini CLI"
slug=$(python3 -c "import re,sys; print(re.sub(r'[^a-z0-9]+','-', sys.argv[1].lower()).strip('-'))" "$(python3 tools/agent_cli.py current --agent 'Gemini CLI')")
ASLUG="gemini_cli"
git switch -c "feature/${ASLUG}/${slug}" || git checkout -b "feature/${ASLUG}/${slug}"
git add -A && git commit -m "feat(${ASLUG}): $(python3 tools/agent_cli.py current --agent 'Gemini CLI') (initial)"
git push -u origin "feature/${ASLUG}/${slug}"
command -v gh >/dev/null && gh pr create --base main --head "feature/${ASLUG}/${slug}" --title "feat: $(python3 tools/agent_cli.py current --agent 'Gemini CLI')" --body "Auto-PR by Gemini CLI"

if command -v gh >/dev/null; then PR=$(gh pr view --json number -q .number || echo ""); NOTES="PR opened"; [ -n "$PR" ] && NOTES="PR #$PR opened"; else NOTES="PR opened"; fi
python3 tools/agent_cli.py finish "$(python3 tools/agent_cli.py current --agent 'Gemini CLI')" --agent "Gemini CLI" --status "REVIEW" --notes "$NOTES"
git checkout main && git pull --rebase || true
