#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : facebook_extractor.py
# @Author: Cedar
# @Date  : 2020/12/17
# @Desc  :


import youtube_dl
import threading
import time
# import xvideos


def start_download(youtube_url_list):
    try:
        # 定义某些下载参数
        ydl_opts = {
            'proxy': '127.0.0.1:7777',
            'format': 'best',
            'retries': 20,
            'autonumber-start': 2,
            'ignore-errors': '',
            'outtmpl': 'E:\\youtube-dl\\' + '%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(youtube_url_list)
    except:
        pass


if __name__ == '__main__':

    url_list = [
        'https://www.xvideos.com/video43778969/china_sauna_full_service_-_grey_tank_top',
        'https://www.xvideos.com/video44108321/china_sauna_full_service_-_young_graduate',
        'https://www.xvideos.com/video32840283/sauna_vip_full_service_massage',
        'https://www.xvideos.com/video43863633/china_sauna_full_service_-_lisa',
        'https://www.xvideos.com/video23359374/_',

    ]
    # url_list = xvideos.result
    print(len(url_list))

    totalThread = 50  # 需要创建的线程数，可以控制线程的数量
    lenList = len(url_list)  # 列表的总长度
    threads = []  # 创建线程列表

    for i in range(totalThread):
        thread = []
        for j in range(lenList):
            if j % totalThread == i:
                thread.append(url_list[j])
                # print(thread)
        threads.append(thread)

    print(threads)

    for i in range(totalThread):  # 创建10个线程
        t = threading.Thread(target=start_download, args=(threads[i],))
        t.start()

# youtube-dl "https://www.youtube.com/watch?v=POArm5fZbR8" --proxy "127.0.0.1:7777" -f best --retries 20
