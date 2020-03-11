# -*- coding: utf-8 -*-


# class YidianzixunSpider(scrapy_test.Spider):
#     name = 'yidianzixun'
#     allowed_domains = ['yidianzixun.com']
#     start_urls = ['http://yidianzixun.com/']
#
#     def parse(self, response):
#         pass



import scrapy
import re
from Yidianmsg.items import YidianmsgItem

# P脚本分割字符串
def P(text, pattern, partNo=0):
    text_p = text
    pattern_list = pattern.split('*')
    # print(pattern_list)

    # 先把关键字替换成/
    for str in pattern_list:
        if str:
            if str in text:
                text_p = text_p.replace(str,'/')

    text_list = text_p.split('/')
    pattern_count = pattern.count('*')
    # print(text_p)
    # print(text_list)

    # partNo是整数时以及pattern需要有*才进行截取
    if isinstance(partNo,int) and pattern.find('*')>=0:
        if partNo == 0:
            result = text
        # pattern是否以*开头
        elif partNo > 0 and partNo <= pattern_count and len(text_list)>1 and pattern.startswith('*'):
            result = text_list[partNo - 1]
        elif partNo > 0 and partNo <= pattern_count and len(text_list)>1 and not pattern.startswith('*'):
            result = text_list[partNo]
        else:
            result = ''
    else:
        result = ''
    return result

class YidianSpider(scrapy.Spider):
    name = 'yidian'
    allowed_domains = ['yidianzixun.com']
    start_urls = ['http://yidianzixun.com/']

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "Referer": "http://www.yidianzixun.com/",
    }

    def parse(self, response):
        url = "http://www.yidianzixun.com/channel/m134914"
        yield scrapy.Request(url=url, callback=self.parse_page_links, headers=self.headers)

    def parse_page_links(self, response):
        # response_html = response.body.decode('utf-8')
        # article_links = re.findall(r'href="(.*?)"', response_html)
        # for article_link in article_links:
        #     if 'article' in article_link:
        #         article_url = "http://www.yidianzixun.com" + str(article_link)
        #     else:
        #         continue

        source = response.xpath('//a[@class="piece"]')

        for each_news in source:
            item = YidianmsgItem()

            title = each_news.xpath('//div[@class="doc-title"]/text()').extract()[0].strip()
            link = each_news.xpath('@href').extract()[0].strip()
            # title = title.decode('utf-8')
            P_link = P(link, '*?s=', 1)
            print(P_link)
            link = "http://www.yidianzixun.com" + str(link)

            item['name'] = title
            item['original_url'] = link
            print('-' * 50)
            print(item['name'])
            print('-' * 50)
            yield item

