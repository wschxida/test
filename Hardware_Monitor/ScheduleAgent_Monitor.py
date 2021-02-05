#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2020/12/18
# @Desc  :


import os
import time


def is_running(process_name):
    try:
        process = len(os.popen('tasklist | findstr ' + process_name).readlines())
        if process >= 1:
            return True
        else:
            return False
    except:
        print("program error!")
        return False


def start_process(process_name):
    try:
        os.popen('start ' + process_name)
        return True
    except:
        print("program error!")
        return False


def main():
    process_name = 'ScheduleAgent.exe'
    while True:
        flag = is_running(process_name)
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        f = open('ScheduleAgent_Monitor.txt', 'a', encoding='utf-8')
        print('\n', time_str)
        f.write('\n' + time_str + '\n')
        if flag:
            print('ScheduleAgent.exe is running...!!!')
            f.write('ScheduleAgent.exe is running...!!!\n')
        else:
            print('error! ScheduleAgent.exe is not detected...!!!')
            print('Restarted ScheduleAgent...!!!')
            f.write('error! ScheduleAgent.exe is not detected...!!!\n')
            f.write('Restarted ScheduleAgent...!!!\n')
            start_process(process_name)
        f.close()
        time.sleep(60)   # 每隔60s进行检查


if __name__ == "__main__":
    main()
