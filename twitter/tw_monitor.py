from locale import getdefaultlocale
from lxml import etree
import requests
import time
import sys
import os
import random
from urllib.parse import quote
import datetime
import json


def get_code_page():
    """
    Compatible with Linux and Windows
    :return:
    Linux:  ('en_US', 'UTF-8')
    Windows: ('zh_CN', 'cp936')
    """
    code_page = getdefaultlocale()[1]
    return code_page


def get_lines_from_file(file_path, remove_space_line=True):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as fp:
        content = fp.read().strip()
    try:
        content = content.decode('utf8')
    except Exception as e:
        content = content.decode(get_code_page())
    lines = content.splitlines()
    if remove_space_line:
        # 移除文件中的空行
        lines = [i for i in lines if i != '']
    return lines


def get_one_proxy(file_path='config/proxy_list.txt'):
    """
    随机取一个代理ip
    :param file_path:
    :return:一个代理ip
    """
    lines = get_lines_from_file(file_path)
    if lines is not None:
        if len(lines) > 0:
            proxy_ip = random.sample(lines, 1)
            return proxy_ip[0].strip()


def date_format(time_str):
    """
    mobile接口的列表数据没有时间戳，只有时间字符串。改函数作用为修改时间字符串为标准时间格式
    :param time_str: 列表上的时间字符串，格式为2s,5        time_str = int(time_str.replace("s", ''))
m,6h,March 24....
    :return:
    """
    current_time = datetime.datetime.now()
    if time_str.endswith("s"):
        time_str = int(time_str.replace("s", ''))
        time_difference = datetime.timedelta(seconds=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    elif time_str.endswith("m"):
        time_str = int(time_str.replace("m", ''))
        time_difference = datetime.timedelta(minutes=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    elif time_str.endswith("h"):
        time_str = int(time_str.replace("h", ''))
        time_difference = datetime.timedelta(hours=time_str)
        publish_time_str = current_time - time_difference
        format_time = publish_time_str.strftime('%Y-%m-%d %H:%M:%S')
    else:
        time_list = time_str.split(' ')
        if len(time_list) == 3:
            year = "20" + time_list[-1]
            month = time_list[1]
            date = time_list[0]
            time_str = f"{year}-{month}-{date}"
            format_time = time_str
        else:
            format_time = datetime.datetime.strptime('2020 ' + time_str, '%Y %b %d')
            time_difference = str(current_time-format_time)
            if '-' in time_difference:
                format_time = datetime.datetime.strptime('2019 ' + time_str, '%Y %b %d')
            format_time = str(format_time)
    return format_time


def get_html(url):
    for i in range(3):
        proxies = None
        proxy_ip = get_one_proxy()  
        if not proxy_ip is None:
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
        try:
            response = requests.get(url, proxies=proxies, timeout=40).text
            return response
            break
        except Exception as e:
            print(str(e))
            continue


def get_html_via_cloud(url):
    url = url.split('com/')[-1]
    req_data = quote(url)
    req_url = f'http://107.180.91.218:5100/service_app?agent_type=twitter&fetch_type=get_tweet_of_url&query_dict=%7B%22url%22%3A%22{req_data}"%7D%0D%0A'
    for i in range(3):
        proxies = None
        proxy_ip = get_one_proxy()  
        if not proxy_ip is None:
            proxies = {'http': f'http://{proxy_ip}', 'https': f'http://{proxy_ip}'}
        try:
            response = requests.get(req_url, proxies=proxies, timeout=45).text
            res_json = json.loads(response)["data"]
            return res_json
            break
        except Exception as e:
            print(str(e))
            continue


def save_to_file(*param):
    utc_time = int(time.time())
    website_no = param[0]
    output_dir = param[1]
    output_file = f"./output/{website_no}_{utc_time}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_dir)


def parse_html(response):
    """
    解析获取到的message_html源码，提取必须字段，索引至ES
    :return:
    """
    res_byte = bytes(response, encoding="utf-8")
    data_list = []
    xpath_items = '//table[contains(@class,"tweet")]'
    # current_html = '//'
    article_url = '//td[@class="timestamp"]/a[1]/@href'
    author_name = '//strong[@class="fullname"]/text()'
    publish_time = '//td[@class="timestamp"]/a[1]/text()'
    content_html = '//td[@class="tweet-content"]'
    is_image = './/a[contains(@data-url,"photo")]/@data-url'
    is_video = './/a[contains(@data-url,"video")]/@data-url'
    html = etree.HTML(res_byte)
    items = html.xpath(xpath_items)
    for i, article in enumerate(items):
        data = {}
        current_html = article.xpath(xpath_items)[i]
        current_html = etree.tostring(current_html, encoding='utf-8').decode('utf-8')
        data['current_html'] = current_html
        data['is_image'] = article.xpath(is_image)
        data['is_video'] = article.xpath(is_video)
        data['article_url'] = f"https://twitter.com{article.xpath(article_url)[i].split('?')[0]}"
        data['author_name'] = article.xpath(author_name)[i]
        data['article_pubtime_str'] = article.xpath(publish_time)[i]
        data['article_content'] = str(etree.tostring(article.xpath(content_html)[i], encoding='utf-8'),
                                      encoding="utf-8")
        publish_time_str = article.xpath(publish_time)[i]
        data['publish_time_str'] = publish_time_str
        data['article_pubtime'] = date_format(publish_time_str)
        data_list.append(data)
    # next_cursor = html.xpath("//div[@class='w-button-more']/a[1]/@href")
    error_page = html.xpath("//div[@class='system']//text()")
    return [data_list, error_page]


def tweet_detail(url):
    try:
        detail_html = get_html(url)
        det_byte = bytes(detail_html, encoding="utf8")
        html = etree.HTML(det_byte)
        img_url = html.xpath('//div[@class="media"]/img[1]/@src')[0].replace(':small', '')
        error_page = html.xpath("//div[@class='system']//text()")
        if len(error_page) > 0:
            detail_html = get_html_via_cloud(url)
            det_byte = bytes(detail_html, encoding="utf8")
            html = etree.HTML(det_byte)
            img_url = html.xpath('//div[@class="media"]/img[1]/@src')[0].replace(':small', '')
        return img_url
    except Exception as e:
        print(str(e))
        pass


def get_id(author_account):
    file_path = f"./id/{author_account}.txt"
    if os.path.exists(file_path):
        with open(file_path) as fp:
            author_id = fp.read().strip()
    else:
        url = f"http://107.180.91.218:5100/service_app?agent_type=twitter&fetch_type=get_profile&target_express={author_account}"
        response = get_html(url)
        html = json.loads(response)
        author_id = html["target_profile"][0]["author_id"]
        with open(file_path, 'w') as f:
            f.write(author_id)
    return author_id


def main():
    start_time = time.time()
    time_out = 10
    input_dir ="./Input/TWA_WEB_A.txt"
    argv = sys.argv
    output_dict = {}
    author_id = ""

    if len(argv) > 1:
        try:
            input_dir = argv[1]
        except:
            pass
        try:
            time_out = int(argv[2])
        except:
            pass
   
    # input_dir = "./Input/TWA_WEB_A.txt"
    with open(input_dir, 'r', encoding='utf-8') as f:
        input_list = f.readlines()
        for x in input_list:
            try:
                if len(x) > 1:
                    website_no = x.split('=')[0]
                    request_account = x.split('=')[1].strip()
                    url = f"https://mobile.twitter.com/{request_account}"
                    response = get_html(url)
                    page_content = parse_html(response)
                    data_list = page_content[0]
                    error_page = page_content[1]
                    if len(error_page) > 0:
                        response = get_html_via_cloud(url)
                        page_content = parse_html(response)
                        data_list = page_content[0]
                    author_id = get_id(request_account)
                    article_list = []
                    for x in data_list:
                        author_account = x["article_url"].split('/')[-3]
                        message_raw_id = x["article_url"].split('/')[-1]
                        x["author_account"] = author_account
                        # 转推的author_id需要额外获取
                        if author_account != request_account:
                            x["is_retweeted"] = 1
                            author_id = get_id(author_account)
                        x["author_id"] = author_id
                        if len(x["is_image"]) > 0:
                            detail_url = x["article_url"].replace('twitter', 'mobile.twitter')
                            img_url = tweet_detail(detail_url)
                            x["img_url"] = img_url
                        if len(x["is_video"]) > 0:
                            vedio_url = f"https://twitter.com/i/videos/tweet/{message_raw_id}"
                            x["vedio_url"] = vedio_url
                        del x["is_image"]
                        del x["is_video"]
                        article_list.append(x)
                    output_dict["data"] = article_list
                    output_dir = json.dumps(output_dict)
                    save_to_file(website_no, output_dir)
            except Exception as e:
                print(str(e))
    print("spend time : %s" % (time.time() - start_time))


if __name__ == '__main__':
    main()