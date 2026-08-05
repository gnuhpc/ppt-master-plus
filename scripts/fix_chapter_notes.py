import os
import glob

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
notes_dir = os.path.join(proj, 'notes')
total_md = os.path.join(notes_dir, 'total.md')

chapters = {
    '08_章节页.md': """【演讲引导】
接下来我们进入第二部分：什么是战略。在上一部分我们明白了运营效益不能替代战略之后，现在我们将直面战略定位的核心本质。

【核心要点】
这一部分我们将重点探讨三个核心概念：
首先是心智卡位。在当今这个信息爆炸的时代，真正的战场不在货架上，而是在用户的大脑里。
其次，我们会探讨定位的源泉从何而来。它绝不是凭空捏造的，而是基于企业自身的禀赋、行业的变化以及客户真实的需求。
最后，我们会分析如何利用创业者的优势，在变化中寻找到那些传统大企业难以覆盖的“新定位”。

【过渡语】
让我们先来看看，为什么说在现代商业中，抢占用户心智是所有战略的起点。
""",
    '13_章节页.md': """【演讲引导】
理解了战略定位的本质后，我们正式进入第三部分：活动系统与战略配称。这是波特战略理论中最精妙，也是最考验企业系统性思考能力的部分。

【核心要点】
定位如果只是停留在纸面上的口号，那就毫无价值。这部分我们将学习：
第一，如何将一个定位转化为一整套相互协同的“活动系统”。
第二，什么是“战略取舍”。真正的战略不是什么都做，而是为了目标，勇敢地放弃那些不符合定位的诱惑。
第三，配称的三种类型。我们将通过经典案例，看看如何通过系统性的活动配称，建立起竞争对手难以复制的巨大壁垒，并产生几何级的放大效应。

【过渡语】
到底什么是活动系统？我们先来了解一下定位与活动系统之间的骨架关系。
""",
    '23_章节页.md': """【演讲引导】
现在我们已经有了定位和活动系统，接下来进入第四部分：战略定位的落地与评估体系。任何战略都需要经过实践的检验。

【核心要点】
在这一部分，我们会探讨：
第一，如何亲手绘制你企业的活动系统图，把隐性的战略变成一张团队都能看懂的作战地图。
第二，我们会提供一套客观的“战略定位评估标准”，帮你给现在的战略做一次全面体检。
第三，战略不是一成不变的。我们会分析定位在不同发展阶段的动态演进机制。
最后，我们会通过案例深拆，以及复盘麦肯锡战略理论的局限性，从正反两面巩固我们的战略落地能力。

【过渡语】
那么，一张合格的活动系统图到底该怎么画？我们需要遵循哪些关键步骤？
""",
    '32_章节页.md': """【演讲引导】
在明确了落地评估体系之后，我们来到第五部分，也是非常实战的环节：定位落地——四种商战形式。商业就是一场没有硝烟的战争。

【核心要点】
根据企业在行业中的不同地位，特劳特将商战分为四种基本形式：
1. 进攻战：挑战行业领导者，攻击其强势中的弱点。
2. 侧翼战：在无争地带发动突袭，开辟新战场。
3. 防御战：作为领导者，如何自我攻击、封死对手的切入口。
4. 游击战：找到足够小且守得住的局部第一。
我们将通过Perplexity、Abridge、吉列等最新的实战案例，深入拆解这四种打法的精髓，帮你找到最适合你企业当下的商战兵法。

【过渡语】
首先，让我们全面了解一下这四种商战形式的适用场景和基本原则。
"""
}

# 1. Overwrite the specific chapter notes
for filename, content in chapters.items():
    filepath = os.path.join(notes_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# 2. Rebuild total.md exactly according to current SVGs
svg_dir = os.path.join(proj, 'svg_output')
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
        # Default fallback should not be needed but just in case
        content = notes_content.get(note_name, f"【讲稿占位】\n{stem} 讲稿内容待完善。")
        f.write(content)
        f.write("\n\n---\n\n")

print("Chapter notes rewritten and total.md successfully rebuilt.")
