from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import hashlib
import traceback
import time, json, sys
import requests, random
import redis
from stem import Signal
from stem.control import Controller
import datetime

_start_time = time.time()
run_time = 300


class GoogleSearcher:

    def __init__(self, start_time):
        self.max_workers = 50
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.lowercase_str_list = [chr(i) for i in range(97, 123)]  # 小写字母a-z
        self.capital_str_list = [chr(i) for i in range(65, 91)]  # 大写字母A-Z
        self.number_str_list = [str(i) for i in range(0, 10)]   # 数字字符0-9
        self.ua_list = self.get_useragent_list()
        self.proxy = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'}
        self.proxy_requests_failed_max_count = 10
        self.failed_url_list_key_name = 'google:failed_urls'
        self.html_dict_key_name = 'google:items'
        self.url_list_key_name = 'google:urls'
        redis_connect_params = dict(
            host='192.168.1.134',
            port='6380',
            db='0',
            password='ks_3000',
            decode_responses=True  # 返回解码结果
        )
        pool = redis.ConnectionPool(**redis_connect_params)
        self.redis_help = redis.Redis(connection_pool=pool)
        self.failed_count = 0
        self.sleep_max_second_count = 5
        self.start_time = start_time

    def is_need_restart(self):
        if time.time() - _start_time > run_time:
            python = sys.executable
            print('重启')
            try:
                os.execl(python, python, *[sys.argv[0]])
            except:
                os.execl(python, python, *['google_searcher.exe'])

    def switch_proxy(self):
        """
        切换 Tor 代理地址
        :return: NULL
        """
        while True:
            self.is_need_restart()
            with Controller.from_port() as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
            url = 'https://www.google.com.hk/search?q=特朗普&safe=strict&source=lnms&sa=X&ved=0ahUKEwjard-' \
                  'G55LrAhXFqZ4KHRFbADUQ_AUIDSgA&biw=623&bih=907&dpr=1&tbs=qdr:w'
            requests_result = self.requests_search_engine(url)
            if requests_result[0]:
                break
            else:
                print('切换代理中')

    @staticmethod
    def get_token(md5str):
        # md5str = "abc"
        # 生成一个md5对象
        m1 = hashlib.md5()
        # 使用md5对象里的update方法md5转换
        m1.update(md5str.encode("utf-16LE"))
        token = m1.hexdigest()
        return token

    @staticmethod
    def get_random_str(as_l=True, as_u=False, as_n=False, str_count=0, arg=None):
        lowercase_str_list = [chr(i) for i in range(97, 123)]
        capital_str_list = [chr(i) for i in range(65, 91)]
        number_str_list = [str(i) for i in range(0, 10)]
        ran_s = [] + (arg or [])
        if as_l:
            ran_s += lowercase_str_list
        if as_u:
            ran_s += capital_str_list
        if as_n:
            ran_s += number_str_list

        return ''.join([random.sample(ran_s, 1)[0] for i in range(str_count)])

    @staticmethod
    def no_error_requests(url, headers=None, cookies=None, proxy=None, timeout=None):
        try:
            response = requests.get(url=url, headers=headers, cookies=cookies, proxies=proxy, timeout=timeout)
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, 请求失败')
            return ''

    def get_task_from_redis(self, pop_task_count):
        result = []
        for i in range(pop_task_count):
            url = self.redis_help.lpop(self.url_list_key_name)
            if url:
                result.append(url)
        if not result:
            # 没有采集任务，从采集失败ur队列中取出任务
            for i in range(pop_task_count):
                url = self.redis_help.lpop(self.failed_url_list_key_name)
                if url:
                    result.append(url)
                else:
                    break

        return result

    def run(self):
        time.sleep(3)
        count = 0
        while True:
            pop_task_count = self.max_workers
            # 获取任务
            task_list = self.get_task_from_redis(pop_task_count)
            thread_task_list = []
            if not task_list:
                # 无任务，暂停
                print(f'no task,sleep {self.sleep_max_second_count} second')
                time.sleep(self.sleep_max_second_count)
                continue
            for task in task_list:
                article_url = task.strip()
                print(f'requests url:{article_url}')
                # 区分是新闻还是搜索引擎
                if '&tbm=nws' in article_url:
                    thread_task = self.executor.submit(self.requests_news_page, article_url)
                else:
                    thread_task = self.executor.submit(self.requests_search_engine, article_url)
                thread_task_list.append(thread_task)
                count += 1
                # 达到最大线程工作数，开始获取结果，获取完后再执行下一轮线程，防止对代理造成过高并发
                if count >= self.max_workers:
                    self.parse_thread_task_result(thread_task_list)
                    _successful_list, _failed_list = [], []
                    thread_task_list = []
                    count = 0

            self.parse_thread_task_result(thread_task_list)

    def parse_thread_task_result(self, thread_task_list):
        # 解析线程任务
        successful_list = []
        failed_list = []
        for thread_task in as_completed(thread_task_list):
            as_successful, response_text, url = thread_task.result()
            url_md5 = self.get_token(url)
            if as_successful:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 请求成功')
                successful_list.append((url_md5, response_text))
            else:
                self.failed_count += 1
                failed_list.append(url)
        if self.failed_count >= self.proxy_requests_failed_max_count:
            # 请求失败次数过多，切换代理
            self.failed_count = 0
            self.switch_proxy()
        for url_md5, response_text in successful_list:
            # 保存结果至redis
            self.redis_help.hset(self.html_dict_key_name, url_md5, response_text)
        if failed_list:
            self.redis_help.lpush(self.failed_url_list_key_name, *failed_list)

        return successful_list, failed_list

    def requests_search_engine(self, url):
        cookies = {
            'CGIC': self.get_random_str(True, True, True, 160)
        }
        user_agent = random.sample(self.ua_list, 1)[0]
        headers = {'User-agent': user_agent}
        response = self.no_error_requests(url=url.replace('&tbs=qdr:w', '') + '&tbs=qdr:w', headers=headers,
                                          cookies=cookies, proxy=self.proxy, timeout=20)
        if response and response.status_code != 429:
            print('requests succeed')
            return True, response.text, url
        else:
            return False, None, url

    def requests_news_page(self, url):
        cookies = {
            'CGIC': self.get_random_str(True, True, True, 160)
        }
        user_agent = random.sample(self.ua_list, 1)[0]
        headers = {'User-agent': user_agent}
        response = self.no_error_requests(url=url.replace('&tbs=qdr:w', '') + '&tbs=qdr:w', headers=headers,
                                          cookies=cookies,
                                          proxy=self.proxy, timeout=20)
        if response:
            return True, response.text, url
        else:
            return False, None, url

    def get_useragent_list(self):
        file = os.path.join(self.dirname, '../input/ua.txt')
        with open(file, 'r', encoding='utf-8') as f:
            _ua_list = f.readlines()
            ua_list = [i.replace('\n', '') for i in _ua_list]
        return ua_list


if __name__ == '__main__':
    try:
        searcher = GoogleSearcher(_start_time)
        searcher.run()
    except:
        with open('error.log', 'a', encoding='utf8') as f:
            f.write(traceback.format_exc())
