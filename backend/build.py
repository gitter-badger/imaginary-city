import dateutil.parser
import yaml

def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value)

yaml.add_constructor(u'tag:yaml.org,2002:timestamp', timestamp_constructor)

with open("../database/blog.yaml") as f:
    blog = yaml.load(f.read())

blog.sort(key=lambda x : x["datetime"], reverse=True)
print(blog)


with open("../frontend/page/1.html", "w") as page:
    for blogpost in blog:
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
