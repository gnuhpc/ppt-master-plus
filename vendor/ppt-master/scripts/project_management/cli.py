#!/usr/bin/env python3
"""PPT Master project-management CLI implementation.

Usage:
    python3 scripts/project_manager.py init <project_name> [--format <registered_format>]
        [--dir <path>] [--quick-generate]
    python3 scripts/project_manager.py import-sources <project_path> <source1> [<source2> ...] [--move | --copy]
    python3 scripts/project_manager.py scaffold-spec <project_path>
    python3 scripts/project_manager.py scaffold-lock <project_path>
    python3 scripts/project_manager.py validate <project_path>
    python3 scripts/project_manager.py info <project_path>
    python3 scripts/project_manager.py page-context <project_path> P07 [--record-usage]
    python3 scripts/project_manager.py page-context-report <project_path>

Examples:
    python3 scripts/project_manager.py init demo
    python3 scripts/project_manager.py init widescreen --format ppt169
    python3 scripts/project_manager.py validate projects/demo

Dependencies:
    Standard library plus local PPT Master project and source-conversion modules.
"""

from __future__ import annotations

import argparse
import filecmp
from hashlib import sha256
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from .page_context import (
    build_page_context,
    page_context_usage_report,
    record_page_context_usage,
    render_page_context,
)
from .paths import (
    PROJECTS_ROOT,
    REPO_ROOT,
    SCRIPTS_DIR,
    SOURCE_TO_MD_DIR,
)
from .project_specs import scaffold_project_artifact, validate_project_artifacts

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from workflow_log import append_note  # noqa: E402
from pptx_ooxml.clone import clone_presentation_slides  # noqa: E402

try:
    from project_utils import (
        CANVAS_FORMATS,
        get_project_info as get_project_info_common,
        normalize_canvas_format,
        validate_project_structure,
        validate_svg_viewbox,
    )
except ImportError:
    tools_dir = SCRIPTS_DIR
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from project_utils import (  # type: ignore
        CANVAS_FORMATS,
        get_project_info as get_project_info_common,
        normalize_canvas_format,
        validate_project_structure,
        validate_svg_viewbox,
    )

TOOLS_DIR = SCRIPTS_DIR
SOURCE_TO_MD_TOOLS_DIR = SOURCE_TO_MD_DIR
if str(SOURCE_TO_MD_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_TO_MD_TOOLS_DIR))

from _dispatcher import (  # noqa: E402
    DOC_SUFFIXES,
    EXCEL_SUFFIXES,
    LEGACY_EXCEL_SUFFIXES,
    PDF_SUFFIXES,
    PRESENTATION_SUFFIXES,
    build_conversion_command,
)

SOURCE_DIRNAME = "sources"
TEXT_SOURCE_SUFFIXES = {".md", ".markdown", ".txt"}
TABLE_TEXT_SUFFIXES = {".csv", ".tsv"}
BITMAP_IMAGE_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".tif",
}
IMAGE_ASSET_SUFFIXES = BITMAP_IMAGE_SUFFIXES | {
    ".emf", ".wmf", ".svg",
}
DEFERRED_CANVAS_MESSAGE = (
    "Canvas is determined during authoring and recorded in spec_lock.md "
    "(Default) or the first SVG (Quick)."
)
NATIVE_EDIT_MODULES = {
    "page_plan",
    "content_edit",
    "notes",
    "narration",
    "transitions",
    "animations",
    "visible_content_locked",
}

_PML = "http://schemas.openxmlformats.org/presentationml/2006/main"
_DML = "http://schemas.openxmlformats.org/drawingml/2006/main"
_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
_OOXML_NS = {"p": _PML, "a": _DML, "r": _REL, "pr": _PKG_REL}
_PAGE_KIT_SELECTION_SCHEMA = "ppt-master-plus.brand-import-selection.v1"
_PAGE_KIT_ROLES = {"cover", "toc", "section", "content", "closing"}


def _package_relationship_part(part: str) -> str:
    path = Path(part)
    return str(path.parent / "_rels" / f"{path.name}.rels")


def _resolve_package_target(part: str, target: str) -> str:
    pieces: list[str] = []
    for piece in (Path(part).parent / target).parts:
        if piece in {"", "."}:
            continue
        if piece == "..":
            if pieces:
                pieces.pop()
            continue
        pieces.append(piece)
    return "/".join(pieces)


def _presentation_slide_parts(package: zipfile.ZipFile) -> list[str]:
    presentation_part = "ppt/presentation.xml"
    presentation = ET.fromstring(package.read(presentation_part))
    relationships = ET.fromstring(
        package.read(_package_relationship_part(presentation_part))
    )
    targets = {
        row.get("Id", ""): _resolve_package_target(
            presentation_part, row.get("Target", "")
        )
        for row in relationships.findall("pr:Relationship", _OOXML_NS)
    }
    return [
        targets[node.get(f"{{{_REL}}}id", "")]
        for node in presentation.findall(".//p:sldIdLst/p:sldId", _OOXML_NS)
        if node.get(f"{{{_REL}}}id", "") in targets
    ]


def _load_brand_page_selection(
    *, source: Path, analysis_dir: Path, archetypes: dict[str, object]
) -> list[dict[str, object]]:
    selection_path = analysis_dir / "brand_import_selection.json"
    try:
        selection = json.loads(selection_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            "Brand Page Kit registration requires a confirmed Web selection. "
            f"Run scripts/brand_import_ui/server.py for this project first: {exc}"
        ) from exc
    if not isinstance(selection, dict) or selection.get("schema") != _PAGE_KIT_SELECTION_SCHEMA:
        raise RuntimeError(f"Invalid Brand import selection schema: {selection_path}")
    source_digest = sha256(source.read_bytes()).hexdigest()
    if selection.get("source_sha256") != source_digest:
        raise RuntimeError(
            "Brand import selection belongs to a different PPTX; reopen the Brand Import Web"
        )
    slides = archetypes.get("slides") if isinstance(archetypes, dict) else None
    if not isinstance(slides, list):
        raise RuntimeError("Template archetypes contain no slide roster")
    source_rows = {
        row.get("source_slide"): row
        for row in slides
        if isinstance(row, dict) and isinstance(row.get("source_slide"), int)
    }
    pages = selection.get("pages")
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("Brand import selection contains no approved pages")
    approved: list[dict[str, object]] = []
    seen: set[tuple[int, str]] = set()
    for position, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            raise RuntimeError(f"Brand import selection item {position} must be an object")
        source_slide = page.get("source_slide")
        role = page.get("role")
        if not isinstance(source_slide, int) or source_slide not in source_rows:
            raise RuntimeError(f"Brand import selection item {position} names an unknown slide")
        source_row = source_rows[source_slide]
        if source_row.get("role") in {"guide", "unusable"}:
            raise RuntimeError(
                f"Brand import selection item {position} selects a guide/unusable slide"
            )
        if role not in _PAGE_KIT_ROLES:
            raise RuntimeError(f"Brand import selection item {position} has invalid role {role!r}")
        key = (source_slide, str(role))
        if key in seen:
            raise RuntimeError(f"Brand import selection repeats slide {source_slide} as {role}")
        seen.add(key)
        approved.append({"role": role, "source_slide": source_slide, "source": source_row})
    if not any(page["role"] == "content" for page in approved):
        raise RuntimeError("Brand import selection must include at least one content Master/Layout")
    return approved


def _sanitize_content_master_slides(
    source: Path,
    destination: Path,
    content_title_shapes: dict[int, set[str]],
) -> None:
    """Copy a PPTX while stripping every slide-local object from content shells.

    The slide relationship to its Layout (and therefore its Master, theme,
    background images, Master text and placeholders) remains untouched. The
    selected slide's title text frame is the only slide-local exception: its
    geometry and typography survive as an empty editable title slot. No example
    text, chart, picture, group, connector, timing or transition survives. Its
    relationship part retains only the linked Slide Layout, so a removed
    slide-local picture/chart/diagram cannot be carried into later cloning.
    """
    ET.register_namespace("a", _DML)
    ET.register_namespace("p", _PML)
    ET.register_namespace("r", _REL)
    with zipfile.ZipFile(source) as package:
        parts = _presentation_slide_parts(package)
        selected_parts = {
            parts[index - 1]
            for index in content_title_shapes
            if 0 < index <= len(parts)
        }
        if len(selected_parts) != len(content_title_shapes):
            raise RuntimeError("Selected content Master/Layout references an unavailable slide")
        part_to_slide = {
            parts[index - 1]: index for index in content_title_shapes
        }
        with zipfile.ZipFile(destination, "w") as output:
            for info in package.infolist():
                data = package.read(info.filename)
                if info.filename in selected_parts:
                    root = ET.fromstring(data)
                    tree = root.find("p:cSld/p:spTree", _OOXML_NS)
                    if tree is None:
                        raise RuntimeError(
                            f"Selected content slide has no shape tree: {info.filename}"
                        )
                    keep_titles = content_title_shapes[part_to_slide[info.filename]]
                    for child in list(tree):
                        local = child.tag.rsplit("}", 1)[-1]
                        if local in {"nvGrpSpPr", "grpSpPr"}:
                            continue
                        identity = child.find(".//p:cNvPr", _OOXML_NS)
                        shape_id = identity.get("id") if identity is not None else None
                        if local == "sp" and shape_id in keep_titles:
                            for text_node in child.findall(".//a:t", _OOXML_NS):
                                text_node.text = ""
                        else:
                            tree.remove(child)
                    for name in ("p:transition", "p:timing"):
                        node = root.find(name, _OOXML_NS)
                        if node is not None:
                            root.remove(node)
                    data = ET.tostring(root, encoding="utf-8", xml_declaration=True)
                elif info.filename in {
                    _package_relationship_part(part) for part in selected_parts
                }:
                    relationships = ET.fromstring(data)
                    for relationship in list(relationships):
                        if not relationship.get("Type", "").endswith("/slideLayout"):
                            relationships.remove(relationship)
                    data = ET.tostring(relationships, encoding="utf-8", xml_declaration=True)
                output.writestr(info, data)


def _validate_image_manifest(
    payload: object,
    path: Path,
) -> list[dict]:
    """Require a safe, case-insensitively unique image manifest payload."""
    if not isinstance(payload, list):
        raise RuntimeError(
            f"Image manifest must be a JSON array: {path}"
        )

    seen_filenames: dict[str, str] = {}
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise RuntimeError(
                f"Existing image manifest item {index} must be an object: {path}"
            )
        filename = item.get("filename")
        if (
            not isinstance(filename, str)
            or not filename.strip()
            or filename in {".", ".."}
            or "/" in filename
            or "\\" in filename
            or ":" in filename
            or Path(filename).is_absolute()
            or Path(filename).name != filename
        ):
            raise RuntimeError(
                f"Image manifest item {index} has no safe bare filename: {path}"
            )
        normalized_filename = filename.casefold()
        if normalized_filename in seen_filenames:
            raise RuntimeError(
                f"Image manifest filename {filename!r} conflicts with "
                f"{seen_filenames[normalized_filename]!r} (case-insensitive): {path}"
            )
        seen_filenames[normalized_filename] = filename
    return payload


def _read_existing_image_manifest(path: Path) -> list[dict]:
    """Load an existing project image manifest or fail closed on corruption."""
    if not path.exists():
        return []
    if not path.is_file():
        raise RuntimeError(f"Existing image manifest is not a regular file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Existing image manifest is unreadable: {path} ({exc}); "
            "repair or restore it before importing more assets"
        ) from exc
    return _validate_image_manifest(payload, path)


def _write_json_atomic(path: Path, payload: object) -> None:
    """Write JSON through a same-directory temporary file and atomic rename."""
    fd, temp_name = tempfile.mkstemp(
        prefix=f"{path.stem}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def is_url(value: str) -> bool:
    """Return whether a string looks like an HTTP(S) URL."""
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def sanitize_name(value: str) -> str:
    """Sanitize a user-facing name into a filesystem-safe token."""
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value.strip())
    safe = safe.strip("._")
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe[:120] or "source"


def derive_url_basename(url: str) -> str:
    """Derive a stable base filename from a URL."""
    parsed = urlparse(url)
    parts = [sanitize_name(parsed.netloc)]
    if parsed.path and parsed.path != "/":
        path_part = sanitize_name(parsed.path.strip("/").replace("/", "_"))
        if path_part:
            parts.append(path_part)
    return "_".join(part for part in parts if part) or "web_source"


def is_within_path(path: Path, parent: Path) -> bool:
    """Return whether `path` resolves inside `parent`."""
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _has_usable_import(summary: dict[str, list[str]]) -> bool:
    """Return whether import-sources produced at least one usable source artifact."""
    return any(
        summary.get(key)
        for key in ("archived", "markdown", "assets", "images", "analysis")
    )


def _brand_id(value: str) -> str:
    """Validate a library Brand id without accepting a filesystem path."""
    candidate = sanitize_name(value)
    if candidate != value or candidate in {"", ".", ".."}:
        raise ValueError(
            "Brand id must be a single filesystem-safe identifier (no path separators)"
        )
    return candidate


def _hex_values(value: object) -> list[str]:
    """Return normalized six-digit HEX values, keeping their declared order."""
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str):
            continue
        raw = item.strip().upper()
        if re.fullmatch(r"#[0-9A-F]{6}", raw) and raw not in result:
            result.append(raw)
    return result


def _observed_font(identity: dict, *, preferred_words: tuple[str, ...]) -> str | None:
    observed = identity.get("observed") if isinstance(identity, dict) else None
    fonts = observed.get("fonts") if isinstance(observed, dict) else None
    candidates = fonts.get("ea") if isinstance(fonts, dict) else None
    if not isinstance(candidates, list):
        return None
    values = [
        item.get("value") for item in candidates
        if isinstance(item, dict) and isinstance(item.get("value"), str)
    ]
    for value in values:
        lowered = value.casefold()
        if all(word.casefold() in lowered for word in preferred_words):
            return value
    return values[0] if values else None


class ProjectManager:
    """Create, inspect, validate, and populate project folders."""

    CANVAS_FORMATS = CANVAS_FORMATS

    def __init__(self, base_dir: str | Path | None = None) -> None:
        self.base_dir = Path(base_dir) if base_dir is not None else Path.cwd() / "projects"

    def scaffold_artifact(self, project_path: str, artifact: str) -> str:
        """Delegate deterministic Markdown scaffold rendering."""
        return scaffold_project_artifact(Path(project_path), artifact)

    def init_project(
        self,
        project_name: str,
        canvas_format: str | None = None,
        base_dir: str | None = None,
        *,
        quick_generate: bool = False,
    ) -> str:
        base_path = Path(base_dir) if base_dir else self.base_dir

        if (
            not project_name
            or project_name in {".", ".."}
            or Path(project_name).is_absolute()
            or "/" in project_name
            or "\\" in project_name
        ):
            raise ValueError(
                "Project name must be a single, non-absolute path component"
            )

        normalized_format: str | None = None
        if canvas_format is not None:
            normalized_format = normalize_canvas_format(canvas_format)
            if normalized_format not in self.CANVAS_FORMATS:
                available = ", ".join(sorted(self.CANVAS_FORMATS.keys()))
                raise ValueError(
                    f"Unsupported canvas format: {canvas_format} "
                    f"(available: {available}; common alias: xhs -> xiaohongshu)"
                )

        date_str = datetime.now().strftime("%Y%m%d")
        if normalized_format is None:
            project_dir_name = f"{project_name}_{date_str}"
        else:
            # A name already carrying a `_<format>_<YYYYMMDD>` suffix (e.g. a
            # full project dir name pasted back into init) is used as-is —
            # re-appending would produce
            # `name_ppt169_20260101_ppt169_20260102`.
            if re.search(rf"_{re.escape(normalized_format)}_\d{{8}}$", project_name):
                project_dir_name = project_name
            else:
                project_dir_name = f"{project_name}_{normalized_format}_{date_str}"
        project_path = base_path / project_dir_name

        if not is_within_path(project_path, base_path):
            raise ValueError(
                f"Project directory must stay within the base directory: {base_path}"
            )
        if project_path.exists():
            raise FileExistsError(f"Project directory already exists: {project_path}")

        project_dirs = (
            ("svg_output",)
            if quick_generate
            else (
                "svg_output",
                "svg_final",
                "images",
                "icons",
                "notes",
                "templates",
                "template",
                "live_preview",
                SOURCE_DIRNAME,
                "analysis",
                "validation",
                "exports",
            )
        )
        for rel_path in project_dirs:
            (project_path / rel_path).mkdir(parents=True, exist_ok=True)

        if not quick_generate:
            canvas_summary = (
                f"- Canvas format: {normalized_format}\n"
                if normalized_format is not None
                else f"- {DEFERRED_CANVAS_MESSAGE}\n"
            )
            readme_path = project_path / "README.md"
            readme_path.write_text(
                (
                    f"# {project_name}\n\n"
                    f"{canvas_summary}"
                    f"- Created: {date_str}\n\n"
                    "## Directories\n\n"
                    "- `svg_output/`: raw SVG output\n"
                    "- `svg_final/`: self-contained SVG visual preview; may be inserted manually as an SVG image, but PowerPoint Convert to Shape is unsupported\n"
                    "- `images/`: runtime image pool; converter assets keep their original short filenames when possible\n"
                    "- `icons/`: project icon set — selected library icons copied in (via icon_sync.py) plus any custom icons you add; embedded from here at export\n"
                    "- `notes/`: speaker notes\n"
                    "- `templates/`: project templates\n"
                    "- `template/`: read-only Brand source for Import Brand PPTX\n"
                    "- `live_preview/`: browser preview runtime files and history (lock.json, server.log, edits.jsonl, annotations.jsonl)\n"
                    "- `sources/`: source materials and normalized markdown\n"
                    "- `analysis/`: machine-extracted intermediate analysis (PPTX intake, image_analysis.csv) — the pipeline's canonical must-read source/asset facts\n"
                    "- `validation/`: cold workflow audit log, SVG quality reports, and PPTX postflight audit reports\n"
                    "- `exports/`: final native DrawingML pptx deliverables only (timestamped); `_native_charts_tables.pptx` name with `--native-charts-and-tables`, `_narrated.pptx` name when narration audio is embedded\n"
                    "- `backup/<timestamp>/`: svg_output/ archive (always written in default-flow mode; safe to delete old timestamps)\n"
                ),
                encoding="utf-8",
            )

        print(f"Project created: {project_path}")
        if normalized_format is None:
            print(DEFERRED_CANVAS_MESSAGE)
        else:
            canvas_info = self.CANVAS_FORMATS[normalized_format]
            print(f"Canvas: {canvas_info['name']} ({canvas_info['dimensions']})")
        return str(project_path)

    def _source_dir(self, project_path: Path) -> Path:
        sources_dir = project_path / SOURCE_DIRNAME
        sources_dir.mkdir(parents=True, exist_ok=True)
        return sources_dir

    def _analysis_dir(self, project_path: Path) -> Path:
        analysis_dir = project_path / "analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        return analysis_dir

    def _ensure_unique_path(self, path: Path) -> Path:
        if not path.exists():
            return path

        suffix = path.suffix
        stem = path.stem
        counter = 2
        while True:
            candidate = path.with_name(f"{stem}_{counter}{suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def _copy_or_move_file(self, source: Path, destination: Path, move: bool) -> Path:
        try:
            if source.resolve() == destination.resolve():
                return destination
        except FileNotFoundError:
            pass

        destination = self._ensure_unique_path(destination)
        if move:
            shutil.move(str(source), str(destination))
        else:
            shutil.copy2(source, destination)
        return destination

    def _copy_or_move_tree(self, source: Path, destination: Path, move: bool) -> Path:
        try:
            if source.resolve() == destination.resolve():
                return destination
        except FileNotFoundError:
            pass

        destination = self._ensure_unique_path(destination)
        if move:
            shutil.move(str(source), str(destination))
        else:
            shutil.copytree(source, destination)
        return destination

    def _run_tool(self, args: list[str]) -> None:
        child_env = os.environ.copy()
        child_env["PYTHONUTF8"] = "1"
        child_env["PYTHONIOENCODING"] = "utf-8:replace"
        try:
            result = subprocess.run(
                args,
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=child_env,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(f"Missing executable: {args[0]}") from exc
        except subprocess.CalledProcessError as exc:
            details = (exc.stderr or exc.stdout or "").strip()
            raise RuntimeError(details or "tool execution failed") from exc

        if result.stdout.strip():
            print(result.stdout.strip())

    def _import_pdf(self, pdf_path: Path, markdown_path: Path) -> None:
        route = build_conversion_command(
            str(pdf_path),
            markdown_path,
            forced_type="pdf",
        )
        self._run_tool(route.command)

    def _import_doc(self, doc_path: Path, markdown_path: Path) -> None:
        route = build_conversion_command(
            str(doc_path),
            markdown_path,
            forced_type="doc",
        )
        self._run_tool(route.command)

    def _import_presentation(self, presentation_path: Path, markdown_path: Path) -> None:
        route = build_conversion_command(
            str(presentation_path),
            markdown_path,
            forced_type="pptx",
        )
        self._run_tool(route.command)

    def _import_pptx_intake(self, presentation_path: Path, project_dir: Path) -> Path:
        # Multi-deck intake: each PPTX writes its own `<stem>.identity.json` /
        # `<stem>.slide_library.json` and is merged into the single multi-deck
        # index `analysis/source_profile.json` (one entry per source deck).
        analysis_dir = self._analysis_dir(project_dir)
        self._run_tool(
            [
                sys.executable,
                str(TOOLS_DIR / "pptx_intake.py"),
                str(presentation_path),
                "-o",
                str(analysis_dir),
            ]
        )
        return analysis_dir

    def _import_excel(self, excel_path: Path, markdown_path: Path) -> None:
        route = build_conversion_command(
            str(excel_path),
            markdown_path,
            forced_type="excel",
        )
        self._run_tool(route.command)

    def _import_url(
        self,
        url: str,
        markdown_path: Path,
    ) -> None:
        route = build_conversion_command(
            url,
            markdown_path,
            forced_type="web",
        )
        self._run_tool(route.command)

    def _is_valid_imported_url_markdown(self, markdown_path: Path) -> bool:
        """Return whether web_to_md produced a usable Markdown source."""
        if not markdown_path.is_file():
            return False
        content = markdown_path.read_text(encoding="utf-8", errors="replace")
        if "[Failed URLs]:" in content:
            return False
        return bool(content.strip())

    def _archive_url_record(self, sources_dir: Path, url: str) -> Path:
        file_path = self._ensure_unique_path(sources_dir / f"{derive_url_basename(url)}.url.txt")
        file_path.write_text(
            f"URL: {url}\nImported: {datetime.now().isoformat(timespec='seconds')}\n",
            encoding="utf-8",
        )
        return file_path

    def _normalize_text_source(self, source_path: Path, sources_dir: Path) -> Path:
        target = self._ensure_unique_path(sources_dir / f"{source_path.stem}.md")
        content = source_path.read_text(encoding="utf-8", errors="replace")
        target.write_text(content, encoding="utf-8")
        return target

    def _canonicalize_markdown_content(self, content: str) -> str:
        canonical = content.replace("\r\n", "\n")
        canonical = re.sub(r"(?m)^(\s*Crawled:\s+).*$", r"\1__IGNORED__", canonical)
        canonical = re.sub(r"(?m)^(\s*Imported:\s+).*$", r"\1__IGNORED__", canonical)
        canonical = re.sub(r"([^\s\]()/]+_files)/", "__ASSET_DIR__/", canonical)
        return canonical.strip()

    def _find_equivalent_markdown(self, source_path: Path, sources_dir: Path) -> Path | None:
        source_content = source_path.read_text(encoding="utf-8", errors="replace")
        canonical_source = self._canonicalize_markdown_content(source_content)

        for existing in sorted(sources_dir.iterdir()):
            if existing.suffix.lower() not in {".md", ".markdown"}:
                continue
            try:
                if existing.resolve() == source_path.resolve():
                    continue
            except FileNotFoundError:
                pass

            existing_content = existing.read_text(encoding="utf-8", errors="replace")
            if self._canonicalize_markdown_content(existing_content) == canonical_source:
                return existing

        return None

    def _companion_asset_dir(self, source_path: Path) -> Path | None:
        candidate = source_path.with_name(f"{source_path.stem}_files")
        if candidate.exists() and candidate.is_dir():
            return candidate
        return None

    def _rewrite_markdown_asset_refs(
        self,
        markdown_path: Path,
        original_asset_dirname: str,
        imported_asset_dirname: str,
    ) -> None:
        if original_asset_dirname == imported_asset_dirname:
            return

        content = markdown_path.read_text(encoding="utf-8", errors="replace")
        updated = content.replace(f"{original_asset_dirname}/", f"{imported_asset_dirname}/")
        if updated != content:
            markdown_path.write_text(updated, encoding="utf-8")

    def _merge_image_manifest(self, source_items: list[dict], destination_manifest: Path) -> None:
        """Merge per-source manifest items into the project-level manifest, keyed by filename."""
        _validate_image_manifest(source_items, destination_manifest)
        existing_data = _read_existing_image_manifest(destination_manifest)

        new_by_filename: dict[str, dict] = {}
        new_order: list[str] = []
        for item in source_items:
            filename = item.get("filename")
            if not isinstance(filename, str):
                continue
            normalized_filename = filename.casefold()
            if normalized_filename not in new_by_filename:
                new_order.append(normalized_filename)
            new_by_filename[normalized_filename] = item

        merged: list[dict] = []
        seen: set[str] = set()
        for item in existing_data:
            if not isinstance(item, dict):
                continue
            filename = item.get("filename")
            if not isinstance(filename, str):
                continue
            normalized_filename = filename.casefold()
            if normalized_filename in new_by_filename:
                merged.append(new_by_filename[normalized_filename])
            else:
                merged.append(item)
            seen.add(normalized_filename)

        for normalized_filename in new_order:
            if normalized_filename not in seen:
                merged.append(new_by_filename[normalized_filename])

        _validate_image_manifest(merged, destination_manifest)
        _write_json_atomic(destination_manifest, merged)

    @staticmethod
    def _namespace_from_asset_dir(asset_dir: Path) -> str:
        """Derive a per-source namespace from a `<stem>_files` companion directory name."""
        name = asset_dir.name
        suffix = "_files"
        return name[:-len(suffix)] if name.endswith(suffix) else name

    def _image_destination_name(
        self,
        images_dir: Path,
        source_file: Path,
        namespace: str,
        existing_manifest: dict[str, dict],
        occupied_names: set[str],
    ) -> str:
        """Return a short unique image filename for the runtime image pool."""
        candidate = images_dir / source_file.name
        if candidate.name.casefold() not in occupied_names:
            return source_file.name
        try:
            meta = existing_manifest.get(candidate.name, {})
            if (
                meta.get("source_namespace") == namespace
                and candidate.is_file()
                and filecmp.cmp(source_file, candidate, shallow=False)
            ):
                return candidate.name
        except OSError:
            pass

        stem = source_file.stem
        suffix = source_file.suffix
        counter = 2
        while True:
            candidate = images_dir / f"{stem}_{counter}{suffix}"
            if candidate.name.casefold() not in occupied_names:
                return candidate.name
            try:
                meta = existing_manifest.get(candidate.name, {})
                if (
                    meta.get("source_namespace") == namespace
                    and candidate.is_file()
                    and filecmp.cmp(source_file, candidate, shallow=False)
                ):
                    return candidate.name
            except OSError:
                pass
            counter += 1

    def _propagate_image_assets(self, asset_dir: Path, project_dir: Path) -> None:
        """Copy converter-generated image assets and manifest into project images/.

        Filenames are preserved when possible because source Markdown commonly
        uses short names that are meaningful in context. Only real collisions
        receive a compact numeric suffix.
        """
        manifest_path = asset_dir / "image_manifest.json"
        if not manifest_path.is_file():
            return

        try:
            source_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[WARN] Cannot read image manifest {manifest_path}: {exc}")
            return
        try:
            source_data = _validate_image_manifest(source_payload, manifest_path)
        except RuntimeError as exc:
            print(f"[WARN] {exc}")
            return

        images_dir = project_dir / "images"
        namespace = self._namespace_from_asset_dir(asset_dir)
        destination_manifest = images_dir / "image_manifest.json"
        existing_data = _read_existing_image_manifest(destination_manifest)
        images_dir.mkdir(parents=True, exist_ok=True)

        existing_manifest = {
            item["filename"]: item
            for item in existing_data
        }
        occupied_names = {
            path.name.casefold()
            for path in images_dir.iterdir()
            if path.is_file()
        }
        rename_map: dict[str, str] = {}

        copied_count = 0
        for source_file in sorted(asset_dir.iterdir()):
            if not source_file.is_file():
                continue
            if source_file.suffix.lower() not in IMAGE_ASSET_SUFFIXES:
                continue
            new_name = self._image_destination_name(
                images_dir,
                source_file,
                namespace,
                existing_manifest,
                occupied_names,
            )
            destination = images_dir / new_name
            if source_file.resolve() != destination.resolve():
                shutil.copy2(source_file, destination)
            occupied_names.add(new_name.casefold())
            rename_map[source_file.name] = new_name
            copied_count += 1

        rebased_items: list[dict] = []
        for item in source_data:
            if not isinstance(item, dict):
                continue
            original = item.get("filename")
            if not isinstance(original, str):
                continue
            new_item = dict(item)
            new_item["filename"] = rename_map.get(original, original)
            new_item["source_namespace"] = namespace
            rebased_items.append(new_item)

        self._merge_image_manifest(rebased_items, images_dir / "image_manifest.json")
        print(
            f"Propagated {copied_count} image asset(s) + manifest "
            f"from {asset_dir} → images/ (namespace: {namespace})"
        )

    def _propagate_companion_image_assets(self, markdown_path: Path, project_dir: Path) -> None:
        asset_dir = markdown_path.with_name(f"{markdown_path.stem}_files")
        if asset_dir.is_dir():
            self._propagate_image_assets(asset_dir, project_dir)

    def _import_markdown_with_assets(
        self,
        source_path: Path,
        sources_dir: Path,
        move: bool,
    ) -> tuple[Path, Path | None, str | None]:
        archived_markdown = self._copy_or_move_file(
            source_path,
            sources_dir / source_path.name,
            move=move,
        )

        profile_src = source_path.with_name(f"{source_path.stem}.conversion_profile.json")
        if profile_src.is_file():
            self._copy_or_move_file(
                profile_src,
                sources_dir / f"{archived_markdown.stem}.conversion_profile.json",
                move=move,
            )

        asset_dir = self._companion_asset_dir(source_path)
        if asset_dir is None:
            return archived_markdown, None, None

        imported_asset_dir = self._copy_or_move_tree(
            asset_dir,
            sources_dir / f"{archived_markdown.stem}_files",
            move=move,
        )
        self._rewrite_markdown_asset_refs(
            archived_markdown,
            original_asset_dirname=asset_dir.name,
            imported_asset_dirname=imported_asset_dir.name,
        )

        note = None
        if archived_markdown.stem != source_path.stem:
            note = (
                f"{source_path}: renamed imported markdown to {archived_markdown.name} "
                f"and rewrote asset references to {imported_asset_dir.name}/"
            )
        return archived_markdown, imported_asset_dir, note

    def import_sources(
        self,
        project_path: str,
        source_items: list[str],
        move: bool = False,
        copy: bool = False,
    ) -> dict[str, list[str]]:
        if move and copy:
            raise ValueError("--move and --copy are mutually exclusive")
        project_dir = Path(project_path)
        if not project_dir.exists() or not project_dir.is_dir():
            raise FileNotFoundError(f"Project directory not found: {project_dir}")
        if not source_items:
            raise ValueError("At least one source path or URL is required")

        sources_dir = self._source_dir(project_dir)
        summary: dict[str, list[str]] = {
            "archived": [],
            "url_records": [],
            "markdown": [],
            "assets": [],
            "images": [],
            "analysis": [],
            "notes": [],
            "skipped": [],
        }

        expanded_items: list[str] = []
        supplied_dirs: list[Path] = []
        for item in source_items:
            if is_url(item):
                expanded_items.append(item)
                continue
            item_path = Path(item)
            if item_path.is_dir():
                supplied_dirs.append(item_path)
                directory_files = sorted(
                    path for path in item_path.iterdir() if path.is_file()
                )
                if directory_files:
                    expanded_items.extend(str(path) for path in directory_files)
                    summary["notes"].append(
                        f"{item}: expanded directory into {len(directory_files)} file(s)"
                    )
                else:
                    summary["skipped"].append(f"{item}: directory contains no files")
                continue
            expanded_items.append(item)

        explicit_markdown_stems = {
            Path(item).stem
            for item in expanded_items
            if not is_url(item)
            and Path(item).exists()
            and Path(item).is_file()
            and Path(item).suffix.lower() in {".md", ".markdown"}
        }

        for item in expanded_items:
            if is_url(item):
                markdown_path = self._ensure_unique_path(
                    sources_dir / f"{derive_url_basename(item)}.md"
                )
                try:
                    self._import_url(item, markdown_path)
                except Exception as exc:  # pragma: no cover - summary path
                    archived = self._archive_url_record(sources_dir, item)
                    summary["url_records"].append(str(archived))
                    summary["skipped"].append(f"{item}: {exc}")
                    continue

                if not self._is_valid_imported_url_markdown(markdown_path):
                    markdown_path.unlink(missing_ok=True)
                    archived = self._archive_url_record(sources_dir, item)
                    summary["url_records"].append(str(archived))
                    summary["skipped"].append(f"{item}: URL conversion produced no usable Markdown")
                    continue

                summary["markdown"].append(str(markdown_path))
                self._propagate_companion_image_assets(markdown_path, project_dir)
                continue

            source_path = Path(item)
            if not source_path.exists():
                summary["skipped"].append(f"{item}: path not found")
                continue
            if source_path.is_dir():
                summary["skipped"].append(f"{item}: directories are not supported")
                continue

            inside_projects = is_within_path(source_path, PROJECTS_ROOT)
            if copy:
                effective_move = False
            elif inside_projects:
                effective_move = True
            else:
                effective_move = False
            if move and not inside_projects:
                print(
                    f"note: {source_path} is outside {PROJECTS_ROOT}; copied "
                    f"(not moved). Only sources under projects/ may be moved.",
                    file=sys.stderr,
                )
            elif inside_projects and not move and not copy:
                print(
                    f"note: {source_path} is under projects/; moved into the target "
                    f"project. Pass --copy to preserve it.",
                    file=sys.stderr,
                )
            suffix = source_path.suffix.lower()

            if suffix in {".md", ".markdown"}:
                duplicate_markdown = self._find_equivalent_markdown(source_path, sources_dir)
                if duplicate_markdown is not None:
                    summary["markdown"].append(str(duplicate_markdown))
                    self._propagate_companion_image_assets(duplicate_markdown, project_dir)
                    summary["notes"].append(
                        f"{item}: skipped duplicate markdown import because equivalent content already exists as {duplicate_markdown.name}"
                    )
                    continue

                archived_markdown, asset_dir, note = self._import_markdown_with_assets(
                    source_path,
                    sources_dir,
                    move=effective_move,
                )
                summary["archived"].append(str(archived_markdown))
                summary["markdown"].append(str(archived_markdown))
                if asset_dir is not None:
                    summary["assets"].append(str(asset_dir))
                    self._propagate_image_assets(asset_dir, project_dir)
                if note:
                    summary["notes"].append(note)
                continue

            archived_path = self._copy_or_move_file(
                source_path,
                sources_dir / source_path.name,
                move=effective_move,
            )
            summary["archived"].append(str(archived_path))

            if suffix in BITMAP_IMAGE_SUFFIXES:
                images_dir = project_dir / "images"
                images_dir.mkdir(parents=True, exist_ok=True)
                image_path = self._ensure_unique_path(images_dir / archived_path.name)
                shutil.copy2(archived_path, image_path)
                summary["images"].append(str(image_path))
                if image_path.name != archived_path.name:
                    summary["notes"].append(
                        f"{item}: copied runtime image as {image_path.name} "
                        "to avoid a filename collision"
                    )
            elif suffix in PDF_SUFFIXES:
                canonical_markdown_path = sources_dir / f"{archived_path.stem}.md"
                if archived_path.stem in explicit_markdown_stems:
                    summary["notes"].append(
                        f"{item}: skipped PDF auto-conversion because a same-stem Markdown source was provided"
                    )
                    continue
                if canonical_markdown_path.exists():
                    summary["markdown"].append(str(canonical_markdown_path))
                    self._propagate_companion_image_assets(canonical_markdown_path, project_dir)
                    summary["notes"].append(
                        f"{item}: skipped PDF auto-conversion because {canonical_markdown_path.name} already exists"
                    )
                    continue
                markdown_path = canonical_markdown_path
                try:
                    self._import_pdf(archived_path, markdown_path)
                    summary["markdown"].append(str(markdown_path))
                    self._propagate_companion_image_assets(markdown_path, project_dir)
                except Exception as exc:  # pragma: no cover - summary path
                    summary["skipped"].append(f"{item}: PDF conversion failed ({exc})")
            elif suffix in PRESENTATION_SUFFIXES:
                canonical_markdown_path = sources_dir / f"{archived_path.stem}.md"
                try:
                    intake_dir = self._import_pptx_intake(archived_path, project_dir)
                    intake_str = str(intake_dir)
                    if intake_str not in summary["analysis"]:
                        summary["analysis"].append(intake_str)
                except Exception as exc:  # pragma: no cover - summary path
                    summary["notes"].append(f"{item}: PPTX intake analysis failed ({exc})")
                if archived_path.stem in explicit_markdown_stems:
                    summary["notes"].append(
                        f"{item}: skipped presentation auto-conversion because a same-stem Markdown source was provided"
                    )
                    continue
                if canonical_markdown_path.exists():
                    summary["markdown"].append(str(canonical_markdown_path))
                    self._propagate_companion_image_assets(canonical_markdown_path, project_dir)
                    summary["notes"].append(
                        f"{item}: skipped presentation auto-conversion because {canonical_markdown_path.name} already exists"
                    )
                    continue
                markdown_path = canonical_markdown_path
                try:
                    self._import_presentation(archived_path, markdown_path)
                    summary["markdown"].append(str(markdown_path))
                    self._propagate_companion_image_assets(markdown_path, project_dir)
                except Exception as exc:  # pragma: no cover - summary path
                    summary["skipped"].append(f"{item}: presentation conversion failed ({exc})")
            elif suffix in EXCEL_SUFFIXES:
                canonical_markdown_path = sources_dir / f"{archived_path.stem}.md"
                if archived_path.stem in explicit_markdown_stems:
                    summary["notes"].append(
                        f"{item}: skipped Excel auto-conversion because a same-stem Markdown source was provided"
                    )
                    continue
                if canonical_markdown_path.exists():
                    summary["markdown"].append(str(canonical_markdown_path))
                    self._propagate_companion_image_assets(canonical_markdown_path, project_dir)
                    summary["notes"].append(
                        f"{item}: skipped Excel auto-conversion because {canonical_markdown_path.name} already exists"
                    )
                    continue
                markdown_path = canonical_markdown_path
                try:
                    self._import_excel(archived_path, markdown_path)
                    summary["markdown"].append(str(markdown_path))
                    self._propagate_companion_image_assets(markdown_path, project_dir)
                except Exception as exc:  # pragma: no cover - summary path
                    summary["skipped"].append(f"{item}: Excel conversion failed ({exc})")
            elif suffix in LEGACY_EXCEL_SUFFIXES:
                summary["notes"].append(
                    f"{item}: archived only; legacy .xls is not converted automatically. "
                    "Resave as .xlsx to generate Markdown."
                )
            elif suffix in TABLE_TEXT_SUFFIXES:
                summary["notes"].append(
                    f"{item}: archived as a plain-text table source; no Markdown conversion needed"
                )
            elif suffix in DOC_SUFFIXES:
                canonical_markdown_path = sources_dir / f"{archived_path.stem}.md"
                if archived_path.stem in explicit_markdown_stems:
                    summary["notes"].append(
                        f"{item}: skipped document auto-conversion because a same-stem Markdown source was provided"
                    )
                    continue
                if canonical_markdown_path.exists():
                    summary["markdown"].append(str(canonical_markdown_path))
                    self._propagate_companion_image_assets(canonical_markdown_path, project_dir)
                    summary["notes"].append(
                        f"{item}: skipped document auto-conversion because {canonical_markdown_path.name} already exists"
                    )
                    continue
                markdown_path = canonical_markdown_path
                try:
                    self._import_doc(archived_path, markdown_path)
                    summary["markdown"].append(str(markdown_path))
                    self._propagate_companion_image_assets(markdown_path, project_dir)
                except Exception as exc:  # pragma: no cover - summary path
                    summary["skipped"].append(f"{item}: document conversion failed ({exc})")
            elif suffix == ".txt":
                markdown_path = self._normalize_text_source(archived_path, sources_dir)
                summary["markdown"].append(str(markdown_path))
            else:
                summary["notes"].append(f"{item}: archived only, no automatic conversion")

        # Cleanup: only a projects-local source directory may be removed after
        # its files move into the target project. Every other location is copied
        # and remains untouched, even when the caller passes --move.
        for directory in supplied_dirs:
            if copy or not is_within_path(directory, PROJECTS_ROOT):
                continue
            if directory.is_dir() and not any(directory.iterdir()):
                try:
                    directory.rmdir()
                except OSError:
                    continue
                summary["notes"].append(
                    f"{directory}: removed empty source directory after import"
                )

        context_path = project_dir / "route_context.json"
        if context_path.is_file():
            try:
                context = json.loads(context_path.read_text(encoding="utf-8"))
                if context.get("route") == "create_pptx_from_template":
                    context["content_sources"] = sorted(
                        str(path.relative_to(project_dir))
                        for path in sources_dir.rglob("*")
                        if path.is_file()
                    )
                    _write_json_atomic(context_path, context)
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Cannot refresh route context: {context_path}: {exc}") from exc

        return summary

    def import_template(
        self,
        project_path: str,
        template_pptx: str,
        *,
        replace: bool = False,
        render_previews: bool = True,
        register_brand: str | None = None,
        register_icon_layout: str | None = None,
        register_chart_layout: str | None = None,
        register_page_kit_layout: str | None = None,
    ) -> dict[str, object]:
        """Import a user-provided PPTX and optionally register reusable assets.

        The public import is always a Brand import.  Icon and chart grammar
        Layouts are optional, deliberately narrow companion assets: they never
        turn the source deck's pages into reusable layouts.
        """
        project_dir = Path(project_path).expanduser().resolve()
        source = Path(template_pptx).expanduser().resolve()
        if not project_dir.is_dir():
            raise FileNotFoundError(f"Project directory not found: {project_dir}")
        if not source.is_file():
            raise FileNotFoundError(f"Template PPTX not found: {source}")
        if source.suffix.lower() != ".pptx":
            raise ValueError(f"Template must be a .pptx package: {source}")

        template_dir = project_dir / "template"
        template_dir.mkdir(parents=True, exist_ok=True)
        destination = template_dir / f"source{source.suffix.lower()}"
        source_digest = sha256(source.read_bytes()).hexdigest()
        if destination.exists():
            destination_digest = sha256(destination.read_bytes()).hexdigest()
            if destination_digest != source_digest and not replace:
                raise FileExistsError(
                    f"A different template is already imported: {destination}; "
                    "pass --replace to replace the project copy"
                )
        if destination.exists() and sha256(destination.read_bytes()).hexdigest() != source_digest:
            destination.chmod(0o644)
        if not destination.exists() or sha256(destination.read_bytes()).hexdigest() != source_digest:
            shutil.copy2(source, destination)
        destination.chmod(0o444)

        analysis_dir = self._analysis_dir(project_dir)
        command = [
            sys.executable,
            str(TOOLS_DIR / "pptx_intake.py"),
            str(destination),
            "-o",
            str(analysis_dir),
            "--intent",
            "template",
        ]
        if not render_previews:
            command.append("--no-previews")
        self._run_tool(command)

        registered_icon_layout = None
        if register_icon_layout:
            registered_icon_layout = self._materialize_imported_icon_layout(
                analysis_dir=analysis_dir,
                layout_id=register_icon_layout,
            )
        registered_chart_layout = None
        if register_chart_layout:
            registered_chart_layout = self._materialize_imported_chart_layout(
                source=source,
                analysis_dir=analysis_dir,
                layout_id=register_chart_layout,
            )
        registered_page_kit_layout = None
        if register_page_kit_layout:
            registered_page_kit_layout = self._materialize_imported_page_kit_layout(
                source=source, analysis_dir=analysis_dir, layout_id=register_page_kit_layout,
            )
        # Materialize the Page Kit first so the Brand's frontmatter records a
        # durable link rather than relying on a project-local import context.
        registered_brand = None
        if register_brand:
            registered_brand = self._materialize_imported_brand(
                source=source,
                analysis_dir=analysis_dir,
                brand_id=register_brand,
                page_kit_layout_id=(
                    registered_page_kit_layout["layout_id"]
                    if registered_page_kit_layout is not None else None
                ),
            )

        sources_dir = self._source_dir(project_dir)
        content_sources = sorted(
            str(path.relative_to(project_dir))
            for path in sources_dir.rglob("*")
            if path.is_file()
        )
        context_path = project_dir / "route_context.json"
        previous_context: dict[str, object] = {}
        if context_path.is_file():
            try:
                loaded_context = json.loads(context_path.read_text(encoding="utf-8"))
                if isinstance(loaded_context, dict):
                    previous_context = loaded_context
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Cannot read existing route context: {context_path}: {exc}") from exc

        context = {
            "schema": "ppt-master-plus.route-context.v1",
            "route": "create_pptx_from_template",
            "engine": "svg_generate",
            "profile": "imported_brand",
            "adaptation": "brand_identity",
            "modules": [],
            "visualization_style_source": "skill_builtin",
            "visualization_catalogs": [
                "templates/charts/charts_index.json",
                "templates/tables/tables_index.json",
            ],
            "template_origin": "user_provided_pptx",
            "template_import_required": True,
            "template_import_mode": "readonly_copy",
            "template_kind": "brand",
            "template_reuse": "identity_only",
            "template_archetypes_reusable": False,
            "template_pptx": str(destination.relative_to(project_dir)),
            "template_sha256": source_digest,
            "content_sources": content_sources,
            "output_pptx": None,
            "source_template_path": str(source),
            "source_template_immutable": True,
        }
        for key in (
            "brand_id", "brand_library_path", "icon_layout_id",
            "icon_layout_library_path", "chart_layout_id", "chart_layout_library_path",
            "chart_visualization_style_source",
            "page_kit_layout_id", "page_kit_layout_library_path", "page_kit_enabled",
        ):
            if key in previous_context:
                context[key] = previous_context[key]
        if registered_brand is not None:
            context["brand_id"] = registered_brand["brand_id"]
            context["brand_library_path"] = registered_brand["path"]
        if registered_icon_layout is not None:
            context["icon_layout_id"] = registered_icon_layout["layout_id"]
            context["icon_layout_library_path"] = registered_icon_layout["path"]
        if registered_chart_layout is not None:
            context["chart_layout_id"] = registered_chart_layout["layout_id"]
            context["chart_layout_library_path"] = registered_chart_layout["path"]
            context["chart_visualization_style_source"] = "registered_layout"
        if registered_page_kit_layout is not None:
            context["page_kit_layout_id"] = registered_page_kit_layout["layout_id"]
            context["page_kit_layout_library_path"] = registered_page_kit_layout["path"]
            context["page_kit_enabled"] = True
            context["adaptation"] = "brand_page_kit"
            context["template_reuse"] = "page_kit"
            context["template_archetypes_reusable"] = True
        _write_json_atomic(context_path, context)
        return {
            "template_pptx": str(destination),
            "analysis_dir": str(analysis_dir),
            "route_context": str(context_path),
            **({"registered_brand": registered_brand} if registered_brand else {}),
            **({"registered_icon_layout": registered_icon_layout} if registered_icon_layout else {}),
            **({"registered_chart_layout": registered_chart_layout} if registered_chart_layout else {}),
            **({"registered_page_kit_layout": registered_page_kit_layout} if registered_page_kit_layout else {}),
        }

    def _materialize_imported_page_kit_layout(self, *, source: Path, analysis_dir: Path, layout_id: str) -> dict[str, str]:
        """Store only Web-confirmed native prototypes and clean content shells."""
        resolved_id = _brand_id(layout_id)
        layout_root = REPO_ROOT / "templates" / "layouts"
        destination = layout_root / resolved_id
        if destination.exists():
            raise FileExistsError(f"Layout already exists: {destination}; choose a new --register-page-kit-layout id")
        try:
            archetypes = json.loads((analysis_dir / "template_archetypes.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError("Template archetypes are required before registering a Page Kit") from exc
        approved = _load_brand_page_selection(
            source=source, analysis_dir=analysis_dir, archetypes=archetypes,
        )
        prototypes: list[dict[str, object]] = []
        for selected in approved:
            item = selected["source"]
            assert isinstance(item, dict)
            role = str(selected["role"])
            if item.get("copy_strategy") != "native_roundtrip_clone":
                raise RuntimeError(
                    f"Selected slide {selected['source_slide']} is not safe for native cloning"
                )
            if role == "content":
                title_candidates = [
                    obj
                    for obj in item.get("objects", [])
                    if isinstance(obj, dict)
                    and obj.get("kind") == "shape"
                    and obj.get("role") == "title"
                    and obj.get("shape_id") is not None
                ]
                if not title_candidates:
                    raise RuntimeError(
                        f"Selected content slide {selected['source_slide']} has no title text frame; "
                        "choose a body Master/Layout candidate that includes the large-title slot"
                    )
                largest_title = max(
                    title_candidates,
                    key=lambda obj: (
                        float((obj.get("capacity") or {}).get("observed_font_size_px") or 0),
                        -int((obj.get("geometry") or {}).get("y_emu") or 0),
                    ),
                )
                title_slots = [str(largest_title["shape_id"])]
                prototypes.append(
                    {
                        "role": role,
                        "source_slide": selected["source_slide"],
                        "copy_strategy": "native_roundtrip_clone",
                        "shell_policy": "master_layout_plus_empty_title",
                        "locked_objects": [],
                        "editable_slots": title_slots,
                        "content_edit_policy": "add_slide_local_content_over_locked_master_layout",
                    }
                )
                continue
            prototypes.append(
                {
                    "role": role,
                    "source_slide": selected["source_slide"],
                    "copy_strategy": "native_roundtrip_clone",
                    "shell_policy": "native_prototype",
                    "locked_objects": [
                        obj.get("shape_id")
                        for obj in item.get("objects", [])
                        if isinstance(obj, dict) and not obj.get("editable")
                    ],
                    "editable_slots": [
                        obj.get("shape_id")
                        for obj in item.get("objects", [])
                        if isinstance(obj, dict) and obj.get("editable")
                    ],
                }
            )
        if not prototypes:
            raise RuntimeError("The confirmed Brand import selection contains no prototypes")
        temp_dir = Path(tempfile.mkdtemp(prefix=f".{resolved_id}.", dir=str(layout_root)))
        try:
            _sanitize_content_master_slides(
                source,
                temp_dir / "prototype_source.pptx",
                {
                    int(prototype["source_slide"]): {
                        str(shape_id) for shape_id in prototype["editable_slots"]
                    }
                    for prototype in prototypes if prototype["role"] == "content"
                },
            )
            (temp_dir / "page_kit_manifest.json").write_text(
                json.dumps(
                    {
                        "schema": "ppt-master-plus.brand-page-kit.v2",
                        "prototype_source": "prototype_source.pptx",
                        "roles": prototypes,
                        "selection_source": "Brand Import Web",
                        "excluded_roles": ["guide", "unusable", "unselected"],
                        "reuse": "web_confirmed_native_prototypes_and_master_layout_shells",
                        "content_shell_policy": (
                            "strip every slide-local object; retain only the selected slide's "
                            "Master/Layout inheritance, including Master background images, "
                            "Master text and Master/Layout placeholders, plus an empty editable "
                            "large-title text frame with its original typography and geometry"
                        ),
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )
            (temp_dir / "design_spec.md").write_text(f"""---\nlayout_id: {resolved_id}\nkind: layout\nsummary: 用户通过 Brand Import Web 确认的封面、目录、过渡、正文母版与封底\ncanvas_format: ppt169\npage_count: {len(prototypes)}\npage_types: [{', '.join(sorted({str(p['role']) for p in prototypes}))}]\n---\n\n# Brand Page Kit\n\nOnly clone Web-confirmed rows in `page_kit_manifest.json`. Cover, TOC, section and closing rows retain their selected native prototypes. Content rows retain the linked Master/Layout background images, text and placeholders, plus one empty editable large-title text frame with its original geometry and typography. Every other slide-local object is removed. New body content may be added only above that locked Master/Layout. Guide, specification, unselected pages and source examples are prohibited.\n""", encoding="utf-8")
            os.replace(temp_dir, destination)
        except OSError as exc:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to materialize Page Kit: {exc}") from exc
        return {"layout_id": resolved_id, "path": str(destination.relative_to(REPO_ROOT))}

    def _materialize_imported_icon_layout(
        self,
        *,
        analysis_dir: Path,
        layout_id: str,
    ) -> dict[str, str]:
        """Register a neutral Layout that records imported PPTX icon grammar.

        This is deliberately a layout-local visual grammar, not a copy of any
        branded icon, logo, page composition, chart legend, or source geometry.
        Its neutral SVG is a reusable reference board; an active Brand supplies
        color and typography at generation time.
        """
        resolved_id = _brand_id(layout_id)
        layout_root = REPO_ROOT / "templates" / "layouts"
        destination = layout_root / resolved_id
        if destination.exists():
            raise FileExistsError(
                f"Layout already exists: {destination}; choose a new --register-icon-layout id"
            )
        assets_path = analysis_dir / "template_assets.json"
        try:
            assets = json.loads(assets_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Template intake assets are required before registering an icon Layout"
            ) from exc
        icon_candidates = [
            {
                "filename": item.get("filename"),
                "format": item.get("format"),
                "width_px": item.get("width_px"),
                "height_px": item.get("height_px"),
                "role_confidence": item.get("role_confidence"),
            }
            for item in assets.get("items", [])
            if isinstance(item, dict) and item.get("role") == "icon_candidate"
        ]
        temp_dir = Path(tempfile.mkdtemp(prefix=f".{resolved_id}.", dir=str(layout_root)))
        try:
            (temp_dir / "icon_style_manifest.json").write_text(
                json.dumps(
                    {
                        "schema": "ppt-master-plus.imported-icon-layout.v1",
                        "source": "user_provided_pptx",
                        "icon_candidates": icon_candidates,
                        "reuse": "neutral_icon_grammar_only",
                        "excluded": [
                            "brand_colors",
                            "brand_logos",
                            "source_page_geometry",
                            "chart_table_legend_styles",
                            "sample_copy",
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )
            spec = f'''---
layout_id: {resolved_id}
kind: layout
summary: 从用户 PPTX 提取的中性图标语法参考，用于科技发布类页面的图标点缀与强调
canvas_format: ppt169
page_count: 1
page_types: [icon_grammar]
---

# Imported Icon Grammar Layout

> Structure-only Layout. This is a neutral icon grammar board, not a source-slide replica. Brand controls color, typography, logos, and icon assets.

## I. Template Overview
| Property | Value |
|---|---|
| Use Cases | 科技发布、产品能力分组、流程步骤和关键点强调 |
| Structure | 小型图标作为标题前缀、节点标识或局部视觉锚点；不承载页面主结构 |

## II. Icon Grammar
- Source signals: {len(icon_candidates)} transparent icon candidate(s) detected in the user-supplied PPTX.
- Shape language: compact, high-contrast, single-focus icon anchors with generous surrounding whitespace.
- Color rule: inherit the resolved Brand primary/accent colors at generation time; the neutral SVG below does not lock a color.
- Prohibited reuse: source logos, business illustration content, chart/table legend conventions, source-page geometry, and sample text.

## III. SVG Roster
- `01_icon_grammar.svg`: neutral reference for icon scale, alignment, and callout placement only.
'''
            (temp_dir / "design_spec.md").write_text(spec, encoding="utf-8")
            svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <g id="icon-grammar" fill="none" stroke="#1A1A1A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="180" cy="240" r="54"/>
    <path d="M150 240h60M180 210v60"/>
    <rect x="400" y="186" width="108" height="108" rx="20"/>
    <path d="M432 240h44M454 218v44"/>
    <path d="M680 294l54-108 54 108zM716 258h36"/>
  </g>
  <g fill="#1A1A1A" font-family="Arial, sans-serif" font-size="24">
    <text x="126" y="350">icon anchor</text>
    <text x="402" y="350">icon + label</text>
    <text x="674" y="350">key callout</text>
  </g>
</svg>
'''
            (temp_dir / "01_icon_grammar.svg").write_text(svg, encoding="utf-8")
            os.replace(temp_dir, destination)
        except OSError as exc:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to materialize icon Layout: {exc}") from exc
        return {
            "layout_id": resolved_id,
            "path": str(destination.relative_to(REPO_ROOT)),
        }

    def _materialize_imported_chart_layout(
        self,
        *,
        source: Path,
        analysis_dir: Path,
        layout_id: str,
    ) -> dict[str, str]:
        """Register chart visual grammar without importing source chart data or pages."""
        resolved_id = _brand_id(layout_id)
        layout_root = REPO_ROOT / "templates" / "layouts"
        destination = layout_root / resolved_id
        if destination.exists():
            raise FileExistsError(
                f"Layout already exists: {destination}; choose a new --register-chart-layout id"
            )
        library_path = analysis_dir / "source.slide_library.json"
        try:
            library = json.loads(library_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Template slide-library facts are required before registering a chart Layout"
            ) from exc
        chart_specs: list[dict[str, object]] = []
        for slide in library.get("slides", []):
            if not isinstance(slide, dict):
                continue
            for chart in slide.get("charts", []):
                if not isinstance(chart, dict):
                    continue
                chart_specs.append({
                    "chart_type": chart.get("chart_type"),
                    "chart_kind": chart.get("chart_kind"),
                    "series_count": chart.get("series_count"),
                    "category_count": chart.get("category_count"),
                    "plot_types": chart.get("plot_types"),
                    "edit_capability": chart.get("edit_capability"),
                })
        style_parts: list[dict[str, str]] = []
        style_payloads: dict[str, bytes] = {}
        chart_profiles: list[dict[str, object]] = []
        try:
            with zipfile.ZipFile(source) as package:
                for part in sorted(
                    name for name in package.namelist()
                    if name.startswith("ppt/charts/")
                    and Path(name).name.startswith(("style", "colors"))
                    and name.endswith(".xml")
                ):
                    data = package.read(part)
                    style_payloads[Path(part).name] = data
                    style_parts.append({
                        "part": part,
                        "sha256": sha256(data).hexdigest(),
                    })
                for part in sorted(
                    name for name in package.namelist()
                    if name.startswith("ppt/charts/chart") and name.endswith(".xml")
                ):
                    root = ET.fromstring(package.read(part))
                    tags = [node.tag.rsplit("}", 1)[-1] for node in root.iter()]
                    chart_profiles.append({
                        "part": part,
                        "style": next((node.attrib.get("val") for node in root.iter()
                                       if node.tag.rsplit("}", 1)[-1] == "style"), None),
                        "chart_types": sorted({tag for tag in tags if tag in {
                            "barChart", "lineChart", "pieChart", "doughnutChart", "areaChart",
                            "scatterChart", "radarChart", "bubbleChart", "stockChart"
                        }}),
                        "legend_position": next((node.attrib.get("val") for node in root.iter()
                                                 if node.tag.rsplit("}", 1)[-1] == "legendPos"), None),
                        "has_major_gridlines": "majorGridlines" in tags,
                        "data_label_fields": sorted({tag for tag in tags if tag in {
                            "showVal", "showCatName", "showSerName", "showLegendKey", "showPercent"
                        }}),
                        "color_tokens": sorted({node.attrib.get("val") for node in root.iter()
                                              if node.tag.rsplit("}", 1)[-1] in {"srgbClr", "schemeClr"}
                                              and node.attrib.get("val")}),
                    })
        except (OSError, zipfile.BadZipFile) as exc:
            raise RuntimeError(f"Cannot inspect chart styles in {source}: {exc}") from exc

        temp_dir = Path(tempfile.mkdtemp(prefix=f".{resolved_id}.", dir=str(layout_root)))
        try:
            manifest = {
                "schema": "ppt-master-plus.imported-chart-layout.v1",
                "source": "user_provided_pptx",
                "chart_visual_grammar": chart_specs,
                "native_chart_profiles": chart_profiles,
                "chart_style_parts": style_parts,
                "reuse": "chart_visual_grammar_only",
                "excluded": [
                    "source_categories",
                    "source_series_names",
                    "source_series_values",
                    "source_page_geometry",
                    "brand_logos",
                    "sample_copy",
                ],
            }
            (temp_dir / "chart_style_manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            style_dir = temp_dir / "chart_styles"
            style_dir.mkdir(parents=True, exist_ok=True)
            for filename, data in style_payloads.items():
                (style_dir / filename).write_bytes(data)
            chart_types = sorted({str(item.get("chart_type")) for item in chart_specs if item.get("chart_type")})
            spec = f'''---
layout_id: {resolved_id}
kind: layout
summary: 从用户 PPTX 提取的图表视觉语法 Layout，保留图表类型、视觉层级与标注规则，不含示例数据
canvas_format: ppt169
page_count: 1
page_types: [chart_grammar]
---

# Imported Chart Grammar Layout

> Structure-only chart Layout. It may guide chart type, series hierarchy, axes, gridlines, legend, and labels. The selected Brand supplies colors and typography; source data and page geometry are never reused.

## I. Template Overview
| Property | Value |
|---|---|
| Use Cases | 经营分析、版本回顾、技术能力对比与趋势解读 |
| Detected Chart Types | {", ".join(chart_types) if chart_types else "none"} |
| Source Style Parts | {len(style_parts)} OOXML chart style part(s) captured as metadata |

## II. Chart Grammar
- Prefer source-derived chart type and information hierarchy only when this Layout is explicitly selected.
- Resolve color, font, icon and logo from the selected Brand; never bake a Brand color or logo into this Layout.
- Use current project data only. Do not reuse source categories, series names, values, or slide placement.
- `chart_style_manifest.json` records detected native chart families and style-part hashes; `chart_styles/` preserves the corresponding OOXML chart-style XML for renderer adaptation.

## III. SVG Roster
- `01_chart_grammar.svg`: neutral reference board for axis, gridline, bar/line hierarchy and legend treatment.
'''
            (temp_dir / "design_spec.md").write_text(spec, encoding="utf-8")
            svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <g id="chart-grammar" fill="none" stroke="#1A1A1A" stroke-width="3">
    <path d="M150 520H650M150 180V520"/>
    <path d="M150 270H650M150 395H650" stroke="#D0D0D0"/>
    <rect x="220" y="365" width="54" height="155" fill="#4A4A4A" stroke="none"/>
    <rect x="320" y="295" width="54" height="225" fill="#808080" stroke="none"/>
    <rect x="420" y="230" width="54" height="290" fill="#B0B0B0" stroke="none"/>
    <path d="M770 470L870 385 970 420 1070 250" stroke="#1A1A1A" stroke-width="7"/>
    <circle cx="770" cy="470" r="8" fill="#1A1A1A"/><circle cx="870" cy="385" r="8" fill="#1A1A1A"/><circle cx="970" cy="420" r="8" fill="#1A1A1A"/><circle cx="1070" cy="250" r="8" fill="#1A1A1A"/>
  </g>
  <g fill="#1A1A1A" font-family="Arial, sans-serif" font-size="22">
    <text x="150" y="575">axis + light grid</text><text x="760" y="575">series + restrained legend</text>
  </g>
</svg>
'''
            (temp_dir / "01_chart_grammar.svg").write_text(svg, encoding="utf-8")
            os.replace(temp_dir, destination)
        except OSError as exc:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to materialize chart Layout: {exc}") from exc
        return {
            "layout_id": resolved_id,
            "path": str(destination.relative_to(REPO_ROOT)),
        }

    def _materialize_imported_brand(
        self,
        *,
        source: Path,
        analysis_dir: Path,
        brand_id: str,
        page_kit_layout_id: str | None = None,
    ) -> dict[str, str]:
        """Create a global identity-only Brand from a user-authorized PPTX import.

        Only named Brand assets that are referenced by a Slide Master or Layout
        are copied. Example pages, source topology, and the original PPTX are
        deliberately excluded. Chart/table grammar can only be registered as a
        separate, explicit companion Layout.
        """
        resolved_id = _brand_id(brand_id)
        brand_root = REPO_ROOT / "templates" / "brands"
        destination = brand_root / resolved_id
        if destination.exists():
            raise FileExistsError(
                f"Brand already exists: {destination}; choose a new --register-brand id"
            )

        token_path = analysis_dir / "template_design_tokens.json"
        identity_path = analysis_dir / "source.identity.json"
        assets_path = analysis_dir / "template_assets.json"
        try:
            tokens = json.loads(token_path.read_text(encoding="utf-8"))
            identity = json.loads(identity_path.read_text(encoding="utf-8"))
            assets = json.loads(assets_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Template intake artifacts are required before registering a Brand"
            ) from exc

        colors = _hex_values(tokens.get("declared_hex_colors"))
        theme = tokens.get("theme") if isinstance(tokens.get("theme"), dict) else {}
        palette = theme.get("palette") if isinstance(theme, dict) else {}
        primary = colors[0] if colors else str(palette.get("primary") or "#0055FF")
        accent = colors[1] if len(colors) > 1 else str(palette.get("accent5") or "#FF6A00")
        title_font = _observed_font(identity, preferred_words=("bold",))
        body_font = _observed_font(identity, preferred_words=("medium",))
        theme_fonts = theme.get("fonts") if isinstance(theme, dict) else {}
        title_font = title_font or str(
            ((theme_fonts.get("title") or {}).get("ea")) if isinstance(theme_fonts, dict) else ""
        ) or "Arial"
        body_font = body_font or str(
            ((theme_fonts.get("body") or {}).get("ea")) if isinstance(theme_fonts, dict) else ""
        ) or title_font

        fixed_assets = [
            item for item in assets.get("items", [])
            if isinstance(item, dict)
            and item.get("role") == "fixed_template_asset"
            and isinstance(item.get("part"), str)
            and isinstance(item.get("filename"), str)
        ]
        temp_dir = Path(tempfile.mkdtemp(prefix=f".{resolved_id}.", dir=str(brand_root)))
        try:
            images_dir = temp_dir / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            extracted: list[str] = []
            with zipfile.ZipFile(source) as package:
                for index, asset in enumerate(fixed_assets):
                    part = asset["part"]
                    suffix = Path(asset["filename"]).suffix.lower() or ".bin"
                    name = "logo" + suffix if index == 0 else f"brand_asset_{index + 1}{suffix}"
                    target = temp_dir / name if index == 0 else images_dir / name
                    with package.open(part) as src_handle, target.open("wb") as dst_handle:
                        shutil.copyfileobj(src_handle, dst_handle)
                    extracted.append(str(target.relative_to(temp_dir)))

            source_digest = sha256(source.read_bytes()).hexdigest()
            spec = f'''---
brand_id: {resolved_id}
kind: brand
summary: 从“{source.stem}”导入的品牌身份，适用于与源模板一致的演示场景
keywords: [imported brand, user-authorized PPTX]
primary_color: "{primary}"
{f"page_kit_layout_id: {page_kit_layout_id}" if page_kit_layout_id else ""}
---

# Imported Brand Specification

> Identity-only preset imported from a user-authorized PPTX. It contains no source-page roster, master/layout topology, object geometry, sample copy, or chart/table styling. A user may register the latter separately as a narrowly scoped chart-grammar Layout.

## I. Brand Overview
| Property | Value |
|---|---|
| Brand Name | {source.stem} |
| Use Cases | 与源模板一致的演示场景 |
| Tone | 由源模板的实际视觉身份决定 |

## II. Color Scheme
| Role | HEX | Provenance |
|---|---|---|
| primary | {primary} | fact（模板规范页） |
| secondary | #FFFFFF | fact（模板规范页） |
| accent | {accent} | fact（模板规范页） |
| neutral | #929292 | fact（模板规范页） |
| text | #000000 | fact（模板规范页） |
| bg | #FFFFFF | fact（模板规范页） |

Usage notes [fact]：颜色令牌来自源模板；默认使用 Skill 内置图表与表格样式。若用户显式选择同源的 chart-grammar Layout，才可采用其图例、坐标轴、网格线与标签规则，数据仍来自当前内容。

## III. Typography
| Role | Family | Weight |
|---|---|---|
| title | {title_font} | Bold |
| body | {body_font} | Medium |
| latin | Arial | Regular |

Type scale [fact]：大标题 54pt Bold；副标题 32pt Regular；正文 22pt Regular、1.5 倍行距；重点文字 22pt Bold + 主色。

## IV. Logo
- File: `./logo.png`（若源模板的主版资源格式不支持直接渲染，则将其作为品牌资产参考）
- Usage: cover and recurring brand-anchor pages

## V. Voice & Tone
- Formality: formal
- Person: we
- Emoji: forbidden
- Abbreviations: common-abbrev-allowed

## VI. Icon Style
- Preference: duotone
- Rule: 使用内置图标库；不复用模板示例页的业务图例或信息图语法。

## VII. Visual Assets
- Master-derived assets: {", ".join(f"`./{item}`" for item in extracted) if extracted else "none"}
- Source provenance: `{source.name}`; SHA-256 `{source_digest}`
'''
            (temp_dir / "design_spec.md").write_text(spec, encoding="utf-8")
            os.replace(temp_dir, destination)
        except (OSError, zipfile.BadZipFile, KeyError) as exc:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to materialize Brand assets from {source}: {exc}") from exc

        return {
            "brand_id": resolved_id,
            "path": str(destination.relative_to(REPO_ROOT)),
        }

    def activate_confirmed_brand_page_kit(self, project_path: str) -> str:
        """Turn a confirmed Brand Page Kit choice into a native executor contract.

        This deliberately creates no free-design fallback.  The native executor
        receives an immutable source package plus the approved prototype and
        editable-slot roster; an unapproved role or an identity-only choice
        remains on the normal SVG generation path.
        """
        project_dir = Path(project_path).expanduser().resolve()
        result_path = project_dir / "confirm_ui" / "result.json"
        context_path = project_dir / "route_context.json"
        if not result_path.is_file():
            raise FileNotFoundError(f"Confirmed UI result not found: {result_path}")
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Cannot read confirmation result: {result_path}") from exc
        brand_id = result.get("brand")
        if not isinstance(brand_id, str) or not brand_id or brand_id == "none":
            raise ValueError("A selected Brand is required before activating a Page Kit")
        if result.get("page_kit", "identity_only") != "use_page_kit":
            raise ValueError("Confirmed choice is identity_only; native Page Kit execution is disabled")
        index_path = REPO_ROOT / "templates" / "brands" / "brands_index.json"
        try:
            brands = json.loads(index_path.read_text(encoding="utf-8"))
            brand = brands[brand_id]
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            raise RuntimeError(f"Selected Brand is not registered: {brand_id!r}") from exc
        layout_id = brand.get("page_kit_layout_id")
        if not isinstance(layout_id, str) or not layout_id:
            raise ValueError(f"Brand {brand_id!r} has no registered Page Kit")
        layout_dir = REPO_ROOT / "templates" / "layouts" / layout_id
        manifest_path = layout_dir / "page_kit_manifest.json"
        source_path = layout_dir / "prototype_source.pptx"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Cannot read Page Kit manifest: {manifest_path}") from exc
        if (
            not source_path.is_file()
            or manifest.get("reuse")
            != "web_confirmed_native_prototypes_and_master_layout_shells"
        ):
            raise RuntimeError(f"Invalid Page Kit Layout: {layout_id}")
        roles = manifest.get("roles")
        if not isinstance(roles, list) or not roles:
            raise RuntimeError(f"Page Kit {layout_id} contains no approved prototypes")
        approved = {"cover", "toc", "section", "content", "closing"}
        if any(not isinstance(row, dict) or row.get("role") not in approved or row.get("copy_strategy") != "native_roundtrip_clone" for row in roles):
            raise RuntimeError(f"Page Kit {layout_id} has an unsafe prototype roster")
        if any(
            row.get("role") == "content"
            and (
                row.get("shell_policy") != "master_layout_plus_empty_title"
                or not isinstance(row.get("editable_slots"), list)
                or not row.get("editable_slots")
                or row.get("locked_objects") != []
            )
            for row in roles
        ):
            raise RuntimeError(
                f"Page Kit {layout_id} contains a non-sanitized content prototype"
            )
        project_template = project_dir / "template"
        project_template.mkdir(parents=True, exist_ok=True)
        project_source = project_template / "page_kit_source.pptx"
        shutil.copy2(source_path, project_source)
        project_source.chmod(0o444)
        plan_path = project_dir / "native_page_kit_plan.json"
        _write_json_atomic(plan_path, {
            "schema": "ppt-master-plus.native-page-kit-plan.v1",
            "brand_id": brand_id,
            "layout_id": layout_id,
            "prototype_source": str(project_source.relative_to(project_dir)),
            "reuse": "web_confirmed_native_prototypes_and_master_layout_shells",
            "roles": roles,
            "overflow_policy": ["condense", "alternate_prototype", "duplicate_and_split", "stop"],
            "content_shell_policy": manifest.get("content_shell_policy"),
        })
        context: dict[str, object] = {}
        if context_path.is_file():
            try:
                loaded = json.loads(context_path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    context = loaded
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Cannot read route context: {context_path}") from exc
        context.update({
            "schema": "ppt-master-plus.route-context.v1",
            "route": "create_pptx_from_template",
            "engine": "edit_native",
            "profile": "template_fill",
            "adaptation": "brand_page_kit",
            "modules": ["page_plan", "content_edit"],
            "template_reuse": "page_kit",
            "template_archetypes_reusable": True,
            "brand_id": brand_id,
            "page_kit_layout_id": layout_id,
            "page_kit_enabled": True,
            "page_kit_plan": str(plan_path.relative_to(project_dir)),
            "template_pptx": str(project_source.relative_to(project_dir)),
            "source_template_immutable": True,
        })
        _write_json_atomic(context_path, context)
        return str(context_path)

    def execute_brand_page_kit(
        self,
        project_path: str,
        roles: list[str] | None,
        output_pptx: str,
        *,
        page_plan_path: str | None = None,
    ) -> str:
        """Clone a confirmed Page Kit roster as the native content-edit carrier.

        Special pages still contain only their confirmed native prototype
        content. Content pages are sanitized Master/Layout shells with one
        empty title slot; ``content_edit`` may add new slide-local body objects
        above that locked shell. It must never modify a Master/Layout object or
        recover any removed source-slide example.
        """
        project_dir = Path(project_path).expanduser().resolve()
        context_path = project_dir / "route_context.json"
        if not context_path.is_file():
            raise FileNotFoundError(f"Route context not found: {context_path}")
        try:
            context = json.loads(context_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Cannot read route context: {context_path}") from exc
        if context.get("engine") != "edit_native" or context.get("profile") != "template_fill":
            raise ValueError("Activate the confirmed Brand Page Kit before native execution")
        plan_ref = context.get("page_kit_plan")
        if not isinstance(plan_ref, str):
            raise RuntimeError("Native Page Kit plan is missing from route context")
        plan_path = project_dir / plan_ref
        try:
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Cannot read native Page Kit plan: {plan_path}") from exc
        source_ref = plan.get("prototype_source")
        prototypes = plan.get("roles")
        if not isinstance(source_ref, str) or not isinstance(prototypes, list):
            raise RuntimeError("Invalid native Page Kit plan")
        source = project_dir / source_ref
        if not source.is_file():
            raise FileNotFoundError(f"Page Kit source package is missing: {source}")
        allowed = {"cover", "toc", "section", "content", "closing"}
        if page_plan_path is None and (
            not roles or any(role not in allowed for role in roles)
        ):
            raise ValueError("--role must use only cover, toc, section, content, or closing")
        by_role: dict[str, list[dict[str, object]]] = {}
        for row in prototypes:
            if not isinstance(row, dict):
                continue
            role = row.get("role")
            source_slide = row.get("source_slide")
            if role in allowed and isinstance(source_slide, int) and row.get("copy_strategy") == "native_roundtrip_clone":
                by_role.setdefault(role, []).append(row)
        selected: list[tuple[dict[str, object], dict[str, object]]] = []
        if page_plan_path is not None:
            plan_path = Path(page_plan_path).expanduser().resolve()
            if not plan_path.is_file():
                raise FileNotFoundError(f"Page Kit page plan not found: {plan_path}")
            try:
                page_plan = json.loads(plan_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Cannot read Page Kit page plan: {plan_path}") from exc
            pages = page_plan.get("pages") if isinstance(page_plan, dict) else None
            if not isinstance(pages, list) or not pages:
                raise ValueError("Page Kit page plan must contain a non-empty pages array")

            used_by_role: dict[str, set[int]] = {}
            for position, page in enumerate(pages, start=1):
                if not isinstance(page, dict):
                    raise ValueError(f"Page Kit page plan item {position} must be an object")
                role = page.get("role")
                source_slide = page.get("source_slide")
                if role not in allowed or not isinstance(source_slide, int):
                    raise ValueError(
                        f"Page Kit page plan item {position} requires role and integer source_slide"
                    )
                candidates = by_role.get(role, [])
                prototype = next(
                    (candidate for candidate in candidates if candidate.get("source_slide") == source_slide),
                    None,
                )
                if prototype is None:
                    raise ValueError(
                        f"Page Kit page plan item {position} selects unapproved "
                        f"{role!r} prototype source_slide={source_slide}"
                    )
                used = used_by_role.setdefault(role, set())
                allow_repeat = page.get("allow_repeat") is True
                if source_slide in used and len(used) < len(candidates) and not allow_repeat:
                    raise ValueError(
                        f"Page Kit page plan repeats {role!r} source_slide={source_slide} "
                        "while another approved prototype is available; choose a different "
                        "source_slide or set allow_repeat: true with an explicit rationale"
                    )
                if allow_repeat and not isinstance(page.get("repeat_rationale"), str):
                    raise ValueError(
                        f"Page Kit page plan item {position} sets allow_repeat but lacks repeat_rationale"
                    )
                used.add(source_slide)
                selected.append((prototype, page))
        else:
            assert roles is not None
            repeated_roles = {role for role in roles if roles.count(role) > 1}
            ambiguous = sorted(
                role for role in repeated_roles if len(by_role.get(role, [])) > 1
            )
            if ambiguous:
                raise ValueError(
                    "Repeated Page Kit roles with multiple approved prototypes require "
                    f"--page-plan; ambiguous roles: {', '.join(ambiguous)}"
                )
            for role in roles:
                candidates = by_role.get(role, [])
                if not candidates:
                    raise ValueError(f"Page Kit has no approved {role!r} prototype")
                selected.append((candidates[0], {"role": role, "source_slide": candidates[0]["source_slide"]}))
        output = Path(output_pptx).expanduser().resolve()
        if output.exists():
            raise FileExistsError(f"Refusing to overwrite native Page Kit output: {output}")
        clone_presentation_slides(
            source,
            tuple(int(prototype["source_slide"]) for prototype, _ in selected),
            output,
        )
        execution_path = output.with_suffix(".native_page_kit_execution.json")
        _write_json_atomic(execution_path, {
            "schema": "ppt-master-plus.native-page-kit-execution.v1",
            "output_pptx": str(output),
            "pages": [
                {
                    "output_slide": index,
                    "role": prototype["role"],
                    "source_slide": prototype["source_slide"],
                    **({"page_id": page["page_id"]} if isinstance(page.get("page_id"), str) else {}),
                    **({"visual_type": page["visual_type"]} if isinstance(page.get("visual_type"), str) else {}),
                    "editable_slots": prototype.get("editable_slots", []),
                    "locked_objects": prototype.get("locked_objects", []),
                    **(
                        {
                            "shell_policy": "master_layout_plus_empty_title",
                            "content_edit_policy": prototype.get("content_edit_policy"),
                        }
                        if prototype.get("role") == "content"
                        else {}
                    ),
                }
                for index, (prototype, page) in enumerate(selected, start=1)
            ],
        })
        context["output_pptx"] = (
            str(output.relative_to(project_dir)) if is_within_path(output, project_dir) else str(output)
        )
        context["native_page_kit_execution"] = (
            str(execution_path.relative_to(project_dir))
            if is_within_path(execution_path, project_dir) else str(execution_path)
        )
        _write_json_atomic(context_path, context)
        return str(execution_path)

    def record_output(self, project_path: str, output_pptx: str) -> str:
        """Record the delivered PPTX without changing the exported package."""
        project_dir = Path(project_path).expanduser().resolve()
        output = Path(output_pptx).expanduser().resolve()
        context_path = project_dir / "route_context.json"
        if not context_path.is_file():
            raise FileNotFoundError(f"Route context not found: {context_path}")
        if not output.is_file() or output.suffix.lower() != ".pptx":
            raise FileNotFoundError(f"Output PPTX not found: {output}")
        context = json.loads(context_path.read_text(encoding="utf-8"))
        context["output_pptx"] = (
            str(output.relative_to(project_dir))
            if is_within_path(output, project_dir)
            else str(output)
        )
        context["output_sha256"] = sha256(output.read_bytes()).hexdigest()
        _write_json_atomic(context_path, context)
        return str(context_path)

    def configure_native(self, project_path: str, modules: list[str]) -> str:
        """Publish the unified Edit Native module contract for a round-trip workspace."""
        project_dir = Path(project_path).expanduser().resolve()
        if not (project_dir / "authoring-svg-flat").is_dir():
            raise FileNotFoundError(
                f"Round-trip workspace not found: {project_dir / 'authoring-svg-flat'}"
            )
        selected = list(dict.fromkeys(modules))
        unknown = sorted(set(selected) - NATIVE_EDIT_MODULES)
        if unknown:
            raise ValueError(f"Unknown native-edit module(s): {', '.join(unknown)}")
        if "visible_content_locked" in selected and {"page_plan", "content_edit"} & set(selected):
            raise ValueError(
                "visible_content_locked cannot be combined with page_plan or content_edit"
            )
        context = {
            "schema": "ppt-master-plus.route-context.v1",
            "route": "edit_native_pptx",
            "engine": "edit_native",
            "profile": None,
            "adaptation": "native_adaptive",
            "modules": selected,
            "template_pptx": None,
            "content_sources": [],
            "output_pptx": None,
        }
        context_path = project_dir / "route_context.json"
        _write_json_atomic(context_path, context)
        return str(context_path)

    def write_native_page_plan(self, project_path: str, page_specs: list[str]) -> str:
        """Write the exporter-native roster after the user confirms its complete order."""
        project_dir = Path(project_path).expanduser().resolve()
        authoring = project_dir / "authoring-svg-flat"
        if not authoring.is_dir():
            raise FileNotFoundError(f"Round-trip authoring directory not found: {authoring}")
        if not page_specs:
            raise ValueError("At least one --page is required")
        pages: list[dict[str, object]] = []
        used_svgs: set[str] = set()
        for raw in page_specs:
            source_text, separator, svg_name = raw.partition(":")
            try:
                source_slide = int(source_text)
            except ValueError as exc:
                raise ValueError(f"Invalid page spec {raw!r}; expected N or N:file.svg") from exc
            if source_slide <= 0:
                raise ValueError(f"Source slide must be positive: {raw}")
            canonical = f"slide_{source_slide:02d}.svg"
            chosen = svg_name if separator else canonical
            if Path(chosen).name != chosen or not chosen.endswith(".svg"):
                raise ValueError(f"Page-plan SVG must be a safe filename: {chosen}")
            if chosen in used_svgs:
                raise ValueError(f"Every output page needs a distinct SVG: {chosen}")
            if not (authoring / chosen).is_file():
                if separator and (authoring / canonical).is_file():
                    shutil.copy2(authoring / canonical, authoring / chosen)
                else:
                    raise FileNotFoundError(f"Authoring SVG not found: {authoring / chosen}")
            used_svgs.add(chosen)
            row: dict[str, object] = {"source_slide": source_slide}
            if separator:
                row["svg"] = chosen
            pages.append(row)
        plan_path = project_dir / "page_plan.json"
        _write_json_atomic(
            plan_path,
            {"schema": "ppt-master.roundtrip-page-plan.v1", "pages": pages},
        )
        return str(plan_path)

    def validate_project(self, project_path: str) -> tuple[bool, list[str], list[str]]:
        project_path_obj = Path(project_path)
        _, errors, warnings = validate_project_structure(
            str(project_path_obj),
            validate_communication=False,
        )

        if project_path_obj.exists() and project_path_obj.is_dir():
            project_info = get_project_info_common(str(project_path_obj))
            artifact_errors, artifact_warnings = validate_project_artifacts(
                project_path_obj,
                project_info,
            )
            errors.extend(artifact_errors)
            warnings.extend(artifact_warnings)

        if project_path_obj.exists() and project_path_obj.is_dir():
            info = get_project_info_common(str(project_path_obj))
            if info.get("svg_files"):
                svg_files = [project_path_obj / "svg_output" / name for name in info["svg_files"]]
                expected_format = info.get("format")
                if expected_format == "unknown":
                    expected_format = None
                warnings.extend(validate_svg_viewbox(svg_files, expected_format))

        return not errors, list(dict.fromkeys(errors)), warnings

    def get_project_info(self, project_path: str) -> dict[str, object]:
        shared = get_project_info_common(project_path)
        canvas_format = (
            "Not encoded in the project directory name"
            if shared.get("format") == "unknown"
            else shared.get("format_name", "Unknown")
        )
        return {
            "name": shared.get("name", Path(project_path).name),
            "path": shared.get("path", str(project_path)),
            "exists": shared.get("exists", False),
            "svg_count": shared.get("svg_count", 0),
            "has_spec": shared.get("has_spec", False),
            "has_source": shared.get("has_source", False),
            "source_count": shared.get("source_count", 0),
            "canvas_format": canvas_format,
            "create_date": shared.get("date_formatted", "Unknown"),
        }


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="PPT Master project management helpers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 scripts/project_manager.py init demo
  python3 scripts/project_manager.py init widescreen --format ppt169
  python3 scripts/project_manager.py import-sources projects/demo file.md
  python3 scripts/project_manager.py import-template projects/demo template.pptx --register-brand example_brand
  python3 scripts/project_manager.py scaffold-spec projects/demo_ppt169_20260718
  python3 scripts/project_manager.py scaffold-lock projects/demo_ppt169_20260718
  python3 scripts/project_manager.py validate projects/demo
  python3 scripts/project_manager.py info projects/demo
  python3 scripts/project_manager.py page-context projects/demo P07 --record-usage
  python3 scripts/project_manager.py page-context-report projects/demo
""",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create a project directory")
    init.add_argument("project_name", help="Project name")
    init.add_argument(
        "--format",
        default=None,
        help="Registered canvas format; omit to determine the canvas during authoring",
    )
    init.add_argument("--dir", default=None, help="Base directory for the project")
    init.add_argument(
        "--quick-generate",
        action="store_true",
        help=(
            "Create svg_output plus the validation workflow audit log and "
            "omit README.md"
        ),
    )

    import_sources = subparsers.add_parser(
        "import-sources",
        help="Import source files or URLs into a project",
    )
    import_sources.add_argument("project_path", help="Project directory")
    import_sources.add_argument("sources", nargs="+", help="Source files, directories, or URLs")
    mode = import_sources.add_mutually_exclusive_group()
    mode.add_argument(
        "--move",
        action="store_true",
        help="Move local sources under projects/; sources elsewhere are copied",
    )
    mode.add_argument("--copy", action="store_true", help="Copy local source files")

    import_template = subparsers.add_parser(
        "import-template",
        help="Import a user-provided .pptx file read-only and analyze it as an identity-only Brand",
    )
    import_template.add_argument("project_path", help="Project directory")
    import_template.add_argument("template_pptx", help="User-provided .pptx file path")
    import_template.add_argument(
        "--replace",
        action="store_true",
        help="Replace a different template already copied into this project",
    )
    import_template.add_argument(
        "--no-previews",
        action="store_true",
        help="Skip template thumbnail rendering",
    )
    import_template.add_argument(
        "--register-brand",
        metavar="BRAND_ID",
        help=(
            "Materialize the imported identity as templates/brands/BRAND_ID; "
            "copies only Master/Layout-referenced brand assets, never page layouts "
            "or visualization examples"
        ),
    )
    import_template.add_argument(
        "--register-icon-layout",
        metavar="LAYOUT_ID",
        help="Materialize detected icon grammar as a neutral shared Layout",
    )
    import_template.add_argument(
        "--register-chart-layout",
        metavar="LAYOUT_ID",
        help="Materialize detected chart visual grammar as a shared Layout without source data",
    )
    import_template.add_argument(
        "--register-page-kit-layout",
        metavar="LAYOUT_ID",
        help=(
            "Materialize only pages confirmed in analysis/brand_import_selection.json; "
            "content pages become Master/Layout + empty-title shells"
        ),
    )

    activate_page_kit = subparsers.add_parser(
        "activate-brand-page-kit",
        help="Read the confirmed Brand Page Kit choice and publish its native round-trip executor contract",
    )
    activate_page_kit.add_argument("project_path", help="Project containing confirm_ui/result.json")

    execute_page_kit = subparsers.add_parser(
        "execute-brand-page-kit",
        help="Clone an approved Page Kit roster into a native PPTX carrier for slot replacement",
    )
    execute_page_kit.add_argument("project_path", help="Project with an activated Page Kit")
    page_kit_source = execute_page_kit.add_mutually_exclusive_group(required=True)
    page_kit_source.add_argument(
        "--role", action="append",
        choices=["cover", "toc", "section", "content", "closing"],
        help="One approved prototype role per output page; repeating an ambiguous role requires --page-plan",
    )
    page_kit_source.add_argument(
        "--page-plan",
        help="JSON page plan selecting an approved role + source_slide for every output page",
    )
    execute_page_kit.add_argument("--output", required=True, help="New PPTX output path; existing files are refused")

    set_output = subparsers.add_parser(
        "set-output",
        help="Record a delivered PPTX in the route context",
    )
    set_output.add_argument("project_path", help="Project directory")
    set_output.add_argument("output_pptx", help="Delivered PPTX path")

    configure_native = subparsers.add_parser(
        "configure-native",
        help="Record enabled modules for an Edit Native round-trip workspace",
    )
    configure_native.add_argument("project_path", help="Round-trip workspace")
    configure_native.add_argument(
        "--module",
        action="append",
        choices=sorted(NATIVE_EDIT_MODULES),
        default=[],
        help="Enable one native-edit module; repeat as needed",
    )

    native_plan = subparsers.add_parser(
        "native-plan",
        help="Write a confirmed round-trip page plan for Edit Native PPTX only",
    )
    native_plan.add_argument("project_path", help="Round-trip workspace")
    native_plan.add_argument(
        "--page",
        action="append",
        required=True,
        help="Output page as source slide N or N:copied-name.svg; repeat in output order",
    )

    scaffold_spec = subparsers.add_parser(
        "scaffold-spec",
        help="Create design_spec.md from the versioned scaffold",
    )
    scaffold_spec.add_argument("project_path", help="Project directory")

    scaffold_lock = subparsers.add_parser(
        "scaffold-lock",
        help="Create spec_lock.md from the versioned scaffold",
    )
    scaffold_lock.add_argument("project_path", help="Project directory")

    validate = subparsers.add_parser("validate", help="Validate a project directory")
    validate.add_argument("project_path", help="Project directory")

    info = subparsers.add_parser("info", help="Print project metadata")
    info.add_argument("project_path", help="Project directory")

    page_context = subparsers.add_parser(
        "page-context",
        help="Print one deterministic per-page execution view",
    )
    page_context.add_argument("project_path", help="Project directory")
    page_context.add_argument("page", help="Positive page key such as P07")
    page_context.add_argument(
        "--bundle",
        action="store_true",
        help="Deprecated compatibility flag; output remains compact",
    )
    page_context.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the page-context JSON payload",
    )
    page_context.add_argument(
        "--record-usage",
        action="store_true",
        help="Write compact-output token telemetry under analysis/page-context/",
    )

    page_context_report = subparsers.add_parser(
        "page-context-report",
        help="Summarize fresh per-page context telemetry",
    )
    page_context_report.add_argument("project_path", help="Project directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    manager = ProjectManager()

    try:
        if args.command == "init":
            project_path = manager.init_project(
                args.project_name,
                args.format,
                base_dir=args.dir,
                quick_generate=args.quick_generate,
            )
            print(f"[OK] Project initialized: {project_path}")
            print("Next:")
            if args.quick_generate:
                print("1. Generate SVG files into svg_output/")
                print("2. Run the Quick Generate final checker and exporter")
                profile = "quick"
            else:
                print("1. Put source files into sources/ (or use import-sources)")
                print("2. Save your design spec to the project root")
                print("3. Generate SVG files into svg_output/")
                profile = "default"
            try:
                canvas_note = (
                    f"; canvas={args.format}"
                    if args.format is not None
                    else ""
                )
                append_note(
                    project_path,
                    f"Project initialized: profile={profile}{canvas_note}; "
                    f"path={project_path}",
                )
            except OSError as exc:
                print(
                    f"[WARN] Workflow audit unavailable: {exc}",
                    file=sys.stderr,
                )
            return 0

        if args.command == "import-sources":
            summary = manager.import_sources(
                args.project_path,
                args.sources,
                move=args.move,
                copy=args.copy,
            )
            import_complete = _has_usable_import(summary)
            if import_complete:
                print(f"[OK] Imported sources into: {args.project_path}")
            else:
                print(
                    f"[ERROR] No usable sources imported into: {args.project_path}",
                    file=sys.stderr,
                )
            if summary["archived"]:
                print("\nArchived originals:")
                for item in summary["archived"]:
                    print(f"  - {item}")
            if summary["url_records"]:
                print("\nArchived URL records:")
                for item in summary["url_records"]:
                    print(f"  - {item}")
            if summary["markdown"]:
                print("\nNormalized markdown:")
                for item in summary["markdown"]:
                    print(f"  - {item}")
            if summary["assets"]:
                print("\nImported asset directories:")
                for item in summary["assets"]:
                    print(f"  - {item}")
            if summary["images"]:
                print("\nRuntime image copies:")
                for item in summary["images"]:
                    print(f"  - {item}")
            if summary["analysis"]:
                print("\nAnalysis artifacts:")
                for item in summary["analysis"]:
                    print(f"  - {item}")
            if summary["notes"]:
                print("\nNotes:")
                for item in summary["notes"]:
                    print(f"  - {item}")
            if summary["skipped"]:
                print("\nSkipped:")
                for item in summary["skipped"]:
                    print(f"  - {item}")
            return 0 if import_complete else 1

        if args.command == "import-template":
            result = manager.import_template(
                args.project_path,
                args.template_pptx,
                replace=args.replace,
                render_previews=not args.no_previews,
                register_brand=args.register_brand,
                register_icon_layout=args.register_icon_layout,
                register_chart_layout=args.register_chart_layout,
                register_page_kit_layout=args.register_page_kit_layout,
            )
            print(f"[OK] Template imported into: {args.project_path}")
            for key, value in result.items():
                print(f"  {key}: {value}")
            return 0

        if args.command == "activate-brand-page-kit":
            context_path = manager.activate_confirmed_brand_page_kit(args.project_path)
            print(f"[OK] Brand Page Kit native executor activated: {context_path}")
            return 0

        if args.command == "execute-brand-page-kit":
            execution_path = manager.execute_brand_page_kit(
                args.project_path, args.role, args.output, page_plan_path=args.page_plan,
            )
            print(f"[OK] Brand Page Kit native carrier created: {execution_path}")
            return 0

        if args.command == "set-output":
            context_path = manager.record_output(args.project_path, args.output_pptx)
            print(f"[OK] Output recorded: {context_path}")
            return 0

        if args.command == "configure-native":
            context_path = manager.configure_native(args.project_path, args.module)
            print(f"[OK] Native modules recorded: {context_path}")
            return 0

        if args.command == "native-plan":
            plan_path = manager.write_native_page_plan(args.project_path, args.page)
            print(f"[OK] Native page plan written: {plan_path}")
            return 0

        if args.command == "scaffold-spec":
            artifact_path = manager.scaffold_artifact(args.project_path, "design_spec")
            print(f"[OK] Design spec scaffold created: {artifact_path}")
            return 0

        if args.command == "scaffold-lock":
            artifact_path = manager.scaffold_artifact(args.project_path, "spec_lock")
            print(f"[OK] Execution lock scaffold created: {artifact_path}")
            return 0

        if args.command == "validate":
            project_path = args.project_path
            is_valid, errors, warnings = manager.validate_project(project_path)

            print(f"\nProject validation: {project_path}")
            print("=" * 60)

            if errors:
                print("\n[ERROR]")
                for error in errors:
                    print(f"  - {error}")

            if warnings:
                print("\n[WARN]")
                for warning in warnings:
                    print(f"  - {warning}")

            if is_valid and not warnings:
                print("\n[OK] Project structure is complete.")
            elif is_valid:
                print("\n[OK] Project structure is valid, with warnings.")
            else:
                print("\n[ERROR] Project structure is invalid.")
                return 1
            return 0

        if args.command == "info":
            project_path = args.project_path
            info = manager.get_project_info(project_path)

            print(f"\nProject info: {info['name']}")
            print("=" * 60)
            print(f"Path: {info['path']}")
            print(f"Exists: {'Yes' if info['exists'] else 'No'}")
            print(f"SVG files: {info['svg_count']}")
            print(f"Design spec: {'Yes' if info['has_spec'] else 'No'}")
            print(f"Source materials: {'Yes' if info['has_source'] else 'No'}")
            print(f"Source count: {info['source_count']}")
            print(f"Canvas format: {info['canvas_format']}")
            print(f"Created: {info['create_date']}")
            return 0

        if args.command == "page-context":
            result = build_page_context(args.project_path, args.page)
            output, measured_reads = render_page_context(
                result,
                bundle=args.bundle,
                pretty=args.pretty,
            )
            if args.record_usage:
                _usage_path, token_status = record_page_context_usage(
                    result,
                    output,
                    measured_reads,
                )
                if token_status != "exact":
                    print(
                        "[WARN] tiktoken/o200k_base unavailable; recorded bytes "
                        "and hashes without token counts",
                        file=sys.stderr,
                    )
            print(output, end="")
            return 0

        if args.command == "page-context-report":
            report = page_context_usage_report(args.project_path)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0

        parser.error(f"Unknown command: {args.command}")
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1
