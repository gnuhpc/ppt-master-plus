#!/usr/bin/env python3
"""PPT Master Plus soundtrack and narration synchronization utility."""

import runpy
import sys
from pathlib import Path

_CORE = Path(__file__).resolve().parents[1] / "vendor" / "ppt-master" / "scripts"
sys.path.insert(0, str(_CORE))
runpy.run_path(str(_CORE / "sound_sync.py"), run_name="__main__")
