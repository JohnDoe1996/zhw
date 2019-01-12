import datetime
import json
from tornado.websocket import WebSocketHandler
import bill


class WsHandler(WebSocketHandler):  # websocket类

    users = set()  # 用来存放在线用户的容器

    def open(self, info, id): # 当用户连接上调用
        self.id = str(id) # 获取用户ID
        self.info = str(info) # 获取用户类型shop or user
        self.users.add(self)  # 建立连接后添加用户到容器中
        msg = "id:[%s] ip:[%s] time:[%s]" % \
              (self.id, self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("A [%s] connected %s" % ( self.info, msg)) # 控制台显示由用户加入

    def on_message(self, message): # 用户发送消息的时候调用
        msgData = json.loads(message) # json格式消息转换成字典类型数据
        print(msgData)
        if  msgData['act'] == "buy": # 当为购买操作的时候
            result,m = bill.buy(self.id,msgData['id'],msgData['num'])  # 调用bill类里面的购买方法
            if result: # 购买成功
                ret = {
                    'host': "zhw",
                    'act': "unlock",
                    'id': msgData['id'],
                    'num': msgData['num'],
                }
                for u in self.users: # 查找编号为id的shop
                    if "shop" == u.info and msgData['id'] == u.id:
                        u.write_message(json.dumps(ret,ensure_ascii=False)) # 给对应的shop发送开箱信息
                        ret={
                            'code': 0,
                            'data': "开箱成功，使用后请记得关箱门"
                        }
                        self.write_message(json.dumps(ret,ensure_ascii=False)) # 发送给发起者开箱成功
            else: # 购买失败
                ret = {
                    'code': 1,
                    'data':  m
                }
                self.write_message(json.dumps(ret,ensure_ascii=False)) # 告诉发起者，购买失败的原因
        elif msgData['act'] == 'sell': # 当出售操作
            result = bill.sell(self.id,msgData['id'],msgData['num'],msgData['price']) # 调用bill类里面的出售方法
            if result: # 出售成功
                ret = {
                    'host': "zhw",
                    'act': "unlock",
                    'id': msgData['id'],
                    'num': msgData['num'],
                }
                for u in self.users: # 查找编号为id的shop
                    if "shop" == u.info and msgData['id'] == u.id:
                        u.write_message(json.dumps(ret,ensure_ascii=False)) # 给对应的shop发送开箱信息
                        ret={
                            'code': 0,
                            'data': "开箱成功，使用后请记得关箱门"
                        }
                        self.write_message(json.dumps(ret,ensure_ascii=False)) # 告诉发起者，购买失败的原因
            else: # 出售失败
                ret = {
                    'code': 1,
                    'data': "操作失败"
                }
                self.write_message(json.dumps(ret,ensure_ascii=False)) # 告诉发起者，出售失败的原因
        elif msgData['act'] == 'back': # 当开箱后返回信息
            print(msgData)
        else: #都不是
            ret = {
                'code': 1,
                'data': "响应错误"
            }
            self.write_message(json.dumps(ret,ensure_ascii=False))

    def on_close(self):  # 用户下线
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        msg = "id:[%s] ip:[%s] time:[%s]" % \
              (self.id, self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("A [%s] left %s" % (self.info, msg))  # 控制带打印有用户下线

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求