#!/usr/bin/env python3
"""
PPT Master - Standalone Animation Quality & Craft Auditor

Audits a project's animation configuration (animations.json) against high-craft
design engineering standards inspired by Emil Kowalski's animation guidelines.

Usage:
    python3 scripts/animation_quality_auditor.py <project_path>
    python3 scripts/animation_quality_auditor.py <project_path> --json
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Try loading animation_config helpers if present
try:
    from svg_to_pptx.animation_config import load_animation_config, scan_project_targets
except ImportError:
    # Fallback import assuming script is run from project root or scripts directory
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from svg_to_pptx.animation_config import load_animation_config, scan_project_targets
    except ImportError:
        load_animation_config = None
        scan_project_targets = None

CHROME_KEYWORDS = (
    'background', 'bg', 'decoration', 'decorations', 'decor',
    'header', 'footer', 'chrome', 'watermark', 'pagenumber', 'pagenum',
    'nav', 'logo', 'rule'
)

class AnimationCraftAuditor:
    """Audits project animation craft and outputs findings in Before/After/Why table format."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.findings: List[Tuple[str, str, str]] = []  # (Before, After, Why)

    def audit(self) -> List[Tuple[str, str, str]]:
        """Run all craft checks and return list of findings."""
        if not self.project_path.exists():
            self.findings.append((
                f"Project path: {self.project_path}",
                "Provide valid project path",
                "Specified project path does not exist."
            ))
            return self.findings

        config_path = self.project_path / "animations.json"
        if not config_path.exists():
            self.findings.append((
                "No animations.json found",
                "Create animations.json sidecar if custom motion is required",
                "Deck uses global default animation settings; sidecar allows fine-grained craft tuning."
            ))
            return self.findings

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            self.findings.append((
                "Invalid animations.json JSON syntax",
                "Fix JSON syntax error",
                f"Failed to parse animations.json: {e}"
            ))
            return self.findings

        self._check_defaults(config.get("defaults", {}))
        self._check_slides(config.get("slides", {}))
        return self.findings

    def _check_defaults(self, defaults: Dict[str, Any]):
        anim_cfg = defaults.get("animation", {})
        if isinstance(anim_cfg, dict):
            dur = anim_cfg.get("duration")
            if dur is not None and isinstance(dur, (int, float)) and dur > 0.5:
                self.findings.append((
                    f"defaults.animation.duration = {dur}s",
                    "defaults.animation.duration = 0.4s (or ≤ 0.3s for snappy UI)",
                    "Default element duration > 0.5s feels sluggish during presentations."
                ))

        trans_cfg = defaults.get("transition", {})
        if isinstance(trans_cfg, dict):
            dur = trans_cfg.get("duration")
            if dur is not None and isinstance(dur, (int, float)) and dur > 0.8:
                self.findings.append((
                    f"defaults.transition.duration = {dur}s",
                    "defaults.transition.duration = 0.4s - 0.6s",
                    "Slide transitions longer than 0.8s drag down presentation rhythm."
                ))

    def _check_slides(self, slides: Dict[str, Any]):
        for slide_name, slide_cfg in slides.items():
            if not isinstance(slide_cfg, dict):
                continue

            # Check for agenda/TOC over-animation
            if "toc" in slide_name.lower() or "agenda" in slide_name.lower():
                anim = slide_cfg.get("animation", {})
                if isinstance(anim, dict) and anim.get("effect") not in (None, "none", "fade"):
                    self.findings.append((
                        f"{slide_name}: animation.effect = '{anim.get('effect')}'",
                        f"{slide_name}: animation.effect = 'fade' or 'none'",
                        "Navigational/TOC slides are seen frequently; complex animations delay reading."
                    ))

            # Check groups overrides
            groups = slide_cfg.get("groups", {})
            if isinstance(groups, dict):
                for group_id, group_cfg in groups.items():
                    if not isinstance(group_cfg, dict):
                        continue

                    # Check chrome animation
                    tokens = [t.lower() for t in group_id.replace('-', '_').split('_')]
                    if any(k in tokens for k in CHROME_KEYWORDS):
                        if group_cfg.get("effect") not in ("none", None):
                            self.findings.append((
                                f"{slide_name}/{group_id}: effect = '{group_cfg.get('effect')}'",
                                f"{slide_name}/{group_id}: effect = 'none'",
                                "Chrome elements (header/footer/bg/pagenum) should remain static to prevent visual distraction."
                            ))

                    # Check excessive duration
                    dur = group_cfg.get("duration")
                    if dur is not None and isinstance(dur, (int, float)) and dur > 0.5:
                        self.findings.append((
                            f"{slide_name}/{group_id}: duration = {dur}s",
                            f"{slide_name}/{group_id}: duration = 0.25s - 0.4s",
                            "Element entrance duration > 0.5s delays content consumption."
                        ))

    def print_report(self):
        """Print the findings in a clean Markdown Before/After/Why table."""
        print(f"## Animation Craft Audit Report for `{self.project_path.name}`\n")
        if not self.findings:
            print("✅ **No animation craft issues found!** All checks adhere to design engineering standards.\n")
            return

        print("| Before (Current) | After (Recommended) | Why (Craft Rationale) |")
        print("| --- | --- | --- |")
        for before, after, why in self.findings:
            print(f"| `{before}` | `{after}` | {why} |")
        print()


def main():
    parser = argparse.ArgumentParser(description="Audit project animation craft.")
    parser.add_argument("project_path", type=str, help="Path to the project directory")
    parser.add_argument("--json", action="store_true", help="Output findings in raw JSON format")
    args = parser.parse_args()

    project_path = Path(args.project_path)
    auditor = AnimationCraftAuditor(project_path)
    findings = auditor.audit()

    if args.json:
        result = [
            {"before": b, "after": a, "why": w}
            for b, a, w in findings
        ]
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        auditor.print_report()


if __name__ == "__main__":
    main()
