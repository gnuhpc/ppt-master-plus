import os
import glob

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
notes_dir = os.path.join(proj, 'notes')
target_note = os.path.join(notes_dir, '37_侧翼战与游击战：小厂的蓝海突围.md')

new_content = """【演讲引导】
看完了大厂之间“正面硬刚”的进攻战和“自我颠覆”的防御战，我们来看看资源有限的小企业、创业公司该怎么打。
今天很多企业都会说“我们是大象脚下的蚂蚁，稍不留神就被踩死了”，这说明大家面对巨头是有很深恐惧的。
其实，破局之道就是定位理论里的两套非对称打法：侧翼战与游击战。

【核心要点】

**一、侧翼战（Flanking）：发动无争地带的奇袭**
侧翼战的核心是“不交火”。它的要义不是在别人的主战场上去抢阵地，而是在巨头看不见、或者看不起的无争地带发动奇袭，建立新特性。
侧翼战有三种常见形态：
1. **价格侧翼**：向上做“高价侧翼”，比如早期的哈根达斯，把冰淇淋卖出天价，直接跳出了传统廉价冰淇淋的竞争；向下做“低价侧翼”，比如早期的每日旅馆（Days Inn）或者后来的拼多多，专做巨头下沉不了的市场。
2. **形态侧翼**：比如索尼第一代随身听（Walkman），它舍弃了音响的录音功能和外放喇叭，单纯追求便携。
3. **特性侧翼**：比如联邦快递（FedEx）的“隔夜送达”，在传统邮政体系和普通快递还在拼价格和覆盖面的时候，它一刀切中了“绝对快”这个特性。
**侧翼战最关键的一点是：一旦奇袭成功，必须倾尽所有资源乘胜追击。** 因为一旦你暴露了目标，巨头就会反扑。你必须在巨头调转枪口之前，彻底巩固自己的心智阵地。

**二、游击战（Guerrilla）：小阵地的局部绝对第一**
游击战的核心原则只有一个：**找到一个足够小、大厂根本不愿意全力进去的战场，并在那里做绝对的第一名。**
侧翼战的最终目的是为了做大，甚至把侧翼变成主战场；而游击战的目的就是“守住自己的一亩三分地”。
1. **地理游击**：全国我打不过你，那我就只做某一个省、某一个城市的绝对第一。比如早期的茶颜悦色，死守长沙，密集开店。
2. **人群游击**：专做某一类细分人群，大厂的通用产品服务不了他们那么细碎的需求。
3. **行业游击**：专门给某个冷门行业做系统，比如汽配库存管理系统，大厂根本没有精力去深耕几百万个SKU的复杂业务逻辑。
4. **高端游击**：比如劳斯莱斯，它的销量极低，但单价极高。它永远不可能威胁丰田和大众的市场份额，所以通用和丰田也绝不会去发动一场“消灭劳斯莱斯”的战争。

【总结升华】
侧翼战要在无人区抢占心智，游击战则是把战场缩到自己绝对能守得住的局部第一。
它们共同的底层逻辑是：**用战略视角的战场选择，来弥补战术层面的兵力不足。** 游击战和侧翼战绝不是弱者随便找个小市场躲起来苟延残喘，而是一种极其高级且需要高度克制的战略设计。

【过渡语】
理论听起来容易，接下来，我们就分别深入拆解一下实操中的侧翼战和游击战到底是怎么打的。
"""

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

print("Updated P37 notes and rebuilt total.md.")
