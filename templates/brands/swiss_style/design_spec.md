---
brand_id: swiss_style
kind: brand
summary: Swiss Internationalism style - Klein Blue high contrast accent, strict grid locking, typography weight contrasts
primary_color: "#0020C2"
---

# Swiss Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Swiss Internationalism |
| Use Cases | Technical presentations, IT architectures, engineering plans, design reviews, corporate briefs |
| Tone | Objective, precise, grid-locked, information-driven, architectural |

## II. Color Scheme

Swiss style relies on a single dominant accent functional color. The paper background is always white `#FFFFFF`, and the text ink is near-black `#0A0A0A`.

### 1. Palette Options

| Palette | background | primary | secondary | accent | secondary_accent | body_text |
|---|---|---|---|---|---|---|
| **Klein Blue** (默认) | `#FFFFFF` | `#0A0A0A` | `#4B4B4B` | `#0020C2` | `#E0E4FC` | `#0A0A0A` |
| **Safety Orange** | `#FFFFFF` | `#0A0A0A` | `#4B4B4B` | `#FF6700` | `#FFF0E6` | `#0A0A0A` |
| **Lime Green** | `#FFFFFF` | `#0A0A0A` | `#4B4B4B` | `#39FF14` | `#EBFEE8` | `#0A0A0A` |
| **Lemon Yellow** | `#FFFFFF` | `#0A0A0A` | `#4B4B4B` | `#FFEA00` | `#FFFEE6` | `#0A0A0A` |

### 2. Element Color Assignment
- `background`: Strictly white `#FFFFFF` (or light grey `#F5F5F5` for card-fill containers).
- `primary`: Strictly ink-black `#0A0A0A` for text and layout shapes.
- `accent`: The single functional accent color chosen from above (e.g. Klein Blue `#0020C2`). Used extremely sparingly (under 5% visual area) for key highlights.
- `secondary_accent`: Highly transparent tint of the accent color for card background fills.

---

## III. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| title | `"Inter", "Helvetica Neue", "Arial", "Noto Sans SC", sans-serif` | 200 / 300 | ExtraLight titles for massive typographic size contrast |
| body | `"Inter", "Helvetica Neue", "Arial", "Noto Sans SC", sans-serif` | 300 / 400 | Light weights for crisp, modern layout readability |
| meta | `"JetBrains Mono", "Courier New", monospace` | 500 / 600 | Monospaced figures, data cards, stats labels |

---

## IV. Design Guidelines

- **Angles**: Straight edges only. Border radius `rx="0"` (and `ry="0"`) on all elements. No rounded corners.
- **Elevation**: Strictly flat 2D layout. No shadows (`box-shadow`), no gradients, no texture.
- **Grids**: All items align to a virtual 12-column or 16-column modular grid with explicit borders.
- **Hierarchy**: Extreme size ratios between headers (very large) and body text (small).
- **Legibility**: Follow the rule "the smaller the text, the heavier its weight" (e.g., body 400, meta/caption 500-600).
