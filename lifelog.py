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
act_not_found_list = []

act_found = False

def act_not_found(record, line):
    act_not_found_list.append([record, line])
    print '\033[1;31;40m'
    print 'WARNING: in line %d: \'%s\' match no activity' %(line, record)
    print '\033[0m'

def find_act_from_life_tree(record, line, lnode):
    found = False
    global act_found
    for act in lnode.dict:
        if act in record:
            print 'matching:' + '\''+ act + '\''
            found = True
            act_found = True
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
            find_act_from_life_tree(record, line, lnode.child[i])


def analyze(index, record, line, date):
    print "Category:" + categories[index].tag
    find_act_from_life_tree(record, line, lifetree.child[index])
    global act_found
    if not act_found:
        act_not_found(record, line)
    else:
        act_found = False

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
tree = ET.parse('./LifeTree-Freeman.xml')
for category in tree.getroot():
    categories.append(category)
    if category.attrib.has_key("categoryflag"):
        categoryflags.append(category.attrib["categoryflag"])
    else:
        print '\033[1;31;40m'
        print "Warning: % has no categoryflag", category.tag
        print '\033[0m'
        categoryflags.append("NO-CATEGORY")
lifetree = LT.build_tree_from_xml('./LifeTree-Freeman.xml')

# analyze log file line by line
log = open('log.txt')
line = 0
day_count = 0
for record in log:
    line += 1
    record = record.strip()
    # empty line: ignore
    if not record:
        continue
    # date line: memorize the date
    if re.search('\[[0-9].[0-3]*[0-9]\]', record):
        date = record
        print '======================='
        print date
        day_count += 1
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
            analyze(categoryindex, record, line, date)
            break
    if categorized == False:
        print "Warning: % cannot be categorized"
reduce_tree(lifetree)
other_act = day_count * 24 - lifetree.count
labels = ['other']
fracs = [other_act]
for child in lifetree.child[0].child:
    labels.append(child.name)
    fracs.append(child.count)
drawpie(labels, fracs, "Time Consuming", "./time.png")
