#!/usr/bin/env python3
"""Dependency-light OPC relationship validator for a PPTX package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import zipfile

import importlib.util

CORE_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "vendor" / "ppt-master" / "scripts"
if str(CORE_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_SCRIPTS_DIR))

_vendor_spec = importlib.util.spec_from_file_location(
    "_vendor_pptx_opc_validation", CORE_SCRIPTS_DIR / "pptx_opc_validation.py"
)
if _vendor_spec and _vendor_spec.loader:
    _vendor_mod = importlib.util.module_from_spec(_vendor_spec)
    _vendor_spec.loader.exec_module(_vendor_mod)
    globals().update({k: v for k, v in _vendor_mod.__dict__.items() if not k.startswith("__")})
else:
    raise ImportError("Failed to load vendor pptx_opc_validation")


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
