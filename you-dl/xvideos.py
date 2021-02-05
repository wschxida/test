#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : facebook_extractor.py
# @Author: Cedar
# @Date  : 2020/12/16
# @Desc  :

from lxml import etree
from requests.compat import urljoin


with open('seseporn.html', 'r', encoding='utf-8') as f:
    html = f.read()

root = etree.HTML(html)
items = root.xpath('//a/@href')
result = []
for item in items:
    url = urljoin('https://www.xvideos.com/', item)
    if 'https://www.xvideos.com/video' in url and 'videos-i-like' not in url:
        result.append(url)

result_set = set(result)
result = list(result_set)
print(result)
print(len(result))
