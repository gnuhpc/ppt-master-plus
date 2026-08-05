import os
import glob

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
notes_dir = os.path.join(proj, 'notes')
target_note = os.path.join(notes_dir, '34_进攻战与防御战：大厂的主力交锋.md')

new_content = """【演讲引导】
接下来，我们将四种战法分为两大阵营来分别讲解。这页片子展示的是属于“大厂或准大厂”之间的主力交锋：进攻战与防御战。

【核心要点】
我们先看左边的**进攻战**。
作为行业老二或者有实力的挑战者，打进攻战绝不是去拼刺刀比配置，而是要“攻强势之弱”。你必须从领导者最强大的优势中，去寻找那个它“无法改变”的弱点。
- **第一个经典案例是百事可乐对可口可乐**。可口可乐的强势是“百年经典、正宗原创”，这个优势太强了。但百事可乐怎么进攻呢？它把可口可乐的“经典正宗”反向定位成了“传统、老土、你爷爷喝的可乐”，进而把自己定位为“年轻一代的选择”。可口可乐能反击说“我也年轻”吗？不能，因为它不可能放弃百年经典的品牌基因，这就是“无法改变的弱点”。
- **第二个案例是七喜**。当时碳酸饮料基本等同于可乐。七喜没有去说自己的柠檬味多好喝，而是直接定位为“非可乐”。借着两大可乐的强势品类起飞，再用“不含咖啡因”这个可乐天然不具备的健康属性去攻击它的固有弱点，从而确立了自己第三大饮料的地位。

再看右边的**防御战**。
作为行业老大，打防御战的核心绝对不是“防守反击”，而是**“自我攻击”**。最好的防御就是在对手颠覆你之前，自己先推出新一代产品把自己的老阵地给干掉。
- **正面的典范是吉列**。当年吉列的单层刀片非常赚钱，但当面临挑战者（比如比克）时，吉列怎么做？它在单刀片依然利润丰厚的时候，主动推出了双层刀片（Trac II）去“淘汰”自己的单刀片。宁愿自己蚕食自己的利润，也绝不给对手任何可乘之机。这叫用多刀片淘汰单刀片。
- **反面的教训则是DEC（美国数字设备公司）**。它当年是小型主机的绝对王者。当微型机（PC的前身）开始出现时，DEC为了保住小型机高昂的利润率，不愿意推出便宜的微机来“攻击”自己的主营业务。他们试图用小型机去防守，结果大家都知道，坐等IBM和苹果抢占了PC时代，DEC最终被彻底颠覆。

【总结升华】
总结一下这两种主力战法的核心博弈：
对于**进攻方**，你的首要任务是“找茬”——寻找巨头无法轻易转身、无法轻易改变的固有弱点，一击致命。
对于**防御方**，你的首要任务是“挥刀自宫”——在对手发力之前，先用更先进的理念或产品颠覆自己的既得利益，永远让自己做自己的掘墓人，这才是真正的护城河。"""

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

print("Updated P34 notes and rebuilt total.md.")
