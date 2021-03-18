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


def get_data(year):

    with open("acrawler_amd.js", "r", encoding='utf-8') as f:
        js = f.read()
    # print(js)

    # 编译js代码
    resp = execjs.compile(js)

    # e.sign({url: encodeURI(
    #     )});


    # url = "https://m.toutiao.com/search?keyword=%E6%81%92%E5%A4%A7%E6%9E%97%E6%BA%AA%E9%83%A1&pd=weitoutiao&source=search_subtab_switch&original_source=&in_ogs=&from=weitoutiao"
    #
    # # 调用方法
    # parse = resp.call('glb.sign', {url: url})


def main():
    year = 2018
    get_data(year)


if __name__ == '__main__':
    main()
