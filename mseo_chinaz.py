#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mseo_chinaz.py
# @Author: Cedar
# @Date  : 2020/6/1
# @Desc  :


import requests
import re
from urllib import parse


url = 'http://mseo.chinaz.com/?host=tianya.cn'
session = requests.session()

response = session.get(url)
response.encoding = 'utf-8'
text = response.text
print(text)

deskey = re.findall("desKey = '(.*)'", text)[0]
print(deskey)
deskey = parse.quote(deskey, 'utf-8')
get_alexa_url = f'http://mseo.chinaz.com/Handle/AjaxHandler.ashx?action=GetAlexa&host=tianya.cn&deskey={deskey}'
# get_alexa_url = f'http://mseo.chinaz.com/ajaxseo.aspx?t=alexa&enkey={deskey}&host=tianya.cn'

print(get_alexa_url)

headers = {
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://seo.chinaz.com/?host=tianya.cn",
    "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Host": "mseo.chinaz.com",
    "Connection": "Keep-Alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3756.400 QQBrowser/10.5.4043.400",
}

response_alexa = session.get(get_alexa_url, headers=headers)
response_alexa.encoding = 'utf-8'
text = response_alexa.text
print(text)
