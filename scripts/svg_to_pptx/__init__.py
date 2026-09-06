"""svg_to_pptx — SVG to PPTX conversion package.

Public API:
    - main(): CLI entry point
    - convert_svg_to_slide_shapes(): SVG -> DrawingML slide XML
    - create_pptx_with_native_svg(): Build PPTX from SVG files
"""

from .pptx_cli import main
from .drawingml_converter import convert_svg_to_slide_shapes
from .pptx_builder import create_pptx_with_native_svg

from pathlib import Path

_vendor_path = Path(__file__).resolve().parents[2] / "vendor" / "ppt-master" / "scripts" / "svg_to_pptx"
if _vendor_path.is_dir() and str(_vendor_path) not in __path__:
    __path__.append(str(_vendor_path))

__all__ = [
    'main',
    'convert_svg_to_slide_shapes',
    'create_pptx_with_native_svg',
]
