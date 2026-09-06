---
description: Validate, resolve, and install selected Brand, Style, Layout, and Pack workspaces
---

# Apply Template Workspace

Run after Stage 1 confirms template use. Registered choices come only from the four indexes; exact unregistered workspace roots remain explicit inputs.

## 1. Resolve Pack first

Accept at most one `kind: pack`. Validate that it contains only its Design Spec, references at least two registered Brand/Style/Layout ids, and contains no Pack reference. Expand it to component roots.

Use the deterministic resolver for the receipt fragment:

```bash
python3 scripts/resolve_template_selection.py \
  --pack <pack_id> \
  [--brand <brand_id>] [--style <style_id>] [--layout <layout_id>]
```

Explicit Brand, Style, or Layout selections replace the Pack reference of the same kind. Keep unoverridden Pack references. Reject multiple Packs and any final duplicate base Kind.

Record both source and resolution:

```json
{
  "selected_pack_id": "<id-or-null>",
  "resolved": {
    "brand_id": "<id-or-null>",
    "style_id": "<id-or-null>",
    "layout_id": "<id-or-null>"
  }
}
```

## 2. Validate component ownership

| Kind | Validation | Project effect |
|---|---|---|
| Brand | Identity schema and referenced assets | Locks official identity |
| Style | Roster-free method/default schema | Seeds direction and evidence behavior |
| Layout | SVG roster, canvas, Master/Layout/slot contract | Supplies reusable structure |
| Pack | Reference-only schema | Supplies provenance, never design values |

A raw PPTX is not a workspace; public import creates Brand. Layout is the only structural owner. Style and Pack never activate structured output.

## 3. Atomic installation

Precompute every source/destination mapping and reject collisions before writing. Install component specs as `templates/design_spec.<kind>.<id>.md`; install the Pack spec as `templates/design_spec.pack.<id>.md` for provenance. Copy Layout SVGs once. Copy Brand-owned images/icons once. Pack and Style contribute no assets.

After installation, all downstream roles read project-local state only. Strategist ignores Pack as a design segment and resolves:

- Identity from Brand, otherwise current project confirmation.
- Direction/method from Style, otherwise current project planning.
- Structure from Layout, otherwise free design.

## 4. Handoff gate

- [x] Every selected Kind passed schema validation.
- [x] Pack references expanded and explicit overrides recorded.
- [x] Final set contains at most one Brand, Style, and Layout.
- [x] Only Layout supplied an SVG roster.
- [x] Project-local specs and assets were installed atomically.
- [x] Handoff persists `selected_pack_id` and resolved component ids for resume.
