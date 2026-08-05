import os
import shutil
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_dir = os.path.join(proj, 'svg_output')
backup_dir = os.path.join(proj, 'backup/20260709_114549/svg_output')

ET.register_namespace('', "http://www.w3.org/2000/svg")

def apply_texts_and_tspans(src_file, dst_file, replacements, page_num):
    src = os.path.join(backup_dir, src_file)
    dst = os.path.join(svg_dir, dst_file)
    
    shutil.copy2(src, dst)
    tree = ET.parse(dst)
    root = tree.getroot()
    texts = root.findall('.//{http://www.w3.org/2000/svg}text')
    
    for i, t in enumerate(texts):
        if i in replacements:
            data = replacements[i]
            if isinstance(data, str):
                t.text = data
                for ts in t.findall('{http://www.w3.org/2000/svg}tspan'):
                    ts.text = ''
            elif isinstance(data, dict):
                t.text = data.get('text', '')
                tspans = t.findall('{http://www.w3.org/2000/svg}tspan')
                ts_data = data.get('tspans', [])
                for j, ts in enumerate(tspans):
                    if j < len(ts_data):
                        ts.text = ts_data[j]
                    else:
                        ts.text = ''
        else:
            if i > max(replacements.keys()) and i != len(texts) - 1:
                t.text = ''
                for ts in t.findall('{http://www.w3.org/2000/svg}tspan'):
                    ts.text = ''
                    
    texts[-1].text = f"Page {page_num}"
    tree.write(dst, encoding='UTF-8', xml_declaration=True)

# P34: Offensive (Left) vs Defensive (Right)
apply_texts_and_tspans(
    '35_进攻战与侧翼战：Perplexity与Midjourney.svg',
    '34_进攻战与防御战：大厂的主力交锋.svg',
    {
        0: '第五部分：定位落地：四种商战形式',
        1: {'text': '进攻战与防御战：大厂的主力交锋', 'tspans': []},
        2: '⚔️ 进攻战：攻强势之弱',
        3: '从领导者强势中的弱点出击，借老大的强势反向创造差异。',
        4: '百事可乐 攻击 可口可乐的“老旧”',
        5: {
            'text': '',
            'tspans': [
                '将可口可乐重新定位为“传统老土”，',
                '自身定位为“年轻人的可乐”。'
            ]
        },
        6: '七喜：“非可乐”定位',
        7: {
            'text': '',
            'tspans': [
                '借“两大可乐”的强势品类起飞，',
                '再以“不含咖啡因”攻击可乐固有弱点。'
            ]
        },
        8: '🛡️ 防御战：自我攻击',
        9: '主动淘汰自己的旧阵地，封住挑战者的切入口。',
        10: '吉列：用多刀片淘汰自己的单刀片',
        11: {
            'text': '',
            'tspans': [
                '在单刀片赚钱时，主动推出双刀片，',
                '不给对手任何可乘之机。'
            ]
        },
        12: 'DEC：为了保全利润而错失防线',
        13: {
            'text': '',
            'tspans': [
                '试图用小型机的成功去防守微型机，',
                '最终被PC彻底颠覆。'
            ]
        },
        14: '💡 行业领导者与挑战者的核心博弈：',
        15: '进攻方',
        16: '寻找巨头无法轻易改变的固有弱点',
        17: '防御方',
        18: '在对手发力前先颠覆自己的既得利益',
        19: '',
        20: ''
    },
    34
)

# P37: Flanking (Left) vs Guerrilla (Right)
apply_texts_and_tspans(
    '38_防御战与游击战：大厂防线与垂直模型.svg',
    '37_侧翼战与游击战：小厂的蓝海突围.svg',
    {
        0: '第五部分：定位落地：四种商战形式',
        1: '侧翼战与游击战：小厂的蓝海突围',
        2: '🚀 侧翼战原则',
        3: {
            'text': '',
            'tspans': [
                '在无争地带建立新特性，避开主力战场，',
                '抢占心智空白。'
            ]
        },
        4: '🎯 游击战原则',
        5: {
            'text': '',
            'tspans': [
                '找到足够小、大厂不愿全力进入的阵地，',
                '并在那里做绝对的第一名。'
            ]
        },
        6: '无争地带',
        7: '特性、价格、形态侧翼',
        8: {
            'text': '',
            'tspans': [
                '✓ 低价/高价侧翼：每日旅馆、哈根达斯',
                '✓ 小型产品侧翼：索尼随身听',
                '✓ 特性侧翼：联邦快递“隔夜送达”'
            ]
        },
        9: '乘胜追击',
        10: '奇袭成功后必须巩固阵地',
        11: {
            'text': '',
            'tspans': [
                '✓ 侧翼战的本质是一次奇袭',
                '✓ 目标是不被领导者察觉地建立阵地',
                '✓ 取胜后倾注资源，防止大厂反扑'
            ]
        },
        12: '局部第一',
        13: '游击：小阵地制胜',
        14: {
            'text': '',
            'tspans': [
                '✓ 地理游击：只做某个区域第一',
                '✓ 人口游击：专做小企业主等特定人群',
                '✓ 行业游击：如专门做汽配库存系统',
                '✓ 高端游击：劳斯莱斯（高价但低量）'
            ]
        },
        15: '侧翼战要在无人区抢占心智，游击战则是把战场缩到自己绝对能守得住的局部第一。'
    },
    37
)

print("Restored and fixed exact mappings.")
