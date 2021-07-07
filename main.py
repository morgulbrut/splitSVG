import sys
from xml.dom import minidom
import re
from colorama import Fore, init


class NoGroupsFoundError(Exception):
    pass


init(autoreset=True)

svg_file = 'editor_method_ac.svg'

tags = ['inkscape:label', 'id']

doc = minidom.parse(svg_file)

groups = doc.getElementsByTagName('g')

with open(svg_file, mode='r') as f:
    header = re.split('<g\s', f.read())[0]

layers = []
filenames = []


def get_groups(tag):
    print(Fore.YELLOW+"trying: "+tag)

    for group in groups:
        # todo
        if group.getAttribute(tag) != "":
            layers.append(group)
            filenames.append(group.getAttribute(tag))
    return len(layers)


for t in tags:
    if get_groups(t) != 0:
        break


for i in range(len(layers)):
    prefix = svg_file.split(".")[0]
    with open(prefix+"_"+filenames[i]+".svg", mode='w') as outfile:
        outfile.write(header)
        outfile.write(layers[i].toxml())
        outfile.write("\n</svg>")
