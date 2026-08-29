#!/usr/bin/env python3
"""PPT Master Plus unified project-management entrypoint."""

import runpy
import sys
from pathlib import Path

if "--quick-generate" in sys.argv[1:]:
    raise SystemExit("PPT Master Plus does not expose Quick Generate.")

_CORE = Path(__file__).resolve().parents[1] / "vendor" / "ppt-master" / "scripts"
sys.path.insert(0, str(_CORE))
runpy.run_path(str(_CORE / "project_manager.py"), run_name="__main__")
