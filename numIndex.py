# -*- coding:utf-8 -*-
import sys
from Indexer import Indexer
i = Indexer()

def num(tmp):
    print i.Qsearch(tmp)

if __name__=='__main__':
    while 1:
        tmp = raw_input(' ')
        num(tmp)

