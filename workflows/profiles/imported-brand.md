---
description: Use a read-only user-provided PPTX as an identity-only Brand reference while generating a new presentation.
---

# Imported Brand Profile

Use this profile only when a separate Generate PPTX request explicitly selects
a Brand that was previously imported from a user-supplied `.pptx`. Brand import
itself is a standalone asset operation and does not create a project.

The shared Brand contains identity facts and Master/Layout-referenced assets;
it does not contain the source PPTX. `--register-icon-layout <id>` and
`--register-chart-layout <id>` may create narrowly scoped companion Layouts
for icon or chart visual grammar. `--register-page-kit-layout <id>` may create
a linked Brand Page Kit Layout containing only approved cover, TOC, section,
content and closing native prototypes. It never exposes the entire source deck
or changes ownership of content data.

Without a Page Kit it contributes only brand identity: canvas, palette,
typography, logos, icons, background motifs, and visual tone. With a Page Kit
enabled it additionally contributes only the declared prototypes, their locked
background/title/master objects, and editable slot contracts. It never promotes
guide pages, source sample text or unclassified archetypes.

Generate new SVG pages under the locked identity with the normal Generate Step
1–7 workflow. Choose charts, tables, and other visualizations from the Skill's
built-in catalogs by default. A selected chart-grammar Layout may additionally
guide chart type, series palette, axes, gridlines, legends, and labels, while the current
content source remains the only authority for data.
