import os
from xml.etree import ElementTree as ET

proj = '/Users/gnuhpc/Desktop/myproject/projects/china_enterprise_strategy_ppt169_20260627'
svg_file = os.path.join(proj, 'svg_output/34_进攻战与防御战：大厂的主力交锋.svg')

ET.register_namespace('', "http://www.w3.org/2000/svg")
tree = ET.parse(svg_file)
root = tree.getroot()

# Find the bottom block text
texts = root.findall('.//{http://www.w3.org/2000/svg}text')
for text in texts:
    if '行业领导者与挑战者的核心博弈' in (text.text or ''):
        # Update title font size
        text.set('font-size', '22')
        text.set('y', '38') # slight adjustment down for larger font
        
        # Find the group containing the columns
        parent_g = root.find('.//*{http://www.w3.org/2000/svg}text[.=\"' + text.text + '\"]/..')
        if parent_g is not None:
            g_cols = parent_g.find('{http://www.w3.org/2000/svg}g')
            if g_cols is not None:
                children = list(g_cols)
                
                # Col 1 (index 0, 1, 2)
                # rect
                children[0].set('x', '0')
                children[0].set('y', '-22')
                children[0].set('width', '80')
                children[0].set('height', '30')
                children[0].set('rx', '6')
                
                # label
                children[1].set('x', '40')
                children[1].set('y', '0')
                children[1].set('font-size', '18')
                
                # text
                children[2].set('x', '100')
                children[2].set('y', '2')
                children[2].set('font-size', '20')
                
                # Col 2 (index 3, 4, 5)
                # rect
                children[3].set('x', '560')
                children[3].set('y', '-22')
                children[3].set('width', '80')
                children[3].set('height', '30')
                children[3].set('rx', '6')
                
                # label
                children[4].set('x', '600')
                children[4].set('y', '0')
                children[4].set('font-size', '18')
                
                # text
                children[5].set('x', '660')
                children[5].set('y', '2')
                children[5].set('font-size', '20')
                
                # Remove Col 3 (index 6, 7, 8) if they exist
                if len(children) > 6:
                    g_cols.remove(children[6])
                if len(children) > 7:
                    g_cols.remove(children[7])
                if len(children) > 8:
                    g_cols.remove(children[8])
        break

tree.write(svg_file, encoding='UTF-8', xml_declaration=True)
print("Updated P34 bottom block layout and font sizes.")
