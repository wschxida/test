import threading
import time


def do(threadlist):
    print('start')
    for x in threadlist:
        print(x)
    time.sleep(5)
    print('end')

# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

listImg = ['a','b','c','d','e','f']
totalThread = 3 #需要创建的线程数，可以控制线程的数量
lenList = len(listImg) #列表的总长度


threads = [] #创建线程列表

for i in range(totalThread):
    thread = []
    for j in range(lenList):
        if j % totalThread == i:
            thread.append(listImg[j])
            # print(thread)
    threads.append(thread)

print(threads)



for i in range(totalThread):  # 创建10个线程
    t = threading.Thread(target=do, args=(threads[i],))
    t.start()



