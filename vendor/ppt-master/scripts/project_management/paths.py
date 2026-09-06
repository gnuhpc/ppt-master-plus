#!/usr/bin/env python3
"""
PPT Master - Project Management Paths

Own the repository and Skill resource roots used by project-management modules.

Usage:
    Import the required path constants from project_management.paths.

Examples:
    from project_management.paths import PROJECTS_ROOT, SCHEMA_DIR

Dependencies:
    None (only uses the standard library)
"""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = PACKAGE_DIR.parent
SKILL_DIR = SCRIPTS_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent
PROJECTS_ROOT = REPO_ROOT / "projects"
SOURCE_TO_MD_DIR = SCRIPTS_DIR / "source_to_md"
CHARTS_DIR = SKILL_DIR / "templates" / "charts"
# The vendored engine deliberately consumes ppt-master-plus planning artifacts.
# Upstream's standalone `templates/schemas` directory is not vendored, so use
# the host skill's canonical schema directory when the upstream location is
# absent. Keep the upstream path first for a complete standalone checkout.
_HOST_SKILL_DIR = PACKAGE_DIR.parents[3]
SCHEMA_DIR = SKILL_DIR / "templates" / "schemas"
if not SCHEMA_DIR.is_dir():
    SCHEMA_DIR = _HOST_SKILL_DIR / "templates" / "schemas"
SCAFFOLD_DIR = SKILL_DIR / "templates" / "scaffolds"
