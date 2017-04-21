import tornado.ioloop
import tornado.web

import os

class RequestHandler(tornado.web.RequestHandler):
    pass

class MainHandler(RequestHandler):
    def get(self):
        self.render("blogpost_list.html")


_settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templ"),
    "autoreload" : True,
    "debug" : True 
}


application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static/"}),
], **_settings) 


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
