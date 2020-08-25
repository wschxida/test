#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : screenshot.py
# @Author: Cedar
# @Date  : 2020/7/31
# @Desc  :


import asyncio
from pyppeteer import launch


async def main(screen_file):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://www.runoob.com/redis/redis-data-types.html')

    title = await page.title()
    print(title)
    await page.screenshot({'path': screen_file})
    await browser.close()

asyncio.run(main('redis-data-types.png'))
