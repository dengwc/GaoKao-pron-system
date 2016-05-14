# -*- coding:utf-8 -*-    
# Pron System
import xmlParser
import os
import sys
import tempfile
from smb.SMBConnection import SMBConnection
from kernel import kernel

reload(sys)
sys.setdefaultencoding('utf-8')

def pron_question(pronKeyword,fileObj,outputFile):
    xmltree = xmlParser.xmlparse(fileObj)
    pronQuesList = xmlParser.keyword_position_or(xmltree,pronKeyword)
    #print pronQuesList
    for eachQues in pronQuesList:
        answer = pron_question_solve(eachQues)
        #print 'Question answer',answer
        if answer=='':
            continue

        xmlParser.add_answer(eachQues,answer)
        print
        tmp = raw_input('')

    xmlParser.write_xml(xmltree,outputFile)

def pron_question_solve(question):
    questionDict = xmlParser.pron_parse(question)
    if no_use_check(questionDict):
        return ''

    answer = pron_answer(questionDict)
    return answer

def pron_answer(questionDict):
    print questionDict
    for each in questionDict:
        if each=='options':
            print each
            for i in questionDict[each]:
                print i
        elif each=='point':
            print each
            for i in questionDict[each]:
                for j in i:
                    print j,
            print
        else:
            print 'each',questionDict[each]
    print

    return kernel.ques_solve(questionDict)

def no_use_check(question):
    print question['id']
    '''
    for each in question:
        print each,
        print question[each]
    '''
    if question['body']=='' or question['options']==[] or question['point']==[]:
        return True


    if '$' not in question['options'][0]:
        return True

    return False

def file_connection():
    IP  = sys.argv[1]
    shareName = sys.argv[2]
    inputFile = sys.argv[3]
    port = 139
    conn = SMBConnection("","","","")
    conn.connect(IP,port)
    fileObj = tempfile.NamedTemporaryFile()

    conn.retrieveFile(shareName,inputFile,fileObj)
    return fileObj

def test(keyword):
    paperPath = './papers/'
    fileNames = os.listdir(paperPath)
    for f_name in fileNames:
        print 'processing',f_name
        outName = './output/'+f_name.split('.')[0] + 'out.xml'
        pron_question(keyword,paperPath+f_name,outName)    
        print

if __name__=='__main__':
    #outputFile = sys.argv[4]
    #outputFile = './out.xml'
    #outputFile = sys.argv[2]

    #fileObj = file_connection()
    #fileObj = './02.xml'
    #fileObj = sys.argv[1]
    #xmltree = xmlParser.xmlparse(fileObj)

    pronKeyword = ['读音','字形','错别字','注音','书写']
    test(pronKeyword)
    #pron_question(xmltree,pronKeyword,outputFile)
    #fileObj.close()
