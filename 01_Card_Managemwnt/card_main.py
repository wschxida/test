#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
# -*- coding: UTF-8 -*-

import card_tool
__author__ = 'cedar'

while True:

    # 打印表头提示信息
    print('*' * 50)
    print('名片管理系统')
    print('1. 新建名片')
    print('2. 显示全部')
    print('3. 查询名片')
    print('')
    print('0. 退出')
    print('*' * 50)

    # 输入操作
    input_action = input('请输入操作序号:')

    # 选择操作序号
    if input_action in ['1','2','3']:

        if input_action == '1':
            card_tool.add_card()

        elif input_action == '2':
            card_tool.show_all()

        elif input_action == '3':
            card_tool.search_card()

    elif input_action == '0':
        # 退出
        break

    else:
        print('输入错误')