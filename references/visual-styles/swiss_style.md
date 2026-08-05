# Visual Style: swiss_style

Strict Swiss Internationalism discipline. Strict grid alignment, sharp geometries, aggressive whitespace, high typographic weight contrast, and near-zero graphic decoration.

---

## 1. Shape & Decoration

- **Shape Language**: Strictly straight-angled rectangles and true circles. Corner radius `rx="0"` (and `ry="0"`) on all elements. No rounded corners.
- **Decoration**: No gradients, no drop shadows, no glow overlays. The layout structure and grid spacing themselves act as the design decoration.
- **Rules & Borders**: Use only 1px hairline divider rules (`stroke-width="1"`) in neutral grey or black to separate segments.
- **Grids**: Snap all elements to a 12-column or 16-column modular grid structure. Calculate coordinates (`x`, `y`, `width`) mathematically to prevent visual layout offsets.

---

## 2. Typography Character

- **Weight Contrast**: "The larger the font, the lighter its weight; the smaller the font, the heavier its weight."
  - Large headings (>= 8vw) MUST use `font-weight: 200` (ExtraLight). Do NOT make headings bold.
  - Body text uses `font-weight: 300` or `400` (Light).
  - Kickers, captions, labels, and KPI numbers use `font-weight: 500` or `600` (Medium/SemiBold) to ensure legibility.
- **Alignment**: All text blocks must be strictly left-aligned. No centered headings except on dedicated full-screen statement cover pages (like S03 or S09).
- **Chinese Heading Sizing Tiers**: Adjust title sizes based on Chinese character lengths to prevent awkward line breaks in PPTX text boxes:
  - 1 line (<= 8 characters): `min(6.4vw, 11.2vh)`
  - 2 lines (<= 8 characters per line): `min(5.8vw, 10.2vh)`
  - 2 lines (9-12 characters per line): `min(5.2vw, 9.2vh)`
  - 3 lines or more: `min(4.6vw, 8.2vh)`
- **Line Height**: Restrict large headings to tight spacing: `letter-spacing: -0.04em`, `line-height: 0.9` or `1.0`. Keep body line height at a readable `1.4` or `1.5`.

---

## 3. Color Usage

- **Monochrome Base**: Strictly dark ink `#0A0A0A` text on a pure white `#FFFFFF` canvas background.
- **Single Accent Color**: Only allow a single high-contrast highlight accent color (e.g. Klein Blue `#0020C2` or Safety Orange `#FF6700`) from the locked color scheme.
- **Accent Application**: Accent is applied extremely sparingly (under 5% visual surface)—such as a single timeline dot, a hairline segment, or a key number.
- **Card Fills**: Standard cards use a flat grey background (`#F5F5F5` or `#EAEAEA`) without borders. Only one card in a grid is allowed to take the accent color (anti-repetition color highlight).

---

## 4. Layout & Alignment Rules

- **Margin Alignment**: All page elements (headers, grids, body blocks, page numbers) must align flush to a single left boundary (default 5vw). Never offset elements horizontally.
- **No Double Padding Stack**: Ensure the inner container of your grid does not add extra padding if the parent canvas already has a margin, preventing misaligned margins.
- **Page Rhythm Variety**: A deck of 6+ pages must use at least 4 different Swiss layout styles (S01–S22). Do not repeat the same 3-card grid on consecutive pages.

---

## 5. Image & Diagram Framing

- **Framer Rects**: All image containers must be straight-angled and flat, without border-radius or shadows.
- **Aspect Ratios**: Ensure all images conform to standard aspect ratios (e.g., 21:9 for S22 top main banners, 16:10 or 4:3 for card grids).
- **Fitting**: Use `preserveAspectRatio="xMidYMid slice"` for general illustrations and photos to crop cleanly. Use `preserveAspectRatio="xMidYMid meet"` for diagrams and UI screenshots to prevent cropping vital details.

---

## 6. Paired Image Rendering

- `minimalist-swiss` — flat, structured geometric vector graphics or schematic diagrams that match the architectural aesthetic of the slide.
