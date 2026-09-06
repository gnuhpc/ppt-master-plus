---
description: Internal dispatcher for creating Brand, Style, Layout, or Pack assets
---

# Create Template

This is an internal maintenance entry, not a public presentation route. Select exactly one child workflow:

| Stable reusable value | Child |
|---|---|
| Official identity and brand assets | [`create-brand.md`](./create-brand.md) |
| Communication method, evidence discipline, and visual defaults | [`create-style.md`](./create-style.md) |
| Brand-neutral page structure and SVG prototypes | [`create-layout.md`](./create-layout.md) |
| One-click references to at least two registered components | [`create-pack.md`](./create-pack.md) |

A user-supplied PPTX is always imported as Brand on the public `Import Brand PPTX` route. Only an explicit `--register-icon-layout` or `--register-chart-layout` request may create a narrowly scoped companion Layout; it never creates a reusable source-page Layout or Pack. Ask one discriminator only when the stable reusable value cannot be determined from the request and supplied evidence.

## Shared gates

1. Analyze source evidence without writing final library state.
2. Propose Kind, ID, summary, provenance, and owned fields.
3. Obtain explicit confirmation before creating the final asset directory.
4. Invoke exactly one child workflow and honor its schema boundary.
5. Validate with `svg_quality_checker.py --template-mode` where applicable and `register_template.py <id> --kind <kind> --dry-run`.
6. Register the confirmed library asset; project-scoped workspaces are not added to global indexes.

Pack is metadata-only. Layout is the only Kind with an SVG roster. Brand may carry identity assets. Style and Pack must not carry files beyond their Design Spec.
