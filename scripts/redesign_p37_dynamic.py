import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/37_侧翼战与游击战：小厂的蓝海突围.svg')

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

# Clear everything except defs, header and footer
for child in list(root):
    if child.tag == '{http://www.w3.org/2000/svg}g':
        if child.get('id') not in ['header', 'footer']:
            root.remove(child)
            
main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'modern-layout-p37'})

# Left Panel (Flanking)
p1 = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(60, 150)'})
# Background
ET.SubElement(p1, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '550', 'height': '460', 'rx': '16',
    'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
})
# Left Accent Line
ET.SubElement(p1, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '8', 'height': '460', 'rx': '4',
    'fill': '#00D2FF'
})
# Title
ET.SubElement(p1, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '45', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '26', 'font-weight': 'bold', 'fill': '#00D2FF'
}).text = '🚀 侧翼战：无争地带的奇袭'
# Principle
ET.SubElement(p1, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '85', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'font-weight': 'bold', 'fill': '#F0F6FC'
}).text = '原则：在无争地带建立新特性，避开主力战场，抢占心智空白。'
# Divider
ET.SubElement(p1, '{http://www.w3.org/2000/svg}line', {
    'x1': '30', 'y1': '105', 'x2': '520', 'y2': '105', 'stroke': '#30363D', 'stroke-width': '2'
})

# Flanking Section 1
ET.SubElement(p1, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '145', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#58A6FF'
}).text = '📍 一、无争地带 (寻找特性、价格、形态侧翼)'
t1 = ET.SubElement(p1, '{http://www.w3.org/2000/svg}text', {
    'x': '45', 'y': '180', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#C9D1D9'
})
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '0'}).text = '• 低价/高价侧翼：每日旅馆、拼多多 / 哈根达斯'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '30'}).text = '• 小型产品侧翼：索尼第一代随身听'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '30'}).text = '• 核心特性侧翼：联邦快递“隔夜送达”'

# Flanking Section 2
ET.SubElement(p1, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '300', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#58A6FF'
}).text = '📍 二、乘胜追击 (奇袭成功后必须巩固阵地)'
t2 = ET.SubElement(p1, '{http://www.w3.org/2000/svg}text', {
    'x': '45', 'y': '335', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#C9D1D9'
})
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '0'}).text = '• 侧翼战的本质是一次“不被察觉的奇袭”'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '30'}).text = '• 目标是不被领导者察觉地建立新阵地'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '30', 'fill': '#F0F6FC', 'font-weight': 'bold'}).text = '• 取胜后倾注资源，在巨头调转枪口前建立壁垒'


# Right Panel (Guerrilla)
p2 = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(650, 150)'})
# Background
ET.SubElement(p2, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '550', 'height': '460', 'rx': '16',
    'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
})
# Left Accent Line
ET.SubElement(p2, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '8', 'height': '460', 'rx': '4',
    'fill': '#FF9A00'
})
# Title
ET.SubElement(p2, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '45', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '26', 'font-weight': 'bold', 'fill': '#FF9A00'
}).text = '🎯 游击战：小阵地的绝对第一'
# Principle
ET.SubElement(p2, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '85', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'font-weight': 'bold', 'fill': '#F0F6FC'
}).text = '原则：找到足够小、大厂不愿全力进入的阵地做绝对第一。'
# Divider
ET.SubElement(p2, '{http://www.w3.org/2000/svg}line', {
    'x1': '30', 'y1': '105', 'x2': '520', 'y2': '105', 'stroke': '#30363D', 'stroke-width': '2'
})

# Guerrilla Section 1
ET.SubElement(p2, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '145', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#F0883E'
}).text = '📍 局部第一 (守住边界，克制扩张冲动)'
t3 = ET.SubElement(p2, '{http://www.w3.org/2000/svg}text', {
    'x': '45', 'y': '180', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#C9D1D9'
})
ET.SubElement(t3, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '0'}).text = '• 地理游击：只做某个区域的绝对第一 (如茶颜悦色)'
ET.SubElement(t3, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '35'}).text = '• 人群游击：专做大厂通用产品服务不了的细碎人群'
ET.SubElement(t3, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '35'}).text = '• 行业游击：深耕极度垂直的冷门行业 (如汽配库存系统)'
ET.SubElement(t3, '{http://www.w3.org/2000/svg}tspan', {'x': '45', 'dy': '35'}).text = '• 高端游击：极高的单价，极低的销量 (如劳斯莱斯)'

# Bottom decorative element for Guerrilla
ET.SubElement(p2, '{http://www.w3.org/2000/svg}rect', {
    'x': '30', 'y': '340', 'width': '490', 'height': '80', 'rx': '8',
    'fill': '#FF9A00', 'fill-opacity': '0.1'
})
ET.SubElement(p2, '{http://www.w3.org/2000/svg}text', {
    'x': '275', 'y': '385', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'font-weight': 'bold', 'fill': '#FF9A00', 'text-anchor': 'middle'
}).text = '“永远不要去发动一场大厂必须要消灭你的战争”'


# --- Bottom Summary Banner ---
bottom = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(60, 630)'})
# Background
ET.SubElement(bottom, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1140', 'height': '60', 'rx': '16',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
# Text
ET.SubElement(bottom, '{http://www.w3.org/2000/svg}text', {
    'x': '570', 'y': '36', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#F0F6FC', 'text-anchor': 'middle'
}).text = '💡 总结：侧翼战要在无人区抢占心智，游击战则是把战场缩到自己绝对能守得住的局部第一。'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("Completely redesigned P37 layout for a modern, sleek aesthetic.")
