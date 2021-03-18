import re
import redis
from toutiao.weitoutiao_extractor.source.mysql_helper import MysqlHelper
from toutiao.weitoutiao_extractor.source.signature_generator import SignatureGenerator


def get_task(website_no):
    mysql_helper = connect_mysql()
    sql = f'''select tosearch_keyword_id,article_search_keyword,keyword from 
                        (select tosearch_keyword_id,keyword,
                        if(right(keyword,1)='@',substring_index(keyword,'@',1),keyword) as article_search_keyword,
                        '' as website_no,ceiling(rand()*100) rnd,if(created_time between date_sub(now(),interval 12 hour) and now(),1,0) as lastest_word,
                        priority_level,last_update_time from tosearch_keyword_no_website_group t where (t.expire_time>=now() or t.expire_time is null)
                        union 
                        select tosearch_keyword_id,keyword,
                        if(right(keyword,1)='@',substring_index(keyword,'@',1),keyword) as article_search_keyword,website_no,ceiling(rand()*100) rnd,
                        if(created_time between date_sub(now(),interval 12 hour) and now(),1,0) as lastest_word,
                        priority_level,last_update_time from tosearch_keyword_with_group where website_no='{website_no}' 
                        and (expire_time>=now() or expire_time is null)
                        ) keyword
                        group by keyword 
                        order by lastest_word desc,priority_level desc,last_update_time desc,rnd desc,tosearch_keyword_id desc '''
    data = mysql_helper.execute(sql)
    result = []
    for record in data:
        article_search_keyword = record.get('article_search_keyword')
        result.append(article_search_keyword)
    return result


def connect_redis():
    redis_connect_params = dict(
        host='192.168.1.134',
        port='6379',
        db='0',
        password='ks_3000',
        decode_responses=True  # 返回解码结果
    )
    pool = redis.ConnectionPool(**redis_connect_params)
    redis_help = redis.Redis(connection_pool=pool)
    return redis_help


def connect_mysql():
    mysql_config = {'user': 'root', 'passwd': 'poms@db', 'host': '192.168.1.116', 'port': 3306, 'db': 'mymonitor',
                    'charset': 'utf8mb4'}
    mysql_help = MysqlHelper(**mysql_config)

    return mysql_help


def save_task_to_redis(task_file_name, website_no):
    result_list = []
    with open(task_file_name, 'r', encoding='utf8') as f:
        for read_str in f.readlines():
            req_url = read_str.strip()
            if not req_url:
                continue
            article_search_keyword = re.search('keyword=(.*?)&', req_url)[1]
            listpage_url = req_url
            search_word = article_search_keyword
            referer_id = '123'
            extract_config_no = 'CS7988'
            save_rule = 3
            url = f'{listpage_url}#scrapy_meta#config_no={extract_config_no}#website_no={website_no}#save_rule={save_rule}#search_word={search_word}#referer_id={referer_id}'
            result_list.append(url)
    redis_helper = connect_redis()
    redis_helper.lpush('article_detail:start_urls', *result_list)
    return result_list


def test():
    website_no = 'S19182'
    search_keyword_list = get_task(website_no)
    generator = SignatureGenerator(website_no, keyword_list=search_keyword_list[:2])
    task_file_name = generator.run()
    save_task_to_redis(task_file_name, website_no)


if __name__ == '__main__':
    test()
