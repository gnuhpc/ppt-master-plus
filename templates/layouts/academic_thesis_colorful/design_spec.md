---
layout_id: academic_thesis_colorful
kind: layout
summary: Four-color academic thesis defense; Chinese calligraphic TOC header, per-chapter accent ovals, persistent left-edge colored circle tabs, dashed boundary lines on chapter slides.
keywords: [Academic, Thesis, Chinese Font, Colorful, Four-accent, Graduate, 华文隶书]
canvas_format: ppt169
page_count: 5
page_types: [cover, toc, chapter, content, ending]
replication_mode: standard
---

## I Overview
Scholarly presentation template combining 华文隶书 calligraphy with bold four-color chapter accents. Yellow/Red/Blue/Green are strictly mapped to chapters 1–4 throughout the deck. Four colored circles at cx≈−54 (partially off-canvas) form a persistent left-edge navigation strip on all non-cover slides. The chapter slide uses double dashed boundary lines as its only decoration. Content uses open-top oval paths in chapter accent color. Organic vector art (flowers, clouds) decorates cover and ending pages as simplified geometric motifs. Suited for graduate thesis defenses, academic conferences, and research reports.

## II Color
- Yellow ch1 `#F7B63E` — Chapter 1 / TOC item 1 / top-left oval / sidebar circle 1
- Red ch2 `#FF3E3E` — Chapter 2 / TOC item 2 / top-right oval / sidebar circle 2
- Blue ch3 `#76AADB` — Chapter 3 / TOC item 3 / bottom-left oval / sidebar circle 3
- Green ch4 `#70AD47` — Chapter 4 / TOC item 4 / bottom-right oval / sidebar circle 4
- Dark text `#404040` — main body text, page titles, chapter title
- Near-black `#2E2E2E` — ending headline, short rule
- Divider gray `#D9D9D9` — chapter dashed lines, ending horizontal rule
- Connector gray `#595959` — curved double-arrow connectors

## III Typography
- TOC header: `华文隶书`, `STLiti`, serif — 72px bold (目录), 128px bold (contents), `#2E2E2E`
- TOC items: `方正静蕾简体`, sans-serif — 37.33px, `#404040`
- Chapter title: `微软雅黑`, `Microsoft YaHei`, sans-serif — 96px, `#404040`
- Page title: `幼圆`, `YouYuan`, sans-serif — 64px bold, `#404040`
- Box titles (text zones): `微软雅黑`, sans-serif — 32px bold, per-accent color
- Box body: `微软雅黑`, sans-serif — 18.67px, `#262626`
- Oval labels: `微软雅黑`, sans-serif — 32px bold, per-accent color
- Ending headline: `微软雅黑`, sans-serif — 72px bold, `#2E2E2E`
- Attribution: `幼圆`, sans-serif — 26.67px bold, `#2E2E2E`

## IV Signature Elements
- **Sidebar circles**: Yellow `<ellipse cx="-51.59" cy="215.59" rx="40.19" ry="40.19" fill="#F7B63E"/>`, Red `<ellipse cx="-53.76" cy="295.6" rx="40.19" fill="#FF3E3E"/>`, Blue `<ellipse cx="-53.76" cy="375.64" rx="40.19" fill="#76AADB"/>`, Green `<ellipse cx="-53.76" cy="455.32" rx="40.19" fill="#70AD47"/>`. Present on all non-cover slides.
- **Chapter dashed boundary lines**: stroke-dasharray="8 4", stroke-width=2.667, stroke=`#262626` — top: x1=299.84 y1=307.05 x2=990.52 y2=310.96; bottom: x1=299.84 y1=486.95 x2=990.52 y2=490.86.
- **Oval frames**: open-top curved paths, stroke-width=2.667. Yellow: `M 407.96 216.79 C 465.93 213.69 544.33 205.12 550.64 220.63 C 556.96 236.14 563.98 350.6 551.83 363.7 C 539.68 376.8 403.36 376.35 398.24 353.09 C 395.33 319.05 393.97 265.6 396.18 234.74`. Red/Blue/Green follow same shape offset by (325.34, 0) / (0, 293.87) / (325.34, 293.87).
- **Curved double-arrow connectors**: curved arcs with markerStart+markerEnd (chevron `"M 0 0 L 10 5 L 0 10"` fill=`#595959`), stroke=`#595959`, stroke-width=2.667, round linecap.
- **TOC flame decorations**: four stylized colored flame paths at right edge x≈1140–1250 (one per chapter row), followed by dashed wavy connectors (stroke-dasharray="4 4") linking them to text items.
- **Ending horizontal rule**: `<line x1="304.78" y1="436.96" x2="1011.73" y2="436.96" stroke-width="3.667" stroke="#D9D9D9"/>`.
- **Ending short rule**: `<line x1="594.64" y1="616.43" x2="670.23" y2="616.43" stroke-width="4" stroke="#2E2E2E"/>`.

## V Page Roster
| File | Type | Key Placeholders |
|------|------|-----------------|
| `01_cover.svg` | cover | `{{TITLE}}`, `{{SUBTITLE}}`, `{{AUTHOR}}`, `{{DATE}}` |
| `02_toc.svg` | toc | `{{TOC_ITEM_N_TITLE}}` (N=1–4) |
| `02_chapter.svg` | chapter | `{{CHAPTER_TITLE}}` |
| `03_content.svg` | content | `{{PAGE_TITLE}}`, `{{BOX_TITLE_N}}`, `{{CONTENT_AREA_N}}`, `{{OVAL_LABEL_N}}` (N=1–4) |
| `04_ending.svg` | ending | `{{THANK_YOU}}`, `{{CONTACT_INFO_LEFT}}`, `{{CONTACT_INFO_RIGHT}}` |
