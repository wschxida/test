import requests
import json
import time

url = 'http://lumtest.com/myip.json'


ip_list = ["bxupro:2018Prxy@23.80.142.48:29842",
"bxupro:2018Prxy@23.105.151.201:29842",
"bxupro:2018Prxy@172.102.194.176:29842",
"bxupro:2018Prxy@172.98.185.203:29842",
"bxupro:2018Prxy@23.80.141.145:29842",
"bxupro:2018Prxy@23.105.150.202:29842",
"bxupro:2018Prxy@23.80.142.242:29842",
"bxupro:2018Prxy@23.105.151.150:29842",
"bxupro:2018Prxy@172.102.194.190:29842",
"bxupro:2018Prxy@172.98.185.149:29842",
"bxupro:2018Prxy@23.80.141.80:29842",
"bxupro:2018Prxy@23.105.150.74:29842",
"bxupro:2018Prxy@23.80.142.52:29842",
"bxupro:2018Prxy@23.105.151.234:29842",
"bxupro:2018Prxy@172.102.194.97:29842",
"bxupro:2018Prxy@172.98.185.112:29842",
"bxupro:2018Prxy@23.80.141.226:29842",
"bxupro:2018Prxy@23.80.147.125:29842",
"bxupro:2018Prxy@23.81.55.110:29842",
"bxupro:2018Prxy@23.81.55.15:29842",
"bxupro:2018Prxy@51.68.223.202:29842",
"bxupro:2018Prxy@51.68.223.203:29842",
"bxupro:2018Prxy@23.81.80.184:29842",
"bxupro:2018Prxy@23.81.63.229:29842",
"bxupro:2018Prxy@23.81.80.128:29842",
"bxupro:2018Prxy@23.81.63.175:29842",
"bxupro:2018Prxy@23.81.80.240:29842"]




proxies = {}

for i in ip_list:

    proxies = {"http": "http://" + i, "https": "http://" + i}
    print(proxies)

    try:
        data = requests.get(url, proxies=proxies, timeout=5)
        text = data.text
        print(text)
    except Exception as e:
        print(e)




