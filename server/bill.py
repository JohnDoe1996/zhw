from tornado.web import RequestHandler
from db import Session,User,Shop,Bill
from sqlalchemy import and_,desc
import json


class BillHandler(RequestHandler): # 账单函数

    def post(self, act):
        open_id = self.get_argument('open_id') #得到openid
        if act == "all": # 查询所有账单
            ret = allBill(open_id)
        elif act == "bought": # 查询购买账单
            ret = oneBill(open_id, "buy")
        elif act == "sold": # 查询售出账单
            ret = oneBill(open_id, 'sell')
        elif act == "selling": #查询在售账单
            ret = sellingBill(open_id)
        else:
            ret = resultTemple(code=1,data="动作不存在")
        self.write(ret)


def resultTemple(code, data): # 返回模板
    ret = {
        'code': code,
        'data': data
    }
    return json.dumps(ret,ensure_ascii=False)

def oneBill(open_id, act): # 查询购买或者售出账单
    session = Session()
    res = session.query(Bill).filter(and_(Bill.user == open_id, Bill.act == act)).order_by(desc(Bill.act_at)).all()
    # 查询账单 SELECT * FROM bills WHERE user=open_id and act=act ORDER BY act_at DESC
    if len(res) == 0: # 查询不到返回空列表
        return resultTemple(0,[])
    else:
        lit = []
        for r in res: # 循环把数据加入到列表
            data = {
                'act': r.act,
                'time': str(r.act_at),
                'before': str(r.before),
                'after': str(r.after),
                'change': str(r.change)
            }
            lit.append(data)
        return resultTemple(0,lit) # 返回账单列表

def allBill(open_id):
    session = Session()
    res = session.query(Bill).filter(Bill.user == open_id).order_by(desc(Bill.act_at)).all()
    # 查询账单 SELECT * FROM bills WHERE user=open_id ORDER BY act_at DESC
    if len(res) == 0: # 查询不到返回空列表
        return resultTemple(0,[])
    else:
        lit = []
        for r in res: # 循环把数据加入到列表
            data = {
                'act': r.act,
                'time': str(r.act_at),
                'before': str(r.before),
                'after': str(r.after),
                'change': str(r.change)
            }
            lit.append(data)
        return resultTemple(0,lit)  # 返回账单列表

def sellingBill(open_id):  # 在售列表
    session = Session()
    res = session.query(Shop).filter(Shop.state == open_id).all()
    # 查询商品 SELECT * FROM shops WHERE state == open_id
    if len(res) == 0:  # 查询不到返回空列表
        return resultTemple(0,[])
    else:
        lit = []
        for r in res:  # 循环把数据加入到列表
            data = {
                'act': "selling",
                'id': r.cabinet_num,
                'num': r.grid_num,
                'price': str(r.price)
            }
            lit.append(data)
        return resultTemple(0,lit)  # 返回账单列表


def sell(open_id, id, num, price): # 售出调用此函数
    session = Session()
    try:
        session.query(Shop).filter(and_(Shop.cabinet_num == id, Shop.grid_num == num)).update({"state": open_id, "price": price})
        # 更新商品柜数据 UPDATE shops SET state=open_id WHERE cabinet_num=id and grid_num=num
        session.commit()
        return True
    except Exception as  e:
        print(e)
        return False

def buy(open_id, id, num):  # 购买调用此函数
    session = Session()
    res = session.query(User.balance).filter(User.open_id == open_id).all()
    # 查询余额 SELECT balance FROM users WHERE open_id = open_id
    balance = float(res[0][0]) # 得到余额转成float类型
    res = session.query(Shop).filter(and_(Shop.cabinet_num == id, Shop.grid_num == num)).all()
    # 查找对应的商品柜 SELECT * FROM shops WHERE cabinet_num=id and grid_num=num
    state = res[0].state # 得到商品柜状态，也就是售卖人的openID
    price = float(res[0].price) # 得到价格，并转成float类型
    if balance < price:  # 余额比价格少，返回余额不足
        return False, "余额不足"
    else:
        try:
            after = balance - price # 得到购买后余额
            session.query(User).filter(User.open_id == open_id).update({"balance": after})
            # 更新余额  UPDATE users SET balance=after WHERE open_id=open_id
            session.add(Bill(user=open_id, to=state, act="buy", before=balance, after=after, change=price))
            # 添加一条账单记录 INSERT INTO bills (user,to,act,before,after,change)VALUES(open_id,state,'buy',balance,after,price)
            res = session.query(User.balance).filter(User.open_id == state).all()
            # 查找出售者的余额 SELECT balance FROM users WHERE open_id = state
            balance = float(res[0][0]) # 余额转成float类型
            after = balance + price # 得到售出后余额
            session.query(User).filter(User.open_id == state).update({"balance": after})
            # 更新余额  UPDATE users SET balance=after WHERE open_id=state
            session.add(Bill(user=state, to=open_id, act="sell", before=balance, after=after, change=price))
            # 添加一条账单记录 INSERT INTO bills (user,to,act,before,after,change)VALUES(state,open_id,'sell',balance,after,price)
            session.query(Shop).filter(and_(Shop.cabinet_num == id, Shop.grid_num == num)).update({"state":"", "price":None})
            # 更新商品柜数据为空闲 UPDATE shops SET state='' and price=NULL WHERE cabinet_num=id and grid_num=num
            session.commit()
            return True,""
        except Exception as e:
            print(e)
            return False,"购买失败"
