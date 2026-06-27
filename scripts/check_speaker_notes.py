#!/usr/bin/env python3
"""Validate speaker-note coverage and minimum talk-track quality."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from total_md_split import find_svg_files, parse_total_md


PLACEHOLDERS = (
    "TODO",
    "TBD",
    "待补充",
    "讲稿要点",
    "此处介绍",
    "照着页面讲",
)


def _paragraphs(text: str) -> list[str]:
    return [
        block.strip()
        for block in re.split(r"\n\s*\n", text.strip())
        if block.strip()
    ]


def _is_bullet_heavy(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    bullets = sum(bool(re.match(r"^(?:[-*+]|\d+[.)])\s+", line)) for line in lines)
    return bullets >= 2 and bullets / len(lines) >= 0.5


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_path", type=Path)
    args = parser.parse_args()

    project = args.project_path.resolve()
    notes_path = project / "notes" / "total.md"
    svg_files = find_svg_files(project)
    if not svg_files:
        return 2
    if not notes_path.exists():
        print(f"[ERROR] Missing {notes_path}")
        return 2

    stems = [path.stem for path in svg_files]
    notes = parse_total_md(notes_path, stems, verbose=False)
    errors: list[str] = []
    warnings: list[str] = []

    for index, stem in enumerate(stems):
        text = notes.get(stem, "").strip()
        if not text:
            errors.append(f"{stem}: missing notes")
            continue

        paragraphs = _paragraphs(text)
        cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
        word_count = len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text))
        is_cjk = cjk_count >= word_count
        is_brief_slide = index == 0 or "封面" in stem or "目录" in stem or "章节" in stem

        if len(paragraphs) < 3:
            errors.append(f"{stem}: only {len(paragraphs)} paragraph(s); require at least 3")
        if _is_bullet_heavy(text):
            errors.append(f"{stem}: notes are bullet-heavy; write connected spoken prose")

        if is_cjk:
            minimum = 200 if is_brief_slide else 280
            if cjk_count < minimum:
                errors.append(f"{stem}: {cjk_count} Chinese characters; minimum is {minimum}")
            if cjk_count > 650:
                warnings.append(f"{stem}: {cjk_count} Chinese characters may be too long")
        else:
            minimum = 140 if is_brief_slide else 200
            if word_count < minimum:
                errors.append(f"{stem}: {word_count} English words; minimum is {minimum}")
            if word_count > 500:
                warnings.append(f"{stem}: {word_count} English words may be too long")

        for placeholder in PLACEHOLDERS:
            if placeholder.lower() in text.lower():
                errors.append(f"{stem}: contains placeholder phrase {placeholder!r}")

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")

    if errors:
        print(f"\n[FAIL] {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"[OK] {len(stems)} slide note(s) passed; {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
