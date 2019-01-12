import json
from tornado.web import RequestHandler

from db import Session,User,Bill

class UserHandler(RequestHandler):  # 用户类

    def post(self, act):
        open_id = self.get_argument('open_id') # 得到openID
        if act == "balance": # 查询余额
            ret = getBalance(open_id)
        elif act == "charge": # 充值
            money = self.get_argument('money')
            ret = chargeBalance(open_id,money)
        elif act == "withdraw": # 提现
            money = self.get_argument('money')
            ret = withdrawBalance(open_id,money)
        else:
            ret = resultTemple(code=1,data="动作不存在")
        self.write(ret)



def resultTemple(code, data):  # 返回信息转json
    ret = {
        'code': code,
        'data': data
    }
    return json.dumps(ret,ensure_ascii=False)


def getBalance(open_id): # 查余额函数
    session = Session()
    res = session.query(User.balance).filter(User.open_id == open_id).all()
    # 数据库查找余额 SELECT balance FROM users WHERE open_id = open_id
    if len(res) == 0: # 查找到的数据长度为0，则用户不存在
        ret = resultTemple(1,"用户不存在")
    else:
        balance = str(res[0][0]) # 取出第0个数据则为余额转成string类型
        data = { 'balance': balance }
        ret = resultTemple(0,data)
    return ret

def chargeBalance(open_id,money): # 充值函数
    session = Session()
    res = session.query(User.balance).filter(User.open_id == open_id).all()
    # 数据库查找余额 SELECT balance FROM users WHERE open_id = open_id
    if float(money) <= 0:
        ret = resultTemple(1, "金额有误")
    elif len(res) == 0:
        ret = resultTemple(1,"用户不存在")
    else:
        before = float(res[0][0]) # 余额转成float类型
        change = float(money) # 充值金额转成float类型
        after = before + change # 充值后的金额
        session.add(Bill(user=open_id,to=open_id,act="charge",before=before,after=after,change=change))
        # 数据库添加一个账单记录 INSERT INTO bills (user,to,act,before,after,change)VALUES(open_id,open_id,'charge',before,after,change)
        session.query(User).filter(User.open_id == open_id).update({"balance":after})
        # 数据库更新语句，更新用户余额 UPDATE users SET balance=after WHERE open_id=open_id
        session.commit()
        ret = resultTemple(0,"充值成功")
    return ret

def withdrawBalance(open_id,money): # 提现函数
    session = Session()
    res = session.query(User.balance).filter(User.open_id == open_id).all()
    # 数据库查找余额 SELECT balance FROM users WHERE open_id = open_id
    if float(money) <= 0:
        ret = resultTemple(1, "金额有误")
    elif len(res) == 0:
        ret = resultTemple(1, "用户不存在")
    else:
        before = float(res[0][0]) # 余额转成float类型
        change = float(money) # 充值金额转成float类型
        after = before - change # 提现后的金额
        if after < 0 : # 如果提现后金额少于0，则提现失败并提示余额不足
            ret = resultTemple(1,"余额不足")
        else: # 提现成功
            session.add(Bill(user=open_id, to=open_id, act="withdraw", before=before, after=after, change=change))
            # 账单添加 INSERT INTO bills (user,to,act,before,after,change)VALUES(open_id,open_id,'withdraw',before,after,change)
            session.query(User).filter(User.open_id == open_id).update({"balance": after})
            # 数据库更新语句，更新用户余额 UPDATE users SET balance=after WHERE open_id=open_id
            session.commit()
            ret = resultTemple(0, "提现成功")
    return ret
