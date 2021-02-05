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


BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
LOGOUT_URL = BASE_URL + 'accounts/logout/'
CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
USER_URL = BASE_URL + '{0}/?__a=1'
USER_INFO = 'https://i.instagram.com/api/v1/users/{0}/info/'
STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'


proxies = {
    'http': 'http://127.0.0.1:7777',
    'https': 'http://127.0.0.1:7777'
}
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "keep - alive",
    }

url = 'https://i.instagram.com/api/v1/users/34/info/'
url = 'https://i.instagram.com/api/v1/users/bill/info/'

session = requests.Session()
"""Authenticate as a guest/non-signed in user"""
session.headers.update({'Referer': BASE_URL, 'user-agent': STORIES_UA})
req = session.get(BASE_URL, proxies=proxies)
session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
# session.headers.update({'user-agent': CHROME_WIN_UA})
rhx_gis = ""
authenticated = True
print(req.cookies['csrftoken'])

response = session.get(url, proxies=proxies, allow_redirects=False)
response.encoding = 'utf-8'
text = response.text
print(text)

