# coding=utf8


import time, json, sys
import os
import re
import random
import requests


def get_middle_str(content, start_str, end_str):
    """通用函数，获取前后两个字符串中间的内容"""
    try:
        start_index = content.index(start_str)
        if start_index >= 0:
            start_index += len(start_str)
        content = content[start_index:]
        end_index = content.index(end_str)
        return content[:end_index]
    except Exception as e:
        print(e)
        return None


def get_author_id(content):
    user_id = get_middle_str(content, 'entity_id:', ',')
    page_id = get_middle_str(content, 'pageID:"', '"')
    if user_id:
        author_id = user_id
    else:
        author_id = page_id
    return author_id



proxies = {
    'http': 'http://127.0.0.1:7777',
    'https': 'http://127.0.0.1:7777',
}

# headers = {
#         # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
#         "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#         "Upgrade-Insecure-Requests": "1",
#         "Cache-Control": "max-age=0"
#     }
#
# basic_url = 'https://m.facebook.com/'
# url = basic_url + 'bnbarry34'  # user: 1141684952
# url = basic_url + 'joebiden'  # page: 7860876103
# url = basic_url + 'profile.php?id=100026514127194'  # user: 100026514127194
# url = basic_url + 'groups/432930430071128/'  # group:432930430071128
# url = basic_url + 'groups/cryptofinancialworld/'  # group:1231416480213978

# response = requests.post(url, timeout=30, proxies=proxies, headers=headers, allow_redirects=False)
# response.encoding = 'utf-8'
# text = response.text
#
# print(text)
#
# author_id = get_author_id(text)
#
# print(author_id)

# domain = 'drugs.com'
# aa = f'''
# delete from column_link_oversea where domain_code='{domain}';
# delete from column_link where domain_code='{domain}';
# delete from listpage_url_check where domain_code='{domain}';
# delete from new_listpage_url where domain_code='{domain}';
# delete from new_listpage_url_cache where domain_code='{domain}';
#
# delete from listpage_url where domain_code='{domain}';
# delete from cloud_listpage_url where domain_code='{domain}';
# '''
#
# domain_list = ['powerchina.cn',
# 'aktivteck.com',
# 'zsdgsb.com',
# 'sampledrops.com',
# 'kdx35.com',
# 'suanxion.com',
# '5awx.cc',
# '05188.com',
# 'liptool.com',
# 'jrlady.cn',
# 'youabc.cn',
# 'cnncw.cn',
# 'geonet.cn',
# 'harbin123.com',
# 'zhongguojie.org',
# 'txwnx.com',
# '86516.com',
# 'jining666.com',
# 'qjczp.com',
# 'cnsccj.com',
# 'cplec.com',
# 'cvmkr.com',
# 'page.net.cn',
# 'freebaidu.cn',
# 'jsygc.com',
# 'weixintouxiang.cn',
# 'freebaidu.cn',
# 'jnrcw.net',
# 'baixing.com',
# 'dinakaufman.com',
# 'guandang.net',
# 'xuehai.net',
# 'jljxcfsb.com',
# 'gyxww.cn',
# 'ygxnk.com',
# 'stcpnyinger.com',
# 'guaiju5.cn',
# 'qingdao666.com'
# ]
#
# for domain in domain_list:
#     aa = f'''
#     delete from cloud_listpage_url where domain_code like'%{domain}';
#     '''
#     print(aa)


#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
#     'accept-encoding': 'gzip, deflate',
#     'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw',
#     'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
# }
#
# url = 'http://www.whoopture.com/news/20200930/503895.html'
#
# response = requests.get(url)
# text = response.text
# print(text)
#
#
# def print_1():
#     print(1)
#
#
# def print_2():
#     print(3)
#
#
# print_1()
# print_2()
# print(3)
# print(4)
#
#
#
# class A(type):
#     def __new__(cls, name, bases, dct):  # 注意第一个参数是cls而不是self
#         print('create class %s' % name)
#         return type.__new__(cls, name, bases, dct)
#
#     def __init__(cls, name, bases, dct):
#         print('Init class %s' % name)
#         type.__init__(cls, name, bases, dct)
#
#
# class B(metaclass=type):
#     def b(self):
#         print('b')
#
#
# ins_1 = B()
# ins_1.b()

import time
import datetime


cur_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


print(cur_timestamp)
