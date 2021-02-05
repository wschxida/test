import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
browser.implicitly_wait(40)
browser.get("https://h5.ele.me/login/")

time.sleep(20)
browser.close()
