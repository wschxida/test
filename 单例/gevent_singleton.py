#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/5/25
# @Desc  : 协程中用单例建立实例，能共用参数

import gevent
import gevent.monkey
import requests

# 这里将socket变成异步
gevent.monkey.patch_socket()


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class Cls(object):
    def __init__(self):
        self.conf_num = 0


cls1 = Cls()
cls2 = Cls()
print(id(cls1) == id(cls2))


def hello(i):
    conf = Cls()
    conf.conf_num += 1
    print(conf.conf_num)


tasks = [gevent.spawn(hello, i) for i in range(50)]
gevent.joinall(tasks)

