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

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'chevron-layout'})

# --- 1. TOP ALERT BANNER (The Wrong Way) ---
top_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 150)'})

ET.SubElement(top_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '70', 'rx': '12',
    'fill': '#161B22', 'stroke': '#F85149', 'stroke-width': '1', 'stroke-dasharray': '5,5'
})
# Text
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '30', 'y': '42', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'font-weight': 'bold', 'fill': '#F85149'
}).text = '❌ 战略因果倒置：'

ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '190', 'y': '42', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '18', 'fill': '#8B949E'
}).text = '公司设定宏大愿景 ➔ 将缺口拆解给各业务 ➔ 最终面对强敌 (结果：内部愿景很兴奋，外部竞争不承认)'


# --- 2. MAIN CANVAS (The Right Way - Chevrons) ---
mid_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 280)'})

# Main Title
ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '24', 'font-weight': 'bold', 'fill': '#00D2FF'
}).text = '✅ 正确顺序：先胜而后求战 (由下而上)'


chevron_width = 320
chevron_height = 180
arrow_tip = 45

# Function to create chevron path
def get_chevron_path(is_first=False):
    if is_first:
        return f'M 0,0 L {chevron_width},0 L {chevron_width + arrow_tip},{chevron_height/2} L {chevron_width},{chevron_height} L 0,{chevron_height} Z'
    else:
        return f'M 0,0 L {chevron_width},0 L {chevron_width + arrow_tip},{chevron_height/2} L {chevron_width},{chevron_height} L 0,{chevron_height} L {arrow_tip},{chevron_height/2} Z'

steps = [
    ('1. 定位机会', '外部心智空位', '发现未被占领的心智，实现“先胜”', '#00D2FF'),
    ('2. 资源追击', '活动系统配称', '投入资源构建壁垒，把胜机“钉牢”', '#1F6FEB'),
    ('3. 公司战略', '服务竞争战略', '公司级资源统筹，强化既定定位', '#388BFD')
]

for i, (title, subtitle, desc, color) in enumerate(steps):
    # Overlap them slightly (spacing = chevron_width - 10)
    x_pos = i * (chevron_width + 10)
    g = ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}g', {'transform': f'translate({x_pos}, 40)'})
    
    # Shadow
    ET.SubElement(g, '{http://www.w3.org/2000/svg}path', {
        'd': get_chevron_path(is_first=(i==0)),
        'fill': '#000000', 'fill-opacity': '0.3',
        'transform': 'translate(5, 5)'
    })
    
    # Main Shape
    ET.SubElement(g, '{http://www.w3.org/2000/svg}path', {
        'd': get_chevron_path(is_first=(i==0)),
        'fill': '#161B22', 'stroke': color, 'stroke-width': '2'
    })
    
    # Inside Highlight Line
    ET.SubElement(g, '{http://www.w3.org/2000/svg}path', {
        'd': f'M {arrow_tip + 10 if i>0 else 10},{chevron_height-4} L {chevron_width-4},{chevron_height-4} L {chevron_width + arrow_tip - 8},{chevron_height/2} L {chevron_width-4},4 L {arrow_tip + 10 if i>0 else 10},4',
        'fill': 'none', 'stroke': color, 'stroke-opacity': '0.2', 'stroke-width': '8'
    })
    
    text_x = 60 if i == 0 else 80
    
    # Step Number Background
    ET.SubElement(g, '{http://www.w3.org/2000/svg}rect', {
        'x': str(text_x), 'y': '30', 'width': '40', 'height': '40', 'rx': '8',
        'fill': color, 'fill-opacity': '0.2'
    })
    
    # Title
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': str(text_x + 60), 'y': '58', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '22', 'font-weight': 'bold', 'fill': color
    }).text = title
    
    # Subtitle
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': str(text_x), 'y': '100', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '20', 'font-weight': 'bold', 'fill': '#F0F6FC'
    }).text = subtitle
    
    # Description (Wrap text to avoid overflow)
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': str(text_x), 'y': '135', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '15', 'fill': '#8B949E'
    }).text = desc


# --- 3. BOTTOM TAKEAWAY ---
bot_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 600)'})
# Background
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '70', 'rx': '12',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
# Text (split into two lines to prevent overflow if it's too long, but it's short enough for 1120 width)
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '42', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#C9D1D9', 'text-anchor': 'middle'
}).text = '💡 核心洞察：公司战略绝对不能替代竞争定位；它只能强化已经被外部验证的定位机会。'


tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P42 Chevron layout implemented to fix overflow and improve aesthetics.")
