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
| Explicitly import a user-provided `.pptx` file as a reusable brand asset | Import Brand PPTX | none | none |

When an existing PPTX could be either the deliverable or a design skeleton, ask
only: “这份 PPTX 是要保留现有内容继续修改，还是仅作为模板，用新内容生成一份新的 PPTX？”

The execution context is:

```yaml
route: generate_pptx | edit_native_pptx | import_brand_pptx
engine: svg_generate | edit_native | null
profile: faithful_beautify | image_to_pptx | null
adaptation: native_adaptive | brand_identity | brand_page_kit
visualization_style_source: skill_builtin | registered_layout | null
template_origin: user_provided_pptx | null
template_kind: brand | null
modules: [page_plan, content_edit, notes, narration, transitions, animations]
```

The standalone Brand-import route always resolves to:

```yaml
route: import_brand_pptx
engine: null
profile: null
adaptation: brand_page_kit
visualization_style_source: null
template_origin: user_provided_pptx
template_kind: brand
template_reuse: page_kit
modules: [page_plan, content_edit]
```

This route requires an explicit user-supplied `.pptx` file. A bare template
name, style description, internal Brand/Style/Layout/Pack directory, `.potx`,
or other file type does not trigger it. Analyze the PPTX in isolated temporary
storage, then write only the registered Brand package. If the user has not supplied the file, request
the `.pptx` instead of selecting an internal template on their behalf.

Every user-provided PPTX import is classified as a **Brand**, never as a Layout
or Pack. It supplies brand identity tokens and reusable brand assets: canvas,
palette, typography, logos, icons, background motifs, and visual tone. On an
explicit Page Kit registration, it links to a companion Layout containing only
the cover, TOC, section and closing prototypes confirmed in Brand Import Web,
plus confirmed content Master/Layout shells. A content shell contains no
slide-local examples: registration strips every object on that source slide and
retains only the linked Master/Layout background images, text and placeholders.
Other pages are planned and generated freely under the locked identity.

The supplied PPTX is read-only. The import creates a temporary preview workspace and
requires the Brand Import Web to confirm cover, TOC, section, content and closing roles.
It then materializes identity facts under `templates/brands/<id>/` and a linked Page Kit
under `templates/layouts/`; it never creates a presentation project. A later Generate run
can select the registered Brand by an explicit internal Brand path.

Charts, tables, infographics, and diagrams default to the built-in Skill
catalogs. If the user explicitly registers and selects a companion
chart-grammar Layout, it may supply chart type, series palette, axes,
gridlines, legend, and label conventions; content data still comes only from
the current sources.
Never reuse source-page geometry, sample copy, or exemplar data. An
icon-grammar Layout can likewise guide icon treatment without copying branded
example illustrations.

Brand, Style, Layout, and Pack authoring are internal maintenance tools under
`workflows/internal/template-authoring/`; they are not public routes.
