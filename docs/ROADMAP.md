# Roadmap — Phaser3.90_GameHUD-MockupCreator

> Full path from project start to finished product. Tasks show dependencies and recommended roles.


## M1 — Editor Core MVP
- **Setup Phaser 3.90 project & stage** — feature: F-001; asset: —
  - Depends on: None
  - Recommended roles: Frontend Dev
- **Selection + drag move + snap-to-grid** — feature: F-002; asset: —
  - Depends on: Setup Phaser 3.90 project & stage
  - Recommended roles: Frontend Dev
- **Layers panel + grouping via Containers** — feature: F-003; asset: —
  - Depends on: Selection + drag move + snap-to-grid
  - Recommended roles: Frontend Dev
- **Properties panel (x/y/size/angle/alpha/anchor)** — feature: F-004; asset: —
  - Depends on: Layers panel + grouping via Containers
  - Recommended roles: Frontend Dev


## M2 — Assets, Text & Panels
- **Asset Manager (images/atlases) + drag to canvas** — feature: F-006; asset: —
  - Depends on: Properties panel (x/y/size/angle/alpha/anchor)
  - Recommended roles: Frontend Dev
- **WebFont + BitmapText support** — feature: F-005; asset: —
  - Depends on: Properties panel (x/y/size/angle/alpha/anchor)
  - Recommended roles: Frontend Dev
- **Nine-slice Panels** — feature: F-007; asset: —
  - Depends on: Asset Manager (images/atlases) + drag to canvas
  - Recommended roles: Frontend Dev


## M3 — Export / Import / Themes
- **Custom HUD JSON schema + exporter (placeholders)** — feature: F-009; asset: —
  - Depends on: WebFont + BitmapText support, Asset Manager (images/atlases) + drag to canvas, Nine-slice Panels
  - Recommended roles: Backend Dev, Frontend Dev
- **Importer + minor schema migrations** — feature: F-010; asset: —
  - Depends on: Custom HUD JSON schema + exporter (placeholders)
  - Recommended roles: Backend Dev
- **Color & Theme system** — feature: F-008; asset: —
  - Depends on: Properties panel (x/y/size/angle/alpha/anchor)
  - Recommended roles: Frontend Dev, Designer


## M4 — Runtime & Preview
- **Runtime Loader for Phaser 3.90 (loadHUD)** — feature: F-011; asset: —
  - Depends on: Importer + minor schema migrations
  - Recommended roles: Backend Dev
- **In-editor Live Preview & Validator** — feature: F-012; asset: —
  - Depends on: Runtime Loader for Phaser 3.90 (loadHUD), Color & Theme system
  - Recommended roles: Frontend Dev, QA


## M5 — Polish, Templates & Docs
- **Starter HUD templates (Score, Health, MiniMap frame)** — feature: F-009; asset: —
  - Depends on: In-editor Live Preview & Validator
  - Recommended roles: Designer, Frontend Dev
- **Docs: Editor User Guide + Runtime API** — feature: F-011; asset: —
  - Depends on: Runtime Loader for Phaser 3.90 (loadHUD)
  - Recommended roles: Tech Writer, Frontend Dev, Backend Dev

