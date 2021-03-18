#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/3/10
# @Desc  :

from urllib.parse import quote
from fontTools.ttLib import TTFont


def parse_ziti(class_name):
    if class_name == 'shopNum':  # 评论数， 人均消费， 口味环境服务分数
        woff_name = '0ae7d973.woff'
    elif class_name == 'tagName':  # 店铺分类，哪个商圈
        woff_name = 'a1cae07c.woff'
    elif class_name == 'reviewTag':
        woff_name = '464f062c.woff'
    elif class_name == 'address':
        woff_name = '1cfb8d5a.woff'  # 店铺具体地址
    # 评分
    font_data = TTFont(woff_name)
    font_data.saveXML(class_name + '.xml')  # 保存xml便于做分析


# parse_ziti('shopNum')
# parse_ziti('tagName')
# parse_ziti('reviewTag')
# parse_ziti('address')


font = TTFont('1cfb8d5a.woff')
cmap = font.getBestCmap()
print(cmap)

