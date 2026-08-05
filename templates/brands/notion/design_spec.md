---
brand_id: notion
kind: brand
summary: Notion brand identity - warm paper tones, serif headings, outline card grids, minimalist Knowledge Management aesthetic.
primary_color: "#37352F"
---

# Notion Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Notion |
| Use Cases | Knowledge base sharing, wiki portals, educational tutorials, internal company wikis, project documentation |
| Tone | Intellectual, structured, warm, cozy, minimal, clean |

## II. Color Scheme

Notion style supports 4 warm paper tone palettes. The Strategist should pick one and write it to `spec_lock.colors`.

### 1. Palette Options

| Palette | background | primary | secondary | accent | secondary_accent | body_text |
|---|---|---|---|---|---|---|
| **Notion Soft** (默认暖白) | `#F7F6F3` | `#37352F` | `#787774` | `#0F7BC4` | `#DF5B5B` | `#37352F` |
| **Notion Pure** (纯净白) | `#FFFFFF` | `#191711` | `#5F5E5B` | `#E2B237` | `#0F7BC4` | `#191711` |
| **Notion Sand** (暖沙黄) | `#FAF8F5` | `#37352F` | `#7C7B77` | `#E16957` | `#4DAB9A` | `#37352F` |
| **Notion Dark** (暗黑模式) | `#191919` | `#E3E3E2` | `#9B9A97` | `#2EAADC` | `#DF5B5B` | `#E3E3E2` |

### 2. Element Color Assignment
- `background`: Notion warm paper tone background.
- `primary`: Notion main black or dark ink for main headings and titles.
- `secondary`: Sub-headings, metadata, side column labels.
- `accent`: Highlights, inline tags, block quotes background tint.
- `body_text`: Dark charcoal tone for readable body prose.

---

## III. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| title | `"Georgia", "Noto Serif SC", "Cambria", serif` | 700 / 600 | Elegant serif headings |
| body | `"Inter", "Segoe UI", "Noto Sans SC", sans-serif` | 400 | Clean, default system sans-serif |
| meta | `"JetBrains Mono", monospace` | 400 | For code snippets, tags, dates |

---

## IV. Voice & Tone

- **Style**: Clear, structured paragraph prose, hierarchy of Headings (H1, H2, H3), and bullet/numbered lists.
- **Visuals**: Clean card borders (`stroke="#E3E3E2"`, `stroke-width="1"`), rounded corners (`rx="3"`), zero shadow.
- **Emoji**: Minimalist, clean emoji labels allowed (e.g. icon slots can use standard Notion-style icons or simple SVGs).
