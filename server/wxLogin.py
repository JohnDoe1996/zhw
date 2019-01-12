import json
import uuid
import requests
from tornado.web import RequestHandler
from db import Session,User

class LoginHandler(RequestHandler):  # 微信登录类

    def post(self): # post请求
        js_code = self.get_argument('js_code') # 得到code
        # 这里是换取用户的信息
        user_info = get_user_info(js_code=js_code) # 换取用户信息
        openid = '_' + user_info['openid'] # 提取用户信息中的openID
        user_uuid = str(uuid.uuid4())  # 暴露给小程序端的用户标示
        # 微信小程序不能设置cookie，把用户信息存在了 headers 中
        self.set_header('Authorization', user_uuid)
        # 存储用户信息
        try:
            session = Session()
            session.add(User(open_id=openid))  # 用户信息宝传到数据库user表
            session.commit()
        except: pass
        ret = {'openId': openid}
        self.write(json.dumps(ret, ensure_ascii=False)) # 返回openID到小程序


def get_user_info(js_code):
    req_params = {
        "appid": 'wxbc3d3d801035d3fd',  # 小程序的 ID
        "secret": 'd64748d0461d2cc6d2b91c47f9fc536b',  # 小程序的 secret
        "js_code": js_code,
        "grant_type": 'authorization_code'
    }
    req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                              params=req_params, timeout=3)  # 请求微信服务器换取用户信息
    return req_result.json()
