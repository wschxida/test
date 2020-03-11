# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class YidianmsgPipeline(object):
#     def process_item(self, item, spider):
#         return item


import json


class YidianmsgPipeline(object):
    def open_spider(self, spider):
        self.filename = open('data.json', 'w')

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + "\n"
        self.filename.write(content.encode('utf-8').decode('unicode-escape'))
        return item

    def close_spider(self, spider):
        self.filename.close()