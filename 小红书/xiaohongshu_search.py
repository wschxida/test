# -*- coding: utf-8 -*-
"""
@Time : 2020/7/01 10:03
@Author : wcx
@File : xiaohongshu.py
@Software: PyCharm 
@desc: 小程序端爬虫
"""
import hashlib
import json
import re
import redis
import datetime
import copy
from urllib.parse import quote

import requests

requests.packages.urllib3.disable_warnings()


# 程序出口redis相关信息
params = dict(host='192.168.1.134', port='6380', password='ks_3000', db=0, decode_responses=True)

pool = redis.ConnectionPool(**params)
Rs = redis.Redis(connection_pool=pool)

# 按照天数计数入库信息
today_date = datetime.datetime.now().strftime('%Y%m:%d')


def get_md5(in_str='', coding='UTF-16LE'):
    in_str = in_str.encode(coding)
    md5_str = hashlib.md5(in_str).hexdigest()  # 加密
    return md5_str


def remove_none_printable_char(in_str):
    out_str = re.sub(r'[\x00-\x20]', '', in_str)
    return out_str


def py_md5(in_str, is_file=False, remove_none_printable_chars=False, case_sensitivity=False):
    if is_file:
        return ''
    if remove_none_printable_chars:
        in_str = remove_none_printable_char(in_str)
    if case_sensitivity:
        in_str = in_str.lower()
    return get_md5(in_str, 'UTF-16LE')


def save_image(image_data, article_url_md5_id):
    """
    保存文章图片
    :param image_data:
    :param article_url_md5_id:
    :return:
    """
    article_image_data={}
    for url in image_data:
        article_image_data["article_record_md5_id"]= article_url_md5_id
        article_image_url =f"http:{url}"
        record_md5_id = py_md5(article_image_url)
        article_image_data["article_image_url"]=article_image_url
        article_image_data["record_md5_id"]= record_md5_id
        article_image_data["table_name"]="article_image"
        article_image_data["article_image_no"]=1
        print(article_image_data)
        Rs.rpush('wechat:items', json.dumps(article_image_data))

def save_data(data, keyword):
    """
    补充字段，rpush到这两个键article_detail_data、article_content_data
    :param data:
    :param url:
    :return:
    """
    article_detail_data = copy.deepcopy(data)
    article_content_data = copy.deepcopy(data)
    image_data = article_detail_data["images"]

    article_detail_data['website_no'] = "S16296"
    article_detail_data['article_pubtime'] = article_detail_data['article_pubtime_str']
    article_url_md5_id = py_md5(article_detail_data['article_url'], False, True, True)
    article_detail_data["article_url_md5_id"] = article_url_md5_id
    article_detail_data["media_type_code"] = "U"
    article_detail_data["domain_code"] = "www.xiaohongshu.com"
    article_detail_data["is_with_content"] = 1
    article_detail_data["is_extract_after_detail"] = 0
    article_detail_data["language_code"] = "CN"
    article_detail_data["refpage_type"] = "K"
    article_detail_data["article_search_keyword"] = keyword

    article_detail_data['record_md5_id'] = article_url_md5_id
    article_content_data['article_record_md5_id'] = article_url_md5_id

    # save_image(image_data, article_url_md5_id)

    article_detail_data['table_name'] = 'article_detail'
    article_content_data['table_name'] = 'article_content'

    del article_content_data['images']
    del article_detail_data['images']

    print(article_detail_data)
    Rs.rpush('zhihu:items', json.dumps(article_detail_data))
    Rs.rpush('zhihu:items', json.dumps(article_content_data))
    Rs.incr('counter:xiaohongshu:%s' % today_date)





class Main:
    def __init__(self):
        pass

    def get_proxies(self):
        pass

    def get_xsign(self, keyword, page):
        data = "/fe_api/burdock/weixin/v2/search/notes?keyword=%s&sortBy=create_time_desc&page=%s&pageSize=20&needGifCover=trueWSUDD" % (
            quote(keyword, 'utf-8'), page)
        m = hashlib.md5(data.encode())
        sign = m.hexdigest()
        return "X" + sign

    def search_note(self, keyword, page):
        headers = {
            # 'device-fingerprint': 'WHJMrwNw1k/HHeHdJP9eciZQM1EIuxb06bdwsL2b8Thw5qsGHcWmXEi2/NlTzrKoNtHPzOLrvAPQmwetCdCyPX5EzFGRDVy4fdCW1tldyDzmauSxIJm5Txg==1487582755342',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MicroMessenger/7.0.12.1620(0x27000C50) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm32',
            # "authorization": "01fb7d4a-37d8-4b4b-97d4-9bb9f977421c",
        }
        x_sign = self.get_xsign(keyword, page)
        headers['X-sign'] = x_sign
        url = "https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?keyword=%s&sortBy=create_time_desc&page=%s&pageSize=20&needGifCover=true" % (
            quote(keyword, 'utf-8'), page)
        response = requests.get(url, headers=headers, verify=False).json()
        return response

    def get_detail(self, item):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        resp = requests.get(item['article_url'], headers=headers).content.decode()
        data = re.findall(r'"NoteView":(.*?)</script>', resp)[0][:-1]
        data = json.loads(data)['noteInfo']
        item['images'] = [i['url'] for i in data['imageList']]
        item['article_pubtime_str'] = data['time']
        content_text = data['desc']
        content_html = f'<div class="article-content">{content_text}</div>'
        for image_url in item['images']:
            image_html=f'<img src="http:{image_url}.jpg" width="312" height="416">'
            content_html+=image_html
        item['article_content'] = content_html

    def save_item(self, item):
        open('{}.json'.format(item['out_name']), 'w').write(json.dumps(item))

    def run(self, keyword, page):
        page = int(page)
        ret_list = []
        end_page = 5 if page > 5 else page
        for i in range(end_page):
            ret_json = self.search_note(keyword, i + 1)
            for note in ret_json['data']['notes']:
                item = {}
                item['article_title'] = note['title']
                item['article_author'] = note['user']['nickname']
                item['article_url'] = 'https://www.xiaohongshu.com/discovery/item/{}'.format(note['id'])
                self.get_detail(item)
                ret_list.append(item)
        return ret_list
        # self.save_item(ret_item)


if __name__ == '__main__':
    app = Main()
    # file_name = sys.argv[0]
    # page = sys.argv[1]
    file_name = "search_keyword.txt"
    page =1
    with open(file_name, 'r', encoding='utf-8') as f:
        keywords = f.readlines()
    for k in keywords:
        ret_item = app.run(k.strip(), page)
        for i in ret_item:
            save_data(i, k)
