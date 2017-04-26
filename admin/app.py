import tornado.ioloop
import tornado.web

import os
import json
import datetime

from blogpost import BlogpostHandler


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


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
        method = self.get_argument("method")
        print(filepath)

        if method == "getPost":
            self.finish(BlogpostHandler.inst.get(filepath))
        elif method == "updatePost":
            md = self.get_argument("md", default="")
            BlogpostHandler.inst.updatePost(filepath, md)
        elif method == "createPost":
            err, blogpost = BlogpostHandler.inst.createPost(filepath)
            self.finish(err or json.dumps(blogpost, cls=DateTimeEncoder))


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
