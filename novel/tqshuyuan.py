#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/2/5
# @Desc  :


import requests
from urllib import parse
from lxml import etree
import re


url = 'http://m.tqshuyuan.com/5_5843/all.html'

response = requests.get(url)
response.encoding = 'utf-8'
text = response.text
root = etree.HTML(text)
chapters = root.xpath('//div[@id="chapterlist"]//a')

f = open('乡村女教师.txt', 'a+', encoding='utf-8')
i = 0
for chapter in chapters:
    # i += 1
    # if i > 30000:
    #     break

    title = chapter.text
    if title.startswith('第') is not True:
        try:
            num = re.match('[0-9]+', title).group(0)
            title = title.replace(num, f'第{num}章 ')
            print(num)
        except Exception as e:
            print(e)

    url = chapter.xpath('./@href')[0]
    url = parse.urljoin('http://m.tqshuyuan.com/', url)
    print(title, url)
    # 获取正文
    _content_response = requests.get(url)
    _content_response.encoding = 'utf-8'
    chapter_text = _content_response.text
    _content_root = etree.HTML(chapter_text)
    try:
        content = _content_root.xpath('//div[@id="chaptercontent"]')[0].xpath('string(.)')
        content = content.replace('最懂你的H漫画平台，魔女和宅男的最爱，点击立即进入不一样的二次元世界！！！', '')
        content = content.replace('    ', '\n')
        content = content.strip()
        print(content)
    except Exception as e:
        content = ''
        print(e)

    f.write('\n\n')
    f.write(title)
    f.write('\n')
    f.write(url)
    f.write('\n')
    f.write(content)

