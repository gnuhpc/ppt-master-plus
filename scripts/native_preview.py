#!/usr/bin/env python3
"""Connect round-trip authoring SVGs to the frozen Plus Live Preview UI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def _paths(project: Path) -> tuple[Path, Path]:
    return project / "authoring-svg-flat", project / "svg_output"


def prepare(project: Path) -> dict[str, str]:
    project = project.expanduser().resolve()
    authoring, preview = _paths(project)
    if not authoring.is_dir():
        raise FileNotFoundError(
            f"Round-trip authoring directory not found: {authoring}; run "
            "svg_authoring_view.py with --projection-kind flat first"
        )
    if preview.is_symlink():
        if preview.resolve() != authoring:
            raise RuntimeError(f"svg_output points to a different directory: {preview}")
    elif preview.is_dir() and not any(preview.iterdir()):
        preview.rmdir()
        preview.symlink_to(authoring.name, target_is_directory=True)
    elif preview.exists():
        raise RuntimeError(
            f"Refusing to replace non-empty Generate workspace: {preview}; "
            "use a dedicated native-edit project directory"
        )
    else:
        preview.symlink_to(authoring.name, target_is_directory=True)
    return {"project": str(project), "authoring": str(authoring), "preview": str(preview)}


def clean(project: Path) -> dict[str, str]:
    project = project.expanduser().resolve()
    authoring, preview = _paths(project)
    if preview.is_symlink() and preview.resolve() == authoring:
        preview.unlink()
        status = "removed"
    elif preview.exists():
        status = "preserved_non_adapter_path"
    else:
        status = "absent"
    return {"project": str(project), "status": status}


def status(project: Path) -> dict[str, object]:
    project = project.expanduser().resolve()
    authoring, preview = _paths(project)
    return {
        "project": str(project),
        "authoring_exists": authoring.is_dir(),
        "adapter_active": preview.is_symlink() and preview.resolve() == authoring,
        "slide_count": len(list(authoring.glob("*.svg"))) if authoring.is_dir() else 0,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "status", "clean", "start"))
    parser.add_argument("project", help="Dedicated Edit Native project directory")
    parser.add_argument("--port", type=int, default=5173, help="Live Preview port")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project = Path(args.project)
    try:
        if args.command == "prepare":
            result = prepare(project)
        elif args.command == "clean":
            result = clean(project)
        elif args.command == "status":
            result = status(project)
        else:
            result = prepare(project)
            server = Path(__file__).resolve().parent / "svg_editor" / "server.py"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(server),
                    str(project.expanduser().resolve()),
                    "--live",
                    "--daemon",
                    "--port",
                    str(args.port),
                ],
                check=False,
            )
            return completed.returncode
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
