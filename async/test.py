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


async def get_response(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()


async def run():
    semaphore = asyncio.Semaphore(100)  # 限制并发量为500
    for i in range(1):
        url = 'https://www.nfinv.com/'
        task = asyncio.ensure_future(get_response(url, semaphore))
        tasks.append(task)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    result = loop.run_until_complete(asyncio.gather(*tasks))
    for result_response in result:
        print(result_response)
