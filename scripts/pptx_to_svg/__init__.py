"""PPTX -> SVG semantic converter (reverse of svg_to_pptx).

Reads OOXML (DrawingML) directly from a .pptx zip archive and emits SVG with
shape-level fidelity: <p:sp prst="rect"> -> <rect>, <p:txBody> -> <text>, etc.

Public entry: convert_pptx_to_svg().
"""

from __future__ import annotations

from pathlib import Path

from .converter import convert_pptx_to_svg

_vendor_path = Path(__file__).resolve().parents[2] / "vendor" / "ppt-master" / "scripts" / "pptx_to_svg"
if _vendor_path.is_dir() and str(_vendor_path) not in __path__:
    __path__.append(str(_vendor_path))

__all__ = ["convert_pptx_to_svg"]
