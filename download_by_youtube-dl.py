import youtube_dl
import threading
import time

# youtube-dl "https://www.youtube.com/watch?v=POArm5fZbR8" --proxy "127.0.0.1:7777" -f best --retries 20

def download(youtube_url_list):
    # 定义某些下载参数
    ydl_opts = {
        'proxy': '127.0.0.1:4411',
        'format': 'best',
        'retries': 20,
        'autonumber-start': 2,
        'ignore-errors': '',
        'outtmpl': 'D:\youtube-dl\\' + '%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(youtube_url_list)


if __name__ == '__main__':

    url_list = [
        'https://www.youtube.com/watch?v=3IY9M5jUO_Q',
    ]

    totalThread = 10  # 需要创建的线程数，可以控制线程的数量
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
        t = threading.Thread(target=download, args=(threads[i],))
        t.start()

