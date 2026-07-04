---
layout_id: blue_gray_classic
kind: layout
summary: Simple business blue and gray layout style.
keywords: [Classic, Business, Blue, Gray, Light]
canvas_format: ppt169
page_count: 12
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  02_toc: ["{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}"]
  03_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
---

# Simple Blue Gray Classic Layout — Design Specification

## I. Template Overview
- **Use Cases**: General business presentations, project kickoffs, training sessions, annual reports, summary decks.
- **Design Tone**: Minimalist, corporate, structured, and rational.
- **Theme Mode**: Light mode (soft light gray background `#F3F3F3`, blue and dark-gray accents).

## II. Color Scheme
- **Classic Blue**: `#0070C0` (Headers, numbers, primary highlights)
- **Neutral Gray**: `#7F7F7F` (Labels, subheadings, shapes)
- **Background**: `#F3F3F3` (Light gray canvas background)
- **Dark Text**: `#404040` / `#262626` (Primary readable text)

## III. Signature Design Elements
- **Blue Triangle Header**: Page title has a small right-pointing blue triangle next to it.
- **Translucent Rings**: Cover, chapter, and ending pages feature circular bubble textures.

## IV. Page Roster

| File | Role | Description |
|------|------|-------------|
| `01_cover.svg` | cover | Main cover slide with blue circles, big title, subtitle, and author details box. |
| `02_chapter.svg` | chapter | Chapter divider page with concentric loops, large number, and chapter summary. |
| `02_toc.svg` | toc | Table of contents featuring a 4-step horizontal process card layout. |
| `03_content.svg` | content | Generic content page frame defining title, triangle, footer, and open content area. |
| `03a_content_img_list.svg` | content | Variant content slide: Left photo frame, right 3-step vertical process list. |
| `03b_content_two_col.svg` | content | Variant content slide: 2-column bulleted layout. |
| `03c_content_timeline.svg` | content | Variant content slide: 4-step horizontal progress process nodes. |
| `03d_content_grid.svg` | content | Variant content slide: 2x2 modular matrix card layout. |
| `03e_content_table.svg` | content | Variant content slide: 5-row structured data table layout. |
| `03f_content_funnel.svg` | content | Variant content slide: 4-stage vertical funnel chart layout. |
| `03g_content_venn.svg` | content | Variant content slide: 3-circle Venn diagram layout. |
| `04_ending.svg` | ending | Thank you slide with concentric loops and thank you message. |
