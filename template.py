from jinja2 import Environment, FileSystemLoader

class JinjaLoader(object):
    def __init__(self, template_path):
        self.template_path = template_path
        self.jinja_env = None
        self.template = None

    def generate(self, **context):
        if self.template is None:
            return
        template = self.template
        self.template = None
        return template.render(context)

    def load(self, template_name):
        if self.jinja_env is None:
            jinja_env = Environment(
                loader=FileSystemLoader(self.template_path),
                trim_blocks=True,
                extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"]
                )
            self.jinja_env = jinja_env
        else:
            jinja_env = self.jinja_env
        return jinja_env.get_template(template_name)

    def render(self, template_name, **context):
        return self.load(template_name).render(**context)
