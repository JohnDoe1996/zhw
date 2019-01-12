from websocket import create_connection
import serial
import json
try:
    import thread
except:
    import _thread as thread


WS_URL = "ws://193.112.217.173:8001/ws/shop/" # websocket服务器URL并指明是shop
ID = "00001" # 机器ID

UART_PATH = "/dev/ttyUSB0"  # 串口文件
BPS = "115200" # 波特率

ser = serial.Serial(UART_PATH, BPS) # 连接串口
ws = create_connection(WS_URL + ID) # 连接服务器


def wsThread(): # websocket接收线程函数
    while True:  # 死循环
        quote = ws.recv()  # 接收到数据保存找变量中
        print(quote)
        wsData = json.loads(quote) # json数据转成字典
        if str(wsData['id']) == ID and wsData['host'] == "zhw" and wsData['act'] == "unlock": # 判断数据是否为本机是否为开箱
            num = int(wsData['num']) # 得到要打开的柜子
            data = [0xcf,0x03,0x10,num,0x01, 0xfc] # 拼接好打开箱子的协议
            dt = bytes(data) # 转成byte类型
            print(dt)
            ser.write(dt) # 发送到串口


def uartThread(): # 串口接收线程函数
    uart_data = []
    while True:
        while ser.inWaiting() > 0: #串口接收到数据
            print("uart:")
            d = ser.read(1)  # 获取一个数据
            print(d)
            if d == bytes([0xcf]):  # 判断第一位是否符合协议，协议第一位 0xcf
                d = ser.read(1) # 获取第二位
                print(d)
                if d == bytes([0x3]): # 同上，协议第二位 0x03
                    i = 0
                    while i < 3: # 循环接收中间3个数据
                        i += 1
                        r = ser.read(1)  # 读数据
                        print(r)
                        uart_data.append(ord(r)) # 数据插入到列表中
                    c = ser.read(1)  # 再读取一位数据
                    print(c)
                    if c != bytes([0xfc]):  # 判断协议结束 最后一位 0xfc
                        uart_data.clear() # 结束位不正确便清空数组
                        continue
                    else:
                        print(uart_data)
                        classify(uart_data) # 调用3位有效数据去分类
                        uart_data.clear() # 数据复位

def classify(data): # 数据分类处理函数
    print(data)
    if data[0] == 0x00: # 系统启用
        print("system start")
    elif data[0] == 0x10: # 控制信号
        print("control signal")
    elif data[0] == 0x11: # 节点加入
        print("IN: id:" + str(data[1]))
    elif data[0] == 0x21: # 节点离开
        print("OUT: id" + str(data[1]))
    elif data[0] == 0x20: # 开锁反馈
        print("success control")
        wsData = {
            'host': "zhw",
            'act': "back",
            'id': ID,
            'num': data[1],
            'state': data[2]
        }
        ws.send(json.dumps(wsData)) # 数据发送到websocket
    else:
        print("unknown signal")


if __name__ == '__main__':
    try:
        thread.start_new_thread(wsThread, ()) # 创建websocket接收线程
        thread.start_new_thread(uartThread, ()) # 创建串口接收线程
    except Exception as e:
        print(e)
        exit(1)
    print("running...  Ctrl+C to exit.")
    while True:
        pass