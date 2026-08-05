import os
import glob
import re
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_dir = os.path.join(proj, 'svg_output')
notes_dir = os.path.join(proj, 'notes')
total_md = os.path.join(notes_dir, 'total.md')

# Read original notes mapping
notes_content = {}
for m in glob.glob(os.path.join(notes_dir, '*.md')):
    if os.path.basename(m) == 'total.md': continue
    with open(m, 'r', encoding='utf-8') as f:
        notes_content[os.path.basename(m)] = f.read().strip()

# 1. Delete old 34
old_34_svg = os.path.join(svg_dir, '34_商战细分打法：侧翼与游击的六种小战场.svg')
if os.path.exists(old_34_svg): os.remove(old_34_svg)

# Define exact renames and edits
# Note: we do edits in-place on the old files BEFORE renaming them to avoid conflicts
edits = {
    '35_进攻战与侧翼战：Perplexity与Midjourney.svg': {
        'new_name': '34_进攻战与防御战：大厂的主力交锋.svg',
        'texts': {
            1: '进攻战与防御战：大厂的主力交锋',
            6: '🛡️ 防御战：自我攻击',
            7: '主动淘汰自己的旧阵地，封住挑战者的切入口。',
            8: '吉列自我攻击',
            9: 'DEC 错失防线',
            10: '💡 行业领导者与挑战者的核心博弈：',
            11: '进攻',
            12: '寻找巨头无法轻易改变的固有弱点',
            13: '防御',
            14: '在对手发力前先颠覆自己的既得利益',
            15: '',
            16: ''
        },
        'note_content': """【演讲引导】
接下来我们将四种战法分为两组来讲解。首先是属于大厂或准大厂的交锋：进攻战与防御战。

【核心要点】
作为行业老二或挑战者，打进攻战绝不是去拼刺刀，而是要“攻其不可救必救之弱点”。比如百事可乐当年攻击可口可乐的“老旧”，这就是可口可乐无法改变的基因。
反过来，作为行业老大，打防御战的核心不是“防守”，而是“自我攻击”。最好的防御就是在对手颠覆你之前，自己先推出新一代产品把自己的老阵地给干掉。如果像当年 DEC 那样为了保住小型机的利润而错失微机防线，就会被彻底颠覆。

【过渡语】
下面我们就通过具体的案例，来看看进攻战和防御战到底是怎么打的。"""
    },
    '38_防御战与游击战：大厂防线与垂直模型.svg': {
        'new_name': '37_侧翼战与游击战：小厂的蓝海突围.svg',
        'texts': {
            1: '侧翼战与游击战：小厂的蓝海突围',
            2: '侧翼战原则',
            3: '游击战原则',
            4: '开辟无争地带',
            5: '特性/价格/形态侧翼',
            6: '奇袭后追击',
            7: '胜利后继续投入资源',
            10: '侧翼战要在无人区抢占心智，游击战则是把战场缩到自己绝对能守得住的局部第一。'
        },
        'note_content': """【演讲引导】
看完了大厂的交锋，我们来看看资源有限的小企业、创业公司该怎么打。这就是侧翼战与游击战。

【核心要点】
侧翼战的核心是“不交火”，在无争地带发动奇袭。你可以做低价侧翼、高价侧翼、或者是特定人群侧翼。一旦奇袭成功，必须倾尽所有资源乘胜追击，巩固阵地。
而游击战的核心原则只有一个：找到一个足够小、小到大厂根本看不上或者不愿意全力进去的战场，并在那里做绝对的第一名。比如只做一个非常细分的垂直人群，或者一个特定的地理区域。

【过渡语】
理论听起来容易，实操中侧翼战和游击战怎么落地呢？我们看案例。"""
    }
}

for old_file, data in edits.items():
    svg_path = os.path.join(svg_dir, old_file)
    if os.path.exists(svg_path):
        ET.register_namespace('', "http://www.w3.org/2000/svg")
        tree = ET.parse(svg_path)
        root = tree.getroot()
        texts = root.findall('.//{http://www.w3.org/2000/svg}text')
        for i, text in data.get('texts', {}).items():
            if i < len(texts):
                texts[i].text = text
        tree.write(svg_path, encoding='UTF-8', xml_declaration=True)

# Define full renames sequence (Old -> New)
renames = {
    '35_进攻战与侧翼战：Perplexity与Midjourney.svg': '34_进攻战与防御战：大厂的主力交锋.svg',
    '36_案例深拆：进攻战（Perplexity攻击弱点）.svg': '35_案例深拆：进攻战（Perplexity攻击弱点）.svg',
    '39_案例深拆：防御战（吉列与DEC）.svg': '36_案例深拆：防御战（吉列与DEC）.svg',
    '38_防御战与游击战：大厂防线与垂直模型.svg': '37_侧翼战与游击战：小厂的蓝海突围.svg',
    '37_案例深拆：侧翼战（Abridge临床文书）.svg': '38_案例深拆：侧翼战（Abridge临床文书）.svg',
    '40_案例深拆：游击战（小阵地局部第一）.svg': '39_案例深拆：游击战（小阵地局部第一）.svg',
}

# Shift the rest (41 to 54 become 40 to 53)
for i in range(41, 55):
    old_files = glob.glob(os.path.join(svg_dir, f'{i}_*.svg'))
    if old_files:
        old_name = os.path.basename(old_files[0])
        new_name = f"{i-1:02d}_" + old_name.split('_', 1)[1]
        renames[old_name] = new_name

# Apply renames (must do safely avoiding overwrites)
# Move to temporary names first to avoid chain collisions
temp_renames = {}
for old, new in renames.items():
    if os.path.exists(os.path.join(svg_dir, old)):
        tmp = "TMP_" + new
        os.rename(os.path.join(svg_dir, old), os.path.join(svg_dir, tmp))
        temp_renames[tmp] = new

for tmp, new in temp_renames.items():
    os.rename(os.path.join(svg_dir, tmp), os.path.join(svg_dir, new))

# Update notes mapping with new names and edit new notes content
new_notes_content = {}
for old_svg, new_svg in renames.items():
    old_note = old_svg[:-4] + '.md'
    new_note = new_svg[:-4] + '.md'
    
    if old_svg in edits and 'note_content' in edits[old_svg]:
        new_notes_content[new_note] = edits[old_svg]['note_content']
    elif old_note in notes_content:
        new_notes_content[new_note] = notes_content[old_note]

# Add unmodified early notes to new_notes_content
for m, content in notes_content.items():
    if int(m[:2]) < 34 and m not in new_notes_content:
        new_notes_content[m] = content

# Rebuild total.md
svgs = sorted([os.path.basename(f) for f in glob.glob(os.path.join(svg_dir, '*.svg'))])
with open(total_md, 'w', encoding='utf-8') as f:
    for idx, s in enumerate(svgs, 1):
        stem = s[:-4]
        
        # Also fix page number visually
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
                            text.text = f"{prefix} {idx}"
                            changed = True
        if changed:
            tree.write(fpath, encoding='UTF-8', xml_declaration=True)

        # Write total.md
        f.write(f"# {stem}\n\n")
        note_name = stem + '.md'
        content = new_notes_content.get(note_name, f"【讲稿占位】\n{stem} 讲稿内容待完善。")
        f.write(content)
        f.write("\n\n---\n\n")

# Clean old notes directory (since total_md_split will overwrite, but better to clear orphans)
for m in glob.glob(os.path.join(notes_dir, '*.md')):
    if os.path.basename(m) != 'total.md':
        os.remove(m)

print("Restructure complete. total.md rebuilt and page numbers fixed.")
