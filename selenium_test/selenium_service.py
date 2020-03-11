# encoding=utf-8

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


driver = None
user_data_dir_list = [
    'E:\\selenium\\AutomationProfile1',
    'E:\\selenium\\AutomationProfile2',
    'E:\\selenium\\AutomationProfile3',
    'E:\\selenium\\AutomationProfile4',
    'E:\\selenium\\AutomationProfile5',
]

# =============================================================================


def start_selenium():
    global driver

    options = Options()

    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    # options.add_argument('--headless')  # 浏览器不提供可视化页面
    # twitter下面这个参数会导致登录退出
    # options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument("allow-file-access-from-files")
    # options.add_argument("use-fake-device-for-media-stream")
    # options.add_argument("use-fake-ui-for-media-stream")
    # options.add_argument("use-file-for-fake-audio-capture=C:\\PATH\\TO\\WAV\\xxx.wav")
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
    # 随机取一个chromedriver目录，每个目录的Chromedriver是互相隔开的，登录不同的账号，每次启动随机分配

    dir_selected = ""
    fl = open('user_data_dir_cache.txt', 'r', encoding='utf-8')
    user_data_dir_cache = fl.read()
    print(len(user_data_dir_cache))
    print(user_data_dir_cache)
    if len(user_data_dir_cache) == 0:
        user_data_dir_cache = "[]"
    user_data_dir_cache = json.loads(user_data_dir_cache)
    print(user_data_dir_cache)
    fl.close()

    for data_dir in user_data_dir_list:
        if data_dir not in user_data_dir_cache:
            dir_selected = data_dir
            user_data_dir_cache.append(dir_selected)
            break

    fl = open('user_data_dir_cache.txt', 'w', encoding='utf-8')
    json.dumps(user_data_dir_cache)
    fl.write(json.dumps(user_data_dir_cache))
    fl.close()
    if dir_selected:
        print(dir_selected)
        user_data_dir_arg = r"user-data-dir=" + dir_selected
        options.add_argument(user_data_dir_arg)

    try:
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    except:
        pass

    driver.set_page_load_timeout(60)   # 设置页面加载超时
    driver.set_script_timeout(60)   # 设置页面异步js执行超时
    driver.maximize_window()

    # 先走Facebook首页，再滑动一下，模拟人工操作
    driver.get("https://www.qq.com/")
    time.sleep(10)
    page = driver.page_source
    driver.close()
    return page


if __name__ == '__main__':
    start_selenium()
