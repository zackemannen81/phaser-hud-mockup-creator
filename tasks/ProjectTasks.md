# ProjectTasks

> Canonical task list. Agents may only modify their own `owner/status/notes` fields.

<!-- Milestone M1 — Editor Core MVP -->

- TASK: Setup Phaser 3.90 project & stage\n  owner: Gemini CLI\n  feature/gemini_cli/setup-phaser-3-90-project-stage\n  status: REVIEW\n  notes: feature: F-001 — Editor Canvas Core; roles: Frontend Dev
PR #1 opened\n

- TASK: Selection + drag move + snap-to-grid\n  owner: Gemini CLI\n  status: REVIEW\n  notes: feature: F-002 — Drag, Drop, Resize, Rotate; depends_on: Setup Phaser 3.90 project & stage; roles: Frontend Dev
Auto-picked
PR #2 opened\n

- TASK: Layers panel + grouping via Containers\n  owner: Gemini CLI\n  status: REVIEW\n  notes: feature: F-003 — Layers & Grouping; depends_on: Selection + drag move + snap-to-grid; roles: Frontend Dev
Auto-picked\nPR #3 opened\n

- TASK: Properties panel (x/y/size/angle/alpha/anchor)\n  owner: OPEN\n  status: TODO\n  notes: feature: F-004 — Properties Panel; depends_on: Layers panel + grouping via Containers; roles: Frontend Dev\n

<!-- Milestone M2 — Assets, Text & Panels -->

- TASK: Asset Manager (images/atlases) + drag to canvas\n  owner: OPEN\n  status: TODO\n  notes: feature: F-006 — Image & Atlas Support; depends_on: Properties panel (x/y/size/angle/alpha/anchor); roles: Frontend Dev\n

- TASK: WebFont + BitmapText support\n  owner: OPEN\n  status: TODO\n  notes: feature: F-005 — Text Support (WebFont + BitmapText); depends_on: Properties panel (x/y/size/angle/alpha/anchor); roles: Frontend Dev\n

- TASK: Nine-slice Panels\n  owner: OPEN\n  status: TODO\n  notes: feature: F-007 — Panels (Nine-slice); depends_on: Asset Manager (images/atlases) + drag to canvas; roles: Frontend Dev\n

<!-- Milestone M3 — Export / Import / Themes -->

- TASK: Custom HUD JSON schema + exporter (placeholders)\n  owner: OPEN\n  status: TODO\n  notes: feature: F-009 — Custom HUD Schema & Exporter; depends_on: WebFont + BitmapText support, Asset Manager (images/atlases) + drag to canvas, Nine-slice Panels; roles: Backend Dev, Frontend Dev\n

- TASK: Importer + minor schema migrations\n  owner: OPEN\n  status: TODO\n  notes: feature: F-010 — Importer & Versioning; depends_on: Custom HUD JSON schema + exporter (placeholders); roles: Backend Dev\n

- TASK: Color & Theme system\n  owner: OPEN\n  status: TODO\n  notes: feature: F-008 — Color & Theme; depends_on: Properties panel (x/y/size/angle/alpha/anchor); roles: Frontend Dev, Designer\n

<!-- Milestone M4 — Runtime & Preview -->

- TASK: Runtime Loader for Phaser 3.90 (loadHUD)\n  owner: OPEN\n  status: TODO\n  notes: feature: F-011 — Runtime Loader for Phaser 3.90; depends_on: Importer + minor schema migrations; roles: Backend Dev\n

- TASK: In-editor Live Preview & Validator\n  owner: OPEN\n  status: TODO\n  notes: feature: F-012 — Preview & Validation; depends_on: Runtime Loader for Phaser 3.90 (loadHUD), Color & Theme system; roles: Frontend Dev, QA\n

<!-- Milestone M5 — Polish, Templates & Docs -->

- TASK: Starter HUD templates (Score, Health, MiniMap frame)\n  owner: OPEN\n  status: TODO\n  notes: feature: F-009 — Custom HUD Schema & Exporter; depends_on: In-editor Live Preview & Validator; roles: Designer, Frontend Dev\n

- TASK: Docs: Editor User Guide + Runtime API\n  owner: OPEN\n  status: TODO\n  notes: feature: F-011 — Runtime Loader for Phaser 3.90; depends_on: Runtime Loader for Phaser 3.90 (loadHUD); roles: Tech Writer, Frontend Dev, Backend Dev\n