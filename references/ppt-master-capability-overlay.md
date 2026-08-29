# PPT Master Unified Capability Core

PPT Master Plus uses one integrated PPT Master 5.1 script engine for export,
intake, quality, project management, native round-trip editing, and template filling.
There is no legacy/core dispatcher. The Plus Step 1–7 pipeline, Eight
Confirmations, `gated` / `continuous` behavior, Confirm UI, and Live Preview
remain authoritative.

## Activation boundary

Load only the rows needed by the current deck. Missing optional fields mean the
same engine's flat/default behavior remains active.

| Trigger | Additional authority | Engine behavior |
|---|---|---|
| Editable native charts or tables | [`ppt-master-core/native-data-interface.md`](ppt-master-core/native-data-interface.md), then the matching chart/table Executor reference | Add explicit `data-pptx-replace-with` metadata; the unified exporter emits a native object only when the marker or flag exists |
| Editable formulas | [`ppt-master-core/native-formula.md`](ppt-master-core/native-formula.md) | Use native formula markers only on explicit user request; otherwise the same engine emits ordinary editable text/shapes |
| Hyperlinks | [`ppt-master-core/native-hyperlinks.md`](ppt-master-core/native-hyperlinks.md) | Preserve explicit shape/text hyperlinks through semantic markers |
| Native preset shapes or Boolean shapes | [`ppt-master-core/native-shape-authoring.md`](ppt-master-core/native-shape-authoring.md), [`ppt-master-core/preset-shape-vocabulary.md`](ppt-master-core/preset-shape-vocabulary.md) | Use the vendored stdout-only helpers; they never write a slide |
| Advanced SVG effects | [`ppt-master-core/svg-effects.md`](ppt-master-core/svg-effects.md) | Use only registered effects and their semantic markers |
| Structured Master/Layout/placeholder output | [`ppt-master-core/pptx-structure-interface.md`](ppt-master-core/pptx-structure-interface.md), [`ppt-master-core/semantic-svg.md`](ppt-master-core/semantic-svg.md), [`ppt-master-core/topology-assembly.md`](ppt-master-core/topology-assembly.md) | Allowed only for an installed structured Layout/Deck workspace; free design and existing projects stay `flat` |
| Layered PPTX import or controlled round-trip | [`Edit Native PPTX`](../workflows/edit-native-pptx.md) plus the namespaced native references | Use `pptx_to_svg.py --roundtrip`; never treat it as a redesign path |
| Advanced transition, animation, sound, or video | [`ppt-master-core/animations.md`](ppt-master-core/animations.md), [`ppt-master-core/video-design.md`](ppt-master-core/video-design.md) | Explicit request only; the Plus defaults remain transition `none`, animation `none`, and no narration/video |
| Artifact recovery or delivery diagnostics | [`ppt-master-core/artifact-ownership.md`](ppt-master-core/artifact-ownership.md), [`ppt-master-core/workflows/governance/failure-recovery.md`](ppt-master-core/workflows/governance/failure-recovery.md) | Use ownership and recovery rules without importing the upstream route or page cadence |

## Public command contract

The public scripts remain under `${SKILL_DIR}/scripts/` and always execute the
same integrated engine. `--master-core` is not a public argument.

- Standard export is flat unless the project declares `pptx_structure` or the
  caller supplies `--pptx-structure`.
- Native Charts/Tables require explicit markers plus
  `--native-charts-and-tables`; formulas and hyperlinks use their own semantic
  contracts.
- `pptx_to_svg.py --strict|--roundtrip`, `project_manager.py page-context`, and
  extended quality reports are normal commands of the same engine.
- Public helper entrypoints live under `${SKILL_DIR}/scripts/`; notable
  commands are
  `preset_shape_svg.py`, `shape_boolean_svg.py`, `pptx_delivery_check.py`,
  `pptx_opc_validation.py`, `sound_sync.py`, `video_motion_plan.py`,
  `video_sound_mix.py`, `video_subtitles.py`, `visualization_recall.py`, and the
unified `source_to_md.py`. Their implementation is packaged under
  `${SKILL_DIR}/vendor/ppt-master/scripts/`.

`--quick-generate` is rejected at the Plus public boundary. Do not invoke the
vendored Confirm UI, SVG editor, router, or self-updater; none is packaged into
the overlay.

## Optional project fields

These fields may be added to Design Spec/Spec Lock only when active. Their
absence keeps the unified engine's flat/default behavior.

```yaml
pptx_structure:
  mode: flat | structured
native_charts: false
native_tables: false
native_formulas: false
native_hyperlinks: false
conversion_trace: false
```

- `structured` requires complete Master/Layout/page assignment metadata from a
  validated structured workspace.
- Native charts/tables require both an editable fallback group and explicit
  replacement metadata; enabling the global field alone never upgrades shapes.
- Native formulas require explicit user intent because they change the existing
  Plus formula realization policy.
- Hyperlink preservation may be enabled automatically when it comes from source
  facts or explicit authoring.

## Template/resource overlay

The top-level Plus indexes are the only catalogs. They are a union in which
existing Plus entries win collisions. Style workspaces use
`templates/styles/<id>/templates/design_spec.md`; tables and sounds use their
own indexes. An explicit current workspace may contain
`templates/design_spec.md` instead of the legacy root-level `design_spec.md`.

Never overwrite a Plus template to make it satisfy a newer contract. Validate
the selected workspace and either use it as-is under its declared mode or stop
and ask for a separately recreated structured workspace.
