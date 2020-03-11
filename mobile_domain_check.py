
# 从domain表，读出所有domain_code, 并构造m.domain或者wap.domain
# 目的是找出目前收集的domain的手机版主页进行采集


import requests
import pymysql


def insert(config, name, pwd):
    conn_insert = pymysql.connect(**config)
    cur = conn.cursor()
    sql= "insert into column_root_source(website_url, domain_code, host, media_type_code, website_title, pr_value_baidu, total_score, record_md5_id, source) " \
         "VALUES('{}','{}','{}','{}','{}',200,'{}','m.domain')"
    print(sql)
    sta=cur.execute(sql)
    if sta==1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()



# 连接mysql
config = {
    'host': '192.168.1.116',
    'port': 3306,
    'user': 'root',
    'passwd': 'poms@db',
    'db':'mymonitor',
    'charset':'utf8mb4'
    }
conn = pymysql.connect(**config)
# conn.autocommit(1)
# SSCursor，貌似中文叫做流式游标
cur = conn.cursor(pymysql.cursors.SSCursor)

# 1.查询操作
# 编写sql 查询语句
sql = "select domain_id, Domain_Code, Domain_Name, Media_Type_Code, PR_Value from domain order by Domain_ID limit 100"

print("--开始从数据库读取数据--")
try:
    cur.execute(sql)  # 执行sql语句

    # results = cur.fetchall()  # 获取查询的所有记录
    print('{:<10}\t{:<20}\t{:<20}'.format("domain_id", "Domain_Code", "Domain_Name"))
    # print(cur)    # 生成器，避免读取大数据量时内存溢出
    # 遍历结果
    for row in cur:
        domain_id = row[0]
        Domain_Code = row[1]
        Domain_Name = row[2]
        # print('{:<10}\t{:<20}\t{:<20}'.format(domain_id, Domain_Code, Domain_Name))
        # print(row)
        mobile_domain_code = 'm.' + Domain_Code
        mobile_url = 'http://' + mobile_domain_code
        try:
            response = requests.get(mobile_url, timeout=5)
            if response:
                print('{:<10}\t{:<20}\t{:<20}'.format(domain_id, mobile_domain_code, Domain_Name))
        except:
            pass


except Exception as e:
    raise e
finally:
    conn.close()  # 关闭连接
print("--已从数据库读取数据--")






