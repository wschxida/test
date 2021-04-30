#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/4/28
# @Desc  :

from selenium.webdriver import Chrome
import time


driver = Chrome('chromedriver.exe')
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
driver.get('http://192.168.1.165:8088/tech/new.html')
time.sleep(10)
