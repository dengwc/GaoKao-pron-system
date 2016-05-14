# -*- coding:utf-8 -*-
# judge if the pron of term is correct

from db_connection import db_mysql
import segment as seg

class PronCorrect:

    def __init__(self,dictSource):
        self.ltp = True
        self.word = True
        self.DICTSOURCE = dictSource

    def judge(self,term,pron,pos):
        ###judge
        result = self.dict_model(term,pos,pron)
        print 'dict',result,

        if self.ltp == True and result==0:
            result = self.ltp_model(term,pos,pron)

        if self.word == True and result==0:
            result = self.word_model(term,pos,pron)

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

    def dict_model(self,term,pos,pron):
        ### DictModel . judge pron
        res = self.db_query(term)
        for each in res:
            standard_pron_list = each[self.DICTSOURCE].split(' ')
            standard_pron = standard_pron_list[pos-1]
            if standard_pron == pron:
                return 1
            else:
                print ' '.join(standard_pron_list),
                return -1
        else:
            return 0

    def ltp_model(self,term,pos,pron):
        ### ltp segmentor model. Judge pron
        #words = self.segmentor.segment(term.encode('utf-8'))
        words = seg.segment(term)
        # Position and start pos
        start = 0
        for i in range(0,len(words)):
            #print i,words[i]
            if start + len(words[i])/3 >= pos:
                break
            else:
                start += len(words[i])/3
        # word seg: i  querypos: wordpos
        wordpos = pos-start
        if len(words)==0:
            return 0

        return self.dict_model(words[i],wordpos,pron)

    def word_model(self,term,pos,pron):
        ### word pron word.
        pos_word = term[3*(pos-1):3*pos]
        word_pron_list = []

        res = self.db_query_word(pos_word)
        for each in res:
            #each[3] is pron of word.
            word_pron_list.append(each[3])

        # if pron in pronpos  appears in word_pron_List
        if pron not in word_pron_list:
            return -1
        elif len(word_pron_list)==1:
            return 1

        return 0

if __name__=='__main__':
    import sys
    test = PronCorrect(2)
    print test.judge(sys.argv[1],sys.argv[2],int(sys.argv[3]))
