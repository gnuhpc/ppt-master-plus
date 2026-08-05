# 截图美化与排版手艺标准 (Screenshot Framing & Image Padding Standards)

> 借鉴 `guizang-ppt-skill` 的 CleanShot X 程序化截图适配逻辑。当输入包含产品 UI 截图、网页截图、App 截图或代码截图时，优先使用程序化适配（截图居中 + 统一比例 + 主题背景衬托），严禁盲目让 AI 生图重画真实 UI 文本。

---

## 一、 核心原则

1. **真实 UI 细节保真（程序化优先）**：
   - 截图中包含关键文字、代码或真实 UI 细节时，保持截图 100% 原始像素保真。
   - 不要强行调用生图模型“重新绘制 UI”（除非原图极模糊或需要抽象情景化）。
2. ** CleanShot X 风格居中与衬底**：
   - 根据 Slide 图片槽位比例（如 `16:9`, `4:3`, `1:1`）创建目标画布。
   - 截图放置于画布中央或靠侧，四周留出统一的内边距 (`padding`) 与精致影层，背景充填主题匹配的暗蓝/灰调网格纹理。

---

## 二、 7 大截图排版语义参数

在处理包含截图的 SVG 页面时，按以下 7 参数确定 `<g id="screenshot_container">` 的样式结构：

| 参数 | 可选值 | 说明 |
|---|---|---|
| `ratio` | `16:9` / `4:3` / `1:1` | 跟随 Slide 布局槽位比例 |
| `background` | `grid` / `plain` / `gradient` | 充填画布底色（5%-8% 淡中性调，不盖过截图） |
| `padding` | `compact` (16px) / `standard` (32px) / `spacious` (48px) | 截图中文字密集时选 `spacious` |
| `inset` | `none` / `subtle` / `balanced` | 截图从背景浮起的视差层级 |
| `shadow` | `none` / `soft` / `editorial` | 杂志风选 `soft`；瑞士极简风选 `none` |
| `corners` | `square` / `small` (4px) / `medium` (8px) | 瑞士风选 `square`；杂志风选 `small` |
| `alignment` | `center` / `top-left` / `bottom-right` | 默认为 `center` 居中 |

---

## 三、 SVG 结构示例 (CleanShot X Frame)

```xml
<!-- 截图容器：CleanShot X 风格充填背景与边框 -->
<g id="screenshot_frame_01" transform="translate(640, 120)">
  <!-- 画布背景衬底 (Grid / Neutral Dark) -->
  <rect width="560" height="420" rx="8" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>
  
  <!-- 窗口控制小红黄绿按钮 (Window Chrome) -->
  <circle cx="24" cy="24" r="5" fill="#EF4444"/>
  <circle cx="40" cy="24" r="5" fill="#F59E0B"/>
  <circle cx="56" cy="24" r="5" fill="#10B981"/>
  
  <!-- 真实截图 (保真嵌入) -->
  <image href="images/app_screenshot.png" x="20" y="44" width="520" height="356" preserveAspectRatio="xMidYMid meet"/>
</g>
```
