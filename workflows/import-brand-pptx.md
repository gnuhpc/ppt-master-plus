---
description: Import an explicitly user-provided PPTX as a reusable Brand plus a confirmed native Page Kit, without creating a presentation project.
---

# Import Brand PPTX

This workflow begins by importing a `.pptx` file explicitly provided by the
user. Every such import is classified as a **Brand**, not a Layout or Pack: it
supplies identity and completes as a standalone template-asset operation. It
does not create a presentation project, import content, open the Generate Confirm UI,
or generate a deck. Every imported Brand links to a confirmed **Brand Page Kit
Layout** from the same authorized PPTX; it contains only selected reusable
native page prototypes. It never starts
from a bare template name, a style description, or an internal asset. The
input PPTX remains user-owned and is read only; intake runs in temporary storage.
The result is a shared Brand package linked to a confirmed Page Kit; it never registers the
source PPTX itself. The user may explicitly request a companion
`--register-icon-layout <id>`, `--register-chart-layout <id>`, or
`--register-page-kit-layout <id>`: these are companion Layouts, not a
registration of the whole source deck.

The source is classified directly as a reusable **Brand**. Template-native formatting is never style authority for charts,
tables, or sample content: only explicitly approved Page Kit prototypes may
carry native structure into a new deck.

The **Brand Import Web is mandatory for every import**. It shows the rendered
source slides and requires the user to confirm extracted color and typography
rules plus cover, TOC, section transition, content Master/Layout, and closing
pages. Unselected slides never enter the
Page Kit. A content selection identifies its linked
Master/Layout, not its slide examples: registration deletes every slide-local
object except the large-title text frame. It preserves the Master/Layout layer's
background images, text and placeholders, plus the empty large-title frame's
geometry and typography; the source title wording is cleared.

Template examples, instructions, placeholder copy, and guide text are never final
content. The public import yields `brand_page_kit` adaptation. In later Generate,
the confirmed Page Kit is recommended by default: its named pages use native
round-trip cloning and slot replacement; unmatched pages remain newly generated.
It never clones arbitrary source slides.

The template is not the data or page-layout authority for charts, tables,
infographics, process diagrams, frameworks, or other visuals. By default, use
the Skill's built-in catalogs (`templates/charts/charts_index.json` and
`templates/tables/tables_index.json`). If the user explicitly registers and
selects a chart-grammar Layout, it may guide chart type, series palette, visual
hierarchy, legend, axes, gridlines, and labels; use only current content for
the values.
Never copy exemplar data, source-page geometry, or sample text.

## Import the Brand

1. Require the exact user-provided `.pptx` path and a unique Brand id. Reject `.potx`,
   directories, internal template names, and implicit catalog selection.
2. Run the standalone importer. It reads the supplied PPTX without changing it,
performs intake and preview rendering in an automatically deleted temporary directory,
opens the mandatory Brand Import Web, then materializes identity assets and the
confirmed Page Kit before refreshing both indexes:

```bash
python3 skills/ppt-master-plus/scripts/import_brand.py <template.pptx> --brand-id <brand_id>
```

3. Read the emitted Brand package, linked Page Kit manifest, and both index entries before
reporting completion. The package contains `design_spec.md`, identity assets, and only
Web-confirmed page shells; it contains no original PPTX, unconfirmed page roster,
slide-local body geometry, sample copy, chart/table styling, or presentation project.

The Web writes `analysis/brand_import_selection.json`. Only confirmed rows are registered
as the linked Page Kit. The shared Brand receives identity tokens and assets referenced by
the source Master/Layout; special pages retain only confirmed native prototypes. The
optional icon/chart Layouts only
retain their respective visual grammar; the chart Layout excludes source data.
The Page Kit retains only Web-confirmed native prototypes, explicit editable
slots and locked-object/capacity rules for cover/TOC/section/closing pages. A
content row has no inherited slide-local body objects: it is a sanitized
Master/Layout shell with one empty editable large-title slot, on which new
slide-local content may be created. This deletes all source body text, images,
non-Master background pictures, charts, legends, tables, diagrams, icons,
shapes and example content.
It excludes guide pages, every unselected page, and all slide-local content from
selected body pages.

3. Read `template_manifest.json`, `template_design_tokens.json`,
   `template_archetypes.json`, `template_assets.json`, and template preview index.
   Guide/specification pages stay diagnostic only. The classifier supplies Web
   candidates but never promotes them autonomously. The confirmed selection may
   admit only cover, TOC, section transition, content Master/Layout, or closing
   roles; it records source slide and clone strategy for every row. Content rows
   are sanitized to Master/Layout plus empty-large-title shells during registration.
   Placeholder status alone is never semantic authority: ordinary text boxes,
   shapes, images, graphics, and groups are analyzed to extract identity facts,
   but only the confirmed content page's large-title text frame survives inside
   a selected content shell, with its text cleared.
   Chart, table, infographic, and diagram objects do not become page layouts.
   Their sample data is always excluded. A user-requested chart-grammar Layout
   may retain only chart type and display conventions; an icon-grammar Layout
   may retain only icon treatment.

Fact priority is explicit guide rules, resolved exemplar formatting,
Master/Theme inheritance, shape-name/note hints, then geometric/repetition
inference. Conflicts and confidence live in the four artifacts. Unknown and
low-confidence objects stay locked. Legal or license wording becomes a usage
constraint, not a verified legal claim.

## Later: use the registered Brand in Generate PPTX

The import has already completed. The following rules apply only after a separate
request to generate a presentation supplies both new content and the explicit
`templates/brands/<brand_id>/` path. That later request, not Brand import, creates
the presentation project and enters the normal Generate confirmation flow.

Strategist writes a complete content-backed page plan freely under the imported
Brand identity. Preserve the existing two-layer confirmation.
The Confirm UI shows canvas, colors, fonts, Logo, and Icon as “来自模板并锁定”.
Audience, core message, page plan, production mode, and transitions remain
confirmable. Unlock one design field only on an explicit user request.

After confirmation, publish the ordinary Generate roster and `spec_lock.md`.
When a selected Brand has a Page Kit, Confirm UI also offers `Use page kit`
versus `Identity only`; it lists the approved roles and recommends `Use page kit`
by default. A user may still explicitly choose `Identity only` for a fully free
deck. A Page Kit locks a special-page prototype's
   background, recurring logo, decorations, crop, native master/layout and
   z-order. For a content row it locks the selected Master/Layout, retains the
   empty large-title slot, and creates new body objects above it; no source-slide
   illustration or example object exists to reuse. The page plan decides which
   approved row is used for each page. It never enables guide pages or forces
   source page order.

After the final confirmation, activate a selected Page Kit before production:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py activate-brand-page-kit <project>
```

This verifies the Brand-index link and Page Kit manifest, copies the authorized
prototype package read-only into the project, writes `native_page_kit_plan.json`,
and switches `route_context.json` to `engine: edit_native`,
`profile: template_fill`, and `modules: [page_plan, content_edit]`. A confirmed
`Identity only` choice must not activate the native Page Kit branch.

For each confirmed Page Kit page, Strategist writes
`page_kit_execution_plan.json`. Every row names a `role` plus the exact
approved `source_slide`; it may carry `page_id` and `visual_type` for audit.
The plan is the authority for native prototype selection. Reusing an approved
prototype while another prototype of the same role remains unused requires
`allow_repeat: true` and a `repeat_rationale`; this makes repeated layouts an
explicit decision rather than a silent fallback.

```json
{
  "schema": "ppt-master-plus.native-page-kit-page-plan.v1",
  "pages": [
    { "page_id": "P01", "role": "cover", "source_slide": 1 },
    { "page_id": "P04", "role": "content", "source_slide": 22,
      "visual_type": "built_in_chart_over_master" },
    { "page_id": "P05", "role": "content", "source_slide": 22,
      "visual_type": "free_content_over_master", "allow_repeat": true,
      "repeat_rationale": "same confirmed body Master/Layout" }
  ]
}
```

Execute this plan and then pass the emitted slot roster to `content_edit`:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py execute-brand-page-kit <project> \
  --page-plan <project>/page_kit_execution_plan.json \
  --output <project>/output/native_seed.pptx
```

The command deep-clones the selected native slides and their private OOXML
dependencies. It rejects an unapproved role/source-slide pair, ambiguous
repeated `--role content` calls, silent prototype reuse, and existing output
files. On special pages, `content_edit` may write only emitted editable slots;
on a sanitized content shell it may replace the large-title slot and add new
slide-local body content above the locked Master/Layout, but may not alter the
Master/Layout objects. The legacy
`--role` form remains only for non-repeated roles or roles with one approved
prototype.

## Later: resources and new-page production

Acquire resources for the new content and use imported Brand assets only where
they support the planned page. For an approved special-page row, clone its
selected native prototype with round-trip editing, preserve locked objects, and
replace only declared slots. For an approved content row, clone the sanitized
Master/Layout shell, replace its large title, and build new body content above
the locked Master/Layout; source-slide examples are absent. For an
unplanned/unsupported role, generate a new page under
`spec_lock.md`; do not copy a source slide, Master/Layout, group, z-order, crop,
mask, filter, or object geometry from the imported PPTX.

For every visualization, query the built-in chart/table catalogs, select a
semantic match, and construct its data from `content_sources`. When a
user-selected chart-grammar Layout exists, apply its compatible series palette,
legend, axes, gridline, and label conventions to that built-in choice; it never supplies
values, categories, source-page geometry, or sample wording.

Overflow handling follows Generate rules: shorten content, choose a more suitable
approved Page Kit prototype, clone the same approved content prototype and split
the content, then stop for user direction if needed. Never silently free-redesign
a selected Page Kit page or weaken the imported Brand identity.

After the final generation Confirm UI result (and any required image-acquisition
step), start Live Preview with `svg_editor/server.py <project> --live --daemon`
and wait for its reachable URL **before** creating the first generated page/SVG.
If startup fails, do not author slides; restore the preview first. Use Live
Preview for each generated page. `gated` waits after each page; `continuous`
proceeds. Generate-route SVG drawing constraints apply because this is a
new-page generation branch.

## Later: validate and export

Run `svg_quality_checker.py`, export with `svg_to_pptx.py`, then run OOXML/
postflight and rendered visual checks. Record it:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py set-output <project> <output.pptx>
```

Never overwrite the imported template or the user-supplied original.
