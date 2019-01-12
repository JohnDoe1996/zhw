import json
from tornado.web import RequestHandler
from sqlalchemy import and_
from db import Session,Shop

class ShopHandler(RequestHandler): # 商店类

    def post(self, act):
        id = self.get_argument('id') # 得到要操作的商品柜的ID
        num = self.get_argument('num') # 商品柜的序号
        state, price = checkShop(id, num) # 查询该商品柜的当前状态
        if state is None: # 状态为None，代表商品柜不存在
            ret = resultTemple(code=1,data="格子不存在")
        elif act == "buy": # 当购买
            if state == '': # 状态为空，代表商品柜处于空闲状态，没有东西可以购买
                ret = resultTemple(1,'格子处于空闲状态，里面没有可买的商品。')
            else: # 状态不空
                retData = {
                    'host':'zhw',
                    'act': "buy",
                    'num':num,
                    'id':id,
                    #'state':state,
                    'price':str(price)
                }
                ret = resultTemple(0,retData)  # 返回该商品柜的信息，包括价格
        elif act == "sell": # 当出售
            if state == '': # 状态为空闲
                retData = {
                    'host':'zhw',
                    'act': "sell",
                    'num':num,
                    'id':id,
                    #'state':state
                    'price': price
                }
                ret = resultTemple(0,retData) # 返回可以使用
            else: # 状态不为空，不能在此出售
                ret = resultTemple(1,'格子不是处于空闲状态。')
        else:
            ret = resultTemple(code=1,data="动作不存在")
        self.write(ret)


def resultTemple(code, data): # 返回模板
    ret = {
        'code': code,
        'data': data
    }
    return json.dumps(ret,ensure_ascii=False)

def checkShop(id,num): # 检查商品柜状态的函数
    session = Session()
    res = session.query(Shop).filter(and_(Shop.cabinet_num == id , Shop.grid_num == num)).all()
    #查找给商品柜 SELECT * FROM shops WHERE cabinet_num=id and Shop.grid_num=num
    if len(res) == 0: # 查找到的项为0，说明商品柜不存在，返回None
        state = None
        price = None
    else: # 存在则返回当前状态和价格
        state = res[0].state
        price = res[0].price
    return state, price