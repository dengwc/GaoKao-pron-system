# -*- coding:utf-8 -*-
# judge if term pattern is correct
# dict+ltp+lucene+similar
from db_connection import db_mysql
from Indexer import Indexer
import segment as seg

class TermCorrect:

    def __init__(self):
        self.indexer = Indexer()

        self.ltp = False
        self.lucene = True
        self.similar = True

        self.LUCENENUM = 10            # appear number in corpus / lucene
        self.TERMLEN = 4            # min term length for SimilarModel is 4
        self.SIMILARNUM = self.TERMLEN * 3

    def judge(self,term):
        ### judge term, only character pattern
        result = self.dict_model(term)
        print 'dict',result,
        if self.ltp==True and result==0:
            result = self.ltp_model(term)

        if result!=0:
            return result

        #print len(term),self.SIMILARNUM
        sim_find = False
        if self.similar==True and len(term)>=self.SIMILARNUM:
            sim_result = self.similar_model(term)
            sim_find = True
            print 'similar',sim_result,

        if self.lucene==True:
            luc_result = self.lucene_model(term)
            print 'lucene',luc_result,

        if sim_find==True and sim_result==-1 and luc_result==1:
            return 1
        if sim_find==True and sim_result==-1 and luc_result==0:
            return -1

        if self.lucene==True:
            return luc_result
        return 0

    def db_query(self,term):
        ### database query .
        query = "select * from term where term = '%s'" % term
        db = db_mysql()
        res = db.executeQuery(query)
        #db.close()
        return res

    def db_query_like(self,term):
        ### database query. sql like . find similar term
        query = "select * from term where term like '%s'" % term
        db = db_mysql()
        res = db.executeQuery(query)
        #db.close()
        return res

    def dict_model(self,term):
        #### dict model. find term in sql directly
        res = self.db_query(term)
        for each in res:
            return 1
        else:
            return 0

    def similar_model(self,term):
        ### dict similar model,find similar term in database
        for i in range(len(term)/3):
            thisterm = term[0:3*i] + '%' + term[3*(i+1):]
            #print thisterm,
            res = self.db_query_like(thisterm)

            for each in res:
                ## judge if length of term is equal
                if len(each[1]) != len(term)/3:
                    continue
                print each[1],
                return -1

        return 0

    def ltp_model(self,term):
        ### ltp segmentor model. Judge term.
        #words = self.segmentor.segment(term)
        words = seg.segment(term)
        print 'seg:',' '.join(words),

        exist_number = 0
        for each_word in words:
            res = self.db_query(each_word)
            for each in res:
                exist_number += 1
                break

        if exist_number == len(words):
            return 1
        return 0

    def lucene_model(self,term):
        ### lucene modelif self.indexer.Qsearch >= self.lucnum:
        #print 'lucene num',self.indexer.Qsearch(term),
        if int(self.indexer.Qsearch(term)) >= self.LUCENENUM:
            return 1
        return 0

if __name__=='__main__':
    import sys
    test = TermCorrect()
    print test.judge(sys.argv[1])

