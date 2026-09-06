# Template Packs

Pack is the fourth template kind. It is a metadata-only, one-click combination
of existing Brand, Style, and Layout assets. Pack owns no visual or structural
field and never contains SVG, images, logos, fonts, chart legends, or sample
content.

## Contract

Every `templates/packs/<pack_id>/` directory contains exactly one
`design_spec.md`:

```yaml
---
pack_id: <id>
kind: pack
summary: <discovery summary>
brand_id: <brand id or null>
style_id: <style id or null>
layout_id: <layout id or null>
keywords: [<three-to-five tags>]
---
```

At least two component references must be non-null. Nested Packs are forbidden.
All referenced ids must exist in their corresponding discovery indexes.

## Resolution

Selecting a Pack expands it into Brand, Style, and Layout before installation.
An explicitly selected component replaces the Pack reference of the same kind;
the other Pack references remain. At most one Pack may be selected. The Pack
spec may be retained project-locally as provenance, but Strategist never reads
it as a design segment.

Register or rebuild with:

```bash
python3 scripts/register_template.py <pack_id> --kind pack
python3 scripts/register_template.py --rebuild-all --kind pack
```

Resolve a Pack with optional explicit component overrides:

```bash
python3 scripts/resolve_template_selection.py \
  --pack <pack_id> \
  [--brand <brand_id>] [--style <style_id>] [--layout <layout_id>]
```

[`packs_index.json`](./packs_index.json) is the discovery source of truth.
