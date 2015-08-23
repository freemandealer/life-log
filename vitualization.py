# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pylab import *

def drawpie(labels, fracs, titletext, save):
    figure(1, figsize=(6,6))
 #   ax = axes([0.1, 0.1, 0.8, 0.8])
  #  explode=(0, 0, 0, 0)
    pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    title(titletext, bbox={'facecolor':'0.8', 'pad':5})
    savefig(save)
    show()

if __name__ == '__main__':
    drawpie(['1','2','3','4', '5'], [1,2,3,4,5], 'test pie', './test ipe.png')


