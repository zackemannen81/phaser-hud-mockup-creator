#!/usr/bin/env python3
import sys, os, yaml, re
from jinja2 import Template

ROOT = os.path.dirname(os.path.dirname(__file__))

def load_yaml(fp):
    import io
    with open(fp, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def slugify(s): return re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')

def render(tmpl_path, ctx, out_path):
    tmpl = open(tmpl_path,'r',encoding='utf-8').read()
    out = Template(tmpl).render(**ctx)
    open(out_path,'w',encoding='utf-8').write(out)

def gen_tasks(roadmap, features):
    feat = {f['id']: f for f in features}
    out = ["# ProjectTasks\n\n> Canonical task list. Agents may only modify their own `owner/status/notes` fields.\n\n"]
    for m in roadmap['milestones']:
        out.append(f"<!-- Milestone {m['id']} — {m['title']} -->\n")
        for t in m['tasks']:
            notes = []
            if t.get('feature'): notes.append(f"feature: {t['feature']} — {feat.get(t['feature'],{}).get('title','')}")
            if t.get('asset'): notes.append(f"asset: {t['asset']}")
            if t.get('depends_on'): notes.append("depends_on: " + ", ".join(t['depends_on']))
            if t.get('roles'): notes.append("roles: " + ", ".join(t['roles']))
            out.append(f"- TASK: {t['title']}\n  owner: OPEN\n  status: TODO\n  notes: " + ("; ".join(notes)) + "\n\n")
    return "".join(out)

def main():
    if len(sys.argv)<2:
        print("Usage: specgen.py configs/spec.yaml"); sys.exit(1)
    spec = load_yaml(sys.argv[1])
    ctx = {
        "PROJECT_NAME": spec["project"]["name"],
        "PROJECT_SLUG": spec["project"]["slug"],
        "PROJECT_VISION": spec["project"]["vision"],
        "PROJECT_SUPERVISOR": spec["project"]["supervisor"],
        "product": spec["product_spec"],
        "assets": spec.get("assets", {}),
        "infra": spec.get("infrastructure", {}),
        "milestones": spec["roadmap"]["milestones"],
    }
    render(os.path.join(ROOT,"docs","DEVELOPMENT_PLAN.template.md"), ctx, os.path.join(ROOT,"docs","DEVELOPMENT_PLAN.md"))
    render(os.path.join(ROOT,"docs","ROADMAP.template.md"), ctx, os.path.join(ROOT,"docs","ROADMAP.md"))
    tasks_md = gen_tasks(spec["roadmap"], spec["product_spec"]["features"])
    open(os.path.join(ROOT,"tasks","ProjectTasks.md"),"w",encoding="utf-8").write(tasks_md)
    print("Generated docs/DEVELOPMENT_PLAN.md, docs/ROADMAP.md, tasks/ProjectTasks.md")

if __name__ == "__main__":
    main()
