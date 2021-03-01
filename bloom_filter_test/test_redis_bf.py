#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/2/26
# @Desc  :


import redis


REDIS_CONFIG = {'host': '192.168.2.56', 'port': 6379, 'password': '', 'db': 0}
pool = redis.ConnectionPool(**REDIS_CONFIG)
client = redis.Redis(connection_pool=pool)


client.delete("tiancheng")
size = 100000
count = 0
for i in range(size):
    client.execute_command("bf.add", "tiancheng", "tc%d" % i)
    result = client.execute_command("bf.exists", "tiancheng", "tc%d" % (i + 1))
    if result == 1:
        # print(i)
        count += 1

print("size: {} , error rate: {}%".format(
    size, round(count / size * 100, 5)))

