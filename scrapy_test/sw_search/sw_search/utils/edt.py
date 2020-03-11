#!/usr/bin/python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# str to date
# http://wenku.baidu.com/link?url=qZMHu3KfF21fevw2dLYoBIHthBgiK_oT11Ns-7_kRs5uLngfRKdgd_9dW3vzYyq3hXe9wNmWM4CszJUCXyCZxmXPurlzJKd2SJIqsFHy_oC
# http://blog.csdn.net/mayixixi/article/details/8030473
# http://my.oschina.net/xinxingegeya/blog/394821 https://www.cnblogs.com/pyxiaomangshe/p/7918850.html

# 下面是几种标准时间格式
# 2016-01-13T00:07:59.000Z  ==>UT (转成北京时间：2016-01-13 08:07:59)
# 2016-01-12T23:35:42-05:00 ==>vimeo.com UTC格式时间 (转成北京时间：2016-01-13 12:35:42)
# Wed Jan 13 16:22:04 +0800 2016  ==>SW (转成北京时间：2016-01-13 16:22:04)
# Sun Mar 29 22:15:50 +0000 2015  ==>TW (转成北京时间：2015-03-30 06:15:50)
# 1452676751  ==>Unix timestamp (转成北京时间：2016/1/13 17:19:11)

# import time
# t = time.strptime("2016-01-05T09:57:49-05:00", "%Y-%m-%dT%H:%M:%S-05:%f")
# print time.strftime("%Y-%m-%d %H:%M:%S",t)


import sys
import re
import time
from datetime import datetime
from dateutil.relativedelta import *
from functools import wraps # 装饰器
def stat_time(fn):
    @wraps(fn)
    def wrap(*args, **kw):
        start = time.clock()
        print('call ' + fn.__name__ + '()...')
        ret = fn(*args, **kw)
        ended = time.clock()
        print("cost: {} seconds".format(ended-start))
        return ret
    return wrap


def cn_to_digit(cn_str):
    replace_dict = {
        '〇': '0',
        '一': '1',
        '二': '2',
        '两': '2',
        '三': '3',
        '四': '4',
        '五': '5',
        '六': '6',
        '七': '7',
        '八': '8',
        '九': '9',
        '十': '10',
        '零': '0',
        '壹': '1',
        '贰': '2',
        '叁': '3',
        '肆': '4',
        '伍': '5',
        '陆': '6',
        '柒': '7',
        '捌': '8',
        '玖': '9',
        '拾': '10'
    }
    for i in replace_dict:
        cn_str = cn_str.replace(i, replace_dict[i],1)
    digit_str = cn_str
    return digit_str


def get_absolute_datetime(datetime_str):
    datetime_str = cn_to_digit(datetime_str)
    datetime_str = datetime_str.replace('刚刚', '1 seconds ago', 1)
    if '前' in datetime_str:
        datetime_str = datetime_str.replace('年前', 'years ago', 1)
        datetime_str = datetime_str.replace('月前', 'months ago', 1)
        datetime_str = datetime_str.replace('个月前', 'months ago', 1)
        datetime_str = datetime_str.replace('天前', 'days ago', 1)
        datetime_str = datetime_str.replace('日前', 'days ago', 1)
        datetime_str = datetime_str.replace('小时前', 'hours ago', 1)
        datetime_str = datetime_str.replace('个小时前', 'hours ago', 1)
        datetime_str = datetime_str.replace('时前', 'hours ago', 1)
        datetime_str = datetime_str.replace('分钟前', 'minutes ago', 1)
        datetime_str = datetime_str.replace('分前', 'minutes ago', 1)
        datetime_str = datetime_str.replace('秒前', 'seconds ago', 1)
        datetime_str = datetime_str.replace('秒钟前', 'seconds ago', 1)

    if 'ago' in datetime_str:
        years = re.search(r'(\d{1,2})(\s*years*\s*ago.?)', datetime_str, flags=re.I)
        months = re.search(r'(\d{1,2})\s*months*\s*ago.?', datetime_str, flags=re.I)
        days = re.search(r'(\d{1,2})\s*days*\s*ago.?', datetime_str, flags=re.I)
        hours = re.search(r'(\d{1,2})\s*hours*\s*ago.?', datetime_str, flags=re.I)
        minutes = re.search(r'(\d{1,2})\s*minutes*\s*ago.?', datetime_str, flags=re.I)
        seconds = re.search(r'(\d{1,2})\s*seconds*\s*ago.?', datetime_str, flags=re.I)
        years = int(years.group(1)) if years else 0
        months = int(months.group(1)) if months else 0
        days = int(days.group(1)) if days else 0
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        dt_delta = relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
        dt = datetime.now() - dt_delta
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    if '天' in datetime_str and ':' in datetime_str and datetime_str.count(":")==2:
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now()-relativedelta(days=1)).strftime('%Y-%m-%d')
        before_yesterday = (datetime.now() - relativedelta(days=2)).strftime('%Y-%m-%d')
        datetime_str = datetime_str.replace('今天', today, 1)
        datetime_str = datetime_str.replace('昨天', yesterday, 1)
        datetime_str = datetime_str.replace('前天', before_yesterday, 1)
        dt = datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif '天' in datetime_str and ':' in datetime_str:
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now()-relativedelta(days=1)).strftime('%Y-%m-%d')
        before_yesterday = (datetime.now() - relativedelta(days=2)).strftime('%Y-%m-%d')
        datetime_str = datetime_str.replace('今天', today, 1)
        datetime_str = datetime_str.replace('昨天', yesterday, 1)
        datetime_str = datetime_str.replace('前天', before_yesterday, 1)
        dt = datetime.strptime(datetime_str,'%Y-%m-%d %H:%M')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif '天' in datetime_str and ':' not in datetime_str:
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now()-relativedelta(days=1)).strftime('%Y-%m-%d')
        before_yesterday = (datetime.now() - relativedelta(days=2)).strftime('%Y-%m-%d')
        datetime_str = datetime_str.replace('今天', today, 1)
        datetime_str = datetime_str.replace('昨天', yesterday, 1)
        datetime_str = datetime_str.replace('前天', before_yesterday, 1)
        dt = datetime.strptime(datetime_str,'%Y-%m-%d')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif '-' in datetime_str and 'T' in datetime_str and 'Z' in datetime_str:
        # 2016-01-13T00:07:59.000Z
        dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-\d{2}:00.?', datetime_str, flags=re.I):
        # 2016-01-12T23:35:42-05:00
        dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S-%f:00')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif re.search(r'[A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}\s+[+-]*\d*\s+\d{4}.?', datetime_str, flags=re.I):
        # "Wed Jan 13 16:22:04 +0800 2016","Sun Mar 29 22:15:50 +0000 2015"
        datetime_str = datetime_str.replace('+0000','')
        datetime_str = datetime_str.replace('+0800', '')
        dt = datetime.strptime(datetime_str, '%c')
        return dt.strftime('%Y-%m-%d %H:%M:%S')


    elif '-' in datetime_str:
        if datetime_str.count('-')==1:
            this_year = datetime.now().strftime('%Y')
            if datetime_str.count(':')==0:
                dt = datetime.strptime(this_year+'-'+datetime_str, '%Y-%m-%d')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==1:
                dt = datetime.strptime(this_year+'-'+datetime_str, '%Y-%m-%d %H:%M')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==2:
                dt = datetime.strptime(this_year+'-'+datetime_str, '%Y-%m-%d %H:%M:%S')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
        elif datetime_str.count('-')==2:
            if datetime_str.count(':')==0:
                dt = datetime.strptime(datetime_str, '%Y-%m-%d')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==1:
                dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==2:
                dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif '/' in datetime_str:
        if datetime_str.count('/')==1:
            this_year = datetime.now().strftime('%Y')
            if datetime_str.count(':')==0:
                dt = datetime.strptime(this_year+'/'+datetime_str, '%Y/%m/%d')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==1:
                dt = datetime.strptime(this_year+'/'+datetime_str, '%Y/%m/%d %H:%M')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==2:
                dt = datetime.strptime(this_year+'/'+datetime_str, '%Y/%m/%d %H:%M:%S')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
        elif datetime_str.count('/')==2:
            if datetime_str.count(':')==0:
                dt = datetime.strptime(datetime_str, '%Y/%m/%d')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==1:
                dt = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif datetime_str.count(':')==2:
                dt = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
                return dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None

@stat_time
def run():
    datetime_str = [
        "刚刚","30 秒前","30秒前","30秒钟前",
        "30分前","30分钟前","30 分前","30 分钟前",
        "3小时前","3时前","3 时前","3 小时前",
        "3天前","3 天前","3月前","3 月前","3年前","3 年前",
        "今天 18:25:11", "昨天 18:25:11", "前天 18:25:11",
        "今天 18:25","昨天 18:25","前天 18:25",
        "今天","昨天","前天",
        "09-26","2013-07-20","09/27","2018/09/26",
        "09-26 12:10", "2013-07-20 12:10", "09/27 12:10", "2018/09/26 12:10",
        "09-26 12:10:11", "2013-07-20 12:10:11", "09/27 12:10:11", "2018/09/26 12:10:11",
        "2016-01-13T00:07:59.000Z","2016-01-12T23:35:42-05:00",
        "Wed Jan 13 16:22:04 +0800 2016","Sun Mar 29 22:15:50 +0000 2015",
        "Fri Aug 31 21:24:35 +0800 2018",
        "非时间"
    ]
    for dt_str in datetime_str:
        try:
            print(dt_str," ----> ",get_absolute_datetime(dt_str))
        except Exception as e:
            print(str(e))
            pass
    dt_str = datetime.strptime('Wed Jan 13 16:22:04 2016','%c').strftime('%c')
    print(dt_str)


if __name__ == '__main__':
    run()
