#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/3/3
# @Desc  :

import asyncio
import aiohttp


# async def wait(i):
#     print(i, 1)
#     await asyncio.sleep(3)
#     print(i, 2)
#
#
# async def main():
#     tasks = []
#     for i in range(5):
#         task = asyncio.create_task(wait(i))
#         tasks.append(task)
#     await asyncio.gather(*tasks)
#
# if __name__ == '__main__':
#     asyncio.run(main())

#
# import threading
# import asyncio
# import aiohttp
#
#
# async def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#
#     await asyncio.sleep(1)
#     print('Hello again! (%s)' % threading.currentThread())
#
# async def run():
#     tasks = []
#     for i in range(5):
#         task = asyncio.create_task(hello())
#         tasks.append(task)
#     await asyncio.wait(tasks)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())
# loop.close()

import requests
headers = {
    "Host": "deo.shopeemobile.com",
    "Accept": "*/*",
    "Accept-Language": "zh-cn",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "ShopeeMY/2.67.12 CFNetwork/1220.1 Darwin/20.3.0",
}
url = 'http://deo.shopeemobile.com/shopee/shopee-sticker-live-my/manifest.json'


response = requests.get(url, headers=headers)
text = response.text
print(text)



