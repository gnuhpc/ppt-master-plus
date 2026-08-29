#!/usr/bin/env python3
"""Template-specific analysis layered onto the standard PPTX intake.

The public entry remains ``pptx_intake.py --intent template``.  This module
contains only the additional template interpretation and preview helpers; OOXML
content facts continue to come from the standard identity and slide-library
analyzers.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
from typing import Any, Iterable
from xml.etree import ElementTree as ET
from zipfile import ZipFile


PML = "http://schemas.openxmlformats.org/presentationml/2006/main"
DML = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"p": PML, "a": DML, "r": REL, "pr": PKG_REL}

GUIDE_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bfonts?\b|字体|字号",
        r"\bcolou?r\b|色彩|配色|颜色使用",
        r"\bicons?\b|图标样式|icon\s*样式",
        r"\blogos?\b.*(?:样式|规范)|联合\s*logo|客户\s*logo",
        r"design\s*(?:guide|system)|设计规范|使用规范",
    )
)
PLACEHOLDER_CUES = re.compile(
    r"请(?:填写|添加|替换)|这里是|占位|placeholder|限制.{0,8}(?:行|字)|"
    r"不超过.{0,8}(?:行|字)|可删除",
    re.IGNORECASE,
)
TITLE_CUES = re.compile(r"标题|title|headline|章节|chapter", re.IGNORECASE)
BODY_CUES = re.compile(r"正文|内容|body|description|说明", re.IGNORECASE)
NUMBER_CUES = re.compile(r"数字|比例|百分比|metric|kpi|\bxx%", re.IGNORECASE)
LOGO_CUES = re.compile(r"\blogos?\b|标志|标识", re.IGNORECASE)
ICON_CUES = re.compile(r"\bicons?\b|图标", re.IGNORECASE)
IMAGE_SLOT_CUES = re.compile(r"图片|照片|配图|image\s+slot|photo\s+slot", re.IGNORECASE)
FONT_HINT = re.compile(
    r"Microsoft\s+YaHei|微软雅黑|方正[\w\u4e00-\u9fff]+|Arial|Calibri|"
    r"PingFang\s+SC|苹方|思源[\w\u4e00-\u9fff]+|Noto\s+Sans[\w -]*",
    re.IGNORECASE,
)
HEX_COLOR = re.compile(r"#[0-9a-fA-F]{6}\b")


def _tag(name: str) -> str:
    prefix, local = name.split(":", 1)
    return f"{{{NS[prefix]}}}{local}"


def _xml(package: ZipFile, name: str) -> ET.Element:
    return ET.fromstring(package.read(name))


def _relationship_part(part: str) -> str:
    path = PurePosixPath(part)
    return str(path.parent / "_rels" / f"{path.name}.rels")


def _resolve_target(part: str, target: str) -> str:
    base = PurePosixPath(part).parent
    pieces: list[str] = []
    for piece in (base / target).parts:
        if piece == ".":
            continue
        if piece == "..":
            if pieces:
                pieces.pop()
            continue
        pieces.append(piece)
    return "/".join(pieces)


def _relationships(package: ZipFile, part: str) -> list[dict[str, str]]:
    rel_name = _relationship_part(part)
    if rel_name not in package.namelist():
        return []
    rows: list[dict[str, str]] = []
    for rel in _xml(package, rel_name).findall("pr:Relationship", NS):
        target = rel.get("Target", "")
        rows.append(
            {
                "id": rel.get("Id", ""),
                "type": rel.get("Type", "").rsplit("/", 1)[-1],
                "target": target,
                "resolved_target": (
                    target if rel.get("TargetMode") == "External" else _resolve_target(part, target)
                ),
                "target_mode": rel.get("TargetMode", "Internal"),
            }
        )
    return rows


def _relationship_target(package: ZipFile, part: str, rel_type: str) -> str | None:
    for row in _relationships(package, part):
        if row["type"] == rel_type:
            return row["resolved_target"]
    return None


def _slide_parts(package: ZipFile) -> list[str]:
    presentation = _xml(package, "ppt/presentation.xml")
    rels = {row["id"]: row["resolved_target"] for row in _relationships(package, "ppt/presentation.xml")}
    parts: list[str] = []
    for slide_id in presentation.findall(".//p:sldIdLst/p:sldId", NS):
        rel_id = slide_id.get(_tag("r:id"), "")
        target = rels.get(rel_id)
        if target:
            parts.append(target)
    return parts


def _text(element: ET.Element) -> str:
    return "\n".join(
        value.strip()
        for value in (node.text or "" for node in element.findall(".//a:t", NS))
        if value.strip()
    )


def _shape_id_name(element: ET.Element) -> tuple[str | None, str | None]:
    node = element.find(".//p:cNvPr", NS)
    if node is None:
        return None, None
    return node.get("id"), node.get("name")


def _shape_kind(element: ET.Element) -> str:
    local = element.tag.rsplit("}", 1)[-1]
    return {
        "sp": "shape",
        "pic": "image",
        "graphicFrame": "graphic",
        "grpSp": "group",
        "cxnSp": "connector",
        "contentPart": "content_part",
    }.get(local, local)


def _geometry(element: ET.Element) -> dict[str, int] | None:
    xfrm = element.find("./p:spPr/a:xfrm", NS)
    if xfrm is None:
        xfrm = element.find("./p:xfrm", NS)
    if xfrm is None:
        return None
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return {
        "x_emu": int(off.get("x", "0")),
        "y_emu": int(off.get("y", "0")),
        "width_emu": int(ext.get("cx", "0")),
        "height_emu": int(ext.get("cy", "0")),
    }


def _placeholder(element: ET.Element) -> dict[str, str] | None:
    node = element.find(".//p:ph", NS)
    if node is None:
        return None
    return {key: value for key in ("type", "idx", "sz", "orient") if (value := node.get(key))}


def _object_role(kind: str, text: str, name: str, placeholder: dict[str, str] | None) -> str:
    haystack = f"{name}\n{text}"
    placeholder_type = (placeholder or {}).get("type", "")
    if placeholder_type in {"title", "ctrTitle", "subTitle"} or TITLE_CUES.search(haystack):
        return "title"
    if LOGO_CUES.search(haystack):
        return "logo"
    if ICON_CUES.search(haystack):
        return "icon"
    if kind == "image":
        return "image"
    if kind == "graphic":
        return "data"
    if NUMBER_CUES.search(haystack):
        return "metric"
    if BODY_CUES.search(haystack):
        return "body"
    if text:
        return "text"
    return "decoration"


def _capacity(text: str, font_size_px: float | None) -> dict[str, Any]:
    lower = text.lower()
    max_lines = 1 if re.search(r"限制.{0,8}一行|不超过.{0,8}一行|one\s+line", lower) else None
    return {
        "max_lines": max_lines,
        "deletable": bool(re.search(r"可删除|optional", lower, re.IGNORECASE)),
        "observed_characters": len(text.replace("\n", "")),
        "observed_font_size_px": font_size_px,
        "minimum_font_size_px": None,
        "overflow_policy": "native_adaptive",
    }


def _object_native_details(
    element: ET.Element,
    relationships: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Extract replacement-sensitive native facts without interpreting design intent."""
    refs: list[dict[str, str]] = []
    for node in element.iter():
        for attr, value in node.attrib.items():
            if attr in {_tag("r:id"), _tag("r:embed"), _tag("r:link")} and value in relationships:
                refs.append({"relationship_id": value, **relationships[value]})
    crop_node = element.find(".//a:srcRect", NS)
    crop = (
        {key: int(crop_node.get(key, "0")) for key in ("l", "t", "r", "b")}
        if crop_node is not None
        else None
    )
    alpha_values = [
        int(node.get("amt", "100000"))
        for node in element.findall(".//a:alphaModFix", NS)
    ]
    hyperlinks = []
    for node in element.findall(".//a:hlinkClick", NS) + element.findall(".//a:hlinkHover", NS):
        rel_id = node.get(_tag("r:id"), "")
        hyperlinks.append(
            {
                "kind": node.tag.rsplit("}", 1)[-1],
                "relationship_id": rel_id,
                "target": (relationships.get(rel_id) or {}).get("resolved_target"),
                "action": node.get("action"),
            }
        )
    graphic_data = element.find(".//a:graphicData", NS)
    graphic_uri = graphic_data.get("uri") if graphic_data is not None else None
    child_ids = [
        node.get("id")
        for node in element.findall(".//p:cNvPr", NS)
        if node.get("id")
    ]
    return {
        "relationship_refs": refs,
        "crop_100000": crop,
        "opacity": min(alpha_values) / 100000 if alpha_values else 1.0,
        "hyperlinks": hyperlinks,
        "graphic_uri": graphic_uri,
        "group_child_shape_ids": child_ids[1:] if len(child_ids) > 1 else [],
        "has_shadow": element.find(".//a:outerShdw", NS) is not None,
        "has_mask_or_custom_geometry": element.find(".//a:custGeom", NS) is not None,
    }


def _font_availability(fonts: Iterable[str]) -> list[dict[str, Any]]:
    executable = shutil.which("fc-list")
    installed: set[str] = set()
    status = "not_checked"
    if executable:
        try:
            completed = subprocess.run(
                [executable, ":", "family"],
                check=True,
                capture_output=True,
                text=True,
                timeout=20,
            )
            installed = {
                family.strip().casefold()
                for line in completed.stdout.splitlines()
                for family in line.split(",")
                if family.strip()
            }
            status = "checked_with_fontconfig"
        except (OSError, subprocess.SubprocessError):
            status = "check_failed"
    return [
        {
            "font": font,
            "available": font.casefold() in installed if installed else None,
            "status": status,
        }
        for font in fonts
        if font and font not in {"+mj-lt", "+mn-lt", "+mj-ea", "+mn-ea"}
    ]


def _slide_role(index: int, total: int, page_type: str, text: str) -> tuple[str, float, list[str]]:
    matches = [pattern.pattern for pattern in GUIDE_PATTERNS if pattern.search(text)]
    if matches:
        return "guide", 0.96, matches
    normalized = re.sub(r"\s+", " ", text).strip()
    if index == total and re.search(r"谢谢|thank\s+you|questions?", normalized, re.IGNORECASE):
        return "ending", 0.95, ["last-slide closing text"]
    if page_type == "cover_candidate" or index == 1:
        return "cover", 0.9, [page_type or "first slide"]
    if page_type == "toc_candidate" or re.search(r"目录|contents?|agenda", normalized, re.IGNORECASE):
        return "toc", 0.9, [page_type or "toc text"]
    if len(normalized) <= 80 and normalized.count("\n") <= 3:
        return "section", 0.62, ["short sparse page"]
    return "content", 0.78, [page_type or "content structure"]


def _iter_slide_objects(root: ET.Element) -> Iterable[tuple[int, ET.Element]]:
    tree = root.find("p:cSld/p:spTree", NS)
    if tree is None:
        return []
    allowed = {"sp", "pic", "graphicFrame", "grpSp", "cxnSp", "contentPart"}
    return [
        (z_index, child)
        for z_index, child in enumerate(list(tree))
        if child.tag.rsplit("}", 1)[-1] in allowed
    ]


def _font_hints(values: Iterable[str]) -> list[str]:
    return sorted({match.group(0) for value in values for match in FONT_HINT.finditer(value)}, key=str.casefold)


def _package_facts(package: ZipFile, slide_parts: list[str]) -> dict[str, Any]:
    names = package.namelist()
    relation_types: Counter[str] = Counter()
    transition_count = 0
    timing_count = 0
    notes_count = 0
    hidden_count = 0
    for name in names:
        if name.endswith(".rels"):
            try:
                relation_types.update(
                    rel.get("Type", "").rsplit("/", 1)[-1]
                    for rel in _xml(package, name).findall("pr:Relationship", NS)
                )
            except ET.ParseError:
                continue
    for part in slide_parts:
        root = _xml(package, part)
        transition_count += int(root.find("p:transition", NS) is not None)
        timing_count += int(root.find("p:timing", NS) is not None)
        hidden_count += int(root.get("show") == "0")
        notes_count += int(_relationship_target(package, part, "notesSlide") is not None)
    return {
        "relationship_types": dict(sorted(relation_types.items())),
        "media_part_count": sum(name.startswith("ppt/media/") for name in names),
        "chart_part_count": sum(re.match(r"ppt/charts/chart\d+\.xml$", name) is not None for name in names),
        "embedding_part_count": sum(name.startswith("ppt/embeddings/") for name in names),
        "embedded_font_part_count": sum(name.startswith("ppt/fonts/") for name in names),
        "notes_slide_count": notes_count,
        "slides_with_transition_nodes": transition_count,
        "slides_with_timing": timing_count,
        "hidden_slide_count": hidden_count,
    }


def _asset_manifest(package: ZipFile, slide_parts: list[str], canvas_emu: dict[str, int]) -> dict[str, Any]:
    usage: dict[str, set[str]] = defaultdict(set)
    owners = list(slide_parts)
    owners.extend(name for name in package.namelist() if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", name))
    owners.extend(name for name in package.namelist() if re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", name))
    for owner in owners:
        for rel in _relationships(package, owner):
            if rel["type"] == "image" and rel["resolved_target"].startswith("ppt/media/"):
                usage[rel["resolved_target"]].add(owner)

    items: list[dict[str, Any]] = []
    for name in sorted(item for item in package.namelist() if item.startswith("ppt/media/")):
        data = package.read(name)
        width = height = None
        mode = None
        try:
            from PIL import Image

            with Image.open(BytesIO(data)) as image:
                width, height = image.size
                mode = image.mode
        except (ImportError, OSError):
            pass
        owner_list = sorted(usage.get(name, set()))
        inherited = any("slideLayouts" in owner or "slideMasters" in owner for owner in owner_list)
        square = bool(width and height and abs(width - height) / max(width, height) <= 0.08)
        large = bool(width and height and width >= 1200 and height >= 675)
        if inherited:
            role = "fixed_template_asset"
            role_confidence, role_evidence = 0.95, "referenced by Master or Layout"
        elif square and width and width <= 1024 and mode in {"RGBA", "LA"}:
            role = "icon_candidate"
            role_confidence, role_evidence = 0.65, "small square asset with alpha"
        elif large:
            role = "background_candidate"
            role_confidence, role_evidence = 0.7, "large raster relative to presentation use"
        else:
            role = "content_asset_candidate"
            role_confidence, role_evidence = 0.5, "slide-local media without stronger signal"
        items.append(
            {
                "part": name,
                "filename": PurePosixPath(name).name,
                "sha256": sha256(data).hexdigest(),
                "bytes": len(data),
                "format": PurePosixPath(name).suffix.lower().lstrip("."),
                "width_px": width,
                "height_px": height,
                "mode": mode,
                "has_alpha": mode in {"RGBA", "LA"},
                "used_by": owner_list,
                "role": role,
                "role_confidence": role_confidence,
                "role_evidence": role_evidence,
            }
        )
    return {
        "schema": "ppt-master-plus.template-assets.v1",
        "asset_count": len(items),
        "role_counts": dict(Counter(item["role"] for item in items)),
        "canvas_emu": canvas_emu,
        "items": items,
    }


def _render_previews(source: Path, output_dir: Path) -> dict[str, Any]:
    preview_dir = output_dir / "template_preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    office = shutil.which("soffice") or shutil.which("libreoffice")
    pdftoppm = shutil.which("pdftoppm")
    if not office or not pdftoppm:
        result = {
            "schema": "ppt-master-plus.template-preview.v1",
            "status": "unavailable",
            "reason": "soffice/libreoffice and pdftoppm are required",
            "files": [],
        }
        (preview_dir / "index.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result
    try:
        with tempfile.TemporaryDirectory(prefix="ppt-template-preview-") as temp_name:
            temp_dir = Path(temp_name)
            subprocess.run(
                [office, "--headless", "--convert-to", "pdf", "--outdir", str(temp_dir), str(source)],
                check=True,
                capture_output=True,
                text=True,
                timeout=180,
            )
            pdfs = sorted(temp_dir.glob("*.pdf"))
            if len(pdfs) != 1:
                raise RuntimeError("office conversion did not produce exactly one PDF")
            subprocess.run(
                [pdftoppm, "-png", "-r", "72", str(pdfs[0]), str(preview_dir / "slide")],
                check=True,
                capture_output=True,
                timeout=240,
            )
        files = sorted(path.name for path in preview_dir.glob("slide-*.png"))
        result = {
            "schema": "ppt-master-plus.template-preview.v1",
            "status": "rendered",
            "files": files,
        }
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        result = {
            "schema": "ppt-master-plus.template-preview.v1",
            "status": "failed",
            "reason": str(exc),
            "files": [],
        }
    (preview_dir / "index.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def build_template_artifacts(
    source: Path,
    identity: dict[str, Any],
    slide_library: dict[str, Any],
    output_dir: Path,
    *,
    render_previews: bool,
) -> dict[str, Path]:
    """Build four template contracts and an optional rendered preview baseline."""
    with ZipFile(source) as package:
        slide_parts = _slide_parts(package)
        presentation = _xml(package, "ppt/presentation.xml")
        size = presentation.find("p:sldSz", NS)
        canvas_emu = {
            "width": int(size.get("cx", "0")) if size is not None else 0,
            "height": int(size.get("cy", "0")) if size is not None else 0,
        }
        slide_rows = slide_library.get("slides", [])
        by_index = {int(row.get("slide_index", 0)): row for row in slide_rows}
        layouts: dict[str, dict[str, Any]] = {}
        masters: dict[str, dict[str, Any]] = {}
        archetypes: list[dict[str, Any]] = []
        guide_texts: list[str] = []
        shape_names: list[str] = []
        xml_typefaces: Counter[str] = Counter()
        xml_sizes: Counter[float] = Counter()
        corner_styles: Counter[str] = Counter()
        stroke_widths_emu: Counter[int] = Counter()
        shadow_count = 0
        spacing_gaps_emu: Counter[int] = Counter()

        for part in package.namelist():
            if not part.endswith(".xml") or not part.startswith(("ppt/slides/", "ppt/slideLayouts/", "ppt/slideMasters/")):
                continue
            raw = package.read(part).decode("utf-8", errors="ignore")
            xml_typefaces.update(re.findall(r'typeface="([^"]+)"', raw))
            xml_sizes.update(float(value) / 100 for value in re.findall(r'\bsz="(\d+)"', raw))
            corner_styles.update(re.findall(r'<a:prstGeom[^>]+prst="([^"]+)"', raw))
            stroke_widths_emu.update(int(value) for value in re.findall(r'<a:ln[^>]+w="(\d+)"', raw))
            shadow_count += raw.count("<a:outerShdw")

        for index, slide_part in enumerate(slide_parts, 1):
            root = _xml(package, slide_part)
            slide_relationships = {
                row["id"]: row for row in _relationships(package, slide_part)
            }
            layout_part = _relationship_target(package, slide_part, "slideLayout")
            master_part = _relationship_target(package, layout_part, "slideMaster") if layout_part else None
            if layout_part and layout_part not in layouts:
                layout_root = _xml(package, layout_part)
                c_sld = layout_root.find("p:cSld", NS)
                layouts[layout_part] = {
                    "part": layout_part,
                    "name": (c_sld.get("name") if c_sld is not None else None) or PurePosixPath(layout_part).stem,
                    "master_part": master_part,
                    "shape_count": len(list(_iter_slide_objects(layout_root))),
                }
            if master_part and master_part not in masters:
                master_root = _xml(package, master_part)
                c_sld = master_root.find("p:cSld", NS)
                masters[master_part] = {
                    "part": master_part,
                    "name": (c_sld.get("name") if c_sld is not None else None) or PurePosixPath(master_part).stem,
                    "shape_count": len(list(_iter_slide_objects(master_root))),
                }

            library_row = by_index.get(index, {})
            page_text = _text(root)
            role, confidence, evidence = _slide_role(
                index,
                len(slide_parts),
                str(library_row.get("page_type", "")),
                page_text,
            )
            if root.get("show") == "0" or not layout_part:
                role, confidence, evidence = "unusable", 0.99, [
                    "hidden slide" if root.get("show") == "0" else "missing slide layout relationship"
                ]
            if role == "guide":
                guide_texts.extend(line for line in page_text.splitlines() if line.strip())
            slot_by_shape = {
                str(slot.get("slot_id", "")).rsplit("sh", 1)[-1]: slot
                for slot in library_row.get("slots", [])
            }
            objects: list[dict[str, Any]] = []
            for z_index, element in _iter_slide_objects(root):
                shape_id, name = _shape_id_name(element)
                name = name or ""
                shape_names.append(name)
                text = _text(element)
                kind = _shape_kind(element)
                placeholder = _placeholder(element)
                slot = slot_by_shape.get(str(shape_id), {})
                role_name = _object_role(kind, text, name, placeholder)
                cue = bool(PLACEHOLDER_CUES.search(f"{name}\n{text}"))
                if placeholder and (placeholder.get("type") or "body") not in {"dt", "ftr", "sldNum"}:
                    editable, edit_confidence = True, 0.98
                elif kind == "graphic":
                    editable, edit_confidence = True, 0.9
                elif kind == "image" and role_name == "image" and (cue or IMAGE_SLOT_CUES.search(name)):
                    editable, edit_confidence = True, 0.82
                elif text and cue:
                    editable, edit_confidence = True, 0.9
                elif text and role_name in {"title", "body", "metric"}:
                    editable, edit_confidence = True, 0.72
                else:
                    editable, edit_confidence = False, 0.45
                text_metrics = slot.get("text_metrics", {}) if isinstance(slot, dict) else {}
                objects.append(
                    {
                        "shape_id": shape_id,
                        "name": name,
                        "kind": kind,
                        "z_index": z_index,
                        "geometry": _geometry(element),
                        "placeholder": placeholder,
                        "text": text,
                        "role": role_name,
                        "editable": editable,
                        "edit_confidence": edit_confidence,
                        "locked_reason": None if editable else "low_confidence_or_template_chrome",
                        "replace_policy": (
                            "replace_text"
                            if text
                            else "replace_image_preserve_frame"
                            if kind == "image"
                            else "replace_native_data"
                            if kind == "graphic"
                            else "locked"
                        ),
                        "capacity": _capacity(text, text_metrics.get("font_size_px")),
                        "native": _object_native_details(element, slide_relationships),
                    }
                )
            for axis in ("x_emu", "y_emu"):
                positions = sorted(
                    {
                        int(obj["geometry"][axis])
                        for obj in objects
                        if obj.get("geometry") and obj["geometry"].get(axis) is not None
                    }
                )
                spacing_gaps_emu.update(
                    right - left
                    for left, right in zip(positions, positions[1:])
                    if right > left
                )
            archetypes.append(
                {
                    "source_slide": index,
                    "preview_path": f"template_preview/slide-{index}.png" if render_previews else None,
                    "slide_part": slide_part,
                    "layout_part": layout_part,
                    "layout_name": (layouts.get(layout_part or "") or {}).get("name"),
                    "role": role,
                    "role_confidence": confidence,
                    "role_evidence": evidence,
                    "reusable": role != "guide",
                    "text_summary": library_row.get("text_summary", page_text),
                    "objects": objects,
                    "native_content": {
                        "table_count": len(library_row.get("tables", [])),
                        "chart_count": len(library_row.get("charts", [])),
                        "diagram_count": len(library_row.get("diagrams", [])),
                    },
                    "relationships": list(slide_relationships.values()),
                    "copy_strategy": "native_roundtrip_clone" if role != "guide" else "extract_rules_only",
                }
            )

        guide_fonts = _font_hints(guide_texts)
        name_fonts = _font_hints(shape_names)
        observed_fonts = sorted(xml_typefaces, key=lambda value: (-xml_typefaces[value], value.casefold()))
        theme_fonts = [
            value
            for role in (identity.get("theme", {}).get("fonts", {}) or {}).values()
            if isinstance(role, dict)
            for value in role.values()
            if isinstance(value, str)
        ]
        conflicts: list[dict[str, Any]] = []
        authoritative = {value.casefold() for value in [*guide_fonts, *observed_fonts]}
        stale_hints = [value for value in name_fonts if value.casefold() not in authoritative]
        if stale_hints:
            conflicts.append(
                {
                    "field": "typography.font_family",
                    "lower_priority_values": stale_hints,
                    "resolution": "ignore shape-name hints; use guide text, resolved object style, then theme",
                    "priority": ["guide", "resolved_object_style", "theme", "shape_name", "heuristic"],
                }
            )

        source_bytes = source.read_bytes()
        manifest = {
            "schema": "ppt-master-plus.template-manifest.v1",
            "source": {
                "path": str(source),
                "sha256": sha256(source_bytes).hexdigest(),
                "bytes": len(source_bytes),
                "immutable": True,
            },
            "canvas": {
                "emu": canvas_emu,
                "px": slide_library.get("canvas_px", {}),
                "aspect_ratio": (
                    round(canvas_emu["width"] / canvas_emu["height"], 6)
                    if canvas_emu["height"]
                    else None
                ),
            },
            "slide_count": len(slide_parts),
            "masters": list(masters.values()),
            "layouts": list(layouts.values()),
            "page_role_counts": dict(Counter(row["role"] for row in archetypes)),
            "native_features": _package_facts(package, slide_parts),
            "fact_priority": [
                "explicit guide page",
                "resolved exemplar formatting",
                "master and theme inheritance",
                "shape name or note hint",
                "geometry and repetition heuristic",
            ],
            "inherited_objects_locked": True,
            "visualization_style_policy": {
                "source": "skill_builtin",
                "template_visualization_style_reusable": False,
                "template_visualization_usage": "slot_geometry_and_capacity_only",
                "catalogs": [
                    "templates/charts/charts_index.json",
                    "templates/tables/tables_index.json",
                ],
            },
            "conflicts": conflicts,
            "preview_index": "template_preview/index.json" if render_previews else None,
        }
        tokens = {
            "schema": "ppt-master-plus.template-design-tokens.v1",
            "theme": identity.get("theme", {}),
            "declared_guide_pages": [row["source_slide"] for row in archetypes if row["role"] == "guide"],
            "declared_rules": guide_texts,
            "declared_hex_colors": sorted({color.upper() for text in guide_texts for color in HEX_COLOR.findall(text)}),
            "declared_font_hints": guide_fonts,
            "resolved_typefaces": [
                {"value": value, "count": xml_typefaces[value]} for value in observed_fonts
            ],
            "font_availability": _font_availability([*guide_fonts, *theme_fonts, *observed_fonts]),
            "resolved_sizes_pt": [
                {"value": value, "count": xml_sizes[value]}
                for value in sorted(xml_sizes, key=lambda item: (-xml_sizes[item], item))
            ],
            "shape_name_font_hints": name_fonts,
            "observed_colors": (identity.get("observed") or {}).get("colors", []),
            "visualization_style_source": "skill_builtin",
            "excluded_template_style_domains": [
                "chart_style",
                "table_style",
                "infographic_style",
                "diagram_style",
            ],
            "geometry_style": {
                "preset_geometry_counts": dict(corner_styles),
                "stroke_widths_emu": [
                    {"value": value, "count": stroke_widths_emu[value]}
                    for value in sorted(stroke_widths_emu)
                ],
                "shadow_count": shadow_count,
                "common_alignment_gaps_emu": [
                    {"value": value, "count": count}
                    for value, count in spacing_gaps_emu.most_common(20)
                ],
            },
            "asset_rules": {
                "logos_and_icons": "preserve template assets unless explicitly unlocked",
                "images": "replace within the existing frame while preserving crop and effects",
                "charts_tables_infographics_diagrams": (
                    "ignore template exemplar styling; select a built-in skill visualization "
                    "and adapt it to the locked template palette, typography, and slot geometry"
                ),
            },
            "conflicts": conflicts,
            "default_lock": {
                "canvas": True,
                "colors": True,
                "typography": True,
                "logos": True,
                "icons": True,
            },
        }
        archetype_payload = {
            "schema": "ppt-master-plus.template-archetypes.v1",
            "adaptation": "native_adaptive",
            "overflow_order": [
                "shorten_content",
                "adjust_within_template_limits",
                "select_larger_matching_archetype",
                "duplicate_and_split",
                "request_user_decision",
            ],
            "visualization_policy": {
                "style_source": "skill_builtin",
                "template_objects_contribute": [
                    "slot_geometry",
                    "capacity",
                    "z_order_anchor",
                ],
                "template_objects_do_not_contribute": [
                    "chart_style",
                    "table_style",
                    "infographic_style",
                    "diagram_style",
                ],
                "content_and_data_source": "content_sources",
            },
            "slides": archetypes,
        }
        assets = _asset_manifest(package, slide_parts, canvas_emu)

    outputs = {
        "template_manifest": output_dir / "template_manifest.json",
        "template_design_tokens": output_dir / "template_design_tokens.json",
        "template_archetypes": output_dir / "template_archetypes.json",
        "template_assets": output_dir / "template_assets.json",
    }
    payloads = (manifest, tokens, archetype_payload, assets)
    for path, payload in zip(outputs.values(), payloads):
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if render_previews:
        _render_previews(source, output_dir)
    return outputs
