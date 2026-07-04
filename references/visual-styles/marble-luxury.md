# Visual style: marble-luxury

Stone-material elegance. Marble-texture panels anchor the layout; high-contrast CJK display weights headline; gold or platinum rules divide space. For high-end real estate, luxury brand, premium consulting, board-level corporate.

---

## 1. Shape & decoration

- Shape language: sharp rectangles and ruled lines; no rounded corners (`rx="0"`). Thin hairline rules (1–1.5 px) as section dividers and frame accents.
- Decoration: one marble-texture panel per page maximum — cover strip, sidebar column, or full bleed on title pages. Body pages: near-decoration-free; the texture zone does the work.
- Whitespace: generous lateral margins; the marble zone bleeds to one edge while the opposite field stays pure white/light gray.
- Layout is bilateral: texture on one side, typeset content on the other. Grid is implicit, not decorative.

## 2. Typography character

- High weight contrast: ultra-bold display CJK (≥900 weight, or an expressive display face) for headings, ultra-light or thin for supporting text and labels.
- Latin: a geometric sans at the same weight extremes, or a refined transitional serif for body — never a generic office face.
- Sizing is dramatic: headline 2–3× the body baseline; the large character reads as a graphic element.

> Families are chosen at confirmation `g`; this style asks for the **bold-vs-thin CJK contrast** character — not a specific font.

## 3. Using the deck's colors

- Color family is disciplined and near-neutral: high-key gray scale (white → warm mid-gray → charcoal) with one metallic accent (gold, champagne, or cool platinum) for rules, folios, and key figures.
- The marble texture is the "color" — let it carry warmth or coolness; the typeset field stays achromatic.
- Accent appears as thin rules, number labels, and single-word callout highlights — never as filled blocks or backgrounds.

> HEX values come from confirmation `e`; this style governs the near-neutral palette with metallic rule — it names no colors.

## 4. Texture / elevation

- One material texture per deck: the marble or stone panel. All other surfaces: completely flat, no gradient, no shadow.
- The texture is scanned or rendered stone — not a CSS gradient approximation. Embed as an image reference in the SVG.
- Zero elevation on cards: no drop shadows anywhere. Depth comes from the texture contrast alone.

## 5. Paired image-rendering

`corporate-photo` — editorial photography (architecture, object, detail shots) matches the material luxury register. For illustrations, `flat` with the deck's near-neutral palette.
