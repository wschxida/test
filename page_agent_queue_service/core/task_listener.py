import redis
from flask import Flask, request
import json, hashlib
import traceback
app = Flask(__name__)

app.url_map.strict_slashes = False
redis_connect_params = dict(
    host='192.168.1.134',
    port='6380',
    db='0',
    password='ks_3000',
    decode_responses=True  # 返回解码结果
)
url_list_key_pattern = 'page_agent_queue_service:{}:urls'
html_dict_key_pattern = 'page_agent_queue_service:{}:items'
pool = redis.ConnectionPool(**redis_connect_params)
redis_help = redis.Redis(connection_pool=pool)
return_data_count = 100


def get_token(md5str):
    # md5str = "abc"
    # 生成一个md5对象
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-16LE"))
    token = m1.hexdigest()
    return token


def get_crawler_data(website, url_list):
    html_dict_key_name = html_dict_key_pattern.format(website)
    result = []
    for url in url_list:
        url_md5 = get_token(url)
        html = redis_help.hget(html_dict_key_name, url_md5)
        if html:
            result.append(dict(html=html, url_md5=url_md5))
            redis_help.hdel(html_dict_key_name, url_md5)
    if len(result) == 1:
        return result[0].get('html')
    elif not result:
        return ''
    else:
        return json.dumps(result)


def push_task_to_redis(website, url_list):
    # 提交任务至redis
    url_list_key_name = url_list_key_pattern.format(website)
    task_list = []
    for url in url_list:
        if 'http' in url:
            task_list.append(url)
    redis_help.lpush(url_list_key_name, *task_list)


@app.route('/post_task/url/<path:website>/<path:url>/', methods=['POST', 'GET'])
def post_task_page(website, url):
    json_str = request.get_data(as_text=True)
    try:
        if request.method == 'POST':
            url_list = json.loads(json_str).get('url_list') if json_str else ''
        elif request.method == 'GET':
            url_list = [url]
        else:
            url_list = []
        push_task_to_redis(website, url_list)
        data = get_crawler_data(website, url_list)
        if data:
            return data
        else:
            return ''
    except:
        return ''


if __name__ == '__main__':
    with open('port.txt', 'r', encoding='utf8') as f:
        port = f.read().strip()
    try:
        port = int(port) if port else 6666
        app.run(host='0.0.0.0', port=port, debug=True)
    except:
        print(traceback.format_exc())
