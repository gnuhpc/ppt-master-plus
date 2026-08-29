---
description: Deterministic routing among the three public ppt-master-plus lifecycles.
---

# Routing

Select exactly one public route. Profiles, stages, adapters, modules, and internal
template-authoring tools are never presented as peer workflows.

| User intent | Route | Engine | Profile |
|---|---|---|---|
| Create or redesign visible pages from content | Generate PPTX | `svg_generate` | `faithful_beautify`, `image_to_pptx`, or null |
| Preserve and locally modify the supplied deck itself | Edit Native PPTX | `edit_native` | null |
| Explicitly import a user-provided `.pptx` file as the template for a new deck | Create PPTX from Template | `edit_native` | `template_fill` |

When an existing PPTX could be either the deliverable or a design skeleton, ask
only: “这份 PPTX 是要保留现有内容继续修改，还是仅作为模板，用新内容生成一份新的 PPTX？”

The execution context is:

```yaml
route: generate_pptx | edit_native_pptx | create_pptx_from_template
engine: svg_generate | edit_native
profile: faithful_beautify | image_to_pptx | template_fill | null
adaptation: native_adaptive
visualization_style_source: skill_builtin | null
template_origin: user_provided_pptx | null
modules: [page_plan, content_edit, notes, narration, transitions, animations]
```

The template route always resolves to:

```yaml
route: create_pptx_from_template
engine: edit_native
profile: template_fill
adaptation: native_adaptive
visualization_style_source: skill_builtin
template_origin: user_provided_pptx
template_import_required: true
modules: [page_plan, content_edit]
```

This route requires an explicit user-supplied `.pptx` file. A bare template
name, style description, internal Brand/Style/Layout/Deck directory, `.potx`,
or other file type does not trigger it. Import the PPTX as an immutable project
copy before analysis or planning. If the user has not supplied the file, request
the `.pptx` instead of selecting an internal template on their behalf.

For this route, the template supplies the canvas, layout topology, locked deck
tokens, fixed assets, and visualization-slot geometry. It never supplies chart,
table, infographic, or diagram styling. Select those styles from the built-in
Skill catalogs, then adapt their colors and typography to the locked template
tokens and fit them within the template slot.

Brand, Style, Layout, and Deck authoring are internal maintenance tools under
`workflows/internal/template-authoring/`; they are not public routes.
