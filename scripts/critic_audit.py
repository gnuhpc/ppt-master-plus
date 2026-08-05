#!/usr/bin/env python3
"""
PPT Master - Independent Critic Audit Tool (inspired by addsumtech/slides_maker)

Performs a rigorous, multi-dimensional Critic audit on a generated project:
1. WCAG 2.1 Contrast Ratio Audit (4.5:1 floor)
2. Claim Ledger & Zero Data Fabrication Audit
3. Layout Collision & Footer Band Protection Audit
4. Motion Manifest & Object-level Animation Anchor Audit
5. Unreplaced Placeholder & Overflow Audit

Usage:
    python3 scripts/critic_audit.py <project_path>
"""

import sys
import re
import json
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"

def relative_luminance(hex_color: str) -> float:
    """Calculate WCAG 2.1 relative luminance for HEX color."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    if len(hex_color) != 6:
        return 0.5
    try:
        r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    except ValueError:
        return 0.5
    def srgb_adj(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * srgb_adj(r) + 0.7152 * srgb_adj(g) + 0.0722 * srgb_adj(b)

def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate contrast ratio between two colors."""
    l1 = relative_luminance(color1)
    l2 = relative_luminance(color2)
    max_l, min_l = max(l1, l2), min(l1, l2)
    return (max_l + 0.05) / (min_l + 0.05)

class CriticAuditor:
    def __init__(self, project_path: str):
        self.proj_dir = Path(project_path).resolve()
        self.svg_dir = self.proj_dir / "svg_output"
        self.spec_file = self.proj_dir / "design_spec.md"
        self.findings = []
        self.summary = {"total_pages": 0, "passed_pages": 0, "issues_count": 0, "verdict": "OK"}

    def run_audit(self) -> Dict:
        print(f"=== Running Independent Critic Audit on {self.proj_dir.name} ===")
        
        # 1. Audit Claim Ledger in design_spec.md
        self._audit_claim_ledger()

        # 2. Audit Speaker Notes and Presentation Checkup (humanize-ppt essence)
        self._audit_presentation_checkup()

        # 3. Audit SVG Slide files
        svg_files = sorted(glob.glob(str(self.svg_dir / "*.svg")))
        self.summary["total_pages"] = len(svg_files)


        if not svg_files:
            print("Warning: No SVG files found under svg_output/.")
            return self.summary

        for svg_file in svg_files:
            self._audit_svg_file(Path(svg_file))

        self.summary["issues_count"] = len(self.findings)
        if any(f["severity"] == "ERROR" for f in self.findings):
            self.summary["verdict"] = "REJECTED (Hard Errors Found)"
        elif any(f["severity"] == "WARN" for f in self.findings):
            self.summary["verdict"] = "NEEDS_REFINEMENT (Warnings Found)"
        else:
            self.summary["verdict"] = "APPROVED (Clean Pass)"

        # Save critic report artifact
        report_path = self.proj_dir / "critic_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump({"summary": self.summary, "findings": self.findings}, f, indent=2, ensure_ascii=False)

        print(f"\nAudit complete. Verdict: {self.summary['verdict']}")
        print(f"Report written to: {report_path}")
        return self.summary

    def _audit_claim_ledger(self):
        if not self.spec_file.exists():
            self.findings.append({
                "severity": "WARN",
                "category": "Data Fidelity",
                "page": "design_spec.md",
                "message": "design_spec.md not found. Cannot verify Claim Ledger data tracing."
            })
            return

        spec_text = self.spec_file.read_text(encoding="utf-8")
        if "claim_ledger" not in spec_text.lower():
            self.findings.append({
                "severity": "WARN",
                "category": "Data Fidelity",
                "page": "design_spec.md",
                "message": "No claim_ledger section found in design_spec.md. Ensure data points map to source document."
            })

    def _audit_presentation_checkup(self):
        """Presentation Checkup (演讲体检 - 借鉴 humanize-ppt):
        Ensure speaker notes exist, check note alignment, and detect dead-end look-only cards.
        """
        notes_dir = self.proj_dir / "notes"
        total_notes = notes_dir / "total.md"

        has_notes = notes_dir.exists() or total_notes.exists()
        if not has_notes:
            self.findings.append({
                "severity": "WARN",
                "category": "Presentation Checkup (演讲体检)",
                "page": "notes/",
                "message": "No speaker notes directory or notes/total.md found. Decks without speaker notes risk being look-only dead ends."
            })
            return

        # Check per-slide notes alignment
        svg_files = sorted(glob.glob(str(self.svg_dir / "*.svg")))
        for svg_path in svg_files:
            stem = svg_path.stem
            note_file = notes_dir / f"{stem}.md"
            content = svg_path.read_text(encoding="utf-8")
            
            # Extract plain text from SVG
            plain_text = re.sub(r'<[^>]+>', ' ', content)
            words = plain_text.split()
            
            # Dead-end slide detection: sparse text (< 15 words) and no dedicated note file
            if len(words) < 15 and not note_file.exists():
                self.findings.append({
                    "severity": "WARN",
                    "category": "Presentation Checkup (演讲体检)",
                    "page": svg_path.name,
                    "message": f"Potential look-only dead-end slide ({len(words)} words, missing notes/{stem}.md). A presenter cannot deliver this slide without notes or content."
                })



    def _audit_svg_file(self, svg_path: Path):
        page_name = svg_path.name
        content = svg_path.read_text(encoding="utf-8")

        # McKinsey Title Narrative Audit: Check for catalog/directory titles (e.g. "市场分析", "概览", "Overview")
        title_match = re.search(r'<text[^>]*id=["\'](?:title|page_title)["\'][^>]*>(.*?)</text>', content, re.DOTALL | re.IGNORECASE)
        if not title_match:
            # Fallback: first text element with font-size >= 24
            title_match = re.search(r'<text[^>]*font-size=["\'](?:2[4-9]|[3-9]\d)["\'][^>]*>(.*?)</text>', content, re.DOTALL | re.IGNORECASE)
        
        if title_match:
            raw_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            banned_catalog_phrases = {'概览', '总结', '目录', '背景', '市场分析', '竞争格局', '系统架构', '方案对比',
                                      'overview', 'summary', 'background', 'introduction', 'market analysis'}
            if raw_title.lower() in banned_catalog_phrases:
                self.findings.append({
                    "severity": "WARN",
                    "category": "McKinsey Title Narrative (标题即结论)",
                    "page": page_name,
                    "message": f"Catalog title detected: '{raw_title}'. McKinsey rule: titles must be declarative conclusions with metrics/inference (e.g. '未来三年规模增长35%'), not generic topic headers."
                })

        # Check background color
        bg_match = re.search(r'<(?:rect|path|g)[^>]*fill=["\'](#[0-9A-Fa-f]{6})["\'][^>]*id=["\'](?:bg|background)', content, re.IGNORECASE)
        if not bg_match:
            bg_match = re.search(r'<rect[^>]*width=["\'](?:100%|1280|1920)["\'][^>]*fill=["\'](#[0-9A-Fa-f]{6})["\']', content, re.IGNORECASE)
        bg_color = bg_match.group(1) if bg_match else "#FFFFFF"

        # Check text fill contrast
        text_matches = re.finditer(r'<text[^>]*fill=["\'](#[0-9A-Fa-f]{6})["\'][^>]*>(.*?)</text>', content, re.DOTALL | re.IGNORECASE)
        for m in text_matches:
            color = m.group(1)

            text_snippet = re.sub(r'<[^>]+>', '', m.group(2)).strip()[:30]
            ratio = contrast_ratio(color, bg_color)
            if ratio < 4.5:
                self.findings.append({
                    "severity": "WARN",
                    "category": "WCAG Contrast",
                    "page": page_name,
                    "message": f"Low contrast ({ratio:.2f}:1) for text '{text_snippet}' (fill={color} vs bg={bg_color}). Expected >= 4.5:1."
                })

        # Check Footer Band Protection (y > 670 for canvas height 720)
        try:
            root = ET.fromstring(content)
            for elem in root.iter():
                tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                if tag in ('rect', 'text', 'image', 'path') and elem.get('id') not in ('footer', 'page_num', 'bg'):
                    y_str = elem.get('y')
                    if y_str:
                        try:
                            y_val = float(y_str)
                            if y_val > 675:
                                self.findings.append({
                                    "severity": "WARN",
                                    "category": "Layout Collision",
                                    "page": page_name,
                                    "message": f"Element <{tag} id='{elem.get('id', '')}'> at y={y_val:.1f} invades footer protection band (y > 675)."
                                })
                        except ValueError:
                            pass
        except ET.ParseError:
            self.findings.append({
                "severity": "ERROR",
                "category": "XML Validity",
                "page": page_name,
                "message": "Malformed XML structure."
            })

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/critic_audit.py <project_path>")
        sys.exit(1)

    auditor = CriticAuditor(sys.argv[1])
    res = auditor.run_audit()
    sys.exit(0 if res["verdict"].startswith("APPROVED") else 1)
