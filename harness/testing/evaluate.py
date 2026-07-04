#!/usr/bin/env python3
"""
Post-run evaluation for the ppt-master-plus beautify test harness.

Usage:
    python3 evaluate.py <run_dir> <original_pptx>

Phases:
  1. Locate the exported PPTX in the run directory.
  2. Automated checks: text fidelity + page count via ppt_to_md.py.
  3. AI judgment via `claude -p` — structured JSON rubric score.
  4. Human judgment — interactive score + notes from stdin.
  5. Save evaluation.json and print a summary.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


# ── Helpers ──────────────────────────────────────────────────────────────────

def find_skill_dir() -> Path:
    """Walk up from this file to the skill root (contains SKILL.md)."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "SKILL.md").exists():
            return parent
    raise RuntimeError("Could not find skill root (directory containing SKILL.md)")


def find_output_pptx(run_dir: Path) -> Path | None:
    """Return the first exported PPTX found under run_dir/projects/*/exports/."""
    for candidate in sorted(run_dir.glob("projects/*/exports/*.pptx")):
        return candidate
    return None


def extract_text(pptx_path: Path, md_out: Path, skill_dir: Path) -> str:
    """Run ppt_to_md.py and return the resulting Markdown text."""
    script = skill_dir / "scripts" / "source_to_md" / "ppt_to_md.py"
    result = subprocess.run(
        ["python3", str(script), str(pptx_path), "-o", str(md_out)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  [warn] ppt_to_md.py exited {result.returncode}: {result.stderr[:200]}")
    if md_out.exists():
        return md_out.read_text(encoding="utf-8", errors="replace")
    return ""


def count_slides_from_md(md_text: str) -> int:
    """Count slide separators (## Slide N or --- blocks) in extracted Markdown."""
    slide_headers = re.findall(r"^##\s+Slide\s+\d+", md_text, re.MULTILINE)
    if slide_headers:
        return len(slide_headers)
    # Fallback: count horizontal-rule slide separators
    return len(re.findall(r"^\s*---\s*$", md_text, re.MULTILINE))


def check_text_fidelity(original_md: str, output_md: str) -> tuple[bool, list[str]]:
    """Check that all non-trivial text segments from original appear in output.

    Filters out Markdown image paths, file paths, and hex values — ppt_to_md
    embeds extracted image filenames that won't appear as slide text in the output.
    """
    missing = []
    # Common image/file extension words that appear in ppt_to_md paths but not slide text
    _ARTIFACT_WORDS = {"png", "jpg", "jpeg", "gif", "svg", "webp", "bmp", "tiff",
                       "pptx", "docx", "xlsx", "sample", "original", "image", "files"}
    tokens = set(re.findall(r"[^\s,;:.!?\"'()[\]{}<>|#*`\-]{4,}", original_md))
    for token in tokens:
        # Skip file path fragments produced by ppt_to_md extraction
        if re.search(r"[/\\]|_files?|^\d+$|^0x", token, re.IGNORECASE):
            continue
        # Skip bare extension/artifact words
        if token.lower() in _ARTIFACT_WORDS:
            continue
        if token not in output_md:
            missing.append(token)
    passed = len(missing) == 0
    return passed, missing[:20]


def ai_judge(original_md: str, output_md: str, run_dir: Path) -> dict:
    """Ask claude -p to score the beautified output. Returns a dict."""
    prompt = f"""You are evaluating a PPTX beautification result.

ORIGINAL deck text (Markdown):
---
{original_md[:4000]}
---

BEAUTIFIED deck text (Markdown):
---
{output_md[:4000]}
---

Score the beautification on three dimensions (1=very poor, 5=excellent):
1. text_fidelity: Are all original text strings preserved verbatim?
2. layout_improvement: Does the output show better layout/hierarchy/whitespace than a raw source would suggest?
3. visual_coherence: Does the output read as a coherent, professionally structured deck?

Respond with ONLY valid JSON in this exact shape:
{{
  "text_fidelity": <int 1-5>,
  "layout_improvement": <int 1-5>,
  "visual_coherence": <int 1-5>,
  "summary": "<one sentence>",
  "issues": ["<issue1>", "<issue2>"]
}}"""

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "text", prompt],
            capture_output=True, text=True, timeout=120
        )
        raw = result.stdout.strip()
        # Extract JSON object from response
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            return json.loads(m.group())
    except Exception as exc:
        print(f"  [warn] AI judgment failed: {exc}")
    return {
        "text_fidelity": None,
        "layout_improvement": None,
        "visual_coherence": None,
        "summary": "AI judgment unavailable",
        "issues": []
    }


def human_judge(original_pptx: Path, output_pptx: Path) -> dict:
    """Prompt the user to open both files and rate the output.

    Skips gracefully when stdin is not a TTY (automated / piped context).
    """
    print()
    print("─" * 60)
    print("  HUMAN EVALUATION")
    print("─" * 60)
    print(f"\n  Please open and compare these two files:\n")
    print(f"    原始 / Original : {original_pptx}")
    print(f"    美化 / Beautified: {output_pptx}")

    if not sys.stdin.isatty():
        print("\n  (非交互式环境 / Non-interactive — skipping human score)")
        print(f"  Run manually: python3 evaluate.py {original_pptx.parent.parent.parent.name}/ "
              f"original-sample.pptx")
        return {"score": None, "notes": "skipped (non-interactive)"}

    # Try to open both files automatically
    for path in (original_pptx, output_pptx):
        try:
            subprocess.Popen(["open", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    print()
    print("  评分 / Score 1-5:")
    print("    1 = 效果更差 / worse")
    print("    3 = 差不多   / about the same")
    print("    5 = 明显更好 / clearly better")
    print()

    score = None
    while score is None:
        try:
            raw = input("  你的评分 / Your score (1-5): ").strip()
            v = int(raw)
            if 1 <= v <= 5:
                score = v
            else:
                print("  请输入 1 到 5 的整数。")
        except (ValueError, EOFError):
            print("  跳过人工评分。/ Skipping human score.")
            score = None
            break

    notes = ""
    try:
        notes = input("  备注 / Notes (optional, press Enter to skip): ").strip()
    except EOFError:
        pass

    return {"score": score, "notes": notes}


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <run_dir> <original_pptx>", file=sys.stderr)
        sys.exit(1)

    run_dir = Path(sys.argv[1]).resolve()
    original_pptx = Path(sys.argv[2]).resolve()
    skill_dir = find_skill_dir()
    run_id = run_dir.name

    print(f"\n  Evaluating run: {run_id}")
    print(f"  Run dir : {run_dir}")
    print(f"  Original: {original_pptx}")

    # ── Phase 1: locate output ───────────────────────────────────────────────

    output_pptx = find_output_pptx(run_dir)
    if output_pptx is None:
        print("\n  ✗ No exported PPTX found in projects/*/exports/.")
        print("    The beautify workflow may not have completed.")
        result = {
            "run_id": run_id,
            "original": str(original_pptx),
            "output": None,
            "automated": {"page_count_match": False, "text_fidelity_pass": False, "missing_strings": []},
            "ai_judgment": {"summary": "No output found", "issues": ["Workflow did not complete"]},
            "human_judgment": {"score": None, "notes": ""},
            "overall_pass": False,
        }
        out_path = run_dir / "evaluation.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n  Saved: {out_path}")
        sys.exit(1)

    print(f"  Output  : {output_pptx}")

    # ── Phase 2: automated checks ────────────────────────────────────────────

    print("\n  [1/4] Automated checks...")
    orig_md_path = run_dir / "original_text.md"
    out_md_path = run_dir / "output_text.md"

    original_md = extract_text(original_pptx, orig_md_path, skill_dir)
    output_md = extract_text(output_pptx, out_md_path, skill_dir)

    orig_slides = count_slides_from_md(original_md)
    out_slides = count_slides_from_md(output_md)
    page_count_match = (orig_slides > 0 and orig_slides == out_slides) or orig_slides == 0

    fidelity_pass, missing = check_text_fidelity(original_md, output_md)

    print(f"    Slide count — original: {orig_slides}, output: {out_slides} "
          f"{'✓' if page_count_match else '✗'}")
    print(f"    Text fidelity {'✓' if fidelity_pass else f'✗  ({len(missing)} missing tokens)'}")
    if missing:
        print(f"    Missing (sample): {missing[:5]}")

    automated = {
        "original_slide_count": orig_slides,
        "output_slide_count": out_slides,
        "page_count_match": page_count_match,
        "text_fidelity_pass": fidelity_pass,
        "missing_strings": missing,
    }

    # ── Phase 3: AI judgment ─────────────────────────────────────────────────

    print("\n  [2/4] AI judgment (claude -p)...")
    ai = ai_judge(original_md, output_md, run_dir)
    print(f"    text_fidelity    : {ai.get('text_fidelity')}/5")
    print(f"    layout_improvement: {ai.get('layout_improvement')}/5")
    print(f"    visual_coherence : {ai.get('visual_coherence')}/5")
    print(f"    summary          : {ai.get('summary', '')}")
    if ai.get("issues"):
        print(f"    issues           : {ai['issues']}")

    # ── Phase 4: human judgment ──────────────────────────────────────────────

    print("\n  [3/4] Human judgment...")
    human = human_judge(original_pptx, output_pptx)
    if human["score"] is not None:
        print(f"\n    Score: {human['score']}/5")
    if human["notes"]:
        print(f"    Notes: {human['notes']}")

    # ── Phase 5: save results ────────────────────────────────────────────────

    ai_scores = [v for v in (ai.get("text_fidelity"), ai.get("layout_improvement"), ai.get("visual_coherence"))
                 if v is not None]
    ai_avg = sum(ai_scores) / len(ai_scores) if ai_scores else 0
    overall_pass = (
        fidelity_pass
        and page_count_match
        and ai_avg >= 3.0
        and (human["score"] is None or human["score"] >= 3)
    )

    result = {
        "run_id": run_id,
        "original": str(original_pptx),
        "output": str(output_pptx),
        "automated": automated,
        "ai_judgment": ai,
        "human_judgment": human,
        "overall_pass": overall_pass,
    }

    out_path = run_dir / "evaluation.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n  [4/4] Results saved.")
    print()
    print("═" * 60)
    print(f"  {'✓ PASS' if overall_pass else '✗ FAIL'}  — Run {run_id}")
    print(f"  Text fidelity : {'pass' if fidelity_pass else 'FAIL'}")
    print(f"  Page count    : {'match' if page_count_match else 'MISMATCH'} "
          f"({orig_slides} → {out_slides})")
    if ai_avg:
        print(f"  AI avg score  : {ai_avg:.1f}/5")
    if human["score"] is not None:
        print(f"  Human score   : {human['score']}/5")
    print(f"  Evaluation    : {out_path}")
    print("═" * 60)


if __name__ == "__main__":
    main()
