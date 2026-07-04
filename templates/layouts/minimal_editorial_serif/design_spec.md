---
layout_id: minimal_editorial_serif
kind: layout
summary: High-end editorial style layout with clean serif typography and split-image divider blocks.
keywords: [Editorial, Minimalist, Serif Font, Split Image, Clean]
canvas_format: ppt169
page_count: 5
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}"]
  02_toc: ["{{TOC_ITEM_1_TITLE}}"]
  03_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}"]
  04_ending: ["{{THANK_YOU}}", "{{CLOSING_MESSAGE}}"]
---

# Minimal Editorial Serif — Design Specification

## I. Template Overview
- **Use Cases**: High-end business portfolios, design agency profiles, modern fashion lookbooks, elegant work reports.
- **Design Tone**: Clean, sophisticated, editorial, high-contrast serif headers on pure white.
- **Theme Mode**: Light mode (pure white `#FFFFFF` canvas background).

## II. Color Scheme
- **Charcoal Black**: `#262626` (Text and header box borders)
- **Neutral Soft Gray**: `#BFBFBF` / `#D9D9D9` (Secondary descriptors and borders)
- **Canvas White**: `#FFFFFF` (Background)

## III. Signature Design Elements
- **Split Image Dividers**: Distinct vertical splits with photographic panels.
- **Top Banner Frame**: Centered small text "WE LOVE WHAT WE DO" framed by two line segments at the top margin.
- **Serif Contrast**: Strong juxtaposition between bold serif Chinese characters and clean sans-serif English letters.

## IV. Page Roster

| File | Role | Description |
|------|------|-------------|
| `01_cover.svg` | cover | Centered title in thin border box with top banner and three dots footer. |
| `02_chapter.svg` | chapter | Clean split layout featuring left-hand vertical image block and charcoal title panel. |
| `02_toc.svg` | toc | Dynamic layout with diagonal divider line and triangle clipped image on left. |
| `03_content.svg` | content | Standard content slide frame maintaining cover's top banner and three dots footer. |
| `04_ending.svg` | ending | Thank you slide mirroring cover layout. |
