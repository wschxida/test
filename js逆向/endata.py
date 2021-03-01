#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/3/1
# @Desc  :


# 来自 https://blog.csdn.net/qq_49910332/article/details/113858660?utm_medium=distribute.pc_feed_category.none-task-blog-hot-2.nonecase&dist_request_id=d8e1bf11-20cc-482d-bc81-82780b51c659&depth_1-utm_source=distribute.pc_feed_category.none-task-blog-hot-2.nonecase&spm=1000.2115.3001.4128

# utf-8 报错处理
# https://blog.csdn.net/BigBoy_Coder/article/details/104766626

import requests
import execjs
import os


# os.environ["EXECJS_RUNTIME"] = "JScript"
print(execjs.get().name)
# print(execjs.eval("a = new Array(1, 2, 3)"))
# with open('b.js', 'r', encoding='utf-8') as f:
#     jstext = f.read()
#
# ctx = execjs.compile(jstext)
# a = '123456'
# result = ctx.call('a', a)
# print(result)


def get_data(year):
    for i in range(2):
        data = {
            'year': year,
            'MethodName': 'BoxOffice_GetYearInfoData'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'
        }
        url = 'https://www.endata.com.cn/API/GetData.ashx'
        response = requests.post(url, headers=headers, data=data)
        result = response.text
        print(result)

        with open("a.js", "r", encoding='utf-8') as f:
            js = f.read()
        # print(js)

        # 编译js代码
        resp = execjs.compile(js)

        # 调用方法
        parse = resp.call('webInstace.shell', str(result))
        print(parse)
        year = year + 1


def main():
    year = 2018
    get_data(year)


if __name__ == '__main__':
    main()
