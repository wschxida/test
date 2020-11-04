import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def __init__(self):
    """打开浏览器"""


def get_data(url):
    try:
        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        options.add_argument('--headless')  # 浏览器不提供可视化页面
        # twitter下面这个参数会导致登录退出
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_argument('--audio-output-channels=0')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-sync')
        # options.add_argument("--disable-javascript")    # 禁用JavaScript
        options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        options.add_argument('--no-sandbox')  # 以最高权限运行,解决DevToolsActivePort文件不存在的报错
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏window.navigator.webdriver

        # options.add_argument('--window-size=1920,1080')

        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(60)  # 隐性等待，最长等30秒
        browser.set_page_load_timeout(60)  # 设置页面加载超时
        browser.set_script_timeout(60)  # 设置页面异步js执行超时
        browser.get(url)
        # time.sleep(5)
        page_html = browser.page_source
        browser.quit()
        return page_html
    except Exception as e:
        print("There's some error.")
        print(sys.exc_info()[0])
        sys.exit()


if __name__ == '__main__':
    url = sys.argv[1]
    # url = 'https://twitter.com/omaakatugba'
    # url = "http://www.webscraping.cn/"
    page_html = get_data(url)
    # print(page_html)
    file_name = sys.argv[2]
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(page_html)
