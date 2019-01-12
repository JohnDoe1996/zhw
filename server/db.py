import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

# mysql 相关设置
engine = create_engine('mysql+pymysql://root:@localhost/zhw?charset=utf8', convert_unicode=True, encoding='utf-8') # 连接数据库，使用账号 zhw 密码zhw
conn = engine.connect()

Base = declarative_base()

class User(Base): # User模型
    __tablename__ = "users" # 表名
    open_id = Column(String(32),primary_key=True, unique=True)  # 属性open_id，主键
    create_at = Column(DateTime, default=datetime.datetime.now) # 创建时间
    balance = Column(Numeric(10,2), nullable=False, default="0") # 余额

class Shop(Base): # Shop模型
    __tablename__ = "shops"
    cabinet_num = Column(String(32),primary_key=True,nullable=False) # 机器ID，主键
    grid_num = Column(String(32),primary_key=True,nullable=False)   # 每格ID，主键
    state = Column(String(64)) # 当前状态
    price = Column(Numeric(10,2)) # 价格

class Bill(Base): # Bill模型
    __tablename__ = "bills"
    id = Column(Integer,primary_key=True,autoincrement=True) #id，主键
    user = Column(String(32),nullable=False) # 操作的用户
    to = Column(String(32),nullable=False) # 操作对象
    act = Column(String(16),nullable=False) # 操作内容
    act_at = Column(DateTime,default=datetime.datetime.now) # 操作时间
    before = Column(Numeric(10,2), nullable=False) # 操作前余额
    after = Column(Numeric(10,2), nullable=False) # 操作后余额
    change = Column(Numeric(10,2), nullable=False) # 余额变化值

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

