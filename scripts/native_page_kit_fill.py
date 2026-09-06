#!/usr/bin/env python3
"""Fill only declared editable slots in a cloned Brand Page Kit PPTX.

The Page Kit executor writes an adjacent execution roster. This tool applies a
content plan directly to the affected slide XML, leaving every non-text part of
the package (including masters, layouts, relationships, media, and locked
objects) untouched. It deliberately refuses any undeclared or locked shape.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

PML = "http://schemas.openxmlformats.org/presentationml/2006/main"
DRAWING = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"p": PML, "a": DRAWING}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read JSON: {path}") from exc
    if not isinstance(loaded, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return loaded


def _editable_slots(roster: dict[str, Any]) -> dict[int, set[str]]:
    pages = roster.get("pages")
    if not isinstance(pages, list):
        raise ValueError("Execution roster has no pages list")
    result: dict[int, set[str]] = {}
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("Execution roster contains an invalid page")
        slide = page.get("output_slide")
        slots = page.get("editable_slots")
        if not isinstance(slide, int) or slide < 1 or not isinstance(slots, list):
            raise ValueError("Execution roster contains invalid slot metadata")
        result[slide] = {str(slot) for slot in slots}
    return result


def _validate_plan(plan: dict[str, Any], allowed: dict[int, set[str]]) -> dict[int, dict[str, str]]:
    pages = plan.get("slides")
    if not isinstance(pages, list) or not pages:
        raise ValueError("Fill plan must contain a non-empty slides list")
    result: dict[int, dict[str, str]] = {}
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("Fill plan contains an invalid slide entry")
        slide = page.get("slide")
        slots = page.get("slots")
        if not isinstance(slide, int) or slide not in allowed or not isinstance(slots, dict):
            raise ValueError("Fill plan references an unknown slide or invalid slots")
        replacement: dict[str, str] = {}
        for shape_id, text in slots.items():
            shape_key = str(shape_id)
            if shape_key not in allowed[slide]:
                raise ValueError(f"Slide {slide}: shape {shape_key} is not an editable Page Kit slot")
            if not isinstance(text, str) or not text.strip() or "\n" in text:
                raise ValueError(f"Slide {slide}: slot {shape_key} must contain one non-empty line of text")
            replacement[shape_key] = text.strip()
        if not replacement:
            raise ValueError(f"Slide {slide}: no slot replacements supplied")
        if slide in result:
            raise ValueError(f"Fill plan repeats slide {slide}")
        result[slide] = replacement
    return result


def _replace_text(xml: bytes, replacements: dict[str, str]) -> tuple[bytes, set[str]]:
    root = ET.fromstring(xml)
    replaced: set[str] = set()
    for shape in root.findall(".//p:sp", NS):
        c_nv_pr = shape.find("./p:nvSpPr/p:cNvPr", NS)
        if c_nv_pr is None:
            continue
        shape_id = c_nv_pr.get("id")
        if shape_id not in replacements:
            continue
        text_nodes = shape.findall(".//a:t", NS)
        if not text_nodes:
            raise ValueError(f"Shape {shape_id} has no replaceable text runs")
        text_nodes[0].text = replacements[shape_id]
        for node in text_nodes[1:]:
            node.text = ""
        replaced.add(shape_id)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True), replaced


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_pptx", type=Path, help="Native Page Kit carrier PPTX")
    parser.add_argument("--execution-roster", type=Path, required=True, help="*.native_page_kit_execution.json")
    parser.add_argument("--plan", type=Path, required=True, help="JSON mapping of editable slide slots to one-line text")
    parser.add_argument("--output", type=Path, required=True, help="New output PPTX; existing files are refused")
    args = parser.parse_args()

    source = args.input_pptx.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Input PPTX not found: {source}")
    if output.exists():
        raise SystemExit(f"Refusing to overwrite output: {output}")
    roster = _load_json(args.execution_roster.expanduser().resolve())
    plan = _validate_plan(_load_json(args.plan.expanduser().resolve()), _editable_slots(roster))
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="ppt-master-plus-page-kit-") as temporary:
        staged = Path(temporary) / output.name
        try:
            with zipfile.ZipFile(source, "r") as source_zip, zipfile.ZipFile(staged, "w") as target_zip:
                remaining = {slide: set(slots) for slide, slots in plan.items()}
                for info in source_zip.infolist():
                    payload = source_zip.read(info.filename)
                    if info.filename.startswith("ppt/slides/slide") and info.filename.endswith(".xml"):
                        stem = info.filename.rsplit("/", 1)[-1][5:-4]
                        if stem.isdigit() and int(stem) in plan:
                            payload, changed = _replace_text(payload, plan[int(stem)])
                            remaining[int(stem)] -= changed
                    target_zip.writestr(info, payload)
        except (OSError, zipfile.BadZipFile, ET.ParseError) as exc:
            raise SystemExit(f"Native Page Kit fill failed: {exc}") from exc
        unresolved = {slide: sorted(slots) for slide, slots in remaining.items() if slots}
        if unresolved:
            raise SystemExit(f"Declared editable slots were not found in PPTX: {unresolved}")
        shutil.move(staged, output)
    os.chmod(output, 0o644)
    print(f"[OK] Filled Page Kit slots without changing locked objects: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
