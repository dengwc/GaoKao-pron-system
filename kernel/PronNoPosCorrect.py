# -*- coding:utf-8 -*-
# judge if pron is correct, no position
from db_connection import db_mysql
import segment as seg

class PronNoPosCorrect:

    def __init__(self,dictSource):
        self.ltp = True
        self.word = True
        self.DICTSOURCE = dictSource

    def judge(self,term,pron):
        ###judge
        result = self.dict_model(term,pron)
        print 'dict',result,

        if self.ltp==True and result==0:
            result = self.ltp_model(term,pron)

        if self.word==True and result==0:
            result = self.word_model(term,pron)

        return result

    def db_query(self,term):
        ### database query .
        query = "select * from term where term = '%s'" % term
        db = db_mysql()
        res = db.executeQuery(query)
        #db.close()
        return res

    def db_query_word(self,word):
        ### database query . word pron.
        query = "select * from word where word = '%s'" % word
        db = db_mysql()
        res = db.executeQuery(query)
        #db.close()
        return res

    def dict_model(self,term,pron):
        ### DictModel . judge pron
        res = self.db_query(term)
        for each in res:
            if pron in each[self.DICTSOURCE]:
                return 1
            else:
                print each[self.DICTSOURCE],
                return -1
        else:
            return 0

    def ltp_model(self,term,pron):
        ### ltp segmentor model. Judge pron
        seg_list = seg.segment(term)
        #print ' '.join(seg_list)
        # find all segment pron
        pron_find_str = ''
        for word in seg_list:
            word_res = self.db_query(word)
            for each in word_res:
                pron_find_str += each[self.DICTSOURCE]+'\t'
        print 'ltp',pron_find_str,

        if pron in pron_find_str:
            print 1,
            return 1
        print 0,
        return 0

    def word_model(self,term,pron):
        ### word pron word.
        WORDSOURCE = 3
        word_pron_list = []

        # segment term to word, get all word possible pron
        for i in range(len(term)/3):
            word = term[i*3:i*3+3]
            #print word
            res = self.db_query_word(word)
            for each in res:
                word_pron_list.append(each[WORDSOURCE])
        print 'word',word_pron_list,

        if pron in word_pron_list and len(word_pron_list)==(len(term)/3):
            print 1,
            return 1

        if pron not in word_pron_list:
            print -1,
            return -1
        print 0,
        return 0

if __name__=='__main__':
    import sys
    test = PronNoPosCorrect(2)
    print test.judge(sys.argv[1],sys.argv[2])
