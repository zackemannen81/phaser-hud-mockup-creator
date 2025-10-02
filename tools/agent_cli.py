#!/usr/bin/env python3
import sys, os, re
from datetime import datetime, timezone
ROOT = os.path.dirname(os.path.dirname(__file__))
TASKS = os.path.join(ROOT, "tasks", "ProjectTasks.md")
JOURNAL = os.path.join(ROOT, "journal", "DeveloperJournal.md")
PROJECTINFO = os.path.join(ROOT, "docs", "ProjectInformation.md")
ALLOWED = {"TODO","IN_PROGRESS","REVIEW","DONE","BLOCKED","NEEDS_INFO","FAILED"}

try:
    import fcntl
except Exception:
    fcntl = None

def now_utc(): return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def read_tasks():
    txt = open(TASKS, "r", encoding="utf-8").read()
    # Matcha ett helt block och låt notes spilla över tills nästa "- TASK:" eller EOF
    pattern = r"^- TASK:\s*(?P<title>.+?)\r?\n\s*owner:\s*(?P<owner>.+?)\r?\n\s*status:\s*(?P<status>.+?)\r?\n\s*notes:\s*(?P<notes>(?:.*?))(?=\n- TASK:|\Z)"
    blocks = re.finditer(pattern, txt, flags=re.S | re.M)
    out = []
    for m in blocks:
        g = m.groupdict()
        out.append({k: g[k].strip() for k in ["title","owner","status","notes"]})
    return out

def write_tasks(tasks):
    hdr="# ProjectTasks\n\n> Canonical task list. Agents may only modify their own `owner/status/notes` fields.\n\n"
    parts=[]
    for x in tasks:
        notes=x.get("notes","").rstrip()
        if notes and not notes.endswith("\\n"): notes+="\\n"
        parts.append(f"- TASK: {x['title']}\\n  owner: {x['owner']}\\n  status: {x['status']}\\n  notes: {notes}\\n")
    open(TASKS,"w",encoding="utf-8").write(hdr+"".join(parts))

def append_journal(agent, heading, bullets):
    day=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not os.path.exists(JOURNAL): open(JOURNAL,"w",encoding="utf-8").write("# Developer Journal\\n\\n")
    txt=open(JOURNAL,"r",encoding="utf-8").read()
    if f"## {day}" not in txt: txt += f"\\n## {day}\\n"
    txt += f"\\n### {agent} — {heading}\\n"
    for b in bullets: txt += f"- {b}\\n"
    open(JOURNAL,"w",encoding="utf-8").write(txt)

def cmd_list(args):
    for t in read_tasks(): print(f"[{t['status']:^11}] {t['owner'] or 'OPEN':<14} — {t['title']}")

def cmd_start(args):
    tasks=read_tasks()
    for t in tasks:
        if t["title"]==args.title:
            if t["owner"]!="OPEN" and not args.force: print("Task already owned; use --force.", file=sys.stderr); sys.exit(1)
            t["owner"]=args.agent; t["status"]="IN_PROGRESS"
            if args.notes: t["notes"]=(t.get("notes","")+("\\n" if t.get("notes") else "")+args.notes).strip()
            write_tasks(tasks); append_journal(args.agent,f"Started: {t['title']}",[f"**Time:** {now_utc()}",f"**Notes:** {args.notes or '—'}"]); print("OK"); return
    print("Task not found", file=sys.stderr); sys.exit(1)

def cmd_update(args):
    tasks=read_tasks()
    for t in tasks:
        if t["title"]==args.title:
            if t["owner"]!=args.agent and not args.force: print("Not owner; use --force.", file=sys.stderr); sys.exit(1)
            if args.status:
                if args.status not in ALLOWED: print("Invalid status", file=sys.stderr); sys.exit(1)
                t["status"]=args.status
            if args.notes: t["notes"]=(t.get("notes","")+("\\n" if t.get("notes") else "")+args.notes).strip()
            write_tasks(tasks); append_journal(args.agent,f"Update: {t['title']}",[f"**Time:** {now_utc()}",f"**Status:** {t['status']}",f"**Notes:** {args.notes or '—'}"]); print("OK"); return
    print("Task not found", file=sys.stderr); sys.exit(1)

def cmd_finish(args):
    tasks=read_tasks()
    if args.status not in ALLOWED: print("Invalid status", file=sys.stderr); sys.exit(1)
    for t in tasks:
        if t["title"]==args.title:
            if t["owner"]!=args.agent and not args.force: print("Not owner; use --force.", file=sys.stderr); sys.exit(1)
            t["status"]=args.status
            if args.notes: t["notes"]=(t.get("notes","")+("\\n" if t.get("notes") else "")+args.notes).strip()
            write_tasks(tasks); append_journal(args.agent,f"Finished: {t['title']} → {args.status}",[f"**Time:** {now_utc()}",f"**Notes:** {args.notes or '—'}"]); print("OK"); return
    print("Task not found", file=sys.stderr); sys.exit(1)

def cmd_ack(args):
    if not os.path.exists(PROJECTINFO): print("ProjectInformation.md not found", file=sys.stderr); sys.exit(1)
    txt=open(PROJECTINFO,"r",encoding="utf-8").read()
    m=re.search(rf"- {re.escape(args.notice)}:.*?\\n\\s*- Acknowledged by:\\s*\\n", txt, flags=re.S)
    if not m: print("Notice not found", file=sys.stderr); sys.exit(1)
    pos=m.end(); line=f"    - {args.agent} ({now_utc()})\\n"
    txt=txt[:pos]+line+txt[pos:]
    open(PROJECTINFO,"w",encoding="utf-8").write(txt)
    append_journal(args.agent, f"ACK: {args.notice}", [f"**Time:** {now_utc()}"])
    print("OK")

def cmd_pick(args):
    def pick(tasks):
        allowed={s.strip() for s in (args.allow or 'TODO,NEEDS_INFO').split(',')}
        for t in tasks:
            if t['owner']=='OPEN' and t['status'] in allowed: return t
        return None
    try:
        import fcntl
    except Exception:
        fcntl=None
    if fcntl:
        with open(TASKS, "r+", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            tasks=read_tasks(); chosen=pick(tasks)
            if not chosen: print("No OPEN tasks matching allowed statuses."); fcntl.flock(fh, fcntl.LOCK_UN); return 1
            chosen['owner']=args.agent; chosen['status']='IN_PROGRESS'
            if args.notes: chosen['notes']=(chosen.get('notes','')+("\\n" if chosen.get('notes') else "")+args.notes).strip()
            write_tasks(tasks); fcntl.flock(fh, fcntl.LOCK_UN)
    else:
        tasks=read_tasks(); chosen=pick(tasks)
        if not chosen: print("No OPEN tasks matching allowed statuses."); return 1
        chosen['owner']=args.agent; chosen['status']='IN_PROGRESS'
        if args.notes: chosen['notes']=(chosen.get('notes','')+("\\n" if chosen.get('notes') else "")+args.notes).strip()
        write_tasks(tasks)
    append_journal(args.agent, f"Started: {chosen['title']}", [f"**Time:** {now_utc()}", f"**Notes:** {args.notes or '—'}"])
    print(f"Picked: {chosen['title']}"); return 0

def cmd_current(args):
    for t in read_tasks():
        if t['owner']==args.agent and t['status']=='IN_PROGRESS': print(t['title']); return
    print("")

def main():
    import argparse
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd")
    common=argparse.ArgumentParser(add_help=False); common.add_argument("--agent", required=True)
    s=sub.add_parser("list"); s.set_defaults(func=cmd_list)
    s=sub.add_parser("start", parents=[common]); s.add_argument("title"); s.add_argument("--notes", default=""); s.add_argument("--force", action="store_true"); s.set_defaults(func=cmd_start)
    s=sub.add_parser("update", parents=[common]); s.add_argument("title"); s.add_argument("--status"); s.add_argument("--notes", default=""); s.add_argument("--force", action="store_true"); s.set_defaults(func=cmd_update)
    s=sub.add_parser("finish", parents=[common]); s.add_argument("title"); s.add_argument("--status", required=True); s.add_argument("--notes", default=""); s.add_argument("--force", action="store_true"); s.set_defaults(func=cmd_finish)
    s=sub.add_parser("ack", parents=[common]); s.add_argument("notice"); s.set_defaults(func=cmd_ack)
    s=sub.add_parser("pick", parents=[common]); s.add_argument("--allow", default="TODO,NEEDS_INFO"); s.add_argument("--notes", default=""); s.set_defaults(func=cmd_pick)
    s=sub.add_parser("current", parents=[common]); s.set_defaults(func=cmd_current)
    args=p.parse_args(); 
    if not args.cmd: p.print_help(); sys.exit(0)
    rc=args.__dict__['func'](args); sys.exit(rc if isinstance(rc,int) else 0)
if __name__=="__main__": main()
