/* ============================================================
   PPT Master - SVG Editor  |  app.js
   Vanilla JS, IIFE pattern
   ============================================================ */
(function () {
    "use strict";

    // ---- i18n -------------------------------------------------------
    var MESSAGES = {
        en: {
            page_title: "PPT Master - Live Preview",
            panel_slides: "Slides",
            panel_annotations: "Annotations",
            placeholder_select_slide: "Select a slide on the left to begin",
            label_selected_element: "Selected element",
            empty_selected_element: "Click an element on the slide to select it",
            btn_select_group: "Select parent group",
            label_batch_edit: "Batch edit",
            label_group_edit: "Group edit",
            section_geometry: "Geometry",
            section_style: "Style",
            section_text_style: "Text",
            section_raw_attrs: "Raw attributes",
            label_edit_instruction: "Edit instruction",
            placeholder_annotation: "Describe how the AI should modify this element...",
            placeholder_annotation_multi: "Describe how to modify all {count} elements...",
            btn_add_annotation: "Add annotation",
            label_annotations_on_slide: "Annotations on this slide",
            btn_submit_annotations: "Apply changes",
            btn_exit_preview: "Exit preview",
            modal_submit: "Submit",
            modal_cancel: "Cancel",
            empty_waiting_slides: "Waiting for generated slides...",
            empty_no_slides: "No slides found",
            placeholder_live_ready: "Live preview is ready. Generated slides will appear here.",
            placeholder_slide_writing: "Slide is still being written. Waiting for the next refresh...",
            empty_annotations: "No annotations yet",
            tooltip_remove_annotation: "Remove annotation",
            multi_selected: "{count} elements selected",
            multi_mixed: "mixed",
            err_load_slides: "Failed to load slides: ",
            err_load_slide: "Failed to load slide: ",
            err_add_annotation: "Failed to add annotation: ",
            err_remove_annotation: "Failed to remove annotation: ",
            err_save: "Save failed: ",
            err_edit: "Edit failed: ",
            label_direct_edit: "Object attributes (pending until Apply changes)",
            prop_content_placeholder: "Enter text content...",
            prop_multiline_hint: "Multi-line — select a single line (tspan) to edit text",
            edit_saved_hint: "Change staged. Click Apply changes to write it to svg_output.",
            btn_undo: "Undo",
            undo_done: "Reverted last staged edit",
            undo_empty: "No staged edit to undo",
            overlap_caption: "Overlapping here — pick one",
            err_empty_svg: "Slide loaded but the canvas is empty. The SVG may be malformed or missing a root <svg> element.",
            warn_icon_inline: "{count} icon(s) failed to render: {names}",
            warn_svg_no_dims: "SVG is missing width/height attributes. Please ask the AI to strictly follow shared-standards.md §4 and include width & height in the SVG root element.",
            slide_error_tooltip: "Failed to parse this slide: ",
            reload_banner: "This slide was updated on disk. Click to reload.",
            modal_confirm_submit: "Apply staged attribute edits and annotations to disk?\n\nThe preview service will keep running. Click Exit preview when you want to stop it.",
            modal_success_submit: "Changes saved to svg_output.\n\nThe AI agent should apply annotations automatically. If it does not start within a minute, use the prompt below.",
            modal_prompt_label: "Fallback: if the AI does not start automatically, copy this prompt and paste it into chat:",
            modal_prompt_copied: "Copied. Paste it into your AI tool chat.",
            apply_annotation_prompt: "Please modify slide page(s) {pages} according to the annotations saved in svg_output. The annotations have already been written into svg_output; inspect the annotated SVG element(s), apply the requested changes for those page(s), and MUST remove the annotation markers (`data-edit-target` and `data-edit-annotation`) after applying each annotation. Do not leave resolved annotations in the SVG. Re-export the PPTX if needed.",
            modal_confirm_exit: "Exit preview and stop the local server?\n\nUnapplied edits and annotations will be discarded.",
            modal_success_exit: "Preview stopped.\n\nYou can close this tab and return to the chat.",
            modal_stopping: "Stopping preview server...",
            lang_toggle_title: "Switch language",
            nav_first: "First slide (Home)",
            nav_prev: "Previous slide (←)",
            nav_next: "Next slide (→)",
            nav_last: "Last slide (End)",
            nav_play: "Play (Full Screen)",
            btn_exit_fs: "Exit Full Screen",
            nav_counter: "{current} / {total}",
            nav_empty: "— / —",
            btn_notes_title: "Speaker notes",
            notes_panel_title: "Speaker Notes",
            notes_loading: "Loading…",
            notes_none: "No speaker notes for this slide.",
            btn_delete: "Delete",
            err_delete: "Delete failed: ",
            annotation_delete_text: "Delete this element",
            tab_slides: "Outline",
            tab_notes: "Notes",
            btn_notes_save: "Save",
            label_agent_point: "Agent Task",
            popover_title_page: "Page Agent Tasks",
            popover_placeholder: "Describe what the AI agent should modify for this element/page...",
            ann_tag_page: "Page",
            btn_page_annotate_title: "Annotate entire page",
            hint_tab_annotate: "annotate",
            shortcut_bar: "<span class='hint'><kbd>Click</kbd> Manual edit</span><span class='hint'><kbd>DblClick</kbd> Agent task</span><span class='hint'><kbd>Shift</kbd>+<kbd>Click</kbd> Multi-select</span><span class='hint'><kbd>Right-click</kbd> Overlapping</span><span class='hint'><kbd>←</kbd> <kbd>→</kbd> Prev / Next</span><span class='hint'><kbd>Del</kbd> Delete</span><span class='hint'><kbd>Esc</kbd> Deselect</span>",
            panel_title: "Slide Editor & Agent Tasks",
            tab_manual: "✍️ Manual Edit",
            tab_agent: "🤖 Agent Tasks",
            live_status_text: "Live auto-saved to file",
            live_status_saved: "✓ Saved to file",
            label_agent_target: "Target:",
            target_page: "Entire Page",
            btn_target_all: "Target Page",
            btn_target_elem: "Target Element",
            placeholder_agent_point: "Describe what the AI agent should modify (e.g. convert to timeline, add Q4 chart...)",
            btn_add_point: "+ Add Point",
            btn_stage_slide: "💾 Save Draft",
            btn_stage_agent: "💾 Save Draft",
            btn_submit_agent: "🚀 Submit This Page",
            btn_submit_all_agent: "⚡ Submit All Pages",
            btn_submitting_agent: "⏳ Processing in Background...",
            status_staged: "Staged",
            status_submitted: "Submitted",
            status_completed: "Completed",
            empty_all_points: "No modification points found across any slides to submit.",
            toast_staged_slide: "Saved draft for current slide ({count} points pending)",
            toast_staged_empty: "Please enter modification points first",
            toast_submit_all_success: "Submitted {count} modification points across {slides} slides to background Agent!",
            toast_submit_page_success: "Submitted {count} modification points for this slide to background Agent!",
            label_points_on_slide: "Modification Points on Slide",
            empty_points: "No modification points yet. Enter above to add.",
            agent_processing_text: "AI Agent is processing in background, please wait...",
            agent_done_title: "Background Processing Complete!",
            agent_done_desc: "Slide {page} modifications applied, preview updated.",
            agent_done_generic: "Modifications applied, preview updated.",
            btn_edit_point: "Edit point",
            btn_point_save: "Save",
            btn_point_cancel: "Cancel",
            toast_point_updated: "Modification point updated",
            hint_dblclick_edit: "Double click to edit"
        },
        zh: {
            page_title: "PPT Master - 实时预览",
            panel_slides: "幻灯片",
            panel_annotations: "标注",
            placeholder_select_slide: "在左侧选择一张幻灯片开始",
            label_selected_element: "已选元素",
            empty_selected_element: "点击幻灯片中的元素进行选择",
            btn_select_group: "选择父级组",
            label_batch_edit: "批量编辑",
            label_group_edit: "组编辑",
            section_geometry: "几何",
            section_style: "样式",
            section_text_style: "文本",
            section_raw_attrs: "原始属性",
            label_edit_instruction: "修改说明",
            placeholder_annotation: "描述希望 AI 如何修改该元素……",
            placeholder_annotation_multi: "描述希望如何修改所选 {count} 个元素……",
            btn_add_annotation: "添加标注",
            label_annotations_on_slide: "本页标注",
            btn_submit_annotations: "应用修改",
            btn_exit_preview: "退出预览",
            modal_submit: "提交",
            modal_cancel: "取消",
            empty_waiting_slides: "正在等待生成幻灯片……",
            empty_no_slides: "未找到幻灯片",
            placeholder_live_ready: "实时预览已就绪,生成的幻灯片会在这里出现。",
            placeholder_slide_writing: "幻灯片仍在写入,等待下次刷新……",
            empty_annotations: "暂无标注",
            tooltip_remove_annotation: "删除标注",
            multi_selected: "已选 {count} 个元素",
            multi_mixed: "混合",
            err_load_slides: "加载幻灯片失败:",
            err_load_slide: "加载幻灯片失败:",
            err_add_annotation: "添加标注失败:",
            err_remove_annotation: "删除标注失败:",
            err_save: "保存失败:",
            err_edit: "编辑失败:",
            label_direct_edit: "对象属性(点击应用修改后写入)",
            prop_content_placeholder: "输入文本内容...",
            prop_multiline_hint: "多行文本——选中单行(tspan)编辑文字",
            edit_saved_hint: "修改已暂存。点击“应用修改”后写入 svg_output。",
            btn_undo: "撤销",
            undo_done: "已撤销上一条暂存修改",
            undo_empty: "没有可撤销的暂存修改",
            overlap_caption: "此处重叠元素——点击选择",
            err_empty_svg: "幻灯片已加载但画布为空。SVG 可能损坏或缺少根 <svg> 元素。",
            warn_icon_inline: "{count} 个图标渲染失败:{names}",
            warn_svg_no_dims: "SVG 缺少 width/height 属性，预览可能异常。请让 AI 严格遵守 shared-standards.md §4 规范，在 SVG 根元素中补全 width 和 height。",
            slide_error_tooltip: "该幻灯片解析失败:",
            reload_banner: "当前页已在磁盘上更新,点此重新加载。",
            modal_confirm_submit: "确认将暂存属性修改和标注写入磁盘?\n\n预览服务会继续运行。需要关闭时请点击退出预览。",
            modal_success_submit: "修改已保存到 svg_output。\n\nAI Agent 应会自动开始应用标注，无需任何操作。如果一分钟内没有自动开始，再使用下方备用 prompt。",
            modal_prompt_label: "备用：如果 AI 没有自动开始，复制以下 prompt 粘贴到对话框：",
            modal_prompt_copied: "已复制。如需手动触发，请粘贴到 AI 对话框。",
            apply_annotation_prompt: "请修改第 {pages} 页：根据该页已保存到 svg_output 中的标注进行修改。标注已经写入 svg_output，请检查对应 SVG 中带标注的元素，按标注要求完成该页修改；每条标注修复完成后，必须移除标注标记（`data-edit-target` 和 `data-edit-annotation`），不要把已解决的标注留在 SVG 中。需要时重新导出 PPTX。",
            modal_confirm_exit: "退出预览并停止本地服务?\n\n未应用的属性修改和标注将被丢弃。",
            modal_success_exit: "预览已停止。\n\n可以关闭本标签页并回到对话窗口。",
            modal_stopping: "正在停止预览服务……",
            lang_toggle_title: "切换语言",
            nav_first: "第一页 (Home)",
            nav_prev: "上一页 (←)",
            nav_next: "下一页 (→)",
            nav_last: "末页 (End)",
            nav_play: "全屏播放",
            btn_exit_fs: "退出全屏",
            nav_counter: "{current} / {total}",
            nav_empty: "— / —",
            btn_notes_title: "演讲稿",
            notes_panel_title: "演讲稿",
            notes_loading: "加载中…",
            notes_none: "该页暂无演讲稿",
            btn_delete: "删除",
            err_delete: "删除失败: ",
            annotation_delete_text: "删除此元素",
            tab_slides: "目录",
            tab_notes: "演讲稿",
            btn_notes_save: "保存",
            label_agent_point: "Agent 修改点",
            popover_title_page: "整页修改点",
            popover_placeholder: "输入本页/该元素的Agent修改需求（例如：调整排版、精简文字、补充图例...）",
            ann_tag_page: "整页",
            btn_page_annotate_title: "标注整页",
            hint_tab_annotate: "标注",
            shortcut_bar: "<span class='hint'><kbd>单击</kbd> 手动修改</span><span class='hint'><kbd>双击</kbd> Agent修改点</span><span class='hint'><kbd>Shift</kbd>+<kbd>单击</kbd> 多选</span><span class='hint'><kbd>右键</kbd> 重叠元素</span><span class='hint'><kbd>←</kbd> <kbd>→</kbd> 翻页</span><span class='hint'><kbd>Del</kbd> 删除</span><span class='hint'><kbd>Esc</kbd> 取消选择</span>",
            panel_title: "幻灯片编辑与修改",
            tab_manual: "✍️ 手动修改",
            tab_agent: "🤖 Agent 修改",
            live_status_text: "修改即时生效 (自动保存)",
            live_status_saved: "✓ 已保存到文件",
            label_agent_target: "目标:",
            target_page: "整页修改",
            btn_target_all: "设为整页",
            btn_target_elem: "设为选中元素",
            placeholder_agent_point: "列出本页需要大模型/Agent修改的内容（例如：调整排版为左右结构、加粗标题、补充数据图表...）",
            btn_add_point: "+ 添加修改点",
            btn_stage_slide: "💾 暂存本页",
            btn_stage_agent: "💾 暂存本页",
            btn_submit_agent: "🚀 提交本页",
            btn_submit_all_agent: "⚡ 全部提交 (多页)",
            btn_submitting_agent: "⏳ 后台处理中...",
            status_staged: "待提交",
            status_submitted: "已提交",
            status_completed: "已完成",
            empty_all_points: "当前没有任何待提交的修改点。",
            toast_staged_slide: "已暂存本页修改（{count} 个修改点待提交）",
            toast_staged_empty: "请先在上方输入本页需要修改的内容",
            toast_submit_all_success: "已提交 {slides} 页（共 {count} 个修改点）至后台 Agent 处理！",
            toast_submit_page_success: "已提交本页（共 {count} 个修改点）至后台 Agent 处理！",
            label_points_on_slide: "本页修改点清单",
            empty_points: "当前页暂无修改点，输入上方内容并点击添加",
            agent_processing_text: "后台 Agent 处理中，请稍候...",
            agent_done_title: "后台处理已完成！",
            agent_done_desc: "第 {page} 页修改已生效，预览已更新。",
            agent_done_generic: "后台修改已完成，预览已生效！",
            btn_edit_point: "编辑修改点",
            btn_point_save: "保存",
            btn_point_cancel: "取消",
            toast_point_updated: "修改点已更新",
            hint_dblclick_edit: "双击可编辑修改点"
        }
    };

    // Canonical delete annotation texts for both languages — used to detect
    // delete annotations regardless of which language was active when they were added.
    var _DELETE_ANNOTATION_TEXTS = ["Delete this element", "删除此元素"];
    function isDeleteAnnotation(text) {
        return _DELETE_ANNOTATION_TEXTS.indexOf(text) !== -1;
    }

    var QUICK_ISSUES = [
        { en: "Text obscured", zh: "文字遮挡" },
        { en: "Text overflow", zh: "文字溢出" },
        { en: "Legend obscured", zh: "图例遮挡" },
        { en: "Elements overlapping", zh: "元素重叠" },
        { en: "Misaligned", zh: "对齐偏移" },
        { en: "Improper size", zh: "尺寸不当" },
        { en: "Chinese/English conversion", zh: "中英文转换" },
        { en: "Delete", zh: "删除" }
    ];

    var LANG = (function () {
        try {
            var stored = window.localStorage.getItem("ppt_lang");
            if (stored === "zh" || stored === "en") return stored;
        } catch (e) { /* ignore */ }
        var nav = (navigator.language || navigator.userLanguage || "en").toLowerCase();
        return nav.indexOf("zh") === 0 ? "zh" : "en";
    })();
    var currentLang = LANG;

    function t(key, params) {
        var dict = MESSAGES[LANG] || MESSAGES.en;
        var msg = dict[key];
        if (msg === undefined) msg = MESSAGES.en[key];
        if (msg === undefined) return key;
        if (params) {
            Object.keys(params).forEach(function (p) {
                msg = msg.replace("{" + p + "}", params[p]);
            });
        }
        return msg;
    }

    function applyI18n() {
        document.documentElement.setAttribute("lang", LANG === "zh" ? "zh-CN" : "en");
        document.title = t("page_title");
        document.querySelectorAll("[data-i18n]").forEach(function (el) {
            el.textContent = t(el.getAttribute("data-i18n"));
        });
        document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
            el.placeholder = t(el.getAttribute("data-i18n-placeholder"));
        });
        document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
            el.innerHTML = t(el.getAttribute("data-i18n-html"));
        });
        document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
            el.title = t(el.getAttribute("data-i18n-title"));
        });
        updateNavLabel();
    }

    function setLang(lang) {
        if (lang !== "zh" && lang !== "en") return;
        LANG = lang;
        currentLang = lang;
        try { window.localStorage.setItem("ppt_lang", lang); } catch (e) { /* ignore */ }
        applyI18n();
        var toggleBtn = document.getElementById("btn-lang-toggle");
        if (toggleBtn) {
            toggleBtn.textContent = lang === "zh" ? "EN" : "中";
            toggleBtn.title = t("lang_toggle_title");
        }
        // Re-render dynamic regions so they pick up the new language
        updateSelectionPanel();
        updateAnnotationList();
        updateUndoButton();
        loadSlides();
    }

    // ---- DOM refs ---------------------------------------------------
    var slideListEl       = document.getElementById("slide-list");
    var svgPlaceholder    = document.getElementById("svg-placeholder");
    var svgContent        = document.getElementById("svg-content");
    var selectedElementEl = document.getElementById("selected-element");
    var annotationInput   = document.getElementById("annotation-input");
    var annotationText    = document.getElementById("annotation-text");
    var btnAddAnnotation  = document.getElementById("btn-add-annotation");
    var annotationsEl     = document.getElementById("annotations");
    var btnUndo           = document.getElementById("btn-undo");
    var btnSave           = document.getElementById("btn-save");
    var btnExitPreview    = document.getElementById("btn-exit-preview");
    var modalOverlay      = document.getElementById("modal-overlay");
    var modalMessage      = document.getElementById("modal-message");
    var modalPrompt       = document.getElementById("modal-prompt");
    var modalPromptLabel  = document.getElementById("modal-prompt-label");
    var modalPromptText   = document.getElementById("modal-prompt-text");
    var modalConfirm      = document.getElementById("modal-confirm");
    var modalCancel       = document.getElementById("modal-cancel");
    var elementPropsEl    = document.getElementById("element-props");

    var navFirstBtn       = document.getElementById("nav-first");
    var navPrevBtn        = document.getElementById("nav-prev");
    var navNextBtn        = document.getElementById("nav-next");
    var navLastBtn        = document.getElementById("nav-last");
    var navCounterEl      = document.getElementById("nav-counter");
    var navNameEl         = document.getElementById("nav-name");
    var tabSlides         = document.getElementById("tab-slides");
    var tabNotes          = document.getElementById("tab-notes");
    var btnNotesSave      = document.getElementById("btn-notes-save");
    var notesContentEl    = document.getElementById("notes-content");

    var navPlayBtn        = document.getElementById("nav-play");
    var fullscreenOverlay = document.getElementById("fullscreen-overlay");
    var fsNavPrev         = document.getElementById("fs-nav-prev");
    var fsNavNext         = document.getElementById("fs-nav-next");
    var fsBtnExit         = document.getElementById("fs-btn-exit");
    var fsNavCounter      = document.getElementById("fs-nav-counter");
    var fsNavName         = document.getElementById("fs-nav-name");
    var fsSvgContainer    = document.getElementById("fullscreen-svg-container");
    var fsNotesContent    = document.getElementById("fullscreen-notes-content");
    var fsNotesEditor     = document.getElementById("fullscreen-notes-editor");
    var themeSelect       = document.getElementById("astryx-theme-select");
    var fsThemeSelect     = document.getElementById("fs-theme-select");

    var fsControlsEl      = document.getElementById("fullscreen-controls");
    
    var fsLayoutToggleBtn = document.getElementById("fs-layout-toggle-btn");

    var popoverOverlay    = document.getElementById("annotation-popover-overlay");
    var popoverTitle      = document.getElementById("popover-title");
    var popoverClose      = document.getElementById("popover-close");
    var popoverChips      = document.getElementById("popover-chips");
    var popoverText       = document.getElementById("popover-text");
    var popoverSubmit     = document.getElementById("popover-submit");
    var btnPageAnnotate   = document.getElementById("btn-page-annotate");

    var tabManual           = document.getElementById("tab-manual");
    var tabAgent            = document.getElementById("tab-agent");
    var sectionManual       = document.getElementById("section-manual");
    var sectionAgent        = document.getElementById("section-agent");
    var liveSaveText        = document.getElementById("live-save-text");
    var liveSaveStatus      = document.querySelector(".live-save-status");
    var agentTargetBadge    = document.getElementById("agent-target-badge");
    var btnTargetToggle     = document.getElementById("btn-target-toggle");
    var agentPointText      = document.getElementById("agent-point-text");
    var btnAddPoint         = document.getElementById("btn-add-point");
    var pointsCountBadge    = document.getElementById("points-count-badge");
    var agentPointsList     = document.getElementById("agent-points-list");
    var btnSubmitAgent      = document.getElementById("btn-submit-agent");
    var btnStagePoint       = document.getElementById("btn-stage-point");
    var btnStageAgent       = document.getElementById("btn-stage-agent");
    var btnSubmitAllAgent   = document.getElementById("btn-submit-all-agent");
    var agentStatusIndicator = document.getElementById("agent-status-indicator");
    var agentStatusText     = document.getElementById("agent-status-text");
    var agentLastDoneIndicator = document.getElementById("agent-last-done-indicator");
    var lastDoneSummary     = document.getElementById("last-done-summary");
    var agentNotificationToast = document.getElementById("agent-notification-toast");
    var toastTitle          = document.getElementById("toast-title");
    var toastDesc           = document.getElementById("toast-desc");
    var toastClose          = document.getElementById("toast-close");

    // ---- State ------------------------------------------------------
    var currentSlide      = null;   // filename, e.g. "slide_01.svg"
    var slideNames        = [];     // ordered slide filenames for navigation
    var currentAgentTarget = "__page__";
    var slideTasks        = {};     // {slide_name: [task_obj, ...]}
    var isAgentProcessing = false;
    var lastProcessedTime = 0;
    var submittedSlides   = new Set();
    var selectedElementIds = new Set(); // id attrs of selected SVG elements
    var slideAnnotations  = {};     // {element_id: annotation_text} for current slide
    var liveMode          = false;
    var slidePollTimer    = null;
    var pendingModalAction = "submit";
    var slideMtimes       = {};     // {name: mtime} — last-seen mtime for each slide
    var notesMtimes       = {};     // {name: notes_mtime} — last-seen notes mtime for each slide
    var activeTheme       = "astryx-theme-default";
    var currentRawSvgContent = "";
    var reloadBannerEl    = null;   // singleton banner element shown when currentSlide mtime drifts
    var editStackCount    = {};     // {name: staged edit count} — mirrors backend PENDING_EDITS
    var savedHintShown    = false;  // show the "staged edit" hint once per session
    var annotationsDirty  = false;  // unsaved annotations added/removed this session
    var notesMode         = false;  // false=slides tab, true=notes tab
    var notesDirty        = false;  // unsaved notes changes
    var _notesLoadedText  = "";     // last-loaded notes text for dirty detection
    var isFullscreenMode  = false;
    var _popoverTargetIds = [];
    var _popoverSelectedChips = new Set();
    var _popoverIsPage    = false;

    // Staged edits live in server memory until "Apply changes"; the server can
    // still idle-timeout or be killed and drop them. Warn before the tab leaves
    // so the user remembers to apply (browsers show their own generic prompt).
    function hasUnsavedWork() {
        if (annotationsDirty) return true;
        if (notesDirty) return true;
        return Object.keys(editStackCount).some(function (k) {
            return editStackCount[k] > 0;
        });
    }
    window.addEventListener("beforeunload", function (e) {
        if (!hasUnsavedWork()) return undefined;
        e.preventDefault();
        e.returnValue = "";
        return "";
    });

    function hideModalPrompt() {
        if (!modalPrompt || !modalPromptText || !modalPromptLabel) return;
        modalPrompt.style.display = "none";
        modalPromptText.textContent = "";
        modalPromptLabel.textContent = "";
    }

    function pageNumberFromFilename(name) {
        var idx = slideNames.indexOf(name);
        if (idx >= 0) return idx + 1;
        var m = String(name || "").match(/(?:slide[_-]?|^)(\d+)/i);
        if (m) return parseInt(m[1], 10);
        return null;
    }

    function formatPageList(files) {
        var seen = {};
        var pages = [];
        (files || []).forEach(function (name) {
            var n = pageNumberFromFilename(name);
            if (n && !seen[n]) {
                seen[n] = true;
                pages.push(n);
            }
        });
        if (pages.length === 0 && currentSlide) {
            var cur = pageNumberFromFilename(currentSlide);
            if (cur) pages.push(cur);
        }
        pages.sort(function (a, b) { return a - b; });
        if (pages.length === 0) return LANG === "zh" ? "当前" : "current";
        return pages.join(LANG === "zh" ? "、" : ", ");
    }

    function copyTextToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(text);
        }
        return new Promise(function (resolve, reject) {
            try {
                var ta = document.createElement("textarea");
                ta.value = text;
                ta.setAttribute("readonly", "");
                ta.style.position = "fixed";
                ta.style.left = "-9999px";
                document.body.appendChild(ta);
                ta.select();
                document.execCommand("copy");
                document.body.removeChild(ta);
                resolve();
            } catch (err) {
                reject(err);
            }
        });
    }

    function showAnnotationPrompt(files) {
        if (!modalPrompt || !modalPromptText || !modalPromptLabel) return;
        if (!files || files.length === 0) {
            hideModalPrompt();
            return;
        }
        var pages = formatPageList(files);
        var prompt = t("apply_annotation_prompt", { pages: pages });
        modalPromptLabel.textContent = t("modal_prompt_label");
        modalPromptText.textContent = prompt;
        modalPrompt.style.display = "block";
    }

    function currentSlideIndex() {
        if (!currentSlide) return -1;
        return slideNames.indexOf(currentSlide);
    }

    function gotoSlideIndex(idx) {
        if (idx < 0 || idx >= slideNames.length) return;
        var name = slideNames[idx];
        if (name === currentSlide) return;
        var item = slideListEl.querySelector('.slide-item[data-name="' + cssAttr(name) + '"]');
        selectSlide(name, item || undefined);
    }

    function cssAttr(value) {
        return String(value).replace(/"/g, '\\"');
    }

    function updateNavLabel() {
        if (!navCounterEl) return;
        var total = slideNames.length;
        var counterText = "";
        if (total === 0 || !currentSlide) {
            counterText = t("nav_empty");
            navCounterEl.textContent = counterText;
            if (navNameEl) navNameEl.textContent = "";
            if (fsNavCounter) fsNavCounter.textContent = counterText;
            if (fsNavName) fsNavName.textContent = "";
        } else {
            var idx = currentSlideIndex();
            counterText = t("nav_counter", { current: idx + 1, total: total });
            navCounterEl.textContent = counterText;
            if (navNameEl) navNameEl.textContent = currentSlide;
            if (fsNavCounter) fsNavCounter.textContent = counterText;
            if (fsNavName) fsNavName.textContent = currentSlide;
        }
        var idx2 = currentSlideIndex();
        var hasCurrent = idx2 >= 0;
        if (navFirstBtn) navFirstBtn.disabled = !hasCurrent || idx2 === 0;
        if (navPrevBtn)  navPrevBtn.disabled  = !hasCurrent || idx2 <= 0;
        if (navNextBtn)  navNextBtn.disabled  = !hasCurrent || idx2 >= total - 1;
        if (navLastBtn)  navLastBtn.disabled  = !hasCurrent || idx2 >= total - 1;

        if (fsNavPrev) fsNavPrev.disabled = !hasCurrent || idx2 <= 0;
        if (fsNavNext) fsNavNext.disabled = !hasCurrent || idx2 >= total - 1;
    }

    // ================================================================
    //  1.  loadSlides  -- GET /api/slides
    // ================================================================
    function loadSlides() {
        return fetch("/api/slides")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                slideListEl.innerHTML = "";
                var slides = data.slides || [];
                slideNames = slides.map(function (s) { return s.name; });

                if (slides.length === 0) {
                    var empty = document.createElement("div");
                    empty.className = "slide-list-empty";
                    empty.textContent = liveMode
                        ? t("empty_waiting_slides")
                        : t("empty_no_slides");
                    slideListEl.appendChild(empty);
                    if (!currentSlide) {
                        svgPlaceholder.style.display = "block";
                        svgPlaceholder.textContent = liveMode
                            ? t("placeholder_live_ready")
                            : t("empty_no_slides");
                        svgContent.style.display = "none";
                    }
                    updateNavLabel();
                    return;
                }

                var currentExists = false;
                var currentMtimeChanged = false;
                var currentNotesMtimeChanged = false;
                slides.forEach(function (s) {
                    if (s.name === currentSlide) {
                        currentExists = true;
                        // Compare against the mtime we recorded when we last rendered this slide.
                        var lastSeen = slideMtimes[s.name];
                        if (lastSeen !== undefined && s.mtime && s.mtime !== lastSeen) {
                            currentMtimeChanged = true;
                        }
                        var lastNotesSeen = notesMtimes[s.name];
                        if (lastNotesSeen !== undefined && s.notes_mtime && s.notes_mtime !== lastNotesSeen) {
                            currentNotesMtimeChanged = true;
                        }
                        if (s.mtime !== undefined && lastSeen === undefined) {
                            slideMtimes[s.name] = s.mtime;
                        }
                        if (s.notes_mtime !== undefined && lastNotesSeen === undefined) {
                            notesMtimes[s.name] = s.notes_mtime;
                        }
                    }
                    // Track every slide's mtime for the next poll (only update non-current here;
                    // currentSlide's mtime is updated by selectSlide so we can detect drift).
                    if (s.name !== currentSlide) {
                        if (s.mtime !== undefined) slideMtimes[s.name] = s.mtime;
                        if (s.notes_mtime !== undefined) notesMtimes[s.name] = s.notes_mtime;
                    }

                    var item = document.createElement("div");
                    item.className = "slide-item" + (s.name === currentSlide ? " active" : "");
                    if (s.ok === false) {
                        item.className += " slide-error";
                        item.title = t("slide_error_tooltip") + (s.error || "");
                    }
                    item.setAttribute("data-name", s.name);

                    var nameSpan = document.createElement("span");
                    nameSpan.className = "slide-name";
                    nameSpan.textContent = s.name;
                    item.appendChild(nameSpan);

                    if (s.annotation_count > 0) {
                        var badge = document.createElement("span");
                        badge.className = "badge";
                        badge.textContent = s.annotation_count;
                        item.appendChild(badge);
                    }

                    item.addEventListener("click", function () {
                        selectSlide(s.name, item);
                    });
                    slideListEl.appendChild(item);
                });

                if (!currentSlide || !currentExists) {
                    selectSlide(slides[0].name);
                } else if (currentMtimeChanged) {
                    var item = slideListEl.querySelector('.slide-item[data-name="' + cssAttr(currentSlide) + '"]');
                    selectSlide(currentSlide, item || undefined);
                } else if (currentNotesMtimeChanged) {
                    var matching = slides.find(function(x) { return x.name === currentSlide; });
                    if (matching && matching.notes_mtime !== undefined) {
                        notesMtimes[currentSlide] = matching.notes_mtime;
                    }
                    if (document.activeElement !== notesContentEl) {
                        loadCurrentNotes();
                    }
                }
                updateAllTasksUI();
                updateNavLabel();
            })
            .catch(function (err) {
                console.error("loadSlides:", err);
                showError(t("err_load_slides") + err.message);
            });
    }

    function loadSlideControls(name) {
        var paramBox = document.getElementById("param-controls");
        var paramBody = document.getElementById("param-controls-body");
        if (!paramBox || !paramBody) return;

        fetch("/api/slide/" + encodeURIComponent(name) + "/controls")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.status === "ok" && data.controls && Object.keys(data.controls).length > 0) {
                    paramBody.innerHTML = "";
                    paramBox.style.display = "block";
                    Object.keys(data.controls).forEach(function (key) {
                        var val = data.controls[key];
                        var row = document.createElement("div");
                        row.style.marginBottom = "6px";
                        row.style.fontSize = "13px";
                        row.style.display = "flex";
                        row.style.alignItems = "center";
                        row.style.justifyContent = "space-between";

                        var label = document.createElement("span");
                        label.textContent = key + ": ";
                        row.appendChild(label);

                        if (key === "items") {
                            var slider = document.createElement("input");
                            slider.type = "range";
                            slider.min = "1";
                            slider.max = "6";
                            slider.value = val;
                            slider.style.width = "100px";
                            var valSpan = document.createElement("span");
                            valSpan.textContent = val;
                            valSpan.style.marginLeft = "4px";

                            slider.addEventListener("change", function () {
                                valSpan.textContent = slider.value;
                                fetch("/api/slide/" + encodeURIComponent(name) + "/param-update", {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({ key: key, value: slider.value })
                                }).then(function () {
                                    selectSlide(name);
                                });
                            });
                            row.appendChild(slider);
                            row.appendChild(valSpan);
                        } else {
                            var input = document.createElement("input");
                            input.type = "text";
                            input.value = val;
                            input.style.width = "100px";
                            input.addEventListener("change", function () {
                                fetch("/api/slide/" + encodeURIComponent(name) + "/param-update", {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({ key: key, value: input.value })
                                }).then(function () {
                                    selectSlide(name);
                                });
                            });
                            row.appendChild(input);
                        }
                        paramBody.appendChild(row);
                    });
                } else {
                    paramBox.style.display = "none";
                }
            })
            .catch(function () {
                if (paramBox) paramBox.style.display = "none";
            });
    }

    // ================================================================
    //  2.  selectSlide  -- GET /api/slide/{name}
    // ================================================================
    function selectSlide(name, el) {
        // Update active class in sidebar
        document.querySelectorAll(".slide-item").forEach(function (it) {
            it.classList.remove("active");
        });
        if (el) {
            el.classList.add("active");
            el.scrollIntoView({ block: "nearest" });
        }

        currentSlide = name;
        selectedElementIds.clear();
        slideAnnotations = {};
        updateNavLabel();
        if (notesMode || isFullscreenMode) loadCurrentNotes();

        // Reset right panel and rubber band
        cancelRubberBand();
        clearSelection();

        // Selecting a slide implicitly dismisses any stale "page updated" banner.
        hideReloadBanner();

        // Remove any stale spec-violation banner from a previous load.
        var oldSpecBanner = document.getElementById("spec-banner");
        if (oldSpecBanner) oldSpecBanner.remove();

        loadSlideControls(name);
        loadSlideTasks(name);

        fetch("/api/slide/" + encodeURIComponent(name))
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.error) {
                    console.error("selectSlide:", data.error);
                    showError(t("err_load_slide") + data.error);
                    if (liveMode) {
                        currentSlide = null;
                        svgPlaceholder.style.display = "block";
                        svgPlaceholder.textContent = t("placeholder_slide_writing");
                        svgContent.style.display = "none";
                    }
                    return;
                }
                // Render SVG
                currentRawSvgContent = data.content;
                renderCurrentSlideWithTheme();

                // Empty-canvas guard: surface a clear error if the SVG parsed
                // to nothing renderable (issue #115's silent-blank scenario).
                var rootSvg = svgContent.querySelector("svg");
                // Spec observability: missing width/height → red banner only
                if (rootSvg && (!rootSvg.hasAttribute("width") || !rootSvg.hasAttribute("height"))) {
                    var specBanner = document.createElement("div");
                    specBanner.id = "spec-banner";
                    specBanner.style.cssText = "position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);"
                        + "background:#fee2e2;color:#b91c1c;border:2px solid #f87171;border-radius:8px;"
                        + "padding:24px 36px;font-size:16px;font-weight:bold;text-align:center;z-index:9999;"
                        + "width:420px;line-height:1.6;box-shadow:0 4px 12px rgba(0,0,0,0.15);";
                    specBanner.textContent = t("warn_svg_no_dims");
                    document.body.appendChild(specBanner);
                }
                var hasContent = false;
                if (rootSvg) {
                    var children = rootSvg.querySelectorAll("*");
                    for (var i = 0; i < children.length; i++) {
                        var ctag = children[i].tagName.toLowerCase();
                        if (ctag !== "defs" && ctag !== "style" && ctag !== "title" && ctag !== "desc") {
                            hasContent = true;
                            break;
                        }
                    }
                }
                if (!rootSvg || !hasContent) {
                    showError(t("err_empty_svg"));
                    svgPlaceholder.style.display = "block";
                    svgPlaceholder.textContent = t("err_empty_svg");
                    svgContent.style.display = "none";
                    return;
                }

                // Non-fatal warnings (e.g. icon inline failures): surface as a
                // single combined toast so users know why something looks off.
                if (data.warnings && data.warnings.length > 0) {
                    var names = data.warnings.map(function (w) {
                        return w.icon || "(unknown)";
                    }).join(", ");
                    showWarning(t("warn_icon_inline", {
                        count: data.warnings.length,
                        names: names,
                    }));
                }

                // Record the mtime so the next poll can detect on-disk drift.
                if (data.mtime !== undefined) {
                    slideMtimes[name] = data.mtime;
                }

                // Build annotations map from response
                (data.annotations || []).forEach(function (a) {
                    slideAnnotations[a.element_id] = a.annotation;
                });

                editStackCount[name] = data.undo_depth || 0;
                setupSvgInteraction();
                refreshAnnotationVisuals();
                updateAnnotationList();
                updateUndoButton();
            })
            .catch(function (err) {
                console.error("selectSlide:", err);
                showError(t("err_load_slide") + err.message);
            });
    }

    // ================================================================
    //  3.  setupSvgInteraction
    // ================================================================
    var SKIP_TAGS = ["defs", "style", "title", "desc"];

    function setupSvgInteraction() {
        var svg = svgContent.querySelector("svg");
        if (!svg) return;

        // Visual class only — selectability is handled by the delegated handler below.
        // Skipping the per-element addEventListener brings listener-registration time
        // from O(n) to O(1), which matters on decks with hundreds of elements per slide.
        var allEls = svg.querySelectorAll("*");
        allEls.forEach(function (el) {
            var tag = el.tagName.toLowerCase();
            if (SKIP_TAGS.indexOf(tag) !== -1) return;
            if (el === svg) return;
            el.classList.add("svg-selectable");
        });

        svg.addEventListener("click", function (e) {
            // Skip the synthetic click that follows a rubber-band drag-release.
            if (suppressNextSvgClick) {
                suppressNextSvgClick = false;
                return;
            }
            var target = e.target;
            // Blank-area click on the svg root → clear selection.
            if (target === svg) {
                clearSelection();
                return;
            }
            // Ignore clicks bubbling out of non-interactive subtrees.
            if (target.closest && target.closest("defs, style, title, desc")) return;
            // Backend assign_temp_ids() guarantees every element has an id, so
            // closest("[id]") will always find a hit. The exclusion of `svg`
            // itself routes "click outside any real shape" to clearSelection.
            // Icon placeholders are expanded only for browser preview. If a
            // click lands on a generated child, edit the disk-backed data-icon
            // group instead of an inner preview-only node.
            var picked = e.altKey && target.closest
                ? target.closest("g[id]")
                : null;
            picked = picked || (target.closest && target.closest("[data-icon][id]")) ||
                target.closest("[id]");
            if (!picked || picked === svg) {
                clearSelection();
                return;
            }
            selectElement(picked, e.shiftKey);
        });
    }

    // ================================================================
    //  4.  selectElement
    // ================================================================
    function selectElement(elem, addToSelection) {
        var eid = elem.id;
        if (!eid) return;

        if (addToSelection) {
            // Ctrl+click: toggle this element
            if (selectedElementIds.has(eid)) {
                selectedElementIds.delete(eid);
                elem.classList.remove("svg-selected");
            } else {
                selectedElementIds.add(eid);
                elem.classList.add("svg-selected");
            }
        } else {
            // Normal click: clear others, select only this one
            selectedElementIds.forEach(function (id) {
                if (id !== eid) {
                    var old = svgContent.querySelector("#" + CSS.escape(id));
                    if (old) old.classList.remove("svg-selected");
                }
            });
            selectedElementIds.clear();
            selectedElementIds.add(eid);
            elem.classList.add("svg-selected");
        }

        updateSelectionPanel(addToSelection);
    }

    // ================================================================
    //  5.  clearSelection
    // ================================================================
    function clearSelection() {
        selectedElementIds.forEach(function (id) {
            var el = svgContent.querySelector("#" + CSS.escape(id));
            if (el) el.classList.remove("svg-selected");
        });
        selectedElementIds.clear();
        updateSelectionPanel();
    }

    function updateSelectionPanel(suppressPopover) {
        var propsEl = elementPropsEl;
        var count = selectedElementIds.size;

        if (count === 0) {
            selectedElementEl.classList.add("empty");
            selectedElementEl.textContent = t("empty_selected_element");
            annotationInput.style.display = "none";
            annotationText.value = "";
            propsEl.style.display = "none";
            propsEl.innerHTML = "";
            hideAnnotationPopover();
            if (agentTargetBadge && currentAgentTarget !== "__page__") {
                currentAgentTarget = "__page__";
                agentTargetBadge.textContent = t("target_page");
                agentTargetBadge.setAttribute("data-target", "__page__");
                if (btnTargetToggle) btnTargetToggle.textContent = t("btn_target_all");
            }
            return;
        }

        selectedElementEl.classList.remove("empty");
        propsEl.style.display = "block";

        if (count === 1) {
            var eid = selectedElementIds.values().next().value;
            var el = svgContent.querySelector("#" + CSS.escape(eid));
            if (el) {
                var tag = el.tagName.toLowerCase();
                selectedElementEl.innerHTML =
                    '<span class="el-tag">&lt;' + escapeHtml(tag) + '&gt;</span>' +
                    '<span class="el-id">' + escapeHtml(eid) + '</span>';
                propsEl.innerHTML = renderEditableProps(el);
                attachPropEditors(el);
            }
            if (agentTargetBadge) {
                currentAgentTarget = eid;
                agentTargetBadge.textContent = "#" + eid;
                agentTargetBadge.setAttribute("data-target", eid);
                if (btnTargetToggle) btnTargetToggle.textContent = t("btn_target_all");
            }
        } else {
            selectedElementEl.innerHTML =
                '<span class="multi-count">' + escapeHtml(t("multi_selected", { count: count })) + '</span>' +
                '<span class="tab-hint"><kbd>Tab</kbd> ' + escapeHtml(t("hint_tab_annotate")) + '</span>';
            propsEl.innerHTML = renderMultiSelectSummary(Array.from(selectedElementIds));
            attachMultiSelectionEditors(Array.from(selectedElementIds));
            if (agentTargetBadge) {
                currentAgentTarget = Array.from(selectedElementIds).join(",");
                agentTargetBadge.textContent = t("multi_selected", { count: count });
                agentTargetBadge.setAttribute("data-target", currentAgentTarget);
                if (btnTargetToggle) btnTargetToggle.textContent = t("btn_target_all");
            }
        }

        annotationInput.style.display = "none";
        // 单击选中元素时，默认切到手动修改 Tab，展示手动修改要素
        if (tabManual && tabAgent && sectionManual && sectionAgent) {
            if (!tabManual.classList.contains("active")) {
                tabManual.classList.add("active");
                tabAgent.classList.remove("active");
                sectionManual.style.display = "";
                sectionAgent.style.display = "none";
            }
        }
    }

    // ---- Rubber band selection ----
    var rubberBandEl = null;
    var rubberBandStart = null;
    var rubberBandUsed = false;
    var suppressNextSvgClick = false;
    var RUBBER_BAND_THRESHOLD = 5;

    // ---- Drag-to-move (direct geometry edit on the canvas) ----
    // Pressing on an already-selected element drags the whole selection. Frames
    // only update the preview; one staged edit per element is written on release,
    // reusing attrsForMove + stageEditRequest (and backend coalescing).
    var dragStart = null;       // {x, y} screen coords at mousedown on a selection
    var dragMoved = false;      // crossed the move threshold this gesture
    var dragEls = [];           // top-level selected elements being moved
    var dragStartAttrs = {};    // {id: startGeometryAttrs} for drift-free preview

    function hitSelectedAncestor(target) {
        // Walk up from the pressed node to the first element already in the
        // selection, so a press on a selected shape (or its inner preview
        // children) starts a drag regardless of how it was selected.
        var svg = svgContent.querySelector("svg");
        var node = target;
        while (node && node !== svg && node.nodeType === 1) {
            if (node.id && selectedElementIds.has(node.id)) return node;
            node = node.parentNode;
        }
        return null;
    }

    function screenDeltaToLocal(el, dxScreen, dyScreen) {
        // Map a screen-pixel delta into the coordinate space computeRenderBox /
        // attrsForMove use for THIS element (its getCTM() output space). Using the
        // element's own getCTM ∘ getScreenCTM⁻¹ is robust to how a browser splits
        // the viewBox scale between getCTM and getScreenCTM, and naturally accounts
        // for each element's own group transform (correct under multi-select).
        var sctm = el.getScreenCTM ? el.getScreenCTM() : null;
        var ctm = el.getCTM ? el.getCTM() : null;
        if (!sctm || !ctm) return { x: dxScreen, y: dyScreen };
        try {
            var n = ctm.multiply(sctm.inverse());  // linear part: screen → local delta
            var lx = n.a * dxScreen + n.c * dyScreen;
            var ly = n.b * dxScreen + n.d * dyScreen;
            // Singular CTM → SVGMatrix.inverse() throws, DOMMatrix yields NaN.
            // Either way, fall back to the raw delta rather than wedge the drag.
            if (!isFinite(lx) || !isFinite(ly)) return { x: dxScreen, y: dyScreen };
            return { x: lx, y: ly };
        } catch (err) {
            return { x: dxScreen, y: dyScreen };
        }
    }

    function beginDrag() {
        dragEls = topLevelSelectedElements(Array.from(selectedElementIds));
        dragStartAttrs = {};
        dragEls.forEach(function (el) {
            // attrsForMove(el, 0, 0) returns the element's current geometry in the
            // exact attribute shape a move writes (x/y, cx/cy, … or transform);
            // restoring it before each frame keeps the preview drift-free.
            try { dragStartAttrs[el.id] = attrsForMove(el, 0, 0); }
            catch (err) { dragStartAttrs[el.id] = null; }
        });
        document.body.classList.add("svg-dragging");
    }

    function applyAttrSnapshot(el, sa) {
        if (!sa) return;
        applyElementAttrs(el, sa);
    }

    function applyElementAttrs(el, attrs) {
        if (localName(el) === "g" && el.hasAttribute("data-icon") &&
                attrs.x !== undefined && attrs.y !== undefined) {
            // The preview expands <use data-icon> into a <g>, but disk still owns
            // the source <use>. Keep the browser geometry in sync while the staged
            // edit writes x/y back to the real placeholder instead of persisting a
            // transform.
            var m = ownMatrix(el);
            el.setAttribute("transform", "matrix(" + [
                formatCoord(m.a), formatCoord(m.b), formatCoord(m.c),
                formatCoord(m.d), formatCoord(parseFloat(attrs.x)),
                formatCoord(parseFloat(attrs.y))
            ].join(",") + ")");
            el.setAttribute("data-use-x", attrs.x);
            el.setAttribute("data-use-y", attrs.y);
        }
        Object.keys(attrs).forEach(function (k) {
            if (localName(el) === "g" && el.hasAttribute("data-icon") &&
                    (k === "x" || k === "y" || k === "transform")) return;
            if (attrs[k] === null || attrs[k] === undefined) el.removeAttribute(k);
            else el.setAttribute(k, attrs[k]);
        });
    }

    function localName(el) {
        return el && el.tagName ? el.tagName.toLowerCase() : "";
    }

    function markCommittedAttrs(el, attrs) {
        if (attrs && attrs.transform === null &&
                localName(el) === "g" && el.hasAttribute("data-icon")) {
            el.removeAttribute("data-use-has-transform");
        }
    }

    function payloadForCurrentElementState(el, payload) {
        if (!payload || !payload.attrs || payload.attrs.transform !== null ||
                localName(el) !== "g" || !el.hasAttribute("data-icon") ||
                el.hasAttribute("data-use-has-transform")) {
            return payload;
        }
        var attrs = Object.assign({}, payload.attrs);
        delete attrs.transform;
        return Object.assign({}, payload, { attrs: attrs });
    }

    function restoreDragStart(el) {
        applyAttrSnapshot(el, dragStartAttrs[el.id]);
    }

    function applyMoveLocal(el, dxScreen, dyScreen) {
        // Each element converts the shared screen delta into its own local space,
        // so a selection spanning differently-transformed groups still tracks the
        // pointer. Restore-then-apply keeps every frame relative to the start.
        restoreDragStart(el);
        var d = screenDeltaToLocal(el, dxScreen, dyScreen);
        var attrs;
        try { attrs = attrsForMove(el, d.x, d.y); }
        catch (err) { attrs = null; }
        if (!attrs) return null;
        applyElementAttrs(el, attrs);
        return attrs;
    }

    function updateDragPreview(dxScreen, dyScreen) {
        dragEls.forEach(function (el) { applyMoveLocal(el, dxScreen, dyScreen); });
        if (dragEls.length === 1) refreshGeoInputs(dragEls[0], elementPropsEl);
    }

    function commitDrag(dxScreen, dyScreen) {
        var single = dragEls.length === 1;
        dragEls.forEach(function (el) {
            // Capture the pre-drag snapshot in the closure: endDrag() clears
            // dragStartAttrs synchronously after this call, before the staging
            // promise can reject, so the rollback can't rely on the global.
            var startAttrs = dragStartAttrs[el.id];
            var attrs = applyMoveLocal(el, dxScreen, dyScreen);
            if (!attrs) return;
            var payload = payloadForMovedElement(el, attrs);
            stageEditRequest(el.id, payload).then(function () {
                if (payload.attrs) markCommittedAttrs(el, payload.attrs);
                if (payload.promote_tspan) {
                    var promoted = promoteTspanDom(el, payload.promote_tspan);
                    if (promoted && single) refreshGeoInputs(promoted, elementPropsEl);
                }
            }).catch(function (err) {
                // Optimistic preview already moved the element; roll it back so the
                // canvas never shows a move the server never staged.
                applyAttrSnapshot(el, startAttrs);
                if (single) refreshGeoInputs(el, elementPropsEl);
                showError(t("err_edit") + err.message);
            });
        });
    }

    function endDrag() {
        dragStart = null;
        dragMoved = false;
        dragEls = [];
        dragStartAttrs = {};
        document.body.classList.remove("svg-dragging");
    }

    // Per-element nudge staging is serialized: a held arrow key fires many
    // keydowns, each sending an *absolute* position. Without ordering, the
    // unlocked backend could coalesce them out of order and leave the staged
    // value behind the on-screen one. So at most one nudge stage per element is
    // in flight; extra keypresses only update the preview and the queued target,
    // and the next send reads the current DOM position (= the latest).
    var nudgeFlight = {};   // key -> bool: a nudge stage is in flight
    var nudgeQueued = {};   // key -> {el, single, slide, attrs}: latest target awaiting send
    var nudgeLastOk = {};   // key -> attrs: last position the server confirmed

    function nudgeKey(slide, el) { return slide + "|" + el.id; }

    function sendNudge(key, el, single, slide, payload) {
        if (!payload) return;
        payload = payloadForCurrentElementState(el, payload);
        nudgeFlight[key] = true;
        stageEditRequest(el.id, payload, slide).then(function () {
            if (payload.attrs) nudgeLastOk[key] = payload.attrs;
            if (payload.attrs) markCommittedAttrs(el, payload.attrs);
            nudgeFlight[key] = false;
            var q = nudgeQueued[key];
            if (q) { delete nudgeQueued[key]; sendNudge(key, q.el, q.single, q.slide, q.payload); }
        }).catch(function (err) {
            nudgeFlight[key] = false;
            delete nudgeQueued[key];
            // Re-sync the preview to the last confirmed position so it can't show
            // a move the server never staged (only meaningful on the live slide).
            if (payload.promote_tspan && el.__promotionRollback) {
                var restored = el.__promotionRollback();
                if (single && restored) refreshGeoInputs(restored, elementPropsEl);
            } else if (nudgeLastOk[key] && slide === currentSlide && el.isConnected) {
                applyAttrSnapshot(el, nudgeLastOk[key]);
                if (single) refreshGeoInputs(el, elementPropsEl);
            }
            showError(t("err_edit") + err.message);
        });
    }

    function stageNudge(el, single, slide, payload) {
        var key = nudgeKey(slide, el);
        if (nudgeFlight[key]) {
            nudgeQueued[key] = { el: el, single: single, slide: slide, payload: payload };
            return;
        }
        sendNudge(key, el, single, slide, payload);
    }

    function nudgeSelection(dxScreen, dyScreen) {
        // Keyboard arrow micro-move: same geometry path as drag. The DOM updates
        // immediately; staging is serialized per element (see sendNudge), and
        // consecutive same-direction nudges coalesce into one undo step.
        var els = topLevelSelectedElements(Array.from(selectedElementIds));
        if (els.length === 0) return;
        var slide = currentSlide;
        var single = els.length === 1;
        var lastSingleEl = null;
        els.forEach(function (el) {
            var key = nudgeKey(slide, el);
            if (!nudgeFlight[key] && !nudgeQueued[key]) {
                // Fresh burst: re-capture the pre-move baseline from the current
                // DOM, so a failed nudge rolls back to *this* burst's start rather
                // than a stale position left by an earlier drag/edit/undo.
                try { nudgeLastOk[key] = attrsForMove(el, 0, 0); }
                catch (err) { delete nudgeLastOk[key]; }
            }
            var d = screenDeltaToLocal(el, dxScreen, dyScreen);
            var attrs;
            try { attrs = attrsForMove(el, d.x, d.y); } catch (err) { attrs = null; }
            if (!attrs) return;
            applyElementAttrs(el, attrs);
            var payload = payloadForMovedElement(el, attrs);
            if (payload.promote_tspan) {
                el = promoteTspanDom(el, payload.promote_tspan) || el;
            }
            lastSingleEl = el;
            stageNudge(el, single, slide, payload);
        });
        if (single && lastSingleEl) refreshGeoInputs(lastSingleEl, elementPropsEl);
    }

    // ---- Overlap picker (right-click → list every selectable element here) ----
    // Left-click stays a fast "select the topmost" gesture; right-click is the
    // opt-in disambiguator for stacked elements, so it never pops on normal use.
    var overlapPickerEl = null;

    function collectSelectableAt(clientX, clientY) {
        var svg = svgContent.querySelector("svg");
        if (!svg || !document.elementsFromPoint) return [];
        var out = [];
        var seen = {};
        document.elementsFromPoint(clientX, clientY).forEach(function (node) {
            if (!svg.contains(node) || node === svg) return;
            if (node.closest && node.closest("defs, style, title, desc")) return;
            // Resolve to the disk-backed selectable entity, mirroring the click
            // handler: prefer an enclosing data-icon group, else nearest id.
            var picked = (node.closest && node.closest("[data-icon][id]")) ||
                         (node.closest && node.closest("[id]"));
            if (!picked || picked === svg || !picked.id || seen[picked.id]) return;
            seen[picked.id] = true;
            out.push(picked);
        });
        return out;  // top → bottom in paint order
    }

    function closeOverlapPicker() {
        if (!overlapPickerEl) return;
        var svg = svgContent.querySelector("svg");
        if (svg) {
            svg.querySelectorAll(".overlap-hover").forEach(function (e) {
                e.classList.remove("overlap-hover");
            });
        }
        overlapPickerEl.remove();
        overlapPickerEl = null;
    }

    function showOverlapPicker(clientX, clientY, candidates) {
        closeOverlapPicker();
        var menu = document.createElement("div");
        menu.id = "overlap-picker";
        var cap = document.createElement("div");
        cap.className = "overlap-caption";
        cap.textContent = t("overlap_caption");
        menu.appendChild(cap);
        candidates.forEach(function (el) {
            var item = document.createElement("div");
            item.className = "overlap-item";
            var tag = el.tagName.toLowerCase();
            var txt = (tag === "text" || tag === "tspan")
                ? (el.textContent || "").trim().slice(0, 28) : "";
            item.innerHTML = '<span class="overlap-tag">&lt;' + escapeHtml(tag) +
                '&gt;</span><span class="overlap-id">' + escapeHtml(el.id) + '</span>' +
                (txt ? '<span class="overlap-txt">' + escapeHtml(txt) + '</span>' : '');
            item.addEventListener("mouseenter", function () { el.classList.add("overlap-hover"); });
            item.addEventListener("mouseleave", function () { el.classList.remove("overlap-hover"); });
            item.addEventListener("mousedown", function (ev) {
                if (ev.button !== 0 && ev.button !== 2) return;
                ev.stopPropagation();
                ev.preventDefault();
                var multi = ev.shiftKey;
                selectElement(el, multi);
                if (multi) {
                    menu.querySelectorAll(".overlap-item").forEach(function (it, idx) {
                        it.classList.toggle("overlap-selected", selectedElementIds.has(candidates[idx].id));
                    });
                } else {
                    closeOverlapPicker();
                }
            });
            if (selectedElementIds.has(el.id)) item.classList.add("overlap-selected");
            menu.appendChild(item);
        });
        menu.addEventListener("contextmenu", function (ev) { ev.preventDefault(); });
        document.body.appendChild(menu);
        // Keep the menu inside the viewport.
        var x = Math.min(clientX, window.innerWidth - menu.offsetWidth - 8);
        var y = Math.min(clientY, window.innerHeight - menu.offsetHeight - 8);
        menu.style.left = Math.max(8, x) + "px";
        menu.style.top = Math.max(8, y) + "px";
        overlapPickerEl = menu;
    }

    function initRubberBand() {
        var overlay = document.getElementById("rubber-band-overlay");
        var container = document.getElementById("svg-container");

        container.addEventListener("mousedown", function (e) {
            // Only left mouse button
            if (e.button !== 0) return;

            // Pressing on an already-selected element arms a drag of the whole
            // selection instead of a rubber band. Selecting stays a separate
            // click, so the background is never dragged by accident.
            if (hitSelectedAncestor(e.target)) {
                dragStart = { x: e.clientX, y: e.clientY };
                dragMoved = false;
                return;
            }

            // Always start tracking — rubber band only activates when
            // mousemove exceeds the threshold. This allows clicking on any
            // element (including SVG background rects) to still trigger
            // the element's click handler for selection.
            rubberBandStart = { x: e.clientX, y: e.clientY };
            rubberBandUsed = false;
        });

        document.addEventListener("mousemove", function (e) {
            if (dragStart) {
                var ddx = e.clientX - dragStart.x;
                var ddy = e.clientY - dragStart.y;
                if (!dragMoved && Math.sqrt(ddx * ddx + ddy * ddy) < RUBBER_BAND_THRESHOLD) {
                    return;  // below threshold — still a click, let selection stand
                }
                if (!dragMoved) {
                    dragMoved = true;
                    beginDrag();
                }
                updateDragPreview(ddx, ddy);
                return;
            }
            if (!rubberBandStart) return;

            var dx = e.clientX - rubberBandStart.x;
            var dy = e.clientY - rubberBandStart.y;
            var dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < RUBBER_BAND_THRESHOLD) {
                return;
            }

            // Threshold exceeded — this is a drag, not a click
            if (!rubberBandUsed) {
                rubberBandUsed = true;
                overlay.classList.add("active");
            }

            if (!rubberBandEl) {
                rubberBandEl = document.createElement("div");
                rubberBandEl.id = "rubber-band";
                document.body.appendChild(rubberBandEl);
            }

            var x = Math.min(rubberBandStart.x, e.clientX);
            var y = Math.min(rubberBandStart.y, e.clientY);
            var w = Math.abs(dx);
            var h = Math.abs(dy);

            rubberBandEl.style.left = x + "px";
            rubberBandEl.style.top = y + "px";
            rubberBandEl.style.width = w + "px";
            rubberBandEl.style.height = h + "px";
        });

        document.addEventListener("mouseup", function (e) {
            if (dragStart) {
                if (dragMoved) {
                    commitDrag(e.clientX - dragStart.x, e.clientY - dragStart.y);
                    // Swallow the click that follows the drag-release so it does
                    // not re-trigger selection on the dropped element.
                    suppressNextSvgClick = true;
                    window.setTimeout(function () { suppressNextSvgClick = false; }, 50);
                }
                endDrag();
                return;
            }
            if (!rubberBandStart) return;

            overlay.classList.remove("active");

            var dx = e.clientX - rubberBandStart.x;
            var dy = e.clientY - rubberBandStart.y;
            var dist = Math.sqrt(dx * dx + dy * dy);

            if (rubberBandEl) {
                rubberBandEl.remove();
                rubberBandEl = null;
            }

            // Only process if drag was beyond threshold
            if (dist >= RUBBER_BAND_THRESHOLD) {
                var rect = {
                    left: Math.min(rubberBandStart.x, e.clientX),
                    top: Math.min(rubberBandStart.y, e.clientY),
                    right: Math.max(rubberBandStart.x, e.clientX),
                    bottom: Math.max(rubberBandStart.y, e.clientY)
                };

                if (!e.shiftKey) {
                    clearSelection();
                }

                selectByRubberBand(rect);
                suppressNextSvgClick = true;
                window.setTimeout(function () {
                    suppressNextSvgClick = false;
                }, 50);
            } else {
                // Below threshold: treat as click on empty space
                if (!e.shiftKey) {
                    clearSelection();
                }
            }

            rubberBandStart = null;
        });

        // Right-click → list every selectable element under the pointer, so
        // stacked/overlapping shapes can be reached without blind cycling.
        container.addEventListener("contextmenu", function (e) {
            var svg = svgContent.querySelector("svg");
            if (!svg) return;
            var cands = collectSelectableAt(e.clientX, e.clientY);
            if (cands.length === 0) return;            // nothing here → native menu
            e.preventDefault();
            if (cands.length === 1) { selectElement(cands[0], false); return; }
            showOverlapPicker(e.clientX, e.clientY, cands);
        });

        // Dismiss the picker on any press outside it (item clicks stop their own
        // propagation, so this never fires before a selection is made).
        document.addEventListener("mousedown", function (e) {
            if (overlapPickerEl && !overlapPickerEl.contains(e.target)) {
                closeOverlapPicker();
            }
        });
    }

    function cancelRubberBand() {
        rubberBandStart = null;
        if (rubberBandEl) {
            rubberBandEl.remove();
            rubberBandEl = null;
        }
        var ov = document.getElementById("rubber-band-overlay");
        if (ov) ov.classList.remove("active");
        suppressNextSvgClick = false;
        endDrag();
        closeOverlapPicker();
    }

    function selectByRubberBand(screenRect) {
        var svg = svgContent.querySelector("svg");
        if (!svg) return;

        var selectableEls = svg.querySelectorAll(".svg-selectable");
        selectableEls.forEach(function (el) {
            try {
                var bbox = el.getBBox();
                var ctm = el.getScreenCTM();
                if (!ctm) return;

                // Transform bbox corners to screen coordinates
                var corners = [
                    { x: bbox.x, y: bbox.y },
                    { x: bbox.x + bbox.width, y: bbox.y },
                    { x: bbox.x, y: bbox.y + bbox.height },
                    { x: bbox.x + bbox.width, y: bbox.y + bbox.height }
                ];

                var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
                corners.forEach(function (c) {
                    var sx = c.x * ctm.a + c.y * ctm.c + ctm.e;
                    var sy = c.x * ctm.b + c.y * ctm.d + ctm.f;
                    if (sx < minX) minX = sx;
                    if (sy < minY) minY = sy;
                    if (sx > maxX) maxX = sx;
                    if (sy > maxY) maxY = sy;
                });

                // AABB intersection
                if (minX < screenRect.right && maxX > screenRect.left &&
                    minY < screenRect.bottom && maxY > screenRect.top) {
                    var eid = el.id;
                    if (eid) {
                        selectedElementIds.add(eid);
                        el.classList.add("svg-selected");
                    }
                }
            } catch (err) {
                // getBBox can throw for elements with no geometry
            }
        });

        updateSelectionPanel();
    }

    // ================================================================
    //  Keyboard shortcuts
    // ================================================================
    function initKeyboardShortcuts() {
        document.addEventListener("keydown", function (e) {
            var activeEl = document.activeElement;
            var isTyping = activeEl && (activeEl === annotationText || activeEl === fsNotesEditor ||
                            activeEl.tagName === "INPUT" || activeEl.tagName === "TEXTAREA" || activeEl.tagName === "SELECT");

            // F5 or F key (when not typing) toggles fullscreen
            if (!isTyping && (e.key === "F5" || e.key === "f" || e.key === "F")) {
                e.preventDefault();
                if (isFullscreenMode) {
                    exitFullscreen();
                } else {
                    enterFullscreen();
                }
                return;
            }

            if (isFullscreenMode) {
                // If focus is inside fsNotesEditor, only handle Escape or PageUp/PageDown with Ctrl
                if (activeEl === fsNotesEditor) {
                    if (e.key === "Escape") {
                        e.preventDefault();
                        exitFullscreen();
                        return;
                    }
                } else {
                    if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " " || e.key === "Enter") {
                        e.preventDefault();
                        gotoSlideIndex(currentSlideIndex() + 1);
                        return;
                    } else if (e.key === "ArrowLeft" || e.key === "PageUp" || e.key === "Backspace") {
                        e.preventDefault();
                        gotoSlideIndex(currentSlideIndex() - 1);
                        return;
                    } else if (e.key === "Escape") {
                        e.preventDefault();
                        exitFullscreen();
                        return;
                    }
                }
            }


            // Ctrl+Z / Cmd+Z: drop the last staged edit. Let inputs/selects handle
            // their own native undo when focused.
            if ((e.ctrlKey || e.metaKey) && (e.key === "z" || e.key === "Z")) {
                var ae = document.activeElement;
                if (ae && (ae === annotationText || ae.tagName === "INPUT" ||
                           ae.tagName === "TEXTAREA" || ae.tagName === "SELECT")) {
                    return;
                }
                e.preventDefault();
                runUndo();
                return;
            }

            // Ctrl+A / Cmd+A: select all elements
            if ((e.ctrlKey || e.metaKey) && e.key === "a") {
                var _f = document.activeElement;
                if (_f && (_f.tagName === "INPUT" || _f.tagName === "TEXTAREA" || _f.tagName === "SELECT")) return;

                e.preventDefault();
                var svg = svgContent.querySelector("svg");
                if (!svg) return;

                svg.querySelectorAll(".svg-selectable").forEach(function (el) {
                    var eid = el.id;
                    if (eid) {
                        selectedElementIds.add(eid);
                        el.classList.add("svg-selected");
                    }
                });
                updateSelectionPanel();
            }

            // Delete/Backspace: delete selected elements when not typing.
            if (e.key === "Delete" || e.key === "Backspace") {
                var focusedEl = document.activeElement;
                if (focusedEl && (focusedEl === annotationText || focusedEl.tagName === "INPUT" ||
                        focusedEl.tagName === "TEXTAREA" || focusedEl.tagName === "SELECT")) {
                    return;
                }
                if (selectedElementIds.size > 0) {
                    e.preventDefault();
                    if (e.shiftKey) {
                        deleteSelectedParentsOrElements();
                    } else {
                        deleteSelectedElements();
                    }
                    return;
                }
            }

            // Escape: close annotation popover first, then overlap picker, then clear selection.
            if (e.key === "Escape") {
                if (popoverOverlay && popoverOverlay.style.display !== "none") {
                    hideAnnotationPopover();
                    return;
                }
                if (document.activeElement === annotationText) return;
                if (overlapPickerEl) { closeOverlapPicker(); return; }
                clearSelection();
            }

            // N key (when not typing): toggle speaker notes tab
            if (!isTyping && (e.key === "n" || e.key === "N")) {
                e.preventDefault();
                switchTab(notesMode ? "slides" : "notes");
                return;
            }

            // Tab: open annotation popover for current selection or whole page
            if (e.key === "Tab") {
                if (popoverOverlay && popoverOverlay.style.display !== "none") return;
                var ae = document.activeElement;
                if (ae && (ae.tagName === "INPUT" || ae.tagName === "TEXTAREA" || ae.tagName === "SELECT")) return;
                e.preventDefault();
                if (selectedElementIds.size > 0) {
                    showAnnotationPopover(Array.from(selectedElementIds), false);
                } else if (currentSlide) {
                    showAnnotationPopover(["__page__"], true);
                }
                return;
            }


            // Slide navigation: ArrowLeft/Right + Home/End (skip while typing)
            var _ae = document.activeElement;
            if (_ae && (_ae.tagName === "INPUT" || _ae.tagName === "TEXTAREA" || _ae.tagName === "SELECT")) return;
            if (e.ctrlKey || e.metaKey || e.altKey) return;

            // Arrow keys nudge the selection (1px, Shift = 10px) instead of
            // navigating slides whenever something is selected.
            if (selectedElementIds.size > 0 &&
                (e.key === "ArrowLeft" || e.key === "ArrowRight" ||
                 e.key === "ArrowUp" || e.key === "ArrowDown")) {
                e.preventDefault();
                var step = e.shiftKey ? 10 : 1;
                var nx = e.key === "ArrowLeft" ? -step : e.key === "ArrowRight" ? step : 0;
                var ny = e.key === "ArrowUp" ? -step : e.key === "ArrowDown" ? step : 0;
                nudgeSelection(nx, ny);
                return;
            }

            if (slideNames.length === 0) return;

            if (e.key === "ArrowLeft") {
                e.preventDefault();
                gotoSlideIndex(currentSlideIndex() - 1);
            } else if (e.key === "ArrowRight") {
                e.preventDefault();
                gotoSlideIndex(currentSlideIndex() + 1);
            } else if (e.key === "Home") {
                e.preventDefault();
                gotoSlideIndex(0);
            } else if (e.key === "End") {
                e.preventDefault();
                gotoSlideIndex(slideNames.length - 1);
            }
        });
    }

    function initSlideNav() {
        if (navFirstBtn) navFirstBtn.addEventListener("click", function () { gotoSlideIndex(0); });
        if (navPrevBtn)  navPrevBtn.addEventListener("click", function ()  { gotoSlideIndex(currentSlideIndex() - 1); });
        if (navNextBtn)  navNextBtn.addEventListener("click", function ()  { gotoSlideIndex(currentSlideIndex() + 1); });
        if (navLastBtn)  navLastBtn.addEventListener("click", function ()  { gotoSlideIndex(slideNames.length - 1); });

        if (navPlayBtn)  navPlayBtn.addEventListener("click", enterFullscreen);
        if (fsNavPrev)   fsNavPrev.addEventListener("click", function () { gotoSlideIndex(currentSlideIndex() - 1); });
        if (fsNavNext)   fsNavNext.addEventListener("click", function () { gotoSlideIndex(currentSlideIndex() + 1); });
        if (fsBtnExit)   fsBtnExit.addEventListener("click", exitFullscreen);

        if (slideListEl) {
            slideListEl.setAttribute("tabindex", "0");
            slideListEl.addEventListener("keydown", function (e) {
                if (e.key === "ArrowUp" || e.key === "ArrowDown") {
                    e.preventDefault();
                    var idx = currentSlideIndex();
                    var next = e.key === "ArrowUp" ? idx - 1 : idx + 1;
                    gotoSlideIndex(next);
                }
            });
        }
    }

    // ================================================================
    //  Notes tab (left panel)
    // ================================================================
    function setNotesDirty(dirty) {
        notesDirty = dirty;
        if (btnNotesSave) btnNotesSave.style.display = dirty ? "" : "none";
    }

    function loadCurrentNotes() {
        if (!notesContentEl && !fsNotesEditor) return;
        if (!currentSlide) {
            if (notesContentEl) {
                notesContentEl.value = "";
                notesContentEl.placeholder = t("notes_none");
            }
            if (fsNotesEditor) {
                fsNotesEditor.value = "";
                fsNotesEditor.placeholder = t("notes_none");
            }
            _notesLoadedText = "";
            setNotesDirty(false);
            if (fsNotesContent) fsNotesContent.textContent = t("notes_none");
            return;
        }
        if (notesContentEl) {
            notesContentEl.placeholder = t("notes_loading");
            notesContentEl.value = "";
        }
        if (fsNotesEditor) {
            fsNotesEditor.placeholder = t("notes_loading");
            fsNotesEditor.value = "";
        }
        _notesLoadedText = "";
        setNotesDirty(false);
        if (fsNotesContent) fsNotesContent.textContent = t("notes_loading");
        fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/notes")
            .then(function (r) { return r.json(); })
            .then(function (data) {
                var text = (data.notes || "").trim();
                if (notesContentEl) {
                    notesContentEl.value = text;
                    notesContentEl.placeholder = t("notes_none");
                }
                if (fsNotesEditor) {
                    fsNotesEditor.value = text;
                    fsNotesEditor.placeholder = t("notes_none");
                }
                _notesLoadedText = text;
                setNotesDirty(false);
                if (fsNotesContent) fsNotesContent.textContent = text || t("notes_none");
            })
            .catch(function () {
                if (notesContentEl) {
                    notesContentEl.value = "";
                    notesContentEl.placeholder = t("notes_none");
                }
                if (fsNotesEditor) {
                    fsNotesEditor.value = "";
                    fsNotesEditor.placeholder = t("notes_none");
                }
                if (fsNotesContent) fsNotesContent.textContent = t("notes_none");
            });
    }

    function saveCurrentNotes(silent) {
        if (!currentSlide) return Promise.resolve();
        var text = notesContentEl ? notesContentEl.value : (fsNotesEditor ? fsNotesEditor.value : "");
        return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/notes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes: text })
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            _notesLoadedText = text;
            if (data && data.notes_mtime !== undefined) {
                notesMtimes[currentSlide] = data.notes_mtime;
            }
            if (!silent && btnNotesSave) {
                var orig = btnNotesSave.textContent;
                btnNotesSave.textContent = "✓";
                setTimeout(function () {
                    setNotesDirty(false);
                    btnNotesSave.textContent = orig;
                }, 700);
            } else {
                setNotesDirty(false);
            }
        })
        .catch(function (err) {
            if (!silent) showError(t("err_save") + (err.message || err));
        });
    }

    function switchTab(mode) {
        notesMode = (mode === "notes");
        if (tabSlides) tabSlides.classList.toggle("active", !notesMode);
        if (tabNotes) tabNotes.classList.toggle("active", notesMode);
        if (slideListEl) slideListEl.style.display = notesMode ? "none" : "";
        if (notesContentEl) notesContentEl.style.display = notesMode ? "" : "none";
        if (!notesMode) setNotesDirty(false);
        if (notesMode) loadCurrentNotes();
    }

    function initNotes() {
        if (tabSlides) {
            tabSlides.addEventListener("click", function () {
                if (notesMode && notesDirty) saveCurrentNotes(true);
                switchTab("slides");
            });
        }
        if (tabNotes) {
            tabNotes.addEventListener("click", function () {
                switchTab("notes");
            });
        }
        if (notesContentEl) {
            notesContentEl.addEventListener("input", function () {
                if (fsNotesEditor) fsNotesEditor.value = notesContentEl.value;
                setNotesDirty(notesContentEl.value !== _notesLoadedText);
            });
        }
        if (fsNotesEditor) {
            fsNotesEditor.addEventListener("input", function () {
                if (notesContentEl) notesContentEl.value = fsNotesEditor.value;
                setNotesDirty(fsNotesEditor.value !== _notesLoadedText);
            });
            fsNotesEditor.addEventListener("blur", function () {
                if (notesDirty) saveCurrentNotes(true);
            });
        }
        if (btnNotesSave) {
            btnNotesSave.addEventListener("click", function () {
                saveCurrentNotes(false);
            });
        }
    }


    // ================================================================
    //  Annotation popover
    // ================================================================
    function showAnnotationPopover(targetIds, isPage) {
        if (!popoverOverlay) return;
        _popoverTargetIds = targetIds;
        _popoverSelectedChips.clear();
        _popoverIsPage = isPage;

        if (isPage) {
            popoverTitle.textContent = "🤖 " + t("popover_title_page");
        } else if (targetIds.length === 1) {
            var el = svgContent.querySelector("#" + CSS.escape(targetIds[0]));
            if (el) {
                var tag = el.tagName.toLowerCase();
                popoverTitle.textContent = "🤖 " + t("label_agent_point") + " <" + tag + "> #" + targetIds[0];
            } else {
                popoverTitle.textContent = "🤖 " + t("label_agent_point") + " #" + targetIds[0];
            }
        } else {
            popoverTitle.textContent = "🤖 " + t("label_agent_point") + " (" + targetIds.length + ")";
        }

        renderPopoverChips();

        if (!isPage && targetIds.length === 1 && slideAnnotations[targetIds[0]]) {
            popoverText.value = slideAnnotations[targetIds[0]];
        } else if (isPage && slideAnnotations["__page__"]) {
            popoverText.value = slideAnnotations["__page__"];
        } else {
            popoverText.value = "";
        }
        popoverText.placeholder = t("popover_placeholder");
        if (popoverSubmit) {
            popoverSubmit.textContent = t("btn_add_point");
        }

        popoverOverlay.style.display = "flex";
        setTimeout(function () { popoverText.focus(); }, 50);
    }

    function hideAnnotationPopover() {
        if (!popoverOverlay) return;
        popoverOverlay.style.display = "none";
        _popoverTargetIds = [];
        _popoverSelectedChips.clear();
    }

    function renderPopoverChips() {
        if (!popoverChips) return;
        popoverChips.innerHTML = "";
        QUICK_ISSUES.forEach(function (issue, idx) {
            var chip = document.createElement("button");
            chip.className = "popover-chip";
            chip.type = "button";
            chip.textContent = issue[LANG] || issue.en;
            chip.addEventListener("click", function () {
                if (_popoverSelectedChips.has(idx)) {
                    _popoverSelectedChips.delete(idx);
                    chip.classList.remove("selected");
                } else {
                    _popoverSelectedChips.add(idx);
                    chip.classList.add("selected");
                }
            });
            popoverChips.appendChild(chip);
        });
    }

    function submitAnnotation(ids, text) {
        if (!currentSlide || !text) return;
        var promises = ids.map(function (eid) {
            return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/annotate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ element_id: eid, annotation: text })
            }).then(jsonOrThrow);
        });
        Promise.all(promises)
            .then(function () {
                ids.forEach(function (eid) { slideAnnotations[eid] = text; });
                annotationsDirty = true;
                refreshAnnotationVisuals();
                updateAnnotationList();
                loadSlides();
            })
            .catch(function (err) {
                showError(t("err_add_annotation") + err.message);
            });
    }

    function initAnnotationPopover() {
        if (popoverClose) {
            popoverClose.addEventListener("click", hideAnnotationPopover);
        }
        if (popoverOverlay) {
            popoverOverlay.addEventListener("click", function (e) {
                if (e.target === popoverOverlay) hideAnnotationPopover();
            });
        }
        if (popoverSubmit) {
            popoverSubmit.addEventListener("click", function () {
                var parts = [];
                QUICK_ISSUES.forEach(function (issue, idx) {
                    if (_popoverSelectedChips.has(idx)) {
                        parts.push(issue[LANG] || issue.en);
                    }
                });
                var custom = popoverText.value.trim();
                if (custom) parts.push(custom);
                var text = parts.join("; ");
                if (!text) return;
                var targetId = (_popoverTargetIds && _popoverTargetIds.length > 0)
                    ? _popoverTargetIds[0]
                    : (currentAgentTarget || "__page__");
                addSlideTaskWithText(text, targetId);
                hideAnnotationPopover();
            });
        }
        if (popoverText) {
            popoverText.addEventListener("keydown", function (e) {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    if (popoverSubmit) popoverSubmit.click();
                }
            });
        }
        if (btnPageAnnotate) {
            btnPageAnnotate.addEventListener("click", function () {
                if (!currentSlide) return;
                showAnnotationPopover(["__page__"], true);
            });
        }
    }

    // ================================================================
    //  6.  Add annotation  -- POST /api/slide/{name}/annotate
    // ================================================================
    btnAddAnnotation.addEventListener("click", function () {
        if (!currentSlide || selectedElementIds.size === 0) return;

        var text = annotationText.value.trim();
        if (!text) return;

        var ids = Array.from(selectedElementIds);
        var promises = ids.map(function (eid) {
            return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/annotate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ element_id: eid, annotation: text })
            }).then(jsonOrThrow);
        });

        Promise.all(promises)
            .then(function () {
                ids.forEach(function (eid) {
                    slideAnnotations[eid] = text;
                });
                annotationsDirty = true;
                refreshAnnotationVisuals();
                updateAnnotationList();
                annotationText.value = "";
                loadSlides();
            })
            .catch(function (err) {
                console.error("addAnnotation:", err);
                showError(t("err_add_annotation") + err.message);
            });
    });

    // ================================================================
    //  7.  removeAnnotation  -- DELETE /api/slide/{name}/annotate/{id}
    // ================================================================
    function removeAnnotation(elementId) {
        if (!currentSlide) return;

        fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/annotate/" + encodeURIComponent(elementId), {
            method: "DELETE"
        })
            .then(function (res) { return res.json(); })
            .then(function () {
                delete slideAnnotations[elementId];
                annotationsDirty = true;
                refreshAnnotationVisuals();
                updateAnnotationList();
                loadSlides();
            })
            .catch(function (err) {
                console.error("removeAnnotation:", err);
                showError(t("err_remove_annotation") + err.message);
            });
    }

    // ================================================================
    //  8.  refreshAnnotationVisuals
    // ================================================================
    function refreshAnnotationVisuals() {
        // Clear all annotated/deleting marks
        svgContent.querySelectorAll(".svg-annotated, .svg-deleting").forEach(function (el) {
            el.classList.remove("svg-annotated");
            el.classList.remove("svg-deleting");
        });
        // Apply marks — delete annotations get an extra red overlay class
        Object.keys(slideAnnotations).forEach(function (eid) {
            if (eid === "__page__") return;
            var el = svgContent.querySelector("#" + CSS.escape(eid));
            if (el) {
                el.classList.add("svg-annotated");
                if (isDeleteAnnotation(slideAnnotations[eid])) {
                    el.classList.add("svg-deleting");
                }
            }
        });
    }

    // ================================================================
    //  9.  updateAnnotationList
    // ================================================================
    function updateAnnotationList() {
        annotationsEl.innerHTML = "";

        var ids = Object.keys(slideAnnotations);
        if (ids.length === 0) {
            annotationsEl.innerHTML = '<div class="annotations-empty">' + escapeHtml(t("empty_annotations")) + '</div>';
            return;
        }

        ids.forEach(function (eid) {
            var item = document.createElement("div");
            item.className = "annotation-item";

            var header = document.createElement("div");
            header.className = "ann-header";

            var leftSpan = document.createElement("span");
            if (eid === "__page__") {
                var pageSpan = document.createElement("span");
                pageSpan.className = "ann-tag ann-tag-page";
                pageSpan.textContent = t("ann_tag_page");
                leftSpan.appendChild(pageSpan);
            } else {
                var tag = "";
                var el = svgContent.querySelector("#" + CSS.escape(eid));
                if (el) tag = el.tagName.toLowerCase();
                if (tag) {
                    var tagSpan = document.createElement("span");
                    tagSpan.className = "ann-tag";
                    tagSpan.textContent = "<" + tag + ">";
                    leftSpan.appendChild(tagSpan);
                }
                var idSpan = document.createElement("span");
                idSpan.className = "ann-id";
                idSpan.textContent = eid;
                leftSpan.appendChild(idSpan);
            }

            header.appendChild(leftSpan);

            var removeBtn = document.createElement("button");
            removeBtn.className = "ann-remove";
            removeBtn.innerHTML = "&times;";
            removeBtn.title = t("tooltip_remove_annotation");
            removeBtn.addEventListener("click", function () {
                removeAnnotation(eid);
            });
            header.appendChild(removeBtn);

            item.appendChild(header);

            var annText = slideAnnotations[eid];
            if (isDeleteAnnotation(annText)) {
                item.classList.add("ann-item-delete");
            }

            var textDiv = document.createElement("div");
            textDiv.className = "ann-text";
            textDiv.textContent = annText;
            item.appendChild(textDiv);

            annotationsEl.appendChild(item);
        });
    }

    // ================================================================
    // 10.  Save all  -- two-step: confirm then save
    // ================================================================
    btnSave.addEventListener("click", function () {
        pendingModalAction = "submit";
        hideModalPrompt();
        modalMessage.textContent = t("modal_confirm_submit");
        modalConfirm.textContent = t("modal_submit");
        modalConfirm.style.display = "";
        modalCancel.style.display = "";
        modalOverlay.style.display = "flex";
    });

    btnExitPreview.addEventListener("click", function () {
        pendingModalAction = "exit";
        hideModalPrompt();
        modalMessage.textContent = t("modal_confirm_exit");
        modalConfirm.textContent = t("btn_exit_preview");
        modalConfirm.style.display = "";
        modalCancel.style.display = "";
        modalOverlay.style.display = "flex";
    });


    modalConfirm.addEventListener("click", function () {
        if (pendingModalAction === "exit") {
            modalConfirm.style.display = "none";
            modalCancel.style.display = "none";
            modalMessage.textContent = t("modal_stopping");
            fetch("/api/shutdown", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ reason: "exit-preview" })
            })
                .then(function () {
                    modalMessage.textContent = t("modal_success_exit");
                })
                .catch(function () {
                    modalMessage.textContent = t("modal_success_exit");
                });
            return;
        }

        // Step 2: save annotations. Service lifetime is controlled only by Exit preview.
        modalConfirm.style.display = "none";
        modalCancel.style.display = "none";

        // Wait for any just-fired direct edits (drag/nudge) to land first, or
        // save-all could race ahead and leave their edits as a fresh pending set.
        drainDirectEdits()
            .then(function () { return fetch("/api/save-all", { method: "POST" }); })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.error) {
                    modalMessage.textContent = t("err_save") + data.error;
                } else {
                    modalMessage.textContent = t("modal_success_submit");
                    showAnnotationPrompt(data.annotation_files || []);
                    editStackCount = {};
                    savedHintShown = false;
                    annotationsDirty = false;
                    updateUndoButton();
                    var activeSlide = currentSlide;
                    loadSlides().then(function () {
                        if (activeSlide) {
                            var item = slideListEl.querySelector('.slide-item[data-name="' + cssAttr(activeSlide) + '"]');
                            selectSlide(activeSlide, item || undefined);
                        }
                    });
                }
            })
            .catch(function (err) {
                modalMessage.textContent = t("err_save") + err;
                modalConfirm.style.display = "";
                modalCancel.style.display = "";
            });
    });

    modalCancel.addEventListener("click", function () {
        modalConfirm.textContent = t("modal_submit");
        hideModalPrompt();
        modalOverlay.style.display = "none";
    });

    // Close modal on overlay click
    modalOverlay.addEventListener("click", function (e) {
            if (e.target === modalOverlay) {
                modalConfirm.textContent = t("modal_submit");
                hideModalPrompt();
                modalOverlay.style.display = "none";
            }
        });

    if (modalPromptText) {
        modalPromptText.addEventListener("click", function () {
            var text = modalPromptText.textContent || "";
            if (!text) return;
            copyTextToClipboard(text).then(function () {
                if (modalPromptLabel) modalPromptLabel.textContent = t("modal_prompt_copied");
            }).catch(function () {
                // Clipboard can be blocked outside secure contexts; keep the text selectable.
            });
        });
    }

    // ================================================================
    //  Utility
    // ================================================================
    function sanitizeSvg(svgString) {
        var doc = new DOMParser().parseFromString(svgString, "image/svg+xml");
        doc.querySelectorAll("script,foreignObject").forEach(function (el) { el.remove(); });
        doc.querySelectorAll("*").forEach(function (el) {
            Array.from(el.attributes).forEach(function (attr) {
                if (attr.name.indexOf("on") === 0) el.removeAttribute(attr.name);
                // Strip dangerous URI protocols from href/xlink:href
                if ((attr.name === "href" || attr.name === "xlink:href") &&
                    (/^\s*javascript\s*:/i.test(attr.value) ||
                     /^\s*data\s*:/i.test(attr.value))) {
                    el.removeAttribute(attr.name);
                }
            });
        });
        return new XMLSerializer().serializeToString(doc.documentElement);
    }

    function showError(msg) {
        var banner = document.createElement("div");
        banner.style.cssText = "position:fixed;top:0;left:0;right:0;padding:10px 16px;background:#ef4444;color:#fff;font-size:13px;text-align:center;z-index:999;cursor:pointer;";
        banner.textContent = msg;
        banner.onclick = function () { banner.remove(); };
        document.body.appendChild(banner);
        setTimeout(function () { banner.remove(); }, 5000);
    }

    function showWarning(msg) {
        // Amber, non-fatal counterpart to showError. Stacks below an existing
        // error banner because z-index is identical and DOM order wins.
        var banner = document.createElement("div");
        banner.style.cssText = "position:fixed;top:38px;left:0;right:0;padding:8px 16px;background:#f59e0b;color:#1f1300;font-size:12px;text-align:center;z-index:998;cursor:pointer;";
        banner.textContent = msg;
        banner.onclick = function () { banner.remove(); };
        document.body.appendChild(banner);
        setTimeout(function () { banner.remove(); }, 6000);
    }

    function showReloadBanner(name) {
        // Singleton: replace any prior banner so we never stack reloads.
        hideReloadBanner();
        var banner = document.createElement("div");
        banner.id = "reload-banner";
        banner.style.cssText = "position:fixed;top:0;left:0;right:0;padding:10px 16px;background:#2563eb;color:#fff;font-size:13px;text-align:center;z-index:1000;cursor:pointer;";
        banner.textContent = t("reload_banner");
        banner.onclick = function () {
            hideReloadBanner();
            // Re-fetch via selectSlide so all post-load logic (annotation merge,
            // warnings, mtime update) runs the same way as a manual click.
            var item = slideListEl.querySelector('.slide-item[data-name="' + cssAttr(name) + '"]');
            selectSlide(name, item || undefined);
        };
        document.body.appendChild(banner);
        reloadBannerEl = banner;
    }

    function hideReloadBanner() {
        if (reloadBannerEl) {
            reloadBannerEl.remove();
            reloadBannerEl = null;
        }
    }

    function escapeHtml(str) {
        var d = document.createElement("div");
        d.appendChild(document.createTextNode(str));
        return d.innerHTML;
    }

    function jsonOrThrow(res) {
        return res.json().then(function (data) {
            if (!res.ok || data.error) {
                throw new Error(data.error || ("Request failed with status " + res.status));
            }
            return data;
        });
    }

    function loadConfig() {
        return fetch("/api/config")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                liveMode = !!data.live;
            })
            .catch(function () {
                liveMode = false;
            });
    }

    function startSlidePolling() {
        if (slidePollTimer) return;
        slidePollTimer = window.setInterval(function () {
            loadSlides();
            checkAgentStatus();
        }, 1500);
    }

    // ---- Direct-edit undo + save hint --------------------------------
    function updateUndoButton() {
        if (!btnUndo) return;
        var n = (currentSlide && editStackCount[currentSlide]) || 0;
        btnUndo.disabled = n === 0;
        btnUndo.textContent = n > 0 ? (t("btn_undo") + " (" + n + ")") : t("btn_undo");
    }

    function runUndo() {
        if (!currentSlide) return;
        fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/undo", { method: "POST" })
            .then(jsonOrThrow)
            .then(function (data) {
                if (data.status === "empty") {
                    editStackCount[currentSlide] = 0;
                    updateUndoButton();
                    showWarning(t("undo_empty"));
                    return;
                }
                if (data.undo_depth !== undefined) {
                    editStackCount[currentSlide] = data.undo_depth;
                    updateUndoButton();
                }
                if (data.mtime !== undefined && data.mtime !== null) {
                    slideMtimes[currentSlide] = data.mtime;
                }
                // Reload the page so the canvas reflects the reverted SVG
                var item = slideListEl.querySelector('.slide-item[data-name="' + cssAttr(currentSlide) + '"]');
                selectSlide(currentSlide, item || undefined);
                flashLiveSave();
                showWarning(t("undo_done"));
            })
            .catch(function (err) {
                showError(t("err_edit") + err.message);
            });
    }

    function maybeShowSavedHint() {
        if (savedHintShown) return;
        savedHintShown = true;
        showWarning(t("edit_saved_hint"));
    }

    // ================================================================
    //  Delete selected elements  (direct edit: immediately deletes
    //  the element from disk and removes it from the canvas)
    // ================================================================
    function deleteSelectedElements() {
        if (!currentSlide || selectedElementIds.size === 0) return;
        var ids = Array.from(selectedElementIds);

        var promises = ids.map(function (eid) {
            return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/edit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ element_id: eid, delete: true })
            }).then(jsonOrThrow);
        });

        Promise.all(promises)
            .then(function () {
                ids.forEach(function (eid) {
                    var el = svgContent.querySelector("#" + CSS.escape(eid));
                    if (el) el.remove();
                    selectedElementIds.delete(eid);
                });
                clearSelection();
            })
            .catch(function (err) {
                showError((t("err_delete") || "删除失败: ") + err.message);
            });
    }

    // Cascade delete: deletes the parent group (card/block) of selected elements
    function deleteSelectedParentsOrElements() {
        if (!currentSlide || selectedElementIds.size === 0) return;
        var targetIds = new Set();
        selectedElementIds.forEach(function (eid) {
            var el = svgContent.querySelector("#" + CSS.escape(eid));
            var pg = nearestParentGroup(el);
            if (pg && pg.id) {
                targetIds.add(pg.id);
            } else {
                targetIds.add(eid);
            }
        });
        var ids = Array.from(targetIds);

        var promises = ids.map(function (tid) {
            return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/edit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ element_id: tid, delete: true })
            }).then(jsonOrThrow);
        });

        Promise.all(promises)
            .then(function () {
                ids.forEach(function (tid) {
                    var el = svgContent.querySelector("#" + CSS.escape(tid));
                    if (el) el.remove();
                });
                selectedElementIds.clear();
                clearSelection();
            })
            .catch(function (err) {
                showError((t("err_delete") || "级联删除失败: ") + err.message);
            });
    }

    // ================================================================
    //  Property extraction & rendering
    // ================================================================
    // Editable property panel for a single selected element: computed geometry,
    // text content where safe, and the element's own SVG attributes.
    function renderEditableProps(el) {
        var tag = localName(el);
        var isGroup = tag === "g";
        var html = '<div class="prop-caption">' +
            escapeHtml(isGroup ? t("label_group_edit") : t("label_direct_edit")) + '</div>';

        var parentGroup = nearestParentGroup(el);
        if (parentGroup && !isGroup) {
            html += '<table class="prop-table"><tr><td class="prop-key">group</td><td class="prop-val">' +
                '<button type="button" class="btn-select-group" data-group-id="' +
                escapeHtml(parentGroup.id) + '">' + escapeHtml(t("btn_select_group")) +
                '</button></td></tr></table>';
        }

        html += '<div class="prop-section">' + escapeHtml(t("section_geometry")) + '</div>';
        html += '<table class="prop-table">';
        // Geometry: position + size in render coords — editable, folded into
        // the element's transform matrix on commit (works for any element type).
        try {
            var rb = computeRenderBox(el);
            html += '<tr><td class="prop-key">position</td><td class="prop-val geo-cell">' +
                '<input type="number" class="prop-edit prop-edit-geo" data-geo="x" value="' + Math.round(rb.x) + '">' +
                '<input type="number" class="prop-edit prop-edit-geo" data-geo="y" value="' + Math.round(rb.y) + '">' +
                '</td></tr>';
            html += '<tr><td class="prop-key">size</td><td class="prop-val geo-cell">' +
                '<input type="number" class="prop-edit prop-edit-geo" data-geo="w" min="1" value="' + Math.round(rb.w) + '">' +
                '<input type="number" class="prop-edit prop-edit-geo" data-geo="h" min="1" value="' + Math.round(rb.h) + '">' +
                '</td></tr>';
        } catch (e) { /* no geometry */ }
        html += '</table>';

        html += '<div class="prop-section">' + escapeHtml(t("section_raw_attrs")) + '</div>';
        html += '<table class="prop-table">';
        ownAttributeSpecs(el).forEach(function (spec) {
            html += '<tr><td class="prop-key">' + escapeHtml(spec.key) + '</td><td class="prop-val">';
            if (!spec.editable) {
                html += '<span class="prop-ro">' + escapeHtml(spec.value) + '</span>';
            } else {
                html += renderAttributeControl(spec);
            }
            html += '</td></tr>';
        });
        html += '</table>';

        // L1: text content — placed at the bottom so it has ample space for extensive text.
        if (tag === "text" || tag === "tspan") {
            html += '<div class="prop-section">' + escapeHtml(t("section_text_style")) + '</div>';
            if (el.querySelector("tspan")) {
                html += '<div class="prop-note" style="padding: 6px 0;">' +
                    escapeHtml(t("prop_multiline_hint")) + '</div>';
            } else {
                html += '<div class="prop-content-block">' +
                    '<textarea class="prop-edit prop-edit-content" rows="6" placeholder="' +
                    escapeHtml(t("prop_content_placeholder")) + '">' +
                    escapeHtml(el.textContent || "") + '</textarea></div>';
            }
        }

        html += '<div class="prop-section" style="margin-top: 16px; border-top: 1px solid var(--border, #334155); padding-top: 12px;">' + (LANG === "zh" ? "快捷操作" : "Actions") + '</div>';
        if (parentGroup && !isGroup) {
            var childCount = parentGroup.querySelectorAll("*").length;
            html += '<div style="padding: 4px 0 6px 0;"><button type="button" class="btn-direct-delete-group" style="width: 100%; padding: 10px 12px; background: #dc2626; color: #ffffff; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.15s;" onmouseover="this.style.background=\'#b91c1c\'" onmouseout="this.style.background=\'#dc2626\'">' +
                (LANG === "zh" ? "💥 级联删除所属整组卡片 (含 " + childCount + " 个元素)" : "💥 Delete Entire Group (" + childCount + " items)") +
                '</button></div>';
            html += '<div style="padding: 0 0 8px 0;"><button type="button" class="btn-direct-delete" style="width: 100%; padding: 8px 12px; background: #334155; color: #f8fafc; border: 1px solid #475569; border-radius: 6px; font-size: 13px; font-weight: normal; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; transition: background 0.15s;" onmouseover="this.style.background=\'#475569\'" onmouseout="this.style.background=\'#334155\'">' +
                (LANG === "zh" ? "🗑️ 仅删除当前选中的单个元素" : "🗑️ Delete Only This Item") +
                '</button></div>';
            html += '<div style="font-size: 12px; color: #94a3b8; text-align: center; margin-bottom: 8px;">' +
                (LANG === "zh" ? "快捷键：<kbd style=\"background:#1e293b;padding:2px 4px;border-radius:3px;\">Shift + Del</kbd> 删整组，<kbd style=\"background:#1e293b;padding:2px 4px;border-radius:3px;\">Del</kbd> 删单个" : "Tip: Shift+Del deletes group, Del deletes item") +
                '</div>';
        } else if (isGroup) {
            var groupChildren = el.querySelectorAll("*").length;
            html += '<div style="padding: 4px 0 12px 0;"><button type="button" class="btn-direct-delete" style="width: 100%; padding: 10px 12px; background: #dc2626; color: #ffffff; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.15s;" onmouseover="this.style.background=\'#b91c1c\'" onmouseout="this.style.background=\'#dc2626\'">' +
                (LANG === "zh" ? "💥 删除此分组及所有子元素 (含 " + groupChildren + " 个)" : "💥 Delete Group & All Children (" + groupChildren + ")") +
                '</button></div>';
        } else {
            html += '<div style="padding: 4px 0 12px 0;"><button type="button" class="btn-direct-delete" style="width: 100%; padding: 10px 12px; background: #dc2626; color: #ffffff; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.15s;" onmouseover="this.style.background=\'#b91c1c\'" onmouseout="this.style.background=\'#dc2626\'">' +
                (LANG === "zh" ? "🗑️ 删除此元素 (Delete)" : "🗑️ Delete Element") +
                '</button></div>';
        }

        return html;
    }

    function nearestParentGroup(el) {
        var node = el ? el.parentElement : null;
        while (node && node !== svgContent) {
            if (node.tagName && localName(node) === "g" && node.id) return node;
            node = node.parentElement;
        }
        return null;
    }

    function ownAttributeSpecs(el) {
        var specs = [];
        Array.from(el.attributes).forEach(function (attr) {
            var key = attr.name;
            if (key === "class" || key === "data-edit-target" || key === "data-edit-annotation") return;
            specs.push({
                key: key,
                value: attr.value,
                editable: isEditableAttributeName(key)
            });
        });
        return specs;
    }

    function isEditableAttributeName(key) {
        var k = String(key).toLowerCase();
        if (k === "id" || k === "class" || k === "href" || k === "xlink:href") return false;
        if (k.indexOf("on") === 0) return false;
        return /^[A-Za-z_][A-Za-z0-9_.:-]*$/.test(key);
    }

    function isColorAttribute(key, value) {
        var k = String(key).toLowerCase();
        if (["fill", "stroke", "color", "stop-color", "flood-color", "lighting-color"].indexOf(k) !== -1) {
            return isSafeColor(value);
        }
        return false;
    }

    function renderAttributeControl(spec) {
        if (isColorAttribute(spec.key, spec.value)) {
            return '<input type="color" class="prop-edit prop-edit-color" data-key="' +
                escapeHtml(spec.key) + '" value="' + normalizeHexForPicker(spec.value) + '">' +
                '<input type="text" class="prop-edit prop-edit-color-text" data-key="' +
                escapeHtml(spec.key) + '" value="' + escapeHtml(spec.value) + '">';
        }
        if (spec.value.length > 60 || spec.key === "d" || spec.key === "points" || spec.key === "style") {
            return '<textarea class="prop-edit prop-edit-attr-area" rows="2" data-key="' +
                escapeHtml(spec.key) + '">' + escapeHtml(spec.value) + '</textarea>';
        }
        return '<input type="text" class="prop-edit prop-edit-attr" data-key="' +
            escapeHtml(spec.key) + '" value="' + escapeHtml(spec.value) + '">';
    }

    // ---- Geometry (position/size) helpers ----------------------------
    // Edits fold into the element's own transform matrix so they apply
    // uniformly regardless of how the element is positioned (x/y, cx/cy, d…).

    function computeRenderBox(el) {
        // Local geometry bbox (excludes the element's OWN transform) ...
        var bbox = el.getBBox();
        // ... times the element CTM (includes own + ancestor transforms) =
        // the on-screen box in the svg root user space (= svg_output coords).
        var ctm = el.getCTM();
        if (!ctm) return { x: bbox.x, y: bbox.y, w: bbox.width, h: bbox.height };
        var corners = [
            { x: bbox.x, y: bbox.y },
            { x: bbox.x + bbox.width, y: bbox.y },
            { x: bbox.x, y: bbox.y + bbox.height },
            { x: bbox.x + bbox.width, y: bbox.y + bbox.height }
        ];
        var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        corners.forEach(function (p) {
            var sx = p.x * ctm.a + p.y * ctm.c + ctm.e;
            var sy = p.x * ctm.b + p.y * ctm.d + ctm.f;
            minX = Math.min(minX, sx); minY = Math.min(minY, sy);
            maxX = Math.max(maxX, sx); maxY = Math.max(maxY, sy);
        });
        return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
    }

    function ownMatrix(el) {
        var t = el.transform && el.transform.baseVal;
        if (t && t.numberOfItems) {
            var c = t.consolidate();
            if (c) {
                var m = c.matrix;
                return new DOMMatrix([m.a, m.b, m.c, m.d, m.e, m.f]);
            }
        }
        return new DOMMatrix();
    }

    function parentCTM(el) {
        // parent → svg-root user space; identity when parent is the outer <svg>.
        var p = el.parentNode;
        var pm = (p && p.getCTM) ? p.getCTM() : null;
        return pm ? new DOMMatrix([pm.a, pm.b, pm.c, pm.d, pm.e, pm.f]) : new DOMMatrix();
    }

    function matrixAfterMove(el, rb, nx, ny) {
        // Desired shift in root coords, mapped into parent space (linear part only).
        var pm = parentCTM(el);
        var rx = nx - rb.x, ry = ny - rb.y;
        var det = pm.a * pm.d - pm.b * pm.c || 1;
        var dpx = (pm.d * rx - pm.c * ry) / det;
        var dpy = (-pm.b * rx + pm.a * ry) / det;
        return new DOMMatrix().translate(dpx, dpy).multiply(ownMatrix(el));
    }

    function matrixAfterResize(el, rb, nw, nh) {
        var pm = parentCTM(el);
        var sx = nw / rb.w, sy = nh / rb.h;
        // Anchor = render top-left, mapped to parent coords (full inverse).
        var im = pm.inverse();
        var ax = im.a * rb.x + im.c * rb.y + im.e;
        var ay = im.b * rb.x + im.d * rb.y + im.f;
        return new DOMMatrix()
            .translate(ax, ay).scale(sx, sy).translate(-ax, -ay)
            .multiply(ownMatrix(el));
    }

    function matrixToString(m) {
        var r = function (v) { return Math.round(v * 1e6) / 1e6; };
        var values = [m.a, m.b, m.c, m.d, m.e, m.f].map(r);
        if (!values.every(function (v) { return Number.isFinite(v); })) return null;
        return "matrix(" + values.join(",") + ")";
    }

    function refreshGeoInputs(el, panel) {
        var rb = computeRenderBox(el);
        var vals = { x: Math.round(rb.x), y: Math.round(rb.y), w: Math.round(rb.w), h: Math.round(rb.h) };
        Object.keys(vals).forEach(function (k) {
            var inp = panel.querySelector('.prop-edit-geo[data-geo="' + k + '"]');
            if (inp && document.activeElement !== inp) inp.value = vals[k];
        });
    }

    function normalizeHexForPicker(val) {
        var s = String(val).trim();
        if (/^#[0-9a-fA-F]{6}$/.test(s)) return s;
        if (/^#[0-9a-fA-F]{3}$/.test(s)) {
            return "#" + s[1] + s[1] + s[2] + s[2] + s[3] + s[3];
        }
        return "#000000";
    }

    function isSafeColor(val) {
        // Only allow values that look like CSS colors (hex, rgb, rgba, hsl, named).
        // Reject anything with ; : url @ \ to prevent CSS injection.
        return val.length < 100 && !/[;:@\\]|url\s*\(/i.test(val);
    }

    function splitNumberUnit(value) {
        var m = String(value || "").trim().match(/^(-?\d+(?:\.\d+)?)([A-Za-z%]*)$/);
        if (!m) return null;
        return { num: parseFloat(m[1]), unit: m[2] || "" };
    }

    function shiftedAttrValue(el, key, delta) {
        var parsed = splitNumberUnit(el.getAttribute(key));
        if (!parsed || !Number.isFinite(parsed.num)) return null;
        var next = Math.round((parsed.num + delta) * 1000) / 1000;
        return String(next) + parsed.unit;
    }

    function parentDelta(dx, dy, el) {
        var pm = parentCTM(el);
        var det = pm.a * pm.d - pm.b * pm.c;
        if (Math.abs(det) < 1e-9) return null;
        return {
            x: (pm.d * dx - pm.c * dy) / det,
            y: (-pm.b * dx + pm.a * dy) / det
        };
    }

    function firstNumber(value) {
        var m = String(value || "").match(/-?\d+(?:\.\d+)?/);
        return m ? parseFloat(m[0]) : null;
    }

    function formatCoord(value) {
        return String(Math.round(value * 1000) / 1000);
    }

    function tspanBaseline(tspan) {
        var text = tspan && tspan.parentElement;
        if (!text || localName(text) !== "text") return null;
        var curX = firstNumber(text.getAttribute("x"));
        var curY = firstNumber(text.getAttribute("y"));
        var children = Array.from(text.children);
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
            if (localName(child) !== "tspan") continue;
            var x = firstNumber(child.getAttribute("x"));
            var y = firstNumber(child.getAttribute("y"));
            var dx = firstNumber(child.getAttribute("dx"));
            var dy = firstNumber(child.getAttribute("dy"));
            if (x !== null) curX = x;
            else if (dx !== null) curX = (curX || 0) + dx;
            if (y !== null) curY = y;
            else if (dy !== null) curY = (curY || 0) + dy;
            if (child === tspan) break;
        }
        if (curX === null || curY === null) return null;
        return { x: curX, y: curY };
    }

    function tspanPromotionPayload(tspan) {
        if (localName(tspan) !== "tspan") return null;
        var base = tspanBaseline(tspan);
        if (!base) return null;
        var own = ownMatrix(tspan);
        var close = function (a, b) { return Math.abs(a - b) < 1e-6; };
        if (!close(own.a, 1) || !close(own.b, 0) ||
                !close(own.c, 0) || !close(own.d, 1)) return null;
        return {
            x: formatCoord(base.x + own.e),
            y: formatCoord(base.y + own.f)
        };
    }

    function copyTextAttrs(src, dst, skip) {
        Array.from(src.attributes || []).forEach(function (attr) {
            if (skip[attr.name]) return;
            dst.setAttribute(attr.name, attr.value);
        });
    }

    function adjustedDyValue(oldValue, nextY, prevY) {
        var parsed = splitNumberUnit(oldValue);
        if (!parsed) return formatCoord(nextY - prevY);
        return formatCoord(nextY - prevY) + parsed.unit;
    }

    function promoteTspanDom(tspan, promoted) {
        var text = tspan && tspan.parentElement;
        if (!text || localName(tspan) !== "tspan" || localName(text) !== "text") return null;
        var next = tspan.nextElementSibling;
        var nextBase = next && localName(next) === "tspan" ? tspanBaseline(next) : null;
        var prev = tspan.previousElementSibling;
        var prevBase = prev && localName(prev) === "tspan" ? tspanBaseline(prev) : null;
        var parentBaseY = firstNumber(text.getAttribute("y")) || 0;

        var newText = document.createElementNS(tspan.namespaceURI, "text");
        copyTextAttrs(text, newText, { id: true, x: true, y: true, dx: true, dy: true });
        copyTextAttrs(tspan, newText, {
            id: true, x: true, y: true, dx: true, dy: true, transform: true
        });
        newText.setAttribute("id", tspan.id);
        newText.setAttribute("x", promoted.x);
        newText.setAttribute("y", promoted.y);

        Array.from(tspan.childNodes || []).forEach(function (node) {
            newText.appendChild(node.cloneNode(true));
        });
        if (newText.childNodes.length === 0) {
            newText.textContent = tspan.textContent || "";
        }

        var textParent = text.parentNode;
        var textNext = text.nextSibling;
        var textClone = text.cloneNode(true);
        newText.__promotionRollback = function () {
            if (newText.parentNode) newText.parentNode.removeChild(newText);
            if (text.parentNode) text.parentNode.removeChild(text);
            if (textParent) {
                if (textNext && textNext.parentNode === textParent) {
                    textParent.insertBefore(textClone, textNext);
                } else {
                    textParent.appendChild(textClone);
                }
            }
            selectedElementIds.delete(newText.id);
            selectedElementIds.add(tspan.id);
            markSelection();
            return textClone.querySelector("#" + CSS.escape(tspan.id)) || textClone;
        };

        text.parentNode.insertBefore(newText, text.nextSibling);
        text.removeChild(tspan);
        if (next && nextBase && !next.hasAttribute("y") && next.hasAttribute("dy")) {
            next.setAttribute("dy", adjustedDyValue(
                next.getAttribute("dy"),
                nextBase.y,
                prevBase ? prevBase.y : parentBaseY
            ));
        }
        if (!(text.textContent || "").trim() && text.children.length === 0) {
            text.parentNode.removeChild(text);
        }
        selectedElementIds.delete(tspan.id);
        selectedElementIds.add(newText.id);
        markSelection();
        return newText;
    }

    function payloadForMovedElement(el, attrs) {
        var promoted = tspanPromotionPayload(el);
        if (promoted) return { promote_tspan: promoted };
        return { attrs: attrs };
    }

    function canUseRawGeometry(el) {
        var own = ownMatrix(el);
        var close = function (a, b) { return Math.abs(a - b) < 1e-6; };
        if (close(own.b, 0) && close(own.c, 0)) {
            if (close(own.a, 1) && close(own.d, 1)) return "translate";
            if (localName(el) === "use") return "use-transform";
            if (["rect", "image"].indexOf(localName(el)) !== -1) return "box-transform";
        }
        return "";
    }

    function rawMoveAttrs(el, dx, dy) {
        if (localName(el) === "g" && el.hasAttribute("data-icon") &&
                el.hasAttribute("data-use-x") && el.hasAttribute("data-use-y")) {
            var iconOwn = ownMatrix(el);
            var close = function (a, b) { return Math.abs(a - b) < 1e-6; };
            if (close(iconOwn.b, 0) && close(iconOwn.c, 0)) {
                var iconDelta = parentDelta(dx, dy, el);
                if (iconDelta) {
                    var iconAttrs = {
                        x: formatCoord(iconOwn.e + iconDelta.x),
                        y: formatCoord(iconOwn.f + iconDelta.y)
                    };
                    if (el.hasAttribute("data-use-has-transform")) {
                        iconAttrs.transform = null;
                    }
                    return iconAttrs;
                }
            }
        }

        var rawMode = canUseRawGeometry(el);
        if (!rawMode) return null;
        var d = parentDelta(dx, dy, el);
        if (!d) return null;
        var tag = localName(el);
        var attrs = {};
        var own = ownMatrix(el);
        var add = function (key, delta) {
            if (!el.hasAttribute(key)) return false;
            var next = shiftedAttrValue(el, key, delta);
            if (next === null) return false;
            attrs[key] = next;
            return true;
        };
        var fmt = function (value) {
            return String(Math.round(value * 1000) / 1000);
        };
        var bakeTranslate = function (xKey, yKey) {
            if (!el.hasAttribute(xKey) || !el.hasAttribute(yKey)) return false;
            if (rawMode === "use-transform") {
                attrs[xKey] = fmt(own.e + d.x);
                attrs[yKey] = fmt(own.f + d.y);
                attrs.transform = null;
                return true;
            }
            var nx = shiftedAttrValue(el, xKey, own.e + d.x);
            var ny = shiftedAttrValue(el, yKey, own.f + d.y);
            if (nx === null || ny === null) return false;
            attrs[xKey] = nx;
            attrs[yKey] = ny;
            if (el.hasAttribute("transform")) attrs.transform = null;
            return true;
        };
        var bakeBox = function () {
            if (!el.hasAttribute("x") || !el.hasAttribute("y") ||
                    !el.hasAttribute("width") || !el.hasAttribute("height")) return false;
            var x = splitNumberUnit(el.getAttribute("x"));
            var y = splitNumberUnit(el.getAttribute("y"));
            var w = splitNumberUnit(el.getAttribute("width"));
            var h = splitNumberUnit(el.getAttribute("height"));
            if (!x || !y || !w || !h || x.unit !== y.unit ||
                    x.unit !== w.unit || x.unit !== h.unit) return false;
            attrs.x = fmt(own.a * x.num + own.e + d.x) + x.unit;
            attrs.y = fmt(own.d * y.num + own.f + d.y) + y.unit;
            attrs.width = fmt(Math.abs(own.a) * w.num) + w.unit;
            attrs.height = fmt(Math.abs(own.d) * h.num) + h.unit;
            attrs.transform = null;
            return true;
        };

        if (rawMode === "box-transform") {
            return bakeBox() ? attrs : null;
        }
        if (["rect", "image", "use", "text"].indexOf(tag) !== -1) {
            return bakeTranslate("x", "y") ? attrs : null;
        }
        if (tag === "circle" || tag === "ellipse") {
            return bakeTranslate("cx", "cy") ? attrs : null;
        }
        if (tag === "line") {
            if (add("x1", own.e + d.x) && add("x2", own.e + d.x) &&
                    add("y1", own.f + d.y) && add("y2", own.f + d.y)) {
                if (el.hasAttribute("transform")) attrs.transform = null;
                return attrs;
            }
            return null;
        }
        return null;
    }

    function attrsForMove(el, dx, dy) {
        var attrs = rawMoveAttrs(el, dx, dy);
        if (attrs) return attrs;
        var rb = computeRenderBox(el);
        var moved = matrixAfterMove(el, rb, rb.x + dx, rb.y + dy);
        var tstr = matrixToString(moved);
        return tstr ? { transform: tstr } : null;
    }

    function computeElementsBox(elements) {
        var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        elements.forEach(function (el) {
            var rb = computeRenderBox(el);
            minX = Math.min(minX, rb.x);
            minY = Math.min(minY, rb.y);
            maxX = Math.max(maxX, rb.x + rb.w);
            maxY = Math.max(maxY, rb.y + rb.h);
        });
        return { x: minX, y: minY, w: maxX - minX, h: maxY - minY };
    }

    function topLevelSelectedElements(ids) {
        var els = ids.map(function (eid) {
            return svgContent.querySelector("#" + CSS.escape(eid));
        }).filter(Boolean);
        return els.filter(function (el) {
            return !els.some(function (other) {
                return other !== el && other.contains(el);
            });
        });
    }

    function attachPropEditors(el) {
        var eid = el.id;
        var panel = elementPropsEl;

        var groupBtn = panel.querySelector(".btn-select-group");
        if (groupBtn) {
            groupBtn.addEventListener("click", function () {
                var gid = groupBtn.getAttribute("data-group-id");
                var groupEl = gid ? svgContent.querySelector("#" + CSS.escape(gid)) : null;
                if (groupEl) selectElement(groupEl, false);
            });
        }

        // L1: text content (fires on blur/change).
        var contentBox = panel.querySelector(".prop-edit-content");
        if (contentBox) {
            contentBox.addEventListener("change", function () {
                var newText = contentBox.value;
                stageEditRequest(eid, { text: newText })
                    .then(function () { el.textContent = newText; })
                    .catch(function (err) { showError(t("err_edit") + err.message); });
            });
        }

        // Raw own attributes: color picker + text input stay in sync.
        panel.querySelectorAll(".prop-edit-color").forEach(function (picker) {
            var key = picker.getAttribute("data-key");
            var textInput = panel.querySelector('.prop-edit-color-text[data-key="' + key + '"]');
            picker.addEventListener("input", function () {
                if (textInput) textInput.value = picker.value;
            });
            picker.addEventListener("change", function () {
                stageAttr(el, eid, key, picker.value);
            });
        });
        panel.querySelectorAll(".prop-edit-color-text").forEach(function (textInput) {
            var key = textInput.getAttribute("data-key");
            var picker = panel.querySelector('input.prop-edit-color[data-key="' + key + '"]');
            textInput.addEventListener("change", function () {
                var v = textInput.value.trim();
                if (picker) picker.value = normalizeHexForPicker(v);
                stageAttr(el, eid, key, v);
            });
        });

        panel.querySelectorAll(".prop-edit-attr, .prop-edit-attr-area").forEach(function (input) {
            var key = input.getAttribute("data-key");
            input.addEventListener("change", function () {
                stageAttr(el, eid, key, input.value.trim());
            });
        });

        // Geometry: position (move) + size (resize), folded into the transform.
        if (panel.querySelector(".prop-edit-geo")) {
            var readGeo = function (k) {
                var inp = panel.querySelector('.prop-edit-geo[data-geo="' + k + '"]');
                return inp ? parseFloat(inp.value) : NaN;
            };
            var commitGeo = function (mode) {
                var rb;
                try { rb = computeRenderBox(el); } catch (e) { return; }
                var newM;
                var attrs = null;
                if (mode === "move") {
                    var nx = readGeo("x"), ny = readGeo("y");
                    if (isNaN(nx) || isNaN(ny)) return;
                    if (Math.abs(nx - rb.x) < 1e-6 && Math.abs(ny - rb.y) < 1e-6) return;
                    attrs = attrsForMove(el, nx - rb.x, ny - rb.y);
                    if (!attrs) newM = matrixAfterMove(el, rb, nx, ny);
                } else {
                    var nw = readGeo("w"), nh = readGeo("h");
                    if (isNaN(nw) || isNaN(nh) || nw <= 0 || nh <= 0 || rb.w <= 0 || rb.h <= 0) {
                        showError(t("err_edit") + "size");
                        return;
                    }
                    if (Math.abs(nw - rb.w) < 1e-6 && Math.abs(nh - rb.h) < 1e-6) return;
                    newM = matrixAfterResize(el, rb, nw, nh);
                }
                if (!attrs) {
                    var tstr = matrixToString(newM);
                    if (!tstr) {
                        showError(t("err_edit") + "transform");
                        return;
                    }
                    attrs = { transform: tstr };
                }
                var payload = mode === "move" ? payloadForMovedElement(el, attrs) : { attrs: attrs };
                stageEditRequest(eid, payload)
                    .then(function () {
                    if (payload.promote_tspan) {
                        el = promoteTspanDom(el, payload.promote_tspan) || el;
                    } else {
                        applyElementAttrs(el, attrs);
                        markCommittedAttrs(el, attrs);
                    }
                    refreshGeoInputs(el, panel);
                    })
                    .catch(function (err) { showError(t("err_edit") + err.message); });
            };
            panel.querySelectorAll('.prop-edit-geo[data-geo="x"], .prop-edit-geo[data-geo="y"]').forEach(function (inp) {
                inp.addEventListener("change", function () { commitGeo("move"); });
            });
            panel.querySelectorAll('.prop-edit-geo[data-geo="w"], .prop-edit-geo[data-geo="h"]').forEach(function (inp) {
                inp.addEventListener("change", function () { commitGeo("resize"); });
            });
        }
        var parentGroup = nearestParentGroup(el);
        var delGroupBtn = panel.querySelector(".btn-direct-delete-group");
        if (delGroupBtn && parentGroup) {
            delGroupBtn.addEventListener("click", function () {
                var cCount = parentGroup.querySelectorAll("*").length;
                if (!confirm(LANG === "zh" ? "确定要级联删除整张卡片/父分组（含 " + cCount + " 个元素）吗？" : "Delete entire group and all " + cCount + " items?")) return;
                fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/edit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ element_id: parentGroup.id, delete: true })
                }).then(jsonOrThrow)
                .then(function () {
                    parentGroup.remove();
                    selectedElementIds.clear();
                    clearSelection();
                })
                .catch(function (err) {
                    showError((LANG === "zh" ? "级联删除失败: " : "Cascade delete failed: ") + err.message);
                });
            });
        }
        var deleteBtn = panel.querySelector(".btn-direct-delete");
        if (deleteBtn) {
            deleteBtn.addEventListener("click", function () {
                if (!confirm(LANG === "zh" ? "确定要删除此元素吗？" : "Are you sure you want to delete this element?")) return;
                fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/edit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ element_id: eid, delete: true })
                }).then(jsonOrThrow)
                .then(function () {
                    el.remove();
                    selectedElementIds.delete(eid);
                    clearSelection();
                })
                .catch(function (err) {
                    showError((LANG === "zh" ? "删除失败: " : "Delete failed: ") + err.message);
                });
            });
        }
    }

    function stageAttr(el, eid, key, value) {
        if ((key === "fill" || key === "stroke") && !isSafeColor(value)) {
            showError(t("err_edit") + key);
            return;
        }
        var attrs = {};
        attrs[key] = value;
        stageEditRequest(eid, { attrs: attrs })
            .then(function () { el.setAttribute(key, value); })
            .catch(function (err) { showError(t("err_edit") + err.message); });
    }

    // Tracks every in-flight direct-edit POST so Apply changes can wait for them
    // to land before /save-all (otherwise a just-sent edit could arrive after the
    // save and resurrect a pending edit).
    var inFlightEdits = new Set();

    function drainDirectEdits() {
        if (inFlightEdits.size === 0) return Promise.resolve();
        return Promise.allSettled(Array.from(inFlightEdits)).then(function (results) {
            var failed = results.find(function (r) { return r.status === "rejected"; });
            if (failed) throw (failed.reason || new Error("direct edit failed"));
            return drainDirectEdits();
        });
    }

    function stageEditRequest(eid, payload, slideName) {
        // Pin the slide at call time: a queued nudge may fire after the user has
        // navigated, and must still POST to the slide it was made on, not the
        // global currentSlide.
        var slide = slideName || currentSlide;
        var body = { element_id: eid };
        if (payload.text !== undefined) body.text = payload.text;
        if (payload.attrs !== undefined) body.attrs = payload.attrs;
        if (payload.promote_tspan !== undefined) body.promote_tspan = payload.promote_tspan;
        var p = fetch("/api/slide/" + encodeURIComponent(slide) + "/edit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        }).then(jsonOrThrow).then(function (data) {
            if (data && data.undo_depth !== undefined) {
                editStackCount[slide] = data.undo_depth;
                if (slide === currentSlide) updateUndoButton();
            }
            if (data && data.mtime) {
                slideMtimes[slide] = data.mtime;
            }
            flashLiveSave();
            maybeShowSavedHint();
            return data;
        });
        inFlightEdits.add(p);
        var done = function () { inFlightEdits.delete(p); };
        p.then(done, done);
        return p;
    }

    function renderMultiSelectSummary(ids) {
        var moveEls = topLevelSelectedElements(ids);
        var summary = '<div class="prop-caption">' + escapeHtml(t("label_batch_edit")) + '</div>';

        if (moveEls.length > 0) {
            try {
                var rb = computeElementsBox(moveEls);
                summary += '<div class="prop-section">' + escapeHtml(t("section_geometry")) + '</div>';
                summary += '<table class="prop-table"><tr><td class="prop-key">x / y</td>' +
                    '<td class="prop-val geo-cell">' +
                    '<input type="number" class="prop-edit prop-edit-multi-geo" data-geo="x" value="' +
                    Math.round(rb.x) + '">' +
                    '<input type="number" class="prop-edit prop-edit-multi-geo" data-geo="y" value="' +
                    Math.round(rb.y) + '">' +
                    '</td></tr></table>';
            } catch (e) { /* no multi geometry */ }
        }
        summary += '<div class="prop-section">' + escapeHtml(t("section_style")) + '</div>';
        summary += '<table class="prop-table">';
        batchEditSpecs(moveEls).forEach(function (spec) {
            summary += '<tr><td class="prop-key">' + escapeHtml(spec.key) + '</td><td class="prop-val">';
            summary += renderBatchControl(spec);
            summary += '</td></tr>';
        });
        summary += '</table>';
        summary += '<div class="prop-section" style="margin-top: 16px; border-top: 1px solid var(--border, #334155); padding-top: 12px;">' + (LANG === "zh" ? "快捷操作" : "Actions") + '</div>';
        summary += '<div style="padding: 4px 0 12px 0;"><button type="button" class="btn-direct-delete-multi" style="width: 100%; padding: 10px 12px; background: #dc2626; color: #ffffff; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: background 0.15s;" onmouseover="this.style.background=\'#b91c1c\'" onmouseout="this.style.background=\'#dc2626\'">' +
            (LANG === "zh" ? "🗑️ 批量删除选中元素 (" + ids.length + ")" : "🗑️ Delete Selected (" + ids.length + ")") +
            '</button></div>';
        return summary;
    }

    function batchEditSpecs(elements) {
        var keys = [
            { key: "fill", type: "color" },
            { key: "stroke", type: "color" },
            { key: "opacity", type: "number", min: "0", max: "1", step: "0.05" }
        ];
        if (elements.length > 0 && elements.every(isTextElement)) {
            keys = keys.concat([
                { key: "font-size", type: "text" },
                { key: "font-family", type: "text" },
                { key: "font-weight", type: "select",
                  options: ["", "normal", "bold", "300", "400", "500", "600", "700", "800"] },
                { key: "text-anchor", type: "select", options: ["", "start", "middle", "end"] }
            ]);
        }
        return keys.map(function (spec) {
            var value = commonAttrValue(elements, spec.key);
            var copy = Object.assign({}, spec);
            copy.value = value === null ? "" : value;
            copy.mixed = value === null;
            return copy;
        });
    }

    function isTextElement(el) {
        var tag = el.tagName.toLowerCase();
        return tag === "text" || tag === "tspan";
    }

    function commonAttrValue(elements, key) {
        if (elements.length === 0) return "";
        var first = attrOrComputedValue(elements[0], key);
        for (var i = 1; i < elements.length; i++) {
            if (attrOrComputedValue(elements[i], key) !== first) return null;
        }
        return first;
    }

    function attrOrComputedValue(el, key) {
        var value = el.getAttribute(key);
        if (value !== null && value !== "") return value;
        var style = window.getComputedStyle(el);
        var map = {
            "fill": "fill",
            "stroke": "stroke",
            "opacity": "opacity",
            "font-size": "fontSize",
            "font-family": "fontFamily",
            "font-weight": "fontWeight",
            "text-anchor": "textAnchor"
        };
        return (map[key] && style[map[key]]) || "";
    }

    function renderBatchControl(spec) {
        var placeholder = spec.mixed ? t("multi_mixed") : "";
        if (spec.type === "color") {
            return '<input type="color" class="prop-edit prop-edit-batch-color" data-key="' +
                escapeHtml(spec.key) + '" value="' + normalizeHexForPicker(spec.value) + '">' +
                '<input type="text" class="prop-edit prop-edit-batch" data-key="' +
                escapeHtml(spec.key) + '" placeholder="' + escapeHtml(placeholder) +
                '" value="' + escapeHtml(spec.mixed ? "" : spec.value) + '">';
        }
        if (spec.type === "number") {
            return '<input type="number" class="prop-edit prop-edit-batch" data-key="' +
                escapeHtml(spec.key) + '" min="' + escapeHtml(spec.min || "") +
                '" max="' + escapeHtml(spec.max || "") + '" step="' +
                escapeHtml(spec.step || "1") + '" placeholder="' + escapeHtml(placeholder) +
                '" value="' + escapeHtml(spec.mixed ? "" : spec.value) + '">';
        }
        if (spec.type === "select") {
            var html = '<select class="prop-edit prop-edit-batch" data-key="' + escapeHtml(spec.key) + '">';
            spec.options.forEach(function (opt) {
                var label = opt || placeholder || "";
                var selected = !spec.mixed && spec.value === opt ? " selected" : "";
                html += '<option value="' + escapeHtml(opt) + '"' + selected + '>' +
                    escapeHtml(label) + '</option>';
            });
            html += '</select>';
            return html;
        }
        return '<input type="text" class="prop-edit prop-edit-batch" data-key="' +
            escapeHtml(spec.key) + '" placeholder="' + escapeHtml(placeholder) +
            '" value="' + escapeHtml(spec.mixed ? "" : spec.value) + '">';
    }

    function attachMultiSelectionEditors(ids) {
        var panel = elementPropsEl;

        var moveEls = topLevelSelectedElements(ids);
        if (moveEls.length === 0) return;

        var readGeo = function (k) {
            var inp = panel.querySelector('.prop-edit-multi-geo[data-geo="' + k + '"]');
            return inp ? parseFloat(inp.value) : NaN;
        };
        var commitMove = function () {
            var rb;
            try { rb = computeElementsBox(moveEls); } catch (e) { return; }
            var nx = readGeo("x"), ny = readGeo("y");
            if (isNaN(nx) || isNaN(ny)) return;
            var dx = nx - rb.x, dy = ny - rb.y;
            if (Math.abs(dx) < 1e-6 && Math.abs(dy) < 1e-6) return;

            var jobs = [];
            moveEls.forEach(function (el) {
                var attrs;
                try { attrs = attrsForMove(el, dx, dy); } catch (e) { attrs = null; }
                if (!attrs) return;
                var payload = payloadForMovedElement(el, attrs);
                jobs.push(stageEditRequest(el.id, payload).then(function () {
                    if (payload.promote_tspan) promoteTspanDom(el, payload.promote_tspan);
                    else {
                        applyElementAttrs(el, attrs);
                        markCommittedAttrs(el, attrs);
                    }
                }));
            });

            Promise.all(jobs)
                .then(function () { updateSelectionPanel(); })
                .catch(function (err) { showError(t("err_edit") + err.message); });
        };

        panel.querySelectorAll(".prop-edit-multi-geo").forEach(function (inp) {
            inp.addEventListener("change", commitMove);
        });

        panel.querySelectorAll(".prop-edit-batch-color").forEach(function (picker) {
            var key = picker.getAttribute("data-key");
            var text = panel.querySelector('.prop-edit-batch[data-key="' + key + '"]');
            picker.addEventListener("input", function () {
                if (text) text.value = picker.value;
            });
            picker.addEventListener("change", function () {
                if (text) text.value = picker.value;
                commitBatchAttr(key, picker.value, moveEls);
            });
        });

        panel.querySelectorAll(".prop-edit-batch").forEach(function (input) {
            input.addEventListener("change", function () {
                var key = input.getAttribute("data-key");
                var value = input.value.trim();
                if (!value) return;
                commitBatchAttr(key, value, moveEls);
            });
        });

        var multiDelBtn = panel.querySelector(".btn-direct-delete-multi");
        if (multiDelBtn) {
            multiDelBtn.addEventListener("click", function () {
                if (!confirm(LANG === "zh" ? "确定要删除选中的 " + ids.length + " 个元素吗？" : "Are you sure you want to delete these elements?")) return;
                deleteSelectedElements();
            });
        }
    }

    function commitBatchAttr(key, value, elements) {
        if ((key === "fill" || key === "stroke") && !isSafeColor(value)) {
            showError(t("err_edit") + key);
            return;
        }
        var jobs = elements.map(function (el) {
            var attrs = {};
            attrs[key] = value;
            return stageEditRequest(el.id, { attrs: attrs }).then(function () {
                el.setAttribute(key, value);
            });
        });
        Promise.all(jobs)
            .then(function () { updateSelectionPanel(); })
            .catch(function (err) { showError(t("err_edit") + err.message); });
    }

    // ================================================================
    //  Boot
    // ================================================================
    applyI18n();
    var langToggleBtn = document.getElementById("btn-lang-toggle");
    if (langToggleBtn) {
        langToggleBtn.textContent = LANG === "zh" ? "EN" : "中";
        langToggleBtn.title = t("lang_toggle_title");
        langToggleBtn.addEventListener("click", function () {
            setLang(LANG === "zh" ? "en" : "zh");
        });
    }

    loadConfig().then(function () {
        loadSlides();
        startSlidePolling();
    });
    initRubberBand();
    initKeyboardShortcuts();
    initSlideNav();
    initNotes();
    initAnnotationPopover();
    initFullscreenSplitter();
    
    var fsLayoutMode = "split";
    function setFullscreenLayout(mode) {
        fsLayoutMode = mode;
        var fsTop = document.getElementById("fullscreen-top");
        var fsBottom = document.getElementById("fullscreen-bottom");
        var fsSplitter = document.getElementById("fullscreen-splitter");
        
        if (mode === "notes-only") {
            if (fsTop) fsTop.style.display = "none";
            if (fsSplitter) fsSplitter.style.display = "none";
            if (fsBottom) {
                fsBottom.style.display = "flex";
                fsBottom.style.height = "100vh";
            }
            if (fsLayoutToggleBtn) {
                fsLayoutToggleBtn.textContent = "📄 仅讲稿";
                fsLayoutToggleBtn.title = "当前：仅讲稿。点击切换为分屏模式";
            }
        } else if (mode === "slide-only") {
            if (fsBottom) fsBottom.style.display = "none";
            if (fsSplitter) fsSplitter.style.display = "none";
            if (fsTop) {
                fsTop.style.display = "flex";
                fsTop.style.height = "100vh";
                fsTop.style.padding = "0";
            }
            if (fsLayoutToggleBtn) {
                fsLayoutToggleBtn.textContent = "🎬 仅片子";
                fsLayoutToggleBtn.title = "当前：仅片子。点击切换为仅讲稿模式";
            }
        } else { // "split"
            if (fsTop) {
                fsTop.style.display = "flex";
                fsTop.style.height = "";
                fsTop.style.padding = "";
            }
            if (fsSplitter) fsSplitter.style.display = "flex";
            if (fsBottom) {
                fsBottom.style.display = "flex";
                fsBottom.style.height = "";
            }
            if (fsLayoutToggleBtn) {
                fsLayoutToggleBtn.textContent = "🎬📄 分屏";
                fsLayoutToggleBtn.title = "当前：分屏模式。点击切换为仅片子模式";
            }
        }
    }

    function initFullscreenLayoutControls() {
        if (fsLayoutToggleBtn) {
            fsLayoutToggleBtn.addEventListener("click", function () {
                var nextMode = "split";
                if (fsLayoutMode === "split") {
                    nextMode = "slide-only";
                } else if (fsLayoutMode === "slide-only") {
                    nextMode = "notes-only";
                } else if (fsLayoutMode === "notes-only") {
                    nextMode = "split";
                }
                setFullscreenLayout(nextMode);
            });
        }
    }
    
    var fsControlsTimer = null;
    var isHoveringControls = false;

    function showFullscreenControls() {
        if (fsControlsEl) {
            fsControlsEl.classList.add("visible");
        }
        if (fsControlsTimer) {
            clearTimeout(fsControlsTimer);
            fsControlsTimer = null;
        }
    }

    function resetHideControlsTimer() {
        if (fsControlsTimer) {
            clearTimeout(fsControlsTimer);
        }
        fsControlsTimer = setTimeout(function () {
            if (fsControlsEl && !isHoveringControls) {
                fsControlsEl.classList.remove("visible");
            }
        }, 3000);
    }

    function initFullscreenControlsFade() {
        if (fullscreenOverlay) {
            fullscreenOverlay.addEventListener("mousemove", function () {
                showFullscreenControls();
                resetHideControlsTimer();
            });
        }
        if (fsControlsEl) {
            fsControlsEl.addEventListener("mouseenter", function () {
                isHoveringControls = true;
                showFullscreenControls();
            });
            fsControlsEl.addEventListener("mouseleave", function () {
                isHoveringControls = false;
                resetHideControlsTimer();
            });
        }
    }

    initFullscreenLayoutControls();
    initFullscreenControlsFade();

    function enterFullscreen() {
        isFullscreenMode = true;
        syncFullscreenSvg();
        loadCurrentNotes();
        updateNavLabel();
        showFullscreenControls();
        resetHideControlsTimer();
        if (fullscreenOverlay) {
            fullscreenOverlay.style.display = "flex";
            fullscreenOverlay.focus();
            setTimeout(function () {
                if (fullscreenOverlay) fullscreenOverlay.focus();
            }, 50);
            if (fullscreenOverlay.requestFullscreen) {
                fullscreenOverlay.requestFullscreen().then(function() {
                    if (fullscreenOverlay) fullscreenOverlay.focus();
                }).catch(function(err) {
                    console.warn("Fullscreen error:", err.message);
                });
            } else if (fullscreenOverlay.webkitRequestFullscreen) {
                fullscreenOverlay.webkitRequestFullscreen();
            } else if (fullscreenOverlay.msRequestFullscreen) {
                fullscreenOverlay.msRequestFullscreen();
            }
        }
    }

    function exitFullscreen() {
        isFullscreenMode = false;
        setFullscreenLayout("split");
        if (fsControlsTimer) {
            clearTimeout(fsControlsTimer);
            fsControlsTimer = null;
        }
        if (fsControlsEl) {
            fsControlsEl.classList.remove("visible");
        }
        if (fullscreenOverlay) {
            fullscreenOverlay.style.display = "none";
        }
        if (document.fullscreenElement || document.webkitFullscreenElement || document.msFullscreenElement) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }

    function onFullscreenChange() {
        var fsEl = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement;
        if (!fsEl && isFullscreenMode) {
            exitFullscreen();
        }
    }

    document.addEventListener("fullscreenchange", onFullscreenChange);
    document.addEventListener("webkitfullscreenchange", onFullscreenChange);
    document.addEventListener("mozfullscreenchange", onFullscreenChange);
    document.addEventListener("MSFullscreenChange", onFullscreenChange);

    function syncFullscreenSvg() {
        if (!fsSvgContainer || !svgContent) return;
        fsSvgContainer.innerHTML = svgContent.innerHTML;
        if (activeTheme !== "astryx-theme-default") {
            makeSvgThemeable(fsSvgContainer);
        }
        var svg = fsSvgContainer.querySelector("svg");
        if (svg) {
            var w = parseFloat(svg.getAttribute("width")) || 960;
            var h = parseFloat(svg.getAttribute("height")) || 540;
            if (svg.getAttribute("viewBox")) {
                var vb = svg.getAttribute("viewBox").split(/\s+/);
                if (vb.length === 4) {
                    w = parseFloat(vb[2]) || w;
                    h = parseFloat(vb[3]) || h;
                }
            }
            var ratio = w / h;
            fsSvgContainer.style.aspectRatio = ratio ? String(ratio) : "auto";
        } else {
            fsSvgContainer.style.aspectRatio = "auto";
        }
    }

    var isDraggingSplitter = false;
    function initFullscreenSplitter() {
        var fsSplitter = document.getElementById("fullscreen-splitter");
        if (fsSplitter) {
            fsSplitter.addEventListener("mousedown", startSplitterDrag);
            fsSplitter.addEventListener("touchstart", startSplitterDrag, { passive: true });
        }
    }

    function startSplitterDrag(e) {
        isDraggingSplitter = true;
        var fsSplitter = document.getElementById("fullscreen-splitter");
        if (fsSplitter) fsSplitter.classList.add("dragging");
        
        document.addEventListener("mousemove", onSplitterDrag);
        document.addEventListener("mouseup", stopSplitterDrag);
        document.addEventListener("touchmove", onSplitterDrag, { passive: false });
        document.addEventListener("touchend", stopSplitterDrag);
    }

    function onSplitterDrag(e) {
        if (!isDraggingSplitter) return;
        var clientY = e.touches ? e.touches[0].clientY : e.clientY;
        var totalHeight = window.innerHeight;
        
        var topPercentage = (clientY / totalHeight) * 100;
        if (topPercentage < 20) topPercentage = 20;
        if (topPercentage > 85) topPercentage = 85;
        
        if (fullscreenOverlay) {
            fullscreenOverlay.style.setProperty("--fs-top-height", topPercentage + "vh");
        }
        if (e.cancelable) e.preventDefault();
    }

    function stopSplitterDrag() {
        if (!isDraggingSplitter) return;
        isDraggingSplitter = false;
        var fsSplitter = document.getElementById("fullscreen-splitter");
        if (fsSplitter) fsSplitter.classList.remove("dragging");
        
        document.removeEventListener("mousemove", onSplitterDrag);
        document.removeEventListener("mouseup", stopSplitterDrag);
        document.removeEventListener("touchmove", onSplitterDrag);
        document.removeEventListener("touchend", stopSplitterDrag);
    }

    function getLuminance(hex) {
        if (!hex || hex.indexOf('#') !== 0) return 1;
        var c = hex.substring(1);
        if (c.length === 3) {
            c = c[0] + c[0] + c[1] + c[1] + c[2] + c[2];
        }
        if (c.length !== 6) return 1;
        var r = parseInt(c.substring(0, 2), 16) / 255;
        var g = parseInt(c.substring(2, 4), 16) / 255;
        var b = parseInt(c.substring(4, 6), 16) / 255;
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    function makeSvgThemeable(container) {
        var svg = container.querySelector("svg");
        if (!svg) return;
        
        // Step 1: Detect background color
        var canvasWidth = parseFloat(svg.getAttribute("width")) || 1280;
        var canvasHeight = parseFloat(svg.getAttribute("height")) || 720;
        var bgColor = null;
        var bgRect = svg.querySelector("rect");
        if (bgRect) {
            var w = parseFloat(bgRect.getAttribute("width"));
            var h = parseFloat(bgRect.getAttribute("height"));
            if (w >= canvasWidth * 0.9 && h >= canvasHeight * 0.9) {
                var fill = bgRect.getAttribute("fill");
                if (fill && fill !== "none") bgColor = fill.toLowerCase().trim();
            }
        }
        if (!bgColor) bgColor = "#f8f8f8";
        
        var isBgLight = getLuminance(bgColor) >= 0.5;
        
        // Step 2: Establish the base color map
        var colorMap = {
            "#ffffff": "var(--color-card-bg)",
            "#1a1f29": "var(--color-brand-secondary)",
            "#1a1f2a": "var(--color-brand-secondary)",
            "#404040": "var(--color-brand-secondary)",
            "#383737": "var(--color-brand-secondary)",
            "#af935c": "var(--color-brand-primary)",
            "#f8f8f8": "var(--color-bg-slide)",
            "#f2f2f2": "var(--color-border)",
            "#e2e2e2": "var(--color-border)",
            "#cccccc": "var(--color-border)"
        };
        
        if (bgColor && !colorMap[bgColor]) {
            colorMap[bgColor] = "var(--color-bg-slide)";
            container.style.setProperty("--color-bg-slide-default", bgColor);
        }
        
        // Step 3: Scan other elements' colors
        svg.querySelectorAll("*").forEach(function (el) {
            var attrs = ["fill", "stroke"];
            attrs.forEach(function (attr) {
                var val = el.getAttribute(attr);
                if (val && val !== "none" && val !== "currentColor" && val !== "inherit" && val.indexOf("#") === 0) {
                    var color = val.toLowerCase().trim();
                    if (!colorMap[color]) {
                        var lum = getLuminance(color);
                        if (isBgLight) {
                            if (lum < 0.45) {
                                // Dark elements in a light slide -> map to text/brand-secondary
                                colorMap[color] = "var(--color-brand-secondary)";
                            } else if (lum >= 0.45 && lum < 0.75 && color !== "#ffffff") {
                                // Light accent elements -> map to brand-primary
                                colorMap[color] = "var(--color-brand-primary)";
                            } else if (lum >= 0.75 && color !== "#ffffff") {
                                // Very light elements (borders/dividers) -> map to border
                                colorMap[color] = "var(--color-border)";
                            }
                        } else {
                            if (lum >= 0.55) {
                                // Light elements in a dark slide -> map to text/brand-secondary
                                colorMap[color] = "var(--color-brand-secondary)";
                            } else if (lum < 0.55 && lum > 0.25 && color !== bgColor) {
                                // Dark accents -> map to brand-primary
                                colorMap[color] = "var(--color-brand-primary)";
                            } else if (lum <= 0.25 && color !== bgColor) {
                                // Very dark borders/dividers -> map to border
                                colorMap[color] = "var(--color-border)";
                            }
                        }
                    }
                }
            });
        });
        
        // Step 4: Map elements to CSS variables
        svg.querySelectorAll("*").forEach(function (el) {
            var fill = el.getAttribute("fill");
            if (fill) {
                var lf = fill.toLowerCase().trim();
                if (colorMap[lf]) {
                    el.setAttribute("fill", colorMap[lf]);
                    el.style.fill = colorMap[lf];
                }
            }
            var stroke = el.getAttribute("stroke");
            if (stroke) {
                var ls = stroke.toLowerCase().trim();
                if (colorMap[ls]) {
                    el.setAttribute("stroke", colorMap[ls]);
                    el.style.stroke = colorMap[ls];
                }
            }
        });
    }

    function renderCurrentSlideWithTheme() {
        if (!currentRawSvgContent) return;
        
        svgPlaceholder.style.display = "none";
        svgContent.style.display = "block";
        
        if (activeTheme === "astryx-theme-default") {
            svgContent.innerHTML = sanitizeSvg(currentRawSvgContent);
            if (svgContent) {
                svgContent.style.removeProperty("--color-brand-primary");
                svgContent.style.removeProperty("--color-brand-secondary");
                svgContent.style.removeProperty("--color-bg-slide");
                svgContent.style.removeProperty("--color-card-bg");
                svgContent.style.removeProperty("--color-border");
            }
            if (fsSvgContainer) {
                fsSvgContainer.style.removeProperty("--color-brand-primary");
                fsSvgContainer.style.removeProperty("--color-brand-secondary");
                fsSvgContainer.style.removeProperty("--color-bg-slide");
                fsSvgContainer.style.removeProperty("--color-card-bg");
                fsSvgContainer.style.removeProperty("--color-border");
            }
        } else {
            svgContent.innerHTML = sanitizeSvg(currentRawSvgContent);
            makeSvgThemeable(svgContent);
        }
        
        syncFullscreenSvg();
    }

    var availableThemes = {};
    function applyTheme(themeKey) {
        activeTheme = themeKey;
        try {
            window.localStorage.setItem("ppt_theme", themeKey);
        } catch (e) { /* ignore */ }
        
        var theme = availableThemes[themeKey];
        var fsTop = document.getElementById("fullscreen-top");
        var svgBox = document.getElementById("svg-container");

        if (theme) {
            var isDark = getLuminance(theme.bg) < 0.5;
            var textSecondaryColor = isDark ? "#ffffff" : theme.secondary;
            var cardBgColor = isDark ? "#1e293b" : "#ffffff";
            var borderColor = isDark ? "#334155" : "#e2e8f0";
            
            // Adjust primary accent for visibility on dark backgrounds
            var primaryColor = theme.primary;
            if (isDark && getLuminance(primaryColor) < 0.35) {
                primaryColor = "#f87171"; // soft light red/accent color fallback
            }
            
            [svgContent, fsSvgContainer, svgBox, fsTop].forEach(function(target) {
                if (target) {
                    target.style.setProperty("--color-brand-primary", primaryColor);
                    target.style.setProperty("--color-brand-secondary", textSecondaryColor);
                    target.style.setProperty("--color-bg-slide", theme.bg);
                    target.style.setProperty("--color-card-bg", cardBgColor);
                    target.style.setProperty("--color-border", borderColor);
                }
            });
        } else {
            [svgContent, fsSvgContainer, svgBox, fsTop].forEach(function(target) {
                if (target) {
                    target.style.removeProperty("--color-brand-primary");
                    target.style.removeProperty("--color-brand-secondary");
                    target.style.removeProperty("--color-bg-slide");
                    target.style.removeProperty("--color-card-bg");
                    target.style.removeProperty("--color-border");
                }
            });
        }
        
        if (themeSelect) themeSelect.value = themeKey;
        if (fsThemeSelect) fsThemeSelect.value = themeKey;
        
        renderCurrentSlideWithTheme();
    }

    function initThemeSelectors() {
        fetch("/api/themes")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                availableThemes = data;
                
                var selects = [themeSelect, fsThemeSelect];
                selects.forEach(function (sel) {
                    if (!sel) return;
                    sel.innerHTML = '<option value="astryx-theme-default">Default Theme (Original)</option>';
                    
                    var sortedKeys = Object.keys(data).sort(function (a, b) {
                        return data[a].name.localeCompare(data[b].name);
                    });
                    
                    sortedKeys.forEach(function (key) {
                        var opt = document.createElement("option");
                        opt.value = key;
                        opt.textContent = data[key].name;
                        sel.appendChild(opt);
                    });
                });

                // Restore saved theme preference if present
                try {
                    var savedTheme = window.localStorage.getItem("ppt_theme");
                    if (savedTheme && (savedTheme === "astryx-theme-default" || data[savedTheme])) {
                        applyTheme(savedTheme);
                    }
                } catch (e) { /* ignore */ }
            })
            .catch(function (err) {
                console.error("Failed to load themes:", err);
            });

        if (themeSelect) {
            themeSelect.addEventListener("change", function () {
                applyTheme(themeSelect.value);
            });
        }
        if (fsThemeSelect) {
            fsThemeSelect.addEventListener("change", function () {
                applyTheme(fsThemeSelect.value);
            });
        }
    }


    // =======================================================================
    // Live Save Flash Indicator
    // =======================================================================
    function flashLiveSave() {
        if (!liveSaveStatus || !liveSaveText) return;
        liveSaveStatus.classList.add("saved");
        liveSaveText.textContent = t("live_status_saved");
        setTimeout(function () {
            liveSaveStatus.classList.remove("saved");
            liveSaveText.textContent = t("live_status_text");
        }, 2000);
    }

    // =======================================================================
    // Agent Task Checklist & Background Processing
    // =======================================================================
    var toastTimer = null;
    function showToast(message, type, title) {
        if (!agentNotificationToast) return;
        var iconEl = agentNotificationToast.querySelector(".toast-icon");
        if (iconEl) {
            if (type === "success") iconEl.textContent = "✅";
            else if (type === "info") iconEl.textContent = "💾";
            else if (type === "warning") iconEl.textContent = "⚠️";
            else iconEl.textContent = "🎉";
        }
        if (toastTitle) toastTitle.textContent = title || (type === "info" ? "已暂存" : (type === "warning" ? "提示" : "操作成功"));
        if (toastDesc) toastDesc.textContent = message;
        agentNotificationToast.style.display = "flex";
        if (toastTimer) clearTimeout(toastTimer);
        var duration = (type === "done" || type === "success") ? 8000 : 4500;
        toastTimer = setTimeout(function () {
            agentNotificationToast.style.display = "none";
        }, duration);
    }

    function showAgentDoneToast(slideName, summary) {
        var pageNum = slideName;
        var m = String(slideName).match(/slide_?(\d+)/i);
        if (m) pageNum = m[1];
        var desc = t("agent_done_desc").replace("{page}", pageNum);
        if (summary && summary !== "后台修改已完成") {
            desc += " (" + summary + ")";
        }
        showToast(desc, "done", t("agent_done_title"));
    }

    function loadSlideTasks(name) {
        if (!name) return Promise.resolve();
        return fetch("/api/slide/" + encodeURIComponent(name) + "/tasks")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                slideTasks[name] = data.tasks || [];
                renderSlideTasks(name);
                updateAllTasksUI();
            })
            .catch(function (err) {
                console.error("Failed to load slide tasks:", err);
            });
    }

    function loadAllTasks() {
        return fetch("/api/tasks")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data && data.tasks) {
                    slideTasks = data.tasks;
                    if (currentSlide) renderSlideTasks(currentSlide);
                    updateAllTasksUI();
                }
            })
            .catch(function (err) {
                console.error("Failed to load all tasks:", err);
            });
    }

    function updateSubmitButtonsState(processing) {
        if (processing) {
            if (btnSubmitAgent) {
                btnSubmitAgent.disabled = true;
                btnSubmitAgent.textContent = t("btn_submitting_agent");
            }
            if (btnSubmitAllAgent) {
                btnSubmitAllAgent.disabled = true;
                btnSubmitAllAgent.textContent = t("btn_submitting_agent");
            }
            if (btnStageAgent) btnStageAgent.disabled = true;
            if (btnStagePoint) btnStagePoint.disabled = true;
        } else {
            if (btnStageAgent) btnStageAgent.disabled = false;
            if (btnStagePoint) btnStagePoint.disabled = false;
            updateAllTasksUI();
        }
    }

    function updateAllTasksUI() {
        var totalUncompleted = 0;
        Object.keys(slideTasks).forEach(function (sname) {
            var stasks = slideTasks[sname] || [];
            totalUncompleted += stasks.filter(function (t) { return t.status !== "completed"; }).length;
        });

        var curTasks = (currentSlide && slideTasks[currentSlide]) || [];
        var curCount = curTasks.length;
        var uncompletedTasks = curTasks.filter(function (t) { return t.status !== "completed"; });
        var uncompletedCount = uncompletedTasks.length;

        var hasDraftText = !!(agentPointText && agentPointText.value.trim().length > 0);
        var effectiveCurCount = uncompletedCount + (hasDraftText ? 1 : 0);
        var effectiveAllCount = totalUncompleted + (hasDraftText ? 1 : 0);

        if (btnSubmitAllAgent && !isAgentProcessing) {
            btnSubmitAllAgent.disabled = effectiveAllCount === 0;
            btnSubmitAllAgent.textContent = effectiveAllCount > 0
                ? (t("btn_submit_all_agent") + " (" + effectiveAllCount + ")")
                : t("btn_submit_all_agent");
        }

        if (btnSubmitAgent && !isAgentProcessing) {
            btnSubmitAgent.disabled = effectiveCurCount === 0;
            btnSubmitAgent.textContent = effectiveCurCount > 0
                ? (t("btn_submit_agent") + " (" + effectiveCurCount + ")")
                : t("btn_submit_agent");
        }

        if (pointsCountBadge) {
            pointsCountBadge.textContent = curCount;
        }
        if (tabAgent) {
            tabAgent.textContent = curCount > 0 ? (t("tab_agent") + " (" + curCount + ")") : t("tab_agent");
        }

        if (slideListEl) {
            slideListEl.querySelectorAll(".slide-item").forEach(function (item) {
                var sname = item.getAttribute("data-name");
                var stasks = (sname && slideTasks[sname]) || [];
                var badge = item.querySelector(".badge");
                if (stasks.length > 0) {
                    if (!badge) {
                        badge = document.createElement("span");
                        badge.className = "badge";
                        item.appendChild(badge);
                    }
                    badge.classList.remove("badge-pending", "badge-submitted", "badge-completed");

                    var hasStaged = stasks.some(function (t) { return t.status === "staged" || t.status === "pending" || !t.status; });
                    var hasSubmitted = stasks.some(function (t) { return t.status === "submitted"; });
                    var allCompleted = stasks.every(function (t) { return t.status === "completed"; });

                    if (hasSubmitted) {
                        badge.classList.add("badge-submitted");
                        badge.textContent = stasks.length;
                        badge.title = "后台处理中修改点: " + stasks.length;
                    } else if (hasStaged) {
                        badge.classList.add("badge-pending");
                        badge.textContent = stasks.length;
                        badge.title = "待提交修改点: " + stasks.length;
                    } else if (allCompleted) {
                        badge.classList.add("badge-completed");
                        badge.textContent = stasks.length;
                        badge.title = "所有修改点已完成: " + stasks.length;
                    } else {
                        badge.classList.add("badge-completed");
                        badge.textContent = stasks.length;
                        badge.title = "修改点: " + stasks.length;
                    }
                    badge.style.display = "inline-flex";
                } else if (badge) {
                    badge.style.display = "none";
                }
            });
        }
    }

    function renderSlideTasks(name) {
        if (name !== currentSlide || !agentPointsList) return;
        agentPointsList.innerHTML = "";
        var tasks = slideTasks[name] || [];
        var count = tasks.length;
        if (pointsCountBadge) pointsCountBadge.textContent = count;
        if (tabAgent) {
            tabAgent.textContent = count > 0 ? (t("tab_agent") + " (" + count + ")") : t("tab_agent");
        }
        if (btnSubmitAgent && !isAgentProcessing) {
            btnSubmitAgent.disabled = count === 0;
            btnSubmitAgent.textContent = count > 0
                ? (t("btn_submit_agent") + " (" + count + ")")
                : t("btn_submit_agent");
        }

        if (tasks.length === 0) {
            var empty = document.createElement("div");
            empty.className = "agent-point-empty";
            empty.textContent = t("empty_points");
            agentPointsList.appendChild(empty);
            return;
        }

        tasks.forEach(function (task, idx) {
            var card = document.createElement("div");
            card.className = "point-card";
            if (task.status === "completed") {
                card.classList.add("is-completed");
            }

            var header = document.createElement("div");
            header.className = "point-header";

            var numTag = document.createElement("div");
            numTag.className = "point-num-tag";

            var num = document.createElement("span");
            num.className = "point-num";
            num.textContent = "#" + (idx + 1);
            numTag.appendChild(num);

            var tag = document.createElement("span");
            tag.className = "point-tag";
            tag.textContent = task.target_desc || (task.element_id === "__page__" ? t("target_page") : ("#" + task.element_id));
            numTag.appendChild(tag);

            var statusBadge = document.createElement("span");
            var st = task.status;
            if (st === "completed") {
                statusBadge.className = "point-status-badge status-completed";
                statusBadge.textContent = "✅ " + t("status_completed");
            } else if (st === "submitted") {
                statusBadge.className = "point-status-badge status-submitted";
                statusBadge.textContent = t("status_submitted");
            } else {
                statusBadge.className = "point-status-badge status-staged";
                statusBadge.textContent = t("status_staged");
            }
            numTag.appendChild(statusBadge);

            header.appendChild(numTag);

            var actions = document.createElement("div");
            actions.className = "point-actions";

            var editBtn = document.createElement("button");
            editBtn.className = "point-edit";
            editBtn.type = "button";
            editBtn.innerHTML = "✏️";
            editBtn.title = t("btn_edit_point");

            var delBtn = document.createElement("button");
            delBtn.className = "point-del";
            delBtn.type = "button";
            delBtn.innerHTML = "&times;";
            delBtn.title = t("tooltip_remove_annotation");
            delBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                deleteSlideTask(name, task.id);
            });

            actions.appendChild(editBtn);
            actions.appendChild(delBtn);
            header.appendChild(actions);

            card.appendChild(header);

            var body = document.createElement("div");
            body.className = "point-text";
            body.textContent = task.text;
            body.title = t("hint_dblclick_edit");
            card.appendChild(body);

            // Inline edit container
            var editBox = document.createElement("div");
            editBox.className = "point-edit-box";
            editBox.style.display = "none";

            var editTextarea = document.createElement("textarea");
            editTextarea.className = "point-edit-textarea";
            editTextarea.rows = 3;
            editTextarea.value = task.text;

            var editActions = document.createElement("div");
            editActions.className = "point-edit-actions";

            var saveBtn = document.createElement("button");
            saveBtn.type = "button";
            saveBtn.className = "btn-point-save";
            saveBtn.textContent = t("btn_point_save");

            var cancelBtn = document.createElement("button");
            cancelBtn.type = "button";
            cancelBtn.className = "btn-point-cancel";
            cancelBtn.textContent = t("btn_point_cancel");

            editActions.appendChild(saveBtn);
            editActions.appendChild(cancelBtn);
            editBox.appendChild(editTextarea);
            editBox.appendChild(editActions);
            card.appendChild(editBox);

            function startEdit() {
                body.style.display = "none";
                editBox.style.display = "flex";
                editTextarea.value = task.text;
                editTextarea.focus();
                editTextarea.select();
            }

            function stopEdit() {
                editBox.style.display = "none";
                body.style.display = "";
            }

            editBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                startEdit();
            });

            body.addEventListener("dblclick", function (e) {
                e.stopPropagation();
                startEdit();
            });

            cancelBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                stopEdit();
            });

            saveBtn.addEventListener("click", function (e) {
                e.stopPropagation();
                var newText = editTextarea.value.trim();
                if (!newText) {
                    showError(LANG === "zh" ? "修改点内容不能为空" : "Point text cannot be empty");
                    return;
                }
                saveBtn.disabled = true;
                updateSlideTask(name, task.id, newText)
                    .catch(function (err) {
                        showError((LANG === "zh" ? "更新失败: " : "Update failed: ") + err.message);
                        saveBtn.disabled = false;
                    });
            });

            editTextarea.addEventListener("keydown", function (e) {
                if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
                    e.preventDefault();
                    saveBtn.click();
                } else if (e.key === "Escape") {
                    e.preventDefault();
                    stopEdit();
                }
            });

            agentPointsList.appendChild(card);
        });
    }

    function addSlideTaskWithText(text, targetId, isStage) {
        if (!currentSlide || !text) return Promise.resolve();
        var tid = targetId || currentAgentTarget || "__page__";
        var targetDesc = tid === "__page__" ? t("target_page") : ("#" + tid);

        return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/tasks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                element_id: tid,
                target_desc: targetDesc,
                text: text
            })
        })
            .then(jsonOrThrow)
            .then(function (data) {
                slideTasks[currentSlide] = data.tasks || [];
                if (agentPointText) agentPointText.value = "";
                renderSlideTasks(currentSlide);
                updateAllTasksUI();
                var uncompleted = (data.tasks || []).filter(function (t) { return t.status !== "completed"; });
                if (isStage) {
                    showToast(t("toast_staged_slide").replace("{count}", uncompleted.length), "info", "已暂存");
                }
                return data;
            })
            .catch(function (err) {
                showError(t("err_add_annotation") + err.message);
                throw err;
            });
    }

    function addSlideTask() {
        if (!currentSlide || !agentPointText) return;
        var text = agentPointText.value.trim();
        if (!text) return;
        var targetId = currentAgentTarget || "__page__";
        addSlideTaskWithText(text, targetId, false);
    }

    function stageCurrentSlideTasks() {
        if (!currentSlide) return;
        var text = agentPointText ? agentPointText.value.trim() : "";
        if (text) {
            var targetId = currentAgentTarget || "__page__";
            addSlideTaskWithText(text, targetId, true);
        } else {
            var tasks = slideTasks[currentSlide] || [];
            var uncompleted = tasks.filter(function (t) { return t.status !== "completed"; });
            if (uncompleted.length === 0) {
                showToast("当前页没有待暂存或待提交的新修改点", "warning", "提示");
                if (agentPointText) agentPointText.focus();
                return;
            }
            showToast(t("toast_staged_slide").replace("{count}", uncompleted.length), "info", "已暂存");
            updateAllTasksUI();
        }
    }

    function deleteSlideTask(slideName, taskId) {
        if (!slideName || !taskId) return;
        fetch("/api/slide/" + encodeURIComponent(slideName) + "/tasks/" + encodeURIComponent(taskId), {
            method: "DELETE"
        })
            .then(jsonOrThrow)
            .then(function (data) {
                slideTasks[slideName] = data.tasks || [];
                renderSlideTasks(slideName);
                updateAllTasksUI();
            })
            .catch(function (err) {
                showError(t("err_remove_annotation") + err.message);
            });
    }

    function updateSlideTask(slideName, taskId, newText) {
        if (!slideName || !taskId || !newText) return Promise.reject(new Error("修改内容不能为空"));
        return fetch("/api/slide/" + encodeURIComponent(slideName) + "/tasks/" + encodeURIComponent(taskId), {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: newText })
        })
            .then(jsonOrThrow)
            .then(function (data) {
                slideTasks[slideName] = data.tasks || [];
                renderSlideTasks(slideName);
                updateAllTasksUI();
                showToast(t("toast_point_updated"), "info", "已更新");
            });
    }

    function submitAgentTasks() {
        if (!currentSlide) return;
        var text = agentPointText ? agentPointText.value.trim() : "";
        var tasks = slideTasks[currentSlide] || [];
        var pendingTasks = tasks.filter(function (t) { return t.status !== "completed"; });
        if (!text && pendingTasks.length === 0) {
            showToast("当前页修改点此前均已处理完成并生效，无需重复提交。若有新修改建议，请在上方输入框输入。", "info", "当前页已是最新");
            return;
        }

        isAgentProcessing = true;
        updateSubmitButtonsState(true);
        if (agentStatusIndicator) {
            agentStatusIndicator.style.display = "flex";
        }
        showToast("正在提交修改任务并通知后台处理...", "info", "任务提交中");

        var addPromise = text
            ? addSlideTaskWithText(text, currentAgentTarget || "__page__", false)
            : Promise.resolve();

        addPromise.then(function () {
            var updatedTasks = slideTasks[currentSlide] || [];
            var toSubmit = updatedTasks.filter(function (t) { return t.status !== "completed"; });

            if (toSubmit.length === 0) {
                isAgentProcessing = false;
                updateSubmitButtonsState(false);
                if (agentStatusIndicator) {
                    agentStatusIndicator.style.display = "none";
                }
                showToast("当前页修改点此前均已处理完成并生效，无需重复提交。", "info", "当前页已是最新");
                return;
            }

            submittedSlides.add(currentSlide);
            lastProcessedTime = Date.now() / 1000;

            return fetch("/api/slide/" + encodeURIComponent(currentSlide) + "/submit-tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ slide: currentSlide })
            })
                .then(jsonOrThrow)
                .then(function (data) {
                    return loadAllTasks().then(function () {
                        showToast(
                            t("toast_submit_page_success").replace("{count}", toSubmit.length),
                            "success",
                            "增量提交成功"
                        );
                    });
                });
        }).catch(function (err) {
            isAgentProcessing = false;
            updateSubmitButtonsState(false);
            if (agentStatusIndicator) {
                agentStatusIndicator.style.display = "none";
            }
            showError("提交任务失败: " + (err.message || err));
        });
    }

    function submitAllAgentTasks() {
        var text = agentPointText ? agentPointText.value.trim() : "";
        var totalTasks = 0;
        Object.keys(slideTasks).forEach(function (sname) {
            var tasks = slideTasks[sname] || [];
            totalTasks += tasks.filter(function (t) { return t.status !== "completed"; }).length;
        });

        if (!text && totalTasks === 0) {
            showToast("所有页面修改点此前均已处理完成并生效，无需重复提交。若有新修改建议，请在上方输入框输入。", "info", "全部已是最新");
            return;
        }

        isAgentProcessing = true;
        updateSubmitButtonsState(true);
        if (agentStatusIndicator) {
            agentStatusIndicator.style.display = "flex";
        }
        showToast("正在提交所有页面修改任务...", "info", "全部提交中");

        var addPromise = (text && currentSlide)
            ? addSlideTaskWithText(text, currentAgentTarget || "__page__", false)
            : Promise.resolve();

        addPromise.then(function () {
            var slidesWithTasks = [];
            var finalTotal = 0;
            Object.keys(slideTasks).forEach(function (sname) {
                var tasks = slideTasks[sname] || [];
                var uncompleted = tasks.filter(function (t) { return t.status !== "completed"; });
                if (uncompleted.length > 0) {
                    finalTotal += uncompleted.length;
                    slidesWithTasks.push(sname);
                }
            });

            if (finalTotal === 0) {
                isAgentProcessing = false;
                updateSubmitButtonsState(false);
                if (agentStatusIndicator) {
                    agentStatusIndicator.style.display = "none";
                }
                showToast("所有页面修改点此前均已处理完成并生效，无需重复提交。", "info", "全部已是最新");
                return;
            }

            slidesWithTasks.forEach(function (s) { submittedSlides.add(s); });
            lastProcessedTime = Date.now() / 1000;

            return fetch("/api/submit-tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            })
                .then(jsonOrThrow)
                .then(function (data) {
                    return loadAllTasks().then(function () {
                        var count = data.task_count || finalTotal;
                        var slidesCount = (data.submitted_files || slidesWithTasks).length;
                        showToast(
                            t("toast_submit_all_success")
                                .replace("{count}", count)
                                .replace("{slides}", slidesCount),
                            "success",
                            "全部提交成功"
                        );
                    });
                });
        }).catch(function (err) {
            isAgentProcessing = false;
            updateSubmitButtonsState(false);
            if (agentStatusIndicator) {
                agentStatusIndicator.style.display = "none";
            }
            showError("全部提交失败: " + (err.message || err));
        });
    }

    function checkAgentStatus() {
        fetch("/api/agent-status")
            .then(function (res) { return res.json(); })
            .then(function (data) {
                var flagExists = !!data.flag_exists;
                var isBackendProcessing = flagExists || (data.status === "processing");
                var recentDone = data.recent_done;

                if (isBackendProcessing) {
                    // Backend is genuinely actively working on tasks
                    if (agentStatusIndicator) agentStatusIndicator.style.display = "flex";
                    if (agentLastDoneIndicator) agentLastDoneIndicator.style.display = "none";
                } else {
                    // Backend is idle: guarantee spinner indicator is hidden!
                    if (agentStatusIndicator) agentStatusIndicator.style.display = "none";

                    // Show last done summary banner if available
                    if (recentDone && agentLastDoneIndicator && lastDoneSummary) {
                        agentLastDoneIndicator.style.display = "flex";
                        var timeStr = recentDone.completed_at
                            ? new Date(recentDone.completed_at * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
                            : "";
                        lastDoneSummary.textContent = (recentDone.summary || "后台修改已生效") + (timeStr ? " [" + timeStr + "]" : "");
                    }
                }

                if (isAgentProcessing && !isBackendProcessing) {
                    // User submitted from this tab, and backend has finished
                    isAgentProcessing = false;
                    updateSubmitButtonsState(false);
                    if (agentStatusIndicator) {
                        agentStatusIndicator.style.display = "none";
                    }

                    var doneSlide = (recentDone && recentDone.slide) || currentSlide;
                    var doneSummary = (recentDone && recentDone.summary) || "后台修改已生效";
                    lastProcessedTime = (recentDone && recentDone.completed_at) || (Date.now() / 1000);

                    var targetShowSlide = (doneSlide && doneSlide !== "all") ? doneSlide : currentSlide;
                    showAgentDoneToast(targetShowSlide || "1", doneSummary);

                    loadSlides().then(function () {
                        if (currentSlide) {
                            selectSlide(currentSlide);
                        }
                        loadAllTasks();
                    });
                } else if (!isBackendProcessing && recentDone && recentDone.completed_at > lastProcessedTime) {
                    // Task completed externally while user was looking at slide
                    lastProcessedTime = recentDone.completed_at;
                    if (agentStatusIndicator) {
                        agentStatusIndicator.style.display = "none";
                    }
                    updateSubmitButtonsState(false);

                    var extSlide = recentDone.slide;
                    showAgentDoneToast(extSlide !== "all" ? extSlide : (currentSlide || "1"), recentDone.summary);
                    loadSlides().then(function () {
                        if (currentSlide) {
                            selectSlide(currentSlide);
                        }
                        loadAllTasks();
                    });
                }
            })
            .catch(function () {});
    }

    function setupCanvasDblClickAgent() {
        if (!svgContent) return;
        svgContent.addEventListener("dblclick", function (e) {
            var target = e.target;
            if (!target) return;
            if (target.closest && target.closest("defs, style, title, desc")) return;

            var svg = svgContent.querySelector("svg");
            var picked = e.altKey && target.closest
                ? target.closest("g[id]")
                : null;
            picked = picked || (target.closest && target.closest("[data-icon][id]")) ||
                (target.closest && target.closest("[id]"));

            if (picked === svg) picked = null;

            e.preventDefault();
            e.stopPropagation();

            var targetId = "__page__";
            var isPage = true;

            if (picked && picked.id) {
                selectElement(picked, false);
                targetId = picked.id;
                isPage = false;
                currentAgentTarget = targetId;
                if (agentTargetBadge) {
                    var tag = picked.tagName ? picked.tagName.toLowerCase() : "el";
                    agentTargetBadge.textContent = "<" + tag + " #" + targetId + ">";
                    agentTargetBadge.setAttribute("data-target", targetId);
                }
                if (btnTargetToggle) {
                    btnTargetToggle.textContent = t("btn_target_all");
                }
            } else {
                clearSelection();
                currentAgentTarget = "__page__";
                if (agentTargetBadge) {
                    agentTargetBadge.textContent = t("target_page");
                    agentTargetBadge.setAttribute("data-target", "__page__");
                }
            }

            // 1. Tab页变到 Agent 修改
            if (tabManual && tabAgent) {
                tabAgent.classList.add("active");
                tabManual.classList.remove("active");
                if (sectionAgent) sectionAgent.style.display = "";
                if (sectionManual) sectionManual.style.display = "none";
            }

            // 2. 双击弹出 Agent 修改点
            showAnnotationPopover([targetId], isPage);

            if (agentPointText) {
                agentPointText.focus();
            }
        });
    }

    function initAgentTasksUI() {
        if (tabManual && tabAgent) {
            tabManual.addEventListener("click", function () {
                tabManual.classList.add("active");
                tabAgent.classList.remove("active");
                if (sectionManual) sectionManual.style.display = "";
                if (sectionAgent) sectionAgent.style.display = "none";
            });
            tabAgent.addEventListener("click", function () {
                tabAgent.classList.add("active");
                tabManual.classList.remove("active");
                if (sectionAgent) sectionAgent.style.display = "";
                if (sectionManual) sectionManual.style.display = "none";
            });
        }

        if (btnTargetToggle) {
            btnTargetToggle.addEventListener("click", function () {
                if (currentAgentTarget === "__page__") {
                    if (selectedElementIds.size > 0) {
                        currentAgentTarget = selectedElementIds.values().next().value;
                        if (agentTargetBadge) {
                            agentTargetBadge.textContent = "#" + currentAgentTarget;
                            agentTargetBadge.setAttribute("data-target", currentAgentTarget);
                        }
                        btnTargetToggle.textContent = t("btn_target_all");
                    }
                } else {
                    currentAgentTarget = "__page__";
                    if (agentTargetBadge) {
                        agentTargetBadge.textContent = t("target_page");
                        agentTargetBadge.setAttribute("data-target", "__page__");
                    }
                    btnTargetToggle.textContent = selectedElementIds.size > 0 ? t("btn_target_elem") : t("btn_target_all");
                }
            });
        }

        if (btnAddPoint) {
            btnAddPoint.addEventListener("click", addSlideTask);
        }

        if (agentPointText) {
            agentPointText.addEventListener("input", function () {
                updateAllTasksUI();
            });
            agentPointText.addEventListener("keydown", function (e) {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    addSlideTask();
                }
            });
        }

        if (btnSubmitAgent) {
            btnSubmitAgent.addEventListener("click", submitAgentTasks);
        }

        if (btnStagePoint) {
            btnStagePoint.addEventListener("click", stageCurrentSlideTasks);
        }

        if (btnStageAgent) {
            btnStageAgent.addEventListener("click", stageCurrentSlideTasks);
        }

        if (btnSubmitAllAgent) {
            btnSubmitAllAgent.addEventListener("click", submitAllAgentTasks);
        }

        if (toastClose) {
            toastClose.addEventListener("click", function () {
                if (agentNotificationToast) agentNotificationToast.style.display = "none";
            });
        }

        loadAllTasks();

        setupCanvasDblClickAgent();
    }

    initThemeSelectors();
    initAgentTasksUI();

    if (btnUndo) btnUndo.addEventListener("click", runUndo);
})();
