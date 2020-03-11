# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QktoutiaoExtractListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy_test.Field()
    source_url_id = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    source_name = scrapy.Field()
    read_count = scrapy.Field()
    share_count = scrapy.Field()
    comment_count = scrapy.Field()
    like_num = scrapy.Field()
    url = scrapy.Field()
    introduction = scrapy.Field()
    publish_time = scrapy.Field()
    article_url_md5_id = scrapy.Field()
    extracted_time = scrapy.Field()
