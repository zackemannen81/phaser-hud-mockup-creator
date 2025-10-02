# Roadmap — Phaser3.90_GameHUD-MockupCreator

> Full path from project start to finished product. Tasks show dependencies and recommended roles.

{% for m in milestones %}
## {{m.id}} — {{m.title}}
{% for t in m.tasks %}- **{{t.title}}** — feature: {{t.feature or "—"}}; asset: {{t.asset or "—"}}
  - Depends on: {{ ", ".join(t.depends_on) if t.depends_on else "None" }}
  - Recommended roles: {{ ", ".join(t.roles) if t.roles else "Unspecified" }}
{% endfor %}
{% endfor %}
