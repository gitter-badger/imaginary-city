import dateutil.parser
import yaml

def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value)


class BlogpostHandler:
    inst = None
    def __init__(self):
        BlogpostHandler.inst = self
        with open("../database/blog.yaml") as f:            
            self.blogpost_list = yaml.load(f.read())

    def list(self):
        return self.blogpost_list

    def get(self, filepath):
        with open("../frontend/blog/" + filepath + "/README.md") as f:
            return f.read()
