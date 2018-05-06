from transpile import Transpile, File, Snippet
from transpile import translate as _
from transpile.template import PyClassRender


class Method2(Snippet):

    def get_translator(self):
        return [
            _('"""'),
            _("hello, I am doc 1."),
            _("hello, I am doc 2."),
            _("hello, I am doc 3."),
            _('"""'),
            _("with open", args=("a.txt", "w")).join("as inf:"),
            _("inf.write", args=("abc")).indent(),
            _("inf.flush()").indent()
        ]


class TestAbc(Snippet):

    def get_ipmi_cmd(self, args):
        return [
            _("p = subprocess.Popen",
              args=("ipmitool %s" % args,),
              kwargs=dict(shell=True)),
            _("p.wait()"),
            _("if p.returncode == 0:"),
            _("ret &= True").indent(),
            _("else:"),
            _("ret &= False").indent(),
        ]
    def get_translator(self):
        trans = [
            _("ret = True"),
        ]
        for arg in ["raw 0x01",  "raw 0x02", "raw 0x03"]:
            trans.extend(self.get_ipmi_cmd(arg))
        trans.append(_("return ret"))
        return trans



class Method1(Snippet):
    def get_translator(self):
        return [
            _("print 'Hello, world!'")
        ]

class Main(Snippet):
    def get_translator(self):
        return [
            _("unittest.main()")
        ]

class Imports(Snippet):
    def get_translator(self):
        return [
            "import unittest",
            "import subprocess"
        ]

snippet = Transpile().render_python(
    imports=Imports(),
    class_renders=[
        PyClassRender("TestCase_1", [Method1(), Method2(), TestAbc()], "unittest.TestCase"),
        PyClassRender("TestCase_2", [TestAbc()], "unittest.TestCase"),
        PyClassRender("TestCase_3", [Method1(), TestAbc()], "unittest.TestCase"),
    ],
    main=Main()
)
print Transpile([
    _("from flask import Flask"),
    _("app = Flask(__name__)"),
    _(),
    _("@app.route", args=("/",)),
    _("def index():"),
    _("return").join("Hello, world!", quote=True).indent()
    ]).get_result()


File(snippet).save("snippet_1.py")
