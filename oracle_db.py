# -*- encoding: utf-8 -*-
"""
版权所有 © 2019-present, 乐思软件
All rights reserved.

@file: oracle_db.py
@author: LY
@date: 2020/9/15
"""
import cx_Oracle
import os
from config import base_settings
from common.help_tools import HelpTools


class OracleDB:
    """
    oracle数据库类
    """

    def __init__(self, db_config, auto_close_executed=True, is_auto_classify=None):
        """
        初始化数据库连接
        :param db_config: {'username': 'xx', 'password':'xx', 'host': '192.168.1.170', 'port': 1521, 'server_name': 'orcl'}
        """
        self.conn = None
        self.cur = None
        self.error = None
        self.auto_close_executed = auto_close_executed

        self.host = db_config['host']
        self.port = db_config.get('port', 1521)
        self.server_name = db_config.get('server_name', 'orcl')
        self.username = db_config['username']
        self.password = db_config['password']

        self.help_tools = HelpTools(is_auto_classify)

    # 连接数据库操作
    def __conn(self):
        if self.conn and self.cur:
            return self.cur

        try:
            self.conn = cx_Oracle.connect(f'{self.username}/{self.password}@{self.host}:{self.port}/{self.server_name}')
            self.cur = self.conn.cursor()
            return self.cur
        except cx_Oracle.DatabaseError as e:
            error = f"connect_Oracle_Database failed. {repr(e)}"
            self.help_tools.log(base_settings.CLASSIFY_ERROR_LOG_FILENAME, 'oracle connect error' + error)
            return False

    def __set_error(self, error):
        self.error = error

    def get_error(self):
        return self.error

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        try:
            if self.conn and self.cur:
                self.cur.close()
                self.conn.close()
                self.cur = None
                self.conn = None
        except:  # noqa: E722
            pass
        return True

    def __del__(self):
        # 当程序结束时运行
        # print("\nClose database connect")
        self.close()

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql: str, query_type='not_query', col_name_case='initial'):
        """
        执行 sql 语句
        :param sql
        :param query_type: fetchcolumn, fetch, fetchall, (not_query || '')
        :param col_name_case: 查询用，字段名称大小写 [initial: 数据库定义，lower: 全小写，upper: 全大写]
        """

        if self.__conn() is False:
            return False

        try:
            result = self.cur.execute(sql)

            if query_type == '' or query_type == 'not_query':
                self.conn.commit()
            else:  # 查询
                if query_type == 'fetchcolumn':
                    row = self.cur.fetchone()
                    result = None if row is None else row[0]
                else:
                    if query_type == 'fetch':
                        result = self.cur.fetchone()
                    else:
                        result = self.cur.fetchall()

                    # 将行记录格式化为键值对形式
                    if result is not None:
                        result = self.__format_fetch_result(self.cur.description, result, query_type, col_name_case)

        except cx_Oracle.DatabaseError as e:
            error = f"Execute failed ({query_type}): {repr(e)}: {str(e)}\n{sql}"
            self.help_tools.log(base_settings.CLASSIFY_ERROR_LOG_FILENAME, 'oracle execute error' + error)
            result = False

        if self.auto_close_executed:
            self.close()

        return result

    def query(self, sql, query_type='fetchall', col_name_case='initial'):
        """
        执行查询操作
        :param sql: SELECT SQL
        :param query_type: 查询类型，支持三种：fetchcolumn, fetch, fetchall
        :param col_name_case: 字段名称大小写 [initial: 数据库定义，lower: 全小写，upper: 全大写]

        :return 查无结果返回 None, 异常返回 False 可通过 get_error 获取错误信息
                fetchcolumn 返回第一个字段第一个值, fetch 返回某行记录（字典键值对）, fetchall 返回多行记录（其内元素为键值对）
        """
        return self.execute(sql, query_type, col_name_case)

    @staticmethod
    def __format_fetch_result(cols_desc, data, fetch_type='fetchall', col_name_case='initial'):
        """
        格式化查询结果，使行记录为字典
        :param cols_desc: 字段描述列表
        :param data: 查询结果
        :param fetch_type: 查询类型：fetch 获取一行，data为tuple; fetchall 获取多行，data为列表，其内元素为tuple
        :param col_name_case: 字段名称大小写 [initial: 数据库定义，lower: 全小写，upper: 全大写]
        :return 字典或列表
        """

        # 取出字段名称
        col_names = []
        for col in cols_desc:
            field_name = col[0]

            if col_name_case == 'lower':
                field_name = field_name.lower()
            elif col_name_case == 'upper':
                field_name = field_name.upper()

            col_names.append(field_name)

        def tuple_to_dict(row_tuple):
            d = dict()
            for idx, field_name in enumerate(col_names):
                d[field_name] = row_tuple[idx]

            return d

        if fetch_type == 'fetch':
            return tuple_to_dict(data)
        else:
            return list(map(tuple_to_dict, data))
