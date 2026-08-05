import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/36_案例深拆：防御战（吉列与DEC）.svg')

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

# Clear everything except defs and header
for child in list(root):
    if child.tag == '{http://www.w3.org/2000/svg}g':
        if child.get('id') != 'header':
            root.remove(child)

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'modern-layout'})

# --- Top Principle Ribbon (Sleek Gradient-like styling) ---
ribbon = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 150)'})
# A sleek subtle background
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '60', 'rx': '30',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
# Left side - blue accent text
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}text', {
    'x': '60', 'y': '36', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#58A6FF'
}).text = '🛡️ 防御战原则一：延续心智资产'
# Divider
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}line', {
    'x1': '560', 'y1': '15', 'x2': '560', 'y2': '45', 'stroke': '#30363D', 'stroke-width': '2'
})
# Right side - orange accent text
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}text', {
    'x': '590', 'y': '36', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#FF9A00'
}).text = '⚔️ 防御战原则二：主动淘汰旧载体'

# --- Left Section (Cases) ---
left_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 250)'})

# Case 1 (Gillette - Success)
c1 = ET.SubElement(left_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 0)'})
# Background card
ET.SubElement(c1, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '520', 'height': '170', 'rx': '12',
    'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
})
# Left Accent Line (Green for Success)
ET.SubElement(c1, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '8', 'height': '170', 'rx': '4',
    'fill': '#2EA043'
})
# Title
ET.SubElement(c1, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#2EA043'
}).text = '✅ 吉列：自我迭代，成功防御'
# Text content
t1 = ET.SubElement(c1, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '75', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#C9D1D9'
})
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '0'}).text = '• 旧优势：蓝吉列已建立绝对领导地位'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '30'}).text = '• 新威胁：威尔金森等利用新技术切入'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '30', 'fill': '#F0F6FC', 'font-weight': 'bold'}).text = '• 关键动作：用新产品线主动吃掉自己旧产品的利润'

# Case 2 (DEC - Failure)
c2 = ET.SubElement(left_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 200)'})
# Background card
ET.SubElement(c2, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '520', 'height': '170', 'rx': '12',
    'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
})
# Left Accent Line (Red for Failure)
ET.SubElement(c2, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '8', 'height': '170', 'rx': '4',
    'fill': '#F85149'
})
# Title
ET.SubElement(c2, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#F85149'
}).text = '❌ DEC：眷恋旧利，惨遭颠覆'
# Text content
t2 = ET.SubElement(c2, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '75', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#C9D1D9'
})
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '0'}).text = '• 旧优势：小型机侧翼战成功，称霸一方'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '30'}).text = '• 新威胁：个人电脑(PC)改变了计算入口'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '30', 'fill': '#F0F6FC', 'font-weight': 'bold'}).text = '• 致命误判：迟迟不愿用下一代产品攻击自己的利润池'


# --- Right Section (Strategic Tension Diagram) ---
# A dynamic interconnected layout representing tension
right_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(660, 250)'})

# Center title
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
    'x': '270', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '24', 'font-weight': 'bold', 'fill': '#F0F6FC', 'text-anchor': 'middle'
}).text = '核心张力：守住位置 vs 换掉载体'

# Dynamic Graphic Element
graphic_g = ET.SubElement(right_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 40)'})

# Connection Line
ET.SubElement(graphic_g, '{http://www.w3.org/2000/svg}path', {
    'd': 'M 135 70 L 405 70', 'stroke': '#30363D', 'stroke-width': '4', 'stroke-dasharray': '8,8'
})

# Keep Node (Left)
k_node = ET.SubElement(graphic_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(10, 20)'})
ET.SubElement(k_node, '{http://www.w3.org/2000/svg}circle', {
    'cx': '125', 'cy': '50', 'r': '70', 'fill': '#00D2FF', 'fill-opacity': '0.1',
    'stroke': '#00D2FF', 'stroke-width': '2'
})
ET.SubElement(k_node, '{http://www.w3.org/2000/svg}text', {
    'x': '125', 'y': '25', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '要延续'
tk = ET.SubElement(k_node, '{http://www.w3.org/2000/svg}text', {
    'x': '125', 'y': '55', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#F0F6FC', 'text-anchor': 'middle'
})
ET.SubElement(tk, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '0'}).text = '心智位置'
ET.SubElement(tk, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '24'}).text = '品牌信任'
ET.SubElement(tk, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '24'}).text = '活动系统'

# Discard Node (Right)
d_node = ET.SubElement(graphic_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(280, 20)'})
ET.SubElement(d_node, '{http://www.w3.org/2000/svg}circle', {
    'cx': '125', 'cy': '50', 'r': '70', 'fill': '#FF9A00', 'fill-opacity': '0.1',
    'stroke': '#FF9A00', 'stroke-width': '2'
})
ET.SubElement(d_node, '{http://www.w3.org/2000/svg}text', {
    'x': '125', 'y': '25', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#FF9A00', 'text-anchor': 'middle'
}).text = '要淘汰'
td = ET.SubElement(d_node, '{http://www.w3.org/2000/svg}text', {
    'x': '125', 'y': '55', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#F0F6FC', 'text-anchor': 'middle'
})
ET.SubElement(td, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '0'}).text = '旧产品形态'
ET.SubElement(td, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '24'}).text = '旧流量入口'
ET.SubElement(td, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '24'}).text = '旧利润依赖'

# Center Balance Icon
ET.SubElement(graphic_g, '{http://www.w3.org/2000/svg}circle', {
    'cx': '270', 'cy': '70', 'r': '25', 'fill': '#21262D', 'stroke': '#30363D', 'stroke-width': '3'
})
ET.SubElement(graphic_g, '{http://www.w3.org/2000/svg}text', {
    'x': '270', 'y': '78', 'font-family': "'Arial Black', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#8B949E', 'text-anchor': 'middle'
}).text = 'VS'

# Bottom Rules / Strategy Output
rc = ET.SubElement(right_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 230)'})
# A sleek floating panel
ET.SubElement(rc, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '540', 'height': '140', 'rx': '12',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
r_text = ET.SubElement(rc, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#C9D1D9'
})
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '0', 'fill': '#00D2FF', 'font-weight': 'bold'}).text = '📌 情况一：新载体能强化原有心智'
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '25'}).text = '     对策：直接升级主阵地，用新品自我替换。'
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '40', 'fill': '#FF9A00', 'font-weight': 'bold'}).text = '📌 情况二：新旧冲突明显（破坏原有活动系统）'
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '25'}).text = '     对策：建立独立品牌，或用独立团队/系统承接。'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("Completely redesigned P36 layout for modern dynamic aesthetic.")
