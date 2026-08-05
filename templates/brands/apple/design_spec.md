---
brand_id: apple
kind: brand
summary: Apple brand identity - extreme whitespace, cinematic product layouts, San Francisco style typography, clean and premium minimalism.
primary_color: "#000000"
---

# Apple Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Apple |
| Use Cases | Product keynotes, hardware launches, developer conferences (WWDC style), executive briefs, high-end consumer updates |
| Tone | Cinematic, dramatic, premium, clean, minimal, authoritative |

## II. Color Scheme

Apple style supports 3 main color palette configurations (pure light, WWDC dark, and premium gray). The Strategist should pick one and write it to `spec_lock.colors`.

### 1. Palette Options

| Palette | background | primary | secondary | accent | secondary_accent | body_text |
|---|---|---|---|---|---|---|
| **Apple Light** (默认白色) | `#FFFFFF` | `#000000` | `#515154` | `#86868B` | `#0071E3` | `#1D1D1F` |
| **Apple WWDC** (暗黑纪元) | `#000000` | `#FFFFFF` | `#A1A1A6` | `#86868B` | `#0071E3` | `#F5F5F7` |
| **Apple SpaceGray** (太空灰) | `#1D1D1F` | `#F5F5F7` | `#86868B` | `#0071E3` | `#FF453A` | `#E8E8ED` |

### 2. Element Color Assignment
- `background`: Pure solid white (`#FFFFFF`) or pure deep pitch black (`#000000`).
- `primary`: Solid black or white for high contrast headings.
- `secondary`: Dull gray for descriptive text and captions.
- `accent`: Link Blue (`#0071E3`) or Product Red (`#FF453A`) for highlight anchors.
- `body_text`: Highly readable primary text tone.

---

## III. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| title | `"SF Pro Display", "Helvetica Neue", "Noto Sans SC", sans-serif` | 600 / 700 / 300 | Display sans with tight tracking |
| body | `"SF Pro Text", "Helvetica Neue", "Noto Sans SC", sans-serif` | 400 | Extremely readable body sans |
| meta | `"SF Mono", Consolas, monospace` | 400 | Minimalist monospaced details |

---

## IV. Voice & Tone

- **Style**: Extreme brevity, "one statement per slide", large text sizes, zero bullets.
- **Visuals**: Full-bleed images (`fit="cover"`), extreme margins and whitespace, thin line dividers, no cards or shadow decorations.
- **Rhythm**: Dramatic, cinematic pacing (high variation between light text-only pages and dark image-only pages).
