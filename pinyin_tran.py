# -*- coding:utf-8 -*-
# change pinyin to word + value

class Tran:
    def __init__(self):
        # dict for pinyin
        self.d = {"ā":"a1","á":"a2","ǎ":"a3","à":"a4", \
                  "ō":"o1","ó":"o2","ǒ":"o3","ò":"o4", \
                  "ē":"e1","é":"e2","ě":"e3","è":"e4", \
                  "ī":"i1","í":"i2","ǐ":"i3","ì":"i4", \
                  "ū":"u1","ú":"u2","ǔ":"u3","ù":"u4", \
                  "ǖ":"v1","ǘ":"v2","ǚ":"v3","ǜ":"v4","ü":"v"}

    # tran pinyin to word + value
    def translate(self,term):

        for each in self.d:
            if each in term:
                term = term.replace(each,self.d[each])

        return term
