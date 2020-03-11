#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 1sapp_async.py
# @Author: Cedar
# @Date  : 2020/1/18
# @Desc  :

import time
import asyncio, aiohttp
from aiohttp import ClientSession
import json


tasks = []
url_template = "http://api.1sapp.com/wemedia/content/articleList?token=&dtu=200&version=0&os=android&id={}&page=1"
url_template = "https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=usa&src=typd&include_available_features=1&include_entities=1&reset_error_state=false&max_position="


async def get_response(url, semaphore, proxy):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy) as response:
                return await response.text()


async def run():
    semaphore = asyncio.Semaphore(100)  # 限制并发量为500
    proxy = "http://127.0.0.1:4411"
    for i in range(890946, 890947):
        task = asyncio.ensure_future(get_response(url_template.format(i + 1), semaphore, proxy))
        tasks.append(task)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    result = loop.run_until_complete(asyncio.gather(*tasks))
    print(result)
    end_time = time.time()
    time_length = end_time - start_time
    print(start_time)
    print(end_time)
    print(time_length)
