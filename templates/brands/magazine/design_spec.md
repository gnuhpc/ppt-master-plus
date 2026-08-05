---
brand_id: magazine
kind: brand
summary: Magazine & E-Ink style - warm tones, serif/sans-serif typography contrast, literary layouts
primary_color: "#262626"
---

# Magazine Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Magazine & E-Ink |
| Use Cases | Cultural observations, industry insights, independent magazine portfolios, designer portfolios, personal reflection |
| Tone | Literary, humanist, sophisticated, editorial, slow-paced |

## II. Color Scheme

Magazine style supports 5 warm-toned E-Ink theme palettes. The Strategist should pick one at confirmation tier 2 and write it to `spec_lock.colors`.

### 1. Palette Options

| Palette | background | primary | secondary | accent | secondary_accent | body_text |
|---|---|---|---|---|---|---|
| **Ink Classic** (墨水经典) | `#FBFBF9` | `#262626` | `#5C5C5C` | `#7D7D7D` | `#A3A3A3` | `#262626` |
| **Indigo Porcelain** (靛蓝瓷) | `#F7F9FC` | `#1A2F4C` | `#3D5470` | `#5A738E` | `#7C95B0` | `#1A2F4C` |
| **Forest Green** (森林墨) | `#FAFBF7` | `#1E3A27` | `#3F5C48` | `#5F7F69` | `#82A38B` | `#1E3A27` |
| **Kraft Paper** (牛皮纸) | `#F5EFE6` | `#4B3621` | `#6E553F` | `#91775E` | `#B59980` | `#4B3621` |
| **Dune** (沙丘) | `#FAF6F0` | `#3A2E2B` | `#5D4F4C` | `#81726E` | `#A69692` | `#3A2E2B` |

### 2. Element Color Assignment
- `background`: Pure paper tone background (always soft off-white, never cold `#FFFFFF`).
- `primary`: Dark charcoal or dominant ink tone for main headings and titles.
- `secondary`: Sub-headings, kickers, metadata.
- `accent`: Hairline rules, pull quotes, highlight tags.
- `body_text`: Dark charcoal/ink tone for readable body prose.

---

## III. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| title | `"Playfair Display", "Noto Serif SC", "Georgia", serif` | 700 / 600 | Literary serif voice for high-contrast titles |
| body | `"Inter", "Helvetica Neue", "Noto Sans SC", sans-serif` | 300 / 400 | Clean, highly legible sans-serif |
| meta | `"JetBrains Mono", Courier, monospace` | 400 | For page numbers, categories, act codes |

---

## IV. Voice & Tone

- **Style**: Complete-sentence paragraph prose is preferred over simple fragments or bullet lists.
- **Formality**: Authoritative, magazine editorial style.
- **Emoji**: Strictly forbidden. Use clean Lucide icons.
- **Whitespace**: Large, quiet gutters and open margins (breathing rhythm).
