import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/38_案例深拆：侧翼战（Abridge临床文书）.svg')

ET.register_namespace('', 'http://www.w3.org/2000/svg')
tree = ET.parse(svg_file)
root = tree.getroot()

# Clear everything except defs and header
for child in list(root):
    if child.tag == '{http://www.w3.org/2000/svg}g' and child.get('id') != 'header':
        root.remove(child)

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'clean-dashboard-layout'})

# --- 1. Top Shift Banner ---
top_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 150)'})

# A single elegant horizontal panel for the strategic shift
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '90', 'rx': '12',
    'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
})

# Left part of banner: The giant's focus
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '40', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#8B949E'
}).text = '🔥 巨头正面战场'
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '40', 'y': '70', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#6E7681'
}).text = '通用助手 (拼参数 / 拼算力 / 拼生态)'

# Middle Arrow
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}path', {
    'd': 'M 400 45 L 700 45 M 685 35 L 700 45 L 685 55',
    'stroke': '#30363D', 'stroke-width': '3', 'fill': 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'
})
# Arrow Label
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '490', 'y': '30', 'width': '120', 'height': '30', 'rx': '15',
    'fill': '#21262D'
})
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '550', 'y': '51', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '14', 'font-weight': 'bold', 'fill': '#C9D1D9', 'text-anchor': 'middle'
}).text = '避开火力，寻找无争'

# Right part of banner: The flank
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '1080', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'end'
}).text = '🚀 Abridge 侧翼奇袭'
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '1080', 'y': '70', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#C9D1D9', 'text-anchor': 'end'
}).text = '医疗临床文书 (切入医生最痛的高频场景)'


# --- 2. Middle Area (The 3 Moat Pillars) ---
mid_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 280)'})
# Section Title
ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#F0F6FC', 'text-anchor': 'middle'
}).text = '如何让巨头进不来？ (建立侧翼壁垒)'

cards = [
    ('🎯 任务极窄化', '只做医患诊室对话转录', '不做发散性聊天，将任务边界缩到最小，从而实现极高的垂直准确率。', '#58A6FF'),
    ('🛡️ 信任高门槛', '证据逐字可追溯', '医疗场景容错率为零，所有生成的病历必须能反向追溯到原始音频证据。', '#3FB950'),
    ('⚙️ 工作流嵌入', '直连 EHR 系统', '不是一个需要单独打开的网页，而是深嵌入医生工作流的底层工具。', '#FF9A00')
]

for i, (title, sub, desc, color) in enumerate(cards):
    x_pos = i * 380
    g = ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}g', {'transform': f'translate({x_pos}, 30)'})
    
    # Card Background
    ET.SubElement(g, '{http://www.w3.org/2000/svg}rect', {
        'x': '0', 'y': '0', 'width': '360', 'height': '180', 'rx': '12',
        'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
    })
    # Top Accent Line
    ET.SubElement(g, '{http://www.w3.org/2000/svg}rect', {
        'x': '0', 'y': '0', 'width': '360', 'height': '6',
        'fill': color, 'rx': '3'  # Simple top border highlight
    })
    
    # Title
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '30', 'y': '45', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '22', 'font-weight': 'bold', 'fill': color
    }).text = title
    
    # Subtitle
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '30', 'y': '80', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '18', 'font-weight': 'bold', 'fill': '#F0F6FC'
    }).text = sub
    
    # Description (Wrap text)
    desc_t = ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '30', 'y': '120', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '15', 'fill': '#8B949E'
    })
    mid_idx = len(desc) // 2
    part1, part2 = desc[:mid_idx], desc[mid_idx:]
    # Smarter split around punctuation
    if '，' in desc:
        part1, part2 = desc.split('，', 1)
        part1 += '，'
        
    ET.SubElement(desc_t, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '0'}).text = part1
    ET.SubElement(desc_t, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '24'}).text = part2


# --- 3. Bottom Expansion & Takeaway ---
bot_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 530)'})

# Expansion Bar
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '50', 'rx': '8',
    'fill': '#1F242C', 'stroke': '#30363D', 'stroke-width': '1'
})
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '31', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'font-weight': 'bold', 'fill': '#A5D6FF', 'text-anchor': 'middle'
}).text = '▶ 乘胜追击：通过极窄入口形成壁垒后，逐步扩展至护理记录与医疗计费摘要。'

# Takeaway Bar
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '70', 'width': '1120', 'height': '60', 'rx': '12',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '106', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#C9D1D9', 'text-anchor': 'middle'
}).text = '💡 侧翼战的核心：极窄任务绝不是“市场小”，而是重构工作流、形成默认入口的最锐利武器。'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P38 redesigned to a clean, professional symmetric 3-card dashboard.")
