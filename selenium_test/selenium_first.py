#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : facebook_extractor.py
# @Author: Cedar
# @Date  : 2020/12/16
# @Desc  :

import traceback
import platform
import os
import random
import time
import json
import html
import re
from urllib.parse import quote, unquote, urlencode
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import sys
import io


def start_selenium(user_data_dir):
    global driver

    options = Options()

    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-infobars")
    # twitter下面这个参数会导致登录退出
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('--no-sandbox')  # 以最高权限运行,解决DevToolsActivePort文件不存在的报错

    # 隐藏 window.navigator.webdriver
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)


    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            options.add_argument('--headless')  # 浏览器不提供可视化页面
            chromedriver_path = os.path.join("/usr/local/bin", "chromedriver")
        else:
            # options.add_argument('--headless')  # 浏览器不提供可视化页面
            # user_data_dir = 'E:\\selenium\\AutomationProfile1'
            chromedriver_path = os.path.join("C:/Program Files (x86)/Google/Chrome/Application", "chromedriver.exe")

        # 取一个chrome user-data-dir目录，每个目录的Chromedriver是互相隔开的，登录不同的账号
        options.add_argument(r"user-data-dir=" + user_data_dir)
        # print(user_data_dir)
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    except Exception as e:
        print(e)

    # 隐藏window.navigator.webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })

    driver.implicitly_wait(10)  # 隐性等待，最长等30秒
    # 下面的设置会导致超时就抛出异常，浏览器退出
    driver.set_page_load_timeout(60)  # 设置页面加载超时
    driver.set_script_timeout(60)  # 设置页面异步js执行超时
    # driver.maximize_window()


user_data_dir = 'E:\\selenium\\AutomationProfile5'
start_selenium(user_data_dir)
driver.get("https://www.facebook.com/")
driver.get('https://antispider1.scrape.cuiqingcai.com/')
time.sleep(30)
driver.close()
