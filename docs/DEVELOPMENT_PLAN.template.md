# Development Plan — Phaser3.90_GameHUD-MockupCreator

## Product / Service Specification (English)
**Summary:** {{product.summary}}

### Objectives
{% for o in product.objectives %}- {{o}}
{% endfor %}

### Target Users & Needs
{% for u in product.users %}- **{{u.name}}** — needs: {{ ", ".join(u.needs) }}
{% endfor %}

### Features
{% for f in product.features %}
#### {{f.id}} — {{f.title}}
- Description: {{f.description}}
- Acceptance Criteria:
{% for a in f.acceptance %}  - {{a}}
{% endfor %}
- Dependencies: {{ ", ".join(f.dependencies) if f.dependencies else "None" }}
- Required roles: {{ ", ".join(f.roles) if f.roles else "Unspecified" }}
{% endfor %}

## Assets & Non-code Resources
{% if assets.media %}
### Media
{% for a in assets.media %}- {{a.id}} — {{a.type}} — {{a.description}} (Owner role: {{a.owner_role}})
{% endfor %}
{% endif %}

## Infrastructure
- Hosting: {{infra.hosting.provider}} — {{infra.hosting.notes}}
- Backend needed: {{ "Yes" if infra.backend.need_backend else "No" }}
{% if infra.backend.api_integrations %}- API integrations: {{ ", ".join(infra.backend.api_integrations) }}
{% endif %}
- Database needed: {{ "Yes" if infra.database.need_db else "No" }}
{% if infra.database.need_db %}- DB Engine: {{ infra.database.engine }} — {{ infra.database.notes }}
{% endif %}
