---
description: Start the browser SVG editor when it is not running, and apply submitted annotations before or after PPTX export
---

# Live Preview Workflow

> **Purpose**: (1) start/reopen the browser SVG editor when no preview service is currently running, (2) provide per-slide instant manual editing (修改即生效, auto-saved to disk immediately), and (3) provide per-slide Agent modification task submission ("列完修改点后提交后台处理"), where submitted points wake the backend agent, and upon completion, the preview automatically updates with completion toast notifications.
>
> **Not in scope**: Executor's mandatory auto-startup — that lives in [`SKILL.md`](../SKILL.md) Step 6. Do not re-launch a preview that is already running.

## When to Run

- **Start (Step 1)** — preview service is not currently running and the user wants to look at the deck or click an element. Typical cases: post-export re-entry in a fresh chat, or the user clicked **Exit preview** earlier and now wants it back.
- **Apply annotations (Step 2)** — triggered automatically when `--wait-annotation` returns (user clicked **提交后台处理** / **Apply changes** in the browser). Manual fallback triggers are also accepted:
  - Quoting the browser success dialog (`Changes saved to svg_output...` / `修改已保存到 svg_output...` / `任务已提交后台处理...`)
  - Saying `apply my annotations` / `apply my edits` / `应用注解` / `开始应用` / equivalent

## When NOT to Run

- The preview service is already running → just give the user the URL; do not restart.
- The user gave a precise chat edit ("change page 3 title to X") → edit the SVG directly.
- The user wants a full regeneration → use the main workflow.
- An annotation targets a slide that does not yet exist in `svg_output/` → report that page as pending and apply it after the page is generated.

---

## Step 1: Start / reopen the editor

**Precondition**: no preview service running on this project.

```bash
python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --daemon
```

(Plain mode — no `--live`. The `--live` flag is reserved for Step 6's auto-startup.)

The launcher binds `127.0.0.1:5050` (or the next free port), starts the server in the background, writes runtime files under `<project_path>/live_preview/`, opens the browser on a local desktop when possible, and edits `<project_path>/svg_output/` in place. After it prints the running URL, tell the user in their language, in one short message:

- editor is at the URL reported by the launcher, e.g. `http://localhost:5050`
- **Direct manual edit (直接手动修改，修改即生效)**: on the **✍️ 手动修改 (Manual Edit)** tab (activated by default on single-click selection): change text, typography, colors, coordinates, or drag to move → changes take effect and persist immediately to `svg_output/<slide>.svg` on disk with live status indicator ("● 已实时保存" / "● Live saved"). Properties layout naturally without internal scrollbars. `Ctrl+Z` or the **Undo** button restores previous states directly from disk undo snapshots. Re-export stays chat-driven: say "re-export" / "重新导出" to refresh the PPTX.
- **Agent modification (每页列完修改点后提交后台处理)**: double-click any element on canvas to pop up the Agent modification point dialog and switch to the **🤖 Agent 修改 (Agent Edit)** tab. Add modification points to the checklist → click **"🚀 提交后台处理" (Submit for Agent Processing)**. The AI waits for that save event and starts the repair automatically (the dialog's copyable prompt with the affected page number is only a manual fallback). The server writes annotation markers, saves `live_preview/agent_tasks.json`, and raises `live_preview/annotations_ready.flag`.
- **Processing & Notification (处理完预览生效且有提示信息)**: The agent / backend repair loop processes the tasks, verifies quality, and marks them complete (`--mark-done <slide> --summary "..."`). The preview automatically detects completion, refreshes the slide SVG preview, and displays a floating completion notification toast.
- to skip the editor, just describe the change in chat

Do not wait for confirmation before launching — the user already asked for preview, so launching is the response. If another project already holds the port, the launcher auto-advances to the next free one — report the actual URL from the launch log (`--port <other>` still forces a specific port). Remote access → see the appendix.

**After delivering the startup message above, enter the annotation-wait loop** — but only when this step is triggered outside of an active generation cycle (e.g., post-export re-entry or the user reopened the editor after clicking Exit preview).

Tell the user (in their language, one short sentence): "I'm ready — annotate slides in the browser, click **Apply changes**, and I'll apply them automatically. No need to send any message."

Then run the blocking wait command (long tool timeout — 600000 ms):

```bash
python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --wait-annotation
```

**Codex / desktop-agent adapter**: in tools where the browser cannot directly wake the AI, run the same wait as a separate long-running terminal/tool session and keep the session id:

```bash
python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --wait-annotation --timeout 0
```

Poll or resume that session while the preview is open. When it exits 0, treat that as the browser's **Apply changes** event and continue with Step 2 immediately. After Step 2 deletes `annotations_ready.flag`, start a new wait session so the next browser annotation round is also automatic. Repeat this repair → delete flag → re-arm wait cycle after every batch of annotations until the user stops preview or the workflow ends. The copyable browser prompt is only a fallback for tools that failed to keep this wait session alive.

This command blocks silently until the user clicks **Apply changes** with at least one annotation saved, at which point it exits 0. When it returns:

1. Run Step 2 to apply all pending annotations.
2. Delete the flag so the next wait starts fresh:
   ```bash
   rm <project_path>/live_preview/annotations_ready.flag
   ```
3. Loop back: run `--wait-annotation` again to wait for the next round.

Repeat this loop until the user explicitly stops the preview ("stop preview" / "停止预览" / clicks **Exit preview** in the browser) or starts a full regeneration — then do not re-enter the wait. A repaired slide may prompt the user to submit another batch of annotations; that is normal and must be captured by the re-armed listener without requiring a chat message.

**During active generation**: Step 6 owns the wait loop because the AI must keep page-generation state. Keep one `--wait-annotation` listener attached to the running live preview while generating. When it returns, pause at the current safe checkpoint, run Step 2, delete `annotations_ready.flag`, then resume the correct mode:
- `gated` / 逐页精修: re-preview the repaired slide and wait for explicit user approval before generating the next page.
- `continuous`: resume the continuous generation/export flow after SVG checks pass.

For Codex Desktop specifically, this listener is a background `exec_command` / terminal session blocked on `--wait-annotation --timeout 0`; poll it at each safe checkpoint and after each page write. When it returns, complete Step 2, delete the flag, then immediately open another blocked wait session before showing the repaired result or continuing generation. Do not rely on the user pasting the browser fallback prompt to start the repair.

---

## Step 2: Apply submitted annotations

🚧 **GATE**: every annotation being applied targets an SVG that already exists in `<project_path>/svg_output/`. A prior PPTX export is not required.

Triggered automatically by the browser save event (`--wait-annotation`) or by the manual fallback signals listed in "When to Run".

1. Discover annotations:
   ```bash
   python3 ${SKILL_DIR}/scripts/check_annotations.py <project_path>
   ```
   The output already lists each pending change as `file → element_id → annotation text → content preview`. Use it directly as the to-do list; no need to re-parse SVG attributes yourself.
2. If the output says no annotations: tell the user, stop.
3. For each listed annotation:
   - Re-read `<project_path>/spec_lock.md` before editing that page.
   - Edit the targeted element in `<project_path>/svg_output/<file>` per the annotation text.
   - **Must remove the resolved annotation markers**: delete `data-edit-target` and `data-edit-annotation` from that element after applying the requested change. Never leave already-fixed annotations in `svg_output`.
   - Append one `annotation_applied` JSONL record to `<project_path>/live_preview/annotations.jsonl` with `ts`, `file`, `element_id`, and the original annotation text.
4. Validate the repaired SVGs:
   ```bash
   python3 ${SKILL_DIR}/scripts/svg_quality_checker.py <project_path>
   ```
   Fix every error before continuing. If the annotation materially changes slide content, update its speaker notes. Run the full notes checker only when all deck notes exist; otherwise defer that deck-wide check to the normal notes gate.
5. Choose the output action by project state:
   - **Before the first export**: do not create a partial PPTX. Return to Live Preview; in `Gated` mode wait for approval of the repaired slide, and in `Continuous` mode resume generation.
   - **After an export exists**: re-export the updated deck:
     ```bash
     python3 ${SKILL_DIR}/scripts/finalize_svg.py <project_path>
     python3 ${SKILL_DIR}/scripts/svg_to_pptx.py <project_path>
     ```
6. **Mark Done & Notify UI**:
   Notify the Live Preview UI that agent processing is complete so the slide reloads and shows the toast notification:
   ```bash
   python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --mark-done <slide_name> --summary "已完成修改点调整"
   ```
   (Alternatively, deleting `annotations_ready.flag` will also trigger automatic reload upon mtime update).
7. Tell the user (in their language): annotations applied, markers removed, validation passed, and whether a new PPTX was exported. The browser live preview automatically refreshes with a completion toast notification.
8. Loop: more annotations submitted → repeat from step 1. User signals done or "stop preview" → end.

---

## Notes (editor invariants — referenced from SKILL.md Step 6)

- **UI**: bilingual (EN/中); auto-detects from `navigator.language`, persists in `localStorage`, toggled via the **中 / EN** button on the right panel. Slide navigation: first/prev/next/last buttons at the top of the center panel, plus `←` / `→` / `Home` / `End` (suppressed while typing in textareas/inputs).
- **Two-Tab Right Panel**:
  - **✍️ 手动修改 (Manual Edit)**: Direct manual edits take effect immediately and are saved to disk (`svg_output/<slide>.svg`) in real time, accompanied by a pulsing green status indicator ("● 已实时保存" / "● Live saved"). Single-clicking any element activates this tab and cleanly displays all editable properties without internal scrollbars. Supports text content, typography, colors, geometry, drag-and-drop on canvas, and arrow nudges. `Ctrl+Z` or the **Undo** button restores previous states from the disk-backed undo stack (up to 50 snapshots).
  - **🤖 Agent 修改 (Agent Edit)**: Double-clicking any element on canvas pops up the Agent task modal and switches to this tab. Users can target specific elements or whole-slide modifications, add modification points to the checklist, and click **"🚀 提交后台处理" (Submit for Agent Processing)**.
- **Background Processing & Completion Toast**: When **提交后台处理** is clicked, the server writes annotation markers into SVG, updates `live_preview/agent_tasks.json`, and raises `live_preview/annotations_ready.flag`. The copyable prompt includes the affected page number(s) as a manual fallback. While the agent is working, the UI shows a "⏳ 后台处理中..." indicator. Once completed via `--mark-done` or flag removal, the UI automatically refreshes the SVG preview and displays a floating completion toast notification ("🎉 后台 Agent 修改完成！已自动刷新预览").
- **Agent adapters**: Antigravity CLI and similar always-on agents keep the wait loop in their normal execution loop. Codex Desktop and other terminal-backed desktop tools must keep a separate `--wait-annotation --timeout 0` session open, then poll/resume that session to detect browser saves and start repair. After every repair, they run `--mark-done`, delete the flag, and start a new blocked wait session so later submissions are captured.
- **Direct edit (no AI)**: selection mode determines the right-panel surface. Single element = full object inspector (geometry, safe text content, raw SVG attributes except protected fields like `id`, UI `class`, event handlers, and hrefs). SVG `<g>` group = group-level edit surface; select via `Alt/Option` + click or **Select parent group** from a child element. Multi-select = limited batch editor over top-level selected objects only: shared x/y plus `fill` / `stroke` / `opacity`; text style fields appear only when every selected object is `text`/`tspan`. Modifications take effect and persist immediately on disk.
- **Drag to move**: press and drag an already-selected element on the canvas to reposition it; the whole selection moves together under multi-select. Moves track cursor via CTM and auto-persist to disk on release.
- **Double-click Agent modification popup**: double-click any element on the SVG canvas to pop up the Agent modification point dialog (with preset chips and input box) and automatically switch the right panel to the **🤖 Agent 修改** tab.
- **Arrow-key nudge**: with one or more elements selected, `↑ ↓ ← →` moves the selection 1px and `Shift + arrow` moves 10px. Auto-persists to disk.
- **Overlap picker**: right-click anywhere on the canvas to list every selectable element under the pointer (top→bottom). Left-click selects the topmost.
- **Undo**: `Ctrl+Z` or the **Undo** button pops the last state from the server undo stack and restores `svg_output/<slide>.svg` on disk.
- **Re-export is chat-driven**: manual and agent edits update `svg_output/` directly. Before the first export, annotation repair returns to preview without creating a partial deck. After an export exists, applying annotations re-runs finalize + export; direct edits are re-exported when the user asks.
- **Stop conditions**: the service stops when the user clicks **Exit preview** in the browser, asks in chat to stop it, the idle timeout fires, or the process is killed externally.
- **Port**: default `5050`, auto-advancing to the next free port when another project already holds it (report the actual URL from the launch log); force a specific port with `--port <other>`.
- **Idle timeout**: plain mode `900s`, `--live` mode `7200s`; override with `--timeout <seconds>` (`0` disables).
- **Single instance per project**: `<project_path>/live_preview/lock.json` records the running pid + port.
- **Browser preview**: the server inlines `<use data-icon>` placeholders and serves `images/*` so SVG renders correctly; the on-disk SVG is unchanged by this preview.

---

## Appendix: Remote access

If the project lives on a remote Linux server, run with `--no-browser`:

```bash
python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --daemon --no-browser
# or for Step 6's auto-startup on a remote host:
python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --live --daemon --no-browser
```

- **VS Code / Cursor Remote-SSH**: open the **PORTS** panel (`Ctrl+Shift+P` → `Ports: Focus on Ports View`), click **Forward a Port**, enter `5050`. The workspace remembers it.
- **Termius**: open the **Port Forwarding** module from the left sidebar (top-level, not nested). Add a rule with **Type = Local**, Host = your remote, Binding `127.0.0.1:5050`, Destination `127.0.0.1:5050`. Save, then start the rule (▶ button).
- **Plain SSH**: `ssh -L 5050:127.0.0.1:5050 <user>@<host>` (or add `LocalForward 5050 127.0.0.1:5050` to `~/.ssh/config`).

Then open `http://localhost:5050` in your local browser.
