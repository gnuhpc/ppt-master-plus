---
layout_id: minimal_business_plan
kind: layout
summary: Sleek modern corporate style with off-center grey panels and soft gradient office split images.
keywords: [Business Plan, Modern Corporate, Minimalist, Grey Panel, Gradient]
canvas_format: ppt169
page_count: 5
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}"]
  02_toc: ["{{TOC_ITEM_1_TITLE}}"]
  03_content: ["{{PAGE_TITLE}}", "{{CONTENT_AREA}}"]
  04_ending: ["{{THANK_YOU}}", "{{CLOSING_MESSAGE}}"]
---

# Minimal Business Plan — Design Specification

## I. Template Overview
- **Use Cases**: Corporate reports, business proposals, project briefings.
- **Design Tone**: Ultra-clean, contemporary, architectural feel.
- **Theme Mode**: Light mode (warm off-white background with light grey block borders).

## II. Color Scheme
- **Dark Slate**: `#0D0D0D` (Accent buttons and lines)
- **Soft Grey Block**: `#ECECEC` / `#F2F2F2` (Asymmetric layout bars)
- **Highlight Text**: `#808080` (Muted gray descriptors)

## III. Signature Design Elements
- **Asymmetrical Sidebar Panel**: Large vertical grey block placed off-center on the left.
- **Gradient Overlay Split**: Photographic office backgrounds faded softly using custom linear SVG gradients.
- **Header Line Anchor**: Small thick black line segment anchoring page title headers.

## IV. Page Roster

| File | Role | Description |
|------|------|-------------|
| `01_cover.svg` | cover | Sidebar split cover layout with black year banner. |
| `02_chapter.svg` | chapter | Divider layout mirroring cover style with large bold section titles. |
| `02_toc.svg` | toc | Simple list agenda with diagonal split image and numbered catalog blocks. |
| `03_content.svg` | content | Standard content slide frame maintaining cover's top banner and three dots footer. |
| `04_ending.svg` | ending | Thank you slide mirroring cover layout. |
