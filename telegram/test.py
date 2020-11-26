#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Cedar
# @Date  : 2020/11/16
# @Desc  :

import requests


url = 'http://www.xyferlan.cn'
headers = {
    'Host': 'www.xyferlan.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
}
response = requests.get(url, headers=headers, allow_redirects=True)
response.encoding = 'gb2312'
print(response.url)
text = response.text
print(text)
