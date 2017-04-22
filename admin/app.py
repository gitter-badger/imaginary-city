import tornado.ioloop
import tornado.web

import os
import json

from blogpost import BlogpostHandler

class RequestHandler(tornado.web.RequestHandler):
    pass


class BlogHandler(RequestHandler):
    def get(self, filepath):
        if not filepath:
            self.render("blogpost_list.html",
                blogpost_list = BlogpostHandler.inst.list()
            )
        else:
            self.render("blogpost.html",
                filepath = filepath
            )

    def post(self, filepath):
        self.finish(BlogpostHandler.inst.get(filepath))


_settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templ"),
    "autoreload" : True,
    "debug" : True 
}


application = tornado.web.Application([
    (r"/blog/(.*)", BlogHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static/"}),
    (r'/blogdb/(.*)', tornado.web.StaticFileHandler, {'path': "../frontend/blog/"}),
], **_settings) 


if __name__ == "__main__":
    application.listen(8888)
    BlogpostHandler()
    tornado.ioloop.IOLoop.current().start()
