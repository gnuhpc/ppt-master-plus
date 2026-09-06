#!/usr/bin/env python3
"""Import a user-authorized PPTX as a Brand plus a confirmed native Page Kit.

The import is standalone: its temporary workspace exists only to render the
source and collect the user's page-role confirmation. The resulting Brand keeps
identity tokens; its linked Page Kit stores only approved special-page
prototypes and strictly sanitized content Master/Layout shells.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
CORE_SCRIPTS = SKILL_DIR / "vendor" / "ppt-master" / "scripts"
if str(CORE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(CORE_SCRIPTS))

from project_management.cli import ProjectManager, _brand_id  # noqa: E402


def _index_bytes() -> dict[Path, bytes]:
    """Snapshot the only indexes this transaction may modify."""
    paths = (
        SKILL_DIR / "templates" / "brands" / "brands_index.json",
        SKILL_DIR / "templates" / "layouts" / "layouts_index.json",
    )
    return {path: path.read_bytes() if path.exists() else b"" for path in paths}


def _restore_indexes(snapshot: dict[Path, bytes]) -> None:
    for path, content in snapshot.items():
        if content:
            path.write_bytes(content)
        elif path.exists():
            path.unlink()


def _linked_page_kit_id(brand_id: str) -> str | None:
    index_path = SKILL_DIR / "templates" / "brands" / "brands_index.json"
    try:
        brands = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read Brand index: {index_path}: {exc}") from exc
    entry = brands.get(brand_id)
    if not isinstance(entry, dict):
        return None
    value = entry.get("page_kit_layout_id")
    return value if isinstance(value, str) and value else None


def _move_if_exists(source: Path, backup_root: Path) -> Path | None:
    if not source.exists():
        return None
    target = backup_root / source.name
    shutil.move(str(source), str(target))
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Register a user-provided .pptx as a Brand and a user-confirmed "
            "native Page Kit without creating a presentation project."
        )
    )
    parser.add_argument("template_pptx", help="User-provided .pptx file")
    parser.add_argument("--brand-id", required=True, help="Brand identifier")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Safely replace an existing Brand and its linked Page Kit after confirmation",
    )
    parser.add_argument(
        "--keep-analysis",
        action="store_true",
        help="Keep intake facts beside the Brand under .import-analysis/",
    )
    args = parser.parse_args()

    source = Path(args.template_pptx).expanduser().resolve()
    if not source.is_file() or source.suffix.lower() != ".pptx":
        parser.error(f"template_pptx must be an existing .pptx file: {source}")
    brand_id = _brand_id(args.brand_id)
    brand_dir = SKILL_DIR / "templates" / "brands" / brand_id
    existing_page_kit = _linked_page_kit_id(brand_id) if brand_dir.exists() else None
    page_kit_id = existing_page_kit or f"{brand_id}_page_kit"
    page_kit_dir = SKILL_DIR / "templates" / "layouts" / page_kit_id
    if (brand_dir.exists() or page_kit_dir.exists()) and not args.replace:
        parser.error(
            "Brand or Page Kit already exists; use --replace to rebuild it after "
            "a new page-role confirmation"
        )

    staging = Path(tempfile.mkdtemp(prefix=f"ppt-master-plus-brand-{brand_id}-"))
    staging_project = staging / "page-kit-review"
    analysis = staging_project / "analysis"
    backup_root = staging / "previous-assets"
    old_brand: Path | None = None
    old_page_kit: Path | None = None
    indexes = _index_bytes()
    materialized = False
    asset_transaction_started = False
    try:
        template_dir = staging_project / "template"
        template_dir.mkdir(parents=True)
        intake_source = template_dir / "source.pptx"
        shutil.copy2(source, intake_source)
        subprocess.run(
            [
                sys.executable,
                str(SKILL_DIR / "scripts" / "pptx_intake.py"),
                str(intake_source),
                "-o",
                str(analysis),
                "--intent",
                "template",
            ],
            cwd=SKILL_DIR,
            check=True,
        )
        print("[ACTION REQUIRED] Select cover, TOC, section, content Master/Layout, and closing pages in Brand Import Web.")
        subprocess.run(
            [sys.executable, str(SKILL_DIR / "scripts" / "brand_import_ui" / "server.py"), str(staging_project)],
            cwd=SKILL_DIR,
            check=True,
        )

        # No global asset changes happen until the selection is confirmed.
        backup_root.mkdir()
        asset_transaction_started = True
        if args.replace:
            old_brand = _move_if_exists(brand_dir, backup_root)
            old_page_kit = _move_if_exists(page_kit_dir, backup_root)

        manager = ProjectManager()
        page_kit = manager._materialize_imported_page_kit_layout(
            source=source,
            analysis_dir=analysis,
            layout_id=page_kit_id,
        )
        brand = manager._materialize_imported_brand(
            source=source,
            analysis_dir=analysis,
            brand_id=brand_id,
            page_kit_layout_id=page_kit["layout_id"],
        )
        if args.keep_analysis:
            shutil.copytree(analysis, brand_dir / ".import-analysis")
        subprocess.run(
            [sys.executable, str(SKILL_DIR / "scripts" / "register_template.py"), page_kit["layout_id"], "--kind", "layout"],
            cwd=SKILL_DIR,
            check=True,
        )
        subprocess.run(
            [sys.executable, str(SKILL_DIR / "scripts" / "register_template.py"), brand["brand_id"], "--kind", "brand"],
            cwd=SKILL_DIR,
            check=True,
        )
        materialized = True
    except Exception:
        if asset_transaction_started:
            if brand_dir.exists():
                shutil.rmtree(brand_dir)
            if page_kit_dir.exists():
                shutil.rmtree(page_kit_dir)
        if old_brand is not None:
            shutil.move(str(old_brand), str(brand_dir))
        if old_page_kit is not None:
            shutil.move(str(old_page_kit), str(page_kit_dir))
        _restore_indexes(indexes)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)

    print("[OK] Brand imported with a confirmed native Page Kit")
    print(f"  brand_id: {brand_id}")
    print(f"  brand_path: {brand_dir}")
    print(f"  page_kit_layout_id: {page_kit_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
