import os


def get_signature(_url):
    signature = os.popen(r'node get_sign_1.js {}'.format(url)).read()
    # r'{url}'.format(url='"'+url+'"')).read()
    return "&_signature=" + signature.replace('\n', '').replace(' ', '')


if __name__ == '__main__':
    url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=1232&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1616059291384&'
    signature = get_signature(url)
    url +=signature
    print(url)
