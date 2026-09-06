---
layout_id: 传统行业_经典红
kind: layout
summary: 五页可编辑结构原型，覆盖封面、目录、章节、内容和结束页；不锁定品牌、配色、字体或图表图例样式。
canvas_format: ppt169
page_count: 5
page_types: [cover, toc, chapter, content, ending]
---

# 传统行业_经典红 - 视觉设计规范

> **Structure-only Layout**: 本资产只定义画布、页面结构、语义槽位和 SVG 原型。SVG 中的颜色与字体仅用于结构预览，生成时必须服从所选 Brand、Style 与当前项目 `spec_lock.md`。


## I. 结构画布

| 属性 | 数值 |
| --- | --- |
| **比例** | 标准 16:9 |
| **分辨率** | 1280 × 720 px (缩放自 960 × 540) |
| **viewBox** | `0 0 1280 720` |
| **安全边距** | 左右 56px, 上 48px, 下 40px |

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

## III. 语义槽位

| 占位符 | 说明 |
| --- | --- |
| `{{TITLE}}` | 封面/结束页主标题 |
| `{{SUBTITLE}}` | 封面/结束页副标题 |
| `{{TAGLINE}}` | 封面页详细文本描述 1 |
| `{{AUTHOR}}` | 汇报人/作者名 |
| `{{DATE}}` | 汇报日期/时间 |
| `{{BRAND_LINE}}` | 封面底栏辅助说明 |
| `{{CHAPTER_NUM}}` | 章节大序号 |
| `{{CHAPTER_TITLE}}` | 章节主标题 |
| `{{CHAPTER_DESC}}` | 章节详细描述文本 |
| `{{PAGE_TITLE}}` | 内容页顶部标题 |
| `{{KEY_MESSAGE}}` | 内容页辅助核心陈述信息 |
| `{{CONTENT_1}}` 到 `{{CONTENT_7}}` | 内容页七个环形要素里面的文本 |
