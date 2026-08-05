import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/43_组织落地：大公司如何践行“先胜后战”.svg')

# Base SVG
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1280" height="720" viewBox="0 0 1280 720" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="1280" height="720" fill="#0D1117"/>
<g id="header">
    <text x="80" y="80" font-family="'Microsoft YaHei', 'Calibri', sans-serif" font-size="36" font-weight="bold" fill="#F0F6FC">落地实战：AI 时代的大厂团队如何践行“先胜后战”？</text>
    <text x="80" y="115" font-family="'Microsoft YaHei', 'Calibri', sans-serif" font-size="20" fill="#8B949E">面对大模型迭代的极度不确定性，彻底重塑组织的决策与行动力</text>
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
        '🎯 1. 敏锐决策起点', 
        '平常心对待指标 ➔ 瞄准心智空位', 
        ['面对集团下达的 GAAP', '营收或 Token 消耗', '等指标，保持平常心。', 'AI 时代技术同质化快，', '切忌盲目卷底层模型，', '优先寻找外部心智空位。'], 
        '#00D2FF'
    ),
    (
        '🛡️ 2. 独立决策战场', 
        '不打全面战 ➔ 找准场景侧翼', 
        ['不要动辄做“AI 颠覆', '世界”的全能型产品。', '必须为你的产品找一个', '明确的垂类场景假想敌，', '在极窄场景中切出一块', '无争地带。'], 
        '#3FB950'
    ),
    (
        '⚙️ 3. 超级个体与 Agent', 
        '打破深水井 ➔ 人机协同特战队', 
        ['打破按职能堆人的传统。', 'AI 时代的特战队可以只是', '“一两个真人指挥官 + 多', '个垂类 Agent”，以极低', '的内部协同成本，实现天', '级别的敏捷行动迭代。'], 
        '#FF9A00'
    ),
    (
        '👑 4. 决策层的资源杠杆', 
        '从微操技术 ➔ 乘胜追击放大器', 
        ['产品决策层不应微操具', '体用什么模型或 Prompt。', '当一线跑通场景战机后，', '应倾斜集团算力、开放核', '心数据、调用生态接口，', '将其升维为主力战。'], 
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
        'font-size': '15', 'font-weight': 'bold', 'fill': '#F0F6FC'
    })
    if '➔' in sub:
        ET.SubElement(sub_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = sub.split('➔')[0].strip()
        ET.SubElement(sub_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '22'}).text = '➔ ' + sub.split('➔')[1].strip()
    else:
        ET.SubElement(sub_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = sub

    # Separator Line
    ET.SubElement(g, '{http://www.w3.org/2000/svg}line', {
        'x1': '20', 'y1': '135', 'x2': '240', 'y2': '135',
        'stroke': '#30363D', 'stroke-width': '1'
    })
    
    # Description
    desc_t = ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '20', 'y': '165', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '16', 'fill': '#8B949E'
    })
    for j, line in enumerate(desc_lines):
        ET.SubElement(desc_t, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0' if j==0 else '24'}).text = line

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
}).text = '💡 AI 时代突围心法：决策切入点极度克制，行动上拥抱人机协同（真人+Agent），用算力与数据生态饱和攻击！'

# Footer
footer = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'footer'})
ET.SubElement(footer, '{http://www.w3.org/2000/svg}text', {
    'x': '1220', 'y': '695', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#8B949E', 'text-anchor': 'end'
}).text = 'Page 43'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P43 scaled down to product dimension successfully.")
