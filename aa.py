# coding=utf8


import time, json, sys
import os


class A(object):
    bar = 1

    def foo(self):
        print('foo')

    @staticmethod
    def static_foo():
        print('static_foo')
        print(A.bar)
        print(A.foo())

    @classmethod
    def class_foo(cls):
        print('class_foo')
        print(cls.bar)
        cls().foo()


A.static_foo()
# A.class_foo()
