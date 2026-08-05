import os
import math
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

# Add defs for glows and gradients
defs = root.find('{http://www.w3.org/2000/svg}defs')
if defs is None:
    defs = ET.SubElement(root, '{http://www.w3.org/2000/svg}defs')

# Glow filters
filter_cyan = ET.SubElement(defs, '{http://www.w3.org/2000/svg}filter', {'id': 'glow-cyan', 'x': '-20%', 'y': '-20%', 'width': '140%', 'height': '140%'})
ET.SubElement(filter_cyan, '{http://www.w3.org/2000/svg}feGaussianBlur', {'stdDeviation': '8', 'result': 'blur'})
ET.SubElement(filter_cyan, '{http://www.w3.org/2000/svg}feComposite', {'in': 'SourceGraphic', 'in2': 'blur', 'operator': 'over'})

filter_red = ET.SubElement(defs, '{http://www.w3.org/2000/svg}filter', {'id': 'glow-red', 'x': '-20%', 'y': '-20%', 'width': '140%', 'height': '140%'})
ET.SubElement(filter_red, '{http://www.w3.org/2000/svg}feGaussianBlur', {'stdDeviation': '12', 'result': 'blur'})
ET.SubElement(filter_red, '{http://www.w3.org/2000/svg}feComposite', {'in': 'SourceGraphic', 'in2': 'blur', 'operator': 'over'})

main_g = ET.SubElement(root, '{http://www.w3.org/2000/svg}g', {'id': 'organic-trajectory-layout'})

# --- 1. The Red Ocean (General AI Battlefield) at bottom left ---
red_ocean = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(150, 500)'})
# A chaotic cluster of overlapping circles
for r, opac in [(120, '0.05'), (80, '0.1'), (50, '0.2')]:
    ET.SubElement(red_ocean, '{http://www.w3.org/2000/svg}circle', {
        'cx': '0', 'cy': '0', 'r': str(r), 'fill': '#F85149', 'fill-opacity': opac
    })
ET.SubElement(red_ocean, '{http://www.w3.org/2000/svg}circle', {
    'cx': '0', 'cy': '0', 'r': '30', 'fill': '#F85149', 'filter': 'url(#glow-red)'
})
ET.SubElement(red_ocean, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '80', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#F85149', 'text-anchor': 'middle'
}).text = '正面战场：通用大模型'
ET.SubElement(red_ocean, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '105', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '14', 'fill': '#8B949E', 'text-anchor': 'middle'
}).text = '拼参数 / 拼算力 / 拼生态'

# --- 2. The Trajectory (The Flanking Maneuver) ---
# A sweeping swoosh from bottom-left to top-right
ET.SubElement(main_g, '{http://www.w3.org/2000/svg}path', {
    'd': 'M 150 450 C 300 200, 600 150, 950 150',
    'stroke': '#00D2FF', 'stroke-width': '4', 'fill': 'none',
    'stroke-dasharray': '8 4', 'stroke-linecap': 'round',
    'filter': 'url(#glow-cyan)'
})
# Trajectory Label
ET.SubElement(main_g, '{http://www.w3.org/2000/svg}text', {
    'x': '300', 'y': '320', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '16', 'font-weight': 'bold', 'fill': '#58A6FF', 'transform': 'rotate(-35 300 320)'
}).text = '🚀 避开主战场，精准侧翼切割'

# --- 3. The Blue Ocean (Abridge Target) at top right ---
blue_ocean = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(950, 150)'})
# Target circles
ET.SubElement(blue_ocean, '{http://www.w3.org/2000/svg}circle', {
    'cx': '0', 'cy': '0', 'r': '80', 'fill': '#00D2FF', 'fill-opacity': '0.1', 'stroke': '#00D2FF', 'stroke-width': '1'
})
ET.SubElement(blue_ocean, '{http://www.w3.org/2000/svg}circle', {
    'cx': '0', 'cy': '0', 'r': '60', 'fill': '#00D2FF', 'fill-opacity': '0.2'
})
ET.SubElement(blue_ocean, '{http://www.w3.org/2000/svg}circle', {
    'cx': '0', 'cy': '0', 'r': '40', 'fill': '#00D2FF', 'filter': 'url(#glow-cyan)'
})
ET.SubElement(blue_ocean, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '120', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '24', 'font-weight': 'bold', 'fill': '#00D2FF', 'text-anchor': 'middle'
}).text = 'Abridge 临床文书'
ET.SubElement(blue_ocean, '{http://www.w3.org/2000/svg}text', {
    'x': '0', 'y': '145', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '14', 'fill': '#C9D1D9', 'text-anchor': 'middle'
}).text = 'Ambient AI 专属入口'

# --- 4. The Moat Pillars along the trajectory ---
# Points along the bezier curve roughly: (400, 300), (600, 200), (800, 160)
pillars = [
    (420, 320, '📍 1. 任务极窄化', '只做医患诊室对话转录', '#58A6FF'),
    (650, 220, '📍 2. 信任门槛', '生成的病历必须能溯源录音', '#3FB950'),
    (880, 290, '📍 3. 工作流嵌入', '不做聊天框，直连医院EHR', '#FF9A00')
]

for px, py, title, desc, color in pillars:
    # A sleek floating capsule
    g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': f'translate({px}, {py})'})
    # Line connecting capsule to trajectory
    if px == 880:  # Adjust connection for the third one which is below the curve
        ET.SubElement(g, '{http://www.w3.org/2000/svg}line', {
            'x1': '0', 'y1': '-50', 'x2': '0', 'y2': '0', 'stroke': color, 'stroke-width': '2', 'stroke-dasharray': '4 2'
        })
    else:
        ET.SubElement(g, '{http://www.w3.org/2000/svg}line', {
            'x1': '0', 'y1': '0', 'x2': '0', 'y2': '40', 'stroke': color, 'stroke-width': '2', 'stroke-dasharray': '4 2'
        })
        
    capsule_y = 0 if px == 880 else 40
    
    ET.SubElement(g, '{http://www.w3.org/2000/svg}rect', {
        'x': '-120', 'y': str(capsule_y), 'width': '240', 'height': '70', 'rx': '12',
        'fill': '#161B22', 'stroke': '#30363D', 'stroke-width': '1.5'
    })
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '0', 'y': str(capsule_y + 30), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '16', 'font-weight': 'bold', 'fill': color, 'text-anchor': 'middle'
    }).text = title
    ET.SubElement(g, '{http://www.w3.org/2000/svg}text', {
        'x': '0', 'y': str(capsule_y + 55), 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
        'font-size': '14', 'fill': '#8B949E', 'text-anchor': 'middle'
    }).text = desc


# --- 5. Bottom Takeaway Panel ---
bot_g = ET.SubElement(main_g, '{http://www.w3.org/2000/svg}g', {'transform': 'translate(80, 620)'})
# Background
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}rect', {
    'x': '0', 'y': '0', 'width': '1120', 'height': '60', 'rx': '12',
    'fill': '#1A202C', 'stroke': '#30363D', 'stroke-width': '1'
})
# Text
ET.SubElement(bot_g, '{http://www.w3.org/2000/svg}text', {
    'x': '560', 'y': '36', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
    'font-size': '20', 'font-weight': 'bold', 'fill': '#C9D1D9', 'text-anchor': 'middle'
}).text = '💡 侧翼战的核心：极窄任务绝不是“市场小”，而是重构工作流、形成默认入口的最锐利武器。'


tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("P38 successfully redesigned with a fluid organic trajectory layout.")
