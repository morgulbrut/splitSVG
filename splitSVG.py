import sys
from xml.dom import minidom
import xml
import re
import os
from colorama import Fore, init


class SVGsplitter():

    def __init__(self) -> None:
        init(autoreset=True)
        self.layers = []
        self.filenames = []
        self.tags = ['inkscape:label', 'id']

    def get_groups(self, svgfile, tag):
        print(Fore.YELLOW+"trying: "+tag)
        prefix = os.path.splitext(os.path.basename(svgfile))[0]+"_"
        groups = self.doc.getElementsByTagName('g')
        for group in groups:
            # todo
            if group.getAttribute(tag) != "":
                self.layers.append(group)
                self.filenames.append(prefix+group.getAttribute(tag)+".svg")
        return len(self.layers)

    def parse(self, svg_file):
        try:
            self.doc = minidom.parse(svg_file)
        except xml.parsers.expat.ExpatError:
            print(Fore.RED + "Maybe try some proper SVG editor next time")
            sys.exit(1)
        except FileNotFoundError:
            print(Fore.RED + "File not found")
            sys.exit(2)
        for t in self.tags:
            if self.get_groups(svg_file, t) != 0:
                break

    def get_header(self, svg_file):
        with open(svg_file, mode='r') as f:
            self.header = re.split('<g\s', f.read())[0]

    def write_output(self):
        for i in range(len(self.filenames)):
            print(Fore.CYAN+"Writing {}".format(self.filenames[i]))
            with open(self.filenames[i], mode='w') as outfile:
                outfile.write(self.header)
                outfile.write(self.layers[i].toxml())
                outfile.write("\n</svg>")

    def write_png(self):
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM

        for f in self.filenames:
            png_file = os.path.splitext(os.path.basename(f))[0]+".png"
            print(Fore.CYAN+"Writing {}".format(png_file))
            drawing = svg2rlg(f)
            renderPM.drawToFile(drawing, png_file, fmt="PNG")


if __name__ == "__main__":
    args = sys.argv[1:]
    svgs = SVGsplitter()
    svgs.get_header(args[0])
    svgs.parse(args[0])
    svgs.write_output()
