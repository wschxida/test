#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/09 14:05
# @Author  : Billy
# @Email   : gongrusheng@qq.com
# @File    : redisbloom_filter.py
# @Software: PyCharm

import time
from functools import wraps
import redis
from redisbloom.client import Client
from loguru import logger
import re


class UDF():
    # 公共自定义静态方法
    @staticmethod
    def stat_time(fn):
        @wraps(fn)
        def wrap(*args, **kw):
            start_time = time.time()
            ret = fn(*args, **kw)
            ended_time = time.time()
            print("call {}() cost: {} seconds".format(fn.__name__, ended_time - start_time))
            return ret

        return wrap


class RedisBloomFilter():
    REDIS_CONFIG = {'host': '192.168.1.134', 'port': 6383, 'password': 'ks_3000', 'db': 0}
    WORKING_KEY = 'bf:working'
    SWAP_KEY = 'bf:swap'
    RATE = 0.0001
    CAPACITY = 10000 * 10000 * 10
    CAPACITY = 2000

    def __init__(self):
        self.get_redis_conn()
        self.init_redisbloom_filter(self.WORKING_KEY, self.RATE, self.CAPACITY)
        self.init_redisbloom_filter(self.SWAP_KEY, self.RATE, self.CAPACITY)

    def init_redisbloom_filter(self, key_name, rate, capacity):
        if key_name:
            is_exist = self.redis.exists(key_name)
        if is_exist == 1:
            logger.warning(f"{key_name} is exist.")
        else:
            cmd = f"BF.RESERVE {key_name} {rate} {capacity}"
            self.redis.execute_command(cmd)
        logger.success(f"init redisbloom: {key_name}")
        return True

    def get_redis_conn(self):
        pool = redis.ConnectionPool(**self.REDIS_CONFIG)
        self.redis = redis.Redis(connection_pool=pool)
        logger.success(f"connected to redis:{self.REDIS_CONFIG.get('host')}:{self.REDIS_CONFIG.get('port')}")
        return True

    def get_redisbloom_conn(self):
        rb = Client()
        self.redisbloom = rb
        logger.success(f"connected to redisbloom:{self.REDIS_CONFIG.get('host')}:{self.REDIS_CONFIG.get('port')}")
        return True

    def recreate_redisbloom_filter(self, key_name, rate, capacity):
        if not key_name:
            logger.error(f"key name is null")
            return False

        cmd = f"BF.RESERVE {key_name} {rate} {capacity}"
        with self.redis.pipeline() as p:
            is_exist = self.redis.exists(key_name)
            logger.info(f"`{key_name}` is exist: {is_exist}")
            if is_exist == 1:
                p.delete(key_name)
                p.execute_command(cmd)
                logger.success(f"delete and create bloom filter: {key_name} ")
            else:
                self.redis.execute_command(cmd)
                logger.success(f"create bloom filter: {key_name}")
            p.execute()
        return True

    def get_bloom_used_rate(self, key_name):
        self.redis.ping()
        try:
            rsp = self.redis.execute_command(f'BF.debug {key_name}')
            logger.debug(f"`{key_name}`: {rsp}")
            rsp = rsp[1].decode('utf8')
            capacity_and_size = re.findall('capacity:(\d{1,}).*size:(\d{1,})', rsp, re.I)
            if capacity_and_size:
                used_rate = int(capacity_and_size[0][1]) / int(capacity_and_size[0][0])
                logger.info(f"`{key_name}` used rate: {used_rate}")
                return used_rate
        except Exception as e:
            logger.error(e)
            return 0

    def swap_bloom_filter(self):
        used_rate_swap = self.get_bloom_used_rate(self.SWAP_KEY)
        used_rate = self.get_bloom_used_rate(self.WORKING_KEY)
        if used_rate > 0.8:
            with self.redis.pipeline() as p:
                p.delete(self.WORKING_KEY)
                p.rename(self.SWAP_KEY, self.WORKING_KEY)
                cmd = f"BF.RESERVE {self.SWAP_KEY} {self.RATE} {self.CAPACITY}"
                # self.recreate_redisbloom_filter(self.SWAP_KEY, self.RATE, self.CAPACITY)
                p.execute_command(cmd)
                p.execute()
            logger.success(f"swap redis bloom filter.")
            return True
        elif used_rate > 0.4 and used_rate_swap>0.4:
            self.recreate_redisbloom_filter(self.SWAP_KEY, self.RATE, self.CAPACITY)
            logger.success(f"recreate redis bloom filter: {self.SWAP_KEY}")
            return False

    def start(self):
        while True:
            self.swap_bloom_filter()
            time.sleep(2)


@UDF.stat_time
def main():
    rbf = RedisBloomFilter()
    rbf.start()


if __name__ == '__main__':
    main()
