# -*- coding:utf-8 -*-
# pron query
from db_connection import db_mysql

class PronQuery:

    def __init__(self,dictSource):
        self.DICTSOURCE = dictSource

    def query(self,term):
        ###pron query
        return self.dict_model(term)

    def dict_model(self,term):
        ### dict model . pron query
        res = self.db_query(term)
        for each in res:
            return each[self.DICTSOURCE]

    def db_query(self,term):
        ### database query for term
        query = "select * from term where term = '%s' " % term
        db = db_mysql()
        res = db.executeQuery(query)
        return res

if __name__=='__main__':
    import sys
    test = PronQuery(2)
    print test.query(sys.argv[1])
