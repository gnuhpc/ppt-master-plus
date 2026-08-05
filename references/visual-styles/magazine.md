# Visual Style: magazine

Magazine-grade editorial layout. Warm paper backgrounds, thin rules, a strong serif/sans-serif interplay, and balanced vertical rhythms.

---

## 1. Shape & Decoration

- **Shape Language**: Rectilinear cards and panels. Corner radius `rx="2"` or `rx="4"` (maximum) is permitted to give an organic paper-cutting feel.
- **Decoration**: Focus on typographic structure rather than graphics. Thin rules (`stroke-width="1"` or `1.5`) and column dividers represent margins and structure.
- **Whitespace**: Comfortable but dense. Keep quiet page boundaries (at least 6% page margin) to give an independent magazine aesthetic.
- **Backgrounds**: Utilize soft vector organic backgrounds (like subtle waves, ink textures, or contour curves in `#FAF6F0` or `#F5EFE6` tones). Do NOT use generic white `#FFFFFF`.

---

## 2. Typography Character

- **Interplay**: Bold, large serif headings (e.g. Playfair Display, Noto Serif SC) contrasted against clean, lightweight sans-serif body text (e.g. Inter).
- **Kickers / Eyebrows**: Every page should use a small, monospaced metadata kicker above the title (e.g. "SECTION III // PROCESS") for a curated editorial look.
- **Prose-First**: Preference is given to full-sentence prose and structured quotes rather than brief bullet points.
- **Sizing Hierarchy**:
  - Main Heading: `font-size: min(6.8vw, 12vh)` (Serif)
  - Kickers / Labels: `font-size: min(1.6vw, 3vh)`, monospaced uppercase
  - Body Prose: `font-size: min(2.2vw, 4vh)`, sans-serif with comfortable line height (`line-height="1.5"`)

---

## 3. Color Usage

- **Background Field**: Soft warm cream, sand, or light grey (from the locked brand palette).
- **Text & Structure**: Charcoal black (`#262626`) or deep brown (`#3A2E2B`).
- **Accent**: A single muted color (such as Forest Green or Indigo) used only for kickers, hairline rules, or key words. Never splash color randomly.

---

## 4. Texture & Elevation

- **Flat to Low-raised**: Content segments are divided by thin rules and whitespace. Avoid heavy drop-shadows or glow gradients.
- **Image Border**: Wrap images inside a thin border box with a caption underneath to mimic a physical printed photograph frame.
- **Gradients**: Only linear, soft, two-color ink transitions are permitted in cards.

---

## 5. Paired Image Rendering

- `editorial` or `watercolor` — illustrations resembling editorial ink sketches or high-end magazine photographs.
