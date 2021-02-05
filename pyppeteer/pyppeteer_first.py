#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : facebook_extractor.py
# @Author: Cedar
# @Date  : 2020/12/16
# @Desc  :


import asyncio
from pyppeteer import launch


async def main():
    user_data_dir = 'E:/selenium/AutomationProfile1'
    options = {
        'headless': False,  # 关闭无头模式
        # 'devtools': True,  # 打开 chromium 的 devtools
        # 'executablePath': '你下载的Chromium.app/Contents/MacOS/Chromiu',
        'args': [
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
        ],
        'dumpio': True,
        'ignoreDefaultArgs': ["--enable-automation"],   # 隐藏 window.navigator.webdriver
        'userDataDir': 'E:\\selenium\\pyppeteer',
    }

    browser = await launch(options)
    page = await browser.newPage()
    await page.goto('https://www.facebook.com/bnbarry34')
    # await page.goto('https://antispider1.scrape.cuiqingcai.com/')
    await page.screenshot({'path': 'example.png'})
    content = await page.content()
    # await asyncio.sleep(20)
    await browser.close()
    with open('content.html', 'w', encoding='utf-8') as f:
        f.write(content)


asyncio.get_event_loop().run_until_complete(main())
