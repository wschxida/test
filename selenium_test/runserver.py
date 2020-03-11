#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : runserver.py.py
# @Author: Cedar
# @Date  : 2019/12/11
# @Desc  :


from flask_script import Manager, Shell
from flask import Flask
from selenium_service import start_selenium

# 创建项目对象
app = Flask(__name__)
manager = Manager(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return "1234"


@app.route('/service_app', methods=['GET', 'POST'])
def page_agent_service():
    try:
        return start_selenium()
    except Exception as e:
        print(e)


# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

# 以server形式运行
# start python runserver.py runserver --host 0.0.0.0 --port 5001
# start python runserver.py runserver --host 0.0.0.0 --port 5002
# start python runserver.py runserver --host 0.0.0.0 --port 5003
# start python runserver.py runserver --host 0.0.0.0 --port 5004
# start python runserver.py runserver --host 0.0.0.0 --port 5005

# start python runserver.py runserver --host 127.0.0.1 --port 5001
# start python runserver.py runserver --host 127.0.0.1 --port 5002
# start python runserver.py runserver --host 127.0.0.1 --port 5003
# start python runserver.py runserver --host 127.0.0.1 --port 5004
# start python runserver.py runserver --host 127.0.0.1 --port 5005
