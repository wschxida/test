#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : flask_video.py
# @Author: Cedar
# @Date  : 2020/3/17
# @Desc  :


from flask import Flask


app = Flask(__name__)


@app.route('/wsc_video', methods=['GET', 'GET'])
def home():
    return '''
    <html>
    <head>
    <meta name="viewport" content="width=device-width"></head>
    <body>
    <video controls="" autoplay="" name="media">
    <source src="file:///D:/youtube-dl/%E5%AF%B0%E5%AE%87%E5%85%A8%E8%A6%96%E7%95%8C20200311%E3%80%90%E5%AE%8C%E6%95%B4%E7%89%88%E3%80%91%EF%BD%9C%E6%B2%99%E4%BF%84%E6%B2%B9%E5%83%B9%E9%AC%A7%E7%BF%BB%E9%83%BD%E6%98%AF%E5%81%87%20%E5%90%84%E6%87%B7%E9%AC%BC%E8%83%8E%E6%89%93%E8%80%81%E7%BE%8E%E6%98%AF%E7%9C%9F%E3%80%80%E7%BE%8E%E8%82%A1%E5%B4%A9%E7%89%9B%E8%BD%89%E7%86%8A%E6%B5%B7%E5%98%AF%E4%BE%86%20%20%E7%BE%8E%E4%BC%81%E8%8B%A6%E6%92%90%E7%9B%BC%E8%A7%A3%E7%A6%81%E8%8F%AF%E7%82%BA.mp4" type="video/mp4">
    </video></body></html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
