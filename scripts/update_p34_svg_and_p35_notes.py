import os
import glob
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'

# Task 1: Update P34 SVG layout
svg_file = os.path.join(proj, 'svg_output/34_进攻战与防御战：大厂的主力交锋.svg')
ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

texts = root.findall('.//{http://www.w3.org/2000/svg}text')
for text in texts:
    if '行业领导者与挑战者的核心博弈' in (text.text or ''):
        parent_g = root.find('.//*{http://www.w3.org/2000/svg}text[.=\"' + text.text + '\"]/..')
        if parent_g is not None:
            g_cols = parent_g.find('{http://www.w3.org/2000/svg}g')
            if g_cols is not None:
                # Remove rects
                for rect in g_cols.findall('{http://www.w3.org/2000/svg}rect'):
                    g_cols.remove(rect)
                
                # Now only texts are left in g_cols (assuming we removed rects)
                # We have 4 texts: 
                # 0: Label 1
                # 1: Text 1
                # 2: Label 2
                # 3: Text 2
                col_texts = g_cols.findall('{http://www.w3.org/2000/svg}text')
                if len(col_texts) >= 4:
                    col_texts[0].text = '⚔️ 进攻战核心：'
                    col_texts[0].set('x', '60')
                    col_texts[0].set('y', '0')
                    col_texts[0].set('font-size', '20')
                    col_texts[0].set('text-anchor', 'start')
                    
                    col_texts[1].text = '寻找巨头无法轻易改变的固有弱点'
                    col_texts[1].set('x', '220')
                    col_texts[1].set('y', '0')
                    col_texts[1].set('font-size', '20')
                    
                    col_texts[2].text = '🛡️ 防御战核心：'
                    col_texts[2].set('x', '600')
                    col_texts[2].set('y', '0')
                    col_texts[2].set('font-size', '20')
                    col_texts[2].set('text-anchor', 'start')
                    
                    col_texts[3].text = '在对手发力前颠覆自己的既得利益'
                    col_texts[3].set('x', '760')
                    col_texts[3].set('y', '0')
                    col_texts[3].set('font-size', '20')
        break

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)

# Task 2: Update P35 Notes
notes_dir = os.path.join(proj, 'notes')
target_note = os.path.join(notes_dir, '35_案例深拆：进攻战（Perplexity攻击弱点）.md')

new_content = """【演讲引导】
刚刚我们在上一页讲到了“进攻战”的核心是“攻强势之弱”。在传统的快消品和IT时代，我们有百事可乐和DEC的故事，那么在AI时代，谁是进攻战最经典的代表？
答案是 Perplexity。它完美演绎了如何向 Google 这样的绝对巨头开火。

【核心要点】
很多时候，创业公司做搜索，潜意识里是去比较“我的模型是不是比Google更聪明”、“我的索引是不是比它更大”。如果是这样，你连开战的资格都没有。

Perplexity 是怎么做的？它精准地找到了 Google **强势中必然包含的弱点**。
- Google 的**强势**是什么？是它有无可匹敌的竞价排名商业化体系，是它极度庞大的链接索引分发能力。
- 但这种强势必然带来什么**弱点**？那就是 Google 必须让你“自己找答案”。它给你10条蓝链接，让你自己去点、自己去辨别哪个是广告、自己去拼凑碎片化信息。这是 Google 的护城河决定的，它不能直接给你唯一答案，否则它的竞价广告怎么卖？它的链接生态怎么活？这，就是 Google 无法轻易改变的“固有弱点”。

所以，Perplexity 的**进攻定位**非常明确：我不是更好的搜索引擎，我是“答案引擎（Answer Engine）”。
我把检索和阅读这两步合并，开门见山直接给你综合提炼好的答案，并且内联引用来源来解决信任问题。

【总结升华】
这个案例给我们最大的战略启示是：
打进攻战，绝不是去复制巨头的火力，也不是在正面战场和巨头拼刺刀。而是要把巨头因为体量、因为商业模式而不可避免产生的“摩擦”，重新命名为我们自己的专属阵地。Google 的摩擦是“链接筛选”，Perplexity 的阵地就是“直达答案”。"""

with open(target_note, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Rebuild total.md
md_files = sorted(glob.glob(os.path.join(notes_dir, '*.md')))
total_content = []
for f in md_files:
    if os.path.basename(f) == 'total.md':
        continue
    with open(f, 'r', encoding='utf-8') as md:
        total_content.append(f"## {os.path.basename(f).replace('.md', '')}\n\n")
        total_content.append(md.read().strip() + '\n\n')

total_md_path = os.path.join(notes_dir, 'total.md')
with open(total_md_path, 'w', encoding='utf-8') as f:
    f.write(''.join(total_content))

print("Updated P34 SVG and P35 notes, then rebuilt total.md.")
