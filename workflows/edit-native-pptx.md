---
description: Preserve an existing deck and edit only selected native pages or enhancement modules.
---

# Edit Native PPTX

Use this route when the supplied PPTX is the deck being modified. It preserves
Master/Layout topology, relationships, groups, z-order, media, notes, motion,
native charts, and tables through the vendored v5.1 round-trip engine.

Modules are independently enabled:

| Module | Purpose |
|---|---|
| `page_plan` | Select, delete, reorder, or repeat source pages |
| `content_edit` | Replace text, images, native chart/table data, or selected objects |
| `notes` | Add or modify speaker notes |
| `narration` | Generate and embed narration |
| `transitions` | Preserve or explicitly change transitions/auto-advance |
| `animations` | Preserve or explicitly change object motion |
| `visible_content_locked` | Permit enhancements while forbidding visible-page edits |

Import directly into a dedicated workspace:

```bash
python3 skills/ppt-master-plus/scripts/pptx_to_svg.py source.pptx \
  -o projects/<slug> --inheritance-mode both --roundtrip
python3 skills/ppt-master-plus/scripts/project_manager.py configure-native projects/<slug> \
  --module page_plan --module content_edit
```

Read `authoring-svg-flat/authoring_summary.json` first. Create `page_plan.json`
only for a changed roster. Present the output roster, content mapping, enabled
modules, and known refusals, then wait for confirmation before editing.

After confirmation, publish a changed roster with the unified helper. A repeated
source slide uses `N:new-name.svg`; the helper safely clones its authoring SVG:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py native-plan projects/<slug> \
  --page 1 --page 7:kpi_first.svg --page 7:kpi_second.svg --page 12
```

Edit only planned pages in `authoring-svg-flat/`. Keep `data-pptx-*` identity on
unchanged objects. Replace images inside their existing frames. Edit the inline
native authority for charts/tables and export with `--native-charts-and-tables`.
Low-confidence or unsupported source proxies are atomic and locked.

For Live Preview:

```bash
python3 skills/ppt-master-plus/scripts/native_preview.py prepare projects/<slug>
python3 skills/ppt-master-plus/scripts/native_preview.py start projects/<slug>
```

The adapter exposes `authoring-svg-flat/` to the frozen Plus preview without
changing its implementation. Validate and export:

```bash
python3 skills/ppt-master-plus/scripts/svg_authoring_view.py \
  projects/<slug>/authoring-svg-flat --refresh-summary
python3 skills/ppt-master-plus/scripts/svg_quality_checker.py projects/<slug> --roundtrip
python3 skills/ppt-master-plus/scripts/svg_to_pptx.py projects/<slug> --roundtrip
```

The output is always a new PPTX under `exports/`; the source is never modified.
