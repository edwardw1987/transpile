from transpile import Transpile, File, Method
from transpile import translate as _


class Method2(Method):

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


class TestAbc(Method):

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



class Method1(Method):
    def get_translator(self):
        return [
            _("print 'Hello, world!'")
        ]

snippet = Transpile().render_class(
    classname="MyClass", superclass="object", methods=[
        Method1(),
        Method2(),
        TestAbc(),
    ]
)

File(snippet).save("snippet_1.py")
