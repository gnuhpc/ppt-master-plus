# Optional Diagram Routing

Use companion diagram skills only when they are already available in the
current session. Do not install a missing companion automatically and do not
block production when one is unavailable.

## Route Selection

Use this order when a slide needs a diagram:

| Priority | Need | Preferred route | Output contract |
|---|---|---|
| 1 | Ordinary presentation diagram, branded infographic, chart, or no companion-specific style requested | built-in SVG | Author the page directly through the normal Executor workflow |
| 2 | Formal technical architecture, system topology, data flow, or precise process | `fireworks-tech-graph` | Preserve its source SVG plus exported PNG; use the SVG as the slide asset |
| 3 | Hand-drawn, whiteboard, brainstorming, informal architecture, or editable sketch source | `excalidraw` from `Agents365-ai/excalidraw-skill` | Preserve `.excalidraw` plus exported SVG/PNG when available; use SVG in the deck |
| 4 | Diagrams-as-code, auto-laid-out flowcharts, UML, sequence, ER, state, or C4 diagrams where source text matters | `plantuml-skill` or `creating-mermaid-diagrams` | Preserve `.puml`/`.mmd` plus exported SVG/PNG; use exported SVG as a diagram asset, not as native slide SVG |
| 5 | Precise draw.io-style diagrams, vendor/cloud icons, rich shape vocabulary, strict topology, or advanced UML styling | `drawio-skill` | Preserve `.drawio` plus exported SVG/PNG; use exported SVG as a diagram asset |
| 6 | Explicit tldraw request or tldraw-native whiteboard source | `tldraw-skill` | Preserve `.tldr` plus exported SVG/PNG; use exported SVG as a diagram asset |

Default to built-in SVG when the user did not request a companion-specific
style. In Gated mode, include a companion route in the Production Route Gate
and wait for approval. In Continuous mode, use a companion only when the
confirmed visual style or explicit user request clearly selects it.

When multiple companion routes match, select the earliest available route in
the table above; do not invoke multiple diagram skills for the same diagram.
If a companion fails, retain any diagnostic output, fall back to built-in SVG,
and continue.

## Dependency Check Order

Companion diagram skills are soft dependencies. Check only the route you are
about to use, in priority order, and do not install missing tools unless the
user explicitly asks.

| Route | Minimum check | SVG path | PNG path | Fallback |
|---|---|---|---|---|
| built-in SVG | none beyond the normal `ppt-master-plus` pipeline | native Executor SVG | native export pipeline | Continue with built-in SVG |
| `fireworks-tech-graph` | skill available; `python3` and `cairosvg` CLI or Python module, otherwise `rsvg-convert`/puppeteer if already present | hand-written/validated SVG | `cairosvg` preferred | Fall back to built-in SVG |
| `excalidraw` | skill available; `curl --version` for Kroki SVG | Kroki SVG via `curl`, or local CLI SVG if installed | `excalidraw-brute-export-cli` only | Use SVG-only when PNG export is unavailable; fall back to built-in SVG on render failure |
| `plantuml-skill` | skill available; `curl --version` for Kroki | Kroki SVG | Kroki PNG | Fall back to Mermaid if it better fits and is available; otherwise built-in SVG |
| `creating-mermaid-diagrams` | skill available; `mmdc --version` or `curl --version` for Kroki | `mmdc` SVG or Kroki SVG | `mmdc`/Kroki PNG | Fall back to PlantUML for UML-heavy diagrams if available; otherwise built-in SVG |
| `drawio-skill` | skill available; resolve `drawio`, `draw.io`, or the platform app path | draw.io CLI SVG | draw.io CLI PNG | Use browser/XML-only for user review, but use built-in SVG for PPT production if export is unavailable |
| `tldraw-skill` | skill available; `tldraw --version` | tldraw CLI SVG | tldraw CLI PNG | Fall back to Excalidraw for whiteboard style if available; otherwise built-in SVG |

Do not treat "supports SVG" as sufficient PPT compatibility. External
diagram SVGs may contain styles, masks, foreign objects, or other constructs
outside the PPT Master native SVG subset. Keep them as diagram assets under
`images/` unless they were authored directly by the Executor or explicitly
cleaned and checked against `shared-standards.md`.

Store companion sources under `<project_path>/diagram_sources/` and exported
slide assets under `<project_path>/images/`. Re-run `analyze_images.py` after
adding exported assets so the Executor reads current dimensions.
