#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_proactor.py
# @Author: Cedar
# @Date  : 2020/11/23
# @Desc  :

import time, asyncio, aiohttp
from threading import Thread


async def do_some_work(semaphore, n):
    async with semaphore:
        timeout = aiohttp.ClientTimeout(total=2)
        print('start --------url', n)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            url = 'https://www.shabakeh-mag.com/printpdf/news/world/10390/'
            # url = 'http://01-114.com/'
            try:
                async with session.get(url) as resp:
                    text = await resp.text()
                    return n, len(text)
            except Exception as e:
                print(e)
                return n, 0


def callable(fuction):
    # time.sleep(1)
    print(fuction.result())


def create_task(loop, semaphore):
    tasks = []
    start = now()
    for i in range(511):
        task = asyncio.ensure_future(do_some_work(semaphore, i))
        # task.add_done_callback(callable)
        tasks.append(task)

    # result = loop.run_until_complete(asyncio.wait(tasks))
    result = loop.run_until_complete(asyncio.gather(*tasks))
    print(tasks)
    print(result)
    print(len(result))
    print(now() - start)
    # loop.close()


now = lambda: time.time()


def main():
    semaphore = asyncio.Semaphore(511)  # 限制并发量为5
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    while True:
        create_task(loop, semaphore)


main()
