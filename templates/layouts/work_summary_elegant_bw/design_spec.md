---
layout_id: work_summary_elegant_bw
kind: layout
summary: Monochromatic B&W work-summary; "WE LOVE WHAT WE DO" brand mark, thin gray title frame, three-dot footer signature; heavy full-bleed photography, zero color accent.
keywords: [Minimal, Monochrome, Work Summary, Photography, Open Sans, 方正小标宋简体]
canvas_format: ppt169
page_count: 7
page_types: [cover, toc, chapter, content, content, content, ending]
replication_mode: standard
---

## I Overview
Ultra-minimal monochromatic corporate presentation built around the brand phrase "WE LOVE WHAT WE DO". The entire palette is limited to near-black (`#262626`), grays, and white — no color accent ever appears. Full-bleed and diagonal-clipped photography provides visual richness. Typography mixes 方正小标宋简体 for Chinese display titles, Open Sans Bold for English labels, and 等线/Calibri Light for body. Ideal for annual work-summaries, corporate reports, and portfolio decks.

## II Color
- Primary dark `#262626` — headings, brand mark lines, three-dot footer, chapter label box
- Body gray `#808080` — body text, photo captions
- Border gray `#D9D9D9` — frame rects, diagonal line, circle strokes
- Caption gray `#A6A6A6` — secondary captions, TOC descriptions
- Near-white `#BFBFBF` — decorative placeholder text, subtitle hints
- White `#FFFFFF` — slide background, overlay rect, TOC circle fill

## III Typography
- Chinese display title: `方正小标宋简体`, `FZ XiaoBiaoSong Simplified`, SimSun, serif — 96px, letter-spacing 13.33, fill `#262626`
- English brand mark: `Open Sans`, sans-serif — 16px, letter-spacing 4, fill `#000000`
- English chapter label: `Open Sans`, sans-serif — 37.33px bold, fill `#FFFFFF` (on dark box)
- English section number: `Open Sans`, sans-serif — 184px bold, fill `#000000`
- English ending: `Open Sans`, sans-serif — 106.67px bold, letter-spacing 8, fill `#262626`
- Mixed page title: `微软雅黑`, sans-serif — 18.67px bold, fill `#262626`
- Photo list labels: `Open Sans`, sans-serif — 21.33px bold, fill `#262626`
- Body / captions: `等线`, `DengXian`, `Calibri Light`, sans-serif — 13.33–14px, fill `#808080` or `#A6A6A6`

## IV Signature Elements
- **Brand mark bar**: `"WE LOVE WHAT WE DO"` Open Sans 16px letter-spacing:4 at x=640 y=101.02; flanked by two 43px `#000000` hairlines at y=97.17 (left: x=461.09→503.76; right: x=771.39→814.06). Present on cover and ending only.
- **Title frame**: `<rect x="347.15" y="249.13" width="585.7" height="186.94" fill="none" stroke="#D9D9D9" stroke-width="1"/>` — frames the Chinese 96px title on cover and the 106.67px ending message.
- **Three-dot signature**: three r=7.27 filled circles at cx=611.39/640/668.61, cy=664.73, fill=`#262626`. Present on cover and ending only.
- **Staircase TOC**: four white circles (r=41.47, stroke `#D9D9D9`) with 64px Open Sans numerals; trajectory from (357.9, 237.57) to (698.02, 586.45); step ≈ (110, 117)px per item.
- **Triangular photo split (TOC)**: `clipPath` with `<polygon points="0,0 0,720 720,720"/>` plus a 45° `#D9D9D9` diagonal line (x1=102.79 y1=-6.79 → x2=837.82 y2=728.24).
- **Rectangular photo split (chapter)**: left image placeholder 642.91×720; right white zone with dark label box x=705.39 y=136.73 w=248.8 h=104.73 fill=`#262626`.
- **Section frame (03a)**: `<rect x="496.51" y="182.11" width="286.97" height="306.21" stroke="#D9D9D9"/>` with L-corner guides — vertical x=791.93 y=325.14→497.62; horizontal x=528.03→791.93 y=497.62.

## V Page Roster
| File | Type | Key Placeholders |
|------|------|-----------------|
| `01_cover.svg` | cover | `{{TITLE}}`, `{{SUBTITLE}}`, `{{AUTHOR}}`, `{{DATE}}` |
| `02_toc.svg` | toc | `{{TOC_ITEM_N_TITLE}}`, `{{TOC_ITEM_N_DESC}}` (N=1–4) |
| `02_chapter.svg` | chapter | `{{CHAPTER_TITLE}}`, `{{CHAPTER_DESC}}` |
| `03a_content_section.svg` | content | `{{CHAPTER_NUM}}`, `{{PAGE_TITLE}}`, `{{CONTENT_AREA}}` |
| `03b_content_grid.svg` | content | `{{PAGE_TITLE}}`, `{{SUBTITLE}}`, `{{CONTENT_AREA}}` |
| `03c_content_photo_list.svg` | content | `{{CATEGORY_N}}`, `{{CONTENT_N}}` (N=1–4) |
| `04_ending.svg` | ending | `{{THANK_YOU}}`, `{{CONTACT_INFO}}` |
