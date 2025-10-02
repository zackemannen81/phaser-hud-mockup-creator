# Development Plan — Phaser3.90_GameHUD-MockupCreator

## Product / Service Specification (English)
**Summary:** A complete HUD Editor for Phaser 3.90 with an intuitive GUI. Drag & drop UI elements, resize/align, color & theme controls, load images and fonts, and export/import a custom JSON HUD format that uses {extern_variable} placeholders for runtime binding in Phaser games.

### Objectives
- Make HUD layouting WYSIWYG with grid, guides, and snapping.
- Support Text, BitmapText, Images, Panels (9-slice) and Groups.
- Provide a custom JSON HUD schema with {variable} tags for runtime binding.
- Ship a small Runtime Loader that builds the HUD in a Phaser 3.90 Scene.
- Offer asset and font management plus theming.


### Target Users & Needs
- **Game Developer** — needs: Fast iteration on HUD without hard-coding coordinates, Deterministic export for VCS and CI
- **UI/UX Designer** — needs: Drag-and-drop layout, alignment guides, color & typography control, Asset previews and theme switching
- **Technical Artist** — needs: Nine-slice panels and layered compositions, Custom widgets and extension points


### Features

#### F-001 — Editor Canvas Core
- Description: Phaser-driven canvas with pan/zoom, ruler/grid, snapping and selection marquee.
- Acceptance Criteria:
  - Zoom & pan the stage, toggle grid & snap
  - Select single/multiple elements and move with drag

- Dependencies: None
- Required roles: Frontend Dev

#### F-002 — Drag, Drop, Resize, Rotate
- Description: Interactive transform handles for move/resize/rotate; drop zones to add elements.
- Acceptance Criteria:
  - Drag to move; handles for resize/rotate
  - Drop palette items onto canvas to create elements

- Dependencies: F-001
- Required roles: Frontend Dev

#### F-003 — Layers & Grouping
- Description: Layer panel with z-ordering; group elements with Containers.
- Acceptance Criteria:
  - Reorder z via layer list; group/ungroup selection
  - Hide/lock layers; multi-select operations

- Dependencies: F-001
- Required roles: Frontend Dev

#### F-004 — Properties Panel
- Description: Edit x/y, width/height, angle, alpha, origin/anchor, visibility, interactivity.
- Acceptance Criteria:
  - Two-way binding between selection and property fields
  - Numeric nudge via keyboard; reset to defaults

- Dependencies: F-002, F-003
- Required roles: Frontend Dev

#### F-005 — Text Support (WebFont + BitmapText)
- Description: Create Text/BitmapText nodes; manage fonts (web fonts, bitmap fonts).
- Acceptance Criteria:
  - Load and apply web fonts to Text
  - Load bitmap font (png + xml/json) and add BitmapText

- Dependencies: F-004
- Required roles: Frontend Dev

#### F-006 — Image & Atlas Support
- Description: Load images/atlases into an Asset Manager; drag to canvas as Image/Sprite.
- Acceptance Criteria:
  - Import PNG/JPG; show thumbnails; place on canvas
  - Replace source keeps transforms/styles

- Dependencies: F-004
- Required roles: Frontend Dev

#### F-007 — Panels (Nine-slice)
- Description: Resizable panels using 9-slice for crisp corners.
- Acceptance Criteria:
  - Create panel from texture; resize preserves corners
  - Toggle stretch modes; set padding

- Dependencies: F-006
- Required roles: Frontend Dev

#### F-008 — Color & Theme
- Description: Color picker for fill/stroke/shadow; save named themes and apply.
- Acceptance Criteria:
  - Change colors live; switch theme updates all bound nodes
  - Export/import themes with the project

- Dependencies: F-004
- Required roles: Frontend Dev, Designer

#### F-009 — Custom HUD Schema & Exporter
- Description: Export to JSON with element tree, transforms, styles, and {variable} placeholders.
- Acceptance Criteria:
  - Export JSON file with version & schema
  - Placeholders like {player_health} preserved in text/props

- Dependencies: F-004, F-005, F-006, F-007, F-008
- Required roles: Backend Dev, Frontend Dev

#### F-010 — Importer & Versioning
- Description: Load project JSON, migrate minor schema versions.
- Acceptance Criteria:
  - Recreate scene from JSON; warn on missing assets
  - Version field handled; non-breaking migrations

- Dependencies: F-009
- Required roles: Backend Dev

#### F-011 — Runtime Loader for Phaser 3.90
- Description: Small JS module that builds HUD from exported JSON at runtime and binds {variables}.
- Acceptance Criteria:
  - API: loadHUD(scene, hudJson, bindings)
  - Supports Text/BitmapText/Image/Nine-slice/Containers

- Dependencies: F-009, F-010
- Required roles: Backend Dev

#### F-012 — Preview & Validation
- Description: Live preview inside the Editor; validate missing fonts/assets/placeholders.
- Acceptance Criteria:
  - Preview uses same rendering path as runtime
  - Validation panel lists issues with links to fix

- Dependencies: F-005, F-006, F-007, F-011
- Required roles: Frontend Dev, QA


## Assets & Non-code Resources

### Media
- A-ICON-512 — image — App icon 512x512 PNG (Owner role: Designer)
- A-UI-PACK — image — Sample UI sprites (buttons, frames) for demos (Owner role: Designer)



## Infrastructure
- Hosting: Static SPA (Vite) — Runs in browser; optional Electron wrapper later.
- Backend needed: No

- Database needed: No
