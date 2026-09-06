---
description: Create a metadata-only Pack that combines existing Brand, Style, and Layout assets
---

# Create Pack

Enter only after the internal Create Template router selects `kind: pack`.

## Required contract

1. Choose a filesystem-safe `pack_id`, discovery summary, and 3–5 keywords.
2. Resolve existing ids from `brands_index.json`, `styles_index.json`, and
   `layouts_index.json`; never scan directories or infer an unregistered id.
3. Set at least two of `brand_id`, `style_id`, and `layout_id`; use `null` for
   an intentionally open component. Nested Packs are forbidden.
4. Confirm the exact combination with the user before writing library state.
5. Create `templates/packs/<pack_id>/design_spec.md` only. Do not create SVG,
   images, icons, exports, or duplicate component rules.
6. Validate with `register_template.py <pack_id> --kind pack --dry-run`, then
   register without `--dry-run`.

Pack selection expands to its component roots before installation. An explicit
component selected beside the Pack replaces the Pack reference of the same
kind. The Pack spec is provenance only and never participates in design-field
precedence.
