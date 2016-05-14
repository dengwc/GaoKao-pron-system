# -*- coding:utf-8 -*-
# Pron Module

from kernel import kernel
from pinyin_tran import Tran
import re
import random
import sys

testfile = '../basicinfo/term_tf_ques_1000.txt'
dictSource = 2

tr = Tran()

def test(testfile):
    fp = open(testfile)
    num = 0
    acc = 0
    for line in fp.readlines():
        line = ques_body_regular(line)
        # question dict
        ques_dict = {}
        ques_dict['answer'] = line[0]
        ques_change = line[1:].replace('A','$').replace('B','$').replace('C','$').replace('D','$')
        parts = ques_change.split('$')
        ques_dict['body'] = parts[0]
        ques_dict['options'] = parts[1:]

        print line
        num += 1
        predict_answer = kernel.ques_solve(ques_dict)
        if predict_answer==ques_dict['answer']:
            acc += 1
        print 'id:',num,'acc:',acc,'per:',float(acc)/num
        print
        stop()

def stop():
    tmp = raw_input(' ')

def ques_solve(ques):
    ### question solve
    standard_answer = ques[0]
    ques_change = ques[1:].replace('A','$').replace('B','$').replace('C','$').replace('D','$')
    parts = ques_change.split('$')
    ques_body = parts[0]
    option_list = parts[1:]
    ques_class = class_choose(ques_body)
    show_info(standard_answer,ques_class,ques_body,option_list)

    answer_list = []
    for index in range(len(option_list)):
       answer_list.append(option_answers(option_list[index]))

    print 'ANS list:',answer_list
    predict_answer = score_compare_system(ques_class,answer_list)
    print 'Ans',standard_answer,'Pre',predict_answer,
    if predict_answer==standard_answer:
        return True
    print 'ERROR',
    return False

def show_info(standard_answer,ques_class,ques_body,option_list):
    print 'ans:',standard_answer,'class:',ques_class
    if standard_answer in ['A','B','C','D'] and ques_class in [0,1] and len(option_list)==4:
        return
    print 'Error in question body'
    print 'ans:',standard_answer,'class:',ques_class,'option_list:',len(option_list)
    for each in option_list:
        print each
    stop()

def basic_system(ques_class,answer_list):
    ### basic system to choose answer . not add random
    #print ques_class,answer_list
    res_list = option_answer_to_list(answer_list)
    # candidate answer
    # class 1, all_correct_index_list.len = 1
    if ques_class==1 and len(res_list[0])==1:
        return list_index_to_char(res_list[0][0])
    # class 0, exist_incorrect_index_list.len = 1
    if ques_class==0 and len(res_list[1])==1:
        return list_index_to_char(res_list[1][0])
    return ''

def score_compare_system(ques_class,answer_list):
    ### score compare system to choose answer.
    if ques_class==0:
        # find error
        error_number_list = []
        not_judge_number_list = []
        for i in range(len(answer_list)):
            error_number_list.append(answer_list[i][2])
            not_judge_number_list.append(answer_list[i][1])
        if max(error_number_list)==0:
            # error number is all 0
            return list_index_to_char(not_judge_number_list.index(max(not_judge_number_list)))
        else:
            # has error number
            return list_index_to_char(error_number_list.index(max(error_number_list)))

    if ques_class==1:
        # find correct
        right_number_list = []
        for i in range(len(answer_list)):
            if answer_list[i][2]==0:
                right_number_list.append(answer_list[i][0])
            else:
                right_number_list.append(0)

        return list_index_to_char(right_number_list.index(max(right_number_list)))

    return 0

def option_answer_to_list(answer_list):
    ### option answer to list
    all_correct_index_list = []
    exist_incorrect_index_list = []
    correct_number_list = []
    incorrect_number_list = []
    for i in range(len(answer_list)):
        correct_number_list.append(answer_list[i][0])
        incorrect_number_list.append(answer_list[i][1])
        if answer_list[i][1]==0 and answer_list[i][2]==0:
            all_correct_index_list.append(i)
        if answer_list[i][2]!=0:
            exist_incorrect_index_list.append(i)

    return all_correct_index_list,exist_incorrect_index_list,correct_number_list,incorrect_number_list

def option_answers(option):
    ###option answer,return [rightnum,notJudgenum,errornum]
    term_list = option.replace('\t',' ').split(' ')

    rightNum = 0
    notJudgeNum = 0
    errorNum = 0
    for i in range(len(term_list)):
        if term_list[i]=='':
            continue
        print term_list[i],
        termAnswer = term_answer(term_list[i])
        print termAnswer,

        if termAnswer==1:
            rightNum += 1
        elif termAnswer==0:
            notJudgeNum += 1
        else:
            errorNum += 1
    print
    #print 'rightNum',rightNum,'NotJudgeNum',notJudgeNum,'errorNum',errorNum
    return rightNum,notJudgeNum,errorNum

def term_answer(term):
    ### term answer
    if term_only_judge(term)==True:
        print 'term',
        return term_judge(term)
    else:
        print 'pron',
        term_pron_list = seperate_term_pron_in_term(term)
        return pron_judge(term_pron_list[0],term_pron_list[1])

def term_judge(term):
    ### term judge
    return termCorrect.judge(term)

def pron_judge(term,pron):
    ### pron judge
    return pronCorrect.judge(term,pron)

def seperate_term_pron_in_term(term):
    ### seperate term and pron, return [term,pron]
    term = tr.translate(term)
    sub_term = re.sub(r'\w+','',term)
    pron = re.findall(r'\w+',term)[0]
    pron_tran = re.sub(r'[0-9]','',pron) + re.sub(r'[a-z]','',pron)
    return sub_term,pron_tran

def term_only_judge(term):
    ### seperate if term only. True:only term / False: term and pron
    if term==re.sub(r'\w+','',term):
        return True
    return False

def list_index_to_char(index):
    ### index->answer, eg. 0->A
    return chr(index+65)

def ques_body_regular(text):
    ### question body regular. remove useless character
    special_char = ['(',')','（','）','．','.','\r','\n']
    for each in special_char:
        text = text.replace(each,'')
    return text

def class_choose(quesBody):
    ### question classify 1: find correct 0: find incorrect -1:unknown class
    error = '错误'
    correct = '正确'
    all_ = '全'
    exist = '存在'
    no = '不'
    not_ = '没'
    have = '有'
    wrong = '误'
    regular = '规范'
    right = '对'
    none = '无'
    cuo = '错'

    # 不 (完)全 正确
    if (no in quesBody) and (all_ in quesBody) and (correct in quesBody):
        return 0
    #(完)全 正确
    elif (all_ in quesBody) and (correct in quesBody):
        return 1

    # 没 有 错误
    if (not_ in quesBody) and (have in quesBody) and (error in quesBody):
        return 1
    # 有 错误
    elif (have in quesBody) and (error in quesBody):
        return 0
    # 错误
    elif (error in quesBody):
        return 0

    # 没有 错
    if (not_ in quesBody) and (have in quesBody) and (cuo in quesBody):
        return 1
    elif (have in quesBody) and (cuo in quesBody):
        return 0

    # 无 误
    if (none in quesBody) and (wrong in quesBody):
        return 1
    # 有 误
    if (have in quesBody) and (wrong in quesBody):
        return 0

    # 不 存在 错误
    if (no in quesBody) and (exist in quesBody) and (error in quesBody):
        return 1
    # 存在 错误
    elif (exist in quesBody) and (error in quesBody):
        return 0
    # 不 正确
    if (no in quesBody) and (correct in quesBody):
        return 0
    # 正确
    elif (correct in quesBody):
        return 1
    # 不 规范
    if (no in quesBody) and (regular in quesBody):
        return 0
    elif (regular in quesBody):
        return 1
    # 全 对
    if (all_ in quesBody) and (right in quesBody):
        return 1

    return -1

if __name__=='__main__':
    test(testfile)
