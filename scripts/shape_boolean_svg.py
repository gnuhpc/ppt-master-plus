#!/usr/bin/env python3
"""PPT Master Plus SVG shape boolean-operation entrypoint."""

import runpy
import sys
from pathlib import Path

_CORE = Path(__file__).resolve().parents[1] / "vendor" / "ppt-master" / "scripts"
sys.path.insert(0, str(_CORE))
runpy.run_path(str(_CORE / "shape_boolean_svg.py"), run_name="__main__")
