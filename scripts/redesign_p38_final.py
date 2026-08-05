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

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'comprehensive-abridge-layout'})

# --- LEFT COLUMN: The Flanking Pipeline ---
left_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 160)'})

# Title for Pipeline
ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
    'x': '150', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '🚀 侧翼突围路径'

# The Pipeline Nodes (Vertical)
pipeline = [
    ('🎤', '诊间对话采集', 'Point of care 原声采集'),
    ('📝', '结构化临床笔记', '医疗语境 AI 自动生成'),
    ('🏥', 'EHR 系统写入', '深度融入病历工作流'),
    ('💰', '计费与运营流程', '形成临床到运营的闭环')
]

for i, (icon, title, desc) in enumerate(pipeline):
    y_pos = 50 + i * 110
    
    # Connecting Line
    if i < 3:
        ET.SubElement(left_g, '{http://www.w3.org/2000/svg}line', {
            'x1': '150', 'y1': str(y_pos + 60), 'x2': '150', 'y2': str(y_pos + 110),
            'stroke': '#30363D', 'stroke-width': '4'
        })
        # Arrowhead
        ET.SubElement(left_g, '{http://www.w3.org/2000/svg}polygon', {
            'points': f'145,{y_pos + 95} 155,{y_pos + 95} 150,{y_pos + 105}',
            'fill': '#30363D'
        })
    
    # Card
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}rect', {
        'x': '0', 'y': str(y_pos), 'width': '300', 'height': '70', 'rx': '35',
        'fill': '#161B22', 'stroke': '#00D2FF', 'stroke-width': '1.5'
    })
    
    # Icon Circle
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}circle', {
        'cx': '35', 'cy': str(y_pos + 35), 'r': '25', 'fill': '#00D2FF', 'fill-opacity': '0.1'
    })
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
        'x': '35', 'y': str(y_pos + 42), 'font-family': "'Microsoft YaHei', sans-serif",
        'font-size': '20', 'fill': '#00D2FF', 'text-anchor': 'middle'
    }).text = icon
    
    # Text
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
        'x': '75', 'y': str(y_pos + 30), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '18', 'font-weight': 'bold', 'fill': '#F0F6FC'
    }).text = title
    ET.SubElement(left_g, '{http://www.w3.org/2000/svg}text', {
        'x': '75', 'y': str(y_pos + 52), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '14', 'fill': '#8B949E'
    }).text = desc


# --- RIGHT COLUMN: The 5 Moats ---
right_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(450, 160)'})

# Title for Moats
ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#FF9A00'
}).text = '🛡️ 侧翼战五大核心壁垒'

moats = [
    ('01', '医疗语境专用化', '摒弃开放聊天，专攻临床表达、专科术语及多语言环境，形成专业门槛。'),
    ('02', '深度嵌入 EHR', '集成至 Epic 等原生工作流 (Haiku/Hyperspace)，而非独立工具。'),
    ('03', '信任与可审计 (Linked Evidence)', '医疗文书容错率为零，生成内容必须能逐字映射回原始录音证据。'),
    ('04', '企业级部署势能', '合作超 150 家医疗系统 (如 Mayo Clinic)，建立实施经验与客户壁垒。'),
    ('05', '向运营闭环延伸', '占领阵地后，向护理、住院、收入周期智能延伸，加深系统护城河。')
]

for i, (num, title, desc) in enumerate(moats):
    y_pos = 40 + i * 85
    
    # Background Bar
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}rect', {
        'x': '0', 'y': str(y_pos), 'width': '750', 'height': '70', 'rx': '10',
        'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1'
    })
    
    # Number Badge
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}rect', {
        'x': '15', 'y': str(y_pos + 15), 'width': '40', 'height': '40', 'rx': '8',
        'fill': '#FF9A00', 'fill-opacity': '0.1'
    })
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
        'x': '35', 'y': str(y_pos + 41), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '18', 'font-weight': 'bold', 'fill': '#FF9A00', 'text-anchor': 'middle'
    }).text = num
    
    # Title
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
        'x': '75', 'y': str(y_pos + 31), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '18', 'font-weight': 'bold', 'fill': '#F0F6FC'
    }).text = title
    
    # Description
    ET.SubElement(right_g, '{http://www.w3.org/2000/svg}text', {
        'x': '75', 'y': str(y_pos + 53), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '14', 'fill': '#8B949E'
    }).text = desc


# --- BOTTOM TAKEAWAY ---
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
}).text = '💡 总结：侧翼战的“窄”不是市场想象力小，而是战略入口更尖。找准痛点深、门槛高、易延展的无争地带。'


tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P38 perfectly aligned with speaker notes.")
