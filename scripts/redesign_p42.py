import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/42_先胜而后求战的逻辑顺序.svg')

ET.register_namespace('', 'http://www.w3.org/2000/svg')
tree = ET.parse(svg_file)
root = tree.getroot()

# Clear everything except defs and header
for child in list(root):
    if child.tag == '{http://www.w3.org/2000/svg}g' and child.get('id') != 'header':
        root.remove(child)

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'compare-layout'})

# --- LEFT PANEL: The Wrong Way ---
left_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 160)'})

# Background
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '500', 'height': '440', 'rx': '16',
    'fill': '#161B22', 'stroke': '#F85149', 'stroke-opacity': '0.3', 'stroke-width': '2'
})

# Title
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
    'x': '250', 'y': '45', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '24', 'font-weight': 'bold', 'fill': '#F85149', 'text-anchor': 'middle'
}).text = '❌ 战略因果倒置 (先战后胜)'

# Subtitle
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
    'x': '250', 'y': '75', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#8B949E', 'text-anchor': 'middle'
}).text = '高管视角的“自上而下”推演'

# Top-Down Flow
boxes = [
    (110, '公司先设宏大目标', '#21262D'),
    (200, '把缺口分解到各个业务', '#21262D'),
    (290, '最后才面对外部强敌与心智', '#F85149')  # The collision point
]
for y, text, color in boxes:
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}rect', {
        'x': '80', 'y': str(y), 'width': '340', 'height': '50', 'rx': '8', 'fill': color
    })
    fill_color = '#FFFFFF' if color == '#F85149' else '#C9D1D9'
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
        'x': '250', 'y': str(y + 31), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '18', 'font-weight': 'bold', 'fill': fill_color, 'text-anchor': 'middle'
    }).text = text

# Arrows
for y in [160, 250]:
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}path', {
        'd': f'M 250 {y} L 250 {y+40} M 245 {y+35} L 250 {y+40} L 255 {y+35}',
        'stroke': '#8B949E', 'stroke-width': '2', 'fill': 'none'
    })

# Takeaway Warning
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '30', 'y': '370', 'width': '440', 'height': '45', 'rx': '6',
    'fill': '#F85149', 'fill-opacity': '0.1'
})
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
    'x': '250', 'y': '398', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'font-weight': 'bold', 'fill': '#F85149', 'text-anchor': 'middle'
}).text = '问题：内部愿景很兴奋，外部竞争不承认！'


# --- RIGHT PANEL: The Right Way ---
right_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(620, 160)'})

# Background
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '580', 'height': '440', 'rx': '16',
    'fill': '#161B22', 'stroke': '#00D2FF', 'stroke-opacity': '0.5', 'stroke-width': '2'
})

# Title
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
    'x': '290', 'y': '45', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '24', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '✅ 正确顺序：先胜后战 (由下而上)'

# Subtitle
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
    'x': '290', 'y': '75', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#8B949E', 'text-anchor': 'middle'
}).text = '基于外部竞争现实的“自下而上”构建'

# Bottom-Up Steps (Pyramid style)
steps = [
    (120, '3', '公司战略', '服务竞争战略 (只能强化已经被验证的定位)'),
    (200, '2', '资源追击', '活动系统配称 (把胜机钉牢)'),
    (280, '1', '定位机会', '发现外部心智空位 (先胜！)')
]

for y, num, title, desc in steps:
    width = 300 if num == '3' else 400 if num == '2' else 500
    x_start = 290 - width / 2
    
    # Step Box
    color = '#00D2FF' if num == '1' else '#1F6FEB' if num == '2' else '#388BFD'
    opacity = '0.3' if num == '1' else '0.2' if num == '2' else '0.1'
    
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}rect', {
        'x': str(x_start), 'y': str(y), 'width': str(width), 'height': '60', 'rx': '8',
        'fill': color, 'fill-opacity': opacity, 'stroke': color, 'stroke-width': '1'
    })
    
    # Step Text
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
        'x': str(x_start + 20), 'y': str(y + 36), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '20', 'font-weight': 'bold', 'fill': color
    }).text = f'第{num}步：{title}'
    
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
        'x': str(x_start + 180), 'y': str(y + 35), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '16', 'fill': '#C9D1D9'
    }).text = desc

# Upward arrows between steps
for y in [180, 260]:
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}path', {
        'd': f'M 290 {y+20} L 290 {y} M 285 {y+5} L 290 {y} L 295 {y+5}',
        'stroke': '#00D2FF', 'stroke-width': '2', 'fill': 'none'
    })

# Takeaway Warning
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '30', 'y': '370', 'width': '520', 'height': '45', 'rx': '6',
    'fill': '#00D2FF', 'fill-opacity': '0.1'
})
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
    'x': '290', 'y': '398', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '💡 结论：公司战略绝不能替代竞争定位！'

# --- BOTTOM TAKEAWAY (Full width) ---
bot_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 630)'})
# Background
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '50', 'rx': '10',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
# Text
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '31', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'font-weight': 'bold', 'fill': '#C9D1D9', 'text-anchor': 'middle'
}).text = '战略的本质是回到外部竞争：先有定位机会（胜机），再配置资源形成追击（求战）。'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P42 completely redesigned for clear, visual logic flow.")
