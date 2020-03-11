# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from sw_search.items import TweetItem


class SwSearchPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("192.168.1.229", 27017)
        db = clinet["sw"]
        self.tweet = db["tweet"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, TweetItem):
            try:
                self.tweet.insert(dict(item))
            except Exception:
                pass

        return item