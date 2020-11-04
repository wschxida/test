import requests


url = 'http://lumtest.com/myip.json'
url = 'https://twitter.com/i/profiles/show/Huawei/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true&max_position'
ip_list = [
    '127.0.0.1:4411'
]
proxies = {}
headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://twitter.com/Huawei",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }

for i in range(1):

    proxies = {"http": "http://" + ip_list[0], "https": "http://" + ip_list[0]}
    # print(proxies)

    try:
        data = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        text = data.text
        print(text)
    except Exception as e:
        print(e)




