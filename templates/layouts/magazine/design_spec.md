---
layout_id: magazine
kind: layout
summary: Magazine & E-Ink layout templates - warm tones, serif titles, split layouts, structured margins.
keywords: [Magazine, E-Ink, Editorial, Serif, Warm]
canvas_format: ppt169
page_count: 4
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}"]
  03_content_split: ["{{PAGE_TITLE}}", "{{KICKER}}", "{{CONTENT_LEFT}}", "{{CONTENT_RIGHT}}"]
  04_ending: ["{{THANK_YOU}}", "{{CLOSING_MESSAGE}}"]
---

# Magazine Layout Specification

## I. Template Overview
- **Design Style**: Magazine & E-Ink. Strong serif headings contrasted against clean sans-serif body prose.
- **Rhythm**: Generous margins, clean borders, quiet spaces.
- **Theme**: Light-mode off-white page background with charcoal-ink text.

## II. Layout Elements
- Thin rules (`stroke-width="1"`) in `#BFBFBF` or `#262626` for segment dividers.
- Small monospaced category tags on the top-left of content pages.
- Centered page layout on cover pages with three-dot footer.
