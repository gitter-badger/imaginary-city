import tornado.ioloop
import tornado.web

import os
import json
import datetime

from blogpost import BlogpostHandler
from image import ImageHandler


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class RequestHandler(tornado.web.RequestHandler):
    pass


class BlogServer(RequestHandler):
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

        if method == "getPost":
            self.finish(json.dumps(BlogpostHandler.inst.get(filepath), cls=DateTimeEncoder))
        elif method == "pushPage":
            BlogpostHandler.inst.pushPage()
        elif method == "updatePost":
            md = self.get_argument("md", default=None)
            title = self.get_argument("title", default=None)

            if md is not None :
                BlogpostHandler.inst.updatePostMD(filepath, md)

            if title is not None :
                BlogpostHandler.inst.updatePostTitle(filepath, title)

        elif method == "createPost":
            err, blogpost = BlogpostHandler.inst.createPost(filepath)
            self.finish(err or json.dumps(blogpost, cls=DateTimeEncoder))
        elif method == "deletePost":
            BlogpostHandler.inst.deletePost(filepath)


class ImageServer(RequestHandler):
    def post(self, filepath):
        method = self.get_argument("method")

        if method == "listImage":
            image_list = ImageHandler.inst.listImage(filepath) 
            self.finish(json.dumps(image_list))


_settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "template_path" : os.path.join(os.path.dirname(__file__), "templ"),
    "autoreload" : True,
    "debug" : True 
}


application = tornado.web.Application([
    (r"/blog/(.*)", BlogServer),
    (r"/image/(.*)", ImageServer),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static/"}),
    (r'/blogdb/(.*)', tornado.web.StaticFileHandler, {'path': "../frontend/blog/"}),
], **_settings) 


if __name__ == "__main__":
    application.listen(8888)
    BlogpostHandler()
    ImageHandler()
    tornado.ioloop.IOLoop.current().start()
