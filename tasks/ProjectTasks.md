# ProjectTasks

> Canonical task list. Agents may only modify their own `owner/status/notes` fields.

- TASK: Setup Phaser 3.90 project & stage
  owner: Gemini CLI
  status: IN_PROGRESS
  notes: feature: F-001 — Editor Canvas Core; roles: Frontend Dev

- TASK: Selection + drag move + snap-to-grid
  owner: OPEN
  status: TODO
  notes: feature: F-002 — Drag, Drop, Resize, Rotate; depends_on: Setup Phaser 3.90 project & stage; roles: Frontend Dev

- TASK: Layers panel + grouping via Containers
  owner: OPEN
  status: TODO
  notes: feature: F-003 — Layers & Grouping; depends_on: Selection + drag move + snap-to-grid; roles: Frontend Dev

- TASK: Properties panel (x/y/size/angle/alpha/anchor)
  owner: OPEN
  status: TODO
  notes: feature: F-004 — Properties Panel; depends_on: Layers panel + grouping via Containers; roles: Frontend Dev

<!-- Milestone M2 — Assets, Text & Panels -->

- TASK: Asset Manager (images/atlases) + drag to canvas
  owner: OPEN
  status: TODO
  notes: feature: F-006 — Image & Atlas Support; depends_on: Properties panel (x/y/size/angle/alpha/anchor); roles: Frontend Dev

- TASK: WebFont + BitmapText support
  owner: OPEN
  status: TODO
  notes: feature: F-005 — Text Support (WebFont + BitmapText); depends_on: Properties panel (x/y/size/angle/alpha/anchor); roles: Frontend Dev

- TASK: Nine-slice Panels
  owner: OPEN
  status: TODO
  notes: feature: F-007 — Panels (Nine-slice); depends_on: Asset Manager (images/atlases) + drag to canvas; roles: Frontend Dev

<!-- Milestone M3 — Export / Import / Themes -->

- TASK: Custom HUD JSON schema + exporter (placeholders)
  owner: OPEN
  status: TODO
  notes: feature: F-009 — Custom HUD Schema & Exporter; depends_on: WebFont + BitmapText support, Asset Manager (images/atlases) + drag to canvas, Nine-slice Panels; roles: Backend Dev, Frontend Dev

- TASK: Importer + minor schema migrations
  owner: OPEN
  status: TODO
  notes: feature: F-010 — Importer & Versioning; depends_on: Custom HUD JSON schema + exporter (placeholders); roles: Backend Dev

- TASK: Color & Theme system
  owner: OPEN
  status: TODO
  notes: feature: F-008 — Color & Theme; depends_on: Properties panel (x/y/size/angle/alpha/anchor); roles: Frontend Dev, Designer

<!-- Milestone M4 — Runtime & Preview -->

- TASK: Runtime Loader for Phaser 3.90 (loadHUD)
  owner: OPEN
  status: TODO
  notes: feature: F-011 — Runtime Loader for Phaser 3.90; depends_on: Importer + minor schema migrations; roles: Backend Dev

- TASK: In-editor Live Preview & Validator
  owner: OPEN
  status: TODO
  notes: feature: F-012 — Preview & Validation; depends_on: Runtime Loader for Phaser 3.90 (loadHUD), Color & Theme system; roles: Frontend Dev, QA

<!-- Milestone M5 — Polish, Templates & Docs -->

- TASK: Starter HUD templates (Score, Health, MiniMap frame)
  owner: OPEN
  status: TODO
  notes: feature: F-009 — Custom HUD Schema & Exporter; depends_on: In-editor Live Preview & Validator; roles: Designer, Frontend Dev

- TASK: Docs: Editor User Guide + Runtime API
  owner: OPEN
  status: TODO
  notes: feature: F-011 — Runtime Loader for Phaser 3.90; depends_on: Runtime Loader for Phaser 3.90 (loadHUD); roles: Tech Writer, Frontend Dev, Backend Dev

