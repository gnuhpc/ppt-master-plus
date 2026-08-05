import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/34_进攻战与防御战：大厂的主力交锋.svg')

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

texts = root.findall('.//{http://www.w3.org/2000/svg}text')
for text in texts:
    if '行业领导者与挑战者的核心博弈' in (text.text or '') or '进攻战核心：' in (text.text or ''):
        parent_g = root.find('.//*{http://www.w3.org/2000/svg}text[.=\"' + text.text + '\"]/..')
        if parent_g is not None:
            # Clear existing content
            for child in list(parent_g):
                parent_g.remove(child)
                
            # Card 1
            rect1 = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}rect', {
                'x': '0', 'y': '0', 'width': '540', 'height': '100', 'rx': '12', 
                'fill': '#161B22', 'stroke': '#FF9A00', 'stroke-width': '2'
            })
            title1 = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}text', {
                'x': '30', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
                'font-size': '22', 'font-weight': 'bold', 'fill': '#FF9A00'
            })
            title1.text = '⚔️ 进攻方的核心博弈：'
            
            desc1 = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}text', {
                'x': '30', 'y': '75', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
                'font-size': '20', 'fill': '#F0F6FC'
            })
            desc1.text = '寻找巨头无法轻易改变的固有弱点，从侧方一击致命。'

            # Card 2
            rect2 = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}rect', {
                'x': '580', 'y': '0', 'width': '540', 'height': '100', 'rx': '12', 
                'fill': '#161B22', 'stroke': '#00D2FF', 'stroke-width': '2'
            })
            title2 = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}text', {
                'x': '610', 'y': '40', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
                'font-size': '22', 'font-weight': 'bold', 'fill': '#00D2FF'
            })
            title2.text = '🛡️ 防御方的核心博弈：'
            
            desc2 = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}text', {
                'x': '610', 'y': '75', 'font-family': "'Microsoft YaHei', 'Calibri', sans-serif",
                'font-size': '20', 'fill': '#F0F6FC'
            })
            desc2.text = '在对手发力前，主动用更先进的模式颠覆自己的既得利益。'

            # VS Badge
            circle = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}circle', {
                'cx': '560', 'cy': '50', 'r': '24',
                'fill': '#21262D', 'stroke': '#30363D', 'stroke-width': '2'
            })
            vs = ET.SubElement(parent_g, '{http://www.w3.org/2000/svg}text', {
                'x': '560', 'y': '58', 'font-family': "'Arial Black', sans-serif",
                'font-size': '20', 'font-weight': 'bold', 'fill': '#8B949E', 'text-anchor': 'middle'
            })
            vs.text = 'VS'
            break

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("Completely redesigned P34 bottom section.")
