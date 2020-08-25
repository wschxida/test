#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : access_token.py
# @Author: Cedar
# @Date  : 2020/8/4
# @Desc  :

# encoding:utf-8
import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=gVjITTmcnrE45GdPkvTymC4z&client_secret=vb7g5AtQGQE62LTexcrXf3rRNG0DDQxU'
response = requests.get(host)
if response:
    print(response.json())