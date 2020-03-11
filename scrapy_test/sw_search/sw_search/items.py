# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SwSearchItem(Item):
    # define the fields for your item here like:
    # name = scrapy_test.Field()
    pass

class TweetItem(Item):
    """ 微博信息 """
    #_id = Field()

    # article_detail
    website_no = Field()
    media_type_code = Field()
    domain_code = Field()
    is_with_content = Field()
    node_id = Field()
    language_code = Field()
    refpage_type = Field()
    refpage_url_id = Field()
    extracted_time = Field()

    article_url = Field()
    article_url_md5_id = Field()
    record_md5_id = Field()
    article_pubtime_str = Field()
    article_pubtime = Field()
    article_title = Field()
    article_title_fingerprint = Field()
    article_abstract = Field()
    article_abstract_fingerprint = Field()
    microblog_type = Field()
    article_search_keywords = Field()
    article_source = Field()
    order_no_in_search_result = Field()
    author_raw_id = Field()
    article_author = Field()
    # 额外新增字段
    author_follow_count = Field()
    author_follower_count = Field()
    author_status_count = Field()
    page_no = Field()
    mid = Field()

    # article_content
    article_record_md5_id = Field()
    is_extract_after_detail = Field()
    #article_title
    article_content = Field()
    article_content_fingerprint = Field()
    is_html_content = Field()
    #article_abstract
    #article_pubtime_str
    #article_pubtime
    #language_code
    #node_id
    #extracted_time
    #article_author
    #author_raw_id
    #article_source

    # article_number
    #article_record_md5_id
    #media_type_code
    reply_count = Field()
    forward_count = Field()
    like_count = Field()

    # article_image
    #article_record_md5_id
    article_image_no = Field()
    article_image_url = Field()
    record_md5_id_img = Field()
    # extracted_time = Field()



