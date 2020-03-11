# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YidianmsgItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    channel = scrapy.Field()
    title = scrapy.Field()
    item_type = scrapy.Field()
    create_type = scrapy.Field()
    original_url = scrapy.Field()
    body = scrapy.Field()
    images = scrapy.Field()


