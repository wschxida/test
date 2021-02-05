import requests
import sys

'''
用于获取Instagram页面，可加上代理
示例：
get_instagram_html.exe "http://lumtest.com/myip.json" "myip.txt"
get_instagram_html.exe "http://lumtest.com/myip.json" "myip.txt" "bxupro:2018Prxy@23.105.151.150:29842"
get_instagram_html.exe "http://www.instagram.com/saljeweler1/" "saljeweler1.txt"
get_instagram_html.exe "http://www.instagram.com/saljeweler1/" "saljeweler1.txt" "bxupro:2018Prxy@23.105.151.150:29842"
'''


def get_ig_html(argv):
    query_url = ""
    result_file_name = ""
    proxy = ""

    for i in range(len(argv)):
        if i == 1:
            query_url = argv[1]
        if i == 2:
            result_file_name = argv[2]
        if i == 3:
            proxy = argv[3]

    proxy_list = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    }

    try:
        if proxy:
            response = requests.get(query_url, headers=headers, proxies=proxy_list, timeout=5)
        else:
            response = requests.get(query_url, headers=headers, timeout=5)
        result = response.text
        with open(result_file_name, 'w', encoding="utf-8") as w:
            w.write(result)
    except:
        pass


if __name__ == '__main__':
    get_ig_html(sys.argv)
    # get_ig_html('http://lumtest.com/myip.json', 'test.txt', 'bxupro:2018Prxy@23.105.151.150:29842')
