#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/3/22
# @Desc  :

from my_fake_useragent import UserAgent


ua = UserAgent(phone=True)
print(ua.random())
