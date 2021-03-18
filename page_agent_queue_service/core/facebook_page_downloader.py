# coding=utf8
import aiohttp
import time, traceback
import aiofiles
from aiohttp import ClientSession, client_exceptions
from hashlib import md5
import asyncio
import os
from configparser import ConfigParser
from fake_useragent import UserAgent
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
import io, sys
import redis
from lxml import etree
from lxml.html import fromstring, tostring
from html.parser import unescape
import hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
dirname = os.path.abspath(os.path.dirname(__file__))

ua = UserAgent()

redis_connect_params = dict(
    host='192.168.1.134',
    port='6380',
    db='0',
    password='ks_3000',
    decode_responses=True  # 返回解码结果
)
pool = redis.ConnectionPool(**redis_connect_params)
redis_help = redis.Redis(connection_pool=pool)
url_list_key = 'page_agent_queue_service:facebook:urls'
html_dict_key = 'page_agent_queue_service:facebook:items'
sleep_max_second_count = 2


def get_token(md5str):
    # md5str = "abc"
    # 生成一个md5对象
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-16LE"))
    token = m1.hexdigest()
    return token


def now():
    return time.time()


def parse_html(html):
    data = html
    result_html = etree.HTML(data)
    items = result_html.xpath('//div[contains(@class,"userContentWrapper")]')
    result = ''
    for item in items:
        data = tostring(item, method='html')
        result = result + unescape(data.decode())
    return result


async def save_html_to_local_file(url, html):
    # 使用异步保存
    html = parse_html(html)
    file_name = os.path.join(dirname, f'../output/{get_token(url)}.html')
    async with aiofiles.open(file_name, "w", encoding="utf-8") as fp:
        await fp.write(html)


async def fetch(url_list, proxy, proxy_user, proxy_password, loop):
    # 请求及解析
    requests_task_list = []
    # 构造代理
    if proxy_user and proxy_password:
        proxy_auth = aiohttp.BasicAuth(proxy_user, proxy_password)
    else:
        proxy_auth = None
    # 创建连接对象，多个连接由同一个对象发出请求，减少创建对象资源
    if proxy and 'socks5' in proxy:
        # socks5代理需要额外处理
        connector, request_class = ProxyConnector(enable_cleanup_closed=True), ProxyClientRequest
        client = ClientSession(connector=connector, request_class=request_class)
    else:
        connector = aiohttp.TCPConnector(enable_cleanup_closed=True)
        client = ClientSession(connector=connector)
    async with client:
        # 请求
        for url in url_list:
            task = loop.create_task(requests_page(client, url, proxy, proxy_auth))

            requests_task_list.append(task)
        await asyncio.wait(requests_task_list)

    # 解析任务并保存
    save_file_task_list = []
    requests_failed_url_list = []
    for i, task_future in enumerate(requests_task_list):
        html, url = task_future.result()
        if html:
            # save_file_task = loop.create_task(save_html_to_local_file(url, html))
            url_md5 = get_token(url)
            html = parse_html(html)
            redis_help.hset(html_dict_key, url_md5, html)
            print(f'requests {url} successful')
        else:
            requests_failed_url_list.append(url)
            print(f'requests {url} error')

    # if save_file_task_list:
    # await asyncio.wait(save_file_task_list)
    # return save_file_task_list


async def requests_page(client, url, proxy, proxy_auth):
    # 请求
    proxy = proxy
    # headers = {
    #     "User-Agent": ua.ie,  # 此处有可能部分ie的ua头无法起作用，待验证
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #     "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    #     "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"
    # }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }

    global timeout
    try:
        async with client.get(url, headers=headers, proxy=proxy, proxy_auth=proxy_auth, timeout=timeout) as resp:
            assert resp.status == 200
            return await resp.text(), url
    except client_exceptions.ServerTimeoutError as timeout_error:
        print(f'requests {url} timeout')
        return None, url
    except Exception as e:
        print(f'requests {url} error,{str(e)}')
        return None, url


def get_config():
    # 获取配置
    file_name = os.path.join(dirname, '../config/config.ini')
    cfg = ConfigParser()
    cfg.read(file_name)
    coroutine_max_workers_count = int(cfg.get('crawler', 'coroutine_max_workers_count'))
    requests_retry_max_count = int(cfg.get('crawler', 'requests_retry_max_count'))
    _timeout = int(cfg.get('crawler', 'requests_timeout_max_second_count')) or None

    proxy = cfg.get('proxy', 'url') or None
    proxy_user = cfg.get('proxy', 'user') or None
    proxy_password = cfg.get('proxy', 'password') or None
    return proxy, proxy_user, proxy_password, coroutine_max_workers_count, requests_retry_max_count, _timeout


def get_url_list():
    result = []
    file_name = os.path.join(dirname, '../input/url_list.txt')
    with open(file_name, 'r', encoding='utf8')as f:
        for read_str in f.readlines():
            url = read_str.strip()
            if url:
                result.append(url)
    return result


def test():
    urls = []
    file_name = os.path.join(dirname, '../input/url_list.txt')
    with open(file_name, 'r', encoding='utf8')as f:
        for read_str in f.readlines():
            url = read_str.strip()
            if url:
                urls.append(url)
    redis_help.lpush(url_list_key, *urls)


#
# def run_crawler1(url_list, coroutine_max_workers_count, proxy, proxy_user, proxy_password):
#     task_list = []
#     requests_failed_url_list = []
#     while url_list:
#         url = url_list.pop()
#         task_list.append(url)
#         if len(task_list) == coroutine_max_workers_count:
#             fetch_task = loop.create_task(fetch(task_list, proxy, proxy_user, proxy_password))
#             loop.run_until_complete(fetch_task)
#             task_list = []
#             requests_failed_url_list += fetch_task.result()
#     return requests_failed_url_list

def get_task_from_redis(pop_task_count):
    url_list = []
    for i in range(pop_task_count):
        url = redis_help.lpop(url_list_key)
        if url:
            url_list.append(url)
    result = []
    for url in url_list:
        if not redis_help.hexists(html_dict_key, get_token(url)):
            result.append(url)

    return result


def run_crawler(coroutine_max_workers_count, proxy, proxy_user, proxy_password):
    # task_list = []
    requests_failed_url_list = []
    # file_name = os.path.join(dirname, '../input/url_list.txt')
    while True:
        pop_task_count = coroutine_max_workers_count
        # 获取任务
        task_list = get_task_from_redis(pop_task_count)
        if not task_list:
            # 无任务，暂停
            print(f'no task,sleep {sleep_max_second_count} second')
            time.sleep(sleep_max_second_count)
            continue
        else:
            loop = asyncio.get_event_loop()
            print(f'创建{len(task_list)}个任务')
            fetch_task = loop.create_task(fetch(task_list, proxy, proxy_user, proxy_password, loop))
            loop.run_until_complete(fetch_task)

    return requests_failed_url_list


def save_failed_url_to_local_file(url_list):
    file_name = os.path.join(dirname, '../output/failed_url.txt')
    with open(file_name, 'w', encoding='utf8') as f:
        for url in url_list:
            f.write(f'{url}\n')


def run():
    # test()
    global timeout
    proxy, proxy_user, proxy_password, coroutine_max_workers_count, requests_retry_max_count, timeout = get_config()
    run_crawler(coroutine_max_workers_count, proxy, proxy_user, proxy_password)


if __name__ == '__main__':
    timeout = 0
    run()
