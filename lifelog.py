# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import re
import life_tree as LT
from vitualization import *

categoryflags = []
categories = []
sheet = []

def find_act_from_life_tree(record, lnode):
    found = False
    for act in lnode.dict:
        if act in record:
            print 'matching:' + '\''+ act + '\''
            found = True
            break
    if found:
        value = re.findall(r'\d+\.?\d*', record)
        if value:
            value = float(value[0])
            print value
            oldcount = lnode.count
            lnode.count += int(value)
            print 'count:' + str(oldcount) + ' + ' + str(value) + ' = ' + str(lnode.count)
        print "activity:" + lnode.name 
    else:
        for i in range(len(lnode.child)):
            find_act_from_life_tree(record, lnode.child[i])

def analyze(index, record, date):
    print "Category:" + categories[index].tag
    find_act_from_life_tree(record, lifetree.child[index])

def reduce_tree(root):
    # internal nodes
    if root.child:
        for child in root.child:
            root.count += reduce_tree(child)
        return root.count
    # leaves
    else:
        return root.count

# check categories from XML
tree = ET.parse('./test.xml')
for category in tree.getroot():
    categories.append(category)
    if category.attrib.has_key("categoryflag"):
        categoryflags.append(category.attrib["categoryflag"])
    else:
        print "Warning: % has no categoryflag", category.tag
        categoryflags.append("NO-CATEGORY")
lifetree = LT.build_tree_from_xml('./test.xml')

# analyze log file line by line
log = open('log.txt')
for record in log:
    record = record.strip()
    # empty line: ignore
    if not record:
        continue
    # date line: memorize the date
    if re.search('\[[0-9].[0-3]*[0-9]\]', record):
        date = record
        print '======================='
        print date
        continue
    # activity line: get category first, then analyze
    print '- - - - - - - - - - - -'
    print "processing:" + record
    categorized = False
    for categoryflag in categoryflags:
        if categoryflag in record:
            categorized = True
            # index is for both ET category and LT level 1 
            categoryindex = categoryflags.index(categoryflag)
            analyze(categoryindex, record, date)
            break
    if categorized == False:
        print "Warning: % cannot be categorized"
reduce_tree(lifetree)
print lifetree.count
labels = []
fracs = []
for child in lifetree.child[0].child:
    labels.append(child.name)
    fracs.append(child.count)
drawpie(labels, fracs, "Time Consuming", "./time.png")
