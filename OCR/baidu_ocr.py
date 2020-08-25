#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : baidu_ocr.py
# @Author: Cedar
# @Date  : 2020/8/4
# @Desc  :

# encoding:utf-8

import requests
import base64
import sys

'''
通用文字识别
'''


def run(img_file, output_file):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(img_file, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = '24.ea445854f8aab77619410527263027c2.2592000.1599132089.282335-21215655'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
    with open(output_file, 'w', encoding="utf-8") as w:
        if response:
            for i in response.json()['words_result']:
                w.write(i['words'])
                w.write('\n')


if __name__ == '__main__':
    img_filename = sys.argv[1]
    result_filename = sys.argv[2]
    run(img_filename, result_filename)
