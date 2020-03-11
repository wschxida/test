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
# url_template = "http://api.1sapp.com/wemedia/content/articleList?token=&dtu=200&version=0&os=android&id=891848&page={}"
url_template = "http://api.1sapp.com/wemedia/content/articleList?token=&dtu=200&version=0&os=android&id={}&page=1"


async def get_response(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()


async def run():
    semaphore = asyncio.Semaphore(100)  # 限制并发量为500
    for i in range(880947, 890947):
        task = asyncio.ensure_future(get_response(url_template.format(i + 1), semaphore))
        tasks.append(task)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    result = loop.run_until_complete(asyncio.gather(*tasks))

    pages = []
    for result_response in result:
        page = json.loads(result_response)["data"]["total_page"]
        # print(page)
        pages.append(page)
    print(pages)
    end_time = time.time()
    time_length = end_time - start_time
    print(start_time)
    print(end_time)
    print(time_length)
