#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Cedar
# @Date  : 2021/5/13
# @Desc  :


from flask import Flask, g, jsonify
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_cors import CORS
import re


app = Flask(__name__)
CORS(app, supports_credentials=True)
auth = HTTPBasicAuth()
SECRET_KEY = "12345"


# 生成token, 有效时间为600min
def generate_auth_token(user_id, expiration=36000):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'user_id': user_id})


# 解析token
def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    # token正确
    try:
        data = s.loads(token)
        return data
    # token过期
    except SignatureExpired:
        return None
    # token错误
    except BadSignature:
        return None


# 连接数据库操作
def connect(user_id, password):
    auth_table = [('a', '1'), ('b', '2')]
    if (user_id, password) in auth_table:
        return user_id
    else:
        return None


# 验证token
@auth.verify_password
def verify_password(username, password):
    # 先验证token
    user_id = re.sub(r'^"|"$', '', username)
    user_id = verify_auth_token(user_id)
    # 如果token不存在，验证用户id与密码是否匹配
    if not user_id:
        user_id = connect(username, password)
        # 如果用户id与密码对应不上，返回False
        if not user_id:
            return False
    g.user_id = user_id
    return True


@app.route('/login')
@auth.login_required
def login():
    token = generate_auth_token(g.user_id)
    return jsonify({'token': token})


@app.route('/index')
@auth.login_required
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
