#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 1sapp.py
# @Author: Cedar
# @Date  : 2020/1/18
# @Desc  :


import time
import requests
import json


url_template = "http://api.1sapp.com/wemedia/content/articleList?token=&dtu=200&version=0&os=android&id={}&page=1"


def run():
    result = []
    for i in range(890847, 890947):
        response = requests.get(url_template.format(i+1))
        page = json.loads(response.text)["data"]["total_page"]
        # print(page)
        result.append(page)
    print(result)


if __name__ == '__main__':
    start_time = time.time()
    run()
    end_time = time.time()
    time_length = end_time - start_time
    print(start_time)
    print(end_time)
    print(time_length)

