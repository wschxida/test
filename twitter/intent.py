#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : intent.py
# @Author: Cedar
# @Date  : 2020/9/21
# @Desc  :

import requests
from requests.adapters import HTTPAdapter
import html
import json
import random
import logging


logger = logging.getLogger('twitterscraper')
HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST), 'X-Requested-With': 'XMLHttpRequest'}
logger.info(HEADER)
print(HEADER)


def extractor_get_tweet_of_url(url, proxies=None):
    headers = {
        "Host": "twitter.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=(from%3AVOAChinese)&src=typd&include_available_features=1&include_entities=1&reset_error_state=false&max_position=",
        "Connection": "keep-alive",
        'Cookie': '_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCFQdtq90AToMY3NyZl9p%250AZCIlNDdiMThiZDU1NTc4ZTE5NzY1MDEyMWQ1ODQ2OWY4Mzk6B2lkIiViODVk%250AYzRiMDMzMjdlMzkzMGQwOTBiYjg2MDNjM2UwZg%253D%253D--75ce0f064cc3b85b150ab97da220523c18974578; personalization_id="v1_V8aQmuZbwJ13ptpimuuZVQ=="; guest_id=v1%3A160067578196961723; ct0=d224988bb248ae847de105ac5d407df7; __utma=43838368.78773043.1600675790.1600675790.1600675790.1; __utmb=43838368.1.9.1600675790; __utmc=43838368; __utmz=43838368.1600675790.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); gt=1307967101911674880; _ga=GA1.2.78773043.1600675790; _gid=GA1.2.825472215.1600678638',
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    print(url)
    # requests 重试机制
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.get(url, proxies=proxies, headers=headers, timeout=10)
    response.encoding = "utf-8"
    data = response.text
    return data


def main():

    proxies = {
        'http': 'http://127.0.0.1:7777',
        'https': 'http://127.0.0.1:7777'
    }
    # query = '''
    # {"url": "https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=(from%3AVOAChinese)&src=typd&include_available_features=1&include_entities=1&reset_error_state=false&max_position="}
    # '''
    # query = '''
    #     {"url": "https://twitter.com/i/profiles/show/enlightenmedia5/timeline/tweets?include_available_features=1&lang=en&include_entities=1&include_new_items_bar=true"}
    #     '''
    proxies = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'}
    q = 'VOAChinese'
    lang = 'en'
    pos = ''
    u = 'VOAChinese'
    url = 'https://twitter.com/search?q=%40VOAChinese&f=live'
    INIT_URL = f'https://twitter.com/search?f=tweets&vertical=default&q={q}&l={lang}'
    RELOAD_URL = f'''https://twitter.com/i/search/timeline?f=tweets&vertical=default&include_available_features=1&include_entities=1&reset_error_state=false&src=typd&max_position={pos}&q={q}&l={lang}'''
    INIT_URL_USER = f'https://twitter.com/{u}'
    RELOAD_URL_USER = f'''https://twitter.com/i/profiles/show/{u}/timeline/tweets?include_available_features=1&include_entities=1&max_position={pos}&reset_error_state=false'''

    result = extractor_get_tweet_of_url(url, proxies)
    print(result)


if __name__ == '__main__':
    main()
