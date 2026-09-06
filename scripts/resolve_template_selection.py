#!/usr/bin/env python3
"""Resolve an optional Pack plus explicit template component overrides.

Pack is a discovery/provenance asset. This resolver expands it into Brand,
Style, and Layout IDs, applies explicit same-kind overrides, validates every
result against the four indexes, and emits the stable Stage-1 receipt fragment.
It never installs assets or merges design fields.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
BASE_KINDS = ("brand", "style", "layout")


class SelectionError(RuntimeError):
    """Raised when a template selection cannot be resolved safely."""


def _index_path(kind: str) -> Path:
    plural = {"brand": "brands", "style": "styles", "layout": "layouts", "pack": "packs"}[kind]
    return TEMPLATES_DIR / plural / f"{plural}_index.json"


def _load_index(kind: str) -> dict:
    path = _index_path(kind)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SelectionError(f"cannot read {kind} index: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SelectionError(f"{kind} index must be a JSON object: {path}")
    return data


def resolve_selection(
    *,
    pack_id: str | None = None,
    brand_id: str | None = None,
    style_id: str | None = None,
    layout_id: str | None = None,
) -> dict:
    """Return Pack provenance and the final resolved base components."""
    explicit = {
        "brand_id": brand_id,
        "style_id": style_id,
        "layout_id": layout_id,
    }
    resolved = {key: None for key in explicit}

    if pack_id:
        packs = _load_index("pack")
        pack = packs.get(pack_id)
        if not isinstance(pack, dict):
            raise SelectionError(f"unknown pack_id: {pack_id}")
        for key in resolved:
            value = pack.get(key)
            if value is not None and not isinstance(value, str):
                raise SelectionError(f"Pack {pack_id} has invalid {key}")
            resolved[key] = value
        if sum(value is not None for value in resolved.values()) < 2:
            raise SelectionError(f"Pack {pack_id} must reference at least two base kinds")

    for key, value in explicit.items():
        if value:
            resolved[key] = value

    if not pack_id and not any(resolved.values()):
        raise SelectionError("select one Pack or at least one Brand, Style, or Layout")

    for kind in BASE_KINDS:
        key = f"{kind}_id"
        value = resolved[key]
        if value is not None and value not in _load_index(kind):
            raise SelectionError(f"unknown {key}: {value}")

    return {
        "schema_version": 2,
        "selected_pack_id": pack_id,
        "resolved": resolved,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Expand one Pack and apply explicit Brand/Style/Layout overrides."
    )
    parser.add_argument("--pack", dest="pack_id")
    parser.add_argument("--brand", dest="brand_id")
    parser.add_argument("--style", dest="style_id")
    parser.add_argument("--layout", dest="layout_id")
    parser.add_argument("-o", "--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        receipt = resolve_selection(
            pack_id=args.pack_id,
            brand_id=args.brand_id,
            style_id=args.style_id,
            layout_id=args.layout_id,
        )
    except SelectionError as exc:
        raise SystemExit(f"error: {exc}") from exc

    rendered = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
