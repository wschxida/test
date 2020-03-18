
import requests


def get_result_by_requests(url, proxies=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.121 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Connection": "keep - alive",
    }
    response = requests.get(url, timeout=20, proxies=proxies)
    response.encoding = "utf-8"
    text = response.text
    return text


if __name__ == '__main__':

    _proxies = {'http': 'http://lum-customer-hl_7cc83d7d-zone-zone2:lojhjbwx42hp@zproxy.lum-superproxy.io:22225',
                 'https': 'http://lum-customer-hl_7cc83d7d-zone-zone2:lojhjbwx42hp@zproxy.lum-superproxy.io:22225'}

    _proxies = {'http：//': 'http://lum-customer-hl_7cc83d7d-zone-zone1:ksutslx08n80@zproxy.lum-superproxy.io:22225',
                'https：//': 'http://lum-customer-hl_7cc83d7d-zone-zone1:ksutslx08n80@zproxy.lum-superproxy.io:22225'}

    # _proxies = {'http': 'http://bxupro:2018Prxy@23.80.142.48:29842',
    #             'https': 'http://bxupro:2018Prxy@23.80.142.48:29842'}

    # _url = "https://twitter.com/jack"
    # result = get_result_by_requests(_url, _proxies)
    # print(len(result))

    _url = "http://lumtest.com/myip.json"
    result = get_result_by_requests(_url, _proxies)
    print(result)

    _url = "https://www.instagram.com/jack/"
    result = get_result_by_requests(_url, _proxies)
    print(len(result))
