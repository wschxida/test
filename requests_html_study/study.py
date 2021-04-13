#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/3/26
# @Desc  :

import requests
from requests_html import HTMLSession


url = 'https://www.jianshu.com/u/ef4f2422125f?utm_source=desktop&utm_medium=index-users'
res = requests.get(url)
res.encoding = 'utf-8'
text = res.text
# print(text)
with open('requests.html', 'w+', encoding='utf-8') as a:
    a.write(text)
a.close()


session = HTMLSession()
r = session.get(url, verify=False)
r.html.render(wait=5, timeout=20, scrolldown=10, sleep=2)
text_html = r.html.html
# print(text_html)
with open('requests_html.html', 'w+', encoding='utf-8') as b:
    b.write(text_html)
b.close()
