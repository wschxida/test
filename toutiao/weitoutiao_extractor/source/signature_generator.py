from selenium import webdriver
from functools import wraps
import os

dirname = os.path.abspath(os.path.dirname(__file__))


def try_execute_action(f):
    # 所有动作在执行时都有可能会报错，在此函数统一处理
    @wraps(f)
    def warp(self, *args, **kwargs):
        try:
            result = f(self, *args, **kwargs)
            # print('执行%s成功' % f.__name__)
            return result
        except:
            # print(traceback.format_exc())
            print('执行%s失败' % f.__name__)
            return False

    return warp


class SignatureGenerator:

    def __init__(self, website_no, keyword_list, source_html_file_name=None, temp_html_file_name=None):
        options = webdriver.ChromeOptions()
        webdriver_file = self.get_webdriver()
        self.output_task_path = os.path.abspath(os.path.join(dirname, '../temp'))
        self.task_file_name = f'task_{website_no}.txt'
        self.task_file = os.path.join(dirname, self.output_task_path, f'./{self.task_file_name}')
        self.keyword_list = keyword_list
        self.source_html_file_name = source_html_file_name or os.path.join(dirname, '../input/html/toutiao.html')
        self.temp_html_file_name = temp_html_file_name or os.path.join(dirname, '../input/html/temp.html')
        self.list_page_next_page_max_count = 10
        # 每次启动前先删除之前的任务文件
        if os.path.isfile(self.task_file):
            os.remove(self.task_file)

        # 设置下载路径，用于渲染页面时将任务文件下载到指定路径
        prefs = {"download.default_directory": self.output_task_path}
        options.add_experimental_option("prefs", prefs)
        self.chrome_webdriver = webdriver.Chrome(executable_path=webdriver_file, chrome_options=options)

    def run(self):
        '''批量生成带_signature 的url'''
        task_file_path = self.write_keyword_to_html(self.keyword_list, self.source_html_file_name,
                                                    self.temp_html_file_name, self.task_file_name,
                                                    self.list_page_next_page_max_count)
        file_path = f'file:/{task_file_path}'

        self.chrome_webdriver.get(file_path)
        return self.task_file

    @staticmethod
    def write_keyword_to_html(keyword_list, source_html_file_name, temp_html_file_name, task_file_name,
                              list_page_next_page_max_count=10):
        # 将keyword_list逐一写入html中，并加入将url生成_signature的代码，输出到task_file_name
        html_file_absolute_path = os.path.abspath(os.path.join(dirname, source_html_file_name))

        with open(html_file_absolute_path, 'r', encoding='utf8') as f:
            source_html = f.read()

        replace_source_html_content = '''document.cookie = "_signature=" + e.sign({
                                    url: encodeURI(location.href)
                                })'''

        replace_target_html_content = '''function test(){
                                var req_url_html = "";
                                var keyword_list = %s;
                                var next_page_max_count = %s;
                                var url_format_prefix = "https://so.toutiao.com/search/?keyword=";
                                var url_format_suffix = "&pd=weitoutiao&source=search_subtab_switch&original_source=&in_ogs=&from=weitoutiao&format=json&count=10&offset=";
                                for(var i = 0; i <keyword_list.length; i++){
                                    for(var j=0;j < next_page_max_count; j++){
                                        var req_url = url_format_prefix+ keyword_list[i] + url_format_suffix + (j+1) *10*2;
                                        var _signature = e.sign({url: encodeURI(req_url)});
                                        var req_url = req_url + '&_signature=' + _signature;
                                        var req_url_html = req_url_html + req_url + "\\n";
                                        }
                                    };
                                var blob = new Blob([req_url_html], {type: "text/plain;charset=utf-8"});
                                saveAs(blob, "%s");
                            }()''' % (keyword_list, list_page_next_page_max_count, task_file_name)
        temp_html_content = source_html.replace(replace_source_html_content, replace_target_html_content)
        with open(temp_html_file_name, 'w', encoding='utf8') as f:
            f.write(temp_html_content)

        return temp_html_file_name

    @try_execute_action
    def open_page(self, html_file):
        self.chrome_webdriver.get(html_file)

    @staticmethod
    def get_webdriver():
        '''识别本地chrome浏览器版本并下载相关chrome_driver'''
        return '../input/chromedriver.exe'


if __name__ == '__main__':
    pass
