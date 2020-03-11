# encoding=utf-8

import platform
import os
import time
import json
import html
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from service_app.model.base.base_page_agent import BasePageAgent


driver = None
old_height = 0
curpath = os.path.dirname(os.path.realpath(__file__))

# =============================================================================


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


# helper function: used to scroll the page
def scroll(total_scrolls=5, scroll_time=10):
    global old_height
    current_scrolls = 0
    total_scrolls = int(total_scrolls)

    while True:
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
            WebDriverWait(driver, scroll_time, 5).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return


def start_selenium(url, user_data_dir):
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
    # 取一个chrome user-data-dir目录，每个目录的Chromedriver是互相隔开的，登录不同的账号
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.add_argument(r"user-data-dir=" + user_data_dir)
    print(user_data_dir)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            chromedriver_path = os.path.join(curpath, "chromedriver")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        else:
            chromedriver_path = os.path.join(curpath, "chromedriver.exe")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    except:
        print("Kindly replace the Chrome Web Driver with the latest one from"
              "http://chromedriver.chromium.org/downloads"
              "\nYour OS: {}".format(platform_)
              )

    driver.set_page_load_timeout(60)   # 设置页面加载超时
    driver.set_script_timeout(60)   # 设置页面异步js执行超时
    driver.maximize_window()

    # 先走Facebook首页，再滑动一下，模拟人工操作
    driver.get("https://www.facebook.com/")
    time.sleep(1)
    scroll(1)
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    # 如果发现没登录，就退出
    try:
        is_not_login = driver.find_element_by_name('email')
        if is_not_login:
            return "NotLogin"
        #     email = eval(facebook_email_password[index])["email"]
        #     password = eval(facebook_email_password[index])["password"]
        #     print(email)
        #     login(email, password)
        #     driver.get(url)
    except Exception as e:
        return None


def login(email, password):
    """ Logging into our own profile """

    driver.get("https://en-gb.facebook.com")
    driver.maximize_window()

    # filling the form
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('pass').send_keys(password)

    # clicking on login button
    try:
        driver.find_element_by_name('login').click()
    except Exception as e:
        pass

    try:
        driver.find_element_by_id('loginbutton').click()
    except Exception as e:
        pass


def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("/"))[-1].split("?")[0])
    elif url.find("_tab") != -1:
        original_link = "https://en-gb.facebook.com/" + (url.split("?")[0]).split("/")[-1]
    else:
        original_link = url

    return original_link


def get_middle_str(content, start_str, end_str):
    """通用函数，获取前后两个字符串中间的内容"""
    try:
        start_index = content.index(start_str)
        if start_index >= 0:
            start_index += len(start_str)
        content = content[start_index:]
        end_index = content.index(end_str)
        return content[:end_index]
    except Exception as e:
        print(e)


def get_author_id(content):
    user_id = get_middle_str(content, '"entity_id":"', '"')
    page_id = get_middle_str(content, '"pageID":"', '"')

    if user_id:
        author_id = user_id
    else:
        author_id = page_id

    return author_id


def get_author_account(content):
    user_account = get_middle_str(content, '"uri":"', '"')
    page_account = get_middle_str(content, '"username":"', '"')
    print(user_account)

    if page_account:
        author_account = page_account

    else:
        user_account = user_account + "#"
        author_account = get_middle_str(user_account, 'facebook.com\/', '#')
        if not author_account.find("profile.php") == -1:
            author_account = ''

    return author_account


def get_author_name(content):
    user_name = get_middle_str(content, '<title id="pageTitle">', '</title>')
    page_name = get_middle_str(content, '"pageName":"', '"')

    if user_name:
        author_name = user_name
    else:
        author_name = page_name

    return author_name


def get_author_profile_image(driver):
    try:
        user_profile_image = driver.find_elements_by_xpath('//a[contains(@class,"profilePicThumb")]/img')
        page_profile_image = driver.find_elements_by_xpath('//a[contains(@aria-label,"Profile picture")]/div/img')

        if user_profile_image:
            author_profile_image = user_profile_image[0].get_attribute('src')
        else:
            author_profile_image = page_profile_image[0].get_attribute('src')

        return author_profile_image
    except:
        pass


class FacebookAgent(BasePageAgent):
    """
    facebook类，获取profile，message, friend
    调用get_page_content_by_request可根据page_type返回相应结果
    """

    def __init__(self, params):
        BasePageAgent.__init__(self, params)
        # 调用get方法，然后获取配置的数据
        self.profile_url_pattern = self.config.get("facebook", "profile_url_pattern")
        self.message_url_pattern = self.config.get("facebook", "message_url_pattern")
        self.friend_url_pattern = self.config.get("facebook", "friend_url_pattern")
        self.user_data_dir_list = self.config.get("chromedriver", "user_data_dir")
        # 转成list
        if self.user_data_dir_list:
            self.user_data_dir_list = self.user_data_dir_list.split("||")

        # 选取一个user—data-dir，确定是没有正在使用的
        self.user_data_dir_selected = ""
        # 先读取记录正在使用的user—data-dir的文件
        fl = open(curpath + '\\user_data_dir_cache.txt', 'r', encoding='utf-8')
        user_data_dir_cache = fl.read()
        if len(user_data_dir_cache) == 0:
            user_data_dir_cache = "[]"
        user_data_dir_cache = json.loads(user_data_dir_cache)
        fl.close()

        # 选一个不在cache里的
        for data_dir in self.user_data_dir_list:
            if data_dir not in user_data_dir_cache:
                self.user_data_dir_selected = data_dir
                user_data_dir_cache.append(self.user_data_dir_selected)
                break

        # 写入cache，表示正在使用
        fl = open(curpath + '\\user_data_dir_cache.txt', 'w', encoding='utf-8')
        fl.write(json.dumps(user_data_dir_cache))
        fl.close()

        print('----------FB-----------')
        print(self.__dict__)
        print('==========FB===========')

    def get_page_content(self):
        # 如果user_data_dir全被占用，则直接返回提示
        if not self.user_data_dir_selected:
            return "No user_data_dir available！"

        result = ''
        if self.page_type == 'profile':
            result = self.get_page_content_profile()
        if self.page_type == 'message':
            result = self.get_page_content_message()
        if self.page_type == 'friend':
            result = self.get_page_content_friend()

        # 释放使用的目录，写入cache
        fl = open(curpath + '\\user_data_dir_cache.txt', 'r+', encoding='utf-8')
        user_data_dir_cache = fl.read()
        if len(user_data_dir_cache) == 0:
            user_data_dir_cache = "[]"
        user_data_dir_cache = json.loads(user_data_dir_cache)
        user_data_dir_cache.remove(self.user_data_dir_selected)
        fl.seek(0)
        fl.truncate()   # 清空文件
        fl.write(json.dumps(user_data_dir_cache))
        fl.close()

        return result

    def get_page_content_message(self):
        url = self.message_url_pattern.format(self.target_express)
        # url = "https://www.qq.com/"
        try:
            login_status = start_selenium(url, self.user_data_dir_selected)
            if login_status:
                # 没登录的时候，page可以继续采，所以这里不退出
                print(login_status)
            scroll(self.page_count)
            time.sleep(5)
            page_source = driver.page_source
            driver.close()
            return page_source

        except Exception as e:
            print(e)
            driver.close()
            return "fetch failed!"

    def get_page_content_profile(self):
        url = self.profile_url_pattern.format(self.target_express)
        try:
            login_status = start_selenium(url, self.user_data_dir_selected)
            if login_status:
                # 没登录的时候，page可以继续采，所以这里不退出
                print(login_status)
            page_source = driver.page_source
            author_id = get_author_id(page_source)
            author_account = get_author_account(page_source)
            author_name = get_author_name(page_source)
            author_profile_image = get_author_profile_image(driver)
            about = {}
            url = driver.current_url
            url = create_original_link(url)
            print("\nScraping:", url)
            print("----------------------------------------")
            # 如果是page，只返回page_about
            page_id = get_middle_str(page_source, '"pageID":"', '"')
            if page_id:
                page_url = url + "/about/"
                try:
                    driver.get(page_url)
                    time.sleep(5)
                    data = driver.find_elements_by_xpath('//*[contains(@id,"PagesProfileAboutInfoPagelet")]')
                    about["page_about"] = data[0].get_attribute('innerHTML')

                except Exception as e:
                    print(e)
            # ---------------------------------------------------------------------------------------------------------
            # user获取的profile
            if not page_id:
                scan_list = ["education", "living", "overview", "bio", "contact_info", "relationship", "year_overviews"]
                section = ["/about?section=education", "/about?section=living", "/about?section=overview",
                           "/about?section=bio", "/about?section=contact-info", "/about?section=relationship",
                           "/about?section=year-overviews"]
                # =====WSC: modify xpath=========
                elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 7
                page = []
                for i in range(len(section)):
                    page.append(url + section[i])

                for i in range(len(page)):
                    try:
                        driver.get(page[i])
                        time.sleep(5)
                        data = driver.find_elements_by_xpath(elements_path[i])
                        about[scan_list[i]] = data[0].get_attribute('innerHTML')

                    except Exception as e:
                        print(e)

            driver.close()
            about_result = {"author_id": author_id, "author_account": author_account, "author_name": author_name,
                            "author_profile_image": author_profile_image, "about": about}
            result = json.dumps(about_result, ensure_ascii=False)
            # 再进行html编码，这样最终flask输出才是合法的json
            html_result = html.escape(result)
            print("About Section Done")
            return html_result

        except Exception as e:
            print(e)
            driver.close()
            return "fetch failed!"

    def get_page_content_friend(self):
        url = self.friend_url_pattern.format(self.target_express)
        try:
            login_status = start_selenium(url, self.user_data_dir_selected)
            if login_status:
                # 没登录的时候，friend没法采集，这里直接退出
                print(login_status)
                friend_result = {"author_id": "", "friend_list": {}, "status_message": "Not Login!"}
                result = json.dumps(friend_result, ensure_ascii=False)
                driver.close()
                return result

            page_source = driver.page_source
            author_id = get_author_id(page_source)
            # 如果是page，就返回空
            page_id = get_middle_str(page_source, '"pageID":"', '"')
            if page_id:
                friend_result = {"author_id": author_id, "friend_list": {}, "status_message": "It's Page. No friends."}
                result = json.dumps(friend_result, ensure_ascii=False)
                driver.close()
                return result

            url = driver.current_url
            url = create_original_link(url)
            print("\nScraping:", url)
            print("----------------------------------------")
            print("Friends..")
            # 暂时只获取前面三个，避免封号
            # scan_list = ["All", "Following", "Followers", "Work", "College", "Current City", "Hometown"]
            # section = ["/friends", "/following", "/followers", "/friends_work", "/friends_college",
            #            "/friends_current_city", "/friends_hometown"]
            scan_list = ["All", "Following", "Followers"]
            section = ["/friends", "/following", "/followers"]
            # =====WSC: modify xpath=========
            elements_path = ["//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[@id='pagelet_collections_following']/ul/li",
                             "//*[contains(@class,'fbProfileBrowserListItem')]/div/a",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li"]
            # 结果键不要出现空格，采集软件不支持，Current City-->CurrentCity
            friend_list = {"All": [], "Following": [], "Followers": [], "Work": [], "College": [], "CurrentCity": [],
                           "Hometown": []}
            no_friends_to_show = 0

            page = []
            for i in range(len(section)):
                page.append(url + section[i])

            for i in range(len(page)):
                try:
                    driver.get(page[i])
                    time.sleep(10)
                    # 获取朋友栏目名，如果节点不存在，说明是no_friends_to_show,退出循环
                    try:
                        sections_bar = driver.find_element_by_xpath("//*[@class='_3cz'][1]/div[2]/div[1]")
                    except Exception as e:
                        no_friends_to_show = 1
                        break

                    # 如果有栏目，但是当前栏目如follower不存在，则继续下一个栏目采集
                    if sections_bar.text.find(scan_list[i]) == -1:
                        continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # 暂时不要翻页，防止封号
                    # scroll(self.page_count)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    data = driver.find_elements_by_xpath(elements_path[i])
                    results = [x for x in data]

                    for j in range(len(results)):
                        # friend_author_id
                        friend_author_id_element = results[j].find_element_by_xpath(
                            ".//a[contains(@data-hovercard,'/ajax/hovercard/user.php?id=') and contains(@data-gt,'engagement')]")
                        friend_author_id = \
                            friend_author_id_element.get_attribute("data-hovercard").split("user.php?id=")[1].split(
                                "&")[0]
                        # friend_author_name
                        friend_author_name_element = results[j].find_element_by_xpath(
                            ".//a[contains(@data-hovercard,'/ajax/hovercard/user.php?id=') and contains(@data-gt,'engagement')]")
                        friend_author_name = friend_author_name_element.text
                        # friend_author_url
                        friend_author_url_element = results[j].find_element_by_xpath("./div/a")
                        friend_author_url = friend_author_url_element.get_attribute("href")
                        friend_author_url = friend_author_url.replace(
                            "&fref=profile_friend_list&hc_location=friends_tab",
                            "")
                        friend_author_url = friend_author_url.replace(
                            "?fref=profile_friend_list&hc_location=friends_tab",
                            "")
                        # img_url
                        friend_img_url_element = results[j].find_element_by_xpath("./div/a/img")
                        friend_img_url = friend_img_url_element.get_attribute("src")

                        item = {"author_id": friend_author_id, "author_name": friend_author_name,
                                "author_url": friend_author_url, "author_img_url": friend_img_url}
                        # 结果键不要出现空格，采集软件不支持，Current City-->CurrentCity
                        friend_result_key = scan_list[i].replace(' ', '')
                        friend_list[friend_result_key].append(item)

                except Exception as e:
                    print(e)

            driver.close()
            if no_friends_to_show:
                friend_result = {"author_id": author_id, "friend_list": friend_list,
                                 "status_message": "no friends to show"}
            else:
                friend_result = {"author_id": author_id, "friend_list": friend_list,
                                 "status_message": "success"}
            result = json.dumps(friend_result, ensure_ascii=False)
            # print(result)
            print("Friends Done")
            return result

        except Exception as e:
            print(e)
            driver.close()
            return "fetch failed!"


# =============================================================================

def main():

    params = {
        'page_type': 'message',
        'target_account': 'DonaldTrump',
    }
    result = FacebookAgent(params).get_page_content()
    print(result)


if __name__ == '__main__':
    main()
