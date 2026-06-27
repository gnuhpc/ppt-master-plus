from pathlib import Path
import re
import unittest


OLD_UPSTREAM_SKILL = "ppt" + "-master"
OLD_GATED_SKILL = "article" + "-to-pptx-gated"


def skills_root() -> Path:
    candidates = [Path.cwd(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / OLD_UPSTREAM_SKILL).exists() or (candidate / "ppt-master-plus").exists():
            return candidate
    raise RuntimeError("skills workspace root not found")


ROOT = skills_root()
SKILL = ROOT / "ppt-master-plus"


class PptMasterPlusContractTests(unittest.TestCase):
    def test_only_new_skill_directory_remains(self):
        self.assertTrue(SKILL.is_dir())
        self.assertFalse((ROOT / OLD_UPSTREAM_SKILL).exists())
        self.assertFalse((ROOT / OLD_GATED_SKILL).exists())

    def test_public_name_and_mode_selection_are_declared(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name: ppt-master-plus$")
        self.assertIn("workflows/gated-production.md", text)
        self.assertLess(text.index("逐页确定精修"), text.index("全自动一次性生成"))
        self.assertIn("gated", text.lower())
        self.assertIn("continuous", text.lower())

    def test_gated_workflow_contains_all_required_review_stops(self):
        text = (SKILL / "workflows/gated-production.md").read_text(encoding="utf-8")
        self.assertLess(text.index("逐页确定精修"), text.index("全自动一次性生成"))
        for marker in (
            "Intake Gate",
            "Narrative Analysis Gate",
            "Outline Gate",
            "Production Route Gate",
            "Per-slide Gate",
            "Final Acceptance Gate",
        ):
            self.assertIn(marker, text)
        self.assertIn("check_speaker_notes.py", text)

    def test_optional_diagram_routes_are_non_blocking(self):
        text = (SKILL / "references/diagram-routing.md").read_text(encoding="utf-8")
        self.assertIn("fireworks-tech-graph", text)
        self.assertIn("excalidraw", text)
        self.assertIn("built-in SVG", text)
        self.assertRegex(text, r"(?i)do not (install|block)")

    def test_user_provided_template_fill_is_not_public(self):
        removed_workflow = "template" + "-fill-pptx.md"
        removed_cli = "template" + "_fill_pptx.py"
        self.assertFalse((SKILL / "workflows" / removed_workflow).exists())
        self.assertFalse((SKILL / "scripts" / removed_cli).exists())

        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("No user-provided template-fill route", skill_text)
        self.assertIn("External template paths", skill_text)

        public_files = [
            SKILL / "SKILL.md",
            SKILL / "README.md",
            SKILL / "scripts" / "README.md",
            SKILL / "workflows" / "gated-production.md",
            SKILL / "workflows" / "native-enhance-pptx.md",
            SKILL / "workflows" / "native-narration-pptx.md",
        ]
        forbidden = re.compile(
            rf"`?{re.escape(removed_workflow)}`?|"
            rf"`?{re.escape(removed_cli)}`?|"
            r"native PPTX template deck|"
            r"reuse this deck's design",
            re.IGNORECASE,
        )
        offenders = [
            str(path.relative_to(ROOT))
            for path in public_files
            if path.exists() and forbidden.search(path.read_text(encoding="utf-8"))
        ]
        self.assertEqual([], offenders)

    def test_live_preview_annotation_prompt_is_copyable(self):
        app_js = (SKILL / "scripts/svg_editor/static/app.js").read_text(encoding="utf-8")
        index_html = (SKILL / "scripts/svg_editor/static/index.html").read_text(encoding="utf-8")
        server_py = (SKILL / "scripts/svg_editor/server.py").read_text(encoding="utf-8")
        workflow = (SKILL / "workflows/live-preview.md").read_text(encoding="utf-8")

        self.assertIn("modal-prompt-text", index_html)
        self.assertIn("apply_annotation_prompt", app_js)
        self.assertIn("copyTextToClipboard", app_js)
        self.assertIn("annotation_files", server_py)
        self.assertIn("MUST remove the annotation markers", app_js)
        self.assertIn("必须移除标注标记", app_js)
        self.assertIn("Never leave already-fixed annotations", workflow)
        self.assertIn("page number", workflow.lower())
        self.assertIn("svg_output", app_js)

    def test_new_user_config_precedes_legacy_fallback(self):
        text = (SKILL / "scripts/config.py").read_text(encoding="utf-8")
        new_pos = text.index(".ppt-master-plus")
        old_pos = text.index("'.ppt-master'")
        self.assertLess(new_pos, old_pos)

    def test_destructive_upstream_updater_is_removed(self):
        self.assertFalse((SKILL / "scripts/update_repo.py").exists())
        provenance = (SKILL / "references/upstream.md").read_text(encoding="utf-8")
        self.assertIn("12f74bf11086f6b751bd9689f6642aa7c79d6f3c", provenance)
        self.assertRegex(provenance, r"(?i)manual")

    def test_agent_metadata_uses_new_skill_name(self):
        text = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("PPT Master Plus", text)
        self.assertIn("$ppt-master-plus", text)

    def test_no_old_skill_name_references_remain_outside_provenance(self):
        old_names = re.compile(
            rf"\b{re.escape(OLD_GATED_SKILL)}\b|"
            rf"skills/{re.escape(OLD_UPSTREAM_SKILL)}(?!-plus)(?:/|\b)"
        )
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            if path == SKILL / "references/upstream.md":
                continue
            if path.suffix not in {".md", ".py", ".yaml", ".yml", ".json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if old_names.search(text):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
