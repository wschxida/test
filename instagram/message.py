#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : message.py
# @Author: Cedar
# @Date  : 2020/12/4
# @Desc  :

import requests
import sys


def get_ig_html():

    proxy = "127.0.0.1:7777"
    proxy_list = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'}
    # headers = {
    #     'User-Agent': 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15',
    # }

    try:
        BASE_URL = 'https://www.instagram.com/'
        CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
        MAIN_STORIES_URL = BASE_URL + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables=%7B%22reel_ids%22%3A%5B%22{0}%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%7D'

        session = requests.session()
        # session.headers.update({'Referer': BASE_URL, 'user-agent': STORIES_UA})
        # req = session.get(BASE_URL, proxies=proxy_list)
        # print(req.headers)
        # session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
        session.headers.update({'user-agent': CHROME_WIN_UA})

        # query_url = MAIN_STORIES_URL.format(34)
        query_url = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%2234%22%2C%22first%22%3A50%2C%22after%22%3A%22%22%7D'
        response = session.get(query_url, proxies=proxy_list, timeout=30)
        result = response.text
        print(result)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_ig_html()
