# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 12:15
# @Author  : Can Zhang
# @FileName: change_2_dict.py
# @Software: PyCharm
import json
with open ('aa.txt','r') as f:
    str = f.read().split('\n')


dict = {}
for i in str:
    dict_losd = i.split(' ')
    try:
        if len(dict_losd) == 2:
            dict[dict_losd[0].rstrip()] = dict_losd[1]
        elif len(dict_losd) == 1:
            dict[dict_losd[0].rstrip()] = ''
    except:
        print('transform failed',dict_losd)



print(dict)