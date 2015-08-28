#!/usr/bin/python
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

# match record with activity from sub-lifetree
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

# analyze record for each category
def analyze(index, record, line, date):
    category = categories[index]
    print "Category:" + category.tag
    # this category outputs pie charts
    if category.attrib['showtype'] == 'pie':
        find_act_from_life_tree(record, line, lifetree.child[index])
        global act_found
        if not act_found:
            act_not_found(record, line)
        else:
            act_found = False
    # this category outputs bar charts or unknown(default)
    else:
        print 'BAR'

# harvest leaves to sum up count for the root
def reduce_tree(root):
    # internal nodes
    if root.child:
        for child in root.child:
            root.count += reduce_tree(child)
        return root.count
    # leaves
    else:
        return root.count

def print_usage():
    print '''USAGE:
    lifelog.py [life-tree.xml] [log.txt]
    '''

## START ##
if len(sys.argv) != 3:
    print_usage()
    exit()
# build ElementTree
tree = ET.parse(sys.argv[1])
# check categories from XML
for category in tree.getroot():
    categories.append(category)
    if category.attrib.has_key("categoryflag"):
        categoryflags.append(category.attrib["categoryflag"])
        if category.attrib['showtype'] not in ['pie', 'bar']:
            print '\033[1;31;40m'
            print 'WARNING: \'%s\' has no showtype, using default' %category.tag
            print '\033[0m'
    else:
        print '\033[1;31;40m'
        print 'WARNING: \'%s\' has no categoryflag' %category.tag
        print '\033[0m'
        categoryflags.append("NO-CATEGORY")
# build lifetree
lifetree = LT.build_tree_from_xml(sys.argv[1])
log = open(sys.argv[2])
line = 0
day_count = 0
# analyze log file line by line
for record in log:
    line += 1
    record = record.strip()
    # empty line: ignore
    if not record:
        continue
    # date line: memorize the date and increase day_count
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
        print "WARNING: % cannot be categorized"
# sum up
reduce_tree(lifetree)
# draw output
# time
other_act = day_count * 24 - lifetree.count
labels = ['other']
fracs = [other_act]
for child in lifetree.child[0].child:
    labels.append(child.name)
    fracs.append(child.count)
drawpie(labels, fracs, "Time Consuming", "./time.png")
# finance
labels = []
fracs = []
for child in lifetree.child[1].child:
    labels.append(child.name)
    fracs.append(child.count)
drawpie(labels, fracs, lifetree.child[1].name, './' + lifetree.child[1].name + '.png')
