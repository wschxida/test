
import time
import json
from lxml import etree
from datetime import datetime
from elasticsearch import Elasticsearch
import tldextract
import requests
import sqlite3
import re


def filter_punctuation(input_str):
    """
    过滤标点符号
    :param input_str:
    :return:
    """
    re_punctuation = re.compile("[`~!@#$^&*()=|｜{}':;',\\[\\].《》<>»/?~！@#￥……&*（）——|{}【】‘；：”“'\"。，、？%+_\r|\n|\\s]")
    result = re_punctuation.sub('', input_str)
    result = result.strip()
    return result


url = 'https://mil.news.sina.com.cn/'
response = requests.get(url, verify=False)
response.encoding = 'utf-8'
text = response.text
root = etree.HTML(text, parser=etree.HTMLParser(encoding='utf-8'))
items = root.xpath('//a')

i = 0
j = 0
for item in items:
    j += 1
    title = "".join(item.xpath('.//text()'))
    title = filter_punctuation(title)
    if len(title) > 10:
        i += 1
        print(title)
print(i)
print(j)
#
# conn = sqlite3.connect('test.db')
#
# print("Opened database successfully")
#
# conn.close()

# custom_str_invalid_list = [
#     '服务指南',
#     '.+-.+L',
#     '2D',
# '踩0',
# '5座',
# ]
# str_source = '局座'
# invalid_str_pattern = "|".join(custom_str_invalid_list)
# invalid_str = re.findall(invalid_str_pattern, str_source)
# print(invalid_str)
