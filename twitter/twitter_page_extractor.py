# -*- coding: utf-8 -*-
# @Time    : 2020/08/12 9:44
# @Author  : wcx
# @File    : twitter_page_extractor.py
# @Software: PyCharm

from gevent import monkey

monkey.patch_all()
from locale import getdefaultlocale
import gevent
import time
import redis
import hashlib
import re
import sys
import requests
import json
import datetime
import copy
import os
import random
from lxml import etree

# 程序出口redis相关信息
params = dict(host='192.168.1.134', port='6380', password='ks_3000', db=0, decode_responses=True)

pool = redis.ConnectionPool(**params)
Rs = redis.Redis(connection_pool=pool)

# 按照天数计数入库信息
today_date = datetime.datetime.now().strftime('%Y%m:%d')


def get_md5(in_str='', coding='UTF-16LE'):
    in_str = in_str.encode(coding)
    md5_str = hashlib.md5(in_str).hexdigest()  # 加密
    return md5_str


def remove_none_printable_char(in_str):
    out_str = re.sub(r'[\x00-\x20]', '', in_str)
    return out_str


def py_md5(in_str, is_file=False, remove_none_printable_chars=False, case_sensitivity=False):
    if is_file:
        return ''
    if remove_none_printable_chars:
        in_str = remove_none_printable_char(in_str)
    if case_sensitivity:
        in_str = in_str.lower()
    return get_md5(in_str, 'UTF-16LE')


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


def get_html(url):
    """
    传入url，判断是否需要代理，随机取一个作为proxy发送get请求,重试三次
    :param url:
    :return:
    """
    for i in range(3):
        proxies = None
        proxy_file = 'proxy_list.txt'
        if os.path.exists(proxy_file):
            proxy_ip = get_one_proxy(proxy_file)
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            return response
            break
        except Exception as e:
            continue


def date_format(time_str):
    """
    mobile接口的列表数据没有时间戳，只有时间字符串。改函数作用为修改时间字符串为标准时间格式
    :param time_str: 列表上的时间字符串，格式为2s,5m,6h,March 24....
    :return:
    """
    current_time = datetime.datetime.now()
    if time_str.endswith("s"):
        time_str = int(time_str.replace("s", ''))
        time_difference = datetime.timedelta(seconds=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    elif time_str.endswith("m"):
        time_str = int(time_str.replace("m", ''))
        time_difference = datetime.timedelta(minutes=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    elif time_str.endswith("h"):
        time_str = int(time_str.replace("h", ''))
        time_difference = datetime.timedelta(hours=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    else:
        format_time = str(datetime.datetime.strptime('2020 ' + time_str, '%Y %b %d'))
    return format_time


def parse_html(response):
    """
    解析获取到的message_html源码，提取必须字段，索引至ES
    :return:
    """
    data_list = []
    xpath_items = '//table[contains(@class,"tweet")]'
    article_url = '//td[@class="timestamp"]/a[1]/@href'
    author_name = '//strong[@class="fullname"]/text()'
    publish_time = '//td[@class="timestamp"]/a[1]/text()'
    content_html = '//td[@class="tweet-content"]'
    html = etree.HTML(response.content)
    items = html.xpath(xpath_items)
    for i, article in enumerate(items):
        data = {}
        data['article_url'] = f"https://twitter.com{article.xpath(article_url)[i].split('?')[0]}"
        data['article_author'] = article.xpath(author_name)[i]
        data['article_pubtime_str'] = article.xpath(publish_time)[i]
        data['article_content'] = str(etree.tostring(article.xpath(content_html)[i], encoding='utf-8'),
                                      encoding="utf-8")
        publish_time_str = article.xpath(publish_time)[i]
        data['article_pubtime'] = date_format(publish_time_str)
        data_list.append(data)
    next_cursor = html.xpath("//div[@class='w-button-more']/a[1]/@href")[0]
    return [data_list, next_cursor]


def save_data(data_list, author_raw_id, website_no):
    """
    补充字段，rpush到这两个键article_detail_data、article_content_data
    :param data:
    :param url:
    :return:
    """
    for data in data_list:
        article_detail_data = copy.deepcopy(data)
        article_content_data = copy.deepcopy(data)

        article_url = article_detail_data['article_url']
        article_content = article_detail_data['article_content']
        pattern = re.compile(r'<[^>]+>', re.S)
        article_title = pattern.sub('', article_content).replace('\n', '').replace(' ', '').strip()[0:50]
        article_detail_data["article_title"] = article_title
        article_detail_data['website_no'] = website_no
        article_detail_data['author_raw_id'] = author_raw_id
        article_url_md5_id = py_md5(article_url, False, True, True)
        article_detail_data["article_url_md5_id"] = article_url_md5_id
        article_detail_data["media_type_code"] = "@"
        article_detail_data["domain_code"] = "twitter.com"
        article_detail_data["is_with_content"] = 1
        article_detail_data["is_extract_after_detail"] = 0
        article_detail_data["language_code"] = "CN"
        article_detail_data["refpage_type"] = "K"

        article_detail_data['record_md5_id'] = article_url_md5_id
        article_content_data['article_record_md5_id'] = article_url_md5_id

        article_detail_data['table_name'] = 'article_detail'
        article_content_data['table_name'] = 'article_content'
        print(article_detail_data)

        Rs.rpush('public:items', json.dumps(article_detail_data))
        Rs.rpush('public:items', json.dumps(article_content_data))
        Rs.incr('counter:twitter:%s' % today_date)


def get_data(url, author_raw_id, website_no):
    """
    协程主函数，主要功能：请求url，解析html,入库redis
    :param url:
    :param author_raw_id:
    :param website_no:
    :return:
    """
    try:
        page_content = get_html(url)
        if page_content:
            if page_content.status_code == 200:
                data_list = parse_html(page_content)
                save_data(data_list, author_raw_id, website_no)
            else:
                with open("unvalid.txt", 'a') as f:
                    f.write(url + ' ' + str(page_content.status_code)+'\n')
        else:
            with open("failure.txt", 'a') as f:
                f.write(url + '\n')
    except Exception as e:
        print(url)
        print("error message:" + str(e))


def main():
    """
    主函数：批处理传入website_no与作者列表文件名两个参数,程序将读取作者列表，100个并发请求的形式遍历列表，遍历结束后跳出循环，程序结束
    :return:
    """
    # website_no = sys.argv[1]
    # input_file = sys.argv[2]
    start_time = time.time()
    website_no = 'S18622'
    input_file = "keyword.txt"
    with open(input_file, 'r') as fp:
        urls = fp.readlines()
    while True:
        g_l = []
        print(len(urls))
        if len(urls) >= 50:
            for x in range(50):
                url = urls.pop()
                request_url = url.split('=')[1].strip()
                author_raw_id = url.split('=')[0]
                g = gevent.spawn(get_data, request_url, author_raw_id, website_no)
                g_l.append(g)
        else:
            for x in range(len(urls)):
                url = urls.pop()
                request_url = url.split('=')[1].strip()
                author_raw_id = url.split('=')[0]
                g = gevent.spawn(get_data, request_url, author_raw_id, website_no)
                g_l.append(g)
        gevent.joinall(g_l)
        if len(urls) == 0:
            end_time = time.time()
            print(end_time - start_time)
            break


if __name__ == '__main__':
    main()
