#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 1sapp_async.py
# @Author: Cedar
# @Date  : 2020/1/18
# @Desc  :

import time
import asyncio
import aiohttp
from aiohttp import ClientSession
import json


tasks = []
proxy = 'http://192.168.1.180:3351'


async def get_response(url, semaphore):
    async with semaphore:
        timeout = aiohttp.ClientTimeout(total=10)
        connector = aiohttp.TCPConnector(limit=60, verify_ssl=False)  # 60小于64。也可以改成其他数
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            try:
                async with session.get(url, proxy=proxy) as response:
                    return await response.text()
            except Exception as e:
                print(e)


async def run():
    semaphore = asyncio.Semaphore(100)  # 限制并发量为500
    for i in range(100):
        url = 'https://www.bbc.com/'
        task = asyncio.ensure_future(get_response(url, semaphore))
        tasks.append(task)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    result = loop.run_until_complete(asyncio.gather(*tasks))
    success_count = 0
    for result_response in result:
        if result_response:
            success_count += 1
    print(success_count)
