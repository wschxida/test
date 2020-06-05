#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aa.py
# @Author: Cedar
# @Date  : 2020/5/22
# @Desc  :


import re  # 正则表达式库
import pymysql
import hashlib


def query_mysql(config_params, query_sql):
    """
    执行SQL
    :param config_params:
    :param query_sql:
    :return:
    """
    # 连接mysql
    config = {
        'host': config_params["host"],
        'port': config_params["port"],
        'user': config_params["user"],
        'passwd': config_params["passwd"],
        'db': config_params["db"],
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    results = None
    try:
        conn = pymysql.connect(**config)
        conn.autocommit(1)
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()
        cur.execute(query_sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        conn.close()  # 关闭连接
    except Exception as e:
        pass

    return results


def get_listpage_title_word_count():
    # 连接mysql
    config = {
        'host': '192.168.1.150',
        'port': 3306,
        'user': 'root',
        'passwd': 'poms@db',
        'db': 'mymonitor',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    fn = open('word.txt', 'r', encoding='UTF-8')  # 打开文件
    for i in fn:
        print()i
    fn.close()  # 关闭文件




if __name__ == '__main__':
    get_listpage_title_word_count()
