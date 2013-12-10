import os

try:
    import jinja2

    loader = jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates'))
    env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
except ImportError:
    env = None

from dokus.document import extract_classes

def render(functions, template=None):
    if template == None or isinstance(template, str):
        if env == None:
            raise ValueError('jinja2 required to using default templates')
        else:
            if template == None:
                template = 'default'

            template = env.get_template(template + '/base.html')

    classes, functions = extract_classes(functions)

    data = {
        'classes': [v.format() for v in classes],
        'functions': [v.format() for v in functions]
    }

    return template.render(data)