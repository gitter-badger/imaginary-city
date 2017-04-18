import dateutil.parser
import yaml

def timestamp_constructor(loader, node):
    return dateutil.parser.parse(node.value)

yaml.add_constructor(u'tag:yaml.org,2002:timestamp', timestamp_constructor)

with open("../database/blog.yaml") as f:
    blog = yaml.load(f.read())

print(blog)

with open("../frontend/page/1.html", "w") as page:
    for blogpost in blog:
        dt = blogpost["datetime"]
        page.write(
            '<a href="#/blog/%04d/%02d/%02d/%s">%s</a><br>\n'
            %
            (dt.year, dt.month, dt.day, blogpost["filename"], blogpost["title"])
        )
