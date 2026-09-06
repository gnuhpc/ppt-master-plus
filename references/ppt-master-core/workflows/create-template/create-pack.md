---
description: Author and register a metadata-only Template Pack
---

# Create Pack

Enter only after [`Create Template`](../create-template.md) dispatches
`kind: pack`.

Confirm `pack_id`, summary, keywords, and references to at least two registered
Brand, Style, and Layout ids. A Pack cannot reference another Pack and cannot
contain design rules, SVGs, assets, examples, or review exports.

Library output:

```text
templates/packs/<pack_id>/
└── templates/
    └── design_spec.md
```

The Design Spec frontmatter contains only `pack_id`, `kind`, `summary`,
`brand_id`, `style_id`, `layout_id`, and `keywords`. Validate and register with:

```bash
python3 skills/ppt-master/scripts/register_template.py <pack_id> --kind pack --dry-run
python3 skills/ppt-master/scripts/register_template.py <pack_id> --kind pack
```

At consumption time the Pack expands to its registered components. Explicit
same-kind component selections override Pack references; Pack metadata never
becomes a design segment.
