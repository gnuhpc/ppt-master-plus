import os
import glob
import re
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_dir = os.path.join(proj, 'svg_output')
notes_dir = os.path.join(proj, 'notes')
total_md = os.path.join(notes_dir, 'total.md')

svgs = sorted([os.path.basename(f) for f in glob.glob(os.path.join(svg_dir, '*.svg'))])
mds = sorted([os.path.basename(f) for f in glob.glob(os.path.join(notes_dir, '*.md')) if f != 'total.md'])

# 1. Update SVG page numbers
for idx, s in enumerate(svgs, 1):
    fpath = os.path.join(svg_dir, s)
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree = ET.parse(fpath)
    root = tree.getroot()
    changed = False
    for text in root.findall('.//{http://www.w3.org/2000/svg}text'):
        if text.text:
            try:
                x = float(text.get('x', 0))
                y = float(text.get('y', 0))
            except ValueError:
                continue
            if x > 1100 and y > 650:
                old_text = text.text
                if re.match(r'^0?\d+$', old_text.strip()):
                    text.text = f"{idx:02d}" if old_text.strip().startswith('0') else str(idx)
                    changed = True
                else:
                    m = re.match(r'^(PAGE|Page|page)\s*0?\d+$', old_text.strip())
                    if m:
                        prefix = m.group(1)
                        # Keep formatting
                        text.text = f"{prefix} {idx}"
                        changed = True
    if changed:
        tree.write(fpath, encoding='UTF-8', xml_declaration=True)

# 2. Build mapping of old stems to notes content
notes_content = {}
for m in mds:
    with open(os.path.join(notes_dir, m), 'r', encoding='utf-8') as f:
        content = f.read().strip()
    notes_content[m] = content

# Helper to find matching old note
def find_note_for_svg(svg_name):
    stem = svg_name[:-4]
    if '_' not in stem: return ""
    idx_part, name_part = stem.split('_', 1)
    
    # 1. Exact name match
    for m, content in notes_content.items():
        m_stem = m[:-3]
        if '_' in m_stem and m_stem.split('_', 1)[1] == name_part:
            return content
            
    # 2. Special cases for renamed appendix chapters
    special_cases = {
        "案例集": "附录：本土实战案例",
        "案例01：血尔补血口服液的对立定位": "案例深拆：血尔补血口服液的对立定位",
        "案例02：江中消食片的对立定位革命": "本土实战案例（一）：江中消食片的对立定位革命",
        "案例03：芙蓉王反超白沙的取舍法则": "本土实战案例（二）：芙蓉王反超白沙的取舍法则",
        "案例04：光明乳业：轻资产战略与保鲜奶定位失焦": "光明乳业：轻资产战略与保鲜奶定位失焦",
        "案例05：麦肯锡案例诊断（一）：神州数码的“三级火箭”受挫": "麦肯锡案例诊断（一）：神州数码的“三级火箭”受挫",
        "案例06：麦肯锡案例诊断（二）：德隆与Murray并购破产案": "麦肯锡案例诊断（二）：德隆与Murray并购破产案",
        "案例07：战略失败样本：盲目跨界与愿景倒推": "战略失败样本：盲目跨界与愿景倒推"
    }
    
    if name_part in special_cases:
        target_name = special_cases[name_part]
        for m, content in notes_content.items():
            m_stem = m[:-3]
            if '_' in m_stem and m_stem.split('_', 1)[1] == target_name:
                return content
                
    # 3. Handle duplicates (e.g., multiple "章节页")
    # For multiple 章节页, we can just use the generic 章节页 content
    if "章节页" in name_part:
        for m, content in notes_content.items():
            if "章节页" in m:
                return content
                
    return "【演讲引导】\n待补充\n\n【痛点分析】\n待补充\n\n【总结归纳】\n待补充"

# 3. Write new total.md
with open(total_md, 'w', encoding='utf-8') as f:
    for s in svgs:
        stem = s[:-4]
        f.write(f"# {stem}\n\n")
        f.write(find_note_for_svg(s))
        f.write("\n\n---\n\n")

print("Done generating total.md and updating SVG page numbers.")
