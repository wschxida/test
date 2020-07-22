#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : IG_login.py
# @Author: Cedar
# @Date  : 2019/11/21
# @Desc  :

# import requests
#
# header = {
#     'Host': 'www.instagram.com',
#     'Connection': 'keep-alive',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
#     'Accept': '*/*',
#     'Referer': 'https://www.instagram.com/bill/following/',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cookie': 'mid=XcjUugALAAFqxdFQdYQ1NjdEediM; rur=PRN; ig_did=54FE05C7-08A5-4DE5-BE14-628FF64FE173; csrftoken=IpIyvemxyvn76av3pbuvlJPc4hTscrH4; shbid=8429; shbts=1574301106.5372798; ds_user_id=11862252815; sessionid=11862252815%3AtKqd3NNZMFYSF9%3A16; urlgen="{\"172.105.235.219\": 63949}:1iXbhu:mWoQPq_Pl_NtJHc-71pVK4EbqAA"',
# }
#
# proxy = {"http": "http://127.0.0.1:7777", "https": "http://127.0.0.1:7777"}
#
# url = 'https://www.instagram.com/graphql/query/?query_hash=bd90987150a65578bc0dd5d4e60f113d&variables=%7B%22fetch_media_count%22%3A0%2C%22fetch_suggested_count%22%3A30%2C%22ignore_cache%22%3Atrue%2C%22filter_followed_friends%22%3Atrue%2C%22seen_ids%22%3A%5B%5D%2C%22include_reel%22%3Atrue%7D'
#
# reponse = requests.get(url, headers=header, proxies=proxy)
# print(reponse.text)

# ----------------------------------------------------------------------------------------

import json
import requests


BASE_URL = 'https://www.instagram.com/'
LOGIN_URL = BASE_URL + 'accounts/login/ajax/'
# LOGOUT_URL = BASE_URL + 'accounts/logout/'
# STORIES_UA = 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
# CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
# USER_URL = BASE_URL + '{0}/?__a=1'

CHROME_WIN_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
# STORIES_UA = 'Instagram 52.0.0.8.83 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'
STORIES_UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'


class InstagramScraper(object):

    def __init__(self, **kwargs):
        # self.login_user = "Thervildday@gmail.com"
        # self.login_pass = "TD#Ins@0817$%"
        self.login_user = "squeerssecretary"
        self.login_pass = "jfa6zk8r"
        self.proxies = {"http": "http://127.0.0.1:7777", "https": "http://127.0.0.1:7777"}
        self.session = requests.Session()
        self.session.proxies = self.proxies
        # self.session.headers = {'user-agent': CHROME_WIN_UA}
        self.cookies = None
        self.authenticated = False
        self.logged_in = False

    def authenticate_with_login(self):
        """Logs in to instagram."""
        self.session.headers.update({'Referer': BASE_URL, 'user-agent': CHROME_WIN_UA})
        req = self.session.get(BASE_URL)
        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        login_data = {'username': self.login_user, 'password': self.login_pass}
        login = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True, proxies=self.proxies)
        print(login.cookies)
        # self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
        # login_text = json.loads(login.text)
        cookies = login.cookies.get_dict()
        for i in cookies:
            print(i)
            print(cookies[i])

        # if login_text.get('authenticated') and login.status_code == 200:
        #     self.authenticated = True
        #     self.logged_in = True
        #     self.session.headers.update({'user-agent': STORIES_UA})
        #     self.rhx_gis = ""
        # else:
        #     pass

    def fetch_following(self):
        # url = 'https://www.instagram.com/graphql/query/?query_hash=bd90987150a65578bc0dd5d4e60f113d&variables=%7B%22fetch_media_count%22%3A0%2C%22fetch_suggested_count%22%3A30%2C%22ignore_cache%22%3Atrue%2C%22filter_followed_friends%22%3Atrue%2C%22seen_ids%22%3A%5B%5D%2C%22include_reel%22%3Atrue%7D'
        url = 'https://www.instagram.com/bill'
        response = self.session.get(url)
        print(response.text)


scraper = InstagramScraper()
scraper.authenticate_with_login()
scraper.fetch_following()

