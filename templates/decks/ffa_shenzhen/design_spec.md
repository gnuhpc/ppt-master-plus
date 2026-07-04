---
template_id: ffa_shenzhen
category: scenario
summary: Flink Forward Asia (FFA) Shenzhen Forum tech presentation style.
keywords: [FFA, Flink, Tech, Purple, Dark]
primary_color: "#9966F7"
canvas_format: ppt169
replication_mode: standard
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  02_toc: ["{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}", "{{TOC_ITEM_4_TITLE}}", "{{TOC_ITEM_4_DESC}}"]
  03_content: ["{{PAGE_TITLE}}", "{{KEY_MESSAGE}}", "{{CONTENT_AREA}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}", "{{SOURCE}}"]
  04_ending: ["{{THANK_YOU}}", "{{CLOSING_MESSAGE}}"]
---

# FFA Shenzhen Forum — Design Specification

## I. Template Overview
- **Use Cases**: Flink Forward Asia (FFA) 分论坛分享、大数据/流计算技术汇报、技术方案演进与架构设计展示。
- **Design Tone**: Tech-focused, developer-friendly, dynamic, and brand-consistent.
- **Theme Mode**: Dark mode (deep black background, glowing neon highlights in purple/blue/green/yellow).

FFA (Flink Forward Asia) Shenzhen Forum design template is a dark-theme presentation style characterized by its tech-geek purple accents, glowing grid borders, and developer-friendly layouts.

## II. Color Scheme
- **Primary Purple**: `#9966F7` (Main highlights, number blocks, cover decoration)
- **Secondary Blue**: `#4DB5FF` (Secondary indicators, accents)
- **Neon Green**: `#04CF82` (Status / positive indicator)
- **Neon Yellow**: `#F8DE4B` (Warning / caution highlights)
- **Coral Red**: `#FF5350` (Alert / error highlights)
- **Background**: `#000000` (Deep black with background assets)
- **Text White**: `#FFFFFF` (Primary text)
- **Text Gray**: `#D9D9D9` / `#A0A0A0` (Secondary labels & descriptions)

## III. Signature Design Elements
- **Tech Brand Identity**: FFA & Flink logo prominently placed at top-left.
- **Neon Accents**: Restrained neon linear gradients (`ggrad1`) supporting glassmorphic cards.
- **Structured Spacing**: Standard safe margin (72px left/right, 48px top, 40px bottom) to preserve visual breathing room on dark pages.

## IV. Page Roster

| File | Role | Description |
|------|------|-------------|
| `01_cover.svg` | cover | Main cover slide with dark brand image, title, subtitle, presenter box, and sponsor logos. |
| `02_chapter.svg` | chapter | Chapter divider page featuring large translucent neon numeral and center-aligned description. |
| `02_toc.svg` | toc | Table of contents featuring a 2x2 grid card list for up to four agenda sections. |
| `03_content.svg` | content | Standard content slide frame with FFA logo header, centered title and key message, and a glassmorphic content area container. |
| `04_ending.svg` | ending | Closing thank-you slide reusing the cover background style with centralized closing statement. |

## V. Assets

| File | Purpose |
|------|---------|
| `cover_bg.png` | Dark glowing background image for cover and ending slides. |
| `logo.png` | Flink Forward Asia brand logo. |
| `sponsor_logo.png` | Sponsor and partner logo banner. |
| `content_bg.jpeg` | Glowing network grid background for content and TOC slides. |
| `chapter_bg.jpeg` | Abstract geometric tech background for chapter divider slides. |
