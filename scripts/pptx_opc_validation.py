#!/usr/bin/env python3
"""Dependency-light OPC relationship validator for a PPTX package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import zipfile

CORE_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "vendor" / "ppt-master" / "scripts"

sys.path.insert(0, str(CORE_SCRIPTS_DIR))
from pptx_opc_validation import verify_internal_relationships  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate internal OPC relationships in a PPTX package."
    )
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.pptx.is_file() or not zipfile.is_zipfile(args.pptx):
        parser.error(f"not a readable PPTX ZIP package: {args.pptx}")
    with tempfile.TemporaryDirectory(prefix="pptx-opc-") as tmp:
        with zipfile.ZipFile(args.pptx) as archive:
            archive.extractall(tmp)
        problems = verify_internal_relationships(Path(tmp))
    if args.as_json:
        print(json.dumps({"ok": not problems, "problems": problems}, ensure_ascii=False, indent=2))
    elif problems:
        for problem in problems:
            print(problem)
    else:
        print("OPC relationships: OK")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
