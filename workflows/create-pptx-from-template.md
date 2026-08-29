---
description: Import an explicitly user-provided PPTX file as a read-only Brand reference, then generate a new deck from separate content.
---

# Create PPTX from Template

This workflow begins by importing a `.pptx` file explicitly provided by the
user. Every such import is classified as a project-local **Brand**, not a Deck:
it supplies identity while `content_sources` supply information. It never starts
from a bare template name, a style description, or an internal asset. The
imported PPTX remains a project-local, read-only source and is never registered
into the Skill template library.

Template examples, instructions, placeholder copy, and guide text are never final
content. The public route uses `svg_generate` with the `imported_brand` profile
and `brand_identity` adaptation. It does not clone, edit, or round-trip source
slides.

The template is not the style authority for charts, tables, infographics,
process diagrams, frameworks, or other data visuals. Those visualizations must
use the Skill's built-in catalogs (`templates/charts/charts_index.json` and
`templates/tables/tables_index.json`). Apply the imported Brand's locked palette
and typography to the selected built-in visualization; never copy exemplar
series colors, table skins, legend treatment, axes, gridlines, or diagram
vocabulary.

## Step 1–3: content, project, and template facts

1. Require the exact user-provided `.pptx` path. Reject `.potx`, directories,
   internal template names, and implicit catalog selection. Normalize and read
   content sources separately; do not count the template as content.
2. Initialize a normal Plus project, import content, then use `import-template`
   to copy the user file read-only and analyze it:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py init <slug>
python3 skills/ppt-master-plus/scripts/project_manager.py import-sources <project> <content...> --copy
python3 skills/ppt-master-plus/scripts/project_manager.py import-template <project> <template.pptx>
```

3. Read `template_manifest.json`, `template_design_tokens.json`,
   `template_archetypes.json`, `template_assets.json`, and template preview index.
   The archetype artifact is diagnostic only: guide pages, example pages,
   placeholder text, and object geometry never become reusable output layouts.
   Placeholder status alone is never semantic authority: ordinary text boxes,
   shapes, images, graphics, and groups are analyzed to extract identity facts.
   Chart, table, infographic, and diagram objects contribute neither layout nor
   style; their sample styling and sample data are excluded from reuse.

Fact priority is explicit guide rules, resolved exemplar formatting,
Master/Theme inheritance, shape-name/note hints, then geometric/repetition
inference. Conflicts and confidence live in the four artifacts. Unknown and
low-confidence objects stay locked. Legal or license wording becomes a usage
constraint, not a verified legal claim.

## Step 4: plan and confirm

Strategist writes a complete content-backed page plan freely under the imported
Brand identity. Preserve the existing two-layer confirmation.
The Confirm UI shows canvas, colors, fonts, Logo, and Icon as “来自模板并锁定”.
Audience, core message, page plan, production mode, and transitions remain
confirmable. Unlock one design field only on an explicit user request.

After confirmation, publish the ordinary Generate roster and `spec_lock.md`.
The imported Brand locks identity fields only; it does not prescribe source slide
order, page types, or native Master/Layout skeletons.

## Step 5–6: resources and new-page production

Acquire resources for the new content and use imported Brand assets only where
they support the planned page. Generate each SVG page from scratch under
`spec_lock.md`; do not copy a source slide, Master/Layout, group, z-order, crop,
mask, filter, or object geometry from the imported PPTX.

For every visualization, query the built-in chart/table catalogs, select a
semantic match, and construct its data from `content_sources`. Template-native
chart or table formatting is never style authority.

Overflow handling follows Generate rules: shorten content, choose a more suitable
new-page layout, split the content, then stop for user direction if needed. Never
silently weaken the imported Brand identity.

Use Live Preview for each generated page. `gated` waits after each page;
`continuous` proceeds. Generate-route SVG drawing constraints apply because this
is a new-page generation branch.

## Step 7: validate and export

Run `svg_quality_checker.py`, export with `svg_to_pptx.py`, then run OOXML/
postflight and rendered visual checks. Record it:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py set-output <project> <output.pptx>
```

Never overwrite the imported template or the user-supplied original.
