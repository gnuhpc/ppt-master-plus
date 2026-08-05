import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/38_案例深拆：侧翼战（Abridge临床文书）.svg')

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

# Clear everything except defs and header
for child in list(root):
    if child.tag == '{http://www.w3.org/2000/svg}g' and child.get('id') != 'header':
        root.remove(child)

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'modern-flank-layout'})

# --- Section 1: The Strategic Avoidance (Top) ---
top_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 150)'})

# Frontal Assault (Red)
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '450', 'height': '120', 'rx': '12',
    'fill': '#F85149', 'fill-opacity': '0.1', 'stroke': '#F85149', 'stroke-width': '1.5'
})
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '20', 'y': '35', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#F85149'
}).text = '🔥 巨头正面战场：通用AI助手'
t1 = ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '20', 'y': '70', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#C9D1D9'
})
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '0'}).text = '• 竞争焦点：模型参数、底层算力、全场景入口'
ET.SubElement(t1, '{http://www.w3.org/2000/svg}tspan', {'x': '20', 'dy': '25'}).text = '• Abridge 战略：绝不去做一个小号的 ChatGPT'

# Arrow in middle
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}path', {
    'd': 'M 480 60 L 520 60 M 510 50 L 520 60 L 510 70',
    'stroke': '#8B949E', 'stroke-width': '3', 'fill': 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round'
})
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '500', 'y': '45', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '14', 'fill': '#8B949E', 'text-anchor': 'middle'
}).text = '避开火力'

# Flanking Position (Cyan)
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '550', 'y': '0', 'width': '570', 'height': '120', 'rx': '12',
    'fill': '#00D2FF', 'fill-opacity': '0.1', 'stroke': '#00D2FF', 'stroke-width': '1.5'
})
ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '570', 'y': '35', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#00D2FF'
}).text = '🚀 侧翼奇袭：Abridge 的无争地带'
t2 = ET.SubElement(top_g, '{http://www.w3.org/2000/svg}text', {
    'x': '570', 'y': '70', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'fill': '#C9D1D9'
})
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '570', 'dy': '0'}).text = '• 定位：医疗临床文书生成的专属助手 (Ambient AI)'
ET.SubElement(t2, '{http://www.w3.org/2000/svg}tspan', {'x': '570', 'dy': '25'}).text = '• 特性：切入医生最痛苦、巨头又看不上的“写病历”高频场景'


# --- Section 2: The Moat / Workflow (Middle) ---
mid_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 310)'})
ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '0', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#F0F6FC'
}).text = '侧翼壁垒：如何让巨头进不来？'

# Create a 4-step process timeline
steps = [
    ('1. 任务极窄化', '🎤 诊室对话', '非开放式闲聊，只做医患对话转录与结构化'),
    ('2. 信任门槛', '🔍 证据可追溯', '所有生成的病历必须能逐字追溯到原始录音'),
    ('3. 工作流嵌入', '🏥 写回 EHR', '不是独立的聊天框，而是直接集成进医院系统'),
    ('4. 乘胜追击', '📈 场景扩张', '成功后迅速扩张至护理记录、医疗计费摘要')
]

for i, (title, icon_text, desc) in enumerate(steps):
    x_pos = i * 285
    # Card
    ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}rect', {
        'x': str(x_pos), 'y': '20', 'width': '265', 'height': '150', 'rx': '10',
        'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
    })
    # Step Number / Title (Accent color)
    ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}text', {
        'x': str(x_pos + 15), 'y': '50', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '18', 'font-weight': 'bold', 'fill': '#FF9A00' if i==3 else '#58A6FF'
    }).text = title
    # Core Concept
    ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}text', {
        'x': str(x_pos + 15), 'y': '85', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '20', 'font-weight': 'bold', 'fill': '#F0F6FC'
    }).text = icon_text
    # Description (with multi-line wrap if needed)
    words = desc.split('，') if '，' in desc else desc.split('、') if '、' in desc else [desc[:12], desc[12:]]
    if len(desc) < 14: words = [desc]
    
    dt = ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}text', {
        'x': str(x_pos + 15), 'y': '120', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '14', 'fill': '#8B949E'
    })
    
    # Handle simple text wrap for the short descriptions
    if len(desc) > 16:
        ET.SubElement(dt, '{http://www.w3.org/2000/svg}tspan', {'x': str(x_pos + 15), 'dy': '0'}).text = desc[:14]
        ET.SubElement(dt, '{http://www.w3.org/2000/svg}tspan', {'x': str(x_pos + 15), 'dy': '20'}).text = desc[14:]
    else:
        ET.SubElement(dt, '{http://www.w3.org/2000/svg}tspan', {'x': str(x_pos + 15), 'dy': '0'}).text = desc

    # Draw arrow between steps
    if i < 3:
        ET.SubElement(mid_g, '{http://www.w3.org/2000/svg}path', {
            'd': f'M {x_pos + 270} 95 L {x_pos + 280} 95 M {x_pos + 276} 91 L {x_pos + 280} 95 L {x_pos + 276} 99',
            'stroke': '#8B949E', 'stroke-width': '2', 'fill': 'none'
        })

# --- Section 3: Bottom Takeaway ---
bot_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 540)'})
# Background
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '80', 'rx': '12',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
# Text
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '46', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '22', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = '💡 侧翼战的关键洞察：极窄任务不是因为“市场小”，而是因为它最容易重构工作流，形成默认入口。'

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P38 completely redesigned for maximum logical clarity and visual appeal.")
