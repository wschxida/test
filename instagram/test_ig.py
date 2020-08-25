#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_ig.py
# @Author: Cedar
# @Date  : 2020/7/20
# @Desc  :


import requests


BASE_URL = 'https://www.instagram.com/'
STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
USER_URL = BASE_URL + '{0}/?__a=1'
proxy = '127.0.0.1:7777'
proxy_list = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
USER_INFO = 'https://i.instagram.com/api/v1/users/{0}/info/'


def authenticate_as_guest():
    """Authenticate as a guest/non-signed in user"""
    session = requests.session()
    session.headers.update({'Referer': BASE_URL, 'user-agent': STORIES_UA})
    # req = session.get(BASE_URL, proxies=proxy_list)
    # print(req.cookies)
    # req.encoding = 'utf-8'
    # # print(req.text)
    # session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})
    # session.headers.update({'user-agent': CHROME_WIN_UA})

    # url = USER_URL.format('oppo')
    # url = 'https://www.instagram.com/bill'
    url = 'https://i.instagram.com/api/v1/users/7/info/'
    print(url)
    response = session.get(url, proxies=proxy_list)
    response.encoding = 'utf-8'
    text = response.text
    print(text)


if __name__ == '__main__':
    authenticate_as_guest()
    # user = 'bill'
    # r = requests.get('https://www.instagram.com/web/search/topsearch/?query=' + user, proxies=proxy_list, headers={
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}).text
    # print(r)
