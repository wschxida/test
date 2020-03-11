# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem

class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://www.sohu.com/c/8/1461']

    def parse(self, response):
        source = response.xpath('//div[@id="main-news"]/div/h4')

        for each_news in source:
            item = NewsItem()
            item['name'] = each_news.xpath('a/text()').extract()[0].strip()
            print(each_news)
            print('-' * 50)
            print(item['name'])
            print('-' * 50)
            yield item
        # print('=' * 50)
        # print(len(source))
        # print('=' * 50)
        # item = NewsItem()
        # item['name'] = ''.join(source.xpath('a/text()').extract()).strip()
        # print('-' * 50)
        # print(item['name'])
        # print('-' * 50)
        # yield item


