# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import urllib
from datetime import datetime
from dateutil.relativedelta import *
#from sw_search.search_keyword import search_keyword_list
import re
from sw_search.items import TweetItem
from sw_search.utils.edt import get_absolute_datetime
from w3lib.html import remove_tags
from hashlib import md5
import pymysql

def remove_html_tag(value):
    # 移除标签
    content = remove_tags(value)
    # 移除空格 换行
    return re.sub(r'[\t\r\n\s]', '', content)

def get_md5(content='',coding='UTF-16LE'):
    content = content.encode(coding)
    md5_str = md5(content).hexdigest()  # 加密
    return md5_str

def init_sk(sk_type='all'):
    sk_type = sk_type.strip()
    try:
        query_sql = ""
        with open('sw_search//sk_{}.sql'.format(sk_type),'r',encoding='utf-8') as f:
            query_sql = ''.join(f.readlines())
        try:
            conn = pymysql.connect(host='192.168.1.116', user='root', passwd='poms@db', db='mymonitor')
            cur = conn.cursor()
            cur.execute(query_sql)
            data = cur.fetchall()
            data_list = []
            for item in data:
                data_list.append(item[0])
            cur.close()
            conn.commit()
            conn.close()
            if len(data_list)>0:
                with open('sw_search//sk_{}.txt'.format(sk_type), 'w',encoding='utf-8') as f:
                    f.write('\n'.join(data_list))
            else:
                if sk_type=='latest':
                    pass
                else:
                    raise "no data"
            return data_list
        except Exception as e:
            print(str(e))
            cur.close()
            conn.close()
            # DB 报错或sql无结果时
            with open('sw_search//sk_{}.txt'.format(sk_type), 'r', encoding='utf-8') as f:
                return f.readlines()

    except Exception as e:
        # sql不存在时
        print(str(e))
        with open('sw_search//sk_{}.txt'.format(sk_type),'r',encoding='utf-8') as f:
            return f.readlines()

class SwsearchSpider(scrapy.Spider):
    def __init__(self,my_para=None, *args, **kwargs):
        # 自定义scrapy 参数
        super(SwsearchSpider, self).__init__(*args, **kwargs)
        self.my_para = my_para.strip()
    name = 'swsearch'
    allowed_domains = ['m.weibo.cn']
    start_urls = []

    def start_requests(self):
        self.start_urls = init_sk(self.my_para)
        for search_keyword in self.start_urls:
            search_keyword = search_keyword.strip()
            if search_keyword=='':
                continue

            # 实时
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{}%26t%3D0&page_type=searchall&page=1'.format(
                urllib.parse.quote(search_keyword))
            #url = "https://httpbin.org/get?show_env=1&grs={}".format(search_keyword)
            yield Request(url=url, callback=self.parse_tweet)
            # 热门
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D{}%26t%3D0&page_type=searchall&page=1'.format(
                urllib.parse.quote(search_keyword))
            #url = "https://httpbin.org/get?grs={}".format(search_keyword)
            yield Request(url=url, callback=self.parse_tweet)

    def parse_grs(self, response):
        print("------------------------")
        print(response.url)
        print(response.body_as_unicode())
        print("------------------------")

    def parse_tweet(self, response):
        is_need_next_page = 0
        page_no = 0
        is_need_repost = 1
        max_page_no_search = 200
        max_page_no_repost = 500
        max_page_no_repost_real = max_page_no_repost
        page_url = response.url
        search_keyword = re.findall('&q=(.*)&t=', urllib.parse.unquote(page_url))
        if 'page=' in page_url:
            page_no = int(page_url[page_url.index('page=') + 5:])

        if search_keyword:
            search_keyword = search_keyword[0]
        else:
            search_keyword = ''

        data_len = len(response.text)
        data = json.loads(response.body_as_unicode())
        pubtime_list = []
        is_search_url = page_url.find('containerid')
        is_repost_url = page_url.find("repostTimeline")
        forward_count = 0
        mid = "0"

        if data_len > 100:
            try:
                if is_search_url>=0:
                    status_list = data['data']['cards'][0]['card_group']
                elif is_repost_url>=0:
                    status_list = data['data']['data']
                    max_page_no_repost_real = data['data']['max']
                print("grs-------------------------------")
                print(search_keyword,page_url)
                order_no = 0
                for status in status_list:
                    order_no = order_no + 1
                    try:
                        tweet_item = TweetItem()
                        if is_search_url>=0:
                            tweet = status['mblog']
                        elif is_repost_url>=0:
                            tweet = status
                        author_name = tweet['user']['screen_name']
                        author_status_count = tweet['user']['statuses_count']
                        author_follow_count = tweet['user']['follow_count']
                        author_follower_count = tweet['user']['followers_count']
                        author_id = tweet['user']['id']
                        mid = tweet['mid']
                        article_url = "https://weibo.com/{}/{}".format(author_id, tweet['bid'])
                        article_pubtime_str = tweet['created_at']
                        pubtime_list.append(article_pubtime_str)
                        article_abstract = tweet['text']
                        is_long_text = tweet['isLongText']
                        if is_long_text:
                            article_abstract = tweet['longText']['longTextContent']

                        article_source = tweet['source']
                        forward_count = tweet['reposts_count']
                        reply_count = tweet['comments_count']
                        like_count = tweet['attitudes_count']
                        microblog_type = 'M'
                        repost = ''
                        if 'retweeted_status' in tweet:
                            repost = tweet['retweeted_status']['text']
                            rt_author_name = tweet['retweeted_status']['user']['screen_name']
                            article_abstract = article_abstract+'//@'+rt_author_name+':'+repost
                            microblog_type = 'F'
                        if is_repost_url>=0:
                            microblog_type = 'F'
                        article_image_url = ''
                        if 'bmiddle_pic' in tweet:
                            article_image_url = tweet['bmiddle_pic']
                        elif 'retweeted_status' in tweet and 'bmiddle_pic' in tweet['retweeted_status']:
                            article_image_url = tweet['retweeted_status']['bmiddle_pic']
                        article_content = article_abstract
                        article_abstract = remove_html_tag(article_abstract)

                        print(article_url, article_pubtime_str, article_abstract[0:30])

                        tweet_item['website_no'] = "S15983"
                        tweet_item['media_type_code'] = "M"
                        tweet_item['domain_code'] = "weibo.com"
                        tweet_item['is_with_content'] = "1"
                        tweet_item['node_id'] = "129"
                        tweet_item['language_code'] = "CN"
                        tweet_item['refpage_type'] = "K"
                        tweet_item['refpage_url_id'] = ""
                        tweet_item['extracted_time'] = datetime.utcnow() # ES 默认是统一的UTC时间

                        tweet_item['article_url'] = article_url
                        article_url_md5_id = get_md5(article_url)
                        tweet_item['article_url_md5_id'] = article_url_md5_id
                        tweet_item['record_md5_id'] = article_url_md5_id
                        # tweet_item['_id'] = record_md5_id #mongodb去重用

                        tweet_item['article_pubtime_str'] = article_pubtime_str
                        tweet_item['article_pubtime'] = get_absolute_datetime(article_pubtime_str)
                        article_title = article_abstract[0:30]
                        tweet_item['article_title'] = article_title
                        tweet_item['article_title_fingerprint'] = get_md5(article_title)
                        tweet_item['article_abstract'] = article_abstract
                        tweet_item['article_abstract_fingerprint'] = get_md5(article_abstract)
                        tweet_item['microblog_type'] = microblog_type
                        tweet_item['article_search_keywords'] = search_keyword
                        tweet_item['article_source'] = article_source
                        tweet_item['order_no_in_search_result'] = order_no
                        tweet_item['author_raw_id'] = 'sw_{}'.format(author_id)
                        tweet_item['article_author'] = author_name
                        # 新增字段
                        tweet_item['author_follow_count'] = author_follow_count
                        tweet_item['author_follower_count'] = author_follower_count
                        tweet_item['author_status_count'] = author_status_count
                        tweet_item['page_no'] = page_no
                        tweet_item['mid'] = mid

                        # article_content
                        tweet_item['article_record_md5_id'] = article_url_md5_id
                        tweet_item['is_extract_after_detail'] = 0
                        tweet_item['article_content'] = article_content
                        tweet_item['article_content_fingerprint'] = get_md5(article_abstract)
                        tweet_item['is_html_content'] = 1

                        # article_number
                        tweet_item['reply_count'] = reply_count
                        tweet_item['forward_count'] = forward_count
                        tweet_item['like_count'] = like_count

                        # article_image
                        tweet_item['article_image_no'] = 1
                        tweet_item['article_image_url'] = article_image_url
                        tweet_item['record_md5_id_img'] = get_md5('1'+article_image_url)

                        yield tweet_item

                    except Exception as e:
                        print("grs------error in item------")
                        self.logger.info(e)
                        pass
                print("grs-------------------------------")

            except Exception as e:
                print("grs------error in data [json.loads(response.body_as_unicode())]------")
                self.logger.info(e)
                pass

        else:
            print("grs------no result in request------")
            self.logger.info(response.body)

        if len(pubtime_list) > 0:
            pubtime_list_str = ''.join(pubtime_list)
            days = ['今天', '时前', '分钟前', '分前', '秒钟前', '秒前', '刚刚']
            for day in days:
                if pubtime_list_str.find(day) >= 0:
                    is_need_next_page = 1

        if is_search_url>=0 and page_no < max_page_no_search and is_need_next_page == 1:
            next_page = page_url[:page_url.index('page=') + 5] + str(page_no + 1)
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse_tweet)

        if is_search_url>=0 and forward_count>0 and is_need_repost==1:
            repost_url = "https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1".format(mid)
            next_url = response.urljoin(repost_url)
            yield scrapy.Request(next_url, callback=self.parse_tweet)

        if is_repost_url>=0 and page_no < max_page_no_repost_real and is_need_next_page == 1:
            next_page = page_url[:page_url.index('page=') + 5] + str(page_no + 1)
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse_tweet)
