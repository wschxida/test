import requests


url = 'http://lumtest.com/myip.json'
ip_list = [
    '127.0.0.1:4411'
]
proxies = {}

for i in range(100):

    proxies = {"http": "http://" + ip_list[0], "https": "http://" + ip_list[0]}
    # print(proxies)

    try:
        data = requests.get(url, proxies=proxies, timeout=5)
        text = data.text
        print(text)
    except Exception as e:
        print(e)




