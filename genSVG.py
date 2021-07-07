import svgwrite
from svgwrite.extensions import Inkscape


dwg = svgwrite.Drawing('test-inkscape-extension.svg',
                       profile='full', size=(640, 480))
inkscape = Inkscape(dwg)
top_layer = inkscape.layer(label="top", locked=True)
dwg.add(top_layer)
line = dwg.line((100, 100), (300, 100), stroke=svgwrite.rgb(
    10, 10, 16, '%'), stroke_width=10)
top_layer.add(line)

text = dwg.text('Test', insert=(100, 100), font_size=100, fill='red')
top_layer.add(text)

nested_layer = inkscape.layer(label="overlay", locked=False)
dwg.add(nested_layer)

text = dwg.text('Test2', insert=(100, 200), font_size=100, fill='blue')
nested_layer.add(text)

dwg.save()
