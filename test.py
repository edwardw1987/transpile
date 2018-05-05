from template import JinjaLoader
from config import templates_dir
import keyword


class Echo(object):
    def __init__(self, s=None):
        self.s = s
        self._escaped = self._escape(s)
        self._text = None
        self._joins = []

    def has_indent(self, text):
        return text[:4] == chr(32) * 4

    def get_text(self):
        text_spans = [self._text] + [j.get_text() for j in self._joins]
        return " ".join(text_spans)

    def join(self, echo):
        self._joins.append(echo)
        return self

    def join_many(self, echo_list):
        self._joins.extend(echo)
        return self

    def as_(self, symbol, *args, **kwargs):
        indent = kwargs.pop("indent", 0)
        if symbol == "raw":
            self._text = chr(32) * indent + self._escaped
        else:
            if keyword.iskeyword(symbol):
                fmt = '%s %s' 
                if symbol == "as":
                    self._escaped += '%s:' % str(args[0]) if args else ''
            else:
                fmt = "%s(%s)"
                if symbol == "open":
                    self._escaped += ", %s" % self._escape(args[0] if args else '')
                    
            self._text = chr(32) * indent + fmt % (symbol, self._escaped.strip())
            if symbol == "with":
                print repr(self._text)
        return self

    def _escape(self, s):
        if not s:
            return ''
        if isinstance(s, basestring):
            return '"%s"' % s.strip()
        return str(s)

    def __getattr__(self, attr):
        if attr.startswith("as"):
            _, symbol = attr.split("_")
            def fn(*args, **kwargs):
                return self.as_(symbol, *args, **kwargs)
            return fn

_ = Echo

class Transpile(object):

    def __init__(self):
        self.jinja = JinjaLoader(templates_dir)

    def _render_snippet(self, template, **context):
        for method in context.get("methods", []):
            repl = []
            for line in method.get("lines", []):
                text = line.get_text() if isinstance(line, Echo) else line
                repl.append(text)
            method["lines"] = repl
        return self.jinja.render(template, **context)

    def render_class(self, **context):
        return self._render_snippet("class.j2", **context)

class File(object):
    def __init__(self, content):
        self.content =  content

    def save(self, savefp):
        with open(savefp, "w") as outf:
            outf.write(self.content)
            outf.flush()

if __name__ == '__main__':
    
    snippet = Transpile().render_class(
        classname="MyClass", superclass="object", methods=[
                {"name": "method1", "lines": [_("Hello,world!").as_print()]},
                {"name": "method2", "lines": [
                    _().as_with(indent=4).join(
                        _("abc.txt").as_open('w')
                        ).join(_().as_as("outf")),

                   #  _("hello,world!").as_raw(),
                   #  _("line1").as_raw(indent=4),
                    
                   # _("line3").as_return().join(_("line4").as_and()),
                    ]},

            ]
        )
    ['and', 'as', 'assert', 'break', 'class', 'continue',
     'def', 'del', 'elif', 'else', 'except', 'exec',
     'finally', 'for', 'from', 'global', 'if', 'import',
     'in', 'is', 'lambda', 'not', 'or', 'pass',
     'print', 'raise', 'return', 'try', 'while', 'with', 'yield']

    File(snippet).save("snippet_1.py")