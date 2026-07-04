#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
uupm_advisor.py - Integrates ui-ux-pro-max design intelligence into ppt-master-plus.
Generates recommendations.json for Confirm UI or directly applies style/colors/fonts to spec_lock.md.

Usage:
  python3 uupm_advisor.py <project_path> "<query>" [--apply] [--dark]
"""

import sys
import os
import argparse
import json
from pathlib import Path

def find_uupm(project_path: Path) -> Path | None:
    # Walk up from project_path to look for .agents/skills/ui-ux-pro-max
    curr = project_path.resolve()
    for _ in range(5):
        workspace_path = curr / ".agents" / "skills" / "ui-ux-pro-max"
        if workspace_path.exists() and (workspace_path / "scripts" / "core.py").exists():
            return workspace_path
        if curr.parent == curr:
            break
        curr = curr.parent
        
    # Check global configurations
    global_path = Path("/Users/gnuhpc/.gemini/skills/ui-ux-pro-max")
    if global_path.exists() and (global_path / "scripts" / "core.py").exists():
        return global_path
        
    return None

def main() -> int:
    parser = argparse.ArgumentParser(description="UI/UX Pro Max Advisor for PPT Master Plus")
    parser.add_argument("project_path", help="Path to the PPT Master project directory")
    parser.add_argument("query", help="Visual style, topic or keywords query")
    parser.add_argument("--apply", action="store_true", help="Write changes directly to spec_lock.md and update SVGs")
    parser.add_argument("--dark", action="store_true", help="Request dark theme/mode recommendations")
    
    args = parser.parse_args()
    project_path = Path(args.project_path)
    
    if not project_path.is_dir():
        print(f"Error: Project path '{project_path}' does not exist.", file=sys.stderr)
        return 1
        
    uupm_dir = find_uupm(project_path)
    if not uupm_dir:
        print("Error: ui-ux-pro-max skill was not found in the workspace or global path.", file=sys.stderr)
        print("Please install it first: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill", file=sys.stderr)
        return 1
        
    # Import uupm core search
    sys.path.append(str(uupm_dir / "scripts"))
    try:
        from core import search
    except ImportError as e:
        print(f"Error importing ui-ux-pro-max search: {e}", file=sys.stderr)
        return 1

    print(f"Querying ui-ux-pro-max for: '{args.query}'...")
    
    # 1. Search style
    style_res = search(args.query, "style", 3)
    # 2. Search colors
    color_res = search(args.query, "color", 3)
    # 3. Search typography
    type_res = search(args.query, "typography", 3)
    
    # Defaults in case database has no matches
    visual_style = "swiss-minimal"
    icons_lib = "tabler-outline"
    
    if style_res and style_res.get("results"):
        visual_style = style_res["results"][0].get("Style Category", "swiss-minimal").lower().replace(" ", "-")
        
    # Build color candidates
    color_candidates = []
    if color_res and color_res.get("results"):
        for i, row in enumerate(color_res["results"]):
            bg = row.get("Background", "#FFFFFF")
            card = row.get("Card", "#F8FAFC")
            primary = row.get("Primary", "#1A3A6B")
            accent = row.get("Accent", "#E8A317")
            sec_accent = row.get("Secondary", "#4A7BB5")
            body_text = row.get("Foreground", "#1D2430")
            
            # If dark mode is requested, adjust colors if we got a light candidate
            if args.dark and bg.upper() in ["#FFFFFF", "#F8FAFC", "#FDFBF7", "#FAFAF8"]:
                # Use deep chalkboard dark green or charcoal instead
                bg = "#1E2B22"
                card = "#273A2E"
                primary = "#F8FAFC"
                accent = "#F87171"
                sec_accent = "#34D399"
                body_text = "#F8FAFC"
                
            color_candidates.append({
                "name": row.get("Product Type", f"Palette {i+1}"),
                "note": row.get("Notes", "Design token"),
                "palette": {
                    "background": bg,
                    "secondary_bg": card,
                    "primary": primary,
                    "accent": accent,
                    "secondary_accent": sec_accent,
                    "body_text": body_text
                }
            })
            
    # Fallback default candidates if empty
    if not color_candidates:
        if args.dark:
            color_candidates = [{
                "name": "Dark Blackboard (Teaching)",
                "note": "Deep green blackboard with soft chalk colors",
                "palette": {
                    "background": "#1E2B22",
                    "secondary_bg": "#273A2E",
                    "primary": "#F8FAFC",
                    "accent": "#F87171",
                    "secondary_accent": "#34D399",
                    "body_text": "#F8FAFC"
                }
            }]
        else:
            color_candidates = [{
                "name": "Warm Paper Notebook",
                "note": "Light warm sketchbook theme",
                "palette": {
                    "background": "#FDFBF7",
                    "secondary_bg": "#FFFFFF",
                    "primary": "#2D2D2D",
                    "accent": "#FF4D4D",
                    "secondary_accent": "#10B981",
                    "body_text": "#2D2D2D"
                }
            }]

    # Build typography candidates
    type_candidates = []
    if type_res and type_res.get("results"):
        for i, row in enumerate(type_res["results"]):
            latin_heading = row.get("Heading Font", "Inter")
            latin_body = row.get("Body Font", "Inter")
            
            # Formulate CJK pairings
            cjk_heading = "KaiTi" if "sketch" in args.query.lower() or "hand" in args.query.lower() else "Microsoft YaHei"
            cjk_body = "Microsoft YaHei"
            
            css_heading = f"'{latin_heading}', '{cjk_heading}', Georgia, serif" if cjk_heading == "KaiTi" else f"'{latin_heading}', '{cjk_body}', sans-serif"
            css_body = f"'{latin_body}', '{cjk_body}', 'PingFang SC', sans-serif"
            
            type_candidates.append({
                "name": row.get("Font Pairing Name", f"Pairing {i+1}"),
                "note": row.get("Best For", "Layout typography"),
                "heading": {
                    "cjk": cjk_heading,
                    "latin": latin_heading,
                    "css": css_heading,
                    "sample_cjk": "标题示例 TEXT",
                    "sample_latin": "Heading Sample"
                },
                "body": {
                    "cjk": cjk_body,
                    "latin": latin_body,
                    "css": css_body,
                    "sample_cjk": "正文段落示例文字",
                    "sample_latin": "Body text sample"
                },
                "body_size": 24
            })
            
    if not type_candidates:
        type_candidates = [{
            "name": "Hand-Drawn Sketch (Default)",
            "note": "Handwriting Kalam + KaiTi",
            "heading": {
                "cjk": "KaiTi",
                "latin": "Kalam",
                "css": "Kalam, KaiTi, Georgia, serif",
                "sample_cjk": "手写标题样式",
                "sample_latin": "Chalkboard Title"
            },
            "body": {
                "cjk": "Microsoft YaHei",
                "latin": "Patrick Hand",
                "css": "'Patrick Hand', 'Microsoft YaHei', sans-serif",
                "sample_cjk": "正文内容手绘字体排版",
                "sample_latin": "Normal text layout"
            },
            "body_size": 24
        }]

    # Create recommendations dict
    recs = {
        "lang": "zh",
        "recommend": {
            "canvas": "ppt169",
            "mode": "instructional" if "teach" in args.query.lower() or "ppt" in args.query.lower() else "briefing",
            "visual_style": visual_style,
            "icons": icons_lib,
            "image_usage": "provided",
            "preserve_master": True,
            "formula_policy": "mixed",
            "generation_mode": "gated",
            "transition_effect": "none",
            "delivery_purpose": "balanced"
        },
        "page_count": {"value": "25"},
        "audience": {"value": "期权交易员与投资者"},
        "content_divergence": {"value": ""},
        "color": {
            "selected": 0,
            "candidates": color_candidates
        },
        "typography": {
            "selected": 0,
            "candidates": type_candidates
        },
        "image_strategy": {
            "selected": 0,
            "candidates": [
                {
                    "name": "矢量手绘插图 (Vector Sketch)",
                    "rendering": "vector-illustration",
                    "palette": "outline",
                    "keywords": "chalk sketch line art whiteboard drawing",
                    "avoid": "heavy photo-real gradients 3D rendering",
                    "note": "Matches chalkboard blackboard look"
                }
            ]
        }
    }
    
    # Apply direct to spec_lock.md if --apply is set
    if args.apply:
        print("Applying recommendations directly to spec_lock.md...")
        spec_path = project_path / "spec_lock.md"
        if not spec_path.exists():
            print("Error: spec_lock.md not found. Project must be initialized first.", file=sys.stderr)
            return 1
            
        selected_color = color_candidates[0]["palette"]
        selected_type = type_candidates[0]
        
        # Parse old spec to build replacements map
        old_colors = {}
        old_fonts = {}
        
        old_lines = spec_path.read_text(encoding="utf-8").splitlines()
        current_section = None
        for line in old_lines:
            if line.startswith("## "):
                current_section = line[3:].strip()
            elif line.startswith("- ") and ":" in line:
                parts = line[2:].split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip()
                if current_section == "colors":
                    old_colors[key] = val
                elif current_section == "typography":
                    old_fonts[key] = val
                    
        # Write new spec
        new_lines = []
        skip_section = None
        for line in old_lines:
            if line.startswith("## colors"):
                skip_section = "colors"
                new_lines.append(line)
                new_lines.append(f"- bg: {selected_color['background']}")
                new_lines.append(f"- secondary_bg: {selected_color['secondary_bg']}")
                new_lines.append(f"- primary: {selected_color['primary']}")
                new_lines.append(f"- accent: {selected_color['accent']}")
                new_lines.append(f"- secondary_accent: {selected_color['secondary_accent']}")
                new_lines.append(f"- text: {selected_color['body_text']}")
                new_lines.append(f"- text_secondary: #94A3B8")
                new_lines.append(f"- border: #2D3F33" if args.dark else f"- border: #E2E8F0")
                continue
            elif line.startswith("## typography"):
                skip_section = "typography"
                new_lines.append(line)
                new_lines.append(f"- font_family: {selected_type['body']['css']}")
                new_lines.append(f"- title_family: {selected_type['heading']['css']}")
                new_lines.append(f"- body_family: {selected_type['body']['css']}")
                new_lines.append(f"- emphasis_family: {selected_type['heading']['css']}")
                new_lines.append(f"- code_family: Consolas, \"Courier New\", monospace")
                continue
            elif line.startswith("## ") and skip_section:
                skip_section = None
                
            if skip_section:
                continue
            new_lines.append(line)
            
        spec_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print("spec_lock.md updated!")
        
        # Build direct replacements list
        replacements = {
            old_colors.get("bg", "#F8FAFC"): selected_color["background"],
            old_colors.get("secondary_bg", "#FFFFFF"): selected_color["secondary_bg"],
            old_colors.get("primary", "#0F172A"): selected_color["primary"],
            old_colors.get("accent", "#EA580C"): selected_color["accent"],
            old_colors.get("secondary_accent", "#10B981"): selected_color["secondary_accent"],
            old_colors.get("text", "#0F172A"): selected_color["body_text"],
            old_colors.get("text_secondary", "#64748B"): "#94A3B8",
            old_colors.get("border", "#E2E8F0"): "#2D3F33" if args.dark else "#E2E8F0",
        }
        
        # Add font family replacements to handle any previous runs or styles
        font_variations = [
            ("Kalam, KaiTi, Georgia, serif", selected_type["heading"]["css"]),
            ("'Kalam, KaiTi, Georgia, serif'", selected_type["heading"]["css"]),
            ('"Kalam, KaiTi, Georgia, serif"', selected_type["heading"]["css"]),
            
            ("'Patrick Hand', 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif", selected_type["body"]["css"]),
            ('"Patrick Hand", "Microsoft YaHei", "PingFang SC", Arial, sans-serif', selected_type["body"]["css"]),
            ("'Patrick Hand', 'Microsoft YaHei', Arial, sans-serif", selected_type["body"]["css"]),
            ('"Patrick Hand", "Microsoft YaHei", Arial, sans-serif', selected_type["body"]["css"]),
            
            (old_fonts.get("title_family", "KaiTi, Georgia, serif"), selected_type["heading"]["css"]),
            (old_fonts.get("body_family", '"Microsoft YaHei", "PingFang SC", Arial, sans-serif'), selected_type["body"]["css"]),
            (old_fonts.get("font_family", '"Microsoft YaHei", Arial, sans-serif'), selected_type["body"]["css"])
        ]
        for old_f, new_f in font_variations:
            if old_f:
                replacements[old_f] = new_f
        
        # Apply SVG migrations
        svg_dir = project_path / "svg_output"
        if svg_dir.is_dir():
            print("Migrating SVG files...")
            for p in svg_dir.glob("*.svg"):
                content = p.read_text(encoding="utf-8")
                original = content
                
                # Apply color and font replacements
                for old_val, new_val in replacements.items():
                    content = content.replace(old_val, new_val)
                    
                # Clean up double font-family declarations
                content = content.replace("Kalam, Kalam, ", "Kalam, ")
                content = content.replace("'Patrick Hand', 'Patrick Hand', ", "'Patrick Hand', ")
                content = content.replace('"Patrick Hand", "Patrick Hand", ', '"Patrick Hand", ')
                
                if content != original:
                    p.write_text(content, encoding="utf-8")
                    
            print("SVG assets successfully synchronized to the new style!")
        else:
            print("Warning: svg_output directory not found, skipped SVG migration.")
            
    else:
        # Write to confirm_ui/recommendations.json
        confirm_dir = project_path / "confirm_ui"
        confirm_dir.mkdir(exist_ok=True)
        rec_path = confirm_dir / "recommendations.json"
        rec_path.write_text(json.dumps(recs, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Recommendations successfully written to {rec_path}!")
        print("You can now start the Confirm UI server to review and choose.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
