__author__ = 'cedar'

import sys
import requests
import re, time



def google_news_search(query_url, result_file_name):

    # proxy_file = "D:\\KWM\\Extraction_Server\\Config\\ProxyList\\abuyun_weixin.txt"
    # with open(proxy_file, 'r') as f:
    #     proxy = f.read().split('\n')[0]
    # proxy = proxy.split('/')
    # proxy = 'http://' + proxy[1] + '@' + proxy[0]
    # # print(proxy)
    # proxies = {
    #     "http": "{}".format(proxy),
    #     "https": "{}".format(proxy),
    # }
    # print(proxies)
    # query_url = "https://ip.cn/"

    proxies = {"http": "http://127.0.0.1:4411",
               "https": "http://127.0.0.1:4411"}

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "cache-control": "max-age=0",
        "cookie": "CGIC=InZ0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIz; SID=egcH1VZpWZkibR69sIMbs9GZe7XKcOo4tKtS8WC7nmgFwpYV9hdv3U8KsDTruuJLzLrsuw.; HSID=Awn4tZePkrS1NwHue; SSID=AaXD7RA3ZoqP3FI33; APISID=BbLfpSb-v0BmtcBA/ATfZUKUkz2Pzde3Wx; SAPISID=CAz8i45ehOhljiHB/A2--fHk52fABS6A6H; ANID=AHWqTUmDZRGO0kmRtP8BrENPt_9OqhyvaKixu0r2NCtQvX2k8-3iORfwAURDTFsz; NID=186=cnKsOgrQ7z37Kz5tZYAlOFlvwQVDJgsdbbnaXdke0yyINeMaEjQD2Sbc3_dh9ARIAXuc0DOj6wA9WUDejjePilbXBEJzFYCVY6y5y2F49jeRO9s7czEHM2rfNtvhNStXtwgNkyUlWempIIGlMChe7QK2VX-FXJLRhFFRiibfpenk2BD6pXo4EVuxyf5N9RdONOUgu48vJ5Cv5bxtC0LN9JCQ1XUH-h5LmxUUrUwD5aDCqC90OMqJXdhx_JXr7ds-ZGeWvGlbgIWOFAlxhuyt7NEizx0aWC7Ra4Ao0boue6NVrUax-arl; DV=M0hCY7MiiJkZUHFnxQKTMX_Pr2yOuBY; 1P_JAR=2019-6-24-9; SIDCC=AN0-TYtOTujiI9ZLPBKCfVUorducNgXoEEW5oQyq9thZI-P31xK7J-Tzv3z7hMaXMVtZuAB3eg",
        "referer": "https://www.google.com/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "x-client-data": "CIy2yQEIprbJAQjEtskBCKmdygEIu5/KAQioo8oBCLGnygEI4qjKAQjxqcoBCJKqygE=",
        "Host": "www.google.com",
    }

    retry_num = 1
    text = ""
    response = ""
    status = ""
    # with open("status.txt", 'w', encoding="utf-8") as w:
    #     w.write('\n-----------------------------\n')

    while retry_num < 5:

        print("\n----------------------")
        print(retry_num)
        try:
            response = requests.get(query_url, headers=headers, timeout=10, proxies=proxies,
                                    allow_redirects=False, verify=True)
        except:
            pass



        if response:
            # print(response.headers)
            # response.encoding = "utf-8"
            response.encoding = "utf-8"
            text = response.text
            # text.encode("utf-8")
            # print(text)

            # content = response.content
            # charset = cchardet.detect(content)
            # print(charset)
            # text = content.decode(charset['encoding'])
            # print(text)
            # content = response.content
            # content =content.decode(encoding='utf8',errors='ignore')
            # print(content)
            print(response.status_code)

            if re.search('id="search"', text):
                status = "ok"
                print("ok")
                print(len(text))
                break
            else:
                status = "not ok"
                print("not ok")


        # with open("status.txt", 'a+', encoding="utf-8") as w:
        #     w.write('\n次数：{}'.format(retry_num))
        #     w.write('\n状态：{}'.format(status))
        #     w.write('\n字数：{}'.format(len(text)))
        #     w.write('\n-----------------------------\n')

        retry_num += 1


    with open(result_file_name, 'w', encoding="utf-8") as w:
        if text:
            w.write(text)
        w.write(text)



if __name__ == '__main__':
    # query_url = "https://www.google.com/search?q=%E9%A6%99%E6%B8%AF&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwik2vuw34HjAhWLxrwKHdnJBy8QpwUIIA&biw=1736&bih=859&dpr=1"
    # query_url = "https://www.google.com/search?tbm=nws&q=%E9%A6%99%E6%B8%AF&tbs=sbd:1"
    # result_file_name = "google_result.html"

    google_news_search(sys.argv[1], sys.argv[2])
    # google_news_search(query_url, result_file_name)