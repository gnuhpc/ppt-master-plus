import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/43_组织落地：大公司如何践行“先胜后战”.svg')

# Base SVG
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1280" height="720" viewBox="0 0 1280 720" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="1280" height="720" fill="#0D1117"/>
<g id="header">
    <text x="80" y="80" font-family="'Microsoft YaHei', 'Calibri', sans-serif" font-size="36" font-weight="bold" fill="#F0F6FC">组织落地：大公司如何践行“先胜后战”？</text>
    <text x="80" y="115" font-family="'Microsoft YaHei', 'Calibri', sans-serif" font-size="20" fill="#8B949E">打破 KPI 层层下压的惯性，实施四次“反直觉”的组织手术</text>
    <line x1="80" y1="135" x2="1200" y2="135" stroke="#30363D" stroke-width="2"/>
</g>
</svg>'''

with open(svg_file, 'w') as f:
    f.write(svg_content)

tree = ET.parse(svg_file)
root = tree.getroot()

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'four-pillars-layout'})

cards = [
    (
        '🎯 1. 改变目标起点', 
        '从内部指标 ➔ 扫描外部空位', 
        ['彻底抛弃“先定百亿', 'GMV目标”的做法，', '战略会的第一议题必须', '是寻找“对手无法防御', '的心智空位”。'], 
        '#00D2FF'
    ),
    (
        '🛡️ 2. 独立定义战场', 
        '赋予 BU 独立假想敌', 
        ['拒绝强迫边缘业务呼应', '集团的“宏大叙事”。', '允许产品线打侧翼战，', '让听得见炮火的一线', '去定义假想敌。'], 
        '#3FB950'
    ),
    (
        '⚙️ 3. 无边界特战队', 
        '打破部门墙，组建 Squad', 
        ['一旦验证定位，必须立刻', '抽调产研销组成跨职能', '特战队，强行打破 KPI', '竖井，用压倒性资源把', '胜机迅速钉牢。'], 
        '#FF9A00'
    ),
    (
        '👑 4. 高管角色转变', 
        '从定指标者 ➔ 资源放大器', 
        ['CEO 不应在找方向时', '瞎指挥，而应在一线验', '证胜机后，动用并购、', '公关等公司级资源将其', '升华为全盘战略。'], 
        '#A371F7'
    )
]

for i, (title, sub, desc_lines, color) in enumerate(cards):
    x_pos = 80 + i * 280
    g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': f'translate({x_pos}, 190)'})
    
    # Card Background
    ET.SubElement(g, '{http://www.w3.org/2000/svg}rect', {
        'x': '0', 'y': '0', 'width': '260', 'height': '310', 'rx': '16',
        'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
    })
    # Top Accent Line
    ET.SubElement(g, '{http://www.w3.org/2000/svg}rect', {
        'x': '0', 'y': '0', 'width': '260', 'height': '8',
        'fill': color, 'rx': '4' 
    })
    
    # Title
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '20', 'y': '50', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '20', 'font-weight': 'bold', 'fill': color
    }).text = title
    
    # Subtitle
    sub_t = ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '20', 'y': '90', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '16', 'font-weight': 'bold', 'fill': '#F0F6FC'
    })
    if '➔' in sub:
        ET.SubElement(sub_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = sub.split('➔')[0].strip()
        ET.SubElement(sub_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '24'}).text = '➔ ' + sub.split('➔')[1].strip()
    else:
        ET.SubElement(sub_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = sub

    # Separator Line
    ET.SubElement(g, '{http://www.w3.org/2000/svg}line', {
        'x1': '20', 'y1': '135', 'x2': '240', 'y2': '135',
        'stroke': '#30363D', 'stroke-width': '1'
    })
    
    # Description
    desc_t = ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '20', 'y': '170', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '16', 'fill': '#8B949E'
    })
    for j, line in enumerate(desc_lines):
        ET.SubElement(desc_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0' if j==0 else '26'}).text = line

# --- BOTTOM TAKEAWAY ---
bot_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 560)'})
# Background
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '70', 'rx': '12',
    'fill': '#1A202C', 'stroke': '#00D2FF', 'stroke-opacity': '0.5', 'stroke-width': '1'
})
# Text
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '41', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '💡 总结（落地心法）：在方向上克制（不瞎定脱离外部的愿景），在投入上暴烈（一旦找到空位，立刻饱和攻击）！'

# Footer (Standard Page Number Location)
footer = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'footer'})
ET.SubElement(footer, '{http://www.w3.org/2000/svg}text', {
    'x': '1220', 'y': '695', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#8B949E', 'text-anchor': 'end'
}).text = 'Page 43'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P43 layout generated successfully with fixed wrapping and page number.")
