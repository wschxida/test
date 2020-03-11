# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options

import time


# 创建chrome浏览器驱动，无头模式（超爽）
chrome_options = Options()
chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome(executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')


# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
driver.get("https://story.snapchat.com/s/neha.malik335")



# 获取新的页面快照
driver.save_screenshot("snapchat.png")
time.sleep(7)

for i in range(1,10):

    while 1:
        start = time.clock()
        try:
            driver.find_element_by_xpath('//*[@id="root"]//video')
            print("已定位到元素")
            end = time.clock()
            break
        except:
            pass
            # print("还未定位到元素!")


    video = driver.find_element_by_xpath('//*[@id="root"]//video')
    video_url = video.get_property("src")
    print(video_url)
    time.sleep(5)




# 关闭浏览器
driver.quit()
