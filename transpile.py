from template import JinjaLoader
from config import templates_dir
from util import hump2underline
import keyword


class InvalidKeyword(Exception):
    pass


class Method(object):

    @property
    def name(self):
        return hump2underline(self.__class__.__name__)

    def get_translator(self):
        raise NotImplementedError()

    @property
    def lines(self):
        return [trans.get_result() for trans in self.get_translator()]


def translate(s, verb=False, raw=False, callable=False, args=None, kwargs=None):
    t = Translator(s)
    if raw is True:
        t.set_result(s, quote=True)
    elif verb is True:
        t.set_result(s)
    elif callable is True:
        """ callable """
        t.p_args = args
        t.k_args = kwargs
    else:
        if not keyword.iskeyword(s):
            raise InvalidKeyword(s)
        t.set_result(s)
    return t


class Translator(object):
    def __init__(self, s=None):
        self.s = s
        self._quoted = self.quote(s)
        self._result = None
        self._joins = []
        self.p_args = None
        self.k_args = None
        self.offset = ""

    def indent(self, width=4):
        if self._result is None:
            self.offset = chr(32) * width
        else:
            self._result = chr(32) * width + self._result
        return self
        
    def get_result(self):
        self._translate()
        text_spans = [self._result] + [j.get_result() for j in self._joins]
        return " ".join(text_spans)

    def set_result(self, text, quote=False):
        self._result = self.quote(text) if quote else text

    def join(self, *args, **kwargs):
        self._joins.append(translate(*args, **kwargs))
        return self

    def _translate(self):
        if self._result is None and \
                not keyword.iskeyword(self.s):
            apd = ["%s" % self.quote(p) for p in self.p_args or []]
            apd += ["%s=%s" % (k, self.quote(v))
                    for k, v in (self.k_args or {}).items()]
            self._result = self.offset + "%s(%s)" % (self.s, ', '.join(apd))
        return self

    def quote(self, s):
        if not s:
            return ''
        if isinstance(s, basestring):
            return '"%s"' % s.strip()
        return str(s)

    # def __getattr__(self, attr):
    #     if attr.startswith("as"):
    #         _, symbol = attr.split("_")
    #         def fn(*args, **kwargs):
    #             return self.as_(symbol, *args, **kwargs)
    #         return fn
    #     return getattr(self, attr)


class Transpile(object):

    def __init__(self):
        self.jinja = JinjaLoader(templates_dir)

    def _render_snippet(self, template, **context):
        return self.jinja.render(template, **context)

    def render_class(self, **context):
        return self._render_snippet("class.j2", **context)


class File(object):
    def __init__(self, content):
        self.content = content

    def save(self, savefp):
        with open(savefp, "w") as outf:
            outf.write(self.content)
            outf.flush()
