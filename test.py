#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Cedar
# @Date  : 2020/7/29
# @Desc  :


import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote, unquote, urlencode
import clean_html_attr
from lxml import etree
from lxml.html import fromstring, tostring
from html.parser import unescape

proxies = {
    'http': 'http://127.0.0.1:7777',
    'https': 'http://127.0.0.1:7777'
}
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
url = 'https://www.facebook.com/pg/DonaldTrump/posts/?ref=page_internal'
url = 'https://www.facebook.com/moliwyes/posts'

response = requests.get(url, proxies=proxies, headers=headers)
data = response.text
# data = clean_html_attr.clean_html_attr(data)
result_html = etree.HTML(data)
items = result_html.xpath('//div[contains(@class,"userContentWrapper")]')

content = ''
for item in items:
    data = tostring(item, method='html')
    content = content + unescape(data.decode())

result_pattern = """
    <html>
    <head>
    <meta charset="utf-8">
    </head>
    <body>{}</body>
    </html>
    """
result = result_pattern.format(content)

with open('text.html', 'w', encoding='utf-8') as f:
    f.write(result)

