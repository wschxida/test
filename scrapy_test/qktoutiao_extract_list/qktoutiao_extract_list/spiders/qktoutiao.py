# -*- coding: utf-8 -*-
import scrapy
import json
import time
import datetime
from scrapy.http import Request
from hashlib import md5
from qktoutiao_extract_list.items import QktoutiaoExtractListItem

def get_md5(content='',coding='UTF-16LE'):
    content = content.encode(coding)
    md5_str = md5(content).hexdigest()  # 加密
    return md5_str

class QktoutiaoSpider(scrapy.Spider):
    name = 'qktoutiao'
    allowed_domains = ['qktoutiao.com']
    start_urls = ['http://api.1sapp.com/wemedia/content/articleList?token=&dtu=200&version=0&os=android&id=154068&page=1']

    def start_requests(self):
            # 构造url
        for i in range(154067,154069):
            start_url = 'http://api.1sapp.com/wemedia/content/articleList?token=&dtu=200&version=0&os=android&id=' + str(i)
            # 翻5页
            for j in range(1,10):
                start_url = start_url + '&page=' + str(j)
                yield Request(url=start_url, callback=self.parse, meta={'start_url':start_url})



    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        data_list = sites['data']['list']
        source_url_id = response.meta['start_url'].split('&id=')[-1].split('&')[0]
        for list in data_list:
            item = QktoutiaoExtractListItem()
            item['source_url_id'] = source_url_id
            item['title'] = list['title']
            item['title'] = list['title']
            item['source'] = list['source']
            item['source_name'] = list['source_name']
            item['read_count'] = list['read_count']
            item['share_count'] = list['share_count']
            item['comment_count'] = list['comment_count']
            item['like_num'] = list['like_num']
            # url截取?前面部分
            item['url'] = list['url'].split('?')[0]
            item['introduction'] = list['introduction']
            _timeStamp = int(list['publish_time'][0:10])
            _timeArray = time.localtime(_timeStamp)
            item['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S", _timeArray)
            item['article_url_md5_id'] = get_md5(item['url'])
            item['extracted_time'] = datetime.datetime.now()
            yield item


