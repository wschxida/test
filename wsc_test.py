
import time
import json
from lxml import etree
from datetime import datetime
from elasticsearch import Elasticsearch
import tldextract
import requests
import sqlite3
import re
import os
import random
import pymysql
import warnings

# 忽略mysql插入时主键重复的警告
warnings.filterwarnings('ignore')


# def filter_punctuation(input_str):
#     """
#     过滤标点符号
#     :param input_str:
#     :return:
#     """
#     re_punctuation = re.compile("[`~!@#$^&*()=|｜{}':;',\\[\\].《》<>»/?~！@#￥……&*（）——|{}【】‘；：”“'\"。，、？%+_\r|\n|\\s]")
#     result = re_punctuation.sub('', input_str)
#     result = result.strip()
#     return result
#
#
# url = 'https://mil.news.sina.com.cn/'
# response = requests.get(url, verify=False)
# response.encoding = 'utf-8'
# text = response.text
# root = etree.HTML(text, parser=etree.HTMLParser(encoding='utf-8'))
# items = root.xpath('//a')
#
# i = 0
# j = 0
# for item in items:
#     j += 1
#     title = "".join(item.xpath('.//text()'))
#     title = filter_punctuation(title)
#     if len(title) > 10:
#         i += 1
#         print(title)
# print(i)
# print(j)
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


def get_host_code(url):
    host_code = ''
    domain_info = tldextract.extract(url)
    # print(domain_info)
    if domain_info.domain:
        if is_ip(domain_info.domain):
            host_code = domain_info.domain
        elif domain_info.suffix:
            host_code = f"{domain_info.subdomain}.{domain_info.domain}.{domain_info.suffix}"
            if host_code.find('%') > -1:
                host_code = ''
    return host_code.strip('.')


def is_ip(_str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(_str):
        return True
    else:
        return False


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


score_message = ''
url = 'https://news.qq.com/fg/hjk?hh=1&newszixungg=2.php#'
url = 'https://news.qq.com/d'
title = '新闻的广'
score = 0
host_code = get_host_code(url)

custom_url_keyword_score_dict = {
    'news': 100,
    'zixun': 80,
    'xinwen': 100,
    'index': 80,
    '.asp': -50,
    '.php': -50,
}

custom_title_keyword_score_dict = {
    # 简体中文
    '新闻': 100,
    '资讯': 100,
    '时事': 100,
    '时政': 100,
    '生活': 50,
    '房屋出租': -20,
    '吃喝玩乐': -20,
    '优惠信息': -20,
    '招聘': -80,
}


custom_title_invalid_list = [
    'javascript',
    'company',
    'Part [0-9]+',
    'About Us'
]

title = '新闻的 广'
invalid_title_pattern = "|".join(custom_title_invalid_list)
invalid_title = re.findall(invalid_title_pattern, title)

custom_url_invalid_list = [
    '[/.]mall\.51\.ca',
    '[/.]brasilcn\.com/job/',
    '/job/'
]


title = '即时新闻 | 头条推荐 | 新闻时事 | 热点动态 | 爱新闻 newslove.net - 用心聆听身边的大小故事'
try:
    title = title.split('-')[0].strip()
except Exception as e:
    title = title
try:
    title = title.split('_')[0].strip()
except Exception as e:
    title = title
try:
    title = title.split(',')[0].strip()
except Exception as e:
    title = title
try:
    title = title.split('，')[0].strip()
except Exception as e:
    title = title
try:
    title = title.split('|')[0].strip()
except Exception as e:
    title = title
try:
    title = title.split(' ')[0].strip()
except Exception as e:
    title = title

print(title)

url_list = [
    'https://www.runoob.com/redis/redis-tutorial.html',
    'https://www.runoob.com/redis/redis-intro.html',
    'https://www.runoob.com/redis/redis-install.html',
    'https://www.runoob.com/redis/redis-conf.html',
    'https://www.runoob.com/redis/redis-data-types.html',
    'https://www.pythonf.cn/read/101780',
    'https://www.pythonf.cn/read/139371',
    'https://www.pythonf.cn/read/139370',
    'https://www.pythonf.cn/read/139369',
    'https://www.pythonf.cn/read/139368',
]

for url in url_list:
    file = str(url_list.)
    print(file)