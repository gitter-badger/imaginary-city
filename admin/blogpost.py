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

    def pushPage(self):
        page = open("../frontend/page/1.html", "w")
        for blogpost in self.blogpost_list:
            dt = blogpost["datetime"]
            folder = "%04d/%02d/%02d/%s" % (dt.year, dt.month, dt.day, blogpost["filename"])

            page.write(
                (
                    '<a href="#/blog/%s"><h2>%s</h2></a>\n'
                )
                %
                (folder, blogpost["title"])
            )

            with open("../frontend/blog/%s/README.md" % (folder,)) as md:
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

                if preview_content:
                    page.write(preview_content + "...\n")
                else:
                    page.write("[無內容]\n")

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
        blogpost = self._getBlogpost(filepath)

        with open("../frontend/blog/" + filepath + "/README.md") as f:
            blogpost["md"] = f.read()
        
        return blogpost

    def updatePostMD(self, filepath, md):
        with open("../frontend/blog/" + filepath + "/README.md", "w") as f:
            f.write(md)

    def updatePostTitle(self, filepath, title):
        for blogpost in self.blogpost_list:
            dt = blogpost["datetime"]
            part = filepath.split("/")
            if blogpost["filename"] == part[3] and dt.year == int(part[0]) and dt.month == int(part[1]) and dt.day == int(part[2]) :
                blogpost["title"] = title
                break

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
        for blogpost in self.blogpost_list:
            dt = blogpost["datetime"]
            part = filepath.split("/")
            if blogpost["filename"] == part[3] and dt.year == int(part[0]) and dt.month == int(part[1]) and dt.day == int(part[2]) :
                self.blogpost_list.remove(blogpost)
                break
        shutil.rmtree("../frontend/blog/" + filepath)
        self.pushList()
