# -*- coding:utf-8 -*-
# Pron Module
from TermCorrect import TermCorrect
from PronNoPosCorrect import PronNoPosCorrect
from PronCorrect import PronCorrect
from pinyin_tran import Tran
import re

dictSource = 2

termCorrect = TermCorrect()
pronNoPosCorrect = PronNoPosCorrect(dictSource)
pronCorrect = PronCorrect(dictSource)

tr = Tran()

def ques_solve(ques_dict):
    ### question solve
    ques_class = class_choose(ques_dict['body'])
    option_list = ques_dict['options']

    answer_list = []
    for index in range(len(option_list)):
        if 'point' in ques_dict:
            point_list = choose_point_list_for_option(option_list[index],ques_dict['point'])
        else:
            point_list = []
        answer_list.append(option_answers(option_list[index],point_list))

    print 'ANS list:',answer_list
    predict_answer = score_compare_system(ques_class,answer_list)
    print 'Pre:',predict_answer
    return predict_answer

def score_compare_system(ques_class,answer_list):
    ### score compare system to choose answer.
    if ques_class==0:
        # find error
        error_number_list = []
        not_judge_number_list = []
        for i in range(len(answer_list)):
            not_judge_number_list.append(answer_list[i][1])
            error_number_list.append(answer_list[i][2])
        # choose answer
        if max(error_number_list)==0:
            # error number is all 0
            return list_index_to_char(not_judge_number_list.index(max(not_judge_number_list)))
        else:
            # has error number
            return list_index_to_char(error_number_list.index(max(error_number_list)))

    if ques_class==1:
        # find correct
        right_number_list = []
        error_number_list = []
        for i in range(len(answer_list)):
            error_number_list.append(answer_list[i][2])
            if answer_list[i][2]==0:
                right_number_list.append(answer_list[i][0])
            else:
                right_number_list.append(0)

        if max(right_number_list)!=0:
            return list_index_to_char(right_number_list.index(max(right_number_list)))
        else:
            return list_index_to_char(error_number_list.index(min(error_number_list)))

    return 0

def option_answers(option,point_list):
    ###option answer,return [rightnum,notJudgenum,errornum]
    print 'point_list',' '.join(point_list)
    option = text_body_regular(option)
    term_list = option.replace('\t',' ').replace('$$',' ').split(' ')

    rightNum = 0
    notJudgeNum = 0
    errorNum = 0
    for i in range(len(term_list)):
        if term_list[i]=='':
            continue

        if point_list!=[]:
            point = choose_point_for_term(term_list[i],point_list)
        else:
            point = ''
        print term_list[i],
        termAnswer = term_answer(term_list[i],point)
        print termAnswer

        if termAnswer==1:
            rightNum += 1
        elif termAnswer==0:
            notJudgeNum += 1
        else:
            errorNum += 1
    print
    #print 'rightNum',rightNum,'NotJudgeNum',notJudgeNum,'errorNum',errorNum
    return rightNum,notJudgeNum,errorNum

def term_answer(term,point):
    ### term answer
    term = text_encode_utf8(term)
    if term_only_judge(term)==True:
        print 'term',
        return term_judge(term)
    else:
        print 'pron',
        term_pron_list = seperate_term_pron_in_term(term)
        print 'term:',term_pron_list[0],'pron:',term_pron_list[1],
        return pron_judge(term_pron_list[0],term_pron_list[1],point)

def term_judge(term):
    ### term only
    return termCorrect.judge(term)

def pron_judge(term,pron,point):
    ### pron judge, have point , no point
    if point=='':
        return pronNoPosCorrect.judge(term,pron)
    else:
        position = point_position_in_term(term,point)
        print 'Point',point,'Pos',position,
        return pronCorrect.judge(term,pron,position)

def text_encode_utf8(text):
    ### encode utf-8 for text
    try:
        text = text.encode('utf-8')
    except:
        pass
    return text

def choose_point_list_for_option(option,point_list):
    ### choose point list for option, if have point
    #print 'option',option
    #print 'point list',point_list
    for each_point_list in point_list:
        all_exist = True
        for each_point in each_point_list:
            if each_point not in option:
                all_exist = False
                break
        if all_exist==True:
            return each_point_list
    return []

def choose_point_for_term(term,point_list):
    ### choose point for term, if have point
    for eachPoint in point_list:
        if eachPoint in term:
            return eachPoint

    return ''

def point_position_in_term(term,point):
    ### point position in term, if have point
    if point in term:
        return term.index(point)+1
    return 0

def seperate_term_pron_in_term(term):
    ### seperate term and pron, return [term,pron]
    term = tr.translate(term)
    sub_term = re.sub(r'[a-z|0-9]+','',term)
    pron = re.findall(r'[a-z|0-9]+',term)[0]
    pron_tran = re.sub(r'[0-9]','',pron) + re.sub(r'[a-z]','',pron)
    #sub_term = sub_term.replace('ɡ','')
    return sub_term,pron_tran

def term_only_judge(term):
    ### seperate if term only. True:only term / False: term and pron
    if term==re.sub(r'\w+','',term):
        return True
    return False

def list_index_to_char(index):
    ### index->answer, eg. 0->A
    return chr(index+65)

def text_body_regular(text):
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
    # 有 错
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

    return 0
