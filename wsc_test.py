# coding=utf8
import psutil
import time
import json
import os
import pymysql


status = '0'
response_list = ['']

if len(response_list) > 0:
    status = '1'

print(status)