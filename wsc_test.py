
import time
import json
from lxml import etree
from datetime import datetime
from elasticsearch import Elasticsearch
import tldextract
import requests
import sqlite3
import re
import os
import random
import pymysql
import warnings

# 忽略mysql插入时主键重复的警告
warnings.filterwarnings('ignore')

url = 'https://www.bannedbook.org/'
proxy = {
    'http': 'http://127.0.0.1:7777',
    'https': 'http://127.0.0.1:7777',
}
headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                    # 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/sig"ned-exchange;v=b3;q=0.9',
                    # 'accept-encoding': 'gzip, deflate, br',
                    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                }

# response = requests.get(url, proxies=proxy, headers=headers)
# response.encoding = 'utf-8'
# text = response.text
# print(text)

aa = int('' or 0)
print(aa)
