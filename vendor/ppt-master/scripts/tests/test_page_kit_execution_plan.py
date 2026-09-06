#!/usr/bin/env python3
"""Regression coverage for Page Kit per-page prototype selection."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from project_management.cli import ProjectManager  # noqa: E402


def _write_project(root: Path) -> Path:
    project = root / "project"
    (project / "template").mkdir(parents=True)
    (project / "template" / "page_kit_source.pptx").write_bytes(b"placeholder")
    (project / "route_context.json").write_text(json.dumps({
        "engine": "edit_native",
        "profile": "template_fill",
        "page_kit_plan": "native_page_kit_plan.json",
    }), encoding="utf-8")
    (project / "native_page_kit_plan.json").write_text(json.dumps({
        "prototype_source": "template/page_kit_source.pptx",
        "roles": [
            {"role": "cover", "source_slide": 1, "copy_strategy": "native_roundtrip_clone", "editable_slots": [1], "locked_objects": [2]},
            {"role": "content", "source_slide": 7, "copy_strategy": "native_roundtrip_clone", "editable_slots": [3], "locked_objects": [4]},
            {"role": "content", "source_slide": 8, "copy_strategy": "native_roundtrip_clone", "editable_slots": [5], "locked_objects": [6]},
        ],
    }), encoding="utf-8")
    return project


class PageKitExecutionPlanTests(unittest.TestCase):
    def _clone(self, _source: Path, _slides: tuple[int, ...], output: Path) -> None:
        output.write_bytes(b"pptx")

    def test_page_plan_uses_the_selected_prototypes_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = _write_project(Path(directory))
            plan = project / "page_kit_execution_plan.json"
            plan.write_text(json.dumps({"pages": [
                {"page_id": "P01", "role": "cover", "source_slide": 1},
                {"page_id": "P02", "role": "content", "source_slide": 8, "visual_type": "pipeline"},
                {"page_id": "P03", "role": "content", "source_slide": 7, "visual_type": "icon_grid"},
            ]}), encoding="utf-8")
            output = project / "output.pptx"
            with patch("project_management.cli.clone_presentation_slides", self._clone):
                roster_path = ProjectManager().execute_brand_page_kit(
                    str(project), None, str(output), page_plan_path=str(plan),
                )
            roster = json.loads(Path(roster_path).read_text(encoding="utf-8"))
            self.assertEqual(
                [(row["page_id"], row["source_slide"]) for row in roster["pages"]],
                [("P01", 1), ("P02", 8), ("P03", 7)],
            )
            self.assertEqual(roster["pages"][1]["visual_type"], "pipeline")

    def test_repeated_role_requires_a_page_plan_when_prototypes_are_ambiguous(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = _write_project(Path(directory))
            with self.assertRaisesRegex(ValueError, "require --page-plan"):
                ProjectManager().execute_brand_page_kit(
                    str(project), ["content", "content"], str(project / "output.pptx"),
                )

    def test_unexplained_repeat_is_rejected_when_another_prototype_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = _write_project(Path(directory))
            plan = project / "page_kit_execution_plan.json"
            plan.write_text(json.dumps({"pages": [
                {"role": "content", "source_slide": 7},
                {"role": "content", "source_slide": 7},
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "another approved prototype"):
                ProjectManager().execute_brand_page_kit(
                    str(project), None, str(project / "output.pptx"), page_plan_path=str(plan),
                )


if __name__ == "__main__":
    unittest.main()
