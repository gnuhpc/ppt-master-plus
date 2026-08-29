# Executor Common Guidelines

> Narrative skeleton and visual aesthetic come from this deck's locked files under [`modes/`](./modes/_index.md) and [`visual-styles/`](./visual-styles/_index.md). Technical constraints are in shared-standards.md.

---

## 1. Template Adherence Rules

### 1.0 Pre-generation Batch Read

**Hard rule**: Before the first SVG page, batch-read every template SVG this deck will reference. Read once up front, never re-read during generation.

| Source list | Read path |
|---|---|
| Chosen template's `design_spec.md` (read frontmatter to detect `replication_mode`) | `templates/design_spec.md` |
| Every distinct `<basename>` in `spec_lock.md page_layouts` | `templates/<basename>.svg` |
| Every distinct chart name in `spec_lock.md page_charts` | `templates/charts/<chart_name>.svg` |
| Chart types in `design_spec.md §VII` not covered above | `templates/charts/<chart_name>.svg` |
| `visual_ref` chart names from `design_spec.md §VII` `no-template-match` pages | `templates/charts/<visual_ref>.svg` |

**Default — read each template once; re-read only on the mid-deck exception below**:
- Layout SVG already loaded in this batch
- Chart SVG already loaded in this batch

`spec_lock.md` is the only file re-read per page (§2.1).

**Exception**: user mid-deck adds pages or swaps templates introducing a basename/chart absent from the original batch → read the new file once, continue.

> Note: batched prefix reads stay in the cached prompt prefix; per-page `spec_lock.md` re-reads append below and benefit from that cache. Scattered on-demand reads of layout/chart SVGs would invalidate downstream cache and sit in the compression-vulnerable mid-context region.

Resolve the per-page template SVG via `spec_lock.md page_layouts` (authoritative). The legacy page-type table below is a **last-resort fallback** for legacy decks where `page_layouts` is missing.

**Resolution order (per page):**

1. **Mirror-mode template** (template's `design_spec.md` frontmatter has `replication_mode: mirror`) → see §1.1 below. The page is consumed as a **visual reference**, not as a placeholder shell.
2. `spec_lock.md page_layouts` has `P<NN>: <basename>` for this page → inherit the structure of `templates/<basename>.svg` (already in context from §1.0).
3. `page_layouts` exists but **no entry** for this page → **free design**, no template inheritance.
4. `page_layouts` section absent (legacy deck) **and** `templates/` directory exists → fall back to the page-type table below, matching by SVG filename keyword (cover/chapter/content/ending/toc). Read the matched file at first use if §1.0 batch did not cover it.
5. No template at all → free design.

> Note: `page_layouts` disambiguates the multiple content variants modern templates ship (e.g., `graduation_defense` has 8); the legacy table cannot.

**Templates supply structure, not skin (non-mirror)**: a chart or layout template's gradients, drop-shadows, palette, **and font sizes** are placeholder. Inherit its geometry, label / legend placement, and series-encoding logic; re-skin every fill / stroke to the deck's `visual_style` + `spec_lock.colors` — flat styles strip the gradients and shadows, gradient / glass styles repaint their own. Forbidden — shipping a template's default `<linearGradient>` / `cardShadow` / Tailwind fills unchanged. Mirror templates are the exception: §1.1 preserves their visuals verbatim.

**Font size is skin, not geometry (non-mirror).** A chart / layout template's hardcoded `font-size` values (often 11–16px, sized for the template's own dense placeholder text) are NOT inherited — classify each text into its `spec_lock.md` role and use that role's locked size, exactly as you re-skin color. **Structural roles (page title / body / subtitle / annotation / footnote) hold their one deck-wide size on every page** — the template's placeholder px never overrides it; same-role text drifting page to page is what makes a deck look unprofessional.

**Typography execution order (mandatory):**

1. Build a per-page text inventory from `design_spec.md §IX` + the current `notes/<NN>_*.md`.
2. Classify each text item before drawing. **Structural roles** (`title`, `subtitle` / `lead`, `body`, `annotation`, `footnote` / `page_number`) must map to their declared `spec_lock.typography` slot. A **one-off feature element** (a single hero number, an isolated emphasis label) may take an in-ramp intermediate value — the ramp is anchored on `body`, not a closed menu — but a feature size that **recurs** must be promoted to a declared slot. The failure mode this guards against is structural text silently inheriting the template's compact px, not legitimate feature sizing.
3. Copy the role's locked px value into `font-size` verbatim. Do this before placing the text; never start from a template `font-size` and then "adjust".
4. Layout from those locked sizes: compute line-height, wrapped line count, child `y` / `dy`, card padding, card height, column gaps, and available image/chart area from the chosen px values.
5. Only after this reflow may you inspect fit. If fit fails, move / resize containers or simplify local geometry first; do not reduce the role size merely because the inherited template slot was smaller.

**Geometry adapts to the type, never the reverse**: when the locked size is larger than the template's placeholder text, widen / heighten the card, open spacing, and recompute child `y` / `dy` to make room — do not shrink the font to fit the inherited container. A `font-size` change is a layout change: revise line-height and every downstream vertical coordinate that depends on it. For wrapped text, allocate at least the wrapped line count × line-height plus top / bottom padding; fixed `y` stacks copied from a smaller template are invalid once the locked role size is applied. The Executor renders the page it was given; page count and per-page density are the Strategist's call, fixed at confirmation — do **not** re-paginate, split the page, or drop authored content to cope with size here. Only when a single block still cannot fit after the geometry is fully reflowed may you shrink **that block** as a bounded last resort — and **only body text** is ever shrunk this way. Title, subtitle, annotation / caption, footnote and page number are **locked once set and never adjusted to fit** — their values hold across the whole deck. Step the overflowing body block's `font-size` down by `2`px at a time, and only if it still overflows step it down again, up to a cumulative floor of **`4`px below the locked body size** (e.g. `24` → no smaller than `20`). This is a **local, single-block** reduction — the deck-wide locked body size is unchanged on every other block and page. (The Executor works in **unitless px** throughout — spec_lock and SVG carry no `pt`.) If the block still overflows at the floor, surface a `warning:` rather than silently restructure the page. (Mirror templates are the exception: §1.1 preserves their sizes verbatim — there the source deck's typography *is* the spec.)

### 1.1 Mirror-mode templates — reference-style consumption

When the project's chosen template is a `mirror` template (`design_spec.md` frontmatter declares `replication_mode: mirror`), Executor switches to a **reference-style** consumption path that bypasses placeholder substitution:

1. **Per-page reference selection** — Strategist selects one mirror page per project page via `spec_lock.md page_layouts` (e.g., `P04: 015_content`). The basename is the mirror filename without extension; Strategist made this choice by reading `design_spec.md §V Page Roster` descriptions, not by guessing.
2. **Copy, don't fill** — open the referenced mirror SVG (already in context from §1.0). **Copy it as the starting point for the project page**, then edit text elements in place to express the project's content for `P<NN>`. Preserve every non-text element verbatim: backgrounds, decorative shapes, sprite-cropped images, charts, icon usage, color values, font families, geometry, sprite `<svg viewBox>` wrappers, and **which image** each `<image>` points at.
3. **What you may edit** — the visible text content of `<text>` / `<tspan>` elements that express slide-specific content (title, body, captions, KPI labels, dates, page numbers). Replace the source deck's example text with the project's text for this page from `design_spec.md §IX` and `notes/<NN>_*.md`.
4. **What you must not touch** — element positions, sizes, fonts, colors, fills, strokes, gradients, **which image each `<image>` points at**, `<g>` grouping, sprite-sheet `<svg viewBox>` wrappers, decorative `<rect>` / `<path>` / `<circle>` / `<polygon>` shapes, `<use data-icon="...">` markers, embedded chart data structures. Mirror's value is preserving the source deck's visual identity — any geometric / decorative drift defeats the purpose. **The `href` path is not the image**: normalizing a bare `href="cover_bg.png"` to `href="../images/<name>"` (when Step 3 relocated the asset to `images/`) points at the *same* image and changes nothing visual — that is an allowed path fix, not a fidelity edit. Leaving the bare href as-is is also fine; the exporter and live preview resolve bare hrefs against `images/` either way.
5. **Content fit** — the mirror page was chosen by Strategist because its layout matches the content slot. If the project's content for `P<NN>` legitimately needs more / fewer items than the mirror page provides (e.g. mirror shows 3 KPI cards, project has 4 metrics), keep the mirror page's visual rhythm and either drop one metric to fit or split across two pages — do **not** restructure the mirror page's grid. If neither works, surface a `warning: P<NN> content does not fit mirror reference <basename>; suggest different reference page` and proceed with the closest-fit edit.
6. **No `{{}}` substitution** — mirror SVGs do not contain placeholder markers. Do not search for `{{TITLE}}` / `{{CONTENT_AREA}}` etc.; do not invent placeholders. The whole mirror contract is "verbatim source + in-place text edit".
7. **Output filename** — follow the standard project SVG naming convention (`<NN>_<page_name>.svg` where `<NN>` matches the project page index, not the mirror source index). The mirror filename is the *reference*, not the *output*.

**Detecting mirror mode**: read the chosen template's `design_spec.md` frontmatter once during §1.0 batch read. If `replication_mode: mirror`, every page that hits `page_layouts` follows §1.1 above; pages without a `page_layouts` entry still fall through to free design (resolution rule 3 above).

**Mirror + chart pages**: chart structures inside a mirror SVG are already drawn (axis, series, labels). Treat them as visual references — replace the data labels and series text content to match the project's chart spec, but do not redraw the chart from a `templates/charts/<name>.svg` baseline. A mirror template's `page_charts` entries are normally absent for this reason.

**Legacy fallback table** (used only when `page_layouts` is absent):

| Page Type | Corresponding Template | Adherence Rules |
|-----------|----------------------|-----------------|
| Cover | `01_cover.svg` | Inherit background, decorative elements, layout structure; replace placeholder content |
| Chapter | `02_chapter.svg` | Inherit numbering style, title position, decorative elements |
| Content | `03_content.svg` | Inherit header/footer styles; **content area may be freely laid out** |
| Ending | `04_ending.svg` | Inherit background, thank-you message position, contact info layout |
| TOC | `02_toc.svg` | **Optional**: Inherit TOC title, list styles |

### Page-Template Mapping Declaration (Required Output)

Before generating each page, output which template is used:

```
📝 **Template mapping**: `templates/03a_content_image_text.svg` (or "None (free design)")
🎯 **Adherence rules / layout strategy**: [specific description]
```

- **Content pages**: template defines only header/footer; content area is free
- **No template**: generate entirely per the Design Spec

---

## 2. Design Parameter Confirmation (Mandatory Step)

Before the first SVG page, output a confirmation listing: canvas dimensions, body font size, color scheme (primary/secondary/accent HEX), font plan. Prevents spec/execution drift.

### 2.1 Per-page spec_lock re-read (Mandatory)

> Long decks drift off the declared palette/icons mid-deck due to context compression. `spec_lock.md` is the canonical execution reference — re-read it per page to bypass model memory.

**Hard rule**: Before generating **each** SVG page, `read_file <project_path>/spec_lock.md`. Use only values from this file, not from memory. If context was auto-compacted, also `read_file <project_path>/design_spec.md` for the current page's §IX brief.

**Per-block expression**: render each `design_spec.md §IX Content` block in its written texture — a full-sentence block as wrapped prose, a fragment/label block as bullets/keywords. **Never split a full-sentence block into a bullet list** — splitting loses the information that the block was continuous reasoning, not a set of parallel points; not because a bullet lays out easier, and not because an inherited template slot is shaped as a list. If a block carries no clear texture, infer the mode from its wording and the page layout.

- **Prose render recipe**: one `<text>` per paragraph; wrap lines with sibling `<tspan>` that reset `x` to the block's left edge and advance `dy` by the font size × a line-height factor. **Default — line-height by density (may override per content fit)**: ~1.4–1.5× for dense / small-body blocks (CLReq comfortable minimum), 1.6–2.0× for large-type, sparse, or `breathing` blocks. Fit about width ÷ font-size CJK glyphs per line (Latin fits roughly twice that); the last line runs short. Use the body ramp size, not a new one.
- **Template precedence**: when an inherited template slot is a bullet list but the §IX block is prose, the prose wins — widen or reflow the container to hold the paragraph, or drop that card; do not pour the sentence back into the list slot.
- **Mode precedence**: the locked mode shapes voice / register, not §IX's authored titles or page order. When a `§IX` title is a user-authored topic label, keep it — do not upgrade it to an assertion just because the mode (e.g. `pyramid`) favors them; mode title-tendencies apply only to AI-drafted titles.

> Note: block-level phrasing, applied *within* the page's `page_rhythm` density (below), not against it.

**If `spec_lock.md` is missing**: emit `warning: spec_lock.md missing — generating without execution lock` once, then proceed using `design_spec.md` values. Expected only for legacy projects; new projects MUST have it (see [strategist.md](strategist.md) §6 step 4).

**Forbidden — values outside the lock**:

- Colors (fill / stroke / stop-color) MUST come from `colors`
- Icons MUST come from `icons.inventory`; library MUST equal `icons.library`
- Font family from `typography`: use role override (`title_family` / `body_family` / `emphasis_family` / `code_family`) if declared, else fall back to `font_family`
- Font sizes follow a **ramp anchored on `typography.body`**, not a closed menu. **Structural roles — page title, body, subtitle, annotation / caption, footnote / page number — render at one consistent size deck-wide, taken from their `spec_lock` slot; never re-pick a structural role's size page by page or carry a template's placeholder px.** This locks the **role**, not every glyph: a page may still carry deliberate typographic hierarchy — a lead-in sentence, an inline emphasis figure, a pull-quote, a kicker, a hero number — but each of those is its **own role / feature element** with its own size, **applied consistently deck-wide** (declare a recurring one as its own `spec_lock` slot). In-band intermediate sizes are for exactly these feature elements. What is banned is the *same* role drifting size to fit a container or by page whim — that scatter is what reads as unprofessional. Sizes outside every band require extending the lock first.
- **The page's core message is primary — render it ≥ `body`.** The one-idea / key-claim / key-takeaway line a page is built around is its most important text; map it to the locked `lead` or `subtitle` slot (≥ `body`), never to a sub-`body` size. Demoting it below body while data callouts or labels sit larger inverts the hierarchy — the failure this prevents. If no `lead` / `subtitle` slot is locked for a recurring core-message line, surface it (per below) instead of improvising a smaller one. A footnote / page number / source credit uses the locked `footnote` (or `annotation`) slot — never an invented sub-`annotation` size; and the body-shrink last resort (§1.0) bottoms out at `body − 4`px, a hard floor never crossed.
- **Write the locked px verbatim; at most 2 decimals.** `font-size` MUST be the exact px from `spec_lock.typography` — if `body` is `24`, write `24`; never substitute a "rounder" or PowerPoint-familiar number (`20` / `18` / `36`). The system is px-only — there is no pt to convert, and a remembered pt-style value written as px renders the whole deck the wrong size. Prefer whole numbers (sizes are clean even px); keep a decimal only for a slot that genuinely carries one in `spec_lock`. Never emit long tails like `20.8026`: the exporter rounds the final size to 1 decimal pt, so extra px precision is wasted noise.
- Images MUST reference files listed under `images`; no invented filenames
- Formula PNGs are images with `Acquire Via: formula` / `Status: Rendered`; place them only from the listed file path and never recreate the formula as text.

If a page needs a value not in `spec_lock.md`, surface it — do not silently invent one.

**Per-page layout rhythm — `page_rhythm` section**:

Before drawing each page, look up its entry in `page_rhythm` (key format `P<NN>` matching the page index in §IX of `design_spec.md`) and apply the corresponding layout discipline:

| Tag | Layout discipline |
|-----|-------------------|
| `anchor` | Structural page (cover / chapter / TOC / ending). With a template, follow the matching template verbatim. In free design (no template), realize the page's §IX intent — for the cover deliver its `Cover impact` and for a closing page its `Closing impact` (the committed hook / takeaway + composition), never a default centered title + subtitle or a generic "Thank you" sign-off. |
| `dense` | Information-heavy. Card grids, multi-column layouts, KPI dashboards, tables, and charts are all permitted. This is the baseline behavior. |
| `breathing` | Low-density impact page. Avoid **multi-card grid layouts** — do not organize content as multiple parallel rounded containers (3-card row, 4-card KPI grid, 2×2 matrix rendered as cards). Use naked text blocks, dividers, whitespace, or full-bleed imagery as the content structure. Single rounded visual elements (hero image corners, callouts, tags, one emphasis block) are fine — the rule is about grid structure, not about the `rx` attribute. Proportions follow information weight (not a preset ratio). Typical forms: hero quote, single large number with one-line interpretation, full-bleed image with floating caption, section transition. |

> Without rhythm variation, every page defaults to card grids (the "AI-generated" look). `page_rhythm` is the only narrative lever that survives context compression.

**Missing `page_rhythm` section** → emit `warning: spec_lock.md missing page_rhythm — defaulting all pages to dense` once, fall back to `dense` for all pages.

**Tag not found for current page** → emit `warning: spec_lock.md page_rhythm tag not found for P<NN> — falling back to dense` once per deck (aggregate; do not repeat per page), fall back to `dense`. Do not invent a tag.

**Layout variety — anti-repetition rule**:

The single most recognizable marker of AI-generated decks is uniform composition: the same 3-card grid on every content page, the same left-text / right-image split throughout, the same decorative panel stamped identically on every slide. Before drawing each page, recall the compositional structure used on the preceding 2–3 pages and choose a meaningfully different structure — unless one of the logical exceptions below applies.

What counts as the **same layout** (avoid repeating these consecutively):
- Same grid structure (e.g., 3-column card grid → 3-column card grid → 3-column card grid)
- Same compositional split used 3+ times in a row (e.g., left-half text / right-half image × 4 pages)
- Same accent / decorative motif in an identical position on every page (a shared header stripe is fine; identical sidebar panels page after page is not)
- Same content-organization form across all content pages (bullets every page, or rounded card panels every page)

What counts as **different** (any of these breaks the repetition):
- Different column count or flow direction (2-col → full-width prose → 3-col → 1-col hero)
- Switching between horizontal flow, vertical stack, and free-form placement
- Replacing a card grid with a table, timeline, stepped flow, or text + rule structure
- Moving the accent element (top bar → left sidebar → bottom divider → scattered icon grid)
- Alternating "wide content + narrow sidebar" vs. "centered single column" vs. "full-bleed image + floating text"

**Allowed exceptions — same structure may repeat when**:

| Exception | Rule |
|---|---|
| Logical pairing | Two adjacent pages form a deliberate before/after, problem/solution, or Part 1 / Part 2 pair — matching structure reinforces the link |
| Chapter grouping | Pages within the same chapter share a chapter-level visual motif (e.g., left accent stripe for all sub-pages of one section) |
| Anchor pages | Cover, chapter openers, TOC, and ending share a structural framework with each other — they are not counted against content-page variety |
| Template-locked | `page_layouts` assigns the same SVG basename to multiple consecutive pages — Executor must follow; layout variety for those pages was the Strategist's responsibility |
| Data comparison series | Multi-chart or multi-table pages that the user must compare side-by-side share the same container geometry intentionally |

**Per-page template lookup — `page_layouts` section**:

Before drawing each page, look up its entry in `page_layouts` to decide which basename to inherit (the SVG itself was loaded in §1.0):

- Entry present (e.g., `P04: 03a_content_image_text`) → inherit the corresponding SVG already in context. The basename **must match** an actual file in the chosen template directory; if it doesn't, emit `warning: page_layouts P<NN> references missing file <basename>.svg — falling back to free design` and proceed.
- No entry for this page → free design, no inheritance. **Not an error** — Strategist intentionally left this page free.
- Whole section absent → see §1 fallback (legacy page-type matching).

Do **not** invent a layout entry, and do **not** assume a template just because `templates/` exists — if `page_layouts` is present but silent for this page, that silence is the instruction.

**Per-page chart reference — `page_charts` section**:

Before drawing each page, look up its entry in `page_charts` to decide which chart structure applies (the SVG itself was loaded in §1.0):

- Entry present (e.g., `P09: timeline_horizontal`) → adapt the corresponding chart SVG already in context. Apply project colors/typography/density; do not copy verbatim. Cross-reference `templates/charts/charts_index.json` for the chart's purpose summary if needed.
- No entry for this page → either no chart on this page, or a chart that didn't match any catalog template (Strategist's `no-template-match` fallback). **`no-template-match` means the content shape didn't fit any template's structure — not that chart SVGs are off-limits.** The Strategist also recorded a `visual_ref` chart name in §VII; that SVG is already in context from §1.0. Draw from its visual vocabulary — mark geometry, decoration treatment, label placement, spatial rhythm — while designing the data structure freely. Do not inherit the template's data layout; do inherit its visual ambition. Design the visualization from scratch using `design_spec.md §VII` for data guidance and the `visual_ref` SVG for visual vocabulary.
- Whole section absent → no chart pages in this deck.

> **Free-design chart ambition rule** (applies whenever a chart is designed from scratch — no `page_charts` entry, `no-template-match` fallback, or no template directory at all):
>
> The single most recognizable failure mode of AI-generated charts is **solid color blocks** — flat rectangular bars, flat pie slices, flat line-on-white — with no visual ambition beyond filling the spec palette. Unless the user or `visual_style` explicitly calls for "simple" / "flat" / "minimal", every free-design chart must reach for a higher visual register. Techniques to draw from:
>
> | Chart type | Elevation techniques (pick what fits) |
> |---|---|
> | Bar / column | Gradient fill along the value axis (solid at base → lighter at tip); rounded bar tips (`rx`); thin accent hairline cap at the bar top in `accent` color; chamfered or angled bar ends; oversized value label floating above the bar |
> | Horizontal bar | Leading dot or diamond mark at the bar end; stagger alternate rows with a subtle rule divider; use negative-space gap between bar and axis |
> | Line / area | Stroke `stroke-width` ≥ 2.5px; duplicate the path at lower opacity + larger width for a soft glow; area fill as a gradient from `primary` at 0.55 opacity → `primary` at 0 at baseline; dot markers at each data point with a white inner ring |
> | Scatter / bubble | Mix two marker shapes (circle + diamond) by category; vary opacity by density; add a subtle connecting path or convex hull outline for clusters |
> | Pie / donut | Prefer donut; add a large center label (key stat or category count); use arc stroke rather than fill for a lighter look; offset the most important slice by 6–8px; inner callout lines with precise label placement |
> | Timeline / roadmap | Custom node shapes (circle, hexagon, diamond) at milestones; connector lines with arrowheads or dashes; vertical color band behind active period |
> | KPI / scorecard | Oversized hero number in `primary`; supporting micro-sparkline or progress arc; unit label in `annotation` style beside the number |
> | Table / matrix | Alternating row fills at 0.06 opacity; header row in `primary` at full opacity with inverted text; cell heat-map shading for numeric columns |
> | Radar / spider | Fill polygon at 0.18 opacity + stroke at full; grid rings in `body_text` at 0.12 opacity; axis labels with small colored dots |
>
> **Decoration budget**: add at most one structural embellishment (gradient, glow, shape variation) and one typographic embellishment (oversized label, inline annotation) per chart — do not layer every technique simultaneously, which reads as noise.
>
> **Solid flat color blocks are acceptable** only when: (a) the user explicitly requests "simple" or "flat", (b) `visual_style` is `swiss-minimal` / `brutalist` / `typographic` and the style's aesthetic is precision over decoration, or (c) the chart is a tight small-multiple where embellishment would be unreadable at the rendered size.

> **Architecture and flow diagram semantic color rule** (applies to multi-lane pipelines, component architectures, and process flows — regardless of whether preserve_master is true or false):
>
> Color is a semantic medium in architecture diagrams, not decoration. Assign one color from `spec_lock.colors` per functional role and apply it consistently across that role's entire visual footprint on the page:
>
> | Color's functional scope | How to apply |
> |---|---|
> | Panel / lane border | `stroke="<role-color>"` — the primary semantic signal |
> | Connector arrow | `stroke="<role-color>"` + matching `<marker>` arrowhead filled in the same color |
> | Role heading label | `fill="<role-color>"` — the section title inherits its lane's color |
> | Role icon | `stroke="<role-color>"` (for outline icons) |
>
> Role assignment example for a data pipeline: data-source = `secondary_accent`, processing = `primary`, storage = `accent`, output = `success`. An arrow from processing to storage uses the processing color arrowhead entering an accent-bordered storage panel. One color, one role, applied end-to-end — the audience reads the diagram without a legend.
>
> **Directional arrows are mandatory on flow diagrams**: every connector between architecture components must carry `marker-end` with a pointed arrowhead. A flow diagram without arrowheads is an adjacency diagram — the direction of data or control is the key information. Size arrowhead markers at ≥ 8×8 logical units; match arrow stroke and arrowhead fill to the source lane's semantic color.
>
> **Architecture panels must be semi-transparent**: lane boxes and component panels should use `fill="<secondary_bg>" fill-opacity="0.90–0.96"` rather than a solid opaque fill (e.g., `fill="#1F2937"`). The slight transparency integrates the panel with whatever background is behind it (master or slide-local) and signals a layered overlay rather than a canvas replacement. This rule applies even when preserve_master is false — transparent panels read as contained content, opaque ones read as background.

> **Faithful beautify + `preserve_master=true` override**: these rules apply only when `spec_lock.md` explicitly sets `preserve_master: true`. Generic PPTX beautification through the main pipeline must not set this flag and should generate complete slide backgrounds and visual systems normally. When the flag is present, treat every chart page as **free design regardless of what `page_charts` says**. The preserved master already supplies visual scaffolding (background, palette context, chrome). Design the chart from scratch — choose geometry, mark type, axis layout, and decoration that best express the data and the deck's `visual_style`. `page_charts` entries and the catalog SVGs are optional reference for visualization *type* only; never copy a template's structural geometry. The goal is a custom, aesthetically considered chart, not a template fill. Data values from `design_spec.md §VII` are frozen.
>
> **Chart element background — transparent by default**: when `preserve_master=true`, every chart's plot area, container panel, and bounding box must default to `fill="none"` (SVG transparent). The master background shows through and the chart floats visually on top. Apply this to every chart sub-element: plot-area `<rect>`, legend box, chart card wrapper, grid background — all `fill="none"` unless a specific contrast need exists.
>
> **Conditional background — only when contrast demands it**: if the master's background color (read from `spec_lock.colors.background`) makes data marks or axis labels unreadable without contrast separation, a bounded local panel is permitted — but it must be:
> - Filled with `spec_lock.colors.secondary_bg` at opacity ≤ 0.15, **or** `spec_lock.colors.background` at opacity ≤ 0.12 — never a solid opaque fill, never white, never a gray unrelated to the palette
> - Sized only to the chart's own bounding box (no full-slide reach)
> - Rounded corners (`rx="8"`) to read as a local element, not a page chrome
>
> **Axis lines and gridlines**: stroke with `spec_lock.colors.body_text` at opacity 0.15–0.20. Never solid black or a template's default gray.
>
> **Series colors**: draw from `spec_lock.colors` — `primary`, `accent`, `secondary_accent` as the first three series colors; derive additional series by adjusting opacity or lightness within the same palette. Never carry over a chart template's default series palette.

---

## 3. Execution Guidelines

- **Proximity**: group related elements with tight spacing; separate unrelated groups
- **Spec adherence**: follow color, layout, canvas format, and typography in the spec
- **Template structure**: if templates exist, inherit the visual framework
- **Main-agent ownership**: SVG generation must run in the main agent (not sub-agents) — pages share upstream context for cross-page visual continuity
- **Generation rhythm**: lock global design context first, then generate pages sequentially in one continuous context. No batched groups (e.g., 5 at a time).
- **Phased batch generation** (recommended):
  1. **Visual Construction Phase**: generate all SVG pages sequentially for visual consistency. Use layout judgment for chart marks during the draft. **MUST embed plot-area markers** per §3.1 below on every chart page — coordinate calibration is a post-generation step (see `verify-charts` Stage(../workflows/stages/verify-charts.md)) that depends on these markers.
  2. **Quality Check Gate**: run `python3 scripts/svg_quality_checker.py <project_path>` on `svg_output/`. Any `error` (banned features, viewBox mismatch, spec_lock drift, non-PPT-safe font, etc.) MUST be fixed on the offending page before proceeding — regenerate and re-check. Address `warning`s when straightforward. Do NOT defer to after `finalize_svg.py` — finalize rewrites SVG and masks some violations.
  3. **Logic Construction Phase**: after SVGs pass the quality check, batch-generate speaker notes for narrative continuity.

### 3.1 Chart Plot-Area Marker (MANDATORY on every chart page)

> The [`verify-charts`](../workflows/stages/verify-charts.md) workflow enumerates chart pages from `design_spec.md §VII`, then reads each page's plot-area marker to feed `svg_position_calculator.py`. Missing marker → verify-charts has to re-derive the plot area from axis lines, paying the cost on every run.

**Hard rule**: every SVG page that contains a data visualization chart includes a plot-area marker inside `<g id="chartArea">`, placed **after axis lines** and **before the first data element** (bar, line, area, point).

**Rectangular plot area** (bar / horizontal_bar / grouped_bar / stacked_bar / line / area / stacked_area / scatter / waterfall / pareto / butterfly):

```xml
<!-- chart-plot-area: x_min,y_min,x_max,y_max -->
```

**Radial charts** (pie / donut / radar):

```xml
<!-- chart-plot-area: pie | center: cx,cy | radius: r -->
<!-- chart-plot-area: donut | center: cx,cy | outer-radius: r1 | inner-radius: r2 -->
<!-- chart-plot-area: radar | center: cx,cy | radius: r -->
```

**How to determine coordinate values**:

| Value | Derivation |
|-------|------------|
| `x_min` | X coordinate of the Y-axis line (leftmost data boundary) |
| `y_min` | Y coordinate of the topmost grid line (highest data boundary) |
| `x_max` | X coordinate of the rightmost axis endpoint or grid line |
| `y_max` | Y coordinate of the X-axis baseline |
| `cx, cy` | Center point of pie/donut/radar (accounting for `transform="translate()"`) |
| `r` | Outer radius of the chart |

**Per-page verification** — after writing each chart SVG, confirm the marker exists:

```bash
grep "chart-plot-area" <project_path>/svg_output/<current_page>.svg
```

> All chart templates in `templates/charts/` include this marker as a reference. If you are drawing a chart and the marker is absent, you have a bug.
- **Technical specs**: see [shared-standards.md](shared-standards.md) for SVG/PPT constraints
- **Anti-Collision & Text Overflow Prevention**:
  - **Single-line overflow**: Never let a long subtitle or description run off the right edge (x > 1200). Break it into multiple `<tspan>` lines automatically.
  - **Card/Badge squeeze**: When placing text in fixed-width cards or node boxes, adjust the text size or use `<tspan>` wrapping to ensure the text fits within the shape boundaries.
  - **Horizontal overlap**: Keep X-coordinates of adjacent labels or large metrics spaced appropriately so their bounds do not intersect.
  - **Vertical obstruction**: Ensure adequate Y-padding between icons/badges and their text labels. Prevent edge/connector labels from overlapping the lines they label.
  - **Table/Grid strictness**: For multi-column layouts, use exactly identical X-coordinates for elements in the same column to prevent jagged alignment and resulting collisions.
- **Card containers — use the documented patterns**: when a content page needs section cards (4 quadrants, parallel aspects, capability blocks, info cards), use the patterns codified in [`templates/charts/CHART_STYLE_GUIDE.md`](../templates/charts/CHART_STYLE_GUIDE.md) §11 — half-rounded section tab (§11.1), nested card border without stroke (§11.2), card-grid skeletons (§11.3), diagonal dashed connector for cross-quadrant relationships (§11.5), ground-anchor ellipse as a non-filter depth marker (§11.6), bidirectional interaction arrows for paired protocols (§11.7). Do not reinvent the "tinted full-rounded rect + white cover-rect to hide the bottom corners" hack; it survives in older templates but breaks SVG→PPTX color editing. Reference templates: [`labeled_card.svg`](../templates/charts/labeled_card.svg), [`quadrant_text_bullets.svg`](../templates/charts/quadrant_text_bullets.svg), [`kpi_cards.svg`](../templates/charts/kpi_cards.svg), [`matrix_2x2.svg`](../templates/charts/matrix_2x2.svg), [`team_roster.svg`](../templates/charts/team_roster.svg), [`client_server_flow.svg`](../templates/charts/client_server_flow.svg).

- **TOC / agenda page — avoid the three-equal-column card grid**: the default "3 identical boxes, each with a big number + title" is the weakest possible TOC design — equal visual weight on all items, no typographic energy, reads as a navigation widget rather than a designed spread. Use it only when the TOC items carry very different text lengths that genuinely need bounding. Preferred alternatives:

  | Alternative | How it works |
  |---|---|
  | **Typographic list** | Large chapter number (72–88px) in `primary` on the left, chapter title in body size to the right, separated by a thin horizontal rule extending to a variable width; items stack with generous vertical rhythm; no card boxes at all |
  | **Number-as-atmospheric-texture** | Enormous number (120–160px) rendered in `primary` at 0.06–0.10 opacity as background texture behind each item area; legible chapter title and sub-line float over it; no bounding rect needed |
  | **Staggered horizontal flow** | Items placed at deliberately different vertical positions (e.g., top-third / mid / bottom-third) with a thin connecting horizontal line or dashed trail; chapter title + number only, no card border |
  | **Left-rail numbered list** | A vertical colored rail on the left edge; chapter number at 60–72px to the left of the rail; title and one-line description to the right; items separated by a hairline rule or whitespace only |

  When preserve_master is true, TOC items should float directly on the master — no outer wrapper card, no dark bounding rectangle. The master's dark background already makes light text readable.
- **Reference — prefer semantic shapes over preset stacks (not a constraint)**: when a slide needs to express "ascending / converging / breaking through / stacking" — i.e., a relationship that goes beyond a generic arrow — prefer a single custom `<polygon>` or `<path>` that encodes the semantics geometrically, rather than stacking multiple preset arrows. A converging-tip path or a podium polygon reads faster than three arrows pointing at a label. Examples of this technique appear in many imported corporate decks; see `projects/01_template_import/svg_output/slide_01.svg` shape-158 for a reference (gradient-filled inward-pointing arrow). Do not codify these as templates — they are page-specific; the rule is just "consider polygon before stacking presets."
- **Reference — visual depth through restraint (not a constraint)**: layered depth comes from rhythm (flat vs lifted, dense vs spacious), not from shadows everywhere. Shadow typically suits 2-3 genuinely floating elements per page (cards on photos, primary CTA, overlays); keep peer-grid cards, dividers, body containers flat. Reach for typography weight, spacing, accent bars, subtle tints **before** shadow. Full rules in shared-standards.md §6.

### SVG File Naming Convention

Format: `<NN>_<page_name>.svg` (two-digit number from 01; name matches the deck's language and the page title in the Design Spec).

Examples: `01_封面.svg` / `02_目录.svg` / `03_核心优势.svg`; `01_cover.svg` / `02_agenda.svg` / `03_key_benefits.svg`.

---

## 4. Icon Usage

Strategist chooses the library and inventory; Executor only implements. Library details and one-library rule: [`../templates/icons/README.md`](../templates/icons/README.md). This section defines placeholder syntax.

> **Resolution is project-first.** Strategist copied the chosen icons into `<project_path>/icons/<lib>/` (via `icon_sync.py`); `finalize_svg.py embed-icons` embeds from there, falling back to the global library per-icon. **Custom icons**: drop an `.svg` into `<project_path>/icons/<lib>/` (any `<lib>`, e.g. `custom/`) and reference it as `data-icon="<lib>/<name>"` — it embeds like any other. Reference only icons in the `spec_lock.md` inventory.

**Built-in icons — Placeholder method (recommended)**:

```xml
<!-- chunk-filled (straight-line geometry, sharp corners, structured) -->
<use data-icon="chunk-filled/home" x="100" y="200" width="48" height="48" fill="#005587"/>

<!-- tabler-filled (bezier-curve forms, smooth & rounded contours) -->
<use data-icon="tabler-filled/home" x="100" y="200" width="48" height="48" fill="#005587"/>

<!-- tabler-outline (light, line-art style — screen-only decks) -->
<use data-icon="tabler-outline/home" x="100" y="200" width="48" height="48" fill="#005587"/>

<!-- phosphor-duotone (single color + 20% backplate — soft depth without solid weight) -->
<use data-icon="phosphor-duotone/house" x="100" y="200" width="48" height="48" fill="#005587"/>

<!-- simple-icons (brand logos — used alongside the deck's primary library, only for real company/product marks) -->
<use data-icon="simple-icons/github" x="100" y="200" width="48" height="48" fill="#181717"/>

<!-- tabler-outline with thin / bold stroke (stroke-style libraries only) -->
<use data-icon="tabler-outline/home" x="100" y="200" width="48" height="48" fill="#005587" stroke-width="1.5"/>
<use data-icon="tabler-outline/home" x="100" y="200" width="48" height="48" fill="#005587" stroke-width="3"/>
```

> ⚠️ **Color**: ALWAYS use `fill="#HEX"` on `<use data-icon="...">`. NEVER use `stroke` or `fill="none"`, even for stroke-style libraries.
>
> **stroke-width** (stroke-style libraries only, currently `tabler-outline`): allowed values `{1.5, 2, 3}`. If `spec_lock.md icons.stroke_width` is declared, all placeholders MUST use that value deck-wide. Default `2` if absent (legacy). Ignored on non-stroke libraries.
>
> Icons are auto-embedded by `finalize_svg.py` — no need to run `embed_icons.py` manually.

**Searching for icons** — use terminal, zero token cost:
```bash
ls skills/ppt-master-plus/templates/icons/chunk-filled/ | grep home
ls skills/ppt-master-plus/templates/icons/tabler-filled/ | grep home
ls skills/ppt-master-plus/templates/icons/tabler-outline/ | grep chart
ls skills/ppt-master-plus/templates/icons/phosphor-duotone/ | grep house
ls skills/ppt-master-plus/templates/icons/simple-icons/ | grep github
```

**Abstract concept → icon name** (names for `chunk-filled`; tabler libraries use their own equivalents — verify with `ls | grep`):

| Concept | chunk-filled | tabler-filled / tabler-outline |
|---------|-------|-------------------------------|
| Growth / Increase | `arrow-trend-up` | same |
| Decline / Decrease | `arrow-trend-down` | same |
| Success / Complete | `circle-checkmark` | `circle-check` |
| Warning / Risk | `triangle-exclamation` | `alert-triangle` |
| Innovation / Idea | `lightbulb` | `bulb` |
| Strategy / Goal | `target` | same |
| Efficiency / Speed | `bolt` | same |
| Collaboration / Team | `users` | same |
| Settings / Config | `cog` | `settings` |
| Security / Trust | `shield` | same |
| Money / Finance | `dollar` | `currency-dollar` |
| Time / Deadline | `clock` | same |
| Location / Region | `map-pin` | same |
| Communication | `comment` | `message` |
| Analysis / Data | `chart-bar` | same |
| Process / Flow | `arrows-rotate-clockwise` | `refresh` |
| Global / World | `globe` | `world` |
| Excellence / Award | `star` | same |
| Expand / Scale | `maximize` | same |
| Problem / Issue | `bug` | same |

> For self-evident names (home, user, file, search, arrow, etc.) — just `grep chunk-filled/` directly without consulting the table.

> ⚠️ **Icon validation**: only use icons from the Design Spec's approved inventory. Verify each via `ls | grep` before use. Mixing libraries within one deck is FORBIDDEN.

---

## 5. Visualization Reference

Chart SVGs referenced in **VII. Visualization Reference List** are loaded once via the §1.0 batch read. This section governs adaptation only.

**Hard rule**: adapt the loaded chart SVG; do not improvise from memory and do not replicate verbatim. Apply project colors, typography, content; preserve visualization type.

**Adaptation rules**:
- **Preserve**: visualization type (bar/line/pie/timeline/process/framework…) as specified
- **Adapt**: data, labels, colors (project scheme), dimensions
- **Freely adjust**: composition, axis ranges, grid, legend, spacing, decoration — as long as the chart stays accurate and readable
- **Forbidden**: changing visualization type without spec justification; omitting data points or structural elements from the outline

> Templates: `templates/charts/` (70 types). Index: `templates/charts/charts_index.json`

### 5.1 Chart Coordinate Calibration

Coordinate calibration runs as a **standalone post-generation workflow**, not inside the executor pipeline. After SVG generation completes, if the deck contains data charts, run `verify-charts` Stage(../workflows/stages/verify-charts.md) before post-processing.

The executor's only obligation here is upstream: embed the `<!-- chart-plot-area ... -->` marker on every chart page during initial draft (§3.1). Verify-charts enumerates chart pages from `design_spec.md §VII` (authoritative deck plan) and uses the marker to feed `svg_position_calculator.py`.

> Do NOT run `svg_position_calculator.py` during the initial draft. The calculator calibrates already-generated SVGs against their declared plot areas; running it before the SVG exists has nothing to compare against.

---

## 6. Image Handling

Handle images by their status in the Design Spec's Image Resource List. Status enum and lifecycle: [`svg-image-embedding.md`](svg-image-embedding.md).

| Status | Source | Handling |
|--------|--------|----------|
| **Existing** | User-provided | Reference images directly from `../images/` directory |
| **Generated** | Generated by Image_Generator | Reference images directly from `../images/` directory |
| **Sourced** | Web-acquired by Image_Searcher | Reference from `../images/`. **Read [`image_sources.json`](image-searcher.md) to decide attribution** — see §6.1 below. |
| **Rendered** | Deterministic formula PNG | Reference from `../images/`; use `preserveAspectRatio="xMidYMid meet"` |
| **Needs-Manual** | Acquisition failed and file is absent | Use dashed border placeholder unless the expected file exists |
| **Placeholder** | Not yet prepared | Use dashed border placeholder |

**Reference syntax**: see [`svg-image-embedding.md`](svg-image-embedding.md).

**Template-bundled images**: when a template (deck / layout / brand) is applied, its bitmaps are copied into the project's `images/` alongside every other runtime image (SKILL.md Step 3). Reference them the same way — `../images/<name>` — and do **not** reproduce a template SVG's bare sibling href (e.g. `href="cover_bg.png"`): the template SVG is reference material, the rendered page lives in `svg_output/` and must point at `../images/`. Mirror templates (§1.1) are the one exception — they copy hrefs verbatim, and the exporter resolves those bare hrefs against `images/`.

**Placeholder**: Dashed border `<rect stroke-dasharray="8,4" .../>` + description text

**`no-crop` images**: when a `spec_lock.md images` entry ends with ` | no-crop`, size the container to the image's native ratio (from `analyze_images.py` or file dims) and use `preserveAspectRatio="xMidYMid meet"`. Untagged entries are croppable — default to `slice`.

**Formula images**: rows with `Acquire Via: formula` or `Type: Latex Formula` MUST be treated as no-crop even if a legacy `spec_lock.md` forgot the flag. Use the dimensions from `design_spec.md §VIII`, `analysis/image_analysis.csv`, or `images/formula_manifest.json`; do not normalize all formulas to one height unless the spec explicitly states that layout choice.

### 6.1 Inline Attribution for Sourced Images (web path)

Whenever the slide uses an image with `Status: Sourced`, look up the corresponding entry in `project/images/image_sources.json` and act on `license_tier`:

| `license_tier` | Action on this slide |
|---|---|
| `no-attribution` | Embed the `<image>` element only. **No credit element needed.** |
| `attribution-required` | Embed the `<image>` element **plus** a small inline `<text>` credit element per the visual spec in [image-searcher.md §7](./image-searcher.md). |

The credit text is **not** rendered by post-processing or export — it must be present in the SVG you produce. The shape of the credit element (size, position, color, multi-image source line, hero gradient overlay) is specified in [image-searcher.md §7](./image-searcher.md). Do not invent a different style.

Use `attribution_text` from the manifest entry as the **starting point**, then compress for the small-text constraint (drop URL, drop filename, keep "via Provider / License"). For CC0/PD images that landed in the `attribution-required` tier only because of upstream metadata quirks (rare), credits are still safe to render.

`svg_quality_checker.py` treats missing CC BY / CC BY-SA inline attribution as an **error**. Fix the offending SVG before post-processing.

**The manifest is the single source of truth for credits.** Do not duplicate license info into speaker notes or any other artifact.

---

## 7. Font Usage

Source of truth: `spec_lock.md typography`. Use `font_family` as default; override per role with `title_family` / `body_family` / `emphasis_family` / `code_family` if declared. LaTeX formulas that Strategist rendered are PNG images, not a `code_family` text role.

If `spec_lock.md` is absent, consult [`strategist.md`](strategist.md) §g — do not invent a stack.

**Hard rule**: every SVG `font-family` stack MUST end with a pre-installed family (Microsoft YaHei / SimHei / SimSun / Arial / Calibri / Segoe UI / Times New Roman / Georgia / Consolas / Courier New / Impact / Arial Black). PPTX has no runtime fallback — missing fonts degrade to Calibri.

---

## 8. Speaker Notes Generation Framework

### Task 1. Generate Complete Speaker Notes Document

After all SVG pages are finalized, enter Logic Construction Phase and write the full notes to `notes/total.md`. Batch-writing (not per-page) lets transitions plan coherently.

**Pure spoken narration**: notes are read aloud verbatim by `notes_to_audio.py` (TTS). Write only what should be spoken. No visible markers, no labeled meta-lines, no enumerated key-point lists, no duration annotations — anything you write outside the heading will be vocalized.

**Per-page structure**: `# <number>_<page_title>` heading (the `#` heading line is the only thing stripped before TTS), pages separated by `---`. Body is 2–5 natural sentences carrying the page's core message. Page-to-page transitions live inside the opening sentence as natural prose ("接下来……" / "Having framed X, let's turn to Y") — no bracketed `[过渡]` / `[Transition]` tags.

**Concrete examples** — same shape applies to any language; just write naturally in that language.

中文 deck：

```
# 02_市场格局

在明确了行业背景之后，我们来看具体的市场格局。当前线上零售集中度持续上升，前三大平台合计份额已经达到百分之六十八，腰部玩家正在被快速挤压，留给新进入者的窗口期不超过十八个月。这意味着我们的策略必须聚焦，而不是铺开。
```

英文 deck：

```
# 02_market_landscape

Having framed the industry backdrop, let's look at the actual market landscape. Online retail concentration keeps rising — the top three platforms now hold sixty-eight percent of combined share, mid-tier players are being squeezed fast, and the window for new entrants is under eighteen months. This means our strategy has to focus, not spread.
```

> 日本語 / 한국어 / 其他语言：照搬同样的结构，用对应语言自然书写即可。

**Number readability**: TTS reads digits and symbols literally. Prefer fully-spelled forms in the language being spoken when literal pronunciation would be awkward (e.g. Chinese "百分之六十八" reads better than "68%"; "1-2分钟" reads as "一减二分钟"). Plain integers and percentages in English are fine as-is.

**Common mistakes to avoid**:
- Leaving any bracketed stage marker (`[过渡]` / `[Transition]` / `[Pause]` / `[Data]` / `[Scan Room]` / `[Interactive]` / `[Benchmark]` etc.) in the text — they will be read aloud literally.
- Adding `要点：① …` / `Key points: (1) …` / `时长：2分钟` / `Duration: 2 minutes` / `Flex: …` lines — TTS will speak "要点 一 …".
- Mixing languages within one deck's notes.

### Task 2. Split Into Per-Page Note Files

Auto-split `notes/total.md` into per-page files in `notes/`.

**Naming**: match SVG names (`01_cover.svg` → `notes/01_cover.md`); `slide01.md` also supported (legacy).

---

## 9. Next Steps After Completion

> **Auto-continuation**: After Visual Construction Phase (all SVG pages) and Logic Construction Phase (all notes) are complete, the Executor proceeds directly to the post-processing pipeline.

**Post-processing & Export** (same canonical pipeline as [shared-standards.md §5](shared-standards.md)):

**Faithful beautify + `preserve_master=true` background rule**: these rules apply only when `spec_lock.md` explicitly sets `preserve_master: true`. Generic PPTX beautification through the main pipeline must not set this flag and should generate complete slide backgrounds and visual systems normally. Source master/layout backgrounds and fixed chrome already come from the base PPTX. Generated SVG pages must not add a page-covering background: no `<g id="background">`, full-canvas `<rect>`, full-canvas `<image>`, page-wide overlay, background grid, watermark, duplicated logo/footer/header, or other master-like chrome. Author only slide-local redesigned content and bounded local panels. A live preview may look sparse because it does not show the preserved PowerPoint master; the exported PPTX is the source of truth for the background.

**Full-canvas wrapper card ban**: a single `<rect>` spanning more than 80% of both canvas width AND canvas height simultaneously is a page-covering background regardless of its rounded corners (`rx`), stroke, or fill-opacity. This is the most common accidental violation — the Executor draws a large "card container" covering 85–95% of the canvas to hold all slide content, which is functionally a background. Do NOT draw one outer card that wraps everything; instead, place each content group (title band, diagram, callout panel, footer) as a directly-placed standalone element. When `spec_lock.colors.bg` is a dark color (HEX value implies near-black, e.g. `#0A0E17`, `#111827`, `#000000`, `#0D1117`), the preserved master already supplies dark contrast for light text — no large dark wrapper is needed for legibility.

This rule extends to **chart-level elements**: chart plot-area backgrounds, chart panel wrappers, legend boxes, and any bounding rectangle around a visualization must also default to `fill="none"`. A conditional local panel with low-opacity `spec_lock.colors.secondary_bg` (≤ 0.15) is permitted when contrast demands it — see the chart override rule above for the exact conditions. Axis lines and gridlines use `spec_lock.colors.body_text` at opacity 0.15–0.20; series colors come from `spec_lock.colors`. No solid opaque white, gray, or off-palette fill anywhere inside a chart when `preserve_master=true`.

This rule also extends to **content panels** — section cards, architecture lane boxes, feature panels, module wrappers, and any bounded container that organizes slide content: these must use `fill-opacity` in the range **0.85–0.96** on `secondary_bg` fills rather than a solid opaque value. A solid-filled content panel on a preserved master creates a hard opaque island that visually disconnects from the master's color field. With fill-opacity 0.9, the panel is still clearly present and readable but integrates with the master layer behind it. Exception: a panel used as a legibility bridge directly over a high-contrast image area (e.g., a dark label box over a photo) may be solid — but only if bounded tightly to its content, not covering the full slide or a large blank zone.

```bash
# 1. Split speaker notes
python3 scripts/total_md_split.py <project_path>

# 2. SVG post-processing (auto-embed icons, images, etc.)
python3 scripts/finalize_svg.py <project_path>

# 3. Export PPTX
python3 scripts/svg_to_pptx.py <project_path>
# Beautify with confirmed preserve_master=true:
# python3 scripts/svg_to_pptx.py <project_path> --base-pptx <project_path>/sources/<source.pptx>
# Output (default-flow mode):
#   exports/<project_name>_<timestamp>.pptx           ← native pptx (canonical output)
#   backup/<timestamp>/svg_output/                    ← Executor SVG source backup (always written)
#
# Add --svg-snapshot to additionally emit:
#   exports/<project_name>_<timestamp>_svg.pptx      ← SVG snapshot pptx (sibling of native pptx)
```
