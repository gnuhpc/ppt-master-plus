import os
import glob
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_dir = os.path.join(proj, 'svg_output')
notes_dir = os.path.join(proj, 'notes')
total_md = os.path.join(notes_dir, 'total.md')

changes = {
    '36_案例深拆：Perplexity': {
        'new_stem': '36_案例深拆：进攻战（Perplexity攻击弱点）',
        'text0': '第五部分：进攻战案例深拆',
        'text1': '进攻战：Perplexity攻击搜索强势中的弱点'
    },
    '37_案例深拆：Abridge临床文书侧翼': {
        'new_stem': '37_案例深拆：侧翼战（Abridge临床文书）',
        'text0': '第五部分：侧翼战案例深拆',
        'text1': '侧翼战：Abridge在无争地带的突围'
    },
    '39_防御战详解：吉列自我攻击与DEC错失防线': {
        'new_stem': '39_案例深拆：防御战（吉列与DEC）',
        'text0': '第五部分：防御战案例深拆',
        'text1': '防御战：吉列自我攻击与DEC错失防线'
    },
    '40_游击战详解：小阵地中的局部第一': {
        'new_stem': '40_案例深拆：游击战（小阵地局部第一）',
        'text0': '第五部分：游击战案例深拆',
        'text1': '游击战：找到足够小且守得住的阵地'
    }
}

# 1. Rename files and edit SVGs
for old_stem, data in changes.items():
    old_svg = os.path.join(svg_dir, old_stem + '.svg')
    new_svg = os.path.join(svg_dir, data['new_stem'] + '.svg')
    
    old_note = os.path.join(notes_dir, old_stem + '.md')
    new_note = os.path.join(notes_dir, data['new_stem'] + '.md')
    
    if os.path.exists(old_svg):
        # Edit SVG text
        ET.register_namespace('', "http://www.w3.org/2000/svg")
        tree = ET.parse(old_svg)
        root = tree.getroot()
        texts = root.findall('.//{http://www.w3.org/2000/svg}text')
        if len(texts) > 1:
            texts[0].text = data['text0']
            texts[1].text = data['text1']
        tree.write(old_svg, encoding='UTF-8', xml_declaration=True)
        # Rename SVG
        os.rename(old_svg, new_svg)
        
    if os.path.exists(old_note):
        os.rename(old_note, new_note)

# 2. Rebuild total.md
svgs = sorted([os.path.basename(f) for f in glob.glob(os.path.join(svg_dir, '*.svg'))])
notes_content = {}
for m in glob.glob(os.path.join(notes_dir, '*.md')):
    if os.path.basename(m) == 'total.md': continue
    with open(m, 'r', encoding='utf-8') as f:
        notes_content[os.path.basename(m)] = f.read().strip()

with open(total_md, 'w', encoding='utf-8') as f:
    for s in svgs:
        stem = s[:-4]
        f.write(f"# {stem}\n\n")
        note_name = stem + '.md'
        content = notes_content.get(note_name, "【演讲引导】\n待补充\n\n【痛点分析】\n待补充\n\n【总结归纳】\n待补充")
        f.write(content)
        f.write("\n\n---\n\n")

print("Files renamed, SVGs updated, and total.md rebuilt.")
