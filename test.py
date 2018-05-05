from jinja2 import Template
import os

curdir = os.path.dirname(__file__)

with open(os.path.join(curdir, "templates/class.j2")) as inf:
    template = Template(inf.read())

print template.render(classname="MyClass", superclass="father", methods=[
        {"name": "method1", "lines": ["print \"hello,world!\""]},
        {"name": "method2", "lines": ["print \"hello,world!\"", "line1", "line3"]},

    ])