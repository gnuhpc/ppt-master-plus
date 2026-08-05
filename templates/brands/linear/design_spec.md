---
brand_id: linear
kind: brand
summary: Linear brand identity - ultra-minimalist developer aesthetic, deep dark canvas, neon purple micro-glows, precision spacing.
primary_color: "#5E6AD2"
---

# Linear Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Linear |
| Use Cases | Project management updates, product roadmaps, developer tool updates, tech startups pitches, engineering metrics reports |
| Tone | High efficiency, premium, precise, sleek, futuristic |

## II. Color Scheme

Linear style supports 3 dark-themed high-contrast palettes. The Strategist should pick one and write it to `spec_lock.colors`.

### 1. Palette Options

| Palette | background | primary | secondary | accent | secondary_accent | body_text |
|---|---|---|---|---|---|---|
| **Linear Obsidian** (默认深色) | `#121214` | `#F1F1F3` | `#8A8F98` | `#5E6AD2` | `#B48AD2` | `#DFE1E5` |
| **Linear Pitch** (纯黑微光) | `#000000` | `#FFFFFF` | `#7C818A` | `#5E6AD2` | `#4DAB9A` | `#F1F1F3` |
| **Linear Gray** (中性暗灰) | `#18181B` | `#F4F4F5` | `#A1A1AA` | `#3F51B5` | `#9C27B0` | `#E4E4E7` |

### 2. Element Color Assignment
- `background`: Dark Obsidian or Pitch Black.
- `primary`: Bright white for main titles.
- `secondary`: Dull gray for secondary info, sub-labels, and page numbers.
- `accent`: Linear purple (`#5E6AD2`) for focal points, nodes, active states, and borders.
- `body_text`: Light gray for high readability on dark canvas.

---

## III. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| title | `"Inter", "Helvetica Neue", "Noto Sans SC", sans-serif` | 300 / 400 | Ultra-light sans titles for extreme precision |
| body | `"Inter", "Noto Sans SC", sans-serif` | 400 | Clean, standard sans-serif |
| meta | `"JetBrains Mono", monospace` | 400 | Code font for engineering markers |

---

## IV. Voice & Tone

- **Style**: Direct, punchy assertions, minimal lists, maximum whitespace.
- **Visuals**: Super fine borders (`stroke="#262629"`, `stroke-width="1"`), minimal border radius (`rx="4"`), subtle drop-shadows or glow gradients.
- **Micro-Animations**: Linear's visual grammar relies on subtle transitions and glowing hover highlights.
