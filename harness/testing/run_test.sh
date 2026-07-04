#!/usr/bin/env bash
# Test harness for ppt-master-plus beautify workflow.
# Usage: ./run_test.sh [claude|codex]
#
# Copies original-sample.pptx into a timestamped run directory,
# launches the chosen AI agent interactively with a beautify prompt,
# then runs evaluate.py after the session exits.
#
# IMPORTANT: original-sample.pptx is NEVER moved or modified.

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HARNESS_DIR/../.." && pwd)"
ORIGINAL="$HARNESS_DIR/original-sample.pptx"
AGENT="${1:-claude}"

# ── Sanity checks ────────────────────────────────────────────────────────────

if [ ! -f "$ORIGINAL" ]; then
    echo "ERROR: original-sample.pptx not found at $HARNESS_DIR" >&2
    exit 1
fi

ORIGINAL_HASH=$(shasum -a 256 "$ORIGINAL" | awk '{print $1}')

case "$AGENT" in
    claude|codex) ;;
    *)
        echo "ERROR: unknown agent '$AGENT'. Use 'claude' or 'codex'." >&2
        exit 1
        ;;
esac

if ! command -v "$AGENT" &>/dev/null; then
    echo "ERROR: '$AGENT' not found in PATH." >&2
    exit 1
fi

# ── Create run directory ─────────────────────────────────────────────────────

RUN_TS=$(date +%Y%m%d_%H%M%S)
RUN_DIR="$HARNESS_DIR/runs/$RUN_TS"
mkdir -p "$RUN_DIR/projects"

# Copy (NEVER move) the original PPTX as the test input
cp "$ORIGINAL" "$RUN_DIR/test-input.pptx"

echo "════════════════════════════════════════════════════════"
echo "  ppt-master-plus beautify test run"
echo "  Run ID : $RUN_TS"
echo "  Agent  : $AGENT"
echo "  Input  : $RUN_DIR/test-input.pptx"
echo "  Output : $RUN_DIR/projects/<name>/exports/"
echo "════════════════════════════════════════════════════════"
echo ""
echo "The AI agent will start below. Interact with the browser confirm UI"
echo "when it opens, then let the agent complete SVG generation and export."
echo "Exit the agent session (Ctrl+D or finish) to proceed to evaluation."
echo ""

# ── Build the initial prompt ─────────────────────────────────────────────────

PROMPT="你是 ppt-master-plus skill。请对以下文件运行完整的 beautify（美化）工作流：

  文件路径: $RUN_DIR/test-input.pptx

请完整执行所有步骤，包括：
1. 读取源文件并初始化项目（项目创建在 $RUN_DIR/projects/ 下）
2. 提取视觉标识信息
3. 通过 confirm UI 确认配色/字体/设置（浏览器会自动打开）
4. 生成所有 SVG 页面
5. 导出 PPTX 到 exports/ 目录

注意：这是一个测试运行，请不要修改 $HARNESS_DIR/original-sample.pptx。"

# ── Launch agent ─────────────────────────────────────────────────────────────

cd "$RUN_DIR"

case "$AGENT" in
    claude)
        claude \
            --add-dir "$SKILL_DIR" \
            --permission-mode bypassPermissions \
            "$PROMPT"
        ;;
    codex)
        codex "$PROMPT"
        ;;
esac

# ── Verify original is still untouched ──────────────────────────────────────

ORIGINAL_HASH_AFTER=$(shasum -a 256 "$ORIGINAL" | awk '{print $1}')
if [ "$ORIGINAL_HASH" != "$ORIGINAL_HASH_AFTER" ]; then
    echo ""
    echo "⚠️  WARNING: original-sample.pptx hash changed during the run!" >&2
    echo "   Before: $ORIGINAL_HASH" >&2
    echo "   After : $ORIGINAL_HASH_AFTER" >&2
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Agent session ended. Running evaluation..."
echo "════════════════════════════════════════════════════════"
echo ""

# ── Evaluate ─────────────────────────────────────────────────────────────────

python3 "$HARNESS_DIR/evaluate.py" "$RUN_DIR" "$ORIGINAL"
