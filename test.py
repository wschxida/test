#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Cedar
# @Date  : 2020/7/29
# @Desc  :


import requests
from bs4 import BeautifulSoup
import json


def get_encoding(res):
    encoding = 'utf-8'
    if res.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(res.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = res.apparent_encoding
    return encoding

listpage_url = 'https://www.nfinv.com/'
res = requests.get(listpage_url)

encoding = get_encoding(res)

print(encoding)
res.encoding = encoding

soup = BeautifulSoup(res.text, 'lxml')
print(soup.title.text)
# print(encode_content)
