#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : multi_tasks.py
# @Author: Cedar
# @Date  : 2020/8/25
# @Desc  :


import asyncio
from pyppeteer import launch
import time


tasks = []


async def create_page():
    browser = await launch(headless=True, dumpio=True)
    return browser


async def close_page(browser):
    await browser.close()


async def get_response(screen_file, url, semaphore):
    async with semaphore:
        # browser = await launch(options)
        page = await browser.newPage()
        await page.goto(url)
        title = await page.title()
        print(title)
        await page.screenshot({'path': screen_file})
        # await page.waitFor(2000)
        # await page_close(browser)
        return await page.content()


async def run():
    semaphore = asyncio.Semaphore(5)  # 限制并发量为500
    url_list = [
        'https://www.runoob.com/redis/redis-tutorial.html',
        'https://www.runoob.com/redis/redis-intro.html',
        'https://www.runoob.com/redis/redis-install.html',
        'https://www.runoob.com/redis/redis-conf.html',
        'https://www.runoob.com/redis/redis-data-types.html',
        'https://www.pythonf.cn/read/101780',
        'https://www.pythonf.cn/read/139371',
        'https://www.pythonf.cn/read/139370',
        'https://www.pythonf.cn/read/139369',
        'https://www.pythonf.cn/read/139368',
    ]

    i = 0
    for url in url_list:
        file = '.\\screenshot\\' + str(i) + '.png'
        i += 1
        task = asyncio.ensure_future(get_response(file, url, semaphore))
        tasks.append(task)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    browser = loop.run_until_complete(create_page())  # 创建一个浏览器对象
    loop.run_until_complete(run())
    result = loop.run_until_complete(asyncio.gather(*tasks))
    loop.run_until_complete(close_page(browser))

    for result_response in result:
        print(result_response)
    end_time = time.time()
    print(start_time)
    print(end_time)
