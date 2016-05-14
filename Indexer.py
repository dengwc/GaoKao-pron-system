#_*_ coding:utf-8 _*_

import os,sys,lucene
#from pyltp import Segmentor
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.index import IndexReader
from org.apache.lucene.index import Term

import segment as seg

class Indexer:
    #segmentor = Segmentor()

    def __init__(self):
        #self.segmentor.load('./cws.model')
        INDEXDIR = './Myindex'
        #lucene.initVM(vmargs='-Xcheck:jni,-verbose:jni,-verbose:gc')
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        #vm_env = lucene.getVMEnv()
        #vm_env.attachCurrentThread()
        #lucene.initVM(vmargs='-')
        #print 'lucene', lucene.VERSION
        self.directory = SimpleFSDirectory(File(INDEXDIR))
        self.searcher = IndexSearcher(DirectoryReader.open(self.directory))
        self.analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        self.reader = IndexReader.open(self.directory)

    def Qsearch(self,query):
        words = seg.segment(query.strip())
        #words = self.segmentor.segment(query.strip())
        #print ' '.join(words)
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
        result = QueryParser(Version.LUCENE_CURRENT, "contents",self.analyzer)
        result.setPhraseSlop(0)
        # "\""+' '.join(words)+"\"~0" means words should be continuous
        query = result.parse("\""+' '.join(words)+"\"~0")
        totalHits = self.searcher.search(query, 50)
        #print "%s total matching documents." % totalHits.totalHits
        #return totalHits.totalHits

        for hit in totalHits.scoreDocs:
            #print"Hit Score: ",hit.score, "Hit Doc:",hit.doc, "HitString:",hit.toString()
            doc= self.searcher.doc(hit.doc)
            #print doc.get("name").encode("utf-8")
        #print "----------------------------------------"
        t = Term('contents',' '.join(words))
        #termDocs = ireader.termDocs(t)
        #for tt in termDocs:
        #       print ireader.document(termDocs.docs).getFeildable('neme'),termDocs.freq()
        #print self.reader.totalTermFreq(t)
        return self.reader.totalTermFreq(t)
