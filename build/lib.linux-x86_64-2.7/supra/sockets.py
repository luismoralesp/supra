import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary.
clients = dict()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
    #end def

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        msg = "Client %s received a message : %s" % (self.id, message)
        self.write_message(msg)
        print msg
    #end def
        
    def on_close(self):
        if self.id in clients:
            del clients[self.id]
        #end if
    #end def
#end class

app = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()