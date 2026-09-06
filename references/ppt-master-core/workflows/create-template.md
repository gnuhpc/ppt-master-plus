---
description: Shared internal entry for creating Brand, Style, Layout, or Pack workspaces
---

# Create Template

Choose exactly one child by the reusable value the user wants:

| Kind | Child | Owns |
|---|---|---|
| Brand | [`create-brand.md`](./create-template/create-brand.md) | Identity facts and brand assets |
| Style | [`create-style.md`](./create-template/create-style.md) | Communication method and non-binding defaults |
| Layout | [`create-layout.md`](./create-template/create-layout.md) | Brand-neutral SVG structure and semantic slots |
| Pack | [`create-pack.md`](./create-template/create-pack.md) | References to at least two registered components |

Do not infer reusable Layout or Pack assets from a user-uploaded PPTX. Public PPTX import creates a project-level Brand. Do not author final library state before the user confirms Kind, id, summary, and the child-specific contract.

## Shared lifecycle

1. Inspect source evidence and provenance.
2. Propose the owned reusable contract and explicitly excluded material.
3. Confirm the brief.
4. Create the child workspace.
5. Validate the child schema and assets.
6. Optionally generate review output for Layout only.
7. Run `register_template.py <id> --kind <kind> --dry-run`, then register.
8. Return the exact workspace root for later Generate selection.

The registrar Kind is mandatory and one of `brand`, `style`, `layout`, or `pack`. Layout is the only roster-bearing Kind. Pack carries no design fields or assets, cannot nest, and expands before installation.
