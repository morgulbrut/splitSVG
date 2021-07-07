import sys
from xml.dom import minidom
import xml
import re
import os
from colorama import Fore, init

svg_file = 'test-inkscape-extension.svg'
tags = ['inkscape:label', 'id']


class NoGroupsFoundError(Exception):
    pass


def get_groups(svgfile, tag):
    print(Fore.YELLOW+"trying: "+tag)
    prefix = os.path.basename(svgfile)+"_"
    for group in groups:
        # todo
        if group.getAttribute(tag) != "":
            layers.append(group)
            filenames.append(prefix+group.getAttribute(tag)+".svg")

    return len(layers)


init(autoreset=True)

try:
    doc = minidom.parse(svg_file)
except xml.parsers.expat.ExpatError:
    print(Fore.RED + "Maybe try some proper SVG editor next time")
    sys.exit(1)
except FileNotFoundError:
    print(Fore.RED + "File not found")
    sys.exit(2)

groups = doc.getElementsByTagName('g')

with open(svg_file, mode='r') as f:
    header = re.split('<g\s', f.read())[0]

layers = []
filenames = []

for t in tags:
    if get_groups(svg_file, t) != 0:
        break

for i in range(len(layers)):
    prefix = svg_file.split(".")[0]
    with open(filenames[i], mode='w') as outfile:
        outfile.write(header)
        outfile.write(layers[i].toxml())
        outfile.write("\n</svg>")
