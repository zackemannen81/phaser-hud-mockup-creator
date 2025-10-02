#!/usr/bin/env python3
# agent_cli.py — robust CLI for task management + journal commits on main worktree
# See usage examples in the repository docs.

import sys, os, re, subprocess
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(__file__))
TASKS = os.path.join("tasks", "ProjectTasks.md")
JOURNAL = os.path.join("journal", "DeveloperJournal.md")
PROJECTINFO = os.path.join("docs", "ProjectInformation.md")

ALLOWED_STATUSES = {"TODO","IN_PROGRESS","REVIEW","DONE","BLOCKED","NEEDS_INFO","FAILED"}

ENV_MAIN_BRANCH = os.environ.get("MAIN_BRANCH", "main")
ENV_MAIN_WORKTREE = os.environ.get("MAIN_WORKTREE", "_main-worktree")
ENV_NO_GIT = os.environ.get("NO_GIT_COMMIT", "0") == "1"

def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def repo_root():
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=ROOT).decode().strip()
        return out
    except Exception:
        return ROOT

def ensure_main_worktree():
    # Return absolute path to the main worktree. If not present, create it.
    top = repo_root()
    wt = os.path.join(top, ENV_MAIN_WORKTREE)
    if not os.path.exists(wt):
        try:
            subprocess.check_call(["git", "worktree", "add", "-f", wt, ENV_MAIN_BRANCH], cwd=top)
        except subprocess.CalledProcessError:
            subprocess.check_call(["git", "worktree", "add", "-f", wt, f"origin/{ENV_MAIN_BRANCH}"], cwd=top)
    return wt

def run_git_commit_push(paths_changed, message):
    if ENV_NO_GIT:
        return
    top = repo_root()
    wt = ensure_main_worktree()
    if paths_changed:
        subprocess.check_call(["git", "-C", wt, "add"] + paths_changed)
    status = subprocess.check_output(["git", "-C", wt, "status", "--porcelain"]).decode()
    if not status.strip():
        return
    subprocess.check_call(["git", "-C", wt, "commit", "-m", message])
    try:
        subprocess.check_call(["git", "-C", wt, "pull", "--rebase", "origin", ENV_MAIN_BRANCH])
    except Exception:
        pass
    subprocess.check_call(["git", "-C", wt, "push", "origin", ENV_MAIN_BRANCH])

def read_text_from_main(rel_path):
    wt = ensure_main_worktree()
    p = os.path.join(wt, rel_path)
    with open(p, "r", encoding="utf-8") as fh:
        return fh.read()

def write_text_to_main(rel_path, content, commit_message):
    wt = ensure_main_worktree()
    p = os.path.join(wt, rel_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)
    run_git_commit_push([rel_path], commit_message)

TASK_RE = re.compile(
    r"^-\\s+TASK:\\s*(?P<title>.+?)\\s*\\n"
    r"\\s*owner:\\s*(?P<owner>.+?)\\s*\\n"
    r"(?:\\s*(?P<branch>[A-Za-z0-9_./-]+)\\s*\\n)?"
    r"\\s*status:\\s*(?P<status>[A-Z_]+)\\s*\\n"
    r"\\s*notes:\\s*(?P<notes>(?:.*?(?=\\n\\s*\\n|\\n-\\s+TASK:|\\Z)))",
    re.S | re.M
)

def parse_tasks(md):
    tasks = []
    for m in TASK_RE.finditer(md):
        d = m.groupdict()
        tasks.append({
            "title": d["title"].strip(),
            "owner": d["owner"].strip(),
            "branch": (d.get("branch") or "").strip() or None,
            "status": d["status"].strip(),
            "notes": (d["notes"] or "").strip(),
            "span": (m.start(), m.end()),
        })
    return tasks

def render_task_block(t):
    block = f"- TASK: {t['title']}\\n"
    block += f"  owner: {t['owner']}\\n"
    if t.get("branch"):
        block += f"  {t['branch']}\\n"
    block += f"  status: {t['status']}\\n"
    notes = (t.get("notes") or "").rstrip()
    if notes and not notes.endswith("\\n"):
        notes += "\\n"
    block += f"  notes: {notes}"
    return block

def replace_tasks_in_md(md, tasks):
    spans = [(t["span"], render_task_block(t)) for t in tasks]
    spans.sort(key=lambda x: x[0][0])
    out = []
    last = 0
    for (start, end), rep in spans:
        out.append(md[last:start])
        out.append(rep)
        last = end
    out.append(md[last:])
    return "".join(out)

def append_journal(agent, heading, bullets):
    try:
        txt = read_text_from_main(JOURNAL)
    except FileNotFoundError:
        txt = "# Developer Journal\\n\\n"
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if f"## {day}" not in txt:
        txt += f"\\n## {day}\\n"
    txt += f"\\n### {agent} — {heading}\\n"
    for b in bullets:
        txt += f"- {b}\\n"
    write_text_to_main(JOURNAL, txt, f"journal: {agent}: {heading}")

def cmd_list(args):
    md = read_text_from_main(TASKS)
    tasks = parse_tasks(md)
    for t in tasks:
        print(f"[{t['status']:^11}] {t['owner'] or 'OPEN':<14} — {t['title']}")

def _atomic_edit_tasks(edit_cb, commit_label):
    try:
        import fcntl  # type: ignore
    except Exception:
        fcntl = None
    wt = ensure_main_worktree()
    p = os.path.join(wt, TASKS)
    changed = False
    if fcntl and os.path.exists(p):
        with open(p, "r+", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            md = fh.read()
            tasks = parse_tasks(md)
            changed, tasks = edit_cb(tasks, md)
            if changed:
                new_md = replace_tasks_in_md(md, tasks)
                fh.seek(0); fh.truncate(); fh.write(new_md)
        if changed:
            run_git_commit_push([TASKS], commit_label)
    else:
        md = read_text_from_main(TASKS)
        tasks = parse_tasks(md)
        changed, tasks = edit_cb(tasks, md)
        if changed:
            new_md = replace_tasks_in_md(md, tasks)
            write_text_to_main(TASKS, new_md, commit_label)
    return changed

def cmd_pick(args):
    allow = {s.strip() for s in (args.allow or "TODO,NEEDS_INFO").split(",")}
    def edit(tasks, md):
        for t in tasks:
            if t["owner"] == "OPEN" and t["status"] in allow:
                t["owner"] = args.agent
                t["status"] = "IN_PROGRESS"
                if args.notes:
                    t["notes"] = (t.get("notes","") + ("" if not t.get("notes") else "\\n") + args.notes).strip()
                append_journal(args.agent, "Picked task", [f"**Task:** {t['title']}", f"**Time:** {now_utc()}", f"**Notes:** {args.notes or '—'}"])
                return True, tasks
        return False, tasks
    changed = _atomic_edit_tasks(edit, f"tasks: {args.agent}: pick")
    if not changed:
        print("No OPEN tasks matching allowed statuses.")
        return 1
    print("OK"); return 0

def cmd_current(args):
    md = read_text_from_main(TASKS)
    tasks = parse_tasks(md)
    for t in tasks:
        if t["owner"] == args.agent and t["status"] in {"IN_PROGRESS","REVIEW","BLOCKED","NEEDS_INFO"}:
            print(t["title"]); return 0
    print(""); return 0

def _update_task_by_title(title, agent, status=None, notes=None, allow_takeover=False, action_label="Update"):
    def edit(tasks, md):
        for t in tasks:
            if t["title"] == title:
                if t["owner"] not in ("OPEN", agent) and not allow_takeover:
                    raise SystemExit("Task already owned; use --force to take over.")
                if t["owner"] == "OPEN":
                    t["owner"] = agent
                if status:
                    if status not in ALLOWED_STATUSES:
                        raise SystemExit(f"Invalid status: {status}")
                    t["status"] = status
                if notes:
                    t["notes"] = (t.get("notes","") + ("" if not t.get("notes") else "\\n") + notes).strip()
                append_journal(agent, f"{action_label}: {title}", [f"**Status:** {t['status']}", f"**Time:** {now_utc()}", f"**Notes:** {notes or '—'}"])
                return True, tasks
        raise SystemExit("Task not found.")
    return _atomic_edit_tasks(edit, f"tasks: {agent}: {action_label.lower()}")

def cmd_start(args):
    _update_task_by_title(args.title, args.agent, status="IN_PROGRESS", notes=args.notes, allow_takeover=args.force, action_label="Start")
    print("OK")

def cmd_update(args):
    _update_task_by_title(args.title, args.agent, status=args.status, notes=args.notes, allow_takeover=args.force, action_label="Update")
    print("OK")

def cmd_finish(args):
    if args.status not in ALLOWED_STATUSES:
        raise SystemExit(f"Invalid status: {args.status}")
    _update_task_by_title(args.title, args.agent, status=args.status, notes=args.notes, allow_takeover=args.force, action_label="Finish")
    print("OK")

def cmd_ack(args):
    try:
        txt = read_text_from_main(PROJECTINFO)
    except FileNotFoundError:
        raise SystemExit("docs/ProjectInformation.md not found.")
    pattern = rf"(-\\s+{re.escape(args.notice)}:.*?\\n\\s*-\\s+Acknowledged by:\\s*\\n)"
    m = re.search(pattern, txt, flags=re.S)
    if not m:
        raise SystemExit("Notice not found or missing 'Acknowledged by:' section.")
    insert_at = m.end()
    line = f\"\"\"    - {args.agent} ({now_utc()})\n\"\"\"
    new_txt = txt[:insert_at] + line + txt[insert_at:]
    write_text_to_main(PROJECTINFO, new_txt, f"ack: {args.agent}: {args.notice}")
    append_journal(args.agent, f"ACK: {args.notice}", [f"**Time:** {now_utc()}"])
    print("OK")

def cmd_whoami(args):
    print(args.agent)

def main():
    import argparse
    p = argparse.ArgumentParser(prog="agent_cli.py", description="Task & journal manager that writes to main worktree.")
    sub = p.add_subparsers(dest="cmd")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--agent", required=True, help="Agent display name, e.g., 'Gemini CLI'")

    sub.add_parser("list").set_defaults(func=cmd_list)

    s = sub.add_parser("pick", parents=[common], help="Atomically pick an OPEN task (TODO/NEEDS_INFO by default).")
    s.add_argument("--allow", default="TODO,NEEDS_INFO", help="Comma-separated statuses allowed to pick from OPEN.")
    s.add_argument("--notes", default="")
    s.set_defaults(func=cmd_pick)

    s = sub.add_parser("current", parents=[common], help="Print current task title for this agent (if any).")
    s.set_defaults(func=cmd_current)

    s = sub.add_parser("start", parents=[common], help="Set task to IN_PROGRESS by exact title.")
    s.add_argument("title")
    s.add_argument("--notes", default="")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_start)

    s = sub.add_parser("update", parents=[common], help="Update task status and/or notes by exact title.")
    s.add_argument("title")
    s.add_argument("--status", choices=sorted(ALLOWED_STATUSES))
    s.add_argument("--notes", default="")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("finish", parents=[common], help="Finish a task by setting a terminal status (e.g., REVIEW/DONE).")
    s.add_argument("title")
    s.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUSES))
    s.add_argument("--notes", default="")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_finish)

    s = sub.add_parser("ack", parents=[common], help="Acknowledge a project notice in docs/ProjectInformation.md")
    s.add_argument("notice")
    s.set_defaults(func=cmd_ack)

    s = sub.add_parser("whoami", parents=[common], help="Echo back agent name (debug).")
    s.set_defaults(func=cmd_whoami)

    args = p.parse_args()
    if not args.cmd:
        p.print_help(); sys.exit(0)
    rc = args.__dict__["func"](args)
    sys.exit(rc if isinstance(rc, int) else 0)

if __name__ == "__main__":
    main()
