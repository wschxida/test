# coding=utf8
import pymysql


if __name__ == '__main__':

    # 连接mysql
    config_117 = {
        'host': '192.168.1.117',
        'port': 3306,
        'user': 'root',
        'passwd': 'poms@db',
        'db': 'mymonitor',
        'charset': 'utf8mb4',
    }
    conn_117 = pymysql.connect(**config_117)
    conn_117.autocommit(1)
    cur_117 = pymysql.cursors.SSCursor(conn_117)
    # 使用cursor()方法获取操作游标
    # cur_117 = conn_117.cursor()

    config_doris = {
        'host': '192.168.2.56',
        'port': 9030,
        'user': 'root',
        'passwd': '',
        'db': 'wsc_test',
        'cursorclass': pymysql.cursors.DictCursor
    }
    conn_doris = pymysql.connect(**config_doris)
    conn_doris.autocommit(1)
    # 使用cursor()方法获取操作游标
    cur_doris = conn_doris.cursor()

    select_sql = "select article_detail_id, article_title, article_abstract from article_detail " \
                 "where article_title is not null and article_abstract is not null " \
                 "limit 1000000"

    cur_117.execute(select_sql)
    # data = cur_117.fetchall()
    while True:
        item = cur_117.fetchone()
        if not item:
            break
        # print(item)
        insert_sql = "insert into article_content(id, article_title, article_content) values({}, '{}', '{}')"\
            .format(item[0], item[1][0:1000], item[2][0:65520])
        # print(insert_sql)
        try:
            cur_doris.execute(insert_sql)
        except Exception as e:
            print(e)
    conn_117.close()
    conn_doris.close()











