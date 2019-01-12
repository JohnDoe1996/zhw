import tornado.options
from tornado.options import define, options

from ws import WsHandler
from wxLogin import LoginHandler
from user import UserHandler
from shop import ShopHandler
from bill import BillHandler


define("port", default=8001, type=int) # 定义服务器端口为8001



if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 设置URL路由
    app = tornado.web.Application([
            (r"/ws/(.*)/(.*)", WsHandler),
            (r"/wx_login", LoginHandler),
            (r"/user/(.*)", UserHandler),
            (r"/shop/(.*)", ShopHandler),
            (r"/bill/(.*)", BillHandler)
        ],
        debug=True  # 开启调试模式
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port) # 监听端口
    print("server running...")
    tornado.ioloop.IOLoop.current().start() # 开启服务器