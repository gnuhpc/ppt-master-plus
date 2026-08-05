import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_dir = os.path.join(proj, 'svg_output')

def repair_svg(filename, replacements, clear_from=None):
    path = os.path.join(svg_dir, filename)
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree = ET.parse(path)
    root = tree.getroot()
    texts = root.findall('.//{http://www.w3.org/2000/svg}text')
    
    for i, t in replacements.items():
        if i < len(texts):
            texts[i].text = t
            
    if clear_from is not None:
        for i in range(clear_from, len(texts) - 1): # keep the last one which is usually Page Number
            texts[i].text = ''
            
    tree.write(path, encoding='UTF-8', xml_declaration=True)

# P34
repair_svg('34_进攻战与防御战：大厂的主力交锋.svg', {
    2: '⚔️ 进攻战：攻强势之弱',
    3: '从领导者强势中的弱点出击，借老大的强势反向创造差异。',
    4: '百事可乐 攻击 可口可乐的“老旧”',
    5: '',
    6: '🛡️ 防御战：自我攻击',
    7: '主动淘汰自己的旧阵地，封住挑战者的切入口。',
    8: '吉列：用多刀片淘汰自己的单刀片',
    9: 'DEC：为了保全利润而错失微机防线',
    10: '💡 行业领导者与挑战者的核心博弈：',
    11: '进攻方',
    12: '寻找巨头无法轻易改变的固有弱点',
    13: '防御方',
    14: '在对手发力前先颠覆自己的既得利益'
}, clear_from=15)

# P37
repair_svg('37_侧翼战与游击战：小厂的蓝海突围.svg', {
    2: '🚀 侧翼战原则',
    3: '🎯 游击战原则',
    4: '开辟无争地带',
    5: '特性/价格/形态侧翼',
    6: '奇袭后追击',
    7: '一旦取胜必须倾注资源巩固阵地',
    8: '',
    9: '',
    10: '侧翼战要在无人区抢占心智，游击战则是把战场缩到自己绝对能守得住的局部第一。',
    11: '',
    12: '局部第一',
    13: '把阵地缩小到大厂不愿进入的细分市场',
    14: '',
    15: ''
}, clear_from=None)

print("SVG texts repaired.")
