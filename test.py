from transpile import Transpile, File, Method
from transpile import translate as _


class Method2(Method):

    def get_translator(self):
        return [
            _("with").join("open", callable=True, args=("a.txt", "w")).join(
                "as").join("inf:", verb=True),
            _("inf.write", callable=True, args=("abc"), indent=4),
            _("inf.flush", callable=True, indent=4)
        ]


class TestAbc(Method):

    def get_translator(self):
        return [
            _("p = subprocess.Popen", callable=True,
              args=("ipmitool raw 0x01",),
              kwargs=dict(shell=True)),
            _("p.wait()", verb=True),
            _("if").join("p == 0:", verb=True),
            _("print", indent=4).join("success", raw=True),
            _("else:", verb=True),
            _("print", indent=4).join("fail", raw=True)
        ]

snippet = Transpile().render_class(
    classname="MyClass", superclass="object", methods=[
        # {"name": "method1", "lines": [
        #     _("print").join("Hello,world!", raw=True)
        # ]},
        Method2(),
        TestAbc(),
    ]
)
['and', 'as', 'assert', 'break', 'class', 'continue',
 'def', 'del', 'elif', 'else', 'except', 'exec',
 'finally', 'for', 'from', 'global', 'if', 'import',
 'in', 'is', 'lambda', 'not', 'or', 'pass',
 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']

File(snippet).save("snippet_1.py")
