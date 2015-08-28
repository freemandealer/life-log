# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import re

class life_tree_node:
    def __init__(self, name=None, parent=None, dict=None):
        self.name = name
        self.parent = parent
        self.child = []
        self.count = 0
        self.dict = dict


def build_tree_from_xml(filename):
    eroot = ET.parse(filename).getroot()
    lroot = life_tree_node(name=eroot.tag)
    element_to_life_iter(eroot, lroot)
    return lroot

def text_to_dict(text):
    dict = []
    if text:
        utf8text = text.decode('utf-8')
        utf8text = utf8text.strip()
        for act in utf8text.split(';'):
            if act != '':
                dict.extend([act])
    return dict

def element_to_life_iter(eroot, lroot):
    for echild in eroot:
        lchild = life_tree_node(name=echild.tag, parent=lroot, dict=text_to_dict(echild.text))
        lroot.child.extend([lchild])
        element_to_life_iter(echild, lchild)

if __name__ == '__main__':
    root = build_tree_from_xml('test.xml')
    print root.child[1].name
    print root.child[1].dict
