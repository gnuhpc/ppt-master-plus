import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/36_案例深拆：防御战（吉列与DEC）.svg')

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

# Preserve definitions and standard headers, rewrite main layout
# Find header, ribbon, case-left, balance-right and remove all except header and defs
for child in list(root):
    if child.tag == '{http://www.w3.org/2000/svg}g':
        child_id = child.get('id', '')
        if child_id in ['layout-pattern', 'principle-ribbon', 'case-left', 'balance-right']:
            root.remove(child)

# We will create a fresh clean layout group
main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'clean-layout'})

# --- Top Principle Ribbon ---
ribbon = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 150)'})
# bg
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '60', 'rx': '8',
    'fill': '#161B22', 'stroke': '#30363D'
})
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '35', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#00D2FF'
}).text = '延续心智资产，替换兑现方式'
ET.SubElement(ribbon, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '35', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#FF9A00'
}).text = '淘汰旧载体，不是推翻优势本身'


# --- Left Section (Cases) ---
left_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 240)'})
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#F0F6FC'
}).text = '案例判断：同样面对新战场，领导者走向不同'

# Case 1 (Gillette)
c1 = ET.SubElement(left_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 30)'})
ET.SubElement(c1, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '530', 'height': '160', 'rx': '12',
    'fill': '#161B22', 'stroke': '#00D2FF', 'stroke-width': '1.5'
})
ET.SubElement(c1, '{http://www.w3.org/2000/svg}text', {
    'x': '20', 'y': '35', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#00D2FF'
}).text = '吉列：用新品刷新领导者含义'
t1 = ET.SubElement(c1, '{http://www.w3.org/2000/svg}text', {
    'x': '20', 'y': '70', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#F0F6FC'
})
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = '• 旧优势：蓝吉列已建立剃须刀领导心智'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '30'}).text = '• 威胁：威尔金森等从新技术和一次性产品切入'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '30'}).text = '• 动作：Trac II主动吃掉旧产品 → 成功守住品类代表'

# Case 2 (DEC)
c2 = ET.SubElement(left_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 210)'})
ET.SubElement(c2, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '530', 'height': '160', 'rx': '12',
    'fill': '#161B22', 'stroke': '#FF9A00', 'stroke-width': '1.5'
})
ET.SubElement(c2, '{http://www.w3.org/2000/svg}text', {
    'x': '20', 'y': '35', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#FF9A00'
}).text = 'DEC：未完成从侧翼到防御的转换'
t2 = ET.SubElement(c2, '{http://www.w3.org/2000/svg}text', {
    'x': '20', 'y': '70', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#F0F6FC'
})
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = '• 旧优势：小型机成功进入领导地位'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '30'}).text = '• 威胁：个人电脑改变计算入口与价格结构'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '30'}).text = '• 误判：眷恋利润池，未用下一代产品攻击自己 → 被颠覆'


# --- Right Section (Strategic Tension) ---
right_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(670, 240)'})
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#F0F6FC'
}).text = '战略张力：守住位置，换掉载体'

# Tension Cards
tc = ET.SubElement(right_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 30)'})

# Keep
ET.SubElement(tc, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '250', 'height': '160', 'rx': '12',
    'fill': '#00D2FF', 'fill-opacity': '0.1'
})
ET.SubElement(tc, '{http://www.w3.org/2000/svg}text', {
    'x': '125', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '要延续'
tk = ET.SubElement(tc, '{http://www.w3.org/2000/svg}text', {
    'x': '125', 'y': '85', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#F0F6FC', 'text-anchor': 'middle'
})
ET.SubElement(tk, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '0'}).text = '心智位置'
ET.SubElement(tk, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '30'}).text = '品牌信任'
ET.SubElement(tk, '{http://www.w3.org/2000/svg}tspan', {'x': '125', 'dy': '30'}).text = '活动系统'

# Discard
ET.SubElement(tc, '{http://www.w3.org/2000/svg}rect', {
    'x': '280', 'y': '0', 'width': '250', 'height': '160', 'rx': '12',
    'fill': '#FF9A00', 'fill-opacity': '0.1'
})
ET.SubElement(tc, '{http://www.w3.org/2000/svg}text', {
    'x': '405', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#FF9A00', 'text-anchor': 'middle'
}).text = '要淘汰'
td = ET.SubElement(tc, '{http://www.w3.org/2000/svg}text', {
    'x': '405', 'y': '85', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#F0F6FC', 'text-anchor': 'middle'
})
ET.SubElement(td, '{http://www.w3.org/2000/svg}tspan', {'x': '405', 'dy': '0'}).text = '旧产品形态'
ET.SubElement(td, '{http://www.w3.org/2000/svg}tspan', {'x': '405', 'dy': '30'}).text = '旧入口'
ET.SubElement(td, '{http://www.w3.org/2000/svg}tspan', {'x': '405', 'dy': '30'}).text = '旧利润依赖'

# Rules
rc = ET.SubElement(right_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(0, 210)'})
ET.SubElement(rc, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '530', 'height': '160', 'rx': '12',
    'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
})
r_text = ET.SubElement(rc, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#F0F6FC'
})
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '0', 'fill': '#00D2FF'}).text = '情况一：能强化原有心智'
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '30', 'font-weight': 'normal'}).text = '    对策：直接升级主阵地，自我替换'
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '45', 'fill': '#FF9A00'}).text = '情况二：新旧冲突明显（破坏原有系统）'
ET.SubElement(r_text, '{http://www.w3.org/2000/svg}tspan', {'x': '30', 'dy': '30', 'font-weight': 'normal'}).text = '    对策：用独立品牌或独立系统承接'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("Completely redesigned P36 layout for maximum clarity and beauty.")
