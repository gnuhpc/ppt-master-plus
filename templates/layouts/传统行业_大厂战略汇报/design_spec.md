---
layout_id: 传统行业_大厂战略汇报
kind: layout
summary: 五页可编辑结构原型，覆盖封面、目录、章节、内容和结束页；不锁定品牌、配色、字体或图表图例样式。
canvas_format: ppt169
page_count: 5
page_types: [cover, toc, chapter, content, ending]
---

# 传统行业_大厂战略汇报 - 视觉设计规范

> **Structure-only Layout**: 本资产只定义画布、页面结构、语义槽位和 SVG 原型。SVG 中的颜色与字体仅用于结构预览，生成时必须服从所选 Brand、Style 与当前项目 `spec_lock.md`。


## I. 结构画布

| 属性 | 数值 |
| --- | --- |
| **比例** | 标准 16:9 |
| **分辨率** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |

---

## II. Page Roster

| 文件 | 角色 | 结构用途 |
|---|---|---|
| `01_cover.svg` | cover | 标题、副标题和必要署名槽位 |
| `02_toc.svg` | toc | 目录项及其简短说明槽位 |
| `02_chapter.svg` | chapter | 章节编号、标题和摘要槽位 |
| `03_content.svg` | content | 标题与正文、数据、图片或图表语义槽位 |
| `04_ending.svg` | ending | 收束信息与必要署名槽位 |

图表与表格区域只保留语义槽位和几何；系列配色、图例、坐标轴、表格皮肤与数据装饰必须由 skill 内置 Chart/Table 样式和当前项目 `spec_lock.md` 决定。
