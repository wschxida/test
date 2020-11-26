# coding=utf8


import time, json, sys
import os
import re

with open('title.txt', 'r', encoding='utf-8') as f:
    titles = f.readlines()

for i in titles:
    title = i.replace('\n', '')
    sql = f"delete from column_link where Website_No='GUOWAI' and title='{title}';"
    print(sql)


url = 'http://www.01-114.com/go.php?http://www.cctv.com/'

url = url.replace('/go.php?', '')
url = url.replace('http://www.01-114.com', '')
print(url)

