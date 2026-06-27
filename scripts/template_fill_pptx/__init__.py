"""Internal PPTX intake primitives.

The public user-provided template-fill workflow has been removed. This package
is retained only because `pptx_intake.py` imports `analyze_pptx()` to extract
slide geometry, text, table, and chart facts from PPTX source material.
"""

from __future__ import annotations

from .analyzer import analyze_pptx

__all__ = ["analyze_pptx"]
