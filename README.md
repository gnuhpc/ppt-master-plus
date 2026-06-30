# PPT Master Plus

![PPT Master Plus 扁平手绘宣传图](assets/ppt-master-plus-cover.png)

`ppt-master-plus` 是一个面向高质量、可编辑 PPTX 生产的通用 AI agent skill。它以 [`ppt-master`](https://github.com/hugohe3/ppt-master) 的 SVG→PPTX 方法论和制作链路为底座，融合上游 [`hugohe3/ppt-master`](https://github.com/hugohe3/ppt-master) 的 PPTX intake、美化、原生增强与 Confirm UI 能力，并新增传统行业模板、分阶段审核和软依赖绘图路由。

它的目标不是”快速吐几页幻灯片”，而是把资料理解、叙事组织、视觉规范、逐页制作、讲稿质检和最终导出串成一条可控的生产线。

## 安装

复制以下 prompt，发给你的 AI Agent 即可完成安装：

```
请安装并使用 ppt-master-plus skill：https://github.com/gnuhpc/ppt-master-plus

可选伴侣 skill（按需安装，缺失时自动降级回内置 SVG）：
- fireworks-tech-graph（正式技术架构图）：https://github.com/yizhiyanhua-ai/fireworks-tech-graph
- excalidraw（手绘/白板风格）：https://github.com/Agents365-ai/excalidraw-skill
- Mermaid（流程图/时序图/ER 图）：https://github.com/Agents365-ai/creating-mermaid-diagrams
- PlantUML（UML/组件图）：https://github.com/Agents365-ai/plantuml-skill
- draw.io（拓扑/云厂商图标）：https://github.com/Agents365-ai/drawio-skill
- tldraw（tldraw 白板）：https://github.com/Agents365-ai/tldraw-skill
```

## 与 ppt-master 的功能对比

`ppt-master-plus` 是在 `ppt-master` 的基础上进行了全方位能力扩充的进阶版本。以下是核心功能的对比：

| 功能维度 | `ppt-master` (标准版) | `ppt-master-plus` (进阶版) |
| :--- | :--- | :--- |
| **定位与重点** | 面向标准 SVG→PPTX 生成，强调快捷、批量自动排版。 | 面向高水准商业汇报、流程交互确认、以及多源技术架构图路由。 |
| **生成模式控制** | • **连续模式**：一气呵成直接生成整份 PPT。 | • **逐页确定精修（Gated）**：生成每页都停下供预览与批注确认。<br>• **连续模式**：自动不打断生成。<br>• **分段模式（Split）**：长文档跨对话分阶段执行。 |
| **网页配置端与批注机制** | 基础配置（调色板、字体、主题元素）。生成过程中忽视批注，导出后统一应用。 | 升级版 Confirm UI（支持模式切换与 `preserve_master`）。**支持中途批注修复**：生成过程中点击 **Apply changes** 后，AI 自动读取批注并开始修复；Antigravity CLI 与 Codex Desktop 都通过 `--wait-annotation` 监听适配。 |
| **Live Preview 页内直接编辑** | 无。导出后在 PowerPoint 中手动修改。 | 支持三类无需 AI 介入的交互式编辑：**直接属性改写**（文字、颜色、坐标、SVG 属性）；**批注标记**（描述复杂意图，交由 AI 在 Apply changes 后处理）；**元素删除标注**（选中元素后按 Delete/Backspace 或点击删除按钮，元素以红框+半透明标记为"待删"，记录到批注面板，AI 在 Apply changes 后完成实际删除）。 |
| **演讲稿在线编辑** | 无。需在 PowerPoint 中手动输入讲稿。 | Left 面板内置 **目录 / 演讲稿** 切换标签：切换到演讲稿标签即可直接编辑当前页讲稿，有改动时面板顶部出现 **保存** 按钮，点击后立即写入 `notes/<slide>.md`，无需 Apply changes。 |
| **美化入口路由** | 无独立美化流程。无论用户要求如何，PPTX 一律经 `ppt_to_md.py` 提取为 Markdown 后走主生产流程，Strategist 可自由重构叙事、页数、页序和视觉系统。 | 智能路由：泛化请求（"美化一下"/"让它更专业"）→ 主流程（Strategist 自由重构）；用户显式要求保留页数/页序/文字/母版 → [`beautify-pptx.md`](workflows/beautify-pptx.md) 保真美化流程，两种路线互不混淆。 |
| **保真美化（Faithful Beautify）** | 不支持。PPTX 被当作普通资料输入，不区分内容保留约束，不保证页数/页序/文字不变。 | 专属工作流 [`beautify-pptx.md`](workflows/beautify-pptx.md)：<br>• **画布原尺寸**：`beautify_identity.py` 从 PPTX `p:sldSz` 读取精确像素尺寸，不强制归一化到 1280×720<br>• **内容冻结契约**：`pptx_intake.py` + `beautify_inventory.py` 生成逐页台账（文字/图表数据/表格/图片），文字逐字冻结，数据值锁定，严格 1:1 页数映射<br>• **源身份提取**：`analysis/<stem>.identity.json` 含主题调色板、实际观察字体/字号；Confirm UI 以源 PPT 风格预填，用户可确认或覆盖<br>• **`preserve_master`**：OOXML 级逐页保留——源第 N 页的 slideLayout/master 映射到输出第 N 页，主版式背景/Logo/页脚等 PPT 原生元素不转入 SVG，由母版承载<br>• **图表再生成模式**：`preserve_master=true` → 自由设计；`false` → catalog 引导（与主流程一致）<br>• **输出验证**：对导出 PPTX 重跑 `ppt_to_md.py`，逐页核对文字保真度和页数 |
| **Deck 模板** | 8 套品牌专属 Deck 模板（中国电信、中国电建、中汽研、招商银行、重庆大学等企业/高校定制风格）。 | **30 套**：继承 8 套品牌模板 + 1 套 ffa_shenzhen + **21 套传统行业模板**（商业汇报、咨询麦肯锡风、教学课件、党建、竞聘述职、数据可视化、学术开题等全场景覆盖），配 3 套专属版式规范指导文件（[`executor-general.md`](references/executor-general.md)、[`executor-consultant.md`](references/executor-consultant.md)、[`executor-consultant-top.md`](references/executor-consultant-top.md)）。 |
| **图表 / 信息图 SVG** | 71 个（图表、流程、框架、信息图、战略模型等基础覆盖）。 | **131 个**（在 71 个基础上新增 60 个，进一步覆盖更丰富的可视化结构和行业场景）。 |
| **Layout 骨架** | 7 组（学术答辩、AI 运营、政务蓝/红、医学、像素复古、心理学共 7 种结构骨架）。 | **23 组**（在 7 组基础上新增 16 组，覆盖极简商务、编辑性衬线、水彩多彩、产品发布、大理石灰、水墨极简等更多版式风格）。 |
| **Brand preset** | 2 套（anthropic、google）。 | **3 套**（新增 flink_ai_style）。 |
| **图标库** | 11,631 个 SVG，含 chunk-filled / phosphor-duotone / simple-icons / tabler-filled / tabler-outline 五套图标库。 | 同款 5 套图标库、同等规模（11,631 个），未扩展；图标检索和复制流程相同。 |
| **外部绘图路由** | 仅支持内置 SVG 基础图解。 | **软依赖绘图路由器**：智能分流到 `fireworks-tech-graph`、`excalidraw`（手绘风格可编辑源文件）、`Mermaid`、`PlantUML` 或 `draw.io`，环境缺失时自动降级回内置 SVG，绝不阻塞。 |
| **讲稿与质检** | 基础字数和段落检查。 | 强制性 SVG 结构警告、PPTX 导出校验，新增讲稿专项校验脚本（[`check_speaker_notes.py`](scripts/check_speaker_notes.py) 与 [`speaker-notes.md`](references/speaker-notes.md)）；讲稿检查是导出前的**硬性门禁**，零错误才允许进入后处理。 |
| **原生 PPTX 增强** | 无此路线。给定 PPTX 必须先提取为 Markdown 再走 SVG 重建流程，不能只追加元数据。 | 专属工作流 [`native-enhance-pptx.md`](workflows/native-enhance-pptx.md)：对已有成品 PPTX 进行 **OOXML zip 级直接 patch**，可追加讲稿、录音音频、自动播放时序和页面转场——全程不走 SVG 转换，不改写任何已有形状/图表/图片/母版，是"加料不重建"的专属路线。 |
| **默认动画策略** | 导出时默认启用元素入场动画（`-a auto`），AI 自动按组别匹配效果。 | 导出时**默认关闭动画**（`-a none`），整页一次性出现，避免"AI 痕迹"感知；仅在用户明确要求时才开启入场动画或页面转场。 |
| **用户配置文件夹** | 使用 `~/.ppt-master` 存储配置与密钥。 | 使用新路径 `~/.ppt-master-plus`，并**支持平滑回退**以读取旧的 `~/.ppt-master` 配置文件。 |
| **自动化契约测试** | 无专门的自动化合约测试套件。 | **新增契约测试**（[`test_skill_contract.py`](scripts/tests/test_skill_contract.py)），自动验证 Gated/Continuous 流程、Live Preview 交互细节及 OOXML 母版媒体完整性。 |


## 推荐 AI Agent 与模型

这个 skill 适合在支持本地文件、脚本执行和长上下文工作的 AI agent 环境中使用。推荐入口：

| AI Agent | 推荐模型 / 档位 | 适用场景 |
|---|---|---|
| Antigravity CLI | `gemini-flash 3.5` / `high` | 长资料 intake、连续制稿、需要较强吞吐和上下文保持的 PPTX 生产 |
| Codex | `gpt5.5` / `medium` | 叙事重构、设计确认、逐页 SVG 制作和质量检查的均衡配置 |

如果环境允许，也可以按任务阶段切换：Antigravity CLI 处理资料量大、连续生产压力高的项目；Codex 处理需要精修判断、文件修订和质量检查的项目。

## 主要功能

- 从 PDF、DOCX、XLSX、PPTX、URL、Markdown 或粘贴文本创建新的 PPTX。
- 支持两种生产模式：
  - 逐页确定精修：每生成一页都停下来，用户在 Live Preview 中确认或批注修复后，才继续下一页。
  - 全自动一次性生成：完成必要设计确认后自动进入制作，不逐页等待。
- 支持已有 PPTX 的多种路线：
  - 普通美化：将 PPTX 当作资料重新组织成新故事。
  - 保真美化：显式保留页序、页数、文字和可选母版。
  - 对成品 PPTX 追加讲稿、音频、自动播放和转场等原生增强。
- 支持浏览器实时预览、页面注解回收、SVG 质量检查、讲稿质量检查和 PPTX 导出验证。
- 支持可选绘图路由：
  - 普通展示图、图表、信息图默认走内置 SVG，保证和 PPTX 导出链路最稳。
  - [`fireworks-tech-graph`](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)：正式、规整的架构图和技术流程图。
  - [`excalidraw`](https://github.com/Agents365-ai/excalidraw-skill)：手绘、白板、头脑风暴风格，并保留可编辑源文件。
  - [`Mermaid`](https://github.com/Agents365-ai/creating-mermaid-diagrams) / [`PlantUML`](https://github.com/Agents365-ai/plantuml-skill) / [`draw.io`](https://github.com/Agents365-ai/drawio-skill) / [`tldraw`](https://github.com/Agents365-ai/tldraw-skill) 作为更专门的外部图资产路线，仅在用户明确需要或内容非常匹配时使用。
  - 缺失依赖时回退到内置 SVG，不安装、不阻塞。

## 常见使用方式

关于用户使用时候的具体动作和交互指令，请首先参阅 **[最佳实践指南](file:///Users/gnuhpc/projects/skills/ppt-master-plus/references/best-practices.md)**。

### 1. 从文档创建新的 PPTX

适合把 PDF、DOCX、XLSX、PPTX、网页、Markdown 或一段文字重新组织成一份新的演示文稿。这个路线会把资料当作内容来源，由 Strategist 重新梳理叙事、页数、结构和视觉风格；原始文档的页序不需要保留，必要时可以合并、拆分、删减或重排内容。

典型输入动作：
```text
使用 ppt-master-plus，把 /path/to/report.pdf 做成一份 12 页左右的路演 PPT，面向投资人，风格专业克制，走逐页确定精修。
```

用户核心动作流程：
1. 告知 Agent 生产模式（`逐页确定精修` 或 `全自动一次性生成`）和源文件。
2. 配合完成画布、页数、受众、风格、配色、图标、字体、图片策略等全局设计决策。
3. 顺序制作并预览 SVG 页；如果选择逐页确定精修，每页确认通过后才继续下一页。

### 2. 普通美化已有 PPTX

适合已经有一份 PPTX，希望让它更专业、更有重点，但没有要求原页数、原页序和每页文字完全不变。这个路线走主生产流程：PPTX 被当作资料来源，Strategist 可以重新梳理叙事、调整页数、拆分/合并页面并重做视觉系统。

典型输入动作：
```text
使用 ppt-master-plus，美化 /path/to/deck.pptx，让它更适合客户汇报，整体更专业、更有重点。
```

用户核心动作流程：
1. 配合 Confirm UI 确认 `content_divergence`：希望多贴近源 PPT，还是允许更自由重构。
2. 配合完成画布、页数、受众、风格、配色、图标、字体、图片策略等全局设计决策。
3. 预览并核对重新生成的 SVG 效果，确认后导出原生可编辑 PPTX。

### 3. 保真美化已有 PPTX

适合必须保留原页数、原页序、每页文字和数据，只优化版式、层级、留白、对齐、图表呈现和整体专业度。这个路线走 `faithful-beautify`，可选择是否保留源 PPTX 母版/版式。

典型输入动作：
```text
使用 ppt-master-plus，美化 /path/to/deck.pptx，保留每页文字和页序不变，只重新排版，让它更专业。
```

用户核心动作流程：
1. 明确要求保留原有的页数、页序、每页文字和数据值。
2. 配合 Confirm UI 网页端确认是否保留原 PPT 各页面的母版与版式。
3. 预览并核对 1:1 重新版面排布后的 SVG 效果，确认后导出原生可编辑 PPTX。

## 浏览器确认、预览与反馈

在生成过程中，系统会自动提示并引导您打开本地浏览器进行配置和预览确认。具体的交互细节请参考 **[最佳实践指南](file:///Users/gnuhpc/projects/skills/ppt-master-plus/references/best-practices.md)**。

### 设计确认页面（Confirm UI）
*   **动作**：在 Strategist 阶段，系统提示后在浏览器中打开 `http://localhost:5050`。
*   **动作**：在 Tier 1 选择并确认画布、受众、交付目的等大方向后，点击下一步。
*   **动作**：在 Tier 2 选择并微调自动推荐的配色、字体、图片、图标策略和是否需要页面转场动画，点击确认。转场动画默认不需要。

### 逐页预览与微调页面（Live Preview）
*   **动作**：在幻灯片制作阶段，在网页端查看实时生成的 slide 效果。
*   **动作（直改）**：直接在预览页面上选中文字或形状，通过右侧属性面板微调文本或属性，点击 **Apply changes** 应用回项目。
*   **动作（批注）**：若需 Agent 进行复杂重构，在 Annotations 框内输入批注要求，点击 **Add annotation** 及 **Apply changes**；AI 会自动读取保存到 `svg_output/` 的批注并开始修复。在 Codex Desktop 这类桌面端工具中，Agent 会保持一个后台 `--wait-annotation --timeout 0` 监听会话来捕获点击事件；每轮修复完成后会重新挂起监听，所以可以继续提交第二批、第三批修改意见。页面中的复制提示仅作为自动监听失效时的备用触发方式。

### 回到 Agent 修改
*   **动作**：您也可以随时跳过网页，在聊天里直接描述修改要求（例如：“第 3 页标题改成‘增长飞轮’，重新导出。”），Agent 将自动修改并更新。

## 已有 PPTX 的处理边界

给定一个 `.pptx`，`ppt-master-plus` 可以美化，但不会把它当作“用户提供模板”来填充新内容。

| 用户意图 | 支持情况 | 路线 |
|---|---|---|
| 普通美化 / 优化 / 更专业，没有显式保留约束 | 支持 | 主生产流程 |
| 保留原页数、页序、每页文字和数据，只优化版式、层级、留白和视觉一致性 | 支持 | `faithful-beautify` |
| 把 PPTX 当作资料来源，重新组织故事、拆分/合并页面、调整页数或重排结构 | 支持 | 主生产流程 |
| 对成品 PPTX 追加讲稿、音频、自动播放、转场等，不改变可见内容和布局 | 支持 | `native-enhance-pptx` |
| 上传或指定一个 PPTX 作为模板，再填入另一批新内容 | 当前不支持 | 如需基于该 PPTX 产出新 deck，请改走主生产流程；内部模板化能力作为未来扩展，不作为当前替代路径承诺 |

这个边界是故意的：普通美化关注“把现有 deck 作为资料重构得更好”，保真美化关注“在明确保留约束下修好现有 deck”，而用户提供模板填充容易把外部 deck 当作不稳定的占位符系统处理，**不再作为公开用户路线暴露**。魔改 fork 可以保留遗留/内部实现文件用于迁移和研究，但入口契约仍然是：用户提供 PPTX 不能被当作任意模板来填新内容。

## 模板与图例丰富度

模板资产覆盖”整套风格模板、页面结构、图表图例、图标库”四层。以下为与 `ppt-master` 的逐项对比：

| 资产类型 | `ppt-master` | `ppt-master-plus` | 说明 |
|---|---:|---:|---|
| Deck 模板 | 8 套 | **30 套** | plus 新增 ffa_shenzhen 和 21 套传统行业模板，覆盖商业汇报、咨询、教学、党建、竞聘、数据可视化、学术开题等全场景 |
| 其中：传统行业模板 | — | **21 套** | `ppt-master-plus` 专有，适合中文商业场景、课件、述职、答辩、项目架构等 |
| 图表 / 信息图 SVG | 71 个 | **131 个** | plus 新增 60 个，进一步覆盖更丰富的可视化结构和行业场景 |
| Layout 骨架 | 7 组 | **23 组** | plus 新增 16 组，覆盖极简商务、水彩多彩、产品发布、大理石灰、水墨极简等更多版式风格 |
| Brand preset | 2 套 | **3 套** | plus 新增 flink_ai_style；两者均含 anthropic、google |
| 图标库（SVG 数量） | 11,631 个 | 11,631 个（同） | chunk-filled / phosphor-duotone / simple-icons / tabler-filled / tabler-outline 五套，两版本完全一致 |

这些模板不是单纯的静态素材库。内置模板只在用户明确选择内部模板路径，或工作流需要调用图表、图标等基础表达组件时参与；默认不会把用户上传的 PPTX 当模板使用。Strategist 根据资料类型、受众、交付目的、内容密度和视觉风格规划表达方式；Executor 再逐页读取 `spec_lock.md`，把模板、图表、图标和内容约束落实到可导出的 SVG / PPTX。

## 基本架构

```text
Source Materials
  ↓
Intake
  - PDF / DOCX / XLSX / PPTX / Web / Markdown 转 Markdown
  - PPTX intake 抽取画布、页结构、表格、图表和版式事实
  ↓
Production Mode Gate
  - 逐页确定精修：每页停下确认，应用批注修复后再继续
  - 全自动一次性生成：确认设计后连续生产
  ↓
Strategist
  - 资料理解
  - 叙事重构
  - 八项设计确认
  - design_spec.md + spec_lock.md
  ↓
Optional Assets
  - AI / Web / User / Formula 图片资源
  - Fireworks / Excalidraw / 内置 SVG 图示路由
  ↓
Executor
  - 顺序逐页手写 SVG
  - 实时预览
  - 质量检查
  ↓
Post-processing
  - SVG 修整
  - 讲稿检查
  - PPTX 导出
  - 可选原生增强
```

核心入口是 [`SKILL.md`](SKILL.md)。分阶段生产流程在 [`workflows/gated-production.md`](workflows/gated-production.md)，上游与本地合并记录在 [`references/upstream.md`](references/upstream.md)。关于模板设计架构请参考 [`references/templates-architecture.md`](references/templates-architecture.md)，系统技术架构设计参考 [`references/technical-design.md`](references/technical-design.md)。

## 致敬 ppt-master

`ppt-master-plus` 继承并致敬 [`ppt-master`](https://github.com/hugohe3/ppt-master)：它保留了原有 skill 对”原生可编辑 PPTX””高质量 SVG 页面””模板驱动制作”和”中文汇报场景”的执着，同时在此基础上把 Deck 模板从 8 套扩充到 30 套（新增 21 套传统行业模板和 ffa_shenzhen）、图表 SVG 从 71 个扩充到 131 个、Layout 骨架从 7 组扩充到 23 组，并新增了讲稿质检能力和更严格的生产流程。

这个 `plus` 不是推翻，而是延展：在 [`ppt-master`](https://github.com/hugohe3/ppt-master) 的地基上，把上游的新工具链、分阶段审核、PPTX 原生增强、软依赖绘图路由和更严格的生产纪律合并到一条更完整的工作流里。

感谢 [`ppt-master`](https://github.com/hugohe3/ppt-master) 打下的底层方法论：先理解内容，再设计叙事；先锁定规范，再逐页制作；最终交付的不是图片截图，而是可编辑、可演示、可继续加工的 PowerPoint。
