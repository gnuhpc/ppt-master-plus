---
layout_id: black_white_flower_minimal
kind: layout
summary: Elegant black and white minimalist style with hand-drawn flower sketch accents.
keywords: [Black and White, Flower Sketch, Minimalist, Elegant]
canvas_format: ppt169
page_count: 5
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}"]
  02_toc: ["{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_4_TITLE}}"]
  03_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}"]
  04_ending: ["{{THANK_YOU}}", "{{CLOSING_MESSAGE}}"]
---

# Black White Flower Minimal — Design Specification

## I. Template Overview
- **Use Cases**: Creative work reports, minimalist project briefings, elegant design portfolios.
- **Design Tone**: Artistic, elegant, minimalist, high contrast.
- **Theme Mode**: Light mode (pure white canvas background).

## II. Color Scheme
- **Deep Charcoal**: `#222A34` / `#0C0C0C` (Main typography and solid blocks)
- **Background**: `#FFFFFF` (Pure white background)
- **Border Gray**: `#445469` (Divider lines)

## III. Signature Design Elements
- **Flower Sketch**: Clean black-and-white flower sketch asset `flower_sketch.png` placed as decoration.
- **Dotted Separators**: White dashed line inside the chapter divider block.

## IV. Page Roster

| File | Role | Description |
|------|------|-------------|
| `01_cover.svg` | cover | Big bold title, thin divider line, and vertical flower sketch illustration. |
| `02_chapter.svg` | chapter | Chapter divider with a solid charcoal block, large white PART number, and description. |
| `02_toc.svg` | toc | Simple list agenda. |
| `03_content.svg` | content | Content slide frame defining title, footer, and open content area. |
| `04_ending.svg` | ending | Thank you slide mirroring cover layout. |
