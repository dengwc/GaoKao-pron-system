# -*- coding:utf-8 -*-
# segment
from pyltp import Segmentor
segmentor = Segmentor()
segmentor.load('./ltp-model/cws.model')

def segment(text):
    return segmentor.segment(text)
