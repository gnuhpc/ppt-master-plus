from pathlib import Path
import base64
import re
import sys
import tempfile
import unittest
import zipfile


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

    def test_gated_per_slide_approval_uses_live_preview_not_png_model_review(self):
        gated = (SKILL / "workflows/gated-production.md").read_text(encoding="utf-8")
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        visual_review = (SKILL / "workflows/visual-review.md").read_text(encoding="utf-8")

        self.assertIn("per-slide style confirmation uses Live Preview directly", gated)
        self.assertIn("Do not render a PNG/screenshot", gated)
        self.assertIn("per-slide style approval surface is Live Preview itself", skill_text)
        self.assertIn("do not render PNGs/screenshots", skill_text)
        self.assertIn("use Live Preview directly", visual_review)
        self.assertIn("do not render PNGs", visual_review)

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

    def test_beautify_preserve_master_contract_is_declared(self):
        workflow = (SKILL / "workflows" / "beautify-pptx.md").read_text(encoding="utf-8")
        confirm_docs = (SKILL / "scripts" / "docs" / "confirm_ui.md").read_text(encoding="utf-8")
        app_js = (SKILL / "scripts" / "confirm_ui" / "static" / "app.js").read_text(encoding="utf-8")
        cli = (SKILL / "scripts" / "svg_to_pptx" / "pptx_cli.py").read_text(encoding="utf-8")
        builder = (SKILL / "scripts" / "svg_to_pptx" / "pptx_builder.py").read_text(encoding="utf-8")

        for text in (workflow, confirm_docs, app_js):
            self.assertIn("preserve_master", text)
        self.assertIn("--base-pptx", workflow)
        self.assertIn("--base-pptx", cli)
        self.assertIn("source slide N", builder)

    def test_base_pptx_export_preserves_per_slide_layout_mapping_and_master_media(self):
        scripts_dir = SKILL / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))

        from pptx import Presentation
        from svg_to_pptx.pptx_builder import create_pptx_with_native_svg

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            base = tmp_path / "base.pptx"
            prs = Presentation()
            prs.slides.add_slide(prs.slide_layouts[0])
            prs.slides.add_slide(prs.slide_layouts[1])
            prs.save(base)

            # Add a master-level image relationship to prove the source package's
            # master/layout media and rels survive the base-pptx export path.
            patched_base = tmp_path / "base_with_master_media.pptx"
            tiny_png = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
                "AAAADUlEQVR42mP8z8BQDwAFgwJ/lw9J7wAAAABJRU5ErkJggg=="
            )
            with zipfile.ZipFile(base, "r") as zin, zipfile.ZipFile(patched_base, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == "ppt/slideMasters/_rels/slideMaster1.xml.rels":
                        rel = (
                            '  <Relationship Id="rIdPreserveMasterBg" '
                            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                            'Target="../media/master_bg.png"/>'
                        )
                        data = data.replace(b"</Relationships>", rel.encode("utf-8") + b"\n</Relationships>")
                    zout.writestr(item, data)
                zout.writestr("ppt/media/master_bg.png", tiny_png)

            def layout_targets(pptx_path: Path) -> list[str]:
                targets = []
                with zipfile.ZipFile(pptx_path, "r") as zf:
                    for idx in (1, 2):
                        rels = zf.read(f"ppt/slides/_rels/slide{idx}.xml.rels").decode("utf-8")
                        match = re.search(r'Type="[^"]+/slideLayout" Target="([^"]+)"', rels)
                        self.assertIsNotNone(match)
                        targets.append(match.group(1))
                return targets

            source_targets = layout_targets(patched_base)
            self.assertNotEqual(source_targets[0], source_targets[1])

            svg_files = []
            for idx in (1, 2):
                svg = tmp_path / f"slide_{idx}.svg"
                svg.write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
                    f'<text x="80" y="{100 + idx * 40}" font-size="36" fill="#111111">Slide {idx}</text>'
                    '</svg>',
                    encoding="utf-8",
                )
                svg_files.append(svg)

            output = tmp_path / "out.pptx"
            ok = create_pptx_with_native_svg(
                svg_files=svg_files,
                output_path=output,
                canvas_format="ppt169",
                verbose=False,
                use_native_shapes=True,
                base_pptx=patched_base,
            )
            self.assertTrue(ok)
            self.assertEqual(source_targets, layout_targets(output))
            with zipfile.ZipFile(output, "r") as zf:
                names = set(zf.namelist())
                self.assertIn("ppt/slideMasters/slideMaster1.xml", names)
                self.assertIn("ppt/media/master_bg.png", names)
                master_rels = zf.read("ppt/slideMasters/_rels/slideMaster1.xml.rels").decode("utf-8")
                self.assertIn("master_bg.png", master_rels)

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
