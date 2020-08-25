import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def __init__(self):
    """打开浏览器"""



def get_data(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # browser = webdriver.Chrome(options=chrome_options)
        # browser.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(options=chrome_options)
        browser.implicitly_wait(30)  # 隐性等待，最长等30秒
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