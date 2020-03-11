#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tw_next_page.py
# @Author: Cedar
# @Date  : 2020/3/6
# @Desc  :


import asyncio
import aiohttp
import time
import configparser
import logging
import random
import sys
import datetime
import os
import json
from async_timeout import timeout

log = logging.getLogger(__name__)


async def get_response(_session, _url, _proxy):
    """
    传入session、url、proxy, 发送get请求，返回response的text
    :param _session:
    :param _url:
    :param _proxy:
    :return: response.text()
    """
    with timeout(60):
        async with _session.get(_url, proxy=_proxy) as response:
            return await response.text()


async def request(_url, _proxy, _num_retries=5):
    """
    新建seesion连接，调用协程Response，来获取response.text()
    :param _url:
    :param _proxy:
    :param _num_retries:
    :return:
    """
    async with aiohttp.ClientSession(loop=loop) as session:
        try:
            return await get_response(session, _url, _proxy)
        except aiohttp.client.ServerDisconnectedError as e:
            if _num_retries > 0:
                return await request(_url, _proxy, _num_retries - 1)
        except aiohttp.client.ClientResponseError as e:
            return str(e)
        except asyncio.TimeoutError as e:
            return str(e)
        except aiohttp.client.ClientConnectorError as e:
            return str(e)


async def download_twitter(_url, proxy):
    """
    调用协程request(),获取twitter页返回的text, 解析text,判断是否存在下一页（has_more_items = True）
    若存在，将由min_position来构造下一页的url,调用协程request()来获取其返回的text,直至没有下一页（has_more_items = False）
    最终将返回一个列表response,来存放一页或者多页的内容
    :param _url:
    :param proxy:
    :return:response(list)
    """
    prefix = _url
    _url = prefix
    has_more_items = True
    response = []
    page_num = 1
    while has_more_items is True:
        result = await request(_url, proxy)
        if result is not None:
            try:
                json_data = json.loads(result, strict=False)
                has_more_items = json_data.get("has_more_items")
                min_position = json_data.get("min_position")
                _url = prefix + min_position
            except json.decoder.JSONDecodeError:
                pass
        response.append(result)
    return response


if __name__ == '__main__':
    start = time.time()
    log_filename = "test.log"
    logging.basicConfig(filename=log_filename, filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    # 生成task列表
    tasks = []
    url = "https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=usa%20since%3A2016-04-27%20until%3A2016-04-28&src=typd&include_available_features=1&include_entities=1&reset_error_state=false&max_position="
    # url = "http://www.baidu.com"
    proxy_info = "http://127.0.0.1:4411"
    sem = asyncio.Semaphore(50)
    task = asyncio.ensure_future(save_to_dir(url, proxy_info, sem))
    tasks.append(task)
    # 新建事件循环，用于循环task,直至所有的协程运行完毕，退出循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    print("spend time : %s" % (time.time() - start))

