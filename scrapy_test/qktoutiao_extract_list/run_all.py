# -*- coding: utf-8 -*-
from scrapy import cmdline
import time
import os
from platform import platform



def run(cmd):
    os_platform = platform()
    fn = os.path.basename(__file__)
    if 'Linux' in os_platform:
        result = os.popen('ps -ef |grep "{}" |grep -v "grep" |wc -l'.format(fn)).read()
        if result.strip() == '1':
            os.system(cmd)
            # cmdline.execute(cmd.split())
        else:
            print("only run one at the same time!")
    elif 'Windows' in os_platform:
        result = os.popen('tasklist /v /fi "imagename ne pycharm64.exe" |find /c "{}"'.format(fn)).read()
        if result.strip() == '1':
            os.system(cmd)
            # cmdline.execute(cmd.split())
        else:
            print("only run one at the same time!")


def main():
    cmd = 'scrapy_test crawl qktoutiao'
    log_file = os.path.basename(__file__).split(".")[0] + ".log"

    while True:
        with open(log_file,'a') as f:
            f.write("begin_time:{}\n".format(time.ctime()))
        start_time = time.time()
        run(cmd)
        ended_time = time.time()
        t = ended_time - start_time
        with open(log_file,'a') as f:
            f.write("ended_time:{},took time:{}m {}s\n".format(time.ctime(), round(t // 60), round(t % 60, 2)))
        size = os.path.getsize(log_file)
        if size>=1024*1024*1:
            os.remove(log_file)
        time.sleep(30)

if __name__ == '__main__':
    main()

