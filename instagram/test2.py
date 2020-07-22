#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test2.py
# @Author: Cedar
# @Date  : 2020/7/21
# @Desc  :


import platform
import os
import random
import time
import json
import html
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


driver = None
old_height = 0
curpath = os.path.dirname(os.path.realpath(__file__))


def start_selenium(url, user_data_dir=''):
    global driver

    options = Options()

    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    # options.add_argument('--headless')  # 浏览器不提供可视化页面
    # twitter下面这个参数会导致登录退出
    # options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument("allow-file-access-from-files")
    # options.add_argument("use-fake-device-for-media-stream")
    # options.add_argument("use-fake-ui-for-media-stream")
    # options.add_argument("use-file-for-fake-audio-capture=C:\\PATH\\TO\\WAV\\xxx.wav")
    options.add_argument('--audio-output-channels=0')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-sync')
    # options.add_argument("--disable-javascript")    # 禁用JavaScript
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('--no-sandbox')  # 以最高权限运行,解决DevToolsActivePort文件不存在的报错
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏window.navigator.webdriver
    # 取一个chrome user-data-dir目录，每个目录的Chromedriver是互相隔开的，登录不同的账号
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.add_argument(r"user-data-dir=" + user_data_dir)
    print(user_data_dir)

    # 打开chrome人工登录账号
    # chrome --user-data-dir="E:\selenium\AutomationProfile1"
    # google-chrome --user-data-dir="/home/kismanager/KIS/selenium/AutomationProfile1"
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            chromedriver_path = os.path.join("/usr/local/bin", "chromedriver")
            print(chromedriver_path)
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        else:
            chromedriver_path = os.path.join('E:/python_project/test/selenium_test', "chromedriver.exe")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    except Exception as e:
        print(e)

    driver.set_page_load_timeout(60)   # 设置页面加载超时
    driver.set_script_timeout(60)   # 设置页面异步js执行超时
    # driver.maximize_window()

    driver.get(url)


if __name__ == '__main__':
    # url = 'https://www.instagram.com/bill/?__a=1'
    url = 'https://www.instagram.com/bill/'
    user_data_dir = 'E:/selenium/AutomationProfile1'
    start_selenium(url, user_data_dir)
    page_source = driver.page_source
    driver.close()
    print(page_source)
