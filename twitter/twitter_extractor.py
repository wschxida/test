#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/08/24 18:08
# @Author  : wcx
# @Email   : 972761574@qq.com
# @File    : fetch_twitter.py
# @Software: PyCharm

from functools import wraps
from lxml import etree
from locale import getdefaultlocale
from urllib.parse import quote
import sys
import os
import random
import json
import requests
import time
import datetime


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


def get_html(url):
    for i in range(3):
        proxies = None
        proxy_file = './config/proxy_list.txt'
        if os.path.exists(proxy_file):
            proxy_ip = get_one_proxy(proxy_file)
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
        try:
            response = requests.get(url, proxies=proxies, timeout=45).text
            return response
            break
        except Exception as e:
            print(str(e))
            continue


def get_html_via_cloud(url):
    url = url.split('com/')[-1]
    req_data = quote(url)
    req_url = f'http://107.180.91.218:5100/service_app?agent_type=twitter&fetch_type=get_tweet_of_url&query_dict=%7B%22url%22%3A%22{req_data}"%7D%0D%0A'
    for i in range(3):
        proxies = None
        proxy_file = './config/proxy_list.txt'
        if os.path.exists(proxy_file):
            proxy_ip = get_one_proxy(proxy_file)
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
        try:
            response = requests.get(req_url, proxies=proxies, timeout=45).text
            res_json = json.loads(response)["data"]
            return res_json
            break
        except Exception as e:
            print(str(e))
            continue


def get_profile(url, output_dir):
    for i in range(3):
        try:
            response = get_html(url)
            if len(response.text) > 10:
                with open(output_dir, 'w', encoding="utf-8") as f:
                    f.write(response.text)
                break
        except Exception as e:
            print(e)


def get_id(request_account):
    url = f"http://107.180.91.218:5100/service_app?agent_type=twitter&fetch_type=get_profile&target_express={request_account}"
    response = get_html(url)
    html = json.loads(response)
    author_id = html["target_profile"][0]["author_id"]
    author_name = html["target_profile"][0]["author_name"]
    file_name = f"./temp/{request_account}.id"
    with open(file_name, 'w') as f:
        f.write(author_id)
    return [author_id, author_name]


def tweet_detail(url):
    try:
        detail_html = get_html(url)
        det_byte = bytes(detail_html, encoding="utf8")
        html = etree.HTML(det_byte)
        img_url = html.xpath('//div[@class="media"]/img[1]/@src')[0].replace(':small', '')
        error_page = html.xpath("//div[@class='system']//text()")
        if len(error_page) > 0:
            detail_html = get_html_via_cloud(url)
            det_byte = bytes(detail_html, encoding="utf8")
            html = etree.HTML(det_byte)
            img_url = html.xpath('//div[@class="media"]/img[1]/@src')[0].replace(':small', '')
        return img_url
    except Exception as e:
        print(str(e))
        pass


def get_tweet(*params):
    url = params[0]
    request_account = str(params[0]).split('/')[-1]
    request_author_id = str(params[2][0])
    request_author_name = str(params[2][1])
    url_prefix = url
    for i in range(params[1]):
        try:
            response = get_html(url)
            # response = get_html_via_cloud(url)
            page_content = parse_html(response)
            data_list = page_content[0]
            next_cursor = page_content[1]
            error_page = page_content[2]
            if len(error_page) > 0:
                response = get_html_via_cloud(url)
                page_content = parse_html(response)
                data_list = page_content[0]
                next_cursor = page_content[1]
            if i == 0:
                with open(profile_dir, 'w', encoding="utf-8") as f:
                    f.write(response)
            for x in data_list:
                author_account = x["article_url"].split('/')[-3]
                message_raw_id = x["article_url"].split('/')[-1]
                x["author_id"] = request_author_id
                x["author_name"] = request_author_name
                x["author_account"] = request_account
                if author_account != request_account:
                    x["is_retweeted"] = 1
                    del x["is_image"]
                    del x["is_video"]
                    str_json = json.dumps(x)
                    with open(retweet_dir, 'a', encoding="utf-8") as f:
                        f.write(str_json + '\r')
                else:
                    if len(x["is_image"]) > 0:
                        detail_url = x["article_url"].replace('twitter', 'mobile.twitter')
                        img_url = tweet_detail(detail_url)
                        x["img_url"] = img_url
                    if len(x["is_video"]) > 0:
                        vedio_url = f"https://twitter.com/i/videos/tweet/{message_raw_id}"
                        x["vedio_url"] = vedio_url
                    del x["is_image"]
                    del x["is_video"]
                    str_json = json.dumps(x)
                    with open(message_dir, 'a', encoding="utf-8") as f:
                        f.write(str_json + '\r')
            if len(next_cursor) > 0:
                next_cursor = next_cursor[0].split('=')[-1]            
                url = f"{url_prefix}?max_id={next_cursor}"
                print(url)
            else:
                break
        except Exception as e:
            print(str(e))
            break


def parse_html(response):
    """
    解析获取到的message_html源码，提取必须字段，索引至ES
    :return:
    """
    res_byte = bytes(response, encoding="utf-8")
    data_list = []
    xpath_items = '//table[contains(@class,"tweet")]'
    article_url = '//td[@class="timestamp"]/a[1]/@href'
    author_name = '//strong[@class="fullname"]/text()'
    publish_time = '//td[@class="timestamp"]/a[1]/text()'
    content_html = '//td[@class="tweet-content"]'
    is_image = './/a[contains(@data-url,"photo")]/@data-url'
    is_video = './/a[contains(@data-url,"video")]/@data-url'
    html = etree.HTML(res_byte)
    items = html.xpath(xpath_items)
    for i, article in enumerate(items):
        data = {}
        data['is_image'] = article.xpath(is_image)
        data['is_video'] = article.xpath(is_video)
        data['article_url'] = f"https://twitter.com{article.xpath(article_url)[i].split('?')[0]}"
        data['ORIGINAL_AUTHOR_NAME'] = article.xpath(author_name)[i]
        data['article_pubtime_str'] = article.xpath(publish_time)[i]
        data['article_content'] = str(etree.tostring(article.xpath(content_html)[i], encoding='utf-8'),
                                      encoding="utf-8")
        publish_time_str = article.xpath(publish_time)[i]
        data['publish_time_str'] = publish_time_str
        data['article_pubtime'] = date_format(publish_time_str)
        data_list.append(data)
    next_cursor = html.xpath("//div[@class='w-button-more']/a[1]/@href")
    error_page = html.xpath("//div[@class='system']//text()")
    return [data_list, next_cursor, error_page]


def date_format(time_str):
    """
    mobile接口的列表数据没有时间戳，只有时间字符串。改函数作用为修改时间字符串为标准时间格式
    :param time_str: 列表上的时间字符串，格式为2s,5        time_str = int(time_str.replace("s", ''))
m,6h,March 24....
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
        time_list = time_str.split(' ')
        if len(time_list) == 3:
            year = "20" + time_list[-1]
            month = time_list[1]
            date = time_list[0]
            time_str = f"{year}-{month}-{date}"
            format_time = time_str
        else:
            format_time = datetime.datetime.strptime('2020 ' + time_str, '%Y %b %d')
            time_difference = str(current_time-format_time)
            if '-' in time_difference:
                format_time = datetime.datetime.strptime('2019 ' + time_str, '%Y %b %d')
            format_time=str(format_time)
    return format_time


if __name__ == '__main__':
    start_time = time.time()
    # account = "Ahmed_2021"
    # loop_count = 160
    account = sys.argv[1]
    loop_count = sys.argv[2]
    message_dir = f"./temp/message/{account}.txt"
    profile_dir = f"./temp/profile/{account}.txt"
    retweet_dir = f"./temp/retweet/{account}.txt"
    profile_url = f"https://mobile.twitter.com/{account}"
    author_info = get_id(account)
    get_tweet(profile_url, int(loop_count), author_info)
    print("spend time : %s" % (time.time() - start_time))
