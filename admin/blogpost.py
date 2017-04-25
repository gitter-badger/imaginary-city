import dateutil.parser
import yaml
import os
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

        self.blogpost_list.append({
            "filename" : filepath.split("/")[-1],
            "title" : "Notitle",
            "datetime" : datetime.datetime.now() 
        })

        self.pushList()
