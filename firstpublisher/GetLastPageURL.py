#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 18:08
# @Author  : wcx
# @Email   : 972761574@qq.com
# @File    : first_publisher_scraper.py
# @Software: PyCharm

from async_timeout import timeout
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from re import findall
from locale import getdefaultlocale
from functools import wraps
import sys
import random
import os
import datetime
import time



def stat_time(fn):
    @wraps(fn)
    def wrap(*args, **kw):
        start_time = time.time()
        ret = fn(*args, **kw)
        ended_time = time.time()
        print("call {}() cost: {} seconds".format(fn.__name__, ended_time - start_time))
        return ret

    return wrap

def get_code_page():
    """
    Compatible with Linux and Windows
    :return:
    Linux:  ('en_US', 'UTF-8')
    Windows: ('zh_CN', 'cp936')
    """
    code_page = getdefaultlocale()[1]
    return code_page

def get_lines_from_file(file_path, remove_space_line=True):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as fp:
        content = fp.read().strip()
    try:
        content = content.decode('utf8')
    except Exception as e:
        content = content.decode(get_code_page())
    lines = content.splitlines()
    if remove_space_line:
        # 移除文件中的空行
        lines = [i for i in lines if i != '']
    return lines

def get_one_proxy(file_path='config/ProxyList.txt'):
    """
    随机取一个代理ip
    :param file_path:
    :return:一个代理ip
    """
    lines = get_lines_from_file(file_path)
    proxy_ip = random.sample(lines, 1)
    return proxy_ip[0].strip()


async def Response(session, url, proxies):
    with timeout(30):
        async with session.get(url, ssl=False, proxy=proxies, timeout=20) as response:
            return await response.text()


# 计算传入的URL中的时间和当前的时间差
def date_diff(url):
    dt2 = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime()), '%Y-%m-%d')
    dt = url[-17:-7]
    dt1 = datetime.datetime.strptime(dt, '%Y-%m-%d')
    day_diff = (dt2 - dt1).days
    return day_diff

# 传入tweet_list，以字典形式输出最小值 key:tweet_account, value:tweet_id
def min_tweet_id(*args):
    d = {}
    for tweet in args[0]:
        tweet_url = tweet.get('href')
        tweet_account = tweet_url.split('/')[1]
        tweet_id = int(tweet_url.split('/')[-1].replace('?p=v', ''))
        args[1][tweet_account] = tweet_id
    value = min(args[1].values())
    key = min(args[1], key=args[1].get)
    d[key] = value
    return d


#
async def main(proxy_file, input_file, output_file):
    """
    :param proxy_file: /config/proxy.txt
    :param input_file: {$fetch_task_id}.task
    :param output_file: $fetch_task_id}.txt
    :return:
    """
    url = str(get_lines_from_file(input_file)[0])
    day_diff = date_diff(url)
    url_prefix = url
    url_list = []
    id_list = {}
    start_time = time.time()
    #need_proxy = False


    if os.path.exists(proxy_file):
        proxy_ip = get_one_proxy(proxy_file)
        proxies = f"http://{proxy_ip}"
    else:
        proxies = ''





    # if os.path.exists(proxy_file):
    #     need_proxy = True
    # if need_proxy:
    #     proxy_ip = get_one_proxy(proxy_file)
    # else:
    #     proxy_ip = False
    # if proxy_ip:
    #     proxies = f"http://{proxy_ip}"
    # else:
    #     proxies = ''

    next_cursor = "1"
    # 如果发布时间在7天前，循环获取下一页按钮的href，获取到最后一页的最底部的tweet即可
    if day_diff > 7:
        while len(next_cursor) > 0:
            async with aiohttp.ClientSession() as session:
                try:
                    response = await Response(session, url, proxies)
                    soup = BeautifulSoup(response, "html.parser")
                    next_cursor = soup.find_all("div", "w-button-more")
                    try:
                        next_cursor = findall(r'next_cursor=(.*?)">', str(next_cursor))[0]
                    except Exception as e:
                        print(str(e) + " [x] feed.Mobile")
                    url = f"{url_prefix}&next_cursor={next_cursor}"
                    url_list.append(url)
                except Exception as e:
                    print("get last_page_url failure: " + str(e))
        if len(url_list) < 3:
            lastpage_url = url_prefix
        else:
            lastpage_url = url_list[-3]
        async with aiohttp.ClientSession() as session:
            try:
                last_page_html = await Response(session, lastpage_url, proxies)
            except Exception as e:
                print("get last_page_html failure: " + str(e))
        soup = BeautifulSoup(last_page_html, "html.parser")
        tweet_list = soup.find_all("table", "tweet")
        last_tweet_suffix = tweet_list[-1].get('href')
        last_tweet_url = f"http://www.twitter.com/{last_tweet_suffix}"
    # 如果发布时间在7天内，需要循环翻页，对比获取最小的tweet_id和与其对应的tweet_count，返回构造的tweet_url
    else:
        while len(next_cursor) > 0:
            async with aiohttp.ClientSession() as session:
                try:
                    response = await Response(session, url, proxies)
                    soup = BeautifulSoup(response, "html.parser")
                    tweets_list = soup.find_all("table", "tweet")
                    id_list = min_tweet_id(tweets_list, id_list)
                    next_cursor = soup.find_all("div", "w-button-more")
                    try:
                        next_cursor = findall(r'next_cursor=(.*?)">', str(next_cursor))[0]
                    except Exception as e:
                        print(str(e) + " [x] feed.Mobile")
                    url = f"{url_prefix}&next_cursor={next_cursor}"
                except Exception as e:
                    print("get last_page_html failure: " + str(e))
        for key, values in id_list.items():
            last_tweet_url = f"http://www.twitter.com/{key}/status/{values}"
            print(last_tweet_url)
    # 请求last_tweet_url, 将text保存到本地
    async with aiohttp.ClientSession() as session:
        try:
            last_tweet_html = await Response(session, last_tweet_url, proxies)
        except Exception as e:
            print("get last_tweet_html failure: "+str(e))
    with open(output_file, 'w', encoding='utf8') as fp:
        fp.write(last_tweet_html)
    ended_time = time.time()
    print(f"took time:{ended_time - start_time} seconds")



if __name__ == '__main__':
    argv = sys.argv
    target_express = argv[1]
    proxy_file = 'config/ProxyList.txt'
    input_file = f"{target_express}.task"
    output_file = f"{target_express}.txt"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(proxy_file, input_file, output_file))