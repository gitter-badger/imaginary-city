import dateutil.parser
import yaml
import os
import shutil
import datetime

def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value)


class BlogpostHandler:
    inst = None
    def __init__(self):
        BlogpostHandler.inst = self
        self.pullList()

    def pullList(self):
        with open("../database/blog.yaml") as f:            
            self.blogpost_list = yaml.load(f.read())

    def pushList(self):
        with open("../database/blog.yaml", "w") as f:
            yaml.dump(self.blogpost_list, f, default_flow_style=False)

    def list(self):
        return self.blogpost_list

    def get(self, filepath):
        with open("../frontend/blog/" + filepath + "/README.md") as f:
            return f.read()

    def updatePost(self, filepath, md):
        with open("../frontend/blog/" + filepath + "/README.md", "w") as f:
            f.write(md)

    def createPost(self, filepath):
        os.makedirs("../frontend/blog/" + filepath + "/", exist_ok = True)
        with open("../frontend/blog/" + filepath + "/README.md", "w") as f:
            f.write("# NoTitle")

        blogpost = {
            "filename" : filepath.split("/")[-1],
            "title" : filepath.split("/")[-1],
            "datetime" : datetime.datetime.now()
        }
        self.blogpost_list.append(blogpost)
        self.pushList()

        return None, blogpost

    def deletePost(self, filepath):
        for blogpost in self.blogpost_list:
            dt = blogpost["datetime"]
            part = filepath.split("/")
            if blogpost["filename"] == part[-1] and dt.year == int(part[0]) and dt.month == int(part[1]) and dt.day == int(part[2]) :
                self.blogpost_list.remove(blogpost)
                break
        shutil.rmtree("../frontend/blog/" + filepath)
        self.pushList()
