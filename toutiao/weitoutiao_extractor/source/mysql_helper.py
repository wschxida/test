import MySQLdb, re
import MySQLdb.cursors
import traceback


class MysqlHelper:
    # json数据转换mysql数据类
    def __init__(self, **database_config):
        self.conn = MySQLdb.connect(**database_config)
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, sql, params=None):
        # 替换原有的执行方式，
        try:
            res = self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
            self.conn.commit()
            if re.search('select|show', sql, re.I):
                return self.cursor.fetchall()
            return True, True
        except Exception as e:
            error_info = str(e)
        return False, error_info

    def executemany(self, sql, params_list=None):
        # 替换原有的批量执行方式，

        try:
            res = self.cursor.executemany(sql, params_list) if params_list else self.cursor.execute(sql)
            self.conn.commit()
            return True, True
        except Exception as executemany_error:
            # 批量执行失败时，循环执行单插入
            print('批量执行失败:',executemany_error)
            for params in params_list:
                try:
                    self.execute(sql, params)
                    self.conn.commit()
                except Exception as execute_error:
                    error_info = str(execute_error)
                    print(error_info)
            return False, False

    def generate_insert_sql_statement(self, data, table_name):
        # 生成sql批量插入语句
        # 要求接收的数据严格按照模板来，不能缺少key，如key没有值设置为空字符串即可
        #
        data = data if data else {}
        placeholder_str_list = []  # 占位符字符串列表
        column_name_str_list = []  # 列名字符串列表
        for key in data.keys():
            column_name_str_list.append(str(key))
            placeholder_str_list.append('%({})s'.format(key))
        column_str = ','.join(column_name_str_list)
        placeholder_str = ','.join(placeholder_str_list)
        insert_sql = 'INSERT INTO %s(%s) VALUES(%s)' % (table_name, column_str, placeholder_str)
        return insert_sql
