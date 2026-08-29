---
description: Import an explicitly user-provided PPTX file as a read-only template, then generate a new deck from separate content.
---

# Create PPTX from Template

This workflow begins by importing a `.pptx` file explicitly provided by the
user. The imported PPTX supplies design and topology; `content_sources` supply
information. It never starts from a bare template name, a style description, or
an internal Brand/Style/Layout/Deck asset. The imported PPTX remains a project-
local, read-only source and is never registered into the Skill template library.

Template examples, instructions, placeholder copy, and guide text are never final
content. The public route is independent, while execution uses `edit_native` with
`template_fill`, `native_adaptive`, `page_plan`, and `content_edit`.

The template is not the style authority for charts, tables, infographics,
process diagrams, frameworks, or other data visuals. Those visualizations must
use the Skill's built-in catalogs (`templates/charts/charts_index.json` and
`templates/tables/tables_index.json`). The template contributes only their slot
geometry, capacity, z-order anchor, and locked deck tokens. Apply the template's
locked palette and typography to the selected built-in visualization; never copy
the exemplar's series colors, table skin, legend treatment, axes, gridlines, or
diagram vocabulary.

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
python3 skills/ppt-master-plus/scripts/pptx_to_svg.py <project>/template/source.pptx \
  -o <project> --inheritance-mode both --roundtrip
```

3. Read `template_manifest.json`, `template_design_tokens.json`,
   `template_archetypes.json`, `template_assets.json`, and template preview index.
   Guide pages contribute rules/assets only; reusable exemplar pages become
   archetypes. Placeholder status alone is never semantic authority: ordinary
   text boxes, shapes, images, graphics, and groups are classified too.
   Chart, table, infographic, and diagram objects contribute slot evidence only;
   their sample styling and sample data are excluded from the reusable design.

Fact priority is explicit guide rules, resolved exemplar formatting,
Master/Theme inheritance, shape-name/note hints, then geometric/repetition
inference. Conflicts and confidence live in the four artifacts. Unknown and
low-confidence objects stay locked. Legal or license wording becomes a usage
constraint, not a verified legal claim.

## Step 4: plan and confirm

Strategist maps every target message to a matching archetype and writes a
complete source-backed page plan. Preserve the existing two-layer confirmation.
The Confirm UI shows canvas, colors, fonts, Logo, and Icon as “来自模板并锁定”.
Audience, core message, page plan, production mode, and transitions remain
confirmable. Unlock one design field only on an explicit user request.

After confirmation, use `project_manager.py native-plan` to publish the ordered
roster. `N:new-name.svg` clones an archetype for repeated or split pages while
keeping the source slide as its native Master/Layout skeleton.

## Step 5–6: resources and native production

Acquire resources only for editable content slots; never regenerate fixed
template assets. For each page, copy a source archetype, give every repeated page
a distinct SVG filename in `page_plan.json`, and replace native objects through
the round-trip authoring view. Keep Master/Layout, groups, relationships, z-order,
crop, masks, and filters for non-visualization template objects.

For every visualization slot, query the built-in chart/table catalogs, select a
semantic match, and construct its data from `content_sources`. Preserve the
template slot frame and z-order anchor, but replace the exemplar visual instead
of inheriting or editing its style. Native chart/table output must be rebuilt
from semantic JSON plus the selected built-in style; template-native chart or
table formatting is never style authority.

Overflow handling is fixed: shorten content; adjust size/spacing only inside
template limits; choose a larger matching archetype; duplicate and split; then
stop for user direction. Never fall back to free redesign.

Use `native_preview.py start <project>` for page-by-page rendered preview.
`gated` waits after each page; `continuous` proceeds. Generate-route SVG drawing
constraints do not apply to this native branch.

## Step 7: validate and export

Refresh the authoring summary, run `svg_quality_checker.py --roundtrip`, export
with `svg_to_pptx.py --roundtrip` (plus native chart/table and requested motion or
narration flags), then run OOXML/postflight and rendered visual checks. Record it:

```bash
python3 skills/ppt-master-plus/scripts/project_manager.py set-output <project> <output.pptx>
```

Never overwrite the imported template or the user-supplied original.
