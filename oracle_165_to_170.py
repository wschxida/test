#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : oracle_165_to_170.py
# @Author: Cedar
# @Date  : 2020/10/10
# @Desc  :


import cx_Oracle


def query_oracle(config_params, query_sql):
    """
    执行SQL
    :param config_params:
    :param query_sql:
    :return:
    """
    results = None
    try:
        # 连接oracle
        conn = cx_Oracle.connect(config_params)
        c = conn.cursor()
        c.execute(query_sql)
        results = c.fetchall()  # 获取查询的所有记录
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(e)

    return results


config_165 = 'wdm_app/1234@192.168.1.165:1521/orcl'
config_170 = 'wdm_app/1234@192.168.1.170:1521/orcl'
# sql = 'select * from article_detail where extracted_time>sysdate-1/100'
sql = 'select * from hotspot_insight where rownum<100 order by hotspot_insight_id desc'
data = query_oracle(config_165, sql)
print(len(data))
# print(data)

for item in data:
    print(item)
    insert = f'insert into hotspot_insight values{item}'
    print(insert)
    query_oracle(config_170, insert)


