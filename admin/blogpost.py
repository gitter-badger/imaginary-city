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
        with open("../database/blog.yaml", encoding="utf-8") as f:
            self.blogpost_list = yaml.load(f.read())

    def pushList(self):
        with open("../database/blog.yaml", "w") as f:
            yaml.dump(self.blogpost_list, f, default_flow_style=False, allow_unicode=True)

    def pushPage(self):
        
        page = open("../frontend/page/1.html", "w", encoding="utf-8")
        fullblogpost_list = []

        for blogpost in sorted(self.blogpost_list, key=lambda x : x["datetime"], reverse=True):
            
            bp = blogpost.copy()

            dt = blogpost["datetime"]
            bp['folder'] = "%04d/%02d/%02d/%s" % (dt.year, dt.month, dt.day, blogpost["filename"])

            with open("../frontend/blog/%s/README.md" % (bp['folder'],), encoding="utf-8") as md:
                preview_content = ""
                get_line = 0
                new_line = False
                for line in md:
                    if line[0] == '#': continue
                    if line == '\n':
                        if not new_line and preview_content:
                            preview_content += "<br>"
                            new_line = True
                        continue

                    new_line = False
                    get_line += 1
                    if get_line > 3: break
                    preview_content += line
                
                bp["content"] = preview_content
            
            fullblogpost_list.append(bp)

        import tornado.template
        loader = tornado.template.Loader("./front_templ")
        cont = loader.load("page.html").generate(
            blogpost_list = fullblogpost_list
        )
        page.write(cont.decode('utf-8'))
        page.close()
        

    def list(self):
        return self.blogpost_list

    def _getBlogpost(self, filepath):
        for blogpost in self.blogpost_list:
            dt = blogpost["datetime"]
            part = filepath.split("/")
            if blogpost["filename"] == part[3] and dt.year == int(part[0]) and dt.month == int(part[1]) and dt.day == int(part[2]) :
                return blogpost

        return None

    def get(self, filepath):
        blogpost = self._getBlogpost(filepath).copy()

        with open("../frontend/blog/" + filepath + "/README.md") as f:
            blogpost["md"] = f.read()
        
        return blogpost

    def updatePostMD(self, filepath, md):
        with open("../frontend/blog/" + filepath + "/README.md", "w") as f:
            f.write(md)

    def updatePostTitle(self, filepath, title):
        blogpost = self._getBlogpost(filepath)
        blogpost["title"] = title
        self.pushList()

    def createPost(self, filepath):
        os.makedirs("../frontend/blog/" + filepath + "/", exist_ok = True)
        with open("../frontend/blog/" + filepath + "/README.md", "w") as f:
            f.write("# NoTitle")

        part = filepath.split("/")

        blogpost = {
            "filename" : part[3],
            "title" : part[3],
            "datetime" : datetime.datetime(int(part[0]), int(part[1]), int(part[2]), 8, 0)
        }
        self.blogpost_list.append(blogpost)
        self.pushList()

        return None, blogpost

    def deletePost(self, filepath):
        blogpost = self._getBlogpost(filepath)
        self.blogpost_list.remove(blogpost)
        shutil.rmtree("../frontend/blog/" + filepath)
        self.pushList()
